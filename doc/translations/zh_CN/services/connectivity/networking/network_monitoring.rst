.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _network_monitoring:

监控网络流量
############

.. contents::
    :local:
    :depth: 2

在调试连接问题或为 Zephyr 开发新协议支持时，能够监控网络流量非常有用。本页介绍如何设置网络流量捕获方式，以便用户可以在远程主机上使用 Wireshark 或类似工具查看 Zephyr 设备发送或接收的网络数据包。

有关需要启用的配置选项，另请参阅 Zephyr 源代码发行版中的 :zephyr:code-sample:`net-capture` 示例应用。

主机配置
********

这里的说明介绍如何设置 Linux 主机以捕获 Zephyr 网络的 RX 和 TX 流量。类似的说明在其他操作系统中也应适用。

在 Linux 主机上，找到 Zephyr 的 `net-tools`_ 项目；它既可以在 Zephyr 标准安装的 ``tools/net-tools`` 目录中找到，也可以从其独立的 git 仓库单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools

``net-tools`` 项目提供了一个配置文件，用于设置 IP-to-IP 隧道接口，以便将监控数据从 Zephyr 传输到主机。

在终端 #1 中，输入：

.. code-block:: console

   ./net-setup.sh -c zeth-tunnel.conf

此脚本将创建以下 IPIP 隧道接口：

.. csv-table::
   :header: "接口名称", "描述"
   :widths: auto

   "``zeth-ip6ip``", "IPv6 over IPv4 隧道"
   "``zeth-ipip``", "IPv4 over IPv4 隧道"
   "``zeth-ipip6``", "IPv4 over IPv6 隧道"
   "``zeth-ip6ip6``", "IPv6 over IPv6 隧道"

Zephyr 会将捕获的网络数据包发送到其中一个接口。实际使用哪个接口取决于捕获的配置方式。然后，您可以使用 Wireshark 监控相应的网络接口。

创建隧道接口后，您可以使用 ``net-tools`` 项目中的 ``net-capture.py`` 脚本打印或保存捕获的网络数据包。``net-capture.py`` 提供一个 UDP 监听器，可以将捕获的数据打印到屏幕，还可以选择将数据保存到 pcap 文件。

.. code-block:: console

   $ ./net-capture.py -i zeth-ip6ip -w capture.pcap
   [20210408Z14:33:08.959589] Ether / IP / ICMP 192.0.2.1 > 192.0.2.2 echo-request 0 / Raw
   [20210408Z14:33:08.976178] Ether / IP / ICMP 192.0.2.2 > 192.0.2.1 echo-reply 0 / Raw
   [20210408Z14:33:16.176303] Ether / IPv6 / ICMPv6 Echo Request (id: 0x9feb seq: 0x0)
   [20210408Z14:33:16.195326] Ether / IPv6 / ICMPv6 Echo Reply (id: 0x9feb seq: 0x0)
   [20210408Z14:33:21.194979] Ether / IPv6 / ICMPv6ND_NS / ICMPv6 Neighbor Discovery Option - Source Link-Layer Address 02:00:5e:00:53:3b
   [20210408Z14:33:21.217528] Ether / IPv6 / ICMPv6ND_NA / ICMPv6 Neighbor Discovery Option - Destination Link-Layer Address 00:00:5e:00:53:ff
   [20210408Z14:34:10.245408] Ether / IPv6 / UDP 2001:db8::2:47319 > 2001:db8::1:4242 / Raw
   [20210408Z14:34:10.266542] Ether / IPv6 / UDP 2001:db8::1:4242 > 2001:db8::2:47319 / Raw

``net-capture.py`` 具有以下命令行选项：

.. code-block:: console

   Listen captured network data from Zephyr and save it optionally to pcap file.
   ./net-capture.py \
        -i | --interface <network interface>
                Listen this interface for the data
        [-p | --port <UDP port>]
                UDP port (default is 4242) where the capture data is received
        [-q | --quiet]
                Do not print packet information
        [-t | --type <L2 type of the data>]
                Scapy L2 type name of the UDP payload, default is Ether
        [-w | --write <pcap file name>]
                Write the received data to file in PCAP format

除了使用 ``net-capture.py`` 脚本之外，您也可以使用 ``netcat`` 提供 UDP 监听器，这样主机就不会向 Zephyr 发送端口不可达消息：

.. code-block:: console

   nc -l -u 2001:db8:200::2 4242 > /dev/null

上面的 IP 地址是内部隧道端点，可以更改，具体取决于 Zephyr 的配置方式。Zephyr 会将包含捕获网络数据包的 UDP 数据包发送到配置的 IP 隧道，因此我们需要这样终止网络连接。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools

Zephyr 配置
***********

在本示例中，我们使用 ``native_sim`` 开发板。您也可以使用任何其他支持网络的开发板。

在终端 #3 中，输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/capture
   :host-os: unix
   :board: native_sim
   :gen-args: -DCONFIG_UART_NATIVE_PTY_AUTOATTACH_DEFAULT_CMD=\""gnome-terminal -- screen %s"\"
   :goals: build
   :compact:

要查看 Zephyr 控制台和 shell，请按如下方式启动 Zephyr 实例：

.. code-block:: console

   build/zephyr/zephyr.exe -attach_uart

也可以使用任何其他应用，只需确保启用了合适的配置选项（示例参见 ``samples/net/capture/prj.conf`` 文件）。

如果需要，网络捕获可以自动配置，但当前的 ``capture`` 示例应用不会这样做。用户必须使用 ``net-shell`` 来设置并启用监控。

需要先设置网络数据包监控。``net-shell`` 提供了 ``net capture setup`` 命令来完成此操作。命令语法为

.. code-block:: console

   net capture setup <remote-ip-addr> <local-ip-addr> <peer-ip-addr>
        <remote> is the (outer) endpoint IP address
        <local> is the (inner) local IP address
        <peer> is the (inner) peer IP address
        Local and Peer IP addresses can have UDP port number in them (optional)
        like 198.0.51.2:9000 or [2001:db8:100::2]:4242

在 Zephyr 控制台中，输入：

.. code-block:: console

   net capture setup 192.0.2.2 2001:db8:200::1 2001:db8:200::2

此命令将创建隧道接口。``192.0.2.2`` 是隧道终止的远程主机。该地址用于选择隧道接口所连接的本地网络接口。``2001:db8:200::1`` 指定隧道的本地 IP 地址，``2001:db8:200::2`` 是发送捕获网络数据包的对端 IP 地址。对于 IPv6 over IPv4 隧道，可以在设置命令中按如下方式指定 UDP 数据包的端口号

.. code-block:: console

   net capture setup 192.0.2.2 [2001:db8:200::1]:9999 [2001:db8:200::2]:9998

对于 IPv4 over IPv4 隧道，则按如下方式

.. code-block:: console

   net capture setup 192.0.2.2 198.51.100.1:9999 198.51.100.2:9998

如果省略端口号，则默认使用 UDP 端口 ``4242``。

可以按如下方式检查当前的监控配置：

.. code-block:: console

   uart:~$ net capture
   Network packet capture disabled
                   Capture  Tunnel
   Device          iface    iface   Local                  Peer
   NET_CAPTURE0    -        1      [2001:db8:200::1]:4242  [2001:db8:200::2]:4242

这将打印当前配置。由于我们尚未启用监控，因此未设置 ``Capture iface``。

然后，我们需要按如下方式启用网络数据包监控：

.. code-block:: console

   net capture enable 2

``2`` 指定要捕获其流量的网络接口。在本示例中，``2`` 是 ``native_sim`` 开发板的以太网接口。请注意，在本示例中，我们将网络流量发送到正在监控的同一接口。监控系统会避免捕获已捕获的网络流量，因为那样会导致递归。您可以使用 ``net iface`` 命令查看可用的网络接口。请注意，不能捕获来自隧道接口的流量，否则会导致递归循环。如果需要，可以将捕获的网络流量发送到其他网络接口。只需在 ``net capture setup`` 中正确设置 ``<remote-ip-addr>`` 选项，使 IP 隧道连接到所需的网络接口即可。可以再次按如下方式检查捕获状态：

.. code-block:: console

   uart:~$ net capture
   Network packet capture enabled
                   Capture  Tunnel
   Device          iface    iface   Local                  Peer
   NET_CAPTURE0    2        1      [2001:db8:200::1]:4242  [2001:db8:200::2]:4242

启用监控后，系统会将捕获的（接收或发送的）网络数据包发送到隧道接口以进行进一步处理。

可以按如下方式禁用监控：

.. code-block:: console

   net capture disable

这将关闭当前正在运行的监控。可以按如下方式清除监控设置：

.. code-block:: console

   net capture cleanup

配置监控不一定要使用 ``net-shell``。如果需要，应用可以调用 :ref:`网络捕获 API <net_capture_interface>` 函数。

Wireshark 配置
**************

可以使用 `Wireshark <https://www.wireshark.org/>`_ 工具以直观的方式监控捕获的网络流量。

您可以监控隧道接口或 ``zeth`` 接口。要查看 UDP 数据包内部实际捕获的数据，请参阅 `Wireshark decapsulate UDP`_ 文档以获取说明。

.. _Wireshark decapsulate UDP:
   https://osqa-ask.wireshark.org/questions/28138/decoding-ethernet-encapsulated-in-tcp-or-udp/
