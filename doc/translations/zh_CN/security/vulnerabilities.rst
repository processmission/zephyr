.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _vulnerabilities:

漏洞
####

本页汇总每个版本中发现并修复的所有漏洞。这里通常还包含比版本说明中更多的细节。某些漏洞被视为敏感漏洞，在留出足够时间修复之前不会公开讨论。由于版本说明与特定版本绑定，此处的信息可在保密期结束后更新。

往年的漏洞收集在单独的页面上：

.. toctree::
   :maxdepth: 1

   vulnerabilities/2017
   vulnerabilities/2019
   vulnerabilities/2020
   vulnerabilities/2021
   vulnerabilities/2022
   vulnerabilities/2023
   vulnerabilities/2024
   vulnerabilities/2025

CVE-2026
========

:cve:`2026-0849`
----------------

crypto：ATAES132A 响应长度可导致栈缓冲区溢出

长度字段过大的畸形 ATAES132A 响应会溢出 Zephyr crypto 驱动中的 52 字节栈缓冲区，使受感染的设备或总线攻击者能够破坏内核内存，并可能劫持执行流程。

- `Zephyr 项目漏洞跟踪 GHSA-ff4p-3ggg-prp6 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-ff4p-3ggg-prp6>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 103163 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/103163>`_

:cve:`2026-1677`
----------------

net：TLS 1.3 socket 上允许建立 TLS 1.2 连接

当 Kconfig 中同时启用两个 TLS 版本时，使用 ``IPPROTO_TLS_1_3`` 创建的 Zephyr socket 仍可协商出 TLS 1.2 连接，因为 socket 级别的协议选择未传递到 mbedTLS（例如通过 ``mbedtls_ssl_conf_min_tls_version``）。ClientHello 会通告两个版本，对端可以建立 TLS 1.2，因此那些认为 ``IPPROTO_TLS_1_3`` 会强制使用 TLS 1.3 的应用可能会静默使用 TLS 1.2，并继续暴露于 TLS 1.2 特有的弱点。

- `Zephyr 项目漏洞跟踪 GHSA-23r2-m5wx-4rvq <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-23r2-m5wx-4rvq>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 102570 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/102570>`_


:cve:`2026-1678`
----------------

dns：DNS 名称解析器中的内存安全问题

``dns_unpack_name()`` 只缓存一次缓冲区尾部空间，并在追加 DNS 标签时重复使用该值。随着缓冲区增长，缓存的大小会变得不正确，最终的空终止符可能被写到缓冲区末尾之外。在禁用断言（默认情况）时，一旦启用 ``CONFIG_DNS_RESOLVER`` 时，恶意 DNS 响应便可触发越界写。


- `Zephyr 项目漏洞跟踪 GHSA-536f-h63g-hj42 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-536f-h63g-hj42>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 99683 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/99683>`_

- `PR 99830 针对 4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/99830>`_

- `PR 99829 针对 4.2 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/99829>`_

- `PR 99828 针对 3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/99828>`_

:cve:`2026-1679`
----------------

eswifi socket offload 驱动将用户提供的负载复制到固定缓冲区中，而不检查可用空间；过大的发送会溢出 eswifi->buf，破坏内核内存（CWE-120）。利用此漏洞需要能够调用 socket 发送 API 的本地代码；远程攻击者无法直接触及该路径。

- `Zephyr 项目漏洞跟踪 GHSA-qx3g-5g22-fq5w <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-qx3g-5g22-fq5w>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 102119 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/102119>`_

:cve:`2026-1681`
----------------

net：通过 Shell 向自身 IP 地址执行 Ping 导致栈溢出

通过 ``net ping`` shell 命令向设备自身的 IPv4 地址发送 ICMP ping 会导致网络栈在同一系统 work-queue 栈上递归重入输入路径。由于目标被识别为本地地址，echo request 和由此产生的 echo reply 都会在当前帧返回前被内联处理。嵌套的输入路径帧超出 work-queue 栈容量，从而触发栈溢出。

- `Zephyr 项目漏洞跟踪 GHSA-6fcc-8rwr-w7xx <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-6fcc-8rwr-w7xx>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 102268 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/102268>`_

:cve:`2026-4179`
----------------

stm32：usb：中断处理程序中的无限 while 循环

stm32 USB 设备驱动中的问题可能导致无限 while 循环。

- `Zephyr 项目漏洞跟踪 GHSA-9xg7-g3q3-9prf <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9xg7-g3q3-9prf>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 104390 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104390>`_

:cve:`2026-5066`
----------------

net：sockets：tls：socket_op_vtable::connect 函数中潜在的越界写/读

网络 sockets 子系统的 TLS socket 连接路径（``subsys/net/lib/sockets/sockets_tls.c``）中存在潜在的越界写/读。当 TLS 会话缓存启用时，``tls_session_store()`` 和 ``tls_session_restore()`` 会使用调用方控制的 ``addrlen`` 值将调用方提供的地址 ``memcpy`` 到固定大小缓冲区中，而不根据目标大小校验该值。由于 ``struct net_sockaddr`` 是不透明类型，应用可以传入大于 ``sizeof(struct net_sockaddr)`` 的 ``addrlen`` （例如将 128 字节写入 24 字节栈缓冲区），导致 ``memcpy`` 读写超出 TLS 会话缓存所用地址内存的末尾。这可能导致崩溃和拒绝服务，并有可能导致任意代码执行。

- `Zephyr 项目漏洞跟踪 GHSA-wgrc-jrf6-24f3 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wgrc-jrf6-24f3>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 104871 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104871>`_

- `PR 105044 针对 4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/105044>`_

- `PR 105043 针对 4.2 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/105043>`_

- `PR 105042 针对 3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/105042>`_

:cve:`2026-5067`
----------------

通过未以 null 结尾的 Sec-WebSocket-Key 在 HTTP WebSocket 升级过程中造成越界读/写

远程未认证攻击者可通过发送特制的 ``Sec-WebSocket-Key`` 头来触发 Zephyr HTTP 服务器 WebSocket 升级路径中的内存破坏，该头在被复制时不保证 NUL 终止，随后被传递给 ``strlen()``。这可能导致栈内存上的越界读和越界写，造成崩溃（拒绝服务），并可能实现代码执行。启用 ``CONFIG_HTTP_SERVER_WEBSOCKET`` 时该路径可达。

- `Zephyr 项目漏洞跟踪 GHSA-wgr4-9pwq-94vj <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wgr4-9pwq-94vj>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 104740 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104740>`_

- `PR 107927 针对 4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107927>`_

- `PR 107926 针对 3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107926>`_

:cve:`2026-5068`
----------------

Bluetooth：L2CAP LE CoC：通过存储在 net_buf user_data 中的分段计数器实现的远程越界写

远程未认证 BLE 对端可在 L2CAP LE CoC SDU 重组期间触发 Bluetooth 主机中的 2 字节越界写。当应用启用分段（通过 ``chan_ops.alloc_buf``）且所选 RX pool 的 ``user_data_size`` 小于 2 字节时，存储在 ``net_buf`` user_data 区域中的分段计数器会在 ``l2cap_chan_le_recv_seg`` （``subsys/bluetooth/host/l2cap.c``）中越界写入。这可能导致堆破坏和致命错误。

- `Zephyr 项目漏洞跟踪 GHSA-qrcq-hxwj-mqxm <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-qrcq-hxwj-mqxm>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 104913 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104913>`_

- `PR 108335 针对 4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108335>`_

- `PR 108336 针对 3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108336>`_

:cve:`2026-5071`
----------------

can：通过 SocketCAN 发送实现本地拒绝服务

SocketCAN 发送路径（``zcan_sendto_ctx``）使用 ``NET_ASSERT`` 而不是真正的运行时检查来校验调用方提供的缓冲区长度。在断言被编译掉的生产构建中，用户空间应用可以传入短于 ``struct socketcan_frame`` 的缓冲区，``socketcan_to_can_frame()`` 将解引用超出该缓冲区末尾的字段——这是一次越界读，可能导致系统崩溃（本地 DoS），或者由于解析后的帧随后被发送，可能泄漏相邻内存。

- `Zephyr 项目漏洞跟踪 GHSA-c3w6-x7m3-3c58 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-c3w6-x7m3-3c58>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 104654 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104654>`_

- `PR 104679 针对 4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104679>`_

- `PR 104678 针对 4.2 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104678>`_

- `PR 104677 针对 3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104677>`_

:cve:`2026-5072`
----------------

net：ptp：通过 PTP 间隔移位实现潜在的拒绝服务

位移位漏洞允许远程攻击者通过发送特制的 PTP Management 或 Delay Response 数据包，在 PTP 子系统中造成未定义行为和潜在崩溃，该数据包包含一个用于位移操作、未经校验的超大负值 log_announce_interval。

- `Zephyr 项目漏洞跟踪 GHSA-3v98-458v-388r <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3v98-458v-388r>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 104613 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104613>`_

- `PR 108337 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108337>`_

- `PR 108338 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108338>`_

:cve:`2026-5589`
----------------

Bluetooth：Mesh：整数下溢导致的越界写

Bluetooth Mesh 请求处理（``subsys/bluetooth/mesh/solicitation.c``）中 ``bt_mesh_sol_recv()`` 里的整数下溢会导致越界写。当启用 ``CONFIG_BT_MESH_OD_PRIV_PROXY_SRV`` 时，该函数从原始 BLE 广播负载中解析请求 PDU。AD 解析循环读取攻击者控制的长度字节，并在未检查 ``reported_len`` 至少为 3 的情况下计算 ``reported_len - 3``。当该值更小时，有符号减法会产生一个负数，绕过长度保护，随后被隐式转换为非常大的 ``size_t``，使缓冲区指针远远越过边界，从而导致后续读取解引用无效内存。附近的 BLE 设备可以通过携带 UUID16 AD 结构和特制长度字节的不可连接广播触发此漏洞，无需配对或事先关联，可能导致拒绝服务或任意代码执行。

- `Zephyr 项目漏洞跟踪 GHSA-4pm9-4v7f-x6gr <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4pm9-4v7f-x6gr>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 105585 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/105585>`_

- `PR 108334 针对 4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108334>`_

- `PR 108333 针对 3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108333>`_

:cve:`2026-5590`
----------------

net：ip/tcp：竞态条件可触发空指针解引用

TCP 连接拆除期间的竞态条件可能导致 tcp_recv() 操作一个已被释放的连接。如果在处理 SYN 数据包时 tcp_conn_search() 返回 NULL，则从过期上下文数据派生的 NULL 指针会被传递给 tcp_backlog_is_full() 并在未校验的情况下解引用，导致崩溃。

- `Zephyr 项目漏洞跟踪 GHSA-4vqm-pw24-g9jp <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4vqm-pw24-g9jp>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 102110 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/102110>`_

:cve:`2026-8718`
----------------

Zephyr net sockets/TLS 中 DTLS 对端 Connection ID getsockopt（``TLS_DTLS_PEER_CID_VALUE``）的越界写

``subsys/net/lib/sockets/sockets_tls.c`` 中的 ``tls_opt_dtls_peer_connection_id_value_get()`` 负责处理 ``getsockopt(SOL_TLS, TLS_DTLS_PEER_CID_VALUE)``，它会将调用方提供的 ``optval`` 直接传给 ``mbedtls_ssl_get_peer_cid()``，而未验证缓冲区至少为 ``MBEDTLS_SSL_CID_OUT_LEN_MAX`` （默认 32）字节。``mbedtls_ssl_get_peer_cid()`` 会将协商出的对端 DTLS Connection ID（长度 1.. ``MBEDTLS_SSL_CID_OUT_LEN_MAX``）复制到该缓冲区，且不带目标大小参数，因此调用方提供的 ``optlen`` 小于 CID 时，会在缓冲区末尾之后写入最多 31 字节。

在 ``CONFIG_USERSPACE`` 构建中，getsockopt syscall 校验器（``z_vrfy_zsock_getsockopt``）会将用户的 ``optval`` bounce-buffer 到大小恰好为 ``optlen`` 字节的内核分配中（``k_usermode_alloc_from_copy`` -> ``z_thread_malloc``），因此，在启用了 Connection ID 的已连接 DTLS socket 上，传递较小 ``optlen`` 的非特权用户线程会引发内核堆缓冲区溢出，溢出的内容是远程对端的 CID。

该缺陷需要启用 ``CONFIG_MBEDTLS_SSL_DTLS_CONNECTION_ID``、建立具有已协商对端 CID 的 DTLS 会话，并且（对于跨内核的情形）需要 ``CONFIG_USERSPACE``。该缺陷是在添加 ``TLS_DTLS_CID`` 选项时引入的（v3.5.0）。

修复方案会拒绝 ``optlen`` 低于 ``MBEDTLS_SSL_CID_OUT_LEN_MAX`` 的调用方，并返回 -EINVAL。

- `Zephyr 项目漏洞跟踪 GHSA-p3r6-mx6c-33gq <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-p3r6-mx6c-33gq>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109244 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109244>`_

- `PR 109624 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109624>`_

- `PR 113749 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113749>`_

- `PR 113750 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113750>`_

:cve:`2026-9263`
----------------

Bluetooth Controller ISOAL framed RX 重组中的越界读会将相邻内存泄漏到主机 HCI ISO 数据包中

Zephyr Bluetooth controller ISO Adaptation Layer（``subsys/bluetooth/controller/ll_sw/isoal.c``）未校验 framed ISO PDU 起始段的长度字段。按照 Bluetooth 规范，起始段（``sc=0``）始终携带 3 字节的 ``time_offset``，因此其段头 ``len`` 必须至少为 ``PDU_ISO_SEG_TIMEOFFSET_SIZE`` （3）。``isoal_check_seg_header()`` 接受 ``len`` 小于 3 的起始段为有效段，随后 ``isoal_rx_framed_consume()`` 在 ``uint8_t`` 中计算 ``length = seg_hdr->len - 3``，当 ``len`` 为 0-2 时下溢为 253-255。这个过大的长度会被传递给 ``isoal_rx_append_to_sdu()``，而后者只根据目标 SDU 缓冲区大小限制复制量，而不检查源 PDU 长度，因此最多约 255 字节超出所接收 PDU 的 controller 内存会（通过 ``sink_sdu_write_hci()`` / ``net_buf_add_mem``）被复制到 HCI ISO 数据包中并交付给主机。PDU 及其段头完全由攻击者控制并通过无线方式到达，可通过 CIS 和 BIS-sync HCI 数据路径（``hci_driver.c``）以及厂商数据路径（``ull_iso.c``）到达，因此远程 CIS 对端或设备已同步的广播者可以触发越界读，导致向主机泄露信息以及潜在的拒绝服务（故障或畸形的超大 HCI ISO 数据包）。该缺陷影响自 v3.0.0 引入 framed ISO 接收以来的所有 Zephyr 版本。修复方案会在 ``isoal_check_seg_header()`` 中拒绝 ``len`` 小于 3 的 ``sc=0`` 段，并在 ``isoal_rx_framed_consume()`` 中的减法之前增加保护。

- `Zephyr 项目漏洞跟踪 GHSA-6gvp-pmh8-fjh2 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-6gvp-pmh8-fjh2>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109369 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109369>`_

- `PR 109617 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109617>`_

- `PR 109619 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109619>`_

- `PR 109618 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109618>`_

:cve:`2026-10593`
-----------------

Bluetooth LE Audio BAP 单播客户端 QoS 状态处理中可远程触发的 NULL 指针解引用

Zephyr Bluetooth LE Audio Basic Audio Profile（BAP）单播客户端未正确处理对端提供的 ASE 状态通知。在 ``unicast_client_ep_qos_state()`` （``subsys/bluetooth/audio/bap_unicast_client.c``）中，处理程序仅通过 ``stream != NULL`` 进行保护，便经由 ``stream->qos`` 指针写入攻击者控制的 QoS 字段（``interval``、``framing``、``phy``、``sdu``、``rtn``、``latency``、``pd``）。对于已通过 ``bt_bap_stream_config()`` 完成 codec 配置、但尚未加入单播组的任何 stream，``stream->qos`` 为 ``NULL`` （该指针仅由 ``unicast_group_add_stream()`` 设置）。

本地设备作为 BAP 单播客户端连接的远程 ASCS 服务器如果是恶意或有缺陷的，就可以在本地端点仍处于 Codec Configured 状态时，发送宣称 ASE 已进入 QoS Configured 状态的 GATT 通知——调度程序明确允许这种转换——在那个窗口期内造成通过 NULL 指针写入并崩溃（拒绝服务）。写入的数据本身也由远程控制。

该缺陷存在于 v4.3.0 和 v4.4.0（以及更早版本）中。修复方案将所有 BAP QoS 存储重新指向始终有效的内嵌 ``ep->qos`` 结构体，从而消除 NULL 解引用。

- `Zephyr 项目漏洞跟踪 GHSA-22q8-m94g-2pwh <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-22q8-m94g-2pwh>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 104887 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104887>`_

- `PR 110779 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110779>`_

- `PR 110777 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110777>`_

:cve:`2026-10634`
-----------------

Zephyr 原生 TCP ``net_tcp_foreach()`` 中因在回调期间释放 ``tcp_lock`` 而导致的释放后使用

Zephyr 原生 TCP 栈在 ``net_tcp_foreach()`` （``subsys/net/ip/tcp.c``）中使用 ``SYS_SLIST_FOR_EACH_CONTAINER_SAFE`` 宏遍历全局连接列表，该宏会缓存指向下一个链表节点的指针。在此修复之前，该函数在调用每个连接的回调时会释放 ``tcp_lock``，之后重新获取。在那个窗口期内，并发的 ``tcp_conn_release()`` （当连接引用计数降为零时，在专用 TCP work-queue 线程上运行，例如远程对端关闭或重置连接）可以移除缓存的下一连接并调用 ``k_mem_slab_free()`` 将其释放。当迭代器前进时，它会解引用已释放（并可能已被重新分配）的 slab 内存——这是一次释放后使用，可能导致系统崩溃（拒绝服务），并且如果该槽位已被重用，还会导致回调操作一个受攻击者影响的对象（可能泄露信息或引发进一步故障）。在生产环境中，可通过 ``net conn`` 网络 shell 命令以及接口 down 时的 ``net_tcp_close_all_for_iface()`` 到达 ``net_tcp_foreach()``；释放侧由普通 TCP 流量驱动。修复方案将 ``tcp_conn_release()`` 中的连接/上下文拆除移入 ``tcp_lock`` 临界区，并在 ``net_tcp_foreach()`` 的回调期间始终保持 ``tcp_lock``。该缺陷随 2020 年的现代（TCP2）栈引入，影响直至并包括 v4.4.0 的版本。

- `Zephyr 项目漏洞跟踪 GHSA-6c57-xfhw-j26x <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-6c57-xfhw-j26x>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 106992 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/106992>`_

- `PR 107287 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107287>`_

- `PR 107288 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107288>`_

- `PR 107289 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107289>`_

:cve:`2026-10635`
-----------------

Xtensa MMU 页表代码在内存域 de-init 时的悬空内存域指针（释放后使用）

在启用了 ``CONFIG_USERSPACE`` 和 ``CONFIG_XTENSA_MMU`` 的 Xtensa 目标上，页表代码（``arch/xtensa/core/ptables.c``）使用嵌入在调用方拥有的 ``struct k_mem_domain`` 内部的链表节点，维护活动内存域的全局链表 ``xtensa_domain_list``。当通过 ``k_mem_domain_deinit()`` -> ``arch_mem_domain_deinit()`` 销毁一个域时，页表会被拆除，``domain->arch.ptables`` 被设为 ``NULL``，但该域的节点并未从 ``xtensa_domain_list`` 中移除。因此，已释放/取消初始化的域仍作为悬空指针链接在全局链表中，指向调用方拥有的存储，而该存储随后可能被释放或重用。

后续任何 ``arch_mem_map()`` / ``arch_mem_unmap()`` 操作（被内核内存映射和按需分页代码广泛调用）都会遍历该过期节点并解引用 ``domain->ptables``：至少会造成空指针解引用，引发致命的 MMU 异常（拒绝服务）；如果 ``k_mem_domain`` 存储已被释放或重用，则还会发生释放后使用，在页表遍历期间解引用过期/受控的 ``ptables`` 值并写入（``l2_page_table_map`` 写入 ``l1_table[...]`` 和 ``l2_table[...]``，``xtensa_mmu_compute_domain_regs`` 写入域结构体和 L1 表），造成页表内存破坏，从而可能破坏用户空间隔离。

该漏洞路径只能从特权内核/超级用户代码到达（``k_mem_domain_deinit`` 不是 syscall），不能直接由非特权用户线程或远程触发。受影响版本：Zephyr v4.4.0（Xtensa 内存域取消初始化功能由提交 3032b58f52d 引入，并首次随 v4.4.0 发布）；该问题已在 ``main`` 上通过向 ``arch_mem_domain_deinit()`` 中添加 ``sys_slist_find_and_remove()`` 修复。Xtensa MPU 路径不受影响。

- `Zephyr 项目漏洞跟踪 GHSA-39v7-cx8j-gq82 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-39v7-cx8j-gq82>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 106923 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/106923>`_

- `PR 110758 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110758>`_

:cve:`2026-10636`
-----------------

Zephyr IPv4 IGMP 发送路径（``igmp_send``）中的释放后使用

Zephyr 的 IPv4 IGMP 实现中，``subsys/net/ip/igmp.c`` 里的 ``igmp_send()`` 在数据包已交给 ``net_send_data()`` 之后，通过 ``net_pkt_iface(pkt)`` 从该数据包中再次读取网络接口。在发送成功路径上，数据包的最后一个引用可能已由 L2 驱动或网络栈的 TX 处理释放（在默认 ``NET_TC_TX_COUNT=0`` 立即发送配置中为同步释放），从而将 ``net_pkt`` slab 块归还到空闲链表。随后的 ``net_pkt_iface(pkt)`` 会解引用已释放的数据包，这是一次释放后使用读取；当启用 ``CONFIG_NET_STATISTICS_PER_INTERFACE`` 时，由此得到的悬空接口指针会被进一步解引用，用于写入统计计数器。IGMP 发送路径可在无需认证的情况下，从发往 224.0.0.1 的入站 IPv4 IGMP 成员查询到达（``net_ipv4_igmp_input`` -> ``send_igmp_report`` / ``send_igmp_v3_report`` -> ``igmp_send``），也可由本地多播加入/离开/重新加入操作到达。实际影响是未定义行为和潜在的拒绝服务（偶发崩溃或统计信息损坏）；要获得可控写入，需要异步 TX 路径并伴随并发的 slab 重用。该缺陷随 IGMPv2 支持引入，影响从 v2.6.0 到 v4.4.0 的版本。修复方案会在发送前缓存接口指针。注意，类似的 IPv6 MLD 路径（``subsys/net/ip/ipv6_mld.c`` 中的 ``mld_send``）仍保留相同的未修复模式。

- `Zephyr 项目漏洞跟踪 GHSA-fj6q-975v-65c9 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fj6q-975v-65c9>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107100 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107100>`_

- `PR 110659 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110659>`_

- `PR 110658 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110658>`_

- `PR 107369 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107369>`_

:cve:`2026-10637`
-----------------

IPv6 MLD 发送路径中由链路本地 MLD Query 触发的 ``net_pkt`` 释放后使用

``subsys/net/ip/ipv6_mld.c`` 中的 ``mld_send()`` 在 ``net_send_data(pkt)`` 成功返回后，通过 ``net_pkt_iface(pkt)`` 读取数据包接口。按照网络栈的所有权约定（``include/zephyr/net/net_core.h``，以及 ``subsys/net/ip/net_core.c``:453-460 中明确的警告“do not use pkt after that call”），成功发送会转移 ``net_pkt`` 的所有权，L2 驱动会释放它（例如 ``ethernet_send()`` 在成功时对数据包执行 unref，``subsys/net/l2/ethernet/ethernet.c``:790），将其归还到 ``k_mem_slab``。因此，随后的 ``net_pkt_iface(pkt)`` 是对已释放对象的读取；当启用 ``CONFIG_NET_STATISTICS_PER_INTERFACE`` 时，恢复出的接口指针会被每接口统计路径（``net_stats.h`` ``UPDATE_STAT`` / ``SET_STAT``）解引用并递增。如果该空闲槽位被并发重新分配，``pkt->iface`` 可能读回 ``NULL`` （空指针解引用/崩溃），或读回过期/垃圾指针（错误递增写入/内存破坏）。该路径可在本地链路上远程且无需认证地到达：``handle_mld_query()`` （为 ``NET_ICMPV6_MLD_QUERY`` 注册）会通过调用 ``send_mld_report()`` -> ``mld_send()`` 来响应有效的 MLDv2 General Query（未指定多播地址，hop limit 1）。结果是可远程触发的网络栈拒绝服务，并存在较小的内存破坏可能性。修复方案会在发送前将接口缓存到局部变量中，并且不再在 ``net_send_data()`` 之后访问数据包。IPv4/IGMP 对应路径（``igmp_send``）已采用修正后的模式。

- `Zephyr 项目漏洞跟踪 GHSA-m23w-34pp-4h92 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-m23w-34pp-4h92>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107100 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107100>`_

- `PR 110659 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110659>`_

- `PR 110658 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110658>`_

- `PR 107369 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107369>`_

:cve:`2026-10638`
-----------------

Zephyr ICMPv6 RX 路径中在发送 echo reply 或错误后更新统计信息时的释放后使用

``subsys/net/ip/icmpv6.c`` 在数据包已交给 ``net_try_send_data()`` 之后，从 ``net_pkt`` 中读取网络接口。在 ``icmpv6_handle_echo_request()`` 和 ``net_icmpv6_send_error()`` 中，发送后的统计更新会对刚发送的数据包调用 ``net_pkt_iface(reply)`` / ``net_pkt_iface(pkt)``。发送路径（``net_try_send_data`` -> ``net_if_tx``）会在返回前取消引用该数据包，并可能将其释放回内存 slab——在未配置 TX 队列时（``CONFIG_NET_TC_TX_COUNT`` == 0），这会在 RX 线程中同步发生，否则驱动/L2 可能已通过异步方式将其释放。因此，``net_pkt_iface()`` 会解引用已释放（并可能已被重用）的 ``net_pkt``；当启用 ``CONFIG_NET_STATISTICS_PER_INTERFACE`` 时，过期的 ``iface`` 指针会被进一步解引用并写入（``iface->stats.icmp.sent++``），从而将释放后使用读取转变为通过受攻击者影响的指针进行写入。核心栈已在 ``net_core.c`` 中记录了此危险（“do not use pkt after that call”）并在发送前缓存 ``iface``；ICMPv6 调用方没有这样做。未认证的远程攻击者只需发送 ICMPv6 Echo Request（ping）或一个会引发 ICMPv6 错误的 IPv6 数据包（未知下一报头、分片重组超时、目标不可达），即可触发该缺陷，导致拒绝服务（通过崩溃）和潜在的内存破坏。受影响版本：启用 ``CONFIG_NET_NATIVE_IPV6`` 的 Zephyr 网络功能，大约从 v4.2.0 到 v4.4.0。修复方案会在发送前缓存接口指针，并将其用于所有统计更新；配套提交 86e21665d46 修复了 ICMPv4 中相同的缺陷。

- `Zephyr 项目漏洞跟踪 GHSA-m92g-94xv-wvw2 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-m92g-94xv-wvw2>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107100 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107100>`_

- `PR 110659 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110659>`_

- `PR 110658 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110658>`_

- `PR 107369 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107369>`_

:cve:`2026-10639`
-----------------

在 ``icmpv4_handle_echo_request()`` 中读取已发送 ICMPv4 echo-reply 数据包的 ``net_pkt_iface()`` 时的释放后使用

在 Zephyr 的原生 IPv4 栈中，``subsys/net/ip/icmpv4.c`` 里的 ``icmpv4_handle_echo_request()`` 会构建一个 echo-reply 数据包（``reply``），将其交给 ``net_try_send_data()``，然后在成功时调用 ``net_stats_update_icmp_sent(net_pkt_iface(reply))``。``net_try_send_data()`` 会将 ``reply`` 的所有权转移给 TX 路径（``net_if_try_queue_tx`` -> ``net_if_tx`` -> L2/driver send，或异步 ``net_if_tx_thread``），该路径可能在 stats 行运行之前将其 unref 到引用计数 0，并把 ``struct net_pkt`` 归还到其 slab（``net_pkt_unref`` -> ``k_mem_slab_free``）。``net_core.c`` 记录了这一确切约定（“the pkt might contain garbage already ... do not use pkt after that call”）。

因此，发送后的 ``net_pkt_iface(reply)`` 会从已释放（并可能已重新分配）的 ``net_pkt`` 中读取 ``reply->iface``，这是一次释放后使用读取；当启用 ``CONFIG_NET_STATISTICS_PER_INTERFACE`` 时，统计宏还会通过该值递增计数器，即通过过期或已回收槽位的指针进行解引用/写入。

任何对设备执行 ping 的远程主机都可在未认证的情况下到达该路径（``net_icmpv4_input`` -> ``net_icmp_call_ipv4_handlers`` -> ``icmpv4_handle_echo_request``），该路径受 ``CONFIG_NET_STATISTICS_ICMP`` 控制。影响是概率性地读取已回收的数据包内存，并在存在时序竞争时可能发生野指针写入，最可能导致接口统计信息损坏或可远程触发的崩溃（DoS）。

该缺陷于 2019 年（v1.14）引入，并一直存在于 v4.4.0 中。``net_icmpv4_send_error()`` 中的配套修改不属于释放后使用，因为它读取的是 ``net_pkt_iface(orig)``，即调用方拥有的接收数据包，该数据包在发送期间始终保持有效。修复方案会在发送前从仍在使用的接收数据包中缓存接口指针，并将其用于发送后的统计更新。

- `Zephyr 项目漏洞跟踪 GHSA-qhrf-w466-qmpw <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-qhrf-w466-qmpw>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107100 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107100>`_

- `PR 110659 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110659>`_

- `PR 110658 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110658>`_

- `PR 107369 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107369>`_

:cve:`2026-10640`
-----------------

IPv6 Neighbor Discovery（``ipv6_nbr.c``）中发送后读取 ``net_pkt`` ``iface`` 导致的释放后使用

Zephyr 的 IPv6 Neighbor Discovery 发送路径（``subsys/net/ip/ipv6_nbr.c`` 中的 ``net_ipv6_send_na``、``net_ipv6_send_ns``、``net_ipv6_send_rs``）在 ``net_send_data(pkt)`` 已成功返回之后，通过调用 ``net_pkt_iface(pkt)`` 来更新每接口 ICMP 发送统计信息。在成功路径上，网络栈拥有并释放数据包的引用（L2/驱动发送会对其 unref，例如 ``ethernet_send`` -> ``net_pkt_unref``），因此对于引用计数为 1 的新分配数据包，``net_pkt`` slab 块可能在统计行运行之前就被释放（未配置 TX 队列线程时为同步释放，否则可能通过并发 TX 线程释放）。

随后的 ``net_pkt_iface(pkt)`` 会从已释放的 slab 块中读取 ``pkt->iface``；当启用 ``CONFIG_NET_STATISTICS_PER_INTERFACE`` 时，加载得到的指针会被解引用，以递增 ``iface->stats.icmp.sent``，这是一次释放后使用（CWE-416）。如果该 slab 块在此期间被重新分配，则读取/递增将针对无关或受攻击者影响的内存，导致统计信息损坏、故障/崩溃（拒绝服务），或潜在的有限内存破坏。

任何未认证的链路上节点只需向启用了原生 IPv6 的 Zephyr 节点发送 ICMPv6 Neighbor Solicitation，即可到达存在漏洞的 Neighbor Advertisement 路径（``handle_ns_input`` -> ``net_ipv6_send_na``）。

受影响版本从 v3.3.0 到 v4.4.0；修复方案使用已有的 ``iface`` 参数，而不是访问已发送的数据包。未启用每接口统计信息的配置只会解引用全局计数器，不受内存安全方面的影响。

- `Zephyr 项目漏洞跟踪 GHSA-r74c-mr4m-7g9g <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-r74c-mr4m-7g9g>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107100 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107100>`_

- `PR 110659 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110659>`_

- `PR 110658 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110658>`_

- `PR 107369 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107369>`_

:cve:`2026-10641`
-----------------

Bluetooth HFP Hands-Free CIND 指示符解析中的越界写入（cind_handle_values）

Zephyr 的 Bluetooth Classic Hands-Free Profile（HFP）Hands-Free 角色解析器（subsys/bluetooth/host/classic/hfp_hf.c）存在越界写入。在 Service Level Connection 建立期间，HF 发送 AT+CIND=?，并在 cind_handle() 中解析 AG 的 +CIND: 响应，为每个列表项分配一个逐项计数器 ``index``，并对每个列表元素调用 cind_handle_values()。cind_handle_values() 随后写入 ``hf->ind_table[index] = i``，却没有校验 ``index`` 是否位于 struct bt_hfp_hf 的 20 元素 int8_t ind_table[] 数组范围内。由于解析器未对 +CIND: 列表项数量设置上限，远端 Attendant Gateway（设备通过 Bluetooth 连接的对端，可能是恶意的、被入侵的或被冒充的）可以发送包含超过 20 个可识别指示符条目的响应，使 ``index`` 任意增大，从而把一个由攻击者定位的小值写出数组之外，写入相邻的结构体字段（feature mask、SDP/version 状态、calls[] 数组、work/atomic 记账数据），并可能越过静态连接池槽位。这会造成内存破坏，并至少导致 Bluetooth 主机拒绝服务，只需一个畸形的 AT 响应即可触发，无需用户交互。同类消费方 ag_indicator_handle_values() 已执行了等价的边界检查；本次提交添加了同样的 ``index >= ARRAY_SIZE(hf->ind_table)`` 防护来弥补缺口。影响启用 CONFIG_BT_HFP_HF 的构建；该缺陷随最初的 HFP HF CIND 解析器引入（约 v1.7），一直存在到 v4.4.0。

- `Zephyr 项目漏洞跟踪 GHSA-wx5j-q6f2-59p3 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wx5j-q6f2-59p3>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107331 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107331>`_

- `PR 110765 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110765>`_

- `PR 110764 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110764>`_

- `PR 110763 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110763>`_

:cve:`2026-10642`
-----------------

CTS 硬件流控下 Zephyr PL011 UART 驱动中无上限的 TX 忙循环拒绝服务

Zephyr PL011 UART 驱动（``drivers/serial/uart_pl011.c``）在 ``pl011_irq_tx_enable()`` 中包含一个无界的软件循环；当 TX 中断屏蔽位（``PL011_IMSC_TXIM``）置位时，该循环会反复调用中断驱动的应用回调，用以规避控制器的电平跳变 TX 中断行为。

当启用 CTS 硬件流控（devicetree ``hw-flow-control`` 或运行时 ``UART_CFG_FLOW_CTRL_RTS_CTS``）且有线串口对端撤销 CTS 时，控制器停止排空 TX FIFO；此时只要应用仍有待发数据，``pl011_fifo_fill()`` 每次调用都会返回 0，因此永远不会禁用 TX 中断。循环条件始终无法清除，调用 ``uart_irq_tx_enable()`` 的线程（例如 Bluetooth HCI H4 驱动中的 ``h4_send()``）会无限自旋，挂起所在执行上下文并使传输停滞——这是一种拒绝服务（CWE-835）。

控制连接到 UART CTS 线路的设备的攻击者，可以在传输期间扣住 CTS 不置位来触发该挂起。由于该对端就是接在 UART 上的设备——它可能是可拆卸或外置模块（例如 HCI H4 链路上的板外 Bluetooth 控制器），而不是永久焊接在 PCB 上的部件——因此攻击向量被评为相邻（AV:A）而非物理；安全小组委员会应针对具体部署确认该向量。影响仅限可用性；不存在内存安全、机密性或完整性后果。

该存在漏洞的循环由提交 b783bc8448ef（2025 年 2 月）引入，并随 v4.1.0 至 v4.4.0 版本发布。修复方案是在 CTS 阻塞时跳出循环，并使能 CTS 调制解调器状态中断，以便在 CTS 重新置位时恢复传输。

- `Zephyr 项目漏洞跟踪 GHSA-3fgh-73jh-2q5j <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3fgh-73jh-2q5j>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 103684 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/103684>`_

- `PR 110768 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110768>`_

- `PR 110767 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110767>`_

:cve:`2026-10643`
-----------------

Zephyr ``recvmsg()`` 辅助数据路径中的堆越界写入（``insert_pktinfo`` 对控制缓冲区容量检查不足）

Zephyr 的 IP socket ``recvmsg()`` 实现（``subsys/net/lib/sockets/sockets_inet.c``、``insert_pktinfo()``）在写入一条由对齐的 cmsg 头部加负载组成的完整控制消息之前，仅使用负载长度（``msg->msg_controllen`` < ``pktinfo_len``）来校验用户提供的辅助数据（``msg_control``）缓冲区。由于校验遗漏了 cmsg 头部大小，长度落在校验不足窗口内的控制缓冲区（例如 64 位目标上 IPv4 ``IP_PKTINFO`` 的 16 至 27 字节，而单个元素实际占用 28 字节）能通过该防护，却会越过缓冲区末尾造成固定大小的越界写入，最多写出一个 cmsg 头部（约 12 字节）。

在 ``CONFIG_USERSPACE`` 下，``recvmsg`` 校验器会按 ``msg_controllen`` 的大小分配控制缓冲区的内核堆副本，并针对该副本运行实现，因此溢出会破坏内核堆内存，并可由非特权用户态线程触发；在 supervisor 模式下则会破坏调用者自身的缓冲区。

当应用使用过小的控制缓冲区调用 ``recvmsg()`` 且收到数据报时，在启用 ``IP_PKTINFO``/``IPV6_RECVPKTINFO`` （或 hoplimit/timestamping）的 UDP/IP socket 上即可触达该路径；被覆写字节的一部分（``ipi_addr`` 中的目的 IP）受所接收报文的影响。

修复方案让容量检查改用 ``NET_CMSG_SPACE(pktinfo_len)`` （对齐头部 + 对齐数据），并在缓冲区过小时返回 ``-ENOMEM``。受影响版本：v3.6.0 至 v4.4.0。

- `Zephyr 项目漏洞跟踪 GHSA-pvf7-7mrp-35w7 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-pvf7-7mrp-35w7>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 106464 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/106464>`_

- `PR 110668 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110668>`_

- `PR 110669 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110669>`_

- `PR 110670 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110670>`_

:cve:`2026-10644`
-----------------

Microchip SERCOM-G1（PIC32CM-JH）异步 UART RX 在 1 字节缓冲区下的越界写入

PIC32CM-JH SoC 系列使用的 Microchip SERCOM-G1 UART 驱动（``drivers/serial/uart_mchp_sercom_g1.c``）在其异步（DMA）接收路径中存在越界写入。当使用单字节接收缓冲区（``len == 1``）调用 ``uart_rx_enable()`` 且启用 ``CONFIG_UART_MCHP_ASYNC`` 时，RX 完成 ISR 会在 SERCOM DATA 寄存器中已有接收字节的情况下启动单次 DMA 传输。在该 SoC 上，外设触发的 DMA 启动时序会越过调用者提供的缓冲区末尾写入一个字节（CWE-787）。

溢出字节的值是已连接串口对端（相邻攻击者）提供的 UART RX 数据，而其大小和位置固定为紧邻缓冲区之后的一个字节。

利用该漏洞需要启用异步 UART 配置（树内 PIC32CM-JH 板默认未启用），且需要有一个使用单字节缓冲区启用 RX 的消费方；影响仅限于 RX 缓冲区相邻处的单字节内存破坏（可能导致崩溃/拒绝服务）。

该缺陷随 v4.4.0 发布。修复方案改用 CPU 读取第一个字节；对于单字节缓冲区完全不再执行 DMA，对于更大的缓冲区则按剩余 ``len-1`` 字节设置 DMA 长度。

- `Zephyr 项目漏洞跟踪 GHSA-xv2x-56j7-6wc3 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xv2x-56j7-6wc3>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107400 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107400>`_

- `PR 110750 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110750>`_

:cve:`2026-10645`
-----------------

从构造的文件系统镜像触发 Zephyr ext2 目录项遍历越界读取

Zephyr ext2 文件系统驱动（``subsys/fs/ext2``）在遍历目录块时信任磁盘上的目录项字段 ``de_rec_len`` 和 ``de_name_len``。``ext2_fetch_direntry()`` 仅以 ``de_name_len > EXT2_MAX_FILE_NAME`` 作为防护，但 ``de_name_len`` 是 ``uint8_t``，而 ``EXT2_MAX_FILE_NAME`` 为 255，因此该检查恒为假；函数随后会 ``memcpy`` 最多 255 个名称字节，而查找/readdir 路径会按未经校验的 ``de_rec_len`` 推进遍历。每个目录块被读入一个 ``block_size`` 大小的 slab 缓冲区，前面的目录项可通过其 ``rec_len`` 将 ``block_off`` 推到接近块末尾的位置，因此 8 字节头部读取和随后的名称 ``memcpy`` 可能越过块缓冲区末尾读取多达约 263 字节，进入相邻的堆/slab 内存。在 readdir 路径上，这些字节会通过 ``fs_dirent.name`` 返回给调用者，泄露相邻的内核堆内存；``de_rec_len`` 为 0 还会导致无进展的无限循环（拒绝服务），而 unlink 路径中针对未校验记录的 ``memmove(de, next, next_reclen)`` 则是另一个越界读/写来源。该缺陷可通过已挂载 ext2 卷上的任意基于路径的操作（open、stat、unlink、rename、mkdir）或目录列举触发，因此攻击者提供的存储介质（SD 卡、USB 大容量存储或其他方式挂载的镜像）上的构造或损坏的 ext2 镜像即可触发。受影响：Zephyr ext2 自 v3.5.0 引入起至 v4.4.0。修复方案在解析器中校验 ``rec_len`` 和 ``name_len``，并在所有遍历调用方中拒绝头部无法容纳于剩余块内或 ``rec_len`` 跨越块边界的目录项。

- `Zephyr 项目漏洞跟踪 GHSA-hwrh-9h3x-vccm <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hwrh-9h3x-vccm>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108226 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108226>`_

- `PR 110031 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110031>`_

- `PR 110033 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110033>`_

- `PR 110030 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110030>`_

:cve:`2026-10646`
-----------------

``zsock_getaddrinfo()`` 中 DNS 查询超时后未取消即重试导致的返回后使用（use-after-return）

Zephyr 的 BSD socket ``getaddrinfo()`` 实现（``subsys/net/lib/sockets/getaddrinfo.c``）将一个指向栈上状态对象的指针（``struct getaddrinfo_state ai_state``）作为异步 DNS 解析器查询的 ``user_data`` 传入。socket 层在一个信号量上等待，其超时被刻意设置为略长于解析器自身的单次查询超时。当该信号量等待仍然超时时（``-EAGAIN``）——这可能发生在解析器的超时工作因工作队列争用而被延迟时，或在文档所述的多重重试配置中 ``CONFIG_NET_SOCKETS_DNS_TIMEOUT`` 大于 ``CONFIG_NET_SOCKETS_DNS_BACKOFF_INTERVAL`` 时——修复前的代码会在不取消前一次查询、也不重置信号量的情况下重试该查询（``goto again``）。

前一次查询槽位仍在解析器中保持活动状态，其回调和作为 ``user_data`` 的栈指针依然存在，而 ``ai_state->dns_id`` 被覆写，导致这个过期查询再也无法被取消。随后通过 UDP 送达并按其 16 位事务 ID 匹配的 DNS 响应（在 ``dispatcher_cb()``/``dns_read()`` 中），或解析器自身延迟的查询超时工作，会针对此时已超出作用域的栈帧调用 ``dns_resolve_cb()``，通过该过期指针进行写入（``state->status``、``state->idx``、``state->ai_arr[]`` 以及 ``k_sem_give()``）。

由于触发响应经由网络送达，且其 16 位 ID 可被路径上或路径外的攻击者伪造/重放，因此这是一个可受网络影响的返回后使用问题，可能破坏被复用的栈内存，导致崩溃/拒绝服务或内存破坏。

修复方案在重试前按名称和类型取消已超时的查询，并重置本地信号量，从而消除过期回调路径。受影响版本：Zephyr v4.0.0 至 v4.4.0。

- `Zephyr 项目漏洞跟踪 GHSA-h752-vhmf-29w6 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-h752-vhmf-29w6>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107609 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107609>`_

- `PR 110774 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110774>`_

- `PR 110773 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110773>`_

:cve:`2026-10647`
-----------------

USB CDC-NCM 设备类在 TX 入队失败时的死锁拒绝服务

USB CDC-NCM 设备类（``subsys/usb/device_next/class/usbd_cdc_ncm.c``）在其以太网发送回调 ``cdc_ncm_send()`` 中忽略了 ``usbd_ep_enqueue()`` 的返回值。当入队失败时，该函数仍会调用 ``k_sem_take(&data->sync_sem, K_FOREVER)``，阻塞在一个仅由 bulk-IN 传输完成回调发出信号的完成信号量上。由于没有任何内容被入队，该回调永远不会触发，调用线程——一个共享的网络流量类 TX 线程——会在持有接口 TX 锁的情况下永久死锁，使传输停止直到重启（并泄漏发送缓冲区）。

入队失败发生在由所连接的 USB 主机控制的情形下：只要总线处于挂起状态（一种常规且可持续的主机操作），``usbd_ep_enqueue()`` 就返回 ``-EPERM``，而底层的 ``udc_ep_enqueue()`` 在断开连接、总线复位或端点禁用时返回 ``-EPERM``/``-ENODEV``。``cdc_ncm_send()`` 的防护只检查 ``DATA_IFACE_ENABLED`` 和 ``IFACE_UP`` 标志，而不检查挂起状态，因此在主机保持总线挂起期间发送的报文会走到失败的入队路径并使 TX 路径死锁。

现实中的触发场景是：在导出的网络接口处于活动状态且有流量待发时发生总线挂起——主机休眠、USB 选择性/自动挂起或 hub 电源管理——此后任何由设备发出的报文都会使该路径死锁，只能通过重启恢复。影响是主机 NCM 接口与 Zephyr 设备之间的虚拟网络连接持续丢失；由于死锁的线程是共享的流量类 TX 线程，其他网络接口的出站流量也可能停滞。不存在内存破坏或信息泄露。

该缺陷随 CDC-NCM 驱动引入，并随直至 v4.4.0 的各版本发布；修复方案是检查 ``usbd_ep_enqueue()`` 的返回值，并在阻塞等待之前释放缓冲区。

- `Zephyr 项目漏洞跟踪 GHSA-xcf7-r86m-5q9f <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xcf7-r86m-5q9f>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107126 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107126>`_

- `PR 110652 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110652>`_

- `PR 110653 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110653>`_

:cve:`2026-10648`
-----------------

MCUmgr 串口/控制台 SMP 传输在缓冲区池耗尽时的 NULL 指针解引用

``subsys/mgmt/mcumgr/transport/src/serial_util.c`` 中的 ``mcumgr_serial_process_frag()`` 在检查 ``smp_packet_alloc()`` 的结果是否为 ``NULL`` 之前，就先对其调用了 ``net_buf_reset()``。``smp_packet_alloc()`` 针对共享的 MCUmgr 报文池（``CONFIG_MCUMGR_TRANSPORT_NETBUF_COUNT``，默认 4）使用 ``net_buf_alloc(K_NO_WAIT)``，当池耗尽时返回 ``NULL``。在默认构建中，``net_buf_reset`` 中的 ``__ASSERT_NO_MSG`` 是空操作，因此 ``net_buf_simple_reset`` 会通过 ``NULL`` 指针写入（``buf->len = 0; buf->data = buf->__buf``），导致 fault/崩溃。

分片数据经由 MCUmgr 串口/UART/shell 控制台传输（``smp_uart.c``、``smp_raw_uart.c``、``smp_shell.c``）上攻击者可控的字节到达此代码，而几乎每个新报文开始时都会分配一个新缓冲区。串口/控制台链路上的攻击者可以洪泛该传输以耗尽这个 4 项缓冲区池，从而引发 ``NULL`` 解引用，使设备崩溃（拒绝服务）。

该缺陷在最初的 MCUmgr 重构之后引入，并随 Zephyr v4.4.0 发布。修复方案将 ``NULL`` 检查移到 ``net_buf_reset`` 之前。

- `Zephyr 项目漏洞跟踪 GHSA-j64f-h3ww-f32c <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-j64f-h3ww-f32c>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107812 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107812>`_

- `PR 108026 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108026>`_

:cve:`2026-10651`
-----------------

Bluetooth Classic SDP 属性解析中的越界读取（``bt_sdp_parse_attribute``）

``subsys/bluetooth/host/classic/sdp.c`` 中的 ``bt_sdp_parse_attribute()`` 只校验 SDP 记录缓冲区中包含类型标记字节加 2 字节属性 ID（检查 ``buf->len < 3``），但随后却通过 ``net_buf_simple_pull_u8()`` 读取第四个字节，即数据元素描述符（``type``）。由于 ``net_buf_simple_pull_u8()`` 在其唯一的边界防护（当 ``CONFIG_ASSERT`` 被禁用即生产默认配置时会被编译掉的 ``__ASSERT_NO_MSG``）之前就解引用了 ``buf->data[0]``，因此恰好三字节的记录（0x09 后跟 2 字节属性 ID）会造成越过逻辑缓冲区末尾的一字节读取。该解析器可由入站的远程可控数据触达：充当 SDP 服务器的 Bluetooth BR/EDR 对端返回的发现响应记录会被原样存入客户端接收缓冲区，并通过公开的 ``bt_sdp_get_attr()``/``bt_sdp_has_attr()``/``bt_sdp_record_parse()`` 辅助函数解析。该越界读取被限制为一个字节，且仅用作内部长度选择器，绝不会泄露给攻击者；随后的长度检查会拒绝该畸形记录。因此现实影响仅限于边界情况下的拒绝服务（仅当记录恰好结束于映射内存边界时才会 fault，或在 ``CONFIG_ASSERT=y`` 时确定性地触发 assert panic）。影响 Zephyr v4.3.0 和 v4.4.0；修复方案是在长度检查中加入 ``sizeof(type)``。

- `Zephyr 项目漏洞跟踪 GHSA-p93g-3r68-cj53 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-p93g-3r68-cj53>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107325 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107325>`_

- `PR 110850 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110850>`_

- `PR 110851 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110851>`_

:cve:`2026-10652`
-----------------

Zephyr DNS 解析器 TXT/SRV 记录解析中的越界读取（未校验的 ``rdlength``）

Zephyr 的 DNS 解析器（``subsys/net/lib/dns``）在 ``dns_unpack_answer()`` 中解析 DNS 响应里的资源记录，该函数只校验固定长度的 RR 头部（type、class、TTL、``rdlength``），并接受攻击者声明的任意 ``rdlength``，包括超出所接收数据报末尾的值。``resolve.c`` 中 ``dns_validate_record()`` 的 TXT 和 SRV 消费方随后通过 ``memcpy`` 从接收缓冲区读取最多 ``rdlength`` 字节（仅按记录类型的最大值截断，例如 ``DNS_MAX_TEXT_SIZE``，默认 64，而未按报文长度限制），且自身没有边界检查，并把结果传给应用的解析回调。恶意或被冒充的 DNS 服务器、伪造 UDP DNS 应答的路径上攻击者，或（在启用 mDNS/LLMNR 时）任意 LAN 节点，都可以构造截断的 TXT 或 SRV 响应，对相邻的接收池内存造成越界读取；被泄露的陈旧字节（先前 DNS 报文的残留内容/未初始化的池内存）会作为 TXT/SRV 记录内容返回给应用，构成信息泄露，并且在某些配置下可能跨越分配边界而 fault，导致拒绝服务。该读取是有界的（TXT 约 64 字节，SRV 约 6 字节）且为只读（无写入）。修复方案在 ``dns_unpack_answer()`` 这一唯一咽喉点处拒绝任何声明的 rdata 超出 ``dns_msg->msg_size`` 的记录。受影响版本：v4.3.0 和 v4.4.0。

- `Zephyr 项目漏洞跟踪 GHSA-3jxq-xx8g-q8j2 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3jxq-xx8g-q8j2>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107977 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107977>`_

- `PR 108844 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108844>`_

- `PR 108843 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108843>`_

- `PR 108845 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108845>`_

:cve:`2026-10653`
-----------------

非原子的 ``net_buf`` 引用计数在并发 unref 下导致双重释放/空闲链表破坏

Zephyr ``net_buf`` 库（``lib/net_buf/buf.c``）使用普通的非原子 C 运算符（``buf->ref++``、``if (--buf->ref > 0)``、``if (--(*ref_count))``）操作它的两个引用计数——每个头部的 ``buf->ref`` 以及每个可变/堆数据分配起始处的每数据块 ``ref_count``。

该 API 被文档描述为自同步：调用者可以跨线程共享同一个缓冲区（例如通过 ``k_fifo``），各持有者各自独立地调用 ``net_buf_unref()``，外部无需加锁。在真正的并发下（SMP，或单核上非原子加载与存储之间发生抢占而另一上下文又对同一缓冲区执行 unref），两个持有者可能观察到相同的先前引用值，并都认为自己持有最后一个引用。

对于堆/可变数据池（``mem_pool_data_unref``/``heap_data_unref``，用于 zbus 消息订阅者、当 ``CONFIG_NET_BUF_FIXED_DATA_SIZE=n`` 时的 IP 协议栈 RX/TX 缓冲区、capture、wireguard、ISO-TP 和 usbip），这会对同一块内存执行两次 ``k_heap_free()``/``k_free()``——造成堆元数据破坏，并因堆加固的 poison 模式而产生释放后使用。

对于每头部引用计数，任何池类型（包括 Bluetooth 和网络使用的固定数据池）都会把缓冲区两次归还到池的空闲 LIFO 中，从而破坏空闲链表，使后续分配将同一缓冲区交给两个所有者。

修复方案将两个引用计数都改为 ``atomic_inc``/``atomic_dec`` （把 ``buf->ref`` 覆盖到 ``atomic_t`` 大小的联合体中，并将数据块引用计数从 ``uint8_t`` 改为 ``atomic_t``）。

影响取决于是否真正存在并发，以及应用架构是否在多个独立的 unref 执行者之间共享同一缓冲区；触发条件是与报文内容无关的引用计数/时序竞争，因此外部攻击者对该竞争窗口至多只有微弱的间接影响。影响直至 v4.4.0 的所有 Zephyr 版本。

- `Zephyr 项目漏洞跟踪 GHSA-284j-5jm9-55hh <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-284j-5jm9-55hh>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108065 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108065>`_

- `PR 110853 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110853>`_

- `PR 110852 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110852>`_

:cve:`2026-10654`
-----------------

Zephyr Bluetooth Classic 中 RFCOMM 会话断开竞争导致会话/L2CAP 泄漏并拒绝后续 RFCOMM 服务

Zephyr Bluetooth Classic RFCOMM 主机协议栈（``subsys/bluetooth/host/classic/rfcomm.c``）中的一处竞争条件错误地处理了同时发生的双向会话断开。当本地设备已发起会话拆除（状态为 ``BT_RFCOMM_STATE_DISCONNECTING``，已发送 DISC，RTX 定时器已启动）而对端又并发地针对 dlci 0 发送自己的 DISC 帧时，``rfcomm_handle_disc()`` 会调用 ``rfcomm_session_disconnected()``，后者无条件地将会话强制置为 ``BT_RFCOMM_STATE_DISCONNECTED``，却从未调用 ``bt_l2cap_chan_disconnect()``。

由于恢复定时器也被取消，且在 DISCONNECTED 状态下后续的 UA 会被忽略，会话会永久卡死：底层 L2CAP 通道始终得不到释放，固定的 ``bt_rfcomm_pool[CONFIG_BT_MAX_CONN]`` 数组中的会话槽位也永远不会被回收（其 ``conn`` 指针保持设置状态）。

由于会话状态无效，之后在该连接上调用 ``bt_rfcomm_dlc_connect()`` 会以 ``-EINVAL`` 失败，因此该对端的 RFCOMM 服务被拒绝，反复出现还会耗尽会话池。DISC 帧由对端通过空口控制，但利用该漏洞需要对端的 DISC 与本地发起的断开发生碰撞（高复杂度的时序竞争）。影响仅为可用性/资源泄漏；不存在内存安全、机密性或完整性后果。该缺陷出现在已发布版本中（v4.4.0 及更早版本均存在）。

修复方案仅在会话尚未处于 DISCONNECTING 状态时才转换到 DISCONNECTED，从而保留正确的 L2CAP 拆除路径。

- `Zephyr 项目漏洞跟踪 GHSA-4m37-wp5x-hq4h <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4m37-wp5x-hq4h>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108089 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108089>`_

- `PR 110865 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110865>`_

- `PR 110864 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110864>`_

- `PR 110863 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110863>`_

:cve:`2026-10655`
-----------------

SNTP 异步客户端在 socket 服务仍在轮询该 socket 时将其关闭导致的释放后使用竞争

Zephyr 中的异步 SNTP 客户端（``subsys/net/lib/sntp/sntp.c``、``sntp_close_async``）在将 UDP socket 文件描述符从网络 socket 服务解绑后，立即在调用线程中直接关闭它，而未与 socket 服务的轮询线程同步。

socket 服务线程通过 ``zvfs_poll`` 轮询每个 socket；该函数（在 ``zsock_poll_prepare_ctx`` 中）会注册一个指向该 socket 的 ``net_context`` 的 ``k_poll_event`` （``&ctx->recv_q``），随后在不持有引用或锁的情况下阻塞在 ``k_poll`` 中。``net_context`` 对象从固定池（``contexts[CONFIG_NET_MAX_CONTEXTS]``）中分配，并在关闭后被复用。

当 ``sntp_close_async`` 由与轮询线程不同的线程调用时（在树内消费方 ``subsys/net/lib/config/init_clock_sntp.c`` 中，SNTP 超时处理程序运行在系统工作队列上，而 socket 服务线程正阻塞在对同一 fd 的 poll 上），关闭操作会释放并可能复用该 ``net_context``，而轮询线程仍有 poller 节点链接在这个已被释放的对象中，导致内核 poll 结构的释放后使用/对象混淆。

SNTP 超时路径是正常的无响应失败模式，因此丢弃或延迟 SNTP/NTP 响应的网络对端或路径外攻击者可以反复触发这种竞争性关闭（在 ``NET_CONFIG_SNTP_INIT_RESYNC`` 下还会周期性触发）。最可能的后果是网络线程崩溃（拒绝服务），当被释放的 context 槽位被重新分配时还可能发生内存破坏。

修复方案利用 ``NET_SOCKET_SERVICE_CLOSE_SOCKETS`` 机制，通过 ``net_socket_service_close`` 将关闭操作延迟到 socket 服务线程自身执行，使轮询的同一线程完成关闭，从而消除该竞争。受影响版本：v4.2.0 至 v4.4.0。

- `Zephyr 项目漏洞跟踪 GHSA-34wr-cg29-c4mw <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-34wr-cg29-c4mw>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108180 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108180>`_

- `PR 110860 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110860>`_

- `PR 110858 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110858>`_

:cve:`2026-10656`
-----------------

MAX32 USB 设备控制器传输完成处理程序中的 NULL 指针解引用拒绝服务

MAX32xxx USB 设备控制器驱动（``drivers/usb/udc/udc_max32.c``，compatible 为 ``adi_max32_usbhs``）在其 OUT 和 IN 传输完成处理程序中解引用端点缓冲区时未检查其是否为 ``NULL``。``udc_event_xfer_out_done()`` 在 ``buf = udc_buf_get(ep_cfg)`` 之后立即调用 ``net_buf_add(buf, ep_request->actlen)``，而 ``udc_buf_get()`` 在端点 FIFO 为空时返回 ``NULL``。

传输完成事件从中断上下文入队，并由驱动线程异步处理；在入队与处理之间，端点 FIFO 可能被主机控制的控制流排空——特别是每当新的 SETUP 报文到达时 ``udc_setup_received()`` 会排空 EP0 OUT/IN FIFO，出队/禁用/清除路径也同样会将其排空。

因此，用新的 SETUP 报文中止正在进行的 EP0 控制传输的 USB 主机（这是合法的 USB 行为）可以使过期的 ``XFER_OUT_DONE`` 事件在空 FIFO 上被处理，从而产生 ``net_buf_add(NULL, ...)``，即一次近乎 NULL 的指针解引用，触发 fault 并使设备崩溃。无需任何认证；攻击者就是设备所连接的 USB 主机（物理总线访问）。影响为拒绝服务（设备崩溃）。

该缺陷在加入 MAX32 UDC 驱动时引入，并随 Zephyr v4.4.0 发布。修复方案在 OUT 完成和 IN 完成处理程序中增加 NULL 缓冲区检查，并以 ``UDC_EVT_ERROR``/-ENOBUFS 提前返回。

- `Zephyr 项目漏洞跟踪 GHSA-58p9-6mjq-rf2m <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-58p9-6mjq-rf2m>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108447 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108447>`_

- `PR 109517 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109517>`_

:cve:`2026-10657`
-----------------

Zephyr DNS 解析器 mDNS 后缀检查中的越界读取（memcmp 越过字符串 NUL）

Zephyr 的 DNS 解析器在 ``dns_resolve_name_internal()`` 函数（``subsys/net/lib/dns/resolve.c``）中使用 ``memcmp(strrchr(query, '.'), ".local", 7)`` 检测 mDNS（.local）查询，该调用总是从后缀指针读取固定的 7 个字节。当解析出的主机名最后一个标签短于 7 个字节时（例如以 .org、.com、.net、.io 结尾或带尾随点），比较会越过字符串的 NUL 终止符读取 1-2 个字节。

主机名（``query``）是调用者提供的名称，经由标准的 ``getaddrinfo()``/``dns_get_addr_info()``/``dns_resolve_name()`` 路径传入，可被操作人员或远程输入影响（配置中的服务器名、解析出的 URL 或面向应用的接口）。

在没有任何余量的紧凑缓冲区上（例如用户态 ``getaddrinfo`` 调用中，主机名通过 ``k_usermode_string_alloc_copy`` 复制到恰好 ``strlen+1`` 字节），越界读取会跨越分配边界；如果该边界未被映射（保护页、MPU 下的内存域边界或地址消毒器），越界读取就会触发异常并导致拒绝服务。越界读取的字节从不会被返回，因此不存在信息泄露。

该缺陷仅在启用 ``CONFIG_MDNS_RESOLVER`` 时才会编译进来，自 v1.10.0 起就存在，修复方式是用 NUL 安全的 ``strcmp(ptr, ".local")`` 替换定长的 ``memcmp``。

- `Zephyr 项目漏洞跟踪 GHSA-76jh-3j5f-9vq4 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-76jh-3j5f-9vq4>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108372 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108372>`_

- `PR 110870 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110870>`_

- `PR 110867 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110867>`_

- `PR 110868 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110868>`_

:cve:`2026-10658`
-----------------

蓝牙 ISO 接收（``bt_iso_recv``）中因缺少 SDU 头长度校验导致的越界访问

``subsys/bluetooth/host/iso.c`` 中的 ``bt_iso_recv()`` 通过 ``net_buf_pull_mem()`` 从入站 HCI ISO Data 缓冲区取出 ISO SDU 头（4 字节）或带时间戳的 SDU 头（8 字节，当设置了时间戳标志时），且事先没有检查 ``buf->len``。上游 ``hci_iso()`` 处理程序会强制要求 ``buf->len`` 等于控制器声明的 ISO Data_Load 长度，因此恶意的或有缺陷的控制器，或已建立 CIS/BIS 上的邻近 BLE 对端，可以提供比 SDU 头更短的首个分片（``BT_ISO_START``）或单分片（``BT_ISO_SINGLE``）PDU。由于 ``net_buf_simple_pull_mem`` 仅用 ``__ASSERT_NO_MSG`` 保护长度（在禁用 ``CONFIG_ASSERT`` 时会被编译掉，而这是生产环境的默认配置），该取出操作会使 ``buf->len`` 下溢（``uint16_t``，例如 ``0 - 8 = 0xFFF8``），并把 ``buf->data`` 推进到有效数据之外：随后对 ``hdr->slen`` 和 ``hdr->sn`` 的读取就成为对相邻池内存的越界读取。对于多分片（START）情形，被破坏的缓冲区会保留为 ``iso->rx``，随后 CONT/END 分片的 ``net_buf_tailroom()`` 保护值会下溢到接近 ``SIZE_MAX``，使边界检查失效，并导致 ``net_buf_add_mem()`` 用 ``memcpy`` 把攻击者提供的分片数据写入远超 RX 池缓冲区的位置（越界写）。该缺陷影响启用了 ISO 接收的构建（``CONFIG_BT_ISO_RX``，由默认关闭的 LE Audio 选项 ``BT_ISO_PERIPHERAL``/``BT_ISO_CENTRAL``/``BT_ISO_SYNC_RECEIVER`` 选中），自 ISO 子系统引入（v2.6.0）以来一直存在，直至 v4.4.0。修复方式是在取出数据前增加显式的 ``buf->len < sizeof(*ts_hdr)`` 和 ``buf->len < sizeof(*hdr)`` 检查并丢弃该缓冲区。

- `Zephyr 项目漏洞跟踪 GHSA-26g8-rmpf-j6cw <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-26g8-rmpf-j6cw>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108603 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108603>`_

- `PR 111024 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111024>`_

- `PR 110959 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110959>`_

- `PR 110958 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110958>`_

:cve:`2026-10659`
-----------------

Zephyr Dhara FTL 磁盘驱动在日志恢复期间发生 flash 读取错误时的 NULL 指针解引用

Dhara flash 转换层磁盘驱动（``drivers/disk/ftl_dhara.c``）实现的 ``dhara_nand_*`` 回调在发生 flash 错误时，会无条件地通过调用者提供的 ``dhara_error_t *err`` 指针写入错误码（例如 ``dhara_nand_read`` 中的 ``*err = DHARA_E_ECC``，``dhara_nand_erase``/``prog``/``copy`` 中也是如此）。

上游 Dhara 库在其日志恢复二分查找过程中会以 ``err == NULL`` 调用这些回调：``find_last_checkblock()`` 调用 ``find_checkblock(j, mid, &found, NULL)``，后者把 NULL 指针传入 ``dhara_nand_read()``。每当挂载/初始化 FTL 磁盘时，该路径都会在 ``disk_ftl_access_init()`` -> ``dhara_map_resume()`` 期间执行。

如果在探测的某个检查点页上发生 flash 读取错误（无法纠正的 ECC、坏块、控制器错误），驱动会解引用并写入 ``NULL``，导致内核故障（拒绝服务）。触发条件是 NAND 介质的内容/健康状况，可能受介质磨损、诱发故障或损坏/精心构造的片上镜像影响。

修复方案将所有错误写入都改为通过库中 NULL 安全的 ``dhara_set_error()`` 辅助函数完成。影响引入该驱动的 Zephyr v4.4.0。

- `Zephyr 项目漏洞跟踪 GHSA-q28v-3729-f82g <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-q28v-3729-f82g>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108594 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108594>`_

- `PR 110955 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110955>`_

:cve:`2026-10660`
-----------------

蓝牙 BAP 广播助理中的共享重组缓冲区导致跨连接内存破坏

``subsys/bluetooth/audio/bap_broadcast_assistant.c`` 中的蓝牙 BAP 广播助理 GATT 客户端将远端的 Broadcast Receive State 数据重组到所有连接实例共享的单个文件级静态 ``net_buf_simple`` （``att_buf``，``BT_ATT_MAX_ATTRIBUTE_LEN`` = 512 字节）中，而 BUSY 标志、长读句柄以及重置/偏移状态却是按连接维护的。

当设备作为广播助理连接多个 Scan Delegator 外设时，来自不同连接的通知和长读回调会在共享缓冲区上交错：``notify_handler`` 中的追加操作（非 busy 分支中的 ``net_buf_simple_add_mem``）不做尾部空间检查，因此来自两个或更多 delegator 的接收状态通知会累积到同一个 512 字节缓冲区上，并且在配置的 ATT MTU 足够大（``BT_L2CAP_TX_MTU`` 最高 2000）且存在两到三个并发连接时，会越过缓冲区写入相邻的 .bss（``net_buf_simple_add`` 仅在调试构建中才断言）。

即使未达到溢出阈值，一个连接的 ``net_buf_simple_reset`` 也会在另一个连接的重组和 GATT 读取偏移仍在进行时把共享长度清零，从而把一个对端的数据混入另一个对端的解析过程中。恶意的或被攻陷的 Scan Delegator（或两个串通的对端）可通过 BLE 触发该问题，造成越界写（内存破坏/拒绝服务）和跨连接的数据破坏。

修复方案把缓冲区移入按连接的实例结构体，使每个连接重组到各自的缓冲区中。影响所有携带共享缓冲区版广播助理的 Zephyr 发行版，包括 v4.4.0 及更早版本。

- `Zephyr 项目漏洞跟踪 GHSA-73c7-3rh7-v5p9 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-73c7-3rh7-v5p9>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107563 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107563>`_

- `PR 111066 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111066>`_

- `PR 111065 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111065>`_

- `PR 111182 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111182>`_

:cve:`2026-10663`
-----------------

实验性 USB 主机栈中根 USB 设备的释放后使用/双重释放

在 Zephyr 的实验性 USB 主机栈（``CONFIG_USB_HOST_STACK``）中，``usbh_device_disconnect()`` （``subsys/usb/host/usbh_device.c``）在释放根 ``usb_device`` slab 对象时没有清除缓存的指针 ``ctx->root``。总线移除处理程序 ``dev_removed_handler()`` （``subsys/usb/host/usbh_core.c``）仅根据 ``ctx->root`` 决定要拆除什么，并且只检查它是否为非 NULL。

由于 UHC 控制器驱动（例如 ``uhc_max3421e``、``uhc_mcux_common``）直接从物理总线线路状态合成 ``UHC_EVT_DEV_REMOVED``，没有去抖或状态保护，具有物理 USB 访问权限的攻击者（或反复插拔自身连接的恶意设备）可以在根设备断开后再投递一次设备移除事件。处理程序随后会带着悬空指针再次进入 ``usbh_device_disconnect()``，锁定已释放对象内部的互斥锁（释放后使用），从设备链表中移除已释放的节点，并对已释放的块调用 ``k_mem_slab_free()`` （双重释放）。如果在此期间该 slab 块已被重新分配给新接入的设备，就会破坏一个仍在使用的对象。

影响是拒绝服务（崩溃）和内存破坏；攻击向量为物理/本地。该缺陷由 v4.4.0 的连接/断开重构引入，修复方式是在释放前于 ``usbh_device_disconnect()`` 中清除 ``ctx->root``。

- `Zephyr 项目漏洞跟踪 GHSA-26q8-xjq3-f5p6 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-26q8-xjq3-f5p6>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108796 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108796>`_

- `PR 111021 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111021>`_

:cve:`2026-10664`
-----------------

nRF70 Wi-Fi 驱动省电事件处理程序中的越界写（TWT 流数量未做限制）

``drivers/wifi/nrf_wifi/src/wifi_mgmt.c`` 中 nRF70 Wi-Fi 驱动的省电事件处理程序 ``nrf_wifi_event_proc_get_power_save_info()`` 会把 TWT（Target Wake Time）流表项从 ``nrf_wifi_umac_event_power_save_info`` 事件复制到调用者提供的 ``struct wifi_ps_config`` 的固定大小 ``twt_flows[WIFI_MAX_TWT_FLOWS]`` （8 元素）数组中，其循环次数来自事件中的 ``num_twt_flows``，却未对照 ``WIFI_MAX_TWT_FLOWS`` 校验，也未检查 ``event_len``。当 ``num_twt_flows`` 超过 8 时，处理程序会越过目标数组写入（该数组通常位于调用者栈上，例如 ``wifi ps`` shell 命令），即越界写入约 40 字节的 TWT 表项，同时还会越过事件缓冲区读取 ``twt_flow_info[i]``。该事件由 nRF70 协处理器固件在响应主机发起的省电 GET 时投递，因此要触发溢出需要固件发出畸形或越界的事件；信任边界是主机到受信任协处理器，而不是来自远端 AP 的直接写入，空口对流数量的影响是间接的，并且受 3 位 TWT 流 ID 空间的限制。受影响范围：启用 ``CONFIG_NRF70_STA_MODE`` 的构建，直至 v4.4.0 的各个发行版。修复方案会拒绝 ``num_twt_flows`` > ``WIFI_MAX_TWT_FLOWS`` 的事件，或 ``event_len`` 短于其所声称表项数的事件，并对调用者缓冲区增加 NULL 检查。

- `Zephyr 项目漏洞跟踪 GHSA-3r6j-pm38-r43m <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3r6j-pm38-r43m>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108849 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108849>`_

- `PR 109067 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109067>`_

- `PR 109068 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109068>`_

:cve:`2026-10665`
-----------------

WireGuard 接收路径上因入站报文长度未做限制导致的堆缓冲区溢出

在 Zephyr 的 WireGuard 子系统（``subsys/net/lib/wireguard``）中，``wg_crypto.c`` 里的 ``wg_process_data_message()`` 会在解密前把入站的传输数据载荷线性化到大小为 ``CONFIG_WIREGUARD_BUF_LEN`` 字节的固定池缓冲区中。调用 ``net_buf_linearize(buf->data, data_len, pkt->buffer, ..., data_len)`` 时把由攻击者控制的 ``data_len`` 同时作为目标容量和复制长度传入，使函数内部的 ``len = min(len, dst_len)`` 限制失效。``data_len`` 来自接收到的 UDP 数据报长度，仅由 ``wg_ctrl_recv()`` 做下界约束（没有上界）。当 ``data_len`` 超过 ``CONFIG_WIREGUARD_BUF_LEN`` 时——例如缓冲区长度被调低到链路 MTU 以下、链路 MTU 高于缓冲区大小，或通过超过该大小的 IPv4/IPv6 重组分片——底层 ``memcpy`` 会越过池缓冲区末尾写入，构成越界写（CWE-787）。该溢出发生在 Poly1305 认证检查之前，因此只需有效的接收方会话索引，而不需要有效的认证器，恶意的或被攻陷的对端（或驱动已建立会话的路径中间攻击者）可经由网络触发，造成远程内存破坏，并至少导致可靠的拒绝服务。该缺陷存在于 Zephyr 4.4.0 随附的 WireGuard 实现中。修复方案增加了显式的 ``data_len > CONFIG_WIREGUARD_BUF_LEN`` 拒绝检查，并修正 linearize 调用，改传 ``net_buf_max_len(buf)`` 作为目标容量。

- `Zephyr 项目漏洞跟踪 GHSA-3wqm-wgx2-9367 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3wqm-wgx2-9367>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108841 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108841>`_

- `PR 111084 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111084>`_

:cve:`2026-10667`
-----------------

Zephyr ``CONFIG_USERSPACE`` 动态内核对象跟踪中的 SMP 释放后使用，可由非特权用户线程触发

Zephyr 的动态内核对象跟踪（``kernel/userspace/userspace.c``，原为 ``kernel/userspace.c``）维护一个由动态分配的内核对象组成的双向链表（``obj_list``）。``k_object_wordlist_foreach()`` 中对该链表的遍历在 ``lists_lock`` 保护下使用 SAFE 迭代器（会缓存下一个节点）进行，但链表节点的移除和释放却在另外两个互不相交的自旋锁下进行：``k_object_free()`` 中的 ``objfree_lock`` 和 ``unref_check()`` 中的 ``obj_lock``。在 SMP 系统上，当一个 CPU 在 ``lists_lock`` 保护下遍历 ``obj_list`` 时，另一个 CPU 可能断开链接并 ``k_free()`` 掉迭代器缓存为下一个指针的 ``dyn_obj`` 节点，导致迭代器解引用已释放的内核内存（释放后使用/悬空链表遍历）。所有竞争操作都可以由非特权用户态线程通过系统调用触发：``k_object_alloc``/``k_object_alloc_size`` 和 ``k_object_release`` 经由 ``unref_check()`` （在 ``obj_lock`` 下）驱动移除，而 ``k_thread_abort`` 和线程创建则经由 ``k_thread_perms_all_clear()``/``k_thread_perms_inherit()`` （在 ``lists_lock`` 下）驱动遍历。因此，在 ``CONFIG_SMP`` + ``CONFIG_USERSPACE`` 构建上，被降权的用户线程可以跨越用户空间安全边界破坏内核的对象跟踪结构，导致内核内存破坏（可能提权）或内核崩溃（拒绝服务）。修复方案移除了 ``objfree_lock``，并将所有 ``obj_list`` 修改都在 ``lists_lock`` 下串行化，包括在 ``k_object_free()`` 中的查找+移除期间以及 ``k_thread_perms_clear()`` 中 ``unref_check()`` 前后一直持有该锁。影响 ``CONFIG_SMP`` + ``CONFIG_USERSPACE`` + ``CONFIG_DYNAMIC_OBJECTS`` 配置；该缺陷可追溯到 2019 年的自旋锁化改造（提交 8a3d57b6cc6，首个包含它的发行版为 v1.14.0），并一直影响到 v4.4.0。

- `Zephyr 项目漏洞跟踪 GHSA-9x5j-h3rh-x579 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9x5j-h3rh-x579>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108721 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108721>`_

- `PR 111067 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111067>`_

- `PR 111019 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111019>`_

- `PR 111018 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111018>`_

:cve:`2026-10668`
-----------------

Nuvoton NuMaker HSUSBD UDC 驱动中可由主机触发的控制端点卡死（拒绝服务）

Nuvoton NuMaker HSUSBD USB 设备控制器驱动（``drivers/usb/udc/udc_numaker.c``）会无条件地武装控制 Data IN 阶段（``numaker_hsusbd_ep_trigger`` 中的 ``base->CEPTXCNT = len``）。由于 HSUSBD 硬件无法解除先前传输已武装的控制 Data IN，USB 主机若取消正在进行的控制传输（超时）然后发送新的 SETUP 包，就会使驱动失步：新传输中可能发送过期数据，并且控制端点可能永久卡在 NAK 后续每一次控制传输的状态。

恶意或有缺陷的主机（驱动总线的物理/邻近攻击者）可以反复取消并重新发送 SETUP，使设备的 USB 控制端点卡死，令设备的 USB 功能无法服务（设备停止枚举/响应控制管道），直到发生 USB 复位或重新插拔。该缺陷是仅影响可用性的拒绝服务；FIFO 复制循环（受 ``net_buf`` 长度和硬件 BUFFULL 标志限制）以及 ``net_buf`` 生命周期与武装失步无关，因此不存在越界访问、释放后使用或信息泄露。

修复方案监视 IN token 和新 SETUP 事件（``k_event``），只有在存在 IN token 且没有新 SETUP 到达时才武装控制 Data IN，并在新 SETUP 到达时取消当前传输。影响使用 Nuvoton NuMaker HSUSBD 控制器的板卡（``CONFIG_UDC_NUMAKER`` 配合 ``DT_HAS_NUVOTON_NUMAKER_HSUSBD_ENABLED``）；该问题出现在 v4.4.0 中。

- `Zephyr 项目漏洞跟踪 GHSA-rm28-x84j-4qrx <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rm28-x84j-4qrx>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107010 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107010>`_

- `PR 110646 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110646>`_

:cve:`2026-10669`
-----------------

Xtensa MPU ``arch_buffer_validate()`` 整数溢出致使用户线程绕过系统调用指针校验

在启用 ``CONFIG_XTENSA_MPU`` 和 ``CONFIG_USERSPACE`` 构建的 Xtensa SoC 上，``arch/xtensa/core/mpu.c`` 中的 ``arch_buffer_validate()`` （该架构钩子用于验证用户态提供的缓冲区能否以所请求的权限被调用方用户线程访问）把返回值默认为 0（允许访问），仅在逐 MPU 区域的探测循环内部设置拒绝结果。当缓冲区取整后的范围在 32 位地址空间上回绕时（大小加对齐偏移接近 ``SIZE_MAX``，或 ``ROUND_UP(size + offset)`` 溢出为 0），循环执行零次迭代，函数在未探测任何 MPU 区域的情况下返回 0，即允许访问。

系统调用层的预检查（``K_SYSCALL_MEMORY_SIZE_CHECK`` / ``Z_DETECT_POINTER_OVERFLOW``）只能捕获裸的 ``addr+size`` 回绕，无法覆盖由 ``ROUND_UP`` 引起的回绕；而字符串路径（``arch_user_string_nlen`` -> ``arch_buffer_validate``）完全没有系统调用层的防护。

因此，非特权用户态线程可以把精心构造的 ``(addr, size)`` 传给任何通过 ``k_usermode_from_copy``/``to_copy`` 或 ``k_usermode_string_copy`` 校验用户缓冲区的系统调用，使本不应访问的内存通过校验；随后内核会代表该线程读取（泄露）攻击者选定的内核或其他分区内存，或在 ``write=1`` 时写入（破坏）这些内存，从而造成信息泄露、内存破坏、提权和拒绝服务。

受影响范围从 v3.7.0（加入 Xtensa MPU 用户空间支持）直至 v4.4.0。修复方案把默认值改为 ``-EINVAL`` （默认拒绝），增加显式的 ``size_add_overflow`` 检查，并且仅在整个范围都通过校验后才设置成功值。

- `Zephyr 项目漏洞跟踪 GHSA-4r4p-gh69-v6w4 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4r4p-gh69-v6w4>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109000 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109000>`_

- `PR 109239 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109239>`_

- `PR 109238 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109238>`_

- `PR 109236 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109236>`_

:cve:`2026-10670`
-----------------

``k_thread_name_copy()`` 系统调用校验器中可由用户触发的内核 NULL 指针解引用（拒绝服务）

``k_thread_name_copy()`` 系统调用的 ``CONFIG_USERSPACE`` 校验处理程序（``kernel/thread.c`` 中的 ``z_vrfy_k_thread_name_copy()``）会对调用者提供的线程指针调用 ``k_object_find()``，然后解引用返回的 ``struct k_object``，却没有检查它是否为 ``NULL``。只要传入的指针不是已注册（静态或动态）的内核对象，``k_object_find()`` 就会返回 ``NULL``。

修复前的防护检查的是 ``thread == NULL`` 而不是 ``ko == NULL``，因此非特权用户态线程用任何非 NULL 但未注册的指针（例如任意地址）调用 ``k_thread_name_copy()`` 都能通过 NULL 检查，随后校验器会通过 NULL 指针读取 ``ko->type``。

由于系统调用校验器运行在特权模式下，该 NULL 解引用属于内核态故障，会导致系统停机或重启，使不受信任的用户代码能够跨越用户空间安全边界使内核崩溃（拒绝服务）。marshaller 在校验前没有对线程参数做任何 ``K_SYSCALL_OBJ`` 校验，因此坏指针会直接到达缺陷处。

该缺陷影响同时启用 ``CONFIG_USERSPACE`` 和 ``CONFIG_THREAD_NAME`` 的构建，自 v2.0.0 前后引入该特例查找以来一直存在；v4.4.0 及更早版本均受影响。修复方案把防护改为在解引用前检查 ``k_object_find()`` 的返回值（``ko == NULL``）。

- `Zephyr 项目漏洞跟踪 GHSA-82h2-v4vm-q2g9 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-82h2-v4vm-q2g9>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109076 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109076>`_

- `PR 111088 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111088>`_

- `PR 111089 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111089>`_

- `PR 109364 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109364>`_

:cve:`2026-10671`
-----------------

用户线程可重新初始化正在使用的 ``k_pipe``，破坏内核等待队列（``CONFIG_USERSPACE``）

在 Zephyr 的内核管道实现中，``kernel/pipe.c`` 里的用户空间系统调用校验器 ``z_vrfy_k_pipe_init()`` 使用了 ``K_SYSCALL_OBJ()`` （要求内核对象已经初始化），而不是 ``K_SYSCALL_OBJ_NEVER_INIT()`` （会拒绝已初始化的对象）。因此在 ``CONFIG_USERSPACE`` 构建上，被授予 ``k_pipe`` 对象访问权限的非特权用户线程可以调用 ``k_pipe_init`` 系统调用来重新初始化一个正在使用中的管道。

``z_impl_k_pipe_init()`` 会无条件重置环形缓冲区、把 ``pipe->waiting`` 置 0，并重新初始化两个等待队列（对 ``pipe->data`` 和 ``pipe->space`` 调用 ``z_waitq_init``），既不会唤醒也不会处理当前阻塞在该管道上的线程。任何已经挂起在 ``k_pipe_read()``/``k_pipe_write()`` 中的线程都会变成孤儿：仍然被标记为挂起，``pended_on`` 指向已被清空的等待队列，``qnode_dlist`` 中仍保留着指向（现已重新初始化的）内嵌链表头的过期链接。

当这样的孤儿等待者稍后超时或被唤醒时，调度器会对其过期节点调用 ``sys_dlist_remove()``，通过悬空的 ``prev``/``next`` 指针写入内核等待队列/调度器结构，造成链表破坏（攻击者驱动的非法内核写）、丢失唤醒、线程无限阻塞以及静默的数据丢失。该缺陷使被降权的用户线程可以破坏与其他线程/分区共享的内核对象状态。

修复方案把校验器改为 ``K_SYSCALL_OBJ_NEVER_INIT()``，与现有 ``k_msgq_init`` 校验器保持一致，使用户线程无法再重新初始化正在使用的管道。易受攻击的代码随 v4.1.0 发布，并一直保留到 v4.4.0。

- `Zephyr 项目漏洞跟踪 GHSA-p8w8-3x99-mg8f <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-p8w8-3x99-mg8f>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109091 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109091>`_

- `PR 111101 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111101>`_

- `PR 111102 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111102>`_

:cve:`2026-10672`
-----------------

未终止的 URI 缓冲区导致 LwM2M 固件拉取（Package URI）中的越界读取

``subsys/net/lib/lwm2m/lwm2m_pull_context.c`` 用 ``memcpy(context.uri, uri, LWM2M_PACKAGE_URI_LEN)`` 把固件更新 Package URI 复制到固定的静态缓冲区（``context.uri``，大小由 ``CONFIG_LWM2M_SWMGMT_PACKAGE_URI_LEN`` 决定，默认 128），即恰好复制目标缓冲区大小且不做长度校验。Firmware-Update 对象把服务器提供的 Package URI（/5/0/1）保存在 255 字节缓冲区中，因此 LwM2M 管理服务器（或缺少强 DTLS 的会话上的路径中间攻击者）可以 WRITE 一个 128-254 字符的 URI；随后只有前 128 字节被复制进 ``context.uri``，且没有 NUL 终止符。该缓冲区随后会被 ``http_parser_parse_url(context.uri, strlen(context.uri), ...)``、基于 ``strlen`` 的 CoAP URI-path/PROXY-URI 选项追加以及 ``lwm2m_parse_peerinfo()`` 当作 C 字符串使用，导致对相邻静态内存的越界读取。越界读取到的字节会被附加到发往服务器的 CoAP 请求中（向服务器/代理泄露相邻设备内存的信息），并可能导致设备崩溃（拒绝服务）。该有漏洞的复制由 pull-context 重构引入（首个包含它的发行版为 v3.0.0），并一直存在到 v4.4.0；默认开启的 ``CONFIG_LWM2M_FIRMWARE_UPDATE_PULL_SUPPORT`` 路径受影响。修复方案增加 ``strlen(uri) >= sizeof(context.uri)`` 检查并返回 ``-ENOMEM``，同时改用 ``strcpy()``，从而保证缓冲区有界且以 NUL 终止。

- `Zephyr 项目漏洞跟踪 GHSA-rf6j-4mpp-j9mf <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rf6j-4mpp-j9mf>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108964 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108964>`_

- `PR 109235 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109235>`_

- `PR 109234 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109234>`_

- `PR 109233 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109233>`_

:cve:`2026-10674`
-----------------

NXP LPUART 驱动中的拒绝服务（硬故障）：不支持的运行时 UART 配置导致时钟保持关闭

NXP LPUART 串口驱动（``drivers/serial/uart_mcux_lpuart.c``）在启用 ``CONFIG_UART_USE_RUNTIME_CONFIGURE`` 时，会在 ``mcux_lpuart_configure()`` 开头调用 ``LPUART_Deinit()``，从而关闭 LPUART 外设时钟。请求的配置直到之后才校验（在 ``mcux_lpuart_configure_basic`` 中），对于不支持的校验位/数据位/停止位/流控值会返回 ``-ENOTSUP``，而此时时钟尚未重新开启。

结果，带不支持配置的 ``uart_configure()`` 请求会使 LPUART 处于时钟关闭状态；此后任何对 LPUART 寄存器的访问（``poll_out``/``poll_in``、中断处理或后续重新配置）都会在时钟被门控的外设上触发错误并升级为硬故障，导致系统崩溃。

``uart_configure()`` 是一个 Zephyr 系统调用，其校验器（``z_vrfy_uart_configure``）只检查 ``cfg`` 是否为可读用户内存，并原样转发调用者提供的配置，因此有权访问 LPUART 设备的非特权用户空间线程可以确定性地触发该故障，造成持久的全系统拒绝服务。

该问题在 v2.5.0 中引入，并在此修复之前的各个发行版中一直存在；修复方案移除了 ``LPUART_Deinit()`` 调用，改为仅禁用发送器/接收器，保持时钟运行。

- `Zephyr 项目漏洞跟踪 GHSA-mw68-r353-m3vf <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-mw68-r353-m3vf>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107186 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107186>`_

- `PR 111106 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111106>`_

- `PR 111105 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111105>`_

- `PR 111104 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111104>`_

:cve:`2026-10675`
-----------------

Bluetooth Mesh PB-ADV：已失效的配网链路被无限期保持，阻塞（重新）配网（拒绝服务）

在 Zephyr 的 Bluetooth Mesh PB-ADV 配网承载（``subsys/bluetooth/mesh/pb_adv.c``）中，``prov_msg_recv()`` 会在函数开头无条件重新调度配网协议看门狗定时器，位于 FCS 检查和 ``ADV_LINK_INVALID`` 检查之前。一旦配网尝试失败，``prov_failed()`` 会设置 ``ADV_LINK_INVALID``，而唯一的恢复路径是协议定时器触发（``protocol_timeout`` -> ``prov_link_close`` -> ``close_link`` -> ``reset_adv_link``，并重新启用扫描和未配网设备信标）。

BLE 广播信道上的远程未认证攻击者可以先诱发一次配网失败（例如发送畸形的通用配网 PDU），然后在同一 link ID 上以高于每个协议超时周期一次的频率发送任意通过 FCS 的 PB-ADV 事务 PDU（协议超时为 60 秒，OOB 输入/输出时为 120 秒）。由于即使在失效链路上每个这样的报文都会重置定时器，``protocol_timeout`` 永远不会触发，死链路永远不会被拆除，设备会一直停留在无法配网的状态：未配网信标被禁用，新的 Link Open 请求被拒绝。

PB-ADV PDU 的处理不需要认证，FCS 也是无密钥的 CRC，因此无需配对或预先信任，攻击者可以自行选择 link ID。其影响是持续拒绝配网/重新配网服务；不存在内存安全、机密性或完整性影响。

易受攻击的代码在直至 v4.4.1 的各个发行版中提供。修复方案把定时器重新调度移到 ``ADV_LINK_INVALID`` 检查之后（并把 FCS 检查移到重置之前），使已失效的链路无法再被传入报文维持存活。

- `Zephyr 项目漏洞跟踪 GHSA-4rwg-6mr4-55hc <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4rwg-6mr4-55hc>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109324 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109324>`_

- `PR 110910 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110910>`_

- `PR 110909 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110909>`_

- `PR 110911 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110911>`_

:cve:`2026-10677`
-----------------

``z_vrfy_k_poll()`` 中的内核堆内存泄漏使非特权用户线程能够耗尽内核资源池

``kernel/poll.c`` 中的 ``CONFIG_USERSPACE`` 系统调用校验器 ``z_vrfy_k_poll()`` 会通过 ``z_thread_malloc()`` 分配用户提供的 ``k_poll_event[]`` 的内核侧副本，然后校验每个事件的对象句柄。在此修复之前，校验在循环内联使用 ``K_OOPS(K_SYSCALL_OBJ(...))``，它会在不释放 ``events_copy`` 的情况下终止调用线程。

用户线程可以传入伪造的对象句柄并配合 ``num_events >= 1`` 来泄漏该分配；由于新创建的用户线程会继承父线程的 ``resource_pool`` （``kernel/thread.c``），攻击者可不断创建牺牲线程重复该泄漏，直至共享的内核 heap 被耗尽。一旦耗尽，来自该 pool 的合法内核分配（``k_queue`` 的分配节点、``k_msgq`` 的 buffer、后续的 ``k_poll`` 调用等）都会失败，造成系统级拒绝服务。

该修复把每个内联的 ``K_OOPS`` 替换为带条件的 ``goto oops_free``，以便在线程被终止前释放 buffer。影响从 v1.12.0（``k_poll`` 首次向用户态开放）到 v4.4.1 的 Zephyr 发行版。

- `Zephyr 项目漏洞跟踪 GHSA-r3cc-8wcr-xfj9 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-r3cc-8wcr-xfj9>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109361 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109361>`_

- `PR 111111 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111111>`_

- `PR 111112 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111112>`_

- `PR 109535 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109535>`_

:cve:`2026-10678`
-----------------

由未认证的 I2C 控制器触发的 Zephyr MCTP I2C+GPIO target 绑定空指针／越界写

Zephyr 中的 MCTP-over-I2C+GPIO target 绑定（``subsys/pmci/mctp/mctp_i2c_gpio_target.c``）在 ``mctp_i2c_gpio_target_write_received()`` 中逐字节处理来自 I2C 总线主机的伪寄存器写，却不校验写入顺序和接收 buffer。在受影响版本中，``MCTP_I2C_GPIO_RX_MSG_ADDR`` （数据）处理函数会解引用并通过 ``b->rx_pkt`` 写入，却未检查接收 buffer 是否已分配：如果控制器选择数据寄存器后直接写入一个字节，而没有先发送长度寄存器（正是该操作分配了 buffer），就会通过一个空或未分配的 ``mctp_pktbuf`` 指针写入攻击者选定的字节（即写入地址 0 之上某处可由攻击者推进的小偏移），造成内存破坏或 hard fault。

同一处理函数还采用先写入后检查的边界判断，因此在发送超过 255 个数据字节时会在 ``data[255]`` 处造成一字节的 heap 溢出。

由于 I2C target 回调被调用时携带的是由总线主机提供的原始字节，而该绑定不做任何认证，总线上的恶意或故障控制器无需任何前置协议状态即可触发这些问题，导致目标设备上的内存破坏和／或拒绝服务。

该漏洞代码是在加入 I2C+GPIO target 绑定时引入的，并随 Zephyr v4.3.0 和 v4.4.0 发布。修复方案把分配推迟到第一个数据字节并加上空指针检查，将缺失的长度视为 libmctp 会拒绝的零长度数据包，并把边界检查移到写入之前。

- `Zephyr 项目漏洞跟踪 GHSA-pmwm-5rcm-39rr <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-pmwm-5rcm-39rr>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109428 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109428>`_

- `PR 111118 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111118>`_

- `PR 111117 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111117>`_

:cve:`2026-10679`
-----------------

DesignWare SPI 驱动中可由 spi_transceive 系统调用触达的除零错误（本地 DoS）

DesignWare SPI 驱动（``drivers/spi/spi_dw.c``）在计算 SPI BAUDR 时钟分频值时使用 ``info->clock_frequency / config->frequency``，却没有校验 ``config->frequency``。

``spi_transceive`` 是 Zephyr 的 ``__syscall``，其 verify handler（``drivers/spi/spi_handlers.c``）会从用户空间复制调用者提供的 ``spi_config`` 而不检查 frequency 字段，因此被授予 DesignWare SPI 设备内核对象访问权限的用户空间线程可以传入 ``frequency = 0``，在 ``spi_dw_configure()`` 中触发无符号整数除零。

在 Cortex-M Mainline 上（``SCB->CCR.DIV_0_TRP`` 在 ``z_arm_fault_init()`` 中被置位）以及在 ARC 上（专用的 ``__ev_div_zero`` 向量），这会引发 CPU 异常，导致内核 fault 和本地拒绝服务。

修复方案用 ``-EINVAL`` 拒绝零频率以及高于 ``clock_frequency / 2`` 的频率（DesignWare SSI 数据手册要求的最小 SCKDIV 为 2）。该缺陷影响直至 v4.4.0（含）的所有 Zephyr 发行版；利用它需要 ``CONFIG_USERSPACE=y``，以及一个已被授予 SPI 驱动权限的非特权线程。不存在内存破坏或信息泄露影响。

- `Zephyr 项目漏洞跟踪 GHSA-3qcm-qwh2-v4hq <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3qcm-qwh2-v4hq>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 105452 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/105452>`_

- `PR 111121 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111121>`_

- `PR 111120 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111120>`_

:cve:`2026-10680`
-----------------

Zephyr BR/EDR L2CAP 配置请求处理中因 ``uint16_t`` 长度下溢导致的越界访问

Classic（BR/EDR）L2CAP 信令处理函数 ``l2cap_br_conf_req()`` 和 ``l2cap_br_conf_rsp()`` （``subsys/bluetooth/host/classic/l2cap_br.c``）把最小命令长度的校验对象错写为 ``buf->len`` （整个接收 PDU 中剩余的字节数），而不是 ``len`` （L2CAP 信令头中该命令的数据长度）。由于多个信令命令可以打包进同一个 PDU，``buf->len`` 可能大于某条命令的 ``len``。攻击者可发送一个头长度小于配置请求结构的 ``CONF_REQ`` 命令（例如 0），并在其后紧跟另一条命令，使 ``buf->len`` 仍然满足该检查。于是该检查错误通过，而 ``opt_len = len - sizeof(*req)`` 会让 ``uint16_t`` 下溢为接近 0xFFFF 的值。缺少 ``opt_len`` 与 ``buf->len`` 防护的配置选项循环随后借助不做运行时边界检查的 ``net_buf`` pull 原语，远远越过池化 ACL 接收 buffer 的末尾，造成对主机内存的越界读；当越界的选项字节编码出 MTU 或 flush-timeout 选项时，还会造成越界写。BR/EDR 信令通道在配对／加密之前就被处理，而与 SDP 等 L0 服务之间的 L2CAP 通道无需配对即可打开，因此处在无线电范围内、能够建立 ACL 连接的未认证对端就能触发该缺陷，导致内存破坏和拒绝服务（主机／设备崩溃）。该缺陷存在于包括 v4.4.0 在内的已发布版本中。修复方案在两个处理函数中都改为按 ``len`` 而不是 ``buf->len`` 进行校验。

- `Zephyr 项目漏洞跟踪 GHSA-vrwx-p97q-8854 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vrwx-p97q-8854>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109308 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109308>`_

- `PR 110661 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110661>`_

- `PR 110662 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110662>`_

- `PR 111405 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111405>`_

:cve:`2026-10681`
-----------------

``thread_idx_alloc()`` 中的 SMP 竞态使并发的 ``k_object_alloc(K_OBJ_THREAD)`` 调用者共享同一个内核对象权限槽位

在 Zephyr 的用户空间动态对象子系统中，``kernel/userspace/userspace.c`` 中的 ``thread_idx_alloc()`` 在未持有 ``lists_lock`` 的情况下，从全局 ``_thread_idx_map[]`` 位图分配新的线程权限索引。

在 SMP 系统上，两个用户态线程并发调用 ``k_object_alloc(K_OBJ_THREAD)`` 系统调用时，可能观察到同一个低位空闲 bit，执行同样的非原子 RMW 将其清零，并返回相同的 ``tidx``。

这两个新建的 ``K_OBJ_THREAD`` 对象随后被赋予相同的 ``thread_id``，因此这两个用户线程在每个内核对象的 ``perms[]`` 位域中别名到同一位：此后把某个内核对象的访问权限授予其中一个线程，就等于隐式授予另一个线程，从而破坏了用户空间 ACL 隔离。另外，alloc 中未加锁的 ``&=~BIT()`` 与 ``thread_idx_free()`` 中加锁的 ``|= BIT()`` 之间存在丢失更新的窗口，也可能泄漏线程索引池中的条目。

任何用户态线程都能通过不受限制的 ``__syscall`` ``k_object_alloc`` 触达该缺陷，其前提是启用 ``CONFIG_USERSPACE``、``CONFIG_DYNAMIC_OBJECTS`` 和 ``CONFIG_SMP``。该缺陷源于 2018 年加入每线程权限索引之时，存在于直至 v4.4.0（含）的每个发行版中。修复方式是在位图 RMW 和权限清除期间始终持有 ``lists_lock`` （并把原先自行加锁的 ``obj_list`` 遍历内联进来）。

- `Zephyr 项目漏洞跟踪 GHSA-j693-5rh5-8g8h <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-j693-5rh5-8g8h>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109616 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109616>`_

- `PR 111409 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111409>`_

- `PR 111410 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111410>`_

- `PR 111408 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111408>`_

:cve:`2026-10682`
-----------------

Zephyr ``log_filter_set`` 系统调用校验器中可由用户空间触达的越界写

``subsys/logging/log_mgmt.c`` 中，``log_filter_set`` 系统调用的用户空间校验器 ``z_vrfy_log_filter_set()`` 对 ``int16_t`` 类型的 ``src_id`` 参数执行了有符号比较：``src_id < (int16_t)log_src_cnt_get(domain_id)``。任何为负的 ``src_id`` （例如 -1）都能轻易通过该检查并被转发到 ``z_impl_log_filter_set``，进而传播到 ``filter_set()``，最终到达 ``get_dynamic_filter()``；后者把 ``source_id`` 当作无符号索引，用于访问链接器段数组 ``&TYPE_SECTION_START(log_dynamic)[source_id].filters``。

经 ``uint32_t`` 隐式转换后，``int16_t`` 的 -1 会变成 0xFFFFFFFF，使 ``log_dynamic`` 的索引远远越界，导致内核对 ``log_dynamic`` 段相邻的内存执行越界读和越界读-改-写（``LOG_FILTER_SLOT_GET/SET``）。

写入的值只是目标 32 位字中一个受限的 3 位日志级别槽位，但目标地址由攻击者选定（相对 ``log_dynamic`` 的一个小的负偏移），且该写入是在非特权用户线程发起系统调用后以超级用户模式进行的，从而提供了内核内存破坏／权限提升的原语。

启用 ``CONFIG_USERSPACE=y`` 和 ``CONFIG_LOG_RUNTIME_FILTERING=y`` 的任何构建都能触达该缺陷。该缺陷存在于 Zephyr v3.3.0 至 v4.4.1。修复方案把有符号边界检查改为无符号比较：``(uint32_t)src_id < log_src_cnt_get(domain_id)``，从而正确拒绝负值输入。

- `Zephyr 项目漏洞跟踪 GHSA-6vqh-mg7h-58qh <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-6vqh-mg7h-58qh>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109690 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109690>`_

- `PR 111418 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111418>`_

- `PR 111419 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111419>`_

- `PR 111417 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111417>`_

:cve:`2026-10683`
-----------------

总线主机可把 DesignWare I2C target 驱动永久卡在停滞状态（DoS）

在以 target/slave 模式工作的 Synopsys DesignWare I2C 驱动（``drivers/i2c/i2c_dw.c``）中，``rx_full`` 中断处理函数以 ``dw->state`` != ``CMD_SEND`` 作为调用 ``write_requested()`` 回调的条件，而 ``dw->state`` 只在 STOP 中断时才被重置为 READY。``START_DET`` 中断的处理函数位于 ``i2c_dw_slave_read_clear_intr_bits()``，本可在每次（重）START 时重置状态，但该中断从未被加入 ``i2c_dw_slave_register()`` 中启用的中断掩码，因此这条恢复路径成了死代码。

因此，如果 STOP 中断丢失（总线毛刺／复位，或并发的总线主机发出 STOP），或者总线主机发出方向相同的合法 WRITE-repeated-START-WRITE 序列，驱动就会永久停留在 ``CMD_SEND`` 状态，并且在该 target 的整个生命周期内再也不会调用 ``write_requested()``。

同一物理总线上的 I2C 主机可以故意触发该问题，使 I2C target 功能在此后所有写事务中都无法正常工作，并破坏上层使用者的组帧状态（例如 MCTP-over-I2C），从而造成需复位才能恢复的目标外设拒绝服务。

修复方案解除对 ``START_DET`` 的屏蔽，使状态在每次总线（重）START 时都被重置。其影响仅限于本地板级总线上的可用性；树内使用者不会出现内存破坏，因为其逐字节的 buffer 写入是单独做了边界检查的。

- `Zephyr 项目漏洞跟踪 GHSA-fj9c-r5qw-3639 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fj9c-r5qw-3639>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107537 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107537>`_

- `PR 111415 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111415>`_

- `PR 111414 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111414>`_

:cve:`2026-10684`
-----------------

coredump shell 打印已存储 dump 的目标代码时的越界读

在 ``subsys/debug/coredump/coredump_shell.c`` 中，``print_coredump_hdr()`` 把已存储的 Zephyr coredump 头中的 16 位 ``tgt_code`` 字段直接用作 ``coredump_target_code2str[]`` 的索引，而后者是一个固定的 7 元素字符串指针数组，没有任何边界检查。

当已存储 coredump 的 ``tgt_code`` >= 7 时，会越过数组末尾最多约 64K 个条目读取一个 ``char*``；该值会作为 ``%s`` 参数传给 ``shell_print``，后者将其解引用并当作字符串遍历。其结果是向 shell 用户泄露设备内存内容，或者在该越界指针未映射时发生崩溃。

该缺陷通过 ``coredump print`` shell 命令触达（``cmd_coredump_print_stored_dump`` -> ``pretty_print_coredump`` -> ``parse_and_print_coredump`` -> ``print_coredump_hdr``）。``tgt_code`` 字段由设备生成，在正常崩溃处理过程中处于合法范围内，因此触发该缺陷需要本地 shell 访问权限，并且能够植入或篡改 flash／内存后端中已存储的 coredump。

在 v4.2.0 中引入（commit 13abd7fe730），并一直存在于 v4.4.0；修复方式是把超出范围的代码收敛到 'unknown'（索引 0）条目。

- `Zephyr 项目漏洞跟踪 GHSA-9fw2-4429-49q8 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9fw2-4429-49q8>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109630 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109630>`_

- `PR 111421 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111421>`_

- `PR 111422 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111422>`_

:cve:`2026-10685`
-----------------

Bluetooth 主机 CCC 写响应处理函数中 GATT subscribe params 的释放后使用

Zephyr Bluetooth GATT 客户端 CCC 写响应处理函数 ``gatt_write_ccc_rsp()`` （``subsys/bluetooth/host/gatt.c``）在已经调用 ``params->notify(conn, params, NULL, 0)`` 之后，又调用了应用的 ``params->subscribe()`` 回调。

按照公开的 GATT API，带 ``NULL`` 数据的 notify 回调是文档规定的信号，表示订阅已终止、应用可以释放或重用 ``bt_gatt_subscribe_params`` 结构体；此后仍对该结构体调用 ``subscribe()`` 就是释放后使用，其中还包括通过已释放的 ``params->subscribe`` 函数指针发起间接调用。

该错误分支可以由邻近设备远程触达：当已连接的 GATT 服务端对端用 ATT Error Response 应答 CCC 写时，作为 GATT 客户端且调用了 ``bt_gatt_subscribe()`` 的 Zephyr 设备就会被引入这一调用顺序（对端提供的错误码经 ``att_error_rsp`` -> ``att_handle_rsp`` 流入 ``gatt_write_ccc_rsp``）。

对于在通知终止处理函数中释放或回收订阅参数的应用，这会导致内存破坏、崩溃（拒绝服务），甚至可能是受攻击者影响的控制流。修复方案调整了处理函数的顺序，使 ``subscribe()`` 回调在错误路径和取消订阅路径下都先于终止性的 ``notify(NULL)`` 执行。

- `Zephyr 项目漏洞跟踪 GHSA-29xh-jm2m-4qvx <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-29xh-jm2m-4qvx>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 99920 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/99920>`_

- `PR 111430 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111430>`_

- `PR 111429 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111429>`_

- `PR 111428 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111428>`_

:cve:`2026-10686`
-----------------

IPv6 转发路径缺少跳数限制递减，导致 Zephyr 路由器出现无界数据包环路（DoS）

Zephyr 的 IPv6 转发路径在重发被路由的单播数据包时从不递减 IPv6 跳数限制。``ipv6_route_packet()`` （``subsys/net/ip``）的两条路由分支都受影响：显式路由路径（``net_route_packet()``）和链路内跨接口路径（``net_route_packet_if()``）。二者都只设置数据包转发标志并调用 ``net_send_data()``，既不递减跳数限制，也不做超期检查。

根据 RFC 8200，跳数限制递减是限定数据包生存期并终止路由环路的机制；缺少它时，充当 IPv6 路由器的设备会无限中继循环的数据包。路径上攻击者若能诱发或利用瞬时 L3 环路，就能把它变成永久的转发风暴，造成转发设备和相邻链路的 CPU／带宽资源耗尽（可用性 DoS）；依赖跳数限制超期的路径发现和环路诊断也会失效。

**受影响的配置。** 在每个受影响发行版中，转发路径都要经 ``CONFIG_NET_ROUTE`` 进入（设置 ``CONFIG_NET_IPV6_NBR_CACHE`` 时默认启用），跨接口路由还需要 ``CONFIG_NET_ROUTING``。请注意，``CONFIG_NET_IPV6_FORWARDING`` 和 ``CONFIG_NET_IPV4_FORWARDING`` —— 它们出现在修复补丁和本公告的证据说明中 —— 是在路由选项被拆分并重命名时、即 v4.4.0 *之后* 才引入的；任何受影响发行版中都不存在这两个选项。审计 v4.4.1 或更早的配置时，应查找 ``CONFIG_NET_ROUTE`` 和 ``CONFIG_NET_ROUTING``。

**任何发行版中的 IPv4 都不受影响。** IPv4 转发路径（``route_ipv4.c`` 中的 ``net_route_ipv4_packet()``）在 v4.4.0 之后才加入，从未随发行版发布。其 TTL 递减和 IPv4 首部校验和重算作为同一修复的一部分进入了 ``main``，因此下面的证据说明会讨论它，但没有任何已发布版本可经 IPv4 触达。

受影响发行版为 v1.8.0 至 v4.4.1：v1.8.0 引入了 ``net_route_packet()``，v2.2.0 加入了 ``net_route_packet_if()``，二者都未递减跳数限制。v4.3.1 带有显式路由路径的修复但不含链路内路径的修复，因此同样受影响。``main`` 上已分别由 7d8f1afa7345（显式路由路径）和 589eadc74efa（链路内路径）修复。

- `Zephyr 项目漏洞跟踪 GHSA-4cg6-6jc4-2r6h <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4cg6-6jc4-2r6h>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109585 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109585>`_

- `PR 111451 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111451>`_

- `PR 111450 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111450>`_

- `PR 111449 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111449>`_

:cve:`2026-10687`
-----------------

在 2026-08-01 之前保密

:cve:`2026-10772`
-----------------

在 2026-08-01 之前保密

:cve:`2026-10773`
-----------------

DHCPv4 客户端消息类型名称查找中的越界读（net_dhcpv4_msg_type_name）

DHCPv4 客户端辅助函数 ``net_dhcpv4_msg_type_name()`` （``subsys/net/lib/dhcpv4/dhcpv4.c``）在完成一个有缺陷的边界检查后，去索引一个静态的 8 元素 ``const char *`` 名称表。该防护使用的是 ``msg_type <= sizeof(name)``，而不是 ``msg_type <= ARRAY_SIZE(name)``； ``sizeof`` 返回的是指针数组的字节大小（32 位目标上为 32，64 位目标上为 64），而不是元素个数 8，因此 9 到该字节大小之间的消息类型值都能通过检查，使 ``name[msg_type - 1]`` 越界读取数组末尾之外的内容。

``msg_type`` 的值来自 DHCP 的 MESSAGE TYPE 选项，该选项是从收到的数据包中按未经检查的原始字节读取的（``net_pkt_read_u8``），并被原样传入该查找。因此 DHCP 服务器，或任何能向客户端所在链路注入伪造 DHCP 应答的主机，都能使该索引越界。越界的槽位会给出一个垃圾 ``const char *``，随后被 ``%s`` 日志转换解引用。

该查找只能从一条调试日志语句（``NET_DBG`` / ``LOG_DBG``）到达，因此只有在 DHCPv4 日志模块以 DEBUG 级别构建（``CONFIG_NET_DHCPV4_LOG_LEVEL_DBG``）时才能触发该越界读，而这并非默认配置。在该条件成立时，结果是越界读和野指针解引用：最可能是 DHCP 客户端崩溃（拒绝服务），也可能通过日志输出泄露相邻指针的内容。修复方案把 ``sizeof`` 换成 ``ARRAY_SIZE``，恢复了正确的 1..8 可接受区间。

- `Zephyr 项目漏洞跟踪 GHSA-r5hq-xq42-wcfq <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-r5hq-xq42-wcfq>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110135 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110135>`_

- `PR 112423 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112423>`_

- `PR 115146 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/115146>`_

:cve:`2026-10774`
-----------------

Bluetooth Mesh 子网删除中的 PSA 密钥槽泄漏，导致资源耗尽型 DoS

Zephyr 的 Bluetooth Mesh 子网密钥管理在每次拆除子网密钥时都会泄漏一个 PSA Crypto 密钥槽。在 ``subsys/bluetooth/mesh/subnet.c`` 中，``net_keys_create()`` 在 ``CONFIG_BT_MESH_PRIV_BEACONS`` （默认启用）下把 Private Beacon Key 导入一个 PSA 密钥槽，但 ``subnet_keys_destroy()`` 却用 ``CONFIG_BT_MESH_V1d1`` 保护对应的 ``psa_destroy_key()``。该 Kconfig 符号在显式 Mesh 1.0.1 支持被移除时已删除，因此销毁分支成了永久的死代码，导入操作永远不会被销毁操作配平。

每次销毁子网密钥时都会走到这一不配平的拆除逻辑：删除子网（Config Server 的 NetKey Delete）、完成密钥刷新过程（会淘汰旧的密钥集），以及复位／重新配网节点。这些空口触发路径只在节点的 device key 下处理，因此拥有该节点的配网器或网络管理员就能通过 Bluetooth Mesh 网络加以利用。

在 ``CONFIG_MBEDTLS_PSA_KEY_SLOT_COUNT`` 默认为 16 的情况下，反复执行添加／删除或密钥刷新大约十几轮后就会耗尽共享的 PSA 密钥槽池。一旦耗尽，``bt_mesh_private_beacon_key()`` 乃至子网创建都会失败：节点无法再添加子网或完成密钥刷新，设备上其他 PSA crypto 使用者也可能被饿死，直至设备重启。修复方案让销毁侧的防护与导入侧一致（``CONFIG_BT_MESH_PRIV_BEACONS``），从而释放每个槽位。

- `Zephyr 项目漏洞跟踪 GHSA-6q7g-798f-76p2 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-6q7g-798f-76p2>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110235 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110235>`_

- `PR 110438 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110438>`_

- `PR 110437 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110437>`_

- `PR 110436 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110436>`_

:cve:`2026-10848`
-----------------

Zephyr OCPP 1.6 RPC 消息解析器中的越界读（parse_rpc_msg）

``subsys/net/lib/ocpp`` 中的 OCPP 1.6 客户端在 ``parse_rpc_msg()`` （``subsys/net/lib/ocpp/ocpp_j.c``）里使用手写的辅助函数 ``extract_string_field()`` 解析传入的 WAMP RPC 帧，该函数用 ``strncpy(out_buf, token + 1, outlen - 1)`` 复制消息的 ``uid`` 和 ``action`` 字段，然后用 ``strchr(out_buf, '"')`` 扫描结果。由于当源串长度至少为 ``outlen - 1`` （127）字节时 ``strncpy`` 不会为目标串补 NUL 终止符，随后的 ``strchr`` 会越过 128 字节的目标 buffer 读入相邻栈内存；如果在 buffer 之外找到 ``"`` 字节，还会发生一字节的越界 NUL 写入。``extract_payload()`` 中还有一个相关缺陷：它对接收 buffer 执行 ``strchr``/``strrchr``，而该 buffer 在被最大长度帧填满时可能没有 NUL 终止符。

被解析的字节直接来自 websocket 上的 OCPP 中央系统服务器：读取线程通过 ``websocket_recv_msg()`` 填充 ``recv_buf``，并对每个入站 DATA 帧调用 ``parse_rpc_msg()`` （``subsys/net/lib/ocpp/ocpp.c``）。恶意或被攻陷的中央服务器，或者路径上攻击者（OCPP 常以明文 ``ws://`` 部署），可以发送 ``uid`` 或 ``action`` 字段长达 127 字节以上且没有结束引号的 RPC 帧，从而触发该越界访问。

主要影响是可远程触发的拒绝服务：无界扫描可能在未映射页面上触发 fault，而越界的 NUL 写入会破坏相邻的栈状态。越界读取的数据不会回传给对端，因此泄露有限。该功能为 EXPERIMENTAL，必须显式启用（``CONFIG_OCPP``）。修复方案把手写解析器改为尊重边界的 ``json_mixed_arr_parse()``，并用显式 NUL 终止的 buffer 复制提取出的 ``uid``，从而消除这两处越界读。

- `Zephyr 项目漏洞跟踪 GHSA-jgqq-7mjj-w642 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-jgqq-7mjj-w642>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 95399 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/95399>`_

- `PR 112426 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112426>`_

:cve:`2026-10849`
-----------------

Zephyr hawkBit OTA 客户端终止服务器响应体时的 heap 越界写

``subsys/mgmt/hawkbit`` 中的 hawkBit 设备管理客户端在 ``response_json_cb()`` （``subsys/mgmt/hawkbit/hawkbit.c``）里把来自更新服务器的 HTTP 响应体累积到一个 heap buffer 中。该 buffer 的大小仅够存放接收到的响应体字节，没有为终止 NUL 预留空间。当完整响应到达后，代码会写入 ``response_data[downloaded_size] = '\0'`` —— 而只要累积的响应体长度等于分配大小，该终止符就会落在 heap 对象末尾之后一个字节处（基于 heap 的越界写，CWE-122 / CWE-787）。

响应体长度和分片方式直接取自解析后的 HTTP 响应（``rsp->body_frag_start`` / ``rsp->body_frag_len``），完全由远端 hawkBit 服务器控制，因为它可以自行选择响应长度。确切的触发条件取决于 buffer 的增长方式，而两种形式都可远程触达。自 v4.0.0 起，重新分配的大小恰好等于 ``downloaded_size + body_len``，因此 **任何** 大于 1100 字节初始 buffer 的响应体都会使越界写成为确定行为；这类响应大小对 hawkBit 的部署元数据来说很常见。在 v4.0.0 之前，buffer 按倍增方式增长，而增长判断（``(downloaded_size + body_len) > response_buffer_size``）在相等时为假，因此当响应体长度恰好等于当前分配大小——默认初始 buffer 下即 1100 字节——时会完全跳过重新分配，并把终止符写到 1100 字节对象的 ``response_data[1100]`` 处。HTTP 的长度不匹配检查无法发现这一点，因为声明的长度与接收到的长度确实一致。两种形式都可由恶意、被攻陷或中间人更新服务器触发（TLS 是可选的，且即使启用也不能防御敌对服务器），因为响应内容没有任何认证，客户端也没有长度上限来保护该写入。

该越界写是紧跟在分配内存之后的一个固定 NUL 字节，会破坏相邻的分配器元数据或下一个分配块。实际影响是堆损坏，进而导致拒绝服务（后续分配或释放时出错），并且在受分配器实现限制的范围内还可能造成进一步损坏。修复方案是把缓冲区大小设为正文长度加一，并使用 ``memcpy`` 复制，确保终止符始终落在分配范围之内。

- `Zephyr 项目漏洞跟踪 GHSA-39h3-7phx-pwhv <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-39h3-7phx-pwhv>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109285 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109285>`_

- `PR 112429 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112429>`_

- `PR 112428 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112428>`_

- `PR 115262 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/115262>`_

:cve:`2026-11368`
-----------------

Bluetooth 主机 ATT TX 完成路径在传输中途断开连接时的释放后使用漏洞

Bluetooth 主机 ATT 层（``subsys/bluetooth/host/att.c``）通过静态数组 ``tx_meta_data_storage[]`` 把每个在途 ATT TX 缓冲区与其所属通道关联起来（``data->att_chan = chan``）。当缓冲区的最后一个引用被释放时，其 net-buf 销毁回调会把完成处理推迟到系统工作队列执行（``att_tx_destroy`` -> ``att_tx_destroy_work_handler`` -> ``att_on_sent_cb`` -> ``bt_att_sent``），其中 ``bt_att_sent`` 会解引用该通道及其 ATT 上下文（``sys_slist_get(&att->reqs)``）。

当某个 ATT PDU（服务器通知/指示或任何响应）仍在控制器 TX 路径中传输时对端断开连接，L2CAP 会在 ``l2cap_chan_del()`` 中拆除该通道：先运行 disconnected 回调，再运行 released 回调（``bt_att_released``），后者会释放通道的 slab 槽位。由于在途缓冲区由连接 TX 路径而非通道自身的队列持有，其延迟销毁工作可能在通道已释放之后才执行。本意是丢弃过期回调的 ``att_on_sent_cb`` 防护逻辑本身会解引用 ``meta->att_chan``，而该指针此时已变成指向已释放（且可能被复用）slab 槽位的悬空指针。

具有 ATT 连接的远程对端只需在常规 ATT 流量期间断开连接即可触发该漏洞；访问 ATT 承载无需配对或用户交互。其结果是已释放通道内存的释放后使用读写，会稳定地使 Bluetooth 主机崩溃（拒绝服务），而且由于通道 slab 槽位可能被复用，还可能破坏仍在使用的内存。

修复方案是在释放通道之前，让 ``bt_att_released()`` 把仍引用该通道的每个 ``tx_meta_data_storage[]`` 条目的 ``att_chan`` 字段置为 ``NULL``，这样延迟执行的防护逻辑会看到 ``NULL`` 指针并丢弃该回调。拆除流程与销毁工作都在协作式系统工作队列上运行，因此对数组的更新是串行化的，无需加锁。

- `Zephyr 项目漏洞跟踪 GHSA-85vg-gwc4-77g7 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-85vg-gwc4-77g7>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110416 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110416>`_

- `PR 112431 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112431>`_

:cve:`2026-11742`
-----------------

内核 ``k_queue_peek_head/tail`` 因缺少自旋锁导致的释放后使用竞态

``kernel/queue.c`` 中的内核队列辅助函数 ``z_queue_node_peek()`` 会解引用从队列 ``data_q`` 链表取出的节点，读取该节点的标志字节，并对通过 ``k_queue_alloc_append``/``alloc_prepend`` 入队的项读取内部分配的 ``alloc_node`` 结构中的数据指针。``z_impl_k_queue_peek_head()`` 和 ``z_impl_k_queue_peek_tail()`` 的实现执行这种读取和解引用时并未持有队列的自旋锁，而同一链表的所有其他访问者——包括会摘除节点并对其后备 ``alloc_node`` 调用 ``k_free()`` 的 ``k_queue_get()``——都在该锁保护下操作。

由于 peek 未做同步，同一队列上并发的 ``k_queue_get()`` （在 SMP 构建中，或在抢占/ISR 并发下）可能在 peek 取得节点指针之后、解引用之前释放该节点。这样 peek 就会从已释放且可能被重新分配的堆内存中读取标志位和数据指针，并向调用者返回过期或悬空的指针。``k_fifo`` 和 ``k_lifo`` 只是 ``k_queue`` 的薄封装，因此这会影响 ``net_buf``、Bluetooth、USB 和网络子系统中广泛使用的缓冲区队列；peek 操作还是 ``CONFIG_USERSPACE`` 线程可访问的系统调用。

其后果是可能泄露陈旧堆内容（一个字长的指针）的释放后使用读取；并且当返回的悬空指针随后被当作有效缓冲区使用时，解引用会导致系统崩溃或内存损坏。利用该漏洞需要本地访问并赢得一个很小的竞态窗口（例如用户态进程在共享队列上用 ``k_queue_peek_*`` 与 ``k_queue_get`` 竞争，或需要两个 CPU），因此实际影响有限，严重程度较低。

修复方案用 ``k_spin_lock``/``k_spin_unlock`` 对队列锁加锁来包裹两个 peek 实现，使读取并解引用的操作相对于并发的摘除并释放操作具有原子性，从而让 peek 与队列其余部分的加锁规则保持一致。

- `Zephyr 项目漏洞跟踪 GHSA-8xm3-4w69-29mm <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8xm3-4w69-29mm>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110576 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110576>`_

- `PR 112439 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112439>`_

- `PR 112438 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112438>`_

- `PR 112437 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112437>`_

:cve:`2026-11743`
-----------------

SF32LB MPI QSPI NOR flash 驱动缺少负偏移/溢出检查，导致越界读写

SF32LB MPI QSPI NOR flash 驱动（drivers/flash/flash_sf32lb_mpi_qspi_nor.c）在其读、写路径上用 ``(offset + size) > data->size`` 这一判断校验 flash 偏移和长度。由于 ``offset`` 是有符号的 ``off_t``，而 ``size`` 是无符号类型，负偏移会被转换为很大的无符号值，加法可能回绕成很小结果从而通过检查。随后读路径执行 ``memcpy(dst, (void *)(data->base + offset), size)``，写路径则在 ``offset`` 处编程 flash 并使 ``data->base + offset`` 的缓存失效，两种情况都会访问映射 flash 窗口之外的内存。驱动的擦除路径已经拒绝负偏移，但读和写路径没有。

在启用 ``CONFIG_USERSPACE`` 的构建中，``flash_read`` 和 ``flash_write`` 是系统调用，其验证器会校验设备对象和调用者的缓冲区，但有意把偏移边界检查交给驱动负责。因此，已被授予该 flash 设备访问权限的非特权线程可以用精心构造的负偏移和在其自身内存域中有效的缓冲区调用该系统调用，从而触达未做检查的访问。

最直接的影响在读路径：攻击者通过选择负偏移和与之匹配的 size，把 ``memcpy`` 的源地址移到 flash 基址之下，将任意 CPU 可寻址内存复制到自己的缓冲区，从而泄露其无权读取的内存。写路径还允许在越界地址编程 flash，并使攻击者选定的缓存范围失效，影响完整性和可用性。可达性要求启用用户态，并把原始 flash 设备对象授予不受信任的线程。

修复方案用 ``qspi_nor_range_is_valid()`` 取代原有检查，该函数会拒绝负偏移，并在两条路径上使用防溢出的 64 位算术进行边界比较；此外还增加了 SRAM DMA 弹跳缓冲区以及源/目标重叠拒绝逻辑，以防出现另一个 DMA 总线挂起问题。

- `Zephyr 项目漏洞跟踪 GHSA-c6wh-gwg4-fj5j <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-c6wh-gwg4-fj5j>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107793 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107793>`_

- `PR 112433 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112433>`_

- `PR 112434 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112434>`_

:cve:`2026-11809`
-----------------

UpdateHub 探测：对网络提供的元数据进行未初始化堆越界读取

``subsys/mgmt/updatehub/updatehub.c`` 中的 UpdateHub OTA 客户端在 ``z_impl_updatehub_probe()`` 中存在越界/未初始化内存读取。来自 UpdateHub 服务器的探测响应被复制到一个正确以 NUL 结尾的堆缓冲区（``metadata``），但第二个缓冲区（``metadata_copy``）由 ``k_malloc`` 分配（未清零），并用 ``memcpy(metadata_copy, metadata, strlen(metadata))`` 填充，该调用省略了结尾的 NUL。复制内容之后的所有字节仍是未初始化的堆内存。

当对数组描述符执行的第一次 ``json_obj_parse()`` 失败时，代码会回退到 ``json_obj_parse(metadata_copy, strlen(metadata_copy), ...)``。``strlen()`` 调用会越过已复制的字节在未初始化的堆中继续扫描，如果在分配末尾之前未找到零字节，就会读出缓冲区之外；得到的过长长度随后会被当作 JSON 解析。探测负载完全由 UpdateHub 服务器（恶意、被攻陷的服务器，或者在未启用可选的 ``CONFIG_UPDATEHUB_DTLS`` 时的路径中间攻击者）控制，它可以构造一个使首次解析失败的大负载来触发该路径。

后果是读取未初始化的堆，最坏情况下会越过 ``metadata_copy`` 分配范围进行越界读取，可能导致出错并使更新线程/设备崩溃，形成可由网络触发的拒绝服务。越界读取的数据仅在内部用于评估更新，不会返回给攻击者，因此不存在直接的信息泄露，也不存在越界写。

修复方案在复制之前用 ``memset`` 将 ``metadata_copy`` 清零，从而保证 NUL 结尾并把 ``strlen()`` 限制在分配范围之内。

- `Zephyr 项目漏洞跟踪 GHSA-6r86-hvv2-h6g4 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-6r86-hvv2-h6g4>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 104704 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104704>`_

- `PR 112445 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112445>`_

- `PR 112444 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112444>`_

- `PR 112443 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112443>`_

:cve:`2026-11810`
-----------------

UpdateHub OTA 代理在内层元数据数组为空时发生空指针解引用（远程拒绝服务）

UpdateHub 固件更新代理的探测处理函数（``z_impl_updatehub_probe()``，位于 ``subsys/mgmt/updatehub/updatehub.c``）会把更新服务器返回的 JSON 元数据解析到固定的两级嵌套数组结构中。解析之后，它只校验外层数组长度（``objects_len != 2``），随后就通过 ``strlen()`` 解引用 ``objects[1].objects[0].objects.sha256sum``，而没有检查元素 ``[1]`` 的内层对象数组是否非空。

该元数据是攻击者可施加影响的网络输入：代理在例行 OTA 探测期间通过 CoAP 从所配置的 UpdateHub 服务器获取它。恶意或被攻陷的更新服务器（或在 DTLS 被禁用时的网络中间人）可以返回第二个外层对象数组为空的响应。由于解析目标已零初始化，相应的 ``objects[1].objects[0].objects.sha256sum`` 指针为 NULL，随后的 ``strlen()`` 会解引用地址零。'any boards' 和 'some boards' 两种元数据布局都存在同一缺陷。

在 Zephyr 默认错误处理下，由此产生的 CPU 错误是致命的，会使设备停机或复位，因此该缺陷是可远程触发的拒绝服务。影响仅限于可用性；它是对 NULL 的读取，不存在越界写、内存损坏或信息泄露。修复方案在两种布局上都在任何解引用之前拒绝内层对象数组为空的元数据。

- `Zephyr 项目漏洞跟踪 GHSA-jfpc-324j-84ww <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-jfpc-324j-84ww>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 104704 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104704>`_

- `PR 112445 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112445>`_

- `PR 112444 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112444>`_

- `PR 112443 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112443>`_

:cve:`2026-11811`
-----------------

UpdateHub OTA 客户端 start_coap_client() 中的套接字文件描述符泄漏导致资源耗尽型拒绝服务

UpdateHub 空中升级客户端的 ``start_coap_client()`` （位于 ``subsys/mgmt/updatehub/updatehub.c``）在连接建立失败路径上会泄漏 CoAP/DTLS 套接字描述符。共享的 ``error:`` 清理逻辑以 ``ret > 0`` 标志作为关闭套接字的条件，但在套接字创建之后 ``ret`` 立即被置为 ``-1``，因此当 ``zsock_setsockopt()`` （DTLS）或 ``zsock_connect()`` 随后失败时该条件为假，``cleanup_connection()`` 从未被调用。全局 ``ctx.sock`` 中已打开的描述符会被下一次尝试覆盖，从而一直从套接字/net_context 池中泄漏，直到设备重启。

每当 OTA 客户端尝试联系 UpdateHub 服务器且连接无法建立时，就会进入这条失败的建立路径——该过程由周期性的 ``autohandler()`` 轮询自动驱动（也可通过 ``updatehub_probe()``/``updatehub_update()`` API 或 ``updatehub run`` shell 命令按需触发）。DTLS 握手/连接结果可被丢弃、重置或以其他方式干扰发往服务器流量的网络攻击者或路径中间攻击者影响，并且在服务器不可达时也会自然失败。

每次失败尝试都会永久泄漏一个描述符；一旦共享套接字池耗尽，整台设备的网络功能都会退化，直到设备重启，形成拒绝服务状况。严重程度为低，因为泄漏速率受所配置的 OTA 轮询间隔限制（默认每 24 小时一次），影响是渐进的且可通过重启恢复，并且只有启用了 UpdateHub 客户端的构建会受影响。不存在内存损坏、信息泄露或认证方面的影响。

- `Zephyr 项目漏洞跟踪 GHSA-q3mh-4wj7-mq7f <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-q3mh-4wj7-mq7f>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 104704 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104704>`_

- `PR 112445 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112445>`_

- `PR 112444 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112444>`_

- `PR 112443 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112443>`_

:cve:`2026-11812`
-----------------

UpdateHub：共享上下文上的竞态条件导致越界写和拒绝服务

UpdateHub 管理子系统（subsys/mgmt/updatehub/updatehub.c）通过一个文件作用域的单例 ``ctx`` 结构驱动所有更新操作，该结构保存 CoAP 块上下文、负载缓冲区、状态码、套接字以及单元素轮询 fd 数组 ``fds[1]``。对 ``ctx`` 的访问未做串行化，``prepare_fds()`` 在写入 ``ctx.fds[ctx.nfds]`` 并递增 ``ctx.nfds`` 时没有任何边界检查。

有两条独立路径会并发修改 ``ctx``：在系统工作队列上运行的后台 autohandler，以及通过 ``updatehub run`` shell 命令、直接 API 调用到达的用户触发操作，或者——由于这些操作以系统调用形式暴露——用户态线程。当第二条流程在 ``ctx.nfds`` 已为 1 时进入 ``prepare_fds()``，写操作会落在数组之后的一个元素位置；按结构体布局，它会与相邻的 ``ctx.sock``/``ctx.nfds`` 成员重叠。更广泛地说，这种未同步的共享会让两条流程交错执行连接建立与拆除，导致套接字描述符被重复关闭或共享缓冲区被破坏。

其结果是更新子系统内部状态被破坏，固件更新路径出现拒绝服务；越界写被限制在 ``ctx`` 结构内部，尚无已证明的路径可访问其外部内存或实现代码执行。触发需要能够调用更新操作的本地行为者（或者在启用 CONFIG_USERSPACE 时，一个非特权用户态线程），并能在时序竞争中胜过后台处理程序；远程对端无法控制该竞态时序。修复方案用互斥锁串行化各入口点，并为 ``prepare_fds()`` 增加边界检查。

- `Zephyr 项目漏洞跟踪 GHSA-vprh-rff6-46xp <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vprh-rff6-46xp>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 104704 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104704>`_

- `PR 112445 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112445>`_

- `PR 112444 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112444>`_

- `PR 112443 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112443>`_

:cve:`2026-11893`
-----------------

Bouffalo Lab HCI 驱动 send() 错误路径中的双重释放/释放后使用（hci_bflb）

用于 Bouffalo Lab 片上 BLE 控制器（BL60x/BL70x/BL61x）的 Bluetooth HCI 驱动，即 ``drivers/bluetooth/hci/hci_bflb.c`` 中的 ``bt_bflb_send()``，违反了 ``bt_hci_driver_api.send()`` 的缓冲区所有权约定。该约定（记录于 ``include/zephyr/drivers/bluetooth.h``）要求仅在成功时才消耗缓冲区引用；出错时调用者仍拥有该引用并自行 unref。而该驱动把所有错误路径都汇入一个共享标签，在返回错误码之前无条件调用 ``net_buf_unref(buf)``，于是失败时也消耗了缓冲区。

当 ``send()`` 返回错误时，主机 TX 路径（``subsys/bluetooth/host/conn.c`` 中的 ``send_buf()``）认为它仍拥有该缓冲区，于是再次 unref 同一个缓冲区。这种重复 unref 会使 net_buf 引用计数过度递减。由于该缓冲区是一个 TX 分片，其销毁回调还会递减仍在队列中的父缓冲区，父缓冲区会在仍可被连接 TX 队列访问时被提前释放，造成释放后使用并破坏共享的 net_buf 池，而不是无害的泄漏。

这些错误状况出现在主机到控制器的发送路径上（控制器发送失败，或不受支持的 H:4 数据包类型），因此并非由攻击者提供的无线数据字节直接驱动；远程/邻近对端只能间接影响它们，例如在链路负载很高时诱发控制器 TX 失败。一旦触发，后果是 BLE 协议栈拒绝服务（崩溃/池损坏），并可能带来进一步的内存损坏，影响范围限于使用这些 Bouffalo Lab 片上控制器之一的设备。

- `Zephyr 项目漏洞跟踪 GHSA-ph42-6rqx-728c <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-ph42-6rqx-728c>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110711 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110711>`_

- `PR 112558 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112558>`_

:cve:`2026-11894`
-----------------

Realtek BEE Bluetooth HCI 驱动 ``send()`` 错误路径中的双重释放/释放后使用

Realtek BEE Bluetooth HCI 驱动的发送回调，即 ``drivers/bluetooth/hci/hci_bee.c`` 中的 ``bt_hci_bee_send()``，违反了 ``bt_hci_driver_api`` 的缓冲区所有权约定。该约定要求驱动仅在成功时才消耗（unref）发送用的 ``net_buf``；返回错误时主机调用者保留所有权并自行 unref 该缓冲区。修复前的代码把所有错误路径都汇入一个共享清理标签，在返回错误码之前无条件调用 ``net_buf_unref(buf)``。

由于主机 TX 路径（位于 ``subsys/bluetooth/host/hci_core.c``）在 ``send()`` 返回错误后会再次 unref 该缓冲区，缓冲区被释放两次：驱动把它归还到 ``net_buf`` 池，而主机随后又 unref 已释放的缓冲区，从而破坏共享池/使引用计数下溢（CWE-415）。同一错误分支还在缓冲区已被 unref 之后于 ``LOG_ERR`` 调用中解引用 ``buf->len``，这是对已释放内存的读取（CWE-416），并且在默认错误日志级别下就会被编译进来。

当控制器的主机到控制器缓冲区分配失败或控制器发送失败（资源耗尽/IO 状况）时，就会走到这些失败分支。远程 Bluetooth 对端可以通过制造大量主机发送活动间接把设备推向这些状况，此时双重释放会破坏主机 ``net_buf`` 池并极有可能使设备崩溃，还残留进一步内存损坏的可能。影响仅限于使用该特定 Realtek BEE HCI 驱动的构建。

修复方案让每条错误路径提前返回且不做 unref，只在成功路径上 unref 缓冲区，从而恢复所有权约定，同时消除双重释放和释放后使用读取。

- `Zephyr 项目漏洞跟踪 GHSA-v9mj-h2m6-v9c6 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-v9mj-h2m6-v9c6>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110711 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110711>`_

- `PR 112558 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112558>`_

:cve:`2026-11985`
-----------------

ARM 上启用 FPU 但未启用寄存器共享时出现跨线程 FPU 寄存器泄漏

在 Zephyr 的 ARM 移植上，启用硬件 FPU（``CONFIG_FPU``）会强制选择 “Floating point ABI”，其默认值为 ``CONFIG_FP_HARDABI``。``FP_HARDABI`` 和 ``FP_SOFTABI`` 都允许编译器在任何函数中生成硬件 FP 指令，即使该代码从不使用浮点类型。然而，被调用者保存的 FP 寄存器（s16-s31 / d8-d15）只有在启用 ``CONFIG_FPU_SHARING`` 时才会在上下文切换中保存和恢复（``arch/arm/core/cortex_m/swap_helper.S`` 和 ``arch/arm/core/cortex_a_r/swap_helper.S``），而在本次修复之前，选择 ABI 并不会启用默认关闭的 FPU 寄存器共享。

在启用 FPU 并使用默认 ABI 但未启用 ``CONFIG_FPU_SHARING`` 的构建中，内核在线程切换时不会保存任何被调用者保存的 FP 寄存器状态。这种“非共享”模式所记录的前提条件——即始终只有一个线程执行 FP 指令——会被悄无声息地破坏，因为编译器可能在每个线程中都生成 FP 指令。

在 ``CONFIG_USERSPACE`` 下，线程之间相互隔离，该缺陷就变成跨越信息泄露边界的问题：受害线程可能在 s16-s31 中留下由机密派生的值，而同一设备上的非特权线程可以直接读取这些寄存器（FP 寄存器访问不受权限限制），从而恢复另一个线程遗留的数据。未启用用户态时，同一缺陷会导致跨线程 FP 状态损坏（正确性故障）。泄漏仅限于 16 个被调用者保存的单精度寄存器，且需要机会性触发，因此影响较低。

修复方案让 ``FP_HARDABI`` 和 ``FP_SOFTABI`` 选择 ``CONFIG_FPU_SHARING``，并在创建时为每个线程打上 ``K_FP_REGS`` 标记，从而在编译器可能生成 FP 指令时，被调用者保存的 FP 状态始终能在上下文切换中得到保留。

- `Zephyr 项目漏洞跟踪 GHSA-qxr9-wh3c-hvgv <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-qxr9-wh3c-hvgv>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110300 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110300>`_

- `PR 112547 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112547>`_

- `PR 112551 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112551>`_

- `PR 112550 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112550>`_

:cve:`2026-12051`
-----------------

USB DFU device_next 下载处理程序中的空指针解引用（handle_download）

Zephyr 新的（实验性） ``device_next`` USB 设备协议栈中的 USB DFU 类实现，在 ``handle_download()`` （subsys/usb/device_next/class/usbd_dfu.c）中存在空指针解引用。该处理程序计算 ``MIN(setup->wLength, buf->len)`` 并把 ``buf->data`` 传给镜像写入回调，却未检查 ``buf`` 这个 net_buf 指针是否非空。

该处理程序通过 USB 控制端点到达，由 USB 主机驱动。对于没有 Data OUT 阶段的 ``DFU_DNLOAD`` （下载）请求——特别是 DFU 协议用来结束固件传输的零长度终止下载——USB 核心会以 NULL 缓冲区调用类处理程序。在设备被推进到 ``DFU_DNLOAD_IDLE`` 状态之后（通过发送一个有效的下载块和一个 ``GET_STATUS``），零长度的 ``DFU_DNLOAD`` 会以 ``buf == NULL`` 到达 ``handle_download()``，从而解引用该指针。

其结果是 NULL+偏移读取，会触发致命的 CPU 错误，即拒绝服务（设备崩溃/复位）。攻击者是控制该设备所连接 USB 主机的任何一方；必须启用 DFU 下载支持并注册镜像。不存在内存损坏或信息泄露——影响仅限于可用性。修复方案增加了显式的 ``if (buf != NULL)`` 防护，使回调收到零长度、数据为 NULL 的传输而不会崩溃。

- `Zephyr 项目漏洞跟踪 GHSA-vhvq-q6rw-jvm4 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vhvq-q6rw-jvm4>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110830 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110830>`_

- `PR 112560 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112560>`_

:cve:`2026-12052`
-----------------

主机 wLength 小于响应长度时 USB CDC NCM 控制处理程序中的越界写

``subsys/usb/device_next/class/usbd_cdc_ncm.c`` 中 USB 设备端 CDC NCM 类的控制到主机处理程序 ``usbd_cdc_ncm_cth`` 为 ``GET_NTB_PARAMETERS`` （28 字节的 ``struct ntb_parameters``）和 ``GET_NTB_INPUT_SIZE`` （8 字节的 ``struct ntb_input_size``）类请求构造固定大小的响应，并用 ``net_buf_add_mem(buf, ..., sizeof(...))`` 把整个结构复制到控制 DATA IN 缓冲区，而忽略主机提供的 ``wLength``。

控制 DATA IN 缓冲区由 USB 协议栈按恰好 ``wLength`` 字节的容量分配（``usbd_ep_ctrl_data_in_alloc`` -> ``udc_ctrl_data_alloc`` -> ``net_buf_alloc_len(&udc_ep_pool, wLength)``；对 IN 端点不做向上取整）。由于 ``net_buf_add_mem``/``net_buf_simple_add`` 仅用 ``__ASSERT_NO_MSG`` 限制复制长度，而该断言在生产构建中会被编译掉，因此主机若以小于响应结构的 ``wLength`` （例如 ``wLength = 1``）发起这些标准 CDC NCM 控制请求之一，就会使处理程序 ``memcpy`` 超出所分配池缓冲区末尾最多 27 字节。

请求字段直接来自 USB SETUP 数据包，因此只要连接了使用 device_next USB 协议栈和 CDC NCM 类构建的镜像，Zephyr 设备所枚举对接的任何主机（或 USB 中间设备）都可以在无需认证的情况下触发该溢出。越界写会破坏共享 ``udc_ep_pool`` 中相邻的分配块和元数据，主要造成内存损坏和 USB 协议栈拒绝服务；溢出长度有限（<= 27 字节），写入内容是固定的设备常量，而且该缺陷不会读回任何数据，因此不存在信息泄露。修复方案用 ``MIN(sizeof(...), setup->wLength)`` 限制复制长度，与现有的 CDC ACM 处理程序保持一致。

- `Zephyr 项目漏洞跟踪 GHSA-vr4p-6rg5-qgpx <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vr4p-6rg5-qgpx>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110831 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110831>`_

- `PR 112615 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112615>`_

- `PR 112614 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112614>`_

:cve:`2026-12232`
-----------------

Intel ALH DAI get_properties 中因未校验 stream_id 导致的越界读取

``drivers/dai/intel/alh/alh.c`` 中的 Intel ALH 数字音频接口驱动函数 ``dai_alh_get_properties()`` 使用调用者提供的 ``int stream_id``，但没有做范围校验。该值用于索引固定大小的 ``static const uint8_t alh_handshake_map[64]`` 数组，并对一个 FIFO 寄存器地址进行缩放，因此超出范围的 ``stream_id`` 会在距数组起始位置的攻击者可控有符号偏移处产生一个字节的越界读取。该字节被写入 ``prop->dma_hs_id``，随后所得的 ``struct dai_properties`` 被复制回调用者，造成信息泄露。

``dai_get_properties_copy()`` 是一个 Zephyr ``__syscall``，其验证器 ``z_vrfy_dai_get_properties_copy()`` （``drivers/dai/dai_handlers.c``）只校验设备对象权限和目标缓冲区，不校验 ``stream_id``。因此，已被授予 ALH DAI 设备对象访问权限的用户态线程可以用任意 ``stream_id`` 调用该系统调用，从而跨越用户态/内核的沙箱边界。

其影响是每次调用可在任意偏移泄露一个字节的内核信息（并通过 ``fifo_address`` 泄露一个计算出的内核地址）；若 ``stream_id`` 解析到未映射页，则会在内核上下文中触发错误，造成本地拒绝服务。利用该漏洞需要 ``CONFIG_USERSPACE`` 和设备访问权限，因此属于本地、中等严重程度的问题。修复方案预先拒绝负数和过大的 ``stream_id`` 值并返回 NULL，复制包装函数会将其映射为 ``-ENOENT``。

- `Zephyr 项目漏洞跟踪 GHSA-3557-j848-pv24 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3557-j848-pv24>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110946 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110946>`_

- `PR 112747 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112747>`_

- `PR 112745 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112745>`_

:cve:`2026-12233`
-----------------

TLS 受信任凭据后端中未初始化的互斥锁在竞争下导致内核空指针解引用拒绝服务

PSA Protected Storage 凭据后端（subsys/net/lib/tls_credentials/tls_credentials_trusted.c）将其凭据存储互斥量声明为普通的清零 ``static struct k_mutex credential_lock;``，并且从未对其调用过 ``k_mutex_init()``。静态清零的 ``k_mutex`` 等待队列未初始化（其 dlist 头/尾为 NULL，而不是 ``k_mutex_init``/``K_MUTEX_DEFINE`` 安装的自引用哨兵）。无争用的加锁路径不会接触等待队列，因此该缺陷处于潜伏状态，串行使用时行为正确。

当两个执行上下文争用该锁时，``k_mutex_lock()`` 会通过 ``z_pend_curr()`` 把阻塞线程挂起到等待队列上，后者对清零的链表调用 ``sys_dlist_append()`` 并解引用为 NULL 的 tail 指针（``tail->next = node``），导致内核出错。该锁在 TLS 握手凭据加载期间以及所有凭据的添加/获取/删除操作中被持有，因此执行并发 TLS 握手的部署（例如服务器同时处理来自远端对等方的多个连接），或者与握手并发的凭据管理操作，都可能触发该解引用。

影响是拒绝服务：首次争用时就会发生确定性的内核 panic / 设备复位。除 NULL 解引用之外没有内存破坏，也没有机密性或完整性影响；快速路径上的互斥仍然正确。暴露范围仅限于启用了 ``CONFIG_TLS_CREDENTIALS_BACKEND_PROTECTED_STORAGE`` 的构建（PSA Protected Storage / TF-M 平台）；默认的易失性 RAM 后端会正确初始化其锁，不受影响。

修复方法是使用 ``K_MUTEX_DEFINE(credential_lock)`` 静态初始化该互斥量，从而提供有效的等待队列，使争用路径不再接触 NULL 链表。

- `Zephyr 项目漏洞跟踪 GHSA-57c4-xcq2-fqj7 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-57c4-xcq2-fqj7>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110943 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110943>`_

- `PR 112741 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112741>`_

- `PR 112740 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112740>`_

- `PR 112739 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112739>`_

:cve:`2026-12234`
-----------------

``zsock_sendmsg``/``recvmsg`` 用户空间验证器中的 TOCTOU 双重读取可导致内核堆越界写入

``subsys/net/lib/sockets/sockets.c`` 中的用户空间系统调用验证器 ``z_vrfy_zsock_sendmsg()`` 和 ``z_vrfy_zsock_recvmsg()`` 使用 ``k_usermode_from_copy()`` 把调用方提供的 ``struct net_msghdr`` 快照到内核侧副本，但随后又为后续判定重新读取仍然活动的用户结构体。内核 ``iovec`` 影子缓冲区的大小来自对 ``msg->msg_iovlen`` 的一次读取，而填充循环的边界却来自对同一字段的第二次实时读取。

由于 ``msg`` 指向普通用户内存，同一内存域中相互配合的第二个线程可以在确定大小的读取与循环判断之间的窗口内增大 ``msg->msg_iovlen`` 的值（典型的双重读取 / TOCTOU）。随后填充循环会越过实际分配的 ``net_iovec`` 槽位数量继续迭代，把受攻击者影响的 ``iov_base``/``iov_len`` 值写到内核堆影子缓冲区末尾之外。``recvmsg`` 验证器在其入站和结果回写这两个循环上都存在同样的缺陷。

只要启用了 ``CONFIG_USERSPACE`` 并且 ``zsock_sendmsg``/``zsock_recvmsg`` 系统调用可用，非特权用户线程即可到达该代码。成功的竞态会跨越用户到内核的特权边界破坏内核管理的堆内存，形成本地权限提升原语，或至少造成内核故障类拒绝服务。修复方法只复制一次头部，并基于该快照推导所有大小、边界和门控条件，同时原子地复制每个 ``iovec`` 条目，使其基址和长度不再可能被竞态拆开。

- `Zephyr 项目漏洞跟踪 GHSA-fcp3-vrr2-xfjv <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fcp3-vrr2-xfjv>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108079 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108079>`_

- `PR 112619 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112619>`_

- `PR 112624 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112624>`_

- `PR 112625 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112625>`_

:cve:`2026-12235`
-----------------

Xtensa llext PLT 重定位处理畸形 ELF 时的越界写入（CWE-787）

Linkable Loadable Extensions（llext）子系统在链接可重定位（部分链接）ELF 扩展时会错误处理 PLT/RELA 重定位条目。在 ``subsys/llext/llext_link.c`` 的 ``llext_link_plt()`` 中，可重定位分支（``tgt != NULL``，即用于 Xtensa 可重定位对象的路径）将补丁地址计算为 ``ext->mem[LLEXT_MEM_TEXT] - text.sh_offset + rela.r_offset + tgt->sh_offset``，然后在未校验 ``rela.r_offset`` 的情况下直接在那里执行重定位写入。其同类的共享/动态分支已经通过 ``llext_file_offset()`` 拒绝越界偏移。

``rela.r_offset`` 直接读取自 ELF 的 RELA 表，因此一个偏移量大于目标节的构造条目会让写入落在扩展 text 缓冲区之外任意远的位置。其结果是在链接时、任何扩展代码运行之前，在超级用户上下文中执行受攻击者影响的越界写入（写入位置由 ``r_offset`` 决定，写入的值为解析出的符号地址）。

当应用在具有可写存储的 Xtensa 上加载受攻击者影响的 ELF 扩展时，即可从 ``llext_load()`` 到达该路径；llext 的文档说明其可接受来源不可信的扩展。影响是超级用户上下文中的内存破坏（完整性、可用性损失，以及用户模式扩展的沙箱边界逃逸）。利用受限于 Xtensa 可重定位 PLT 路径和可写存储，且把越界写入转化为有用的原语并非易事。

修复方法增加了边界检查，拒绝任何 ``r_offset >= tgt->sh_size`` 的 RELA 条目，与共享分支中已有的校验保持一致。

- `Zephyr 项目漏洞跟踪 GHSA-xv9q-6mrf-8j49 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xv9q-6mrf-8j49>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109875 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109875>`_

- `PR 112635 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112635>`_

- `PR 112634 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112634>`_

- `PR 111541 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111541>`_

:cve:`2026-12236`
-----------------

Bluetooth GATT 客户端解析数据长度为零的 Read-By-Type 响应时出现无限循环（DoS）

``subsys/bluetooth/host/gatt.c`` 中的 Bluetooth 主机 GATT 客户端函数 ``parse_read_std_char_desc()`` 会在 ``BT_GATT_DISCOVER_STD_CHAR_DESC`` 发现过程中解析从远端 GATT 服务器收到的 ATT Read By Type Response。每个条目的步长 ``rsp->len`` 直接取自对端的 PDU，解析循环既用它测试退出条件（``length >= rsp->len``），又用它推进（``length -= rsp->len``、``pdu += rsp->len``）。在循环之前从未校验过 ``rsp->len`` 的最小值。

恶意或工作异常的对端可以回复 ``rsp->len = 0``。由于 ``length`` 是无符号数且永不减少，循环条件将永远为真，读指针也永不前进；只要正文至少有若干字节、包含非零句柄和匹配的描述符 UUID，主机就会反复重新解析同样的字节并调用发现回调，永不终止。这会使 Bluetooth 主机处理线程挂起（CWE-835，退出条件不可达的循环）。

一旦本地设备发起标准描述符值发现，任何已连接的对端都能触发该条件；GATT 发现不需要配对或加密，因此设备所连接的不经认证的邻近攻击者即可触发。影响是 Bluetooth 子系统拒绝服务（在资源受限的目标上很可能还会看门狗复位）；不存在内存泄露或破坏。

修复方法在循环之前增加了 ``rsp->len < sizeof(struct bt_att_data)`` 检查，拒绝长度不足的响应，从而使步长始终非零、循环能够终止。同类的 ``parse_include()`` 和 ``parse_characteristic()`` 解析器已经校验过 ``rsp->len``，不受影响。

- `Zephyr 项目漏洞跟踪 GHSA-483r-jq2x-5cp9 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-483r-jq2x-5cp9>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109066 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109066>`_

- `PR 112840 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112840>`_

- `PR 112839 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112839>`_

- `PR 112841 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112841>`_

:cve:`2026-7007`
----------------

Zephyr ext2 超级块解析中的除零问题可被构造的文件系统镜像触发 DoS

Zephyr ext2 文件系统在完成挂载之前会在 ``subsys/fs/ext2/ext2_impl.c`` 的 ``ext2_verify_disk_superblock()`` 中校验磁盘上的超级块。该校验器检查了魔数、块大小、修订版本和特性标志，但没有验证磁盘字段 ``s_blocks_per_group`` 和 ``s_inodes_per_group`` 为非零。这两个字段都直接读取自镜像，并在稍后的挂载初始化中用作除数。

在挂载过程中，``subsys/fs/ext2/ext2_diskops.c`` 中的 ``get_ngroups()`` 对 ``s_blocks_count`` 做除以和取模 ``s_blocks_per_group`` 的运算（经由 ``ext2_init_fs()`` 中的 ``ext2_fetch_block_group()`` 到达），而 ``get_itable_entry()`` 在获取根 inode 时用 ``(ino - 1)`` 除以 ``s_inodes_per_group``。因此，任一字段被置零的超级块都会在挂载序列中引发整数除零。

能够向挂载 ext2 的设备提供构造的 ext2 镜像的攻击者（例如 SD 卡或 USB 大容量存储设备等可移动介质）即可触发该问题。在 ARMv7-M / ARMv8-M-mainline Cortex-M 目标上，除零陷阱处于启用状态（``SCB_CCR_DIV_0_TRP``），因此该除法会引发 UsageFault，而 Zephyr 将其视为致命错误，从而造成拒绝服务。影响仅限于可用性；该畸形值仅被用作除数。

修复方法在超级块校验器中拒绝为零的 ``s_blocks_per_group`` 或 ``s_inodes_per_group``，并返回 ``-EINVAL``，使挂载在任何块组或 inode I/O 发生之前就失败。

- `Zephyr 项目漏洞跟踪 GHSA-wrf2-79mm-cvw5 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wrf2-79mm-cvw5>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107929 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107929>`_

- `PR 113331 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113331>`_

- `PR 110884 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110884>`_

- `PR 110883 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110883>`_

:cve:`2026-8023`
----------------

Zephyr HTTP 服务器静态文件系统资源处理器中的路径遍历允许未经认证的远程任意文件读取

Zephyr 的 HTTP 服务器（``subsys/net/lib/http``）提供静态文件系统资源类型（``HTTP_RESOURCE_TYPE_STATIC_FS``，在启用 ``CONFIG_FILE_SYSTEM`` 时可用），用于从配置的根目录提供文件。在此修复之前，HTTP/1 与 HTTP/2 前端都会把原始的、由攻击者控制的请求路径放入 ``client->url_buffer`` 中（HTTP/1 在 ``on_url()`` 中组装，HTTP/2 则逐字复制自 ``:path`` 伪首部），而不解析 ``.``/``..`` 段。随后静态 FS 处理器通过把配置的根与该原始 URL 直接拼接来构造磁盘上的文件名（在 ``http_server_http1.c:603`` 和 ``http_server_http2.c:490`` 处为 ``snprintk(fname, ..., "%s%s", static_fs_detail->fs_path, client->url_buffer)``），并用 ``fs_open(fname, FS_O_READ)`` 打开它。由于该处理器是通过通配符/前导目录匹配（``fnmatch`` ``FNM_LEADING_DIR``）或回退资源匹配到达的，诸如 ``GET /<prefix>/../../<file>`` 的请求会被分派到该处理器，并且在底层文件系统（例如 LittleFS/FAT）解析 ``..`` 段之后逃出配置的 Web 根目录，使未经认证的远程客户端能够读取挂载卷上任意可读文件（信息泄露）。到达该路径的 HTTP 服务器不需要 TLS 或认证。修复方法增加了 ``http_server_remove_dot_segments()``，它在两种协议处理器中于资源查找之前将 URL 的路径部分规范化，从而消除路径遍历。受影响的是注册了静态文件系统资源的部署中的 v4.0.0 至 v4.4.0 版本。

- `Zephyr 项目漏洞跟踪 GHSA-hch3-53g6-jj3h <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hch3-53g6-jj3h>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108531 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108531>`_

- `PR 111347 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111347>`_

- `PR 111346 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111346>`_

:cve:`2026-9728`
----------------

mbox_send 系统调用验证器中的 TOCTOU 竞态允许用户空间泄露内核内存

``drivers/mbox/mbox_handlers.c`` 中的用户空间系统调用验证器 ``z_vrfy_mbox_send()`` 通过直接读取活动的用户空间内存来校验嵌套的 ``msg->data``/``msg->size`` 字段，随后又把原始的、仍可变动的用户空间 ``struct mbox_msg *`` 指针转发给 ``z_impl_mbox_send()`` 和底层驱动。在校验访问与驱动实际使用 ``msg->data`` 之间，已校验的指针可能被替换，形成检查时间/使用时间窗口。

在使用 ``CONFIG_USERSPACE`` 构建的系统上，任何非特权用户空间线程都可以调用 ``mbox_send()`` 系统调用。与调用方共享地址空间的第二个线程可以在验证器的边界检查通过之后、驱动解引用之前，竞态地把 ``msg->data`` 覆盖为超级用户（内核）地址。随后驱动会在超级用户上下文中读取攻击者选定的地址（例如 NXP mailbox 驱动中的 ``memcpy(&data32, msg->data, msg->size)``，其字节随后被发送到对端邮箱端点）。

其影响是用户空间到超级用户的访问控制绕过：内核内存内容被泄露（高机密性影响），或者对于无效/未映射的目标地址，内核读取出错并造成拒绝服务。修复方法使用 ``k_usermode_from_copy()`` 把整个 ``struct mbox_msg`` 快照到内核栈副本中，并校验和转发这一不可变副本，从而消除该竞态。

- `Zephyr 项目漏洞跟踪 GHSA-47q2-w832-7w67 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-47q2-w832-7w67>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109946 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109946>`_

- `PR 110657 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110657>`_

- `PR 110656 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110656>`_

- `PR 113308 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113308>`_

:cve:`2026-9771`
----------------

flash_copy() 系统调用中缺少设备指针校验导致用户空间权限提升

``flash_copy()`` 系统调用由 ``drivers/flash/flash_util.c`` 中的 ``z_vrfy_flash_copy()`` 验证。在启用了 ``CONFIG_USERSPACE`` 的构建中，该处理器是用户模式调用方的内核侧信任边界。在修复之前，它只校验了输出缓冲区（``K_SYSCALL_MEMORY_WRITE``），并把两个 ``struct device *`` 参数 ``src_dev`` 和 ``dst_dev`` 直接传入实现，未做任何对象校验——这不同于所有同类的 flash 系统调用，后者都用 ``K_SYSCALL_DRIVER_FLASH`` 保护其设备指针。

用户模式线程完全控制 ``src_dev``/``dst_dev`` 的值及其自身地址空间的内容。实现 ``z_impl_flash_copy()`` 会解引用这些指针并通过其驱动 API 函数表调用（例如 ``api->get_parameters(dst_dev)``、``flash_read(src_dev, ...)``、``flash_write(dst_dev, ...)``）。通过提供一个指向伪造 ``struct device`` 的指针，并让其 ``api`` 表包含攻击者选定的函数指针，非特权线程就能使内核在超级用户模式下执行任意代码；否则，传入任意或无效地址会导致内核崩溃或越界读取。

其结果是逃出用户空间沙箱的本地权限提升（内核拒绝服务和信息泄露是次要后果）。修复方法在 ``z_vrfy_flash_copy()`` 中增加了 ``K_SYSCALL_DRIVER_FLASH(src_dev, read)`` 和 ``K_SYSCALL_DRIVER_FLASH(dst_dev, write)``，它们在任何解引用之前验证每个设备都是调用线程有权使用的已注册 flash 驱动内核对象，从而彻底关闭该路径。

- `Zephyr 项目漏洞跟踪 GHSA-68cj-3hg4-5vpm <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-68cj-3hg4-5vpm>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109962 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109962>`_

- `PR 110874 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110874>`_

- `PR 110873 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110873>`_

:cve:`2026-12363`
-----------------

LoRaWAN 分段传输中分片索引为 0 导致的越界写入

LoRaWAN 分段数据块传输服务（``subsys/lorawan/services/frag_transport.c``）在收到 ``DATA_FRAGMENT`` 命令后、将其转发给配置的解码器之前，不校验其中的分片计数器。在 ``frag_transport_package_callback()`` 中，值 ``frag_counter = hdr->frag_index_n & 0x3FFF`` 直接取自下行载荷并传给解码器，后者以 ``frag_counter - 1`` 推导数组索引和 flash 偏移。DataFragment 分片从 1 开始编号，因此 ``frag_counter`` 为 ``0`` 时该运算会发生下溢。

使用默认的 Semtech/LoRaMAC-node 解码器时，这会到达 ``FragDecoderProcess()`` 中的 ``FragDecoder.FragNbMissingIndex[fragCounter - 1] = 0;``，其中 ``fragCounter - 1`` 求值为 ``-1``，从而越界写入一个 ``uint16_t`` 零值，正好写在数组之前、并进入静态解码器对象相邻的 ``MatrixM2B`` 恢复矩阵状态（``CWE-787``）。与之相伴的写入会推导出野 flash 偏移，但该路径会被 ``flash_area_write()`` 的边界检查拒绝。树内的低内存解码器（``frag_dec()``）不会受损：其越界位数组和 flash 访问会被 ``sys_bitarray_*`` 和 ``flash_area_*`` 边界检查捕获。

该处理器是分段传输端口注册的下行回调，只要存在活动分段会话就可到达，因此触发字节是攻击者可以影响的 LoRaWAN/FUOTA 网络输入。触发它需要经过认证的下行（LoRaWAN MAC 会话密钥，或恶意/被攻陷的网络或 FUOTA 服务器）以及活动分段会话。影响是受限的：解码器状态被破坏、固件更新（FUOTA）会话被拒绝，而不是可控的内存破坏或代码执行。修复方法增加了传输层检查，拒绝 ``frag_counter == 0``，从而为两种解码器后端都关闭该缺陷。

- `Zephyr 项目漏洞跟踪 GHSA-fvm7-7whg-8gj6 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fvm7-7whg-8gj6>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111287 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111287>`_

- `PR 112928 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112928>`_

:cve:`2026-12364`
-----------------

日志系统调用 z_log_msg_static_create 中缺少用户空间指针校验，导致内核内存泄露和拒绝服务

``subsys/logging/log_msg.c`` 中的用户空间系统调用验证器 ``z_vrfy_z_log_msg_static_create()`` 是一个纯粹的直通实现：它把调用方提供的 ``source``、``desc``、``package`` 和 ``data`` 参数直接转发给内核模式实现 ``z_impl_z_log_msg_static_create()``，而没有执行任何必需的 ``K_SYSCALL_*`` 检查。由于 ``z_log_msg_static_create()`` 被声明为 ``__syscall``，在 ``CONFIG_USERSPACE`` 下任何非特权用户模式线程都能以完全由攻击者控制的参数直接调用它。

内核模式处理器会解引用这些不可信值中的每一个：``frontend_runtime_filtering()`` 以 ``struct log_source_dynamic_data`` 的形式通过 ``source`` 指针读取，``cbprintf_package_copy()`` 从 ``package`` 指针读取 ``desc.package_len`` 字节，而 ``z_log_msg_finalize()`` 从 ``data`` 指针用 ``memcpy()`` 复制 ``desc.data_len`` 字节。由于没有校验，用户线程可以提供任意的内核地址和任意长度，内核都会去读取。

影响是内核模式的拒绝服务（内核解引用攻击者选定的指针时出错），并且在日志后端输出对攻击者可见的情况下，还会把任意内核内存复制到生成的日志消息中造成泄露——这是对用户空间沙箱本应维护的用户/内核边界机密性的破坏。这些读取不会破坏内核内存，因此不存在越界写原语。

修复方法为验证器增加了必需的校验：它把 ``desc.package_len`` 限制在 ``Z_LOG_MSG_MAX_PACKAGE`` 之内，拒绝非 NULL 与长度不匹配的情况，并对 ``package``、``data`` 以及在启用前端运行时过滤时的 ``source`` 应用 ``K_SYSCALL_MEMORY_READ()``，因此任何越界或内核指针现在都会引发 ``K_OOPS``，而不再被接受。

- `Zephyr 项目漏洞跟踪 GHSA-h7rf-g9mg-g23f <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-h7rf-g9mg-g23f>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110506 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110506>`_

- `PR 112853 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112853>`_

- `PR 112854 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112854>`_

- `PR 116338 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/116338>`_

:cve:`2026-12365`
-----------------

SMP 时序竞态下 Zephyr 可延迟工作队列取消操作中的释放后使用

Zephyr 第二代工作队列（``kernel/work.c``）在处理可延迟工作超时时存在释放后使用问题。当一个可延迟工作项的超时已被出队、其处理函数 ``work_timeout()`` 正在执行（阻塞在获取工作队列自旋锁上）时，并发的取消操作不会等待该处理函数完成。修复前的代码在 ``unschedule_locked()`` 中调用 ``z_abort_timeout()``，而该函数对于已处于 announcing 状态的记录会返回 ``-EINVAL`` 且不移除它；随后 ``cancel_async_locked()`` 观察到该工作处于空闲状态，因此就连 ``k_work_cancel_delayable_sync()`` 和 ``k_work_flush_delayable()`` 也会在未阻塞等待正在执行的处理函数的情况下返回。

由于内核头文件把这些 API 记录为在释放 ``k_work_delayable`` 之前安全取消的方式，调用方在同步取消成功后立即释放对象时，就可能与仍未结束的处理函数发生竞态。随后 ``work_timeout()`` 会解引用已释放的记录：它通过 ``z_is_timeout_handler_canceled()`` 读取 ``to->dticks``，如果已释放的槽位被复用而使提前退出检查失败，还会对 ``wp->flags`` 中的 ``K_WORK_DELAYED_BIT`` 执行读-改-写，并针对过期的 ``dw->queue`` 指针提交工作——这是一次释放后使用的读和写。

``k_work`` API 仅限内核模式使用（没有 ``__syscall`` 入口点），因此这是内核内部的并发缺陷，而非用户空间权限提升。触发它需要 SMP 构建，以及某个子系统在其超时处于 announcing 状态的狭窄窗口内调度并随后释放（或重新调度）可延迟工作项；能够影响此类销毁时序的攻击者（例如通过连接抖动驱动子系统定时器）有一条可信但概率性的路径。影响是内核内存破坏或崩溃（拒绝服务）。

修复方法让 ``unschedule_locked()`` 等待：在释放并重新获取工作自旋锁的同时，对返回 ``-EAGAIN`` 的 ``z_try_abort_timeout()`` 进行自旋，直到任何正在执行的处理函数完成才返回；并把 ``work_timeout()`` 改为原子的 ``K_WORK_DELAYED_BIT`` 所有权。这同时关闭了先释放后由处理函数访问的释放后使用问题以及相关的重新调度提前触发竞态。

- `Zephyr 项目漏洞跟踪 GHSA-rhmh-r93p-6g99 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rhmh-r93p-6g99>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109977 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109977>`_

- `PR 112961 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112961>`_

:cve:`2026-12366`
-----------------

释放 Zephyr 用户空间对象销毁路径中已启动的动态分配 k_timer 时的释放后使用

Zephyr 的动态内核对象销毁路径 ``kernel/userspace/userspace.c`` 中的 ``unref_check()`` 在对象引用计数归零后释放其存储（``k_free(dyn->data)``），并且此前会执行按对象类型的清理。清理 ``switch`` 只处理了 ``K_OBJ_MSGQ`` 和 ``K_OBJ_STACK``；没有 ``K_OBJ_TIMER`` 分支。一个动态分配、已初始化并已启动的 ``k_timer`` 会让其内嵌的 ``struct _timeout`` dnode 保持链接在全局超时队列（``_timeout_q``）中，因此在未取消超时的情况下释放定时器存储就会在该队列中留下悬空节点。

当下次定时器到期时，超时机制会遍历 ``_timeout_q`` 并针对已释放的节点调用 ``z_timer_expiration_handler()``，从而在内核/ISR 上下文中解引用并写入已释放（且可被复用）的内核堆。这是一个确定性的释放后使用问题，不依赖于 SMP：该排队节点在释放时根本没有被解除链接。

在 ``CONFIG_USERSPACE`` + ``CONFIG_DYNAMIC_OBJECTS`` 下，非特权用户线程可以到达该销毁路径：持有此类定时器最后一个权限的线程通过 ``k_object_release()`` 系统调用将其释放（或在退出时通过 ``k_thread_perms_all_clear()`` 释放），并且该线程本身可以通过 ``k_timer_start()`` 系统调用启动该定时器。释放和到期处理函数以内核特权运行，而操作者是用户线程，因此该缺陷是可被用于权限提升的沙箱逃逸内存破坏原语。修复方法增加了 ``k_timer_cleanup()`` 函数（取消超时并等待任何正在执行的处理函数），并在释放之前对 ``K_OBJ_TIMER`` 调用它。

- `Zephyr 项目漏洞跟踪 GHSA-x96g-542c-gccq <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-x96g-542c-gccq>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 109977 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109977>`_

- `PR 112961 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112961>`_

:cve:`2026-12519`
-----------------

Zephyr WNC-M14A2A 调制解调器 socket 通知解析中的栈越界读取和写入

WNC-M14A2A LTE-M 调制解调器驱动（``drivers/modem/vendor_standalone/wncm14a2a.c``）中的 ``on_cmd_socknotifyev()`` 错误处理主动上报的 ``%NOTIFYEV:`` 事件。响应行通过 ``net_buf_linearize()`` 线性化到一个固定的 40 字节栈缓冲区中，该函数把复制量限制为 39 字节并返回 ``out_len <= 39``。然而，两个引号定界符扫描循环却以 ``len`` 为边界，即 ``net_buf_findcrlf()`` 返回的、包含 CR/LF 的完整帧长度，而不是以 ``out_len`` 为边界。

当一行超过 39 字节的 ``%NOTIFYEV:`` 在线性化区域内不含任何 ``"`` 时，循环索引 ``p1``/``p2`` 会越过 ``value[39]`` 读取相邻的栈内存，直到找到杂散的引号字节或索引达到 ``len``。这个越界读取的字符串随后被传给 ``strncmp()``/``atoi()``/``LOG_*``；而如果在越界处找到引号字节，后续的 ``value[p2] = '\0'`` 就会在受攻击者影响的偏移处执行单 NUL 字节的栈越界写入。

``%NOTIFYEV:`` 载荷携带来自网络的内容（``LTIME`` 网络时间、``SIB1`` 基站系统信息、``CSPS``/``RRCSTATE``），因此流氓蜂窝基站、恶意或被攻陷的调制解调器模块，或者诱导出过长通知行的射频操纵，都能在应用无任何交互的情况下到达该缺陷；该处理函数会在调制解调器 RX 线程中自动响应此主动上报事件运行。

影响是栈越界泄露（进入日志和解析过程）以及可能导致调制解调器 RX 线程崩溃的栈破坏（拒绝服务）。写入偏移仅受到微弱控制，因此未能证明可实现内存安全的代码执行。修复方法以 ``out_len`` 限制两个扫描循环，使所有访问都保持在线性化缓冲区内。

- `Zephyr 项目漏洞跟踪 GHSA-8hrc-q8cp-6xhf <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8hrc-q8cp-6xhf>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111243 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111243>`_

- `PR 113040 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113040>`_

- `PR 113042 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113042>`_

- `PR 113041 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113041>`_

:cve:`2026-12520`
-----------------

Zephyr HL7800 调制解调器 AT 响应处理函数中的栈缓冲区溢出和差一写入

Sierra Wireless HL7800 蜂窝调制解调器驱动（``drivers/modem/vendor_standalone/hl7800.c``，在 v4.4.0 及更早版本中位于 ``drivers/modem/hl7800.c``）使用大约二十个处理函数解析 AT 响应，这些处理函数调用 ``net_buf_linearize(value, sizeof(value), *buf, 0, len)`` 写入 128 字节栈缓冲区，然后执行 ``value[out_len] = 0``。由于 ``lib/net_buf/buf.c`` 中的 ``net_buf_linearize()`` 可能返回等于其目标长度参数的计数，一个恰好填满缓冲区的字段会使终止 NUL 落在缓冲区末尾之后一个字节处，即对相邻栈内存的单字节越界写入。

``+KCELLMEAS`` 小区测量处理函数 ``on_cmd_atcmdinfo_rssi()`` 更为糟糕：它把线路长度 ``len`` 作为目标大小传入（``net_buf_linearize(value, len, *buf, 0, len)``），因此长度超过 128 字节的响应行会用受攻击者影响的内容溢出 ``value`` 栈缓冲区。该行长度来自 ``net_buf_findcrlf()``，后者在整个 ``net_buf`` 分片链上累加字节而不受 128 限制，因此过长的行会到达该缺陷。

这些数据来自 UART 上的蜂窝调制解调器，受网络驱动：运营商扫描结果、``+CGCONTRDP`` IP/DNS 信息、socket 指示以及 ``+KCELLMEAS`` 邻区报告。能够影响调制解调器输出内容的攻击者——流氓基站、被攻陷的调制解调器基带，或塞入超大响应帧的远端对等方——可以驱动一行超过 128 字节。这些处理函数在内核上下文中于驱动的 RX 线程里运行，因此破坏发生在内核侧。

``+KCELLMEAS`` 路径是完整的栈缓冲区溢出，其最坏情况是在内核上下文中执行代码，最低限度则是必然崩溃；其余位置均为单字节 NUL 越界写入。利用该漏洞需要调制解调器发出超长的 AT 响应行，因此攻击复杂度较高，且需要相邻（蜂窝无线）攻击向量。修复方案改为传入 ``sizeof(dst) - 1``，并对 IMSI 与 ``+KCELLMEAS`` 相关位置显式使用正确的边界，从而使终止符始终保持在边界之内。

- `Zephyr 项目漏洞跟踪 GHSA-9xc4-j5x8-v6jx <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9xc4-j5x8-v6jx>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111243 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111243>`_

- `PR 113040 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113040>`_

- `PR 113042 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113042>`_

- `PR 113041 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113041>`_

:cve:`2026-12521`
-----------------

Zephyr HTTP 服务器在 zsock_poll() 虚假返回时破坏内核超时链表

``subsys/net/lib/http/http_server_core.c`` 中的 HTTP 服务器核心循环 ``http_server_run()`` 以无限超时轮询监听套接字、停止套接字和客户端套接字，并认为 ``zsock_poll()`` 返回 ``0`` 是不可能的，于是执行 ``break`` 并返回 ``0``，而未到达 ``closing:`` 清理分支。然而，``zsock_poll()`` （即 ``lib/os/zvfs/zvfs_poll.c`` 中的 ``zvfs_poll_internal()``）即使在无限超时的情况下也可能合法地返回 ``0``：``k_poll()`` 被唤醒后，``ZFD_IOCTL_POLL_UPDATE`` 处理过程可能发现所有 fd 都没有报告任何 ``revents`` （即虚假唤醒），从而得到 ``ret == 0``。

在这条路径上，``close_all_sockets()`` 被跳过，因此 ``close_client_connection()`` 中针对每个客户端的 ``inactivity_timer`` 取消操作（``struct k_work_delayable``）永远不会执行。控制权返回到 ``http_server_thread()``，此时 ``server_running`` 仍为 true，于是会重新进入 ``http_server_init()``。随后 ``http_server_init()`` 会通过 ``memset()`` 将 ``ctx->clients`` 数组清零，其中包括 ``k_work_delayable`` 超时节点，而此时仍有一个或多个这类定时器处于已装载状态，并链接在内核的 sys-timeout 链表中。

当内核稍后处理这类超时时，它操作的已是被重新初始化的对象，并会沿着已清零的链表指针进行访问，从而破坏内核超时链表并造成延迟故障。HTTP 服务器循环由未经认证的远程网络对端驱动（``CONFIG_HTTP_SERVER``，涵盖 HTTP/1/2/3），而连接的频繁建立与断开提高了虚假唤醒竞态出现的概率，因此远程对端可以影响触发条件。实际影响是因超时链表损坏而导致的拒绝服务（内核崩溃或挂起）。

修复方案把 ``break`` 替换为 ``continue``，在出现虚假的 ``0`` 返回时重新轮询，从而保持套接字及其已装载的定时器不变，并且绝不在定时器仍然存活时重新初始化上下文。

- `Zephyr 项目漏洞跟踪 GHSA-g5v9-xmfp-7gxm <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-g5v9-xmfp-7gxm>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111239 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111239>`_

- `PR 112942 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112942>`_

- `PR 112941 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112941>`_

- `PR 112940 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112940>`_

:cve:`2026-12522`
-----------------

Zephyr hl7800 调制解调器驱动解析网络提供的 +CGCONTRDP 地址字段时的栈缓冲区溢出

HL7800 蜂窝调制解调器驱动中处理 ``+CGCONTRDP:`` 响应的 ``on_cmd_atcmdinfo_ipaddr()`` 位于 ``drivers/modem/vendor_standalone/hl7800.c``，它会解析蜂窝网络分配给设备的 PDP 上下文动态参数（本地地址、子网掩码、网关和 DNS 服务器）。该响应被线性化到 256 字节的栈缓冲区中，随后各地址字段的长度根据网络提供的数据中逗号或 ``.`` 分隔符的位置计算得出，并被直接用作 ``strncpy()`` 的长度参数，复制到固定的 64 字节栈缓冲区 ``temp_addr_str`` 以及 16 字节的 ``iface_ctx.dns_v4_string`` 中。

由于字段长度来自攻击者可控的分隔符位置，且未根据目标缓冲区加以限制，单个字段可能远大于 64 字节。恶意或伪造的蜂窝网络（例如伪基站）可以返回带有超长地址字段的精心构造的 ``+CGCONTRDP`` 响应，使 ``strncpy()`` 越过调制解调器工作线程栈上的 ``temp_addr_str`` 进行写入，并在 ``temp_addr_str[addr_len]`` 处产生越界的 NUL 写入。

该漏洞不需要设备侧权限，也不需要用户交互：设备在正常网络附着过程中会自行发出 ``AT+CGCONTRDP=1`` 查询，并解析网络返回的任何内容。该溢出会破坏 supervisor 上下文中的相邻栈内存，至少会导致可远程触发的崩溃，在未启用栈保护的平台上还可能导致控制流劫持。

修复方案在每次复制前都根据目标缓冲区（``temp_addr_str`` 和 ``dns_v4_string``）限制每个字段的长度，并拒绝超长字段。

- `Zephyr 项目漏洞跟踪 GHSA-hchc-6489-w66v <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hchc-6489-w66v>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111243 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111243>`_

- `PR 113040 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113040>`_

- `PR 113042 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113042>`_

- `PR 113041 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113041>`_

:cve:`2026-7656`
----------------

IPv6 邻居发现输入校验存在缺陷，导致 Zephyr 网络栈接受伪造的 RA/NS/NA 报文

``subsys/net/ip/ipv6_nbr.c`` 中的 IPv6 邻居发现处理函数（``handle_ra_input``、``handle_ns_input`` 和 ``handle_na_input``）使用了一个错误的布尔表达式，它以错误的运算符优先级把 RFC 4861 的有效性检查与 ICMPv6 code 检查组合在一起，形式为 ``((length/hop/source/target checks) && (icmp_hdr->code != 0))``。由于所有合法的 ND 报文都携带 ICMPv6 code 0，攻击者设置 ``code == 0`` （即正常取值）会使整个判断结果为假，于是报文永远不会被丢弃，其他所有检查也被静默跳过。被绕过的检查包括强制的 Hop Limit == 255 校验（该校验用于证明 ND 报文源自链路上且未被转发），对于路由器通告还包括源地址必须是链路本地地址的要求，以及组播目标的合理性检查。因此，相邻的链路上攻击者，以及由于 Hop-Limit-255 防护被绕过而原本会被拒绝的远程或非链路上攻击者，都可以让伪造的路由器通告、邻居请求和邻居通告报文被接受。伪造的 RA 使攻击者能够重新配置受害者的默认路由器、链路上前缀（SLAAC）、MTU、可达与重传定时器，以及在启用 ``CONFIG_NET_IPV6_RA_RDNSS`` 时重新配置 DNS 服务器；伪造的 NS/NA 则可实现邻居缓存投毒，进而实施中间人攻击、流量重定向和拒绝服务。该缺陷属于输入校验与认证方面的弱点，而不是内存安全问题：底层报文解析原语（``net_pkt_get_data``、``net_pkt_read`` 和 ``net_pkt_skip``）本身已做越界防护，校验后的 ``length`` 就是真实的缓冲区长度，因此跳过长度检查不会造成越界访问。该缺陷自 2018 年引入该逻辑以来一直存在，并出现在直至 v4.4.0 的所有版本中；修复方法是拆分该条件，使任何一项检查失败都会丢弃报文。

- `Zephyr 项目漏洞跟踪 GHSA-cpjw-rvwx-ph9f <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-cpjw-rvwx-ph9f>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 107902 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/107902>`_

- `PR 108131 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108131>`_

- `PR 108192 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108192>`_

- `PR 108195 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108195>`_

:cve:`2026-10666`
-----------------

``subsys/net/ip/utils.c`` 中 ``net_ipaddr_parse()`` 解析 IPv4 带端口地址时的栈缓冲区溢出

``subsys/net/ip/utils.c`` 中的 ``parse_ipv4()`` （对形如 “a.b.c.d:port” 的字符串会经由 ``net_ipaddr_parse()`` 到达）使用长度 ``str_len - end - 1`` 把端口子串复制到固定的 17 字节栈缓冲区（``char ipaddr[NET_IPV4_ADDR_LEN + 1]``）中，其中 ``str_len`` 是完整且未加限制的输入长度，而 end 只是 ':' 分隔符的偏移（<=15 字节）。由于从未考虑目标缓冲区的大小，一个在冒号之后带有长后缀的精心构造地址字符串（例如 “1.2.3.4:” 后跟数百字节）会造成越界的栈写入，其长度和内容完全由攻击者控制（对后缀执行 ``memcpy`` 并附加结尾 NUL），从而实现内存破坏，至少导致拒绝服务，并有可能劫持控制流。该解析器可经由标准套接字 API（``zsock_getaddrinfo`` / 字面地址解析）、DNS 服务器字符串配置以及 eswifi Wi-Fi 协处理器的 DNS 响应路径到达，因此任何解析受网络影响的地址字符串的应用都会受到影响。该缺陷在解析器引入时（Zephyr v1.9.0）就已存在，并出现在直至 v4.4.0 的所有版本中。修复方案移除了无界复制，并在复制到小型专用缓冲区之前校验端口长度。注意：``parse_ipv6()`` 中对应的 IPv6 “[addr]:port” 路径在当前提交中仍保留相同的无界复制，是另一个仍可触达的同类缺陷。

- `Zephyr 项目漏洞跟踪 GHSA-532c-7g7f-jhmh <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-532c-7g7f-jhmh>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108529 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108529>`_

- `PR 109058 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109058>`_

- `PR 109072 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109072>`_

- `PR 109065 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/109065>`_

:cve:`2026-10673`
-----------------

ADIN2111/ADIN1110 在 OA SPI 模式下重组以太网接收帧时的越界写入

Zephyr 的 ADIN2111/ADIN1110 10BASE-T1S/T1L 以太网驱动（``drivers/ethernet/eth_adin2111.c``）在 OPEN Alliance（OA）SPI 模式下重组接收到的以太网帧的方式，是把设备提供的 64 字节数据块复制到大小为 ``CONFIG_ETH_ADIN2111_BUFFER_SIZE`` （默认 1524 字节）的固定静态缓冲区 ``ctx->buf`` 中。在 ``eth_adin2111_oa_data_read()`` 中，每个有效数据块都被 ``memcpy`` 到 ``ctx->buf[ctx->scur]``，并推进写游标 ``scur``，但没有检查 ``scur`` + len 是否仍在缓冲区范围内。数据块的数量（最多 255 个，来自 BUFSTS RCA 字段）以及每个数据块的长度完全取自从线路上收到的帧数据；只有在帧起始数据块处才会重置游标。因此，单对以太网网段上的攻击者可以发送重组后大小超过所配置缓冲区的帧，使驱动的 RX 卸载线程把攻击者控制的帧字节写到静态缓冲区末尾之外，破坏相邻的驱动或内核内存（最坏情况下约 14.8 KB）。这是一个可远程或相邻触达的越界写入（CWE-787），可造成内存破坏并导致拒绝服务，甚至可能执行代码。该缺陷在加入 OA SPI 支持时引入（提交 0ca8b0756b1），并出现在 v3.7.0 至 v4.4.0 的版本中。修复方案增加了边界检查，在复制之前丢弃超长帧并重置游标。

- `Zephyr 项目漏洞跟踪 GHSA-hm6v-4jh4-3qc4 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hm6v-4jh4-3qc4>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108200 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108200>`_

- `PR 108900 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108900>`_

- `PR 108901 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108901>`_

- `PR 108899 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108899>`_

:cve:`2026-12629`
-----------------

PL011 UART 错误中断从未被清除，外部对端可借此发起中断风暴式拒绝服务

``drivers/serial/uart_pl011.c`` 中的 ARM PL011 UART 驱动未能确认接收错误中断。在 PL011 上，帧错误、奇偶校验错误、break 错误和溢出错误中断（``PL011_IMSC_ERROR_MASK``）只有通过写中断清除寄存器 ``UARTICR`` 才能清除；读取数据寄存器会清除 RX 中断以及每字节的 RSR 状态，但不会清除 ``MIS`` 中的错误中断状态。中断服务程序 ``pl011_isr()`` 只确认了 CTS 调制解调器状态中断，从未为错误位写入 ``icr``，因此已置位的错误中断在 ISR 返回后仍保持挂起。

当应用通过公开的 ``uart_irq_err_enable()`` API 启用错误中断上报后，控制串行对端的攻击者可以通过在 RX 线上注入线路错误来稳定地置位这些错误位，例如波特率或停止位不匹配、字符中间的 break 错误（帧错误或 break 错误）、奇偶校验位翻转（奇偶校验错误）或 FIFO 溢出（溢出错误）。由于错误中断从未被清除，中断线始终保持置位，CPU 会立即且无限次地重新进入 ``pl011_isr()``，形成中断风暴式活锁，使内核无法继续推进。

其影响是仅限于可用性的拒绝服务（永久挂起），可由外部或可插拔的 UART 对端触达。利用该漏洞受配置限制：错误中断默认关闭，且树内没有任何子系统会启用它，因此只有那些在基于 PL011 的中断驱动端口上显式调用 ``uart_irq_err_enable()`` 的应用才会受影响。修复方案让 ``pl011_isr()`` 通过 ``uart->icr`` 确认挂起的错误位，从而打破该循环，并额外在 ``pl011_err_check()`` 中清除锁存的 RSR 状态。

- `Zephyr 项目漏洞跟踪 GHSA-36rp-2hcp-f5hv <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-36rp-2hcp-f5hv>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111222 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111222>`_

- `PR 112933 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112933>`_

- `PR 112932 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112932>`_

:cve:`2026-12630`
-----------------

6LoWPAN IPHC 解压缩在保留的目标地址模式上发生越界读取

Zephyr 的 6LoWPAN IP 头压缩（IPHC）解压缩代码在 ``get_ihpc_inlined_size()`` （位于 ``subsys/net/ip/6lo.c``）中存在越界读取。目标内联大小通过 ``da_inline_size_table`` 查表获得，该表有 13 个条目，索引由所收到 IPHC 分派字中的 ``M``、``DAC`` 和 ``DAM`` 位构成（``iphc & NET_6LO_IPHC_DA_MASK``，一个 0-15 的 4 位值）。保留组合 13、14 和 15 未做边界检查，会读取到该表末尾之外。

``iphc`` 字直接取自收到的帧，而每个入站 6LoWPAN 帧都会经由 802.15.4 接收路径（``subsys/net/l2/ieee802154/ieee802154_6lo.c`` 和 ``ieee802154_6lo_fragment.c``）中的 ``net_6lo_uncompress()`` 到达 ``get_ihpc_inlined_size()``。因此，无线链路或相邻链路上未经认证的攻击者可以构造这样一个帧：其目标地址模式半字节选中越界的索引，且无需任何权限或用户交互。

该越界值成为计算出的 ``inline_size``，而它会在缓冲区长度检查之前驱动头部重建：该值被用于解引用 ``*(pkt->buffer->data + sizeof(iphc) + inline_size)``，并用于计算可能下溢的 ``size_t`` 类型的 ``diff``，从而导致对报文缓冲区的进一步越界读取以及错误的解压缩。实际影响是接收端可被无线触发越界读取或拒绝服务；泄漏的字节不会返回给攻击者。修复方案会拒绝任何超出表的索引，并中止对畸形帧的处理。

- `Zephyr 项目漏洞跟踪 GHSA-45c8-pmgj-6jrc <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-45c8-pmgj-6jrc>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111272 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111272>`_

- `PR 113046 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113046>`_

- `PR 113044 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113044>`_

:cve:`2026-12631`
-----------------

Zephyr 内核中 k_thread_join/k_thread_abort 系统调用校验的访问控制拒绝逻辑存在缺陷

Zephyr 内核通过 ``kernel/thread.c`` 中的 ``thread_obj_validate()`` 校验 ``k_thread_join()`` 和 ``k_thread_abort()`` 系统调用（它们在 ``include/zephyr/kernel.h`` 中声明为 ``__syscall``）。其 ``default`` switch 分支是访问被拒绝的处理路径，在 ``k_object_validate()`` 返回 ``-EPERM`` 时进入（此时调用方用户线程从未获得对目标线程对象的访问权限），或在返回 ``-EBADF`` 时进入（此时传入的指针不是类型正确的已注册内核对象）。该分支调用了 ``K_OOPS(K_SYSCALL_VERIFY_MSG(ret, "access denied"))``，但 ``K_SYSCALL_VERIFY_MSG`` 把表达式为真视为成功；因此非零的错误码 ``ret`` 被判读为 “verified OK”，内核 oops 从未触发，控制流随后落入 ``CODE_UNREACHABLE``。

由于 ``k_thread_join()`` 和 ``k_thread_abort()`` 是系统调用，非特权用户模式线程（在 ``CONFIG_USERSPACE`` 下）只要对不属于自己的线程对象调用其中任一系统调用，就能直接到达该拒绝路径。此时违规线程不会被干净地终止，而是在系统调用处理程序内部以 supervisor 模式执行到 ``__builtin_unreachable()``。

在 Clang 构建中，``CODE_UNREACHABLE`` 会触发非法指令陷阱，因此用户线程可以确定性地使内核崩溃，这是一种可在本地触发且能逃逸用户空间沙箱的拒绝服务。在 GCC 构建中，该路径属于未定义行为：编译器可能省略对 ``thread_obj_validate()`` 返回值的处理，使其返回未定义的 ``bool``；若该值为 ``false``，调用方就会针对用户从未获授权访问的线程进入真正的 ``k_thread_join()``/``k_thread_abort()`` 实现，从而绕过访问控制。

修复方案将校验表达式改为 ``ret == 0``，这样被拒绝（非零）的结果现在会正确触发 ``K_OOPS`` 并终止违规的调用方。

- `Zephyr 项目漏洞跟踪 GHSA-crfw-75jw-hjm3 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-crfw-75jw-hjm3>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111301 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111301>`_

- `PR 113287 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113287>`_

- `PR 113286 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113286>`_

- `PR 113285 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113285>`_

:cve:`2026-12632`
-----------------

Zephyr PTP 报文解析因未校验报文类型而发生越界读取

Zephyr 的精确时间协议接收处理函数 ``ptp_msg_post_recv()`` 位于 ``subsys/net/lib/ptp/msg.c``，它通过 ``ptp_msg_type()`` 直接从线路上取出 4 位报文类型（``msg->header.type_major_sdo_id & 0xF``，范围 0-15），并用它索引 ``msg_size[]`` 表。该表只定义到 ``PTP_MSG_MANAGEMENT`` 为止的条目，即 0xD，因此 ``ARRAY_SIZE == 14``。修复之前没有上界检查，因此未定义的类型 ``0xE`` 和 ``0xF`` 会索引到数组末尾之后的一两个 ``int`` 槽位，即对相邻只读数据的越界读取。

随后该越界值被当作长度复用：它决定 ``msg_size[type] > cnt`` 的判断，而当它很小或为负时，会使 ``cnt - msg_size[type]`` 变成一个很大的正预算并传给 ``msg_tlv_post_recv()``，后者的 TLV 循环随后会越过已接收字节遍历报文的剩余部分，在报文 slab 之外的内存上执行更多越界读取和就地字节序转换写入。

该缺陷可直接从网络触达：``subsys/net/lib/ptp/port.c`` 中的 ``ptp_port_event_gen()`` 使用 ``ptp_transport_recv()`` 读取 PTP 帧，并以攻击者选择的类型调用 ``ptp_msg_post_recv()``。PTP 使用 UDP 组播或原始以太网（``0x88F7``），且不进行认证，因此同一链路上的任何主机都能在启用 ``CONFIG_PTP`` 的节点上触发该索引操作，且没有任何前置条件。

可稳定复现的影响是拒绝服务（故障或崩溃）；还存在一条有限的内存破坏路径，但它取决于 ``msg_size[]`` 相邻位置的具体构建取值，攻击者无法调控。修复方案在索引之前用 ``-EBADMSG`` 拒绝 ``type >= ARRAY_SIZE(msg_size)``。

- `Zephyr 项目漏洞跟踪 GHSA-frjr-h396-7wh4 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-frjr-h396-7wh4>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111271 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111271>`_

- `PR 111665 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111665>`_

- `PR 111667 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111667>`_

- `PR 111666 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111666>`_

:cve:`2026-12633`
-----------------

通过未经认证的路由器通告触发的 IPv6 6LoWPAN 上下文选项处理越界写入

``subsys/net/ip/ipv6_nbr.c`` 中的 IPv6 邻居发现代码会处理 ICMPv6 路由器通告中携带的 6LoWPAN 上下文选项（6CO，RFC 6775）。在 ``handle_ra_6co()`` 中，8 位的 ``context_len`` 字段直接取自报文，从未被限制在 RFC 规定的最大值 128 以内。该函数先计算 ``context->context_len / 8``，然后执行 ``memset(context->prefix + context_len, 0, sizeof(context->prefix) - context_len)``，其中 ``context->prefix`` 是固定的 16 字节数组。

当 ``context_len`` 介于 136 和 255 之间（且选项长度字段被设为 3，这是修复前的校验所接受的）时，``context_len / 8`` 的值为 17..31，因此 ``memset`` 的长度 ``16 - context_len/8`` 会使无符号 ``size_t`` 参数下溢，约为 ``SIZE_MAX``。这会产生无界的越界 ``memset``，把远超 6lo 上下文结构的内核内存清零。

该缺陷可由未经认证的链路本地输入触达：同一链路上的任何主机都能发送带有 6CO 选项的精心构造的路由器通告。RA 处理程序在调用 ``handle_ra_6co()`` 之前只校验选项长度字段，因此单个报文即可触发该任意写入。启用 ``CONFIG_NET_6LO_CONTEXT`` 时会编译该代码。

其影响是可通过内存破坏稳定实现的远程（相邻）拒绝服务，并且在系统发生故障之前，``memset`` 会把连续内存清零，造成附带的数据完整性损失。路由器通告的作用范围限于链路且不会被转发，因此攻击者必须位于同一链路上（``AV:A``）。修复方案在计算长度之前拒绝任何大于 128 的 ``context_len``。

- `Zephyr 项目漏洞跟踪 GHSA-h5m5-hm6j-cgpf <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-h5m5-hm6j-cgpf>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111275 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111275>`_

- `PR 113049 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113049>`_

- `PR 113051 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113051>`_

- `PR 113050 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113050>`_

:cve:`2026-12634`
-----------------

settings NVS 后端因 nvs_read 返回长度虚高而发生越界栈写入

Zephyr settings 子系统的 NVS 后端（``subsys/settings/src/settings_nvs.c``）会把存储的设置名条目读入固定的 74 字节栈缓冲区，并用 ``buf[rc] = '\0'`` 为其添加 NUL 终止符，其中 ``rc`` 是 ``nvs_read()`` 的返回值。按照约定，``nvs_read()`` 返回的是 *完整存储条目长度*，即 ``wlk_ate.len``，该值可能超过所提供的缓冲区长度：实际只会复制 ``MIN(len, stored_len)`` 个字节，但返回值可能大得多，仅受 NVS 扇区大小限制。有三处代码（``settings_nvs_cache_match()``、``settings_nvs_load()`` 和 ``settings_nvs_save()``）直接把这个值用作写入 NUL 的下标而未做钳制，因此某个超长的已存储名称条目会导致在受攻击者影响的偏移处、于栈缓冲区末尾之外写入单个 ``\0`` 字节（CWE-787）。

通过正常的 settings API 无法产生这种超长条目，因为名称受 ``SETTINGS_MAX_NAME_LEN`` 限制。它需要攻击者能够写入承载 settings 分区的 flash，例如共享该 flash 设备的共驻留或不可信组件、恶意的 settings 镜像或恢复操作，或离线与物理访问 flash（共享 flash 威胁模型）。当启动或子系统初始化时运行 ``settings_load()``，或者执行 ``settings_save()`` 时，会解析该畸形条目。

该越界写入是在等于精心构造的条目长度（最大为 NVS 扇区大小）的偏移处写入单个 NUL 字节，因此实际影响是崩溃或拒绝服务以及有限的栈破坏，而不是可靠的代码执行。它没有机密性影响，且无法通过网络经由普通 settings 接口触达。修复方案在执行 NUL 写入之前跳过任何 ``nvs_read()`` 长度大于或等于缓冲区大小的条目。

- `Zephyr 项目漏洞跟踪 GHSA-q7c8-m2qg-385c <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-q7c8-m2qg-385c>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111314 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111314>`_

- `PR 113298 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113298>`_

- `PR 113296 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113296>`_

- `PR 113297 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113297>`_

:cve:`2026-12999`
-----------------

Infineon Airoc Wi-Fi 驱动在发送失败时泄漏 TX 缓冲区，导致缓冲池永久耗尽

Infineon Airoc Wi-Fi 驱动的发送回调 ``airoc_mgmt_send()`` 位于 ``drivers/wifi/infineon/airoc_wifi.c``，它会为每个出站报文从固定的 ``airoc_pool`` 中分配一个 ``net_buf``。当 ``whd_network_send_ethernet_data()`` 返回同步失败时，底层的 WHD 库并不会接管该缓冲区，但修复前的驱动直接返回 ``-EIO`` 而未释放它。因此每次发送失败都会从池中永久泄漏一个缓冲区。

``airoc_pool`` 很小且大小固定（``AIROC_WIFI_TX_PACKET_POOL_COUNT`` + ``AIROC_WIFI_RX_PACKET_POOL_COUNT``，默认 20 个缓冲区），并由 WHD 的 ``whd_host_buffer_get`` 回调在发送和接收之间共享。一旦发送失败的次数足以耗尽该池，``airoc_wifi_host_buffer_get()`` 就会对之后的所有分配返回 ``WHD_BUFFER_ALLOC_FAIL``，于是发送和 WHD 驱动的接收路径都会失败，Wi-Fi 连接将丢失，直到设备重启。

该泄漏只发生在发送错误路径上。Wi-Fi 相邻的攻击者可以影响导致同步发送失败的条件（例如在本机协议栈持续尝试发送时使该站点去认证或去关联），而设备生命周期内普通的瞬时故障也会逐步累积到同样的状态。可靠地按需触发难度很高，且影响仅限于可用性，但由此导致的拒绝服务是永久的，不重启设备就无法恢复。

修复方案在失败分支上用 ``airoc_wifi_buffer_release()`` 释放缓冲区，将其归还到池中。该提交还移除了 ``airoc_mgmt_disconnect()`` 中多余的 ``k_sem_give()``；由于 ``data->sema_common`` 是二值信号量（上限为 1），这次重复 give 只是在 1 处饱和，没有安全影响。

- `Zephyr 项目漏洞跟踪 GHSA-8w97-ghfm-5wjp <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8w97-ghfm-5wjp>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111163 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111163>`_

- `PR 113304 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113304>`_

- `PR 113306 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113306>`_

- `PR 113305 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113305>`_

:cve:`2026-13212`
-----------------

Zephyr virtio 驱动会因 used ring 描述符 id 越界而调用任意函数指针

Zephyr virtio 驱动不会校验 virtio 设备写入 used ring 的描述符链头部 id。在 ``drivers/virtio/virtio_common.c`` 的 ``virtio_isr()`` 中，设备写入的 ``vq->used->ring[idx].id`` 被直接用作 ``vq->recv_cbs[]`` 和 ``vq->desc[]`` 的下标，而这两个数组都恰好按 ``vq->num`` 个条目分配。``recv_cbs[]`` 保存 ``{cb, opaque}`` 回调条目，随后被索引到的回调指针会以 ``cbe.cb(cbe.opaque, used_len)`` 的形式被调用。

由于 id 以 16 位值的形式被使用且没有边界检查，恶意或被攻陷的 virtio 后端（不可信的 hypervisor，或 PCI 或 MMIO 传输上不可信的硬件或对端处理器 virtio 设备）可以提供远大于 ``vq->num`` 的 id。这会导致从 ``recv_cbs[]`` 之后的堆内存中越界读取一个 ``{function pointer, argument}`` 对，随后驱动在客户机的中断上下文中调用这个由攻击者塑造的指针。此过程不需要客户机权限，也不需要用户交互；后端只需写入共享的 used ring 并触发队列中断即可实现。

其结果是 Zephyr 客户机中一次任意的、受攻击者影响的函数指针调用，即一个可导致代码执行或至少可靠崩溃的控制流劫持原语。修复方案在索引 ``recv_cbs[]``/``desc[]`` 或调用回调之前，拒绝任何 ``>= vq->num`` 的 used ring id。这影响使用 ``CONFIG_VIRTIO`` 并采用 PCI 或 MMIO 传输的构建。

- `Zephyr 项目漏洞跟踪 GHSA-7884-373w-qqhx <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-7884-373w-qqhx>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111289 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111289>`_

- `PR 113344 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113344>`_

- `PR 113345 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113345>`_

:cve:`2026-13213`
-----------------

Bluetooth HAS：已配对对端在 bt_has_register 之前重连时空指针解引用导致拒绝服务

``subsys/bluetooth/audio/has.c`` 中的助听器访问服务（HAS）GATT 服务器通过 ``BT_CONN_CB_DEFINE`` 无条件安装了一组连接回调，因此即使应用尚未调用 ``bt_has_register()``，每个建立安全连接的连接也都会执行 ``security_changed()``。在 ``bt_has_register()`` 解析这些属性并设置 ``has.registered`` 之前，服务属性指针 ``hearing_aid_features_attr``、``preset_control_point_attr`` 和 ``active_preset_index_attr`` 始终保持为 ``NULL``。

在启用 ``CONFIG_BT_SETTINGS`` 时，``settings_set_cb()`` 会在启动时恢复每个已配对客户端持久化的上下文，并无条件把 ``context->flags`` 设为 ``BONDED_CLIENT_INIT_FLAGS`` （非零）。当之前配对过的对端在 ``bt_has_register()`` 尚未被调用的启动窗口期内重连并重新建立安全连接时，``security_changed()`` 会看到非零的标志位并调度 ``notify_work_handler``，后者用一个仍为 ``NULL`` 的属性指针调用 ``bt_gatt_is_subscribed()``。这会触发断言（``bt_gatt_is_subscribed()`` 中的 ``__ASSERT(attr, ...)``），或者在断言被编译掉后对 ``attr->uuid`` 产生空指针解引用。

其结果是可远程（Bluetooth 相邻）触发的 HAS 外设崩溃。利用该漏洞要求对端此前已与该设备配对，并在应用注册服务之前的启动竞态窗口内重连；持续重连的对端可以延长服务中断时间。影响仅限于拒绝服务，不涉及内存破坏或信息泄漏。

修复方案在 ``security_changed()`` 中增加了提前返回的保护 ``if (!has.registered) { return; }``，从而在 GATT 服务完成注册且其属性指针有效之前不会调度任何通知工作。

- `Zephyr 项目漏洞跟踪 GHSA-9rj8-3fvm-cc9f <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9rj8-3fvm-cc9f>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111767 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111767>`_

- `PR 113349 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113349>`_

- `PR 113347 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113347>`_

- `PR 113348 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113348>`_

:cve:`2026-13214`
-----------------

OCPP GetConfiguration 键解析中的栈缓冲区溢出

``subsys/net/lib/ocpp/ocpp_j.c`` 中的 OCPP 1.6 客户端在 ``parse_getconfig_msg()`` 中存在栈缓冲区溢出。在处理来自中央系统的 ``GetConfiguration`` 请求时，处理程序使用无界的 ``strcpy()`` 把攻击者可控的 JSON ``"key"`` 字符串复制到调用方的固定 50 字节栈缓冲区（``skey[CISTR50]``，声明于 ``subsys/net/lib/ocpp/ocpp.c``）中。解析出的键值直接指向接收缓冲区，因此其长度仅受报文大小限制（``CONFIG_OCPP_RECV_BUFFER_SIZE``，默认 2048）。

``GetConfiguration`` 消息通过充电点向其配置的中心系统建立的 WebSocket 连接下发。读取线程 ``ocpp_wsreader()`` 将消息读入 ``ui->recv_buf``，并通过 PDU 函数表将其分派给 ``parse_getconfig_msg()``。控制中心系统端点的攻击者，或在未加密连接上的中间人攻击者，可以发送 ``GetConfiguration`` 请求，其 ``"key"`` 字段超过 50 字节，从而用攻击者选定的字节溢出读取线程的栈。

其后果是 OCPP 读取线程上可远程触发的栈破坏：至少会导致拒绝服务；视构建期加固措施（例如栈金丝雀和 MPU 配置）而定，还可能实现远程代码执行。修复方案是用有界的 ``strncpy(key, payload.key[0], CISTR50 - 1)`` 替换 ``strcpy()``，并显式添加 NUL 终止符，与其他处理程序中已使用的有界拷贝保持一致。

- `Zephyr 项目漏洞跟踪 GHSA-fqhf-6v24-4px2 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fqhf-6v24-4px2>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111242 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111242>`_

- `PR 113330 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113330>`_

- `PR 113329 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113329>`_

:cve:`2026-13215`
-----------------

Zephyr ext2 挂载：未校验的超级块块大小导致由精心构造的文件系统镜像引发越界写入

Zephyr ext2 文件系统驱动程序在挂载文件系统时未校验磁盘超级块中的 ``s_log_block_size`` 字段。``subsys/fs/ext2/ext2_impl.c`` 中的 ``ext2_verify_disk_superblock()`` 会检查 magic 值、修订版本、inode 大小和块组数量，但从不限制 ``s_log_block_size``。校验成功后，``subsys/fs/ext2/ext2_ops.c`` 会用这个由攻击者控制的 ``uint32_t`` 计算 ``fs->block_size = 1024 << superblock.s_log_block_size``，因此精心构造的值要么使移位溢出（未定义行为），要么产生远大于 ``CONFIG_EXT2_MAX_BLOCK_SIZE`` 的块大小。

该块大小随后由 ``ext2_init_blocks_slab()`` 传给 ``k_mem_slab_init()``，以便从固定静态缓冲区 ``__ext2_block_memory_buffer`` 中划分出 ``CONFIG_EXT2_MAX_BLOCK_COUNT`` 个块，而该缓冲区的大小为 ``CONFIG_EXT2_MAX_BLOCK_COUNT * CONFIG_EXT2_MAX_BLOCK_SIZE``。``k_mem_slab_init()`` 不校验所请求的块是否能放入缓冲区，而 ext2 的封装函数又丢弃了它的返回值，因此该 slab 的布局会超出静态缓冲区的末尾。挂载过程会立即把块组、位图和 inode 块（每个大小为 ``fs->block_size`` 字节）读入这些 slab 块，在首次读取块时即对相邻静态内存产生越界写入。

整条路径仅由从所挂载镜像中读取的数据决定，因此任何能够向设备提供精心构造 ext2 镜像（例如可移动 SD 卡或其他存储介质）的攻击者都可以触发该问题。由于 ext2 驱动以内核模式运行，提供镜像字节即可获得超级用户模式的内存破坏原语，影响范围从拒绝服务到潜在的代码执行。

修复方案会拒绝使移位溢出（大于 11）或产生超过 ``CONFIG_EXT2_MAX_BLOCK_SIZE`` 的块大小的 ``s_log_block_size`` 值，因此块 slab 再也无法被初始化为大于其底层缓冲区。

- `Zephyr 项目漏洞跟踪 GHSA-j52j-gfj9-rwjm <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-j52j-gfj9-rwjm>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111241 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111241>`_

- `PR 113754 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113754>`_

- `PR 113327 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113327>`_

- `PR 113326 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113326>`_

:cve:`2026-13216`
-----------------

Zephyr virtio PCI 驱动中因未校验设备提供的 capability 长度导致的越界栈写入

virtio PCI 驱动（``drivers/virtio/virtio_pci.c``）在驱动初始化期间解析设备的 PCI capability 列表。在 ``virtio_pci_read_cap()`` 中，设备提供的 capability 长度字节 ``cap_len`` 仅由 ``assert(tmp.cap_len == cap_struct_size)`` 加以检查，而该字节是通过 ``pcie_conf_read()`` 从 PCI 配置空间读取的。该 ``assert`` 会展开为 ``__ASSERT_NO_MSG()``，它受 ``CONFIG_ASSERT`` 控制，而该选项在生产构建中默认为关闭，因此该值在完全未校验的情况下进入了拷贝逻辑。

该长度随后驱动一个循环，把额外的 capability dword 拷贝到调用方提供的固定大小栈缓冲区中。``cap_len`` 小于 24 字节的基础结构 ``struct virtio_pci_cap`` 时，无符号计数 ``extra_data_words`` 会下溢到接近 ``SIZE_MAX`` 的值，造成实际上无界的栈写入；``cap_len`` 大于调用方缓冲区（最大 255）时，会向缓冲区之后写入最多约 228 字节由设备控制的数据。这两者都是在启动阶段的设备探测过程中以内核模式执行的、对攻击者可控内容的越界写入。

该输入来自 virtio 设备。在 Zephyr 作为虚拟机监控程序下客户机运行的常见部署中，设备后端就是宿主机，其权限本就完全高于客户机，因此该缺陷不会带来权限提升。可利用的场景是与 Zephyr 内核相比不可信的 virtio 设备——例如裸机系统上不可信的或物理/直通的 virtio PCIe 设备，或需要客户机防御宿主机的机密计算场景——此时恶意设备可以破坏内核栈，并可能实现代码执行或导致崩溃。

修复方案用运行时范围检查取代了被编译掉的 assert，在进行任何算术运算或拷贝之前拒绝超出 ``[sizeof(struct virtio_pci_cap), cap_struct_size]`` 范围的 ``cap_len``。

- `Zephyr 项目漏洞跟踪 GHSA-qrh3-4mvv-w667 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-qrh3-4mvv-w667>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111289 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111289>`_

- `PR 113344 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113344>`_

- `PR 113345 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113345>`_

:cve:`2026-13217`
-----------------

Zephyr OCPP CALLRESULT 解析中因未检查 strtok_r/atoi 导致的空指针解引用

``subsys/net/lib/ocpp/ocpp.c`` 中的 OCPP 1.6 客户端会从 CALLRESULT 消息的 ``uid`` 字段重建会话句柄和 PDU id。在 ``ocpp_process_server_msg()`` 中，代码调用 ``atoi(strtok_r(uid, "-", &tmp))`` 时未检查 ``strtok_r`` 的返回值。当服务器提供的 ``uid`` 为空或不包含 ``-`` 分隔符时，``strtok_r()`` 返回 ``NULL``，而 ``atoi(NULL)`` 会解引用空指针，这属于未定义行为。

``uid`` 来源于网络数据：``subsys/net/lib/ocpp/ocpp_j.c`` 中的 ``parse_rpc_msg()`` 会对通过 TCP/WebSocket 从 OCPP 中心系统收到的帧进行 JSON 解析，并把服务器控制的字符串拷贝到本地缓冲区。恶意或被攻陷的中心系统，或在非 TLS 的 ``ws://`` 连接上的中间人攻击者，都可以返回格式错误的 ``uid`` 来触发该缺陷。除现有的服务器连接（或中间人位置）之外无需任何认证，而且重建出的指针会由 ``ocpp_session_is_valid()`` 进行有效性校验，因此影响仅限于空指针解引用，而不是任意指针使用。

在会捕获地址 0 访问的 Zephyr 目标上（MMU/MPU 平台，或启用 ``CONFIG_NULL_POINTER_EXCEPTION_DETECTION`` 时），该解引用会在 OCPP 读取线程内触发异常并调用 fatal 处理程序，造成充电点的远程拒绝服务；在地址 0 可读的裸机目标上，该调用返回 0，不会有危害，因此影响仅限于可用性且取决于平台。

所应用的修复只保护了第一个 ``atoi()``；同一函数中第二个 ``strtok_r(NULL, "-", &tmp)`` 及其后的 ``pdu = atoi(buf)`` 仍未受保护，当 ``uid`` 有第一个 token 但没有第二个以 ``-`` 分隔的 token 时，相同的网络输入仍可触发完全一样的空指针解引用。完整的修复还应校验第二个 token。

- `Zephyr 项目漏洞跟踪 GHSA-w234-pcxp-4q8r <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-w234-pcxp-4q8r>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111242 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111242>`_

- `PR 113330 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113330>`_

- `PR 113329 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113329>`_

:cve:`2026-13343`
-----------------

MIDI 2.0 UMP Stream 响应器中的未初始化栈内存泄露

``lib/midi2/ump_stream_responder.c`` 中的 UMP Stream 响应器库在 16 字节的结构体 ``struct midi_ump`` 中构建应答报文，该结构体定义为 ``uint32_t data[4]``。构建函数 ``make_endpoint_info()`` 和 ``make_function_block_info()`` 只填充前两个字（``res.data[0]`` 和 ``res.data[1]``），并且在此修复之前把结果声明为未初始化的局部变量（``struct midi_ump res;``）。其余两个字（``res.data[2]``、``res.data[3]``）会保留栈上的残留内容。

Endpoint Info 和 Function Block Info 通知是 UMP Stream 消息（``UMP_MT_UMP_STREAM``），长度为 4 个字，因此整个 16 字节报文——包括那两个未初始化的字——都会由 ``cfg->send()`` 原样发送。响应器由攻击者提供的 UMP Stream Endpoint-Discovery / Function-Block-Discovery 请求经 ``ump_stream_respond()`` 驱动。在源码树内的 Network MIDI 2.0 服务器（``subsys/net/lib/midi2/netmidi2.c``）中，这些请求以 UDP 数据报形式到达，且由于默认端点不进行认证，远程对端可以建立会话并触发这些响应；该库同样用于服务 USB MIDI 2.0 主机。

每个发现请求都会使设备向对端泄露 8 字节自身的未初始化栈内存，而且该请求可以随意重复。这属于仅涉及机密性的信息泄露（根本原因是使用了未初始化的变量，CWE-457/CWE-908）；泄露的字中可能包含残留数据或指针值。不存在内存破坏、完整性或可用性影响。

修复方案将两个结果结构体都零初始化（``struct midi_ump res = {0};``），因此在发送前会清除尾部的字。它们是仅有的两个未设置尾部字的响应器构建函数（``send_string()`` 已经会清零其缓冲区），所以该泄露已被完全消除。

- `Zephyr 项目漏洞跟踪 GHSA-4w5x-w7j4-6xxc <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4w5x-w7j4-6xxc>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111286 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111286>`_

- `PR 113341 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113341>`_

:cve:`2026-13351`
-----------------

net：恶意分片的 IPv6 数据包会阻止后续入站数据包的接收/处理

只需发送少量恶意分片的 IPv6 数据包，就能使 Zephyr 网络栈无法接收或处理后续入站数据包。当 ``net_ipv6_handle_fragment_hdr()`` 针对畸形分片触发 ICMPv6 错误响应时，它会在未解除数据包引用的情况下返回 ``NET_OK``，从而泄露 RX 网络数据包缓冲区。每次 ``k_mem_slab_alloc()`` 调用都没有对应的 ``k_mem_slab_free()``，因此反复重放这样的数据包会耗尽 RX 缓冲区 slab，此后驱动程序会持续无法获取 RX 缓冲区，导致拒绝服务。

- `Zephyr 项目漏洞跟踪 GHSA-cv4q-2j56-4wqf <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-cv4q-2j56-4wqf>`_

此问题已在 main 中针对 v4.4.0 修复

- `PR 104044 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104044>`_

- `PR 104205 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104205>`_

- `PR 104206 针对 v4.2 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104206>`_

- `PR 104209 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/104209>`_

:cve:`2026-13478`
-----------------

Zephyr ext2 块位图校验中因精心构造的 s_blocks_count 导致的越界读取

Zephyr ext2 文件系统驱动程序在 ``subsys/fs/ext2/ext2_impl.c`` 的 ``ext2_init_fs()`` 中校验磁盘上的块位图，其做法是把 ``fs_blocks = s_blocks_count - s_first_data_block`` 传给 ``ext2_bitmap_count_set()``。该辅助函数（``subsys/fs/ext2/ext2_bitmap.c``）把参数视为位数，每 8 位读取一个位图字节，但位图缓冲区（``BGROUP_BLOCK_BITMAP``）只是取出的一个块，仅有 ``fs->block_size`` 字节（容量为 ``fs->block_size * 8`` 位）。``s_blocks_count`` 和 ``s_first_data_block`` 直接取自超级块，从未针对这个单一块组的容量加以限制；``ext2_verify_disk_superblock()`` 会检查 magic、修订版本和块大小移位，但不检查块数量。

带有超大 ``s_blocks_count`` 的精心构造 ext2 镜像（最高约 40 亿，而位图最多为 4096 字节的块 / 32768 位）会使 ``ext2_bitmap_count_set()`` 扫描位图块之后约 512 MB 的内存——这是对静态块 slab 及相邻内存的大范围越界读取。

该缺陷在挂载过程中被触发：``ext2_init_fs()`` 由 ``subsys/fs/ext2/ext2_ops.c`` 中的 ``ext2_mount()`` 调用，后者是所注册的 ``.mount`` 操作。任何挂载攻击者提供的 ext2 镜像的路径（可移动介质、磁盘/闪存分区或下载的镜像）都会触发它。该解析器以内核权限运行并处理攻击者控制的数据，因此在任何可以挂载不可信 ext2 介质的地方该缺陷都可被利用。

影响仅限于越界读取：得到的位计数会在内部进行比较并导致挂载被拒绝，因此不会返回攻击者可控的字节（不构成有用的信息泄露）。约 512 MB 的越界读取几乎必然会跨越未映射或受 MPU 保护的边界并触发异常，使系统崩溃——这是仅挂载一个畸形镜像就能触发的拒绝服务。修复方案会在扫描之前拒绝 ``fs_blocks`` 超过 ``fs->block_size * 8`` 的任何镜像。

- `Zephyr 项目漏洞跟踪 GHSA-gj29-7f7m-4c29 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gj29-7f7m-4c29>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111970 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111970>`_

- `PR 112132 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112132>`_

- `PR 112131 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112131>`_

- `PR 113351 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113351>`_

:cve:`2026-13479`
-----------------

LoRaWAN 时钟同步 AppTimeAns 下行处理程序中的越界读取

LoRaWAN 应用层时钟同步服务在 ``subsys/lorawan/services/clock_sync.c`` 的 ``clock_sync_package_callback()`` 中解析下行。其命令循环仅保证单字节的命令 id 在边界内；对于 ``CLOCK_SYNC_CMD_APP_TIME`` 即 ``AppTimeAns`` 命令，处理程序随后通过 ``sys_get_le32()`` 读取 4 字节的时间校正值并读取 1 字节 token，却不检查接收缓冲区中还剩余 5 个字节（``len - rx_pos``）。因此过短或精心构造的 ``AppTimeAns`` 会读到解密后载荷末尾之后最多 5 个字节。

载荷（``rx_buf`` / ``len``）是交付给所注册下行回调（``mcps_indication->Buffer`` / ``BufferSize``）的解密后应用帧。要到达该处理程序，需要一个位于时钟同步端口、且通过 LoRaWAN MAC 完整性校验和 FRMPayload 解密的帧，因此现实中的攻击者是恶意或被攻陷的网络/应用服务器（``AppTimeAns`` 的指定发送方），或持有会话密钥的一方，而不是任意的无线电监听者。

越界读取是有界的：其底层存储是固定的 255 字节静态缓冲区，因此那几个越界字节不会触发异常；而且读到的值（``time_correction``、``token``）仅在内部使用、从不发送，所以既不会向攻击者泄露信息，也不会导致崩溃。唯一的影响是：与 ``ctx.req_token`` 匹配的残留 ``token`` 会把垃圾 ``time_correction`` 应用到设备自身的时钟偏移（``ctx.time_offset``）上，这是局限于受害者时间估计的轻微完整性影响。修复方案增加了显式的长度检查，会丢弃过短的 ``AppTimeAns``。注意，周期性（periodicity）和强制重新同步（force-resync）处理程序中类似的单字节读取仍未受保护，其影响同样可忽略不计。

- `Zephyr 项目漏洞跟踪 GHSA-2m6g-p3vx-p2fh <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-2m6g-p3vx-p2fh>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111983 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111983>`_

- `PR 113433 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113433>`_

- `PR 113432 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113432>`_

- `PR 113431 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113431>`_

:cve:`2026-13480`
-----------------

LoRaWAN 分片数据块传输（FUOTA）下行处理程序中的越界读取

``subsys/lorawan/services/frag_transport.c`` 中的 LoRaWAN TS004 分片数据块传输处理程序 ``frag_transport_package_callback()`` 在解析下行命令字节时，不校验每次访问前是否还剩余足够的载荷字节。循环的唯一边界是 ``rx_pos < len``；在消耗掉单字节命令 id 之后，处理程序把 ``rx_buf + rx_pos`` 强制转换为 10 字节的 ``struct frag_transport_setup_req``，而对于 ``DATA_FRAGMENT`` 命令，则把 ``&rx_buf[rx_pos]`` 传给分片解码器，解码器会恰好读取 ``ctx.frag_size`` 字节——这两种情况都没有剩余长度检查。

分片大小由攻击者在之前的 ``FRAG_SESSION_SETUP`` 命令中选定（``ctx.frag_size = req->frag_size``，上限为 ``CONFIG_LORAWAN_FRAG_TRANSPORT_MAX_FRAG_SIZE``，默认 232）。``rx_buf`` 指向 loramac-node MAC 层中 255 字节的静态 ``MacCtx.RxPayload`` 缓冲区，而 ``len`` 是实际解密后的载荷长度。攻击者可以用索引不匹配的 ``DATA_FRAGMENT`` 填充命令来填充下行（每条命令使 ``rx_pos`` 前进三个字节而不产生应答），并在载荷末尾附近附加一个索引匹配的分片，从而让解码器读取 ``RxPayload`` 末尾之后最多约 ``frag_size`` 字节的内容，把相邻静态内存拷贝到解码器缓冲区和 FUOTA 闪存镜像中。

该处理程序只对已通过 LoRaWAN 帧 MIC 和 FRMPayload 解密的下行运行，因此只有持有设备会话密钥的一方（FUOTA 服务器，或已攻陷这些密钥的攻击者）才能触发该缺陷。越界读取的字节永远不会返回给发送方——唯一发出的上行是携带分片计数的状态应答——因此不存在直接的泄露通道；而且在典型的平坦内存 LoRaWAN MCU 上，越界读取仍位于已映射内存之内，所以不太可能崩溃。影响因此是有界的越界读取，机密性后果有限，且不存在写入或控制流原语。修复方案在每次访问之前增加了剩余长度防护。

- `Zephyr 项目漏洞跟踪 GHSA-845m-2m84-g5h2 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-845m-2m84-g5h2>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111983 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111983>`_

- `PR 113433 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113433>`_

- `PR 113432 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113432>`_

- `PR 113431 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113431>`_

:cve:`2026-13481`
-----------------

Zephyr net PTP 中 PTP 管理 TLV TIME 解析的越界读取

``subsys/net/lib/ptp/tlv.c`` 中的 IEEE 1588 PTP 管理报文解析器对 ``PTP_MGMT_TIME`` 管理 id 处理不当。在 ``tlv_mgmt_post_recv()`` 中，``PTP_MGMT_TIME`` 分支把 ``mgmt_tlv->data`` 强制转换为 10 字节的 ``struct ptp_timestamp`` 并读取它（随后进行字节序转换并写回），却没有先检查 TLV 数据字段至少有 ``sizeof(struct ptp_timestamp)`` 那么大。同一 switch 中其他同族管理 id 都会先校验自身长度；``PTP_MGMT_TIME`` 是唯一缺少该检查的分支。

传入的长度是管理数据大小（``tlv->length - 2``），而 ``ptp_tlv_post_recv()`` 中的上游防护只要求 ``tlv->length > 2``，``msg_tlv_post_recv()`` 也只校验 TLV 是否位于所接收的字节数之内，并不校验每种 id 的最小长度。因此本地 PTP 网段上的对端可以发送携带过短 ``PTP_MGMT_TIME`` TLV（数据小到 2 字节）的 ``PTP_MSG_MANAGEMENT`` 报文，使解析器读写超出已校验数据 8 个字节。报文类型和 TLV 内容直接来自链路，因此在启用 ``CONFIG_PTP`` 时，任何相邻攻击者都能触发该路径。

越界读取和写回仍位于 ``struct ptp_msg`` 分配的内存之内（``mgmt_tlv->data`` 位于开头的 ``mtu[NET_ETH_MTU]`` 联合体成员中，因此 ``data + 10`` 最多只落在 ``mtu[]`` 之后几个字节处，仍在同一对象内），所以这是对对象内相邻内存的越界读取，以及对该报文解析出的时间戳的有界原地破坏，而不是跨越分配边界的内存破坏。影响仅限于相邻字节的轻微信息暴露和设备解析出的管理 TIME 值被破坏；该访问不会导致崩溃，也无法触达引用计数破坏。

修复方案在强制转换之前增加了 ``if (length < sizeof(struct ptp_timestamp)) { return -EBADMSG; }``，与其他管理 id 分支保持一致，并完全消除了接收路径上的该缺陷。

- `Zephyr 项目漏洞跟踪 GHSA-mh5r-jxh8-hxwx <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-mh5r-jxh8-hxwx>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111969 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111969>`_

- `PR 113353 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113353>`_

- `PR 117480 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/117480>`_

- `PR 117479 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/117479>`_

:cve:`2026-13734`
-----------------

Zephyr WireGuard 在防重放检查之前就修改对端状态，导致可通过抓包重放劫持端点

Zephyr 的 WireGuard VPN 数据平面接收处理程序位于 ``subsys/net/lib/wireguard/wg_crypto.c`` 中，其中的 ``wg_process_data_message()`` 过晚校验防重放计数器。在 ``MESSAGE_TRANSPORT_DATA`` 数据包的 AEAD 解密成功后，代码会提交多项对端状态变更——``update_peer_addr()`` 端点漫游更新、``keypair->last_rx`` / ``peer->last_rx`` 存活定时器，以及 ``keypair_update()`` 将 ``next``\ →\ ``current`` 提升并销毁前一个密钥对——之后才调用 ``wg_check_replay()``。对于重放的数据包，重放检查会返回 ``-EINVAL``，但之前的这些修改都没有回滚。

AEAD 标签认证的是内容而非新鲜性，因此被重放但内容真实的传输数据包能够正确解密。攻击者只要在链路上捕获一个有效的密文（路径上或共享介质上的监听者），就可以从任意伪造的源地址重新注入该密文。到达该处理程序不需要任何凭据：它由入站 UDP 数据报经 ``subsys/net/lib/wireguard/wg.c`` 中的分派逻辑直接驱动。

由于这些状态修改在重放检查之前就已提交，重放会把对端端点重新指向攻击者选定的源地址（漫游劫持），从而把受害者后续的出站隧道流量重定向，直到合法对端的下一个数据包将其纠正；它还会提前销毁前一个密钥对并刷新 RX 存活定时器。隧道载荷仍由会话密钥对加密，因此这是完整性/可用性影响（流量重定向与会话中断），而不是载荷泄露。修复方案把 ``wg_check_replay()`` 移到解密成功之后、任何对端状态修改之前，与 WireGuard 规范和 Linux 参考实现保持一致。

- `Zephyr 项目漏洞跟踪 GHSA-x7q7-fjx9-4vj2 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-x7q7-fjx9-4vj2>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111043 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111043>`_

- `PR 112250 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112250>`_

:cve:`2026-13735`
-----------------

WireGuard keepalive 传输数据消息未经 Poly1305 认证即被接受

Zephyr 的 WireGuard 实现（``subsys/net/lib/wireguard/wg_crypto.c``）对 keepalive 数据包处理不当。在 ``wg_process_data_message()`` 中，任何载荷恰好为 16 字节的 type-4 传输数据消息（空明文加一个裸 Poly1305 标签，即 keepalive）都会在 ``wg_decrypt_packet()`` 被调用之前就被接受并立即返回。因此 Poly1305 认证标签从未得到校验；此前的唯一关卡是明文形式的接收方索引查找（对攻击者提供的 ``data_hdr->receiver`` 调用 ``get_peer_keypair_for_index()``）以及一项非密码学的密钥对有效性/过期检查。

该路径完全可以从网络侧到达：WireGuard 端口上的入站 UDP 由 ``wg_input()`` 分派给 ``handle_transport_data()``，然后再交给 ``wg_process_data_message()``。32 位接收方索引在 WireGuard 握手和数据消息中以明文传输，因此路径上的监听者可以直接获知它，路径外的攻击者也可以针对 UDP 端口暴力枚举它。只要该索引对应的会话处于有效接收状态，攻击者无需持有会话密钥就能发送 16 字节的垃圾载荷并使其被接受。

一旦被接受，这条未经认证的消息就会让管理层观察到伪造的 ``NET_EVENT_VPN_CONNECTED`` 信号（设置 ``peer->first_valid`` 并通知任何 ``net_mgmt`` 监听者），同时还会递增 keepalive 接收统计。影响仅限于该状态信号的完整性：没有明文被解密或注入，没有密钥被泄露，而且提前返回的路径不会更新对端端点或存活定时器，因此不存在流量注入、会话接管或可用性方面的后果。

修复方案移除了解密前的提前返回，使 16 字节的载荷会经过 ``wg_decrypt_packet()``，由它在空明文上校验 Poly1305 标签，随后执行现有的防重放检查；只有经过认证且未被重放的消息才会被认定为 keepalive。伪造的 keepalive 现在无法通过标签校验，并会被计为解密失败。

- `Zephyr 项目漏洞跟踪 GHSA-xxrw-r78f-f6mx <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-xxrw-r78f-f6mx>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111043 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111043>`_

- `PR 112250 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112250>`_

:cve:`2026-14366`
-----------------

SiWx91x WiFi 驱动对调用方拥有的 TX net_pkt 重复 unref / 释放后使用

Silicon Labs SiWx917 WiFi 驱动的发送回调位于 ``drivers/wifi/siwx91x/siwx91x_wifi.c``，其中的 ``siwx91x_send()`` 释放了并不属于它的网络数据包。在 Zephyr 的发送路径中，``net_pkt`` 由 L2/网络栈拥有；驱动程序只是借用它把帧字节拷贝到本地 ``net_buf`` 中。在此修复之前，发送完成后 ``siwx91x_send()`` 还会对调用方拥有的数据包调用 ``net_pkt_unref(pkt)``，从而丢弃其最后一个引用并把它过早归还给共享数据包池。该代码路径默认被编译进来（``CONFIG_WIFI_SILABS_SIWX91X_NET_STACK_NATIVE``）。

调用方位于 ``subsys/net/l2/ethernet/ethernet.c``，其中的 ``ethernet_send()`` 在驱动返回之后仍继续使用该数据包：它读取 ``net_pkt_get_len(pkt)``、更新发送统计，然后自己再执行一次 ``net_pkt_unref(pkt)``。由于驱动已经释放了该数据包，这些就是对已释放内存的读取，随后又进行第二次 unref（重复释放）。当并发的网络活动在这两次 unref 之间回收了已释放的 slab 槽位时，后一次的 unref 会递减另一个活动数据包的引用计数并将其释放，从而破坏接收和发送路径共用的 ``net_pkt`` 池。

在原生协议栈的 SiWx917 WiFi 接口上进行普通发送即可触发该缺陷，同一 WiFi 网络上的相邻攻击者也可以诱导发送（例如 ARP 或 ICMP echo 应答，或 TCP 握手）来驱动该路径。可观察到的主要影响是可用性丧失（发送挂起以及缓冲区池损坏引发的崩溃），并伴随依赖竞态的、针对内核网络缓冲区池的内存破坏。修复方案从 ``siwx91x_send()`` 中移除了错误的 ``net_pkt_unref(pkt)``；驱动接收路径中的 unref 会正确释放驱动自身分配的数据包，因此不受影响。

- `Zephyr 项目漏洞跟踪 GHSA-f9qq-jv4w-pqxg <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-f9qq-jv4w-pqxg>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 112180 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112180>`_

- `PR 113523 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113523>`_

- `PR 113522 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113522>`_

:cve:`2026-14367`
-----------------

I3C IBI 工作节点空闲链表在 ISR 与工作队列线程之间的数据竞态

``drivers/i3c/i3c_ibi_workq.c`` 中的 I3C IBI 子系统通过空闲链表 ``i3c_ibi_work_nodes_free`` 分发静态分配的工作节点，该链表实现为普通的 ``sys_slist_t``，不提供任何同步。各分配辅助函数（``i3c_ibi_work_enqueue``、``i3c_ibi_work_enqueue_target_irq``、``i3c_ibi_work_enqueue_hotjoin``、``i3c_ibi_work_enqueue_controller_request``、``i3c_ibi_work_enqueue_cb``）直接从 **ISR 上下文** 调用 ``sys_slist_get()``，而工作队列处理程序 ``i3c_ibi_work_handler()`` 则在 **工作队列线程** 中用 ``sys_slist_append()`` 归还节点，两侧都没有加锁。

由于 ``sys_slist_get()`` 和 ``sys_slist_append()`` 既不是原子的，也不具备中断安全性，当工作队列线程正在执行 append 时触发的 IBI 中断（或在 ``CONFIG_SMP`` 下真正并行的访问）就会在共享链表上产生竞态。这会破坏链表的链接关系：节点可能被交给两个使用者，节点可能丢失，或者头/尾指针可能处于不一致状态，使 ``sys_slist_get()`` 返回过期的或垃圾指针。在重复分发的情况下，随后的 ``memcpy(ibi_node, ibi_work, sizeof(*ibi_node))`` 会覆盖仍在处理中的节点；而垃圾指针则会让同一个 ``memcpy`` 变成越界写入。

该竞态由 I3C 总线流量驱动——IBI、热加入和控制器角色请求都源自总线上的目标设备，而 I3C 支持热加入设备。攻击者若控制着板上芯片间总线上的某个 I3C 外设，就可以生成高频中断，并使其时机与释放操作冲突。利用该问题需要对总线的物理访问，并赢得一个狭窄的时间窗口；最现实的影响是崩溃或挂起（拒绝服务），内存破坏虽有可能但难以控制。

修复方案把所有空闲链表的 ``sys_slist_get()`` / ``sys_slist_append()`` 操作都封装进新的 ``ibi_work_alloc()`` / ``ibi_work_free()`` 辅助函数中，每个函数由一个 ``k_spinlock``、即 ``ibi_work_lock`` 保护，从而消除了 ISR 与线程上下文之间的竞态。

- `Zephyr 项目漏洞跟踪 GHSA-gfj5-gcxv-9jqm <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gfj5-gcxv-9jqm>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 110786 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/110786>`_

- `PR 113436 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113436>`_

- `PR 113437 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113437>`_

- `PR 117902 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/117902>`_

:cve:`2026-14368`
-----------------

Zephyr LwM2M JSON 字符串解析器中的差一越界 NUL 写入

LwM2M JSON 内容格式化器中的 ``get_string()`` （位于 ``subsys/net/lib/lwm2m/lwm2m_rw_json.c`` ）会把解析出的 JSON 字符串复制到调用方提供的缓冲区并以 NUL 结尾。其长度检查使用了 ``if (string_length > buflen)`` ，这会接受长度恰好等于 ``buflen`` 的字符串。当 ``memcpy()`` 填满整个缓冲区后， ``buf[string_length] = '\0'`` 便会写入缓冲区末尾之后的一个字节（CWE-787）。

在 LwM2M WRITE 期间，字符串值及其长度直接取自传入的 CoAP 载荷： ``do_write_op_json()`` 解析通过 ``coap_packet_get_payload()`` 获取的载荷，而 ``get_string()`` 会针对 ``LWM2M_RES_TYPE_STRING`` 资源从 ``lwm2m_write_handler()`` （即 ``subsys/net/lib/lwm2m/lwm2m_message_handling.c`` 中的 ``engine_get_string()`` ）中调用。目标缓冲区 ``buf`` / ``buflen`` 要么是资源实例的固定数据缓冲区（ ``res_inst->data_ptr`` / ``max_data_len`` ），要么是引擎的验证缓冲区（ ``msg->ctx->validate_buf`` ）。因此，LwM2M 服务器（客户端的 DTLS 对端）可以写入一个字符串资源，其值的长度等于目标缓冲区大小，从而强制触发一字节溢出。

该溢出是对常量字节 ``0x00`` 的单次越界写入，位置紧邻资源缓冲区或验证缓冲区之后，会破坏内存中的相邻字节。它不会造成信息泄露，且写入的值固定，因此不是直接的代码执行原语，但可能破坏相邻状态（相邻的资源值、长度/标志字段或结构体字段），导致数据损坏或崩溃。触发该写入是确定性的；实际影响取决于内存布局。

修复方案将该检查改为 ``string_length >= buflen`` ，以拒绝长度恰好相等的情况，并使 JSON 格式化器与其他内容格式化器（ ``lwm2m_rw_plain_text.c`` 、 ``lwm2m_rw_oma_tlv.c`` 、 ``lwm2m_rw_senml_json.c`` 、 ``lwm2m_rw_cbor.c`` 、 ``lwm2m_rw_senml_cbor.c`` ）保持一致，后者已经使用了正确的边界检查。

- `Zephyr 项目漏洞跟踪 GHSA-vg53-h6qq-xx7h <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vg53-h6qq-xx7h>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 112021 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112021>`_

- `PR 113446 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113446>`_

- `PR 113444 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113444>`_

- `PR 113519 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113519>`_

:cve:`2026-14696`
-----------------

以太网桥接 RX 数据包泄漏可导致 RX 缓冲池耗尽型拒绝服务

启用以太网桥接（ ``CONFIG_NET_ETHERNET_BRIDGE`` ）后， ``subsys/net/l2/ethernet/bridge/bridge_input.c`` 中的 ``eth_bridge_input_process()`` 会决定如何处理从桥接成员接口收到的每个帧。对于还必须交付给本地协议栈的帧，代码会调用 ``eth_bridge_handle_locally()`` 并返回 ``NET_OK`` 。该辅助函数并不消费数据包——它只调用 ``bridge_iface_recv()`` （经由 ``virtual_recv()`` ），后者返回 ``NET_CONTINUE`` 且不取得 ``pkt`` 的所有权。

随后， ``NET_OK`` 判定会经由 ``ethernet_recv()`` 向上传播到 ``subsys/net/ip/net_core.c`` 中的 ``processing_data()`` ，在那里 ``NET_OK`` 被解释为“数据包已被消费，不要释放它”。由于实际上没有消费者取得所有权，RX ``net_pkt`` 永远不会归还到池中，从而发生泄漏。可明确复现的泄漏发生在以下情况：当 ``CONFIG_NET_ETHERNET_FORWARD_UNRECOGNISED_ETHERTYPE`` 被设置（启用 ``CONFIG_NET_SOCKETS_PACKET`` 时默认为 ``y`` ）时，某个帧的 EtherType 没有注册的 L3 处理程序：落空后的 L3 分发不会覆盖 ``NET_OK`` 判定，因此 ``ethernet_recv()`` 返回 ``NET_OK`` ，缓冲区永远不会被释放。

桥接 L2 网段上的任何设备都可以在无需认证的情况下发出携带任意 EtherType 的广播/组播帧。每个这样的帧都会从有限的 RX 池（ ``CONFIG_NET_PKT_RX_COUNT`` ）中永久消耗一个缓冲区，因此短暂的广播洪泛就会耗尽该池，设备在重启之前无法再接收流量——这是一种持久性拒绝服务。不会影响机密性或完整性。

修复方案让 ``eth_bridge_handle_locally()`` 传播真实的 ``net_verdict`` ，并对本地保留的帧返回 ``NET_CONTINUE`` ，同时通过新的 ``dst_iface`` 输出参数写回桥接接口，使数据包沿正常接收路径处理并只被取消引用一次。

- `Zephyr 项目漏洞跟踪 GHSA-3m4w-wc4v-766q <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3m4w-wc4v-766q>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 111931 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111931>`_

- `PR 113524 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113524>`_

:cve:`2026-14697`
-----------------

IPv6 邻居请求数据包泄漏导致 TX 池耗尽型拒绝服务

``subsys/net/ip/ipv6_nbr.c`` 中的 ``net_ipv6_send_ns()`` 会为邻居请求分配一个发送 ``net_pkt`` 。当调用它时，若有一个数据包正在等待某个未解析的邻居，且该邻居的 ``pending_queue`` 已经非空（即已有一个 NS 尚未完成），该函数会追加该数据包并提前返回，而不会通过 ``net_send_data()`` 发送 NS，也不会用 ``net_pkt_unref()`` 释放它。新分配的 NS ``net_pkt`` 及其附加的 TX 缓冲区仅由局部变量持有，会被永久泄漏，永远不会归还给 ``CONFIG_NET_PKT_TX_COUNT`` / ``CONFIG_NET_BUF_TX_COUNT`` 。

该泄漏分支位于正常的 IPv6 发送路径上： ``net_ipv6_prepare_for_send()`` （从 ``net_if.c`` 调用）会为任何下一跳尚未进入邻居缓存的出站或转发 IPv6 数据包调用 ``net_ipv6_send_ns()`` 。链路本地（相邻）攻击者可以通过发送一批请求数据包（例如 ICMPv6 回显请求或 UDP 数据报）来确定性地触发该分支，这些数据包全部伪造同一个不存在的链路本地源地址：节点会为每个请求生成回复，第一个回复会排队一个 NS，而在大约三秒的 ``INCOMPLETE`` 解析窗口内，后续每个回复都会进入泄漏分支并丢失一个 TX 数据包。路由器配置的节点在向不存在的链路本地主机转发攻击者流量时也会同样泄漏。

由于泄漏的数据包永远不会被回收，而 ``CONFIG_NET_PKT_TX_COUNT`` 默认仅为 4（以太网为 14），短暂的较低速率突发就会耗尽 TX 池。一旦耗尽，节点便无法再分配任何发送数据包，也无法发送 TCP/UDP、ARP/ND 或任何回复，从而造成完全且持久的网络拒绝服务，且在重启之前无法自行恢复。修复方案会在提前返回之前用 ``net_pkt_unref(pkt)`` 释放未发送的 NS 数据包。

- `Zephyr 项目漏洞跟踪 GHSA-x956-p489-8mf5 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-x956-p489-8mf5>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 112372 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112372>`_

- `PR 113655 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113655>`_

- `PR 113654 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113654>`_

:cve:`2026-14986`
-----------------

在 2026-09-04 之前保密

:cve:`2026-15460`
-----------------

Zephyr 蓝牙经典 L2CAP 接收路径缺少通道状态校验

蓝牙经典（BR/EDR）L2CAP 接收处理程序 ``bt_l2cap_br_recv()`` （位于 ``subsys/bluetooth/host/classic/l2cap_br.c`` ）仅根据目标通道 ID 来分发入站数据 PDU，而未检查目标通道是否已达到 ``BT_L2CAP_CONNECTED`` 状态。动态通道在仍处于 ``BT_L2CAP_CONNECTING`` 状态时（随后还会经历 ``BT_L2CAP_CONFIG`` ）就被分配 RX CID 并加入连接的通道列表——此时配置尚未完成；对于要求安全性的 PSM，对端也尚未通过认证（ ``l2cap_br_conn_req()`` ）。

由于在该窗口期内通道已经可以通过 ``bt_l2cap_br_lookup_rx_cid()`` 找到，处于无线范围内的远程对端可以发送发往该 CID 的数据 PDU，并使其在尚未建立的通道上被处理。分发逻辑会依赖通道字段（ ``BR_CHAN(chan)->rx.mode`` 、 ``rx.mps`` ），而这些字段只有在配置期间才由 ``l2cap_br_conf()`` 初始化；由于通道对象是池化的，且 ``bt_l2cap_br_chan_del()`` 不会重置 ``rx.mode`` 或重组缓冲区 ``_sdu`` ，被复用的通道可能将陈旧状态带入 ``CONNECTING`` 窗口，并以陈旧的参数和可能已失效的 ``_sdu`` 指针将帧路由到重传/流控路径（ ``bt_l2cap_br_ret_fc_recv()`` ）。

其影响是：在半开（且可能未认证）的通道上将攻击者数据交付给上层协议处理程序，以及在复用通道对象上操作陈旧或部分初始化的通道状态——这会导致通道/链路拆除（拒绝服务），并且在 ``_sdu`` 陈旧的情况下造成悬空指针。修复方案增加了一个显式的 ``BR_CHAN(chan)->state < BT_L2CAP_CONNECTED`` 防护，丢弃在通道完全连接之前收到的任何数据。

- `Zephyr 项目漏洞跟踪 GHSA-hx89-rm6c-hjrh <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hx89-rm6c-hjrh>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 112394 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112394>`_

- `PR 113700 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113700>`_

- `PR 113701 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113701>`_

- `PR 113710 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113710>`_

:cve:`2026-15461`
-----------------

Zephyr HL78xx GNSS NMEA 驱动中的类型混淆可导致来自 GNSS 输入的野指针写入

Sierra Wireless HL78xx 调制解调器 GNSS 驱动（ ``drivers/modem/hl78xx/`` ，后来为 ``drivers/modem/vendor_standalone/hl78xx/`` ）在 ``struct hl78xx_gnss_data`` 内嵌了一个通用的 ``struct gnss_nmea0183_match_data match_data`` 。通用 NMEA0183 匹配辅助程序（ ``drivers/gnss/gnss_nmea0183_match.c`` ）要求该上下文必须是 *第一个* 成员，因为其回调会把 ``user_data`` 直接转换为 ``struct gnss_nmea0183_match_data *`` 。在受影响的版本中， ``match_data`` 是第二个成员（位于 ``const struct device *dev`` 之后），因此它处于非零偏移处，而 ``gnss_nmea0183_match_init()`` 却在正确的地址初始化它。注册的 NMEA 处理程序则传入整个设备数据对象（ ``data->devices.gnss->data`` ，偏移 0），从而在状态初始化位置与解析回调读写位置之间产生偏移错位的类型混淆。

当解析来自 GNSS 接收器的 NMEA 语句时，GGA/RMC 回调会把解析出的定位数据写入结构体中的错误位置，而 GSV 回调（ ``gnss_nmea0183_match_gsv_callback`` ，在启用 ``CONFIG_GNSS_SATELLITES`` 时处于活动状态）会从错误的偏移处读取其 ``satellites`` 指针和边界值——即 ``struct hl78xx_gnss_data`` 中的非指针字节——然后通过这个虚假指针写入解析出的 ``struct gnss_satellite`` 条目。这是通过未初始化/野指针并使用垃圾边界值进行的写入。

在使用 HL78xx GNSS 的设备上，NMEA 处理程序默认注册（ ``CONFIG_HL78XX_GNSS_SOURCE_NMEA`` 是默认的 GNSS 来源）。该驱动在内核上下文中运行，且 NMEA 数据来自 GNSS 射频前端，因此能够影响 GNSS 信号的一方（例如在无线电近距离实施 GNSS/GPS 欺骗）可以驱使内核侧解析器进入该错误写入。最可能的影响是崩溃（拒绝服务），因为该虚假指针会解析为一个接近 NULL 的固定值；在无 MMU 的目标上还可能发生相邻内存损坏。机密性不受影响。利用该漏洞需要启用并激活卫星功能，因此攻击复杂度较高。

- `Zephyr 项目漏洞跟踪 GHSA-vvjg-6rg4-7235 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-vvjg-6rg4-7235>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 112937 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112937>`_

- `PR 113705 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113705>`_

:cve:`2026-6682`
----------------

FatFs FAT32 卷挂载（mount_volume）中的整数溢出可导致 Zephyr 中出现攻击者控制的文件大小和越界访问

Zephyr 通过 ``zephyrproject-rtos/fatfs`` west 模块捆绑了 ChaN 的 FatFs，作为支撑 ``subsys/fs/fat_fs.c`` 的 FAT/exFAT 文件系统。在 ``mount_volume()`` （ ``modules/fs/fatfs/ff.c`` ）中，FAT 区域大小按 ``fasize = ld_32(BPB_FATSz32); ... fasize *= fs->n_fats;`` 计算——这是一次没有溢出检查的 32 位乘法。

一个精心构造的 FAT32 卷如果将 ``BPB_FATSz32 = 0x80000001`` 且包含两个 FAT，就会使乘积回绕（变为 ``0x00000002`` ），导致计算出的数据区与 FAT 区重叠。由于乘法前的值保存在 ``fs->fsize`` 中，后续的合理性检查无法发现该回绕。

能让设备挂载此类卷的攻击者（使用恶意 SD 卡或 USB 介质）可以在重叠区域放置伪造的目录项，使 ``f_stat()`` /目录读取返回攻击者控制的文件大小；如果应用程序使用该大小作为长度来读取文件，就会溢出其缓冲区，从而在普通文件操作期间造成基于堆或栈的内存损坏。

这是 FAT32 的核心代码路径，没有编译时开关（FAT12/16/32 始终会被构建），因此默认的 Zephyr FatFs 配置会受到影响。上游 FatFs 在安全方面无人维护（维护者未回应 runZero 或 JPCERT/CC），因此 Zephyr 在其内置副本中包含了修复。上游跟踪编号为 CVE-2026-6682。

- `Zephyr 项目漏洞跟踪 GHSA-m537-wqw2-2wrj <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-m537-wqw2-2wrj>`_

此问题已在 main 中针对 v4.5.0 修复

:cve:`2026-6683`
----------------

FatFs exFAT 同步（sync_fs）中的除零操作会在构造的 exFAT 卷上导致 Zephyr 崩溃

Zephyr 捆绑的 FatFs（ ``zephyrproject-rtos/fatfs`` ）在启用 ``CONFIG_FS_FATFS_EXFAT`` 时支持 exFAT。在 ``sync_fs()`` （ ``modules/fs/fatfs/ff.c`` ）中，空闲簇簿记会除以 ``(fs->n_fatent - 2)`` 。

簇数量从 exFAT 引导区域读取，即 ``ncl = ld_32(BPB_NumClusEx)`` ，并且只与上界（ ``> MAX_EXFAT`` ）进行校验，从不检查下界；因此，将 ``BPB_NumClusEx = 0`` 的构造 exFAT 卷会得到 ``n_fatent = 2`` ，从而使除数为零。

挂载此类卷并执行任何写入/同步操作都会触发除零（SIGFPE / CPU 故障），造成拒绝服务。

该缺陷仅在编译启用了 exFAT 时存在，而这不是 Zephyr 的默认配置；启用 exFAT 并挂载不受信任的可移动介质的设备会受到影响。上游 FatFs 在安全方面无人维护，因此 Zephyr 在其内置副本中包含了修复。上游跟踪编号为 CVE-2026-6683。

- `Zephyr 项目漏洞跟踪 GHSA-c5j5-mrhx-hjg4 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-c5j5-mrhx-hjg4>`_

此问题已在 main 中针对 v4.5.0 修复

:cve:`2026-6685`
----------------

FatFs 脏扇区缓存（f_read/f_write）中的整数下溢会在构造的碎片化介质上导致 Zephyr 中的错误扇区 I/O

在 FatFs 的读/写路径中（ ``modules/fs/fatfs/ff.c`` 中的 ``f_read`` / ``f_write`` ），脏扇区缓存重新填充的决策会使用无符号运算将 ``fp->sect - sect`` 与连续长度 ``cc`` 进行比较。在碎片化的 FAT 布局中，如果后一个簇映射到的绝对扇区比当前缓存的扇区更小，该减法就会下溢（回绕为很大的无符号值），因此用于判断缓存窗口是否与请求范围重叠的防护会被错误地求值。

其结果是 FatFs 刷新或复用了错误的缓存扇区，从错误的磁盘位置读取文件数据或向错误的磁盘位置写入文件数据——造成跨文件数据损坏、可能泄露无关文件内容，并在普通文件操作期间导致越界行为。

带有故意碎片化簇链的构造卷（攻击者控制的可移动介质）会触发该条件。该路径属于默认读写路径（不受 exFAT 或 LFN 开关控制）。上游 FatFs 在安全方面无人维护，因此 Zephyr 在其内置副本中包含了修复。上游跟踪编号为 CVE-2026-6685。

- `Zephyr 项目漏洞跟踪 GHSA-rg3p-32gq-hqw3 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rg3p-32gq-hqw3>`_

此问题已在 main 中针对 v4.5.0 修复

:cve:`2026-6686`
----------------

FatFs f_lseek 越过文件末尾会暴露 Zephyr 中未初始化/陈旧的簇内容（已删除文件的数据）

在 FatFs 中（ ``modules/fs/fatfs/ff.c`` 中的 ``f_lseek`` ），将对以写入方式打开的文件寻址到超过其当前末尾的偏移处，会通过 ``create_chain()`` 扩展簇链，但不会将新分配的簇清零。

FatFs 在未初始化底层扇区的情况下将文件标记为更大，因此后续读取增长区域时会返回这些簇先前在介质上的内容——通常是已删除文件的残留数据。在低权限或后续操作者能够读取以这种方式扩展的文件的设备上，先前已删除或无关的文件数据会被泄露（CWE-908，使用未初始化的资源）。这不会造成内存安全损坏；其影响是介质数据的机密性。

该缺陷位于默认写入路径上（不受 exFAT/LFN 开关控制）。上游 FatFs 在安全方面无人维护，因此 Zephyr 在其内置副本中包含了修复。上游跟踪编号为 CVE-2026-6686。

- `Zephyr 项目漏洞跟踪 GHSA-rjhg-f2h7-rffm <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rjhg-f2h7-rffm>`_

此问题已在 main 中针对 v4.5.0 修复

:cve:`2026-6687`
----------------

FatFs exFAT 卷标读取（f_getlabel）中因未校验磁盘长度导致的栈缓冲区溢出

在 FatFs 的 ``f_getlabel()`` （ ``modules/fs/fatfs/ff.c`` ）中，exFAT 卷标复制循环的边界取决于磁盘上的原始字节 ``dj.dir[XDIR_NumLabel]`` （0–255），而不是规范规定的最大 11 个字符。

构造的 exFAT 卷如果将 ``XDIR_NumLabel`` 设置为较大的值（例如 128），就会使该循环读取超出 32 字节目录项范围的卷标字符，并向调用方提供的 ``label[]`` 缓冲区写入多达相应数量的 UTF 解码字符，从而溢出栈上典型的固定大小卷标数组（例如 ``char label[12]`` / ``label[24]`` ）——造成内存损坏，并可能影响控制流。

在 Zephyr 中，这只能在下游应用中触发： ``f_getlabel`` 仅在配置 ``CONFIG_FS_FATFS_EXTRA_NATIVE_API=y`` 时才会编译，必须启用 exFAT，且 Zephyr 树内没有代码调用它（缓冲区由应用代码提供）。尽管如此，这仍是内置库中的真实缺陷；由于上游 FatFs 在安全方面无人维护，Zephyr 在其内置副本中包含了修复（限制卷标长度），以保护选择启用的应用程序。上游跟踪编号为 CVE-2026-6687。

- `Zephyr 项目漏洞跟踪 GHSA-fxw6-w668-cgfh <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fxw6-w668-cgfh>`_

此问题已在 main 中针对 v4.5.0 修复

:cve:`2026-15890`
-----------------

在 2026-09-21 之前保密

:cve:`2026-15891`
-----------------

Zephyr MQTT-SN 客户端在移除无响应网关时发生 NULL 指针解引用

MQTT-SN 客户端保活处理程序 ``process_ping()`` （位于 ``subsys/net/lib/mqtt_sn/mqtt_sn.c`` ）在 ``PINGREQ`` 重试耗尽后会移除网关记录。它调用了 ``SYS_SLIST_PEEK_HEAD_CONTAINER(&client->gateways, gw, next)`` ，但丢弃了返回值。该宏是纯表达式，不会对 ``gw`` 赋值，因此无论列表内容如何， ``gw`` 都保持其 ``NULL`` 初始值。

随后代码解引用 NULL ``gw`` （ ``gw->gw_id`` ），并将其传给 ``mqtt_sn_gw_destroy()`` ，最终到达 ``k_mem_slab_free(&gateways, NULL)`` 。启用 ``CONFIG_MEM_SLAB_POINTER_VALIDATE`` 时，这会触发 ``k_panic()`` ；在默认配置下，它会通过 NULL 指针执行写入（ ``*(char **)mem = slab->free_list;`` ）并破坏 slab 空闲链表。结果是崩溃/内核 panic，或者在地址 0 可写的目标上造成内存分配器静默损坏。

每当已连接的 MQTT-SN 网关在配置的重试次数内未能应答保活 ``PINGREQ`` ，该易受攻击分支就会执行。此条件由远程对端控制：恶意或被攻陷的网关，或者将自己通告为网关然后停止响应（或黑洞掉真实网关的 ``PINGRESP`` ）的路径中/相邻攻击者，都会迫使客户端进入该缺陷。MQTT-SN 运行在 UDP 之上，且不需要认证。

其影响是可远程触发的受影响 MQTT-SN 客户端拒绝服务（可用性）；不会写入攻击者控制的数据。同类的移除函数 ``process_advertise()`` 使用 ``SYS_SLIST_FOR_EACH_CONTAINER_SAFE`` ，不受影响。修复方案将该宏的返回值赋给 ``gw`` 。

- `Zephyr 项目漏洞跟踪 GHSA-c4g8-4f9p-4746 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-c4g8-4f9p-4746>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 113142 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113142>`_

- `PR 113718 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113718>`_

- `PR 113723 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113723>`_

:cve:`2026-15892`
-----------------

mcumgr 设置管理处理程序在访问钩子拒绝请求时发生堆内存泄漏，导致拒绝服务

mcumgr SMP 设置管理组处理程序 ``settings_mgmt_read()`` 、 ``settings_mgmt_write()`` 和 ``settings_mgmt_delete()`` （位于 ``subsys/mgmt/mcumgr/grp/settings_mgmt/src/settings_mgmt.c`` ）在启用 ``CONFIG_MCUMGR_GRP_SETTINGS_BUFFER_TYPE_HEAP`` 时，会通过 ``k_malloc()`` 分配 ``key_name`` 缓冲区（对于读操作还会分配 ``data`` 缓冲区），并依靠 ``end:`` 标签用 ``k_free()`` 释放它们。当 ``CONFIG_MCUMGR_GRP_SETTINGS_ACCESS_HOOK`` 也启用，且应用访问钩子通过返回状态 ``MGMT_CB_ERROR_RC`` 拒绝请求时，处理程序会直接执行 ``return ret_rc;`` ，从而绕过 ``end:`` 并在每次被拒绝的请求上泄漏堆分配。

这些设置处理程序可通过未认证的 SMP 传输访问（取决于产品配置，可能是蓝牙 LE、UART 或 UDP）。访问钩子是应用用来拒绝未授权设置访问的机制，而 ``MGMT_CB_ERROR_RC`` 是常见的拒绝方式，因此，如果攻击者能够发送会被该钩子拒绝的 ``settings read`` / ``write`` / ``delete`` 命令，就会在每次尝试时触发堆泄漏。

由于泄漏的内存在重启之前永远不会被回收，持续不断的被拒绝请求会单调地耗尽内核堆，直到 ``k_malloc()`` 失败，从而使 mcumgr 服务无法使用，并影响设备上的任何其他堆使用者——造成拒绝服务。其影响仅限于可用性；不会造成内存损坏或信息泄露。只有选择堆缓冲区类型、启用访问钩子并注册了返回 ``MGMT_CB_ERROR_RC`` 的钩子的配置会受到影响（默认的栈缓冲区类型不会泄漏）。

- `Zephyr 项目漏洞跟踪 GHSA-rq68-wgv4-hcq3 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rq68-wgv4-hcq3>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 113178 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113178>`_

- `PR 113507 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113507>`_

- `PR 113506 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113506>`_

- `PR 113505 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113505>`_

:cve:`2026-15893`
-----------------

Zephyr IPv6 邻居发现因构造的路由器通告产生零可达时间，导致断言/拒绝服务

``subsys/net/ip/net_if.c`` 中的 ``net_if_ipv6_calc_reachable_time()`` 根据 ``ipv6->base_reachable_time`` 计算随机的 ND 可达时间，公式为 ``min_reachable + sys_rand32_get() % (max_reachable - min_reachable)`` ，其中 ``min_reachable = base/2`` 、 ``max_reachable = 3*base/2`` 均使用整数除法。当 ``base_reachable_time`` 为 ``1`` 时， ``min_reachable`` 和模数都会塌缩，使函数返回 ``0`` ，随后 ``net_if_ipv6_set_reachable_time()`` 会将该 ``0`` 存入 ``ipv6->reachable_time`` 。

``base_reachable_time`` 由攻击者控制： ``subsys/net/ip/ipv6_nbr.c`` 中的 ``handle_ra_input()`` 会接受传入路由器通告中的 Reachable Time 字段，只要该字段非零且 ``<= MAX_REACHABLE_TIME`` ，因此单个未认证的链路本地 RA（携带的 Reachable Time 为 ``1`` ）就能将计算出的可达时间变为 ``0`` 。路由器通告默认未认证，且攻击者只需与目标链路相邻。

当邻居随后被确认可达时， ``net_ipv6_nbr_set_reachable_timer()`` 会读取该值并执行 ``NET_ASSERT(time, "Zero reachable timeout!")`` 。在启用了 ``CONFIG_ASSERT`` 的构建中，这会触发致命的内核断言——造成远程拒绝服务；在未启用断言的构建中，可达定时器会以 ``K_MSEC(0)`` 启动并立即触发，迫使可达邻居不断重新请求（ ``STALE`` ），从而降低邻居发现的功能。其影响仅限于可用性；不会造成内存安全、机密性或完整性后果。

- `Zephyr 项目漏洞跟踪 GHSA-8v32-9xf8-r765 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8v32-9xf8-r765>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 113226 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113226>`_

- `PR 113605 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113605>`_

- `PR 113686 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113686>`_

- `PR 113687 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113687>`_

:cve:`2026-15894`
-----------------

在 2026-10-07 之前保密

:cve:`2026-15923`
-----------------

Zephyr SDIO 字节 I/O 因卡提供的 max_blk_size 为零而陷入无限循环，导致拒绝服务

Zephyr SDIO 子系统函数 ``sdio_io_rw_extended_helper()`` （位于 ``subsys/sd/sdio.c`` ）通过字节 I/O 循环完成传输，该循环使用 ``size = MIN(remaining, func->cis.max_blk_size)`` 作为每次迭代的步长。 ``func->cis.max_blk_size`` 的值直接由 ``sdio_decode_cis()`` 从 SDIO 卡的 CIS FUNCE 元组中解码得到，且未经验证。当卡报告最大块大小为零时， ``size`` 始终为 ``0`` ， ``remaining`` 永远不会减少，循环会一直空转。

该循环可从驱动使用的公共 SDIO 客户端 API 到达，包括 ``sdio_read_fifo()`` 、 ``sdio_write_fifo()`` 以及递增寄存器读/写辅助函数；这些函数都会在持有每卡互斥锁 ``func->card->lock`` 的情况下进入循环。因此，如果卡通告 ``max_blk_size == 0`` ，则在其第一次非块对齐传输时就会永久挂起调用线程，并且永远不会释放互斥锁，导致 SDIO 外设（以及依赖它的任何子系统，例如 Wi-Fi）在设备复位之前无法使用。

恶意值必须来自 SDIO 卡本身，因此该缺陷仅在可插拔 SDIO/combo 卡槽允许攻击者插入伪造或故障卡的情况下可被利用（属于物理攻击向量）；在 SDIO 外设焊接在板上的主板中，攻击者无法影响该值。此问题不涉及内存安全、机密性或完整性问题——仅导致永久性的可用性丧失。修复方案在进入循环之前，当 ``func->cis.max_blk_size`` 为零时返回 ``-EIO``。

- `Zephyr 项目漏洞跟踪 GHSA-4pvm-wrcp-jjf5 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4pvm-wrcp-jjf5>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 112628 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/112628>`_

- `PR 113730 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113730>`_

- `PR 113731 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113731>`_

- `PR 113732 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113732>`_

:cve:`2026-15924`
-----------------

Zephyr socket 中 TLS 客户端会话缓存未同步并发访问导致的释放后使用/双重释放

Zephyr 的 TLS socket 层在 ``subsys/net/lib/sockets/sockets_tls.c`` 中维护一个进程全局数组 ``client_cache``，用于缓存客户端会话，并由每个 TLS socket 上下文共享。对其进行修改和读取的函数——``tls_session_save()``、``tls_session_get()``、``tls_session_cache_reset()`` 以及设置恢复处理程序——会分配、释放并解引用每个条目的堆缓冲区 ``entry->session``。修复前，这些访问仅由 *per-socket* 上下文互斥锁 ``ctx->lock``，在 ``ctx_set_lock()`` 中按 socket 分配来串行化，而该锁无法在访问共享缓存的不同 socket 之间提供互斥保护。

由于 ``CONFIG_NET_SOCKETS_TLS_MAX_CLIENT_SESSION_COUNT`` 默认为 ``1``，任意两个并发客户端 socket 都会争用同一个槽位。``tls_session_get()`` 线程在 ``mbedtls_ssl_session_load()`` 内读取 ``entry->session`` 时，可能与另一个在 ``tls_session_save()`` 中为复用而选择同一条目、并在重新分配之前执行 ``mbedtls_free(entry->session)`` 的线程并发运行——这会造成一次释放后使用读取，而当两次保存驱逐同一条目时则会造成双重释放。两者都会破坏 mbedTLS 堆。缓存会在普通客户端路径上被访问：连接时通过 ``tls_session_store()``/``tls_session_restore()`` 访问，以及在 ``main`` 上，当 TLS 1.3 会话票据在 ``recv()``/``poll()`` 期间通过 ``tls_session_store_current()`` 到达时访问。

利用该漏洞需要应用程序选择启用按 socket 的客户端会话缓存（即 ``TLS_SESSION_CACHE`` socket 选项，默认关闭），并在多个线程上运行并发 TLS 客户端连接；该竞争窗口出现的时机受远端对等方影响，因此恶意或已被攻陷的服务器可提高会话票据频率来扩大窗口。可可靠证实的影响是内存损坏，进而导致崩溃或堆损坏（拒绝服务）。修复方案新增了一个专用互斥锁 ``session_cache_lock``，在 ``client_cache`` 的每个访问路径上获取，从而串行化所有读取和释放操作并消除该竞争。

- `Zephyr 项目漏洞跟踪 GHSA-wcgm-pq6x-v2gf <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-wcgm-pq6x-v2gf>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 113405 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113405>`_

- `PR 113736 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113736>`_

- `PR 113737 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113737>`_

- `PR 113738 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113738>`_

:cve:`2026-16147`
-----------------

it82xx2 USB 设备控制器提交不完整的 OUT 传输缓冲区，导致释放后使用和事件链表损坏

ITE IT82xx2 USB 设备控制器驱动（``drivers/usb/udc/udc_it82xx2.c``）对非控制端点上的多包 OUT 传输处理不当。在 ``work_handler_out()`` 中，活动传输缓冲区通过 ``udc_buf_peek()`` 获取（该函数不会将其出队）；当一个最大包长的完整数据包到达，但缓冲区仍有尾部空间（传输尚未完成）时，修复前的代码既会重新准备端点，通过 ``work_handler_xfer_continue()`` 继续填充同一个 ``buf``，又会同时用 ``udc_submit_ep_event()`` 将同一个仍在填充的缓冲区交给上层协议栈。

由于 ``udc_submit_ep_event()`` 会将缓冲区所有权转移给 USB 设备协议栈（``usbd_event_carrier()`` 将 ``&buf->node`` 追加到 ``uds_ctx->ep_events``，随后类处理程序会处理该节点并调用 ``net_buf_unref()`` 释放它），驱动会继续通过 DMA 将后续由主机控制的 OUT 数据包写入上层协议栈可能已经释放并回收的缓冲区中——这是一次释放后使用写入。此外，由于该缓冲区从未出队，完成的数据包会对同一对象执行 ``udc_buf_get()`` 并第二次提交它，从而将 ``&buf->node`` 两次追加到事件单向链表中（造成单向链表损坏），并导致 ``net_buf_unref()`` 被调用两次。

IT82xx2 是 USB 外设控制器，因此不受信任的 USB 主机可控制 OUT 传输的分包，并能对任何排队缓冲区超过一个数据包的非控制 OUT 端点强制触发此路径——这是一种常见的批量/中断传输模式。驱动和 USB 设备协议栈在外部主机之上的内核上下文中运行，使主机获得设备侧内核堆损坏原语：可可靠地造成拒绝服务，而且由于写入的字节受攻击者控制，还可能损坏相邻的 ``net_buf`` 池内存。攻击向量为物理方式（USB 接入）。修复方案将提交推迟到缓冲区完全填满之后，并由 ``xfer_work_handler()`` 驱动后续处理，因此每个 OUT 缓冲区只会向上层协议栈提交一次。

- `Zephyr 项目漏洞跟踪 GHSA-3q4g-7w6j-8qfp <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3q4g-7w6j-8qfp>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 113463 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113463>`_

- `PR 113847 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113847>`_

- `PR 113850 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113850>`_

- `PR 113849 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113849>`_

:cve:`2026-16148`
-----------------

it82xx2 USB 设备控制器驱动因重新初始化繁忙的可延迟工作项而导致内核 panic

ITE it82xx2 USB 设备控制器驱动在 ``drivers/usb/udc/udc_it82xx2.c`` 中的 ``it82xx2_enable()`` 函数（该驱动的 ``.enable`` 操作）内，使用 ``k_work_init_delayable(&priv->suspended_work, suspended_handler)`` 初始化其总线挂起检测工作项。在 USB 总线活动期间，该工作项基本上会被持续调度：中断处理程序在每个 SOF 帧上重新调度它，``suspended_handler()`` 也会重新调度自身，因此其超时节点通常链接在内核超时链表/工作队列待处理队列中。

``k_work_init_delayable()`` 函数（位于 ``kernel/work.c``）会无条件覆盖整个 ``k_work_delayable`` 结构，包括其超时和队列链接，且不检查工作项是否繁忙。由于 ``it82xx2_disable()`` 不会取消该工作项，正常的先禁用再启用循环会重新运行 ``api->enable()``；其中 ``udc_enable()`` 仅拒绝重复启用，而不拒绝禁用后的重新启用。该循环会就地重新初始化仍处于待处理状态的工作项，从而破坏内核超时/工作队列链表并导致内核 panic。

外部 USB 主机——例如执行 USB DFU detach（``dfu-util --detach``）或强制反复进行连接/复位/重新枚举的主机——会驱动 ``udc_disable()``/``udc_enable()`` 状态转换并控制挂起/恢复时机，因此可安排在重新启用期间使挂起工作项保持待处理状态。这会导致未认证拒绝服务（内核 panic），可从可插拔且物理连接的主机跨越 USB 边界触发，且未发现机密性或完整性影响。

修复方案将 ``k_work_init_delayable()`` 调用移入一次性的预初始化函数，使该工作项只初始化一次，从而消除对正在使用的工作项进行重新初始化的问题。

- `Zephyr 项目漏洞跟踪 GHSA-fvp9-j2pq-477x <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fvp9-j2pq-477x>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 113463 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113463>`_

- `PR 113847 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113847>`_

- `PR 113850 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113850>`_

- `PR 113849 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/113849>`_

:cve:`2026-16511`
-----------------

在 2026-11-02 之前保密

:cve:`2026-16512`
-----------------

在 2026-09-18 之前保密

:cve:`2026-16513`
-----------------

在 2026-09-25 之前保密

:cve:`2026-16514`
-----------------

在 2026-09-18 之前保密

:cve:`2026-16515`
-----------------

在 2026-09-18 之前保密

:cve:`2026-17050`
-----------------

在 2026-09-19 之前保密

:cve:`2026-17051`
-----------------

在 2026-09-20 之前保密

:cve:`2026-17052`
-----------------

在 2026-09-20 之前保密

:cve:`2026-17053`
-----------------

在 2026-09-20 之前保密

:cve:`2026-17054`
-----------------

在 2026-09-21 之前保密

:cve:`2026-2411`
----------------

Bluetooth GATT notify/indicate 对错误属性执行权限检查，绕过特征值的加密/认证要求

Zephyr 的 Bluetooth 主机将 GATT 特征声明为两个连续属性：Characteristic Declaration 和 Characteristic Value 属性；前者的权限被硬编码为 ``BT_GATT_PERM_READ``，后者携带应用程序指定的安全权限（例如 ``BT_GATT_PERM_READ_ENCRYPT`` / ``READ_AUTHEN`` / ``READ_LESC``）。公开的 notify 和 indicate API 明确接受这两个属性中的任意一个，而传入 Characteristic Declaration 是文档中记载的常见用法。在发送每个通知或指示之前，主机会在 ``gatt_notify()``、``gatt_indicate()`` 和 ``gatt_notify_multiple_verify_params()`` 中，使用 ``bt_gatt_check_perm()`` 针对 ``params->attr`` 重新检查链路安全性（``subsys/bluetooth/host/gatt.c``）。

当应用程序传入 Characteristic Declaration 属性时，主机会正确重定向值句柄，但仍让 ``params->attr`` 指向该声明，因此安全检查评估的是声明的权限（不要求安全性），而不是值的权限。结果，特征值上配置的加密/认证/LESC 要求被跳过。Notify-Multiple 路径还使用了一个省略 LE Secure Connections 要求的掩码。

远端对等方通过连接（可选择不进行配对或加密）并写入 Client Characteristic Configuration 描述符以启用通知或指示，从而触发泄露，使服务器通过尚未达到所需安全级别的链路发送受保护的值。其影响是针对应用程序原本仅打算通过安全链路暴露的特征值发生信息泄露/访问控制绕过；是否发生暴露取决于应用程序是否声明了要求加密/认证的 notify/indicate 特征，以及 CCC 是否可在较低安全层级写入。不存在内存安全或可用性影响。

修复方案新增了 ``bt_gatt_attr_resolve_value()``，该函数会在权限检查之前将声明属性映射到后续的值属性，并将 Notify-Multiple 路径切换为完整的 ``BT_GATT_PERM_READ_ENCRYPT_MASK``，从而也强制执行 LESC 要求。

- `Zephyr 项目漏洞跟踪 GHSA-4w3r-v9q9-4462 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4w3r-v9q9-4462>`_

此问题已在 main 中针对 v4.5.0 修复

- `PR 108371 针对 main 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/108371>`_

- `PR 111535 针对 v4.4 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111535>`_

- `PR 111536 针对 v4.3 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111536>`_

- `PR 111620 针对 v3.7 的修复 <https://github.com/zephyrproject-rtos/zephyr/pull/111620>`_

:cve:`2026-18413`
-----------------

在 2026-09-26 之前保密

:cve:`2026-18414`
-----------------

在 2026-09-26 之前保密

:cve:`2026-18415`
-----------------

在 2026-09-26 之前保密

:cve:`2026-18416`
-----------------

在 2026-09-26 之前保密

:cve:`2026-18417`
-----------------

在 2026-09-27 之前保密

:cve:`2026-18418`
-----------------

在 2026-10-11 之前保密

:cve:`2026-18746`
-----------------

在 2026-09-28 之前保密

:cve:`2026-18747`
-----------------

在 2026-09-28 之前保密

:cve:`2026-18748`
-----------------

在 2026-10-20 之前保密

:cve:`2026-19184`
-----------------

在 2026-10-04 之前保密

:cve:`2026-19185`
-----------------

在 2026-10-04 之前保密

:cve:`2026-19186`
-----------------

在 2026-10-07 之前保密

:cve:`2026-19569`
-----------------

在 2026-10-09 之前保密

:cve:`2026-19570`
-----------------

在 2026-10-09 之前保密

:cve:`2026-19571`
-----------------

在 2026-10-09 之前保密

:cve:`2026-19574`
-----------------

在 2026-10-09 之前保密

:cve:`2026-19575`
-----------------

在 2026-10-09 之前保密

:cve:`2026-19576`
-----------------

在 2026-10-10 之前保密

:cve:`2026-19577`
-----------------

在 2026-10-10 之前保密

:cve:`2026-19595`
-----------------

在 2026-10-18 之前保密

:cve:`2026-19669`
-----------------

在 2026-10-10 之前保密

:cve:`2026-19673`
-----------------

在 2026-10-14 之前保密

:cve:`2026-19676`
-----------------

在 2026-10-17 之前保密

:cve:`2026-19735`
-----------------

在 2026-10-11 之前保密

:cve:`2026-19736`
-----------------

在 2026-10-11 之前保密

:cve:`2026-19737`
-----------------

在 2026-10-11 之前保密

:cve:`2026-19738`
-----------------

在 2026-10-11 之前保密

:cve:`2026-19739`
-----------------

在 2026-10-11 之前保密

:cve:`2026-19740`
-----------------

在 2026-10-11 之前保密

:cve:`2026-19741`
-----------------

在 2026-10-22 之前保密

:cve:`2026-19742`
-----------------

在 2026-10-25 之前保密

:cve:`2026-19809`
-----------------

在 2026-10-19 之前保密

:cve:`2026-19935`
-----------------

在 2026-10-11 之前保密

:cve:`2026-19936`
-----------------

在 2026-10-12 之前保密

:cve:`2026-19937`
-----------------

在 2026-10-12 之前保密

:cve:`2026-19938`
-----------------

在 2026-10-12 之前保密

:cve:`2026-19939`
-----------------

在 2026-10-13 之前保密

:cve:`2026-19940`
-----------------

在 2026-10-13 之前保密

:cve:`2026-19947`
-----------------

在 2026-10-21 之前保密

:cve:`2026-75083`
-----------------

在 2026-10-14 之前保密

:cve:`2026-75084`
-----------------

在 2026-10-14 之前保密

:cve:`2026-75085`
-----------------

在 2026-10-14 之前保密

:cve:`2026-76787`
-----------------

在 2026-10-16 之前保密

:cve:`2026-76788`
-----------------

在 2026-10-16 之前保密

:cve:`2026-77684`
-----------------

在 2026-10-18 之前保密

:cve:`2026-77685`
-----------------

在 2026-10-18 之前保密

:cve:`2026-78116`
-----------------

在 2026-10-20 之前保密

:cve:`2026-78117`
-----------------

在 2026-10-20 之前保密

:cve:`2026-78118`
-----------------

在 2026-10-20 之前保密

:cve:`2026-78119`
-----------------

在 2026-10-20 之前保密

:cve:`2026-79976`
-----------------

在 2026-10-21 之前保密

:cve:`2026-79977`
-----------------

在 2026-10-22 之前保密

:cve:`2026-79978`
-----------------

在 2026-10-23 之前保密

:cve:`2026-79979`
-----------------

在 2026-10-23 之前保密

:cve:`2026-79980`
-----------------

在 2026-10-23 之前保密

:cve:`2026-79981`
-----------------

在 2026-10-23 之前保密

:cve:`2026-79982`
-----------------

在 2026-10-23 之前保密

:cve:`2026-81038`
-----------------

在 2026-10-24 之前保密

:cve:`2026-81039`
-----------------

在 2026-10-24 之前保密

:cve:`2026-82388`
-----------------

在 2026-10-26 之前保密

:cve:`2026-82389`
-----------------

在 2026-10-26 之前保密

:cve:`2026-82390`
-----------------

在 2026-10-26 之前保密

:cve:`2026-82391`
-----------------

在 2026-10-26 之前保密

:cve:`2026-82961`
-----------------

在 2026-10-27 之前保密

:cve:`2026-82962`
-----------------

在 2026-10-27 之前保密

:cve:`2026-85032`
-----------------

在 2026-10-30 之前保密

:cve:`2026-85033`
-----------------

在 2026-10-31 之前保密

:cve:`2026-85034`
-----------------

在 2026-10-31 之前保密

:cve:`2026-85035`
-----------------

在 2026-10-31 之前保密

:cve:`2026-85036`
-----------------

在 2026-10-31 之前保密

:cve:`2026-86086`
-----------------

在 2026-12-01 之前保密

:cve:`2026-86092`
-----------------

在 2026-12-03 之前保密

:cve:`2026-87038`
-----------------

在 2026-11-02 之前保密

:cve:`2026-87039`
-----------------

在 2026-11-02 之前保密

:cve:`2026-87040`
-----------------

在 2026-11-02 之前保密

:cve:`2026-87041`
-----------------

在 2026-11-02 之前保密

:cve:`2026-87042`
-----------------

在 2026-11-03 之前保密

:cve:`2026-87043`
-----------------

在 2026-11-03 之前保密

:cve:`2026-87044`
-----------------

在 2026-11-03 之前保密

:cve:`2026-87045`
-----------------

在 2026-11-06 之前保密

:cve:`2026-90585`
-----------------

在 2026-11-07 之前保密

:cve:`2026-90586`
-----------------

在 2026-11-08 之前保密

:cve:`2026-90587`
-----------------

在 2026-11-08 之前保密

:cve:`2026-90588`
-----------------

在 2026-11-08 之前保密

:cve:`2026-90589`
-----------------

在 2026-11-08 之前保密

:cve:`2026-90590`
-----------------

在 2026-11-09 之前保密

:cve:`2026-90591`
-----------------

在 2026-11-09 之前保密

:cve:`2026-90832`
-----------------

在 2026-11-10 之前保密

:cve:`2026-90833`
-----------------

在 2026-11-10 之前保密

:cve:`2026-90834`
-----------------

在 2026-11-10 之前保密

:cve:`2026-91007`
-----------------

在 2026-11-12 之前保密
