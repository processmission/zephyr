.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_pkt_processing_stats:

网络数据包处理统计信息
######################

.. contents::
    :local:
    :depth: 2

本页面介绍如何获取网络协议栈内部网络数据包处理的统计信息。

网络协议栈包含用于测量网络数据包在发送或接收路径上处理耗时的基础设施。有两个 Kconfig 选项可控制此功能。对于发送（TX）路径，该选项称为 :kconfig:option:`CONFIG_NET_PKT_TXTIME_STATS`；对于接收（RX）路径，该选项称为 :kconfig:option:`CONFIG_NET_PKT_RXTIME_STATS`。请注意，对于 TX，会收集所有类型的网络数据包统计信息；对于 RX，只收集 UDP、TCP 或原始数据包类型的网络数据包统计信息。

启用这些选项后，:ref:`net stats <net_shell>` 网络 shell 命令将显示以下信息：

.. code-block:: console

   Avg TX net_pkt (11484) time 67 us
   Avg RX net_pkt (11474) time 43 us

.. note::

   上面和下面的值来自模拟的 qemu_x86 开发板和 UDP 流量

TX 时间表示网络数据包从创建到发送到网络所花费的时间。RX 时间表示网络数据包从创建到传递给应用所花费的时间。这些值以微秒为单位。如果系统中定义了多个发送或接收队列，统计信息将按流量类别收集。这些由 :kconfig:option:`CONFIG_NET_TC_TX_COUNT` 和 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` 选项控制。

如果启用 :kconfig:option:`CONFIG_NET_PKT_TXTIME_STATS_DETAIL` 或 :kconfig:option:`CONFIG_NET_PKT_RXTIME_STATS_DETAIL` 选项，则当网络数据包经过 IP 协议栈时，会收集 TX 或 RX 网络数据包的额外信息。

启用这些选项后，:ref:`net stats <net_shell>` 将显示以下信息：

.. code-block:: console

   Avg TX net_pkt (18902) time 63 us    [0->22->15->23=60 us]
   Avg RX net_pkt (18892) time 42 us    [0->9->6->11->13=39 us]

括号内的数字表示网络数据包从前一个状态进入下一个状态所经过的微秒数。

在上面的 TX 示例中，这些值是 **18902** 个数据包的平均值，包含以下信息：

* 数据包由应用创建，因此该时间为 **0**。
* 数据包即将被放入发送队列。在本示例中，从网络数据包创建到进入此状态所花费的时间为 **22** 微秒。
* 调用正确的 TX 线程，并从发送队列读取数据包。相对于前一个状态，这花费了 **15** 微秒。
* 网络数据包刚刚发送完毕，网络协议栈即将释放该网络数据包。相对于前一个状态，这花费了 **23** 微秒。
* 总的来说，发送网络数据包平均花费 **60** 微秒。**63** 这个值也表达了相同的信息，但计算方法不同，因此由于舍入误差而略有差异。

在上面的 RX 示例中，这些值是 **18892** 个数据包的平均值，包含以下信息：

* 数据包由网络设备驱动程序创建，因此该时间为 **0**。
* 数据包即将被放入接收队列。在本示例中，从网络数据包创建到进入此状态所花费的时间为 **9** 微秒。
* 调用正确的 RX 线程，并从接收队列读取数据包。相对于前一个状态，这花费了 **6** 微秒。
* 然后处理网络数据包，并将其放入正确的 socket 队列。相对于前一个状态，这花费了 **11** 微秒。
* 最后一个值表示从该状态到应用所花费的时间。此处该值为 **13** 微秒。
* 总的来说，发送网络数据包平均花费 **39** 微秒。**42** 这个值也表达了相同的信息，但计算方法不同，因此由于舍入误差而略有差异。
