.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_shell:

网络 shell
##########

网络 shell 及其配套 shell 提供了辅助工具，用于了解网络状态、启用/禁用功能以及执行 ping、DNS 解析等命令。请注意， ``net-shell`` 可能不应在生产代码中使用，因为它需要额外的内存。有关 shell 的详细信息，另请参见 :ref:`通用 shell <shell_api>`。

请注意，默认情况下，已启用和已禁用的 net-shell 命令都对用户可用。这有助于用户发现有哪些命令可用以及如何启用它们。可以通过禁用 :kconfig:option:`CONFIG_NET_SHELL_SHOW_DISABLED_COMMANDS` 选项来关闭此额外帮助信息。

实现了以下 net-shell 命令：

.. csv-table:: net-shell 命令
   :header: "命令", "描述"
   :widths: 15 85

   "net allocs", "打印网络内存分配信息。仅在设置了 :kconfig:option:`CONFIG_NET_DEBUG_NET_PKT_ALLOC` 选项时可用。"
   "net arp", "打印 IPv4 ARP 缓存信息。仅在启用了 IPv4 的网络中设置了 :kconfig:option:`CONFIG_NET_ARP` 选项时可用。"
   "net bridge", "打印信息并操作以太网网桥。仅在设置了 :kconfig:option:`CONFIG_NET_ETHERNET_BRIDGE_SHELL` 选项时可用。"
   "net capture", "监控网络流量。详情见 :ref:`network_monitoring`。"
   "net cm", "连接管理器 shell。仅在设置了 :kconfig:option:`CONFIG_NET_CONNECTION_MANAGER` 选项时可用。"
   "net conn", "打印网络连接信息。"
   "net dhcpv4", "启用/禁用 DHCPv4 客户端或服务器支持。仅在设置了 :kconfig:option:`CONFIG_NET_DHCPV4_SERVER` 或 :kconfig:option:`CONFIG_NET_DHCPV4` 选项时可用。"
   "net dhcpv6", "启用/禁用 DHCPv6 客户端支持。仅在设置了 :kconfig:option:`CONFIG_NET_DHCPV6` 选项时可用。"
   "net dns", "显示 DNS 的配置方式。该命令还可用于解析 DNS 名称。仅在设置了 :kconfig:option:`CONFIG_DNS_RESOLVER` 选项时可用。"
   "net events", "启用网络事件监控。仅在设置了 :kconfig:option:`CONFIG_NET_MGMT_EVENT_MONITOR` 选项时可用。"
   "net filter", "查看网络数据包过滤规则。仅在设置了 :kconfig:option:`CONFIG_NET_PKT_FILTER` 选项时可用。"
   "net ftp", "连接到 FTP 服务器以传输文件。仅在设置了 :kconfig:option:`CONFIG_FTP_CLIENT` 选项时可用。"
   "net gptp", "打印 gPTP 支持信息。仅在设置了 :kconfig:option:`CONFIG_NET_GPTP` 选项时可用。"
   "net http", "显示 HTTP 服务器信息，或发送 HTTP GET/POST/PUT/DELETE 请求。仅在设置了 :kconfig:option:`CONFIG_HTTP_SERVER` 或 :kconfig:option:`CONFIG_HTTP_CLIENT` 选项时可用。"
   "net iface", "打印网络接口信息。"
   "net ipv4", "打印 IPv4 特定信息和配置。仅在设置了 :kconfig:option:`CONFIG_NET_IPV4` 选项时可用。"
   "net ipv6", "打印 IPv6 特定信息和配置。仅在设置了 :kconfig:option:`CONFIG_NET_IPV6` 选项时可用。"
   "net mem", "打印网络内存使用信息。如果设置了 :kconfig:option:`CONFIG_NET_BUF_POOL_USAGE` 选项，该命令将打印更多信息。"
   "net nbr", "打印邻居信息。仅在设置了 :kconfig:option:`CONFIG_NET_IPV6` 选项时可用。"
   "net ping", "对网络主机执行 ping。"
   "net pkt", "打印低层网络数据包信息以用于调试。 "
   "net pmtu", "打印 MTU 路径发现信息。仅在设置了 :kconfig:option:`CONFIG_NET_IPV6_PMTU` 或 :kconfig:option:`CONFIG_NET_IPV4_PMTU` 选项时可用。"
   "net ppp", "打印点对点协议信息。仅在同时设置了 :kconfig:option:`CONFIG_NET_L2_PPP` 和 :kconfig:option:`CONFIG_NET_PPP` 选项时可用。"
   "net ptp", "打印 PTP 支持信息。使用 ``net ptp <port>`` 查看每个端口的详细信息。仅在设置了 :kconfig:option:`CONFIG_PTP` 选项时可用。"
   "net qbv", "显示并配置 IEEE 802.1Qbv 时间感知整形器（TAS）信息。仅在设置了 :kconfig:option:`CONFIG_NET_QBV` 选项时可用。"
   "net quic", "显示并配置 QUIC 传输。仅在设置了 :kconfig:option:`CONFIG_QUIC` 选项时可用。"
   "net resume", "如果启用了网络电源管理，则恢复网络接口。"
   "net route", "显示 IPv6 或 IPv4 网络路由。仅在设置了 :kconfig:option:`CONFIG_NET_IPV6_ROUTING` 或 :kconfig:option:`CONFIG_NET_IPV4_ROUTING` 选项时可用。"
   "net sockets", "显示网络 socket 信息和统计信息。仅在同时设置了 :kconfig:option:`CONFIG_NET_SOCKETS_OBJ_CORE` 和 :kconfig:option:`CONFIG_OBJ_CORE` 选项时可用。"
   "net ssh", "SSH 客户端支持。仅在设置了 :kconfig:option:`CONFIG_SSH_CLIENT` 选项时可用。"
   "net sshd", "SSH 服务器支持。仅在设置了 :kconfig:option:`CONFIG_SSH_SERVER` 选项时可用。"
   "net ssh_key", "支持生成/删除/保存/加载 SSH 密钥。仅在设置了 :kconfig:option:`CONFIG_SSH_CLIENT` 或 :kconfig:option:`CONFIG_SSH_SERVER` 选项时可用。"
   "net stats", "显示网络统计信息。"
   "net suspend", "如果启用了网络电源管理，则挂起网络接口。"
   "net tcp", "连接/发送数据/关闭 TCP 连接。仅在设置了 :kconfig:option:`CONFIG_NET_TCP` 选项时可用。"
   "net udp", "直接从 shell 发送 UDP 数据。仅在设置了 :kconfig:option:`CONFIG_NET_UDP` 选项时可用。"
   "net virtual", "显示并操作网络虚拟接口。仅在设置了 :kconfig:option:`CONFIG_NET_L2_VIRTUAL` 选项时可用。"
   "net vlan", "显示以太网虚拟 LAN 信息。仅在设置了 :kconfig:option:`CONFIG_NET_VLAN` 选项时可用。"
   "net websocket", "打印 websocket 信息。仅在设置了 :kconfig:option:`CONFIG_WEBSOCKET_CLIENT` 选项时可用。"
   "net wg", "显示 WireGuard VPN 信息并设置 VPN。仅在设置了 :kconfig:option:`CONFIG_WIREGUARD` 选项时可用。"

Wi-Fi shell 提供了扫描、连接、断开连接和配置 Wi-Fi 网络的命令。实现了以下 Wi-Fi shell 命令：

.. csv-table:: wifi-shell 命令
   :header: "Command", "Description"
   :widths: 15 85

   "wifi <cmd>", "用于 Wi-Fi 网络连接、断开连接、扫描和配置的多个命令。仅在设置了 :kconfig:option:`CONFIG_NET_L2_WIFI_SHELL` 选项时可用。"
   "wifi cred", "显示/添加/删除 Wi-Fi 网络凭据。仅在设置了 :kconfig:option:`CONFIG_WIFI_CREDENTIALS_SHELL` 选项时可用。详情见 :ref:`lib_wifi_credentials`。"

TLS 凭据 shell 提供了从易失性或受保护的后端存储中列出、添加、删除和检索 TLS 凭据信息的命令。实现了以下 TLS 凭据 shell 命令。这些命令仅在设置了 :kconfig:option:`CONFIG_TLS_CREDENTIALS_SHELL` 选项时可用。详情见 :ref:`tls_credentials_shell`。

.. csv-table:: tls-credentials-shell 命令
   :header: "Command", "Description"
   :widths: 15 85

   "cred buf", "将凭据数据放入缓冲区，以便添加。"
   "cred add", "添加 TLS 凭据。"
   "cred del", "删除 TLS 凭据。"
   "cred get", "检索 TLS 凭据的内容。"
   "cred list", "列出已存储的 TLS 凭据。"
