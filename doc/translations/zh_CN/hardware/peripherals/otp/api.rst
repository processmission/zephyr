.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _otp_api:

OTP API
#######

概述
****

OTP API 提供对 :abbr:`OTP(One Time Programmable)` 存储设备进行编程和读取的方法

API 实现参考
************
.. doxygengroup:: otp_interface

配置选项
********

OTP 相关配置选项：

* :kconfig:option:`CONFIG_OTP`
* :kconfig:option:`CONFIG_OTP_PROGRAM`
* :kconfig:option:`CONFIG_OTP_INIT_PRIORITY`
* :kconfig:option-regex:`CONFIG_OTP_SHELL.*`
