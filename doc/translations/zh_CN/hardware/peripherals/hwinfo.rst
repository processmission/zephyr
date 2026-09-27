.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _hwinfo_api:

硬件信息
########

概述
****

HW Info API 提供对设备标识符和复位原因标志等硬件信息的访问。

复位原因标志可用于确定设备复位的原因，例如看门狗超时或断电后重新上电。不同设备支持的标志子集不同。使用 :c:func:`hwinfo_get_supported_reset_cause` 获取该设备支持的标志。

大多数实现都针对特定 SoC，从厂商寄存器或内存中读取标识符。通用的 :dtcompatible:`zephyr,hwinfo-nvmem` 后端从 NVMEM 单元获取设备 ID，也可选择获取 EUI-64（参见 :ref:`nvmem` ）。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_HWINFO`
* :kconfig:option:`CONFIG_HWINFO_NVMEM`

API 参考
********

.. doxygengroup:: hwinfo_interface
