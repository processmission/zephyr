.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _usbc_vbus_api:

USB-C VBUS
##########

概述
****

USB-C VBUS 是 USB Type-C 连接中从供电端向受电端设备输送电力的线路。

.. _usbc-vbus-api:

USB-C VBUS API
==============

USB-C VBUS 设备驱动程序提供了用于控制和测量 VBUS 的 API。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_USBC_VBUS_DRIVER`

API 参考
********

.. doxygengroup:: usbc_vbus_api
