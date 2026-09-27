.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

..
  See
  https://docs.zephyrproject.org/latest/releases/index.html#migration-guides
  for details of what is supposed to go into this document.

.. _migration_4.5:

Zephyr v4.5.0 迁移指南（工作草案）
##################################

本文档介绍将应用从 Zephyr v4.4.0 迁移到 Zephyr v4.5.0 时需要进行的更改。

其他更改（与应用迁移无直接关系）请参见 :ref:`版本说明 <zephyr_4.5>`。

.. contents::
    :local:
    :depth: 2

通用
****

* 头文件 :file:`include/zephyr/sys_clock.h` 已弃用，并将在未来版本中移除。应改为包含 :file:`include/zephyr/sys/clock.h`。

构建系统
********

* 要求的最低 CMake 版本现为 3.28.0。Ubuntu 24.04 LTS 软件包仓库随附 CMake 3.28.3。使用 Ubuntu 22.04 LTS 等提供较旧 CMake 的发行版的用户，可以从 `Kitware APT repository <https://apt.kitware.com/>`_ 获取较新版本，或使用 ``pip install cmake``。

* 对早于 C17 的 C 标准版本的支持在弃用后已被移除。Kconfig 选项 ``CONFIG_STD_C11``、``CONFIG_STD_C99`` 和 ``CONFIG_STD_C90`` 已被移除。编译 Zephyr 时请使用 C17 或更高版本。

* :kconfig:option:`CONFIG_LEGACY_GENERATED_INCLUDE_PATH` 已弃用并默认禁用，Zephyr 自身文件的包含路径现在必须以 ``zephyr/`` 为前缀。

* CMake 变量 ``SOC_NAME``、``SOC_SERIES``、``SOC_FAMILY`` 和 ``SOC_V2_DIR`` 已弃用，因为它们与现有变量重复，替代变量如下：:kconfig:option:`CONFIG_SOC`、:kconfig:option:`CONFIG_SOC_SERIES`、:kconfig:option:`CONFIG_SOC_FAMILY` 和 ``SOC_FULL_DIR``。

* ``CONFIG_BUILD_NO_GAP_FILL`` 已被移除。间隙填充现在通过 :kconfig:option:`CONFIG_BUILD_OUTPUT_HEX_GAP_FILL` 和 :kconfig:option:`CONFIG_BUILD_OUTPUT_S19_GAP_FILL` 选择性启用，因此直接删除该选项即可。

* :file:`cmake/app/boilerplate.cmake` 已被移除。仍然直接包含它的应用必须改为在其 :file:`CMakeLists.txt` 开头使用 ``find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})``。

* 名为 :file:`<board>_<revision>.conf` 的开发板版本 Kconfig 片段不再被读取。请将它们重命名为 :file:`<board>_<revision>_defconfig`。

* ``zephyr_code_relocate(FILES ...)`` 不再展开通配符模式，遇到通配符时现在会报错。请改用 ``file(GLOB ...)`` 展开模式，并传入生成的文件名。

* 自 Zephyr 3.1 起弃用的 ``ZephyrUnittest`` CMake 包已被移除，``west zephyr-export`` 也不再注册它。请改用 ``find_package(Zephyr COMPONENTS unittest)``，而不要使用 ``find_package(ZephyrUnittest)``。

* ``west spdx --init`` 已弃用，并将在 Zephyr 5.0 中移除。启用 :kconfig:option:`CONFIG_BUILD_OUTPUT_META` 的构建现在会向 CMake 请求 ``west spdx`` 所读取的基于文件的 API 对象模型，因此生成 SBOM 不再需要预先准备构建目录：照常构建，然后运行 ``west spdx`` 即可。

* CMake 的 ``flash``、``debug``、``debugserver``、``attach`` 和 ``rtt`` 目标已被移除。请改用 ``west flash``、``west debug``、``west debugserver``、``west attach`` 和 ``west rtt``。仿真用的 ``run`` 和 ``debugserver`` 目标不受影响。

* ``WEST_DIR`` 构建系统变量不再使用。

* :kconfig:option:`CONFIG_DEPRECATION_TEST` 已弃用，因为可以改用 :kconfig:option:`CONFIG_WARN_DEPRECATED`，只需把带有 ``CONFIG_DEPRECATION_TEST=y`` 的行替换为 ``CONFIG_WARN_DEPRECATED=n`` 即可。

内核
****

* ``_k_neg_eagain`` 已重命名为 ``_errno_neg_egain``，因为 ``errno`` 已从内核迁移到 ``lib/libc/common``。

* :c:func:`k_sem_reset` 不再唤醒等待该信号量的 poll 等待者。poll 等待者会保持挂起，直到信号量可用或 poll 操作超时。依赖 reset 唤醒 poll 等待者的应用必须改用显式的同步机制。

* ``CONFIG_SMP_BOOT_DELAY`` Kconfig 选项已被移除。将次级 CPU 的启动推迟到运行时现在改为在设备树中按 CPU 表达：在 ``/cpus`` 下对应的 ``cpu`` 节点（通常位于开发板 overlay 中）添加 ``zephyr,deferred-start`` 标志，然后像以前一样稍后用 :c:func:`k_smp_cpu_start` 或 :c:func:`k_smp_cpu_resume` 启动该 CPU。与已被移除的选项会跳过所有次级 CPU 不同，现在可以为每个 CPU 单独选择延迟启动。请注意，该标志仅在设备树绑定包含 ``cpu.yaml`` 的 cpu 节点上生效；没有此类绑定的节点无法延迟启动。

* 启用 :kconfig:option:`CONFIG_SCHED_CPU_MASK_PIN_ONLY` 后，调用 :c:func:`k_thread_cpu_mask_clear`、:c:func:`k_thread_cpu_mask_enable_all` 或 :c:func:`k_thread_cpu_mask_disable` 现在会触发断言，而不再静默产生无效状态。在 PIN_ONLY 模式下使用这些函数的应用必须改用 :c:func:`k_thread_cpu_pin`。

* :kconfig:option:`CONFIG_SCHED_CPU_MASK` 不再局限于 :kconfig:option:`CONFIG_SCHED_SIMPLE`。此前选择 ``SCHED_SCALABLE`` 或 ``SCHED_MULTIQ``，并为了 CPU 亲和性而保留 ``SCHED_SIMPLE`` 来绕过该限制的项目，现在可以直接使用其偏好的调度后端。

* :c:func:`k_sleep` 和 :c:func:`k_usleep` 不再是各自独立的系统调用。它们现在是新增的 :c:func:`k_sleep_ticks` 系统调用的内联封装，以便编译器可以折叠或丢弃其中的单位换算。它们的原型、语义和返回值均未改变，并且已从 :file:`include/zephyr/kernel.h` 移至新文件 :file:`include/zephyr/sleep.h`，由 :file:`kernel.h` 包含。调用它们的代码无需修改。树外代码若获取它们的地址，或依赖 ``K_SYSCALL_K_SLEEP`` 或 ``K_SYSCALL_K_USLEEP``，则必须改用 :c:func:`k_sleep_ticks`。请注意，它会把从 ``K_FOREVER`` 的提前唤醒报告为 ``K_TICKS_FOREVER``，而 :c:func:`k_sleep` 会返回 ``-1``。

* ``sys_port_trace_k_thread_sleep_*()``、``sys_port_trace_k_thread_msleep_*()`` 和 ``sys_port_trace_k_thread_usleep_*()`` 钩子被 ``sys_port_trace_k_thread_sleep_ticks_enter()`` 和 ``sys_port_trace_k_thread_sleep_ticks_exit()`` 取代，因为 :c:func:`k_sleep_ticks` 现在是这四者中唯一非内联的实现。退出钩子以 tick 为单位报告剩余睡眠时间，因此若某后端此前以毫秒呈现它，则需要进行换算，例如使用 :c:func:`k_ticks_to_ms_ceil64`。定义了任何已退役钩子的树外跟踪后端必须更新。

* :c:struct:`k_futex` 不再是内核对象，对应的类型 :c:enumerator:`K_OBJ_FUTEX` 已被移除。任何用户可访问的内存都可以用作 futex 地址。futex 操作不再会产生 -EINVAL 错误。

开发板
******

* 在 NXP LPC54xxx 上，``CONFIG_LPC54XXX_SRAM2_CLOCK`` 已被 ``CONFIG_SOC_SERIES_LPC54XXX_SRAM_CLOCKS`` 取代。旧名称在 LPC54114 是该系列中唯一 SoC 时是贴切的，那时 CMSIS 的 ``SystemInit()`` 只启用 SRAM2。而在 LPC546xx 上它会启用 SRAM2 和 SRAM3，因此该选项现在涵盖的 bank 已不止其命名所指的那一个。两者的默认值均为 ``y``。赋给旧符号的配置必须更新，在更新之前会构建失败。

* 在 RP2040 和 RP2350 上，``vreg`` 节点（:dtcompatible:`raspberrypi,core-supply-regulator`）的默认状态现在是 ``disabled`` 而不是 ``okay``。需要使用该稳压器的树外开发板必须在 ``&vreg`` 节点上设置 ``status = "okay"``。

  在 RP2040 上，``regulator-always-on`` 和 ``regulator-allowed-modes = <REGULATOR_RPI_PICO_MODE_NORMAL>`` 属性现在默认在 SoC dtsi 中设置。此前显式设置它们的开发板可以删除这些行。（:github:`114751`）

* 在 RP2350（rpi_pico 系列）上，``hazard3`` 和 ``m33`` cpucluster 限定符已弃用，改用 ``hazard3_0`` 和 ``m33_0``，后者明确将集群标识为 CPU0，并为双核支持铺平道路。树内所有 RP2350 开发板都已迁移到新的限定符（例如从 ``rpi_pico2/rp2350a/m33`` 改为 ``rpi_pico2/rp2350a/m33_0``）。使用裸 ``hazard3``/``m33`` 限定符的树外开发板应重命名其开发板文件、``board.yml`` 的 ``cpucluster:`` 条目以及 Kconfig select 行，改用 ``SOC_RP2350[AB]_HAZARD3_0``/``SOC_RP2350[AB]_M33_0``。``soc.yml`` 中的裸 ``hazard3``/``m33`` 条目以及对应的 ``SOC_RP2350[AB]_HAZARD3``/``_M33`` Kconfig 符号已弃用，两者都将在未来版本中移除。

* Kconfig 选项 :kconfig:option:`CONFIG_SRAM_SIZE` 和 :kconfig:option:`CONFIG_SRAM_BASE_ADDRESS` 已弃用，开发板应改为使用设备树的 ``zephyr.sram`` chosen 节点来指定将要使用的 RAM 节点（这些 Kconfig 值原先由该节点填充）。若手动调整了其中任一选项，就会设置 :kconfig:option:`CONFIG_SRAM_DEPRECATED_KCONFIG_SET`，以表明这一弃用状态。

* Nordic 内部的 SoC 平台 Kconfig 符号 ``NRF_PLATFORM_HALTIUM`` 和 ``NRF_PLATFORM_LUMOS`` 不再被树内代码使用，这些代码现在依赖显式的 :kconfig:option:`CONFIG_SOC_SERIES_NRF54H`、:kconfig:option:`CONFIG_SOC_SERIES_NRF92`、:kconfig:option:`CONFIG_SOC_SERIES_NRF54L` 和 :kconfig:option:`CONFIG_SOC_SERIES_NRF71` 判断。这两个符号都保留为已弃用的桩，当选择对应的 SoC 系列且启用 :kconfig:option:`CONFIG_NRF_PLATFORM_DEPRECATED_SYMBOLS` 时默认值为 ``y``，因此现有的 ``CONFIG_NRF_PLATFORM_*=y`` 行和 ``depends on NRF_PLATFORM_*`` 子句仍可继续构建，只是会出现 Kconfig 弃用警告。使用这些符号的树外 Kconfig、CMake 和代码应更新为：

  * ``CONFIG_NRF_PLATFORM_HALTIUM`` 改用 :kconfig:option:`CONFIG_SOC_SERIES_NRF54H` 或 :kconfig:option:`CONFIG_SOC_SERIES_NRF92`。
  * ``CONFIG_NRF_PLATFORM_LUMOS`` 改用 :kconfig:option:`CONFIG_SOC_SERIES_NRF54L` 或 :kconfig:option:`CONFIG_SOC_SERIES_NRF71`。

* Aesc Silicon 的 ``elemrv`` 开发板已重命名为 ``elemrv_flask_n``。

* Nordic sysbuild 的 Kconfig 选项 ``SB_CONFIG_NRF_HALTIUM_GENERATE_UICR`` 已重命名为 :kconfig:option:`SB_CONFIG_NRF_GENERATE_UICR`。请更新 sysbuild 配置以使用新名称。

* Nordic SoC 头文件 :file:`<haltium_power.h>` 和 :file:`<haltium_pm_s2ram.h>` 已分别重命名为 :file:`<soc_power.h>` 和 :file:`<soc_pm_s2ram.h>`。旧名称下的转发头文件仍然可用，并会发出指向新包含路径的 ``#warning``。包含旧路径的树外代码应更新为：

  * ``#include <haltium_power.h>`` 改为 ``#include <soc_power.h>``。
  * ``#include <haltium_pm_s2ram.h>`` 改为 ``#include <soc_pm_s2ram.h>``。

* 基于 STM32H7RS 的开发板（stm32h7s78_dk 和 nucleo_h7s3l8）的系统时钟已提升到 600 MHz。这是通过将 PLL1 频率提高到 300 MHz 实现的，这也会影响总线和内核时钟，使其频率略有提高。

* :kconfig:option:`CONFIG_GPIO` 在大多数 STM32 开发板上不再默认启用（带 GPIO hogs 的开发板仍保持启用，因为 hogs 需要 GPIO 才能工作）。依赖 ``CONFIG_GPIO=y`` 为默认值的应用需要显式启用该选项。（:github:`109468`）

* 使用 UF2 镜像并迁移到 :dtcompatible:`zephyr,mapped-partition` 的开发板应在其 defconfig 中启用 HEX 输出（:kconfig:option:`CONFIG_BUILD_OUTPUT_HEX`），因为 UF2 镜像生成不能再依赖 :kconfig:option:`CONFIG_FLASH_LOAD_OFFSET` 从 BIN 输出确定代码地址。现在默认由 HEX 生成 UF2（而不是从 BIN 生成）。（:github:`107944`）

* Ezurio 的 bl54l15u_dvk 已被移除。bl54l15_dvk 仍然可用，并支持该模块的 bl54l15 和 bl54l15u 两种变体，功能相同。使用 bl54l15u_dvk 的开发板应视情况迁移到 bl54l15_dvk/nrf54l15/cpuapp 或 bl54l15_dvk/nrf54l15/cpuflpr。

* 开发板 stm32h573i_dk 和 b_u585i_iot02a 的默认 MCUboot 签名类型已从 RSA-3072 改为 EC-P256。这会影响在 TF-M 中启用 MCUboot 的构建（:kconfig:option:`CONFIG_TFM_BL2`）。如果希望继续使用 RSA-3072，需要将 :kconfig:option:`CONFIG_TFM_MCUBOOT_SIGNATURE_TYPE` 设为 ``"RSA-3072"``。否则，请确保拥有正在使用的签名类型的签名密钥。

* modules/hal_silabs/gecko 下的所有 Kconfig 已从 ``SOC_GECKO_*`` 重命名为 ``SILABS_GECKO_*``。请相应地调整你的开发板。

* 所有 Silabs 系列 0 和系列 1 开发板的时钟配置现在需要在设备树中指定。Kconfig ``CONFIG_SOC_GECKO_HAS_HFRCO_FREQRANGE`` 和 ``CONFIG_CMU_*`` 已被移除。有关如何调整开发板的示例，请参见 :github:`111754`。

* 在 nRF54LM20 DK 上，``nrf7002eb2`` shield（及其 ``nrf7002eb2_nrf7001`` 和 ``nrf7002eb2_nrf7000`` 变体）不再重定向应用的控制台。此前它会禁用 UART20，并把控制台（shell、mcumgr 和蓝牙监视器）改接到 UART30，以规避仅存在于试产套件、而非量产 nRF54LM20 DK 上的引脚冲突。现在控制台保留在 UART20（VCOM1）上，与开发板的标准行为一致，且不再删除 ``button3``/``sw3``。在 nRF54LM20 DK 上使用该 shield 的现有用户必须把串口终端从 VCOM0 移回 VCOM1。nRF54L15 DK 不受影响：其扩展排针确实与 UART20 冲突，因此仍将控制台改接到 UART30。

* mimxrt1180_evk 的 Kconfig 选项 ``NXP_BOARD_SPECIFIC_MPU_SETTINGS`` 已重命名为 :kconfig:option:`CONFIG_BOARD_NXP_SPECIFIC_MPU_SETTINGS`，与其他 NXP 开发板选项以及 frdm_imxrt1186 使用的 ``BOARD_NXP_*`` 命名保持一致。设置 ``CONFIG_NXP_BOARD_SPECIFIC_MPU_SETTINGS`` 的配置必须更新为新名称。

* 如果开发板支持通过 TF-M 进行固件更新，现在必须选择 :kconfig:option:`CONFIG_TFM_PARTITION_FIRMWARE_UPDATE_SUPPORTED`。

* :kconfig:option:`CONFIG_SPI_STM32_INTERRUPT` 的默认启用已从原先这样做的 STM32 开发板中移除。选择中断驱动还是轮询式 SPI 传输是应用层面的问题，而非开发板层面的问题。在受影响的开发板上依赖中断驱动 SPI（例如在没有 DMA 的情况下使用 :c:func:`spi_transceive_signal` 或 :c:func:`spi_transceive_cb`）的应用，现在必须在其自身配置中显式启用 :kconfig:option:`CONFIG_SPI_STM32_INTERRUPT`。（:github:`116218`）

* 以下开发板名称别名在 v4.3 或更早版本中已弃用，现已被移除（:github:`116657`、:github:`116750`）。请改为针对该别名原先重定向到的开发板 target 进行构建：

  * ``arduino_uno_r4_minima`` → ``arduino_uno_r4@minima``
  * ``arduino_uno_r4_wifi`` → ``arduino_uno_r4@wifi``
  * ``esp32c6_devkitc`` → ``esp32c6_devkitc/esp32c6/hpcore``
  * ``esp32_devkitc_wroom/esp32/procpu`` 和 ``esp32_devkitc_wrover/esp32/procpu`` → ``esp32_devkitc/esp32/procpu``
  * ``esp32_devkitc_wroom/esp32/appcpu`` 和 ``esp32_devkitc_wrover/esp32/appcpu`` → ``esp32_devkitc/esp32/appcpu``
  * ``neorv32`` → ``neorv32/neorv32/up5kdemo``
  * ``panb511evb`` → ``panb611evb``
  * ``raytac_an54l15q_db/nrf54l15/cpuapp`` → ``raytac_an54lq_db_15/nrf54l15/cpuapp``
  * ``scobc_module1`` → ``scobc_a1``
  * ``xiao_esp32c6`` → ``xiao_esp32c6/esp32c6/hpcore``

* Nordic nRF52 的 Kconfig 选项 ``CONFIG_GPIO_AS_PINRESET`` 已移除。请改为在 ``&uicr`` 设备树节点上设置 ``gpio-as-nreset`` 属性。

* Nordic 的 Kconfig 选项 ``CONFIG_SOC_DCDC_NRF52X``、``CONFIG_SOC_DCDC_NRF52X_HV``、``CONFIG_SOC_DCDC_NRF53X_APP``、``CONFIG_SOC_DCDC_NRF53X_NET`` 和 ``CONFIG_SOC_DCDC_NRF53X_HV`` 已移除。请改为在设备树中配置稳压器：在 ``&reg1``/``&vregmain``/ ``&vregradio`` 上设置 ``regulator-initial-mode = <NRF5X_REG_MODE_DCDC>``，并在 ``&reg0``/``&vregh`` 上设置 ``status = "okay"``。

* Nordic nRF53 的 Kconfig 选项 ``CONFIG_BOARD_ENABLE_CPUNET`` 已移除。请改用 :kconfig:option:`CONFIG_SOC_NRF53_CPUNET_ENABLE`。

* ``esp_threadbr_ethernet`` 扩展板已移除。现有用户应改为针对 ``esp_threadbr/esp32s3/procpu/ethernet`` 构建，而不是将 ``esp_threadbr/esp32s3/procpu`` 与 ``SHIELD=esp_threadbr_ethernet`` 组合使用。除该扩展板外，``esp_threadbr`` 子板连接器描述也已移除，因此 ``espressif,esp-threadbr-header`` 绑定、``esp_threadbr_header`` GPIO nexus 节点以及 ``esp_threadbr_spi`` 和 ``esp_threadbr_i2c`` 设备树标签均不复存在。使用它们的树外 overlay 必须直接引用 SoC 节点（``&spi2``、``&i2c0``、``&gpio0``、``&gpio1``）。（:github:`116956`）

* STM32MP15 Cortex-M4 SoC 的 Kconfig 符号 ``SOC_STM32MP15_M4`` 已重命名为 :kconfig:option:`CONFIG_SOC_STM32MP157CXX_M4`。选择了 ``SOC_STM32MP15_M4`` 的树外 STM32MP15 开发板必须改为选择 :kconfig:option:`CONFIG_SOC_STM32MP157CXX_M4`。（:github:`118151`）

* 在 Arduino UNO R4 WiFi 上， ``zephyr,console`` 和 ``zephyr,shell-uart`` 现在默认使用 SCI9，由板载 ESP32-S3 桥接到 USB-C 连接器并作为 USB CDC ACM 端口，而不再是 D0/D1 排针上的 SCI2。控制台输出现在可以在烧录开发板所用的同一端口上看到，无需外部 USB 转串口适配器。依赖控制台位于 D0/D1 的应用可以在应用 overlay 中重新选择它：

  .. code-block:: devicetree

     / {
         chosen {
             zephyr,console = &uart2;
             zephyr,shell-uart = &uart2;
         };
     };

  Arduino UNO R4 Minima 不受影响。（:github:`118433`）

* Espressif 按模块划分的设备树 include 文件及其 SoC Kconfig 符号已移除。模块或 SIP 料号描述的是开发板所搭载的 flash 和 PSRAM 容量，这属于开发板而非 SoC 的属性，因此两者现在都由开发板自身声明。

  每个 ``espressif/<soc>/<soc>_<module>.dtsi`` 文件都被替换为每个 SoC 一个 ``espressif/<soc>/<soc>.dtsi``。相应的隐藏 Kconfig 符号（例如 ``SOC_ESP32S3_WROOM_N8`` 和 ``SOC_ESP32_WROVER_E_N16R8``）被替换为普通的 SoC 符号，例如 :kconfig:option:`CONFIG_SOC_ESP32S3`。``SOC_PART_NUMBER`` 现在报告的是 SoC，而不是模块。

  树外的 Espressif 开发板必须更新，在完成更新之前将无法构建：

  * 改为包含普通的 SoC dtsi，而不是模块的 dtsi。
  * 在 ``Kconfig.<board>`` 中选择普通的 SoC 符号。
  * 在开发板 dts 中描述 flash，同时给出 ``reg`` 和匹配的 ``ranges``，因为 SoC 的 dtsi 不再设置这两者。

    .. code-block:: devicetree

       &flash0 {
           reg = <0x0 DT_SIZE_M(8)>;
           ranges = <0x0 0x0 DT_SIZE_M(8)>;
       };

  * 对于带有 PSRAM 的开发板，以相同的方式描述 PSRAM：

    .. code-block:: devicetree

       &psram0 {
           size = <DT_SIZE_M(2)>;
       };

  在双核 ESP32 上， ``espressif/esp32/esp32_appcpu.dtsi`` 也不再设置 flash，因此 APPCPU 开发板 dts 必须声明与其 PROCPU 对应板相同的 flash。

* 在 NXP S32K148 上，ENET 节点 ``enet`` （:dtcompatible:`nxp,enet`）、``enet_mac`` （:dtcompatible:`nxp,enet-mac`）、``enet_mdio`` （:dtcompatible:`nxp,enet-mdio`）和 ``enet_ptp_clock`` （:dtcompatible:`nxp,enet-ptp-clock`）现在默认是 ``disabled`` 而不是 ``okay``。使用以太网的树外开发板必须在这些节点上设置 ``status = "okay"``。

* Silabs 的 Kconfig 选项 ``CONFIG_SOC_SILABS_IMAGE_PROPERTIES`` 已重命名为 :kconfig:option:`CONFIG_SOC_VENDOR_SILABS_IMAGE_PROPERTIES`。

* Silabs 的 Kconfig 选项 ``CONFIG_SOC_SILABS_PM_LOW_INTERRUPT_LATENCY`` 已重命名为 :kconfig:option:`CONFIG_SOC_VENDOR_SILABS_PM_LOW_INTERRUPT_LATENCY`。

* stm32h573i_dk 和 stm32h5f5j_dk disco 套件现在采用 mspi 控制器模型。这是向 mspi stm32 支持迁移的下一步。对于这两款开发板，请将 xspi 节点声明为 ``st,stm32-xspi-controller`` 兼容。待所有目标开发板都完成更改后，将更新 stm32h5 设备 DTS。

设备驱动与设备树
****************

.. Only place contents common to all device drivers here. Contents specific to one driver subsystem
   goes into its own subsection, below.

* :c:macro:`DEVICE_API` 宏现在对于声明任何上游驱动类的设备驱动 API 实例都是必需的，包括树外驱动。:c:macro:`DEVICE_API_GET` 现在会断言该 API 属于所请求的类，这要求该实例位于该类的可迭代段中。将上游 API 作为首个成员嵌入的树外驱动类，还必须通过 :c:macro:`DEVICE_API_EXTENDS` 声明这种关系，这样对父类的 :c:macro:`DEVICE_API_GET` 才能在实现子类 API 的设备上成功。详见 :ref:`device_driver_api`。

.. Group contents in this section by subsystem, e.g.:
..
.. ADC
.. ===
..
.. ...

.. zephyr-keep-sorted-start re(^\w) ignorecase

ADC
===

* :dtcompatible:`microchip,xec-adc` 的 ``girqs`` 和 ``pcrs`` 属性（数组类型）已被替换为编码后的 ``girqs`` （使用 ``MCHP_XEC_ECIA_GIRQ_ENC`` 宏）和 ``pcr-scr`` （int 类型），分别表示编码后的 PCR 寄存器索引和位位置（:github:`105658`）。

* :kconfig:option:`CONFIG_LPADC_DO_OFFSET_CALIBRATION` 选项现在仅在启用 :kconfig:option:`CONFIG_ADC_MCUX_LPADC` 时才有意义，其 ``default y`` 现在也限定在该条件下。树内开发板不再在 defconfig 中显式启用它，因为默认值已经覆盖了这些开发板。

* ``CONFIG_LPADC_CHANNEL_COUNT`` Kconfig 选项已移除。NXP LPADC 驱动现在将硬件命令槽视为逻辑 ADC 通道，并根据设备树中为该实例声明的 ``channel`` 子节点推导每个实例的逻辑通道数，因此未使用的命令槽不再占用 RAM。为节省 RAM 而调低该 Kconfig 选项的应用只需将其删除。未声明 ``channel`` 节点的实例会保留全部硬件容量，因此仅在运行时通过 :c:func:`adc_channel_setup` 配置通道的应用不受影响；两者混用的应用必须在设备树中声明其在运行时设置的通道标识符中的最大值。声明超出 SoC 所实现 ``CMD`` 寄存器数量的通道标识符现在会导致构建错误，而不再是运行时 HAL 断言；:c:func:`adc_read` 现在会以 ``-EINVAL`` 拒绝空通道掩码或选择了超出该限制的通道的掩码，而不是静默忽略（:github:`116995`）。

Analog Devices
==============

* :kconfig:option:`CONFIG_NUM_IRQS` 现在会根据设备树，基于处于活动状态（``status = "okay";``）的设备，使用 ``dt_highest_controller_irq_number`` Kconfig 预处理函数为所有 MAX32 SoC 自动计算。原先按 SoC 硬编码的值已移除，生成的 IRQ 表通常比之前小得多。使用 :c:macro:`IRQ_CONNECT()` 注册自定义 ISR 的应用可能因为 :kconfig:option:`CONFIG_NUM_IRQS` 取值偏小，而遇到如下所示的构建失败：

  .. code-block::

    gen_isr_tables.py: error: IRQ 88 (offset=0) exceeds the maximum of 54

  请显式将 :kconfig:option:`CONFIG_NUM_IRQS` 设置为合适的值来解决这些问题。（:ref:`以下文档页面 <setting_configuration_values>` 说明了具体做法）

  使用 :c:func:`irq_connect_dynamic` 在运行时安装 ISR 的应用不在该构建时检查范围内，必须人工审查。

DMA
===

* :dtcompatible:`silabs,siwx91x-dma` 已重命名为 :dtcompatible:`silabs,udma`。Kconfig 选项也已重命名以与新名称保持一致（``DMA_SILABS_SIWX91X`` 改为 ``DMA_SILABS_SIWX91X_UDMA``，``DMA_SILABS_SIWX91X_SG_BUFFER_COUNT`` 改为 ``DMA_SILABS_SIWX91X_UDMA_DESCR_COUNT``）

* 为与其他驱动保持一致，``GPDMA_SILABS_SIWX91X_DESCRIPTOR_COUNT`` 已重命名为 ``DMA_SILABS_SIWX91X_GPDMA_DESCR_COUNT``。

ESPI
====

* ECUSTOM_HOST_SUBS_INTERRUPT_EN 已弃用，取而代之的新 API 可以细粒度地启用或禁用各个 eSPI 硬件中断。新 API 取代了当前全有或全无的方式，后者与 CONFIG_ESPI_PERIPHERAL_CUSTOM_OPCODE 紧密耦合，并要求所有 eSPI 驱动中只存在单个 eSPI ACPI 硬件块实例。该选项将在下一个 Zephyr 版本中完全移除，以便留出迁移时间。

* Microchip XEC eSPI v2 驱动（:dtcompatible:`microchip,xec-espi-v2`）已从 MEC172x 移植，以同时支持 MEC174x、MEC175x 和 MEC165xB。这带来了若干设备树改动，会影响使用该绑定的树外开发板（:github:`109519`）：

  * ``pcrs`` 属性已由 ``pcr-scr`` 取代，后者现在是使用 ``MCHP_XEC_SCR_ENCODE(reg, bit)`` 辅助宏编码的单个整数，而不再是 ``<reg bit>`` 单元对。请将现有 overlay 中的 ``pcrs = <2 19>;`` 更新为 ``pcr-scr = <MCHP_XEC_SCR_ENCODE(2, 19)>;``。

  * 仅在 MEC174x/5x/165xB 上，``girqs`` 单元现在是由 ``MCHP_XEC_ECIA_GIRQ_ENC(reg, bit)`` 生成的每个条目一个整数，而不再是 ``<reg bit>`` 对。MEC172x 继续使用现有的 ``MCHP_XEC_ECIA(...)`` 形式。

  * 对于地址空间超过 32 位的主机，eSPI 控制器节点上新增了两个可选属性：``host-memmap-addr-high``，即内存映射逻辑设备的主机地址位 [47:32]；以及 ``sram-bar-addr-high``，即两个 SRAM BAR 的主机地址位 [47:32]。

  * 为保持一致性，eSPI 控制器及其主机设备子节点的 ``interrupt-names`` 已重命名。请相应更新 overlay：

    * 控制器：``rst`` → ``erst``；``vwct_0_6`` / ``vwct_7_10`` → ``ht_vw_bank0`` / ``ht_vw_bank1``。还必须向 ``interrupts`` 数组中添加两个对应的中断（``ht_vw_bank0`` / ``ht_vw_bank1``）。
    * KBC 子节点：``kbc_obe`` / ``kbc_ibf`` → ``obe`` / ``ibf``。
    * ACPI EC 子节点：``acpi_ibf`` / ``acpi_obe`` → ``ibf`` / ``obe``。

  * 在 MEC5 SoC DTSI（MEC174x/5x/165xB）中，eSPI 控制器的每个主机设备子节点（mailbox、KBC、ACPI EC、ACPI PM1、port92、glue、EMI、BIOS 调试端口等）现在都必须声明 :dtcompatible:`microchip,xec-espi-host-dev` 所要求的 ``ldn`` 属性（逻辑设备编号）。覆盖或新增这些 SoC 主机设备子节点的树外开发板必须在每个节点上设置 ``ldn``。

Flash
=====
* :dtcompatible:`jedec,spi-nand` 现在要求提供 ``plane-bytes`` 属性，用于指示 flash 设备中每个 plane 的大小。对于只有一个 plane 的设备，应将其设置为与 ``size-bytes`` 相同的值。

* :dtcompatible:`st,stm32-nv-flash` 的 ``bank2-flash-size`` 属性已弃用，改为使用 ``reg`` 大小单元确定 flash bank 的大小。除了移除上述属性外，无需对设备树做其他改动。（:github:`114971`）

GPIO
====

* STM32 GPIO 驱动现在在尝试通过 :c:func:`gpio_pin_configure` 将处于禁用状态的 GPIO 引脚配置为上拉/下拉电阻时会返回 ``-EINVAL``。以前驱动会返回 ``0``，但并不会真正执行这些标志（未启用上拉/下拉电阻）。遇到此错误的应用应从传给 :c:func:`gpio_pin_configure` 的 ``flags`` 中移除 :c:macro:`GPIO_PULL_UP`/ :c:macro:`GPIO_PULL_DOWN`；由于这些标志实际上被忽略，这样做将与之前的行为相同。（:github:`104690`）

* 在 STM32F1 系列上，GPIO 输出引脚现在使用最高 50 MHz 的速度，而不是 10 MHz。（:github:`104690`）

* :dtcompatible:`awinic,aw9523b-gpio` 驱动不再有 ``reset-gpios`` 属性。该属性已改为移到父级 :dtcompatible:`awinic,aw9523b` MFD 设备上。

I2C
===

* 在基于 :kconfig:option:`CONFIG_I2C_DW` 的控制器上，``CONFIG_I2C_DW_RW_TIMEOUT_MS`` 选项已替换为 :kconfig:option:`CONFIG_I2C_TRANSFER_TIMEOUT_MS`，默认值为 500ms。

* ITE I2C 控制器 :dtcompatible:`ite,enhance-i2c`、:dtcompatible:`ite,it51xxx-i2c`、:dtcompatible:`ite,it8xxx2-i2c` 的传输超时现在使用通用的 ``zephyr,transfer-timeout-ms`` 属性，而不再使用 ``transfer-timeout-ms``，默认值为 500ms。

* :dtcompatible:`nxp,sc18im704-i2c` 桥不再向 SC18IM704 发送未移位的目标地址。Zephyr I2C API 会将 7 位地址传给控制器的 ``transfer()`` 回调，而驱动现在会将其左移一位，以构造桥所期望的地址字节。位于 :dtcompatible:`nxp,sc18im704-i2c` 总线上的设备树节点，如果之前通过声明预先移位的 ``reg`` 来补偿缺少的移位（例如地址为 ``0x50`` 的设备使用 ``reg = <0xa0>``），现在必须声明真实的 7 位地址（``reg = <0x50>``）。

I2S
===

* :c:func:`i2s_buf_write` 现在在分配发送块时会遵循流配置中的 ``timeout``。以前它会无限等待，因此文档中所述的 ``-EAGAIN`` 返回值无法到达，多线程构建中的 ``-ENOMEM`` 也是如此。依赖无限等待的调用方可以将 ``timeout`` 设为 ``SYS_FOREVER_MS``，但同一字段也会限制驱动的入队等待时间，因此没有任何一个取值能重现旧有的“无限分配 + 有界入队”组合。

IEEE 802.15.4
=============

* 自 Zephyr 3.6 起弃用的 ``IEEE802154_HW_SLEEP_TO_TX`` 无线电能力已被移除，位于其上的能力比特位也已重新编号。所有树内驱动都支持直接从低功耗状态发送，因此该能力不携带任何信息；OpenThread 平台现在始终通告 ``OT_RADIO_CAPS_SLEEP_TO_TX``，并允许从睡眠状态发送。通告该能力的树外驱动只需将其删除即可。

MSPI
====

* MSPI 设备绑定文件名现在对 MSPI 专用变体使用 ``(vendor,)device-mspi.yaml``，而设备树 ``compatible`` 字符串描述设备本身，不再编码 MSPI 总线。建议开发板、扩展板、示例、测试和树外设备树 overlay 按如下方式更新 MSPI 子节点兼容字符串：

  * ``jedec,mspi-nor`` -> ``jedec,nor``
  * ``mspi-atxp032`` -> ``atxp032``
  * ``mspi-is25xX0xx`` -> ``is25xX0xx``
  * ``mspi-aps6404l`` -> ``aps6404l``
  * ``mspi-aps-z8`` -> ``aps-z8``
  * ``zephyr,mspi-emul-device`` -> ``zephyr,emul-device-mspi``
  * ``zephyr,mspi-emul-flash`` -> ``zephyr,emul-flash``

  建议树外 MSPI 设备驱动同样将 ``DT_DRV_COMPAT`` 和生成的设备树 Kconfig 符号引用更新为新的兼容字符串名称。如果驱动、示例或测试必须确保某个通用兼容字符串实例化在 MSPI 总线上，请添加显式的 MSPI 总线检查，例如 Kconfig 中的 ``dt_compat_on_bus``，或测试元数据中的 ``dt_compat_on_bus`` 过滤器。

* MSPI 内存映射特性已从“XIP”重命名为“MEMMAP”，因为 XIP（:kconfig:option:`CONFIG_XIP`）在 Zephyr 中是软件配置概念，而 MSPI 特性只是对设备进行内存映射，既可用于代码执行，也可用于数据访问（:github:`104657`）。MSPI API 是实验性的，因此不提供弃用别名。树外用户必须更新：

  * ``CONFIG_MSPI_XIP`` -> :kconfig:option:`CONFIG_MSPI_MEMMAP`
  * ``CONFIG_FLASH_MSPI_XIP_READ`` -> :kconfig:option:`CONFIG_FLASH_MSPI_MEMMAP_READ`
  * ``struct mspi_xip_cfg`` -> ``struct mspi_memmap_cfg``
  * ``enum mspi_xip_permit`` -> ``enum mspi_memmap_permit``，其取值 ``MSPI_XIP_READ_WRITE``/``MSPI_XIP_READ_ONLY`` -> ``MSPI_MEMMAP_READ_WRITE``/``MSPI_MEMMAP_READ_ONLY``
  * ``mspi_xip_config`` -> :c:func:`mspi_memmap_config`，驱动 API 条目 ``xip_config`` -> ``memmap_config``
  * ``MSPI_XIP_CONFIG_DT``/``MSPI_XIP_CONFIG_DT_INST``/``MSPI_XIP_CONFIG_DT_NO_CHECK``
    -> ``MSPI_MEMMAP_CONFIG_DT``/``MSPI_MEMMAP_CONFIG_DT_INST``/``MSPI_MEMMAP_CONFIG_DT_NO_CHECK``
  * ``MSPI_XIP_CFG_STRUCT_DECLARE``/``MSPI_XIP_BASE_ADDR_DECLARE``/``MSPI_XIP_BASE_ADDR_INIT``
    -> ``MSPI_MEMMAP_CFG_STRUCT_DECLARE``/``MSPI_MEMMAP_BASE_ADDR_DECLARE``/``MSPI_MEMMAP_BASE_ADDR_INIT``
  * MSPI 设备节点上的设备树属性 ``xip-config`` -> ``memmap-config``

Nordic
======

* :dtcompatible:`nordic,owned-memory` 和 :dtcompatible:`nordic,owned-partitions` 的 ``owner-id``、``perm-read``、``perm-write``、``perm-execute``、``perm-secure`` 和 ``non-secure-callable`` 属性已被移除。请改用 ``nordic,access``，例如 ``<NRF_OWNER_ID_APPLICATION NRF_PERM_RW>``。所有者不再隐式确定：省略 ``owner-id`` 过去表示正在编译的域，因此现在必须显式指定。

NXP
===

* :kconfig:option:`CONFIG_MCUX_LPTMR_TIMER` 不再因 ``/chosen/zephyr,system-timer`` chosen 节点与 :dtcompatible:`nxp,lptmr` 兼容而默认为 ``y``。依赖 LPTMR 作为系统定时器的树外 SoC 和开发板现在必须在其 ``Kconfig.defconfig`` 中显式设置该符号的默认值（例如 ``default y if PM``）。

* 启用 :kconfig:option:`CONFIG_PM` 时，Kinetis KE1xF 不再需要开发板 overlay 来指定系统定时器。SoC DTSI 现在设置了 ``zephyr,system-timer`` chosen 属性，因此按照 Zephyr 4.4 迁移指南添加了该 overlay 的开发板可以将其移除。

* NXP LPC DTSI 文件已从扁平目录 ``dts/arm/nxp/lpc/`` 重组为按系列划分的子目录。直接包含这些文件的树外开发板必须更新其包含路径。

  新的子目录布局如下：

  +--------------------------+------------------------------------------+
  | LPC 系列                 | 新位置                                   |
  +==========================+==========================================+
  | LPC11U6x                 | ``dts/arm/nxp/lpc/lpc11u6x/``            |
  +--------------------------+------------------------------------------+
  | LPC51U68                 | ``dts/arm/nxp/lpc/lpc51u68/``            |
  +--------------------------+------------------------------------------+
  | LPC54xxx                 | ``dts/arm/nxp/lpc/lpc54xxx/``            |
  +--------------------------+------------------------------------------+
  | LPC55xxx                 | ``dts/arm/nxp/lpc/lpc55xxx/``            |
  +--------------------------+------------------------------------------+
  | LPC84x                   | ``dts/arm/nxp/lpc/lpc84x/``              |
  +--------------------------+------------------------------------------+

  示例：

  .. code-block:: dts

    /* Before */
    #include <nxp/lpc/nxp_lpc55S6x.dtsi>

    /* After */
    #include <nxp/lpc/lpc55xxx/nxp_lpc55S6x.dtsi>

* NXP Kinetis DTSI 文件已从扁平目录 ``dts/arm/nxp/kinetis/`` 重组为按系列划分的子目录。直接包含这些文件的树外开发板必须更新其包含路径。

  新的子目录布局如下：

  +--------------------------+------------------------------------------+
  | Kinetis 系列             | 新位置                                   |
  +==========================+==========================================+
  | K2X                      | ``dts/arm/nxp/kinetis/k2x/``             |
  +--------------------------+------------------------------------------+
  | K32Lx                    | ``dts/arm/nxp/kinetis/k32lx/``           |
  +--------------------------+------------------------------------------+
  | K6X                      | ``dts/arm/nxp/kinetis/k6x/``             |
  +--------------------------+------------------------------------------+
  | K8X                      | ``dts/arm/nxp/kinetis/k8x/``             |
  +--------------------------+------------------------------------------+
  | KE1xF                    | ``dts/arm/nxp/kinetis/ke1xf/``           |
  +--------------------------+------------------------------------------+
  | KE1xZ                    | ``dts/arm/nxp/kinetis/ke1xz/``           |
  +--------------------------+------------------------------------------+
  | KL2X                     | ``dts/arm/nxp/kinetis/kl2x/``            |
  +--------------------------+------------------------------------------+
  | KV5X                     | ``dts/arm/nxp/kinetis/kv5x/``            |
  +--------------------------+------------------------------------------+
  | KWX                      | ``dts/arm/nxp/kinetis/kwx/``             |
  +--------------------------+------------------------------------------+

  示例：

  .. code-block:: dts

    /* Before */
    #include <nxp/kinetis/nxp_k66.dtsi>

    /* After */
    #include <nxp/kinetis/k6x/nxp_k66.dtsi>

* NXP MCX DTSI 文件已从扁平目录 ``dts/arm/nxp/mcx/`` 重组为按系列划分的子目录。直接包含这些文件的树外开发板必须更新其包含路径。

  新的子目录布局如下：

  +--------------------------+------------------------------------------+
  | MCX 系列                 | 新位置                                   |
  +==========================+==========================================+
  | MCXA                     | ``dts/arm/nxp/mcx/mcxa/``                |
  +--------------------------+------------------------------------------+
  | MCXC                     | ``dts/arm/nxp/mcx/mcxc/``                |
  +--------------------------+------------------------------------------+
  | MCXE                     | ``dts/arm/nxp/mcx/mcxe/``                |
  +--------------------------+------------------------------------------+
  | MCXL                     | ``dts/arm/nxp/mcx/mcxl/``                |
  +--------------------------+------------------------------------------+
  | MCXN                     | ``dts/arm/nxp/mcx/mcxn/``                |
  +--------------------------+------------------------------------------+
  | MCXW                     | ``dts/arm/nxp/mcx/mcxw/``                |
  +--------------------------+------------------------------------------+

  示例：

  .. code-block:: dts

    /* Before */
    #include <nxp/mcx/nxp_mcxc242.dtsi>

    /* After */
    #include <nxp/mcx/mcxc/nxp_mcxc242.dtsi>

* NXP MCXN 系列新增了针对 mcxn547、mcxn947 和 mcxn236 的专用按器件 composer DTSI 文件（``nxp_mcxn547.dtsi``、``nxp_mcxn947.dtsi`` 和 ``nxp_mcxn236.dtsi``），以及本版本新增的 mcxn546、mcxn946 和 mcxn235 phantom 器件。这些文件都只是包含现有的系列文件（分别为 ``nxp_mcxn54x.dtsi``、``nxp_mcxn94x.dtsi`` 和 ``nxp_mcxn23x.dtsi``），没有任何覆盖；而 mcxn547、mcxn947 和 mcxn236 的树内开发板现在改为包含新的按器件文件。系列文件本身没有变化，直接包含它们仍然可用，因此这不是必须的迁移，但这三种器件的树外开发板可能希望改用新的按器件文件，以与系列中的其他器件保持一致。

  示例：

  .. code-block:: dts

    /* Before */
    #include <nxp/mcx/mcxn/nxp_mcxn94x.dtsi>

    /* After */
    #include <nxp/mcx/mcxn/nxp_mcxn947.dtsi>

* NXP i.MX RT DTSI 文件已从扁平目录 ``dts/arm/nxp/imxrt/`` 重组为按系列划分的子目录。直接包含这些文件的树外开发板必须更新其包含路径。

  新的子目录布局如下：

  +--------------------------+------------------------------------------+
  | i.MX RT 系列             | 新位置                                   |
  +==========================+==========================================+
  | RT10xx                   | ``dts/arm/nxp/imxrt/imxrt10xx/``         |
  +--------------------------+------------------------------------------+
  | RT11xx                   | ``dts/arm/nxp/imxrt/imxrt11xx/``         |
  +--------------------------+------------------------------------------+
  | RT5xx                    | ``dts/arm/nxp/imxrt/imxrt5xx/``          |
  +--------------------------+------------------------------------------+
  | RT6xx                    | ``dts/arm/nxp/imxrt/imxrt6xx/``          |
  +--------------------------+------------------------------------------+
  | RT7xx                    | ``dts/arm/nxp/imxrt/imxrt7xx/``          |
  +--------------------------+------------------------------------------+
  | RT118x                   | ``dts/arm/nxp/imxrt/imxrt118x/``         |
  +--------------------------+------------------------------------------+

  示例：

  .. code-block:: dts

    /* Before */
    #include <nxp/imxrt/nxp_rt1060.dtsi>

    /* After */
    #include <nxp/imxrt/imxrt10xx/nxp_rt1060.dtsi>

* i.MX RT118x 开发板现在包含单个 part-core composer 文件 ``nxp_rt118<part>_cm<core>.dtsi``，而不再包含 series-core 文件外加单独的器件 overlay。树外开发板必须相应地更新其设备树包含路径（:github:`110228`）。

  对于以前需要 series 文件加器件 overlay 的器件，示例如下：

  .. code-block:: dts

    /* Before */
    #include <nxp/imxrt/nxp_rt118x_cm7.dtsi>
    #include <nxp/imxrt/nxp_rt1186.dtsi>

    /* After */
    #include <nxp/imxrt/imxrt118x/nxp_rt1186_cm7.dtsi>

* i.MX RT7xx 开发板现在包含单个 part-core composer 文件 ``nxp_<part>_<core>.dtsi``，而不再包含 series-core 文件。树外开发板必须相应地更新其设备树包含路径。

  对于以前需要 series 文件的器件，示例如下：

  .. code-block:: dts

    /* Before */
    #include <nxp/imxrt/imxrt7xx/nxp_rt7xx_cm33_cpu0.dtsi>

    /* After */
    #include <nxp/imxrt/imxrt7xx/nxp_rt798s_cm33_cpu0.dtsi>

* ``hal_nxp`` ``dts/nxp/`` 目录树下的 NXP SoC 引脚控制头文件已重组，以与 ``dts/arm/nxp/<family>/<series>/`` 布局保持一致：每个 SoC 的 ``*-pinctrl.h`` / ``*-pinctrl.dtsi`` 文件都移入了 ``pinctrl/`` 子目录。直接包含这些 SoC 引脚控制头文件的树外开发板必须更新其包含路径。

  采用 family/series 层次的分组（i.MX RT、Kinetis、LPC、MCX）将头文件放在 ``<family>/<series>/pinctrl/`` 中；结构扁平的分组（i.MX、S32、RW）则放在 family 级目录 ``<family>/pinctrl/`` 中。Kinetis 还为以前没有对应 series 目录的器件新增了 series 目录（``k0x``、``km3x``、``kv3x``）。此外，原先的 ``nxp_imx`` 目录被拆分：``nxp_imx/rt/`` 成为 ``imxrt/`` family，其余 i.MX 应用处理器则成为扁平的 ``imx/`` family。

  示例：

  .. code-block:: dts

    /* Before */
    #include <nxp/nxp_imx/rt/mimxrt1151dvm8b-pinctrl.dtsi>
    #include <nxp/nxp_imx/mimx8ml8dvnlz-pinctrl.dtsi>
    #include <nxp/kinetis/MK64FN1M0VLL12-pinctrl.h>

    /* After */
    #include <nxp/imxrt/imxrt11xx/pinctrl/mimxrt1151dvm8b-pinctrl.dtsi>
    #include <nxp/imx/pinctrl/mimx8ml8dvnlz-pinctrl.dtsi>
    #include <nxp/kinetis/k6x/pinctrl/MK64FN1M0VLL12-pinctrl.h>

PWM
===

* :dtcompatible:`microchip,xec-pwm` 的 ``pcrs`` 属性（数组类型）已由 ``pcr-scr`` 属性（int 类型）取代，以便使用编码了 PCR 寄存器索引和位位置的宏（:github:`104570`）。

* 自 Zephyr v3.3.0 起弃用的 STM32 PWM 设备树绑定宏 ``PWM_STM32_COMPLEMENTARY`` 不再定义。请改用 ``STM32_PWM_COMPLEMENTARY``。

* :dtcompatible:`nxp,ctimer-pwm` 现在通过通用的 :ref:`mux <mux_api>` 子系统路由其输入捕获信号。``inputmux-connections`` 属性已被移除；请改用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）描述该路由，并改为从定时器节点的 ``mux-states`` 属性引用它。（:github:`112088`）

* :dtcompatible:`nxp,sctimer-pwm` 现在通过通用的 :ref:`mux <mux_api>` 子系统路由其输入捕获信号。``input-channels`` 属性已被移除；请改用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）描述该路由，并改为从定时器节点的 ``mux-states`` 属性引用它。（:github:`112088`）

RTC
===

* 旧的基于计数器的 DS3231 驱动已被移除，:github:`95221` 中引入的弃用至此完成。使用 :dtcompatible:`maxim,ds3231`、``CONFIG_COUNTER_MAXIM_DS3231`` 或 :file:`<zephyr/drivers/rtc/maxim_ds3231.h>` 的应用必须迁移到 RTC 子系统驱动。

  将单个旧 I2C 节点替换为 :dtcompatible:`maxim,ds3231-mfd` 父节点和 :dtcompatible:`maxim,ds3231-rtc` 子节点。将 ``isw-gpios`` 移至 RTC 子节点，把原先使用的 ``32k-gpios`` 重命名为 ``freq-32khz-gpios``，并将 ``maxim_ds3231_*`` 辅助 API 的用法替换为通用 RTC 子系统 API。

* :dtcompatible:`microcrystal,rv3032` 的 ``trickle-resistor-ohms`` 和 ``trickle-charger-mode`` 属性已移至父设备 :dtcompatible:`microcrystal,rv3032-mfd`。父 MFD 设备现在负责为所有子设备配置备用电源模式。

SD 主机控制器
=============

* 将 Kconfig 选项 ``CONFIG_SDHC_STM32_POLLING_SUPPORT`` 重命名为 :kconfig:option:`CONFIG_SDHC_STM32_DMA_MODE`。新符号启用 DMA（默认 ``y``）；将其设为 ``n`` 即可使用轮询模式。（:github:`101617`）

* 将 Kconfig 选项 ``CONFIG_SDHC_STM32_SDIO`` 重命名为 :kconfig:option:`CONFIG_SDHC_STM32_SDMMC`。（:github:`101617`）

* 设备树 compatible ``st,stm32-sdio`` 已重命名。请改用 :dtcompatible:`st,stm32-sdmmc`。使用该 compatible 后，旧的磁盘驱动与 SDHC 驱动可以指向同一节点。要迁移到 SDHC STM32 SDMMC 驱动，请禁用旧的磁盘驱动：

  .. code-block:: kconfig

     CONFIG_SDMMC_STM32=n

  (:github:`101617`)

* 对于 :dtcompatible:`st,stm32-sdmmc`，``sdhi-on-gpios`` 属性已合并到现有的 ``pwr-gpios`` 属性中。请在树外设备树节点中将 ``sdhi-on-gpios`` 替换为 ``pwr-gpios``。

* :kconfig:option:`CONFIG_SDMMC_STM32_HWFC` 现在对旧的 SDMMC_STM32 磁盘驱动默认启用，以避免磁盘访问期间出现 FIFO 下溢和上溢错误。此前设置 ``CONFIG_SDMMC_STM32_HWFC=y`` 的应用应在其开发板配置文件中移除该配置，因为它现在已是默认值。

* :dtcompatible:`litex,mmc` 现在使用 ``dma-coherent`` 设备树属性来表明控制器的 DMA 访问与 CPU 保持一致。:kconfig:option:`CONFIG_SDHC_LITEX_LITESDCARD_NO_COHERENT_DMA` 会根据该属性自动设置，且不再可由用户配置。（:github:`108411`）

SPI
===

* SPI API 已迁移到 :ref:`coding_guideline_inclusive_language` 中选定的包容性术语（controller/peripheral 角色、SDO/SDI 信号名）。旧名称已弃用，并将在 Zephyr v5.0 中移除：

  * :c:macro:`SPI_OP_MODE_CONTROLLER` 和 :c:macro:`SPI_OP_MODE_PERIPHERAL` 取代 ``SPI_OP_MODE_MASTER`` 和 ``SPI_OP_MODE_SLAVE``。
  * :c:struct:`spi_config` 的 ``slave`` 成员已重命名为 ``peripheral``。
  * :c:macro:`SPI_SDO_OVERRUN_UNKNOWN`、:c:macro:`SPI_SDO_OVERRUN_DT` 和 :c:macro:`SPI_SDO_OVERRUN_DT_INST` 取代 ``SPI_MOSI_OVERRUN_*`` 宏。
  * :kconfig:option:`CONFIG_SPI_PERIPHERAL` 取代 ``CONFIG_SPI_SLAVE``。
  * 在面向驱动的 ``spi_context.h`` 辅助函数中，``spi_context_is_peripheral()`` 取代 ``spi_context_is_slave()``。
  * :dtcompatible:`zephyr,spi-bitbang` 和 :dtcompatible:`raspberrypi,pico-spi-pio` 的 ``sdo-gpios``/``sdi-gpios`` 属性、:dtcompatible:`brcm,afbr-s50` 的 ``spi-sdi-gpios``/``spi-sdo-gpios`` 属性、:dtcompatible:`nxp,s32-spi` 的 ``peripheral`` 属性以及 :dtcompatible:`realtek,bee-spi` 的 ``is-peripheral`` 属性，取代了它们原先基于 ``mosi``/``miso``/``slave`` 的名称；这些旧名称在绑定中仍被接受，但已标记为弃用。
  * :dtcompatible:`zephyr,bt-hci-spi-peripheral` 设备树 compatible 取代 ``zephyr,bt-hci-spi-slave``。

* ``SPI_SILABS_SIWX91X_GSPI_DMA`` 和 ``SPI_SILABS_SIWX91X_GSPI_DMA_MAX_BLOCKS`` 已被移除。它们由 ``SPI_SILABS_SIWX91X_GSPI_DMA_DESCR_COUNT`` 取代，后者可用于启用 DMA 并配置描述符数量。

* :dtcompatible:`st,stm32h7-spi` 的 ``fifo-enable`` 属性已被移除。现在轮询和中断模式下始终使用 FIFO 以提升性能。新增的 ``st,fifo-threshold`` 属性可用于配置 FIFO 阈值（默认值 = 1）。（:github:`110265`）

* :c:macro:`SPI_CONFIG_DT`、:c:macro:`SPI_CONFIG_DT_INST`、:c:macro:`SPI_DT_SPEC_GET`、:c:macro:`SPI_DT_SPEC_INST_GET`、:c:macro:`SPI_DT_IODEV_DEFINE`、:c:macro:`SPI_DT_INST_IODEV_DEFINE` 和 :c:macro:`SPI_CS_CONTROL_INIT` 的可选 delay 参数已被移除；请从每次调用中删除该参数。请改用 ``spi-cs-setup-delay-ns`` 和 ``spi-cs-hold-delay-ns`` 设备树属性（注意它们以纳秒而不是微秒为单位）。

STM32
=====

* :dtcompatible:`gpio-keys` 设备将无法挂起，除非 Devicetree 中存在属性 ``zephyr,suspend-action`` 且其值为 ``"none"`` 或 ``"full-disconnect"``。有关更多详细信息，请参阅与此绑定相关的迁移指南条目。（:github:`104690` / :github:`108294`）

* SoC DTSI 文件现在对所有外设一致使用中断优先级零。如果应用此前依赖 SoC DTSI 文件中的值，则现在必须通过 Devicetree 显式配置中断优先级。（:github:`106188`）

* :dtcompatible:`st,stm32-sai` 绑定已重构，以反映 SAI 硬件拓扑。父节点现在表示 SAI Block 控制器，而新的 ``child-binding`` 表示 SAI 子块实例。以下属性应从父 SAI 节点移至子子块节点：``dmas``、``dma-names`` （现根据 ``enum: [tx, rx]`` 进行校验）、``pinctrl-0``、``pinctrl-names``、``mclk-enable``、``mclk-divider``、``synchronous`` 和 ``fifo-threshold``。（:github:`104423`）

* :dtcompatible:`st,stm32-adc` 绑定已重构，以反映 ADC 硬件拓扑。父节点现在表示 ADC 公共块，其中保存时钟以及连接到它的所有 ADC 实例共享的设置，而新的 ``child-binding`` 表示 ADC 实例本身。

  现有的 ``&adcN`` 节点标签仍用于指代 ADC 实例，这些实例现在是标号为 ``&adcN_common`` 的公共块节点的子节点，其中 ``N`` 表示共享该块的实例（例如 ``&adc1_common``、``&adc12_common`` 或 ``&adc123_common``）。除实例节点外，还必须启用公共块节点。

  以下属性应从 ``&adcN`` 实例节点移至其 ``&adcN_common`` 父节点：``clocks``、``clock-names``、``st,adc-clock-source``、``st,adc-prescaler`` 和 ``vref-mv``。由于时钟现在按公共块描述一次，共享该时钟的实例不能再被赋予相互冲突的时钟设置。

  .. tabs::

    .. group-tab:: 之前

      .. code-block:: devicetree

          &adc1 {
            clocks = <&rcc STM32_CLOCK(AHB2, 13)>,
                     <&rcc STM32_SRC_SYSCLK ADC_SEL(3)>;
            clock-names = "adcx", "adc_ker";
            st,adc-clock-source = "ASYNC";
            st,adc-prescaler = <4>;
            vref-mv = <3000>;
            pinctrl-0 = <&adc1_in1_pa0>;
            pinctrl-names = "default";
            status = "okay";
          };

    .. group-tab:: 之后

      .. code-block:: devicetree

          &adc12_common {
            clocks = <&rcc STM32_CLOCK(AHB2, 13)>,
                     <&rcc STM32_SRC_SYSCLK ADC_SEL(3)>;
            clock-names = "adcx", "adc_ker";
            st,adc-clock-source = "ASYNC";
            st,adc-prescaler = <4>;
            vref-mv = <3000>;
            status = "okay";
          };

          &adc1 {
            pinctrl-0 = <&adc1_in1_pa0>;
            pinctrl-names = "default";
            status = "okay";
          };

  请注意，只有当 ``vref-mv`` 与其默认值 ``3300`` 不同时，才需要设置该属性。

  对于 :dtcompatible:`st,stm32f1-adc` 和 :dtcompatible:`st,stm32f4-adc`，每个实例保留自己的寄存器时钟，因此 ``clocks`` 和 ``clock-names`` 仍位于 ``&adcN`` 节点上。（:github:`117309`）

* :dtcompatible:`st,hci-stm32wba` 和 :dtcompatible:`st,stm32wba-ieee802154` 节点（节点标签分别为 ``bt_hci_wba`` 和 ``ieee802154``）现在是顶层 :dtcompatible:`st,stm32wba-radio` 节点的子节点，后者的节点标签为 ``radio``。``interrupts`` 属性现在设置在 ``&radio`` 节点上，而不再在 ``&bt_hci_wba`` 和 ``&ieee802154`` 两个节点上重复设置。修改了这两个节点中任一节点上 ``interrupts`` 属性的树外开发板，必须改为在顶层 ``&radio`` 节点上设置该属性。（:github:`110546`）

* ST 摄像头和显示屏连接器 gpio-nexus 的重命名如下：``st,dsi-lcd-qsh-030`` 重命名为 :dtcompatible:`st,dsi-lcd-qsh-030-connector`，``st,stm32-dcmi-camera-fpu-330zh`` 重命名为 :dtcompatible:`st,dvp-cam-zif-30-connector`

* :dtcompatible:`st,stm32-xspim` 现在还用于 STM32H5 和 STM32H7RS 系列，以声明和配置 XSPI Manager。使用 XSPI 的开发板现在除了所需的 XSPI 控制器外，还必须启用 ``&xspim`` 节点才能使用 XSPI。（:github:`109903`）

* STM32MP13 SoC DTSI 以太网：将标签从 ``mac:`` 和 ``mdio:`` 重命名为 ``mac0:`` 和 ``mdio0:``。目的是区分两个可用的以太网控制器。（:github:`108574`）

* Kconfig 选项 ``CONFIG_STM32_MEMMAP`` 已重命名为 :kconfig:option:`CONFIG_FLASH_STM32_NOR_MEMMAP`。

* 使用 ``stm32_lp_tick_source`` 节点标签选择 LPTIM 作为系统定时器已不再支持，并且会触发构建错误。请改用 :ref:`通用 chosen <devicetree-zephyr-chosen-nodes>` ``zephyr,system-timer``。（:github:`112999`）

* 与唤醒引脚相关的 :dtcompatible:`st,stm32-pwr` 的 ``wkup-pins-nb``、``wkup-pins-srcs``、``wkup-pins-pol`` 和 ``wkup-pins-pupd`` 属性以及子绑定已被移除。作为替代，新增了一个名为 ``wakeup-controller`` 的节点，其新 compatible 为 :dtcompatible:`st,stm32-pwr-wkupctrl`，该节点作为所有现有 :dtcompatible:`st,stm32-pwr` 节点的子节点引入。

  对于大多数树外用户，只需将 ``status = "okay";`` 属性以及开发板 DTS 中声明的唤醒引脚节点（如果有）从 ``&pwr`` 节点移至其新子节点 ``wakeup-controller`` 即可。以下 Devicetree 片段展示了如何通过在开发板 DTS 中添加两行来实现这一点：

  .. tabs::

    .. group-tab:: 之前

      .. code-block:: devicetree

          &pwr {
            wkup-pin@1 {
              /* ... */
            };

            status = "okay";
          };

    .. group-tab:: 之后

      .. code-block:: devicetree
        :emphasize-lines: 2, 8

          &pwr {
            wakeup-controller {
              wkup-pin@1 {
                /* ... */
              };

              status = "okay";
            };
          };

  请注意，树中的唤醒引脚节点现在称为 :samp:`wkup@{N}`，而不是 :samp:`wkup-pin@{N}`。此更改只是名称上的调整，没有功能影响。（:github:`114092`）

* :dtcompatible:`st,stm32-pwr` 节点现在由 SoC DTSI 默认启用，因为 ``status = "disabled";`` 属性已被移除。这应该没有影响，因为该属性除了用于唤醒引脚功能外并未使用，而该功能现在由 :dtcompatible:`st,stm32-pwr-wkupctrl` 处理。（:github:`114092`）

* STM32H5 系列的所有以太网 pinctrl 节点（:samp:`eth_mdc_{px0}`、:samp:`eth_mdio_{px0}` 和 :samp:`eth_pps_out_{px0}` 除外）已重命名，以匹配数据手册中的名称（:github:`118318`）。

  下表给出了新旧名称之间的映射关系，可用于迁移：

  .. list-table::
     :header-rows: 1
     :widths: 30 35 35

     * - 旧名称
       - 新名称（``mii`` PHY）
       - 新名称（``rmii`` PHY）
     * - :samp:`eth_crs_dv_{px0}`
       - *MII 不适用*
       - :samp:`eth_rmii_crs_dv_{px0}`
     * - :samp:`eth_ref_clk_{px0}`
       - *MII 不适用*
       - :samp:`eth_rmii_ref_clk_{px0}`
     * - :samp:`eth_col_{px0}`
       - :samp:`eth_mii_col_{px0}`
       - *RMII 不适用*
     * - :samp:`eth_crs_{px0}`
       - :samp:`eth_mii_crs_{px0}`
       - *RMII 不适用*
     * - :samp:`eth_rx_clk_{px0}`
       - :samp:`eth_mii_rx_clk_{px0}`
       - *RMII 不适用*
     * - :samp:`eth_rx_dv_{px0}`
       - :samp:`eth_mii_rx_dv_{px0}`
       - *RMII 不适用*
     * - :samp:`eth_rx_er_{px0}`
       - :samp:`eth_mii_rx_er_{px0}`
       - *RMII 不适用*
     * - :samp:`eth_rxd0_{px0}`
       - :samp:`eth_mii_rxd0_{px0}`
       - :samp:`eth_rmii_rxd0_{px0}`
     * - :samp:`eth_rxd1_{px0}`
       - :samp:`eth_mii_rxd1_{px0}`
       - :samp:`eth_rmii_rxd1_{px0}`
     * - :samp:`eth_rxd2_{px0}`
       - :samp:`eth_mii_rxd2_{px0}`
       - *RMII 不适用*
     * - :samp:`eth_rxd3_{px0}`
       - :samp:`eth_mii_rxd3_{px0}`
       - *RMII 不适用*
     * - :samp:`eth_tx_clk_{px0}`
       - :samp:`eth_mii_tx_clk_{px0}`
       - *RMII 不适用*
     * - :samp:`eth_tx_en_{px0}`
       - :samp:`eth_mii_tx_en_{px0}`
       - :samp:`eth_rmii_tx_en_{px0}`
     * - :samp:`eth_txd0_{px0}`
       - :samp:`eth_mii_txd0_{px0}`
       - :samp:`eth_rmii_txd0_{px0}`
     * - :samp:`eth_txd1_{px0}`
       - :samp:`eth_mii_txd1_{px0}`
       - :samp:`eth_rmii_txd1_{px0}`
     * - :samp:`eth_txd2_{px0}`
       - :samp:`eth_mii_txd2_{px0}`
       - *RMII 不适用*
     * - :samp:`eth_txd3_{px0}`
       - :samp:`eth_mii_txd3_{px0}`
       - *RMII 不适用*

  .. note::
    引脚名称现在取决于使用的是 MII PHY 还是 RMII PHY；以太网节点在 Devicetree 中通过 ``phy-connection-type`` 属性来指示，其取值为 ``mii`` 或 ``rmii``。

    :samp:`{px0}` 是占位符，应替换为实际的引脚名称（例如 ``pa1``）。

    STM32H5Ex/STM32H5Fx 系列的 SoC 不受此更改影响，因为它们自引入 Zephyr 以来一直使用新名称。

Syscon
======

* syscon API 函数 :c:func:`syscon_read_reg` 和 :c:func:`syscon_write_reg` 现在使用 ``uint32_t`` 而不是 ``uint16_t`` 作为寄存器偏移参数。这样可以支持更大的寄存器偏移。显式为寄存器参数声明 ``uint16_t`` 变量或实现 syscon 驱动 API 函数的代码可能需要更新。

Texas Instruments
=================

* 现在使用 :dtcompatible:`ti,am654-timer` 实例作为系统定时器时，需要通过 :ref:`通用 chosen <devicetree-zephyr-chosen-nodes>` ``zephyr,system-timer`` 节点进行显式选择，所有使用它的 SoC 都已提供该节点。希望使用不同于 SoC 默认实例的下游开发板和应用需要覆盖该节点。（:github:`115068`）

USB
===

* 在 STM32N6 上，用于配置 USBPHYC 时钟多路复用器的 ``clocks`` 单元已在 SoC DTSI 层面从 :samp:`usbotg_hs{N}` 移至 :samp:`usbphyc{N}` 节点。使用 STM32N6 SoC 且带有自定义时钟多路复用配置的开发板，现在必须在 :samp:`usbphyc{N}` 而不是 :samp:`usbotg_hs{N}` 上设置 ``clocks`` 属性。（:github:`107813`）
* 在控制传输处理程序中通过 ``errno`` 指示协议错误已弃用。处理程序应直接返回错误码。（:github:`108118`）
* 当主机发起数据阶段为从主机到设备的控制传输时，现在会在接收数据阶段之前以 ``buf`` 为 NULL 调用 :c:struct:`usbd_class_api` 中的 ``control_to_dev`` 回调以及 :c:struct:`usbd_vreq_node` 中的 ``to_dev`` 回调。这样协议栈就可以在数据阶段返回 STALL。树外的类和供应商处理程序需要更新。（:github:`108840`）
* :c:struct:`usbd_class_api` 中的 ``control_to_host`` 和 :c:struct:`usbd_vreq_node` 中的 ``to_host`` 这两个 USB 控制传输回调现在需要自行分配数据阶段缓冲区。这样可以只分配实际所需的内存，使最坏情况下的内存用量取决于处理程序的实现，而不再取决于来自主机的不可信 wLength 值。树外的类和供应商处理程序需要更新。（:github:`102491`）
* Espressif USB-OTG 全速控制器的 compatible ``espressif,esp32-usb-otg`` 已重命名为 :dtcompatible:`espressif,esp32-usb-otg-fs`。内部 PHY 的 D+/D- 焊盘编号现在通过 ``phy-dp-pin`` 和 ``phy-dm-pin`` 属性提供。使用旧 compatible 的树外设备树必须更新节点 compatible 并添加这两个引脚属性。
* 现在 :dtcompatible:`st,stm32-usbphyc` 节点上要求提供 ``clock-names`` 属性。SoC DTSI 层面提供了默认值，但 *可能* 需要由开发板 DTS 覆盖。（:github:`112477`）

* USB 主机控制器 API 结构体 ``uhc_api`` 已重命名为 :c:struct:`uhc_driver_api`。它现在也使用 :c:macro:`DEVICE_API`。树外的 USB 主机控制器驱动必须重命名其 API 结构体定义，并将其 API 实例改为 ``DEVICE_API(uhc, ...)``。（:github:`108414`）

* :dtcompatible:`st,stm32u5-otghs-phy` 的 ``clock-reference`` 属性现已弃用，应从 DTS 文件中移除；如果该属性不存在，底层驱动会自动计算出正确的值（若存在则沿用该值）。（:github:`117882`）

* :c:struct:`usbd_class_api` 中的 ``get_desc`` 回调现在返回 ``const void *`` 而不是 ``void *``，这样类就可以将其描述符指针数组保存在 ROM 中。树外的类必须更新其处理程序的返回类型。（:github:`118251`）

Wi-Fi
=====

* 在由 :c:struct:`net_wifi_mgmt_offload`、内部的 :c:struct:`ethernet_api` 和 :c:struct:`wifi_mgmt_ops` 实现的函数中，新增了一个指向 :c:struct:`net_if` 的指针参数。该 API 不直接暴露给应用，因此只有树外驱动需要更新。（:github:`106086`）

* Espressif Wi-Fi 驱动的 Kconfig 选项 ``CONFIG_ESP32_WIFI_STA_AUTO_DHCPV4`` 已被移除，改用通用的 :kconfig:option:`CONFIG_WIFI_STA_AUTO_DHCPV4`。此前禁用了 Espressif 专用选项的应用，现在必须禁用该通用选项，才能在 STA 连接后保持手动 DHCPv4 或静态 IP 行为。

* :c:struct:`wifi_status` 新增了 ``status_code`` 和 ``reason_code`` 成员，用于承载原始 IEEE 802.11 代码，因此该结构体比原来的 ``int`` 更大。触发或接收 :c:enumerator:`NET_EVENT_WIFI_SCAN_DONE`、:c:enumerator:`NET_EVENT_WIFI_CONNECT_RESULT`、:c:enumerator:`NET_EVENT_WIFI_DISCONNECT_RESULT`、:c:enumerator:`NET_EVENT_WIFI_DISCONNECT_COMPLETE`、:c:enumerator:`NET_EVENT_WIFI_AP_ENABLE_RESULT` 或 :c:enumerator:`NET_EVENT_WIFI_AP_DISABLE_RESULT` 的代码必须使用 ``sizeof(struct wifi_status)`` 而不是 ``sizeof(int)`` 作为事件负载长度。仅读取状态值的事件处理程序不受影响，因为它仍然是第一个成员。（:github:`116704`）

* 超过超时时间仍未完成的 Wi-Fi 连接请求现在会在 :c:enumerator:`NET_EVENT_WIFI_CONNECT_RESULT` 中报告 :c:enumerator:`WIFI_STATUS_CONN_TIMEOUT`，而不是原始的 ``-ETIMEDOUT``。这仅涉及由 supplicant 处理的连接。此前根据 errno 值进行匹配的应用，现在必须改为根据状态值进行匹配。（:github:`116704`）

Xen
===

* 随着 zephyr-xenlib 的引入，Xen 公共头文件的路径已发生变化。请使用 ``xen/public/...`` 而不是 ``zephyr/xen/public/...``。

中断控制器
==========

* 所有中断控制器绑定现在使用 ``flags`` 作为中断单元名称，而不再使用 ``sense``。以下中断控制器绑定已更新：

  * :dtcompatible:`intel,ioapic`
  * :dtcompatible:`intel,loapic`
  * :dtcompatible:`cdns,xtensa-core-intc`
  * :dtcompatible:`intel,ace-intc`
  * :dtcompatible:`intel,cavs-intc`
  * :dtcompatible:`snps,designware-intc`
  * :dtcompatible:`mediatek,adsp_intc`

  使用这些中断控制器的驱动已更新为使用 ``flags`` 作为单元名称。不过，任何使用 ``DT_INST_IRQ(n, sense)`` 或 ``DT_IRQ(node, sense)`` 直接访问中断属性的树外驱动，都应改为使用 ``flags`` 而不是 ``sense``。

* 弃用 GIC 头文件 :file:`gic.h` 中的 ``GIC_NUM_CPU_IF``。应改用 :kconfig:option:`CONFIG_MP_MAX_NUM_CPUS`。

串行接口
========

* :c:func:`uart_irq_update` 的返回类型现在是 ``void``，而不再是 ``int``。（:github:`105231`）

* :dtcompatible:`brcm,bcm2711-aux-uart` 设备树绑定已被移除，改用 :dtcompatible:`brcm,bcm283x-aux-uart`。节点必须添加 :dtcompatible:`ns16550` 作为 compatible，将 ``clocks`` 属性替换为 ``clock-frequency``，并指定 ``reg-shift = <2>``。专用的 BCM2711 辅助 UART 驱动已被移除，改用通用的 NS16550 驱动；后者现在通过厂商特定的扩展为 Broadcom BCM283x 辅助 UART 提供支持。（:github:`115112`）

以太网
======

* WIZnet 以太网驱动现在共用一组 Kconfig 选项。请将 ``CONFIG_ETH_W5500_*``、``CONFIG_ETH_W6100_*`` 和 ``CONFIG_ETH_W6300_*`` 替换为相应的 ``CONFIG_ETH_WIZNET_*`` 选项。

* ``ETHERNET_CONFIG_TYPE_T1S_PARAM`` 及相关的 ``NET_REQUEST_ETHERNET_SET_T1S_PARAM`` 已被移除。应改用 :c:func:`phy_set_plca_cfg` 和 :c:func:`net_eth_get_phy` 来设置这些参数（:github:`108136`）。

* :c:struct:`ethernet_api` 中实现的函数新增了一个指向 :c:struct:`net_if` 的指针参数。该 API 不直接暴露给应用，因此只有树外驱动需要更新。（:github:`106086`）

* :dtcompatible:`nxp,enet-mac` 的 ``pinctrl-0`` 和 ``pinctrl-names`` 设备树属性需要从 MAC 节点移到父以太网控制器节点。（:github:`107352`）

* NuMaker 以太网驱动已随 ``CONFIG_ETH_NUMAKER`` 一起移除。NuMaker EMAC 现在改由通用的 Synopsys DesignWare MAC 驱动负责，对应的 Kconfig 选项为 :kconfig:option:`CONFIG_ETH_NUMAKER_DWC_ETHER_1000`；该驱动需要在设备树中提供 MDIO 控制器和 PHY。树外开发板必须启用 ``mdio`` 节点，在其 pinctrl 状态中配置 MDC 和 MDIO 引脚，将 PHY 添加到该节点，并通过 ``phy-handle`` 让 ``emac`` 节点指向它。:dtcompatible:`nuvoton,numaker-ethernet` 的 ``phy-addr`` 属性已被移除。

* :c:struct:`dsa_api` 的 ``port_generate_random_mac`` 已被移除。此外，:c:struct:`dsa_port_config` 现在使用 :c:struct:`net_eth_mac_config` 设置 MAC 地址。:c:struct:`dsa_port_config` 的 ``mac_addr`` 和 ``use_random_mac_addr`` 成员已被移除。树外 DSA 驱动必须更新其端口配置代码，改用新的 API 和结构体。（:github:`108952`）

* Kconfig 选项 ``CONFIG_ETH_NATIVE_TAP_PTP_CLOCK`` 已被 :kconfig:option:`CONFIG_PTP_CLOCK_NATIVE` 取代。为 native_sim PTP 时钟驱动新增了 :dtcompatible:`zephyr,native-ptp-clock` 兼容字符串。当存在 :dtcompatible:`zephyr,native-ptp-clock` 兼容字符串时，:kconfig:option:`CONFIG_PTP_CLOCK_NATIVE` 默认启用。

* native_sim TAP 以太网驱动现在通过 :dtcompatible:`zephyr,native-tap` 兼容字符串从设备树实例化。每个接口由设备树节点定义，而不再使用已被移除的 ``CONFIG_ETH_NATIVE_TAP_INTERFACE_COUNT`` Kconfig 选项。添加多个节点即可创建多个接口。以下 Kconfig 选项已被移除，并由设备树属性取代：

  * ``CONFIG_ETH_NATIVE_TAP_DRV_NAME`` -> ``host-interface`` 属性。
  * ``CONFIG_ETH_NATIVE_TAP_MAC_ADDR`` -> ``local-mac-address`` 属性。
  * ``CONFIG_ETH_NATIVE_TAP_RANDOM_MAC`` -> ``zephyr,random-mac-address`` 属性。

  ``--eth-if``、``--mac-addr``、``--ipv4-addr``、``--ipv4-gw`` 和 ``--ipv4-nm`` 命令行选项仍然受支持，并作用于第一个接口。其余接口新增了按接口区分的变体，例如 ``<node>_eth-if``、``<node>_mac-addr`` 等。

* :c:struct:`dsa_api` 的 ``port_phylink_change`` 现在是可选的。DSA 驱动不再需要在 PHY 链路变化时调用 :c:func:`net_eth_carrier_on` 或 :c:func:`net_eth_carrier_off`，现在由 DSA 核心处理。``port_phylink_change`` 的 ``void *user_data`` 参数已改为 ``const struct device *dev``，因此不再需要通过强制转换来获取设备指针。树外 DSA 驱动必须更新其 ``port_phylink_change`` 回调以匹配新 API，并且可以从中移除对 :c:func:`net_eth_carrier_on` 或 :c:func:`net_eth_carrier_off` 的任何调用。（:github:`109671`）

* 使用 :c:func:`net_if_up` 启动以太网接口时，现在会检查 MAC 地址的有效性。如果 MAC 地址无效，接口将无法启动，并记录一条错误日志。该检查在调用 :c:struct:`ethernet_api` 的 ``start`` 函数之前完成。这也适用于 native Wi-Fi 驱动。（:github:`110435`）

* Xilinx GEM 以太网驱动（:dtcompatible:`xlnx,gem`）已改为使用当前的 MDIO 和 PHY 设施，其实现被拆分为独立的 MDIO 驱动和以太网 MAC 驱动。该驱动自定义的 PHY 管理代码已被移除。被移除的自定义代码所支持的以太网 PHY 类型，即 Marvell Alaska GBit PHY 系列和 TI TLK105/DP83822 100 MBit PHY，现在都由标准的 :dtcompatible:`ethernet-phy` 驱动覆盖。模拟 Xilinx GEM 的 QEMU 目标已相应更新，Zynq-7000 和 ZynqMP / UltraScale+ SoC 系列的设备树也已更新。（:github:`87313`）

* 使用 :c:enumerator:`ETHERNET_CONFIG_TYPE_EXTRA_TX_PKT_HEADROOM` 为发送数据包请求额外 headroom 的以太网和 Wi-Fi 驱动，现在必须选择 :kconfig:option:`CONFIG_NET_L2_ETHERNET_EXTRA_TX_PKT_HEADROOM`。（:github:`112924`）

* ``ETHERNET_PTP`` 标志已从 :c:enum:`ethernet_hw_caps` 中移除。请使用 :c:func:`net_eth_get_ptp_clock` 检查以太网接口是否有 PTP 时钟。树外驱动必须从其 :c:struct:`ethernet_api` 的 ``get_capabilities`` 实现中移除对这些标志的引用。（:github:`112788`）

* 支持 LLDP 的以太网驱动不再需要在初始化时调用 :c:func:`net_lldp_set_lldpdu`。现在这项工作由 :c:func:`ethernet_init` 完成。（:github:`114087`）

* :dtcompatible:`infineon,xmc4xxx-ethernet` 和 :dtcompatible:`wch,ethernet` 节点已与其父节点合并。同级的 MDIO 节点不会移动，因此成为这些 ``ethernet`` 节点的子节点。（:github:`114899`）

* ``infineon,xmc4xxx-mdio`` 的 ``mdi-port-ctrl`` 属性已移到父节点（:dtcompatible:`infineon,xmc4xxx-ethernet`）。（:github:`114899`）

* 兼容字符串 ``espressif,esp32-mdio``、``infineon,xmc4xxx-mdio``、``nxp,enet-qos-mdio``、``nxp,s32-gmac-mdio``、``st,stm32-mdio`` 和 ``wch,mdio`` 已替换为 :dtcompatible:`snps,dwmac-mdio`。（:github:`114899`）

* NXP ENET-QOS 以太网控制器（:dtcompatible:`nxp,enet-qos`）的设备树结构已扁平化，以与其他类似控制器保持一致。时钟、中断、``pinctrl-0``、``pinctrl-names``、``phy-handle`` 和 MAC 地址属性现在直接位于父 ``nxp,enet-qos`` 节点上，而不再位于单独的 MAC 子节点上。``nxp,enet-qos-mac`` 兼容字符串及其 ``enet_mac`` 节点已被移除。使用该控制器的树外开发板必须将这些属性从旧的 ``enet_mac`` 节点移到 ``enet`` 节点。（:github:`115952`）

* Kconfig 选项 ``CONFIG_ETH_NXP_ENET_QOS_MAC_UNIQUE_MAC_ADDRESS`` 已重命名为 :kconfig:option:`CONFIG_ETH_NXP_ENET_QOS_UNIQUE_MAC_ADDRESS`。设置旧名称的配置必须更新为使用新名称。（:github:`115952`）

* Synopsys DesignWare MAC 驱动现在默认过滤组播（:kconfig:option:`CONFIG_ETH_DWC_ETHER_MULTICAST_FILTER`），因此只会接收到网络协议栈已加入的地址的组播。若要像以前一样接收所有组播，请禁用该选项。（:github:`113235`）

* 带以太网接口的开发板现在应默认启用 :kconfig:option:`CONFIG_ETH_DRIVER`，而不是 :kconfig:option:`CONFIG_NET_L2_ETHERNET`。后者现在会在前者启用时默认启用。（:github:`117121`）

传感器
======

* :dtcompatible:`pixart,paa3905` 驱动现在强制遵循传感器数据手册中的 SPI 约定：模式 3 由驱动设置，设备树中 ``spi-max-frequency`` 超过 2 MHz 会导致构建失败。对总线超频的树外开发板必须将该属性降低到 2000000 或更小。

* :dtcompatible:`microchip,xec-tach` 的 ``girqs`` 和 ``pcrs`` 属性（数组类型）已由 ``pcr-scr`` 属性（int 类型）取代，以便使用编码了 PCR 寄存器索引和位位置的宏。GIRQ 配置现在通过 ``microchip,dmec-ecia-girq`` 绑定包含文件处理（:github:`104808`）。
* :dtcompatible:`st,lps22hh` 现在忽略 ``odr`` 属性，改用单次采样模式，除非启用 :kconfig:option:`CONFIG_LPS22HH_TRIGGER` 以使用周期性采样。

* 设备树 compatible ``tdk,ntcg163jf103ft1`` 已重命名为 :dtcompatible:`tdk,ntcgxx3jx103x`，因为按照器件命名规则，电阻 (R25) 和 beta (B25/85) 值相同的 TDK NTCG 热敏电阻器件具有相同的补偿值（:github:`110123`）。

* :dtcompatible:`nxp,mcux-qdc` 现在通过通用的 :ref:`mux <mux_api>` 子系统路由其输入信号。``input-channels`` 和 ``inputmux-connections`` 属性已被移除；请改用 mux 控制器节点（例如 :dtcompatible:`nxp,inputmux`）描述该路由，并改为从解码器节点的 ``mux-states`` 属性引用它。（:github:`112088`）

* :dtcompatible:`nxp,mcux-qdec` 现在通过通用的 :ref:`mux <mux_api>` 子系统路由其输入信号。``xbar`` 属性已被移除；请改用 mux 控制器节点（例如 :dtcompatible:`nxp,mcux-xbar`）描述该路由，并改为从解码器节点的 ``mux-states`` 属性引用它。（:github:`112088`）

* :dtcompatible:`avago,apds9960` 的 ``pgain``、``again``、``ppulse-length`` 和 ``pled-boost`` 属性过去以十六进制形式 (``0x00``/``0x01``/``0x10``/``0x11``) 表示其所选的 2 位寄存器字段，现在改为采用所选的物理值：``pgain`` 为 ``1``/``2``/``4``/``8``，``again`` 为 ``1``/``4``/``16``/``64``，表示增益倍数；``ppulse-length`` 为 ``4``/``8``/``16``/``32``，单位为微秒；``pled-boost`` 为 ``100``/``150``/``200``/``300``，单位为百分比。大多数旧值会被新的枚举拒绝，但 ``pgain = <0x01>`` 和 ``again = <0x01>`` 仍可构建，且现在选择的是 1 倍而不是 2 倍和 4 倍，因此请显式更新它们。未设置这些属性的节点不受影响（:github:`116079`）。

存储
====

* :c:struct:`flash_sector` 的 ``fs_off`` 元素已从 ``off_t`` 类型改为 ``ptrdiff_t``。这应使所有平台和工具链都使用原生机器寄存器宽度，而不再随从 C 库继承的 POSIX ``off_t`` 类型而变化。Picolibc 1.8.12 即使在 32 位平台上也将 ``off_t`` 定义为 64 位整数；此更改在使用该 C 库时可让结构体实际上恢复为之前的布局。对于较旧的 Picolibc 版本以及所有其他受支持的 C 库，``ptrdiff_t`` 与 ``off_t`` 使用相同的底层 C 类型；此更改旨在 Picolibc 更新过程中保持 ``fs_off`` 所用的底层 C 类型不变。

定时器
======

* :c:func:`sys_clock_set_timeout`、:c:func:`sys_clock_announce` 和 :c:func:`sys_clock_announce_locked` 现在将其时钟节拍计数作为无符号 ``uint32_t`` 而不是有符号 ``int32_t``。树外系统定时器驱动必须相应更新其 :c:func:`sys_clock_set_timeout` 定义，否则构建会因类型冲突错误而失败。内核现在还会将请求的超时上限设为 ``SYS_CLOCK_MAX_WAIT``，并且不再向驱动传递 ``K_TICKS_FOREVER``，因此这类驱动不再需要根据 :c:func:`sys_clock_announce` 的范围来钳制请求，也不必对 ``K_TICKS_FOREVER`` 做特殊处理；只有它们自身的硬件周期计数限制仍需强制执行（:github:`111022`）。

* :c:func:`sys_clock_set_timeout` 的 ``bool idle`` 参数已弃用。内核现在改为调用新的 :c:func:`sys_clock_idle_enter` 钩子，而不是以 ``idle=true`` 调用 :c:func:`sys_clock_set_timeout`。为保持向后兼容，:c:func:`sys_clock_idle_enter` 的默认实现会通过以 ``idle=true`` 调用 :c:func:`sys_clock_set_timeout` 来模拟旧行为，因此仍检查 ``idle`` 的定时器驱动无需更改即可继续工作。这类驱动应更新为实现 :c:func:`sys_clock_idle_enter`，并将其针对 ``idle`` 的处理移至其中。该参数将在未来的版本中移除（:github:`115844`）。

* 启用 :kconfig:option:`CONFIG_SYSTEM_CLOCK_SLOPPY_IDLE` 时，如果没有待处理的超时，内核现在会调用新的 :c:func:`sys_clock_no_timeout` 钩子，而不是以 ``ticks=K_TICKS_FOREVER`` 调用 :c:func:`sys_clock_set_timeout`。为保持向后兼容，:c:func:`sys_clock_no_timeout` 的默认实现会以 ``ticks=UINT32_MAX`` 调用 :c:func:`sys_clock_set_timeout`，二者在数值上相同，因此将此值视为“无截止时间”信号的驱动无需更改即可继续工作，无论它们是停止时钟还是设置最大等待时间。这类驱动应更新为改为实现 :c:func:`sys_clock_no_timeout`。

  注意这两个新钩子之间的分工。在 CPU 仍在运行时屏蔽唤醒应放在 :c:func:`sys_clock_no_timeout` 中，它必须保持 :c:func:`sys_clock_cycle_get_32` 正常工作。停止时基应放在 :c:func:`sys_clock_idle_enter` 中，即向其传入 ``SYS_CLOCK_IDLE_FOREVER`` 时。具体语义请参阅 :ref:`系统定时器驱动程序 <system_timer_drivers>`。（:github:`115844`）

* 无滴答（tickless）系统定时器驱动不应再自行处理时钟节拍。实现头文件 :file:`drivers/timer/system_timer_generic.h` 现在负责以往由每个驱动手工重新实现且常有细微错误的核算工作：周期到节拍的转换、announce 基准、按节拍对齐的截止时间计算以及计数器范围钳制，包括窄计数器的回绕处理。驱动只需实现少量周期域原语，即一次周期计数器读取加上一次绝对比较的 arm 操作，并包含一次该头文件；该头文件会生成 :c:func:`sys_clock_set_timeout`、:c:func:`sys_clock_elapsed` 以及 :c:func:`sys_clock_cycle_get_32` / :c:func:`sys_clock_cycle_get_64` （:github:`115844`）。

* 启用 :kconfig:option:`SYSTEM_TIMER_LPM_COMPANION_COUNTER` 时，由 :ref:`通用 chosen <devicetree-zephyr-chosen-nodes>` ``zephyr,system-timer-companion`` 选择的低功耗伴随计数器会在构建时进行检查，并且必须可用作唤醒源。如果这些节点尚未包含 ``wakeup-source`` 属性，则应添加该属性，以表明它们可用作唤醒源。（:github:`117274`）

  .. note::

    在以前的 Zephyr 版本中本就预期会有此行为，但从未进行断言检查。

控制器局域网（CAN）
===================

* NXP SJA1000（``can_sja1000.h``）和 Bosch M_CAN（``can_mcan.h``）CAN 控制器驱动后端的头文件已改为库专用的 include。基于这些后端的树外驱动需要相应更新其 include 指令。

* Bosch M_CAN 驱动现在仅使用 RX FIFO0 处理接收到的 CAN 帧，确保这些帧按总线上接收的顺序处理。树外用户可能希望更新任何 ``bosch,mram-cfg`` 设备树属性覆盖，将所有 FIFO 元素分配给 RX FIFO0。

* 已弃用的 ``bus-speed`` 和 ``bus-speed-data`` CAN 控制器设备树属性已移除。请改用 ``bitrate`` 和 ``bitrate-data``。

* CAN 控制器驱动操作不再包含 ``can_set_state_change_callback_t`` 函数指针，因为添加和移除回调现在通过通用的 :c:func:`can_add_state_change_callback` 和 :c:func:`can_remove_state_change_callback` API 函数处理。树外驱动可以完全移除该驱动操作，也可以按需将其替换为 ``can_state_change_callbacks_enabled_t``。驱动现在必须使用 :c:func:`can_fire_state_change_callbacks` 来触发 CAN 控制器状态变化回调（:github:`117889`）。

数字麦克风
==========

* DMIC 驱动后端 API 现在使用 :c:struct:`dmic_driver_api`，而不再使用 ``struct _dmic_ops``。

  树外的 DMIC 驱动必须重命名其后端 API 结构体定义，并将其 API 实例改为 ``DEVICE_API(dmic, ...)``。有关树内驱动如何更新的示例，请参见 :github:`107695`。使用 :c:func:`dmic_configure`、:c:func:`dmic_trigger` 和 :c:func:`dmic_read` 的应用代码不受影响。

时钟控制
========

* Nordic 的 Kconfig 选项 ``CONFIG_NRFS_LOCAL_DOMAIN_DVFS_SCALE_DOWN_AFTER_INIT`` 已移除。请改用 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_HSFLL_LOCAL_REQ_LOW_FREQ`。

* :dtcompatible:`nxp,imxrt11xx-arm-pll` 绑定现在使用 ``loop-div`` 和 ``post-div`` 进行 ARM PLL 配置。旧有的 ``clock-mult`` 和 ``clock-div`` 属性仍然受支持，但已弃用。现有的 RT11xx overlay 应按映射 ``loop-div = clock-mult * 2`` 和 ``post-div = clock-div`` 进行更新。

* SiWx91x 时钟控制已拆分为三个管理器（:dtcompatible:`silabs,siwx91x-cmu-aon`、:dtcompatible:`silabs,siwx91x-cmu-ulp`、:dtcompatible:`silabs,siwx91x-cmu-hp`）。旧的 :dtcompatible:`silabs,siwx91x-clock` 绑定和 ``clock0`` 节点已移除。树外开发板和 overlay 必须将 ``clocks`` phandle 更新为对应的 CMU，并使用 ``siwx91x-clock.h`` 中更新后的 ``SIWX91X_CLK_*`` ID。例如， ``clocks = <&clock0 SIWX91X_CLK_UART0>;`` 将变为 ``clocks = <&cmu_hp SIWX91X_CLK_UART0>;``。

时钟控制 nrf 弃用
-----------------

.. toggle::

   :ref:`clock_control_api` 驱动已针对 nRF52、nRF53、nRF91 和 nRF54L 系列设备上的以下时钟完成更新：

   * HFCLK
   * LFCLK
   * XO
   * XO24M
   * HFCLK192M
   * HFCLKAUDIO

   要恢复旧版驱动实现，请将 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF` 设置为 ``y``。

   要将代码从 zephyr v4.4.0 迁移到 zephyr v4.5.0，请完成以下步骤：

   1. 在应用专用或开发板专用的设备树 overlay 文件中启用每个由应用控制的时钟。

      这会启用相应的时钟驱动。例如：

      .. code-block:: dts

          /* if nRF54L XO is to be controlled */
          &xo {
              status = "okay";
          };

          /* if nRF52, nRF53 HFCLK is to be controlled */
          &hfclk {
              status = "okay";
          };

          /* if nRF52, nRF53, nRF91 or nRF54L LFCLK is to be controlled */
          &lfclk {
              status = "okay";
          };

          /* if HFCLK192M is to be controlled */
          &hfclk192m {
              status = "okay";
          };

          /* if XO24M is to be controlled */
          &xo24m {
              status = "okay";
          };

          /* if HFCLKAUDIO is to be controlled */
          &hfclkaudio {
              status = "okay";
          };

   #. 重命名以下 Kconfig 选项：

      * 将 :kconfig:option:`CONFIG_NRFX_CLOCK_USE_LFRC_CALIBRATION` 替换为 :kconfig:option:`CONFIG_NRFX_CLOCK_LFCLK_USE_LFRC_CALIBRATION`。
      * 将 :kconfig:option:`CONFIG_NRFX_CLOCK_LF_CAL_ENABLED` 替换为 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_K32SRC_RC_CALIBRATION`。

   #. 将以下 Kconfig 选项移到 ``nordic,nrf-clock-lfclk`` 设备树节点：

      * 将 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_K32SRC_FREQUENCY` 替换为 ``k32src-frequency`` 属性。
      * 将 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_SOURCE` choice 替换为 ``k32src`` 枚举属性。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_RC` 和 :kconfig:option:`NRFX_CLOCK_LF_SRC_RC` 替换为 ``k32src = "rc"``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_XTAL` 和 :kconfig:option:`NRFX_CLOCK_LF_SRC_XTAL` 替换为 ``k32src = "xtal"``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_SYNTH` 和 :kconfig:option:`NRFX_CLOCK_LF_SRC_SYNTH` 替换为 ``k32src = "synth"``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_EXT_LOW_SWING` 和 :kconfig:option:`NRFX_CLOCK_LF_SRC_LOW_SWING` 替换为 ``k32src = "ext_low_swing"``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_EXT_FULL_SWING` 和 :kconfig:option:`NRFX_CLOCK_LF_SRC_FULL_SWING` 替换为 ``k32src = "ext_full_swing"``。
      * 将 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_ACCURACY_PPM` choice 替换为 ``k32src-accuracy-ppm`` 枚举属性。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_500PPM` 替换为 ``k32src-accuracy-ppm = <500>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_250PPM` 替换为 ``k32src-accuracy-ppm = <250>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_150PPM` 替换为 ``k32src-accuracy-ppm = <150>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_100PPM` 替换为 ``k32src-accuracy-ppm = <100>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_75PPM` 替换为 ``k32src-accuracy-ppm = <75>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_50PPM` 替换为 ``k32src-accuracy-ppm = <50>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_30PPM` 替换为 ``k32src-accuracy-ppm = <30>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_20PPM` 替换为 ``k32src-accuracy-ppm = <20>``。
      * 将 :kconfig:option:`CONFIG_NRFX_CLOCK_LFXO_TWO_STAGE_ENABLED` 替换为 ``k32src = "xtal"``、``k32src = "ext_low_swing"`` 或 ``k32src = "ext_full_swing"``。

   #. 更新应用以使用新的时钟控制 API。

      更新 API 调用时请使用以下映射：

      * ``mgr`` 是为 ``nordic,nrf-clock`` 创建的通断管理器，通过 ``z_nrf_clock_control_get_onoff`` 获取。
      * ``dev`` 是与 ``nordic,nrf-clock`` 兼容的设备。
      * ``sys`` 是 ``nordic,nrf-clock`` 的子系统。
         新的时钟实现不使用它。
      * ``new_dev`` 是与之前使用的 ``sys`` 值相对应的设备。它必须与以下节点之一兼容：

        * ``nordic,nrf-clock-lfclk``
        * ``nordic,nrf-clock-hfclk``
        * ``nordic,nrf-clock-xo``
        * ``nordic,nrf-clock-hfclk192m``
        * ``nordic,nrf-clock-xo24m``
        * ``nordic,nrf-clock-hfclkaudio``

      以下示例展示了已弃用的 API 用法和对应的新 API 用法：

      .. code-block:: c

         // Old API usage (deprecated)
         z_nrf_clock_calibration_init(&mgrs);    //1
         onoff_release(mgr)                      //2
         onoff_request(mgr, &cli);               //3
         onoff_cancel_or_release(mgr, &cli);     //4
         clock_control_on(dev,sys)               //5
         clock_control_off(dev,sys)              //6
         clock_control_async_on(dev,sys)         //7
         clock_control_get_status(dev,sys)       //8
         z_nrf_clock_control_get_onoff(sys)      //9

         // New API usage
         z_nrf_clock_calibration_init();                             //1
         nrf_clock_control_release(new_dev, NULL);                   //2
         nrf_clock_control_request(new_dev, NULL, &cli);             //3
         nrf_clock_control_cancel_or_release(new_dev, NULL, &cli);   //4
         clock_control_on(new_dev, NULL)                             //5
         clock_control_off(new_dev, NULL)                            //6
         clock_control_async_on(new_dev, NULL)                       //7
         clock_control_get_status(new_dev, NULL)                     //8
         // Remove all uses of z_nrf_clock_control_get_onoff         //9

显示
====

* 用于 SDL 显示像素格式选择的 Kconfig 选项 ``CONFIG_SDL_DISPLAY_DEFAULT_PIXEL_FORMAT_*`` 已移除，改为使用 :zephyr_file:`include/zephyr/dt-bindings/display/panel.h` 中的 PANEL_PIXEL_FORMAT_* 宏，在设备树中直接为 SDL 伪设备节点设置像素格式属性。（:github:`104099`）

* LVGL 的 ``CONFIG_LV_Z_COLOR_24_BGR_TO_RGB`` Kconfig 选项已移除。LVGL 的 RGB888 颜色格式在内存中按蓝、绿、红的顺序存储字节，这与 :c:enumerator:`PIXEL_FORMAT_RGB_888` 的内存布局一致，因此对于报告该格式的显示器不再进行通道交换。帧缓冲反而期望红、绿、蓝字节顺序的显示器，现在必须报告 :c:enumerator:`PIXEL_FORMAT_BGR_888`，LVGL 适配层会为其自动执行红/蓝通道交换。

* LVGL 现在对报告 :c:enumerator:`PIXEL_FORMAT_RGB_565X` 的显示器直接以其 ``RGB565_SWAPPED`` 颜色格式渲染，因此这些显示器不再需要 :kconfig:option:`CONFIG_LV_COLOR_16_SWAP`，并且不得与该像素格式一起启用，否则缓冲区会被交换两次字节序。``t_deck``、``m5stack_core2`` 和 ``wio_terminal`` 开发板不再默认启用该选项。

* 用于 ST7305 和 ST7306 显示器的 Kconfig 选项 ``CONFIG_ST730X_POWERMODE_LOW`` 已移除，改为在设备节点上切换 low-power-mode 属性。

* ST7567 显示驱动的 ``set_contrast`` 函数现在期望的对比度值范围为 0-255，而不是 0-63。驱动现在会将值缩放到控制器期望的 6 位范围。``CONFIG_ST7567_DEFAULT_CONTRAST`` Kconfig 选项已更新以反映新范围。（:github:`112528`）

* :dtcompatible:`raspberrypi,bcm2711-framebuffer` 现在需要 ``pixel-format`` 属性，并新增了可选的 ``red-blue-swap`` 布尔属性，用于指示面板期望 BGR 通道顺序。依赖固件协商的像素顺序来纠正通道交换的开发板也必须设置 ``red-blue-swap``。（:github:`115633`）

* ``chipone,co5300`` MIPI DSI 显示驱动不再维护内部影子帧缓冲，``pitch-align``、``addr-align`` 和 ``ext-ram`` 设备树属性已从 :dtcompatible:`chipone,co5300` 绑定中移除。之前依赖这些属性满足显示控制器对齐要求的开发板，应改为启用 :kconfig:option:`CONFIG_LV_Z_AREA_X_ALIGNMENT_WIDTH` 和 :kconfig:option:`CONFIG_LV_Z_AREA_Y_ALIGNMENT_WIDTH` （LVGL），使失效区域在传给驱动之前被舍入到所需边界。（:github:`117765`）

步进电机
========

* :dtcompatible:`adi,tmc50xx-stepper-ctrl` 和 :dtcompatible:`adi,tmc51xx-stepper-ctrl` 的 ``activate-stallguard2``、``stallguard-threshold-velocity`` 和 ``stallguard-velocity-check-interval-ms`` 属性已被移除。StallGuard 配置现在通过 :c:func:`tmc50xx_stepper_ctrl_configure_stallguard`、:c:func:`tmc51xx_stepper_ctrl_configure_stallguard` 和 :c:struct:`tmc_stallguard_settings` 在运行时完成。使用这些属性的树外驱动必须更新以移除它们。（:github:`110062`）

比较器
======

* 已弃用的、以 ``nxp,`` 为前缀的 :dtcompatible:`nxp,kinetis-acmp` 属性已移除：请改用 ``enable-pin-out``、``use-unfiltered-output``、``enable-high-speed-mode``、``filter-enable-sample``、``filter-count``、``filter-period`` 和 ``enable-window-mode``。

电量计
======

* 电量计的多种属性枚举和联合体字段已弃用，改用带明确单位后缀的新版本。应用和驱动应迁移到带单位后缀的名称。例如，``FUEL_GAUGE_CURRENT`` （``val.current``）已被 ``FUEL_GAUGE_CURRENT_UA`` （``val.current_ua``）取代。

* 驱动之前在 ``FUEL_GAUGE_CYCLE_COUNT`` 属性中报告完整充放电循环数或“1/100ths”个循环时并不一致。现在该属性统一报告完整循环数，之前报告循环小数的驱动（即 ADP5360 和 BQ27Z746）已更新为报告完整循环数。依赖旧行为的应用应进行更新。（:github:`112276`）

硬件自旋锁
==========

* ``num-locks`` 设备树属性现在是 hwspinlock 控制器绑定中标准的必需属性。每个 hwspinlock 控制器节点都必须设置它，树外绑定必须删除其自身的 ``num-locks`` ``type``/``required`` 声明。

* :c:func:`hw_spin_lock`、:c:func:`hw_spin_trylock` 和 :c:func:`hw_spin_unlock` 不再接收 ``hwspinlock_ctx_t *`` 参数；每把锁的 Zephyr 自旋锁现在位于驱动的 config 结构体中。``struct hwspinlock_context``、``hwspinlock_ctx_t``、:c:struct:`hwspinlock_dt_spec` 的 ``ctx`` 成员以及 ``HWSPINLOCK_CTX_INITIALIZER`` 已被移除。:c:func:`hw_spin_lock_dt`、:c:func:`hw_spin_trylock_dt` 和 :c:func:`hw_spin_unlock_dt` 辅助函数保持不变。因此，所有引用同一硬件自旋锁的 :c:macro:`HWSPINLOCK_DT_SPEC_GET` 实例现在共享同一个 Zephyr 自旋锁，而不再各自拥有一个。

* 硬件自旋锁驱动现在必须将 :c:struct:`hwspinlock_driver_config` 嵌入为其 config 结构体的第一个成员，使用 :c:macro:`HWSPINLOCK_COMMON_CONFIG_FROM_DT_INST` 或 :c:macro:`HWSPINLOCK_COMMON_CONFIG_FROM_DT_NODE` 初始化它，并使用 :c:macro:`HWSPINLOCK_SPINLOCK_ARRAY_DT_INST_DEFINE` 或 :c:macro:`HWSPINLOCK_SPINLOCK_ARRAY_DT_DEFINE` 声明底层自旋锁数组。``get_max_id`` 驱动操作现在是可选的：未实现时，:c:func:`hw_spinlock_get_max_id` 的默认实现返回 ``num-locks`` 设备树属性的值减 1。

磁盘
====

* :kconfig:option:`CONFIG_NVME_REQUEST_TIMEOUT` 以秒为单位记录取值范围。NVMe 请求超时路径以前在未换算的情况下将该值与 :c:func:`k_uptime_get_32` 的毫秒值进行比较，因此默认值 ``5`` 会在约 5 ms 后过期，而不是 5 秒。驱动现在会在调度和过期检查之前使用 ``MSEC_PER_SEC`` 进行换算。如果应用依赖之前的短超时行为，请检查任何非默认设置。（:github:`117809`）

视频
====

* :dtcompatible:`ovti,ov7670` 和 :dtcompatible:`ovti,ov7675` 摄像头驱动现在假定 XCLK 输入为 24 MHz 而不是之前的 6 MHz，这与 OV7670 数据手册中列出的典型 XCLK 频率一致。驱动 OV7670 或 OV7675 传感器的开发板必须相应更新其开发板级 XCLK 时钟配置。例如，``frdm_mcxn236`` 已从 ``kFRO12M_to_CLKOUT`` （除以 2 得到 6 MHz）改为 ``kFRO_HF_to_CLKOUT`` （除以 2 得到 24 MHz），而 ``frdm_mcxn947`` 保留 ``kMAIN_CLK_to_CLKOUT``，但将 CLKOUT 分频比从 25 改为 6，以得到 24 MHz。（:github:`109393`）

* ``<zephyr/drivers/video.h>`` 中的 API 现在也可以通过 ``<zephyr/video/video.h>`` 使用。（:github:`112420`）

触觉反馈
========

* ``cirrus,cs40l5x`` 兼容字符串已替换为特定于变体的兼容字符串 :dtcompatible:`cirrus,cs40l50`、:dtcompatible:`cirrus,cs40l51`、:dtcompatible:`cirrus,cs40l52` 和 :dtcompatible:`cirrus,cs40l53`。使用旧兼容字符串的应用必须相应更新其设备树节点。

* :dtcompatible:`ti,drv2605` 的 ``vib-rated-mv`` 和 ``vib-overdrive-mv`` 属性现在默认使用设备复位值 1362 mV 和 3075 mV，而不是 3200 mV。需要先前驱动电平的开发板必须显式设置这些属性。

计数器
======

* :dtcompatible:`nxp,lpc-ctimer` 现在将其输入捕获信号通过通用 :ref:`mux <mux_api>` 子系统路由。``inputmux-connections`` 属性已移除；请改用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）描述路由，并从定时器节点的 ``mux-states`` 属性引用它。单元布局未改变，因此现有的 ``inputmux-connections = <&inputmux0 0 0x06000024>;`` 将变为 ``mux-states = <&inputmux0 0 0x06000024>;`` （:github:`112088`）

* :dtcompatible:`nxp,lptmr` 的 ``prescaler`` 属性已移除。请改用 ``prescale-glitch-filter`` 和 ``prescale-glitch-filter-bypass``。新属性是指数而不是除数：预分频器按 ``2^(prescale-glitch-filter + 1)`` 进行分频。

* :dtcompatible:`adi,max32-rtc-counter` 和 :dtcompatible:`adi,max32-wut` 现在使用共享的 ``clk_32k`` 节点进行 32 kHz 时钟源选择。时钟源现在通过 ``clk_32k`` 节点的 ``clocks`` 属性配置，而不是各外设节点中的 ``clock-source`` 属性（:github:`117709`）。

设备树
======

* ``int`` 和 ``array`` 类型的设备树属性，如果其 DTS 源使用负字面量（例如 ``<(-1)>``），现在会展开为负值，而不是之前使用的二进制补码无符号值。依赖旧无符号表示形式的代码，例如无符号比较或 ``BUILD_ASSERT(DT_PROP(node, foo) > 0, ...)`` 检查，必须改为使用有符号类型或能识别符号的检查（:github:`107271`）。

* ``zephyr,memory-region-mpu`` 属性已移除。请改用 ``zephyr,memory-attr``。它接受整数位掩码，而不是字符串：

  .. code-block:: none

     "RAM"         -> <DT_MEM_ARM_MPU_RAM>
     "RAM_NOCACHE" -> <DT_MEM_ARM_MPU_RAM_NOCACHE>
     "FLASH"       -> <DT_MEM_ARM_MPU_FLASH>
     "PPB"         -> <DT_MEM_ARM_MPU_PPB>
     "IO"          -> <DT_MEM_ARM_MPU_IO>
     "EXTMEM"      -> <DT_MEM_ARM_MPU_EXTMEM>

输入
====

* :dtcompatible:`gpio-keys` 的 ``no-disconnect`` 属性已由枚举属性 ``zephyr,suspend-action`` 取代。新属性目前有三个取值，其中两个直接替代了旧有的情形：

    * ``zephyr,suspend-action = "none";`` 用于替代存在 ``no-disconnect`` 时的行为。使用 ``no-disconnect`` 属性的用户应将其替换为 ``zephyr,suspend-action = "none";``。

    * ``zephyr,suspend-action = "disconnect-with-pupd";`` 用于替代未出现 ``no-disconnect`` 时的行为。为与先前行为保持向后兼容，默认选用该取值。

    * ``zephyr,suspend-action = "full-disconnect";`` 是一个新增取值。（更多细节请参阅 :dtcompatible:`绑定 <gpio-keys>`）

  建议使用默认配置的用户重新考虑该配置是否真的合适；推荐迁移到 ``zephyr,suspend-action = "full-disconnect";``。（:github:`108294`）

* ft6146、ft5336 和 cst8xx 输入驱动的 Kconfig 选项已重命名，以与其他输入驱动保持一致。使用以下 Kconfig 选项的应用必须相应更新其配置：

  * ``CONFIG_INPUT_FT5336_PERIOD`` → :kconfig:option:`CONFIG_INPUT_FT5336_PERIOD_MS`
  * ``CONFIG_INPUT_CST8XX_PERIOD`` → :kconfig:option:`CONFIG_INPUT_CST8XX_PERIOD_MS`
  * ``CONFIG_INPUT_FT6146_PERIOD`` → :kconfig:option:`CONFIG_INPUT_FT6146_PERIOD_MS`

  * Nunchuk 驱动在按键事件中错误地报告了 ``INPUT_KEY_Z`` 和 ``INPUT_KEY_C``。此问题已修复，现在使用 ``INPUT_BTN_Z`` 和 ``INPUT_BTN_C``。

邮箱
====

* :dtcompatible:`renesas,rz-mhu-mbox` 驱动经过重构，现在由单个 MHU 单元在一个 MBOX 通道上同时处理 TX 和 RX，而不是让每个通道专用于一个方向。现在一个驱动实例可以拥有多个通道。使用该兼容字符串的设备树节点必须更新：

  * ``channel`` 已重命名为 ``unit``，因为它索引的是底层 MHU 硬件单元，而不是 MBOX 通道。这两种编号方案相互独立。
  * ``tx-mask`` 和 ``rx-mask`` 已替换为单个 ``channel-mask``，即有效 MBOX 通道的位掩码，其中 ``n`` 位对应通道 ``n``，置位即启用。
  * ``channels-count`` 必须与节点上 ``interrupt-names`` 条目的数量一致。现在会在构建时进行强制检查。
  * ``shared-memory`` 现在是可选的，大多数情况下应保持不设置。共享内存改由名为 ``mhu_shmem`` 的单个 ``zephyr,memory-region`` 节点提供，该节点取代了每个单元各自的 ``mmio-sram`` 节点，并使链接器为 FSP MHU 驱动生成 ``__mhu_shmem_start``。没有该内存区域的开发板会因该符号未定义而链接失败。

  例如：

  .. code-block:: devicetree

     /* Before */
     mhu3_shm: memory@62f01018 {
             compatible = "mmio-sram";
             reg = <0x62f01018 0x8>;
     };

     mbox3: mhu@40400060 {
             channel = <3>;
             tx-mask = <0x00000002>;
             rx-mask = <0x00000001>;
             shared-memory = <&mhu3_shm>;
     };

     /* After */
     mhu_shmem: memory-region@62f01000 {
             compatible = "zephyr,memory-region";
             reg = <0x62f01000 0x1000>;
             zephyr,memory-region = "mhu_shmem";
     };

     mbox3: mhu@40400060 {
             unit = <3>;
             channel-mask = <0x1>;
     };

音频编解码器
============

* 音频编解码器驱动后端 API 现在使用 :c:struct:`audio_codec_driver_api`，而不再使用 ``struct audio_codec_api``。

  树外的音频编解码器驱动必须重命名其后端 API 结构体定义，并将其 API 实例改为 ``DEVICE_API(audio_codec, ...)``。有关树内驱动如何更新的示例，请参见 :github:`110631`。使用 ``audio_codec_...`` API 的应用代码不受影响。

.. zephyr-keep-sorted-stop

蓝牙
****

蓝牙音频
========

.. zephyr-keep-sorted-start re(^\* \w)

* BAP

  * :c:member:`bt_bap_stream.codec_cfg` 现在为 ``const``，以更好地反映它是一个只读值。任何非读取用途都需要使用相应操作更新，例如 :c:func:`bt_bap_stream_config`、:c:func:`bt_bap_stream_reconfig`、:c:func:`bt_bap_stream_enable` 或 :c:func:`bt_bap_stream_metadata`。(:github:`104219`)
  * :c:member:`bt_bap_stream.qos` 现在为 ``const``，以更好地反映它是一个只读值。任何非读取用途都需要使用相应操作设置，例如 :c:func:`bt_bap_unicast_group_create`、:c:func:`bt_bap_unicast_group_reconfig`、:c:func:`bt_bap_broadcast_source_create` 或 :c:func:`bt_bap_broadcast_source_reconfig`。(:github:`104887`)
  * 几乎所有使用 ``struct bt_bap_qos_cfg *`` 的 API 现在都使用 ``const``，这意味着一旦 ``qos`` 被存储到参数结构体（如 :c:struct:`bt_bap_broadcast_source_param` 或 :c:struct:`bt_bap_unicast_group_stream_param`）中，就不能再通过该参数的指针修改 ``qos``，而应改为修改结构体的实际定义。(:github:`104219`)
  * :c:member:`bt_bap_unicast_group_info.sink_pd` 和 :c:member:`bt_bap_unicast_group_info.source_pd` 现在反映为该组定义的本地值，而不是为任何远端 ASE 配置的值。(:github:`104887`)
  * :c:func:`bt_bap_unicast_client_discover` 和 :c:func:`bt_bap_broadcast_assistant_discover` 现在要求连接已经过配对过程，并在进行任何发现之前满足 BAP 的安全要求。在大多数情况下，这需要对新的设备调用 :c:func:`bt_conn_set_security`。重新连接的已绑定设备不应需要任何操作。
  * 几乎所有使用 ``struct bt_audio_codec_cfg *`` 的 API 现在都使用 ``const``，这意味着一旦 ``codec_cfg`` 被存储到参数结构体（如 :c:struct:`bt_bap_stream` 或 :c:struct:`bt_bap_broadcast_source_subgroup_param`）中，就不能再通过该参数的指针修改 ``codec_cfg``，而应改为修改结构体的实际定义。(:github:`104219`)
  * 所有 BAP 角色现在都要求 :kconfig:option:`CONFIG_BT_AUDIO_CODEC_CFG_MAX_DATA_SIZE` 至少为 19 个八位组，这是 BAP 规范的要求。如果在与 BAP 一起使用时 :kconfig:option:`CONFIG_BT_AUDIO_CODEC_CFG_MAX_DATA_SIZE` 被设置为更小的值，则应用需要将其设置为至少 19 个八位组。受影响的 Kconfig 选项如下：

    * :kconfig:option:`CONFIG_BT_ASCS`
    * :kconfig:option:`CONFIG_BT_BAP_UNICAST_SERVER`
    * :kconfig:option:`CONFIG_BT_BAP_UNICAST_CLIENT`
    * :kconfig:option:`CONFIG_BT_BAP_BROADCAST_SOURCE`
    * :kconfig:option:`CONFIG_BT_BAP_BROADCAST_SINK`
    * :kconfig:option:`CONFIG_BT_BAP_SCAN_DELEGATOR`
    * :kconfig:option:`CONFIG_BT_BAP_BROADCAST_ASSISTANT`

    (:github:`107989`)
  * :zephyr:code-sample:`bluetooth_bap_broadcast_assistant`、:zephyr:code-sample:`bluetooth_bap_broadcast_sink`、:zephyr:code-sample:`bluetooth_bap_broadcast_source`、:zephyr:code-sample:`bluetooth_bap_unicast_client` 和 :zephyr:code-sample:`bluetooth_bap_unicast_server` 已从 :zephyr_file:`samples/bluetooth/` 移至 :zephyr_file:`samples/bluetooth/audio`。
  * ``bt_bap_stream_ops.configured`` 已重命名为 :c:member:`bt_bap_stream_ops.codec_configured`，``bt_bap_stream_ops.qos_set`` 已重命名为 :c:member:`bt_bap_stream_ops.qos_configured`，以使其名称与 ASCS 规范定义的 ASE 状态保持一致。回调签名及其调用条件均未改变，因此应用只需在分配回调的位置将 ``configured`` 搜索替换为 ``codec_configured``，并将 ``qos_set`` 搜索替换为 ``qos_configured``。(:github:`114835`)

  * :c:func:`bt_bap_scan_delegator_mod_src` 不再将 ``metadata_len = 0`` 视为“保留现有值”，现在会将子组的元数据长度设置为 0。若要保留现有数据，需要将 ``metadata_len`` 字段设置为现有长度，并复制现有元数据。

* CAP

  * :c:func:`bt_cap_commander_broadcast_reception_start` 现在会等待 CAP 接受器同步到广播后再完成。这意味着广播源必须处于活动状态，包括由 :c:func:`bt_cap_handover_unicast_to_broadcast` 创建的共置广播源，并启用周期性广播且配置好 BASE。对于 :c:func:`bt_cap_handover_unicast_to_broadcast`，可以使用新增的 :c:member:`bt_cap_handover_cb.unicast_to_broadcast_created` 来配置 BASE。这也意味着，应用为实现等待指示同步成功的接收状态更新而做的任何现有检查都可以移除，因为 :c:func:`bt_cap_commander_broadcast_reception_start` 现在会在调用 :c:member:`bt_cap_commander_cb.broadcast_reception_start` 时确保这一点。类似规则也适用于 :c:func:`bt_cap_commander_broadcast_reception_stop`。(:github:`101070`)
  * :zephyr:code-sample:`bluetooth_cap_acceptor`、:zephyr:code-sample:`bluetooth_cap_handover` 和 :zephyr:code-sample:`bluetooth_cap_initiator` 已从 ``samples/bluetooth/`` 移至 ``samples/bluetooth/audio``。
  * :c:func:`bt_cap_initiator_unicast_audio_update` 现在会在 API 调用不会导致任何状态变化时拒绝该调用（即参数中的元数据与服务器报告给我们的元数据相同），并返回 ``-EALREADY``。

* CCP

  * :c:member:`bt_tbs_client_cb.technology` 已将 ``value`` 参数的类型从 ``uint32_t`` 改为 ``enum bt_bearer_tech``。使用该回调的应用应改用新的类型。(:github:`102430`)
  * 所有 ``BT_TBS_TECHNOLOGY_*`` 值（例如 ``BT_TBS_TECHNOLOGY_3G``）都已重命名为 ``BT_BEARER_TECH_*``，例如 ``BT_BEARER_TECH_3G``。应用可以执行从 ``BT_TBS_TECHNOLOGY`` 到 ``BT_BEARER_TECH`` 的搜索替换。此外，这些值现在定义在 :zephyr_file:`include/zephyr/bluetooth/assigned_numbers.h` 中，而不是 :zephyr_file:`include/zephyr/bluetooth/audio/tbs.h` 中。(:github:`102430`)
  * ``bt_tbs_register_param.supported_features`` 已重命名为 :c:member:`bt_tbs_register_param.optional_opcodes`。应用可以对 ``supported_features`` 到 ``optional_opcodes`` 执行简单的搜索替换。此外，``BT_TBS_FEATURE_*`` 宏已改为 ``BT_TBS_OPTIONAL_OPCODE_*``。应用可以对 ``BT_TBS_FEATURE_`` 到 ``BT_TBS_OPTIONAL_OPCODE_`` 执行简单的搜索替换。(:github:`103350`)
  * :zephyr:code-sample:`bluetooth_ccp_call_control_client` 和 :zephyr:code-sample:`bluetooth_ccp_call_control_server` 已从 ``samples/bluetooth/`` 移至 ``samples/bluetooth/audio``。

* CSIP

  * 可选的 CSIS 特征现在可通过 Kconfig 配置，并且必须显式启用：

    * 协调集合大小 → :kconfig:option:`CONFIG_BT_CSIP_SET_MEMBER_SIZE_SUPPORT`
    * 集合成员锁定 → :kconfig:option:`CONFIG_BT_CSIP_SET_MEMBER_LOCK_SUPPORT`
    * 集合成员排名 → :kconfig:option:`CONFIG_BT_CSIP_SET_MEMBER_RANK_SUPPORT`

* HAP

  * :zephyr:code-sample:`bluetooth_hap_ha` 已从 ``samples/bluetooth/`` 移至 ``samples/bluetooth/audio``。

* PBP

  * :zephyr:code-sample:`bluetooth_public_broadcast_sink` 和 :zephyr:code-sample:`bluetooth_public_broadcast_source` 已从 ``samples/bluetooth/`` 移至 ``samples/bluetooth/audio``。

* TMAP

  * :zephyr:code-sample:`ble_peripheral_tmap_bmr`、:zephyr:code-sample:`ble_peripheral_tmap_bms`、:zephyr:code-sample:`ble_peripheral_tmap_central` 和 :zephyr:code-sample:`ble_peripheral_tmap_peripheral` 已从 ``samples/bluetooth/`` 移至 ``samples/bluetooth/audio``。

* VOCS

  * VOCS 客户端现在要求自动发现 CCC（客户端特征配置）。:kconfig:option:`CONFIG_BT_VOCS_CLIENT` 现在依赖 :kconfig:option:`CONFIG_BT_GATT_AUTO_DISCOVER_CCC`。使用 VOCS 客户端的应用必须确保已启用 CCC 自动发现支持。(:github:`110607`)

.. zephyr-keep-sorted-stop

蓝牙经典
========

* :c:struct:`bt_conn_cb` 中针对 BR/EDR 的专用回调 ``role_changed`` 和 ``br_mode_changed`` 已移至新的子结构体 :c:struct:`bt_conn_br_cb`，可通过 ``br`` 成员访问。使用这些回调的应用代码必须更新指定初始化器：

  * ``.role_changed`` → ``.br.role_changed``
  * ``.br_mode_changed`` → ``.br.mode_changed``

  (:github:`108022`)

* 已将 ``CONFIG_BT_DEVICE_VEDNOR_ID`` 重命名为 :kconfig:option:`CONFIG_BT_DEVICE_VENDOR_ID`，以修正拼写错误。

* :c:member:`bt_rfcomm_dlc_ops.recv` 的回调签名已从 ``void`` 改为 ``int``。现有实现必须更新为返回 ``0`` 以保持以前的同步行为，或返回 ``-EINPROGRESS`` 以使用新的异步完成路径。

蓝牙 HCI
========

* 设备树 compatible ``bflb,bl70x-bt-hci`` 已重命名为 :dtcompatible:`bflb,bt-hci`，因为现在单个绑定即可覆盖所有 Bouffalo Lab 片上 BLE 控制器（BL60x/BL70x/BL70XL）。树外开发板和扩展板必须相应更新其设备树节点。

* 蓝牙 HCI 驱动现在必须在其 data（:c:struct:`bt_hci_driver_data`）和 config（:c:struct:`bt_hci_driver_config`）结构体的第一个字段中提供一个必需的公共结构体。

* :c:member:`bt_hci_driver_api.open` 回调不再有 ``recv`` 参数；公共 HCI 驱动层代码改为在公共数据结构体中管理该参数。新增了 :c:func:`bt_hci_recv` API，供驱动将数据传递给上层（例如蓝牙主机栈）。对于需要访问 recv() 错误的驱动（大多数驱动并不需要），还新增了 :c:func:`bt_hci_recv_err` API；在发生错误时，它把释放缓冲区引用的责任留给调用者。

* :kconfig:option:`CONFIG_BT_HCI_SET_PUBLIC_ADDR` 不再选择 :kconfig:option:`CONFIG_BT_HCI_SETUP`。在 ``setup()`` 实现中应用公共地址的树外 HCI 驱动现在必须自行选择 :kconfig:option:`CONFIG_BT_HCI_SETUP`；否则，``setup`` 成员不会存在于 :c:struct:`bt_hci_driver_api` 中，回调也不会被调用。现在，从传输层打开时起，也可以通过 :c:func:`bt_hci_get_public_addr` 获取地址，从而允许驱动在 ``open()`` 期间改为应用该地址。
* :ref:`HCI 驱动 API <bt_hci_drivers>` 现在记录了其生命周期约定。对于其使用者：:c:func:`bt_hci_open`、:c:func:`bt_hci_close` 和 :c:func:`bt_hci_send` 不能对同一设备并发调用；:c:func:`bt_hci_send` 仅在打开的传输上有效；并且不会从接收回调中调用 :c:func:`bt_hci_close`。对于驱动：``open()`` 失败会使传输保持关闭状态，且之后不会调用 ``close()``；``close()`` 失败会使传输保持打开状态；``close()`` 成功后不再调用接收回调；除 ``setup()`` 外的驱动操作不使用主机的 HCI 命令 API。树外 HCI 驱动以及直接调用 HCI 驱动 API 的树外代码，可能需要修改以遵循这些规则。

蓝牙主机
========

* :c:struct:`bt_conn_cb` 中的 ``le_param_updated`` 回调在连接参数更新失败（即 LE Connection Update Complete 事件报告非零状态）时不再被调用。以前该回调会无条件调用，报告未更改的连接参数且不给出错误指示，因而无法与更新成功区分。需要获知被拒绝的、由应用发起的参数更新的应用，应启用 :kconfig:option:`CONFIG_BT_USER_CONN_PARAM_REJECTED` 并实现新的 ``le_param_update_rejected`` 回调。

* ``CONFIG_BT_RECV_CONTEXT`` Kconfig 选择项及其选项 ``CONFIG_BT_RECV_WORKQ_SYS`` 和 ``CONFIG_BT_RECV_WORKQ_BT`` 已被移除。主机现在无条件地在专用的蓝牙 RX 工作队列上处理低优先级 HCI 数据包（即先前的 ``CONFIG_BT_RECV_WORKQ_BT`` 行为）。为节省 RAM（例如在 nRF51 上）而选择 ``CONFIG_BT_RECV_WORKQ_SYS`` 的应用必须去掉该选项；现在始终会创建专用的 RX 线程。应根据应用启用的主机功能调整 :kconfig:option:`CONFIG_BT_RX_STACK_SIZE`，即调整 RX 线程栈。由于低优先级 RX 不再在系统工作队列上运行，应用或许可以减小 :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`，但这两个栈大小都取决于具体应用，应通过栈使用量测量来验证。

* 启用 :kconfig:option:`CONFIG_BT_GATT_AUTO_READ_CENTRAL_ADDR_RES` 时（在可能的情况下为默认值），主机在创建绑定后读取一次已绑定对端的 Central Address Resolution 特征；并且当对已知不支持地址解析的对端使用 :c:enumerator:`BT_LE_ADV_OPT_DIR_ADDR_RPA` 时，:c:func:`bt_le_adv_start`、:c:func:`bt_le_ext_adv_create` 和 :c:func:`bt_le_ext_adv_update_param` 现在会失败并返回 ``-ENOTSUP``。这类对端无法解析目标地址，因此永远不会响应广播。需要提前了解情况的应用可以使用 :c:func:`bt_le_bond_addr_res_support` 读取相同的答案，并改为使用面向其对端身份地址的定向广播来连接这些对端。禁用该选项可恢复以前的行为。

* 现在，部分蓝牙主机工作项在专用的蓝牙 RX 工作队列上运行，而不是在系统工作队列上运行。因此，从这些工作项触发的应用回调会在蓝牙 RX 线程中运行。这包括连接拆除和延迟的连接工作（例如 ``disconnected()`` 连接回调和 SMP 配对超时），以及 ATT/GATT、L2CAP、AVDTP 和 HFP AG 中的超时与完成路径。曾依赖这些回调在系统工作队列中运行的应用应重新审视其同步和回调栈需求。详情请参见拉取请求 :github:`93033`。

* ``CONFIG_BT_AUTO_PHY_UPDATE`` 已被移除。请改用按角色设置的 ``BT_AUTO_PHY_CENTRAL`` 和 ``BT_AUTO_PHY_PERIPHERAL`` 选择项。``=n`` 不等同于移除该选项：central 角色选择项默认为 :kconfig:option:`CONFIG_BT_AUTO_PHY_CENTRAL_2M`，因此必须将两个角色都显式设置为 ``_NONE``。

* 已弃用的 ``CONFIG_BT_CONN_TX_MAX`` Kconfig 选项已被移除。该选项自 Zephyr 4.2 起就已弃用，带回调的挂起 TX 缓冲区数量始终由 :kconfig:option:`CONFIG_BT_BUF_ACL_TX_COUNT` 决定。

* :c:member:`bt_le_ext_adv_info.sid` 现在对传统广播集设置为 ``BT_GAP_SID_INVALID``，因为 SID 仅对扩展广播集有效。应用不应期望 :c:member:`bt_le_adv_param.sid` 会应用于传统广播集。

* :c:member:`bt_le_ext_adv_info.sid` 现在反映传递给 :c:func:`bt_le_ext_adv_update_param` 的 SID。此前即使控制器已应用新值，它仍保留来自 :c:func:`bt_le_ext_adv_create` 的值。

* :c:func:`bt_addr_le_to_str` 现在使用单字符类型前缀格式化 LE 地址：公共地址用 ``P:``，随机地址用 ``R:``，其后紧跟地址，例如 ``R:11:22:33:44:55:66``。不再生成以前的 ``11:22:33:44:55:66 (random)`` 形式；带有额外 HCI 级位的地址类型（例如 ``BT_ADDR_LE_RANDOM_ID``）按其基础类型格式化，而不再格式化为 ``(random-id)`` 或原始十六进制值。解析 Zephyr 日志或 shell 输出以提取地址的代码必须更新。相应地，:c:macro:`BT_ADDR_LE_STR_LEN` 已从 ``30`` 缩减为 ``20``。

* :c:func:`bt_addr_le_from_str` 不再接受单独的地址类型字符串。它只接受由 :c:func:`bt_addr_le_to_str` 生成的带 ``P:``/``R:`` 前缀的格式；不再支持以前 ``"XX:XX:XX:XX:XX:XX"`` 加上 ``"public"``/``"random"`` 的形式。因此，所有接受 LE 地址的蓝牙 shell 命令（例如 ``bt connect``、``bt disconnect``、``bt clear``、``bt fal-add``、``bt per-adv-sync-create``、``gatt resubscribe`` 和 ``bap_broadcast_assistant add_src``）都改为将其作为一个 ``P:XX:XX:XX:XX:XX:XX`` 或 ``R:XX:XX:XX:XX:XX:XX`` 参数接收，而不是一个地址后跟单独的类型参数。

蓝牙 Mesh
=========

* 已弃用的 ``CONFIG_BT_MESH_BLOB_IO_FLASH_WITH_ERASE`` 和 ``CONFIG_BT_MESH_BLOB_IO_FLASH_WITHOUT_ERASE`` Kconfig 选项已被移除，且没有替代选项。它们自 Zephyr 4.3 起就已弃用，当时 BLOB IO Flash 模块开始在运行时查询擦除能力，从此便一直不再有效。

蓝牙服务
========

* :kconfig:option:`CONFIG_BT_OTS_MAX_OBJ_CNT` 已从 ``hex`` 改为 ``int``，以获得更直观的类型。只需将任何十六进制值（例如 ``0x30``）改为其十进制值（例如 ``48``）。

网络
****

* HTTP 客户端响应回调（:c:type:`http_response_cb_t`）现在对单个接收缓冲区可能会被多次调用，每个正文片段调用一次，例如分块响应的每个块调用一次。假定每次接收只回调一次的应用必须追加收到的每个片段。

* ``CONFIG_NET_TEST_PROTOCOL`` 是一个 JSON 控制通道，可让树外 TTCN-3 测试套件驱动 TCP 栈并读取其内部状态；它已被移除，同时被移除的还有作为其唯一被测系统的 ``samples/net/sockets/tcp`` 示例。树内没有任何配置启用该选项，其背后的代码也已多年无法编译。使用它的测试套件已由其作者归档。

  启用该选项还会关闭初始序列号随机化，并使 ``net_tcp_connect()`` 不等待连接建立就返回，因此启用它的构建与未启用它的构建行为并不相同。

  没有替代选项，因为替代方案并不是一个选项：:zephyr_file:`tests/net/conformance` 下的一致性测试改为通过网络驱动未经改动的构建，包括覆盖相同内容的 TCP 测试套件。请参见 :ref:`ttcn3_testing`。

* 嵌套在 :c:struct:`dns_resolve_context` 中的 ``struct dns_server`` 类型已重命名为 ``struct dns_server_info``。C++ 类成员不能与其所属类同名，因此旧标签导致无法从 C++ 包含 ``<zephyr/net/dns_resolve.h>``。没有任何字段被重命名，因此诸如 ``ctx->servers[i].dns_server_addr`` 这样的访问不受影响；只有直接使用该类型名称的代码（例如在 ``CONTAINER_OF()`` 调用中）才需要更新。

* 各种与 IP 路由相关的 Kconfig 选项现在都会加上 ``IPV6`` 前缀。这样做是为了能够提供与 IPv6 路由符号功能相同、但可以单独控制的 IPv4 路由符号。

* IPv4 和 IPv6 单播路由表支持现在通过 :kconfig:option:`CONFIG_NET_IPV4_ROUTE` 和 :kconfig:option:`CONFIG_NET_IPV6_ROUTE` 选项提供。

  这些选项控制按协议族区分的单播路由表，这些路由表供静态路由管理、网络 shell 路由命令以及本机发起流量（例如发往 VPN 的数据包）的主机侧路由选择使用。它们本身不会启用接口间的数据包转发。

* Kconfig 选项 :kconfig:option:`CONFIG_NET_IPV4_ROUTING` 和 :kconfig:option:`CONFIG_NET_IPV6_ROUTING` 已重命名为 :kconfig:option:`CONFIG_NET_IPV4_FORWARDING` 和 :kconfig:option:`CONFIG_NET_IPV6_FORWARDING`。

  重命名后的选项明确表示接口间的 IP 转发。只需要路由表查询或静态路由的应用应启用 :kconfig:option:`CONFIG_NET_IPV4_ROUTE` 或 :kconfig:option:`CONFIG_NET_IPV6_ROUTE`，并保持转发功能禁用。充当路由器的应用应同时启用路由表选项和相应的转发选项。

* 树外 IPv6 配置也应不再使用已弃用的旧别名 :kconfig:option:`CONFIG_NET_ROUTE`、:kconfig:option:`CONFIG_NET_ROUTING`、:kconfig:option:`CONFIG_NET_MAX_ROUTES` 和 :kconfig:option:`CONFIG_NET_MAX_NEXTHOPS`，并直接使用 :kconfig:option:`CONFIG_NET_IPV6_*` 符号。

* ``samples/net/wifi/test_certs/rsa2k`` 企业测试证书已被移除。TF-PSA-Crypto 无法解密其经过 DES 加密的 PKCS#8 私钥。请改用 ``samples/net/wifi/test_certs/rsa2k_no_des``，或将 :envvar:`WIFI_TEST_CERTS_DIR` 设置为另一个存放 AES 加密证书的目录。

* :kconfig:option:`CONFIG_OPENTHREAD_JOINER_PSKD` 不再默认使用公开记录的 ``"J01NME"`` 凭据，现在完全没有默认值。启用 :kconfig:option:`CONFIG_OPENTHREAD_JOINER_AUTOSTART` 的构建，在配置好 6 到 32 个大写字母或数字字符（0-9 和 A-Z，但不包括 I、O、Q 和 Z）的 PSKd 之前会失败。

  通过 Kconfig 设置的 PSKd 会被编译到镜像中，因此在运行该固件的每个设备上都相同，这会让范围内的任何配网器都能将未配网设备加入自己的网络。应将该选项仅视为开发辅助手段：产品固件应从出厂数据读取每台设备各自的 PSKd，并改为由应用调用 ``otJoinerStart()``。

* ``net_if_config_get`` 因与 :c:func:`net_if_get_config` 重复而被移除。(:github:`110930`)

* ZVFS eventfd 的数量现在由 ``ZVFS_EVENTFD_SIZE`` 宏定义决定，而不再直接使用 :kconfig:option:`CONFIG_ZVFS_EVENTFD_MAX` Kconfig 选项。子系统可以通过指定以 ``CONFIG_ZVFS_EVENTFD_ADD_SIZE_`` 为前缀的 Kconfig 选项来说明自己所需的 eventfd 数量。这些数量会被汇总，并与 :kconfig:option:`CONFIG_ZVFS_EVENTFD_MAX` 比较；取两者中较大的值。若要强制使用 :kconfig:option:`CONFIG_ZVFS_EVENTFD_MAX`，即使其值小于自定义需求之和，也可以启用新增的 :kconfig:option:`CONFIG_ZVFS_EVENTFD_IGNORE_MIN` 选项（默认禁用）。因此，分配 eventfd 的网络子系统（例如 HTTP 服务器、CoAP 服务器、LwM2M、PTP、SSH、套接字服务和 WPA 请求者）不再需要应用手动调高 :kconfig:option:`CONFIG_ZVFS_EVENTFD_MAX` 来为它们预留数量。(:github:`111201`)

* :kconfig:option:`CONFIG_NET_L2_PTP` 已弃用，并由 :kconfig:option:`CONFIG_NET_L2_PTP_TIMESTAMPING` 取代。新选项更准确地描述了它所启用的功能。显式启用 :kconfig:option:`CONFIG_NET_L2_PTP` 的应用或开发板配置应改用 :kconfig:option:`CONFIG_NET_L2_PTP_TIMESTAMPING`。

* WPA 请求者默认的网络选择标准已从基于吞吐量改为基于可靠性（SNR），:kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_NW_SEL` 的 Kconfig 默认值从 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_NW_SEL_THROUGHPUT` 切换为 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_NW_SEL_RELIABILITY`。以前，高于 25 dBm 的 SNR 被视为足够好，基本上会排除在 AP 选择之外；现在始终会将 SNR 纳入考虑，从而改善嵌入式 Wi-Fi 用例的连接稳定性。需要以前行为的用户可以通过启用 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_NW_SEL_THROUGHPUT` 来恢复。

* LLMNR 支持已弃用。Kconfig 选项 :kconfig:option:`CONFIG_LLMNR_RESOLVER` 和 :kconfig:option:`CONFIG_LLMNR_RESPONDER` 将在未来版本中移除（最早为 4.7）。LLMNR（RFC 4795）正被 Microsoft 淘汰，并且在现代 Windows 上默认禁用。依赖本地名称解析的应用应迁移到 mDNS（:kconfig:option:`CONFIG_MDNS_RESOLVER` / :kconfig:option:`CONFIG_MDNS_RESPONDER`）。

* 以下 MQTT-SN 传输函数现在接受 :c:struct:`mqtt_sn_transport`，而不是 :c:struct:`mqtt_sn_client`：

  * :c:member:`mqtt_sn_transport.recvfrom`
  * :c:member:`mqtt_sn_transport.poll`
  * :c:member:`mqtt_sn_transport.sendto`

* 在调用 :c:func:`net_if_down` 时，不再从接口清除多播地址。仍会发送离开消息，但地址会保留在接口的多播列表中，并在接口重新启用时重新加入。这样应用就可以在关闭再启用接口时不丢失多播地址。(:github:`115307`)

* DHCPv4 客户端现在会在放弃租约之前触发 ``NET_EVENT_IPV4_DHCP_STOP``，而以前会在最后才触发它。在该处理函数中停止客户端并检查接口的应用，现在会看到租约地址和租约的 DNS 服务器仍然存在；它们会在处理函数返回后被移除，其中地址最后移除。应将此类工作移到 ``NET_EVENT_IPV4_ADDR_DEL`` 的处理函数，该事件现在是拆除过程的最终事件。

Ethernet
========

* :kconfig:option:`CONFIG_NET_DEFAULT_IF_ETHERNET` 现在允许获取第一个以太网接口，而不是在以太网和 Wi-Fi 之间获取第一个接口。

* 不能再使用 :kconfig:option:`CONFIG_ETH_QEMU_EXTRA_ARGS` 和 :kconfig:option:`CONFIG_NET_QEMU_USER_EXTRA_ARGS` 选项为 QEMU 以太网设备指定 MAC 地址。请改用 :kconfig:option:`CONFIG_NET_QEMU_DEVICE_EXTRA_ARGS`。这是因为我们不再使用 QEMU 的 ``-nic`` 选项，而是使用 ``-netdev`` 和 ``-device`` 选项。(:github:`107326`)

* 提供 RX 时间戳的以太网驱动现在必须在接收数据包中存储有效时间戳后调用 :c:func:`net_pkt_set_rx_timestamping`。AF_PACKET 套接字使用 :c:func:`net_pkt_is_rx_timestamping` 作为 ``SO_TIMESTAMPING`` 控制数据有效的唯一指示。仅填充 ``pkt->timestamp`` 的树外驱动必须更新，否则其 RX 时间戳不会传递给套接字应用。(:github:`110582`)

调制解调器
==========

* 蜂窝调制解调器的 chat 分隔符和过滤器现在在 :c:struct:`modem_cellular_vendor_config` 中指定，而不是在 :c:struct:`modem_cellular_data` 中。
* 蜂窝调制解调器实例的 PPP 指针现在会自动填充到 :c:struct:`modem_cellular_config` 中。必须删除对 :c:struct:`modem_cellular_data` 的赋值。
* Chat 脚本回调参数类型已更新。现在会在 ``user_data`` 参数之前插入一个新的 :c:struct:`modem_chat_script_completion_info` 指针。

PTP
===

* PTP UDP 协议 Kconfig 符号已重命名，以统一大小写：

  * :kconfig:option:`CONFIG_PTP_UDP_IPv4_PROTOCOL` → :kconfig:option:`CONFIG_PTP_UDP_IPV4_PROTOCOL`
  * :kconfig:option:`CONFIG_PTP_UDP_IPv6_PROTOCOL` → :kconfig:option:`CONFIG_PTP_UDP_IPV6_PROTOCOL`

gPTP
====

* 在 :c:struct:`ethernet_context` 中将 ``int port`` 转换为 ``uint16_t gptp_port``，以明确该字段仅供 gPTP 协议栈用于存储 gPTP 端口号。

* 根据 IEEE 1588 标准，在 :c:struct:`gptp_default_ds` 中将 ``nb_ports`` 改为 ``uint16_t``。

* 移除了 ``net_eth_get_ptp_port`` 和 ``net_eth_set_ptp_port``。可以改用新增的 :c:func:`gptp_get_port_number` 和 :c:func:`gptp_set_port_number`。

* 移除了 ``CONFIG_NET_GPTP_CLOCK_ACCURACY_*``，用户需要确保在 :kconfig:option:`CONFIG_NET_GPTP_CLOCK_ACCURACY` 中配置了正确的 gPTP 时钟精度值。

Modem
*****

SIMCOM SIM7080
==============

* 由于 NB-IoT 与 CAT-M 的可用频段略有差异，Kconfig 选项 :kconfig:option:`CONFIG_MODEM_SIMCOM_SIM7080_LTE_BANDS` 已拆分为 :kconfig:option:`CONFIG_MODEM_SIMCOM_SIM7080_LTE_BANDS_M1` 和 :kconfig:option:`CONFIG_MODEM_SIMCOM_SIM7080_LTE_BANDS_NB1`。新增配置项的类型是所选频段的十六进制位图。默认选择频段 8、20 和 28。

  配置了 :kconfig:option:`CONFIG_MODEM_SIMCOM_SIM7080_LTE_BANDS` 的应用必须更新其配置。

LoRaWAN
*******

* 原生 LoRaWAN 后端（:kconfig:option:`CONFIG_LORA_MODULE_BACKEND_NATIVE`）现在要求先调用 :c:func:`lorawan_start`，之后才会接受以下运行时配置 API：

  * 如果在启动前调用，:c:func:`lorawan_set_datarate` 和 :c:func:`lorawan_set_conf_msg_tries` 将返回 ``-EPERM``。
  * :c:func:`lorawan_enable_adr` （返回类型为 ``void``）在启动前调用时会记录一条警告并丢弃该调用。

  这些 API 以前在 :c:func:`lorawan_start` 之前锁存的配置值不再保留。在初始化期间调用这些 API 的应用必须将这些调用移到启动之后。它们仍可在 :c:func:`lorawan_join` 成功之前或之后运行。

  :c:func:`lorawan_set_channels_mask` 不受影响，在 :c:func:`lorawan_start` 之后的任意时刻仍可调用，因为信道掩码会影响 Join-Request 的信道选择本身。

  这些顺序要求不适用于 LoRaMac-node 后端（:kconfig:option:`CONFIG_LORA_MODULE_BACKEND_LORAMAC_NODE`）。

库
***

环形缓冲区
==========

环形缓冲区 API 已经过重构，以减小 :c:struct:`ring_buf` 的大小并提高簿记路径的效率。为适应这些变化，零拷贝的 claim/finish API（``ring_buf_put_claim()`` / ``ring_buf_put_finish()`` 及其 ``get`` 对应函数）已由不进行叠加的 :c:func:`ring_buf_put_ptr` 和 :c:func:`ring_buf_get_ptr` 取代。

旧版 claim/finish API 仍然可用，但仅在启用 :kconfig:option:`CONFIG_RING_BUFFER` 时才可用。新代码应直接使用 ``_ptr`` API。

启用 :kconfig:option:`CONFIG_RING_BUFFER` 会选中旧版的环形缓冲区头文件，同时还会恢复默认头文件中缺失的其他已弃用符号：整个 item API（:c:func:`ring_buf_item_init`、:c:func:`ring_buf_item_put`、:c:func:`ring_buf_item_get`、:c:func:`ring_buf_item_space_get`、``RING_BUF_ITEM_DECLARE*`` 和 ``RING_BUF_ITEM_SIZEOF``）以及 ``ring_buf_internal_reset()``。仍然使用其中任一符号的树外代码会在编译时失败且没有其他提示；启用该选项就是恢复这些符号的开关，同时可将代码迁移到 :c:struct:`sys_ringq` 和 ``_ptr`` API。

:c:func:`ring_buf_get` 在默认（精简）构建中不再接受 ``NULL`` 目标地址来丢弃数据；仅当启用 :kconfig:option:`CONFIG_RING_BUFFER` 时才容忍传入 ``NULL``。若要在没有目标缓冲区的情况下丢弃数据，可直接用 :c:func:`ring_buf_consume` 推进读索引，例如 ``ring_buf_consume(rb, MIN(count, ring_buf_size_get(rb)))``。

诸如 **先推测性写入再取消** （speculative-write-then-cancel）和 **回填** （backfilling，即在提交前修改先前写入的头部）等高级用例，现在依赖 :c:func:`ring_buf_put_ptr` 和 :c:func:`ring_buf_get_ptr` 末尾的 ``offset`` 参数。该偏移量是调用者已试探性预留的、超出当前写（或读）索引的字节数，回绕由内部处理。通过传入递增的偏移量来依次布置各个区域，同时让真正的环形缓冲区保持不变，只有在调用 :c:func:`ring_buf_commit` （或 :c:func:`ring_buf_consume`）时才会推进它。如果某一步失败，只需不提交而直接返回即可，这相当于旧版 ``ring_buf_put_finish(rb, 0)`` 的取消操作。

例如，以下 claim/finish 代码：

.. code-block:: c

   int write_pkg(struct ring_buf *rb, const uint8_t *payload, size_t payload_size)
   {
           struct hdr *h;
           uint8_t *ptr;
           uint32_t claim_size;

           claim_size = ring_buf_put_claim(rb, (uint8_t **)&h, sizeof(*h));
           if (claim_size < sizeof(*h)) {
                   ring_buf_put_finish(rb, 0);
                   return -ENOMEM;
           }

           claim_size = ring_buf_put_claim(rb, &ptr, payload_size);
           if (claim_size == 0) {
                   ring_buf_put_finish(rb, 0);
                   return -ENOMEM;
           }
           h->len = claim_size;
           /* ... write payload through ptr ... */
           ring_buf_put_finish(rb, sizeof(*h) + h->len);
           return h->len;
   }

大致可改写为：

.. code-block:: c

   int write_pkg(struct ring_buf *rb, const uint8_t *payload, size_t payload_size)
   {
           struct hdr *h;
           uint8_t *ptr;
           uint32_t claim_size;

           /* Reserve the header region without committing it. */
           if (ring_buf_put_ptr(rb, (uint8_t **)&h, 0) < sizeof(*h)) {
                   return -ENOMEM;
           }

           /* Expose the region right after the header via a trailing offset. */
           claim_size = ring_buf_put_ptr(rb, &ptr, sizeof(*h));
           if (claim_size == 0) {
                   /* Nothing was committed to rb, so the write is cancelled. */
                   return -ENOMEM;
           }
           h->len = MIN(claim_size, payload_size);
           /* ... write payload through ptr ... */

           /* Publish header and payload atomically to the real buffer. */
           ring_buf_commit(rb, sizeof(*h) + h->len);
           return h->len;
   }

其他子系统
**********

* 按需分页（``subsys/demand_paging``）已移到内存管理下的 ``subsys/mem_mgmt/demand_paging``。自定义后备存储和逐出算法的代码也需要移到该位置。

* ``<zephyr/sys/ring_buffer.h>`` 中的环形缓冲区“item”API 已弃用，改用 ``<zephyr/sys/ringq.h>`` 中新的固定大小队列 API。

  存储固定大小项的代码应迁移到 :c:struct:`sys_ringq` （参见 :ref:`fixed_size_ringq_api`）。仅在字节层面使用 item API 的代码应改用同一个 :c:struct:`ring_buf` 上的字节模式函数 :c:func:`ring_buf_put` / :c:func:`ring_buf_get` 调用。（:github:`98255`）

* :c:func:`ZTEST_BENCHMARK_SETUP_TEARDOWN` 和 :c:func:`ZTEST_BENCHMARK_TIMED_SETUP_TEARDOWN` 宏已被移除。它们的 setup/teardown 签名已合并到 :c:func:`ZTEST_BENCHMARK` 和 :c:func:`ZTEST_BENCHMARK_TIMED`，这两个宏现在要求在每个调用点显式传入 ``setup_fn`` 和 ``teardown_fn`` 参数。当基准测试确实两者都不需要时，传入 ``NULL``。

  请按如下方式更新现有调用点：

  .. code-block:: c

     /* Before */
     ZTEST_BENCHMARK(suite, my_bench, 100) { /* ... */ }
     ZTEST_BENCHMARK_TIMED(suite, my_bench, 1000) { /* ... */ }
     ZTEST_BENCHMARK_SETUP_TEARDOWN(suite, my_bench, 100, setup, teardown) { /* ... */ }
     ZTEST_BENCHMARK_TIMED_SETUP_TEARDOWN(suite, my_bench, 1000, setup, teardown) { /* ... */ }

     /* After */
     ZTEST_BENCHMARK(suite, my_bench, 100, NULL, NULL) { /* ... */ }
     ZTEST_BENCHMARK_TIMED(suite, my_bench, 1000, NULL, NULL) { /* ... */ }
     ZTEST_BENCHMARK(suite, my_bench, 100, setup, teardown) { /* ... */ }
     ZTEST_BENCHMARK_TIMED(suite, my_bench, 1000, setup, teardown) { /* ... */ }

* ``CONFIG_ZTEST_SHUFFLE_SUITE_REPEAT_COUNT`` 和 ``CONFIG_ZTEST_SHUFFLE_TEST_REPEAT_COUNT`` 这两个 Kconfig 选项自 Zephyr 4.0 起已弃用，现已被移除。仅使用 :kconfig:option:`CONFIG_ZTEST_SHUFFLE` 时，测试套件和测试用例每次执行只运行一次，且顺序是打乱的；若要重复运行，请启用 :kconfig:option:`CONFIG_ZTEST_REPEAT` 并设置 :kconfig:option:`CONFIG_ZTEST_SUITE_REPEAT_COUNT` 和 :kconfig:option:`CONFIG_ZTEST_TEST_REPEAT_COUNT`。

* CPU 负载指标模块已合并到统一的 :ref:`cpu_load` 模块中。:kconfig:option:`CONFIG_CPU_LOAD_METRIC` 选项已弃用；请改为启用 :kconfig:option:`CONFIG_CPU_LOAD` 并使用 :kconfig:option:`CONFIG_CPU_LOAD_BACKEND_RUNTIME_STATS` 后端。``<zephyr/sys/cpu_load_metric.h>`` 头文件现在只是包含 ``<zephyr/sys/cpu_load.h>``，而 :c:func:`cpu_load_metric_get` 是围绕 :c:func:`cpu_load_get_cpu` 的已弃用封装。请注意，:c:func:`cpu_load_get_cpu` 返回的负载以千分数（0...1000）表示，而不是百分比；请使用 :c:macro:`CPU_LOAD_PERMILLE_TO_PERCENT` 进行换算。

* 内部的 ``__ASSERT_ON`` 定义已被移除。树外代码应直接调用 ``__ASSERT()`` 或 ``__ASSERT_NO_MSG()``，因为断言被禁用时这些宏本来就会被编译掉。请酌情用 ``__maybe_unused`` 或 ``ARG_UNUSED()`` 标记仅由断言使用的值。

FIDO2
=====

* FIDO2 传输回调 API 已发生变化。:c:type:`fido2_transport_recv_cb_t` 回调现在返回 ``int``，用于指示收到的消息是否被 FIDO2 核心接受；:c:type:`fido2_transport_cancel_cb_t` 现在接收收到取消命令的 :c:struct:`fido2_transport` 实例。树外的传输层实现必须更新，以处理接收回调的返回值，并在调用取消回调时传入该传输层实例。（:github:`116552`）
* 通过 :kconfig:option:`CONFIG_FIDO2_UP_CUSTOM` 选择的应用提供的用户在场（user-presence）后端，现在必须实现 :c:func:`fido2_up_reset`，以便针对每个新请求清除其状态。（:github:`116552`）

hawkBit
=======

* 自 Zephyr 4.0 起已弃用的旧版 ``<zephyr/mgmt/hawkbit.h>`` 头文件已被移除。请改为包含 ``<zephyr/mgmt/hawkbit/hawkbit.h>``、``<zephyr/mgmt/hawkbit/config.h>`` 和 ``<zephyr/mgmt/hawkbit/autohandler.h>``。

日志记录
========

* UART 字典日志解析脚本 ``scripts/logging/dictionary/log_parser_uart.py`` 已被移除。请改用 :zephyr_file:`scripts/logging/dictionary/live_log_parser.py`，该脚本在 ``serial`` 子命令之后接收端口和波特率参数。

MCUboot
=======

* ``CONFIG_MCUBOOT_BOOTLOADER_MODE_SWAP_WITHOUT_SCRATCH`` 已被移除。请改用 :kconfig:option:`CONFIG_MCUBOOT_BOOTLOADER_MODE_SWAP_USING_MOVE`。

* Sysbuild 不再在 Espressif SoC 上强制使用 MCUboot 的仅覆盖模式和未签名镜像。使用这些设置的开发板现在会采用通用默认值：使用偏移量交换（保留之前的映像以便回退），以及使用 MCUboot 开发密钥的 RSA-2048 签名。拥有自己密钥的项目必须设置 :kconfig:option:`SB_CONFIG_BOOT_SIGNATURE_KEY_FILE`，而依赖先前行为的项目可以显式选择 :kconfig:option:`SB_CONFIG_MCUBOOT_MODE_OVERWRITE_ONLY` 和 :kconfig:option:`SB_CONFIG_BOOT_SIGNATURE_TYPE_NONE`。在此变更之后构建的引导加载程序会拒绝未签名镜像，因此当设备改用新的默认值时，必须同时重新烧录引导加载程序和应用程序。

* 共享的 Espressif 分区表不再定义 ``scratch_partition``，因此使用这些分区表的开发板不再提供 :kconfig:option:`SB_CONFIG_MCUBOOT_MODE_SWAP_SCRATCH`。其他分区保持各自的偏移量不变。需要该分区的项目可以在开发板 overlay 中将其重新添加回来。

MCUmgr
======

* ``CONFIG_MCUMGR_GRP_OS_INFO_HARDWARE_INFO_SHORT_HARDWARE_PLATFORM`` 已被移除。:ref:`mcumgr_os_application_info` 命令现在始终将开发板目标报告为硬件平台；不再提供 4.3 之前的开发板与开发板修订版本输出。

* 镜像管理客户端（:kconfig:option:`CONFIG_MCUMGR_GRP_IMG_CLIENT`）现在除 SHA-256 外还支持 SHA-512 镜像摘要：

  * :c:func:`img_mgmt_client_state_write` 新增了一个 ``hash_len`` 参数。当 ``hash`` 不为 ``NULL`` 时，传入其以字节为单位的长度（例如 SHA-256 对应 ``32``）。否则传入 ``0``。
  * :c:struct:`mcumgr_image_data` 现在存储可变长度的摘要：``hash`` 缓冲区为 :c:macro:`IMG_MGMT_CLIENT_HASH_MAX_LEN` （64）字节，新增的 ``hash_len`` 字段保存实际长度。读取 ``hash`` 的代码必须使用 ``hash_len``，而不能假定 :c:macro:`IMG_MGMT_DATA_SHA_LEN`。

网络缓冲区
==========

* :c:func:`net_buf_max_len` 和 :c:func:`net_buf_simple_max_len` 已弃用。它们返回的是缓冲区 ``data`` 指针之后的空间容量，这既不是存储大小，也不是剩余可用于添加数据的空间。请使用 :c:func:`net_buf_tailroom` 或 :c:func:`net_buf_simple_tailroom` 确定还能添加多少数据，使用 :c:func:`net_buf_headroom` 或 :c:func:`net_buf_simple_headroom` 确定能在前面推入多少数据。将返回值用作从 ``data`` 开始的暂存区大小的代码，可以按 ``buf->len + net_buf_tailroom(buf)`` 计算。

POSIX
=====

* ``CONFIG_POSIX_READER_WRITER_LOCKS`` 已被移除。请改用 :kconfig:option:`CONFIG_POSIX_RW_LOCKS`。

随机数
======

* ``CONFIG_CTR_DRBG_CSPRNG_GENERATOR`` 已被移除。请改用 :kconfig:option:`CONFIG_PSA_CSPRNG_GENERATOR`。

* ``CONFIG_CS_CTR_DRBG_PERSONALIZATION`` 已被移除。它没有任何效果。

安全存储
========

* 以下文件已重命名：

  * ``zephyr/secure_storage/its/store/settings_get.h`` ->
    ``zephyr/secure_storage/its/store/settings.h``
  * ``zephyr/secure_storage/its/transform/aead_get.h`` ->
    ``zephyr/secure_storage/its/transform/aead.h``

* ZMS 后端分区的 chosen 名称已从 ``secure_storage_its_partition`` 更新为 ``zephyr,secure-storage-its-partition``。（:github:`118501`）

* ``psa_its_get*()`` 函数现在可能返回 ``PSA_ERROR_INVALID_SIGNATURE`` 和 ``PSA_ERROR_DATA_CORRUPT``，这两个错误以前报告为 ``PSA_ERROR_GENERIC_ERROR``。（:github:`118718`）

* 以 0 作为 ``data_size`` 调用 ``psa_its_get()`` 会走常规的检索路径，因此现在可能失败（例如返回 ``PSA_ERROR_DOES_NOT_EXIST``），而不再总是返回 ``PSA_SUCCESS``。（:github:`118718`）

Shell
=====

* ``kernel log_level <module> <severity>`` shell 命令自 Zephyr v4.1.0 起已弃用，现已被移除。请改用 ``log enable <severity> <module>``：参数顺序相反，且严重级别是名称（``none``、``err``、``wrn``、``inf``、``dbg``）而不是数字。

流式 Flash
==========

* ``stream_flash_erase_page()`` 已被移除。请改用 :c:func:`flash_area_erase` 或 :c:func:`flash_erase`；流式 Flash API 中没有对应的功能。

工具
****

* 调用 runner 的 ``west`` 命令（``flash``、``debug``、``debugserver``、``attach``、``rtt``、``reset``、``robot`` 和 ``simulate``）的 ``--skip-rebuild`` 选项已被移除。请改用 ``--no-rebuild``。

* ``pyocd`` runner 不再读取 ``PYOCD_DAPARG`` 环境变量。请改为向 ``west flash``/``west debug`` 传入 ``--daparg``。

* ``openocd`` runner 现在与其他 runner 一样，通过规范的 ``-i``/``--dev-id`` 选项按序列号选择调试适配器。原先的 ``--serial`` 选项已弃用并作为别名保留；它映射到相同的机制（该值仍会作为 ``_ZEPHYR_BOARD_SERIAL`` 传递给 OpenOCD 配置）。请将相关脚本更新为使用 ``west flash -i <serial>``。

模块
****

* `CHRE <https://github.com/zephyrproject-rtos/chre>`_ 框架不再是 Zephyr manifest 的可选模块，其示例也已移出 Zephyr 代码树。它现在是一个 :ref:`外部模块 <external_module_chre>`；如需继续使用，请将其添加到应用 manifest 中。

* 对 `CANopenNode <https://github.com/CANopenNode/CANopenNode>`_ 协议栈的支持已移到 :ref:`外部模块 <external_module_canopennode>`。

lvgl
====

* ``zephyr,lvgl-pointer-input`` 设备树绑定将 ``swap-xy``、``invert-x`` 和 ``invert-y`` 属性标记为 **已弃用**。用户应改为将相应的触摸屏属性 ``swapped-x-y``、``inverted-x`` 和 ``inverted-y`` 添加到下层触摸输入控制器设备节点，这些变换现在已在设备节点中规范化定义。

* :kconfig:option:`CONFIG_LV_Z_FULL_REFRESH` 现在是 ``LV_Z_RENDERING_MODE`` Kconfig choice 的一部分，与 :kconfig:option:`CONFIG_LV_Z_PARTIAL_REFRESH` （默认）和 :kconfig:option:`CONFIG_LV_Z_DIRECT_RENDERING` 并列。在 ``.conf`` 片段中设置 ``CONFIG_LV_Z_FULL_REFRESH=y`` 仍然有效，但 ``CONFIG_LV_Z_FULL_REFRESH=n`` 会被静默忽略，因为 choice 成员无法通过这种方式取消选中。原先通过 ``CONFIG_LV_Z_FULL_REFRESH=n`` 来选择不使用全刷新默认值的树外开发板或扩展板，必须改为在 ``Kconfig.defconfig`` 或 ``.defconfig`` 文件中覆盖 choice 的默认值：

  .. code-block:: kconfig

     choice LV_Z_RENDERING_MODE
       default LV_Z_PARTIAL_REFRESH
     endchoice

hal_nxp
=======

* S32K344：该 SoC 的 pinmux 头文件已从 ``S32K344-172MQFP-pinctrl.h`` 重命名为 ``S32K344_K324_K314_172HDQFP-pinctrl.h``。树外开发板必须相应地更新其 include 指令::

    #include <nxp/s32/S32K344_K324_K314_172HDQFP-pinctrl.h>

Mbed TLS
========

* 以下已弃用的 Kconfig 选项已被移除：

  * ``CONFIG_MBEDTLS_MD`` -> :kconfig:option:`CONFIG_MBEDTLS_MD_C`
  * ``CONFIG_MBEDTLS_LMS`` -> :kconfig:option:`CONFIG_MBEDTLS_LMS_C`
  * ``CONFIG_MBEDTLS_TLS_VERSION_1_2`` -> :kconfig:option:`CONFIG_MBEDTLS_SSL_PROTO_TLS1_2`
  * ``CONFIG_MBEDTLS_DTLS`` -> :kconfig:option:`CONFIG_MBEDTLS_SSL_PROTO_DTLS`
  * ``CONFIG_MBEDTLS_TLS_VERSION_1_3`` -> :kconfig:option:`CONFIG_MBEDTLS_SSL_PROTO_TLS1_3`
  * ``CONFIG_MBEDTLS_TLS_SESSION_TICKETS`` ->
    :kconfig:option:`CONFIG_MBEDTLS_SSL_SESSION_TICKETS`
  * ``CONFIG_MBEDTLS_CTR_DRBG_ENABLED`` -> :kconfig:option:`CONFIG_MBEDTLS_CTR_DRBG_C`
  * ``CONFIG_MBEDTLS_HMAC_DRBG_ENABLED`` -> :kconfig:option:`CONFIG_MBEDTLS_HMAC_DRBG_C`

  与已移除的选项不同，新选项不会自动启用其依赖项。

* :kconfig:option:`CONFIG_MBEDTLS_SSL_EARLY_DATA` 现在是需要显式启用的选项，不再由 :kconfig:option:`CONFIG_MBEDTLS_SSL_TLS1_3_KEY_EXCHANGE_MODE_PSK_ENABLED` 隐式启用。依赖 TLS 1.3 PSK 早期数据（0-RTT）的树外应用或开发板配置，现在必须显式启用 :kconfig:option:`CONFIG_MBEDTLS_SSL_EARLY_DATA`。

* ``CONFIG_PSA_CRYPTO_CLIENT`` 已被移除，因为它是 :kconfig:option:`CONFIG_PSA_CRYPTO` 的重复项。如果您之前在使用它，请改用 :kconfig:option:`CONFIG_PSA_CRYPTO`。（:github:`108960`）

* 接口 CMake 库 ``mbedTLS`` 已重命名为 ``mbedtls_iface``。为保持向后兼容，前者作为后者的别名保留，但会在未来的版本中移除。

* Mbed TLS 已更新到 4.1.1 版本。版本说明参见 `这里 <https://github.com/Mbed-TLS/mbedtls/releases/tag/mbedtls-4.1.1>`_。

* TF-PSA-Crypto 已更新到 1.1.1 版本。版本说明参见 `这里 <https://github.com/Mbed-TLS/TF-PSA-Crypto/releases/tag/tf-psa-crypto-1.1.1>`_。

Trusted Firmware-M (TF-M)
=========================

* :kconfig:option:`CONFIG_TFM_ZEPHYR_4_0_TO_4_2_COMPATIBILITY` 已弃用，改用 :kconfig:option:`CONFIG_TFM_ZEPHYR_4_2_COMPATIBILITY`，后者更准确地描述了需要设置该符号的场景。

* :kconfig:option:`CONFIG_BUILD_WITH_TFM` 不再启用 :kconfig:option:`CONFIG_MBEDTLS` / :kconfig:option:`CONFIG_PSA_CRYPTO`。请确保在构建时按需显式启用它们。（:github:`114762`）

* :kconfig:option:`CONFIG_TFM_PARTITION_CRYPTO` 现在依赖于 :kconfig:option:`CONFIG_PSA_CRYPTO_PROVIDER_TFM`，这意味着需要启用 :kconfig:option:`CONFIG_PSA_CRYPTO`，TF-M Crypto 分区才会启用。（:github:`116318`）

片段
****

* 将 ``xen_dom0`` 重命名为 ``xen-dom0``。

架构
****

* 新增了一个架构原语 ``arch_cpu_irqs_are_enabled()``。它在不修改调用 CPU 中断使能状态的情况下返回该状态，与检查已保存键值的 ``arch_irq_unlocked()`` 形成互补。树外的架构移植实现必须提供该原语。

* ``CONFIG_XTENSA_MPU_ONLY_SOC_RANGES`` 已被移除。如果 SoC 或开发板要覆盖默认的 MPU 区域表，请改为在 SoC 或开发板层覆盖 :c:var:`xtensa_mpu_ranges`。

* ``xtensa_soc_mpu_ranges[]`` 和 ``xtensa_soc_mpu_ranges_num`` 已被移除。如果 SoC 或开发板在启动时需要自己的内存区域，请改为覆盖 :c:var:`xtensa_mpu_ranges`。

* ``CONFIG_XTENSA_MPU_DEFAULT_MEM_TYPE`` 已被移除，因为内存类型现在通过 ``xtensa_mpu_mem_type_ranges[]`` 定义。

* ``CONFIG_XTENSA_BACKTRACE_EXCEPTION_DUMP_HOOK`` 已被移除，因为回溯现在始终使用 :c:macro:`EXCEPTION_DUMP` 进行输出。

* 使用 :kconfig:option:`CONFIG_XTENSA_BACKTRACE` 的 SoC 现在需要实现 :c:func:`xtensa_soc_stack_ptr_is_sane` 和 :c:func:`xtensa_soc_ptr_executable`。

* ARMv7-M MPU 的 device-type 区域属性 ``REGION_PPB_ATTR``、``REGION_IO_ATTR`` 和 ``REGION_EXTMEM_ATTR`` 现在会在所有 ARMv7-M 内核上设置 Execute-Never（``XN=1``）。在 ARMv7-M 上，从 Device/Strongly-ordered 内存执行在架构上是 UNPREDICTABLE 的，因此不会影响任何有效的用例。在 Cortex-M7 上，XN 属性还会阻止推测性取指进入这些区域，否则可能导致总线挂起或外设空间中的读副作用（Arm Cortex-M7 TRM，“Speculative accesses - Considerations for system design”）；仅靠内存类型无法阻止这些情况。仍然从用这些属性映射的区域执行代码的树外开发板，必须改为定义自定义属性。

* 新增的 :kconfig:option:`CONFIG_ARM_MPU_CM7_UNMAPPED_REGION` 选项会让 Arm MPU 驱动将优先级最低的 MPU 区域（区域 0）编程为 4GB 的 Strongly-ordered、不可访问、Execute-Never 兜底区域，从而实现 Arm Cortex-M7 勘误 1013783（SDEN-1068427）的规避措施，并防止 Cortex-M7 对未映射地址的推测性访问。静态 MPU 区域表已显式覆盖固件所用全部内存的 Cortex-M7 开发板或 SoC 可以启用它；此时静态区域将从 MPU 区域 1 开始编程。``mimxrt1180_evk`` 和 ``frdm_imxrt1186`` 的 cm7 目标默认启用该选项，用运行时行为完全相同的方式取代了它们之前手工编写的 ``UNMAPPED`` MPU 区域表条目。

* ``CONFIG_SSE`` 和 ``CONFIG_SSE_FP_MATH`` 已被移除。请改用 :kconfig:option:`CONFIG_X86_SSE` 和 :kconfig:option:`CONFIG_X86_SSE_FP_MATH`。

* ``CONFIG_PLATFORM_SPECIFIC_INIT`` 及其 ``z_arm_platform_init()`` 钩子已被移除。请启用 :kconfig:option:`CONFIG_SOC_RESET_HOOK` 并将该钩子重命名为 :c:func:`soc_reset_hook`。新钩子在复位流程中运行得更晚，即在栈指针设置完成之后，并且从 suspend-to-RAM 恢复时会被跳过。

* RISC-V 专用的 ``CONFIG_EXTRA_EXCEPTION_INFO`` 已被移除。请改用 :kconfig:option:`CONFIG_EXCEPTION_DEBUG`。该选项在 Arm 和 SPARC 上保持不变。

* :c:func:`arch_mem_map` 和 :c:func:`arch_mem_unmap` 的返回值都已从 ``void`` 改为 ``int``，以便在断言被禁用时调用者可以对错误码做出响应。如果断言已启用，则目前基本保留先前使系统停止运行的行为。

Video
=====

* :c:func:`video_import_buffer` 不再通过 ``uint16_t *idx`` 输出参数返回导入缓冲区的索引，而是返回指向导入的 :c:struct:`video_buffer` 的指针，失败时返回 ``NULL``。这有助于对应用屏蔽索引，同时也使应用可以直接访问该缓冲区。

Twister
=======

* 测试通过后发生的故障现在会被显式检测出来，并导致整个测试套件失败；如果某个测试故意产生故障，则必须为该测试用例标记 ``ignore_faults: true`` （:github:`116359`）。
