.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _smbus_api:

系统管理总线（SMBus）
#####################

.. contents::
    :local:
    :depth: 2

概述
****

系统管理总线（SMBus）源自 I2C，用于与主板上的设备通信。系统可以使用 SMBus 与主板上的外设通信，无需使用专用控制线。SMBus 外设可以提供各种制造商信息、报告错误、接受控制参数等。

总线上的设备可以承担三种角色：控制器，负责发起事务并控制时钟；外设，负责响应事务命令；主机，一种专用控制器，负责提供与系统 CPU 交互的主要接口。Zephyr 为控制器角色提供了 API。

SMBus 外设可以通过两种方式主动与控制器通信：

* **主机通知协议** ：支持主机通知协议的外设以控制器角色执行通知。它向特殊地址“SMBus Host (0x08)”写入一条三字节消息，其中包含自身地址和两个字节的相关数据。
* **SMBALERT# 信号** ：外设使用特殊信号 SMBALERT# 请求控制器关注。控制器需要从特殊地址“SMBus 警报响应地址（ARA）（0x0c）”读取一个字节。外设以一个包含自身地址的数据字节进行响应。

目前，该 API 基于 `SMBus Specification`_ 2.0 版。

.. note::
   有关此 API 所用术语的信息，请参阅 :ref:`coding_guideline_inclusive_language` 。

.. _smbus-controller-api:

SMBus 控制器 API
****************

当 SMBus 设备控制总线，尤其是控制起始条件、停止条件和时钟时，使用 Zephyr 的 SMBus 控制器 API。这是与 SMBus 外设交互时最常用的模式。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_SMBUS`

API 参考
********

.. doxygengroup:: smbus_interface

.. _SMBus Specification: https://smbus.org/specs/smbus20.pdf
