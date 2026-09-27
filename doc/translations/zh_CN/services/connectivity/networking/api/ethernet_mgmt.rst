.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ethernet_mgmt_interface:

以太网管理
##########

.. contents::
    :local:
    :depth: 2

概述
****

以太网管理 API 提供用于管理以太网网络接口底层状态的函数。这些函数的调用者可以：

* 引发 ``carrier ON`` 或 ``carrier OFF`` 管理事件
* 引发 ``VLAN enabled`` 或 ``VLAN disabled`` 管理事件

通常，``carrier OFF`` 事件由以太网设备驱动在检测到网线断开时生成；如果以太网设备驱动检测到网线重新连接，则会生成 ``carrier ON`` 事件。

目前，当启用或禁用特定 VLAN 标签时，VLAN 事件由以太网 L2 层生成。

如果用户应用需要在相应状态发生变化时执行操作，则可以监听这些事件。

API 参考
********

.. doxygengroup:: ethernet_mgmt
