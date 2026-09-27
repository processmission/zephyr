.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _debug-probes:

Debug Probes
############

*调试探针* 是一种专用硬件，用于控制另一块开发板上运行的 Zephyr 应用。它通常支持读写寄存器和内存，并可在主机工作站上通过 GDB 等工具进行断点调试。也可能支持其他调试软件，以及 :ref:`程序执行跟踪 <tracing>` 等高级功能。Zephyr 支持的相关主机软件见 :ref:`flash-debug-host-tools`。

调试探针通常通过 USB 连接主机，有时也可通过 IP 网络等方式访问。它通常使用 JTAG 或 SWD 协议连接运行 Zephyr 的设备，可以是独立硬件，也可以集成在运行 Zephyr 的同一块开发板上。

Zephyr 支持的许多开发板包含第二个微控制器，充当板载调试探针、USB 转串口适配器，有时还支持拖放式闪存编程。这样无需另购外部探针，并可选用多种调试主机工具。

多个硬件厂商提供自有品牌的板载探针。NXP 开发板根据探针固件运行的微控制器，可能使用 `OpenSDA <#opensda-onboard-debug-probe>`_、`LPC-Link2 <#lpc-link2-onboard-debug-probe>`_ 或 `MCU-Link <#mcu-link-onboard-debug-probe>`_。ST 开发板配有 `ST-LINK probe <#stlink-v21-onboard-debug-probe>`_。每种探针微控制器可支持一种或多种固件，分别与对应主机工具通信。例如，OpenSDA 烧录 DAPLink 固件后可与 pyOCD 或 OpenOCD 通信，烧录 J-Link 固件后则可与 J-Link 主机工具通信。


+----------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------+
| | *调试探针与主机工具*                       | 主机工具                                                                                                                                     |
| | *兼容性表*                                 |                                                                                                                                              |
|                                              +----------------------+----------------------+-----------------------+----------------------+----------------------+--------------------------+
|                                              | **J-Link Debug**     | **OpenOCD**          | **pyOCD**             | **NXP S32DS**        | **NXP LinkServer**   | **ST-LINK GDB Server**   |
+------------------+---------------------------+----------------------+----------------------+-----------------------+----------------------+----------------------+--------------------------+
| 调试探针         | **外接 J-Link**           | ✓                    | ✓                    |                       |                      |                      |                          |
|                  +---------------------------+----------------------+----------------------+-----------------------+----------------------+----------------------+--------------------------+
|                  | **LPC-Link2 CMSIS-DAP**   |                      |                      |                       |                      | ✓                    |                          |
|                  +---------------------------+----------------------+----------------------+-----------------------+----------------------+----------------------+--------------------------+
|                  | **LPC-Link2 J-Link**      | ✓                    |                      |                       |                      |                      |                          |
|                  +---------------------------+----------------------+----------------------+-----------------------+----------------------+----------------------+--------------------------+
|                  | **MCU-Link CMSIS-DAP**    |                      |                      |                       |                      | ✓                    |                          |
|                  +---------------------------+----------------------+----------------------+-----------------------+----------------------+----------------------+--------------------------+
|                  | **MCU-Link J-Link**       | ✓                    |                      |                       |                      |                      |                          |
|                  +---------------------------+----------------------+----------------------+-----------------------+----------------------+----------------------+--------------------------+
|                  | **NXP S32 调试探针**      |                      |                      |                       | ✓                    |                      |                          |
|                  +---------------------------+----------------------+----------------------+-----------------------+----------------------+----------------------+--------------------------+
|                  | **OpenSDA DAPLink**       |                      | ✓                    | ✓                     |                      | ✓                    |                          |
|                  +---------------------------+----------------------+----------------------+-----------------------+----------------------+----------------------+--------------------------+
|                  | **OpenSDA J-Link**        | ✓                    |                      |                       |                      |                      |                          |
|                  +---------------------------+----------------------+----------------------+-----------------------+----------------------+----------------------+--------------------------+
|                  | **ST-LINK/V2-1**          | ✓                    | ✓                    | *部分 STM32 开发板*   |                      |                      | ✓                        |
+------------------+---------------------------+----------------------+----------------------+-----------------------+----------------------+----------------------+--------------------------+


Zephyr 支持的某些开发板没有板载探针，必须使用外部探针。带有板载探针的开发板通常也提供 SWD 或 JTAG 接口，允许改用外部探针。这有助于绕过板载探针的限制，例如不支持高级调试器或高速跟踪。可能需要调整跳线，避免板载探针干扰外部探针。

.. _nxp-onboard-debug-probes:

NXP 板载调试探针
****************

NXP 开发板可能配备 :ref:`mcu-link-onboard-debug-probe`、:ref:`lpc-link2-onboard-debug-probe` 或 :ref:`opensda-onboard-debug-probe` 等板载探针。它们均由评估板上的辅助微控制器实现，可根据调试微控制器 SoC 判断类型：

- LPC55S69：:ref:`mcu-link-onboard-debug-probe`
- LPC4322：:ref:`lpc-link2-onboard-debug-probe`
- MK20：:ref:`opensda-onboard-debug-probe`

例如，:zephyr:board:`frdm_k64f` 使用 MK20 调试微控制器，因此采用 :ref:`opensda-onboard-debug-probe`。

.. _mcu-link-onboard-debug-probe:

MCU-Link 板载调试探针
*********************

MCU-Link 板载探针使用 LPC55S69 SoC，支持以下固件：

- :ref:`mcu-link-cmsis-onboard-debug-probe` （默认固件）
- :ref:`mcu-link-jlink-onboard-debug-probe`

此探针通过 MCU-Link 主机工具烧录，工具随 :ref:`linkserver-debug-host-tools` 安装。NXP 建议使用 `MCUXpresso Installer`_ 安装 LinkServer 工具。

.. _mcu-link-cmsis-onboard-debug-probe:

MCU-Link CMSIS-DAP 板载调试探针
===============================

这是 MCU-Link 探针的默认固件。CMSIS-DAP 探针支持通过任何兼容工具链调试，包括 IAR EWARM、Keil MDK、NXP MCUXpresso IDE 及其 VS Code 扩展。除调试功能外，MCU-Link 还可能提供：

1. SWO 跟踪端点：MCUXpresso 通过此虚拟设备获取 SWO 跟踪数据，详情见 MCUXpresso IDE 文档。
#. 连接目标处理器的虚拟 COM（VCOM）端口／UART 桥接。
#. USB 转 UART、SPI 和／或 I2C 接口，取决于 MCU-Link 类型及实现。
#. 目标 MCU 的能耗测量。

此探针兼容以下调试主机工具：

- :ref:`linkserver-debug-host-tools`

安装 MCU-Link 主机工具后，按以下步骤烧录 CMSIS-DAP 固件：

1. 确保主机已有 MCU-Link 工具，可以通过安装 :ref:`linkserver-debug-host-tools` 获取。

#. 连接 DFU 跳线，再连接开发板 USB 调试端口，使 MCU-Link 微控制器进入 DFU 启动模式。该跳线也可能称为 ISP 跳线，连接到 LPC55S69 的 ``PIO0_5``。

#. 运行 MCU-Link 安装目录中 ``scripts`` 下的 ``program_CMSIS`` 脚本。

#. 移除 DFU 跳线，并将开发板断电后重新上电。

.. _mcu-link-jlink-onboard-debug-probe:

MCU-Link JLink 板载调试探针
===========================

此固件提供兼容 JLink 的调试接口及 USB 串口适配器，兼容以下调试主机工具：

- :ref:`jlink-debug-host-tools`

这些探针默认未安装 JLink 固件，需要更新。安装 MCU-Link 主机工具后，按以下步骤烧录 JLink 固件：

1. 确保主机已有 MCU-Link 工具，可以通过安装 :ref:`linkserver-debug-host-tools` 获取。

#. 连接 DFU 跳线，再连接开发板 USB 调试端口，使 MCU-Link 微控制器进入 DFU 启动模式。该跳线也可能称为 ISP 跳线，连接到 LPC55S69 的 ``PIO0_5``。

#. 运行 MCU-Link 安装目录中 ``scripts`` 下的 ``program_JLINK`` 脚本。

#. 移除 DFU 跳线，并将开发板断电后重新上电。

.. _lpc-link2-onboard-debug-probe:

LPC-LINK2 板载调试探针
**********************

LPC-LINK2 板载探针使用 LPC4322 SoC，支持以下固件：

- :ref:`lpclink2-cmsis-onboard-debug-probe`
- :ref:`lpclink2-jlink-onboard-debug-probe`
- :ref:`lpclink2-daplink-onboard-debug-probe` （默认固件）

此探针通过 LPCScrypt 主机工具烧录，工具随 :ref:`linkserver-debug-host-tools` 安装。NXP 建议使用 `MCUXpresso Installer`_ 安装 LinkServer 工具。

.. _lpclink2-cmsis-onboard-debug-probe:

LPC-LINK2 CMSIS DAP 板载调试探针
================================

CMSIS-DAP 探针支持通过任何兼容工具链调试，包括 IAR EWARM、Keil MDK、NXP MCUXpresso IDE 及其 VS Code 扩展。除调试功能外，LPC-Link2 还提供：

1. SWO 跟踪端点：MCUXpresso 通过此虚拟设备获取 SWO 跟踪数据，详情见 MCUXpresso IDE 文档。
2. 连接目标处理器的虚拟 COM（VCOM）端口／UART 桥接。
3. 用于与 I2C 和 SPI 外设通信的 LPCSIO 桥接。

此探针固件兼容以下调试主机工具：

- :ref:`linkserver-debug-host-tools`

可以按以下步骤更新为 CMSIS-DAP 固件：

1. 确保主机已有 LPCScrypt 工具，可以通过安装 :ref:`linkserver-debug-host-tools` 获取。

#. 连接 DFU 跳线，再连接开发板 USB 调试端口，使 LPC-Link2 微控制器进入 DFU 启动模式。该跳线连接到 LPC4322 的 ``P2_6``。

#. 运行 LPCScrypt 安装目录中 ``scripts`` 下的 ``program_CMSIS`` 脚本。

#. 移除 DFU 跳线，并将开发板断电后重新上电。

.. _lpclink2-jlink-onboard-debug-probe:

LPC-Link2 J-Link 板载调试探针
=============================

.. note:: 在部分开发板上，J-Link 探针固件无法再通过 USB 调试端口给开发板供电，烧录该固件后必须采用其他供电方式。

此固件提供兼容 JLink 的调试接口及 USB 串口适配器，兼容以下调试主机工具：

- :ref:`jlink-debug-host-tools`

可以按以下步骤更新为 J-Link 固件：

.. note:: 访问 `Firmware for LPCXpresso`_，确认固件支持当前开发板。

1. 确保主机已有 LPCScrypt 工具，可以通过安装 :ref:`linkserver-debug-host-tools` 获取。

#. 连接 DFU 跳线，再连接开发板 USB 调试端口，使 LPC-Link2 微控制器进入 DFU 启动模式。该跳线连接到 LPC4322 的 ``P2_6``。

#. 运行 LPCScrypt 安装目录中 ``scripts`` 下的 ``program_JLINK`` 脚本。

#. 移除 DFU 跳线，并将开发板断电后重新上电。

.. _lpclink2-daplink-onboard-debug-probe:

LPC-Link2 DAPLink 板载调试探针
==============================

LPC-Link2 DAPLink 是基于 LPC-Link2 的开发板出厂默认固件，但不推荐使用。请按上述说明更新为 :ref:`lpclink2-cmsis-onboard-debug-probe`。烧录 DAPLink 固件的详情见 `NXP AN13206`_。

.. _opensda-onboard-debug-probe:

OpenSDA 板载调试探针
********************

OpenSDA 板载探针基于 NXP MK20 SoC，支持拖放编程及以下调试固件：

- :ref:`opensda-daplink-onboard-debug-probe` （默认固件）
- :ref:`opensda-jlink-onboard-debug-probe`

.. _opensda-daplink-onboard-debug-probe:

OpenSDA DAPLink 板载调试探针
============================

此探针固件兼容以下调试主机工具：

- :ref:`pyocd-debug-host-tools`
- :ref:`openocd-debug-host-tools`
- :ref:`linkserver-debug-host-tools`

将 DAPLink OpenSDA 固件烧录到 OpenSDA 微控制器即可实现此探针。NXP 提供 `OpenSDA DAPLink Board-Specific Firmwares`_。

烧录固件前先安装调试主机工具。

与其他 OpenSDA 探针一样，固件烧录步骤如下：

1. 按住复位按钮并给开发板上电，使 OpenSDA 微控制器进入引导加载程序模式。这里的“引导加载程序模式”针对 OpenSDA 微控制器自身，而非运行 Zephyr 应用的目标微控制器。

#. 上电后松开复位按钮，会枚举出名为 **BOOTLOADER** 或 **MAINTENANCE** 的 USB 大容量存储设备。如果名称为 **BOOTLOADER**，请先按照 `DAPLink Bootloader Update`_ 将引导加载程序更新到最新版。

#. 将 OpenSDA 固件二进制文件复制到 USB 大容量存储设备。

#. 将开发板断电后重新上电，这次不要按住复位按钮。应枚举出三个 USB 设备：CDC 设备（串口）、HID 设备（调试端口）及大容量存储设备（拖放式闪存编程）。

.. _opensda-jlink-onboard-debug-probe:

OpenSDA J-Link 板载调试探针
===========================

此探针兼容以下调试主机工具：

- :ref:`jlink-debug-host-tools`

将 J-Link OpenSDA 固件烧录到 OpenSDA 微控制器即可实现此探针。Segger 提供 `OpenSDA J-Link Generic Firmwares`_ 和 `OpenSDA J-Link Board-Specific Firmwares`_，有专用版本时通常推荐后者。i.MX RT 开发板必须使用专用固件才能支持外部闪存；通用固件则兼容所有 Kinetis 开发板。

烧录固件前先安装调试主机工具。

与其他 OpenSDA 探针一样，固件烧录步骤如下：

1. 按住复位按钮并将 USB 接入开发板调试端口，使 OpenSDA 微控制器进入引导加载程序模式。此模式针对 OpenSDA 微控制器自身，而非运行 Zephyr 应用的目标微控制器。

#. 上电后松开复位按钮，会枚举出名为 **BOOTLOADER** 或 **MAINTENANCE** 的 USB 大容量存储设备。如果名称为 **BOOTLOADER**，请先按照 `DAPLink Bootloader Update`_ 将引导加载程序更新到最新版。

#. 将 OpenSDA 固件二进制文件复制到 USB 大容量存储设备。

#. 将开发板断电后重新上电，这次不要按住复位按钮。应枚举出两个 USB 设备：CDC 设备（串口）和厂商专用设备（调试端口）。

.. _jlink-external-debug-probe:

J-Link 外接调试探针
*******************

`Segger J-Link`_ 是外接探针产品系列，包括 J-Link EDU、PLUS、ULTRA+ 和 PRO，支持众多不同架构及厂商的设备。

此探针兼容以下调试主机工具：

- :ref:`jlink-debug-host-tools`
- :ref:`openocd-debug-host-tools`

烧录固件前先安装调试主机工具。

.. _stlink-v21-onboard-debug-probe:

ST-LINK/V2-1 板载调试探针
*************************

ST-LINK/V2-1 是所有 Nucleo 和 Discovery 开发板内置的串口与调试适配器，在计算机或其他 USB 主机与目标处理器之间提供桥接，仅需一根 USB 线即可调试、烧录和串行通信。

它兼容以下主机调试工具：

- :ref:`openocd-debug-host-tools`
- :ref:`jlink-debug-host-tools`
- :ref:`stm32cubeclt-host-tools`

对于部分 STM32 开发板，还兼容：

- :ref:`pyocd-debug-host-tools`

OpenOCD 可直接使用，而使用 J-Link 需要先更新固件。SEGGER 提供固件，可将 Nucleo 和 Discovery 上的 ST-LINK/V2-1 升级为兼容 J-LinkOB 的探针，从而使用大多数 J-Link 功能，例如高速闪存下载、调试以及免费 GDBServer。

将 ST-LINK/V2-1 升级为 JLink 或恢复原固件的更多信息，见 `Segger over ST-Link`_。

通过 ST-Link 烧录和调试
=======================

.. tabs::

    .. tab:: 使用 OpenOCD

        ST-Link 默认可使用 OpenOCD，并将其配置为默认烧录和调试工具。操作如下：

          .. zephyr-app-commands::
             :zephyr-app: samples/hello_world
             :goals: flash

          .. zephyr-app-commands::
             :zephyr-app: samples/hello_world
             :goals: debug

    .. tab:: _`Using Segger J-Link`

        STLink 烧录 SEGGER 固件，且主机安装 J-Link GDB 服务器后，可按以下方式烧录和调试：

        调用 CMake 时传入 ``-DBOARD_FLASH_RUNNER=jlink``，将默认 OpenOCD 运行器改为 J-Link。也可以在应用 ``CMakeList.txt`` 中添加以下行。

          .. code-block:: cmake

             set(BOARD_FLASH_RUNNER jlink)

        使用 Zephyr 元工具 west 时，可以通过 ``--runner`` 或 ``-r`` 更改默认运行器。

          .. code-block:: console

             west flash --runner jlink

        使用 ``jlink`` 将调试器附加到开发板并打开调试控制台：

          .. code-block:: console

             west debug --runner jlink

        west 及其选项详情见 :ref:`west`。

        如果应用改用 `Segger RTT`_ 控制台，请打开 telnet：

          .. code-block:: console

             $ telnet localhost 19021
             Trying ::1...
             Trying 127.0.0.1...
             Connected to localhost.
             Escape character is '^]'.
             SEGGER J-Link V6.30f - Real time terminal output
             J-Link STLink V21 compiled Jun 26 2017 10:35:16 V1.0, SN=773895351
             Process: JLinkGDBServerCLExe
             Zephyr Shell, Zephyr version: 1.12.99
             Type 'help' for a list of available commands
             shell>

        如果没有 RTT 输出，可能需要禁用示例或应用默认启用、且与 RTT 冲突的其他控制台，例如在 menuconfig 中禁用 UART_CONSOLE。

.. _stlink-adapter-firmware-update:

更新或恢复 ST-Link 固件
=======================

可以通过 `STM32CubeProgrammer Tool`_ 更新 ST-Link 固件。遇到烧录问题时通常有帮助，例如使用 twister 的设备测试选项时。

安装后，可用以下命令更新已连接开发板的 ST-Link 固件：

  .. code-block:: console

     s java -jar ~/STMicroelectronics/STM32Cube/STM32CubeProgrammer/Drivers/FirmwareUpgrade/STLinkUpgrade.jar -sn <board_uid>

board_uid 可通过 twister 的 generate-hardware-map 选项获取。twister 及选项详情见 :ref:`twister_script`。

OpenOCD 弃用 HLA ST-Link 接口
=============================

OpenOCD 于 2024 年 1 月弃用 ST-Link 固件使用的旧 HLA 接口，改用通用 DAP 接口，见 `OpenOCD deprecates ST-Link HLA Interface`_。ST-Link 固件从 2015 年的 v2j24 起支持 DAP 接口。

弃用后，使用较新 OpenOCD（v0.12.0 标签之后版本）时，如果 ST-Link 固件早于 v2j24，可能遇到通信问题。建议更新固件，参见 `ST-LINK firmware update <#_stlink-adapter-firmware-update>`_。如果无法更新，仍可修改 OpenOCD 配置使用旧 HLA 接口，将以下两行（如存在）：

  .. code-block::

    source [find interface/stlink-dap.cfg]
    transport select dapdirect_swd

替换为以下两行：

  .. code-block::

    source [find interface/stlink-hla.cfg]
    transport select hla_swd

.. _nxp-s32-debug-probe:

NXP S32 调试探针
****************

`NXP S32 Debug Probe`_ 通过标准调试端口调试 NXP S32 目标系统，可通过 USB 连接开发工作站，也可通过以太网远程连接。

NXP S32 调试探针设计为配合 NXP S32 Design Studio（S32DS）及 NXP 汽车微控制器和处理器使用。烧录固件前，按照 :ref:`nxp-s32-debug-host-tools` 安装主机工具。

.. _black-magic-probe:

Black Magic Probe
*****************

Black Magic Probe 是配合 `Black Magic Debug`_ 固件使用的开源调试硬件。固件集成 GDB 服务器，可以直接从 ``gdb`` 连接目标设备。

部分基于 STM32F103 的开发板可运行 `Black Magic Debug`_ 固件，见 `Black Magic Debug supported hardware`_。

.. _LPCScrypt:
   https://www.nxp.com/lpcscrypt

.. _Firmware for LPCXpresso:
   https://www.segger.com/products/debug-probes/j-link/models/other-j-links/lpcxpresso-on-board/

.. _OpenSDA DAPLink Board-Specific Firmwares:
   https://www.nxp.com/opensda

.. _OpenSDA J-Link Generic Firmwares:
   https://www.segger.com/downloads/jlink/#JLinkOpenSDAGenericFirmwares

.. _OpenSDA J-Link Board-Specific Firmwares:
   https://www.segger.com/downloads/jlink/#JLinkOpenSDABoardSpecificFirmwares

.. _Segger J-Link:
   https://www.segger.com/products/debug-probes/j-link/

.. _Segger over ST-Link:
   https://www.segger.com/products/debug-probes/j-link/models/other-j-links/st-link-on-board/

.. _Segger RTT:
    https://www.segger.com/jlink-rtt.html

.. _STM32CubeProgrammer Tool:
    https://www.st.com/en/development-tools/stm32cubeprog.html

.. _OpenOCD deprecates ST-Link HLA Interface:
    https://sourceforge.net/p/openocd/code/ci/34ec5536c0ba3315bc5a841244bbf70141ccfbb4

.. _MCUXpresso Installer:
        https://www.nxp.com/lgfiles/updates/mcuxpresso/MCUXpressoInstaller.exe

.. _NXP S32 Debug Probe:
   https://www.nxp.com/design/software/automotive-software-and-tools/s32-debug-probe:S32-DP

.. _NXP AN13206:
   https://www.nxp.com/docs/en/application-note/AN13206.pdf

.. _DAPLink Bootloader Update:
   https://os.mbed.com/blog/entry/DAPLink-bootloader-update/

.. _Black Magic Debug:
   https://black-magic.org/index.html

.. _Black Magic Debug supported hardware:
   https://black-magic.org/index.html#other-hardware-supported-by-black-magic-debug
