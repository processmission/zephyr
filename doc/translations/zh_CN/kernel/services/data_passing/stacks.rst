.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _stacks_v2:

栈
###

:dfn:`栈` 是实现传统后进先出（LIFO）队列的内核对象，允许线程和 ISR 添加或移除有限数量的整数数据值。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的栈（仅受可用 RAM 限制）。每个栈都通过其内存地址引用。

栈具有以下主要属性：

* 一个 **队列**，存放已添加但尚未移除的整数数据值。队列使用 stack_data_t 类型的数组实现，必须按本机字边界对齐。stack_data_t 类型的大小与本机字长相同，即根据 CPU 架构和编译模式为 32 位或 64 位。

* 数组中可存放数据值的 **最大数量**。

栈必须初始化后才能使用。初始化会将其队列置空。

线程或 ISR 均可向栈 **添加** 数据值。如果有线程正在等待，则直接将数据值交给该线程；否则将其加入 LIFO 队列。

.. note::
    如果启用了 :kconfig:option:`CONFIG_NO_RUNTIME_CHECKS`，内核 *不会* 检测和阻止向已达到容量上限的栈添加数据值的尝试。向已满的栈添加数据值会导致数组溢出，进而产生不可预测的行为。

线程可以从栈 **移除** 数据值。如果栈的队列为空，线程可以选择等待数据值到来。任意数量的线程都可以同时等待一个空栈。添加数据项后，它会被交给优先级最高且等待时间最长的线程。

.. note::
    内核允许 ISR 从栈移除数据项，但栈为空时，ISR 不得尝试等待。

实现
****

定义栈
======

栈使用 :c:struct:`k_stack` 类型的变量定义，随后必须调用 :c:func:`k_stack_init` 或 :c:func:`k_stack_alloc_init` 进行初始化。使用后者时无需提供缓冲区，缓冲区会从调用线程的资源池中分配。

以下代码定义并初始化一个空栈，最多可容纳十个字大小的数据值。

.. code-block:: c

    #define MAX_ITEMS 10

    stack_data_t my_stack_array[MAX_ITEMS];
    struct k_stack my_stack;

    k_stack_init(&my_stack, my_stack_array, MAX_ITEMS);

也可以使用 :c:macro:`K_STACK_DEFINE` 在编译时定义并初始化栈。

以下代码与上面的代码片段效果相同。注意，该宏同时定义了栈及其数据值数组。

.. code-block:: c

    K_STACK_DEFINE(my_stack, MAX_ITEMS);

入栈
====

调用 :c:func:`k_stack_push` 可以向栈添加数据项。

以下代码延续上面的示例，展示线程如何将数据结构的内存地址保存在栈中，从而创建数据结构池。

.. code-block:: c

    /* define array of data structures */
    struct my_buffer_type {
        int field1;
        ...
        };
    struct my_buffer_type my_buffers[MAX_ITEMS];

    /* save address of each data structure in a stack */
    for (int i = 0; i < MAX_ITEMS; i++) {
        k_stack_push(&my_stack, (stack_data_t)&my_buffers[i]);
    }

出栈
====

调用 :c:func:`k_stack_pop` 可以从栈取出数据项。

以下代码延续上面的示例，展示线程如何动态分配一个尚未使用的数据结构。当不再需要该数据结构时，线程必须将其地址重新压入栈，以便复用。

.. code-block:: c

    struct my_buffer_type *new_buffer;

    k_stack_pop(&buffer_stack, (stack_data_t *)&new_buffer, K_FOREVER);
    new_buffer->field1 = ...

使用建议
********

如果已知最多需要存储多少个数据项，可以使用栈以“后进先出”的方式存取整数数据值。

配置选项
********

相关配置选项：

* 无。

API 参考
********

.. doxygengroup:: stack_apis
