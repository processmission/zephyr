.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _kernel_timing:

内核计时
########

Zephyr 提供稳健且可扩展的计时框架，能够基于任意精度的硬件计时源报告和跟踪定时事件。

时间单位
========

内核使用多种单位跟踪时间，以满足不同用途。

向应用代码提供时间时，默认采用通常以毫秒或微秒表示的实际时间值。这种表示具有普遍可移植、易于理解的优点，但不一定与底层硬件的精度完全匹配。

内核通过 :c:func:`k_cycle_get_32` 和 :c:func:`k_cycle_get_64` API 提供“周期”计数。其设计目标是提供操作系统能向用户暴露的最快周期计数器（例如 CPU 周期计数器），且读取操作应非常快速。对时序非常敏感的应用代码可以通过轮询此计数器获得最高精度。可通过 :c:func:`sys_clock_hw_cycles_per_sec` 获取该计数器的频率。在大多数平台上，它是一个运行时常量，值为 :kconfig:option:`CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC`，在系统整个运行期间保持不变。在系统定时器频率不固定的平台上，:c:func:`sys_clock_hw_cycles_per_sec` 返回运行时值，应用代码不能假设频率始终不变。

运行时系统定时器频率
--------------------

某些平台需要在运行时获取系统定时器频率，原因可能是定时器驱动程序从硬件探测时钟频率，或定时器时钟频率在启动后可能改变。

能够在运行时更改当前系统定时器频率的平台必须启用 :kconfig:option:`CONFIG_SYSTEM_CLOCK_HW_CYCLES_PER_SEC_RUNTIME_UPDATE`，并执行以下操作：

* 应用时钟变更后，调用 :c:func:`z_sys_clock_hw_cycles_per_sec_update`。
* 如果系统定时器驱动程序缓存了派生常量（例如每个时钟节拍的周期数），或需要在时钟改变时重新配置硬件，则应由定时器驱动程序覆盖 :c:func:`z_sys_clock_hw_cycles_per_sec_update`。

:c:func:`z_sys_clock_hw_cycles_per_sec_update` 的默认实现仅更新保存的频率值。

.. note::

  :kconfig:option:`CONFIG_SYSTEM_CLOCK_HW_CYCLES_PER_SEC_RUNTIME_UPDATE` 将系统定时器频率作为单个 **全局** 值进行跟踪。它不兼容各 CPU 可能观察到不同系统定时器频率的按 CPU 调频配置。

  启用后，:c:func:`sys_clock_hw_cycles_per_sec` 和时间单位转换均遵循当前运行时值。

对于异步计时，内核定义了“时钟节拍”（tick）的概念。时钟节拍是内核记录运行时间和超时所用的内部计数单位。在实际可行的范围内，中断应在时钟节拍边界触发，内核不记录不足一个时钟节拍的部分。时钟节拍频率可通过 :kconfig:option:`CONFIG_SYS_CLOCK_TICKS_PER_SEC` 配置。大多数支持任意设置中断超时的硬件平台，默认值预计在 10 kHz 左右；软件仿真平台和旧版驱动程序则使用较传统的 100 Hz。

转换
----

Zephyr 提供覆盖各种组合且可控制舍入方式的时间单位转换库。“ms”（毫秒）、“us”（微秒）、“tick”（时钟节拍）和“cyc”（周期）可相互转换。每种转换均提供“floor”（向下取整至输出单位）、“ceil”（向上取整）和“near”（舍入至最接近的值）三种舍入方式。还可将输出精度指定为 32 位或 64 位。

例如，:c:func:`k_ms_to_ticks_ceil32` 将输入的毫秒值向上取整转换为时钟节拍数，并返回截断为 32 位精度的结果；:c:func:`k_cyc_to_us_floor64` 则以完整的 64 位精度将测得的周期数向下取整转换为经过的微秒数。完整的转换函数列表请参见参考文档。

在大多数平台上，如果各计数器频率互为整数倍，且输出能容纳在单个机器字中，这些转换会展开为 2 至 4 步操作序列，只在实际需要且请求时才使用完整精度。

.. _kernel_timing_uptime:

运行时间
========

内核为应用维护系统运行时间计数。可随时通过 :c:func:`k_uptime_get` 获取自系统启动以来以毫秒为单位的运行时间。大多数可移植应用代码应使用此函数。

不过，内部实际上使用 64 位整数的时钟节拍计数进行跟踪。具有精确计时需求、且愿意自行转换为可移植实际时间单位的应用，可以通过 :c:func:`k_uptime_ticks` 访问该值。

:c:func:`k_uptime_delta` 可用于获取参考时刻与当前时刻之间经过的时间。参考时刻会更新为当前运行时间，以便计算下一段经过的时间。


超时
====

Zephyr 内核提供了许多带“超时”参数的 API。从概念上说，它表示事件将发生的时刻。例如：

* :c:func:`k_sem_take` 或 :c:func:`k_queue_get` 等内核阻塞操作可指定超时；若到期时仍没有可用数据，函数将返回错误代码。

* 内核 :c:struct:`k_timer` 对象必须为其持续时间和周期指定延迟。

* 内核 :c:struct:`k_work_delayable` API 提供超时参数，指定何时将工作队列项加入系统队列。

这些值均使用 :c:type:`k_timeout_t` 指定。这是一种不透明结构体类型，必须通过一组内核超时宏之一初始化。最常用的 :c:macro:`K_MSEC` 定义相对于当前时刻、以毫秒为单位的延迟时间。

对于相对超时，“当前时刻”的含义取决于上下文：

* 在超时回调内部安排相对超时时（例如在传给 :c:func:`k_timer_init` 的到期函数，或传给 :c:func:`k_work_init_delayable` 的工作处理函数中），“当前时刻”指当前触发的超时最初安排的精确到期时刻，即使“实际时间”已经推进。这确保在另一个定时器回调中安排的定时器，始终以相对于触发该回调的定时器的精确偏移进行计算。因此，可以按固定间隔触发，而不会随时间积累系统性时钟漂移。

* 从应用上下文安排超时时，“当前时刻”指内核接收到超时值时 :c:func:`k_uptime_ticks` 返回的值。

其他超时初始化方式遵循上述单位约定：:c:macro:`K_NSEC()`、:c:macro:`K_USEC`、:c:macro:`K_TICKS` 和 :c:macro:`K_CYC()` 分别指定经过相应数量的纳秒、微秒、时钟节拍和周期后到期的超时值。

:c:type:`k_timeout_t` 值的精度可配置，默认为 32 位。对于以非时钟节拍单位表示的大运行时间计数，回绕语义较为复杂，因此长期运行且对时序敏感的应用应配置为使用 64 位超时类型。

最后，还可将超时指定为自系统启动以来的绝对时间。使用 :c:macro:`K_TIMEOUT_ABS_MS` 初始化的超时，会在系统运行时间达到指定值后到期。该 API 也有纳秒、微秒、周期和时钟节拍的变体。

计时内部实现
============

超时队列
--------

所有使用上述 API 指定的 Zephyr :c:type:`k_timeout_t` 事件，都在单个全局事件队列中管理。请求事件的子系统通过回调函数指针指定事件发生时执行的操作，并提供一个 :c:struct:`_timeout` 跟踪结构体。该结构体应嵌入子系统定义的数据结构中，例如 :c:struct:`wait_q` 结构体或 :c:type:`k_tid_t` 线程结构体。

注意，通过 :c:type:`k_timeout_t` 传入的各种单位，都会在插入队列时一次性转换为时钟节拍。内核内部不会执行多次转换，因此无论存在多少事件、超时时间有多长，都能保证时钟节拍级别的精度。

承载队列的数据结构在构建时通过 :kconfig:option:`CONFIG_TIMEOUT_BACKEND` 选择项确定。各后端仅共享前端（时钟节拍通告路径、SMP 重入处理，以及相对和绝对超时规则）；每个后端自行提供队列，因此集成者可根据工作负载选择数据结构，而无需修改公共代码。

默认后端 :kconfig:option:`CONFIG_TIMEOUT_BACKEND_DLIST` 将事件存放在按到期时间排序的双向链表中，每项保存相对于前一项的时钟节拍差值。插入复杂度相对于待处理超时数量为 O(N)：典型系统只有少量待处理超时时开销很低，但数量较多时扩展性较差。以下四种替代后端目前均处于实验阶段，通过增加内存占用或改变行为，换取大规模使用时更快的插入速度：

* :kconfig:option:`CONFIG_TIMEOUT_BACKEND_MINHEAP` 将事件保存在以绝对到期时间为键的二叉最小堆中，使插入和移除的复杂度均为 O(log N)。它要求使用 64 位时钟节拍（:kconfig:option:`CONFIG_TIMEOUT_64BIT`）和固定容量的堆（:kconfig:option:`CONFIG_TIMEOUT_HEAP_MAX_ENTRIES`，溢出将导致致命错误），且不保留同一时钟节拍到期的超时事件的触发顺序。

* :kconfig:option:`CONFIG_TIMEOUT_BACKEND_WHEEL` 是分层时间轮，对于近期事件，插入和移除复杂度为 O(1)，更远期事件则放入有序溢出列表。它的单事件和静态内存占用最大，不保留同一时钟节拍的触发顺序；而且由于下一次超时的估算受时间轮周期限制，会周期性唤醒处于无节拍空闲状态的 CPU，产生其他后端没有的功耗开销。

* :kconfig:option:`CONFIG_TIMEOUT_BACKEND_BUCKET` 是单层分桶差值链表，可视为时间轮的简化形式。在可调的近期时间窗口（:kconfig:option:`CONFIG_TIMEOUT_BUCKET_LISTS`）内，插入复杂度为 O(1)，窗口之外的事件则退回使用有序溢出列表。它也要求使用 64 位时钟节拍，但与时间轮不同，它保留同一时钟节拍的触发顺序，且不会增加空闲唤醒开销。

* :kconfig:option:`CONFIG_TIMEOUT_BACKEND_SKIPLIST` 是以绝对到期时间为键的 Pugh 跳表。插入和移除的期望复杂度为 O(log N)，没有容量限制，且同一时钟节拍的事件按 FIFO 顺序触发。它要求使用 64 位时钟节拍。每个事件保存 :kconfig:option:`CONFIG_TIMEOUT_SKIPLIST_MAX_LEVEL` 个前向指针，因此单事件 RAM 占用高于差值链表或最小堆。

非默认后端面向同时维护大量超时事件的系统，尤其适合事件集中在近期的情况。对于大多数应用，差值链表仍是合适的默认选择。

定时器驱动程序
--------------

时钟节拍级别的内核计时由定时器驱动程序驱动。其接口及运行时的锁定机制见 :ref:`system_timer_drivers`。

时间片
------

计时子系统的辅助职责之一，是向调度器提供时钟节拍计数器，以实现线程时间片。线程时间片不能使用超时值，因为它表示的不是全局到期事件，而是一个按 CPU 维护的值，在 SMP 环境中需要由每个 CPU 独立跟踪。

由于可能没有其他硬件可用于驱动时间片，Zephyr 复用了现有定时器驱动程序。因此，当前调度的是使用时间片的线程时，传给 :c:func:`sys_clock_set_timeout` 的值可能被限制为小于当前下一次超时的值。

保留毫秒 API 的子系统
---------------------

通常，这类代码的移植方式与应用代码相同。子系统可以按需处理用户提供的毫秒值，然后在将其传给内核时使用 :c:macro:`K_MSEC()` 转换为内核超时值。

显然，这意味着无法使用更高精度的超时构造宏或绝对超时等新功能。但对于需求简单的许多子系统，这可能是可以接受的。

一个复杂之处是 :c:macro:`K_FOREVER`。过去其毫秒 API 能接受该值的子系统，现在不再能这样做，因为它已不再是整数类型。这类代码需要改用其他整数值标记来表示“永久”。当然，:c:macro:`K_NO_WAIT` 也有相同的类型安全问题，但它现在和过去都只是数值零，因此有自然的移植方式。

使用 ``k_timeout_t`` 的子系统
-----------------------------

理想情况下，接受“超时”参数来指定等待时间的代码，应尽可能使用内核原生抽象。但 :c:type:`k_timeout_t` 是不透明类型，应用必须先转换它才能检查其内容。

有些转换很简单。需要判断是否为 :c:macro:`K_FOREVER` 的代码，可以直接使用 :c:macro:`K_TIMEOUT_EQ()` 宏对不透明结构体进行相等性检查，再执行特殊处理。

更复杂的情况是，子系统接受超时值后需要在循环中等待其到期，同时执行一些可能多次调用底层内核阻塞操作的处理。例如，考虑以下设计：

.. code-block:: c

    void my_wait_for_event(struct my_subsys *obj, int32_t timeout_in_ms)
    {
        while (true) {
            uint32_t start = k_uptime_get_32();

            if (is_event_complete(obj)) {
                return;
            }

            /* Wait for notification of state change */
            k_sem_take(obj->sem, timeout_in_ms);

            /* Subtract elapsed time */
            timeout_in_ms -= (k_uptime_get_32() - start);
        }
    }

此代码需要检查超时值，而现在已无法这样做。对于此类情况，新 API 提供内部函数 :c:func:`sys_timepoint_calc` 和 :c:func:`sys_timepoint_timeout`，可在任意超时值与基于到期运行时间时钟节拍的时间点值之间转换。因此，这样的循环可以写成：


.. code-block:: c

    void my_wait_for_event(struct my_subsys *obj, k_timeout_t timeout)
    {
        /* Compute the end time from the timeout */
        k_timepoint_t end = sys_timepoint_calc(timeout);

        do {
            if (is_event_complete(obj)) {
                return;
            }

            /* Update timeout with remaining time */
            timeout = sys_timepoint_timeout(end);

            /* Wait for notification of state change */
            k_sem_take(obj->sem, timeout);
        } while (!K_TIMEOUT_EQ(timeout, K_NO_WAIT));
    }

注意，:c:func:`sys_timepoint_calc` 接受特殊值 :c:macro:`K_FOREVER` 和 :c:macro:`K_NO_WAIT`，对绝对超时和常规超时的处理方式相同。反过来，如果创建时间点时使用了这些特殊值，:c:func:`sys_timepoint_timeout` 也可能返回 :c:macro:`K_FOREVER` 或 :c:macro:`K_NO_WAIT`；如果时间点已在过去，也会返回后者。简单场景下还可使用 :c:func:`sys_timepoint_expired`。

不过，使用这些函数的子系统仍需谨慎。注意，相对超时必须相对于某个“当前时刻”解释，显然这里的时刻是调用 :c:func:`sys_timepoint_calc` 的时刻。但用户期望的是其向子系统传入超时值的时刻。因此必须确保该函数只调用一次，并且尽可能紧接着用户代码创建超时值之后调用。不应对“保存下来”的超时值使用它，也绝不应在循环中反复调用。


API 参考
********

.. doxygengroup:: clock_apis
