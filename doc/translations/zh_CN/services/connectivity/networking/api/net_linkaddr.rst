.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_linkaddr_interface:

链路层地址处理
##############

.. contents::
    :local:
    :depth: 2

概述
****

为网络接口设置链路层地址，使 L2 连接能在网络协议栈中正常工作。通常链路层地址像以太网那样为 6 字节，但对于 IEEE 802.15.4，链路层地址长度为 8 字节。

API 参考
********

.. doxygengroup:: net_linkaddr
