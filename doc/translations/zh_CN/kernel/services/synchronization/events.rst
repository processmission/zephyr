.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _events:

事件
####

:dfn:`事件对象` 是实现传统事件机制的内核对象。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的事件对象（仅受可用 RAM 限制）。每个事件对象都通过其内存地址引用。一个或多个线程可以等待某个事件对象，直到所需的事件集合被递交给该对象。当新事件被递交给事件对象时，所有等待条件得到满足的线程会同时进入就绪状态。

事件对象具有以下主要属性：

* 一个 32 位值，用于记录已递交给该对象的事件。

事件对象必须初始化后才能使用。

线程或 ISR 均可 **递交** 事件。递交时，可以覆盖已有事件集合，也可以按位追加。覆盖已有事件集合称为设置（setting）；按位追加称为发布（posting）。发布和设置事件都可能满足多个等待该事件对象的线程的匹配条件。所有匹配条件得到满足的线程会同时被激活。

线程可以等待一个或多个事件，既可以等待所有请求的事件，也可以等待其中任意一个事件。此外，发起等待请求的线程可以选择在等待前重置事件对象当前记录的事件集合。当多个线程等待同一事件对象时，必须谨慎使用此选项。

.. note::
    内核允许 ISR 查询事件对象，但 ISR 不得尝试等待事件。

实现
****

定义事件对象
============

事件对象使用 :c:struct:`k_event` 类型的变量定义，随后必须调用 :c:func:`k_event_init` 进行初始化。

以下代码定义一个事件对象。

.. code-block:: c

    struct k_event my_event;

    k_event_init(&my_event);

也可以使用 :c:macro:`K_EVENT_DEFINE` 在编译时定义并初始化事件对象。

以下代码与上面的代码片段效果相同。

.. code-block:: c

    K_EVENT_DEFINE(my_event);

设置事件
========

调用 :c:func:`k_event_set` 可以设置事件对象中的事件。

以下代码延续上面的示例，将事件对象记录的事件设置为 0x001。

.. code-block:: c

    void input_available_interrupt_handler(void *arg)
    {
        /* notify threads that data is available */

        k_event_set(&my_event, 0x001);

        ...
    }

发布事件
========

调用 :c:func:`k_event_post` 可以向事件对象发布事件。

以下代码延续上面的示例，向事件对象发布一组事件。

.. code-block:: c

    void input_available_interrupt_handler(void *arg)
    {
        ...

        /* notify threads that more data is available */

        k_event_post(&my_event, 0x120);

        ...
    }

等待事件（不移除）
==================

线程通过调用 :c:func:`k_event_wait` 等待事件。

以下代码延续上面的示例，等待任意一个指定事件被发布，最长等待 50 毫秒。如果没有事件及时发布，则发出警告。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait(&my_event, 0xFFF, false, K_MSEC(50));
        if (events == 0) {
            printk("No input devices are available!");
        } else {
            /* Access the desired input device(s) */
            ...
        }
        ...
    }

如果消费者线程需要等到所有事件都发生后再继续，可以改用 :c:func:`k_event_wait_all`。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait_all(&my_event, 0x121, false, K_MSEC(50));
        if (events == 0) {
            printk("At least one input device is not available!");
        } else {
            /* Access the desired input devices */
            ...
        }
        ...
    }

等待事件（移除）
================

线程通过调用 :c:func:`k_event_wait_safe` 等待事件，并在收到事件时以原子方式移除它们。

以下代码延续上面的示例，等待任意一个指定事件被发布，最长等待 50 毫秒。如果没有事件及时发布，则发出警告。

如果及时收到事件，这些事件将从事件对象中移除，直到下一次被设置或发布。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait_safe(&my_event, 0xFFF, false, K_MSEC(50));
        if (events == 0) {
            printk("No input devices are available!");
        } else {
            /* Access the desired input device(s) */
            ...
        }
        ...
    }

如果消费者线程需要等到所有事件都发生后再继续，并在收到时以原子方式移除它们，可以改用 :c:func:`k_event_wait_all_safe`。

如果及时收到所有事件，这些事件将从事件对象中移除，直到下一次被设置或发布。

.. code-block:: c

    void consumer_thread(void)
    {
        uint32_t  events;

        events = k_event_wait_all_safe(&my_event, 0x121, false, K_MSEC(50));
        if (events == 0) {
            printk("At least one input device is not available!");
        } else {
            /* Access the desired input devices */
            ...
        }
        ...
    }

使用建议
********

使用事件表示一组条件已经成立。

使用事件一次向多个线程传递少量数据。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_EVENTS`

API 参考
********

.. doxygengroup:: event_apis
