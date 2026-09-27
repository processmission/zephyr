.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _charger_api:

充电器
######

充电器子系统提供了用于统一访问电池充电器设备的 API。

充电器设备（或充电器外设）以供给系统的外部电源作为输入，并向下游的一个或多个电池组以及系统输出电力。充电器设备可以是模块、集成电路，也可以是电源管理集成电路（PMIC）中的功能块。

为电池组充电的过程称为充电周期。执行充电周期时，电池组按照充电器设备上配置的充电曲线进行充电。充电曲线由制造商提供的电池组规格书定义。对于具有控制端口的充电器设备，主控制器可以通过设置相关属性来配置充电曲线，并可在运行时调整充电曲线以应对环境变化。

基本操作
********

启动充电周期
============

使用 :c:func:`charger_charge_enable` 启动或终止充电周期。

属性
====

从本质上讲，属性是可配置的设置、状态，或充电器设备能够测量的量。

充电器通常支持多种属性，例如电池组的温度读数或当前的电流、电压。

客户端使用 :c:func:`charger_get_prop` 逐一获取属性，使用 :c:func:`charger_set_prop` 逐一设置属性。

.. _charger_api_reference:

API 参考
********

.. doxygengroup:: charger_interface
