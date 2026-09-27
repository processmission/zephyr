.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _c_library_newlib:

Newlib
######

`Newlib`_ 是面向嵌入式系统的完整 C 库实现，属于独立开源项目，Zephyr 不包含其源代码。:ref:`toolchain_zephyr_sdk` 则为每种受支持的架构提供预编译库（:file:`libc.a` 和 :file:`libm.a`）。

.. note::
   :ref:`toolchain_gnuarmemb` 等第三方工具链也附带预编译形式的 Newlib。

Zephyr 实现了由 Newlib 标准 C 库函数调用的“API 钩子”函数。这些函数位于 :file:`lib/libc/newlib/libc-hooks.c`，将库内部系统调用转换为等效的 Zephyr API 调用。

Newlib 类型
***********

:ref:`toolchain_zephyr_sdk` 中的 Newlib 有 full（完整）和 nano（精简）两个变体。

完整 Newlib
===========

Newlib 完整变体（:file:`libc.a` 和 :file:`libm.a`）是 Zephyr SDK 中功能最齐全的 Newlib 变体，支持几乎所有标准 C 库功能。它优先优化性能而非代码体积，因此占用显著大于 nano 变体。

在应用配置文件中选择 :kconfig:option:`CONFIG_NEWLIB_LIBC`，并取消选择 :kconfig:option:`CONFIG_NEWLIB_LIBC_NANO`，即可启用此变体。

精简 Newlib
===========

Newlib nano 变体（:file:`libc_nano.a` 和 :file:`libm_nano.a`）针对体积优化，支持完整变体的全部功能，但不支持 C99 新增的格式说明符，例如 ``char`` 和 ``long long`` 类型的格式说明符，即 ``%hhX`` 和 ``%llX``。

在应用配置文件中选择 :kconfig:option:`CONFIG_NEWLIB_LIBC` 和 :kconfig:option:`CONFIG_NEWLIB_LIBC_NANO`，即可启用此变体。

注意，并非所有架构都提供 Newlib nano 变体。是否可用由 :kconfig:option:`CONFIG_HAS_NEWLIB_LIBC_NANO` 指定。

.. _`Newlib`: https://sourceware.org/newlib/

格式化输出
**********

Newlib 支持所有标准 C 格式化输入输出函数，包括 ``printf``、``fprintf``、``sprintf`` 和 ``sscanf``。

Newlib 格式化输入输出实现支持 C 标准定义的所有格式说明符，但有以下例外：

* 浮点格式说明符（例如 ``%f``）要求启用 :kconfig:option:`CONFIG_NEWLIB_LIBC_FLOAT_PRINTF` 和 :kconfig:option:`CONFIG_NEWLIB_LIBC_FLOAT_SCANF`。
* Newlib nano 变体不支持 C99 格式说明符，即 ``char`` 的 ``%hhX``、``long long`` 的 ``%llX``、``intmax_t`` 的 ``%jX``、``size_t`` 的 ``%zX`` 和 ``ptrdiff_t`` 的 ``%tX``。

动态内存管理
************

Newlib 实现了内部堆分配器，用于管理标准动态内存管理接口（例如 :c:func:`malloc` 和 :c:func:`free`）使用的内存块。

不同 Newlib 类型的内部堆分配器可能不同。例如，Zephyr SDK 的完整 Newlib（:file:`libc.a` 和 :file:`libm.a`）向操作系统请求更大的内存块，其最低内存需求显著高于精简 Newlib（:file:`libc_nano.a` 和 :file:`libm_nano.a`）。

Newlib 动态内存管理函数与 Zephyr 侧 libc 钩子之间的唯一接口是 :c:func:`sbrk`，Newlib 通过它管理为内部堆分配器保留的内存池大小。

Newlib 的内存池大小变更请求由 :c:func:`_sbrk` 钩子处理（实现于 :file:`libc-hooks.c`），该钩子在系统内存不足时返回错误，确保内部堆分配器的内存池不超出可用空间。

启用用户空间时，Newlib 内部堆分配器的内存池放在名为 ``z_malloc_partition`` 的专用内存分区中，供用户模式线程访问。

Newlib 堆的可用内存空间取决于系统配置：

* 启用 MMU（选择 :kconfig:option:`CONFIG_MMU`）时，Newlib 堆的保留空间取 :c:func:`k_mem_free_get` 返回的空闲内存大小与 :kconfig:option:`CONFIG_NEWLIB_LIBC_MAX_MAPPED_REGION_SIZE` 两者中的较小值。

* 启用 MPU，且 MPU 要求分区大小和地址对齐均为 2 的幂（:kconfig:option:`CONFIG_NEWLIB_LIBC_ALIGNED_HEAP_SIZE` 为非零值）时，Newlib 堆的保留空间由 :kconfig:option:`CONFIG_NEWLIB_LIBC_ALIGNED_HEAP_SIZE` 指定。

* 否则，Newlib 堆的保留空间等于 SRAM 区域中空闲、尚未分配的内存大小。

Newlib 实现的标准动态内存管理接口是线程安全的，允许多个线程同时调用。
