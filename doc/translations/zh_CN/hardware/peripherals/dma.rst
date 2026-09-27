.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _dma_api:

直接内存访问（DMA）
###################

概述
****

直接内存访问（控制器）是一种常见的协处理器，通常可以代替 CPU 完成外设与内存之间的数据传输。

DMA API 并非可移植的 API，实际上也无法做到可移植，因为每种 DMA 都有独特的内存要求、外设交互方式和功能。该 API 实际上汇集了代码树中各个驱动所需的所有实用 DMA 功能。对于 DMA IP 非常相似但略有差异的厂商，只要谨慎使用，它仍然可以为其外设提供良好的抽象。

DMA 驱动通常不处理缓存一致性；这由开发者负责，因为不同应用的要求差异很大。有关 Zephyr 中缓存管理的概述，请参阅 :ref:`cache_guide` 。

驱动实现要求
************

同步与所有权
++++++++++++

从 API 的角度来看，DMA 通道是一个只有单一所有者的对象，这意味着驱动不应尝试使用互斥锁或信号量等内核同步原语来保护通道。如果 DMA 通道需要修改共享寄存器，则应使用自旋锁保护这些寄存器更新操作。

这样可以使整个 API 保持低开销，并且能够从任何调用上下文中调用，包括中断服务例程（ISR）；在 ISR 中启动、停止、挂起、恢复或重新加载通道传输可能非常有用。

传输描述符内存管理
++++++++++++++++++

驱动不应尝试使用任何形式的堆内存分配。如果传输描述符需要对象池，则应以不破坏允许在 ISR 中调用这一保证的方式设置对象池。许多驱动选择为每个通道创建一个简单的静态描述符数组，并通过 Kconfig 调整描述符数组的大小。

通道状态机要求
++++++++++++++

应将 DMA 通道视为状态机，DMA API 通过 API 调用的形式为其提供状态转换事件。每个驱动都应自行跟踪通道状态。应能够随时通过 :c:func:`dma_get_status()` 检查通道的忙碌状态。

此处提供了一张示意图，展示预期可能发生的状态转换及其对应的 API 调用，供参考。

.. graphviz::
   :caption: DMA 有限状态机

   digraph {
       node [style=rounded];
       edge [fontname=Courier];
       init [shape=point];

       CONFIGURED [label=Configured,shape=box];
       RUNNING [label=Running,shape=box];
       SUSPENDED [label=Suspended,shape=box];

       init -> CONFIGURED [label=dma_config];

       CONFIGURED -> RUNNING [label=dma_start];
       CONFIGURED -> CONFIGURED [label=dma_stop, headport=c, tailport=e];
       CONFIGURED -> CONFIGURED [label=dma_config, headport=c, tailport=w];

       RUNNING -> CONFIGURED [label=dma_stop];
       RUNNING -> RUNNING [label=dma_start];
       RUNNING -> RUNNING [label=dma_resume, headport=w];
       RUNNING -> SUSPENDED [label=dma_suspend];

       SUSPENDED -> SUSPENDED [label=dma_suspend];
       SUSPENDED -> RUNNING [label=dma_resume];
       SUSPENDED -> CONFIGURED [label=dma_stop];
   }

API 参考
********

.. doxygengroup:: dma_interface
