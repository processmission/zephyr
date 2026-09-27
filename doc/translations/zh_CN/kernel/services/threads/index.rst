.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _threads_v2:

线程
####

.. note::
   也对 :ref:`nothread` 提供有限支持。

.. contents::
    :local:
    :depth: 2

本节介绍用于创建、调度和删除可独立执行指令的线程的内核服务。

:dfn:`线程` 是一种内核对象，用于执行耗时过长或过于复杂、不适合在 ISR 中完成的应用程序处理。

应用程序可以定义任意数量的线程（仅受可用 RAM 限制）。每个线程通过创建时分配的 :dfn:`线程 ID` 来引用。

线程具有以下主要属性：

* **栈区域**，即用作线程栈的一块内存。栈区域的 **大小** 可以根据线程处理的实际需求调整。系统提供专用宏来创建和操作栈内存区域。

* **线程控制块**，供内核在内部记录线程元数据。它是 :c:struct:`k_thread` 类型的实例。

* **入口函数**，在线程启动时调用。最多可以向此函数传递 3 个 **参数值**。

* **调度优先级**，指示内核调度器如何为线程分配 CPU 时间。（参见 :ref:`scheduling_v2`。）

* 一组 **线程选项**，使内核在特定情况下对线程进行特殊处理。（参见 :ref:`thread_options_v2`。）

* **启动延时**，指定内核在线程启动前应等待多长时间。

* **执行模式**，可以是特权模式或用户模式。默认情况下，线程在特权模式下运行，可以访问特权 CPU 指令、整个内存地址空间和外设。用户模式线程拥有的权限较少。此功能取决于 :kconfig:option:`CONFIG_USERSPACE` 选项。参见 :ref:`usermode_api`。

.. _lifecycle_v2:

生命周期
********

.. _spawning_thread:

创建线程
========

线程必须先创建才能使用。内核会初始化线程控制块以及栈的一端。线程栈的其余部分通常不进行初始化。

将启动延时指定为 :c:macro:`K_NO_WAIT`，可指示内核立即开始执行线程。也可以通过指定超时值，让内核延迟执行线程，例如等待线程使用的设备硬件就绪。

内核允许在线程开始执行之前取消延迟启动。如果线程已经启动，取消请求不会生效。成功取消延迟启动的线程必须重新创建后才能使用。

启动线程
========

以 :c:macro:`K_FOREVER` 作为启动延时创建的线程不会加入调度器的就绪队列，只有显式启动后才会开始执行。:c:func:`k_thread_start` 函数可以启动这种未激活的线程，使其具备被调度的条件。启动已经启动的线程不会产生任何影响。

当线程对象需要先创建，而其执行需要推迟到应用程序完成其他设置之后时，这种方式很有用。

线程终止
========

线程启动后通常会一直执行。不过，线程也可以通过从入口函数返回来同步结束执行。这称为 **终止**。

终止的线程负责在返回前释放其持有的所有共享资源（例如互斥量和动态分配的内存），因为内核 *不会* 自动回收这些资源。

在某些情况下，线程可能需要休眠，直到另一个线程终止。可以使用 :c:func:`k_thread_join` API 实现。它会阻塞调用线程，直到超时到期、目标线程自行退出，或目标线程中止（由于调用 :c:func:`k_thread_abort` 或触发致命错误）。

线程终止后，内核保证不再使用其线程结构体。此结构体的内存随后可以用于任何用途，包括创建新线程。请注意，线程必须完全终止：如果线程自身的逻辑发出完成信号，而另一线程在内核处理完成前就看到该信号，就会产生竞态条件。通常，应用程序代码应使用 :c:func:`k_thread_join` 或 :c:func:`k_thread_abort` 同步线程的终止状态，而不应依赖应用程序逻辑内部发出的信号。

线程中止
========

线程可以通过 **中止** 异步结束执行。如果线程触发致命错误（例如解引用空指针），内核会自动中止该线程。

另一个线程（或线程自身）也可以调用 :c:func:`k_thread_abort` 中止线程。不过，通常更推荐向线程发出信号，让它自行正常终止，而不是将其中止。

与线程终止一样，内核不会回收被中止线程持有的共享资源。

.. note::
    内核目前不对应用程序能否重新创建已中止的线程作出任何保证。

线程挂起
========

线程进入 **挂起** 状态后，可以被无限期地禁止执行。:c:func:`k_thread_suspend` 函数可用于挂起任意线程，包括调用线程自身。挂起已经挂起的线程不会产生额外影响。

线程一旦挂起，便无法被调度，直到另一个线程调用 :c:func:`k_thread_resume` 解除挂起。

.. note::
   线程可以使用 :c:func:`k_sleep` 使自身在指定时间内停止执行。不过，这与挂起线程不同，因为休眠线程会在时限到达时自动变为可执行状态。

.. _thread_states:

线程状态
********

如果没有任何因素阻止线程执行，该线程就被视为 **就绪**，可以被选为当前线程。

如果存在一个或多个因素阻止线程执行，该线程就被视为 **未就绪**，不能被选为当前线程。

以下因素会使线程处于未就绪状态：

* 线程尚未启动。
* 线程正在等待内核对象完成操作。（例如，线程正在获取一个不可用的信号量。）
* 线程正在等待超时到期。
* 线程已被挂起。
* 线程已终止或中止。

  .. image:: thread_states.svg
     :align: center

.. note::

  虽然上图看起来可能暗示 **就绪** 和 **运行** 是两种不同的线程状态，但这种理解并不正确。**就绪** 是线程状态，而 **运行** 是仅适用于 **就绪** 线程的调度状态。

线程栈对象
**********

每个线程都需要自己的栈缓冲区，供 CPU 压入上下文。根据配置，必须满足以下若干约束：

- 可能需要为内存管理结构预留额外内存
- 如果启用了基于保护区域的栈溢出检测，则必须在紧邻栈缓冲区的前方设置一小块写保护的内存管理区域，用于捕获溢出。
- 如果启用了用户空间，必须预留一个独立、固定大小的提权栈，作为处理系统调用的专用内核栈。
- 如果启用了用户空间，线程栈缓冲区的大小和对齐必须合适，以便配置一个恰好覆盖它的内存保护区域。

对齐约束可能非常严格，例如某些 MPU 要求区域大小为 2 的幂，并按其自身大小对齐。

因此，可移植代码不能简单地将任意字符缓冲区传递给 :c:func:`k_thread_create`。系统提供了以 ``K_KERNEL_STACK`` 和 ``K_THREAD_STACK`` 为前缀的专用宏，用于静态创建栈。

此外，可以使用 :c:func:`k_thread_stack_alloc` 动态创建栈，随后使用 :c:func:`k_thread_stack_free` 释放。

仅供内核使用的栈
================

如果确定线程永远不会在用户模式下运行，或者栈用于中断处理等特殊上下文，最好使用 ``K_KERNEL_STACK`` 宏定义栈。

这些栈可以节省内存，因为无需配置 MPU 区域来覆盖栈缓冲区本身，内核也无需为提权栈或仅与用户模式线程相关的内存管理数据结构预留额外空间。

从用户模式尝试使用以这种方式声明的栈，会使调用者触发致命错误。

如果未启用 ``CONFIG_USERSPACE``，``K_THREAD_STACK`` 系列宏与 ``K_KERNEL_STACK`` 系列宏的效果相同。

线程栈
======

如果确定栈需要用于用户线程，或者无法确定，应使用 ``K_THREAD_STACK`` 宏定义栈。这可能占用更多内存，但得到的栈对象适合用于用户线程。

如果未启用 ``CONFIG_USERSPACE``，``K_THREAD_STACK`` 系列宏与 ``K_KERNEL_STACK`` 系列宏的效果相同。

.. _thread_priorities:

线程优先级
**********

线程优先级是一个整数，可以为负数或非负数。数值越小，优先级越高。例如，调度器认为优先级为 4 的线程 A 比优先级为 7 的线程 B 优先级 *更高*；同样，优先级为 -2 的线程 C 比线程 A 和线程 B 的优先级都高。

调度器根据线程的优先级将线程分为两类。

* :dfn:`协作式线程` 的优先级值为负数。协作式线程一旦成为当前线程，就会一直保持为当前线程，直到执行使自身变为未就绪状态的操作。

* :dfn:`抢占式线程` 的优先级值为非负数。抢占式线程成为当前线程后，如果协作式线程或优先级更高或相同的抢占式线程进入就绪状态，它随时可能被替换。


线程启动后，其初始优先级值仍可以调高或调低。因此，可以通过改变优先级，将抢占式线程变为协作式线程，反之亦然。

.. note::
    调度器不会通过启发式决策重新调整线程优先级。只有应用程序发出请求时，线程优先级才会被设置或改变。

内核支持的线程优先级数量几乎没有限制。配置选项 :kconfig:option:`CONFIG_NUM_COOP_PRIORITIES` 和 :kconfig:option:`CONFIG_NUM_PREEMPT_PRIORITIES` 分别指定两类线程的优先级级数，从而得到以下可用优先级范围：

* 协作式线程：(-:kconfig:option:`CONFIG_NUM_COOP_PRIORITIES`) 到 -1
* 抢占式线程：0 到 (:kconfig:option:`CONFIG_NUM_PREEMPT_PRIORITIES` - 1)

.. image:: priorities.svg
   :align: center

例如，配置 5 个协作式优先级和 10 个抢占式优先级后，两者的范围分别为 -5 到 -1 和 0 到 9。

.. _metairq_priorities:

Meta-IRQ 优先级
===============

启用此功能后（参见 :kconfig:option:`CONFIG_NUM_METAIRQ_PRIORITIES`），优先级空间的最高端（数值最小端）会存在一个特殊的协作式优先级子类：meta-IRQ 线程。这些线程按其普通优先级调度，但还能够抢占所有优先级更低的其他线程（包括其他 meta-IRQ 线程），即使这些线程是协作式线程和/或已锁定调度器。不过，meta-IRQ 线程仍然是线程，仍可被任何硬件中断打断。

.. note::
   被 meta-IRQ 线程抢占的协作式线程（或已锁定调度器的线程），在 meta-IRQ 线程完成后恢复执行时，仍会位于原来的 CPU 上，前提是它未被挂起或中止。这有助于确保这些线程在查询自身 CPU 的相关属性时，不会意外迁移到其他 CPU。

这种行为使得解除 meta-IRQ 线程阻塞的操作（无论通过何种方式，例如创建线程、调用 k_sem_give() 等），在由低优先级线程执行时，等效于一次同步系统调用；在真正的中断上下文中执行时，则类似于 ARM 的“挂起 IRQ”。此功能旨在用于实现驱动子系统中的中断“下半部”处理和/或“tasklet”功能。线程一旦被唤醒，就保证会在当前 CPU 返回应用程序代码之前运行。

与其他操作系统的类似功能不同，meta-IRQ 线程是真正的线程，在各自的栈上运行（必须照常分配），而不是使用每个 CPU 的中断栈。在支持的架构上使用 IRQ 栈的设计工作尚待完成。

请注意，这打破了 Zephyr API 对协作式线程的承诺（即在当前线程主动阻塞前，操作系统不会调度其他线程），因此应用程序代码必须极为谨慎地使用此功能。它们并非只是优先级很高的线程，不应将其当作普通的高优先级线程使用。

.. _thread_options_v2:

线程选项
********

内核支持一小组 :dfn:`线程选项`，允许在特定情况下对线程进行特殊处理。线程关联的选项集在创建线程时指定。

不需要任何线程选项的线程，其选项值为零。需要线程选项时，通过选项名称指定；如果需要多个选项，则使用 :literal:`|` 字符作为分隔符（即使用按位或运算符组合选项）。

支持以下线程选项。

:c:macro:`K_ESSENTIAL`
    此选项将线程标记为 :dfn:`关键线程`，指示内核将该线程的终止或中止视为致命系统错误。

    默认情况下，线程不被视为关键线程。

:c:macro:`K_SSE_REGS`
    此 x86 专用选项表示线程使用 CPU 的 SSE 寄存器。另请参见 :c:macro:`K_FP_REGS`。

    默认情况下，内核在调度线程时不会尝试保存和恢复这些寄存器的内容。

:c:macro:`K_FP_REGS`
    此选项表示线程使用 CPU 的浮点寄存器，指示内核在线程调度时执行额外步骤以保存和恢复这些寄存器的内容。（更多信息参见 :ref:`float_v2`。）

    默认情况下，内核在调度线程时不会尝试保存和恢复此寄存器的内容。

:c:macro:`K_USER`
    如果启用了 :kconfig:option:`CONFIG_USERSPACE`，此线程将以用户模式创建，权限受限。参见 :ref:`usermode_api`。否则，此标志不起作用。

:c:macro:`K_INHERIT_PERMS`
    如果启用了 :kconfig:option:`CONFIG_USERSPACE`，此线程将继承父线程拥有的所有内核对象权限，但父线程对象的权限除外。参见 :ref:`usermode_api`。


.. _custom_data_v2:

线程自定义数据
**************

每个线程都有一个 32 位的 :dfn:`自定义数据` 区域，仅可由线程自身访问，应用程序可自行决定其用途。线程的默认自定义数据值为零。

.. note::
   ISR 不支持自定义数据，因为它们运行在同一个共享的内核中断处理上下文中。

默认情况下，线程自定义数据支持处于禁用状态。可通过配置选项 :kconfig:option:`CONFIG_THREAD_CUSTOM_DATA` 启用。

:c:func:`k_thread_custom_data_set` 和 :c:func:`k_thread_custom_data_get` 函数分别用于写入和读取线程的自定义数据。线程只能访问自己的自定义数据，不能访问其他线程的数据。

以下代码使用自定义数据功能，记录每个线程调用某个特定例程的次数。

.. note::
    显然，只有一个例程可以使用这种方法，因为它会独占自定义数据功能。

.. code-block:: c

    int call_tracking_routine(void)
    {
        uint32_t call_count;

        if (k_is_in_isr()) {
            /* ignore any call made by an ISR */
        } else {
            call_count = (uint32_t)k_thread_custom_data_get();
            call_count++;
            k_thread_custom_data_set((void *)call_count);
        }

        /* do rest of routine's processing */
        ...
    }

将线程自定义数据用作指向线程所拥有数据结构的指针，可使例程访问线程特定的信息。

.. _thread_name_v2:

线程名称
********

启用 :kconfig:option:`CONFIG_THREAD_NAME` 后，可以为每个线程关联一个便于阅读的名称。名称主要用于辅助调试、日志记录和 shell 内省；内核不会将名称用于调度。

可以通过以下两种方式之一为线程命名：

* 静态指定：向 :c:macro:`K_THREAD_DEFINE` 传入名称。
* 运行时指定：使用 :c:func:`k_thread_name_set`。由于内核只保留指向该字符串的指针，传入的字符串必须在线程的整个生命周期内保持有效。

可通过 :c:func:`k_thread_name_get` 获取线程名称，该函数返回指向名称字符串的指针；也可以使用 :c:func:`k_thread_name_copy`，将名称复制到调用者提供的缓冲区。在用户模式下，调用线程可能无权访问存放其他线程名称的内存，因此复制版本是更安全的选择。

如果未启用 :kconfig:option:`CONFIG_THREAD_NAME`，:c:func:`k_thread_name_set` 会返回错误，:c:func:`k_thread_name_get` 会返回 ``NULL``。

线程内省
********

内核提供了若干接口，用于在运行时检查线程。

**识别当前线程**
    :c:func:`k_current_get` 返回当前正在执行的线程的 ID（:c:type:`k_tid_t`）。此 ID 可传递给其他线程 API，以操作调用线程自身。

**读取线程优先级**
    :c:func:`k_thread_priority_get` 返回线程当前的调度优先级。它反映线程创建后发生的所有优先级变化，例如通过 :c:func:`k_thread_priority_set` 所做的修改。

**获取线程状态**
    :c:func:`k_thread_state_str` 将线程当前状态的可读表示（例如 ``pending``、``suspended`` 或 ``ready``）写入调用者提供的缓冲区。此功能用于诊断输出，不应通过程序解析其结果。

**遍历所有线程**
    启用 :kconfig:option:`CONFIG_THREAD_MONITOR` 后，:c:func:`k_thread_foreach` 会对系统中的每个线程调用一次调用者提供的回调。它在遍历期间持有内部锁，阻止线程创建和终止，从而保证线程列表快照的一致性，但会引入与线程数量成正比的延迟。:c:func:`k_thread_foreach_unlocked` 是延迟较低的版本，在调用每个回调时会释放锁，代价是视图的一致性不那么严格。

**查询栈使用情况**
    启用 :kconfig:option:`CONFIG_INIT_STACKS` 和 :kconfig:option:`CONFIG_THREAD_STACK_INFO` 后，:c:func:`k_thread_stack_space_get` 会报告线程栈剩余的未使用字节数。它通过扫描栈中未使用（仍保留初始化值）的区域进行计算。这是对构建时栈分析工具和下述运行时栈安全功能的补充。

**查询待到期的超时**
    阻塞于限时操作（例如 :c:func:`k_sleep` 或带超时的内核对象操作）的线程具有待到期的超时。可以通过 :c:func:`k_thread_timeout_remaining_ticks` 查询剩余 tick 数，也可以通过 :c:func:`k_thread_timeout_expires_ticks` 查询其到期时的绝对系统 tick 值。如果线程没有待到期的超时，两者均返回零。

实现
****

创建线程
========

创建线程时，先定义其栈区域和线程控制块，再调用 :c:func:`k_thread_create`。

可以使用 :c:macro:`K_THREAD_STACK_DEFINE` 或 :c:macro:`K_KERNEL_STACK_DEFINE` 静态分配栈区域，确保其在内存中得到正确设置。

栈大小参数必须是以下三个值之一：

- 传递给 ``K_THREAD_STACK`` 或 ``K_KERNEL_STACK`` 系列栈创建宏的原始请求栈大小。
- 对于用 ``K_THREAD_STACK`` 系列宏定义的栈对象，使用 :c:macro:`K_THREAD_STACK_SIZEOF()` 对该对象的返回值。
- 对于用 ``K_KERNEL_STACK`` 系列宏定义的栈对象，使用 :c:macro:`K_KERNEL_STACK_SIZEOF()` 对该对象的返回值。

也可以使用 :c:func:`k_thread_stack_alloc` 动态分配栈区域，并使用 :c:func:`k_thread_stack_free` 释放。

线程创建函数返回线程 ID，可用于引用该线程。

以下代码创建一个立即启动的线程。

.. code-block:: c

    #define MY_STACK_SIZE 500
    #define MY_PRIORITY 5

    extern void my_entry_point(void *, void *, void *);

    K_THREAD_STACK_DEFINE(my_stack_area, MY_STACK_SIZE);
    struct k_thread my_thread_data;

    k_tid_t my_tid = k_thread_create(&my_thread_data, my_stack_area,
                                     K_THREAD_STACK_SIZEOF(my_stack_area),
                                     my_entry_point,
                                     NULL, NULL, NULL,
                                     MY_PRIORITY, 0, K_NO_WAIT);

也可以通过调用 :c:macro:`K_THREAD_DEFINE` 在编译时声明线程。请注意，此宏会自动定义栈区域、控制块和线程 ID 变量。

以下代码与上面的代码片段效果相同。

.. code-block:: c

    #define MY_STACK_SIZE 500
    #define MY_PRIORITY 5

    extern void my_entry_point(void *, void *, void *);

    K_THREAD_DEFINE(my_tid, MY_STACK_SIZE,
                    my_entry_point, NULL, NULL, NULL,
                    MY_PRIORITY, 0, 0);

.. note::
   :c:func:`k_thread_create` 的延时参数是 :c:type:`k_timeout_t` 值，因此 :c:macro:`K_NO_WAIT` 表示立即启动线程。:c:macro:`K_THREAD_DEFINE` 的对应参数是以整数毫秒表示的时长，因此等效参数为 0。

以下代码动态分配线程栈，等待线程结束并完成 join，然后释放动态分配的线程栈。

.. code-block:: c

    extern void my_entry_point(void *, void *, void *);

    k_tid_t my_tid;
    void *my_stack_area;

    my_stack_area = k_thread_stack_alloc(CONFIG_DYNAMIC_THREAD_STACK_SIZE);
    my_tid = k_thread_create(&my_thread_data, my_stack_area,
                              CONFIG_DYNAMIC_THREAD_STACK_SIZE,
                              my_entry_point,
                              NULL, NULL, NULL,
                              MY_PRIORITY, 0, K_NO_WAIT);
    k_thread_join(my_tid, K_FOREVER);
    k_thread_stack_free(my_stack_area);

用户模式约束
------------

本节仅适用于启用了 :kconfig:option:`CONFIG_USERSPACE` 且用户线程尝试创建新线程的情况。仍然使用 :c:func:`k_thread_create` API，但必须满足额外约束，否则调用线程将被终止：

* 调用线程必须已被授予对子线程和栈参数的访问权限；二者均由内核作为内核对象跟踪。

* 子线程和栈对象必须处于未初始化状态，即线程当前未运行，且栈内存未被使用。

* 传入的栈大小参数必须小于或等于栈对象声明时的大小范围。

* 必须使用 :c:macro:`K_USER` 选项，因为用户线程只能创建其他用户线程。

* 不得使用 :c:macro:`K_ESSENTIAL` 选项，用户线程不能被视为关键线程。

* 子线程的优先级必须是有效值，并且低于或等于父线程的优先级。

降低权限
========

启用 :kconfig:option:`CONFIG_USERSPACE` 后，在特权模式下运行的线程可以使用 :c:func:`k_thread_user_mode_enter` API 单向切换到用户模式。这是不可逆操作，会重置并清零线程栈内存。该线程将被标记为非关键线程。

终止线程
========

线程通过从入口函数返回来终止自身。

以下代码演示了线程终止的方式。

.. code-block:: c

    void my_entry_point(int unused1, int unused2, int unused3)
    {
        while (1) {
            ...
            if (<some condition>) {
                return; /* thread terminates from mid-entry point function */
            }
            ...
        }

        /* thread terminates at end of entry point function */
    }

如果启用了 :kconfig:option:`CONFIG_USERSPACE`，中止线程还会将线程和栈对象标记为未初始化，以便复用。

运行时统计
**********

启用 :kconfig:option:`CONFIG_THREAD_RUNTIME_STATS` 后，可以收集和获取线程运行时统计信息，例如线程执行的总周期数。

默认情况下，运行时统计使用默认内核定时器收集。在某些架构、SoC 或开发板上，可以通过计时函数使用分辨率更高的定时器。通过 :kconfig:option:`CONFIG_THREAD_RUNTIME_STATS_USE_TIMING_FUNCTIONS` 可启用这些定时器。

示例如下：

.. code-block:: c

   k_thread_runtime_stats_t rt_stats_thread;

   k_thread_runtime_stats_get(k_current_get(), &rt_stats_thread);

   printk("Cycles: %llu\n", rt_stats_thread.execution_cycles);

使用 :c:func:`k_thread_runtime_stats_all_get` 可以获取系统中所有线程的汇总统计信息，它报告所有线程（包括空闲线程）的累计运行时间。这有助于计算总体 CPU 利用率。

启用 :kconfig:option:`CONFIG_SCHED_THREAD_USAGE` 后，可以在运行时通过 :c:func:`k_thread_runtime_stats_enable` 和 :c:func:`k_thread_runtime_stats_disable` 分别启用和禁用单个线程的统计收集。可通过 :c:func:`k_thread_runtime_stats_is_enabled` 检查某个线程当前是否正在收集统计。对不需要测量的线程禁用统计收集，可以减少每次上下文切换带来的记账开销。

运行时栈安全
************

启用 :kconfig:option:`CONFIG_THREAD_RUNTIME_STACK_SAFETY` 后，内核会提供在运行时扫描线程栈的例程，以确定尚未使用的栈空间。如果发现未使用的栈空间低于可为每个线程配置的阈值，就会调用用户定义的处理函数。

此功能供监控软件使用。例如，处理函数可以记录警告、挂起或中止出现问题的线程，甚至重启系统。它允许系统在栈耗尽 *之前* 作出响应，补充了构建时栈分析工具和基于硬件的栈溢出检测。

每个线程都有一个以字节表示的 *未使用栈空间阈值*。栈安全检查发现线程的未使用栈空间低于此阈值时，会调用提供的处理函数。阈值为 0 字节（默认值）时，会禁用该线程的检查。新建线程的默认阈值由 :kconfig:option:`CONFIG_THREAD_RUNTIME_STACK_SAFETY_DEFAULT_UNUSED_THRESHOLD_PCT` 决定，该选项以各线程总栈大小的百分比表示阈值。

可以在运行时设置或查询单个线程的阈值：

* :c:func:`k_thread_runtime_stack_unused_threshold_pct_set` 以线程总栈大小的百分比（0 到 99）设置阈值。
* :c:func:`k_thread_runtime_stack_unused_threshold_set` 以绝对字节数设置阈值。
* :c:func:`k_thread_runtime_stack_unused_threshold_get` 获取当前阈值（以字节为单位）。

有两个例程执行实际检查。两者都接受一个指针，用于在返回时接收未使用栈空间的大小；还接受一个 :c:type:`k_thread_stack_safety_handler_t` 处理函数（以及用户参数），在越过阈值时调用：

* :c:func:`k_thread_runtime_stack_safety_full_check` 扫描整个栈，计算未使用空间的准确大小。
* :c:func:`k_thread_runtime_stack_safety_threshold_check` 进行简化扫描，仅检查线程是否已越过配置的阈值。它比完整检查开销更低，但不能准确测量未使用空间。

以下示例配置线程，使其未使用栈空间低于总栈大小的 10% 时调用处理函数：

.. code-block:: c

   void stack_safety_handler(const struct k_thread *thread,
                             size_t unused_space, void *arg)
   {
           printk("Thread %p low on stack: %zu bytes unused\n",
                  thread, unused_space);
   }

   /* Trigger the handler once less than 10% of the stack remains unused */
   k_thread_runtime_stack_unused_threshold_pct_set(my_tid, 10);

   /* Periodically check the thread from a monitoring context */
   k_thread_runtime_stack_safety_full_check(my_tid, NULL,
                                            stack_safety_handler, NULL);

使用建议
********

使用线程执行无法在 ISR 中完成的处理。

使用不同线程处理逻辑上独立、可并行执行的操作。


配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_MAIN_THREAD_PRIORITY`
* :kconfig:option:`CONFIG_MAIN_STACK_SIZE`
* :kconfig:option:`CONFIG_IDLE_STACK_SIZE`
* :kconfig:option:`CONFIG_THREAD_CUSTOM_DATA`
* :kconfig:option:`CONFIG_NUM_COOP_PRIORITIES`
* :kconfig:option:`CONFIG_NUM_PREEMPT_PRIORITIES`
* :kconfig:option:`CONFIG_TIMESLICING`
* :kconfig:option:`CONFIG_TIMESLICE_SIZE`
* :kconfig:option:`CONFIG_TIMESLICE_PRIORITY`
* :kconfig:option:`CONFIG_USERSPACE`
* :kconfig:option:`CONFIG_THREAD_RUNTIME_STACK_SAFETY`
* :kconfig:option:`CONFIG_THREAD_RUNTIME_STACK_SAFETY_DEFAULT_UNUSED_THRESHOLD_PCT`



API 参考
********

.. doxygengroup:: thread_apis

.. doxygengroup:: thread_stack_api
