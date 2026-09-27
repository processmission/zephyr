.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ethernet_interface:

以太网
######

.. contents::
    :local:
    :depth: 2

.. toctree::
   :maxdepth: 1

   mac_config.rst
   vlan.rst
   lldp.rst
   8021Qav.rst

概述
****

以太网是一种常用于局域网（LAN）的网络技术。更多信息请参见 `Ethernet Wikipedia article <https://en.wikipedia.org/wiki/Ethernet>`_。

Zephyr 支持以下以太网功能：

* 10、100 和 1000 Mbit/s 链路
* 自动协商
* 半双工/全双工
* 混杂模式
* TX 和 RX 校验和卸载
* MAC 地址过滤
* :ref:`MAC 地址配置 <mac_address_config>`
* :ref:`虚拟 LAN（VLAN） <vlan_interface>`
* :ref:`优先级队列 <traffic-class-support>`
* :ref:`IEEE 802.1AS (gPTP) <gptp_interface>`
* :ref:`IEEE 802.1Qav（基于信用的整形） <8021Qav>`
* :ref:`LLDP（链路层发现协议） <lldp_interface>`

并非所有以太网设备驱动都支持所有这些功能。可以通过 ``net iface`` net-shell 命令查看支持情况，它会打印当前支持的以太网功能。

API 参考
********

.. doxygengroup:: ethernet

.. doxygengroup:: ethernet_mii
