.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ip_stack_overview:

概述
####

.. contents::
    :local:
    :depth: 2

支持的功能
**********

网络 IP 协议栈采用模块化设计，可通过构建时配置选项进行高度配置。只启用应用所需的网络功能即可将系统内存占用降至最低。几乎所有功能都可以按需禁用。

* 支持 **IPv6** （:rfc:`8200`）。可根据网络需求启用或禁用各种 IPv6 子选项。

  * 开发者可以设置同时处于活动状态的单播和组播 IPv6 地址数量。
  * 设备的 IPv6 地址可以静态设置，也可以使用 SLAAC（无状态地址自动配置，:rfc:`4862`）动态设置。
  * 系统还支持多个 IPv6 前缀，最大 IPv6 前缀数量可在构建时配置。
  * 如果不需要，可以禁用 IPv6 邻居缓存，其大小也可在构建时配置。
  * 默认启用 IPv6 邻居发现支持（:rfc:`4861`）。
  * 默认启用组播监听者发现第 2 版支持（:rfc:`3810`）。
  * 对于 IEEE 802.15.4 网络，可以使用 IPv6 报头压缩（6lo）提供 IPv6 连接（:rfc:`4944`）。
  * 支持 DHCPv6（Dynamic Host Configuration Protocol for IPv6）客户端功能（:rfc:`8415`）。
  * 支持 IPv6 隐私扩展（:rfc:`8981`）。

* 支持 **IPv4** （:rfc:`791`）。IEEE 802.15.4 无法使用 IPv4，因为该网络技术仅支持 IPv6。例如，IPv4 可用于基于以太网、Wi-Fi 和蜂窝网络的网络。

  * 支持 DHCP（Dynamic Host Configuration Protocol）客户端和服务器（:rfc:`2131`）。
  * 也可以手动配置 IPv4 地址。默认支持静态 IPv4 地址。
  * 支持 IPv4 NAT（Network Address Translation）。通过执行 SNAT 和 DNAT，数据包可以在接口之间跳转。使用连接跟踪和 iptable 规则跨子网过滤和转发数据包。

* **双栈支持。** 网络协议栈允许开发者将系统配置为同时使用 IPv6 和 IPv4。

* 支持 **UDP** （User Datagram Protocol，:rfc:`768`）。开发者可以发送 UDP 数据报（客户端支持），也可以创建监听器接收发往特定端口的 UDP 数据包（服务器端支持）。

* 支持 **TCP** （Transmission Control Protocol，:rfc:`793`）。应用可以同时充当服务器和客户端角色。可供应用使用的 TCP socket 数量可在构建时配置。可通过 :kconfig:option:`CONFIG_NET_TCP_SACK` 对接收的数据启用选择性确认（:rfc:`2018`）。

* **BSD Sockets API** 已实现 :ref:`BSD socket 兼容 API <bsd_sockets_interface>` 的一个子集。同时支持阻塞和非阻塞的数据报（UDP）及流式（TCP）socket。还支持数据包 socket（``AF_PACKET``）。

* **Secure Sockets API** 针对 sockets API 的 TLS/DTLS 安全协议及配置选项提供实验性支持。实现所用的安全函数由 Mbed TLS 库提供。

* 支持 **MQTT** （Message Queue Telemetry Transport，ISO/IEC PRF 20922）3.1.1 和 5.0 版本。提供了适用于 MQTT v3.1.1 和 v5.0 的示例客户端应用 :zephyr:code-sample:`mqtt-publisher`。

* 支持 **MQTT-SN** （MQTT for Sensor Networks）1.2 版本。提供了示例客户端应用 :zephyr:code-sample:`mqtt-sn-publisher`。

* 支持 **CoAP** （Constrained Application Protocol，:rfc:`7252`）。提供了 :zephyr:code-sample:`coap-client` 和 :zephyr:code-sample:`coap-server` 两个示例应用。

* **LwM2M** 通过“Bootstrap”、“Client Registration”、“Device Management & Service Enablement”和“Information Reporting”接口支持 OMA Lightweight Machine-to-Machine Protocol（`LwM2M specification 1.0.2`_）。系统实现了所需的核心 LwM2M 对象以及若干 IPSO 智能对象。使用 Kconfig 选项启用后，还可以类似方式支持 `LwM2M specification 1.1.1`_。示例 :zephyr:code-sample:`lwm2m-client` 演示了该库的用法。

* **HTTP** 支持 Hypertext Transfer Protocol 客户端和服务器。:ref:`http_client_interface` 库支持 HTTP/1.1（:rfc:`2616`）。:ref:`http_server_interface` 库支持 HTTP/1.1（:rfc:`2616`）和 HTTP/2（:rfc:`9113`）。提供了 :zephyr:code-sample:`sockets-http-client` 和 :zephyr:code-sample:`sockets-http-server` 示例。

* 支持 **Websocket** 客户端（:rfc:`6455`）。提供了 :zephyr:code-sample:`sockets-websocket-client` 示例。

* 支持 **DNS** Domain Name Service 客户端功能（:rfc:`1035`）。应用可以使用 DNS API 向 DNS 服务器查询域名信息或 IP 地址。可查询 IPv4（A）和 IPv6（AAAA）记录。同时支持多播 DNS（mDNS，:rfc:`6762`）和链路本地多播名称解析（LLMNR，:rfc:`4795`）。还支持 DNS 服务发现（:rfc:`6763`）。

* **网络管理 API。** 应用可以使用网络管理 API 监听核心网络协议栈生成的管理事件，例如为设备添加 IP 地址或网络接口启动等。

* **Wi-Fi 管理 API。** 应用可以使用 Wi-Fi 管理 API 管理接口，例如连接到 Wi-Fi 网络以及扫描可用的 Wi-Fi 网络。

* **Wi-Fi 网络管理器 API。** Wi-Fi 网络管理器可以向 Wi-Fi 协议栈注册自身，随后实现 Wi-Fi 管理 API 并管理 Wi-Fi 接口。

* **多种网络技术。** 只需在 Kconfig 中启用相应选项，即可将 Zephyr OS 配置为同时支持多种网络技术：例如以太网、Wi-Fi 和 802.15.4。请注意，这些技术之间不提供自动 IP 路由功能。应用可以根据自身需求将数据发送到指定的网络接口。

* **最小复制网络缓冲区管理。** 可以采用最小复制的网络数据路径，即系统在将应用数据发送到网络时尽量避免复制数据。

* **虚拟 LAN 支持。** 虚拟 LAN（VLAN）允许将以太网物理网络划分为多个逻辑网络。更多详情见 :ref:`VLAN 支持 <vlan_interface>`。

* **网络流量分类。** 可以根据应用需求对发送和接收的网络数据包划分优先级。更多详情见 :ref:`流量分类 <traffic-class-support>`。

* **时间敏感网络。** 同时支持 gPTP（generalized Precision Time Protocol）和 PTP（Precision Time Protocol，IEEE 1588）。更多详情见 :ref:`gPTP 支持 <gptp_interface>` 和 :ref:`PTP 支持 <ptp_interface>`。

* 支持 **SNTP** Simple Network Time Protocol 客户端（:rfc:`5905`）。提供了 :zephyr:code-sample:`sntp-client` 示例。

* 支持 **SOCKS5** 代理第 5 版（:rfc:`1928`）。

* 支持 **TFTP** Trivial File Transfer Protocol 客户端（:rfc:`1350`）。提供了 :zephyr:code-sample:`tftp-client` 示例。

* 支持 **MIDI2** MIDI 2.0 网络 UDP 传输。提供了 :zephyr:code-sample:`netmidi2` 示例。

* 支持 **OCPP** Open Charge Point Protocol。提供了 :zephyr:code-sample:`ocpp` 示例。

* 支持 **Prometheus** 指标服务器功能。提供了 :zephyr:code-sample:`prometheus`。

* **网络 shell。** 网络 shell 提供了用于了解网络状态、启用/禁用功能以及执行 ping、DNS 解析等命令的辅助工具。开发网络软件时，net-shell 非常有用。更多详情见 :ref:`网络 shell <net_shell>`。

* **zperf** 是一款 iPerf v2 网络性能和带宽测量工具。同时支持客户端和服务器功能。提供了 :zephyr:code-sample:`zperf` 示例。

此外，Zephyr OS 还支持以下网络技术（链路层）：

* IEEE 802.15.4
* 蓝牙
* 以太网，IEEE 802.3
* Wi-Fi，IEEE 802.11
* 蜂窝网络 / PPP（:rfc:`1661`）
* Thread（提供了 :zephyr:code-sample-category:`openthread` 示例）
* 用于 SocketCAN 的 CAN 总线
* SLIP（串行线路上的 IP）。用于在 QEMU 中测试。它为主机系统（如 Linux）提供以太网接口，测试应用可以在 Linux 主机上运行并向 Zephyr OS 设备发送网络数据。

源码树布局
**********

网络协议栈的源码树组织如下：

:zephyr_file:`subsys/net/`
  这里存放各种可选的网络协议栈组件，如连接管理器、数据包过滤代码和主机名处理。

:zephyr_file:`subsys/net/ip/`
  这里存放核心网络协议栈代码。

:zephyr_file:`subsys/net/l2`
  这里存放 IP 协议栈第 2 层代码，包括对以太网、IEEE 802.15.4 和 Wi-Fi 的通用支持。

:zephyr_file:`subsys/net/lib/`
  应用层协议（DNS、MQTT 等）以及其他协议栈组件（BSD Sockets 等）。

:zephyr_file:`include/zephyr/net/`
  公共 API 头文件。应用需要包含这些头文件才能使用 IP 网络功能。

:zephyr_file:`samples/net/`
  网络示例代码。这是入门网络应用开发的良好参考。

:zephyr_file:`tests/net/`
  测试应用。这些应用用于验证 IP 协议栈的功能，但不是示例代码的最佳来源（请参见 :zephyr_file:`samples/net/`）。

.. _LwM2M specification 1.0.2:
   https://www.openmobilealliance.org/release/LightweightM2M/V1_0_2-20180209-A/OMA-TS-LightweightM2M-V1_0_2-20180209-A.pdf

.. _LwM2M specification 1.1.1:
   https://www.openmobilealliance.org/release/LightweightM2M/V1_1_1-20190617-A/
