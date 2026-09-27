.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _quic_transport_interface:

QUIC 传输接口
#############

.. contents::
    :local:
    :depth: 2

概述
****

QUIC 是一种通用多路复用传输协议，已在 :rfc:`9000` 中标准化。它运行在 UDP 之上，提供有序、可靠的字节流传输，并集成了 TLS 1.3 安全性（:rfc:`9001`）、流多路复用和连接迁移。Zephyr 的 QUIC 实现可通过 :kconfig:option:`CONFIG_QUIC` 启用。

与嵌入式使用相关的关键特性：

* **流多路复用**：双向和单向流共享同一个 UDP socket，从而避免传输层的队头阻塞。
* **集成 TLS 1.3**：握手内置于连接建立过程；无需单独的 TLS 层。
* **流量控制**：基于信用的每流与每连接流量控制可防止快速发送方压垮资源受限的接收方。
* **丢失恢复**：探测超时（PTO，Probe Timeout）机制会重传数据，而无需依赖 ICMP 或 TCP 风格的 ACK 时钟。
* **路径 MTU 发现**：数据报分组化层 PMTU 发现（DPLPMTUD，:rfc:`9000` 第 14.3 节）在握手后探测路径，并且只有在探测得到确认后才提高发送大小。
* **Socket 集成**：使用标准 Zephyr socket 调用（如 ``zsock_send``、``zsock_recv``、``zsock_recvmsg``、``zsock_sendmsg``、``zsock_close``）进行数据传输。
* **双协议栈**：同时支持 IPv4 和 IPv6 连接。

.. note::

   QUIC 支持目前在 Zephyr 中处于 **实验性** 状态。使用 ``CONFIG_QUIC=y`` 启用它，并注意 API 和 Kconfig 选项可能会在版本之间发生变化。


架构与概念
**********

要有效使用该库，理解 **连接** 与 **流** 之间的关系会很有帮助。

* **QUIC 连接 socket**：表示到对端的“隧道”。它处理 TLS 握手、拥塞控制和连接终止。通常不直接通过此 socket 发送应用数据，而是用它来创建流。
* **QUIC 流 socket**：表示连接内部的轻量级数据通道。实际的应用数据（``send`` 或 ``recv``）在此流动。


应用工作流
**********

以下各节介绍如何使用该库编写通用的客户端和服务器应用。

客户端应用
----------

客户端发起与远程服务器的连接，打开一个流，发送请求并读取响应。

**第 1 步：设置地址**

.. code-block:: c

   struct net_sockaddr_in remote_addr = {
       .sin_family = NET_AF_INET,
       .sin_port = net_htons(4422),
   };

   zsock_inet_pton(NET_AF_INET, "192.0.2.1", &remote_addr.sin_addr);


**第 2 步：打开 QUIC 连接**

.. code-block:: c

   int conn_sock = quic_connection_open((struct net_sockaddr *)&remote_addr, NULL);
   if (conn_sock < 0) {
       /* Handle error */
   }

   /* The TLS handshake occurs automatically upon the first stream creation. */


**第 3 步：打开流**

.. code-block:: c

   /* Create a bidirectional stream initiated by the client */
   int stream_sock = quic_stream_open(conn_sock,
                                      QUIC_STREAM_CLIENT,
                                      QUIC_STREAM_BIDIRECTIONAL,
                                      0);


**第 4 步：传输数据**

在 **流 socket** 上使用标准 socket 调用，而不是连接 socket。

.. code-block:: c

   zsock_send(stream_sock, "Hello Server", 12, 0);

   char buffer[64];
   zsock_recv(stream_sock, buffer, sizeof(buffer), 0);


**第 5 步：清理**

.. code-block:: c

   quic_stream_close(stream_sock);
   quic_connection_close(conn_sock);


服务器应用
----------

服务器绑定到本地端口，等待传入连接，接受流并处理数据。

**第 1 步：绑定连接 socket**

.. code-block:: c

   struct net_sockaddr_in local_addr = {
      .sin_family = NET_AF_INET,
      .sin_port = net_htons(4422),
      .sin_addr.s_addr = NET_INADDR_ANY,
   };

   /* Create the listening context */
   int conn_sock = quic_connection_open(NULL, (struct net_sockaddr *)&local_addr);


**第 2 步：接受传入流**

:c:func:`quic_connection_open` socket 充当“父级”。在 **连接 socket** 上使用 :c:func:`zsock_accept()` 获取对端发起的新流的文件描述符。

.. code-block:: c

   struct net_sockaddr_in peer_addr;
   net_socklen_t addrlen = sizeof(peer_addr);

   /* Block until a client opens a stream */
   int stream_sock = zsock_accept(conn_sock, (struct net_sockaddr *)&peer_addr, &addrlen);

   if (stream_sock >= 0) {
       /* Handle the new stream (read/write data) */
       char buf[128];
       int len = zsock_recv(stream_sock, buf, sizeof(buf), 0);

       /* Echo back */
       zsock_send(stream_sock, buf, len, 0);

       /* Close the stream when done, also zsock_close() can be used */
       quic_stream_close(stream_sock);
   }


TLS 与安全配置
**************

QUIC 传输使用 Mbed TLS 和 PSA API 执行加密操作。安全凭证（证书、密钥）通过 Zephyr 的 **TLS Credentials** 子系统管理。

管理证书
--------

在打开连接之前，必须使用 :c:func:`tls_credential_add` 注册证书。

1. **CA 证书**：客户端验证服务器所必需。
2. **服务器证书和私钥**：服务器所必需。

**示例：加载凭证**

.. code-block:: c

   #include <zephyr/net/tls_credentials.h>

   /* Tag ID to reference credentials later */
   #define MY_SEC_TAG 1

   static const char server_cert[] = ...; /* PEM or DER data */
   static const char priv_key[] = ...;    /* PEM or DER data */

   void setup_credentials(void) {
       tls_credential_add(MY_SEC_TAG, TLS_CREDENTIAL_PUBLIC_CERTIFICATE,
                          server_cert, sizeof(server_cert));
       tls_credential_add(MY_SEC_TAG, TLS_CREDENTIAL_PRIVATE_KEY,
                          priv_key, sizeof(priv_key));
   }


将凭证应用到 QUIC
-----------------

创建后应立即在 **连接 socket** 上使用 :c:func:`zsock_setsockopt` 将凭证应用到 QUIC socket。必须在创建流之前设置凭证。

对端证书验证遵循与 Zephyr TLS socket 相同的默认策略：客户端默认要求成功验证对端，而服务器默认不验证客户端证书，除非显式启用 ``ZSOCK_TLS_PEER_VERIFY``。因此，未加载 CA 证书的客户端默认会握手失败；有意跳过服务器身份验证的应用必须通过 ``ZSOCK_TLS_PEER_VERIFY = MBEDTLS_SSL_VERIFY_NONE`` 选择退出。

.. code-block:: c

   sec_tag_t sec_tag_list[] = { MY_SEC_TAG };

   zsock_setsockopt(conn_sock, ZSOCK_SOL_TLS, ZSOCK_TLS_SEC_TAG_LIST,
                    sec_tag_list, sizeof(sec_tag_list));


将 ALPN 应用到 QUIC
-------------------

应用层协议协商（ALPN，Application-Layer Protocol Negotiation）在 QUIC 中是必需的。ALPN 用于协商运行在两个 QUIC 端点之上的应用协议。创建后应立即在 **连接 socket** 上使用 :c:func:`zsock_setsockopt` 将 ALPN 列表应用到 QUIC socket。必须在创建流之前设置 ALPN 列表。注意，列表项必须是常量，不能是变量。

.. code-block:: c

   const char * const alpn_list[] = {
       "echo-quic",
       NULL
   };

   ret = zsock_setsockopt(quic_sock, ZSOCK_SOL_TLS, ZSOCK_TLS_ALPN_LIST,
                               alpn_list, sizeof(alpn_list));
   if (ret < 0) {
       LOG_ERR("Failed to set ALPN (%d)", -errno);
   }


.. _quic_session_resumption:

会话恢复与 0-RTT
****************

在完整握手后，服务器可能签发 TLS 1.3 的 *NewSessionTicket*。客户端可以存储生成的会话状态，并在后续连接中提交它以 **恢复** 会话而无需完整握手；而且在服务器允许时，还可以在握手完成之前，在首批数据包中发送 **0-RTT 早期数据**。

0-RTT 支持通过 :kconfig:option:`CONFIG_QUIC_0RTT` 编译进来（**默认禁用**）。1-RTT 的会话恢复无需该选项即可工作；启用它会增加早期数据的提供/接受/重放处理。

.. warning::

   0-RTT 早期数据可能被网络攻击者 **重放**，见 :rfc:`9001` 第 9.2 节。在 0-RTT 上只应发送用于幂等/可安全重放操作的数据，并做好对端拒绝它的准备（此时必须在握手完成后重试这些数据）。协议栈会使签发的票据变为一次性使用，并应用年龄新鲜度窗口，但这种防重放状态仅存在于内存中且仅限每个实例（重启后不会保留，也不在服务器实例之间共享）。

**客户端：导出并复用会话状态**

握手完成后，从连接 socket 读取可恢复状态并妥善保存。在新连接上，应在打开第一个流之前导入它。当 0-RTT 已就绪时，第一个流的数据会作为早期数据承载。

.. code-block:: c

   struct quic_session_state state;
   net_socklen_t optlen = sizeof(state);

   /* After the first connection's handshake completes: */
   zsock_getsockopt(conn_sock, ZSOCK_SOL_QUIC, ZSOCK_QUIC_SO_SESSION_STATE,
                    &state, &optlen);

   /* On a later connection, before the first stream is opened: */
   zsock_setsockopt(new_conn_sock, ZSOCK_SOL_QUIC, ZSOCK_QUIC_SO_SESSION_STATE,
                    &state, sizeof(state));

由于 ``struct quic_session_state`` 携带恢复密钥，应将其视为敏感信息并安全存储。其布局通过 ``QUIC_SESSION_STATE_VERSION`` 进行版本管理。

**服务器：签发票据并允许 0-RTT**

在握手之前，在监听（或服务器端连接）socket 上设置以下选项：

* ``ZSOCK_QUIC_SO_SESSION_TICKET_ENABLE`` (指向 ``int`` 的指针) —— 非零值会使服务器在握手后发送 NewSessionTicket，从而启用 1-RTT 恢复。
* ``ZSOCK_QUIC_SO_MAX_EARLY_DATA_SIZE`` (指向 ``uint32_t`` 的指针) —— 任何非零值都会为新签发的票据启用 0-RTT（并且需要 :kconfig:option:`CONFIG_QUIC_0RTT`，否则 ``setsockopt()`` 会以 ``ENOTSUP`` 失败）。根据 :rfc:`9001` 第 4.6.1 节，票据始终通告固定的 ``0xffffffff`` 哨兵值；客户端实际可发送的早期数据量受连接的流量控制（传输参数）限制约束，因此该选项是一个启用开关，而不是字节预算。

.. code-block:: c

   int enable = 1;
   uint32_t early_data = 1; /* non-zero enables 0-RTT for issued tickets */

   zsock_setsockopt(quic_sock, ZSOCK_SOL_QUIC, ZSOCK_QUIC_SO_SESSION_TICKET_ENABLE,
                    &enable, sizeof(enable));
   zsock_setsockopt(quic_sock, ZSOCK_SOL_QUIC, ZSOCK_QUIC_SO_MAX_EARLY_DATA_SIZE,
                    &early_data, sizeof(early_data));

**每流早期数据状态**

在服务器上，可在 **流** socket 上使用 ``ZSOCK_QUIC_SO_STREAM_EARLY_DATA`` (指向 ``int`` 的指针) 查询给定流是否承载了已接受的 0-RTT 数据。这使协议层能够应用重放保护（例如，HTTP/3 对非幂等的早期请求回复 ``425 Too Early``）。


.. _quic_dplpmtud:

路径 MTU 发现（DPLPMTUD）
*************************

Zephyr 的 QUIC 协议栈执行 **数据报分组化层路径 MTU 发现** (DPLPMTUD)，如 :rfc:`9000` 第 14.3 节所述。RFC 8899 的搜索状态位于通用的 :ref:`net_dplpmtud` 子系统中；QUIC 通过其恢复机制提供探测数据包（PING 加填充）、不分片 UDP 发送以及 ACK/丢失确认。

目标是找到在不进行 IP 层分片的情况下能够穿越路径的最大 UDP 载荷大小，然后将该大小用于应用数据包。

行为
----

TLS 握手完成后，协议栈可能会发送包含 PING 帧和填充的 **探测数据报**。探测数据报的大小会设置为尝试更大的路径 MTU，并在底层 UDP socket 上启用 **不分片** 后发送（请参见 :c:macro:`ZSOCK_IP_DONTFRAG` / :c:macro:`ZSOCK_IPV6_DONTFRAG`，详情见 :ref:`ip_socket_options`）。这由内部处理；应用无需配置 QUIC 使用的 UDP socket。

协议栈跟踪三个相关限制：

* **对端 ``max_udp_payload_size`` 传输参数** - 远程端点在握手期间通告的上限。
* **本地上限** - 由接口或 socket MTU 减去 IP 和 UDP 头部开销得出。
* **已验证的发送大小** - 由 ACK 确认的最大探测大小。它决定传出 QUIC 数据包可以有多大。

发送大小从 QUIC 要求的 **1200 字节最小 UDP 载荷** 开始。当已验证大小低于本地和对端上限时，协议栈会二分搜索更大的工作大小。探测 ACK 会提高已验证限制；反复探测丢失会缩小搜索范围。流帧的大小会调整为适应当前已验证限制，因此一旦探测成功，高 MTU 路径上的吞吐量会自动提高。

与丢失恢复的交互
----------------

DPLPMTUD 探测会触发 ACK，并参与与流数据相同的丢失恢复机制。在探测超时（PTO）时，**会优先重传在途流帧**；只有在没有流数据需要重传时才发送 DPLPMTUD 探测（即发送裸 PING 探测的相同情形）。

目前没有面向应用的 QUIC API 来启用、禁用或调整 DPLPMTUD。只要可能提供更大的路径 MTU，探测就会在握手完成后自动开始。实现自身 UDP 协议的传输层可以复用 :ref:`net_dplpmtud` 中记录的同一通用 API。


配置选项
********

下面的所有选项都位于 ``if QUIC`` 代码块内，并且仅在启用 :kconfig:option:`CONFIG_QUIC` 时可见。

连接和流数量
------------

.. list-table::
   :widths: 40 12 48
   :header-rows: 1

   * - 选项
     - 默认值
     - 描述
   * - :kconfig:option:`CONFIG_QUIC_MAX_CONTEXTS`
     - 1
     - 系统中同时存在的 QUIC 连接最大数量。每个上下文都携带自己的 TLS 状态、流量控制窗口和已发送数据包历史。内存消耗随该值线性增长。
   * - :kconfig:option:`CONFIG_QUIC_MAX_STREAMS_BIDI`
     - 3-5
     - 最大双向流数量（**每个连接**）。流在构建时分配；未使用的流槽仍会占用其 TX/RX 缓冲区分配。
   * - :kconfig:option:`CONFIG_QUIC_MAX_STREAMS_UNI`
     - 0
     - 每个连接的最大单向流数量。设置为 ``0`` 可完全禁用单向流并回收相关的缓冲区 RAM。
   * - :kconfig:option:`CONFIG_QUIC_MAX_ENDPOINTS`
     - 2-3
     - UDP 端点 socket 的数量。通过一种 IP 版本连接到单个服务器的客户端需要 2 个；双协议栈服务器角色需要 3 个。可考虑启用 :kconfig:option:`CONFIG_QUIC_ENDPOINT_USE_IPV4_MAPPING_TO_IPV6`，以便为 IPv4 和 IPv6 共享单个 socket。
   * - :kconfig:option:`CONFIG_QUIC_MAX_PEER_CIDS`
     - 4
     - 每个连接跟踪的对端 Connection ID 数量。如果不需要连接迁移，在资源非常受限的设备上可减少到 1。

QUIC 传输参数（流量控制）
-------------------------

这些值在握手期间通告给远程对端（参见 :rfc:`9000` 第 18.2 节）。它们决定在收到窗口更新之前 **允许对端发送** 多少数据。每个值都应与对应的本地接收缓冲区大小匹配；通告的窗口大于接收缓冲区会导致缓冲区溢出，而通告的窗口小于缓冲区则会未充分利用可用内存。

.. list-table::
   :widths: 44 12 44
   :header-rows: 1

   * - 选项
     - 默认值
     - 描述
   * - :kconfig:option:`CONFIG_QUIC_INITIAL_MAX_DATA`
     - 16384
     - 连接级接收信用，以字节为单位。必须大于或等于任何单个流的 ``INITIAL_MAX_STREAM_DATA`` 值，否则连接窗口会成为瓶颈。一个良好的起点是 ``streams_bidi x INITIAL_MAX_STREAM_DATA_BIDI_LOCAL``。
   * - :kconfig:option:`CONFIG_QUIC_INITIAL_MAX_STREAM_DATA_BIDI_LOCAL`
     - 16384
     - 本地发起的双向流的初始接收窗口。应设置为等于 :kconfig:option:`CONFIG_QUIC_STREAM_RX_BUFFER_SIZE`。
   * - :kconfig:option:`CONFIG_QUIC_INITIAL_MAX_STREAM_DATA_BIDI_REMOTE`
     - 16384
     - 对端发起的双向流的初始接收窗口。应设置为等于 :kconfig:option:`CONFIG_QUIC_STREAM_RX_BUFFER_SIZE`。
   * - :kconfig:option:`CONFIG_QUIC_INITIAL_MAX_STREAM_DATA_UNI`
     - 16384
     - 对端打开的单向流的初始接收窗口。仅当 :kconfig:option:`CONFIG_QUIC_MAX_STREAMS_UNI` > 0 时相关。
   * - :kconfig:option:`CONFIG_QUIC_INITIAL_MAX_STREAMS_BIDI`
     - QUIC_MAX_STREAMS_BIDI
     - 在对端收到 ``MAX_STREAMS`` 帧之前，其可以打开的双向流最大数量。默认为本地构建时限制。
   * - :kconfig:option:`CONFIG_QUIC_INITIAL_MAX_STREAMS_UNI`
     - QUIC_MAX_STREAMS_UNI
     - 对端可以打开的单向流最大数量。
   * - :kconfig:option:`CONFIG_QUIC_STREAM_RX_WINDOW_UPDATE_THRESHOLD`
     - 25
     - 发送 ``MAX_STREAM_DATA`` 帧以补充对端窗口之前，流接收缓冲区已消耗的百分比。较低的值（例如 15 %）会更频繁地发送更新，这能提高高延迟链路的吞吐量，但会增加额外的控制帧。

缓冲区大小与 RAM 分配
---------------------

以下选项直接控制 QUIC 子系统在初始化时分配多少 RAM。有关这些选项如何相互作用的详细分解，请参见 `内存模型`_。

.. list-table::
   :widths: 44 12 44
   :header-rows: 1

   * - 选项
     - 默认值
     - 描述
   * - :kconfig:option:`CONFIG_QUIC_ENDPOINT_PENDING_DATA_LEN`
     - 1500
     - 每个端点的接收暂存缓冲区大小，以字节为单位。应等于网络 MTU。与 :kconfig:option:`CONFIG_QUIC_PKT_COUNT` 结合时，端点 RX 暂存总量 = ``endpoints x pkt_count x this value``。
   * - :kconfig:option:`CONFIG_QUIC_TX_BUFFER_SIZE`
     - 1500
     - 每个端点的输出数据包组装缓冲区。必须至少为网络 MTU（IPv6 合规最小 1280，最大 1500）。在确认更大的路径 MTU 之前，DPLPMTUD 可能会将 **已验证的** UDP 载荷限制在此值以下；请参见 :ref:`quic_dplpmtud`。
   * - :kconfig:option:`CONFIG_QUIC_CRYPTO_RX_BUFFER_SIZE`
     - 4096
     - 在 TLS 握手期间使用的每端点共享 CRYPTO 帧重组缓冲区。由于 QUIC 按加密级别顺序推进（Initial -> Handshake -> Application），单个缓冲区会在所有级别间复用。4096 字节是与浏览器互操作的最小值：Chrome 和 Firefox 可能会将 ClientHello 拆分为 10 个或更多 CRYPTO 帧片段，总计最多约 4 KiB。对于使用小型证书的嵌入式到嵌入式部署，可减少到 2048。范围：1024-8192。
   * - :kconfig:option:`CONFIG_QUIC_CRYPTO_OOO_SLOTS`
     - 8
     - 每个端点的乱序 CRYPTO 帧元数据槽数量。每个槽（约 8 字节）记录一个乱序片段的偏移和长度，直到其前面的间隙被填充。与浏览器互操作需要 8 个槽；仅嵌入式部署可减少到 4。范围：4-16。
   * - :kconfig:option:`CONFIG_QUIC_STREAM_TX_BUFFER_SIZE`
     - 8192
     - 保存已发送但未确认数据的每流缓冲区。QUIC 发送方无法越过未确认窗口前进，因此在高延迟链路上，这是主要的吞吐量限制参数。大小至少应为带宽延迟积：``throughput_bytes_per_ms x rtt_ms``。
   * - :kconfig:option:`CONFIG_QUIC_STREAM_RX_BUFFER_SIZE`
     - QUIC_STREAM_TX_BUFFER_SIZE
     - 每流接收缓冲区。默认为 TX 缓冲区大小，这对于对称请求/响应模式是最优的。对于非对称工作负载（例如只下载的流），可以独立减小。
   * - :kconfig:option:`CONFIG_QUIC_STREAM_OOO_SLOTS`
     - 4
     - 每流的乱序 STREAM 帧槽数量。每个槽最多可容纳 :kconfig:option:`CONFIG_QUIC_STREAM_OOO_SEG_SIZE` 字节。在无丢失的本地网络上设置为 2；在具有明显重排序的 WAN 链路上增加到 8 或更多。
   * - :kconfig:option:`CONFIG_QUIC_STREAM_OOO_SEG_SIZE`
     - 1280
     - 一个缓冲的乱序片段的最大大小。将其设置为 MTU 可避免传入帧分片。当 OOO 交付不常见时，可减少到 512 字节。
   * - :kconfig:option:`CONFIG_QUIC_SENT_PKT_HISTORY_SIZE`
     - 64
     - 最近发送数据包记录的环形缓冲区深度。每个条目约 24 字节。必须足以同时覆盖所有在途数据包：至少 ``ceil(STREAM_TX_BUFFER_SIZE / TX_BUFFER_SIZE) x 2``。在有丢失或高延迟的 WAN 链路上增加到 128-256。
   * - :kconfig:option:`CONFIG_QUIC_TLS_TRANSCRIPT_BUF_LEN`
     - 4096
     - 每连接缓冲区，用于累积 TLS 1.3 握手记录，以供 ``Finished`` MAC 计算和 HKDF 密钥派生使用。4096 字节可覆盖使用 RSA-2048 和 EC P-256 证书的典型 TLS 1.3 握手。对于更长的证书链或 RSA-4096，增加到 6144-8192。消耗的总 RAM 等于该值乘以 :kconfig:option:`CONFIG_QUIC_MAX_CONTEXTS`。


超时选项
--------

.. list-table::
   :widths: 44 12 44
   :header-rows: 1

   * - 选项
     - 默认值
     - 描述
   * - :kconfig:option:`CONFIG_QUIC_MAX_IDLE_TIMEOUT`
     - 30000
     - 连接在无活动达到该毫秒数后被静默关闭。两个端点都会通告各自的值；两者中较小的值生效。设置为 0 可完全禁用空闲超时。推荐值：5000 ms（环回）、10000 ms（LAN）、30000 ms（WAN）。
   * - :kconfig:option:`CONFIG_QUIC_CONNECT_TIMEOUT`
     - 3000
     - 在 ``connect()`` 调用失败之前，等待握手完成的毫秒数。应至少为预期 RTT 的 10 倍，以容忍握手期间的丢包。
   * - :kconfig:option:`CONFIG_QUIC_MAX_PTO_TIMEOUT_MS`
     - 10000
     - 指数 PTO 退避的上限，以毫秒为单位。PTO 计时器在每次连续探测超时时翻倍：``PTO_n = PTO_base x 2^n``。该上限可防止过长的重传延迟。不应超过 :kconfig:option:`CONFIG_QUIC_MAX_IDLE_TIMEOUT`。

服务线程选项
------------

.. list-table::
   :widths: 44 12 44
   :header-rows: 1

   * - 选项
     - 默认值
     - 描述
   * - :kconfig:option:`CONFIG_QUIC_SERVICE_THREAD_PRIO`
     - NUM_PREEMPT_PRIORITIES
     - QUIC 服务调度器的线程优先级。值 >= 0 为抢占式（0 = 最高）；值 < 0 为协作式。
   * - :kconfig:option:`CONFIG_QUIC_SERVICE_STACK_SIZE`
     - 4096
     - QUIC 服务线程的栈大小，以字节为单位。默认值为 4096 字节，足以进行 Mbed TLS 握手操作。仅在 RAM 极其受限且性能分析确认不需要该栈余量时才减小。
   * - :kconfig:option:`CONFIG_QUIC_PKT_COUNT`
     - QUIC_MAX_ENDPOINTS
     - 同时挂起的数据包接收操作数量。默认值为端点数量，以便每个端点有一个数据包可以并发在途。对于更高吞吐量的场景，可增加该值（例如端点数的 2 倍）。


内存模型
********

下表显示了每个 RAM 区域如何随配置参数扩展。除非另有说明，所有大小均以字节为单位。

.. list-table::
   :widths: 36 64
   :header-rows: 1

   * - 内存区域
     - 公式
   * - 端点 RX 暂存
     - ``QUIC_MAX_ENDPOINTS x QUIC_PKT_COUNT x QUIC_ENDPOINT_PENDING_DATA_LEN``
   * - 端点 TX 缓冲区
     - ``QUIC_MAX_ENDPOINTS x QUIC_TX_BUFFER_SIZE``
   * - Crypto RX 缓冲区
     - ``QUIC_MAX_ENDPOINTS x QUIC_CRYPTO_RX_BUFFER_SIZE``
   * - Crypto OOO 槽
     - ``QUIC_MAX_ENDPOINTS x QUIC_CRYPTO_OOO_SLOTS x 8``
   * - 流 TX 缓冲区
     - ``(QUIC_MAX_CONTEXTS x (QUIC_MAX_STREAMS_BIDI + QUIC_MAX_STREAMS_UNI)) x QUIC_STREAM_TX_BUFFER_SIZE``
   * - 流 RX 缓冲区
     - ``(QUIC_MAX_CONTEXTS x (QUIC_MAX_STREAMS_BIDI + QUIC_MAX_STREAMS_UNI)) x QUIC_STREAM_RX_BUFFER_SIZE``
   * - 流 OOO 缓冲区
     - ``total_streams x QUIC_STREAM_OOO_SLOTS x QUIC_STREAM_OOO_SEG_SIZE``
   * - 已发送数据包历史
     - ``QUIC_MAX_CONTEXTS x QUIC_SENT_PKT_HISTORY_SIZE x 24``
   * - TLS 记录缓冲区
     - ``QUIC_MAX_CONTEXTS x QUIC_TLS_TRANSCRIPT_BUF_LEN``
   * - TLS 上下文（Mbed TLS）
     - ~8192 x ``QUIC_MAX_CONTEXTS`` (估算值；取决于密码套件)
   * - 连接状态
     - ~512 x ``QUIC_MAX_CONTEXTS``
   * - 流状态
     - ~128 x ``total_streams``

**QUIC RAM 总估算值** (1 个连接、3 条双向流、1500 字节流缓冲区、LAN 客户端默认值的粗略下限)：

.. code-block:: none

   Endpoint RX staging :  2 x 1 x 1500 = 3 000 B
   Endpoint TX         :  2 x 1500      = 3 000 B
   Crypto RX buffers   :  2 x 2048      = 4 096 B  (embedded client, LAN)
   Crypto OOO slots    :  2 x 4 x 8     =   256 B
   Stream TX           :  3 x 1500      = 4 500 B
   Stream RX           :  3 x 1500      = 4 500 B
   OOO buffers         :  3 x 2 x 512   = 3 072 B
   Sent-pkt history    :  1 x 16 x 24   =   384 B
   TLS transcript      :  1 x 4096      = 4 096 B
   TLS context         :  1 x 8192      = 8 192 B
   State overhead      :  512 + 3x128   =   896 B
   ---------------------------------------------
   Approximate total                   ~ 35 992 B (~35 KiB)

在低流数量时，主要开销是每连接的 Mbed TLS 上下文。在较高流数量时，流 TX/RX 缓冲区成为主要开销。


Kconfig 优化器
**************

选择既节省内存又能维持目标吞吐量的缓冲区大小，需要平衡多个相互依赖的参数。为帮助完成此工作，Zephyr 提供了一个 Python 优化器脚本：

.. code-block:: none

   scripts/net/quic-kconfig-optimizer.py

该脚本接受对部署场景的描述——连接数量、MTU、网络类型、预期 RTT 和 RAM 预算——并输出一整套推荐的 ``CONFIG_`` 值，以及估算的 RAM 明细和可直接粘贴的 ``prj.conf`` 片段。

前置条件
--------

该脚本需要 Python 3.8 或更高版本，除标准库外没有其他依赖。

.. code-block:: bash

   python3 --version   # must be 3.8+

用法：交互模式
--------------

不带参数运行脚本即可进入引导式交互模式。每个提示都会在方括号中显示其默认值；按 :kbd:`Enter` 可接受该值。

.. code-block:: bash

   python3 scripts/net/quic-kconfig-optimizer.py

示例会话：

.. code-block:: none

   ============================================================
     Zephyr QUIC Kconfig Optimizer -- Interactive Mode
   ============================================================
     Press Enter to accept [default] values.

   Max QUIC connections (QUIC_MAX_CONTEXTS) [1]: 2
   Bidirectional streams per connection [3]:
   Unidirectional streams per connection [0]:
   Network MTU in bytes [1500]:
   RAM budget in bytes (0 = no limit) [0]: 131072
   Device role [client] (client/server/both):
   IP version(s) [ipv4] (ipv4/ipv6/both):
   Expected RTT in ms [10]: 50
   Expected packet loss rate (%) [0.0]:
   Typical application message size (bytes) [1024]: 4096
   Expect out-of-order delivery? [no] (yes/no):
   Network type [lan] (lan/wan/loopback):

用法：命令行模式
----------------

所有参数都可以在命令行上提供。当所有必需参数都存在时，脚本会完全跳过交互提示，因此适合 CI 流水线和脚本化的板级启动。

.. code-block:: bash

   python3 scripts/net/quic-kconfig-optimizer.py \
       --contexts        2          \
       --streams-bidi    3          \
       --streams-uni     0          \
       --mtu             1500       \
       --ram-budget      131072     \
       --role            client     \
       --ip-version      ipv4       \
       --rtt-ms          50         \
       --loss-rate       0.0        \
       --app-message-size 4096      \
       --ooo-expected    no         \
       --network-type    lan

如果只提供了部分参数，脚本会针对缺失的参数回退到交互模式。

.. code-block:: bash

   # Pre-fill the constraints, fill the rest interactively
   python3 scripts/net/quic-kconfig-optimizer.py \
       --contexts 1 --streams-bidi 3 --ram-budget 65536

输入参数
--------

.. list-table::
   :widths: 28 12 12 48
   :header-rows: 1

   * - 参数
     - CLI 标志
     - 默认值
     - 描述
   * - 最大连接数
     - ``--contexts``
     - 1
     - 直接映射到 :kconfig:option:`CONFIG_QUIC_MAX_CONTEXTS`。用于 TLS 上下文、连接状态和已发送数据包历史的内存随该值线性扩展。
   * - 双向流
     - ``--streams-bidi``
     - 3
     - 每个连接的双向流数量。会为每个连接中的每条流分配流 TX/RX 缓冲区，因此在启动时会预留 ``contexts x streams_bidi x 2 x stream_buf`` 字节。
   * - 单向流
     - ``--streams-uni``
     - 0
     - 每个连接的单向流数量。如果不需要，设置为 0 可避免分配相关的接收缓冲区。
   * - MTU
     - ``--mtu``
     - 1500
     - 网络最大传输单元，以字节为单位。它为 :kconfig:option:`CONFIG_QUIC_TX_BUFFER_SIZE` 和 :kconfig:option:`CONFIG_QUIC_ENDPOINT_PENDING_DATA_LEN` 设置下限。对于要求符合 IPv6 最小 MTU 且无法使用路径 MTU 发现的网络，请使用 1280。
   * - RAM 预算
     - ``--ram-budget``
     - 0（无限制）
     - 估算 QUIC RAM 使用量的硬上限，以字节为单位。如果计算出的分配量超过此值，脚本会报错中止。设置为 0 可跳过预算检查，仅报告估算值。
   * - 设备角色
     - ``--role``
     - ``client``
     - ``client``、``server`` 或 ``both``。会影响推荐的端点数量：服务器和双协议栈设备通常需要一个额外端点。
   * - IP 版本
     - ``--ip-version``
     - ``ipv4``
     - ``ipv4``、``ipv6`` 或 ``both``。选择 ``both`` 且未启用 :kconfig:option:`CONFIG_QUIC_ENDPOINT_USE_IPV4_MAPPING_TO_IPV6` 时，需要额外一个端点。
   * - 预期 RTT
     - ``--rtt-ms``
     - 10
     - 设备与远程对端之间的往返时间，以毫秒为单位。用于确定 :kconfig:option:`CONFIG_QUIC_CONNECT_TIMEOUT`、:kconfig:option:`CONFIG_QUIC_MAX_PTO_TIMEOUT_MS` 和窗口更新阈值的大小。
   * - 丢包率
     - ``--loss-rate``
     - 0.0
     - 预期丢包率，以百分比表示（0-100）。丢包 >= 2 % 会使流缓冲区大小加倍，以保持流水线满载；丢包 >= 5 % 会强制将已发送数据包历史设置为至少 128 个条目，以实现有效的丢失检测。
   * - 消息大小
     - ``--app-message-size``
     - 1024
     - 典型的应用载荷大小，以字节为单位。流缓冲区的大小至少可容纳该值的 2 倍，以便在确认前一条消息时，仍有一条完整消息在途。
   * - 预期 OOO
     - ``--ooo-expected``
     - ``no``
     - 是否预期乱序数据包交付（``yes``/``no``）。当为 ``no`` 时，OOO 槽减少到 2，片段大小减少到 512 B，从而节省 ``total_streams x (default_slots - 2) x seg_size`` 字节。
   * - 网络类型
     - ``--network-type``
     - ``lan``
     - ``lan``、``wan`` 或 ``loopback``。控制空闲超时、PTO 上限，以及是否将流缓冲区加倍以填满 WAN 链路更大的带宽延迟积。

输出部分
--------

优化器会打印五个部分。

**输入参数** -- 回显所有提供的值以供验证。

**推荐的 Kconfig 值** -- 按类别（连接数量、传输参数、缓冲区大小、超时）分组的计算出的 ``CONFIG_*`` 值。

**估算的 RAM 使用量** -- 一个表，显示每个内存区域、其大小以及比例 ASCII 条形图。如果给出了 RAM 预算，还会显示利用率百分比。

**prj.conf 片段** -- 一个可复制粘贴的 Kconfig 选项块，可直接放入 ``prj.conf`` 或板级 ``.conf`` 覆盖文件。

**附加说明** -- 根据输入得出的部署特定警告和建议，例如服务线程栈可能太小，或者连接级流量控制窗口可能成为瓶颈。

示例输出
--------

下面展示了最小客户端配置的输出：一个连接、三条双向流、以太网 LAN、10 ms RTT、1 KiB 消息、无 OOO。

.. code-block:: none

   ========================================================================
            QUIC Kconfig Optimizer -- Recommended Settings
   ========================================================================

   ------------------------------------------------------------------------
     INPUT PARAMETERS
   ------------------------------------------------------------------------
     Max connections (QUIC_MAX_CONTEXTS)            1
     Bidi streams per connection                    3
     Uni  streams per connection                    0
     MTU (bytes)                                    1500
     RAM budget                                     unlimited
     Device role                                    client
     IP version                                     ipv4
     Expected RTT (ms)                              10
     Expected packet loss (%)                       0.0
     Typical message size (bytes)                   1024
     Out-of-order delivery expected                 no
     Network type                                   lan

   ------------------------------------------------------------------------
     RECOMMENDED Kconfig VALUES
   ------------------------------------------------------------------------

     [Connection / stream counts]
       CONFIG_QUIC_MAX_CONTEXTS                              1
       CONFIG_QUIC_MAX_STREAMS_BIDI                         3
       CONFIG_QUIC_MAX_STREAMS_UNI                          0
       CONFIG_QUIC_MAX_ENDPOINTS                            2
       CONFIG_QUIC_PKT_COUNT                                2

     [QUIC transport parameters (flow control)]
       CONFIG_QUIC_INITIAL_MAX_DATA                         6144
       CONFIG_QUIC_INITIAL_MAX_STREAM_DATA_BIDI_LOCAL       2048
       CONFIG_QUIC_INITIAL_MAX_STREAM_DATA_BIDI_REMOTE      2048
       CONFIG_QUIC_INITIAL_MAX_STREAM_DATA_UNI              16384
       CONFIG_QUIC_INITIAL_MAX_STREAMS_BIDI                 3
       CONFIG_QUIC_INITIAL_MAX_STREAMS_UNI                  0
       CONFIG_QUIC_STREAM_RX_WINDOW_UPDATE_THRESHOLD        25

     [Buffer sizes (RAM)]
       CONFIG_QUIC_ENDPOINT_PENDING_DATA_LEN                1500
       CONFIG_QUIC_TX_BUFFER_SIZE                           1500
       CONFIG_QUIC_CRYPTO_RX_BUFFER_SIZE                    2048
       CONFIG_QUIC_CRYPTO_OOO_SLOTS                         4
       CONFIG_QUIC_STREAM_TX_BUFFER_SIZE                    2048
       CONFIG_QUIC_STREAM_RX_BUFFER_SIZE                    2048
       CONFIG_QUIC_STREAM_OOO_SLOTS                         2
       CONFIG_QUIC_STREAM_OOO_SEG_SIZE                      512
       CONFIG_QUIC_SENT_PKT_HISTORY_SIZE                    16
       CONFIG_QUIC_TLS_TRANSCRIPT_BUF_LEN                   4096

     [Timeouts]
       CONFIG_QUIC_MAX_IDLE_TIMEOUT                         10000
       CONFIG_QUIC_CONNECT_TIMEOUT                          3000
       CONFIG_QUIC_MAX_PTO_TIMEOUT_MS                       5000

   ------------------------------------------------------------------------
     ESTIMATED RAM USAGE
   ------------------------------------------------------------------------
     Endpoint RX staging              9 KiB  ######
     Endpoint TX buffers              3 KiB  ##
     Crypto RX buffers                4 KiB  ###
     Crypto OOO slots                  64 B
     Stream TX buffers                6 KiB  ####
     Stream RX buffers                6 KiB  ####
     Stream OOO buffers               2 KiB  #
     Stream state overhead            0 KiB
     Sent-packet history              0 KiB
     TLS context overhead             8 KiB  #####
     Connection state overhead        0 KiB
     TLS transcript buffers           4 KiB  ##
     TOTAL                           42 KiB  ######################## <-- TOTAL

   ------------------------------------------------------------------------
     prj.conf SNIPPET
   ------------------------------------------------------------------------

   CONFIG_QUIC_MAX_CONTEXTS=1
   CONFIG_QUIC_MAX_STREAMS_BIDI=3
   ...

最小 IoT 传感器（客户端，仅 IPv4，RAM 预算紧张）
------------------------------------------------

一个传感器，它向云端端点打开一个 QUIC 连接，使用单条双向流报告遥测数据，并且有 48 KiB 可用于 QUIC：

.. code-block:: bash

   python3 scripts/net/quic-kconfig-optimizer.py \
       --contexts 1 --streams-bidi 1 --streams-uni 0 \
       --mtu 1280 --ram-budget 49152 \
       --role client --ip-version ipv4 \
       --rtt-ms 80 --loss-rate 0.5 \
       --app-message-size 256 \
       --ooo-expected no --network-type wan

脚本会将流缓冲区大小设置为 1500 B（最小值，因为 ``2 x 256 = 512 < 1500``），将 OOO 槽设置为 2，并将已发送数据包历史保持在 16 个条目——所有这些都旨在最小化 RAM，同时仍能处理 WAN 链路上预期的 0.5 % 丢包。

双协议栈服务器（IPv4 + IPv6，多个客户端）
-----------------------------------------

一个边缘网关，通过 IPv4 和 IPv6 接受最多四个同时的客户端连接，并且有 256 KiB 可用于 QUIC：

.. code-block:: bash

   python3 scripts/net/quic-kconfig-optimizer.py \
       --contexts 4 --streams-bidi 3 --streams-uni 1 \
       --mtu 1500 --ram-budget 262144 \
       --role server --ip-version both \
       --rtt-ms 5 --loss-rate 0.0 \
       --app-message-size 8192 \
       --ooo-expected no --network-type lan

脚本将推荐三个端点（两个用于监听 socket，每个客户端地址族一个），并将流缓冲区大小设置为 16 KiB（以容纳 2 x 8192 B 消息）；在 4 个上下文且每个上下文 4 条流的情况下，这将占据 RAM 预算的大部分。

有丢包的高吞吐量 WAN 链路
-------------------------

一个通过蜂窝 WAN 连接的数据聚合器，存在可测量的丢包，需要为固件更新载荷维持持续吞吐量：

.. code-block:: bash

   python3 scripts/net/quic-kconfig-optimizer.py \
       --contexts 1 --streams-bidi 2 --streams-uni 0 \
       --mtu 1400 --ram-budget 0 \
       --role client --ip-version ipv4 \
       --rtt-ms 150 --loss-rate 3.0 \
       --app-message-size 32768 \
       --ooo-expected yes --network-type wan

在此场景中，脚本会将流缓冲区加倍（丢包 >= 2 %），并选择 15 % 的窗口更新阈值（高延迟 WAN），以保持对端发送窗口打开，从而最大化流水线利用率。它还会将 OOO 槽设置为 8，并使用 1280 字节片段来处理蜂窝网络的重排序。

调优指南
********

**从优化器默认值开始，然后进行测量。** 脚本的启发式规则较为保守。使用 Zephyr 网络统计信息（``CONFIG_NET_STATISTICS``）观察实际的流窗口停滞和 OOO 事件，然后再决定是否增大缓冲区大小。

**流缓冲区是最大的 RAM 开销。** 在多连接设备上，``contexts x streams x 2 x stream_buf`` 占主导。将流缓冲区大小减半可按比例节省。只有在性能分析显示发送方持续停滞时，才将其增大到超过 BDP。

**连接级窗口绝不能成为瓶颈。** :kconfig:option:`CONFIG_QUIC_INITIAL_MAX_DATA` 必须大于或等于最大的每流窗口；否则即使各流窗口是打开的，连接上限也会限制吞吐量。

**CRYPTO 缓冲区随端点数扩展，而不是随连接数扩展。** :kconfig:option:`CONFIG_QUIC_CRYPTO_RX_BUFFER_SIZE` 和 :kconfig:option:`CONFIG_QUIC_CRYPTO_OOO_SLOTS` 每个端点分配一次，因此其 RAM 开销为 ``QUIC_MAX_ENDPOINTS x buffer_size``。浏览器互操作需要 4096 字节的默认值（Chrome 和 Firefox 会将 ClientHello 分片为许多小的 CRYPTO 帧）；对于对端也是 Zephyr 设备的仅嵌入式部署，可减少到 2048。

**IPv4 映射的 IPv6。** 当同时需要 IPv4 和 IPv6 时，启用 :kconfig:option:`CONFIG_QUIC_ENDPOINT_USE_IPV4_MAPPING_TO_IPV6` 可让一个 UDP socket 同时服务两个地址族，从而将 :kconfig:option:`CONFIG_QUIC_MAX_ENDPOINTS` 减少一个，并节省相关的缓冲区 RAM。

**禁用未使用的流方向。** 如果应用只使用客户端发起的流，请将 :kconfig:option:`CONFIG_QUIC_MAX_STREAMS_UNI` 设置为 0。优化器会自动考虑这一点。

**OOO 内存是按流计算的。** ``QUIC_STREAM_OOO_SLOTS x QUIC_STREAM_OOO_SEG_SIZE x total_streams`` 可能相当可观。在可靠的 LAN 上，将 :kconfig:option:`CONFIG_QUIC_STREAM_OOO_SLOTS` 设置为 2，并将 :kconfig:option:`CONFIG_QUIC_STREAM_OOO_SEG_SIZE` 设置为 512 是安全的，并且每个连接可节省数 KiB。


API 参考
********

.. doxygengroup:: quic
