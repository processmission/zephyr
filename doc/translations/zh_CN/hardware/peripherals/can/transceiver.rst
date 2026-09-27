.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _can_transceiver_api:

CAN 收发器
##########

.. contents::
    :local:
    :depth: 2

概述
****

CAN 收发器是一种外部设备，用于将 CAN 控制器的逻辑电平信号转换为总线电平信号。总线线路称为 CAN High（CAN H）和 CAN Low（CAN L）。从控制器到收发器的发送线称为 CAN TX，接收线称为 CAN RX。这些信号线使用逻辑电平，而总线电平则通过 CAN H 与 CAN L 之间的电压差来判定。总线可以处于隐性（逻辑 1）或显性（逻辑 0）状态。当 CAN H 和 CAN L 两条线路的电压电平大致相同时，总线处于隐性状态。该状态也是空闲状态。要向总线写入一个显性位，开漏晶体管会将 CAN H 连接至 Vdd，并将 CAN L 连接至地。首尾节点在 CAN H 与 CAN L 之间各接入一个 120 欧姆电阻，对总线进行终端匹配。显性状态始终覆盖隐性状态。这种结构称为线与。

.. image:: transceiver.svg
   :width: 70%
   :align: center
   :alt: CAN Transceiver

CAN 收发器 API 参考
*******************

.. doxygengroup:: can_transceiver
