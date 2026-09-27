.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _vlan_interface:

虚拟 LAN（VLAN）支持
####################

.. contents::
    :local:
    :depth: 2

概述
****

`Virtual LAN <https://wikipedia.org/wiki/Virtual_LAN>`_ （VLAN）是在数据链路层（OSI 第 2 层）划分并隔离的计算机网络。对于以太网而言，这指的是 `IEEE 802.1Q <https://en.wikipedia.org/wiki/IEEE_802.1Q>`_

在 Zephyr 中，每个 VLAN 都建模为一个虚拟网络接口。这意味着系统中有一个以太网网络接口对应真实的物理以太网端口。每个 VLAN 都会创建一个虚拟网络接口，该虚拟网络接口连接到真实的网络接口。这与 Linux 实现 VLAN 的方式类似。*eth0* 是真实的网络接口，*vlan0* 是运行在 *eth0* 之上的虚拟网络接口。

必须在编译时启用 VLAN 支持：设置 :kconfig:option:`CONFIG_NET_VLAN` 选项，并将 :kconfig:option:`CONFIG_NET_VLAN_COUNT` 设置为系统中网络接口的数量。例如，如果有一个不支持 VLAN 的网络接口和两个支持 VLAN 的网络接口，则 :kconfig:option:`CONFIG_NET_VLAN_COUNT` 选项应设置为 3。

即使在 :file:`prj.conf` 文件中启用了 VLAN，也需要应用在运行时激活 VLAN。VLAN API 提供了 :c:func:`net_eth_vlan_enable` 函数来完成这一操作。应用需要将该网络接口和所需的 VLAN 标签作为参数传给该函数。可以通过 :c:func:`net_eth_vlan_disable` 函数禁用指定网络接口的 VLAN 标记。应用需要自行配置 VLAN 网络接口，例如设置 IP 地址等。

API 用法示例另见 :zephyr:code-sample:`VLAN 示例应用 <vlan>`。该示例应用的源代码位于 :zephyr_file:`samples/net/ethernet/vlan`。

net-shell 模块包含 *net vlan add* 和 *net vlan del* 命令，可用于启用或禁用指定网络接口的 VLAN 标签。

有关以太网 VLAN 的更多信息，请参见 `IEEE 802.1Q spec`_。

.. _IEEE 802.1Q spec: https://ieeexplore.ieee.org/document/6991462/

API 参考
********

.. doxygengroup:: vlan_api
