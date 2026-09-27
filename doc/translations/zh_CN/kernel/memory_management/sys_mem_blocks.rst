.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _sys_mem_blocks:

内存块分配器
############

内存块分配器允许从指定内存区域动态分配内存块，并具有以下特点：

* 所有内存块具有相同的固定大小。

* 可以一次分配或释放多个块。

* 同一次分配得到的一组块不一定连续，适用于分散／聚集 DMA 传输等操作。

* 已分配块的管理信息存储在关联缓冲区之外，与内存 slab 不同。因此，缓冲区可以放在能够断电以节能的内存区域中。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的内存块分配器（仅受可用 RAM 限制）。每个分配器都通过其内存地址引用。

内存块分配器具有以下主要属性：

* 每个块的 **块大小**，以字节为单位。长度至少为 4N 字节，其中 N 大于 0。

* 可供分配的 **块数量**，必须大于零。

* 一个 **缓冲区**，为分配器提供分配内存块所用的底层存储。长度至少为“块大小”乘以“块数量”字节。

* 一个 **块位图**，用于跟踪哪些块已被分配。

缓冲区必须按 N 字节边界对齐，其中 N 为大于 2 的 2 的幂，即 4、8、16 等。为确保缓冲区中的所有块都按同一边界对齐，块大小也必须为 N 的倍数。

由于内部管理结构及其创建方式的要求，每个内存块分配器都必须在编译时声明和定义。

内部工作方式
============

每个分配器关联的缓冲区都是固定大小块的数组，块之间没有浪费的空间。

内存块分配器使用位图跟踪未分配的块。

Memory Blocks Allocator
***********************

内存块分配器内部使用位图跟踪哪些块已分配。每个分配器通过 ``sys_bitarray`` 接口，逐个从底层缓冲区取得内存块，直到达到请求数量。分配器的所有元数据都存储在底层缓冲区之外。由于分配器代码从不访问缓冲区内容，该缓冲区所在的内存区域可以断电以节能。

多内存块分配器组
****************

多内存块分配器组的辅助函数用于方便地管理一组分配器。用户可以编写自定义函数，从组内选择用于分配内存块的分配器。

应在运行时通过 :c:func:`sys_multi_mem_blocks_init` 初始化分配器组，再通过 :c:func:`sys_multi_mem_blocks_add_allocator` 将各个分配器加入其中。

从组中分配内存块时，调用 :c:func:`sys_multi_mem_blocks_alloc` 并传入一个不透明的“配置”参数。该参数会直接传给分配器选择函数，以选出合适的分配器。选定后，通过 :c:func:`sys_mem_blocks_alloc` 分配内存块。

可以通过 :c:func:`sys_multi_mem_blocks_free` 释放已分配的内存块。调用者无需传入配置参数；分配器代码会根据传入的内存地址找到正确的分配器，再通过 :c:func:`sys_mem_blocks_free` 释放内存块。

用法
****

定义内存块分配器
================

内存块分配器使用 :c:type:`sys_mem_blocks_t` 类型的变量定义，必须调用 :c:macro:`SYS_MEM_BLOCKS_DEFINE` 在编译时定义并初始化。

以下代码定义并初始化一个内存块分配器，包含 4 个长度为 64 字节的块，每个块均按 4 字节边界对齐：

.. code-block:: c

   SYS_MEM_BLOCKS_DEFINE(allocator, 64, 4, 4);

同样，可以在私有作用域中定义内存块分配器：

.. code-block:: c

   SYS_MEM_BLOCKS_DEFINE_STATIC(static_allocator, 64, 4, 4);

也可以向分配器提供预先定义的缓冲区，以便将缓冲区放在单独的位置。注意，定义缓冲区时 **必须** 指定其对齐方式。

.. code-block:: c

   uint8_t __aligned(4) backing_buffer[64 * 4];
   SYS_MEM_BLOCKS_DEFINE_WITH_EXT_BUF(allocator, 64, 4, backing_buffer);

分配内存块
==========

调用 :c:func:`sys_mem_blocks_alloc` 可以分配内存块。

.. code-block:: c

   int ret;
   uintptr_t blocks[2];

   ret = sys_mem_blocks_alloc(allocator, 2, blocks);

如果 ``ret == 0``，数组 ``blocks`` 中将包含指向已分配块的内存地址。

释放内存块
==========

调用 :c:func:`sys_mem_blocks_free` 可以释放内存块。

以下代码延续上面的示例，分配 2 个内存块，并在不再需要时释放。

.. code-block:: c

   int ret;
   uintptr_t blocks[2];

   ret = sys_mem_blocks_alloc(allocator, 2, blocks);
   ... /* perform some operations on the allocated memory blocks */
   ret = sys_mem_blocks_free(allocator, 2, blocks);

使用多内存块分配器组
====================

以下代码演示如何初始化分配器组：

.. code-block:: c

   sys_mem_blocks_t *choice_fn(struct sys_multi_mem_blocks *group, void *cfg)
   {
       ... /* choose which allocator in the group to use based on cfg */
   }

   SYS_MEM_BLOCKS_DEFINE(allocator0, 64, 4, 4);
   SYS_MEM_BLOCKS_DEFINE(allocator1, 64, 4, 4);

   static sys_multi_mem_blocks_t alloc_group;

   sys_multi_mem_blocks_init(&alloc_group, choice_fn);
   sys_multi_mem_blocks_add_allocator(&alloc_group, &allocator0);
   sys_multi_mem_blocks_add_allocator(&alloc_group, &allocator1);

从组中分配和释放内存块：

.. code-block:: c

   int ret;
   uintptr_t blocks[1];
   size_t blk_size;

   ret = sys_multi_mem_blocks_alloc(&alloc_group, UINT_TO_POINTER(0),
                                    1, blocks, &blk_size);

   ret = sys_multi_mem_blocks_free(&alloc_group, 1, blocks);

API 参考
********

.. doxygengroup:: mem_blocks_apis
