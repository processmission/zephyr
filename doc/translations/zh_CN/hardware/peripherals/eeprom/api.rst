.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _eeprom_api:

EEPROM API
##########

概述
****

EEPROM API 提供对电可擦除可编程只读存储器（EEPROM）设备的读写访问。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_EEPROM`

API 参考
********

.. doxygengroup:: eeprom_interface

.. doxygengroup:: eeprom_fake
