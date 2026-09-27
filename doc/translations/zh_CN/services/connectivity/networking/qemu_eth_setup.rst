.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _networking_with_eth_qemu:

使用 QEMU 以太网进行网络连接
############################

.. contents::
    :local:
    :depth: 2

本页面介绍如何在（Linux）主机与运行在 QEMU 中的 Zephyr 应用之间搭建虚拟网络。

在本示例中，Zephyr 源代码发行版中的 :zephyr:code-sample:`sockets-echo-server` 示例应用在 QEMU 中运行。Zephyr 实例通过 tuntap 设备连接到 Linux 主机，该设备在 Linux 中建模为以太网网络接口。

前置条件
********

在 Linux 主机上，找到 Zephyr 的 `net-tools`_ 项目，它可以在 Zephyr 标准安装的 ``tools/net-tools`` 目录中找到，也可以从其独立的 git 仓库单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools


基本搭建
********

对于以下步骤，您需要两个终端窗口：

* 终端 #1 是以 net-tools 为当前目录的终端窗口（``cd net-tools``）
* 终端 #2 是您常用的 Zephyr 开发终端，已初始化 Zephyr 环境。

配置 Zephyr 实例时，必须选择正确的以太网驱动程序以实现 QEMU 连接：

* 对于 ``qemu_x86``，选择 ``Intel(R) PRO/1000 Gigabit Ethernet driver`` 以太网驱动程序。该驱动程序在 Zephyr 源代码树中称为 ``e1000``。
* 对于 ``qemu_cortex_m3``，选择 ``TI Stellaris MCU family ethernet driver`` 以太网驱动程序。该驱动程序在 Zephyr 源代码树中称为 ``stellaris``。
* 对于 ``mps2_an385``，选择 ``SMSC911x/9220 Ethernet driver`` 以太网驱动程序。该驱动程序在 Zephyr 源代码树中称为 ``smsc911x``。
* 对于 ``qemu_cortex_a53``，默认选择 ``Intel(R) PRO/1000 Gigabit Ethernet driver`` 以太网驱动程序。
* 此外，:zephyr:code-sample:`sockets-echo-server` 示例还包含 ``qemu_x86_64`` 上 VIRTIO 网络设备的覆盖文件。

步骤 1 - 创建以太网接口
=======================

在以网络连接方式启动 QEMU 之前，应在主机系统中创建网络接口。

在终端 #1 中输入：

.. code-block:: console

   ./net-setup.sh

您可以调整 ``net-setup.sh`` 脚本的行为。按如下方式运行 ``net-setup.sh`` 可查看各种选项：

.. code-block:: console

   ./net-setup.sh --help


步骤 2 - 在 QEMU 开发板中启动应用
=================================

构建并启动 :zephyr:code-sample:`sockets-echo-server` 示例应用。本示例使用 qemu_x86 开发板。

在终端 #2 中输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :gen-args: -DEXTRA_CONF_FILE=overlay-e1000.conf
   :goals: run
   :compact:

或者，如果您决定在 qemu_x86_64 上使用 VIRTIO 网络设备：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86_64
   :gen-args: -DDTC_OVERLAY_FILE=virtnet.overlay -DEXTRA_CONF_FILE=overlay-virtnet.conf
   :goals: run
   :compact:

按 :kbd:`CTRL+A` :kbd:`x` 退出 QEMU。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
