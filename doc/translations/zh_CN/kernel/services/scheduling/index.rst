.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _scheduling_v2:

调度
####

内核基于优先级的调度器允许应用程序的各线程共享 CPU。

概念
****

调度器决定任意时刻允许哪个线程执行；此线程称为 **当前线程**。

在多个时机，调度器都有机会更换当前线程，即将 CPU 的执行从一个线程切换到另一个线程。这些时机称为 **重新调度点**。可能的重新调度点包括：

- 线程从运行状态转为挂起或等待状态，例如通过 :c:func:`k_sem_take` 或 :c:func:`k_sleep`。
- 线程转为 :ref:`就绪状态 <thread_states>`，例如通过 :c:func:`k_sem_give` 或 :c:func:`k_thread_start`
- 处理中断后返回线程上下文
- 运行中的线程调用 :c:func:`k_yield`

线程主动发起某个操作，使自身转为挂起或等待状态时，该线程便进入 **休眠**。

每当调度器更换当前线程，或者 ISR 取代当前线程执行时，内核都会先保存当前线程的 CPU 寄存器值。线程随后恢复执行时，会恢复这些寄存器值。


调度算法
========

内核调度器选择优先级最高的就绪线程作为当前线程。当存在多个优先级相同的就绪线程时，调度器会选择等待时间最长的线程。

线程的相对优先级主要由其静态优先级决定。不过，如果启用了最早截止时间优先调度（:kconfig:option:`CONFIG_SCHED_DEADLINE`），且待选线程的静态优先级相同，则截止时间更早的线程被视为优先级更高。因此，启用最早截止时间优先调度后，只有静态优先级和截止时间都相同的两个线程才被视为具有相同优先级。使用 :c:func:`k_thread_deadline_set` 例程设置线程的截止时间。

.. note::
    ISR 的执行优先于线程，因此除非中断被屏蔽，当前线程的执行随时都可能被 ISR 取代。这对协作式线程和抢占式线程均适用。


构建内核时，可以从多种就绪队列实现中选择一种，在代码大小、运行时常数开销以及线程数量增多时的性能扩展能力之间作出取舍。

* 简单链表就绪队列（:kconfig:option:`CONFIG_SCHED_SIMPLE`）

  调度器就绪队列实现为简单的无序链表，处理单个线程的常数时间开销极低，代码体积也很小。对于代码大小受限，且任意时刻队列中可运行线程始终只有少量（例如 3 个）的系统，应选择此实现。在大多数未在其他地方使用红黑树的平台上，这可以节省约 2 KB 代码空间。

* 红黑树就绪队列（:kconfig:option:`CONFIG_SCHED_SCALABLE`）

  调度器就绪队列实现为红黑树。它的插入和删除常数开销较高，且在大多数未在其他地方使用红黑树的平台上，需要额外约 2 KB 代码空间。但它可以平稳、高效地扩展到数千个线程。

  需要大量可并发运行线程（约 20 个以上）的应用程序可以使用此实现。大多数应用程序不需要这种就绪队列实现。

* 传统多队列就绪队列（:kconfig:option:`CONFIG_SCHED_MULTIQ`）

  选择此选项后，调度器就绪队列将采用经典的教科书式链表数组实现，每个优先级对应一个链表。

  这对应于 Zephyr 1.12 之前版本所用的调度算法。

  与“简单”调度器相比，它只增加极少的代码大小，几乎所有情况下都能以很低的常数开销在 O(1) 时间内运行。但它需要较多 RAM 来存放各链表头，且功能有限，无法兼容需要对线程进行更精细排序的截止时间调度，也无法兼容需要遍历线程列表的 SMP 亲和性功能。

  可运行线程数量较少的典型应用程序通常更适合使用简单调度器。


IPC 原语使用 wait_q 抽象让线程等待，以便稍后唤醒。它与调度器使用相同的后端数据结构选择，支持相同的实现选项。

* 可扩展 wait_q 实现（:kconfig:option:`CONFIG_WAITQ_SCALABLE`）

  选择此选项后，wait_q 将使用平衡树实现。如果预计单个原语上会有大量线程等待，请选择此实现。如果应用程序未在其他地方使用红黑树，与 :kconfig:option:`CONFIG_WAITQ_SIMPLE` 相比，代码体积会增加约 2 KB（可与 :kconfig:option:`CONFIG_SCHED_SCALABLE` 共享）。对“小”队列执行等待和解除等待操作会稍慢一些（不过，这通常不是性能关键路径）。

* 简单链表 wait_q（:kconfig:option:`CONFIG_WAITQ_SIMPLE`）

  选择此选项后，wait_q 将使用双向链表实现。如果预计任意单个 IPC 原语上只有少量线程阻塞，请选择此实现。

协作式时间片轮转
================

协作式线程一旦成为当前线程，就会保持为当前线程，直到执行使其变为未就绪状态的操作。因此，如果协作式线程执行耗时较长的计算，可能使其他线程（包括优先级更高和相同的线程）的调度产生不可接受的延迟。


  .. image:: cooperative.svg
     :align: center

为解决此类问题，协作式线程可以不时主动让出 CPU，使其他线程能够执行。线程可以通过两种方式让出 CPU：

* 调用 :c:func:`k_yield` 会将线程放到调度器按优先级排列的就绪线程列表中相应位置的末尾，然后调用调度器。优先级高于或等于让出 CPU 的线程的所有就绪线程，均有机会在该线程再次被调度之前执行。如果不存在这样的就绪线程，调度器会立即重新调度让出 CPU 的线程，而不进行上下文切换。

* 调用 :c:func:`k_sleep` 会使线程在指定时间内处于未就绪状态。此时，*所有* 优先级的就绪线程都有机会执行；不过，不能保证优先级低于休眠线程的线程一定会在休眠线程再次就绪之前被调度。

抢占式时间片轮转
================

抢占式线程一旦成为当前线程，就会保持为当前线程，直到更高优先级的线程就绪，或自身执行使其变为未就绪状态的操作。因此，如果抢占式线程执行耗时较长的计算，可能使其他线程（包括相同优先级的线程）的调度产生不可接受的延迟。


  .. image:: preemptive.svg
     :align: center

为解决此类问题，抢占式线程可以采用前述协作式时间片轮转，或者利用调度器的时间片轮转功能，让同优先级的其他线程执行。

.. image:: timeslicing.svg
   :align: center

.. note::
   对于 SMP，行为与上面的单处理器示意图类似，但线程 1 不会紧接在线程 4 之后执行。执行顺序将是线程 2、线程 3、线程 1，依此类推。

调度器将每个 CPU 上的时间划分为一系列 **时间片**，以系统时钟 tick 为单位。时间片大小可以配置，也可以在应用程序运行期间修改。调度新线程时会重置时间片定时器。

每个时间片结束时，调度器会检查当前线程是否可抢占；如果可以，则隐式地代该线程调用 :c:func:`k_yield`。这样，其他相同优先级的就绪线程就有机会在当前线程再次被调度之前执行。如果没有其他相同优先级的就绪线程，当前线程就继续运行。

优先级高于指定阈值的线程不受抢占式时间片轮转影响，也不会被相同优先级的线程抢占。这样，应用程序可以仅对时间敏感程度较低的低优先级线程使用抢占式时间片轮转。

.. note::
   内核的时间片轮转算法 *不能* 保证一组相同优先级的线程获得相等的 CPU 时间，因为它不测量线程实际执行的时长。不过，该算法 *能够* 保证线程每执行至多一个时间片，就必须让出一次 CPU。

每线程时间片
============

通过 :c:func:`k_sched_time_slice_set` 配置的时间片，会全局应用于指定优先级及更低优先级的所有抢占式线程。启用 :kconfig:option:`CONFIG_TIMESLICE_PER_THREAD` 后，可以改用 :c:func:`k_thread_time_slice_set` 为单个线程设置独立时间片。每线程时间片优先于全局值，而且即使线程优先级高于全局时间片轮转阈值，也仍然适用。

除了以 tick 表示的时间片时长外，每线程时间片还会注册一个回调，供内核在时间片到期时调用。该回调运行在中断上下文中，此时受影响的线程仍是当前线程。例如，回调可以调整线程下次执行时的优先级或时间片，也可以将其挂起。

锁定调度器
==========

抢占式线程如果不希望在执行关键操作时被抢占，可以调用 :c:func:`k_sched_lock`，让调度器临时将其视为协作式线程。这可以防止其他线程在关键操作执行期间造成干扰。

关键操作完成后，抢占式线程必须调用 :c:func:`k_sched_unlock`，恢复正常的可抢占状态。

如果线程调用 :c:func:`k_sched_lock` 后，又执行了使自身变为未就绪状态的操作，调度器会将持锁线程切出，允许其他线程执行。当持锁线程再次成为当前线程时，仍保持不可抢占状态。

.. note::
    对于抢占式线程，锁定调度器比将优先级改为负数更能高效地防止抢占。


.. _thread_sleeping:

线程休眠
========

线程可以调用 :c:func:`k_sleep`，将自身的处理推迟指定时长。线程休眠期间会让出 CPU，使其他就绪线程得以执行。指定延时结束后，线程变为就绪状态，可以再次被调度。

其他线程可以使用 :c:func:`k_wakeup` 提前唤醒休眠线程。有时，可以借此让另一个线程通知休眠线程发生了某件事，*无需* 在线程间定义信号量等内核同步对象。允许唤醒没有休眠的线程，但不会产生任何影响。

.. _busy_waiting:

忙等待
======

线程可以调用 :c:func:`k_busy_wait` 执行 ``busy wait``，将自身处理推迟指定时长，且 *不向* 其他就绪线程让出 CPU。

当所需延时太短、不值得让调度器从当前线程切换到其他线程再切换回来时，通常使用忙等待而不是线程休眠。

强制作出调度决策
================

线程可以调用 :c:func:`k_reschedule`，强制调度器立即在当前 CPU 上作出调度决策。在线程中调用时（中断未锁定），调度器会立即运行；在 ISR 中调用时，决策会推迟到 ISR 退出时执行。

与 :c:func:`k_yield` 不同，此例程不保证切换到相同或更高优先级的线程；它只是请求内核根据当前状态，重新评估接下来应运行哪个线程。大多数应用程序从不需要此例程。

查询可抢占性
============

如果代码的行为取决于自身是否可以被抢占，可以使用 :c:func:`k_is_preempt_thread` 查询当前上下文。只有调用者是线程（不是 ISR）、线程优先级处于可抢占范围内，且线程未锁定调度器时，它才返回非零值。

相关例程 :c:func:`k_can_yield` 用于报告当前上下文是否能够让出 CPU 或调用阻塞 API。在 ISR、内核初始化之前的阶段、空闲线程等无法让出 CPU 的上下文中，它返回 false。

使用建议
********

将协作式线程用于设备驱动程序和其他对性能要求严格的工作。

使用协作式线程实现互斥，无需互斥量等内核对象。

使用抢占式线程，让对时间敏感的处理优先于时间敏感程度较低的处理。


配置选项
********

* :kconfig:option:`CONFIG_TIMESLICING`
* :kconfig:option:`CONFIG_TIMESLICE_SIZE`
* :kconfig:option:`CONFIG_TIMESLICE_PRIORITY`

.. _cpu_idle:

CPU 空闲
########

虽然通常由空闲线程负责，但在某些特殊应用程序中，其他线程可能也需要使 CPU 进入空闲状态。

.. contents::
    :local:
    :depth: 2

Concepts
********

使 CPU 进入空闲状态会让内核暂停所有操作，直到某个事件（通常是中断）唤醒 CPU。在常规系统中，这由空闲线程负责。不过，在某些受限系统中，也可能由其他线程承担此职责。

实现
****

使 CPU 进入空闲状态
===================

使 CPU 进入空闲状态很简单：调用 :c:func:`k_cpu_idle` API 即可。CPU 会停止执行指令，直到有事件发生。通常会在循环中调用此函数。请注意，在某些架构上，:c:func:`k_cpu_idle` 返回时会无条件解除中断屏蔽。

.. code-block:: c

    static k_sem my_sem;

    void my_isr(void *unused)
    {
        k_sem_give(&my_sem);
    }

    int main(void)
    {
        k_sem_init(&my_sem, 0, 1);

        /* wait for semaphore from ISR, then do related work */

        for (;;) {

            /* wait for ISR to trigger work to perform */
            if (k_sem_take(&my_sem, K_NO_WAIT) == 0) {

                /* ... do processing */

            }

            /* put CPU to sleep to save power */
            k_cpu_idle();
        }
    }

以原子方式使 CPU 进入空闲状态
=============================

有时需要在使 CPU 进入空闲状态之前原子地完成某些工作。在这种情况下，应改用 :c:func:`k_cpu_atomic_idle`。

实际上，上一个示例存在竞态条件：中断可能发生在尝试获取信号量、发现其不可用之后，到再次让 CPU 空闲之前的间隙。在某些系统中，这会导致 CPU 一直空闲，直到 *另一个* 中断发生，而这个中断可能 *永远不会* 发生，从而使系统完全挂起。为避免此问题，应像本例这样使用 :c:func:`k_cpu_atomic_idle`。

.. code-block:: c

    static k_sem my_sem;

    void my_isr(void *unused)
    {
        k_sem_give(&my_sem);
    }

    int main(void)
    {
        k_sem_init(&my_sem, 0, 1);

        for (;;) {

            unsigned int key = irq_lock();

            /*
             * Wait for semaphore from ISR; if acquired, do related work, then
             * go to next loop iteration (the semaphore might have been given
             * again); else, make the CPU idle.
             */

            if (k_sem_take(&my_sem, K_NO_WAIT) == 0) {

                irq_unlock(key);

                /* ... do processing */


            } else {
                /* put CPU to sleep to save power */
                k_cpu_atomic_idle(key);
            }
        }
    }


Suggested Uses
**************

如果线程除了让 CPU 空闲以等待事件，还必须执行一些实际工作，请使用 :c:func:`k_cpu_atomic_idle`。参见上面的示例。

只有在线程仅负责让 CPU 空闲、不执行任何实际工作时，才使用 :c:func:`k_cpu_idle`，如下例所示。

.. code-block:: c

    int main(void)
    {
        /* ... do some system/application initialization */


        /* thread is only used for CPU idling from this point on */
        for (;;) {
            k_cpu_idle();
        }
    }

.. note::
     **除非绝对必要，否则不要使用这些 API。** 在正常系统中，空闲线程会负责电源管理，包括使 CPU 进入空闲状态。

API 参考
********

.. doxygengroup:: cpu_idle_apis
