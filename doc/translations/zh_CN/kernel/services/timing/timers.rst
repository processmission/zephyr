.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _timers_v2:

定时器
######

:dfn:`定时器` 是利用内核系统时钟测量经过时间的内核对象。到达指定时限时，定时器可以执行应用定义的操作，也可以仅记录到期事件，等待应用读取其状态。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的定时器（仅受可用 RAM 的限制）。每个定时器通过其内存地址引用。

定时器具有以下主要属性：

* **持续时间**，指定定时器首次到期前的时间间隔。这是一个 :c:type:`k_timeout_t` 值，可使用不同单位进行初始化。

* **周期**，指定首次到期后各次到期之间的时间间隔，同样是 :c:type:`k_timeout_t` 值，且必须非负。周期为 ``K_NO_WAIT`` （即零）或 ``K_FOREVER`` 表示该定时器为单次定时器，到期一次后即停止。（例如，若启动定时器时持续时间设为 200、周期设为 75，则会在 200 ms 后首次到期，此后每隔 75 ms 到期一次。）

* **到期函数**，每次定时器到期时执行。该函数由系统时钟中断处理程序执行。如果不需要到期函数，可以将函数指定为 ``NULL``。

* **停止函数**，当运行中的定时器被提前停止时执行。该函数由停止定时器的线程执行。如果不需要停止函数，可以将函数指定为 ``NULL``。

* **状态** 值，表示自上次读取状态值以来，定时器已到期的次数。

定时器使用前必须初始化。初始化会指定到期函数和停止函数，将定时器状态置零，并将定时器置于 **停止** 状态。

通过指定持续时间和周期来 **启动** 定时器。其状态会重置为零，随后定时器进入 **运行** 状态，开始倒计时直至到期。

.. note::

   定时器的持续时间是相对于启动时刻的 **最小** 延迟。定时器的周期是相对于上次“应当”到期时刻的 **最小** 延迟。这意味着周期定时器不会相对于系统定时器产生漂移，实际的周期间隔可能短于或长于指定周期。

   若要保证定时器到期前的最小延迟，应在 **到期函数** 内或定时器到期后重新启动定时器。

   延迟的变化来自系统中的不确定因素，例如中断处理延迟和先前定时器处理程序的执行时间。

运行中的定时器到期时，其状态值递增，并执行到期函数（如果存在）；如果有线程正在等待该定时器，则解除其阻塞。如果定时器周期为零，定时器进入停止状态；否则，定时器重新启动，新的持续时间根据“应当”到期的时刻和周期计算，使下次到期对齐到预定周期。

如有需要，可以在倒计时期间停止运行中的定时器。定时器状态值保持不变，然后进入停止状态并执行停止函数（如果存在）。如果有线程正在等待该定时器，则解除其阻塞。允许尝试停止未运行的定时器，但由于它已经停止，因此不会产生任何影响。

如有需要，可以在倒计时期间重新启动运行中的定时器。定时器状态重置为零，然后使用调用者指定的新持续时间和周期开始倒计时。如果有线程正在等待该定时器，则继续等待。

可以随时直接读取定时器状态，以确定自上次读取状态以来定时器到期的次数。读取状态会将其值重置为零。还可以读取定时器到期前的剩余时间；值为零表示定时器已停止。

线程可以通过与定时器 **同步** 来间接读取其状态。这会阻塞线程，直到定时器状态非零（表示至少到期过一次）或定时器被停止；如果状态已非零或定时器已停止，线程无需等待即可继续。同步操作返回定时器状态，并将其重置为零。

.. note::
    对于任意一个定时器，应当只有一个使用者检查其状态，因为无论直接还是间接读取状态都会改变其值。同样，同一时刻应当只有一个线程与给定定时器同步。ISR 不允许与定时器同步，因为 ISR 不允许阻塞。

定时器观察者
************

启用 :kconfig:option:`CONFIG_TIMER_OBSERVER` 后，代码可以注册 :dfn:`定时器观察者`，接收系统中所有定时器的生命周期事件通知。观察者由一组可选回调组成，在定时器初始化、启动、停止或到期时调用。这使外部模块（例如跟踪、性能分析或电源管理代码）能够响应定时器活动，而无需修改内核内部实现或各个定时器。

通过 :c:macro:`K_TIMER_OBSERVER_DEFINE` 静态定义观察者，该宏接受指向 ``on_init``、``on_start``、``on_stop`` 和 ``on_expiry`` 回调的指针；不需要的回调可传入 ``NULL``。由于到期回调在中断上下文中运行，因此必须保持简短且不能阻塞。

实现
****

定义定时器
==========

使用 :c:struct:`k_timer` 类型的变量定义定时器，然后必须调用 :c:func:`k_timer_init` 将其初始化。

以下代码定义并初始化一个定时器。

.. code-block:: c

    struct k_timer my_timer;
    extern void my_expiry_function(struct k_timer *timer_id);

    k_timer_init(&my_timer, my_expiry_function, NULL);

也可以通过调用 :c:macro:`K_TIMER_DEFINE`，在编译时定义并初始化定时器。

以下代码与上面的代码片段具有相同效果。

.. code-block:: c

    K_TIMER_DEFINE(my_timer, my_expiry_function, NULL);

使用定时器到期函数
==================

以下代码使用定时器定期执行一项较复杂的操作。由于所需工作无法在中断上下文中完成，定时器的到期函数会向 :ref:`系统工作队列 <workqueues_v2>` 提交工作项，由工作队列线程执行该工作。

.. code-block:: c

    void my_work_handler(struct k_work *work)
    {
        /* do the processing that needs to be done periodically */
        ...
    }

    K_WORK_DEFINE(my_work, my_work_handler);

    void my_timer_handler(struct k_timer *dummy)
    {
        k_work_submit(&my_work);
    }

    K_TIMER_DEFINE(my_timer, my_timer_handler, NULL);

    ...

    /* start a periodic timer that expires once every second */
    k_timer_start(&my_timer, K_SECONDS(1), K_SECONDS(1));

读取定时器状态
==============

以下代码直接读取定时器状态，以确定定时器是否已到期。

.. code-block:: c

    K_TIMER_DEFINE(my_status_timer, NULL, NULL);

    ...

    /* start a one-shot timer that expires after 200 ms */
    k_timer_start(&my_status_timer, K_MSEC(200), K_NO_WAIT);

    /* do work */
    ...

    /* check timer status */
    if (k_timer_status_get(&my_status_timer) > 0) {
        /* timer has expired */
    } else if (k_timer_remaining_get(&my_status_timer) == 0) {
        /* timer was stopped (by someone else) before expiring */
    } else {
        /* timer is still running */
    }

使用定时器状态同步
==================

以下代码通过定时器状态同步，使线程能够执行其他有效工作，同时确保两次协议操作之间具有指定的时间间隔。

.. code-block:: c

    K_TIMER_DEFINE(my_sync_timer, NULL, NULL);

    ...

    /* do first protocol operation */
    ...

    /* start a one-shot timer that expires after 500 ms */
    k_timer_start(&my_sync_timer, K_MSEC(500), K_NO_WAIT);

    /* do other work */
    ...

    /* ensure timer has expired (waiting for expiry, if necessary) */
    k_timer_status_sync(&my_sync_timer);

    /* do second protocol operation */
    ...

.. note::
    如果线程没有其他工作要做，可以直接在两次协议操作之间休眠，而无需使用定时器。

使用建议
********

使用定时器在指定时间后发起异步操作。

使用定时器判断指定时间是否已经过去。尤其是当所需精度和／或时间单位控制能力超过较简单的 :c:func:`k_sleep` 和 :c:func:`k_usleep` 调用所能提供的范围时，应使用定时器。

使用定时器，在执行有时间限制的操作期间开展其他工作。

.. note::
   如果线程需要测量某项操作的耗时，可以直接读取 :ref:`系统时钟或硬件时钟 <kernel_timing>`，无需使用定时器。

配置选项
********

相关配置选项：

* 无

API 参考
********

.. doxygengroup:: timer_apis
