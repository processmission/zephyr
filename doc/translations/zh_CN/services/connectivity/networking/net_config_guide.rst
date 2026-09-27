.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _network_configuration_guide:

网络配置指南
############

.. contents::
    :local:
    :depth: 2

本文档介绍如何根据系统中的可用资源设置各种网络配置选项。

网络缓冲区配置选项
******************

网络缓冲区配置选项控制在同一时间能够发送或接收的数据量。

:kconfig:option:`CONFIG_NET_PKT_RX_COUNT`
  同一时间可接收的最大网络数据包数量。

:kconfig:option:`CONFIG_NET_PKT_TX_COUNT`
  同一时间允许挂起发送的最大网络数据包数量。

:kconfig:option:`CONFIG_NET_BUF_RX_COUNT`
  用于接收数据的网络缓冲区分配数量。每个 net_buf 包含一个小型报头和固定长度或可变长度的数据缓冲区。设置 :kconfig:option:`CONFIG_NET_BUF_FIXED_DATA_SIZE` 时，将使用 :kconfig:option:`CONFIG_NET_BUF_DATA_SIZE`。这是默认设置。缓冲区默认大小为 128 字节。

  :kconfig:option:`CONFIG_NET_BUF_VARIABLE_DATA_SIZE` 是实验性设置。在该设置下，每个 net_buf 的数据部分从内存池分配，大小可以等于从网络接收到的数据量。从网络接收数据时，数据会被放入 net_buf 的数据部分。根据设备资源和期望的网络使用情况，用户可以通过设置 :kconfig:option:`CONFIG_NET_BUF_DATA_SIZE` 来调整固定缓冲区的大小；如果使用可变大小缓冲区，还可以通过设置 :kconfig:option:`CONFIG_NET_PKT_BUF_RX_DATA_POOL_SIZE` 和 :kconfig:option:`CONFIG_NET_PKT_BUF_TX_DATA_POOL_SIZE` 来调整数据池大小。

  使用固定大小的数据缓冲区时，可以根据所接收网络数据的类型选择数据部分的大小，从而调整网络缓冲区的内存占用。如果将数据大小设置为 256，但只接收 32 字节长的数据包，那么每个数据包都会“浪费”224 字节，因为剩余数据无法使用。数据大小不应设置得过低，因为每个 net_buf 都有一定的开销。出于这些原因，默认网络缓冲区大小设置为 128 字节。

  可变大小数据缓冲区功能被标记为实验性，因为其测试程度不如固定大小缓冲区。使用可变大小数据缓冲区会按网络数据所需的最小数据量进行分配，从而尝试提高内存利用率。额外的代价是从内存池动态分配缓冲区所需的时间。

  例如，以太网的最大传输单元（MTU）大小为 1500 字节。如果要接收两个完整帧，则 net_pkt RX 计数应设置为 2，net_buf RX 计数应设置为 (1500 / 128) * 2，即 24。如果使用 TCP，则这些值需要更高，因为我们可以在将数据包交付给应用之前在内部排队。

:kconfig:option:`CONFIG_NET_BUF_TX_COUNT`
  用于发送数据的网络缓冲区分配数量。此设置与接收缓冲区计数类似，但用于发送。


连接选项
********

:kconfig:option:`CONFIG_NET_MAX_CONN`
  此选项指定支持多少个网络连接端点。例如，每个 TCP 连接需要一个连接端点。类似地，每个正在监听的 UDP 连接也需要一个连接端点。此外，DHCP 和 DNS 等各种系统服务也需要连接端点才能工作。可以在运行时使用网络 shell 命令 **net conn** 查看网络连接信息。

:kconfig:option:`CONFIG_NET_MAX_CONTEXTS`
  要分配的网络上下文数量。每个网络上下文描述一个网络五元组，用于监听或发送网络流量。系统中的每个 BSD socket 使用一个网络上下文。


Socket 选项
***********

:kconfig:option:`CONFIG_ZVFS_POLL_MAX`
  支持的 poll() 条目数量上限。需要根据系统中被轮询的 BSD socket 数量选择适当的值。

:kconfig:option:`CONFIG_ZVFS_OPEN_MAX`
  打开文件描述符数量上限，其中包括文件、socket、特殊设备等。需要根据系统中创建的 BSD socket 数量选择适当的值。

:kconfig:option:`CONFIG_ZVFS_EVENTFD_MAX`
  ZVFS eventfd 数量上限。多个网络子系统（例如 HTTP 服务器、CoAP 服务器、LwM2M 引擎、PTP、SSH 和 socket 服务）会分配一个 eventfd 来唤醒其轮询循环。每个此类子系统都通过 ``CONFIG_ZVFS_EVENTFD_ADD_SIZE_*`` 选项声明其需求，实际 eventfd 数量取此选项与所有需求之和中的较大值。仅当应用自行创建额外的 eventfd 时才显式设置此选项。

:kconfig:option:`CONFIG_NET_SOCKETPAIR_BUFFER_SIZE`
  此选项由 socketpair() 函数使用。它设置内部中间缓冲区的大小（以字节为单位），从而限制两个 socketpair 端点之间可以传递的消息大小。


TLS 选项
********

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_CONTEXTS`
  TLS/DTLS 上下文数量上限。每个 TLS/DTLS 连接需要一个上下文。

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_CREDENTIALS`
  此变量设置可用于特定 socket 的 TLS/DTLS 凭据数量上限。

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_CIPHERSUITES`
  每个 socket 的 TLS/DTLS 密码套件数量上限。如果通过 socket 选项显式设置，此变量设置可用于特定 socket 的 TLS/DTLS 密码套件数量上限。默认情况下，系统中可用的所有密码套件都可供该 socket 使用。

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_APP_PROTOCOLS`
  支持的应用层协议数量上限。此变量设置可通过 socket 选项显式设置的、基于 TLS/DTLS 的支持应用层协议数量上限。默认情况下，不设置任何支持的应用层协议。

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_CLIENT_SESSION_COUNT`
  此变量指定存储的 TLS/DTLS 会话数量上限，用于 TLS/DTLS 会话恢复。

:kconfig:option:`CONFIG_TLS_MAX_CREDENTIALS_NUMBER`
   可注册的 TLS 凭据数量上限。请确保该值足够大，以便所有证书都能加载到存储中。


IPv4/6 选项
***********

:kconfig:option:`CONFIG_NET_IF_MAX_IPV4_COUNT`
   系统中 IPv4 网络接口数量上限。这表示系统中将有多少个启用 IPv4 的网络接口。例如，如果有两个网络接口，但只有一个可以使用 IPv4 地址，则此值可以设置为 1。如果两个网络接口都可以使用 IPv4，则应设置为 2。

:kconfig:option:`CONFIG_NET_IF_MAX_IPV6_COUNT`
   系统中 IPv6 网络接口数量上限。此设置与 IPv4 计数选项类似，但用于 IPv6。


TCP 选项
********

:kconfig:option:`CONFIG_NET_TCP_TIME_WAIT_DELAY`
  在 TCP *TIME_WAIT* 状态下等待的时长（以毫秒为单位）。为避免之前连接的延迟数据包被投递到复用相同本地/远端端口的下一个连接这一（低概率）问题，`RFC 793 <https://www.rfc-editor.org/rfc/rfc793>`_ （TCP）建议将已关闭的旧连接在特殊的 *TIME_WAIT* 状态下保持 2*MSL（Maximum Segment Lifetime，最大报文段生存时间）的时长。RFC 建议使用 2 分钟的 MSL，但指出

  *这是一项工程选择，如果经验表明有必要更改，可以进行调整。*

  对于资源受限的系统，较大的 MSL 可能导致资源快速耗尽（以及相关的 DoS 攻击）。同时，现代 TCP 协议栈通过使用随机且不重复的端口号和初始序列号，已在很大程度上缓解了数据包误投递问题。因此，Zephyr 默认使用低得多的 1500ms。值 0 会完全禁用 *TIME_WAIT* 状态。

:kconfig:option:`CONFIG_NET_TCP_RETRY_COUNT`
  TCP 报文段最大重传次数。可以使用以下公式确定报文段在等待重传时的缓冲时间（以毫秒为单位）：

  .. math::

     \sum_{n=0}^{\mathtt{NET\_TCP\_RETRY\_COUNT}} \bigg(1 \ll n\bigg)\times
     \mathtt{NET\_TCP\_INIT\_RETRANSMISSION\_TIMEOUT}

  默认值为 9 时，IP 协议栈会尝试重传最多 1:42 分钟。这尽可能接近 `RFC 1122 <https://www.rfc-editor.org/rfc/rfc1122>`_ 推荐的最小值（1:40 分钟）。重传计数只分配了 5 位，因此可接受的取值范围是 0-31。不过，强烈建议不要低于 9。

  如果发生重传超时，将使用 :code:`-ETIMEDOUT` 错误码调用接收回调，并取消引用该上下文。

:kconfig:option:`CONFIG_NET_TCP_MAX_SEND_WINDOW_SIZE`
  要使用的最大发送窗口大小。此值影响 TCP 如何选择最大发送窗口。默认值 0 让 TCP 协议栈根据系统中配置的网络缓冲区数量自动选择该值。请注意，如果系统中有多个活动 TCP 连接，则可能需要微调（降低）此值，否则多个 TCP 连接很容易耗尽用于排队 TX 数据的 net_buf 池。

:kconfig:option:`CONFIG_NET_TCP_MAX_RECV_WINDOW_SIZE`
  要使用的最大接收窗口大小。此值定义 TCP 最大接收窗口大小。增大此值可以提高连接吞吐量，但需要系统中有更多可用接收缓冲区才能高效运行。默认值 0 让 TCP 协议栈根据系统中配置的网络缓冲区数量自动选择该值。

:kconfig:option:`CONFIG_NET_TCP_RECV_QUEUE_TIMEOUT`
  接收数据的排队时长（以毫秒为单位）。如果收到乱序 TCP 数据，我们会将其排队。此值表示在无法将数据传递给应用时，数据在被丢弃之前保留多长时间。如果设置为 0，则不启用接收排队。该值以毫秒为单位。

  请注意，当前版本仅按顺序排队数据，即队列中不应出现空洞。例如，如果收到 SEQ 5、4、3、6，并且正在等待 SEQ 2，则来自报文段 3、4、5、6 的数据会（按此顺序）排队，并在收到 SEQ 2 时交给应用。但如果收到 SEQ 5、4、3、7，则 SEQ 7 会被丢弃，因为缺少编号 6，列表将无法保持顺序。


流量类别选项
************

接收或发送网络数据时，可以配置多个流量类别（队列）。每个流量类别队列实现为一个具有不同优先级的线程。这意味着可以将更高优先级的网络数据包放入更高优先级的网络队列，从而更快或更慢地发送或接收它。由于线程调度延迟，实际上将数据包发送出去最快的方式是直接发送，而不使用专用流量类别线程。因此，如果未启用用户空间，默认情况下 :kconfig:option:`CONFIG_NET_TC_TX_COUNT` 选项设置为 0。如果启用了用户空间，则 TX 流量类别计数至少为 1。原因在于用户空间应用没有足够权限直接传递消息。

在接收侧，建议至少有一个接收流量类别队列。原因是网络设备驱动程序通常在 IRQ 上下文中接收数据包，此时不应尝试将网络数据包直接传递给上层，而应将数据包放入流量类别队列。如果网络设备驱动程序在获取数据包时未运行在 IRQ 上下文中，则可以将 RX 流量类别选项 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` 设置为 0。


栈大小选项
**********

在启用网络的系统中有几个网络专用线程。某些线程可能依赖于可启用或禁用某项功能的配置选项。每个线程栈大小都经过优化，以支持正常的网络操作。

默认情况下，网络管理 API 使用一个专用线程。如果启用了 :kconfig:option:`CONFIG_NET_MGMT` 和 :kconfig:option:`CONFIG_NET_MGMT_EVENT` 选项，该线程负责将网络管理事件传递给系统中设置的事件监听器。如果启用了这些选项，用户可以注册一个回调函数，net_mgmt 线程会为每个网络管理事件调用该函数。默认情况下，net_mgmt 事件线程栈大小相当小。其思路是回调函数执行最少的工作，以便新事件能尽快传递给监听器且不会丢失。net_mgmt 事件线程栈大小由 :kconfig:option:`CONFIG_NET_MGMT_EVENT_QUEUE_SIZE` 选项控制。建议不要在回调函数中执行任何阻塞操作。

可以通过内核 shell 的 **kernel threads** 命令监控网络线程栈的使用情况。
