.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _workqueues_v2:

工作队列线程
############

.. contents::
    :local:
    :depth: 1

:dfn:`工作队列` 是一种内核对象，它使用专用线程按先进先出的顺序处理工作项。每个工作项通过调用其指定的函数进行处理。ISR 或高优先级线程通常使用工作队列，将非紧急处理交给低优先级线程，以免影响对时间敏感的处理。

可以定义任意数量的工作队列（仅受可用 RAM 限制）。每个工作队列通过其内存地址引用。

工作队列具有以下主要属性：

* 由已添加但尚未处理的工作项组成的 **队列**。

* 处理队列中工作项的 **线程**。线程优先级可配置，因此可根据需要设为协作式或抢占式线程。

无论工作队列线程的优先级如何，它都会在处理相邻的已提交工作项之间让出 CPU，以防止协作式工作队列使其他线程饥饿。

工作队列必须先初始化才能使用。初始化会清空队列并创建工作队列线程。该线程持续运行，但在没有可用工作项时会休眠。

工作项生命周期
**************

可以定义任意数量的 **工作项**。每个工作项通过其内存地址引用。

每个工作项都指定一个 **处理函数**，工作队列线程处理该工作项时会执行此函数。函数接受一个参数，即工作项自身的地址。工作项还维护自身的状态信息。

工作项必须先初始化才能使用。初始化会记录工作项的处理函数，并将其标记为非待处理状态。

ISR 或线程可以通过向工作队列提交工作项，使其 **入队** （:c:enumerator:`K_WORK_QUEUED`）。提交操作会将工作项追加到工作队列的队尾。工作队列线程处理完队列中前面的所有工作项后，会取出下一个工作项并调用其处理函数。根据工作队列线程的调度优先级和队列中其他工作项的处理量，已入队的工作项可能很快得到处理，也可能在队列中停留较长时间。

可延迟工作项可以被 **安排** （:c:enumerator:`K_WORK_DELAYED`）到工作队列；参见 `可延迟工作`_。

工作项在工作队列上执行时处于 **运行中** （:c:enumerator:`K_WORK_RUNNING`）状态；如果它在线程请求取消之前已经开始运行，还可能同时处于 **取消中** （:c:enumerator:`K_WORK_CANCELING`）状态。

工作项可以同时处于多个状态；例如，它可以：

* 在某个队列上运行；
* 被标记为取消中（因为某线程使用 :c:func:`k_work_cancel_sync()` 等待工作项完成）；
* 已入队，等待在同一队列上再次运行；
* 已安排在稍后提交到另一个（也可能相同的）队列

以上状态可以 *同时存在*。处于其中任一状态的工作项称为 **待处理** （:c:func:`k_work_is_pending()`）或 **忙碌** （:c:func:`k_work_busy_get()`）。

处理函数可以使用线程可用的任何内核 API。不过，必须谨慎使用可能阻塞的操作（例如获取信号量），因为在处理函数执行完成之前，工作队列无法处理队列中的后续工作项。

如果不需要，处理函数可以忽略传入的唯一参数。如果处理函数需要有关待执行工作的更多信息，可以将工作项嵌入更大的数据结构。随后，处理函数可利用参数值，通过 :c:macro:`CONTAINER_OF` 计算外围数据结构的地址，从而访问所需的额外信息。

工作项通常只初始化一次，此后每当需要执行工作时，就提交到指定工作队列。如果 ISR 或线程尝试提交已经入队的工作项，工作项不会受到影响；它会保留在队列中的当前位置，工作只执行一次。

处理函数可以将作为参数传入的工作项重新提交到工作队列，因为此时该工作项已不在队列中。这允许处理函数分阶段执行工作，而不会过度延迟队列中其他工作项的处理。

.. important::
    待处理的工作项在工作队列线程处理它之前 *不得* 修改。这意味着不能在工作项忙碌时重新初始化它。此外，工作项处理函数执行工作所需的任何附加信息，也不得在处理函数执行完毕前修改。

.. _k_delayable_work:

可延迟工作
**********

ISR 或线程可能需要安排一个工作项，使其在指定时间之后才被处理，而不是立即处理。可以通过 **安排** 一个 **可延迟工作项**，使其在未来某个时刻提交到工作队列。

可延迟工作项包含一个标准工作项，并增加了记录应在何时、向哪个队列提交该工作项的字段。

可延迟工作项的初始化和安排方式与标准工作项类似，但使用不同的内核 API。发出安排请求时，内核会启动超时机制，在指定延时结束后触发。超时发生后，内核将工作项提交到指定工作队列，工作项随后在队列中等待，直到按标准方式得到处理。

请注意，可延迟工作使用的处理函数仍接收指向底层非延迟工作结构的指针，该结构在 :c:struct:`k_work_delayable` 中并不公开。要访问包含可延迟工作对象的外围对象，请使用以下惯用写法：

.. code-block:: c

   static void work_handler(struct k_work *work)
   {
           struct k_work_delayable *dwork = k_work_delayable_from_work(work);
           struct work_context *ctx = CONTAINER_OF(dwork, struct work_context,
                                                   timed_work);
           ...


触发式工作
**********

:c:func:`k_work_poll_submit` 接口安排一个响应 **轮询事件** 的触发式工作项（参见 :ref:`polling_v2`）。当被监视的资源可用、轮询信号被触发或超时发生时，它会调用用户定义的函数。与 :c:func:`k_poll` 不同，触发式工作不需要专用线程等待或主动轮询事件。

触发式工作项是在标准工作项基础上增加以下属性的工作项：

* 指向轮询事件数组的指针，这些事件会触发工作项提交到工作队列

* 轮询事件数组的大小。

触发式工作项的初始化和提交方式与标准工作项类似，但使用专用内核 API。发出提交请求时，内核开始监视轮询事件指定的内核对象。一旦至少一个被监视的内核对象状态发生变化，工作项就会提交到指定工作队列，并在队列中等待，直到按标准方式得到处理。

.. important::
    在触发式工作项的整个生命周期内，即从提交到工作项执行或取消，工作项及其引用的轮询事件数组都必须保持有效，且不能被修改。

只要触发式工作项仍在等待轮询事件，ISR 或线程就可以 **取消** 已提交的工作项。此时，内核停止等待关联的轮询事件，并且不会执行指定工作。否则，无法取消。

系统工作队列
************

内核定义了一个称为 *系统工作队列* 的工作队列，任何需要工作队列支持的应用程序或内核代码都可使用它。系统工作队列是可选的，只有应用程序使用它时才会存在。

.. important::
    每个新工作队列都会产生显著的内存开销，因此仅在无法将新工作项提交到系统工作队列时，才应定义额外工作队列。如果新工作项与现有系统工作队列工作项共存会造成不可接受的影响，便有理由创建新队列；例如，新工作项执行阻塞操作，会使系统工作队列的其他处理遭受不可接受的延迟。

    另请注意：系统工作队列默认使用最低的协作式优先级。这意味着排空系统工作队列优先于 *所有抢占式线程*。将系统工作队列配置为抢占式优先级存在风险，因为子系统和驱动程序可能隐含依赖于工作项在协作式上下文中执行。因此，低优先级任务可能更适合使用独立的低优先级工作队列。

如何使用工作队列
****************

定义和控制工作队列
==================

工作队列使用 :c:struct:`k_work_q` 类型的变量定义。初始化工作队列时，先定义其线程使用的栈区域，通过清零内存或调用 :c:func:`k_work_queue_init` 初始化 :c:struct:`k_work_q`，然后调用 :c:func:`k_work_queue_start`。栈区域必须使用 :c:macro:`K_THREAD_STACK_DEFINE` 定义，以确保其在内存中得到正确设置。

以下代码定义并初始化工作队列：

.. code-block:: c

    #define MY_STACK_SIZE 512
    #define MY_PRIORITY 5

    K_THREAD_STACK_DEFINE(my_stack_area, MY_STACK_SIZE);

    struct k_work_q my_work_q;

    k_work_queue_init(&my_work_q);

    k_work_queue_start(&my_work_q, my_stack_area,
                       K_THREAD_STACK_SIZEOF(my_stack_area), MY_PRIORITY,
                       NULL);

此外，可以通过可选的最后一个参数控制队列标识以及与线程重新调度相关的某些行为；详情参见 :c:func:`k_work_queue_start()`。

可以使用以下 API 操作工作队列：

* :c:func:`k_work_queue_drain()` 可阻塞调用者，直到工作队列中没有剩余工作项。排空队列期间，仍接受工作队列线程重新提交的工作项，但拒绝其他线程或 ISR 提交的工作项。禁止提交更多工作的限制可以在排空操作完成后继续保留，以便原先阻塞的线程在队列被“封堵”时执行额外工作。请注意，排空队列不影响可延迟工作项的安排或处理，但如果队列被封堵且截止时间到达，工作项会静默提交失败。
* :c:func:`k_work_queue_unplug()` 解除此前排空操作对向队列提交工作项施加的限制。

提交工作项
==========

工作项使用 :c:struct:`k_work` 类型的变量定义。必须调用 :c:func:`k_work_init` 初始化，除非使用 :c:macro:`K_WORK_DEFINE` 定义，此时会在编译时完成初始化。

已初始化的工作项可通过调用 :c:func:`k_work_submit` 提交到系统工作队列，或通过调用 :c:func:`k_work_submit_to_queue` 提交到指定工作队列。

以下代码演示 ISR 如何将错误消息打印工作交给系统工作队列。请注意，如果 ISR 在工作项仍在队列中时尝试重新提交，工作项会保持不变，对应的错误消息不会被打印。

.. code-block:: c

    struct device_info {
        struct k_work work;
        char name[16]
    } my_device;

    void my_isr(void *arg)
    {
        ...
        if (error detected) {
            k_work_submit(&my_device.work);
        }
        ...
    }

    void print_error(struct k_work *item)
    {
        struct device_info *the_device =
            CONTAINER_OF(item, struct device_info, work);
        printk("Got error on device %s\n", the_device->name);
    }

    /* initialize name info for a device */
    strcpy(my_device.name, "FOO_dev");

    /* initialize work item for printing device's error messages */
    k_work_init(&my_device.work, print_error);

    /* install my_isr() as interrupt handler for the device (not shown) */
    ...


可以使用以下 API 检查工作项状态或与工作项同步：

* :c:func:`k_work_busy_get()` 返回表示工作项状态的标志快照。值为零表示工作项未被安排、未被提交、未在执行，也未以其他方式被工作队列基础设施引用。
* :c:func:`k_work_is_pending()` 是一个辅助函数，当且仅当工作项已被安排、已入队或正在运行时返回 ``true``。
* 线程可以调用 :c:func:`k_work_flush()`，阻塞直到工作项完成。如果工作项不处于待处理状态，则立即返回。
* :c:func:`k_work_cancel()` 尝试阻止工作项执行，但不保证成功。可安全地从 ISR 调用此函数。
* 线程可以调用 :c:func:`k_work_cancel_sync()`，阻塞直到工作完成；如果取消成功或无需取消（工作项未被提交或未在运行），则立即返回。在 ISR 调用 :c:func:`k_work_cancel()` 后，可以使用此函数确认 ISR 发起的取消操作已经完成。

安排可延迟工作项
================

可延迟工作项使用 :c:struct:`k_work_delayable` 类型的变量定义。必须通过调用 :c:func:`k_work_init_delayable` 初始化。

延迟工作有两种常见用法，区别在于新事件发生时是否应延长截止时间。例如，收集异步到达的数据，如连接键盘的 UART 接收到的字符。有两个 API 可以在延时后提交工作：

* :c:func:`k_work_schedule()` （或 :c:func:`k_work_schedule_for_queue()`）安排工作在指定时间或延时后执行。在延时结束之前再次使用此 API 安排同一工作项，不会改变它提交到队列的时间。如果策略是从收到 **第一份** 尚未处理的数据开始，持续收集数据直到指定延时结束，请使用此 API；
* :c:func:`k_work_reschedule()` （或 :c:func:`k_work_reschedule_for_queue()`）无条件设置工作的截止时间，替换之前任何尚未完成的延时，并在必要时更改目标队列。如果策略是从收到 **最后一份** 尚未处理的数据开始，持续收集数据直到指定延时结束，请使用此 API。

如果工作项尚未被安排，这两个 API 的行为相同。如果延时指定为 :c:macro:`K_NO_WAIT`，其行为等同于立即将工作项直接提交到目标队列，无需等待最短超时（使用 :c:func:`k_work_schedule()` 且此前的延时尚未完成时除外）。

两者也都有允许指定提交目标队列的版本。

辅助函数 :c:func:`k_work_delayable_from_work()` 可以根据传入工作处理函数的 :c:struct:`k_work` 指针，获取指向其所属 :c:struct:`k_work_delayable` 的指针。

还可以使用以下 API 检查工作项状态或与工作项同步：

* :c:func:`k_work_delayable_busy_get()` 对应于 :c:func:`k_work_busy_get()`，用于可延迟工作。
* :c:func:`k_work_delayable_is_pending()` 对应于 :c:func:`k_work_is_pending()`，用于可延迟工作。
* :c:func:`k_work_flush_delayable()` 对应于 :c:func:`k_work_flush()`，用于可延迟工作。
* :c:func:`k_work_cancel_delayable()` 对应于 :c:func:`k_work_cancel()`，用于可延迟工作；:c:func:`k_work_cancel_delayable_sync()` 也有类似的对应关系。

与工作项同步
============

虽然可以从任何上下文中使用 :c:func:`k_work_busy_get()` 和 :c:func:`k_work_delayable_busy_get()` 获取普通工作项和可延迟工作项的状态，但某些用法需要在提交后与工作项同步。可在线程上下文中调用 :c:func:`k_work_flush()`、:c:func:`k_work_cancel_sync()` 和 :c:func:`k_work_cancel_delayable_sync()`，等待达到请求的状态。

这些 API 必须接收一个 :c:struct:`k_work_sync` 对象。该对象没有供应用程序检查的成员，但用于提供所需的同步对象。如果代码需要在启用 :kconfig:option:`CONFIG_KERNEL_COHERENCE` 的架构上工作，就不应将这些对象分配在栈上。

工作队列最佳实践
****************

避免竞态条件
============

有时工作项需要处理的数据天然是线程安全的，例如某个线程将数据放入 :c:struct:`k_queue`，再由工作线程处理。更多时候，需要外部同步来避免数据竞争，即工作线程检查或操作的共享状态同时被另一个线程或中断访问的情况。这种状态可以是表示需要执行工作的标志，也可以是由 ISR 或线程填充、由工作处理函数读取的共享对象。

对于简单标志，:ref:`atomic_v2` 可能已足够。其他情况下，可使用自旋锁（:c:struct:`k_spinlock`）或感知线程的锁（:c:struct:`k_sem`、:c:struct:`k_mutex` 等）来确保不发生数据竞争。

如果所选锁机制可能 :ref:`api_term_sleep`，允许工作线程休眠就会使队列中的其他工作项饥饿，而这些工作项可能需要继续执行才能释放该锁。工作处理函数应尝试以不等待的方式获取锁。例如：

.. code-block:: c

   static void work_handler(struct work *work)
   {
           struct work_context *parent = CONTAINER_OF(work, struct work_context,
                                                      work_item);

           if (k_mutex_lock(&parent->lock, K_NO_WAIT) != 0) {
                   /* NB: Submit will fail if the work item is being cancelled. */
                   (void)k_work_submit(work);
                   return;
           }

           /* do stuff under lock */
           k_mutex_unlock(&parent->lock);
           /* do stuff without lock */
   }

请注意，如果锁由优先级低于工作队列的线程持有，重新提交可能使负责释放锁的线程饥饿，从而导致应用程序失败。需要使用上述写法时，最好使用可延迟工作项，并以非零延时安排（或重新安排）工作，让持锁线程有机会继续执行。

请注意，如果工作项已被取消，从处理函数中提交工作可能失败。通常这是可以接受的，因为处理函数结束后取消操作就会完成。如果不能接受，上述代码必须采取其他步骤，通知应用程序工作未能执行。

工作项自身具有内部锁保护，因此仅为提交或安排工作项，无需持有外部锁。即使使用受外部锁保护的状态来阻止进一步重新提交，只要能确保工作项最终会获取该锁并检查状态，以判断是否需要执行操作，重新提交就是安全的。如果可延迟工作项因无法获取锁而在其处理函数中重新安排，则需要其他具有自身同步保护的状态，例如应用程序或驱动程序在发起取消时设置的原子标志，以检测取消操作，避免已取消的工作项在截止时间到达后再次提交。

检查返回值
==========

所有工作 API 函数都会返回底层操作的状态。在许多情况下，必须检查预期结果是否已实现。

* 如果工作项正在取消，或者队列不接受新工作项，提交工作项（:c:func:`k_work_submit_to_queue`）可能失败。此时工作不会执行，可能导致依赖工作处理函数活动来推进的子系统失去响应。
* 异步取消（:c:func:`k_work_cancel` 或 :c:func:`k_work_cancel_delayable`）可能在处理函数仍在运行工作项时返回。此后继续操作与工作处理函数共享的状态，会产生可能导致故障的数据竞争。

Zephyr 代码中曾出现许多因未检查操作结果而产生的竞态条件。

有时，有充分理由认为返回值所表示的操作未按预期完成并不是问题。在这些情况下，代码应明确说明：(1) 将返回值强制转换为 ``void``，表示有意忽略结果；(2) 记录意外情况发生时的行为。例如：

.. code-block:: c

   /* If this fails, the work handler will check pub->active and
    * exit without transmitting.
    */
   (void)k_work_cancel_delayable(&pub->timer);

不过，即使如此，后续代码仍必须避免数据竞争，因为无法保证工作线程没有在访问与工作相关的状态。

不要过早优化
============

工作队列 API 的设计保证了从多个线程和中断中调用时的安全性。尝试从外部检查工作项状态并据此作出决策，很可能引入新问题。

因此，有新工作时直接提交即可。不要尝试通过 :c:func:`k_work_is_pending` 或 :c:func:`k_work_busy_get` 检查状态快照，判断工作项是否已提交，或通过 :c:func:`k_work_delayable_remaining_get()` 检查是否存在非零延时来进行“优化”。这些检查并不可靠：“忙碌”状态在检查返回时可能已经过时；如果工作从多个上下文提交，或者对于可延迟工作，截止时间已到但工作仍处于排队或运行状态，那么“非忙碌”状态也可能有误。

通常，最佳做法是在共享状态中始终维护一个可由处理函数检查的条件，以确认是否有工作需要执行。这样便可将工作处理函数作为标准的清理路径：无需在工作项提交处处理取消和清理，而可能将所有操作都放在工作处理函数自身中完成。

在极少数情况下，可以安全地使用 :c:func:`k_work_is_pending` 进行检查，以避免调用 :c:func:`k_work_flush` 或 :c:func:`k_work_cancel_sync`：前提是你 *确定* 在检查期间没有其他代码可能提交此工作项（通常是因为持有某把锁，阻止访问用于提交工作的状态）。

使用建议
********

使用系统工作队列，将复杂的中断相关处理从 ISR 推迟到共享线程中执行。这样可以及时完成中断相关处理，又不影响系统响应后续中断的能力，而且无需应用程序定义和管理额外的处理线程。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`
* :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_PRIORITY`
* :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_NO_YIELD`

API 参考
********

.. doxygengroup:: workqueue_apis
