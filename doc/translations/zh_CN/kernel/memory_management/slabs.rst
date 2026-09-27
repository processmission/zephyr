.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _memory_slabs_v2:

内存 slab
#########

:dfn:`内存 slab` 是一种内核对象，允许从指定内存区域动态分配内存块。同一 slab 中的所有内存块都具有相同的固定大小，因此可以高效分配和释放，并避免内存碎片问题。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的内存 slab（仅受可用 RAM 限制）。每个内存 slab 都通过其内存地址引用。

内存 slab 具有以下主要属性：

* 每个块的 **块大小**，以字节为单位。在 32 位平台上至少为 4N 字节，在 64 位平台上至少为 8N 字节，其中 N 大于 0。

* 可供分配的 **块数量**，必须大于零。

* 为 slab 的内存块提供存储空间的 **缓冲区**，长度至少为“块大小”乘以“块数量”字节。

内存 slab 的缓冲区必须按 N 字节边界对齐，其中 N 为 2 的幂。32 位平台上的 N 至少为 4，64 位平台上的 N 至少为 8。为确保缓冲区中的所有内存块都按同一边界对齐，块大小也必须为 N 的倍数。

内存 slab 必须初始化后才能使用。初始化会将所有块标记为未使用。

线程需要内存块时，只需从内存 slab 中分配。使用完毕后，必须将块释放回 slab，以便复用。

如果所有块都在使用中，线程可以选择等待某个块变为可用。任意数量的线程都可以同时等待一个没有空闲块的 slab；内存块可用后，会被交给优先级最高且等待时间最长的线程。

需要时可以定义多个内存 slab，以便分别提供较小或较大的内存块。也可以改用内存池对象。

内部工作方式
============

内存 slab 的缓冲区是一个固定大小块的数组，块之间没有浪费的空间。

内存 slab 使用链表跟踪未分配的块。32 位平台使用每个空闲块的前 4 字节保存链表指针，64 位平台则使用前 8 字节。

实现
****

定义内存 slab
=============

内存 slab 使用 :c:type:`k_mem_slab` 类型的变量定义，随后必须调用 :c:func:`k_mem_slab_init` 进行初始化。

以下代码定义并初始化一个内存 slab，包含 6 个长度为 400 字节的块，每个块均按 8 字节边界对齐。

.. code-block:: c

    struct k_mem_slab my_slab;
    char __aligned(8) my_slab_buffer[6 * 400];

    k_mem_slab_init(&my_slab, my_slab_buffer, 400, 6);

也可以使用 :c:macro:`K_MEM_SLAB_DEFINE` 在编译时定义并初始化内存 slab。

以下代码与上面的代码片段效果相同。注意，该宏同时定义了内存 slab 及其缓冲区。

.. code-block:: c

    K_MEM_SLAB_DEFINE(my_slab, 400, 6, 8);

同样，可以在私有作用域中定义内存 slab：

.. code-block:: c

    K_MEM_SLAB_DEFINE_STATIC(my_slab, 400, 6, 8);

分配内存块
==========

调用 :c:func:`k_mem_slab_alloc` 可以分配内存块。

以下代码延续上面的示例，等待内存块可用，最长等待 100 毫秒，然后将其清零。如果未取得合适的块，则打印警告。

.. code-block:: c

    char *block_ptr;

    if (k_mem_slab_alloc(&my_slab, (void **)&block_ptr, K_MSEC(100)) == 0) {
        memset(block_ptr, 0, 400);
        ...
    } else {
        printf("Memory allocation time-out");
    }

释放内存块
==========

调用 :c:func:`k_mem_slab_free` 可以释放内存块。

以下代码延续上面的示例，分配一个内存块，并在不再需要时释放。

.. code-block:: c

    char *block_ptr;

    k_mem_slab_alloc(&my_slab, (void **)&block_ptr, K_FOREVER);
    ... /* use memory block pointed at by block_ptr */
    k_mem_slab_free(&my_slab, (void *)block_ptr);

查询 slab 使用情况
==================

可以在运行时查询内存 slab 的当前使用情况。:c:func:`k_mem_slab_num_used_get` 返回当前已分配的块数，:c:func:`k_mem_slab_num_free_get` 返回仍可用的块数。启用 :kconfig:option:`CONFIG_MEM_SLAB_TRACE_MAX_UTILIZATION` 时，:c:func:`k_mem_slab_max_used_get` 报告同时分配的块数峰值，:c:func:`k_mem_slab_runtime_stats_get` 则通过 :c:struct:`sys_memory_stats` 结构体一并返回这些数据。

使用建议
********

使用内存 slab 以固定大小的块为单位分配和释放内存。

在线程之间传递大量数据时，使用内存 slab 块可避免不必要的数据复制。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_MEM_SLAB_TRACE_MAX_UTILIZATION`

API 参考
********

.. doxygengroup:: mem_slab_apis
