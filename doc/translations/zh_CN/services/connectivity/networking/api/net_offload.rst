.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_offload_interface:

网络流量卸载
============

.. contents::
    :local:
    :depth: 2

网络卸载
########

概述
****

网络卸载 API 提供了一些钩子，设备厂商可以使用它们为 IP 协议栈提供另一种实现。这意味着实际的网络连接创建、数据传输等操作由厂商 HAL 而非 Zephyr 网络协议栈完成。

API 参考
********

.. doxygengroup:: net_offload

.. _net_socket_offloading:

socket 卸载
###########

Overview
********

除网络卸载 API 外，Zephyr 还允许在 socket API 层面卸载网络功能。采用这种方式，为网络设备提供另一套网络协议栈实现并暴露 socket API 的厂商，可以轻松地将其与 Zephyr 集成。

在 socket 层面集成网络卸载的示例实现见 :zephyr_file:`drivers/wifi/simplelink/simplelink_sockets.c`。
