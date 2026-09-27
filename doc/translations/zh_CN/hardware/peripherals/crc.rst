.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _crc_api:

循环冗余校验（CRC）
###################

概述
****

循环冗余校验（CRC）API 提供了用于配置硬件 CRC 并通过硬件计算 CRC 值的函数。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_CRC_DRIVER`
* :kconfig:option:`CONFIG_CRC_DRIVER_INIT_PRIORITY`

API 参考
********

.. doxygengroup:: crc_interface
