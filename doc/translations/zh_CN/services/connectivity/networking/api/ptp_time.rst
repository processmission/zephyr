.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ptp_time_interface:


精确时间协议（PTP）时间格式
###########################

.. contents::
    :local:
    :depth: 2

概述
****

PTP 时间结构体可以以高精度格式（纳秒）存储时间信息。扩展时间戳格式可以存储具有小数纳秒精度的时间。PTP 时间格式用于 :ref:`gptp_interface` 实现。

API 参考
********

.. doxygengroup:: ptp_time
