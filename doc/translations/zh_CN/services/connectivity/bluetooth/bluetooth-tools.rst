.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth-tools:

工具
####

本页列出并介绍可用于协助蓝牙协议栈或应用开发的工具，以帮助简化并加速开发过程。

.. contents::
    :local:
    :depth: 2

.. _bluetooth-mobile-apps:

移动应用
********

利用现有移动应用与运行 Zephyr 的硬件交互通常很有用，这样无需编写任何额外代码或增加额外硬件即可测试功能。

推荐用于与 Zephyr 交互的移动应用如下：

* Android：

  * `nRF Connect for Android`_
  * `nRF Mesh for Android`_
  * `LightBlue for Android`_

* iOS：

  * `nRF Connect for iOS`_
  * `nRF Mesh for iOS`_
  * `LightBlue for iOS`_

.. _bluetooth_bluez:

将 BlueZ 与 Zephyr 配合使用
***************************

Linux 蓝牙协议栈 BlueZ 附带一组非常有用的工具，可用于调试 Zephyr 的蓝牙主机和控制器，并与之交互。要使用这些工具，需要确保运行较新版本的 Linux 内核和 BlueZ：

* Linux 内核 4.10+
* BlueZ 4.45+

此外，您的 Linux 发行版可能默认未附带某些 BlueZ 工具。如果需要从源码构建 BlueZ 以更新到较新版本或获取其全部工具，可以按照以下步骤操作：

.. code-block:: console

   git clone git://git.kernel.org/pub/scm/bluetooth/bluez.git
   cd bluez
   ./bootstrap-configure --disable-android --disable-midi
   make

随后可以在 :file:`tools/` 文件夹中找到 :file:`btattach`、:file:`btmgt` 和 :file:`btproxy`，在 :file:`monitor/` 文件夹中找到 :file:`btmon`。

您需要启用 BlueZ 的实验性功能，才能访问其最新的蓝牙功能。方法是编辑 :file:`/lib/systemd/system/bluetooth.service` 文件，并确保在守护进程的执行启动行中包含 :literal:`-E` 选项：

.. code-block:: console

   ExecStart=/usr/libexec/bluetooth/bluetoothd -E

最后，重新加载并重启守护进程：

.. code-block:: console

   sudo systemctl daemon-reload
   sudo systemctl restart bluetooth

.. _bluetooth_qemu_native:

在 QEMU 或 native_sim 上运行
****************************

可以使用 :ref:`QEMU 模拟器 <application_run_qemu>` 或 :zephyr:board:`native_sim <native_sim>` 运行蓝牙应用。

无论哪种情况，都需要将蓝牙控制器从主机操作系统（Linux）导出到模拟器。为此，需要使用 :ref:`bluetooth_bluez` 一节中描述的某些工具。

使用主机系统的蓝牙控制器
========================

主机操作系统的蓝牙控制器按以下方式连接：

* 通过 UNIX 套接字连接到第二条 QEMU 串行线路。借助 QEMU 选项 :literal:`-serial unix:/tmp/bt-server-bredr` 使用该套接字。只要应用启用了蓝牙支持，该选项就会通过 :makevar:`QEMU_EXTRA_FLAGS` 自动传递给 QEMU。
* 通过传递给 native_sim 可执行文件的命令行选项连接到 :ref:`native_sim 的 BT 用户通道驱动 <nsim_bt_host_cont>`，即 ``--bt-dev=hci0``

在主机端，BlueZ 允许通过所谓的用户通道导出其蓝牙控制器，供 QEMU 和 :zephyr:board:`native_sim <native_sim>` 使用。

.. note::
   仅在使用 QEMU 时需要运行 ``btproxy``。native_sim 会自动处理 UNIX 套接字代理。

如果使用 QEMU，则需再执行一个步骤，使用 ``btproxy`` 使控制器可用：

#. 确保蓝牙控制器处于关闭状态

#. 使用 btproxy 工具打开监听 UNIX 套接字，输入：

   .. code-block:: console

      sudo tools/btproxy -u -i 0
      Listening on /tmp/bt-server-bredr

   您可能需要将 :literal:`-i 0` 替换为要代理的控制器索引。

   如果在运行 QEMU 时看到 ``Received unknown host packet type 0x00``，请在 ``btproxy`` 命令行中添加 :literal:`-z`，以忽略启动时传输的任何空字节。

硬件连接并准备就绪后，即可继续构建并运行示例：

* 在 :literal:`samples/bluetooth` 中选择一个蓝牙示例应用。

* 要在 QEMU 中运行蓝牙应用，请输入：

  .. zephyr-app-commands::
     :zephyr-app: samples/bluetooth/<sample>
     :host-os: unix
     :board: qemu_x86
     :goals: run
     :compact:

  现在运行 QEMU 会通过第二条串行线路连接到 :literal:`bt-server-bredr` UNIX 套接字，使应用能够访问蓝牙控制器。

* 要在 :zephyr:board:`native_sim <native_sim>` 中运行蓝牙应用，请先构建它：

  .. zephyr-app-commands::
     :zephyr-app: samples/bluetooth/<sample>
     :host-os: unix
     :board: native_sim
     :goals: build
     :compact:

  然后使用以下命令运行它::

     $ sudo ./build/zephyr/zephyr.exe --bt-dev=hci0

使用基于 Zephyr 的蓝牙控制器
============================

根据您手头可用的硬件，在构建单模、基于 Zephyr 的蓝牙控制器时，可以选择两种传输方式：

* UART：使用 :zephyr:code-sample:`bluetooth_hci_uart` 示例，并按照 :ref:`bluetooth-hci-uart-qemu-posix` 中的说明操作。
* USB：使用 :zephyr:code-sample:`bluetooth_hci_usb` 示例，然后将其视为主机系统蓝牙控制器（参见上一节）

.. _bluetooth-hci-tracing:

HCI 跟踪
========

在连接到外部控制器的计算机上运行主机时，能够以 :ref:`bluetooth-hci` 日志的格式查看两者之间的完整交互日志非常有用。要查看这些日志，可以使用 BlueZ 内置的 ``btmon`` 工具：

.. code-block:: console

   $ btmon

输出类似如下::

   = New Index: 00:00:00:00:00:00 (Primary,Virtual,Control)                     0.274200
   = Open Index: 00:00:00:00:00:00                                              0.274500
   < HCI Command: Reset (0x03|0x0003) plen 0                                 #1 0.274600
   > HCI Event: Command Complete (0x0e) plen 4                               #2 0.274700
         Reset (0x03|0x0003) ncmd 1
         Status: Success (0x00)
   < HCI Command: Read Local Supported Features (0x04|0x0003) plen 0         #3 0.274800
   > HCI Event: Command Complete (0x0e) plen 12                              #4 0.274900
         Read Local Supported Features (0x04|0x0003) ncmd 1
         Status: Success (0x00)
         Features: 0x00 0x00 0x00 0x00 0x60 0x00 0x00 0x00
            BR/EDR Not Supported
            LE Supported (Controller)

.. _bluetooth-embedded-hci-tracing:

嵌入式 HCI 跟踪
---------------

当主机和控制器都运行在实际集成电路（IC）上时，默认情况下控制台上只能看到普通日志消息，无法访问主机与控制器之间的 HCI 流量。不过，有一种特殊的蓝牙日志模式，可将控制台切换为使用二进制协议，并交错输出普通日志消息和 HCI 流量。

在构建应用之前，设置以下 Kconfig 选项以启用此协议：

.. code-block:: cfg

   CONFIG_BT_DEBUG_MONITOR_UART=y
   CONFIG_UART_CONSOLE=n

- 设置 :kconfig:option:`CONFIG_BT_DEBUG_MONITOR_UART` 可激活格式化功能
- 清除 :kconfig:option:`CONFIG_UART_CONSOLE` 会使 UART 无法用于系统控制台。例如，对于 ``printk`` 和 :kconfig:option:`启动横幅 <CONFIG_BOOT_BANNER>`

可选地，在监控 UART 驱动支持中断 API 的开发板上，设置 :kconfig:option:`CONFIG_BT_DEBUG_MONITOR_UART_INTERRUPT_DRIVEN` 会将完整的监控记录排队，并从 UART 中断处理程序中发送，而不是在发送每个字节时阻塞。无法放入缓冲区的记录将被丢弃，并在下一条监控记录中报告。可以使用 :kconfig:option:`CONFIG_BT_DEBUG_MONITOR_UART_BUFFER_SIZE` 调整缓冲区大小。

要解码现在将发送到控制台 UART 的二进制协议，需要使用 :ref:`BlueZ <bluetooth_bluez>` 提供的 btmon 工具：

.. code-block:: console

   $ btmon --tty <console TTY> --tty-speed 115200

如果 UART 不可用（或者仍希望使用非二进制日志），可以改用 :kconfig:option:`CONFIG_BT_DEBUG_MONITOR_RTT`，它将使用 Segger RTT。例如，尝试连接到序列号为 683578642 的 nRF52840DK 时：

.. code-block:: console

   $ btmon --jlink nRF52840_xxAA,683578642

.. _bluetooth_virtual_posix:

在虚拟控制器和 native_sim 上运行
********************************

蓝牙物理控制器的替代方案是使用虚拟控制器。该控制器可以通过 HCI TCP 服务器连接。此 TCP 服务器必须支持 HCI H4 协议。与物理控制器方案相比，虚拟控制器允许在没有物理蓝牙控制器的情况下测试运行于原生开发板上的 Zephyr 应用。

虚拟控制器的主要用例是在无需蓝牙硬件的情况下进行蓝牙连接测试。这样可以针对蓝牙网关或移动应用等外部应用实现蓝牙集成测试的自动化。

为了演示此功能，下面给出了与虚拟控制器交互的示例。为此，使用了 Google 的实验性 Python 模块 `Bumble`_，因为它可以创建 TCP 蓝牙虚拟控制器并与 Zephyr 蓝牙主机连接。要安装 bumble，请参阅 `Bumble Getting Started Guide`_。

.. note::
   如果您的 Zephyr 应用需要使用 HCI LE Set 扩展命令，请从 Bumble 安装 ``controller-extended-advertising`` 分支。

Android 模拟器
==============

您可以通过将蓝牙 Zephyr 应用连接到 `Android Emulator`_ 来测试虚拟控制器。

要将应用连接到 Android 模拟器，请执行以下步骤：

    #. 构建 Zephyr 应用并禁用 HCI ACL 流控制（即 ``CONFIG_BT_HCI_ACL_FLOW_CONTROL=n``），因为 Android 的虚拟控制器目前不支持该功能。

    #. 安装 Android Emulator 33.1.4.0 或更高版本。最简单的方法是安装最新的 `Android Studio Preview`_ 版本。

    #. 使用 `Android Device Manager`_ 创建新的 Android 虚拟设备（AVD）。AVD 应至少使用 SDK API 34。

    #. 在终端中按如下方式运行 Android 模拟器：

       ``emulator avd YOUR_AVD -packet-streamer-endpoint default``

    #. 使用 `Bumble`_ 工具 ``hci-bridge`` 在 Zephyr 应用与 Android 模拟器的虚拟控制器之间创建蓝牙桥接。

       ``bumble-hci-bridge tcp-server:_:1234 android-netsim``

       该命令将在本地主机 IP 地址 ``127.0.0.1`` 和端口号 ``1234`` 上创建 TCP 服务器桥接。

    #. 运行 Zephyr 应用并连接到上一步创建的 TCP 服务器。

       ``./zephyr.exe --bt-dev=127.0.0.1:1234``

完成这些步骤后，Zephyr 应用将通过使用 Bumble 桥接的虚拟蓝牙控制器供 Android 模拟器使用。您可以打开 AVD 中的蓝牙设置并扫描 Zephyr 应用设备，以验证 Zephyr 应用能够通过蓝牙通信。要测试这一点，可以构建蓝牙外设示例，例如 :zephyr:code-sample:`ble_peripheral_hr` 或 :zephyr:code-sample:`ble_peripheral_dis`。

.. _bluetooth_ctlr_bluez:

将基于 Zephyr 的控制器与 BlueZ 配合使用
***************************************

如果要使用 BlueZ 的蓝牙主机测试由 Zephyr 驱动的蓝牙控制器，则需要 :ref:`bluetooth_bluez` 一节中描述的若干工具。安装这些工具后，即可使用它们与基于 Zephyr 的控制器交互：

   .. code-block:: console

      sudo tools/btmgmt --index 0
      [hci0]# auto-power
      [hci0]# find -l

您可能需要将 :literal:`--index 0` 替换为要管理的控制器索引。有关 :file:`btmgmt` 的更多信息，请参阅其手册页。


.. _nRF Connect for Android: https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&hl=en
.. _nRF Connect for iOS: https://itunes.apple.com/us/app/nrf-connect/id1054362403
.. _LightBlue for Android: https://play.google.com/store/apps/details?id=com.punchthrough.lightblueexplorer&hl=en_US
.. _LightBlue for iOS: https://itunes.apple.com/us/app/lightblue-explorer/id557428110
.. _nRF Mesh for Android: https://play.google.com/store/apps/details?id=no.nordicsemi.android.nrfmeshprovisioner&hl=en
.. _nRF Mesh for iOS: https://itunes.apple.com/us/app/nrf-mesh/id1380726771
.. _Bumble: https://github.com/google/bumble
.. _Bumble Getting Started Guide: https://google.github.io/bumble/getting_started.html
.. _Android Emulator: https://developer.android.com/studio/run/emulator
.. _Android Device Manager: https://developer.android.com/studio/run/managing-avds
.. _Android Studio Preview: https://developer.android.com/studio/preview
