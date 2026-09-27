.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_stat:

Mesh 统计
#########

统计 API 提供对 Bluetooth Mesh 通信的运行时监控。

帧统计
******

帧统计 API 允许监控不同接口上接收到的帧数量，以及计划的和成功的传输与中继尝试次数。

该 API 帮助用户评估广播者配置参数的效率以及设备的扫描能力。可以通过自定义值轻松扩展受监控参数的数量。

LPN 时序测量
************

启用 :kconfig:option:`CONFIG_BT_MESH_LOW_POWER` 后，统计模块通过对协议事件打时间戳来测量 LPN friendship 时序参数：

* T1：轮询发送完成
* T2：扫描器启用（ReceiveDelay 已过）
* T3：收到 Friend 响应或 ReceiveWindow 到期

根据这些时间戳，模块以微秒为单位计算测得的 ReceiveDelay（T2 - T1）和 ReceiveWindow（T3 - T2）。应用可以使用这些值，根据配置的 friendship 参数评估实际空口时序。

应用可以随时读取和重置统计数据。

API 参考
********

.. doxygengroup:: bt_mesh_stat
