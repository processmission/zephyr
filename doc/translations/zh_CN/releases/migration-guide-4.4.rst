.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

..
  See
  https://docs.zephyrproject.org/latest/releases/index.html#migration-guides
  for details of what is supposed to go into this document.

.. _migration_4.4:

Zephyr v4.4.0 迁移指南
######################

本文档介绍将应用从 Zephyr v4.3.0 迁移到 Zephyr v4.4.0 时需要进行的更改。

其他更改（与应用迁移无直接关系）请参见 :ref:`版本说明 <zephyr_4.4>`。

.. contents::
    :local:
    :depth: 2

通用
****

* 要求的最低 Zephyr SDK 版本现为 1.0.0。
* 要求的最低 Python 版本现为 3.12（此前为 3.10）。

构建系统
********

* Zephyr 现在正式默认使用 C17（ISO/IEC 9899:2018）作为最低要求的 C 标准版本。如果您的工具链不支持该标准，则需要使用现有且现已弃用的选项之一： :kconfig:option:`CONFIG_STD_C99` 或 :kconfig:option:`CONFIG_STD_C11`。
* board.yml 文件中新开发板对应的 ``board``/``boards`` 条目的 ``full_name`` 属性现为必填项。
* CMake 变量 ``BOARD_QUALIFIERS`` 已与对应的 :kconfig:option:`CONFIG_BOARD_QUALIFIERS` 对齐，因此不再以 ``/`` 为前缀。这意味着任何使用 ``${BOARD}${BOARD_QUALIFIERS}`` 的地方都必须更新为包含 ``/``，例如： ``${BOARD}/${BOARD_QUALIFIERS}``。
* ``SNIPPET_ROOT`` 已与其他 Zephyr ``<type>_ROOT`` 设置保持一致，这些设置默认不包含应用源目录。需要将应用源目录添加到 ``SNIPPET_ROOT`` 的示例，必须改为在 :file:`zephyr/module.yml` 中使用 ``snippet_root = <dir>`` 条目添加应用源目录，或者手动将该文件夹追加到 CMake 变量 ``SNIPPET_ROOT``。
* Shell 自动补全（``west completion``）应重新生成，因为开发板目标自动补全现在支持开发板版本。

内核
****

* 堆加固支持已通过添加构建时生成的 ``zephyr/heap_constants.h`` 文件实现，该文件现由 ``kernel.h`` 包含。这可能会给以 CMake 库形式构建的下游应用带来构建竞态条件，CMake 可能会在头文件生成之前尝试构建它们；这些应用可能需要在 CMake 中额外添加 ``add_dependencies(${lib} zephyr_generated_headers)`` 条目，详情参见 :github:`106439`。

* ``__pinned_*`` 属性族以及 ``CONFIG_LINKER_USE_PINNED_SECTION`` / ``CONFIG_LINKER_GENERIC_SECTIONS_PRESENT_AT_BOOT`` Kconfig 选项已被移除（:github:`108773`）。内核镜像现在始终驻留在物理内存中；按需分页仅适用于通过 :c:func:`k_mem_map` 创建的匿名映射，以及通过 :kconfig:option:`CONFIG_LINKER_USE_ONDEMAND_SECTION` 放置在 ``__ondemand_*`` 链接器段中的符号。

  之前“默认可驱逐”的模型（任何未显式标记 ``__pinned_*`` 的内核页都可能被换出）从设计上从来就不安全：某个构建能否幸存取决于代码和数据相对于缺页处理调度路径的偶然布局，而非任何保证。如果您的应用依赖旧模型，且它在现有版本上运行正常，建议继续使用该版本（最好是 :ref:`长期支持 <release_process_lts>` 版本），而不是升级。迁移到更高版本很可能改变布局（新增代码、函数重排、新编译器），使未标记的页落入缺页调度路径，从而以难以诊断的方式破坏系统。正是这种潜在脆弱性，促使我们移除该模型而不是继续沿用。需要升级的应用必须进行以下更新：

  * 从开发板 defconfig 和 prj.conf 覆盖文件中删除任何 ``CONFIG_LINKER_USE_PINNED_SECTION=y`` 或 ``CONFIG_LINKER_GENERIC_SECTIONS_PRESENT_AT_BOOT=n`` 行。

  * 从源代码中删除 ``__pinned_func``、``__pinned_data``、``__pinned_rodata``、``__pinned_bss`` 和 ``__pinned_noinit`` 属性。需要支持按需分页的代码必须改用 ``__ondemand_func`` / ``__ondemand_rodata``；贡献者需自行确保这些符号不会从缺页处理程序的执行路径中被访问到。

  * 将汇编代码中对 ``PINNED_TEXT``、``PINNED_RODATA``、``PINNED_DATA``、``PINNED_BSS`` 和 ``PINNED_NOINIT`` 的使用（作为 ``SECTION_FUNC()`` / ``SECTION_VAR()`` 的段名参数）替换为普通的 ``TEXT``、``RODATA``、``DATA``、``BSS`` 和 ``NOINIT`` 别名。

  * 将 ``K_KERNEL_PINNED_STACK_DEFINE``、``K_KERNEL_PINNED_STACK_ARRAY_DEFINE``、``K_KERNEL_PINNED_STACK_ARRAY_DECLARE``、``K_THREAD_PINNED_STACK_DEFINE`` 和 ``K_THREAD_PINNED_STACK_ARRAY_DEFINE`` 的使用重命名为对应的非 pinned 版本（``K_KERNEL_STACK_DEFINE``、``K_KERNEL_STACK_ARRAY_DEFINE``、``K_KERNEL_STACK_ARRAY_DECLARE``、``K_THREAD_STACK_DEFINE``、``K_THREAD_STACK_ARRAY_DEFINE``）。

  * 提供了带 pinned 段（``pinned_text`` / ``pinned_rodata`` / ``pinned_data`` / ``pinned_bss`` / ``pinned_noinit``）的自定义链接脚本的树外开发板，应将这些输入段匹配项合并回常规的 text / rodata / data / bss / noinit 输出段。

  * 依赖 ``lnkr_pinned_*`` 链接器符号或 ``lnkr_is_pinned()`` / ``lnkr_is_region_pinned()`` 的树外代码必须移除这些引用。相应的 ``app_smem_pinned*.ld`` 包含文件以及 ``scripts/build/gen_app_partitions.py`` 的 ``--pinoutput`` / ``--pinpartitions`` 选项也已被移除。

开发板
******

* OpenOCD runner 现在使用标准的 ``--file`` 和 ``--file-type`` 接口来指定烧录文件，与其他 runner（如 JLink）保持一致。具体更改如下：

  * ``--use-hex``、``--use-elf`` 和 ``--use-bin`` 标志已弃用。请改用 ``--file-type``：

    * ``--use-elf`` → ``--file-type=elf``
    * ``--use-bin`` → ``--file-type=bin``
    * ``--use-hex`` → ``--file-type=hex`` （默认即为 hex，可省略）

  * 现在支持 ``--file`` 选项来指定自定义文件路径，与 JLink runner 类似。

  * 使用已弃用标志的开发板 CMake 文件仍可继续工作，但会发出弃用警告。

  * ``--file-type`` 选项现在可以在不使用 ``--file`` 的情况下使用，以在构建产物（hex、elf、bin）之间进行选择。

* native_sim：主机 FUSE 访问：现在默认使用 libfusev3 而非 v2，但可通过 :kconfig:option:`CONFIG_FUSE_LIBRARY_VERSION` 选择（:github:`104965`）。

* m5stack_fire：移除 UART2 未使用的 pinctrl 条目，并将 UART1 的引脚映射从 GPIO32/GPIO33 更新为 GPIO16/GPIO17，以匹配文档中描述的 Grove PORT.C 接线。

* Ai-Thinker 的 ``ai_m62_12f`` 和 ``ai_wb2_12f`` 开发板已分别重命名为 ``ai_m62_12f_kit`` 和 ``ai_wb2_12f_kit``。

* 编译定义 'XIP_EXTERNAL_FLASH'、'USE_HYPERRAM' 和 'XIP_BOOT_HEADER_XMCD_ENABLE' 仅在 :zephyr_file:`boards/nxp/mimxrt1180_evk/xip/evkmimxrt1180_flexspi_nor_config.c` 和 :zephyr_file:`boards/nxp/mimxrt1170_evk/xmcd/xmcd.c` 中使用，我们已将它们改为各自开发板 CMakeLists.txt 文件中的局部作用域。依赖这些定义全局可用的应用可能需要更新。（:github:`101322`）

* Renesas ``ek_ra8t2/r7ka8t2lfecac/cm85`` 已重命名为 ``ek_ra8t2/r7ka8t2lflcac/cm85``。

* NXP 调整了部分树内编译标志的作用域，将其可见性限制在真正需要的位置。依赖这些标志全局可用的树外应用或开发板可能需要将它们添加到自己的 CMakeLists.txt 文件中，以确保仍能正常构建。（:github:`100252`）受影响的标志如下：

  * 对于 RT10xx 和 RT11xx 系列，编译标志 ``BOARD_FLASH_SIZE`` 最初定义在 ``boards/nxp/mimxrt10xx_evk/CMakeLists.txt`` 和 ``boards/nxp/mimxrt11xx_evk/CMakeLists.txt`` 中，仅被 HAL 头文件 ``fsl_flexspi_nor_boot.h`` 使用，而该头文件由 :zephyr_file:`soc/nxp/imxrt/imxrt10xx/soc.c` 和 :zephyr_file:`soc/nxp/imxrt/imxrt11xx/soc.c` 包含。为避免与其他全局标志可能发生的冲突，该宏现在改为在 SoC 层通过 :zephyr_file:`soc/nxp/imxrt/imxrt10xx/CMakeLists.txt` 和 :zephyr_file:`soc/nxp/imxrt/imxrt11xx/CMakeLists.txt` 中的 ``zephyr_library_compile_definitions()`` 定义。此更改已应用于所有 RTxxxx 开发板。

  * 对于 RTxxx 系列，编译标志 ``BOARD_FLASH_SIZE`` 最初定义在 ``boards/nxp/mimxrtxxx_evk/CMakeLists.txt`` 中，由于在 Zephyr 代码树中未被使用，因此已从所有 RTxxx 开发板的 CMakeLists.txt 文件中移除。

  * 对于 RTxxx 系列，编译标志 ``BOOT_HEADER_ENABLE`` 此前定义在 ``boards/nxp/mimxrtxxx_evk/CMakeLists.txt`` 中并在 ``boards/nxp/rtxxx/<boot_header>.c`` 中使用，现已被 Kconfig 选项取代。因此，RTxxx 开发板 CMakeLists.txt 文件中的 ``zephyr_compile_definitions(BOOT_HEADER_ENABLE=1)`` 行已被移除。

  * 从 :zephyr_file:`boards/nxp/rd_rw612_bga/CMakeLists.txt` 中移除了编译标志 ``BOOT_HEADER_ENABLE`` 定义，因为它在 Zephyr 代码树中未被使用。

  * 最初，编译标志 ``XIP_BOOT_HEADER_ENABLE`` 和 ``XIP_BOOT_HEADER_DCD_ENABLE`` 在 ``boards/nxp/rt1xxx/<boot_header>.c`` 中使用。这些标志已在 NXP RTxxxx 评估板上全部转换为 Kconfig 选项，从而可以通过 Kconfig 构建系统而非编译期定义来配置启动头。因此，我们从 RTxxxx 开发板级 CMakeLists.txt 文件中移除了 ``zephyr_compile_definitions(XIP_BOOT_HEADER_ENABLE=1)`` 和 ``zephyr_compile_definitions(XIP_BOOT_HEADER_DCD_ENABLE=1)``。由于 ``hal_nxp/rt10xx/fsl_flexspi_nor_boot.h`` 和 ``hal_nxp/rt11xx/fsl_flexspi_nor_boot.h`` 也需要这些宏，因此已通过 ``zephyr_library_compile_definitions()`` 将它们添加到对应的 SoC 层 CMakeLists.txt 文件中，以限制其作用域。

* 以下 Nordic SoC Kconfig 已被弃用并替换；如果 Kconfig/CMake/代码中引用了这些已弃用的 Kconfig，则需要进行更新：

  * :kconfig:option:`CONFIG_SOC_SERIES_NRF51X` 替换为 :kconfig:option:`CONFIG_SOC_SERIES_NRF51`
  * :kconfig:option:`CONFIG_SOC_SERIES_NRF52X` 替换为 :kconfig:option:`CONFIG_SOC_SERIES_NRF52`
  * :kconfig:option:`CONFIG_SOC_SERIES_NRF53X` 替换为 :kconfig:option:`CONFIG_SOC_SERIES_NRF53`
  * :kconfig:option:`CONFIG_SOC_SERIES_NRF54HX` 替换为 :kconfig:option:`CONFIG_SOC_SERIES_NRF54H`
  * :kconfig:option:`CONFIG_SOC_SERIES_NRF54LX` 替换为 :kconfig:option:`CONFIG_SOC_SERIES_NRF54L`
  * :kconfig:option:`CONFIG_SOC_SERIES_NRF91X` 替换为 :kconfig:option:`CONFIG_SOC_SERIES_NRF91`
  * :kconfig:option:`CONFIG_SOC_SERIES_NRF92X` 替换为 :kconfig:option:`CONFIG_SOC_SERIES_NRF92`

* 以下 Sifive Freedom SoC Kconfig 已被弃用并替换；如果 Kconfig/CMake/代码中引用了这些已弃用的 Kconfig，则需要进行更新：

  * :kconfig:option:`CONFIG_SOC_SERIES_SIFIVE_FREEDOM_FE300` 替换为 :kconfig:option:`CONFIG_SOC_SERIES_FE300`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FE310_G000` 替换为 :kconfig:option:`CONFIG_SOC_FE310_G000`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FE310_G002` 替换为 :kconfig:option:`CONFIG_SOC_FE310_G002`
  * :kconfig:option:`CONFIG_SOC_SERIES_SIFIVE_FREEDOM_FU500` 替换为 :kconfig:option:`CONFIG_SOC_SERIES_FU500`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FU540` 替换为 :kconfig:option:`CONFIG_SOC_FU540`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FU540_E51` 替换为 :kconfig:option:`CONFIG_SOC_FU540_E51`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FU540_U54` 替换为 :kconfig:option:`CONFIG_SOC_FU540_U54`
  * :kconfig:option:`CONFIG_SOC_SERIES_SIFIVE_FREEDOM_FU700` 替换为 :kconfig:option:`CONFIG_SOC_SERIES_FU700`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FU740` 替换为 :kconfig:option:`CONFIG_SOC_FU740`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FU740_S7` 替换为 :kconfig:option:`CONFIG_SOC_FU740_S7`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FU740_U74` 替换为 :kconfig:option:`CONFIG_SOC_FU740_U74`

* ITE ``it515xx_evb`` 已重命名为 ``it51xxx_evb``。

* 使用 :kconfig:option:`CONFIG_USE_DT_CODE_PARTITION` 或设置了 ``zephyr,code-partition`` chosen 节点的开发板，现在应改用新的 :dtcompatible:`zephyr,mapped-partition` compatible。该绑定使用设备树单元地址来获取分区的内存映射地址，而无需手动向上遍历子节点、直到找到具有特定名称的节点才能计算；同时，使用 :dtcompatible:`zephyr,mapped-partition` 时不再允许使用 :kconfig:option:`CONFIG_FLASH_LOAD_OFFSET` 和 :kconfig:option:`CONFIG_FLASH_LOAD_SIZE`，因为链接脚本现在可以自行计算出 NVM 偏移和大小，无需 Kconfig 作为中间步骤执行数学运算。此外，切换到 :dtcompatible:`zephyr,mapped-partition` 后，内存映射设备上不再需要 :dtcompatible:`fixed-subpartitions`，因为它们可以原生地相互嵌套，并具有正确的地址和偏移（与设备树 ``ranges`` 属性一起使用时）。对于尚未更新为对 ``zephyr,code-partition`` chosen 设备使用 :dtcompatible:`zephyr,mapped-partition` 绑定的开发板目标，将设置 :kconfig:option:`CONFIG_FLASH_CODE_PARTITION_USING_FIXED_PARTITIONS`。未来将弃用将 fixed-partitions 用作 chosen ``zephyr,code-partition`` 节点的用法。

* 基于 STM32N6x SoC（:kconfig:option:`CONFIG_SOC_SERIES_STM32N6X`）的开发板或项目，当期望 Zephyr 应用在处理器的安全状态下执行时，现在需要显式启用 :kconfig:option:`CONFIG_TRUSTED_EXECUTION_SECURE`。反之，如果期望 Zephyr 应用在处理器的非安全状态下执行，开发板或项目必须显式启用 :kconfig:option:`CONFIG_TRUSTED_EXECUTION_NON_SECURE`。

* 以下 WCH SoC Kconfig 已被重命名。如果 Kconfig/CMake/代码引用了旧 Kconfig，则需要进行更新：

  * ``CONFIG_SOC_SERIES_CH32V00X`` 替换为 :kconfig:option:`CONFIG_SOC_SERIES_QINGKE_V2C`

设备驱动与设备树
****************

.. zephyr-keep-sorted-start re(^\w) ignorecase

ADC
===

* :dtcompatible:`renesas,ra-adc` compatible 已被 :dtcompatible:`renesas,ra-adc12` 取代。使用旧 compatible 的应用必须更新其设备树节点。

* 新增了 :dtcompatible:`renesas,ra-adc16` compatible。在使用提供 16 位 ADC 分辨率的 EK-RA2A1 开发板时必须使用它。

* 将 :kconfig:option:`CONFIG_ADC_MCUX_SAR_ADC` 重命名为 :kconfig:option:`CONFIG_ADC_NXP_SAR_ADC`。
* 将驱动文件从 ``adc_mcux_sar_adc.c`` 重命名为 :zephyr_file:`drivers/adc/adc_nxp_sar_adc.c`。
* 使用 SAR ADC 驱动的应用需要更新设备树中的节点，加入 ``zephyr,input-positive`` 以指定硬件通道。对于当前支持 SAR ADC 的 SoC，参考电压应使用 ``ADC_REF_VDD_1`` 而不是 ``ADC_REF_INTERNAL``。此驱动更新也修正了该问题，因此用户还需要相应更新设备树中该属性的值。（:github:`100978`）

* :dtcompatible:`st,stm32-adc` 不再具有 ``resolutions`` 属性，取而代之的是 ``st,adc-resolutions`` 属性。对于 revision Y 的 STM32H7 器件，不再需要替换 14 位和 12 位分辨率的值。如果使用 14 位或 12 位分辨率，此更改可能会影响功耗。此前使用功耗优化值，现在使用标准值（未做功耗优化，但精度更好）。对其他系列没有影响。

DMA
===

* 移除了 :kconfig:option:`CONFIG_DMA_MCUX_EDMA_V5` （:github:`100341`）。该宏此前用于区分 nxp,version(5) 和 nxp,version(4)。现在它统一支持两个版本的维护。用户可以将 ``DMA_MCUX_EDMA_V5`` 改为 ``DMA_MCUX_EDMA_V4``。

EEPROM
======

* 为 I2C EEPROM 目标驱动新增了 :c:func:`eeprom_target_read_data()` 和 :c:func:`eeprom_target_write_data()`，它们接受偏移量和长度参数，并弃用了 :c:func:`eeprom_target_program()`。

* 更新了 :dtcompatible:`microchip,xec-eeprom` 的 PCR 和 GIRQ 属性，使其使用新的宏（:github:`104591`）。

ESP32-S3
========

* 原先的 ``espressif,esp32-lcd-cam`` 绑定已重构。LCD_CAM 外设现在由通用的 ``lcd_cam`` 节点表示，其功能模块拆分为两个独立的子节点：

    * 用于 DVP（摄像头）输入模块的 :dtcompatible:`espressif,esp32-lcd-cam-dvp` compatible 节点，标签为 ``lcd_cam_dvp``。
    * 用于 LCD 输出模块的 :dtcompatible:`espressif,esp32-lcd-cam-mipi-dbi` compatible 节点，标签为 ``lcd_cam_disp``。

  原有的 :dtcompatible:`espressif,esp32-lcd-cam` compatible 节点保留通用的 pinctrl、时钟和中断属性，而摄像头专用属性已移至新的 ``lcd_cam_dvp`` 子节点。

  摄像头相关属性必须从 ``lcd_cam`` 节点移至新的 ``lcd_cam_dvp`` 子节点，且 ``zephyr,camera`` chosen 属性应指向 ``lcd_cam_dvp``。

GPIO
====

* LiteX GPIO 驱动 :dtcompatible:`litex,gpio` 已经过重构，以支持更改方向。该驱动现在使用 reg-names 属性来检测 GPIO 控制器支持的模式。设备树属性 ``port-is-output`` 已被移除。reg-names 现在直接取自 LiteX。（:github:`99329`）

* :dtcompatible:`renesas,rz-gpio` 的 ``irqs`` 属性已经过重构，改为将引脚显式映射到中断 phandle，而不是中断索引（:github:`101256`）。

  .. code-block:: devicetree

     /* Old (Zephyr ≤ 4.3) */
     &gpio16 {
         /* Map port16 pin3 to tint7 */
         irqs = <3 7>;
     };

     /* New (Zephyr ≥ 4.4) */
     &tint7 {
         status = "okay";
     };

     &gpio16 {
         /* Map port16 pin3 to tint7 */
         irqs = <&tint7 3>;
     };

Infineon
========

* Infineon 驱动文件名已重命名，从名称中去掉了 ``cat1``，以支持在多个设备类别中复用。以下驱动已重命名（:github:`99174`）：

  * ``adc_ifx_cat1.c`` → ``adc_ifx.c``
  * ``clock_control_ifx_cat1.c`` → ``clock_control_ifx.c``
  * ``counter_ifx_cat1.c`` → ``counter_ifx.c``
  * ``dma_ifx_cat1.c`` → ``dma_ifx.c``
  * ``dma_ifx_cat1_pdl.c`` → ``dma_ifx_pdl.c``
  * ``flash_ifx_cat1.c`` → ``flash_ifx.c``
  * ``flash_ifx_cat1_qspi.c`` → ``flash_ifx_qspi.c``
  * ``flash_ifx_cat1_qspi_mtb_hal.c`` → ``flash_ifx_qspi_mtb_hal.c``
  * ``gpio_ifx_cat1.c`` → ``gpio_ifx.c``
  * ``i2c_ifx_cat1.c`` → ``i2c_ifx.c``
  * ``i2c_ifx_cat1_pdl.c`` → ``i2c_ifx_pdl.c``
  * ``mbox_ifx_cat1.c`` → ``mbox_ifx.c``
  * ``pinctrl_ifx_cat1.c`` → ``pinctrl_ifx.c``
  * ``rtc_ifx_cat1.c`` → ``rtc_ifx.c``
  * ``ifx_cat1_sdio.c`` → ``ifx_sdio.c``
  * ``sdio_ifx_cat1_pdl.c`` → ``sdio_ifx_pdl.c``
  * ``serial_ifx_cat1_uart.c`` → ``serial_ifx_uart.c``
  * ``spi_ifx_cat1.c`` → ``spi_ifx.c``
  * ``spi_ifx_cat1_pdl.c`` → ``spi_ifx_pdl.c``
  * ``uart_ifx_cat1.c`` → ``uart_ifx.c``
  * ``uart_ifx_cat1_pdl.c`` → ``uart_ifx_pdl.c``
  * ``wdt_ifx_cat1.c`` → ``wdt_ifx.c``

  相应的 Kconfig 符号和绑定文件也已更新：

  * ``CONFIG_*_INFINEON_CAT1`` → ``CONFIG_*_INFINEON``
  * ``compatible: "infineon,cat1-adc"`` → ``compatible: "infineon,adc"``

* compatible 为 :dtcompatible:`infineon,bt-hci-uart` 的 Infineon 蓝牙 HCI UART 驱动（:kconfig:option:`CONFIG_BT_HCI_UART_INFINEON`）现在明确限定为使用 HCI UART 传输的 AIROC 连接芯片。（:github:`103871`）

  相应的 Kconfig 符号和设备树 compatible 也已更新：

  * ``CONFIG_BT_CYW43XX`` → :kconfig:option:` CONFIG_BT_HCI_UART_INFINEON`
  * ``dtcompatible: "infineon,cyw43xxx-bt-hci"`` → ``dtcompatible: "infineon,bt-hci-uart"``

MDIO
====

* ``mdio_bus_enable()`` 和 ``mdio_bus_disable()`` 函数已被移除。MDIO 总线的启用/禁用现在由 MDIO 驱动内部处理。（:github:`99690`）。

* MDIO 驱动区域已并入以太网驱动区域。驱动已从 ``drivers/mdio/`` 移至 :zephyr_file:`drivers/ethernet/mdio/`。设备树绑定已从 ``dts/bindings/mdio/`` 移至 :zephyr_file:`dts/bindings/ethernet/mdio/`。（:github:`103944`）

MEMC
====

* :dtcompatible:`st,stm32-xspi-psram` 和 :dtcompatible:`st,stm32-ospi-psram` compatible 节点现在需要包含 ``st,refresh`` 属性，以内存时钟周期数指定 PSRAM 刷新率（:github:`102735`）。驱动中硬编码的默认值 320（:dtcompatible:`st,stm32-xspi-psram`）和 129（:dtcompatible:`st,stm32-ospi-psram`）已被移除。

NXP
===

* NXP DTSI 文件已移至 ``dts/arm/nxp`` 下按系列划分的子目录，以提高可维护性和可发现性，并与 ``soc/nxp`` 下的结构保持一致。被移动文件的设备树包含路径必须更新。请将 ``#include <nxp/nxp_*.dtsi>`` 形式的包含更新为使用正确的系列子目录。（:github:`101243`）。

  示例：

  .. code-block:: dts

    /* Before */
    #include <nxp/nxp_rt1060.dtsi>

    /* After */
    #include <nxp/imxrt/nxp_rt1060.dtsi>

  此更改仅适用于从 ``dts/arm/nxp`` 移出的 NXP ARM SoC 包含文件。不要更改位于其他位置（例如 ``dts/arm64/nxp`` 下）的 DTSI 文件的包含。

  要定位受影响的包含语句，可以搜索旧的包含前缀：

  .. code-block:: console

    git grep "#include <nxp/nxp_" -- '*.dtsi' '*.dts' '*.overlay'

* :dtcompatible:`nxp,lptmr` 节点用作系统定时器时，现在必须通过 ``zephyr,system-timer`` chosen 属性指定。基于 i.MX95 和 MCX-W SoC 的开发板已在 SoC DTSI 中设置好此项，无需更改。所有其他使用 :kconfig:option:`CONFIG_MCUX_LPTMR_TIMER` 的开发板必须添加开发板覆盖文件：

  .. code-block:: devicetree

     / {
         chosen {
             zephyr,system-timer = &lptmr0;
         };
     };

  在 Kinetis KE1xF 上，启用 :kconfig:option:`CONFIG_PM` 时也需要此覆盖文件。

* :dtcompatible:`nxp,imx-flexspi-nor` compatible 节点现在有一个 :dtcompatible:`soc-nv-flash` compatible 子节点来描述闪存。``nxp,imx-flexspi-nor`` 节点充当闪存控制器（重命名为 ``flash-controller@0``），``erase-block-size``、``write-block-size`` 属性以及 ``partitions`` 节点已移至闪存芯片节点中。树外开发板必须相应更新其设备树。

* ``zephyr,flash`` chosen 属性必须指向 :dtcompatible:`soc-nv-flash` compatible 节点。

  * ``zephyr,flash-controller`` chosen 属性必须指向 :dtcompatible:`nxp,imx-flexspi-nor` compatible 节点。
  * 控制器节点上需要提供 ``ranges`` 属性。

QSPI
====

* 使用 ``dual-flash`` 属性配置的 :dtcompatible:`st,stm32-qspi` compatible 节点现在还需要包含 ``ssht-enable`` 属性，以重新启用采样移位。采样移位现在可配置，且默认禁用。（:github:`98999`）。

Radio
=====

* 以下设备树绑定已重命名，以与 ``radio-`` 前缀保持一致：

  * :dtcompatible:`generic-fem-two-ctrl-pins` 现为 :dtcompatible:`radio-fem-two-ctrl-pins`
  * :dtcompatible:`gpio-radio-coex` 现为 :dtcompatible:`radio-gpio-coex`

* 新增了 :dtcompatible:`radio.yaml` 基础绑定，用于描述通用无线电硬件能力。为保持一致，``tx-high-power-supported`` 属性已重命名为 ``radio-tx-high-power-supported``。

* 使用旧 compatible 字符串的设备树和覆盖文件必须更新为新名称。

SD 主机控制器
=============

* 根据 `SD Host Controller Specification <https://www.sdcard.org/downloads/pls/pdf/?p=PartA2_SD%20Host_Controller_Simplified_Specification_Ver4.20.jpg>`_，将额外字段 ``bus_4_bit_support``、``hs200_support`` 和 ``hs400_support`` 从 :c:struct:`sdhc_host_caps` 移至 :c:struct:`sdhc_host_props`。（:github:`91701`）

Shell
=====

* :c:func:`shell_set_bypass` 现在需要传入用户数据指针。相应地，:c:type:`shell_bypass_cb_t` 现在具有用户数据参数。（:github:`100311`）

STM32
=====

* STM32 供电配置现在使用设备树属性进行。新增了 :dtcompatible:`st,stm32h7-pwr`、:dtcompatible:`st,stm32h7rs-pwr` 和 :dtcompatible:`st,stm32-dualreg-pwr` 绑定，并移除了所有与供电配置相关的 Kconfig 符号：

  * ``CONFIG_POWER_SUPPLY_LDO``

  * ``CONFIG_POWER_SUPPLY_DIRECT_SMPS``,

  * ``CONFIG_POWER_SUPPLY_SMPS_1V8_SUPPLIES_LDO``

  * ``CONFIG_POWER_SUPPLY_SMPS_2V5_SUPPLIES_LDO``,

  * ``CONFIG_POWER_SUPPLY_SMPS_1V8_SUPPLIES_EXT_AND_LDO``

  * ``CONFIG_POWER_SUPPLY_SMPS_2V5_SUPPLIES_EXT_AND_LDO``

  * ``CONFIG_POWER_SUPPLY_SMPS_1V8_SUPPLIES_EXT``

  * ``CONFIG_POWER_SUPPLY_SMPS_2V5_SUPPLIES_EXT``

  * ``CONFIG_POWER_SUPPLY_EXTERNAL_SOURCE``

* STM32 专用的 chosen 属性 ``/chosen/zephyr,ccm`` 已被 ``/chosen/zephyr,dtcm`` 取代。属性宏 ``__ccm_data_section``、``__ccm_bss_section`` 和 ``__ccm_noinit_section`` 已弃用，但为向后兼容而保留；**它们将在 Zephyr 4.5 中移除**。应改用通用的 ``__dtcm_{data,bss,noinit}_section`` 宏。（:github:`100590`）

* STM32 平台现在使用 MCUboot 的默认运行模式 ``swap using offset`` （:kconfig:option:`SB_CONFIG_MCUBOOT_MODE_SWAP_USING_OFFSET`）。为支持此引导加载程序模式，需要对开发板设备树进行一些更改。若干开发板已支持此模式（参见 :github:`100385`）。此前的 ``swap using move`` 模式仍可在 sysbuild 中通过启用 :kconfig:option:`SB_CONFIG_MCUBOOT_MODE_SWAP_USING_MOVE` 来选择。

* 对于 STM32F2x/F4x/F7x，不同的 PLL 绑定（:dtcompatible:`st,stm32f2-pll-clock`、:dtcompatible:`st,stm32f4-pll-clock`、:dtcompatible:`st,stm32f4-plli2s-clock`、:dtcompatible:`st,stm32f411-plli2s-clock`、:dtcompatible:`st,stm32f7-pll-clock` 和 :dtcompatible:`st,stm32fx-pllsai-clock`）已合并为一个 :dtcompatible:`st,stm32fx-pll-clock`。此合并带来了一些变化，特别是 ``div-divq`` 和 ``div-divr`` 属性已分别重命名为 ``post-div-q`` 和 ``post-div-r``。此外，在 SoC 适用时，如果使用了对应的 ``div-q`` 或 ``div-r`` 属性，则必须定义这些属性。

* 对于 STM32L4x，:dtcompatible:`st,stm32l4-pllsai-clock` 绑定已被现有的 :dtcompatible:`st,stm32l4-pll-clock` 取代。此替代将 ``div-divr`` 属性重命名为 ``post-div-r``。

* 当 MAC 设备树节点中使用以下属性之一时，STM32 平台在 :zephyr_file:`drivers/ethernet/eth_stm32_hal_common.c` 中的 MAC 地址生成现在使用 :c:struct:`net_eth_mac_config`：

    * ``zephyr,random-mac-address`` (a)
    * ``local-mac-address`` (b)
    * ``nvmem-cells`` (c)（新增）

  这会导致使用 (a) 或 (b) 属性的实现出现向后兼容性问题。此前在设备树中使用这些属性的实现，将 ST OUI 作为 MAC 地址的前 3 个最高有效字节，并使用随机 (a) 或显式 (b) 位作为后 3 个最低有效字节。现在，MAC 地址要么完全随机 (a)，要么完全或部分由设备树写入 (b)。

  新实现 (c) 允许引用存储在非易失性存储器中的 MAC 地址。例如：在 STM32N6x 平台上管理 :abbr:`OTP(One Time Programmable)` 熔丝的 BSEC 外设。更多详细信息请参见 :c:func:`net_eth_mac_load`。

  当 MAC 节点中未指定这些属性中的任何一个时，将使用旧版实现。（:github:`102810`）

  .. note:: 此更改使 STM32 平台的行为与 Zephyr 的通用行为保持一致。此前的实现尚未达到产品可用状态，因此应该不会造成太多麻烦。

* Kconfig 选项 ``CONFIG_SPI_STM32_USE_HW_SS`` 已被移除。SPI 运行模式现在根据设备树配置自动选择：具有 ``cs-gpios`` 或新增的 ``st,soft-nss`` 属性的实例以 “Soft NSS” 模式工作，而所有其他实例以 “Hard NSS” 模式工作。

* 为确保 SPI 在任何频率下都能正常工作，所有 SPI 引脚现在默认配置为 ``very-high-speed`` 压摆率。这可能会导致功耗升高。可以在开发板的 dts 或覆盖文件中将压摆率值改为较慢的速度，以降低功耗。

* :kconfig:option:`CONFIG_NUM_IRQS` 现在通过新的 ``dt_highest_controller_irq_number`` Kconfig 预处理函数，基于活动（``status = "okay";``）设备自动计算。注册自定义 ISR（使用 :c:macro:`IRQ_CONNECT()`）的应用可能会因 :kconfig:option:`CONFIG_NUM_IRQS` 取值偏低而遇到如下构建失败：

  .. code-block::

    gen_isr_tables.py: error: IRQ 114 (offset=0) exceeds the maximum of 106

  请将 :kconfig:option:`CONFIG_NUM_IRQS` 显式设置为适当的值以解决这些问题。（:ref:`以下文档页面 <setting_configuration_values>` 说明了具体做法）

USB
===

* :dtcompatible:`maxim,max3421e_spi` 已重命名为 :dtcompatible:`maxim,max3421e-spi`。
* USB 控制传输缓冲区分配已从 UDC 移至 USB device_next。树外 UDC 驱动需要相应重构。（:github:`103493`）。

* UVC 设备应用 API 已修改：

  * ``uvc_set_video_dev`` 已重命名为 :c:func:`uvc_device_init`
  * ``uvc_add_format`` 已重命名为 :c:func:`uvc_device_add_format`
  * 新增了 :c:func:`uvc_device_enable`
  * 新增了 :c:func:`uvc_device_shutdown`

USB-C
=====

* ``alert_handler_cb`` 字段已从 :c:struct:`tcpc_driver_api` 结构体中移除，因为它未被使用，且与通过 :c:func:`tcpc_set_alert_handler_cb` 注册的回调重复。

中断控制器
==========

* :dtcompatible:`swerv,pic` 现已通过添加厂商前缀变为 :dtcompatible:`cdns,swerv-pic`。

以太网
======

* 以下驱动已引入使用 :c:struct:`net_eth_mac_config` 的驱动 MAC 地址配置支持：

  * :dtcompatible:`atmel,sam-gmac` 和 :dtcompatible:`atmel,sam0-gmac` （:github:`96598`）

    * 移除了 ``CONFIG_ETH_SAM_GMAC_MAC_I2C_EEPROM``
    * 移除了 ``CONFIG_ETH_SAM_GMAC_MAC_I2C_INT_ADDRESS``
    * 移除了 ``CONFIG_ETH_SAM_GMAC_MAC_I2C_INT_ADDRESS_SIZE``
    * 移除了 ``mac-eeprom`` 属性

  * :dtcompatible:`litex,liteeth` （:github:`100620`）
  * :dtcompatible:`microchip,lan865x` （:github:`100318`）
  * :dtcompatible:`microchip,lan9250` （:github:`99127`）
  * :dtcompatible:`nxp,enet-mac` （:github:`102775`）
  * :dtcompatible:`sensry,sy1xx-mac` （:github:`100619`）
  * :dtcompatible:`st,stm32n6-ethernet`、:dtcompatible:`st,stm32h7-ethernet` 和 :dtcompatible:`st,stm32-ethernet` （:github:`102810`、:github:`105090`）
  * :dtcompatible:`virtio,net` （:github:`100106`）
  * :dtcompatible:`vnd,ethernet` （:github:`96598`）
  * :dtcompatible:`wiznet,w5500` （:github:`100919`）
  * :dtcompatible:`snps,designware-ethernet` （:github:`105090`）

  现在应将 MAC 地址设置为 :dtcompatible:`nvmem-layout` 的子节点。请参阅 :ref:`MAC 地址配置 <mac_address_config>` 文档。

* ``fixed-link`` 属性已从 :dtcompatible:`ethernet-phy` 中移除。如果需要该功能，请改用新的 :dtcompatible:`ethernet-phy-fixed-link` compatible。此时需要使用 ``default-speeds`` 属性指定固定链路参数（:github:`100454`）。

* :dtcompatible:`microchip,ksz8081` 的 ``reset-gpios`` 属性已改为低电平有效，您可能需要在设备树中将该引脚设置为 ``GPIO_ACTIVE_LOW`` （:github:`100751`）。

* :kconfig:option:`CONFIG_ETH_INIT_PRIORITY` 现在默认设置为 60。:kconfig:option:`CONFIG_PHY_INIT_PRIORITY` 和 :kconfig:option:`CONFIG_MDIO_INIT_PRIORITY` 现在默认取 :kconfig:option:`CONFIG_ETH_INIT_PRIORITY` 的值。:kconfig:option:`CONFIG_PTP_CLOCK_INIT_PRIORITY` 也是如此，但仅在启用 :kconfig:option:`CONFIG_ETH_DRIVER` 时成立。这样，优先级便基于设备树中的依赖关系。（:github:`104310`）

* 支持校验和卸载的驱动现在需要选择新的 Kconfig 选项 :kconfig:option:`CONFIG_NET_CHECKSUM_OFFLOAD_SUPPORTED`。要使用校验和卸载，需要启用 :kconfig:option:`CONFIG_NET_CHECKSUM_OFFLOAD`。如果选择了 :kconfig:option:`CONFIG_NET_CHECKSUM_OFFLOAD_SUPPORTED`，该选项默认启用。（:github:`105051`）

* :dtcompatible:`microchip,lan865x` 的 ``phy-handle`` 属性现在必须设置为 phy 节点。

* ``CONFIG_NET_DSA_DEPRECATED`` 已被移除。由于 ``microchip,ksz8463``、``microchip,ksz8794`` 和 ``microchip,ksz8863`` 这些 compatible 的驱动尚未迁移到新的 DSA 子系统，它们已被移除。（:github:`105926`）

* 当通过 ``ETHERNET_CONFIG_TYPE_MAC_ADDRESS`` 更改 MAC 地址时，以太网驱动不再需要自行调用 :c:func:`net_if_set_link_addr`。（:github:`105931`）

定时器
======

* 通过兼容性宏 ``z_cms_lptim_hook_on_lpm_entry`` 和 ``z_cms_lptim_hook_on_lpm_exit`` 实现旧版 Cortex-M SysTick 低功耗伴随接口的树外 SoC 或平台代码，应迁移到 :zephyr_file:`include/zephyr/drivers/timer/system_timer_lpm.h` 中的 :c:func:`z_sys_clock_lpm_enter` 和 :c:func:`z_sys_clock_lpm_exit`。:zephyr_file:`drivers/timer/cortex_m_systick.h` 中的兼容性垫片已在 Zephyr 4.4.0 中弃用，目前计划在 Zephyr 4.6.0 中移除。以下旧版 Kconfig 选项也已弃用： :kconfig:option:`CONFIG_CORTEX_M_SYSTICK_LPM_TIMER_NONE`、:kconfig:option:`CONFIG_CORTEX_M_SYSTICK_LPM_TIMER_COUNTER`、:kconfig:option:`CONFIG_CORTEX_M_SYSTICK_LPM_TIMER_HOOKS` 和 :kconfig:option:`CONFIG_CORTEX_M_SYSTICK_RESET_BY_LPM`。chosen 属性 ``/chosen/zephyr,cortex-m-idle-timer`` 已弃用，取而代之的是 ``/chosen/zephyr,system-timer-companion``。请迁移到 :kconfig:option:`CONFIG_SYSTEM_TIMER_LPM_COMPANION_NONE`、:kconfig:option:`CONFIG_SYSTEM_TIMER_LPM_COMPANION_COUNTER`、:kconfig:option:`CONFIG_SYSTEM_TIMER_LPM_COMPANION_HOOKS` 和 :kconfig:option:`CONFIG_SYSTEM_TIMER_RESET_BY_LPM`。

* :dtcompatible:`renesas,rza2m-ostm` 名称已由 :dtcompatible:`renesas,rza2m-ostm-timer` 取代。Kconfig 符号 :kconfig:option:`DT_HAS_RENESAS_RZA2M_OSTM_ENABLED` 已由 :kconfig:option:`DT_HAS_RENESAS_RZA2M_OSTM_TIMER_ENABLED` 取代（:github:`100934`）

控制器局域网（CAN）
===================

* 移除了 ``CONFIG_CAN_MAX_FILTER``、``CONFIG_CAN_MAX_STD_ID_FILTER`` 和 ``CONFIG_CAN_MAX_EXT_ID_FILTER`` （:github:`100596`）。这些选项由以下驱动专用的 Kconfig 符号取代，其中一些符号的默认值已提高以满足典型的软件需求：

  * :kconfig:option:`CONFIG_CAN_LOOPBACK_MAX_FILTERS` 用于 :dtcompatible:`zephyr,can-loopback`
  * :kconfig:option:`CONFIG_CAN_MAX32_MAX_FILTERS` 用于 :dtcompatible:`adi,max32-can`
  * :kconfig:option:`CONFIG_CAN_MCP2515_MAX_FILTERS` 用于 :dtcompatible:`microchip,mcp2515`
  * :kconfig:option:`CONFIG_CAN_MCP251XFD_MAX_FILTERS` 用于 :dtcompatible:`microchip,mcp251xfd`
  * :kconfig:option:`CONFIG_CAN_MCUX_FLEXCAN_MAX_FILTERS` 用于 :dtcompatible:`nxp,flexcan`
  * :kconfig:option:`CONFIG_CAN_NATIVE_LINUX_MAX_FILTERS` 用于 :dtcompatible:`zephyr,native-linux-can`
  * :kconfig:option:`CONFIG_CAN_RCAR_MAX_FILTERS` 用于 :dtcompatible:`renesas,rcar-can`
  * :kconfig:option:`CONFIG_CAN_SJA1000_MAX_FILTERS` 用于 :dtcompatible:`kvaser,pcican` 和 :dtcompatible:`espressif,esp32-twai`
  * :kconfig:option:`CONFIG_CAN_STM32_BXCAN_MAX_EXT_ID_FILTERS` 用于 :dtcompatible:`st,stm32-bxcan`
  * :kconfig:option:`CONFIG_CAN_STM32_BXCAN_MAX_STD_ID_FILTERS` 用于 :dtcompatible:`st,stm32-bxcan`
  * :kconfig:option:`CONFIG_CAN_STM32_FDCAN_MAX_EXT_ID_FILTERS` 用于 :dtcompatible:`st,stm32-fdcan`
  * :kconfig:option:`CONFIG_CAN_STM32_FDCAN_MAX_STD_ID_FILTERS` 用于 :dtcompatible:`st,stm32-fdcan`
  * :kconfig:option:`CONFIG_CAN_XMC4XXX_MAX_FILTERS` 用于 :dtcompatible:`infineon,xmc4xxx-can-node`

* 将 :dtcompatible:`nxp,flexcan` 和 :dtcompatible:`nxp,flexcan-fd` 的 Kconfig 选项 ``CONFIG_CAN_MAX_MB`` 替换为每个实例的 ``number-of-mb`` 设备树属性（:github:`99483`）。

* :dtcompatible:`nxp,flexcan` 的 ``clk-source`` 设备树属性（如果存在）现在会自动在名为 ``clksrc0`` 和 ``clksrc1`` 的输入时钟之间选择，用作 CAN 协议引擎时钟。

* 由于 NXP LPC 系列 MCAN 驱动并非基于 NXP MCUXpresso HAL，其 Kconfig 选项 ``CONFIG_CAN_MCUX_MCAN`` 已重命名为 :kconfig:option:`CONFIG_CAN_NXP_LPC_MCAN` （:github:`103679`）。

* 为 :dtcompatible:`ti,tcan4x5x` 新增了设备树属性 ``ti,nwkrq-voltage-vio``，用于配置 ``nWKRQ`` 引脚使用的电压轨。为保持驱动此前使用 VIO 的默认行为，必须设置该属性（:github:`104182`）。

文件系统
========

* 如果设备树中存在任何启用了 ``automount`` 属性的 :dtcompatible:`zephyr,fstab,fatfs`，则 :kconfig:option:`CONFIG_FS_FATFS_FSTAB_AUTOMOUNT` 现在默认启用。不想要此行为的应用需要显式禁用该选项。（:github:`103139`）

* NVS 和 ZMS 已移至新的键值存储系统（KVSS）子系统；此次调整涉及 NVS 和 ZMS 接口头文件路径，它们已从 ``zephyr/fs/`` 移至 ``zephyr/kvss/``。NVS 和 ZMS 的 Kconfig 选项已从 “File Systems” 菜单下移至 “Key-Value Storage Systems” 菜单下，没有 Kconfig 受到影响。（:github:`103244`）

时钟控制
========

* ``bflb,bl60x-pll``、``bflb,bl61x-root-clk``、``bflb,bl60x-root-clk``、``bflb,bl61x-wifipll``、``bflb,bl70x-root-clk`` 和 ``bflb,bl61x-flash-clk`` 已分别替换为 :dtcompatible:`bflb,flash-clk`、:dtcompatible:`bflb,pll` 和 :dtcompatible:`bflb,root-clk`。

* :dtcompatible:`infineon,peri-div` 时钟控制绑定移除了 ``resource-type``、``resource-instance`` 和 ``resource-channel`` 属性。驱动不再使用这些属性，且已从驱动的内部数据结构中删除相应字段。使用该 compatible 的树外开发板必须从其设备树节点中删除这些属性。（:github:`105393`）

显示
====

* 对于 ILI9XXX 控制器，设备树中用于选择面板颜色格式的 ``ILI9XXX_PIXEL_FORMAT_x`` 已更新为 ``PANEL_PIXEL_FORMAT_x``。树外开发板和扩展板应相应更新。（:github:`99267`）。

* 对于 ILI9341 控制器，显示镜像配置已更新，以符合示例 ``samples/drivers/display`` 所描述的行为。（:github:`99267`）。此更改会导致某些显示面板出现镜像问题，该问题将在 v4.4.1 版本中妥善修复。（:github:`106862`）

* ``PIXEL_FORMAT_BGR_565`` 像素格式（及其对应的设备树宏 ``PANEL_PIXEL_FORMAT_BGR_565``）已重命名为 :c:enumerator:`PIXEL_FORMAT_RGB_565X` （以及 :c:macro:`PANEL_PIXEL_FORMAT_RGB_565X`），以正确反映它是 RGB-565 的字节交换版本，而不是红蓝通道交换格式。（:github:`99276`）使用 ``PIXEL_FORMAT_BGR_565`` 表示字节交换 RGB-565 的应用和库必须更新为使用 :c:enumerator:`PIXEL_FORMAT_RGB_565X`。

* Kconfig 选项 ``CONFIG_SDL_DISPLAY_DEFAULT_PIXEL_FORMAT_BGR_565`` 和 ``CONFIG_ST7789V_BGR565`` 已分别重命名为 :kconfig:option:`CONFIG_SDL_DISPLAY_DEFAULT_PIXEL_FORMAT_RGB_565X` 和 :kconfig:option:`CONFIG_ST7789V_RGB565X`。（:github:`99276`）

* ``CONFIG_SSD1327`` 符号已重命名为 :kconfig:option:`CONFIG_SSD1327_5`，以同时支持 ``SSD1325``。

* ``solomon,ssd1327fb``、``solomon,ssd1306fb`` 和 ``solomon,ssd1309fb`` 设备树 compatible 已分别重命名为 :dtcompatible:`solomon,ssd1327`、:dtcompatible:`solomon,ssd1306` 和 :dtcompatible:`solomon,ssd1309`，以与其他显示控制器保持一致，并去掉与 Zephyr 无关的 ``fb`` 后缀。

* NXP eLCDIF 控制器（:dtcompatible:`nxp,imx-elcdif`）现在正确地声明支持 :c:macro:`PIXEL_FORMAT_XRGB_8888` 而不是 :c:macro:`PIXEL_FORMAT_ARGB_8888`。

* ``waveshare,7inch-dsi-lcd-c`` 设备树 compatible 已被 :dtcompatible:`waveshare,dsi2dpi` 取代，``CONFIG_WAVESHARE_7INCH_DSI_LCD_C`` 选项已被 :kconfig:option:`CONFIG_WAVESHARE_DSI2DPI` 取代。（:github:`100140`）

* 使用 STM32 LTDC 显示控制器的开发板必须更新其设备树，在 :dtcompatible:`st,stm32-ltdc` 节点中将 ``pixel-format`` 设置为 :c:macro:`PANEL_PIXEL_FORMAT_RGB_888`。（:github:`99277`）

步进电机
========

* 对于 :dtcompatible:`adi,tmc2209`，属性 ``msx-gpios`` 现已被 ``m0-gpios`` 和 ``m1-gpios`` 取代，以与其他 step/dir 步进电机驱动保持一致。

* 多个 API 函数已重命名：

  * ``stepper_move_by`` 重命名为 :c:func:`stepper_ctrl_move_by`。
  * ``stepper_move_to`` 重命名为 :c:func:`stepper_ctrl_move_to`。
  * ``stepper_is_moving`` 重命名为 :c:func:`stepper_ctrl_is_moving`。
  * ``stepper_run`` 重命名为 :c:func:`stepper_ctrl_run`。
  * ``stepper_stop`` 重命名为 :c:func:`stepper_ctrl_stop`。
  * ``stepper_set_reference_position`` 重命名为 :c:func:`stepper_ctrl_set_reference_position`。
  * ``stepper_get_actual_position`` 重命名为 :c:func:`stepper_ctrl_get_actual_position`。
  * ``stepper_set_microstep_interval`` 重命名为 :c:func:`stepper_ctrl_set_microstep_interval`。

* 以下事件已从 :c:enum:`stepper_event` 移至 :c:enum:`stepper_ctrl_event`：

  * ``STEPPER_EVENT_STEPS_COMPLETED`` 重命名为 ``STEPPER_CTRL_EVENT_STEPS_COMPLETED``。
  * ``STEPPER_EVENT_LEFT_END_STOP_DETECTED`` 重命名为 ``STEPPER_CTRL_EVENT_LEFT_END_STOP_DETECTED``。
  * ``STEPPER_EVENT_RIGHT_END_STOP_DETECTED`` 重命名为 ``STEPPER_CTRL_EVENT_RIGHT_END_STOP_DETECTED``。
  * ``STEPPER_EVENT_STOPPED`` 重命名为 ``STEPPER_CTRL_EVENT_STOPPED``。

* ``step-gpios``、``dir-gpios``、``invert-direction`` 和 ``counter`` 属性已从所有 step-dir 步进电机硬件驱动设备的绑定中移除（:dtcompatible:`adi,tmc2209`、:dtcompatible:`ti,drv84xx` 和 :dtcompatible:`allegro,a4979`），并移至新的通用步进电机运动控制器绑定 :dtcompatible:`zephyr,gpio-step-dir-stepper-ctrl`。

* 现在必须通过 :dtcompatible:`zephyr,gpio-step-dir-stepper-ctrl` 设备执行运动控制，该设备通过 ``stepper-driver`` 属性引用步进电机硬件驱动设备树节点。应用必须更新其设备树，添加运动控制器节点并使用 ``stepper_ctrl_*`` API，而不再直接在步进电机硬件驱动设备上调用运动控制函数。

* H 桥步进电机控制器中已移除步进电机硬件驱动专用 API：

  * :dtcompatible:`zephyr,h-bridge-stepper` 已重命名为 :dtcompatible:`zephyr,h-bridge-stepper-ctrl`，以反映它是步进电机运动控制器绑定，而不是步进电机硬件驱动绑定。

  * :c:func:`stepper_enable`、:c:func:`stepper_disable`、:c:func:`stepper_set_micro_step_res` 和 :c:func:`stepper_get_micro_step_res` API 函数不再适用于 :dtcompatible:`zephyr,h-bridge-stepper-ctrl` compatible 设备。

  * ``en-gpios`` 属性已从 :dtcompatible:`zephyr,h-bridge-stepper-ctrl` 中移除。

  * 在 :dtcompatible:`zephyr,h-bridge-stepper-ctrl` 中，``micro-step-res`` 属性已被 ``lut-step-gap`` 取代，以更好地反映 H 桥控制机制，该机制使用查找表插值而非硬件微步进。

  使用 H 桥步进电机控制器的应用必须：

  1. 移除在 H 桥控制器设备上对步进电机硬件驱动专用 API 的调用
  2. 更新设备树，使用 ``lut-step-gap`` 而不是 ``micro-step-res``
  3. 删除 ``en-gpios`` 属性（如果存在）

* :dtcompatible:`adi,tmc50xx` 和 :dtcompatible:`adi,tmc51xx` 设备现在建模为 MFD。

* 移除了用于生成 :kconfig:option:`CONFIG_STEPPER_*_GENERATE_ISR_SAFE_EVENTS` 和 :kconfig:option:`CONFIG_STEPPER_*_EVENT_QUEUE_LEN` 符号的 Kconfig.stepper_event_template 模板

* :kconfig:option:`CONFIG_STEPPER_STEP_DIR_GENERATE_ISR_SAFE_EVENTS` 已被 :kconfig:option:`CONFIG_STEPPER_CTRL_ISR_SAFE_EVENTS` 取代

* :kconfig:option:`CONFIG_STEPPER_STEP_DIR_EVENT_QUEUE_LEN` 已被 :kconfig:option:`CONFIG_STEPPER_CTRL_EVENT_QUEUE_LEN` 取代

* :kconfig:option:`CONFIG_STEPPER_CTRL_ISR_SAFE_EVENTS` 现在默认启用

看门狗
======

* :kconfig:option:`CONFIG_WDT_DISABLE_AT_BOOT` 的语义已明确：``CONFIG_WDT_DISABLE_AT_BOOT=n`` 时的预期行为此前不明确，且各驱动的实现不一致，现已在 :kconfig:option:`CONFIG_WDT_DISABLE_AT_BOOT` 的说明中明确记录（详情请参阅该说明）。

  所有树内看门狗驱动都已更新，以遵循现在已记录的语义。

  值得注意的是，``CONFIG_WDT_DISABLE_AT_BOOT=n`` 不能再用于在启动时 “自动” 启用看门狗。依赖此行为的用户必须更新其应用以显式配置看门狗，如 :zephyr:code-sample:`watchdog` 中所示。以下与此错误用法相关的 Kconfig 选项已被移除：

    * ``CONFIG_IWDG_STM32_INITIAL_TIMEOUT``
    * ``CONFIG_WDT_RPI_PICO_INITIAL_TIMEOUT``
    * ``CONFIG_WDT_CC13XX_CC26XX_INITIAL_TIMEOUT``
    * ``CONFIG_WDT_CC23X0_INITIAL_TIMEOUT``
    * ``CONFIG_WDT_CC32XX_INITIAL_TIMEOUT``

* 更新了 :dtcompatible:`microchip,xec-watchdog` 的 PCR 和 GIRQ 属性，使其使用新的宏（:github:`105668`）。

视频
====

* ``CONFIG_VIDEO_HIMAX_HM01B0`` 已重命名为 :kconfig:option:`CONFIG_VIDEO_HM01B0`。
* ``CONFIG_VIDEO_OV7670`` 现已移除，由 :kconfig:option:`CONFIG_VIDEO_OV767X` 取代。这样可以同时支持 OV7670 和 0V7675。
* :kconfig:option:`CONFIG_VIDEO_BUFFER_POOL_SZ_MAX` 已由 :kconfig:option:`CONFIG_VIDEO_BUFFER_POOL_HEAP_SIZE` 取代，后者表示分配给整个视频缓冲区池的大小（以字节为单位）。

* :dtcompatible:`ovti,ov2640` 的复位引脚处理已修正，导致有效电平与之前相反，以匹配传感器期望的有效电平。

* 为与数据保持一致，以下像素格式已重命名（:github:`105522`）：

  * :c:macro:`VIDEO_PIX_FMT_ARGB32` （与 :c:macro:`VIDEO_PIX_FMT_BGRA32` 互换）
  * :c:macro:`VIDEO_PIX_FMT_BGRA32` （与 :c:macro:`VIDEO_PIX_FMT_ARGB32` 互换）
  * :c:macro:`VIDEO_PIX_FMT_RGBA32` （保持不变）
  * :c:macro:`VIDEO_PIX_FMT_ABGR32` （保持不变）
  * :c:macro:`VIDEO_PIX_FMT_XRGB32` （保持不变）
  * :c:macro:`VIDEO_PIX_FMT_XBGR32` （新增）
  * :c:macro:`VIDEO_PIX_FMT_BGRX32` （新增）
  * :c:macro:`VIDEO_PIX_FMT_RGBX32` （新增）

计数器
======

* 实现 ``get_value_64`` API 的驱动现在需要选择 :kconfig:option:`CONFIG_COUNTER_SUPPORTS_64BITS_TICKS`，应用则需要 :kconfig:option:`CONFIG_COUNTER_64BITS_TICKS` 才能启用该 API。（:github:`94189`）。

* NXP LPTMR 驱动（:dtcompatible:`nxp,lptmr`）已更新，以修正分频器和毛刺滤波器配置错误：

  * ``prescale-glitch-filter`` 属性的有效范围从 ``[0-16]`` 改为 ``[0-15]``。值 ``16`` 在脉冲计数模式下无效，已被移除。使用值 ``16`` 的设备树必须更新为使用 ``[0-15]`` 范围内的值。

  * 新增了一个布尔属性 ``prescale-glitch-filter-bypass``，用于显式控制分频器/毛刺滤波器旁路。此前，设置 ``prescale-glitch-filter = <0>`` 会隐式启用旁路模式，含义不明确。

    在 v4.4 及更高版本中，旁路仅由是否存在 ``prescale-glitch-filter-bypass`` 控制。如果该属性不存在，则分频器/毛刺滤波器处于活动状态，并应用 ``prescale-glitch-filter``。

  * 分频器/毛刺滤波器的行为已明确如下：

    * 定时器计数模式：分频器将时钟除以 ``2^(prescale-glitch-filter + 1)``
    * 脉冲计数模式：毛刺滤波器在 ``2^prescale-glitch-filter`` 个上升沿后识别到变化（毛刺滤波不支持值 0）

  * 所有树内设备树节点均已更新为使用 ``prescale-glitch-filter-bypass;`` 而不是 ``prescale-glitch-filter = <0>;``。树外开发板也应相应更新。

  * 如果同时设置了 ``prescale-glitch-filter-bypass`` 和 ``prescale-glitch-filter``，则旁路模式优先，``prescale-glitch-filter`` 的值将被忽略。

  迁移示例：

  .. code-block:: devicetree

     /* Old (deprecated) */
     lptmr0: counter@40040000 {
         compatible = "nxp,lptmr";
         /* Implicitly bypassed */
         prescale-glitch-filter = <0>;
     };

     /* New (correct) */
     lptmr0: counter@40040000 {
         compatible = "nxp,lptmr";
         /* Explicitly bypassed */
         prescale-glitch-filter-bypass;
     };

  .. rubric:: Examples of using ``prescale-glitch-filter``

  .. note::

     ``prescale-glitch-filter-bypass`` 是一个布尔值。如果存在，则启用旁路；如果不存在，则禁用旁路并应用 ``prescale-glitch-filter``。

     在脉冲计数模式下，``prescale-glitch-filter = <0>`` 不是受支持的毛刺滤波器配置。若要不进行滤波，请使用 ``prescale-glitch-filter-bypass;``。

  * 定时器计数模式：对计数器时钟进行分频

    在定时器计数模式下，分频器除以 ``2^(N + 1)``。

    .. code-block:: devicetree

       /* Divide by 2^(0+1) = 2 */
       lptmr0: counter@40040000 {
           compatible = "nxp,lptmr";
           /* Time Counter mode */
           timer-mode-sel = <0>;
           clk-source = <1>;
           clock-frequency = <32768>;
           /* /2 */
           prescale-glitch-filter = <0>;
           resolution = <16>;
       };

       /* Divide by 2^(3+1) = 16 */
       lptmr1: counter@40041000 {
           compatible = "nxp,lptmr";
           /* Time Counter mode */
           timer-mode-sel = <0>;
           clk-source = <1>;
           clock-frequency = <32768>;
           /* /16 */
           prescale-glitch-filter = <3>;
           resolution = <16>;
       };

  * 定时器计数模式：显式旁路（不分频）

    .. code-block:: devicetree

       lptmr0: counter@40040000 {
           compatible = "nxp,lptmr";
           /* Time Counter mode */
           timer-mode-sel = <0>;
           clk-source = <1>;
           clock-frequency = <32768>;
           /* no prescaler */
           prescale-glitch-filter-bypass;
           resolution = <16>;
       };

  * 脉冲计数模式：毛刺滤波

    在脉冲计数模式下，毛刺滤波器在 ``2^N`` 个上升沿后识别到变化。毛刺滤波不支持值 ``0``；如果不想进行滤波，请使用旁路。

    .. code-block:: devicetree

       /* Recognize change after 2^2 = 4 rising edges */
       lptmr0: counter@40040000 {
           compatible = "nxp,lptmr";
           /* Pulse Counter mode */
           timer-mode-sel = <1>;
           clk-source = <1>;
           input-pin = <0>;
           prescale-glitch-filter = <2>;
           resolution = <16>;
       };

       /* No filtering (explicit bypass) */
       lptmr1: counter@40041000 {
           compatible = "nxp,lptmr";
           /* Pulse Counter mode */
           timer-mode-sel = <1>;
           clk-source = <1>;
           input-pin = <0>;
           prescale-glitch-filter-bypass;
           resolution = <16>;
       };

* NXP i.MX GPT 计数器驱动（:dtcompatible:`nxp,imx-gpt`）现在默认使用 ``run-mode = "restart"``，而不是此前硬编码的自由运行行为。

  * **此前行为** （Zephyr ≤ 4.3）：GPT 计数器始终以自由运行模式运行（``enableFreeRun = true``）。计数器在比较事件时不会复位，而是持续计数。

  * **新行为** （Zephyr ≥ 4.4）：除非显式配置，否则 GPT 计数器默认使用 restart 模式。新增的 ``run-mode`` 设备树属性控制该行为：

    * ``"restart"`` （默认）：计数器达到比较通道 1 的值时复位为 0
    * ``"free-run"``：计数器持续计数而不复位（此前行为）

  **需要迁移**：使用 GPT 计数器的树外开发板和应用必须在其设备树节点中添加 ``run-mode = "free-run";``，以保留此前行为。

  .. code-block:: devicetree

     /* Out-of-tree boards: add this to preserve previous behavior */
     gpt2: gpt@400f0000 {
         compatible = "nxp,imx-gpt";
         /* Explicitly restore Zephyr ≤4.3 behavior */
         run-mode = "free-run";
         /* ... other properties ... */
     };

  .. warning::

     该驱动使用比较通道 1 实现 Zephyr 计数器闹钟功能。使用 ``run-mode = "restart"`` 时，设置闹钟会导致计数器在闹钟比较点复位。如果您的应用依赖闹钟和连续计数，则必须使用 ``run-mode = "free-run"``。

  .. note::

     此更改统一了 NXP 计数器驱动的运行模式配置。GPT 现在使用显式的设备树属性而非硬编码值，从而允许按实例进行自定义。

.. _migration_4.4_devicetree:

设备树
======

* :ref:`dt-bindings` 不再允许为 ``status`` 以及 ``#address-cells``、``#size-cells`` 属性指定任何默认值。这些属性的语义在 Devicetree `Specification <https://www.devicetree.org/specifications>`_ 第 2.3.4 节和 `Specification <https://www.devicetree.org/specifications>`_ 第 2.3.5 节中定义，用户不应尝试用自己的默认值覆盖它们。

  以下绑定语法现在会导致构建错误：

  .. code-block:: yaml

     properties:
       "status":
         default: ...             <---- any default is a build error
       "#address-cells":
         default: ...             <---- any default is a build error
       "#size-cells":
         default: ...             <---- any default is a build error

  如果您此前依赖绑定中的默认值，现在必须在设备树源文件中显式指定这些值，以修复这些构建错误。

* 设备树 compatible ``ilitek,ili9806e-dsi`` 已重命名。请改用 :dtcompatible:`ilitek,ili9806e`。

输入
====

* CST816S 输入驱动已泛化，以支持 CST8xx 系列。驱动和 Kconfig 文件已重命名（:github:`105348`）

  * ``input_cst816s.c`` → ``input_cst8xx.c``
  * ``Kconfig.cst816s`` → ``Kconfig.cst8xx``

  相应的设备树 compatible 已更新：

  * ``hynitron,cst816s`` → :dtcompatible:`hynitron,cst8xx`

  相应的 Kconfig 也已更新：

  * ``CONFIG_INPUT_CST816S`` → :kconfig:option:` CONFIG_INPUT_CST8XX`
  * ``CONFIG_INPUT_CST816S_PERIOD`` → :kconfig:option:` CONFIG_INPUT_CST8XX_PERIOD`
  * ``CONFIG_INPUT_CST816S_INTERRUPT`` → :kconfig:option:` CONFIG_INPUT_CST8XX_INTERRUPT`
  * ``CONFIG_INPUT_CST816S_EV_DEVICE`` → :kconfig:option:` CONFIG_INPUT_CST8XX_EV_DEVICE`

  dt-binding 宏前缀也已从 ``CST816S_*`` 更新为 ``CST8XX_*``。

键盘矩阵
========

* 通用的键盘矩阵设备树绑定已更新，轮询周期属性改用微秒而不是毫秒。

  以下属性已重命名，其单位也已更改：

  * ``poll-period-ms`` -> ``poll-period-us``
  * ``stable-poll-period-ms`` -> ``stable-poll-period-us``

  使用这些属性的应用必须：

  * 将旧属性名替换为新属性名，并且
  * 将值从毫秒转换为微秒。例如，原先表示 10 ms 的值 ``10`` 现在必须写为 ``10000``，表示 10,000 µs。


.. zephyr-keep-sorted-stop

蓝牙
****

蓝牙主机
========

* :kconfig:option:`CONFIG_BT_SIGNING` 已弃用。
* :c:macro:`BT_GATT_CHRC_AUTH` 已弃用。
* :c:member:`bt_conn_le_info.interval` 已弃用。请改用 :c:member:`bt_conn_le_info.interval_us`。注意单位已更改：``interval`` 的单位为 1.25 毫秒，而 ``interval_us`` 的单位为微秒。
* 从蓝牙核心规范 v6.2 起，使用 passkey 输入方法的旧版蓝牙 LE 配对不再提供认证（MITM）保护。使用该方法生成的已存储绑定在从持久化存储加载时将被降级为未认证，从而导致安全级别降低。
* 蓝牙主机不再依赖 :c:func:`k_poll`，因此不再选择 :kconfig:option:`CONFIG_POLL`。如果应用代码本身依赖它，则需要在配置中显式启用 :kconfig:option:`CONFIG_POLL`。
* 将任何 :kconfig:option:`CONFIG_DEVICE_NAME_GATT_WRITABLE_NONE` 的使用替换为 :kconfig:option:`CONFIG_BT_DEVICE_NAME_GATT_WRITABLE_NONE`。
* 将任何 :kconfig:option:`CONFIG_DEVICE_NAME_GATT_WRITABLE_ENCRYPT` 的使用替换为 :kconfig:option:`CONFIG_BT_DEVICE_NAME_GATT_WRITABLE_ENCRYPT`。
* 将任何 :kconfig:option:`CONFIG_DEVICE_NAME_GATT_WRITABLE_AUTHEN` 的使用替换为 :kconfig:option:`CONFIG_BT_DEVICE_NAME_GATT_WRITABLE_AUTHEN`。
* 将任何 :kconfig:option:`CONFIG_DEVICE_APPEARANCE_GATT_WRITABLE_AUTHEN` 的使用替换为 :kconfig:option:`CONFIG_BT_DEVICE_APPEARANCE_GATT_WRITABLE_AUTHEN`。
* :c:struct:`bt_iso_chan` 中的 ``required_sec_level`` 字段已被移除。需要为 CIS 连接设置安全性的应用应在调用 :c:func:`bt_iso_chan_connect` 之前，对 ACL 连接调用 :c:func:`bt_conn_set_security`。
* :c:struct:`bt_iso_server` 中的 ``sec_level`` 字段已被移除。

蓝牙音频
========

* :c:func:`bt_bap_broadcast_assistant_discover` 现在不再在过程结束时读取远程 BASS 接收状态。用户必须在执行任何操作之前，自行调用 :c:func:`bt_bap_broadcast_assistant_read_recv_state` 读取现有的接收状态（如果有）。（:github:`91587`）
* :kconfig:option:`CONFIG_BT_AUDIO` 现在依赖 :kconfig:option:`CONFIG_UTF8`。启用 :kconfig:option:`CONFIG_BT_AUDIO` 的应用也必须启用 :kconfig:option:`CONFIG_UTF8`。（:github:`102350`）
* :c:func:`bt_tbs_set_uri_scheme_list` 现在只接受单个字符串值，而不是 URI 的列表/数组。应用需要将当前输入（例如 ``{"tel", "skype"}``）修改为 ``"tel,skype"``。（:github:`102724`）
* ``CONFIG_BT_TBS_SUPPORTED_FEATURES`` 已被移除。应用应使用已定义的宏 :c:macro:`BT_TBS_FEATURE_HOLD` 和 :c:macro:`BT_TBS_FEATURE_JOIN` 来设置其支持的特性。（:github:`102666`）
* :c:func:`bt_bap_unicast_server_foreach_ep` 和 :c:func:`bt_has_preset_foreach` 现在可能在迭代提前停止或传入无效参数时返回错误。（:github:`105462`）
* :c:func:`bt_bap_unicast_server_foreach_ep`、:c:func:`bt_bap_unicast_group_foreach_stream`、:c:func:`bt_bap_broadcast_source_foreach_stream`、:c:func:`bt_cap_unicast_group_foreach_stream`、:c:func:`bt_cap_initiator_broadcast_foreach_stream` 和 :c:func:`bt_has_preset_foreach` 的回调现在返回 ``true`` 表示继续迭代，返回 ``false`` 表示停止迭代。这些函数的所有回调都需要更新，以反映新的返回类型和返回值。（:github:`105462`）

蓝牙 Mesh
=========

* :kconfig:option:`CONFIG_BT_MESH_MODEL_VND_MSG_CID_FORCE` 已弃用。启用它不再对消息处理性能产生任何影响。

蓝牙 HCI
========

* 请改用 :c:macro:`BT_HCI_LE_SUPERVISION_TIMEOUT_MIN` 和 :c:macro:`BT_HCI_LE_SUPERVISION_TIMEOUT_MAX`，而不要使用 :c:macro:`BT_HCI_LE_SUPERVISON_TIMEOUT_MIN` 和 :c:macro:`BT_HCI_LE_SUPERVISON_TIMEOUT_MAX`，因为后者因拼写错误已被弃用。

网络
****

Wi-Fi
=====

* :c:struct:`wifi_channel_info` 新增了用于设置信道的 ``band`` 字段。对于 2.4 GHz（信道 1–14）和 5 GHz（36–165），行为保持向后兼容：省略 ``band`` 或将其保留为 :c:macro:`WIFI_FREQ_BAND_UNKNOWN`，驱动会推断频段。对于 6 GHz，请将 ``band`` 设置为 :c:macro:`WIFI_FREQ_BAND_6_GHZ` （信道号与 2.4 GHz 的 1–14 重叠）。调用 net_mgmt 时请重新编译，以确保 ``sizeof(struct wifi_channel_info)`` 正确。

* WPA3 通过选择项 ``WIFI_NM_WPA_SUPPLICANT_WPA3_IMPLEMENTATION`` （Internal、External 或 None）进行配置。请将 ``prj.conf`` 中的任何 ``CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3=y`` 行替换为 ``CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3_IMPLEMENTATION_INT=y`` （或按需使用 ``_EXT`` / ``_NONE``）。:kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3` 现在没有提示符，仅在选择 Internal 时被选中；请勿直接赋值。在 C 代码中，建议使用 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3_COMMON` 来检测内部或外部 WPA3。

* 网络 API 位于

  * :zephyr_file:`include/zephyr/net/net_ip.h`
  * :zephyr_file:`include/zephyr/net/socket.h`

  以及 ``subsys/net`` 中的相关代码等都已命名空间化。这意味着网络 API 名称会加上 ``net_``、``NET_`` 或 ``ZSOCK_`` 前缀。这样做是为了避免与 POSIX 或 libc 中可能定义同名符号而产生循环依赖。已创建兼容性头文件 :zephyr_file:`include/zephyr/net/net_compat.h`，提供旧符号，允许用户继续使用旧符号。外部网络应用可以继续使用 POSIX 定义的网络符号，并包含 ``sys/socket.h`` 等相关 POSIX 头文件来获取 POSIX 符号，因为 Zephyr 网络头文件将不再包含它们。如果应用或 Zephyr 内部代码无法使用 POSIX API，则需要在调用网络 API 的代码中加上相应的网络 API 前缀。

* :c:type:`net_icmp_handler_t` 的返回类型已从 ``int`` 改为 :c:enum:`net_verdict`。（:github:`104815`）

* HTTP 服务器事务状态的枚举已从 ``http_data_status`` 重命名为 ``http_transaction_status``，以更好地反映其用途。枚举值也已重命名如下：

  - ``HTTP_SERVER_DATA_ABORTED`` → ``HTTP_SERVER_TRANSACTION_ABORTED``
  - ``HTTP_SERVER_DATA_MORE`` → ``HTTP_SERVER_REQUEST_DATA_MORE``
  - ``HTTP_SERVER_DATA_FINAL`` → ``HTTP_SERVER_REQUEST_DATA_FINAL``

  动态资源的处理程序回调类型也已相应更新为使用新枚举及其重命名后的值。使用动态 HTTP 资源的应用必须更新其处理程序回调，以使用新枚举并处理重命名后的值。

* HTTP 服务器现在会在响应完整发送给客户端后，为动态资源报告 ``HTTP_SERVER_TRANSACTION_COMPLETE`` 状态。应用现在还应在其处理程序回调中处理该状态，以便在响应成功发送后正确重置资源状态。

* 创建安全套接字时传递给 :c:func:`zsock_socket` 的协议版本现在被强制要求用作 TLS 会话的最低 TLS 版本。

* 已从 :kconfig:option:`NET_SOCKETS_SOCKOPT_TLS` 中移除加密 Kconfig 的自动选择，因为它们很大程度上取决于最终应用的需求。因此，必须显式选择所需的 TLS 协议版本和密码套件。可使用 :kconfig:option-regex:`CONFIG_MBEDTLS_CIPHERSUITE_TLS_.*` Kconfig 辅助选项自动启用给定密码套件的所有依赖项，并可按需按照相同模式添加更多。

CoAP
====

* CoAP ``.well-known/core`` 响应的资源相关元数据现在使用专用的 :c:member:`coap_resource.metadata` 指针配置，而不再使用 :c:member:`coap_resource.user_data`，后者应保留供应用独占使用。实现 CoAP ``.well-known/core`` 处理的应用应更新为使用新指针。

* ``COAP_RESPONSE_CODE_OK`` 2.00 响应码定义已被移除，因为它不是有效的响应码——它未在 :rfc:`7252` 中定义，也未在 IANA 注册表（https://www.iana.org/assignments/core-parameters/core-parameters.xhtml#response-codes）中分配。

调制解调器
**********

Modem HL78XX
============

* 与 HL78XX 启动时序相关的 Kconfig 选项已如下重命名为 :kconfig:option:`CONFIG_MODEM_HL78XX_DEV_*`：

  - ``MODEM_HL78XX_DEV_POWER_PULSE_DURATION`` → ``MODEM_HL78XX_DEV_POWER_PULSE_DURATION_MS``
  - ``MODEM_HL78XX_DEV_RESET_PULSE_DURATION`` → ``MODEM_HL78XX_DEV_RESET_PULSE_DURATION_MS``
  - ``MODEM_HL78XX_DEV_STARTUP_TIME`` → ``MODEM_HL78XX_DEV_STARTUP_TIME_MS``
  - ``MODEM_HL78XX_DEV_SHUTDOWN_TIME`` → ``MODEM_HL78XX_DEV_SHUTDOWN_TIME_MS``

* 默认启动时序已从 1000 ms 改为 120 ms，以提高所有受支持开发板的初始化可靠性。

  依赖此前默认值的应用必须更新其配置。

LoRaWAN
*******

* LoRaWAN 区域的 Kconfig 符号已从 ``LORAMAC_REGION_*`` 重命名为 ``LORAWAN_REGION_*``，以使其与后端无关。使用以下任何符号的应用必须更新其配置文件：

  * ``CONFIG_LORAMAC_REGION_AS923`` → :kconfig:option:`CONFIG_LORAWAN_REGION_AS923`
  * ``CONFIG_LORAMAC_REGION_AU915`` → :kconfig:option:`CONFIG_LORAWAN_REGION_AU915`
  * ``CONFIG_LORAMAC_REGION_CN470`` → :kconfig:option:`CONFIG_LORAWAN_REGION_CN470`
  * ``CONFIG_LORAMAC_REGION_CN779`` → :kconfig:option:`CONFIG_LORAWAN_REGION_CN779`
  * ``CONFIG_LORAMAC_REGION_EU433`` → :kconfig:option:`CONFIG_LORAWAN_REGION_EU433`
  * ``CONFIG_LORAMAC_REGION_EU868`` → :kconfig:option:`CONFIG_LORAWAN_REGION_EU868`
  * ``CONFIG_LORAMAC_REGION_KR920`` → :kconfig:option:`CONFIG_LORAWAN_REGION_KR920`
  * ``CONFIG_LORAMAC_REGION_IN865`` → :kconfig:option:`CONFIG_LORAWAN_REGION_IN865`
  * ``CONFIG_LORAMAC_REGION_US915`` → :kconfig:option:`CONFIG_LORAWAN_REGION_US915`
  * ``CONFIG_LORAMAC_REGION_RU864`` → :kconfig:option:`CONFIG_LORAWAN_REGION_RU864`

其他子系统
**********

CFB
===

* 改用有符号值表示坐标。因此，:c:func:`cfb_print`、:c:func:`cfb_invert_area` 和 :c:struct:`cfb_position` 的定义有所变化。

* DAP 子系统的初始化和配置已更改。请参阅 :zephyr:code-sample:`cmsis-dap` 示例，了解如何使用 USB 后端初始化 Zephyr DAP Link。

* 缓存

  * 请使用 :kconfig:option:`CONFIG_CACHE_HAS_MIRRORED_MEMORY_REGIONS` 而不是 :kconfig:option:`CONFIG_CACHE_DOUBLEMAP`，因为前者更能描述该特性。

Flash
=====

* 此前已弃用的 ``CONFIG_FLASH_AREA_CHECK_INTEGRITY_MBEDTLS`` 现已移除。

* ``CONFIG_FLASH_AREA_CHECK_INTEGRITY_PSA`` 也已被移除，因为现在加密库后端已没有其他选择。

* flash shell 命令 ``flash erase`` 和 ``flash write`` 现在需要显式指定设备参数。这可以避免意外损坏设备的程序闪存。

闪存映射
========

* 以下 :zephyr_file:`include/zephyr/storage/flash_map.h` 宏已弃用并被替换：

  +-------------------------------------------+-------------------------------------+
  | 已弃用宏                                  | 替代宏                              |
  +===========================================+=====================================+
  | :c:macro:`FIXED_PARTITION_EXISTS`         | :c:macro:`PARTITION_EXISTS`         |
  +-------------------------------------------+-------------------------------------+
  | :c:macro:`FIXED_PARTITION_ID`             | :c:macro:`PARTITION_ID`             |
  +-------------------------------------------+-------------------------------------+
  | :c:macro:`FIXED_PARTITION_OFFSET`         | :c:macro:`PARTITION_OFFSET`         |
  +-------------------------------------------+-------------------------------------+
  | :c:macro:`FIXED_PARTITION_ADDRESS`        | :c:macro:`PARTITION_ADDRESS`        |
  +-------------------------------------------+-------------------------------------+
  | :c:macro:`FIXED_PARTITION_NODE_ADDRESS`   | :c:macro:`PARTITION_NODE_ADDRESS`   |
  +-------------------------------------------+-------------------------------------+
  | :c:macro:`FIXED_PARTITION_NODE_OFFSET`    | :c:macro:`PARTITION_NODE_OFFSET`    |
  +-------------------------------------------+-------------------------------------+
  | :c:macro:`FIXED_PARTITION_SIZE`           | :c:macro:`PARTITION_SIZE`           |
  +-------------------------------------------+-------------------------------------+
  | :c:macro:`FIXED_PARTITION_NODE_SIZE`      | :c:macro:`PARTITION_NODE_SIZE`      |
  +-------------------------------------------+-------------------------------------+
  | :c:macro:`FIXED_PARTITION_DEVICE`         | :c:macro:`PARTITION_DEVICE`         |
  +-------------------------------------------+-------------------------------------+
  | :c:macro:`FIXED_PARTITION_NODE_DEVICE`    | :c:macro:`PARTITION_NODE_DEVICE`    |
  +-------------------------------------------+-------------------------------------+
  | :c:macro:`FIXED_PARTITION_MTD`            | :c:macro:`PARTITION_MTD`            |
  +-------------------------------------------+-------------------------------------+
  | :c:macro:`FIXED_PARTITION_NODE_MTD`       | :c:macro:`PARTITION_NODE_MTD`       |
  +-------------------------------------------+-------------------------------------+
  | :c:macro:`FIXED_PARTITION_BY_NODE`        | :c:macro:`PARTITION_BY_NODE`        |
  +-------------------------------------------+-------------------------------------+

  这些新宏还增加了对 :dtcompatible:`zephyr,mapped-partition` 绑定的支持。

JWT
===

* 此前已弃用的 ``CONFIG_JWT_SIGN_RSA_LEGACY`` 已被移除。此次移除早于通常的两个版本弃用期，因为已达成共识（参见 :github:`97660`）：Mbed TLS 属于外部模块，因此常规弃用规则在此情况下不适用。

Libsbc
======

* Libsbc（sbc.c 和 sbc.h）已移至蓝牙子系统下。sbc.h 现在位于 include/zephyr/bluetooth 中。

管理
====

* hawkBit

  * 已弃用的 Kconfig 选项 ``CONFIG_HAWKBIT_DDI_NO_SECURITY`` 已被移除。（:github:`105150`）

* MCUmgr

  * 如果使用 :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_UART`，则现在还必须选择 :kconfig:option:`CONFIG_UART_MCUMGR`，该依赖已从 ``select`` 改为 ``depends on``。

随机数
======

* ``CONFIG_CSPRNG_AVAILABLE`` 已重命名为 :kconfig:option:`CONFIG_ENTROPY_NODE_ENABLED`。

跟踪
====

* CTF：CTF 元数据事件头中的 uint8_t id 已改为 uint16_t id。这使事件 ID 占用的空间翻倍，但可支持 65,535 个事件，而不是 255 个。

  此更改后，现有使用 8 位 ID 的 CTF 跟踪将不再兼容。

串行接口
========

* pl011 UART 驱动：从 :c:func:`pl011_poll_in` 中移除读取状态寄存器（RSR）错误处理。RSR 处理已在 :c:func:`pl011_err_check` 中实现，该函数是检测并报告接收错误状况的合适位置。（:github:`101715`）

Settings
========

* ``CONFIG_SETTINGS_TFM_ITS`` 已重命名为 :kconfig:option:`CONFIG_SETTINGS_TFM_PSA`。

模块
****

HostAP
======

* Kconfig 选项 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_MBEDTLS_PSA` 现在默认启用。

Mbed TLS
========

* Mbed TLS 已升级到 4.1.0 版本。此后，本仓库将只包含 TLS 和 X.509，加密支持已移至 TF-PSA-Crypto。后者新增了一个 west 模块，基于上游 1.1.0 版本。TF-M 仍继续使用 Mbed TLS 3.6.5 构建。此更改在加密方面带来了许多变化，因此强烈建议参阅官方 `Mbed TLS 3.x to TF-PSA-Crypto 1.x migration guide <https://github.com/Mbed-TLS/TF-PSA-Crypto/blob/development/docs/1.0-migration-guide.md>`_。

* ``CONFIG_MBEDTLS_ENTROPY_POLL_ZEPHYR`` 已重命名为 :kconfig:option:`CONFIG_MBEDTLS_PSA_DRIVER_GET_ENTROPY`。

* ``CONFIG_MBEDTLS_PEM_CERTIFICATE_FORMAT`` 已由其此前启用的底层选项取代： :kconfig:option:`CONFIG_MBEDTLS_PEM_PARSE_C`、:kconfig:option:`CONFIG_MBEDTLS_PEM_WRITE_C` 和 :kconfig:option:`CONFIG_MBEDTLS_BASE64_C`。

* ``CONFIG_MBEDTLS_SERVER_NAME_INDICATION`` 已重命名为 :kconfig:option:`CONFIG_MBEDTLS_SSL_SERVER_NAME_INDICATION`。

* ``CONFIG_MBEDTLS_TEST`` 已重命名为 :kconfig:option:`CONFIG_MBEDTLS_DEBUG_C`。

* 以下与 PSA 相关的 Kconfig 符号已被移除，因为 TF-PSA-Crypto 不再支持它们：

  * ``CONFIG_PSA_WANT_KEY_TYPE_DES``
  * ``CONFIG_PSA_WANT_ECC_SECP_R1_192``
  * ``CONFIG_PSA_WANT_ECC_SECP_K1_192``
  * ``CONFIG_PSA_WANT_ECC_SECP_R1_224``

* 以下 Mbed TLS Kconfig 符号已被移除：

  * ``CONFIG_CUSTOM_MBEDTLS_CFG_FILE``
  * ``CONFIG_MBEDTLS_CHACHAPOLY_AEAD_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_AES_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_CAMELLIA_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_CCM_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_CHACHA20_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_DES_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_GCM_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_MODE_CBC_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_MODE_CTR_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_MODE_XTS_ENABLED``
  * ``CONFIG_MBEDTLS_CMAC``
  * ``CONFIG_MBEDTLS_DHM_C``
  * ``CONFIG_MBEDTLS_ECDH_C``
  * ``CONFIG_MBEDTLS_ECDSA_C``
  * ``CONFIG_MBEDTLS_ECDSA_DETERMINISTIC``
  * ``CONFIG_MBEDTLS_ECJPAKE_C``
  * ``CONFIG_MBEDTLS_ECP_ALL_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_C``
  * ``CONFIG_MBEDTLS_ECP_DP_BP256R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_BP384R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_BP512R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_CURVE25519_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_CURVE448_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP192K1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP192R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP224K1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP224R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP256K1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP256R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP384R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP521R1_ENABLED``
  * ``CONFIG_MBEDTLS_GENPRIME_ENABLED``
  * ``CONFIG_MBEDTLS_HKDF_C``
  * ``CONFIG_MBEDTLS_KEY_EXCHANGE_DHE_PSK_ENABLED``
  * ``CONFIG_MBEDTLS_KEY_EXCHANGE_DHE_RSA_ENABLED``
  * ``CONFIG_MBEDTLS_KEY_EXCHANGE_RSA_ENABLED``
  * ``CONFIG_MBEDTLS_KEY_EXCHANGE_RSA_PSK_ENABLED``
  * ``CONFIG_MBEDTLS_MD5``
  * ``CONFIG_MBEDTLS_PKCS1_V15``
  * ``CONFIG_MBEDTLS_PKCS1_V21``
  * ``CONFIG_MBEDTLS_POLY1305``
  * ``CONFIG_MBEDTLS_RSA_C``
  * ``CONFIG_MBEDTLS_SHA1``
  * ``CONFIG_MBEDTLS_SHA224``
  * ``CONFIG_MBEDTLS_SHA256``
  * ``CONFIG_MBEDTLS_SHA384``
  * ``CONFIG_MBEDTLS_SHA512``
  * ``CONFIG_MBEDTLS_USE_PSA_CRYPTO``

OpenThread
==========

* 以下 Kconfig 选项已重命名：

  * ``CONFIG_OPENTHREAD_MBEDTLS_CHOICE`` 重命名为 :kconfig:option:`CONFIG_OPENTHREAD_SECURITY_DEFAULT_CONFIG`
  * ``CONFIG_CUSTOM_OPENTHREAD_SECURITY`` 重命名为 :kconfig:option:`CONFIG_OPENTHREAD_SECURITY_CUSTOM_CONFIG`

* :kconfig:option:`CONFIG_OPENTHREAD_CRYPTO_PSA` 不再依赖 :kconfig:option:`CONFIG_PSA_CRYPTO_CLIENT`，而是选择 :kconfig:option:`CONFIG_PSA_CRYPTO`。

* 在不使用 TF-M 的构建中，如果设置了 :kconfig:option:`CONFIG_OPENTHREAD_SECURITY_DEFAULT_CONFIG` 和 :kconfig:option:`CONFIG_OPENTHREAD_CRYPTO_PSA`，则现在会自动隐含 :kconfig:option:`CONFIG_SECURE_STORAGE`。这保证了 PSA ITS 实现可用，并且需要为安全存储配置后端（Settings、ZMS 或自定义后端）。

* :kconfig:option:`CONFIG_OPENTHREAD_CRYPTO_PSA` 现在默认启用。

* 随着 Mbed TLS 升级到 4.1.0 版本，Zephyr 中不再提供旧版加密支持。因此 ``CONFIG_OPENTHREAD_CRYPTO_LEGACY_MBEDTLS_CONFIG`` 已被移除。:kconfig:option:`CONFIG_OPENTHREAD_CRYPTO_PSA_CONFIG` 此前已是加密支持的默认选择，现在则是唯一受支持的加密选项。

Trusted Firmware-M
==================

* ``SECURE_UART1`` TF-M 定义现在由 Zephyr 的 :kconfig:option:`CONFIG_TFM_SECURE_UART` 控制。该选项将覆盖此前在 TF-M 仓库中指定的任何平台值。

架构
****

* 将 ``CONFIG_ARCH_HAS_COHERENCE`` 重命名为 :kconfig:option:`CONFIG_CACHE_CAN_SAY_MEM_COHERENCE`，因为该特性与缓存相关，所以将其移至缓存下。

  * 请使用 :c:func:`sys_cache_is_mem_coherent` 而不是 :c:func:`arch_mem_coherent`。

* :kconfig:option:`CONFIG_RISCV` 现在要求设备树中存在 :dtcompatible:`riscv`。

* :dtcompatible:`riscv` 的 ``riscv,isa-base`` 和 ``riscv,isa-extensions`` 设备树属性现在用于设置基础整数指令集和 RISC-V 扩展。它们不再由 SoC 设置。设备树属性 ``riscv,isa`` 已弃用，取而代之的是这两个新属性。（:github:`97540`）

  * ``CONFIG_SOC_CV64A6_IMAFDC`` 和 ``CONFIG_SOC_CV64A6_IMAC`` 现在合并为 :kconfig:option:`CONFIG_SOC_CV64A6`，因为 RISC-V 扩展现在由设备树设置。

  * :kconfig:option:`CONFIG_SOC_SERIES_AE350` 的以下选项已被移除，因为它们现在可以通过设备树设置：

    * ``CONFIG_RV32I_CPU``
    * ``CONFIG_RV32E_CPU``
    * ``CONFIG_RV64I_CPU``
    * ``CONFIG_NO_FPU``
    * ``CONFIG_SINGLE_PRECISION_FPU``
    * ``CONFIG_DOUBLE_PRECISION_FPU``
