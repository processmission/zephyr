.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _emulators:

Zephyr 的设备仿真器/模拟器
##########################

概述
====

Zephyr 代码库包含一组设备仿真器/模拟器。这些软件组件与嵌入式软件一起构建，并在系统的其余部分看来表现为某一类别的设备。

这些设备仿真器/模拟器可以为任何具有足够 RAM 和闪存的目标构建，不过其中一些可能具有仅在特定目标上可用的附加功能。

.. note::

   | Zephyr 还包含并使用许多其他类型的模拟器/仿真器，包括 CPU 和平台模拟器、无线电模拟器，以及多个允许在开发主机上运行嵌入式代码的构建目标。
   | Zephyr 的一些通信控制器/驱动还包含回环模式或回环设备。
   | 本页不涉及上述内容。

.. note::
   本页不涉及特定平台专用的驱动，例如通过连接主机 API 来仿真某一类外设的 :ref:`native_sim 专用驱动 <native_sim_peripherals>` 。


可用的仿真器
============

**ADC 仿真器**
  * 一种模拟实际 ADC 的虚拟驱动，可用于测试 ADC 设备的高层 API。
  * 主要 Kconfig 选项： :kconfig:option:`CONFIG_ADC_EMUL`
  * Devicetree 绑定： :dtcompatible:`zephyr,adc-emul`

**DMA 仿真器**
  * 仿真的 DMA 控制器
  * 主要 Kconfig 选项： :kconfig:option:`CONFIG_DMA_EMUL`
  * Devicetree 绑定： :dtcompatible:`zephyr,dma-emul`

**EEPROM 仿真器**
  * 在闪存分区上仿真 EEPROM
  * 主要 Kconfig 选项： :kconfig:option:`CONFIG_EEPROM_EMULATOR`
  * Devicetree 绑定： :dtcompatible:`zephyr,emu-eeprom`

.. _emul_eeprom_simu_brief:

**EEPROM 模拟器**
  * 在 RAM 中仿真 EEPROM
  * 主要 Kconfig 选项： :kconfig:option:`CONFIG_EEPROM_SIMULATOR`
  * Devicetree 绑定： :dtcompatible:`zephyr,sim-eeprom`
  * 注意：对于 :zephyr:board:`原生目标 <native_sim>` ，还可以将内容保存为主机文件系统中的文件。

**外部总线及总线连接外设的仿真器**
  * :ref:`Documentation <bus_emul>`
  * 支持仿真 I2C 或 SPI 等外部总线及连接到这些总线的外设。

.. _emul_flash_simu_brief:

**闪存模拟器**
  * 在 RAM 中仿真闪存
  * 主要 Kconfig 选项： :kconfig:option:`CONFIG_FLASH_SIMULATOR`
  * DT 绑定： :dtcompatible:`zephyr,sim-flash`
  * 注意：对于原生目标，也可以将内容保存为主机文件系统中的文件。请参阅 :ref:`native_sim 闪存模拟器章节 <nsim_per_flash_simu>` 。

**GPIO 仿真器**
  * 可由软件驱动的仿真 GPIO 控制器
  * 主要 Kconfig 选项： :kconfig:option:`CONFIG_GPIO_EMUL`
  * DT 绑定： :dtcompatible:`zephyr,gpio-emul`

**I2C 仿真器**
  * 仿真 I2C 总线。请参阅 :ref:`总线仿真器 <bus_emul>` 。
  * 主要 Kconfig 选项： :kconfig:option:`CONFIG_I2C_EMUL`
  * DT 绑定： :dtcompatible:`zephyr,i2c-emul-controller`

**RTC 仿真器**
  * 仿真 RTC 外设。请参阅 :ref:`RTC 仿真设备章节 <rtc_api_emul_dev>`
  * 主要 Kconfig 选项： :kconfig:option:`CONFIG_RTC_EMUL`
  * DT 绑定： :dtcompatible:`zephyr,rtc-emul`

**SPI 仿真器**
  * 仿真 SPI 总线。请参阅 :ref:`总线仿真器 <bus_emul>` 。
  * 主要 Kconfig 选项： :kconfig:option:`CONFIG_SPI_EMUL`
  * DT 绑定： :dtcompatible:`zephyr,spi-emul-controller`

**MSPI 仿真器**
  * 仿真 MSPI 总线。请参阅 :ref:`总线仿真器 <bus_emul>` 。
  * 主要 Kconfig 选项： :kconfig:option:`CONFIG_MSPI_EMUL`
  * DT 绑定： :dtcompatible:`zephyr,mspi-emul-controller`

**UART 仿真器**
  * 仿真 UART 总线。请参阅 :ref:`总线仿真器 <bus_emul>` 。
  * 主要 Kconfig 选项： :kconfig:option:`CONFIG_UART_EMUL`
  * DT 绑定： :dtcompatible:`zephyr,uart-emul`
