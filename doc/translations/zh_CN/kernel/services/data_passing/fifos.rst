.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _fifos_v2:

FIFO
####

:dfn:`FIFO` 是实现传统先进先出（FIFO）队列的内核对象，允许线程和 ISR 添加或移除任意大小的数据项。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的 FIFO（仅受可用 RAM 限制）。每个 FIFO 都通过其内存地址引用。

FIFO 具有以下主要属性：

* 一个 **队列**，存放已添加但尚未移除的数据项。队列通过简单的链表实现。

FIFO 必须初始化后才能使用。初始化会将其队列置空。

FIFO 数据项必须满足指针的对齐要求，因为内核会保留数据项开头一个指针大小的字段，用于指向队列中的下一个数据项。因此，容纳 N 字节应用数据的数据项需要 N+4（或 N+8）字节内存。如果使用 :c:func:`k_fifo_alloc_put` 添加数据项，则无需满足上述对齐和预留空间要求，而是从调用线程的资源池中临时分配额外内存。

.. note::
    同一个 FIFO 数据项在所有 FIFO 数据队列中最多只能有一个在用实例。在数据项尚未从此前加入的队列中移除时，尝试将它再次加入队列会导致未定义行为。

线程或 ISR 均可向 FIFO **添加** 数据项。如果有线程正在等待，则直接将数据项交给该线程；否则将其加入 FIFO 队列。队列中的数据项数量没有上限。

线程可以从 FIFO **移除** 数据项。如果 FIFO 队列为空，线程可以选择等待数据项到来。任意数量的线程都可以同时等待一个空 FIFO。添加数据项后，它会被交给优先级最高且等待时间最长的线程。

.. note::
    内核允许 ISR 从 FIFO 移除数据项，但 FIFO 为空时，ISR 不得尝试等待。

如果将 **多个数据项** 串成单链表，就可以通过一次操作将它们加入 FIFO。当多个写入者向 FIFO 添加成组的相关数据项时，这一能力很有用，能够确保每组数据项不会与其他数据项交错。一次添加多个数据项也比逐个添加更高效，并可保证取出一组中首个数据项的执行者无需等待即可取出其余数据项。

实现
****

定义 FIFO
=========

FIFO 使用 :c:struct:`k_fifo` 类型的变量定义，随后必须调用 :c:func:`k_fifo_init` 进行初始化。

以下代码定义并初始化一个空 FIFO。

.. code-block:: c

    struct k_fifo my_fifo;

    k_fifo_init(&my_fifo);

也可以使用 :c:macro:`K_FIFO_DEFINE` 在编译时定义并初始化一个空 FIFO。

以下代码与上面的代码片段效果相同。

.. code-block:: c

    K_FIFO_DEFINE(my_fifo);

写入 FIFO
=========

调用 :c:func:`k_fifo_put` 可以向 FIFO 添加数据项。

以下代码延续上面的示例，使用 FIFO 向一个或多个消费者线程发送数据。

.. code-block:: c

    struct data_item_t {
        void *fifo_reserved;   /* 1st word reserved for use by FIFO */
        ...
    };

    struct data_item_t tx_data;

    void producer_thread(int unused1, int unused2, int unused3)
    {
        while (1) {
            /* create data item to send */
            tx_data = ...

            /* send data to consumers */
            k_fifo_put(&my_fifo, &tx_data);

            ...
        }
    }

此外，可以调用 :c:func:`k_fifo_put_list` 或 :c:func:`k_fifo_put_slist`，将由数据项组成的单链表加入 FIFO。

最后，也可以使用 :c:func:`k_fifo_alloc_put` 向 FIFO 添加数据项。使用此 API 时，无需在数据项中为内核预留空间；它会从调用线程的资源池中分配额外内存，直到数据项被读取后才释放。

读取 FIFO
=========

调用 :c:func:`k_fifo_get` 可以从 FIFO 移除数据项。

以下代码延续上面的示例，使用 FIFO 从生产者线程获取数据项，然后对其进行处理。

.. code-block:: c

    void consumer_thread(int unused1, int unused2, int unused3)
    {
        struct data_item_t  *rx_data;

        while (1) {
            rx_data = k_fifo_get(&my_fifo, K_FOREVER);

            /* process FIFO data item */
            ...
        }
    }

使用建议
********

使用 FIFO 以“先进先出”的方式异步传递任意大小的数据项。

配置选项
********

相关配置选项：

* 无

API 参考
********

.. doxygengroup:: fifo_apis
