.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _autopts-linux:

Linux 上的 AutoPTS
##################

本教程介绍如何在 Linux 上设置 AutoPTS 客户端，并在 Windows 10 虚拟机上运行 AutoPTS 服务器。已在 Ubuntu 20.4 和 Linux Mint 20.4 上测试。

您必须已搭建好 Zephyr 开发环境。详情请参见 :ref:`getting_started`。

支持用于测试 Zephyr 蓝牙主机的方法：

- 在 QEMU 上测试 Zephyr 主机协议栈

- 在 :zephyr:board:`native_sim <native_sim>` 上测试 Zephyr 主机协议栈

- 在真实硬件（例如 nRF52）上测试 Zephyr 组合（控制器 + 主机）构建

若要使用 QEMU 或 :zephyr:board:`native_sim <native_sim>` 运行，请参见 :ref:`bluetooth_qemu_native`。

.. contents::
    :local:
    :depth: 2

设置 Linux
**********

请按照 :ref:`getting_started` 中的说明设置用于构建和烧录应用的 Linux。

设置 Windows 10/11 虚拟机
*************************

选择并安装虚拟机监控程序，例如 VMWare Workstation（推荐）或 VirtualBox。如果主机的 CPU 少于 6 个，使用 VirtualBox 可能会出现问题。

创建 Windows 虚拟机实例。确保其至少具有 2 个核心并已安装来宾扩展。

设置已在 VirtualBox 7.2.4 和 VMWare Workstation 16.1.1 Pro 上测试。

更新 Windows
============

在以下位置更新 Windows：

Start -> Settings -> Update & Security -> Windows Update

设置 NAT
========

可以使用 NAT 和端口转发来在 Linux 主机与 Windows 来宾之间建立通信。这是 VirtualBox 最简单的设置方式，不需要配置任何静态 IP，也不会被 Windows 防火墙阻止。

VirtualBox
----------

打开虚拟机网络设置。在适配器 1 上，默认会创建 NAT。打开“端口转发”菜单，添加所需的端口。


.. image:: virtualbox_nat_1.png
   :width: 500
   :align: center

例如，进行以下设置后，您可以使用 ``localhost:65000`` 和 ``localhost:65002`` （或 ``127.0.0.0:65000`` 和 ``127.0.0.0:65002`` ）连接到 Windows 中运行在端口 65000 和 65002 上的 AutoPTS 服务器。

.. image:: virtualbox_nat_2.png
   :width: 500
   :align: center

设置静态 IP
===========

如果您不能或不想使用 NAT，也可以配置静态 IP。

VMWare Works
------------

在 Linux 上，打开 Virtual Network Editor 应用并创建网络：

.. image:: vmware_static_ip_1.png
   :height: 400
   :width: 500
   :align: center

打开虚拟机网络设置。添加自定义适配器：

.. image:: vmware_static_ip_2.png
   :height: 400
   :width: 500
   :align: center

如果在终端中输入 'ifconfig'，应能发现主机 IP：

.. image:: vmware_static_ip_3.png
   :height: 150
   :width: 550
   :align: center

VirtualBox
----------

在 Linux、macOS 和 Solaris 上，Oracle VM VirtualBox 仅允许将 ``192.168.56.0/21`` 范围内的 IP 地址分配给仅主机适配器，因此如果在 VirtualBox 中使用静态地址，这是唯一可用的地址范围。

转到：

File -> Tools -> Network Manager

并创建网络：

.. image:: virtualbox_static_ip_1.png
   :width: 500
   :align: center

打开虚拟机网络设置。在适配器 1 上，默认会创建 NAT。添加适配器 2：

.. image:: virtualbox_static_ip_2.png
   :width: 500
   :align: center

Windows
-------
在 Windows 虚拟机上设置静态 IP。转到

Settings -> Network & Internet -> Ethernet -> Unidentified network -> Edit

并进行设置：

.. image:: windows_static_ip.png
   :height: 400
   :width: 400
   :align: center


安装 Python 3
=============

在 Windows 上下载并安装最新的 `Python 3 <https://www.python.org/downloads/>`_。让安装程序将 Python 安装目录添加到 PATH，并禁用路径长度限制。

.. image:: install_python1.png
   :height: 300
   :width: 450
   :align: center

.. image:: install_python2.png
   :height: 300
   :width: 450
   :align: center

安装 Git
========

下载并安装 `Git <https://git-scm.com/downloads>`_。在安装过程中启用选项：Enable experimental support for pseudo consoles。我们将使用 Git Bash 作为 Windows 终端。

.. image:: install_git.png
   :height: 350
   :width: 400
   :align: center

安装 PTS
========

在 Windows 虚拟机上，从 https://pts.bluetooth.com/download 安装最新的 PTS。请记住从安装目录 “C:/Program Files (x86)/Bluetooth SIG/Bluetooth PTS/PTS Driver/win64/CSRBlueCoreUSB.inf” 安装驱动。

.. image:: install_pts_drivers.png
   :height: 250
   :width: 850
   :align: center

.. note::

    从 PTS 8.0.1 开始，不再包含 Bluetooth Protocol Viewer。因此，要捕获 Bluetooth 事件，您需要单独下载它。

连接 PTS 加密狗
===============

使用 VirtualBox 应该没有问题。只需在 Devices -> USB 中找到加密狗并连接。

使用 VMWare 时，如果在 VM -> Removable Devices 中找不到加密狗，可能需要使用一些技巧。在 Linux 终端中输入：

.. code-block::

    usb-devices

并在输出中找到您的 PTS Bluetooth USB 加密狗

.. image:: usb-devices_output.png
   :height: 100
   :width: 500
   :align: center

记下 Vendor 和 ProdID 编号。关闭 VMWare Workstation，在文本编辑器中打开虚拟机的 .vmx 文件（路径类似于 /home/codecoup/vmware/Windows 10/Windows 10.vmx）。在文件任意位置写入以下行：

.. code-block::

    usb.autoConnect.device0 = "0x0a12:0x0001"

只需将 0x0a12 替换为您之前找到的 Vendor 编号，将 0x0001 替换为 ProdID 编号。

连接设备（仅在实际硬件测试模式下需要）
**************************************

.. image:: devices_1.png
   :height: 400
   :width: 600
   :align: center

.. image:: devices_2.png
   :height: 700
   :width: 500
   :align: center

设置 auto-pts 项目
******************

Linux 上的 AutoPTS 客户端
=========================

克隆 auto-pts 项目：

.. code-block::

    git clone https://github.com/auto-pts/auto-pts.git


安装 socat，用于从 UART 的 tty 文件传输 BTP 数据流：

.. code-block::

    sudo apt-get install python-setuptools socat

安装所需的 Python 模块：

.. code-block::

   cd auto-pts
   pip3 install --user -r autoptsclient_requirements.txt

Windows 虚拟机上的 AutoPTS 服务器
=================================
在 Git Bash 中，克隆 auto-pts 项目仓库：

.. code-block::

    git clone https://github.com/auto-pts/auto-pts.git

安装所需的 Python 模块：

.. code-block::

   cd auto-pts
   pip3 install --user wheel
   pip3 install --user -r autoptsserver_requirements.txt

重新启动虚拟机。

运行 AutoPTS
************

请按照 https://github.com/zephyrproject-rtos/zephyr/tree/main/tests/bluetooth/tester 中的信息了解如何构建、烧录和运行 Bluetooth Tester 应用。

服务器和客户端默认将在 localhost 地址上运行。在 Windows 虚拟机中运行服务器：

.. code-block::

    python ./autoptsserver.py

.. image:: autoptsserver_run_2.png
   :height: 120
   :width: 700
   :align: center

有关如何运行 auto-pts 的更多信息，另请参见 https://github.com/auto-pts/auto-pts。

在硬件上测试 Zephyr 主机协议栈
==============================

.. code-block::

    python ./autoptsclient-zephyr.py zephyr-master -t /dev/ttyACM0 -b BOARD -i SERVER_IP -l LOCAL_IP

其中 ``/dev/ttyACM0`` 是开发板的 tty，``BOARD`` 是要使用的开发板（例如 ``nrf53_audio``），``SERVER_IP`` 是 AutoPTS 服务器的 IP，``LOCAL_IP`` 是 Linux 机器的本地 IP。

Testing Zephyr Host Stack on QEMU
=================================

需要挂载 Bluetooth 控制器。若要使用 HCI UART 运行，请访问 :zephyr:code-sample:`bluetooth_hci_uart`。

.. code-block::

    python ./autoptsclient-zephyr.py zephyr-master BUILD_DIR/zephyr/zephyr.elf -i SERVER_IP -l LOCAL_IP

其中 ``BUILD_DIR`` 是构建目录，``SERVER_IP`` 是 AutoPTS 服务器的 IP，``LOCAL_IP`` 是 Linux 机器的本地 IP。

Testing Zephyr Host Stack on :zephyr:board:`native_sim <native_sim>`
====================================================================

当测试器应用为 :zephyr:board:`native_sim <native_sim>` 构建时，会生成一个 ``zephyr.exe`` 文件，它可以作为原生 Linux 应用运行。根据您的系统，您可能需要执行以下步骤才能成功运行 ``zephyr.exe``。

设置能力
--------

由于应用需要访问 HCI 套接字，您可能需要执行以下操作

.. code-block::

    setcap cap_net_raw,cap_net_admin,cap_sys_admin+ep zephyr.exe

如果您使用例如 ``sudo`` 运行 ``zephyr.exe`` 或 ``./autoptsclient-zephyr.py``，则不需要这样做。

关闭 HCI 控制器
---------------

在运行 ``zephyr.exe`` 之前，您可能还需要“down”或“power off” HCI 控制器。可以使用 ``hciconfig`` 按如下方式完成：

.. code-block::

    hciconfig hciX down

其中 ``hciX`` 是类似 ``hci0`` 的值。您可以运行 ``hciconfig`` 获取 HCI 设备列表。

由于 ``hciconfig`` 在某些系统上已弃用，您可能需要使用

.. code-block::

    btmgmt -i hciX power off

与 ``hciconfig`` 类似，``btmgmt info`` 可用于列出当前控制器及其状态。

在关闭控制器电源时，``hciconfig`` 和 ``btmgmt`` 都可能需要 ``sudo``。

运行客户端
----------

该应用可以按如下方式运行

.. code-block::

    python ./autoptsclient-zephyr.py zephyr-master --hci HCI BUILD_DIR/zephyr/zephyr.exe -i SERVER_IP -l LOCAL_IP

其中 ``HCI`` 是 HCI 索引，例如 ``0`` 或 ``1``，``BUILD_DIR`` 是构建目录，``SERVER_IP`` 是 AutoPTS 服务器的 IP，``LOCAL_IP`` 是 Linux 机器的本地 IP。

故障排查
********

运行一个测试后，我需要重新启动 Windows 虚拟机才能运行另一个测试，因为 PTS 日志中 APICOM 给出了 fail 判定
========================================================================================================

这意味着您的虚拟机没有足够的处理器核心或内存。请尝试在设置中增加。请注意，如果使用 VirtualBox 作为虚拟机监控程序，具有 4 个 CPU 的主机可能不够。在这种情况下，请选择 VMWare Workstation。

我无法启动 autoptsserver-zephyr.py。总是收到 Python 错误
========================================================

.. image:: autoptsserver_typical_error.png
   :height: 300
   :width: 650
   :align: center

以下一个或多个步骤应该有帮助：

- 关闭所有 PTS Windows。

- 重新插拔 PTS Bluetooth 加密狗。

- 删除临时工作区。您可以在 auto-pts-code/workspaces/zephyr/zephyr-master/ 中找到它，名为 temp_zephyr-master。请注意，不要删除原来的 zephyr-master.pqw6。

- 重新启动 Windows 虚拟机。

PTS 自动化窗口不断打开和关闭
============================

这表明它未能捕获 PTS 加密狗。如果 AutoPTS 服务器能够找到并使用 PTS 加密狗，那么窗口标题将显示该加密狗的 Bluetooth 地址。如果没有出现这种情况，请确保加密狗已插入、已更新并被 PTS 识别。

.. image:: pts_automation_window.png
   :width: 500
   :align: center

如果在此之后仍无法运行测试，请确保已安装 Bluetooth Protocol Viewer。
