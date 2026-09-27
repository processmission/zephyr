.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mbox_api:

多通道处理器间邮箱（MBOX）
##########################

概述
****

MBOX 设备是一种能够在系统中的 CPU 和 CPU 集群之间传递信号（以及数据，具体取决于外设）的外设。每个 MBOX 实例提供一个或多个通道，每个通道均指向另一个 CPU 集群（多个通道可以指向同一个集群）。


API 参考
********

.. doxygengroup:: mbox_interface
