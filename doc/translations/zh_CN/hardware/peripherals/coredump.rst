.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _coredump_device_api:

核心转储设备
############

概述
****

核心转储设备是一种伪设备驱动，支持两种类型。COREDUMP_TYPE_MEMCPY 类型通过 Devicetree 绑定指定要包含在每次转储中的内存地址和大小值。该驱动还提供 API，用于在运行时添加或移除转储内存区域。COREDUMP_TYPE_CALLBACK 设备要求 memory-regions 数组恰好包含一个条目，其大小为 0，并指定所需大小。驱动将静态分配所需大小的内存，并提供 API 来注册回调函数，以便在发生转储时填充该内存。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_COREDUMP_DEVICE`

API 参考
********

.. doxygengroup:: coredump_device_interface
