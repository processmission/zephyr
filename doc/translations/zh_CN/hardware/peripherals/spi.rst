.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _spi_api:

串行外设接口（SPI）总线
#######################

概述
****

术语
====

Zephyr SPI API 使用 :ref:`coding_guideline_inclusive_language` 中选定的包容性术语，遵循 `OSHWA resolution to redefine SPI signal names`_ ：

* 驱动时钟的设备是 *控制器* ，它寻址的设备是 *外设* （参见 :c:macro:`SPI_OP_MODE_CONTROLLER` 和 :c:macro:`SPI_OP_MODE_PERIPHERAL` ）。
* 数据信号从各设备自身的角度命名：*SDO* （串行数据输出）和 *SDI* （串行数据输入），选择信号线则使用 *CS* （片选）。

原有的 master/slave 和 MOSI/MISO 名称仍作为兼容性别名保留。这些名称自 Zephyr v4.5 起已弃用，并将在 Zephyr v5.0 中移除。

.. _OSHWA resolution to redefine SPI signal names:
   https://oshwa.org/resources/a-resolution-to-redefine-spi-signal-names/

API 参考
********

.. doxygengroup:: spi_interface
