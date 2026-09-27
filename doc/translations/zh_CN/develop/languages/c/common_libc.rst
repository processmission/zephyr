.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _c_library_common:

公共 C 库代码
#############

Zephyr 提供一些可与多种 C 库配合使用的 C 库函数。它们补充多种 C 库中缺少的函数，或以更适合 Zephyr 环境的代码替换 C 库中的功能。

时间函数
********

这里基于 Zephyr 的 :c:func:`sys_clock_gettime` 实现标准 C 函数 :c:func:`time`。选择 :kconfig:option:`COMMON_LIBC_TIME` 可启用该函数。

动态内存管理
************

在应用配置文件中选择 :kconfig:option:`CONFIG_COMMON_LIBC_MALLOC`，可启用公共动态内存管理实现。

公共 C 库内部使用 :ref:`内核内存堆 API <heap_v2>`，管理 :c:func:`malloc` 和 :c:func:`free` 等标准动态内存管理接口使用的堆。

内部堆通常位于 ``.bss`` 段。启用用户空间后，则放入名为 ``z_malloc_partition`` 的专用内存分区，供用户模式线程访问。内部堆大小由 :kconfig:option:`CONFIG_COMMON_LIBC_MALLOC_ARENA_SIZE` 指定。

使用公共 C 库的应用默认堆大小为零，即没有堆。对于其他 C 库用户，若存在 MMU，默认堆大小为 16kB；否则堆使用全部可用内存。

还可以分别控制 :c:func:`calloc` （:kconfig:option:`COMMON_LIBC_CALLOC`）和 :c:func:`reallocarray` （:kconfig:option:`COMMON_LIBC_REALLOCARRAY`）的启用。两者默认都启用，因为不使用它们的应用不会因此增加内存占用。

公共 C 库实现的标准动态内存管理接口是线程安全的，允许多个线程同时调用。这些函数实现于 :file:`lib/libc/common/source/stdlib/malloc.c`。
