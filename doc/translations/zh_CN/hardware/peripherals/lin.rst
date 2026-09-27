.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _lin:

局部互连网络（LIN）
###################

概述
****

LIN（局部互连网络）是一种串行总线系统。自 2016 年起，ISO 将其纳入国际标准。2025 年，ISO 17987 系列标准的多个部分进行了更新。ISO 17987 系列文档涵盖了 OSI（开放系统互连）七层模型的要求及相应的一致性测试计划。

LIN 底层
========

LIN 数据链路层通常称为 LIN 协议，它规定了一种指挥节点与响应节点之间的通信协议。LIN 指挥节点使用一个或多个预先编程的调度表来启动 LIN 帧的发送和接收。这些调度表至少包含启动 LIN 帧发送的相对时序信息。LIN 帧由帧头和响应两部分组成。LIN 指挥节点发送帧头，而响应则由一个指定的 LIN 响应节点或 LIN 指挥节点自身发送。

帧头包含 1 字节的间断信号（Break）、字节间隔、1 字节的同步字段（SYNC，0x55）、标识符和响应间隔。响应由有效载荷字节和 CRC 字节组成。

LIN 帧中的数据以 8 位数据字节为单位串行传输，每个字节附加一个起始位和一个停止位，但没有奇偶校验位。注意，帧头中的间断字段没有起始位和停止位。

比特率可在 1 kbit/s 至 20 kbit/s 范围内变化。总线上的位值为隐性（逻辑高电平）或显性（逻辑低电平）。LIN 指挥节点的稳定时钟源提供时间基准，最小时间单位为一个位时间（比特率为 19.2 kbit/s 时为 52 µs）。总线定义了两种状态：休眠模式和活动模式。总线上有数据传输时，所有 LIN 节点都必须处于活动模式。经过指定的超时时间后，节点进入休眠模式，并通过唤醒帧恢复到活动模式。任何请求总线活动的节点都可以发送此帧，既可以是按照内部调度运行的 LIN 指挥节点，也可以是由内部软件应用激活的某个已连接的 LIN 响应节点。所有节点唤醒后，LIN 指挥节点继续调度下一个 LIN 帧。

有关 LIN 的更多技术信息，请参阅 `维基百科上的 LIN 条目 <https://en.wikipedia.org/wiki/Local_Interconnect_Network>`_ 。

Zephyr LIN 控制器支持以下 LIN 功能：

* 在指挥节点模式和响应节点模式下发送和接收 LIN 帧。
* 支持帧头掩码的过滤器（响应节点模式），可根据帧头 ID 触发响应节点回调。
* 发送唤醒脉冲。

示例
****

以下示例演示了 Zephyr LIN 控制器 API 的用法：

* :zephyr:code-sample:`lin-ncv7430` ：演示如何在指挥节点模式下使用 LIN API。
* :zephyr:code-sample:`lin-ncv7430-responder` ：通过模拟 NCV7430 LED 控制器，演示如何在响应节点模式下使用 LIN API。

LIN 收发器
**********

LIN 收发器是一种外部设备，用于将 LIN 控制器的逻辑电平信号转换为 LIN 总线电平。一些开发板通过 ``lin-transceiver-gpio`` compatible 直接集成 LIN 收发器控制（使能/唤醒引脚）；LIN 控制器驱动会在执行 :c:func:`lin_start` 和 :c:func:`lin_stop` 时自动启用和禁用收发器，因此应用通常无需直接调用收发器 API。

API 参考
********

.. doxygengroup:: lin_controller

LIN 收发器 API 参考
*******************

.. doxygengroup:: lin_transceiver
