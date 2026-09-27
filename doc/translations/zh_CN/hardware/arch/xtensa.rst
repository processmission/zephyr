.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _xtensa_developer_guide:

Xtensa 开发者指南
#################

概述
****

本页介绍为基于 Xtensa 的平台进行开发时需要了解的一些事项。

HiFi 音频引擎 DSP
*****************

在支持 HiFi 音频引擎 DSP 寄存器的开发板上，内核允许线程使用这些寄存器。内核仅支持线程使用 HiFi 寄存器，不支持中断服务例程（ISR）使用这些寄存器。

.. note::
    目前，仅 Intel ADSP ACE 硬件平台默认配置为支持 HiFi。

概念
====

可以配置内核，使应用能够使用 Xtensa HiFi 音频引擎 DSP 提供的服务。内核支持以下三种工作模式。

不使用 HiFi 寄存器模式
----------------------

当应用中没有线程使用 HiFi 寄存器时，使用此模式。这是内核默认的 HiFi 服务模式。

HiFi 寄存器非共享模式
---------------------

当应用中只有一个线程使用 HiFi 寄存器时，使用此模式。每次发生上下文切换时，HiFi 寄存器均保持不变。

.. note::
    如果两个或更多线程尝试使用 HiFi 寄存器，则行为未定义，因为内核不会尝试检测或阻止多个线程使用这些寄存器。

HiFi 寄存器共享模式
-------------------

当应用中有两个或更多线程使用 HiFi 寄存器时，使用此模式。启用后，内核会自动允许所有线程使用 HiFi 寄存器。从概念上看，此模式可细分为两种子模式：即时模式和延迟模式。两者都会保存和恢复 HiFi 寄存器，但保存和恢复寄存器的时机不同，保存的目标位置和恢复的来源位置也不同。

在即时共享模型中，每次线程上下文切换时都会保存和恢复 HiFi 寄存器，无论线程是否使用过这些寄存器。由于需要保存额外的寄存器，每个线程可能需要额外的栈空间。这是两种模型中的默认模型。

在延迟共享模型中，内核会跟踪“拥有”协处理器的线程。如果“拥有”协处理器的线程被切出，HiFi 寄存器不会立即保存，而是等到新线程尝试使用 HiFi 时才保存，随后该新线程成为新的拥有者，并加载其 HiFi 寄存器值。

.. note::
    如果 SMP 系统检测到即将成为拥有者的线程仍是另一个 CPU 上的拥有者，就会向该 CPU 发送处理器间中断（IPI），以启动将其 HiFi 寄存器保存到内存的操作。随后，当前处理器会自旋等待，直到 HiFi 寄存器保存完成。这种自旋等待可能偶尔导致较长的延迟。为获得最佳性能，建议将使用 HiFi 的线程绑定到单个 CPU。

配置选项
========

当配置选项 :kconfig:option:`CONFIG_XTENSA_HIFI_SHARING` 被禁用，而配置选项 :kconfig:option:`CONFIG_XTENSA_HIFI3` 和/或 :kconfig:option:`CONFIG_XTENSA_HIFI4` 被启用时，将选择 HiFi 寄存器非共享模式。

当启用配置选项 :kconfig:option:`CONFIG_XTENSA_HIFI3` 和/或 :kconfig:option:`CONFIG_XTENSA_HIFI4` ，并同时启用配置选项 :kconfig:option:`CONFIG_XTENSA_HIFI_SHARING` 时，将选择 HiFi 寄存器共享模式。如上所述，线程必须具有足够的栈空间，以便在上下文切换期间保存 HiFi 寄存器值。

即时和延迟 HiFi 共享模式都要求启用配置选项 :kconfig:option:`CONFIG_XTENSA_HIFI_SHARING` 。虽然默认采用即时 HiFi 共享模式，但也可以通过启用配置选项 :kconfig:option:`CONFIG_XTENSA_EAGER_HIFI_SHARING` 来显式选择该模式。要改用延迟 HiFi 共享模式，请启用配置选项 :kconfig:option:`CONFIG_XTENSA_LAZY_HIFI_SHARING` 。
