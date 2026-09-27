.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _system_threads_v2:

系统线程
########

.. contents::
    :local:
    :depth: 2

:dfn:`系统线程` 是内核在系统初始化期间自动创建的线程。

内核会创建以下系统线程：

**主线程**
    此线程执行内核初始化，然后调用应用程序的 :c:func:`main` 函数（如果已定义）。

    默认情况下，主线程使用配置的最高抢占式线程优先级（即 0）。如果内核未配置为支持抢占式线程，主线程则使用配置的最低协作式线程优先级（即 -1）。

    主线程在执行内核初始化或应用程序的 :c:func:`main` 函数期间属于关键线程；这意味着线程中止会引发致命系统错误。如果未定义 :c:func:`main`，或者该函数执行后正常返回，主线程将正常终止，不会引发错误。

**空闲线程**
    系统没有其他工作可做时，此线程便会执行。如果可能，空闲线程会启用开发板的电源管理支持以节省功耗；否则，它只执行一个“什么也不做”的循环。只要系统仍在运行，空闲线程就一直存在，永不终止。

    空闲线程始终使用配置的最低线程优先级。

    空闲线程属于关键线程，这意味着线程中止会引发致命系统错误。

根据应用程序指定的内核和开发板配置选项，还可能创建其他系统线程。例如，启用系统工作队列会创建一个系统线程，处理提交到该队列的工作项。（参见 :ref:`workqueues_v2`。）

实现
****

编写 main() 函数
================

内核初始化完成后，应用程序提供的 ``main()`` 函数开始执行。除非选择了 ``CONFIG_BOOTARGS``，否则内核不会向该函数传递任何参数。选择此选项后，内核会向其传递参数，此时可以使用 ``main(int, char **)``。

以下代码展示了一个简单的 ``main(void)`` 函数。实际应用程序中的函数可以根据需要实现更复杂的逻辑。

.. code-block:: c

    int main(void)
    {
        /* initialize a semaphore */
        ...

        /* register an ISR that gives the semaphore */
        ...

        /* monitor the semaphore forever */
        while (1) {
            /* wait for the semaphore to be given by the ISR */
            ...
            /* do whatever processing is now needed */
            ...
        }
    }

使用建议
********

对于只需要一个线程的应用程序，使用主线程完成基于线程的处理，无需再定义一个应用程序专用线程。
