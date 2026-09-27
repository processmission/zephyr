.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _networking_with_native_sim:

使用 native_sim 开发板进行网络连接
##################################

.. contents::
    :local:
    :depth: 2

使用虚拟/TAP 以太网驱动程序
***************************

本段介绍如何在（Linux）主机与运行于 :zephyr:board:`native_sim <native_sim>` 开发板的 Zephyr 应用之间搭建虚拟网络。

在本示例中，Zephyr 源代码发行版中的 :zephyr:code-sample:`sockets-echo-server` 示例应用在 native_sim 开发板上运行。Zephyr native_sim 开发板实例通过 tuntap 设备连接到 Linux 主机，该设备在 Linux 中建模为以太网网络接口。

前置条件
========

在 Linux 主机上，找到 Zephyr 的 `net-tools`_ 项目，它可以在 Zephyr 标准安装的 ``tools/net-tools`` 目录中找到，也可以从其独立的 git 仓库单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools


基本搭建
========

对于以下步骤，您需要三个终端窗口：

* 终端 #1 是以 net-tools 为当前目录的终端窗口（``cd net-tools``）
* 终端 #2 是您常用的 Zephyr 开发终端，已初始化 Zephyr 环境。
* 终端 #3 是连接到正在运行的 Zephyr native_sim 实例的控制台（可选）。

步骤 1 - 创建以太网接口
-----------------------

在以网络仿真方式启动 native_sim 之前，应创建一个网络接口。

在终端 #1 中输入：

.. code-block:: console

   ./net-setup.sh

您可以调整 net-setup.sh 脚本的行为。按如下方式运行 ``net-setup.sh`` 可查看各种选项：

.. code-block:: console

   ./net-setup.sh --help


步骤 2 - 在 native_sim 开发板中启动应用
---------------------------------------

构建并启动 ``echo_server`` 示例应用。

在终端 #2 中输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: native_sim
   :goals: run
   :compact:


步骤 3 - 连接到控制台（可选）
-----------------------------

启动 Zephyr 实例时，控制台窗口应会自动打开；如果它没有出现，您可以手动连接到控制台。native_sim 开发板在启动时会打印如下字符串：

.. code-block:: console

   UART connected to pseudotty: /dev/pts/5

您可以按如下方式手动连接到控制台：

.. code-block:: console

   screen /dev/pts/5

使用卸载式 socket
*****************

与 `使用虚拟/TAP 以太网驱动程序`_ 相比，其主要优势是无需在主机上设置虚拟网络接口。这意味着不需要提升（root）权限。

步骤 1 - 在 native_sim 开发板中启动应用
=======================================

构建并启动 ``echo_server`` 示例应用：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: native_sim
   :gen-args: -DEXTRA_CONF_FILE=overlay-nsos.conf
   :goals: run
   :compact:

步骤 2 - 从 net-tools 运行 echo-client
======================================

在 Linux 主机上，找到 Zephyr 的 `net-tools`_ 项目，它可以在 Zephyr 标准安装的 ``tools/net-tools`` 目录中找到，也可以从其独立的 git 仓库单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools

.. note::

   使用卸载式 socket 网络驱动程序的 Native Simulator 会使用与任何其他使用 BSD sockets API 的（Linux）应用相同的网络接口/命名空间。这意味着 :zephyr:code-sample:`sockets-echo-server` 和 ``echo-client`` 应用将通过 localhost/回环接口（地址 ``127.0.0.1``）通信。

要运行 UDP 测试，请输入：

.. code-block:: console

   ./echo-client 127.0.0.1

要进行 TCP 测试，请输入：

.. code-block:: console

   ./echo-client -t 127.0.0.1

从命令行设置接口名称和 IPv4 参数
********************************

默认情况下，native_sim 使用的以太网接口名称由 ``zephyr,native-tap`` Devicetree 节点的 ``host-interface`` 属性决定，也可以使用 ``--eth-if=<interface_name>`` 从命令行设置。

IPv4 地址、网关和子网掩码也是如此。可以使用 ``--ipv4-addr=<ip_address>``、``--ipv4-gw=<gateway>`` 和 ``--ipv4-nm=<netmask>`` 从命令行设置。

这些选项适用于第一个接口。当定义多个 ``zephyr,native-tap`` 接口时，每个附加接口都有各自以 Devicetree 节点名称为前缀的每接口选项，例如 ``--<node>_eth-if`` 和 ``--<node>_ipv4-addr``。

请注意，配置项 :kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_ADDR` 和命令行参数会并行生效。这意味着如果两者都设置，接口最终可能会有两个 IP 地址。在大多数情况下，同时只使用其中一个是合理的。

如果应用需要以多个实例运行，而为每个实例重新编译又很麻烦，那么这会很有用。

.. code-block:: console

   ./zephyr.exe --eth-if=zeth2 --ipv4-addr=192.0.2.2 --ipv4-gw=192.0.0.1
   --ipv4-nm=255.255.0.0

.. note::

   这些命令行选项也可以在构建时通过 :kconfig:option:`CONFIG_NATIVE_EXTRA_CMDLINE_ARGS` 配置选项提供。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
