.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _fuel_gauge_api:

电量计
######

电量计子系统提供了一个 API，用于以统一方式访问电池电量计设备。

基本操作
********

属性
====

从根本上说，属性是电量计设备能够测量的量。

电量计通常支持多种属性，例如电池组的温度读数或实时电流、电压。

客户端使用 :c:func:`fuel_gauge_get_prop` 逐个获取属性，或使用 :c:func:`fuel_gauge_get_props` 批量获取属性。缓冲区属性（例如设备名称）使用 :c:func:`fuel_gauge_get_buffer_prop` 获取。

客户端使用 :c:func:`fuel_gauge_set_prop` 逐个设置属性，或使用 :c:func:`fuel_gauge_set_props` 批量设置属性。缓冲区属性（例如电池配置映像）使用 :c:func:`fuel_gauge_set_buffer_prop` 设置。


电池断电
========

许多嵌入电池组的电量计会提供一个寄存器地址，向该地址写入特定数据即可切断电池供电。这种电池断电功能通常称为运输模式、存储模式或睡眠模式，因为它有助于减少设备在存储或运输期间的电池电量消耗。

电量计 API 通过 :c:func:`fuel_gauge_battery_cutoff` 函数提供电池断电功能。

缓存
====

电量计 API 明确不为其客户端提供任何缓存。


.. _fuel_gauge_api_reference:

API 参考
********

.. doxygengroup:: fuel_gauge_interface
.. doxygengroup:: fuel_gauge_emulator_backend
