.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _network_stack_architecture:

网络协议栈架构
##############

.. toctree::
   :maxdepth: 1
   :hidden:

   net_pkt_processing_stats.rst

Zephyr 网络协议栈是专为 Zephyr OS 设计的原生网络协议栈。它由多个层组成，每一层都旨在为其他层提供特定的服务。网络协议栈的功能可通过 Kconfig 选项进行高度配置。

.. contents::
    :local:
    :depth: 2

网络协议栈的高层概览
********************

.. figure:: zephyr_netstack_overview.svg
    :alt: 网络协议栈架构概览
    :figclass: align-center

    网络协议栈概览

网络协议栈采用分层结构，由以下几部分组成：

* **网络应用。** 网络应用既可以使用所提供的应用层协议库，也可以直接访问 :ref:`BSD socket API <bsd_sockets_interface>` 来创建网络连接、收发数据和关闭连接。应用还可以使用 :ref:`网络管理 API <net_mgmt_interface>` 配置网络并设置网络链路选项、启动扫描（如适用）、监听网络配置事件等相关参数。:ref:`网络接口 API <net_if_interface>` 可用于为网络接口设置 IP 地址、关闭网络接口等。

* **网络协议。** 这部分提供各种协议的实现，例如

  * CoAP、LwM2M 和 MQTT 等应用层网络协议。相关信息见 :ref:`应用层协议一章 <net_protocols>`。
  * IPv6、IPv4、UDP、TCP、ICMPv4 和 ICMPv6 等核心网络协议。通过 :ref:`BSD socket API <bsd_sockets_interface>` 访问这些协议。

* **网络接口抽象。** 这部分提供所有网络接口通用的功能，例如关闭网络接口等。系统中可以有多个网络接口。更多详情见 :ref:`网络接口概览 <net_if_interface>`。

* **L2 网络技术。** 这部分提供与实际网络设备之间收发数据的通用 API。更多详情见 :ref:`L2 概览 <net_l2_interface>`。

  这些网络技术包括 :ref:`以太网 <ethernet_interface>`、:ref:`IEEE 802.15.4 <ieee802154_interface>`、:ref:`蓝牙 <bluetooth_api>`、:ref:`CANBUS <can_api>` 等。

  其中一些技术支持 IPv6 报头压缩（6Lo），详情见 :rfc:`6282`。例如，IPv4 的 ARP（:rfc:`826`）由 :ref:`以太网组件 <ethernet_interface>` 完成。

* **网络设备驱动。** 实际的低层设备驱动负责网络数据包的物理收发。

网络数据流
**********

应用通常由一个或多个执行应用逻辑的 :ref:`线程 <threads_v2>` 组成。使用 :ref:`BSD socket API <bsd_sockets_interface>` 时，会发生以下情况。

.. figure:: zephyr_netstack_overview-rx_sequence.svg
    :alt: Network RX data flow
    :figclass: align-center

    网络接收（RX）数据流

数据接收（RX）
--------------

1. 设备驱动接收网络数据包。

2. 设备驱动分配足够数量的网络缓冲区来存储接收到的数据。网络数据包被放入相应的接收队列（由 :ref:`k_fifo <fifos_v2>` 实现）。默认情况下系统中只有一个接收队列，但最多可以有 8 个接收队列。这些队列会以不同的优先级处理传入的数据包。更多详情见 :ref:`traffic-class-support`。接收队列还用于分离数据处理流水线（bottom-half），因为设备驱动在中断上下文中运行，必须尽可能快地完成处理。

3. 随后，网络数据包被传递给正确的 L2 驱动。L2 驱动可以检查数据包是否正确，并在需要时进行修改，例如剥离 L2 报头和帧校验序列等。

4. 数据包由网络接口处理。如果启用了 :kconfig:option:`CONFIG_NET_STATISTICS`，则收集网络统计信息。

5. 随后数据包进入 L3 处理。如果数据包基于 IP，L3 层会检查它是否是正确的 IPv6 或 IPv4 数据包。

6. 然后 socket 处理程序会找到该网络数据包所属的活动 socket，并将其放入该 socket 的队列中，从而将网络代码与应用分离。通常应用运行在用户空间上下文中，而网络协议栈运行在内核上下文中。

7. 随后应用会接收数据并根据需要处理。应用应使用 :ref:`BSD socket API <bsd_sockets_interface>` 创建用于接收数据的 socket。


.. figure:: zephyr_netstack_overview-tx_sequence.svg
    :alt: Network TX data flow
    :figclass: align-center

    网络发送（TX）数据流

数据发送（TX）
--------------

1. 应用发送数据时应使用 :ref:`BSD socket API <bsd_sockets_interface>`。

2. 应用数据被准备好发送到内核空间，然后复制到内部 net_buf 结构中。

3. 根据 socket 类型的不同，会在数据前面添加协议报头。例如，如果 socket 是 UDP socket，则会构造 UDP 报头并将其置于数据前面。

4. 对于 UDP 或 TCP 数据包，会为其添加 IP 报头。

5. 网络协议栈会检查是否为该网络数据包正确设置了网络接口，并在数据排队发送之前确保网络接口已启用。

6. 随后对网络数据包进行分类，并将其放入相应的发送队列（由 :ref:`k_fifo <fifos_v2>` 实现）。默认情况下系统中只有一个发送队列，但最多可以有 8 个发送队列。这些队列会以不同的优先级处理发送的数据包。更多详情见 :ref:`traffic-class-support`。发送数据包分类完成后，由正确的 L2 层模块检查数据包。L2 模块会对数据做进一步检查，并为网络数据包构造所需的 L2 报头。如果一切正常，数据将交给网络设备驱动发送出去。

7. 设备驱动会将数据包发送到网络。

请注意，在 TX 和 RX 两条数据路径中，队列（:ref:`k_fifo <fifos_v2>`）构成了数据从一个 :ref:`线程 <threads_v2>` 传递到另一个线程的分离点。这些 :ref:`线程 <threads_v2>` 可能运行在不同的上下文中（:ref:`内核 <kernel_api>` 与 :ref:`用户空间 <usermode_api>`），并具有不同的 :ref:`优先级 <scheduling_v2>`。


网络数据包处理统计
******************

网络处理统计信息见 :ref:`此处 <net_pkt_processing_stats>`。
