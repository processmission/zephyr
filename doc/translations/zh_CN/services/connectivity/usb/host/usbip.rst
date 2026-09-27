.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _usbip:

USB/IP 协议支持
###############

概述
****

新的 USB 支持包含对 USB/IP 协议的初步支持。该功能仍在开发中，目前仅限于导出连接到主机控制器的一个设备。

USB/IP 使用 TCP/IP。其底层的两个连接协议栈（USB 和网络）都需要大量内存资源，在选择平台时必须加以考虑。

在 USB/IP 协议中，服务器导出 USB 设备，客户端导入这些设备。Zephyr RTOS 中的 USB/IP 支持实现服务器功能，导出一台运行 Zephyr RTOS 的设备上连接到主机控制器的设备。客户端（通常运行 Linux 内核）导入该设备。USB/IP 协议参见 `USB/IP protocol documentation`_。

要使用 USB/IP 支持，请确保客户端已加载所需的模块。

.. code-block:: console

   modprobe vhci_hcd
   modprobe usbip-core
   modprobe usbip-host

在客户端，还需要 **usbip** 用户工具。可以使用 Linux 发行版的包管理系统安装该工具，或从 Linux 内核源代码构建。

日常使用有几个基本命令。要列出已导出的 USB 设备，请运行以下命令：

.. code-block:: console

   $ usbip list -r 192.0.2.1
   Exportable USB devices
   ======================
    - 192.0.2.1
           1-1: NordicSemiconductor : unknown product (2fe3:0001)
              : /sys/bus/usb/devices/usb1/1-1
              : Miscellaneous Device / ? / Interface Association (ef/02/01)
              :  0 - Communications / Abstract (modem) / None (02/02/00)
              :  1 - CDC Data / Unused / unknown protocol (0a/00/00)

连接 busid 为 1-1 的已导出设备：

.. code-block:: console

   $ sudo usbip attach -r 192.0.2.1 -b 1-1

断开端口 0 上的已导出设备：

.. code-block:: console

   $ sudo usbip detach -p 0

在 native_sim 上使用 USB/IP
***************************

在启用 USB/IP 支持的情况下进行开发，首选方法是使用 :zephyr:board:`native_sim <native_sim>`。在真实硬件上的使用尚未经过充分测试。USB/IP 需要网络连接，有关如何在客户端设置接口，请参见 :ref:`networking_with_native_sim`。

使用 USB/IP 构建和运行示例需要大量配置，你可以使用 usbip-native-sim snippet 来配置主机和 USB/IP 支持。

.. zephyr-app-commands::
   :zephyr-app: samples/subsys/usb/cdc_acm
   :board: native_sim/native/64
   :gen-args: -DSNIPPET=usbip-native-sim -DEXTRA_DTC_OVERLAY_FILE=app.overlay
   :goals: build

.. _USB/IP protocol documentation: https://www.kernel.org/doc/html/latest/usb/usbip_protocol.html
