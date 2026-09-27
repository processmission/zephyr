.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _dhcpv4_interface:

DHCPv4
######

.. contents::
    :local:
    :depth: 2

概述
****

动态主机配置协议（DHCP，Dynamic Host Configuration Protocol）是用于 IPv4 网络的网络管理协议。DHCPv4 服务器为网络中的每台设备动态分配 IPv4 地址和其他网络配置参数，使它们能够与其他 IP 网络通信。DHCP 工作原理的详细概述见 `DHCP Wikipedia article <https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol>`_。

请注意，Zephyr 同时支持 DHCPv4 客户端和服务器功能。

用法示例
********

详见 :zephyr:code-sample:`dhcpv4-client` 示例应用。

API 参考
********

.. doxygengroup:: dhcpv4
