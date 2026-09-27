.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _traffic-class-support:

流量分类
########

概述
****

`Traffic classification <https://en.wikipedia.org/wiki/Traffic_classification>`_ （流量分类）是一种根据各种参数对计算机网络流量进行分类的自动化过程。在 Zephyr 中，使用 VLAN 优先级代码点（PCP）对接收和发送的网络数据包进行分类。有关 VLAN 优先级的更多信息，请参见 `IEEE 802.1Q <https://en.wikipedia.org/wiki/IEEE_802.1Q>`_。

默认情况下，Zephyr 中所有网络流量都同等对待。如有需要，可以使用 :kconfig:option:`CONFIG_NET_TC_TX_COUNT` 选项设置发送队列的数量，使用 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` 选项设置接收队列的数量。每个流量类别队列对应一个特定的内核工作队列，每个内核工作队列都有一个优先级。VLAN 优先级按照 `IEEE 802.1Q spec`_ 第 I.3 章、第 8.6.6 章表 8-4 和第 34.5 章表 34-1 中规定的规则映射到特定的流量类别。每个流量类别又映射到特定的内核工作队列。接收和发送的流量类别数量上限均为 8。

各种映射的具体实现细节见 :zephyr_file:`subsys/net/ip/net_tc.c`。

.. _IEEE 802.1Q spec: https://ieeexplore.ieee.org/document/6991462/
