.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mdio_api:

管理数据输入/输出（MDIO）
#########################

概述
****

MDIO 是一种常用于与以太网 PHY 设备通信的总线。许多以太网 MAC 控制器也提供了通过 MDIO 总线与外设通信的硬件。

此 API 主要供 PHY 驱动程序使用，也可供用户固件使用。

API 参考
********

.. doxygengroup:: mdio_interface
