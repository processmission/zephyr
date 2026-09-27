.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _networking_with_multiple_instances:

使用多个 Zephyr 实例进行网络连接
################################

.. contents::
    :local:
    :depth: 2

本页面介绍如何在多个 Zephyr 实例之间搭建虚拟网络。这些 Zephyr 实例可以运行在 QEMU 中，也可以是 native_sim 开发板进程。Linux 主机可用于在这些系统之间路由网络流量。

前置条件
********

在 Linux 主机上，找到 Zephyr 的 `net-tools`_ 项目，它可以在 Zephyr 标准安装的 ``tools/net-tools`` 目录中找到，也可以从其独立的 git 仓库单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools

基本搭建
********

对于以下步骤，您需要五个终端窗口：

* 终端 #1 和 #2 是以 net-tools 为当前目录的终端窗口（``cd net-tools``）
* 终端 #3，用于在 Linux 主机中设置桥接
* 终端 #4 和 #5 是您常用的 Zephyr 开发终端，已初始化 Zephyr 环境。

由于搭建 Zephyr 网络有多种方式，下面的示例使用带 ``e1000`` 以太网控制器的 ``qemu_x86`` 开发板和 native_sim 开发板，以简化搭建说明。如有需要，您可以使用其他 QEMU 开发板和驱动程序，详情见 :ref:`networking_with_eth_qemu`。您也可以使用两个或更多 native_sim 开发板 Zephyr 实例，并将它们连接在一起。


步骤 1 - 创建配置文件
=====================

在以网络连接方式启动 QEMU 之前，应在主机系统中为每个 Zephyr 实例创建网络接口。此处不能使用创建网络接口的默认设置，因为它用于将一个 Zephyr 实例连接到 Linux 主机。

对于 Zephyr 实例 #1，在 ``net-tools`` 项目或其他合适的目录中创建名为 ``zephyr1.conf`` 的文件。

.. code-block:: console

   # Configuration file for setting IP addresses for a network interface.
   INTERFACE="$1"
   HWADDR="00:00:5e:00:53:11"
   IPV6_ADDR_1="2001:db8:100::2"
   IPV6_ROUTE_1="2001:db8:100::/64"
   IPV4_ADDR_1="198.51.100.2/24"
   IPV4_ROUTE_1="198.51.100.0/24"
   ip link set dev $INTERFACE up
   ip link set dev $INTERFACE address $HWADDR
   ip -6 address add $IPV6_ADDR_1 dev $INTERFACE nodad
   ip -6 route add $IPV6_ROUTE_1 dev $INTERFACE
   ip address add $IPV4_ADDR_1 dev $INTERFACE
   ip route add $IPV4_ROUTE_1 dev $INTERFACE > /dev/null 2>&1

对于 Zephyr 实例 #2，在 ``net-tools`` 项目或其他合适的目录中创建名为 ``zephyr2.conf`` 的文件。

.. code-block:: console

   # Configuration file for setting IP addresses for a network interface.
   INTERFACE="$1"
   HWADDR="00:00:5e:00:53:22"
   IPV6_ADDR_1="2001:db8:200::2"
   IPV6_ROUTE_1="2001:db8:200::/64"
   IPV4_ADDR_1="203.0.113.2/24"
   IPV4_ROUTE_1="203.0.113.0/24"
   ip link set dev $INTERFACE up
   ip link set dev $INTERFACE address $HWADDR
   ip -6 address add $IPV6_ADDR_1 dev $INTERFACE nodad
   ip -6 route add $IPV6_ROUTE_1 dev $INTERFACE
   ip address add $IPV4_ADDR_1 dev $INTERFACE
   ip route add $IPV4_ROUTE_1 dev $INTERFACE > /dev/null 2>&1


步骤 2 - 创建以太网接口
=======================

应在 net-tools 目录中（``cd net-tools``）输入以下 ``net-setup.sh`` 命令。

在终端 #1 中输入：

.. code-block:: console

   ./net-setup.sh -c zephyr1.conf -i zeth.1

在终端 #2 中输入：

.. code-block:: console

   ./net-setup.sh -c zephyr2.conf -i zeth.2


步骤 3 - 设置网络桥接
=====================

在终端 #3 中输入：

.. code-block:: console

   sudo brctl addbr zeth-br
   sudo brctl addif zeth-br zeth.1
   sudo brctl addif zeth-br zeth.2
   sudo ifconfig zeth-br up


步骤 4 - 启动 Zephyr 实例
=========================

在本示例中，我们启动 :zephyr:code-sample:`sockets-echo-server` 和 :zephyr:code-sample:`sockets-echo-client` 示例应用。您也可以根据需要改用其他应用。

在终端 #4 中，如果使用 QEMU，请输入：

.. code-block:: console

   west build -d build/server -b qemu_x86 -t run \
      samples/net/sockets/echo_server -- \
      -DEXTRA_CONF_FILE=overlay-e1000.conf \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"203.0.113.1\" \
      -DCONFIG_ETH_QEMU_IFACE_NAME=\"zeth.1\" \
      -DCONFIG_NET_QEMU_DEVICE_EXTRA_ARGS=\"mac=00:00:5e:00:53:01\"

或者，如果要使用 native_sim 开发板，请输入：

.. code-block:: console

   west build -d build/server -b native_sim \
      samples/net/sockets/echo_server -- \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"203.0.113.1\"
   build/server/zephyr/zephyr.exe --eth-if=zeth.1 --mac-addr=00:00:5e:00:53:01


在终端 #5 中，如果使用 QEMU，请输入：

.. code-block:: console

   west build -d build/client -b qemu_x86 -t run \
      samples/net/sockets/echo_client -- \
      -DEXTRA_CONF_FILE=overlay-e1000.conf \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"198.51.100.1\" \
      -DCONFIG_ETH_QEMU_IFACE_NAME=\"zeth.2\" \
      -DCONFIG_NET_QEMU_DEVICE_EXTRA_ARGS=\"mac=00:00:5e:00:53:02\"

或者，如果要使用 native_sim 开发板，请输入：

.. code-block:: console

   west build -d build/client -b native_sim \
      samples/net/sockets/echo_client -- \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"198.51.100.1\"
   build/client/zephyr/zephyr.exe --eth-if=zeth.2 --mac-addr=00:00:5e:00:53:02


此外，如果主机上启用了防火墙，您需要允许 ``zeth.1``、``zeth.2`` 和 ``zeth-br`` 接口之间的流量。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
