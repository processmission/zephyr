.. SPDX-FileCopyrightText: Copyright The Process Mission
.. SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
.. SPDX-License-Identifier: Apache-2.0

.. zephyr:code-sample:: code_relocation_nocopy
   :name: 无需复制的代码重定位

   使用自定义链接脚本重定位代码段、数据段或 BSS 段。

概述
****
此示例演示如何使用自定义链接脚本重定位代码段、数据段或 BSS 段。

与代码重定位示例不同，本示例将 ext_code.c 的内容放入另一个 Flash 区域，
并直接在该区域就地执行（XIP），无需在运行时复制或重定位代码。
其他代码（例如 main() 和 Zephyr 内核）仍放在内部 Flash 中。

nRF5340 DK 平台说明
*******************

nRF5340 DK 配备了支持 Quad SPI 的 64 Mb 外部 Flash，映射地址为 0x10000000。

使用以下命令构建并烧录应用，包括位于外部存储器中的部分：

.. zephyr-app-commands::
   :zephyr-app: samples/application_development/code_relocation_nocopy
   :board: nrf5340dk/nrf5340/cpuapp
   :goals: build flash
   :compact:

STM32F769I-Discovery 平台说明
*****************************

stm32f769i_disco 通过 QSPI 连接了 64MB 外部 Flash，映射地址为 0x90000000。

.. zephyr-app-commands::
   :zephyr-app: samples/application_development/code_relocation_nocopy
   :board: stm32f769i_disco
   :goals: build flash
   :compact:

STM32 b_u585i_iot02a Discovery 套件说明
***************************************

b_u585i_iot02a 通过 OSPI 连接了 64MB 外部 Flash，映射地址为 0x70000000。

.. zephyr-app-commands::
   :zephyr-app: samples/application_development/code_relocation_nocopy
   :board: b_u585i_iot02a
   :goals: build flash
   :compact:

运行输出
********

.. code-block:: console

  *** Booting Zephyr OS build v3.0.0-rc3-25-g0df32cec1ff2  ***
  Address of main function 0x4f9
  Address of function_in_ext_flash 0x10000001
  Address of var_ext_sram_data 0x200000a0 (10)
  Address of function_in_sram 0x20000001
  Address of var_sram_data 0x200000a4 (10)
  Hello World! nrf5340dk/nrf5340/cpuapp
