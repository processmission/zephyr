.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _networking_with_qemu:

使用 QEMU 进行网络连接
######################

.. contents::
    :local:
    :depth: 2

本页面介绍如何在（Linux）主机与运行在 QEMU 虚拟机中的 Zephyr 应用之间搭建虚拟网络（这些应用是为 qemu_x86、qemu_cortex_m3 等 Zephyr 目标构建的）。某些虚拟 ARM 开发板（如 qemu_cortex_a53）仅支持单个 UART，在这种情况下，建议使用 QEMU 以太网，详情见 :ref:`networking_with_eth_qemu`。

在本示例中，Zephyr 源代码发行版中的 :zephyr:code-sample:`sockets-echo-server` 示例应用在 QEMU 中运行。QEMU 实例通过串行端口连接到 Linux 主机，并使用 SLIP 在 Zephyr 应用与 Linux 之间传输数据（通过一条虚拟连接链）。

前置条件
********

在 Linux 主机上，找到 Zephyr 的 `net-tools`_ 项目，它可以在 Zephyr 标准安装的 ``tools/net-tools`` 目录中找到，也可以从其独立的 git 仓库单独安装：

.. code-block:: console

   sudo apt install -y socat libpcap-dev
   git clone https://github.com/zephyrproject-rtos/net-tools
   cd net-tools
   make

.. note::

   如果出现关于 AX_CHECK_COMPILE_FLAG 的错误，请在 Debian/Ubuntu 上安装 ``autoconf-archive`` 包。

基本搭建
********

对于以下步骤，您至少需要 4 个终端窗口：

* 终端 #1 是您常用的 Zephyr 开发终端，已初始化 Zephyr 环境。
* 终端 #2、#3 和 #4 是以 net-tools 为当前目录的终端窗口（``cd net-tools``）

步骤 1 - 创建辅助 socket
========================

在启动带网络仿真的 QEMU 之前，应创建用于仿真的 Unix socket。

在终端 #2 中输入：

.. code-block:: console

   ./loop-socat.sh

步骤 2 - 启动 TAP 设备路由守护进程
==================================

在终端 #3 中输入：


.. code-block:: console

   sudo ./loop-slip-tap.sh

对于需要 DNS 的应用，此时可能需要按照 :ref:`networking_internet` 中所述重新启动主机的 DNS 服务器。

步骤 3 - 在 QEMU 中启动应用
===========================

构建并启动 ``echo_server`` 示例应用。

在终端 #1 中输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :goals: run
   :compact:

如果看到 QEMU 报出关于 unix:/tmp/slip.sock 的错误，说明您漏掉了上面的步骤 1。

步骤 4 - 在主机上运行应用
=========================

现在，您可以在终端 #4 中运行各种工具，与 QEMU 中运行的应用通信。

可以先从 ping 开始：

.. code-block:: console

   ping 192.0.2.1
   ping6 2001:db8::1

您可以使用 netcat（“nc”）工具，通过 UDP 连接：

.. code-block:: console

   echo foobar | nc -6 -u 2001:db8::1 4242
   foobar

.. code-block:: console

   echo foobar | nc -u 192.0.2.1 4242
   foobar

如果 echo_server 编译时启用了 TCP 支持（现在 echo_server 示例默认启用该支持，CONFIG_NET_TCP=y）：

.. code-block:: console

   echo foobar | nc -6 -q2 2001:db8::1 4242
   foobar

.. note::

   使用 Ctrl+C 退出。

您也可以使用 telnet 命令实现上述操作。

步骤 5 - 停止辅助守护进程
=========================

完成使用 QEMU 的网络测试后，应停止初始步骤中启动的所有守护进程或辅助程序，以避免可能出现的网络或路由问题，例如本地网络接口中的地址冲突。例如，当您从使用 QEMU 测试网络切换到使用真实硬件，或要让主机笔记本电脑恢复正常使用 Wi-Fi 时，请停止这些进程。

要停止这些守护进程，请在相应的终端窗口中按 Ctrl+C（需要同时停止 ``loop-slip-tap.sh`` 和 ``loop-socat.sh``）。

按 :kbd:`CTRL+A` :kbd:`x` 退出 QEMU。

.. _networking_internet:

在主机上设置 Zephyr 和 NAT/地址伪装以访问互联网
***********************************************

要让 Zephyr 应用访问互联网，可能需要在主机上进行一些额外设置。假设开发板连接到开发主机，则此设置对在 QEMU 中运行的应用和在真实硬件上运行的应用是通用的。如果开发板连接到专用路由器，则不需要此设置。

要让使用 IPv4 的 Zephyr 应用访问互联网，应通过 DHCP 设置网关，或手动配置网关。对于使用“Settings”功能的应用（启用配置选项 :kconfig:option:`CONFIG_NET_CONFIG_SETTINGS`），请将 :kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_GW` 选项设置为网关的 IP 地址。对于不使用“Settings”功能的应用，请在运行时调用 :c:func:`net_if_ipv4_set_gw` 来设置网关。例如：``CONFIG_NET_CONFIG_MY_IPV4_GW="192.0.2.2"``

要让在 QEMU 中运行的自定义应用访问互联网，应为 QEMU 的源地址设置 NAT（地址伪装）。假设使用 ``192.0.2.1``，且 Zephyr 网络接口为 ``zeth``，则应以 root 身份运行以下命令：

.. code-block:: console

   iptables -t nat -A POSTROUTING -j MASQUERADE -s 192.0.2.1/24
   iptables -I FORWARD 1 -i zeth -j ACCEPT
   iptables -I FORWARD 1 -o zeth -m state --state RELATED,ESTABLISHED -j ACCEPT

此外，应在主机上启用 IPv4 转发，并且您可能需要检查其他防火墙（iptables）规则不会干扰地址伪装。要启用 IPv4 转发，应以 root 身份运行以下命令：

.. code-block:: console

   sysctl -w net.ipv4.ip_forward=1

某些应用可能还需要 DNS 服务器。Zephyr 提供的许多示例默认假设主机（IP ``192.0.2.2``）上可用 DNS 服务器，而在现代 Linux 发行版中，主机通常至少运行一个 DNS 代理。使用 QEMU 运行时，可能需要重新启动主机的 DNS，使其能够在新创建的 TAP 接口上处理请求。例如，在基于 Debian 的系统上：

.. code-block:: console

   service dnsmasq restart

除了依赖主机的 DNS 服务器外，也可以使用网络中的 DNS 服务器。例如，``8.8.8.8`` 是一个公开可用的 DNS 服务器。您可以使用 :kconfig:option:`CONFIG_DNS_SERVER1` 选项进行配置。


两个 QEMU 虚拟机之间的网络连接
******************************

与上述虚拟机到主机的搭建方式不同，虚拟机到虚拟机的搭建是自动的。对于支持此模式的示例应用（如 echo_server 和 echo_client 示例），您需要两个配置好 Zephyr 开发环境的终端窗口。

终端 #1：
=========

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :goals: build
   :build-args: server
   :compact:

这将启动 QEMU，并等待来自客户端 QEMU 的连接。

终端 #2：
=========

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_client
   :host-os: unix
   :board: qemu_x86
   :goals: build
   :build-args: client
   :compact:

这将启动第二个 QEMU 实例，您应该能在两者中看到发送和接收数据的日志。

运行同一示例的多个 QEMU 虚拟机
******************************

如果您需要运行多个同一 Zephyr 示例应用的实例，且这些实例之间不需要相互通信，请使用 ``QEMU_INSTANCE`` 参数。

对于所需的任意多个实例，请手动启动 ``socat`` 和 ``tunslip6`` （而不是使用 ``loop-xxx.sh`` 脚本）。可参考以下内容，并替换 MAIN 或 OTHER。

Terminal #1:
============

.. code-block:: console

   socat PTY,link=/tmp/slip.devMAIN UNIX-LISTEN:/tmp/slip.sockMAIN &
   sudo $ZEPHYR_BASE/../tools/net-tools/tunslip6 -t tapMAIN -T -s /tmp/slip.devMAIN 2001:db8::1/64 &
   # Now run Zephyr
   make -Cbuild run QEMU_INSTANCE=MAIN

Terminal #2:
============

.. code-block:: console

   socat PTY,link=/tmp/slip.devOTHER UNIX-LISTEN:/tmp/slip.sockOTHER &
   sudo $ZEPHYR_BASE/../tools/net-tools/tunslip6 -t tapOTHER -T -s /tmp/slip.devOTHER 2001:db8::1/64 &
   make -Cbuild run QEMU_INSTANCE=OTHER

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
