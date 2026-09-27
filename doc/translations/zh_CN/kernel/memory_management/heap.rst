.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _heap_v2:

内存堆
######

Zephyr 提供一组工具，允许线程动态分配内存。

带同步的堆分配器
****************

创建堆
======

定义堆最简单的方式是使用 :c:macro:`K_HEAP_DEFINE` 宏进行静态定义。它创建一个具有指定名称的静态 :c:struct:`k_heap` 变量，用于管理指定大小的内存区域。

也可以使用 :c:func:`k_heap_init` 创建堆，管理由应用控制的任意内存区域。

分配内存
========

使用 :c:func:`k_heap_alloc`，传入堆对象地址和所需字节数，即可从堆中分配内存。其行为类似标准 C 的 ``malloc()``，分配失败时返回 NULL 指针。

堆支持阻塞操作，允许线程睡眠直到内存可用。最后一个参数是 :c:type:`k_timeout_t` 类型的超时值，表示线程返回前最多可以睡眠多久，也可以使用超时常量 :c:macro:`K_NO_WAIT` 或 :c:macro:`K_FOREVER`。

需要特定对齐方式的块时，可以使用 :c:func:`k_heap_aligned_alloc`。调用者提供一个为 2 的幂的对齐值，分配块的起始地址将是该值的倍数。:c:func:`k_heap_calloc` 则分配数组并将其清零。

可以使用 :c:func:`k_heap_realloc` 改变已分配区域的大小。它返回所需大小的块，并保留旧大小与新大小中较小值范围内的内容。与标准 C 的 ``realloc()`` 一样，返回的指针可能与原指针不同。

释放内存
========

使用 :c:func:`k_heap_alloc` 分配的内存必须通过 :c:func:`k_heap_free` 释放。与标准 C 的 ``free()`` 类似，传入的指针必须为 ``NULL``，或此前由同一个堆的 :c:func:`k_heap_alloc` 返回的指针。释放 ``NULL`` 不产生任何效果。

枚举堆
======

所有通过 :c:macro:`K_HEAP_DEFINE` 静态定义的堆都会放入专用链接器段，从而可在运行时枚举。:c:func:`k_heap_array_get` 返回静态堆数组的地址及其中的条目数，主要用于需要检查系统全部堆的监测和诊断功能。

底层堆分配器
************

:c:struct:`k_heap` 抽象的底层实现由名为 :c:struct:`sys_heap` 的数据结构提供。它具有完全相同的分配语义，但不提供内核同步工具。应用如果需要在同步不可用或较难实现的上下文中（例如用户空间）自行管理内存块，可以使用它。与 ``k_heap`` 不同，对同一个堆的所有 ``sys_heap`` 函数调用都必须由调用者串行化，不允许不同线程同时使用。

实现
====

在内部，``sys_heap`` 内存区域被划分为 8 字节的“单元”。每次分配都由连续的单元区域组成。每个已分配块或空闲块的起始单元包含一个头部，记录块长度、物理内存中相邻低地址侧（“左侧”）块的长度、表示是否在用的标志位，以及空闲链表中前后块的链接；链接以单元索引表示，未使用的块会加入该空闲链表。

堆实现会采取措施减少碎片。空闲块按大小存放在不同的“桶”中，每个桶覆盖一个以 2 的幂划分的大小区间，例如 3—4 个单元、5—8 个单元、9—16 个单元等。这样，新分配可以优先使用可用的最小、最零碎的块。此外，已分配块释放回堆时，会自动与相邻空闲块合并，以防止碎片化。

所有元数据都存储在连续堆内存区域的开头，包括长度随堆大小变化的桶链表头数组。唯一需要的外部内存是 :c:struct:`sys_heap` 结构体自身。

``sys_heap`` 函数不提供同步。使用者必须防止并发访问，同一时刻只能有一个上下文进入该堆的 API 函数。

堆实现注重高性能和可预测的延迟。所有 ``sys_heap`` API 函数都保证在常数时间内完成，在典型架构上耗时为 1—200 个周期。其中一个细节是：为某次分配搜索最小适用桶（其中的空闲块“可能够用”）时，迭代次数有编译期上限，以避免无界的链表搜索，代价是对碎片的抵抗能力有所降低。用户可在构建时通过 :kconfig:option:`CONFIG_SYS_HEAP_ALLOC_LOOPS` 选择该上限，默认值为 3。

多堆封装工具
************

``sys_heap`` 要求所管理的全部内存位于单个连续区域。复杂的微控制器应用往往具有更复杂的内存布局，却仍希望将其作为“堆”动态管理。例如，内存可能分散于不连续的区域，不同区域可能具有不同的缓存、性能或功耗特性，外设也可能只能对特定区域进行 DMA 访问。

为此，Zephyr 提供 ``sys_multi_heap``。它实际上是对一个或多个 ``sys_heap`` 对象的简单封装。应先初始化子堆，再调用 :c:func:`sys_multi_heap_init` 初始化多堆，之后通过 :c:func:`sys_multi_heap_add_heap` 将各个堆加入管理集合。库不提供销毁工具；与 ``sys_heap`` 一样，需要销毁多堆的应用只需确保所有已分配块都已释放，或至少不再使用，然后将底层内存改作他用。

它提供两个分配入口：:c:func:`sys_multi_heap_alloc` 和 :c:func:`sys_multi_heap_aligned_alloc`。其行为与同类 ``sys_heap`` 函数相同，但额外接收一个不透明的“配置”参数。多堆代码本身不检查该指针，而是将其传给初始化时提供的回调函数。应用提供的回调负责从某个受管理堆实际分配内存，并可按需利用配置参数选择堆。

要缩小或扩大已分配缓冲区，可以使用 :c:func:`sys_multi_heap_realloc` 和 :c:func:`sys_multi_heap_aligned_realloc`。如果无法在缓冲区当前所在的堆上扩容，可以使用配置参数所允许的其他堆。

不再使用的多堆分配内存可以通过 :c:func:`sys_multi_heap_free` 释放，应用无需传入配置参数。从任意受管理 ``sys_heap`` 对象分配的内存都可以用同样方式释放。

系统堆
******

:dfn:`系统堆` 是预定义的内存分配器，允许线程以类似 :c:func:`malloc` 的方式，从公共内存区域动态分配内存。

系统只定义一个系统堆。与其他堆或内存池不同，系统堆不能通过内存地址直接引用。

只要空间允许，系统堆可以配置为任意大小。

线程可以调用 :c:func:`k_malloc` 动态分配一块堆内存。分配地址保证按指针大小的倍数对齐。如果找不到合适的堆内存块，则返回 ``NULL``。

线程使用完一块堆内存后，可以调用 :c:func:`k_free` 将其释放回系统堆。

定义堆内存池
============

堆内存池的大小由 :kconfig:option:`CONFIG_HEAP_MEM_POOL_SIZE` 配置选项指定。

默认情况下，堆内存池大小为零字节，表示内核不定义堆内存池对象。最大大小受系统可用内存限制。如果无法满足指定大小，项目构建会在链接阶段失败。

此外，各子系统（开发板、驱动程序、库等）可以定义以 ``HEAP_MEM_POOL_ADD_SIZE_`` 为前缀的 Kconfig 选项，指定自身需求，单位为字节。如果多个子系统指定了自定义值，则以这些值之和作为最小需求。如果应用尝试设置低于该最小值的大小，该设置会被忽略，改用最小值。

要强制使用低于最小需求的值，应用可以启用 :kconfig:option:`CONFIG_HEAP_MEM_POOL_IGNORE_MIN`。在针对特定应用优化堆大小、能够更准确地确定最小需求时，此选项很有用。

Allocating Memory
=================

调用 :c:func:`k_malloc` 可以分配一块堆内存。

以下代码分配一块 200 字节的堆内存，然后将其清零。如果未取得合适的内存块，则发出警告。

.. code-block:: c

    char *mem_ptr;

    mem_ptr = k_malloc(200);
    if (mem_ptr != NULL)) {
        memset(mem_ptr, 0, 200);
        ...
    } else {
        printf("Memory not allocated");
    }

Releasing Memory
================

调用 :c:func:`k_free` 可以释放一块堆内存。

以下代码分配一块 75 字节的内存，并在不再需要时释放。

.. code-block:: c

    char *mem_ptr;

    mem_ptr = k_malloc(75);
    ... /* use memory block */
    k_free(mem_ptr);

使用建议
========

使用堆内存池以类似 :c:func:`malloc` 的方式动态分配内存。

配置选项
========

相关配置选项：

* :kconfig:option:`CONFIG_HEAP_MEM_POOL_SIZE`

API 参考
========

.. doxygengroup:: heap_apis

.. doxygengroup:: low_level_heap_allocator

.. doxygengroup:: multi_heap_wrapper

堆监听器
********

.. doxygengroup:: heap_listener_apis
