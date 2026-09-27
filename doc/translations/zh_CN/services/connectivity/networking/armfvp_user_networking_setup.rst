.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _networking_with_armfvp:

使用 Arm FVP 用户模式的网络连接
###############################

.. contents::
    :local:
    :depth: 2

本页面旨在为有兴趣在 Zephyr 中使用 Arm FVP 用户模式网络连接的用户提供一个起点。

简介
****

用户模式网络会模拟内置的 IP 路由器和 DHCP 服务器，并在客户机（guest）与主机之间路由 TCP 和 UDP 流量。它使用主机的用户模式 socket 层与其他主机通信。这样，无需管理员权限，也无需在运行该模型的主机上安装单独的驱动程序，即可使用大量 IP 网络服务。

默认情况下，Arm FVP 使用 ``172.20.51.0/24`` 网络，并在 ``172.20.51.254`` 上运行网关。该网关还充当 GOS 的 DHCP 服务器，使其可以自动分配到 IP 地址 ``172.20.51.1``。

有关 Arm FVP 用户模式网络连接的更多详细信息，请参见：https://developer.arm.com/documentation/100964/latest/Introduction-to-Fast-Models/User-mode-networking

在 Zephyr 中使用 Arm FVP 用户模式网络连接
*****************************************

Arm FVP 用户模式网络连接可在任何应用中启用，并且不需要在主机系统上进行任何配置。DHCPv4 客户端示例已启用此功能。请参见 :zephyr:code-sample:`dhcpv4-client` 示例应用。

限制
****

* 可以通过 IP 使用 TCP 和 UDP，但不能使用 ICMP（ping）。
* 用户模式网络不支持将主机上的 UDP 端口转发到模型。
* 只能在专用网络内使用 DHCP。
* 只能通过将主机上的 TCP 端口映射到模型来建立入站连接。所有使用 NAT 提供主机连接的实现都有此限制。
* 需要特权源端口的操作无法正常工作，例如使用默认配置的 NFS。
* 如果搭建失败，或参数语法不正确，则不会有错误报告。
