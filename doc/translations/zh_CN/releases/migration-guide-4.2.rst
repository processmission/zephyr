.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

..
  See
  https://docs.zephyrproject.org/latest/releases/index.html#migration-guides
  for details of what is supposed to go into this document.

.. _migration_4.2:

Zephyr v4.2.0 迁移指南
######################

本文档介绍将应用从 Zephyr v4.1.0 迁移到 Zephyr v4.2.0 所需的变更。

其他变更（与迁移应用不直接相关）请参见 :ref:`版本说明 <zephyr_4.2>`。

.. contents::
    :local:
    :depth: 2

构建系统
********

* HWMv1 支持已被移除。任何采用 HWMv1 格式的树外开发板或 SoC 都必须迁移到 :ref:`HWMv2 <hw_model_v2>`，才能在 Zephyr v4.2 及更高版本中正常工作。

内核
****

开发板
******

* 所有默认使用 ``nrfjprog`` Nordic 命令行工具进行烧录的基于 Nordic IC 的开发板，均已改为默认使用新的 nRF Util（``nrfutil``）工具。这意味着你可能需要 `安装 nRF Util <https://www.nordicsemi.com/Products/Development-tools/nrf-util>`_，或者，如果你更希望继续使用 ``nrfjprog``，可以在调用 west 时指定 runner 来做到：``west flash -r nrfjprog``。nRF Util 的完整文档见 `此处 <https://docs.nordicsemi.com/bundle/nrfutil/page/README.html>`_。

* 所有基于 nRF54L 系列 Nordic IC 的开发板，现在默认在烧录时不擦除内部存储的任何部分。如果你想恢复以前默认擦除待烧录固件将要写入的页面的行为，可以在调用 ``west flash`` 时将新的 ``--erase-mode`` 命令行开关设置为 ``ranges``。请注意，nRF54L 器件上的 RRAM 在物理上并非按页组织，分页只是为了便于将 nRF52 软件迁移到 nRF54L 器件而人为提供的，页大小为 4096 字节。

* 配置选项 :kconfig:option:`CONFIG_NATIVE_POSIX_SLOWDOWN_TO_REAL_TIME` 已弃用，取而代之的是 :kconfig:option:`CONFIG_NATIVE_SIM_SLOWDOWN_TO_REAL_TIME`。

* 设备树绑定 :dtcompatible:`zephyr,native-posix-cpu` 已弃用，取而代之的是 :dtcompatible:`zephyr,native-sim-cpu`。

* Zephyr 现在支持 :zephyr:board:`neorv32` 的 1.11.6 版本。NEORV32 处理器（SoC）实现需要更新到此版本，才能与 Zephyr v4.2.0 兼容。

* :zephyr:board:`neorv32` 现在通过开发板变体来面向 NEORV32 处理器（SoC）模板。旧的 ``neorv32`` 开发板目标现在命名为 ``neorv32/neorv32/up5kdemo``。

* ``arduino_uno_r4_minima``、``arduino_uno_r4_wifi`` 和 ``mikroe_clicker_ra4m1`` 已迁移到新的基于 FSP 的配置。虽然没有重大的功能变更，但设备树结构已大幅修改。以下设备树绑定现已被移除：``renesas,ra-gpio``、``renesas,ra-uart-sci``、``renesas,ra-pinctrl``、``renesas,ra-clock-generation-circuit`` 和 ``renesas,ra-interrupt-controller-unit``。请改用以下替代项：- :dtcompatible:`renesas,ra-gpio-ioport` - :dtcompatible:`renesas,ra-sci-uart` - :dtcompatible:`renesas,ra-pinctrl-pfs` - :dtcompatible:`renesas,ra-cgc-pclk-block`

* Nucleo WBA52CG 开发板（``nucleo_wba52cg``）不再受支持，因为它已属于 NRND（Not Recommended for New Design，不推荐用于新设计），并且 STM32CubeWBA 从 1.1.0 版（2023 年 7 月）起也不再支持它。建议迁移到 :zephyr:board:`nucleo_wba55cg` 开发板（``nucleo_wba55cg``），迁移无需任何改动。

* Espressif 开发板 ``esp32_devkitc_wroom`` 和 ``esp32_devkitc_wrover`` 的特性几乎完全相同。两者的差异已由 Kconfig 选项覆盖，因此这两个开发板已合并为 ``esp32_devkitc``。

* STM32 开发板现在应通过包含 ``openocd-stm32.board.cmake`` 而不是 ``openocd.board.cmake`` 来添加 OpenOCD 烧录支持。``openocd-stm32.board.cmake`` 文件在默认 OpenOCD runner 的基础上扩展了厂商特定的配置，例如 STM32 批量擦除命令。

* STM32N6570-DK 开发板的默认变体（``stm32n6570_dk/stm32n657xx``）现在应为链式加载应用，并且应使用 ``--sysbuild`` 构建。旧的默认变体构建的是作为 First Stage BootLoader 运行的应用，现在它作为专用变体（``stm32n6570_dk/stm32n657xx/fsbl``）提供，必须显式选择。有关这些变体的更多信息，请参见开发板文档。

* 内嵌 TF-M BL2 启动阶段的 STM32 开发板（``b_u585i_iot02a//ns``、``nucleo_l552ze_q//ns`` 和 ``stm32l562e_dk//ns``）不再像以前那样在 BL2 中内嵌硬件加密加速器驱动，而是依赖 Mbed TLS 软件实现。这与升级到 TF-M v2.2 有关。硬件加密加速器在 TF-M 中仍然受支持，但仅限于运行时安全固件中使用。

设备驱动与设备树
****************

.. zephyr-keep-sorted-start re(^\w)

DAI
===

* 将设备树属性 ``dai_id`` 重命名为 ``dai-id``。
* 将设备树属性 ``afe_name`` 重命名为 ``afe-name``。
* 将设备树属性 ``agent_disable`` 重命名为 ``agent-disable``。
* 将设备树属性 ``ch_num`` 重命名为 ``ch-num``。
* 将设备树属性 ``mono_invert`` 重命名为 ``mono-invert``。
* 将设备树属性 ``quad_ch`` 重命名为 ``quad-ch``。
* 将设备树属性 ``int_odd`` 重命名为 ``int-odd``。

DMA
===

* 将设备树属性 ``nxp,a_on`` 重命名为 ``nxp,a-on``。
* 将设备树属性 ``dma_channels`` 重命名为 ``dma-channels``。
* Xilinx DMA 控制器的绑定文件已重命名，以使用正确的厂商前缀（``xlnx`` 而非 ``xilinx``）并与兼容字符串保持一致。

EEPROM
======

* :dtcompatible:`ti,tmp116-eeprom` 已重命名为 :dtcompatible:`ti,tmp11x-eeprom`，因为它同时支持 tmp117 和 tmp119。

Flash
=====

* 将文件从 ``flash_hp_ra.h`` 重命名为 ``soc_flash_renesas_ra_hp.h``。
* 将文件从 ``flash_hp_ra.c`` 重命名为 ``soc_flash_renesas_ra_hp.c``。
* 将文件从 ``flash_hp_ra_ex_op.c`` 重命名为 ``soc_flash_renesas_ra_hp_ex_op.c``。

* Flash HP Renesas RA 双存储体模式 Kconfig 符号 :kconfig:option:`CONFIG_DUAL_BANK_MODE` 已被移除。
* Flash HP Renesas RA Kconfig 符号 :kconfig:option:`CONFIG_RA_FLASH_HP` 已重命名为 :kconfig:option:`CONFIG_SOC_FLASH_RENESAS_RA_HP`。
* Flash HP Renesas RA 写保护 Kconfig 符号 :kconfig:option:`CONFIG_FLASH_RA_WRITE_PROTECT` 已重命名为 :kconfig:option:`CONFIG_FLASH_RENESAS_RA_HP_WRITE_PROTECT`。

* 将文件 ``renesas,ra-nv-flash.yaml`` 拆分为 2 个文件：``renesas,ra-nv-code-flash.yaml`` 和 ``renesas,ra-nv-data-flash.yaml``。
* 将 ``compatible`` 从 ``renesas,ra-nv-flash`` 分离为 :dtcompatible:`renesas,ra-nv-code-flash.yaml` 和 :dtcompatible:`renesas,ra-nv-data-flash.yaml`。

GPIO
====

* 为了支持引脚数量较多的 RP2350B，Raspberry Pi-GPIO 的配置已更改。原先 :dtcompatible:`raspberrypi,rpi-gpio` 的角色已迁移到 :dtcompatible:`raspberrypi,rpi-gpio-port`，而 :dtcompatible:`raspberrypi,rpi-gpio` 现在作为占位和映射节点保留。相应的标签也已更改，因此常规使用无需做任何调整。
* ``arduino-nano-header-r3`` 已重命名为 :dtcompatible:`arduino-nano-header`。因为 R3 来自 Arduino UNO R3，它的连接器与前代版本相比有所变化，与 Arduino Nano 无关。
* 将文件 ``include/zephyr/dt-bindings/gpio/nordic-npm1300-gpio.h`` 移到 :zephyr_file:`include/zephyr/dt-bindings/gpio/nordic-npm13xx-gpio.h`，并将所有定义中的 ``NPM1300`` 重命名为 ``NPM13XX``
* 将 ``CONFIG_GPIO_NPM1300`` 重命名为 :kconfig:option:`CONFIG_GPIO_NPM13XX`，将 ``CONFIG_GPIO_NPM1300_INIT_PRIORITY`` 重命名为 :kconfig:option:`CONFIG_GPIO_NPM13XX_INIT_PRIORITY`

I2S
===
* :dtcompatible:`nxp,mcux-i2s` 驱动新增了 ``mclk-output`` 属性。将该属性设置为
* 可将 MCLK 信号配置为输出。较早的驱动版本使用宏
* ``I2S_OPT_BIT_CLK_SLAVE`` 来配置 MCLK 信号方向。（:github:`88554`）

LED
===

* 将 ``CONFIG_LED_NPM1300`` 重命名为 :kconfig:option:`CONFIG_LED_NPM13XX`

MFD
===

* 将文件 ``include/zephyr/drivers/mfd/npm1300.h`` 移到 :zephyr_file:`include/zephyr/drivers/mfd/npm13xx.h`，并将枚举和函数名中所有 ``npm1300``/``NPM1300`` 重命名为 ``npm13xx``/``NPM13XX``
* 将 ``CONFIG_MFD_NPM1300`` 重命名为 :kconfig:option:`CONFIG_MFD_NPM13XX`，将 ``CONFIG_MFD_NPM1300_INIT_PRIORITY`` 重命名为 :kconfig:option:`CONFIG_MFD_NPM13XX_INIT_PRIORITY`

SPI
===

* 将 ``CONFIG_SPI_MCUX_LPSPI`` 重命名为 :kconfig:option:`CONFIG_SPI_NXP_LPSPI`，该驱动的所有子配置也相应重命名，包括 :kconfig:option:`CONFIG_SPI_NXP_LPSPI_DMA` 和 :kconfig:option:`CONFIG_SPI_NXP_LPSPI_CPU`。
* 将设备树属性 ``port_sel`` 重命名为 ``port-sel``。
* 将设备树属性 ``chip_select`` 重命名为 ``chip-select``。
* :dtcompatible:`andestech,atcspi200` 的绑定文件已重命名，以使其名称与兼容字符串一致。

qSPI/oSPI/xSPI
==============

* 在 STM32 器件上，外部存储器的设备树描述中，大小和地址现在拆分为两个独立属性，以符合规范建议。

  例如，以下外部 flash 描述 ``reg = <0x70000000 DT_SIZE_M(64)>; /* 512 Mbits /`` 会改为 ``reg = <0>;`` ``size = <DT_SIZE_M(512)>; / 512 Mbits */``。

  请注意，该属性给出的是存储器件以比特为单位的实际大小。以前的映射地址信息现在在 SoC dtsi 层的 xspi、ospi 或 qspi 节点中描述。

串行接口
========

* ``uart_native_posix`` 已重命名为 ``uart_native_pty``，其 Kconfig 选项和设备树绑定也一并重命名。:dtcompatible:`zephyr,native-posix-uart` 已弃用，取而代之的是 :dtcompatible:`zephyr,native-pty-uart`。:kconfig:option:`CONFIG_UART_NATIVE_POSIX` 及其相关选项已替换为 :kconfig:option:`CONFIG_UART_NATIVE_PTY`。选择项 :kconfig:option:`CONFIG_NATIVE_UART_0` 已替换为 :kconfig:option:`CONFIG_UART_NATIVE_PTY_0`，而且现在还可以在运行时通过命令行选项 ``--<uart_name>_stdinout`` 选择将 UART 连接到进程的 stdin/stdout 而不是 PTY。:kconfig:option:`CONFIG_NATIVE_UART_AUTOATTACH_DEFAULT_CMD` 已替换为 :kconfig:option:`CONFIG_UART_NATIVE_PTY_AUTOATTACH_DEFAULT_CMD`。:kconfig:option:`CONFIG_UART_NATIVE_WAIT_PTS_READY_ENABLE` 已弃用，它原先启用的功能现在始终启用，因为这样做没有任何缺点。:kconfig:option:`CONFIG_UART_NATIVE_POSIX_PORT_1_ENABLE` 已弃用，该选项现在不起任何作用。用户应改为按所需的原生 PTY UART 实例数量实例化相应数量的 :dtcompatible:`zephyr,native-pty-uart` 节点。（:github:`86739`）

以太网
======

* 移除了 Kconfig 选项 ``ETH_STM32_HAL_MII``，参见 :github:`86074`。PHY 接口类型现在通过设备树中的 ``phy-connection-type`` 属性选择。

* :dtcompatible:`st,stm32-ethernet` 驱动现在要求将 ``phy-handle`` phandle 设置为设备树中对应的 PHY 节点（:github:`87593`）。

* Kconfig 选项 ``ETH_STM32_HAL_PHY_ADDRESS``、``ETH_STM32_CARRIER_CHECK``、``ETH_STM32_CARRIER_CHECK_RX_IDLE_TIMEOUT_MS``、``ETH_STM32_AUTO_NEGOTIATION_ENABLE``、``ETH_STM32_SPEED_10M``、``ETH_STM32_MODE_HALFDUPLEX`` 已被移除，因为它们不再需要；驱动现在使用以太网 PHY API 与 PHY 驱动通信，由后者负责配置 PHY 设置（:github:`87593`）。

* ``ethernet_native_posix`` 已重命名为 ``ethernet_native_tap``，其 Kconfig 选项也一并重命名：:kconfig:option:`CONFIG_ETH_NATIVE_POSIX` 及其相关选项已弃用，取而代之的是 :kconfig:option:`CONFIG_ETH_NATIVE_TAP`，参见 :github:`86578`。

* NuMaker 以太网驱动 ``eth_numaker.c`` 现在支持 ``gen_random_mac``，并且 EMAC 数据 flash 功能已被移除（:github:`87953`）。

* :zephyr_file:`include/zephyr/net/ethernet.h` 中的枚举 ``ETHERNET_DSA_MASTER_PORT`` 和 ``ETHERNET_DSA_SLAVE_PORT`` 已重命名为 ``ETHERNET_DSA_CONDUIT_PORT`` 和 ``ETHERNET_DSA_USER_PORT``。

* 以太网速度相关的枚举已重命名，以更独立于所使用的介质。``LINK_HALF_10BASE_T``、``LINK_FULL_10BASE_T``、``LINK_HALF_100BASE_T``、``LINK_FULL_100BASE_T``、``LINK_HALF_1000BASE_T``、``LINK_FULL_1000BASE_T``、``LINK_FULL_2500BASE_T`` 和 ``LINK_FULL_5000BASE_T`` 已重命名为 :c:enumerator:`LINK_HALF_10BASE`、:c:enumerator:`LINK_FULL_10BASE`、:c:enumerator:`LINK_HALF_100BASE`、:c:enumerator:`LINK_FULL_100BASE`、:c:enumerator:`LINK_HALF_1000BASE`、:c:enumerator:`LINK_FULL_1000BASE`、:c:enumerator:`LINK_FULL_2500BASE` 和 :c:enumerator:`LINK_FULL_5000BASE`。``ETHERNET_LINK_10BASE_T``、``ETHERNET_LINK_100BASE_T``、``ETHERNET_LINK_1000BASE_T``、``ETHERNET_LINK_2500BASE_T`` 和 ``ETHERNET_LINK_5000BASE_T`` 则分别重命名为 :c:enumerator:`ETHERNET_LINK_10BASE`、:c:enumerator:`ETHERNET_LINK_100BASE`、:c:enumerator:`ETHERNET_LINK_1000BASE`、:c:enumerator:`ETHERNET_LINK_2500BASE` 和 :c:enumerator:`ETHERNET_LINK_5000BASE`，参见 :github:`87194`。

* ``ETHERNET_CONFIG_TYPE_LINK``、``ETHERNET_CONFIG_TYPE_DUPLEX``、``ETHERNET_CONFIG_TYPE_AUTO_NEG`` 以及相关的 ``NET_REQUEST_ETHERNET_SET_LINK``、``NET_REQUEST_ETHERNET_SET_DUPLEX``、``NET_REQUEST_ETHERNET_SET_AUTO_NEGOTIATION`` 已被移除。应改用 :c:func:`phy_configure_link` 和 :c:func:`net_eth_get_phy` 来配置链路（:github:`90652`）。

* :c:func:`phy_configure_link` 新增了一个 ``flags`` 参数。将其设置为 ``0`` 可保持旧行为（:github:`91354`）。

传感器
======

* ``ltr`` 厂商前缀已重命名为 ``liteon``，其中 :dtcompatible:`ltr,f216a` 的名称也已替换为 :dtcompatible:`liteon,ltrf216a`。选择项 :kconfig:option:`DT_HAS_LTR_F216A_ENABLED` 已替换为 :kconfig:option:`DT_HAS_LITEON_LTRF216A_ENABLED`，参见 :github:`85453`

* :dtcompatible:`ti,tmp116` 已重命名为 :dtcompatible:`ti,tmp11x`，因为它同时支持 tmp116、tmp117 和 tmp119。

* :dtcompatible:`meas,ms5837` 已被 :dtcompatible:`meas,ms5837-30ba` 和 :dtcompatible:`meas,ms5837-02ba` 取代。要使用这两个变体之一，还需要使用 status 属性。

* :dtcompatible:`we,wsen-itds` 驱动已重命名为 :dtcompatible:`we,wsen-itds-2533020201601`。设备树可以按如下方式配置：

  .. code-block:: devicetree

    &i2c0 {
      itds:itds-2533020201601@19 {
        compatible = "we,wsen-itds-2533020201601";
        reg = <0x19>;
        odr = "400";
        op-mode = "high-perf";
        power-mode = "normal";
        events-interrupt-gpios = <&gpio1 1 GPIO_ACTIVE_HIGH>;
        drdy-interrupt-gpios = <&gpio1 2 GPIO_ACTIVE_HIGH>;
      };
    };

* :dtcompatible:`raspberrypi,pico-temp.yaml` 的绑定文件已重命名，以使其名称与兼容字符串一致。

* 将文件 ``include/zephyr/drivers/sensor/npm1300_charger.h`` 移到 :zephyr_file:`include/zephyr/drivers/sensor/npm13xx_charger.h`，并将所有枚举中的 ``NPM1300`` 重命名为 ``NPM13XX``

* 将 ``CONFIG_NPM1300_CHARGER`` 重命名为 :kconfig:option:`CONFIG_NPM13XX_CHARGER`

其他
====

* 将文件 ``drivers/memc/memc_nxp_flexram.h`` 移到 :zephyr_file:`include/zephyr/drivers/misc/flexram/nxp_flexram.h`，以便可以通过 ``<zephyr/drivers/misc/flexram/nxp_flexram.h>`` 包含该文件。不再需要修改 CMakeList.txt 来使用并包含该驱动。
* 所有以 ``memc_flexram_*`` 命名空间命名的内容（包括 Kconfig 和 C API）都已改为 ``flexram_*``。

* 启用 Ethos-U NPU 驱动请选择 ``CONFIG_ETHOS_U``，而不再使用 ``CONFIG_ARM_ETHOS_U``。
* 将所有以 ``CONFIG_ARM_ETHOS_U_`` 为前缀的配置重命名为 ``CONFIG_ETHOS_U_``。

增强型串行外设接口（eSPI）
==========================

* 将设备树属性 ``io_girq`` 重命名为 ``io-girq``。
* 将设备树属性 ``vw_girqs`` 重命名为 ``vw-girqs``。
* 将设备树属性 ``pc_girq`` 重命名为 ``pc-girq``。
* 将设备树属性 ``poll_timeout`` 重命名为 ``poll-timeout``。
* 将设备树属性 ``poll_interval`` 重命名为 ``poll-interval``。
* 将设备树属性 ``consec_rd_timeout`` 重命名为 ``consec-rd-timeout``。
* 将设备树属性 ``sus_chk_delay`` 重命名为 ``sus-chk-delay``。
* 将设备树属性 ``sus_rsm_interval`` 重命名为 ``sus-rsm-interval``。

定时器
======

* ``native_posix_timer`` 已重命名为 ``native_sim_timer``，其 Kconfig 选项 :kconfig:option:`CONFIG_NATIVE_POSIX_TIMER` 也已弃用，取而代之的是 :kconfig:option:`CONFIG_NATIVE_SIM_TIMER`，参见 :github:`86612`。

* :dtcompatible:`andestech,machine-timer`、:dtcompatible:`neorv32-machine-timer`、:dtcompatible:`telink,machine-timer`、:dtcompatible:`lowrisc,machine-timer`、:dtcompatible:`niosv-machine-timer` 和 :dtcompatible:`scr,machine-timer` 已统一为 :dtcompatible:`riscv,machine-timer`。

  现在必须通过 ``reg`` 和 ``reg-names`` 属性显式指定 ``MTIME`` 和 ``MTIMECMP`` 两个寄存器的地址。``reg-names`` 属性现在是 **必需** 的，并且列出的名称必须与 ``reg`` 中的每一项一一对应。（:github:`84175` 和 :github:`89847`）

  示例：

  .. code-block:: devicetree

    mtimer: timer@d1000000 {
        compatible = "riscv,machine-timer";
        interrupts-extended = <&cpu0_intc 7>;
        reg = <0xd1000000 0x8
               0xd1000008 0x8>;
        reg-names = "mtime", "mtimecmp";
    };

* 现在可以使用 cpus DTS 组中的 ``timebase-frequency`` 属性来为 :kconfig:option:`CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC` 提供值，而无需直接写死数值：:github:`91296`

显示
====

* 在 STM32 器件上，LTDC 驱动（:dtcompatible:`st,stm32-ltdc`）的 RGB565 格式 ``PIXEL_FORMAT_RGB565`` 已被替换为 ``PIXEL_FORMAT_BGR565``，以与 Zephyr 期望的格式一致。此变更可确保显示和视频采集示例都能正常工作。

步进电机
========

* 将 ``stepper_enable(const struct device * dev, bool enable)`` 函数重构为 :c:func:`stepper_enable` 和 :c:func:`stepper_disable`。

熵源
====

* ``fake_entropy_native_posix`` 已重命名为 ``fake_entropy_native_sim``，其 Kconfig 选项和设备树绑定也一并重命名。:dtcompatible:`zephyr,native-posix-rng` 已弃用，取而代之的是 :dtcompatible:`zephyr,native-sim-rng`。:kconfig:option:`CONFIG_FAKE_ENTROPY_NATIVE_POSIX` 及其相关选项也已替换为 :kconfig:option:`CONFIG_FAKE_ENTROPY_NATIVE_SIM`，参见 :github:`86615`。

看门狗
======
* 将 ``CONFIG_WDT_NPM1300`` 重命名为 :kconfig:option:`CONFIG_WDT_NPM13XX`，将 ``CONFIG_WDT_NPM1300_INIT_PRIORITY`` 重命名为 :kconfig:option:`CONFIG_WDT_NPM13XX_INIT_PRIORITY`

稳压器
======

* 将文件 ``include/zephyr/dt-bindings/regulator/npm1300.h`` 移到 :zephyr_file:`include/zephyr/dt-bindings/regulator/npm13xx.h`，并将所有定义中的 ``NPM1300`` 重命名为 ``NPM13XX``
* 将 ``CONFIG_REGULATOR_NPM1300`` 重命名为 :kconfig:option:`CONFIG_REGULATOR_NPM13XX`，将 ``CONFIG_REGULATOR_NPM1300_COMMON_INIT_PRIORITY`` 重命名为 :kconfig:option:`REGULATOR_NPM13XX_COMMON_INIT_PRIORITY`，将 ``CONFIG_REGULATOR_NPM1300_INIT_PRIORITY`` 重命名为 :kconfig:option:`CONFIG_REGULATOR_NPM13XX_INIT_PRIORITY`
* :dtcompatible:`nordic,npm1300-regulator` 的 BUCK 和 LDO 节点 GPIO 属性现在指定为不带 GPIO 控制器的整数数组，因此不再需要存在并启用 :dtcompatible:`nordic,npm1300-gpio` 节点来对输出电源轨进行 GPIO 控制。例如，``enable-gpios = <&pmic_gpios 3 GPIO_ACTIVE_LOW>;`` 现在指定为 ``enable-gpio-config = <3 GPIO_ACTIVE_LOW>;``。

视频
====

* 8 位 RAW Bayer 格式 BGGR8 / GBRG8 / GRBG8 / RGGB8 已重命名，在前面加上 S 前缀：

  ``VIDEO_PIX_FMT_BGGR8`` 变为 :c:macro:`VIDEO_PIX_FMT_SBGGR8`，``VIDEO_PIX_FMT_GBRG8`` 变为 :c:macro:`VIDEO_PIX_FMT_SGBRG8`，``VIDEO_PIX_FMT_GRBG8`` 变为 :c:macro:`VIDEO_PIX_FMT_SGRBG8`，``VIDEO_PIX_FMT_RGGB8`` 变为 :c:macro:`VIDEO_PIX_FMT_SRGGB8`

* 在 STM32 器件上，DCMI 驱动（:dtcompatible:`st,stm32-dcmi`）现在依赖基于 endpoint 的 video-interfaces.yaml 绑定来提供传感器接口属性（例如总线宽度和同步信号）。此外，``capture-rate`` 属性已被帧间隔 API :c:func:`video_set_frmival` 取代。参见 :github:`89627`。

* :c:enum:`video_endpoint_id` 已被移除。它不再是任何视频 API 的参数。

* 新增了 :c:enum:`video_buf_type`。它是以下视频 API 的必需参数：:c:func:`set_stream`、:c:func:`video_stream_start`、:c:func:`video_stream_stop`

* ``video_format.pitch`` 已改为由驱动显式设置，而这项工作以前需要应用完成。此更新使应用能够针对不同驱动正确分配缓冲区大小。现有应用不会因此变更而失效，但可以像提交 ``33dcbe37cfd3593e8c6e9cfd218dd31fdd533598`` 中的示例那样进行简化。

* 使用 :zephyr:board:`native simulator <native_sim>` 的示例和项目现在需要指定 ``--snippet`` :ref:`video-sw-generator <snippet-video-sw-generator>` 才能正确构建。

* :c:func:`video_query_ctrl` 现在只接受一个 :c:struct:`video_ctrl_query` 类型的参数，其中包含 ``video_ctrl_query.dev`` 字段，用于指定并回读正在查询的设备（:github:`91265`）。

计数器
======

* ``counter_native_posix`` 已重命名为 ``counter_native_sim``，其 Kconfig 选项和设备树绑定也一并重命名。:dtcompatible:`zephyr,native-posix-counter` 已弃用，取而代之的是 :dtcompatible:`zephyr,native-sim-counter`，:kconfig:option:`CONFIG_COUNTER_NATIVE_POSIX` 及其相关选项也已替换为 :kconfig:option:`CONFIG_COUNTER_NATIVE_SIM`，参见 :github:`86616`。

设备树
======

* 原先位于 dts/common 中的许多厂商特定和架构特定文件已移到更具体的位置。因此，任何通过 ``#include <common/some_file.dtsi>`` 包含 zephyr 树中文件的 dts 文件，都需要改为 ``#include <some_file.dtsi>``。

* 用于 Series 2 的 Silicon Labs SoC 级 dts 文件已按器件超级系列重新组织到子目录中。因此，使用 Series 2 SoC 的开发板的 dts 文件需要将包含语句从 ``#include <silabs/some_soc.dtsi>`` 改为 ``#include <silabs/xg2[1-9]/some_soc.dtsi>``。

* :c:macro:`DT_ENUM_HAS_VALUE` 和 :c:macro:`DT_INST_ENUM_HAS_VALUE` 宏现在用于数组时会检查所有值，而不再只检查第一个值。

* 设备树和绑定中的属性名称使用连字符（``-``）作为分隔符，取代以前使用的所有下划线（``_``）。对于本地代码，你可以运行 ``scripts/utils/migrate_bindings_style.py`` 脚本，将绑定中的属性名称迁移为使用连字符。

调制解调器
==========

* 移除了 Kconfig 选项 :kconfig:option:`CONFIG_MODEM_CELLULAR_CMUX_MAX_FRAME_SIZE`，改用 :kconfig:option:`CONFIG_MODEM_CMUX_WORK_BUFFER_SIZE` 和 :kconfig:option:`CONFIG_MODEM_CMUX_MTU`。

音频
====

* :dtcompatible:`cirrus,cs43l22` 的绑定文件已重命名，以使其名称与兼容字符串一致。

.. zephyr-keep-sorted-stop

蓝牙
****

.. zephyr-keep-sorted-start re(^\w)

经典蓝牙
========

* HFP AG 回调 :c:struct:`bt_hfp_ag_cb` 的 ``sco_disconnected`` 参数已改为 SCO 连接对象 ``struct bt_conn *sco_conn`` 和 SCO 连接的断开原因 ``uint8_t reason``。

蓝牙 HCI
========

* 通过 HCI 驱动接口传递的缓冲区类型现在以 H:4 编码的前缀字节形式指示，作为缓冲区负载本身的一部分。bt_buf_set_type() 和 bt_buf_get_type() 函数已弃用，但仍然可用，只是每个缓冲区只能调用一次。

* :c:func:`bt_hci_cmd_create` 函数已弃用，应改用新的 :c:func:`bt_hci_cmd_alloc` 函数。新函数不接受任何参数，因为命令发送函数已更新为负责命令头编码。

蓝牙主机
========

* :zephyr_file:`include/zephyr/bluetooth/conn.h` 中的符号 ``BT_LE_CS_TONE_ANTENNA_CONFIGURATION_INDEX_<NUMBER>`` 已重命名为 ``BT_LE_CS_TONE_ANTENNA_CONFIGURATION_A<NUMBER>_B<NUMBER>``。

* ISO 数据路径不再自动建立，应用应分别调用 :c:func:`bt_iso_setup_data_path` 和 :c:func:`bt_iso_remove_data_path` 显式建立和移除它们。（:github:`75549`）

* ``BT_ISO_CHAN_TYPE_CONNECTED`` 已拆分为 ``BT_ISO_CHAN_TYPE_CENTRAL`` 和 ``BT_ISO_CHAN_TYPE_PERIPHERAL``，以更好地描述 ISO 通道类型，因为每种角色的行为可能不同。现有对 ``BT_ISO_CHAN_TYPE_CONNECTED`` 的使用/检查可以用二者的 ``||`` 替代。（:github:`75549`）

* :zephyr_file:`include/zephyr/bluetooth/gatt.h` 中的 ``struct _bt_gatt_ccc`` 已重命名为结构体 :c:struct:`bt_gatt_ccc_managed_user_data`。（:github:`88652`）

* :zephyr_file:`include/zephyr/bluetooth/gatt.h` 中的宏 ``BT_GATT_CCC_INITIALIZER`` 已重命名为 :c:macro:`BT_GATT_CCC_MANAGED_USER_DATA_INIT`。（:github:`88652`）

* ``CONFIG_BT_ISO_TX_FRAG_COUNT`` Kconfig 选项已被移除，因为它完全未被使用。任何对该选项的使用都可以直接删除。（:github:`89836`）

蓝牙音频
========

* ``CONFIG_BT_CSIP_SET_MEMBER_NOTIFIABLE`` 已重命名为 :kconfig:option:`CONFIG_BT_CSIP_SET_MEMBER_SIRK_NOTIFIABLE`。（:github:`86763`）

* ``bt_csip_set_member_get_sirk`` 已被移除。请使用 :c:func:`bt_csip_set_member_get_info` 获取 SIRK（以及其他信息）。（:github:`86996`）

* ``BT_AUDIO_CONTEXT_TYPE_PROHIBITED`` 已重命名为 :c:enumerator:`BT_AUDIO_CONTEXT_TYPE_NONE`。（:github:`89506`）

.. zephyr-keep-sorted-stop

网络
****

* 结构体 ``net_linkaddr_storage`` 已重命名为结构体 :c:struct:`net_linkaddr`，旧的结构体 ``net_linkaddr`` 已被移除。结构体 :c:struct:`net_linkaddr` 现在包含用于存储链路地址的空间，而不再使用指向链路地址的指针。这避免了克隆 :c:struct:`net_pkt` 结构体时可能出现悬空指针。对于 IEEE 802.15.4，这会使 :c:struct:`net_pkt` 结构体增大 4 个八位字节，但对于以太网等其他网络技术则不会增大。请注意，任何直接使用 :c:struct:`net_linkaddr` 结构体并且具有类似 ``if (lladdr->addr == NULL)`` 检查的代码，将不再按预期工作（因为 addr 不是指针）；如果代码想要检查链路地址未设置，则必须改为 ``if (lladdr->len == 0)``。

* TLS 凭据类型 ``TLS_CREDENTIAL_SERVER_CERTIFICATE`` 已重命名为更通用的 :c:enumerator:`TLS_CREDENTIAL_PUBLIC_CERTIFICATE`，以更好地反映该凭据类型的用途。

* MQTT 公共 API 函数 :c:func:`mqtt_disconnect` 已更改。该函数现在接受额外的 ``param`` 参数以支持 MQTT 5.0 场景。该参数是可选的，在较旧的 MQTT 版本中不使用——MQTT 3.1.1 用户应传入 NULL 作为该参数。

* 不再支持 ``AF_PACKET/SOCK_RAW/IPPROTO_RAW`` 套接字组合，因为 ``AF_PACKET`` 套接字只应接受 IEEE 802.3 协议编号。作为替代，可以根据实际用例使用 ``AF_PACKET/SOCK_DGRAM/ETH_P_ALL`` 或 ``AF_INET(6)/SOCK_RAW/IPPROTO_IP`` 套接字。

* HTTP 服务器现在会遵循所配置的 ``_concurrent`` 和 ``_backlog`` 值。请检查你为 :c:macro:`HTTP_SERVICE_DEFINE_EMPTY`、:c:macro:`HTTPS_SERVICE_DEFINE_EMPTY`、:c:macro:`HTTP_SERVICE_DEFINE` 和 :c:macro:`HTTPS_SERVICE_DEFINE` 提供了适用的值。

* :kconfig:option:`CONFIG_NET_ZPERF` 不再默认包含服务器支持。要使用服务器命令，请启用 :kconfig:option:`CONFIG_NET_ZPERF_SERVER`。如果不需要服务器支持，可以适当减小 :kconfig:option:`CONFIG_ZVFS_POLL_MAX`。

* L2 Wi-Fi shell 现在支持大多数命令的接口选项，为适应此变更，一些现有选项已被重命名。下表总结了这些变更：

  +-------------------------------------------------------+-----------------------+----------------------+
  | 命令                                                  | 旧选项                | 新选项               |
  +-------------------------------------------------------+-----------------------+----------------------+
  | ``wifi connect`` ``wifi ap enable``                   | ``-i``                | ``-g``               |
  +-------------------------------------------------------+-----------------------+----------------------+
  | ``wifi twt setup``                                    | ``-i``                | ``-p``               |
  +-------------------------------------------------------+-----------------------+----------------------+
  | ``wifi ap config``                                    | ``-i``                | ``-t``               |
  +-------------------------------------------------------+-----------------------+----------------------+
  | ``wifi mode`` ``wifi channel`` ``wifi packet_filter`` | ``--if-index``        | ``--iface``          |
  +-------------------------------------------------------+-----------------------+----------------------+

* :c:type:`http_response_cb_t` HTTP 客户端响应回调的签名已更改。回调函数现在返回 ``int`` 而不是 ``void``。这使应用可以中止 HTTP 连接。现有应用需要更新其响应回调实现。要保持当前行为，只需从回调中返回 0。

* ``net_mgmt`` 事件处理函数 :c:type:`net_mgmt_event_handler_t` 和请求处理函数 :c:type:`net_mgmt_request_handler_t` 的 API 签名已更改。管理事件类型从 ``uint32_t`` 改为 ``uint64_t``。此变更允许事件编号值为位掩码，而不再局限于枚举值。层代码仍然保持为枚举值。如有需要，可以在请求或事件处理函数中使用 :c:macro:`NET_MGMT_LAYER_CODE` 和 :c:macro:`NET_MGMT_GET_COMMAND` 从实际事件值中获取层代码和管理事件命令。

* ``net_mgmt`` 类型套接字的套接字选项不能直接使用网络管理事件类型，因为这些类型现在是 ``uint64_t``，而套接字选项期望普通的 32 位整数值。因此，新引入了 ``SO_NET_MGMT_ETHERNET_SET_QAV_PARAM`` 和 ``SO_NET_MGMT_ETHERNET_GET_QAV_PARAM`` 套接字选项，用来取代以前使用的 ``NET_REQUEST_ETHERNET_SET_QAV_PARAM`` 和 ``NET_REQUEST_ETHERNET_GET_QAV_PARAM`` 选项。

* DNS 服务器解析器配置函数 :c:func:`dns_resolve_reconfigure` 和 :c:func:`dns_resolve_reconfigure_with_interfaces` 现在要求用户提供 DNS 服务器信息的来源。例如，当通过 DHCPv4 收到 DNS 服务器信息时，需要指定 :c:enumerator:`DNS_SOURCE_DHCPV4`。

.. zephyr-keep-sorted-start re(^\w)

LwM2M
=====

* 加速度计对象：可选资源 Y 值、Z 值、最小量程值、最大量程值现在可以按照加速度计对象规范选择性地使用。这些资源的使用者现在需要提供读取缓冲区。

OpenThread
==========

* Zephyr 中的 OpenThread 协议栈集成经历了重大重构。其实现已从 Zephyr 网络层（``subsys/net/l2/openthread/``）移至专用模块（``modules/openthread/``）。

* OpenThread 现在是 Zephyr 中的一个独立模块。它可以在不依赖 Zephyr 网络协议栈（L2 和 IEEE802.15.4 shim 层）的情况下单独使用。这带来了新的用例，例如应用直接配合自己的 IEEE802.15.4 驱动使用 OpenThread，或者不需要完整的 Zephyr 网络协议栈。

* :zephyr_file:`include/zephyr/net/openthread.h` 文件中的大多数函数已弃用。这些弃用的 API 仍可用于向后兼容，但新应用应使用 OpenThread 模块提供的新 API。以下列表总结了这些变更：

  * 互斥锁处理：

    * 以前：

      * ``openthread_api_mutex_lock``
      * ``openthread_api_mutex_try_lock``
      * ``openthread_api_mutex_unlock``

    * 现在使用：

      * :c:func:`openthread_mutex_lock`
      * :c:func:`openthread_mutex_try_lock`
      * :c:func:`openthread_mutex_unlock`

  * OpenThread 启动：

    * 以前：``openthread_start``
    * 现在使用：:c:func:`openthread_run`

  * 回调注册：

    * 以前：

      * ``openthread_state_changed_cb_register``
      * ``openthread_state_changed_cb_unregister``

    * 现在使用：

      * :c:func:`openthread_state_changed_callback_register`
      * :c:func:`openthread_state_changed_callback_unregister`

  * 回调结构体：

    * 以前：``openthread_state_changed_cb``
    * 现在使用：:c:struct:`openthread_state_changed_callback`

  * 以下 :c:struct:`openthread_context` 结构体字段已弃用，不应再在新代码中使用：

    * ``instance``
    * ``api_lock``
    * ``work_q``
    * ``api_work``
    * ``state_change_cbs``

  * 以下是以前不存在的新函数：

    * :c:func:`openthread_init` 用于初始化 OpenThread 协议栈。
    * :c:func:`openthread_stop` 用于停止并禁用 OpenThread 协议栈。
    * :c:func:`openthread_set_receive_cb` 用于为 OpenThread 协议栈设置接收回调。

* ``subsys/net/l2/openthread/Kconfig`` 中与 OpenThread 相关的 Kconfig 选项已移到 :zephyr_file:`modules/openthread/Kconfig`。所有 Kconfig 选项保持不变。你仍可以像以前一样使用它们，但要修改这些选项，需要在 menuconfig 或 guiconfig 中使用新路径。

* 如果启用了 :kconfig:option:`CONFIG_NET_L2_OPENTHREAD` Kconfig 选项，Zephyr 的 L2 层将使用新的 OpenThread 模块 API 作为其后端。L2 层不再自行实现 OpenThread，而是把实现委托给该模块。

* 对于通过 Zephyr 网络协议栈使用 OpenThread 的现有应用：

  * 你的应用应能继续工作，因为旧 API 仍可用于兼容。不过，建议你迁移到新 API，以便适应未来变化并使用新的模块化结构。
  * 将你在配置工具中对 OpenThread Kconfig 选项的引用更新为新路径（``modules/openthread/Kconfig``）。

* 对于使用 :c:struct:`openthread_context` 或其他已弃用 API 的应用：

  * 开始迁移到新 API。已弃用的 API 将在未来版本中移除。
  * 避免直接使用 :c:struct:`openthread_context` 及相关字段；请改用新的初始化和回调注册函数。

* 对于新应用或在不使用 Zephyr L2 的情况下使用 OpenThread 的应用：

  * 使用新的初始化（:c:func:`openthread_init`）、运行（:c:func:`openthread_run`）和回调注册 API（:c:func:`openthread_state_change_callback_register`）。
  * 如果你的用例允许，现在可以直接使用 OpenThread，而无需启用 Zephyr 的 L2 或 IEEE802.15.4 层。

.. zephyr-keep-sorted-stop


其他子系统
**********

.. zephyr-keep-sorted-start re(^\w)

Modbus
======

* :c:struct:`modbus_serial_param` 中的 ``client_stop_bits`` 字段已重命名为 ``stop_bits``。该设置在客户端和服务器模式下都有效。
* 自定义停止位设置默认禁用，应通过 :kconfig:option:`CONFIG_MODBUS_NONCOMPLIANT_SERIAL_MODE` 启用。

hawkBit
=======

* 当启用 :kconfig:option:`CONFIG_HAWKBIT_CUSTOM_DEVICE_ID` 时，device_id 将不再前置 :kconfig:option:`CONFIG_BOARD`。如需前置开发板名称，需要用户自行编写回调。

状态机框架
==========

* :c:func:`smf_set_handled` 已被移除。
* 状态运行动作现在返回 :c:enum:`smf_state_result` 值而不是 void，返回码决定了事件是传播到父运行动作还是已被处理。完全处理事件的运行动作应返回 :c:enum:`SMF_EVENT_HANDLED`，而将处理传播到父状态的运行动作应返回 :c:enum:`SMF_EVENT_PROPAGATE`。
* 扁平状态机忽略返回值；返回 :c:enum:`SMF_EVENT_HANDLED` 是技术上最准确的响应。

.. zephyr-keep-sorted-stop

模块
****

.. zephyr-keep-sorted-start re(^\w)

CMSIS
=====

* Cortex-M 开发板/SoC 现在需要 ``CMSIS_6`` 模块才能正确构建（取代之前作为 CMSIS 5.9.0 的 ``cmsis``）。如果尝试构建 Cortex-M 开发板，请先执行 ``west update``，确保 ``CMSIS_6`` 模块可用，然后再运行 ``west build`` 或其他命令。

  使用旧 ``cmsis`` 模块（无论是本地副本还是通过 :kconfig:option:`CONFIG_ZEPHYR_CMSIS_MODULE_DIR`）的开发板、SoC 或模块，请改用可通过 :kconfig:option:`CONFIG_ZEPHYR_CMSIS_6_MODULE_DIR` 配置访问的 ``CMSIS_6`` 模块。

  注意：对于 Cortex-A 和 Cortex-R 目标，Zephyr 将继续使用旧的 ``cmsis`` 模块。

.. zephyr-keep-sorted-stop

架构
****

* 将 :kconfig:option:`CONFIG_SRAM_VECTOR_TABLE` 从 ``zephyr/Kconfig.zephyr`` 移到 ``zephyr/arch/Kconfig``，并添加对 :kconfig:option:`CONFIG_XIP`、:kconfig:option:`CONFIG_ARCH_HAS_VECTOR_TABLE_RELOCATION` 和 :kconfig:option:`CONFIG_ROMSTART_RELOCATION_ROM` 的依赖，以支持向量表重定位到 RAM。
* 将 :kconfig:option:`CONFIG_DEBUG_INFO` 重命名为 :kconfig:option:`CONFIG_X86_DEBUG_INFO`，以更好地反映其用途。该选项现在仅适用于 x86 架构。
