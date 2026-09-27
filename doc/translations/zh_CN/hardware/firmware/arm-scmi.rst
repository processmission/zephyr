.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _arm_scmi:

ARM 系统控制与管理接口
######################

概述
****

系统控制与管理接口（SCMI）是 ARM 制定的一项规范，描述了一组与操作系统无关的软件接口，用于执行系统管理（例如时钟控制、引脚控制等）。在此场景中，Zephyr 充当 SCMI 代理。

.. note::

   Zephyr 的实现可能仅包含本文档所述特性或功能的一部分。

标准协议
********

支持的 **标准** [#]_ 协议汇总如下：

.. list-table::
   :align: center

   * - ID
     - 名称
     - 支持的版本

   * - 0x10
     - 基础协议
     - 2.1

   * - 0x11
     - 电源域管理协议
     - 3.1

   * - 0x12
     - 系统电源管理协议
     - 2.1

   * - 0x14
     - 时钟管理协议
     - 3.0

   * - 0x19
     - 引脚控制协议
     - 1.0

传输机制
********

支持的传输机制汇总如下：

.. list-table::
   :align: center

   * - 名称
     - 描述
     - 兼容字符串

   * - MBOX
     - 采用基于邮箱的门铃机制的共享内存
     - :dtcompatible:`arm,scmi`

   * - SMC
     - 采用基于 SMC 的门铃机制的共享内存
     - :dtcompatible:`arm,scmi-smc`

厂商扩展
********

SCMI 规范允许厂商引入额外的协议，并为平台固件在某些情况下的行为提供一定的自由度。在本文档中，这些统称为 **厂商扩展** 。

NXP
===

NXP 提供了符合 SCMI 规范的平台固件，称为 **System Manager (SM)** 。其文档可在 `此处 <https://github.com/nxp-imx/imx-sm>`__ 查阅。

支持的 NXP 专用协议汇总如下：

.. list-table::
   :align: center

   * - ID
     - 名称
     - 支持的版本

   * - 0x82
     - CPU
     - 1.0

支持的 NXP 特有特殊行为汇总如下：

#. 根据平台固件的配置，共享内存中可能包含消息 CRC 字段，固件会对收到的每条消息检查此字段。请参阅 :kconfig:option:`CONFIG_ARM_SCMI_NXP_VENDOR_EXTENSIONS` 。

.. rubric:: 脚注

.. [#] 指 SCMI 规范涵盖的协议。
