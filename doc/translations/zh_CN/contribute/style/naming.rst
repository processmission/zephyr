.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _naming_conventions:

命名约定
########

本节介绍 Zephyr 项目针对其中使用的每种编程语言或工具所采用的命名约定。

C 代码命名约定
**************

如各小节所述，本节的命名约定适用于 C 源文件和头文件。

公共符号前缀
============

引入 Zephyr 的所有 :term:`公共 API <public API>` 都必须根据其所属的领域或子系统添加前缀。下面给出了一些领域或子系统前缀的示例，供参考。

* ``k_`` 用于内核
* ``sys_`` 用于系统级代码和功能
* ``net_`` 用于网络子系统
* ``bt_`` 用于蓝牙子系统
* ``i2c_`` 用于 I2C 控制器子系统
