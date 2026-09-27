.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_core_interface:

网络核心辅助函数
################

.. contents::
    :local:
    :depth: 2

概述
****

网络子系统包含两个用于从网络收发数据的函数。网络设备驱动通常使用 ``net_recv_data()``，将接收到的网络数据向上推送至网络协议栈以进一步处理。所有数据都通过网络接口接收，而该接口通常由设备驱动创建。

发送数据可以使用 ``net_send_data()``。通常应用不直接调用该函数，因为已有 :ref:`bsd_sockets_interface` API 用于收发网络数据。

API 参考
********

.. doxygengroup:: net_core
