.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _flash_api:

Flash
#####

概述
****

**烧录偏移量概念**

用户 API 使用的偏移量以烧录存储器的起始地址为基准。对于所有可通过页面布局查询 API 获取布局的烧录控制器常规存储区域，均应遵循此规则（参见 :kconfig:option:`CONFIG_FLASH_PAGE_LAYOUT` ）。

供应商专用的烧录存储器特殊用途区域可不受此规则约束（此类区域显然无法由页面布局查询 API 涵盖）。



用户 API 参考
*************
.. doxygengroup:: flash_interface

实现接口 API 参考
*****************
.. doxygengroup:: flash_internal_interface
