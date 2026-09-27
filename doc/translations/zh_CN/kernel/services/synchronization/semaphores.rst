.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _semaphores_v2:

信号量
######

:dfn:`信号量` 是实现传统计数信号量的内核对象。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的信号量（仅受可用 RAM 限制）。每个信号量都通过其内存地址引用。

信号量具有以下主要属性：

* **计数**，表示可以获取该信号量的次数。计数为零表示信号量不可用。

* **上限**，表示信号量计数可以达到的最大值。

信号量必须初始化后才能使用。其计数必须设为非负值，且不大于上限。

线程或 ISR 均可 **释放** 信号量。释放信号量会使其计数加一，除非计数已经达到上限。

线程可以 **获取** 信号量。获取信号量会使其计数减一，除非信号量不可用（即计数为零）。信号量不可用时，线程可以选择等待它被释放。任意数量的线程都可以同时等待一个不可用的信号量。信号量被释放后，将由优先级最高且等待时间最长的线程获取。

.. note::
    可以将信号量初始化为“满”状态（计数等于上限），以限制能够同时执行临界区的线程数。也可以将信号量初始化为空（计数为 0，上限大于 0），使所有等待线程都必须等到信号量计数增加后才能通过。常见信号量的所有标准用法均受支持。

.. note::
    内核允许 ISR 获取信号量，但信号量不可用时，ISR 不得尝试等待。

实现
****

定义信号量
==========

信号量使用 :c:struct:`k_sem` 类型的变量定义，随后必须调用 :c:func:`k_sem_init` 进行初始化。

以下代码定义一个信号量，并将计数设为 0、上限设为 1，使其成为二值信号量。

.. code-block:: c

    struct k_sem my_sem;

    k_sem_init(&my_sem, 0, 1);

也可以使用 :c:macro:`K_SEM_DEFINE` 在编译时定义并初始化信号量。

以下代码与上面的代码片段效果相同。

.. code-block:: c

    K_SEM_DEFINE(my_sem, 0, 1);

释放信号量
==========

调用 :c:func:`k_sem_give` 可以释放信号量。

以下代码延续上面的示例，释放信号量，表示已有一份数据可供消费者线程处理。

.. code-block:: c

    void input_data_interrupt_handler(void *arg)
    {
        /* notify thread that data is available */
        k_sem_give(&my_sem);

        ...
    }

获取信号量
==========

调用 :c:func:`k_sem_take` 可以获取信号量。

以下代码延续上面的示例，等待信号量被释放，最长等待 50 毫秒。如果未能及时获取信号量，则发出警告。

.. code-block:: c

    void consumer_thread(void)
    {
        ...

        if (k_sem_take(&my_sem, K_MSEC(50)) != 0) {
            printk("Input data not available!");
        } else {
            /* fetch available data */
            ...
        }
        ...
    }

使用建议
********

使用信号量控制多个线程对一组资源的访问。

使用信号量在生产者和消费者线程或 ISR 之间同步处理过程。

配置选项
********

相关配置选项：

* 无。

API 参考
********

.. doxygengroup:: semaphore_apis

用户模式信号量 API 参考
***********************

:c:struct:`sys_sem` 位于用户内存中，启用用户模式时，它为用户模式线程提供计数信号量功能。未启用用户模式时，:c:struct:`sys_sem` 的行为与 :c:struct:`k_sem` 相同。

.. doxygengroup:: user_semaphore_apis
