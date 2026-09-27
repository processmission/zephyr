.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _lifos_v2:

LIFO
####

:dfn:`LIFO` 是实现传统后进先出（LIFO）队列的内核对象，允许线程和 ISR 添加或移除任意大小的数据项。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的 LIFO（仅受可用 RAM 限制）。每个 LIFO 都通过其内存地址引用。

LIFO 具有以下主要属性：

* 一个 **队列**，存放已添加但尚未移除的数据项。队列通过简单的链表实现。

LIFO 必须初始化后才能使用。初始化会将其队列置空。

LIFO 数据项必须满足指针的对齐要求，因为内核会保留数据项开头一个指针大小的字段，用于指向队列中的下一个数据项。因此，容纳 N 字节应用数据的数据项需要 N+4（或 N+8）字节内存。如果使用 :c:func:`k_lifo_alloc_put` 添加数据项，则无需满足上述对齐和预留空间要求，而是从调用线程的资源池中临时分配额外内存。

.. note::
    同一个 LIFO 数据项在所有 LIFO 数据队列中最多只能有一个在用实例。在数据项尚未从此前加入的队列中移除时，尝试将它再次加入队列会导致未定义行为。

线程或 ISR 均可向 LIFO **添加** 数据项。如果有线程正在等待，则直接将数据项交给该线程；否则将其加入 LIFO 队列。队列中的数据项数量没有上限。

线程可以从 LIFO **移除** 数据项。如果 LIFO 队列为空，线程可以选择等待数据项到来。任意数量的线程都可以同时等待一个空 LIFO。添加数据项后，它会被交给优先级最高且等待时间最长的线程。

.. note::
    内核允许 ISR 从 LIFO 移除数据项，但 LIFO 为空时，ISR 不得尝试等待。

实现
****

定义 LIFO
=========

LIFO 使用 :c:struct:`k_lifo` 类型的变量定义，随后必须调用 :c:func:`k_lifo_init` 进行初始化。

以下代码定义并初始化一个空 LIFO。

.. code-block:: c

    struct k_lifo my_lifo;

    k_lifo_init(&my_lifo);

也可以使用 :c:macro:`K_LIFO_DEFINE` 在编译时定义并初始化一个空 LIFO。

以下代码与上面的代码片段效果相同。

.. code-block:: c

    K_LIFO_DEFINE(my_lifo);

写入 LIFO
=========

调用 :c:func:`k_lifo_put` 可以向 LIFO 添加数据项。

以下代码延续上面的示例，使用 LIFO 向一个或多个消费者线程发送数据。

.. code-block:: c

    struct data_item_t {
        void *LIFO_reserved;   /* 1st word reserved for use by LIFO */
        ...
    };

    struct data_item_t tx data;

    void producer_thread(int unused1, int unused2, int unused3)
    {
        while (1) {
            /* create data item to send */
            tx_data = ...

            /* send data to consumers */
            k_lifo_put(&my_lifo, &tx_data);

            ...
        }
    }

可以使用 :c:func:`k_lifo_alloc_put` 向 LIFO 添加数据项。使用此 API 时，无需在数据项中为内核预留空间；它会从调用线程的资源池中分配额外内存，直到数据项被读取后才释放。

读取 LIFO
=========

调用 :c:func:`k_lifo_get` 可以从 LIFO 移除数据项。

以下代码延续上面的示例，使用 LIFO 从生产者线程获取数据项，然后对其进行处理。

.. code-block:: c

    void consumer_thread(int unused1, int unused2, int unused3)
    {
        struct data_item_t  *rx_data;

        while (1) {
            rx_data = k_lifo_get(&my_lifo, K_FOREVER);

            /* process LIFO data item */
            ...
        }
    }

使用建议
********

使用 LIFO 以“后进先出”的方式异步传递任意大小的数据项。

配置选项
********

相关配置选项：

* 无。

API 参考
********

.. doxygengroup:: lifo_apis
