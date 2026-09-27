.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _networking_with_host:

与主机系统联网
##############

.. toctree::
   :maxdepth: 1
   :hidden:

   native_sim_setup.rst
   qemu_eth_setup.rst
   qemu_setup.rst
   usbnet_setup.rst
   qemu_user_setup.rst
   networking_with_multiple_instances.rst
   eth_bridge_native_sim_setup.rst
   qemu_802154_setup.rst
   armfvp_user_networking_setup.rst

在开发网络软件时，通常需要与主机系统（如 Linux 台式计算机）连接并交换数据。根据开发所用的开发板，可以采用以下几种方式：

* 使用 SLIP（Serial Line Internet Protocol，串行线路网际协议）的 QEMU。

  * 在此方式中，IP 数据包通过串行端口在 Zephyr 与主机系统之间交换。这是传统的数据传输方式，速度也相当慢，因此仅在必要时使用。详情见 :ref:`networking_with_qemu`。

* 使用内置以太网驱动程序的 QEMU。

  * 在此方式中，IP 数据包通过 QEMU 的内置以太网驱动程序在 Zephyr 与主机系统之间交换。并非所有 QEMU 开发板都支持内置以太网，因此在某些情况下，您可能需要使用 SLIP 方式实现主机连接。详情见 :ref:`networking_with_eth_qemu`。

* 使用 SLIRP（Qemu User Networking）的 QEMU。

  * QEMU 用户模式网络使用“slirp”实现，它在 QEMU 内部提供完整的 TCP/IP 协议栈，并利用该协议栈实现虚拟 NAT 网络。由于此支持内置于 QEMU，因此可与任何模型一起使用，并且与 TAP 不同，不需要主机上的管理员权限。但是，它有一些限制（包括性能方面），这使其在实际用途中价值较低。详情见 :ref:`networking_with_user_qemu`。

* Arm FVP（用户模式网络）。

  * 用户模式网络会模拟内置的 IP 路由器和 DHCP 服务器，并在客户机与主机之间路由 TCP 和 UDP 流量。它使用主机的用户模式 socket 层与其他主机通信。这样，无需管理员权限，也无需在运行该模型的主机上安装单独的驱动程序，即可使用大量 IP 网络服务。详情见 :ref:`networking_with_armfvp`。

* native_sim 开发板。

  * Zephyr 实例可以作为用户空间进程在主机系统中运行。这是调试 Zephyr 系统最便捷的方式，因为可以将主机调试器直接附加到正在运行的 Zephyr 实例。这要求 Zephyr 中有用于与主机系统对接的适配驱动程序。为此可以使用两种网络驱动程序：TAP 虚拟以太网驱动程序和卸载式 socket 驱动程序。详情见 :ref:`networking_with_native_sim`。

* USB 设备网络。

  * 在此方式中，Zephyr 实例在真实开发板上运行，通过 USB 与主机系统建立连接。详情见 :ref:`usb_device_networking_setup`。

* 将多个 Zephyr 实例连接在一起。

  * 如果您有多个 Zephyr 实例（QEMU 或 native_sim 实例），并希望它们之间建立连接，详情见 :ref:`networking_with_multiple_instances`。

* 在两个 QEMU 之间模拟 IEEE 802.15.4 网络。

  * 在此方式中，运行两个 Zephyr 实例，它们之间通过 UART 运行 IEEE 802.15.4 链路层。详情见 :ref:`networking_with_ieee802154_qemu`。

* 使用 native_sim 模拟以太网桥接网络。

  * 在此方式中，运行一个 Zephyr 实例，并通过 :kconfig:option:`CONFIG_NET_ETHERNET_BRIDGE` Kconfig 选项启用了以太网桥接。存在两个主机网络接口 ``zeth0`` 和 ``zeth1``，网络数据包在这两个接口之间桥接。详情见 :ref:`networking_with_native_sim_eth_bridge`。
