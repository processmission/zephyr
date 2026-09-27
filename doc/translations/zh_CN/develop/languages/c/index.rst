.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _language_c:

C 语言支持
##########

C 是一种通用的底层编程语言，广泛用于嵌入式系统编程。

Zephyr 主要用 C 编写，原生支持 C 语言应用。所有 Zephyr API 函数和宏都以 C 实现，并通过 :file:`include` 目录中的 C 头文件提供，因此使用 C 编写 Zephyr 应用可以使用最完整的功能。

Zephyr 应用在 C 标准定义的“宿主”环境中运行，因此 ``main()`` 函数的返回类型必须为 ``int``。应用必须从 main 返回零（0），所有非零返回值均为保留值。

.. _c_standards:

语言标准
********

Zephyr 不以某个特定 C 标准版本为目标，但源码广泛使用 1999 年 ISO C 标准（ISO/IEC 9899:1999，下称 C99）引入的功能，例如下列功能，因此实际上要求编译器工具链至少支持 C99：

* 内联函数
* 标准布尔类型（``<stdbool.h>`` 中的 ``bool``）
* 固定宽度整数类型（``<stdint.h>`` 中的 ``[u]intN_t``）
* 指定初始化器
* 可变参数宏
* ``restrict`` 限定符

此外，某些组件或其部分代码使用 C11 和 C17 标准（分别为 ISO/IEC 9899:2011 和 9899:2018）引入的功能：

* _Generic 关键字
* _Static_assert 关键字

因此，建议使用至少支持 C17 的编译器工具链开发 Zephyr。但需注意，某些可选组件和外部模块可能使用更新 C 标准引入的语言功能，此时必须使用支持这些标准的更新工具链。

.. _c_library:

标准库
******

`C Standard Library`_ （C 标准库）是任何 C 程序不可或缺的一部分。Zephyr 支持多种 C 库，应用可以根据构建时使用的编译器工具链选择。

.. toctree::
   :maxdepth: 2

   common_libc.rst
   minimal_libc.rst
   newlib.rst
   picolibc.rst

.. _`C Standard Library`: https://en.wikipedia.org/wiki/C_standard_library

.. _c_library_formatted_output:

格式化输出
**********

C 定义了 ``printf``、``sprintf`` 等标准格式化输出函数，由 C 标准库实现。

各 C 标准库对格式化输出模式和功能的选择有不同的要求和配置，详情请参阅对应库的文档。

.. _c_library_dynamic_mem:

动态内存管理
************

C 定义了标准动态内存管理接口，例如 :c:func:`malloc` 和 :c:func:`free`，由 C 标准库实现。

各 C 标准库的动态内存管理实现细节有所不同，但所有受支持的库都必须遵循以下约定：

* 在内部自行管理堆，或通过调用 :file:`libc-hooks.c` 中实现的钩子函数（例如 :c:func:`sbrk`）管理。

* 通过标准动态内存分配接口（例如 :c:func:`malloc`）分配的块，必须满足架构和内存区域特定的对齐要求。

* 启用用户空间时，在 ``z_malloc_partition`` 内存分区内分配内存块。参见 :ref:`memory_domain_predefined_partitions`。

各 C 标准库内存管理实现的详细信息，请参阅对应库的文档。

.. note::
   原生 Zephyr 应用应使用 Zephyr 内核支持的 :ref:`内存管理 API <memory_management_api>`，例如 :c:func:`k_malloc`，以利用其高级功能。

   :c:func:`malloc` 等标准 C 动态内存管理接口，应仅供面向多个操作系统的可移植应用和库使用。
