.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _message_queues_v2:

消息队列
########

:dfn:`消息队列` 是实现简单消息队列的内核对象，允许线程和 ISR 异步发送和接收固定大小的数据项。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的消息队列（仅受可用 RAM 限制）。每个消息队列都通过其内存地址引用。

消息队列具有以下主要属性：

* 一个 **环形缓冲区**，存放已发送但尚未接收的数据项。

* **数据项大小**，以字节为单位。

* 环形缓冲区可排队存放数据项的 **最大数量**。

消息队列必须初始化后才能使用。初始化会将其环形缓冲区置空。

线程或 ISR 均可向消息队列 **发送** 数据项。如果有线程正在等待，则将发送线程所指向的数据项复制给该线程；否则，在有可用空间时将数据项复制到消息队列的环形缓冲区。无论哪种情况，发送的数据区域大小都 *必须* 等于消息队列的数据项大小。

如果线程在环形缓冲区已满时尝试发送数据项，它可以选择等待可用空间。环形缓冲区已满时，任意数量的发送线程都可以同时等待；空间可用后，会优先交给优先级最高且等待时间最长的发送线程。

线程可以从消息队列 **接收** 数据项。数据项会被复制到接收线程指定的区域；接收区域大小 *必须* 等于消息队列的数据项大小。

如果线程在环形缓冲区为空时尝试接收数据项，它可以选择等待数据项到来。环形缓冲区为空时，任意数量的接收线程都可以同时等待；数据项可用后，会被交给优先级最高且等待时间最长的接收线程。

线程还可以 **窥视** 消息队列头部的消息，而不将其移出队列。数据项会被复制到接收线程指定的区域；接收区域大小 *必须* 等于消息队列的数据项大小。

.. note::
    内核允许 ISR 从消息队列接收数据项，但消息队列为空时，ISR 不得尝试等待。

.. note::
    消息队列的环形缓冲区无需对齐。底层实现使用与对齐无关的 :c:func:`memcpy`，也不暴露任何内部指针。

实现
****

定义消息队列
============

消息队列使用 :c:struct:`k_msgq` 类型的变量定义，随后必须调用 :c:func:`k_msgq_init` 进行初始化。

以下代码定义并初始化一个空消息队列，最多可容纳 10 个数据项，每项长 12 字节。

.. code-block:: c

    struct data_item_type {
        uint32_t field1;
        uint32_t field2;
        uint32_t field3;
    };

    char my_msgq_buffer[10 * sizeof(struct data_item_type)];
    struct k_msgq my_msgq;

    k_msgq_init(&my_msgq, my_msgq_buffer, sizeof(struct data_item_type), 10);

也可以使用以下宏之一，在编译时定义并初始化消息队列：

* :c:macro:`K_MSGQ_DEFINE` —— 定义公共消息队列。
* :c:macro:`K_MSGQ_DEFINE_STATIC` —— 定义私有（静态作用域）消息队列。
* :c:macro:`K_MSGQ_DEFINE_TYPE` —— 为指定的数据项类型定义公共消息队列。
* :c:macro:`K_MSGQ_DEFINE_STATIC_TYPE` —— 为指定的数据项类型定义私有消息队列。

以下代码与上面的代码片段效果相同。注意，该宏同时定义了消息队列及其缓冲区。

.. code-block:: c

    K_MSGQ_DEFINE(my_msgq, sizeof(struct data_item_type), 10, 1);

如果在编译时已知队列的数据项类型，可以使用简化宏 :c:macro:`K_MSGQ_DEFINE_TYPE`。该宏会自动配置队列的数据项大小和对齐方式：

.. code-block:: c

    K_MSGQ_DEFINE_TYPE(my_msgq, struct data_item_type, 10);

写入消息队列
============

调用 :c:func:`k_msgq_put` 可以向消息队列添加数据项。

以下代码延续上面的示例，使用消息队列将数据项从生产者线程传给一个或多个消费者线程。如果消费者处理不及导致消息队列已满，生产者线程会丢弃队列中的所有已有数据，以便保存较新的数据。注意，此 API 会触发重新调度。

.. code-block:: c

    void producer_thread(void)
    {
        struct data_item_type data;

        while (1) {
            /* create data item to send (e.g. measurement, timestamp, ...) */
            data = ...

            /* send data to consumers */
            while (k_msgq_put(&my_msgq, &data, K_NO_WAIT) != 0) {
                /* message queue is full: purge old data & try again */
                k_msgq_purge(&my_msgq);
            }

            /* data item was successfully added to message queue */
        }
    }

读取消息队列
============

调用 :c:func:`k_msgq_get` 可以从消息队列取出数据项。

以下代码延续上面的示例，使用消息队列处理一个或多个生产者线程生成的数据项。注意，应检查 :c:func:`k_msgq_get` 的返回值，因为调用 :c:func:`k_msgq_purge` 可能使其返回 ``-ENOMSG``。

.. code-block:: c

    void consumer_thread(void)
    {
        struct data_item_type data;

        while (1) {
            /* get a data item */
            k_msgq_get(&my_msgq, &data, K_FOREVER);

            /* process data item */
            ...
        }
    }


窥视消息队列
============

调用 :c:func:`k_msgq_peek` 可以读取消息队列中的数据项。

以下代码窥视消息队列，读取由一个或多个生产者线程生成、位于队列头部的数据项。

.. code-block:: c

    void consumer_thread(void)
    {
        struct data_item_type data;

        while (1) {
            /* read a data item by peeking into the queue */
            k_msgq_peek(&my_msgq, &data);

            /* process data item */
            ...
        }
    }

使用建议
********

使用消息队列在线程之间异步传递小数据项。

.. note::
    必要时，消息队列也可以传递大数据项。不过，这可能增加中断延迟，因为读写数据项时会锁定中断。由于需要将整个数据项复制到内存缓冲区或从中复制出来，读写耗时会随数据项大小线性增长。因此，传递大数据项时，通常更适合交换指向它的指针，而非传递数据项本身。

    使用内核的邮箱对象可以实现同步传输。

配置选项
********

相关配置选项：

* 无。

API 参考
********

.. doxygengroup:: msgq_apis
