.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _c_library_minimal:

最小 libc
#########

名为“minimal libc”的基础 C 库包含在 Zephyr 源码中，提供满足 Zephyr 及其子系统需求的最小标准 C 库子集，主要涉及字符串操作和显示。

它的占用很小，适合不依赖 ISO C 标准库中较少使用部分的项目，也可配合多种工具链使用。

最小 libc 的实现位于 Zephyr 主源码树的 :file:`lib/libc/minimal`。

函数
****

最小 libc 实现满足 Zephyr 内核需求的 ISO/IEC 9899:2011 标准 C 库函数最小子集，其范围由 :ref:`编码指南规则 A.4 <coding_guideline_libc_usage_restrictions_in_zephyr_kernel>` 定义。

格式化输出
**********

最小 libc 不自行实现格式化输出处理器，而是将 ``printf``、``sprintf`` 等标准 C 格式化输出函数映射到 :c:func:`cbprintf`，即 Zephyr 自带的兼容 C99 的格式化输出实现。

详情参阅 :ref:`格式化输出 <formatted_output>` 操作系统服务文档。

动态内存管理
************

最小 libc 使用 :ref:`公共 C 库 <c_library_common>` 提供的 malloc 系列 API 实现，后者基于 :ref:`内核内存堆 API <heap_v2>`。

错误编号
********

Zephyr API 广泛使用错误编号作为函数返回值，表示错误条件。它们通常以本节定义的整数字面量的负值返回，并定义在 :file:`errno.h` 头文件中。

最小 libc 已纳入 `POSIX errno.h specification`_ 和其他事实标准中定义的部分错误编号。

Zephyr 努力使最小 libc 的错误编号值与其支持的其他 C 标准库实现保持一致。会将最小 libc 的 :file:`errno.h` 与 :ref:`Newlib <c_library_newlib>` 对照检查，以保证错误编号一致。

下面列出错误编号定义。实际数值见 `errno.h`_。

.. doxygengroup:: system_errno

.. _`POSIX errno.h specification`: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/errno.h.html
.. _`errno.h`: https://github.com/zephyrproject-rtos/zephyr/blob/main/lib/libc/minimal/include/errno.h
