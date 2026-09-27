.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _networking_with_native_sim_eth_bridge:

使用 native_sim 开发板的以太网桥接
##################################

.. contents::
    :local:
    :depth: 2

本文档介绍如何在（Linux）主机与运行于 :zephyr:board:`native_sim <native_sim>` 开发板的 Zephyr 应用之间搭建桥接以太网网络。

当测试可使用 :kconfig:option:`CONFIG_NET_ETHERNET_BRIDGE` Kconfig 选项启用的以太网桥接功能时，此搭建方式很有用。在此搭建方式中，net-tools 配置会创建两个主机网络接口 ``zeth0`` 和 ``zeth1``，并将它们连接到 Zephyr 的 :zephyr:board:`native_sim <native_sim>` 应用。

首先创建主机接口。本示例中创建两个接口。

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools
   ./net-setup.sh -c zeth-multiface.conf -i zeth0 -t 2

``-c`` 指定要使用的配置文件，其中 ``zeth-multiface.conf`` 专门用于在主机中生成多个网络接口。``-i`` 选项指定第一个主机接口的名称。``-t`` 指定要创建的网络接口数量。

主机接口的示例输出：

.. code-block:: console

   zeth0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
          inet 192.0.2.2  netmask 255.255.255.255  broadcast 0.0.0.0
          inet6 2001:db8::2  prefixlen 128  scopeid 0x0<global>
          inet6 fe80::200:5eff:fe00:5300  prefixlen 64  scopeid 0x20<link>
          ether 00:00:5e:00:53:00  txqueuelen 1000  (Ethernet)
          RX packets 33  bytes 2408 (2.4 KB)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 49  bytes 4092 (4.0 KB)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

   zeth1: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
          inet 198.51.100.1  netmask 255.255.255.255  broadcast 0.0.0.0
          inet6 fe80::200:5eff:fe00:5301  prefixlen 64  scopeid 0x20<link>
          inet6 2001:db8:2::1  prefixlen 128  scopeid 0x0<global>
          ether 00:00:5e:00:53:01  txqueuelen 1000  (Ethernet)
          RX packets 21  bytes 1340 (1.3 KB)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 45  bytes 3916 (3.9 KB)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

然后创建一个示例并启用以太网桥接支持。本示例中我们创建 :zephyr:code-sample:`sockets-echo-server` 示例应用。

桥接需要第二个 TAP 接口。创建一个 devicetree 覆盖文件 :file:`second-iface.overlay`，用于添加第二个 ``zephyr,native-tap`` 接口：

.. code-block:: devicetree

   / {
       zeth1: zeth1 {
           compatible = "zephyr,native-tap";
           status = "okay";
           zephyr,random-mac-address;
           host-interface = "zeth1";
       };
   };

然后构建并运行应用，并指定该覆盖文件：

.. code-block:: console

   west build -p -b native_sim -d ../build/echo-server \
      samples/net/sockets/echo_server -- \
      -DCONFIG_UART_NATIVE_PTY_AUTOATTACH_DEFAULT_CMD="\"gnome-terminal -- screen %s\"" \
      -DCONFIG_NET_ETHERNET_BRIDGE=y \
      -DCONFIG_NET_ETHERNET_BRIDGE_SHELL=y \
      -DEXTRA_DTC_OVERLAY_FILE=second-iface.overlay \
      -DCONFIG_NET_IF_MAX_IPV6_COUNT=2 \
      -DCONFIG_NET_IF_MAX_IPV4_COUNT=2
   ../build/echo-server/zephyr/zephyr.exe -attach_uart

这将创建并运行 :zephyr:code-sample:`sockets-echo-server`，此时桥接已启用但尚未配置。要配置桥接，您可以使用 bridge shell，或直接从应用调用桥接 API。我们使用 bridge shell 按如下方式设置桥接：

.. code-block:: console

   net bridge addif 1 3 2
   net iface up 1

在上面的示例中，桥接接口索引为 1，接口 2 和 3 是以太网接口，它们链接到主机侧的接口 ``zeth0`` 和 ``zeth1``。

Zephyr 侧的网络接口如下所示：

.. code-block:: console

   net iface
   Hostname: zephyr

   Interface bridge0 (0x8090ebc) (Virtual) [1]
   ==================================
   Virtual name : <enabled>
   No attached network interface.
   Link addr : 3B:DB:31:0F:CC:B6
   MTU       : 1500
   Flags     : NO_AUTO_START
   Device    : BRIDGE_0 (0x8088354)
   Promiscuous mode : disabled
   IPv6 not enabled for this interface.
   IPv4 not enabled for this interface.

   Interface eth0 (0x8090fcc) (Ethernet) [2]
   ===================================
   Link addr : 02:00:5E:00:53:D2
   MTU       : 1500
   Flags     : AUTO_START,IPv4,IPv6
   Device    : zeth0 (0x808837c)
   Promiscuous mode : disabled
   Ethernet capabilities supported:
           TXTIME
           Promiscuous mode
   Ethernet PHY device: <none> (0)
   IPv6 unicast addresses (max 3):
           fe80::5eff:fe00:53d2 autoconf preferred infinite
           2001:db8::1 manual preferred infinite
   IPv6 multicast addresses (max 4):
           ff02::1
           ff02::1:ff00:53d2
           ff02::1:ff00:1
   IPv6 prefixes (max 2):
           <none>
   IPv6 hop limit           : 64
   IPv6 base reachable time : 30000
   IPv6 reachable time      : 18476
   IPv6 retransmit timer    : 0
   IPv4 unicast addresses (max 1):
           192.0.2.1/255.255.255.0 manual preferred infinite
   IPv4 multicast addresses (max 2):
           224.0.0.1
   IPv4 gateway : 0.0.0.0

   Interface eth1 (0x80910dc) (Ethernet) [3]
   ===================================
   Link addr : 02:00:5E:00:53:87
   MTU       : 1500
   Flags     : AUTO_START,IPv4,IPv6
   Device    : zeth1 (0x8088368)
   Promiscuous mode : disabled
   Ethernet capabilities supported:
           TXTIME
           Promiscuous mode
   Ethernet PHY device: <none> (0)
   IPv6 unicast addresses (max 3):
           fe80::5eff:fe00:5387 autoconf preferred infinite
   IPv6 multicast addresses (max 4):
           ff02::1
           ff02::1:ff00:5387
   IPv6 prefixes (max 2):
           <none>
   IPv6 hop limit           : 64
   IPv6 base reachable time : 30000
   IPv6 reachable time      : 25158
   IPv6 retransmit timer    : 0
   IPv4 unicast addresses (max 1):
           <none>
   IPv4 multicast addresses (max 2):
           224.0.0.1
   IPv4 gateway : 0.0.0.0

``net bridge`` 命令将显示桥接的当前状态：

.. code-block:: console

   net bridge
   Bridge Status   Config   Interfaces
   1      up       ok       2 3

``addif`` 命令将以太网接口 2 和 3 添加到桥接接口 1。执行 ``addif`` 命令后，桥接仍处于禁用状态，因为桥接接口默认未启用。``net iface up`` 命令将启用桥接。

如果在主机侧运行 wireshark 并监控 ``zeth0`` 和 ``zeth1``，您应该会在两个主机接口上看到相同的网络流量。

请注意，接口索引号不是固定的，在您的搭建环境中，桥接接口和以太网接口的索引值可能有所不同。

可以通过关闭桥接接口来禁用桥接，也可以使用 ``delif`` 命令从桥接中移除以太网接口。

.. code-block:: console

   net iface down 1
   net bridge delif 1 2 3
