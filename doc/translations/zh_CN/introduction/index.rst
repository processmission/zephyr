.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _introducing_zephyr:

简介
####

Zephyr OS 基于一个小型内核，面向资源受限的嵌入式系统设计，应用范围从简单的嵌入式环境传感器和 LED 穿戴设备，到复杂的嵌入式控制器、智能手表和 IoT 无线应用。

Zephyr 内核支持多种架构，包括：

 - ARCv2（EM 和 HS）以及 ARCv3（HS6X）
 - ARMv6-M、ARMv7-M 和 ARMv8-M（Cortex-M）
 - ARMv7-A 和 ARMv8-A（Cortex-A，32 位和 64 位）
 - ARMv7-R、ARMv8-R（Cortex-R，32 位和 64 位）
 - Qualcomm Hexagon
 - Intel x86（32 位和 64 位）
 - MIPS（MIPS32 Release 1 规范）
 - OpenRISC（32 位）
 - Renesas RX
 - RISC-V（32 位和 64 位）
 - SPARC V8
 - Tensilica Xtensa
 - TriCore（TC1.6.2 和 TC1.8）

这些架构支持的开发板完整列表见 :ref:`此处 <boards>`。

在 Zephyr OS 中，:term:`子系统 <subsystem>` 指操作系统中负责特定功能或提供特定服务的逻辑独立部分。子系统可以包括网络、文件系统、设备驱动类别、电源管理和通信协议等组件。每个子系统都采用模块化设计，可根据不同嵌入式应用的需求进行配置、定制和扩展。

许可证
******

Zephyr 采用宽松的 `Apache 2.0 license`_ 授权（见项目 `GitHub repo`_ 中的 ``LICENSE`` 文件）。Zephyr 项目中有少量导入或复用的组件采用其他许可证，详情见 :ref:`Zephyr_Licensing`。

.. _Apache 2.0 license:
   https://github.com/zephyrproject-rtos/zephyr/blob/main/LICENSE

.. _GitHub repo: https://github.com/zephyrproject-rtos/zephyr


主要特性
********

Zephyr 提供大量且持续增长的功能，包括：

**丰富的内核服务**
   Zephyr 提供多种常用的开发服务：

   * *多线程服务*：支持协作式、基于优先级的非抢占式线程和抢占式线程，并可选轮转时间片调度。包含兼容 POSIX pthreads 的 API。

   * *中断服务*：支持在编译期注册中断处理程序。

   * *内存分配服务*：支持动态分配和释放固定大小或可变大小的内存块。

   * *线程间同步服务*：提供二值信号量、计数信号量和互斥信号量。

   * *线程间数据传递服务*：提供基础消息队列、增强消息队列和字节流。

   * *电源管理服务*：包括应用或策略定义的系统电源管理，以及驱动定义的细粒度设备电源管理。

**多种调度算法**
   Zephyr 提供全面的线程调度选项：

   * 协作式和抢占式调度
   * 最早截止时间优先（EDF）
   * 实现“中断下半部”或“tasklet”行为的 Meta IRQ 调度
   * 时间片调度：在优先级相同的可抢占线程之间分配时间片
   * 多种就绪队列策略：

     * 简单链表就绪队列
     * 红黑树就绪队列
     * 传统多队列就绪队列

.. _zephyr_intro_configurability:

**高度可配置、模块化灵活设计**
   应用可以只集成所需功能，并指定各项资源的数量和大小。

**跨架构支持**
   支持多种不同 CPU 架构和开发工具对应的 :ref:`受支持开发板 <boards>`。社区贡献持续扩展对 SoC、平台和驱动的支持。

**内存保护**
   提供可配置的架构专用栈溢出保护、内核对象和设备驱动权限跟踪，以及线程隔离。x86、ARC 和 ARM 架构支持线程级内存保护、用户空间和内存域。

   对于没有 MMU/MPU 的平台和内存受限设备，支持将应用专用代码与定制内核组合成单体镜像，并加载到硬件上执行。应用代码和内核代码在同一个共享地址空间中运行。

**编译期资源定义**
   支持在编译期定义系统资源，以减小代码体积并提升资源受限系统的性能。

**优化的设备驱动模型**
   提供统一的设备模型，用于配置平台或系统包含的驱动并初始化已配置的所有驱动；对于具有相同设备或 IP 模块的平台，还可以复用驱动。

**Devicetree 支持**
   使用 :ref:`Devicetree <dt-guide>` 描述硬件，并根据其中的信息生成应用镜像。

**支持多种协议的原生网络协议栈**
   网络功能完整且经过优化，包括 LwM2M 和兼容 BSD sockets 的支持。还支持在 Nordic 芯片组上运行 OpenThread。OpenThread 是一种网状网络，可安全、可靠地连接家庭中的数百种产品。

**Bluetooth Low Energy 5.0 支持**
   符合 Bluetooth 5.0（ESR10）规范，并支持 Bluetooth Low Energy Controller（LE Link Layer）。还包含 Bluetooth Mesh 和可用于 Bluetooth 认证的控制器。

   * 支持通用访问配置文件（GAP）的所有 LE 角色
   * 通用属性配置文件（GATT）
   * 支持配对，包括 Bluetooth 4.2 引入的 Secure Connections 功能
   * 简洁的 HCI 驱动抽象层
   * 提供原始 HCI 接口，可让 Zephyr 以 Controller 模式运行，而不启用完整 Host 协议栈
   * 已在多种常见控制器上验证
   * 高度可配置

   Mesh 支持：

   * 支持 Relay、Friend Node、Low-Power Node（LPN）和 GATT Proxy 功能
   * 支持两种 Provisioning bearer（PB-ADV 和 PB-GATT）
   * 可灵活配置，可运行在至少有 16 KiB RAM 的设备上

**原生 Linux、macOS 和 Windows 开发环境**
   命令行 CMake 构建环境可运行在主流开发操作系统上。原生移植 (:zephyr:board:`native_sim <native_sim>`) 支持将 Zephyr 构建并作为 Linux 原生应用运行，便于开发和测试。

**支持 ext2、FatFs 和 LittleFS 的虚拟文件系统接口**
   支持 ext2、LittleFS 和 FatFs；面向内存受限应用提供 FCB（Flash Circular Buffer，闪存循环缓冲区）。

**强大的多后端日志框架**
   支持日志过滤、对象转储、panic 模式和多个后端（内存、网络、文件系统、控制台等），并可与 shell 子系统集成。

**易用且功能丰富的 Shell 接口**
   多实例 shell 子系统提供自动补全、通配符、着色、特殊按键（方向键、Backspace、Ctrl+U 等）和历史记录等易用功能。支持静态命令和动态子命令。

**在非易失性存储中保存设置**
   设置子系统为模块提供持久化保存设备配置和运行状态的方式。设置项以键值对字符串形式存储。

**非易失性存储（NVS）**
  NVS 支持存储二进制块、字符串、整数、长整数及其任意组合。

**原生移植**
  :zephyr:board:`Native sim <native_sim>` 支持将 Zephyr 作为 Linux 应用运行，并提供多种子系统和网络功能。


.. include:: ../../README.rst
   :start-after: start_include_here


基本术语与概念
**************

参见 :ref:`术语表 <glossary>`
