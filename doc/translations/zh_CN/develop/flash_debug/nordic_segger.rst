.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

.. _nordic_segger:

Nordic nRF5x Segger J-Link
##########################

概述
****

所有 Nordic nRF5x 开发套件、预览开发套件和 Dongle 都配有调试芯片 Atmel ATSAM3U2C，提供以下功能：

* Segger J-Link 固件和桌面工具
* nRF5x 芯片的 SWD 调试
* 支持拖放映像烧录的大容量存储设备
* 桥接到 nRF5x UART 外设的 USB CDC ACM 串口
* Segger RTT 控制台
* Segger Ozone 调试器

安装 Segger J-Link 软件
***********************

按照以下步骤安装 J-Link 软件及文档包：

#. 从 `J-Link Software and documentation pack`_ 网站下载适合的平台软件包。
#. 根据平台安装软件包或运行安装程序。
#. 连接支持 J-Link 的 nRF5x DK、PDK 或 Dongle 后，应出现 USB 大容量存储设备对应的驱动器，以及一个串口。

安装 nRF5x 命令行工具
*********************

nRF5x 命令行工具可从命令行控制 nRF5x 设备，包括复位、擦除或烧录闪存等。

访问 `nRF5x Command-Line Tools`_，选择操作系统并安装。

安装后，确保可执行文件搜索路径中包含 ``nrfjprog``，以便从任意位置调用。

.. _nordic_segger_flashing:

烧录
****

按照说明安装 Segger J-Link 软件和 nRF5x 命令行工具后，通过以下步骤将编译好的 Zephyr 映像写入闪存：

* 用 micro-USB 线连接 nRF5x 开发板与计算机。
* 擦除 nRF5x 芯片闪存：

.. code-block:: console

   nrfjprog --eraseall -f nrf5<x>

其中，nRF51 开发板的 ``<x>`` 为 1，nRF52 开发板为 2。

* 从所选示例目录烧录 Zephyr 映像：

.. code-block:: console

   nrfjprog --program outdir/<board>/zephyr.hex -f nrf5<x>

其中，``<board>`` 是构建时 BOARD 指定的开发板名称，例如 nrf52dk/nrf52832；nRF51 开发板的 ``<x>`` 为 1，nRF52 开发板为 2。

* 复位并启动 Zephyr：

.. code-block:: console

   nrfjprog --reset -f nrf5<x>

其中，nRF51 开发板的 ``<x>`` 为 1，nRF52 开发板为 2。

设置 USB CDC ACM 串口
*********************

**重要说明**：nRF5x 开发板的 Segger J-Link 固件存在问题，可能在某些计算机上导致 USB CDC ACM 串口数据丢失或损坏。可以按 :ref:`nordic_segger_msd` 禁用开发板的大容量存储设备以规避。

Windows
=======

串口显示为 ``COMxx``，可在设备管理器的“端口（COM 和 LPT）”中查看。

GNU/Linux
=========

串口显示为 ``/dev/ttyACMx``。默认并非所有用户都能访问；运行以下命令，将用户加入 dialout 组以取得串口权限。重新登录后才会生效。

.. code-block:: bash

   sudo usermod -a -G dialout `whoami`

较新版本存在 `ModemManager send AT commands to TTY-like devices`_ 的行为，Nordic 开发套件也受影响。这会让串口暂时无法使用几秒钟；如果应用读取 UART 数据，还可能造成异常行为。运行应用前，可通过以下命令临时禁用 ModemManager：

.. code-block:: bash

   systemctl stop ModemManager.service
   systemctl disable ModemManager.service

也可以执行以下命令，通过 `blocklist Segger devices by editing udev rules`_ 修改规则，使 ModemManager 忽略 Segger 设备：

.. code-block:: bash

   sudo sh -c 'echo "ATTRS{idVendor}==\"1366\", ENV{ID_MM_DEVICE_IGNORE}=\"1\" " \
     >> /etc/udev/rules.d/99-segger-modemmanager-blocklist.rules'
   sudo service udev restart

预计 ModemManager 1.8 和新版 Segger IMCU 固件将修复此问题。

Apple macOS（OS X）
===================

串口显示为 ``/dev/tty.usbmodemXXXX``。

.. _nordic_segger_msd:

禁用大容量存储设备功能
**********************

由于 Segger J-Link 固件的已知问题，在某些操作系统和版本上，通过 USB CDC ACM 串口传输超过 64 字节的数据包时，可能出现数据损坏或丢失。GNU/Linux 和 macOS（OS X）上均观察到此问题。

为避免此问题，可禁用大容量存储设备。首先打开：

* GNU/Linux 或 macOS（OS X）上，在终端启动 JLinkExe。
* Microsoft Windows 上，打开 JLink Commander 应用。

然后输入：

.. code-block:: bat

   MSDDisable

最后拔下并重新插入开发板。大容量存储设备应不再出现，此时即可通过虚拟串口发送长数据包。Segger 提供的更多说明见 `Segger SAM3U Wiki`_。

RTT 控制台
**********

Segger J-Link 支持 `Real-Time Tracing (RTT)`_，可在目标 nRF5x 开发板与开发计算机之间建立双向终端连接，用于日志输出和输入。Zephyr 在 nRF5x 目标上支持 RTT；当经 USB CDC ACM 连接的 UART 已用于其他用途，例如 hci_uart 应用的 HCI 通信时，这尤其有用。要使用 RTT，先在 ``.conf`` 文件中添加以下内容启用它：

.. code-block:: cfg

   CONFIG_USE_SEGGER_RTT=y
   CONFIG_RTT_CONSOLE=y

.. warning::

   另有 ``HAS_SEGGER_RTT`` 符号，表示平台支持 SEGGER J-Link RTT，由 SoC Kconfig 文件自动设置。请勿将其与 ``USE_SEGGER_RTT`` 混淆。

   ``USE_SEGGER_RTT`` 依赖 ``HAS_SEGGER_RTT``。

如果没有 RTT 输出，可能需要禁用示例或应用默认启用、且与 RTT 冲突的其他控制台。例如，在 ``.conf`` 中添加以下内容禁用 UART 控制台：

.. code-block:: cfg

   CONFIG_UART_CONSOLE=n

启用 RTT 后编译并烧录，即可按以下步骤显示 RTT 控制台消息：

Windows
=======

* 打开 J-Link RTT Viewer 应用。
* 选择以下选项：

  * Connection：USB
  * Target Device：从列表选择芯片
  * Target Interface and Speed：SWD，4000 KHz
  * RTT Control Block：Auto Detection

GNU/Linux 和 macOS（OS X）
==========================

* 从终端打开 ``JLinkRTTLogger``。
* 选择以下选项：

  * Device Name：使用芯片的完整限定设备名称
  * Target Interface：SWD
  * Interface Speed：4000 KHz
  * RTT Control Block address：auto-detection
  * RTT Channel name or index：0
  * Output file：文件名，或用 ``/dev/stdout`` 直接显示在终端

Python 查看器
=============

Python RTT 查看工具位于 GitHub 仓库 `pyrtt-viewer`_。

Segger Ozone
************

Segger J-Link 兼容可视化调试器 `Segger Ozone`_，可从以下位置获取：

* `Segger Ozone Download`_

下载后安装，并按以下方式配置：

* Target Device：从列表选择芯片
* Target Interface：SWD
* Target Interface Speed：4 MHz
* Host Interface：USB

配置完成后，通过 File->Open 菜单打开构建目录中的 ``zephyr.elf``。

参考资料
********

.. target-notes::

.. _nRF5x Command-Line Tools: https://www.nordicsemi.com/Software-and-Tools/Development-Tools/nRF-Command-Line-Tools

.. _Segger SAM3U Wiki: https://wiki.segger.com/J-Link-OB_SAM3U
.. _Real-Time Tracing (RTT): https://www.segger.com/jlink-rtt.html
.. _pyrtt-viewer: https://github.com/thomasstenersen/pyrtt-viewer
.. _Segger Ozone: https://www.segger.com/ozone.html
.. _Segger Ozone Download: https://www.segger.com/downloads/jlink#Ozone

.. _ModemManager send AT commands to TTY-like devices: https://bugs.freedesktop.org/show_bug.cgi?id=85007
.. _blocklist Segger devices by editing udev rules: http://www.at91.com/linux4sam/bin/view/Linux4SAM/SoftwareTools#Device_or_resource_busy_dev_ttyA

.. _J-Link Software and documentation pack: https://www.segger.com/jlink-software.html
