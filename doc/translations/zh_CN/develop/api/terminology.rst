.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _api_terms:

API 术语
########

以下术语可用作 API 简写标签，表示允许的调用上下文（线程、ISR、内核初始化前）、调用对当前线程状态的影响，以及其他行为特征。

:ref:`api_term_reschedule`
   执行函数时会到达重新调度点
:ref:`api_term_sleep`
   执行函数可能使调用线程睡眠
:ref:`api_term_no-wait`
   函数的某个参数可以阻止调用线程尝试睡眠
:ref:`api_term_isr-ok`
   无论从中断上下文还是线程上下文调用，函数都可以安全执行并产生规定效果
:ref:`api_term_pre-kernel-ok`
   内核完全初始化之前也可以安全调用，并产生规定效果
:ref:`api_term_async`
   函数可能在其启动的操作完成之前返回，即函数返回与操作完成是异步的
:ref:`api_term_supervisor`
   调用线程必须具有特权权限才能执行函数

各属性对行为的具体影响见以下各节。

.. _api_term_reschedule:

reschedule（重新调度）
======================

reschedule 属性表示函数执行期间可能到达 :ref:`重新调度点 <scheduling_v2>`。

详情
----

此属性意味着：线程调用可重新调度的函数时，可能因更高优先级线程变为就绪而暂停执行。是否实际暂停，取决于重新调度点对应的操作，以及调用线程和就绪队列队首线程的相对优先级。

注意，使用时间片或在中断中执行重新调度点时，任何线程都可能在任何函数中暂停执行。

不具有 **reschedule** 属性的函数，可以从线程或中断上下文调用。

具有 **reschedule** 属性的函数，可以从线程上下文调用。

具有 **reschedule** 但不具有 **sleep** 属性的函数，可以从中断上下文调用。

.. _api_term_sleep:

sleep（睡眠）
=============

sleep 属性表示函数可能使调用线程 :ref:`睡眠 <scheduling_v2>`。

说明
----

对于仅使用不可抢占线程的应用，此属性尤其重要，因为除非正在运行的纯协作式线程显式调用了导致其睡眠的操作，否则内核不会在重新调度点将其换下。

此属性不表示函数必然睡眠，而是表示调用线程可能需要先暂停、等待或调用 :c:func:`k_yield`，才能完成操作。**no-wait** 可能改变此行为。

具有 **sleep** 属性的函数隐含具有 **reschedule** 属性。

具有 **sleep** 属性的函数可以从线程上下文调用。

当且仅当使用 **no-wait** 模式时，具有 **sleep** 属性的函数才可以从中断或内核初始化前上下文调用。

.. _api_term_no-wait:

no-wait（不等待）
=================

no-wait 属性用于同时具有 **sleep** 属性的函数，表示可通过某个参数强制选择不会使调用线程睡眠的执行路径。

Explanation
-----------

典型的 no-wait 函数接受超时参数，可以向其传入 :c:macro:`K_NO_WAIT`。此特殊超时值的含义是：如果操作可以立即完成，就执行；否则返回错误码，而不进入睡眠。

正是 no-wait 功能使 :c:func:`k_sem_take` 等函数可以从 ISR 调用，因为中断上下文中不允许睡眠。

函数存在 no-wait 路径，并不意味着选择该路径就能保证函数是同步的。

具有此属性的函数，只有在参数选择 no-wait 路径时，才可以从中断或内核初始化前上下文调用。

.. _api_term_isr-ok:

isr-ok（可在 ISR 中调用）
=========================

isr-ok 属性表示函数从中断上下文或线程上下文调用都能正常工作。

Explanation
-----------

任何不具有 **sleep** 属性的函数，天然具有 **isr-ok** 属性。具有 **sleep** 属性的函数，如果实现能确保从中断上下文调用时仍符合文档行为，也可以具有 **isr-ok** 属性。例如，实现可以检测调用上下文，将会睡眠的操作转交线程；也可以在文档中规定从非线程上下文调用时返回特定错误，通常为 ``-EWOULDBLOCK``。

注意，具有 **no-wait** 属性的函数，仅在选择 no-wait 路径时才能安全地从中断上下文调用。**isr-ok** 函数不一定需要提供 no-wait 路径。

.. _api_term_pre-kernel-ok:

pre-kernel-ok（可在内核初始化前调用）
=====================================

pre-kernel-ok 属性表示即使在内核主线程启动前调用，函数也能按照文档工作。

Explanation
-----------

此属性的作用类似 **isr-ok**，但面向的是可能在 ``PRE_KERNEL_1`` 或 ``PRE_KERNEL_2`` 初始化级别执行的 :c:macro:`DEVICE_DEFINE()` 或 :c:macro:`SYS_INIT()` 调用中使用的 API。

通常，具有 **pre-kernel-ok** 属性的函数会通过 :c:func:`k_is_pre_kernel` 判断是否能够完成规定行为。很多情况下还会检查 :c:func:`k_is_in_isr`，从而同时支持 **isr-ok**。

.. _api_term_async:

async（异步）
=============

如果函数可能在它启动的操作完成之前返回，则具有 **async** （异步）属性。异步函数通常通过回调或事件等机制报告操作完成。

非异步函数就是同步函数，即函数返回时操作一定已经完成。由于大多数函数是同步的，因此不使用单独属性标识此行为。

Explanation
-----------

注意，**async** 与上下文切换互相独立。某些 API 可能通过回调提供完成信息，但在等待启动操作所需的资源时仍会暂停执行，例如 :c:func:`spi_transceive_signal`。

如果函数同时具有 **no-wait** 和 **async** 属性，选择 no-wait 路径只保证函数不会睡眠，不影响操作是否会在函数返回前完成。

.. _api_term_supervisor:

supervisor（特权模式）
======================

supervisor 属性只与用户模式应用有关，表示函数不能从用户模式调用。
