.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _flash-debug-host-tools:

烧录与调试主机工具
##################

本指南介绍可以在主机工作站上运行、用于烧录和调试 Zephyr 应用的软件工具。

只要开发板硬件支持，且 Zephyr 开发板目录中的 :file:`board.cmake` 正确声明了支持，west 的 ``flash``、``debug``、``debugserver`` 和 ``attach`` 命令就内置支持所有这些工具。命令详情见 :ref:`west-build-flash-debug`。

.. _runner_blackmagicprobe:

Black Magic Probe
*****************

Black Magic Probe（BMP）是开源调试硬件，将 GDB 调试服务器功能集成在固件中，因此不需要单独的 GDB 服务器程序，也就没有对应的主机工具程序。

使用方法、支持的目标等详情见 :ref:`black-magic-probe`。

.. _atmel_sam_ba_bootloader:
.. _runner_bossac:

SAM 启动助手（SAM-BA）
**********************

Atmel SAM 启动助手（Atmel SAM-BA）允许通过 USB 或 UART 主机进行在系统编程（ISP），无需外部编程接口。Zephyr 允许通过 :ref:`west <west-flashing>` 开发和烧录支持 SAM-BA 的开发板，支持有或无 ROM 引导加载程序的设备，也支持 Arduino 和 Adafruit 扩展。完整支持从 Zephyr SDK 0.12.0 引入。

典型烧录命令为：

.. code-block:: console

        west flash [ -r bossac ] [ -p /dev/ttyX ] [ --erase ]

.. note::

    默认情况下，bossac 仅擦除包含待烧录应用的闪存页，保留其他页。如需烧录时擦除目标的整个闪存，请传入 ``--erase``。

设备烧录配置：

.. tabs::

    .. tab:: 带 ROM 引导加载程序

        此类设备不需要特殊配置。构建应用后，运行 ``west flash`` 即可烧录。

    .. tab:: 不带 ROM 引导加载程序

        对于此类设备，用户应：

        1. 定义容纳引导加载程序和应用映像所需的闪存分区，详情见 :ref:`flash_map_api`。
        2. 在开发板 :file:`.defconfig` 中将 :kconfig:option:`CONFIG_USE_DT_CODE_PARTITION` 设为 ``y``，告知构建系统使用这些分区进行代码重定位。也可以在 ``prj.conf`` 或其他 Kconfig 片段中设置。
        3. 构建 SAM-BA 引导加载程序并烧录到设备。

    .. tab:: 带兼容 SAM-BA 引导加载程序

        对于此类设备，用户应：

        1. 定义容纳引导加载程序和应用映像所需的闪存分区，详情见 :ref:`flash_map_api`。
        2. 在开发板 :file:`.defconfig` 中将 :kconfig:option:`CONFIG_BOOTLOADER_BOSSA` 设为 ``y``。这会自动选择 :kconfig:option:`CONFIG_USE_DT_CODE_PARTITION`，使构建系统使用这些分区进行代码重定位。还应在 :file:`.defconfig` 中将 :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_ARDUINO`、:kconfig:option:`CONFIG_BOOTLOADER_BOSSA_ADAFRUIT_UF2` 或 :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_LEGACY` 设为 ``y``，选择正确的兼容 SAM-BA 模式。这些选项也可在 ``prj.conf`` 或其他 Kconfig 片段中设置。
        3. 构建 SAM-BA 引导加载程序并烧录到设备。

.. note::

    :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_LEGACY` 只应作为最后手段，应先尝试“不带 ROM 引导加载程序”的配置方式。


典型闪存布局与配置
------------------

对于驻留闪存的引导加载程序，必须提供设备树分区布局。对于带 ROM 引导加载程序的设备，如果应用使用存储分区或其他非应用分区，也必须提供布局。此时应省略启动分区，并让 code_partition 从偏移 0 开始。分区大小必须始终保证互不重叠。

不带 ROM 引导加载程序的设备，其典型闪存布局为：

.. code-block:: devicetree

        / {
                chosen {
                        zephyr,code-partition = &code_partition;
                };
        };

        &flash0 {
                partitions {
                        compatible = "fixed-partitions";
                        #address-cells = <1>;
                        #size-cells = <1>;

                        boot_partition: partition@0 {
                                label = "sam-ba";
                                reg = <0x00000000 0x2000>;
                                read-only;
                        };

                        code_partition: partition@2000 {
                                label = "code";
                                reg = <0x2000 0x3a000>;
                                read-only;
                        };

                        /*
                        * The final 16 KiB is reserved for the application.
                        * Storage partition will be used by FCB/LittleFS/NVS
                        * if enabled.
                        */
                        storage_partition: partition@3c000 {
                                label = "storage";
                                reg = <0x0003c000 0x00004000>;
                        };
                };
        };

带 ROM 引导加载程序和存储分区的设备，其典型闪存布局为：

.. code-block:: devicetree

        / {
                chosen {
                        zephyr,code-partition = &code_partition;
                };
        };

        &flash0 {
                partitions {
                        compatible = "fixed-partitions";
                        #address-cells = <1>;
                        #size-cells = <1>;

                        code_partition: partition@0 {
                                label = "code";
                                reg = <0x0 0xF0000>;
                                read-only;
                        };

                        /*
                        * The final 64 KiB is reserved for the application.
                        * Storage partition will be used by FCB/LittleFS/NVS
                        * if enabled.
                        */
                        storage_partition: partition@F0000 {
                                label = "storage";
                                reg = <0x000F0000 0x00100000>;
                        };
                };
        };


启用 SAM-BA 运行器
------------------

为让 west 使用 SAM-BA 引导加载程序，:file:`board.cmake` 中必须包含 ``include(${ZEPHYR_BASE}/boards/common/bossac.board.cmake)``。可以添加多个条目定义多个运行器，``west flash`` 默认选择第一个。其他运行器可通过 runner 选项选择，例如 ``west flash -r bossac``。


更多实现细节见 :ref:`boards` 文档。以下三个开发板文档页面可作为快速参考：

  - :zephyr:board:`sam4e_xpro` （ROM 引导加载程序）
  - :zephyr:board:`adafruit_feather_m0_basic_proto` （Adafruit UF2 引导加载程序）
  - :zephyr:board:`arduino_nano_33_iot` （Arduino 引导加载程序）
  - :zephyr:board:`arduino_nano_33_ble` （旧版 Arduino 引导加载程序）

在原生 Windows 上启用 BOSSAC［实验性］
--------------------------------------

Zephyr SDK 的 bossac 目前仅支持 Linux 和 macOS。Windows 可以使用 `BOSSA official releases`_ 中的版本。按默认选项安装后，必须将 :file:`bossac.exe` 加入 Windows PATH。也可以通过 ``--bossac`` 指定可执行文件，如下所示：

.. code-block:: console

    west flash -r bossac --bossac="C:\Program Files (x86)\BOSSA\bossac.exe" --bossac-port="COMx"

.. note::

   目前不支持 WSL。


.. _linkserver-debug-host-tools:
.. _runner_linkserver:

LinkServer 调试主机工具
***********************

LinkServer 用于启动和管理 NXP 调试探针的 GDB 服务器，也提供命令行目标闪存编程功能。它可与 `NXP MCUXpresso for Visual Studio Code`_、基于 GNU 工具的自定义调试配置配合使用，也可用于持续集成和测试的无界面方案。它支持 NXP 的 MCU-Link、LPC-Link2、基于 LPC11U35 或 OpenSDA 的独立及板载调试探针。

NXP 建议通过 `MCUXpresso Installer`_ 安装 LinkServer，该方式也会安装以下探针所需工具，包括 MCU-Link 和 LPCScrypt。

LinkServer 兼容以下调试探针：

- :ref:`lpclink2-cmsis-onboard-debug-probe`
- :ref:`mcu-link-cmsis-onboard-debug-probe`
- :ref:`opensda-daplink-onboard-debug-probe`

要配合 west 使用 LinkServer，应将安装目录加入 :envvar:`PATH` :ref:`环境变量 <env_vars>`。默认安装路径为：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

         /usr/local/LinkServer

   .. group-tab:: macOS

      .. code-block:: console

         /Applications/LinkServer_<version>

   .. group-tab:: Windows

      .. code-block:: console

         c:\nxp\LinkServer_<version>

支持的 west 命令：

1. flash
#. debug
#. debugserver
#. attach

备注：


1. 可以通过 LinkServer 列出探针：

.. code-block:: console

   LinkServer probes

2. 主机连接多个调试探针时，通过 LinkServer west 运行器的 ``--probe`` 选项传入探针索引。

.. code-block:: console

   west flash --runner=linkserver --probe=3

3. LinkServer 的 west 运行器可通过 --override 覆盖设备专用设置，可以多次使用。格式由 LinkServer 规定，例如：

.. code-block:: console

   west flash --runner=linkserver --override /device/memory/5/flash-driver=MIMXRT500_SFDP_MXIC_OSPI_S.cfx

4. LinkServer 不会在复位处理程序处隐式设置断点。如需从应用起点单步执行，必须手动在 ``main`` 或复位处理程序处设置断点。

.. _jlink-debug-host-tools:
.. _runner_jlink:

J-Link 调试主机工具
*******************

Segger 为 Linux、macOS 和 Windows 提供一套调试主机工具：

- J-Link GDB Server：GDB 远程调试
- J-Link Commander：命令行控制及闪存编程
- RTT Viewer：RTT 终端输入输出
- SystemView：实时事件可视化和记录

这些主机工具兼容以下调试探针：

- :ref:`lpclink2-jlink-onboard-debug-probe`
- :ref:`opensda-jlink-onboard-debug-probe`
- :ref:`mcu-link-jlink-onboard-debug-probe`
- :ref:`jlink-external-debug-probe`
- :ref:`stlink-v21-onboard-debug-probe`

检查 `J-Link Supported Devices`_ 是否列出你的 SoC。

下载安装 `J-Link Software and Documentation Pack`_，获取 J-Link GDB Server、Commander 及相关 USB 设备驱动程序。RTT Viewer 和 SystemView 可单独下载，但并非必需。

注意，J-Link GDB 服务器尚不支持 Zephyr RTOS 感知功能。

.. _openocd-debug-host-tools:
.. _runner_openocd:

OpenOCD 调试主机工具
********************

OpenOCD 是社区开源项目，为多种 SoC 提供 GDB 远程调试和闪存编程支持。Zephyr SDK 包含加入 Zephyr RTOS 感知功能的分支版本；其他下载方式见 `Getting OpenOCD`_，可从官方仓库获取。

这些主机工具兼容以下调试探针：

- :ref:`opensda-daplink-onboard-debug-probe`
- :ref:`jlink-external-debug-probe`
- :ref:`stlink-v21-onboard-debug-probe`

检查 `OpenOCD Supported Devices`_ 是否列出你的 SoC。

.. note:: Linux 上可通过 `Zephyr SDK <https://github.com/zephyrproject-rtos/sdk-ng/releases>`_ 获取 openocd。Windows 用户按以下步骤安装：

   - 从 `OpenOCD Windows`_ 下载 Windows 版本。
   - 将 bin 和 share 目录复制到 ``C:\Program Files\OpenOCD\``。
   - 将 ``C:\Program Files\OpenOCD\bin`` 加入 PATH 环境变量。

.. _pyocd-debug-host-tools:
.. _runner_pyocd:

pyOCD 调试主机工具
******************

pyOCD 是 Arm 的开源项目，为 Arm Cortex-M SoC 提供 GDB 远程调试和闪存编程支持。它通过 PyPI 分发，在完成入门指南的 :ref:`gs_python_deps` 步骤时安装。pyOCD 支持 Zephyr RTOS 感知功能。

这些主机工具兼容以下调试探针：

- :ref:`lpclink2-cmsis-onboard-debug-probe`
- :ref:`mcu-link-cmsis-onboard-debug-probe`
- :ref:`opensda-daplink-onboard-debug-probe`
- :ref:`stlink-v21-onboard-debug-probe`

检查 `pyOCD Supported Devices`_ 是否列出你的 SoC。

.. _lauterbach-trace32-debug-host-tools:
.. _runner_trace32:

Lauterbach TRACE32 调试主机工具
*******************************

`Lauterbach TRACE32`_ 是微处理器开发工具、调试器和实时跟踪器产品系列，支持 Arm Cortex-A/-R/-M、RISC-V、Xtensa 等多种内核架构上的 JTAG、SWD、NEXUS 或 ETM。Zephyr 允许通过 :ref:`west <west-flashing>` 开发和烧录支持 TRACE32 的开发板。

该运行器封装 TRACE32 软件，允许 Zephyr 开发板为不同受支持命令执行自定义启动脚本（Practice Script），也支持从 CMake 传递额外参数。各命令执行哪些操作，由使用此运行器的开发板定义。

安装 Lauterbach TRACE32 软件
----------------------------

从 `Lauterbach TRACE32 download website`_ 下载软件（需要注册），并按照 `Lauterbach TRACE32 Installation Guide`_ 安装。

烧录与调试
----------

将 :ref:`环境变量 <env_vars>` :envvar:`T32_DIR` 设为 TRACE32 系统目录，再按 :ref:`west-build-flash-debug` 运行 ``west flash`` 或 ``west debug``。``debug`` 启动 TRACE32 图形界面用于调试，``flash`` 则隐藏界面并在后台完成操作。

默认情况下，``t32`` 运行器使用 TRACE32 系统目录中的 ``config.t32`` 启动。如需其他配置文件，传入 ``--config CONFIG``，例如：

.. code-block:: console

        west flash --config myconfig.t32

更多选项可通过 ``west flash --context -r t32`` 查看。

Zephyr RTOS 感知
----------------

按照 `Lauterbach TRACE32 Zephyr OS Awareness Manual`_ 启用 Zephyr RTOS 感知功能。

.. _nxp-s32-debug-host-tools:
.. _runner_nxp_s32dbg:

NXP S32 调试探针主机工具
************************

:ref:`nxp-s32-debug-probe` 设计为与 `NXP S32 Design Studio for S32 Platform`_ 配合使用。

下载 NXP S32 Design Studio for S32 Platform（需要注册），按照 `S32 Design Studio for S32 Platform Installation User Guide`_ 安装所需调试主机工具及 USB 设备驱动程序。

注意，NXP S32 GDB 服务器是否支持 Zephyr RTOS 感知取决于目标设备，详情见产品发行说明。

支持的 west 命令：

1. debug
#. debugserver
#. attach

基本用法
--------

开始前，将 NXP S32 Design Studio 安装目录加入系统 :ref:`PATH 环境变量 <env_vars>`。也可每次调用运行器时通过 ``--s32ds-path`` 指定，如下所示：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

         west debug --s32ds-path=/opt/NXP/S32DS.3.6

   .. group-tab:: Windows

      .. code-block:: console

         west debug --s32ds-path=C:\NXP\S32DS.3.6

如果通过 USB 连接了多个 S32 调试探针，运行器会先在命令行提示用户选择。也可通过 ``--dev-id=<connection-string>`` 指定探针连接字符串，其格式见用户手册。例如，使用序列 ID 为 ``00:04:9f:00:ca:fe`` 的探针：

.. code-block:: console

   west debug --dev-id='s32dbg:00:04:9f:00:ca:fe'

可通过 ``--tool-opt`` 向调试主机工具传递额外选项。执行 ``debug`` 或 ``attach`` 时，仅传给 GDB 客户端；执行 ``debugserver`` 时，则传给 GDB 服务器。例如，将 Zephyr 应用加载到 SRAM 后分离调试会话：

.. code-block:: console

   west debug --tool-opt='--batch'

要求
----

- **S32 Design Studio 版本**：3.6.0 或更新版本。
- **S32DebugProbe OS（固件）**：1.1.0 或更新版本。

S32 Debug Probe OS 升级流程
---------------------------

按照 `S32 Debug Probe User Guide`_ 中 Reprogramming S32 Debug Probe Firmware Images 一章，升级 S32DebugProbe 操作系统。

.. _runner_probe_rs:

probe-rs 调试主机工具
*********************

probe-rs 是用 Rust 编写的开源嵌入式工具包，开箱即支持 CMSIS-DAP、ST-Link、SEGGER J-Link、FTDI 及 ESP32 内置 USB-JTAG 接口等多种探针。

更多设置说明见 `probe-rs Installation`_。

检查 `probe-rs Supported Devices`_ 是否列出你的 SoC。

.. _runner_rfp:

Renesas Flash Programmer（RFP）主机工具
***************************************

Renesas 提供官方编程工具 `Renesas Flash Programmer`_，用于采用 Renesas 标准启动固件的开发板，提供图形界面和命令行版本。

对于配置了 ``rfp`` west 运行器的开发板，可以方便地通过 RFP CLI 烧录 Zephyr。

支持的 west 命令：

1. flash

下载后，如果系统 PATH 中没有 ``rfp-cli``，可以在烧录时指定 ``rfp-cli`` 的位置：

.. code-block:: console

   west flash --rfp-cli ~/Downloads/RFP_CLI_Linux_V31800_x64/linux-x64/rfp-cli

.. _stm32cubeclt-host-tools:
.. _runner_stlink_gdbserver:

STM32CubeCLT 烧录与调试主机工具
*******************************

STMicroelectronics 提供官方一体化工具集 `STM32CubeCLT`_，兼容 Linux®、macOS® 和 Windows®，允许在第三方开发环境中使用其专有工具。

它提供 GDB 调试服务器 *ST-LINK GDB Server*，可通过板载或外接 ST-LINK 探针调试 STM32 开发板上的应用。

它兼容以下调试探针：

- :ref:`stlink-v21-onboard-debug-probe`
- 独立的 `ST-LINK-V2`_、`ST-LINK-V3`_ 和 `STLINK-V3PWR`_ 探针

安装 STM32CubeCLT
-----------------

获取 ST-LINK GDB Server 最简单的方法，是从 STMicroelectronics 网站安装 `STM32CubeCLT`_。需要有效邮箱地址接收下载链接。

Basic usage
-----------

可以通过 ``west attach``、``west debug`` 或 ``west debugserver`` 使用 ST-Link GDB Server 调试 Zephyr 应用。

.. code-block:: console

   west debug --runner stlink_gdbserver

.. note::

   `STM32CubeCLT <STM32CubeProgrammer_>`_ 中附带的 `STM32CubeProgrammer <STM32CubeCLT_>`_ 也可烧录应用。此时应使用专用 :ref:`STM32CubeProgrammer 运行器 <runner_stm32cubeprogrammer>`，而非 ``stlink_gdbserver``，例如：

   .. code-block:: console

      west flash --runner stm32cubeprogrammer

.. _stm32cubeprog-flash-host-tools:
.. _runner_stm32cubeprogrammer:

STM32CubeProgrammer 烧录主机工具
********************************

STMicroelectronics 为 Linux®、macOS® 和 Windows® 提供 STM32 开发板官方编程工具 `STM32CubeProgrammer`_ （STM32CubeProg）。

它提供易用、高效的环境，可通过调试接口（JTAG、SWD）以及引导加载程序接口（UART、USB DFU、I2C、SPI、CAN）读取、写入和验证设备内存。

它支持丰富的编程功能，涵盖 STM32 内部存储器（闪存、RAM、OTP 等）和外部存储器。

还支持选项编程与上传、烧录内容验证，以及通过脚本自动编程。

提供图形界面（GUI）和命令行界面（CLI）版本。

它兼容以下调试探针：

- :ref:`stlink-v21-onboard-debug-probe`
- :ref:`jlink-external-debug-probe`
- 独立的 `ST-LINK-V2`_、`ST-LINK-V3`_ 和 `STLINK-V3PWR`_ 探针

安装 STM32CubeProgrammer
------------------------

获取 `STM32CubeProgrammer`_ 最简单的方法，是从 STMicroelectronics 网站下载。需要有效邮箱地址接收下载链接。

也可安装多操作系统一体化命令行工具集 `STM32CubeCLT`_，其中同时包含它以及 GDB 调试客户端和服务器。

如果已安装 STM32CubeIDE，系统中就已包含 STM32CubeProg。

Basic usage
-----------

Zephyr 当前支持并维护的所有 STM32 开发板，都将 `STM32CubeProgrammer`_ 设为默认 west 运行器。通过 ``west flash`` 即可烧录应用。

.. code-block:: console

   west flash --runner stm32cubeprogrammer

图形界面或命令行的高级用法见 `STM32CubeProgrammer User Manual`_。

.. _runner_xsdb:

XSDB 烧录与调试主机工具
***********************

AMD XSDB（Xilinx Software Command-line Tool for Debug）是用于编程和调试多种 AMD 自适应 SoC 及 FPGA 平台的命令行工具，**不包含** 在 Zephyr SDK 中。请安装 `AMD Vitis`_ 或平台对应的 AMD 工具链发行版，并确保系统 :ref:`PATH <env_vars>` 中存在 ``xsdb``。

选择 ``xsdb`` west 运行器的开发板，通常会在开发板定义旁提供专用的 ``support/xsdb.cfg``。所需启动文件（PDI、比特流、FSBL 等）见开发板文档。

支持的 west 命令包括 ``flash``、``debug`` 和 ``debugserver``。

对于此运行器，``west debug`` 和 ``west debugserver`` 都启动相同的原生 XSDB 交互会话。与基于 GDB 的运行器不同（其 ``debugserver`` 为 IDE 启动远程桩），xsdb 运行器始终直接启动 XSDB，通过开发板 ``xsdb.cfg`` 加载应用，并停留在 XSDB 提示符。

.. code-block:: console

   west flash --runner xsdb

   west debug --runner xsdb

   west debugserver --runner xsdb

.. note::

   这与本章其他专有主机工具的依赖方式相同，例如 :ref:`J-Link <jlink-debug-host-tools>` 或 :ref:`STM32CubeCLT <stm32cubeclt-host-tools>`：Zephyr 通过 west 运行器集成工具，用户负责获取工具链及其许可证。

.. _runner_uf2:

UF2 上传工具
************

uf2 运行器支持通过 UF2（USB Flashing Format）烧录部分开发板。UF2 是便于使用的文件格式，面向 USB 大容量存储设备的拖放编程。

它依赖目标进入特殊引导加载程序模式，以 USB 大容量存储设备形式出现在主机上。在此模式下，将 ``.uf2`` 文件复制到挂载卷即可上传应用映像。

.. code-block:: console

   west flash --runner uf2

如果未自动检测到 UF2 卷，可以通过 ``--device`` 手动指定挂载点：

UF2 格式和相关工具的更多信息，见 `USB Flashing Format (UF2)`_。

.. _runner_rtkprog:

Realtek 替代闪存编程器（rtkprog）
*********************************

``rtkprog`` 是通过 UART 烧录 Realtek Bee 系列 SoC 所需协议的开源实现。

.. code-block:: console

   west flash --runner rtkprog

.. _rtkprog Source Code: https://github.com/a-labs-io/rtkprog
.. _rtkprog Python package: https://pypi.org/p/rtkprog


.. _runner_mpcli:

Realtek Bee 闪存编程器（MPCli）主机工具
***************************************

Realtek 为 Bee 系列提供官方工具 `Realtek Flash Programmer (MPCli)`_，支持 Linux、macOS 和 Windows。MPCli 通过 UART 实现在系统编程（ISP），无需外部编程硬件。多数官方 Bee 系列评估板内置 UART 转 USB 芯片，可直接用于编程和日志。

下载 MPCli 压缩包后解压，选择适合当前操作系统的版本，将 ``mpcli`` 可执行文件所在目录加入系统 :ref:`PATH 环境变量 <env_vars>`。

开始前，确保开发板已进入下载模式，参见 `Realtek Supported Boards`_ 中的开发板文档。

.. code-block:: console

   west flash [--runner mpcli] --port /dev/ttyX


.. _iar-debug-host-tools:
.. _runner_iar:

IAR EW 与 C-Spy 主机工具
************************

IAR 提供 Embedded Workbench 和 CSpyBat 用于调试与烧录。iar 运行器支持 EWARM 10.10 或更新版本。

.. _AMD Vitis:
   https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vitis.html

.. _J-Link Software and Documentation Pack:
   https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack

.. _J-Link Supported Devices:
   https://www.segger.com/downloads/supported-devices.php

.. _Getting OpenOCD:
   https://openocd.org/pages/getting-openocd.html

.. _OpenOCD Supported Devices:
   https://github.com/zephyrproject-rtos/openocd/tree/latest/tcl/target

.. _pyOCD Supported Devices:
   https://github.com/pyocd/pyOCD/tree/main/pyocd/target/builtin

.. _OpenOCD Windows:
    https://gnutoolchains.com/arm-eabi/openocd/

.. _Lauterbach TRACE32:
    https://www.lauterbach.com/

.. _Lauterbach TRACE32 download website:
   https://www.lauterbach.com/download_trace32.html

.. _Lauterbach TRACE32 Installation Guide:
   https://www2.lauterbach.com/pdf/installation.pdf

.. _Lauterbach TRACE32 Zephyr OS Awareness Manual:
        https://www2.lauterbach.com/pdf/rtos_zephyr.pdf

.. _BOSSA official releases:
        https://github.com/shumatech/BOSSA/releases

.. _NXP MCUXpresso for Visual Studio Code:
        https://www.nxp.com/design/software/development-software/mcuxpresso-software-and-tools-/mcuxpresso-for-visual-studio-code:MCUXPRESSO-VSC

.. _MCUXpresso Installer:
        https://mcuxpresso.nxp.com/mcux-vscode/latest/html/MCUXpresso-Installer.html

.. _NXP S32 Design Studio for S32 Platform:
   https://www.nxp.com/design/software/development-software/s32-design-studio-ide/s32-design-studio-for-s32-platform:S32DS-S32PLATFORM

.. _Renesas Flash Programmer:
   https://www.renesas.com/en/software-tool/renesas-flash-programmer-programming-gui

.. _S32 Design Studio for S32 Platform Installation User Guide:
   https://www.nxp.com/webapp/Download?colCode=S32DSIG

.. _S32 Debug Probe User Guide:
   https://www.nxp.com/docs/en/user-guide/S32DBGUG.pdf

.. _probe-rs Installation:
   https://probe.rs/docs/getting-started/installation/

.. _probe-rs Supported Devices:
   https://probe.rs/targets/

.. _STM32CubeCLT:
   https://www.st.com/en/development-tools/stm32cubeclt.html

.. _STM32CubeProgrammer:
   https://www.st.com/en/development-tools/stm32cubeprog.html

.. _STM32CubeProgrammer User Manual:
   https://www.st.com/resource/en/user_manual/um2237-stm32cubeprogrammer-software-description-stmicroelectronics.pdf

.. _ST-LINK-V2:
   https://www.st.com/en/development-tools/st-link-v2.html

.. _ST-LINK-V3:
   https://www.st.com/en/development-tools/stlink-v3set.html

.. _STLINK-V3PWR:
   https://www.st.com/en/development-tools/stlink-v3pwr.html

.. _USB Flashing Format (UF2):
   https://github.com/microsoft/uf2

.. _Realtek Flash Programmer (MPCli):
   https://docs.realmcu.com/tools/mpcli_tool/en/latest/mpcli/text_en/README.html

.. _Realtek Supported Boards:
   https://docs.zephyrproject.org/latest/boards/realtek/index.html
