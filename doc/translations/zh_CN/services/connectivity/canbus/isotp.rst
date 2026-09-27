.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _can_isotp:

ISO-TP 传输协议
###############

.. contents::
    :local:
    :depth: 2

概述
****

ISO-TP 是 ISO 标准 ISO15765-2《道路车辆——基于控制器局域网的诊断通信（DoCAN）第 2 部分：传输协议与网络层服务》中定义的传输协议。顾名思义，它最初就是为道路车辆的控制器局域网诊断而设计，并且至今仍在使用。不过，它并不限于道路车辆或汽车领域的应用。

该传输协议将经典 CAN（8 字节）和 CAN FD（64 字节）有限的有效载荷数据大小扩展到理论上的 4 GB。此外，它还增加了流控制机制来影响发送方的行为。ISO-TP 会根据 CAN 帧的有效载荷大小将数据包分割成小片段，这些片段的头部称为协议控制信息（PCI，Protocol Control Information）。

在经典 CAN 上，小于或等于七字节的数据包称为单帧（SF，single-frame）。它们无需分片，也没有任何流控制。

更大的数据包会被分段为一个首帧（FF，first-frame）和所需数量的连续帧（CF，consecutive-frame）。首帧包含整个有效载荷数据的长度信息，以及有效载荷数据的前几个字节。接收方会回送一个流控制帧（FC，flow-control-frame），以拒绝、推迟或接受后续的连续帧。流控制帧还定义了发送条件，即块大小（BS，block-size）和帧之间的最小间隔时间（STmin）。块大小定义了发送方在必须等待下一个流控制帧之前允许发送的连续帧数量。

.. image:: isotp_sequence.svg
   :width: 20%
   :align: center
   :alt: ISO-TP 时序

API 参考
********

.. doxygengroup:: can_isotp
