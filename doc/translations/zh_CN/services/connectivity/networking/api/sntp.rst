.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _sntp_interface:

简单网络时间协议（SNTP）库
##########################

.. contents::
    :local:
    :depth: 2

概述
****

SNTP 库实现了 :rfc:`4330`。

SNTP 提供了一种在计算机网络中同步时钟的方法。

客户端（:kconfig:option:`CONFIG_SNTP`）从 SNTP 服务器查询时间。服务器（:kconfig:option:`CONFIG_SNTP_SERVER`）会在所有已启用的地址族上应答 UDP 端口 123 的此类查询。应用负责设置系统时钟，并通过 :c:func:`sntp_server_clock_source` 告知服务器其时间来源。在此之前，服务器应答时会将闰秒指示符设置为“时钟未同步”，层级（stratum）为 16，以便客户端丢弃其时间戳。

API 参考
********

.. doxygengroup:: sntp

.. doxygengroup:: sntp_server
