.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _atomic_v2:

原子服务
########

:dfn:`原子变量` 是线程和 ISR 能够以不可中断的方式读取和修改的变量。在 32 位机器上它是 32 位变量，在 64 位机器上则是 64 位变量。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的原子变量（仅受可用 RAM 的限制）。

使用内核的原子 API 操作原子变量，可以保证所需操作正确执行，即使更高优先级的上下文也在操作同一个变量。

内核还支持对原子变量数组中的单个位进行原子操作。

实现
****

定义原子变量
============

使用 :c:type:`atomic_t` 类型的变量来定义原子变量。

默认情况下，原子变量初始化为零。不过，也可以使用 :c:macro:`ATOMIC_INIT` 将其初始化为其他值：

.. code-block:: c

    atomic_t flags = ATOMIC_INIT(0xFF);

操作原子变量
============

通过本节末尾列出的 API 来操作原子变量。

以下代码展示如何使用原子变量记录函数的调用次数。由于计数以原子方式递增，即使调用函数的线程被同样调用该函数的更高优先级上下文中断，也不会在递增过程中破坏计数值。

.. code-block:: c

    atomic_t call_count;

    int call_counting_routine(void)
    {
        /* increment invocation counter */
        atomic_inc(&call_count);

        /* do rest of routine's processing */
        ...
    }

操作原子变量数组
================

可以按常规方式定义 32 位原子变量数组，也可以使用 :c:macro:`ATOMIC_DEFINE` 定义由原子变量构成的 N 位数组。

可以使用本节末尾列出的、以 :c:func:`_bit` 结尾的 API 操作原子变量数组中的单个位。

以下代码展示如何使用原子变量数组实现一组 200 个标志位。

.. code-block:: c

    #define NUM_FLAG_BITS 200

    ATOMIC_DEFINE(flag_bits, NUM_FLAG_BITS);

    /* set specified flag bit & return its previous value */
    int set_flag_bit(int bit_position)
    {
        return (int)atomic_set_bit(flag_bits, bit_position);
    }

内存顺序
========

为保证一致性和正确性，当硬件有此需要时，所有 Zephyr 原子 API 都应包含完整的内存屏障，以确保不同上下文看到一致可靠的状态。这里的完整内存屏障类似于 x86 上的“串行化”指令、ARM 上的“DMB”，或 C++ 内存模型定义的“顺序一致”操作。各架构专用实现负责保证这一行为。

使用建议
********

使用原子变量实现只需操作单个 32 位值的临界区处理。

使用多个原子变量，对长度超过 32 位的位数组中的一组标志位实现临界区处理。

.. note::
    使用原子变量通常比互斥锁或锁定中断等其他临界区实现方式高效得多。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_BUILTIN`
* :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_ARCH`
* :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_C`

API 参考
********

.. important::
    所有原子服务 API 均可在线程和 ISR 中使用。

.. doxygengroup:: atomic_apis
