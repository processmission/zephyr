.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

概述
####

电源管理子系统提供的接口和 API 在设计上与架构和 SoC 无关。这使得电源管理的实现可以方便地适配不同的 SoC 和架构。

这种与架构和 SoC 的无关性是通过把核心 PM 基础设施与 SoC 相关组件的实现分离来实现的。这样就向操作系统的其余部分以及应用层提供了一致的抽象。

电源管理功能划分为以下几类。

* 系统电源管理
* 设备电源管理
