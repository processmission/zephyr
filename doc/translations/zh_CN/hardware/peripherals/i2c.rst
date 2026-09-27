.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _i2c_api:

集成电路间（I2C）总线
#####################

概述
****

.. note::

   Zephyr I2C API 使用的术语遵循 `NXP I2C Bus Specification Rev 7.0 <i2c-specification_>`_。该版本于 2021 年 10 月 1 日发布，其术语相较于先前版本有所变更。

`I2C`_ （Inter-Integrated Circuit，读作“eye squared see”）是一种常用的双信号线共享外设接口总线。许多片上系统（SoC）解决方案提供可通过 I2C 总线通信的控制器。总线上的设备可以承担两种角色：作为“控制器”发起事务并控制时钟，或作为“目标设备”响应事务命令。SoC 上的 I2C 控制器通常支持控制器角色，其中一些还支持目标设备模式。Zephyr 为这两种角色都提供了 API。

.. _i2c-controller-api:

I2C 控制器 API
==============

当 I2C 外设控制总线，特别是控制起始条件、停止条件和时钟时，使用 Zephyr 的 I2C 控制器 API。这是最常见的模式，用于与传感器、串行存储器等 I2C 设备交互。

源码树中的所有 I2C 外设驱动都支持此 API，该 API 被认为是稳定的。

.. _i2c-target-api:

I2C 目标设备 API
================

当 I2C 外设响应总线上另一个控制器发起的事务时，使用 Zephyr 的 I2C 目标设备 API。此 API 可用于充当换能器、由主机处理器等其他设备控制的 Zephyr 应用。

源码树中只有极少数 I2C 外设驱动支持此 API。该 API 被认为是实验性的，因为它无法兼容所有支持控制器模式的 I2C 外设的能力。


配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_I2C`
* :kconfig:option:`CONFIG_I2C_TRANSFER_TIMEOUT_MS`

传输超时
========

I2C 子系统提供了两种互补的机制，用于控制驱动在返回 ``-ETIMEDOUT`` 前等待传输完成的时长。

应用全局默认值（Kconfig）
-------------------------

:kconfig:option:`CONFIG_I2C_TRANSFER_TIMEOUT_MS` 为所有通过驱动选择 ``I2C_TRANSFER_TIMEOUT_SUPPORTED`` 来启用此功能的 I2C 控制器设置默认超时时间，单位为毫秒。值为 ``0`` 表示无限等待（ ``K_FOREVER`` ）。不允许无限等待的驱动（例如将该值直接写入硬件寄存器的驱动）使用 :c:macro:`BUILD_ASSERT_INVALID_I2C_TRANSFER_TIMEOUT` 在构建时强制要求该值非零。

通过 DT 为单个控制器覆盖默认值
------------------------------

各个控制器可以通过 ``dts/bindings/i2c/i2c-controller.yaml`` 中定义的 ``zephyr,transfer-timeout-ms`` Devicetree 属性覆盖应用全局默认值。如果未设置该属性，驱动将回退到 :kconfig:option:`CONFIG_I2C_TRANSFER_TIMEOUT_MS`。

开发板 overlay 示例::

    &i2c1 {
        /* Fast sensor bus - fail quickly on a hung device */
        zephyr,transfer-timeout-ms = <50>;
    };

    &i2c2 {
        /* EEPROM bus - allow for long internal write cycles */
        zephyr,transfer-timeout-ms = <2000>;
    };

支持按实例设置超时的驱动使用 :c:macro:`I2C_DT_INST_TRANSFER_TIMEOUT` （需要直接使用整数值时则使用 :c:macro:`I2C_DT_INST_TRANSFER_TIMEOUT_MS` ），这些宏按以下优先级确定超时时间：

1. 控制器节点上的 ``zephyr,transfer-timeout-ms`` DT 属性
2. :kconfig:option:`CONFIG_I2C_TRANSFER_TIMEOUT_MS`
3. 当解析得到的值为 ``0`` 时，使用 ``K_FOREVER``

API 参考
********

.. doxygengroup:: i2c_interface

.. _i2c-specification:
   https://www.nxp.com/docs/en/user-guide/UM10204.pdf

.. _I2C: i2c-specification_
