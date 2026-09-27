.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _polling_v2:

轮询 API
########

轮询 API 用于同时等待多个条件中的任意一个得到满足。

.. contents::
    :local:
    :depth: 2

概念
****

轮询 API 的主要函数是 :c:func:`k_poll`。它在概念上与 POSIX 的 :c:func:`poll` 函数非常相似，但操作的是内核对象，而不是文件描述符。

轮询 API 允许单个线程同时等待一个或多个条件满足，无需逐个主动检查。

支持的条件种类有限：

- 信号量变为可用
- 内核 FIFO 中有可读取的数据
- 内核 LIFO 中有可读取的数据
- 内核消息队列中有可读取的数据
- 内核管道中有可读取的数据
- 轮询信号被触发

需要等待多个条件的线程必须定义一个 **轮询事件** 数组，每个条件对应一个事件。

轮询数组之前，必须初始化数组中的所有事件。

每个事件必须指定待满足条件的 **类型**，以便通过改变状态来表示请求的条件已满足。

每个事件必须指定希望其条件得到满足的 **内核对象**。

每个事件必须指定条件满足时使用的操作 **模式**。

每个事件还可根据用户需要指定一个 **标签**，用于将多个事件分组。

除内核对象外，还有一种 **轮询信号** 伪对象类型，可以直接向其发出信号。

:c:func:`k_poll` 等待的任意一个条件满足后，函数就会返回。由于条件可能在调用 :c:func:`k_poll` 之前就已满足，或者由于内核具有抢占式多线程特性，:c:func:`k_poll` 返回时可能已有多个条件满足。调用者必须检查数组中所有轮询事件的状态，确定哪些条件已满足以及应采取什么操作。

目前只有一种操作模式：不获取对象。例如，:c:func:`k_poll` 返回且轮询事件状态表示信号量可用时，:c:func:`k_poll()` 的调用者还必须调用 :c:func:`k_sem_take` 获取信号量。如果存在对该信号量的竞争，则不能保证调用 :c:func:`k_sem_take` 时它仍然可用。

实现
****

使用 k_poll()
=============

主要 API 是 :c:func:`k_poll`，它操作由 :c:struct:`k_poll_event` 类型组成的轮询事件数组。数组中的每个元素表示一个带有条件的事件，调用 :c:func:`k_poll` 会等待其中的条件得到满足。

轮询事件可以使用运行时初始化器 :c:macro:`K_POLL_EVENT_INITIALIZER()` 或 :c:func:`k_poll_event_init`，也可以使用静态初始化器 :c:macro:`K_POLL_EVENT_STATIC_INITIALIZER()` 初始化。必须向初始化器传入与指定 **类型** 匹配的对象。**模式** *必须* 设置为 :c:enumerator:`K_POLL_MODE_NOTIFY_ONLY`。状态 *必须* 设置为 :c:macro:`K_POLL_STATE_NOT_READY` （初始化器会完成此操作）。用户 **标签** 是可选的，API 完全不解释其含义：它用于帮助用户将相似事件分组。由于标签是可选的，出于性能考虑，只有静态初始化器接受它，运行时初始化器不接受。使用运行时初始化器时，用户必须在 :c:struct:`k_poll_event` 数据结构中单独设置标签。如果需要忽略数组中的某个事件（通常是临时忽略），可以将其类型设置为 :c:macro:`K_POLL_TYPE_IGNORE`。

.. code-block:: c

    struct k_poll_event events[4] = {
        K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_SEM_AVAILABLE,
                                        K_POLL_MODE_NOTIFY_ONLY,
                                        &my_sem, 0),
        K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_FIFO_DATA_AVAILABLE,
                                        K_POLL_MODE_NOTIFY_ONLY,
                                        &my_fifo, 0),
        K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_MSGQ_DATA_AVAILABLE,
                                        K_POLL_MODE_NOTIFY_ONLY,
                                        &my_msgq, 0),
        K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_PIPE_DATA_AVAILABLE,
                                        K_POLL_MODE_NOTIFY_ONLY,
                                        &my_pipe, 0),
    };

或在运行时初始化

.. code-block:: c

    struct k_poll_event events[4];
    void some_init(void)
    {
        k_poll_event_init(&events[0],
                          K_POLL_TYPE_SEM_AVAILABLE,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &my_sem);

        k_poll_event_init(&events[1],
                          K_POLL_TYPE_FIFO_DATA_AVAILABLE,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &my_fifo);

        k_poll_event_init(&events[2],
                          K_POLL_TYPE_MSGQ_DATA_AVAILABLE,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &my_msgq);

        k_poll_event_init(&events[3],
                          K_POLL_TYPE_PIPE_DATA_AVAILABLE,
                          K_POLL_MODE_NOTIFY_ONLY,
                          &my_pipe);

        // tags are left uninitialized if unused
    }


事件初始化后，可将数组传递给 :c:func:`k_poll`。可以指定超时，仅等待指定时长；也可以使用特殊值 :c:macro:`K_NO_WAIT` 和 :c:macro:`K_FOREVER`，分别表示不等待，或一直等待到某个事件条件满足才返回。

每个信号量或 FIFO 都提供一个轮询等待者列表，应用程序可以按需让任意数量的事件在其中等待。请注意，等待者按先到先服务的顺序处理，而不是按优先级顺序。

成功时，:c:func:`k_poll` 返回 0。超时时，返回 -:c:macro:`EAGAIN`。

.. code-block:: c

    // assume there is no contention on this semaphore and FIFO
    // -EADDRINUSE will not occur; the semaphore and/or data will be available

    void do_stuff(void)
    {
        rc = k_poll(events, ARRAY_SIZE(events), K_MSEC(1000));
        if (rc == 0) {
            if (events[0].state == K_POLL_STATE_SEM_AVAILABLE) {
                k_sem_take(events[0].sem, 0);
            } else if (events[1].state == K_POLL_STATE_FIFO_DATA_AVAILABLE) {
                data = k_fifo_get(events[1].fifo, 0);
                // handle data
            } else if (events[2].state == K_POLL_STATE_MSGQ_DATA_AVAILABLE) {
                ret = k_msgq_get(events[2].msgq, buf, K_NO_WAIT);
                // handle data
            } else if (events[3].state == K_POLL_STATE_PIPE_DATA_AVAILABLE) {
                bytes_read = k_pipe_read(events[3].pipe, buf, bytes_to_read, K_NO_WAIT);
                // handle data
            }
        } else {
            // handle timeout
        }
    }

在循环中调用 :c:func:`k_poll` 时，用户必须将事件状态重置为 :c:macro:`K_POLL_STATE_NOT_READY`。

.. code-block:: c

    void do_stuff(void)
    {
        for(;;) {
            rc = k_poll(events, ARRAY_SIZE(events), K_FOREVER);
            if (events[0].state == K_POLL_STATE_SEM_AVAILABLE) {
                k_sem_take(events[0].sem, 0);
            }
            if (events[1].state == K_POLL_STATE_FIFO_DATA_AVAILABLE) {
                data = k_fifo_get(events[1].fifo, 0);
                // handle data
            }
            if (events[2].state == K_POLL_STATE_MSGQ_DATA_AVAILABLE) {
                ret = k_msgq_get(events[2].msgq, buf, K_NO_WAIT);
                // handle data
            }
            if (events[3].state == K_POLL_STATE_PIPE_DATA_AVAILABLE) {
                bytes_read = k_pipe_read(events[3].pipe, buf, bytes_to_read, K_NO_WAIT);
                // handle data
            }
            events[0].state = K_POLL_STATE_NOT_READY;
            events[1].state = K_POLL_STATE_NOT_READY;
            events[2].state = K_POLL_STATE_NOT_READY;
            events[3].state = K_POLL_STATE_NOT_READY;
        }
    }

使用 k_poll_signal_raise()
==========================

其中一种事件类型是 :c:macro:`K_POLL_TYPE_SIGNAL`，它是直接发给轮询事件的信号。可以将其视为一种只允许一个线程等待的轻量级二值信号量。

轮询信号是一个独立的 :c:struct:`k_poll_signal` 类型对象，与信号量或 FIFO 类似，必须关联到一个 k_poll_event。首先必须通过 :c:macro:`K_POLL_SIGNAL_INITIALIZER()` 或 :c:func:`k_poll_signal_init` 对其初始化。

.. code-block:: c

    struct k_poll_signal signal;
    void do_stuff(void)
    {
        k_poll_signal_init(&signal);
    }

通过 :c:func:`k_poll_signal_raise` 函数触发信号。该函数接受一个用户 **结果** 参数，API 不解释其含义，可用它向等待事件的线程传递额外信息。

.. code-block:: c

    struct k_poll_signal signal;

    // thread A
    void do_stuff(void)
    {
        k_poll_signal_init(&signal);

        struct k_poll_event events[1] = {
            K_POLL_EVENT_INITIALIZER(K_POLL_TYPE_SIGNAL,
                                     K_POLL_MODE_NOTIFY_ONLY,
                                     &signal),
        };

        k_poll(events, 1, K_FOREVER);

        int signaled, result;

        k_poll_signal_check(&signal, &signaled, &result);

        if (signaled && (result == 0x1337)) {
            // A-OK!
        } else {
            // weird error
        }
    }

    // thread B
    void signal_do_stuff(void)
    {
        k_poll_signal_raise(&signal, 0x1337);
    }

如果在循环中轮询信号，则每次迭代中，若信号已触发，*既要* 将事件状态重置为 :c:macro:`K_POLL_STATE_NOT_READY`，*也要* 使用 :c:func:`k_poll_signal_reset()` 重置其 ``result``。

.. code-block:: c

    struct k_poll_signal signal;
    void do_stuff(void)
    {
        k_poll_signal_init(&signal);

        struct k_poll_event events[1] = {
            K_POLL_EVENT_INITIALIZER(K_POLL_TYPE_SIGNAL,
                                     K_POLL_MODE_NOTIFY_ONLY,
                                     &signal),
        };

        for (;;) {
            k_poll(events, 1, K_FOREVER);

            int signaled, result;

            k_poll_signal_check(&signal, &signaled, &result);

            if (signaled && (result == 0x1337)) {
                // A-OK!
            } else {
                // weird error
            }

            k_poll_signal_reset(&signal);
            events[0].state = K_POLL_STATE_NOT_READY;
        }
    }

请注意，轮询信号内部不进行同步。向 :c:func:`k_poll` 传入信号后，只要系统中的任何代码调用 :c:func:`k_poll_signal_raise()`，该调用就会返回。但如果信号由外部代码管理，并通过 :c:func:`k_poll_signal_init()` 重置，应用程序检查时事件状态可能已经不再等于 :c:macro:`K_POLL_STATE_SIGNALED`，简单实现的应用程序就可能遗漏事件。最佳做法是始终只在执行 :c:func:`k_poll` 循环的线程内重置信号，或使用其他能够跟踪事件计数的事件类型：在这一点上，信号量和 FIFO 更不易出错，因为它们在机制上不会“遗漏”事件。

使用建议
********

使用 :c:func:`k_poll` 合并原本分别等待单个对象的多个线程，可能节省大量栈空间。

如果只有一个线程等待，可以将轮询信号用作轻量级二值信号量。

.. note::
    只有在没有其他线程等待对象变为可用时，才会为对象发出轮询通知，而且同一对象只能由一个线程轮询，因此轮询最适合用于多个线程之间不会竞争对象的场景。典型情况是，单个线程充当多个对象的主要“服务器”或“分发器”，且只有该线程尝试获取这些对象。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_POLL`

API 参考
********

.. doxygengroup:: poll_apis
