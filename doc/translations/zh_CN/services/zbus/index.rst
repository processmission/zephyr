.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _zbus:

Zephyr 总线（zbus）
###################

..
   Note to documentation authors: the diagrams included in this documentation page were designed
   using the following Figma library:
   https://www.figma.com/community/file/1292866458780627559/zbus-diagram-assets


:dfn:`Zephyr 总线 - zbus` 是一种轻量级且灵活的软件总线，使线程能够以多对多的方式轻松地相互通信。

.. contents::
    :local:
    :depth: 2

概念
****
线程可以使用 zbus 向一个或多个观察者发送消息。它使多对多通信成为可能。该总线实现了消息传递和发布/订阅通信范式，使线程能够通过共享内存进行同步或异步通信。

通过 zbus 进行的通信基于通道。线程（或回调）使用通道交换消息。此外，除其他操作外，线程还可以发布和观察通道。当线程在通道上发布消息时，总线会将该消息提供给该已发布通道的所有观察者。根据观察者的类型，它可以直接访问消息、接收其副本，甚至只接收所发布通道的引用。

下图展示了一个使用 zbus 的典型应用示例，其中应用逻辑（与硬件无关）通过软件总线与其他线程通信。请注意，这些线程彼此解耦，因为它们只使用 zbus 通道，相互之间无需了解即可通信。


.. figure:: images/zbus_overview.svg
    :alt: zbus 使用概览
    :width: 75%

    典型的 zbus 应用架构。

该总线包括：

* 由控制元数据信息和消息本身组成的通道集合；
* :dfn:`虚拟分布式事件分发器` （VDED），负责向观察者发送通知/消息的总线逻辑。VDED 逻辑在发布操作内部、同一线程上下文中运行，使总线具有分布式执行的概念。当线程向通道发布时，它还会将通知传播给观察者；
* 线程（订阅者和消息订阅者）、回调（监听器），以及异步监听器（推迟到工作队列执行的回调）从总线发布、读取和接收通知。

.. figure:: images/zbus_anatomy.svg
    :alt: ZBus 剖析
    :width: 70%

    ZBus 剖析。

该总线通过通道提供发布、读取、认领、完成、通知和订阅操作。发布、读取、认领和完成在所有 RTOS 线程上下文和 ISR 中均可用。发布和读取操作简单快捷；其过程是先锁定通道，然后在共享内存区域之间进行内存拷贝，最后解锁通道。zbus 的另一个重要方面是观察者。观察者共有四种类型：

.. figure:: images/zbus_type_of_observers.svg
    :alt: ZBus 观察者类型
    :width: 70%

    ZBus 观察者。

* 监听器：一种回调，每当被观察的通道被发布或通知时，事件分发器都会执行该回调；
* 异步监听器：一种回调，每当被观察的通道被发布或通知时，事件分发器都会将其安排到工作队列（默认为系统工作队列）中执行；
* 订阅者：一种基于线程的观察者，内部依赖消息队列；每当被观察的通道被发布或通知时，事件分发器都会将发生变化的通道的引用放入该消息队列。注意，这类观察者不接收消息本身。它应在收到通知后从通道读取消息；
* 消息订阅者：一种基于线程的观察者，内部依赖 FIFO；每当被观察的通道被发布或通知时，事件分发器都会将消息的副本放入该 FIFO。

通道观察结构定义了通道与其观察者之间的关系。每个观察关系都会创建一个通道/观察者对。开发者可以使用 :c:macro:`ZBUS_CHAN_DEFINE` 或 :c:macro:`ZBUS_CHAN_ADD_OBS` 静态分配观察关系。此外还有运行时观察者，使开发者能够创建运行时观察关系。既可以完全禁用一个观察者，也可以单独禁用各个观察关系。事件分发器将忽略已禁用的观察者和观察关系。

.. figure:: images/zbus_observation_mask.svg
    :alt: ZBus observation mask.
    :width: 75%

    ZBus 观察掩码。

上图展示了从 (a) 到 (d) 的一些状态，涉及通道 ``C1`` 到 ``C5``、``Subscriber 1`` 以及各观察关系。最后两个以橙色显示，表示它们是动态分配的（运行时观察关系）。(a) 表明观察者及所有观察关系均已启用。(b) 表明观察者已禁用，因此事件分发器将忽略它。(c) 表明观察者已启用，但有一个静态观察关系被禁用；事件分发器只会停止发送来自通道 ``C3`` 的通知。在 (d) 中，事件分发器将停止向 ``Subscriber 1`` 发送来自通道 ``C3`` 和 ``C5`` 的通知。


假设下图展示了一个常见的基于传感器的解决方案，仅用于说明。定时器被触发后，会向 ``Trigger`` 通道发布。由于传感器线程订阅了 ``Trigger`` 通道，它会收到传感器数据。请注意，VDED 也会执行 ``Blink``，因为它同样监听 ``Trigger`` 通道。当传感器数据准备就绪后，传感器线程将其发布到 ``Sensor data`` 通道。核心线程作为 ``Sensor data`` 通道的消息订阅者接收该消息，处理传感器数据，并将其存储在内部采样缓冲区中。该过程重复进行，直到采样缓冲区满；此时核心线程会汇总采样缓冲区信息，准备一个数据包，并将其发布到 ``Payload`` 通道。LoRa 线程因为是 ``Payload`` 通道的消息订阅者而收到该数据包，并将载荷发送到云端。传输完成后，LoRa 线程向 ``Transmission done`` 通道发布。由于 VDED 监听了 ``Transmission done`` 通道，它会再次执行 ``Blink``。

.. figure:: images/zbus_operations.svg
    :alt: ZBus 基于传感器的应用
    :width: 85%

    ZBus 基于传感器的应用。

这种实现方式使应用更加灵活，使我们能够独立地更改各部分。例如，我们想将触发源从定时器改为按键按下；我们可以这样做，而这一更改不会影响系统的其他部分。同样，如果我们想将通信接口从 LoRa 改为 Bluetooth，只需更改 LoRa 线程，无需其他更改即可使其正常工作。因此，开发者可以对图中的每个模块都这样做。基于此，这表明 zbus 促进了系统架构中的解耦。

使用 zbus 的另一个重要方面是系统模块的复用。如果一段具有明确定义行为的代码（我们称之为模块）只使用 zbus 通道而不使用硬件接口，那么它就能轻松地在其他解决方案中复用。新的解决方案必须实现该模块工作所需的接口（一组通道）。这表明 zbus 可以提高模块复用性。

最后一点重要说明是 zbus 的灵活性。Zbus 提供了许多特性，让开发者可以自由创建适合自身特定需求的解决方案。这些特性包括：

* 消息可以动态或静态分配
* 通知可以是同步或异步的
* 可以通过认领通道以多种方式对通道进行控制
* 可以使用 user-data 字段向通道添加自定义元数据
* 可以使用可选的校验函数来保证消息格式的正确性

这些特性扩展了使用 zbus 可以构建的解决方案范围，使其非常适合作为开源社区工具。

.. _Virtual Distributed Event Dispatcher:

虚拟分布式事件分发器
====================

VDED 的执行始终发生在发布者的上下文中。发布者可以是线程或 ISR。在 ISR 内发布时要小心，因为调度器不会抢占 VDED。请明智地使用这一点。其执行的基本描述如下：


* 获取通道锁；
* 通道通过直接拷贝（使用原始的 :c:func:`memcpy`）接收新消息；
* 事件分发器逻辑按照通道观察者列表中的顺序执行监听器、将消息副本发送给消息订阅者，并将通道的引用推送到订阅者的通知消息队列中。监听器可以直接对常量消息引用进行非拷贝的快速访问（通过 :c:func:`zbus_chan_const_msg` 函数），因为此时通道仍处于锁定状态；
* 最后，发布函数解锁通道。


为了说明 VDED 的执行过程，请参考下面给出的示例。我们有四个优先级递增的线程 ``S1``、``MS2``、``MS1`` 和 ``T1`` （优先级最高）；两个监听器 ``L1`` 和 ``L2``；以及通道 A。假设 ``L1``、``L2``、``MS1``、``MS2`` 和 ``S1`` 都观察通道 A。

.. figure:: images/zbus_publishing_process_example_scenario.svg
    :alt: ZBus 示例场景
    :width: 45%

    ZBus VDED 执行示例场景。


以下代码实现了通道 A。注意 ``struct a_msg`` 仅用于说明。

.. code-block:: c

    ZBUS_CHAN_DEFINE(a_chan,                       /* Name */
             struct a_msg,                         /* Message type */

             NULL,                                 /* Validator */
             NULL,                                 /* User Data */
             ZBUS_OBSERVERS(L1, L2, MS1, MS2, S1), /* observers */
             ZBUS_MSG_INIT(0)                      /* Initial value {0} */
    );


在下图中，字母表示与 VDED 执行相关的某些操作。X 轴表示时间，Y 轴表示线程的优先级。通道 A 的消息以语音气泡表示，它只是一段内存（共享内存）。它多次出现仅用于示意该时刻的消息。


.. figure:: images/zbus_publishing_process_example.svg
    :alt: ZBus 发布处理细节
    :width: 85%

    优先级为 T1 > MS1 > MS2 > S1 时的 ZBus VDED 执行细节。



上图展示了 T1 向通道 A 发布时 VDED 执行期间所执行的操作。因此，下表描述了 VDED 执行的各项活动（以字母表示）。该场景考虑以下优先级：T1 > MS1 > MS2 > S1。T1 的优先级最高。


.. list-table:: 优先级为 T1 > MS1 > MS2 > S1 时的 VDED 执行步骤详解。
   :widths: 5 65
   :header-rows: 1

   * - 操作
     - 描述
   * - a
     - T1 启动，并在某一时刻向通道 A 发布。
   * - b
     - 发布（VDED）过程开始。VDED 锁定通道 A。
   * - c
     - VDED 将 T1 的消息拷贝到通道 A 的消息中。

   * - d, e
     - VDED 按相应顺序执行 L1 和 L2。在监听器内部，通常会调用 :c:func:`zbus_chan_const_msg` 函数，它提供对通道 A 消息的直接常量引用。这很快，且此处无需拷贝。

   * - f, g
     - VDED 拷贝消息并依次发送给 MS1 和 MS2。注意，这些线程在收到通知后立即准备执行。但是，由于它们的优先级低于 T1，因此进入挂起状态。
   * - h
     - VDED 将通知消息推送到 S1 的队列中。注意，该线程在收到通知后立即准备执行。但是，由于通道仍处于锁定状态而无法访问，因此它进入挂起状态。

   * - i
     - VDED 通过解锁通道 A 完成发布。MS1 离开挂起状态并开始执行。

   * - j
     - MS1 执行完毕。MS2 离开挂起状态并开始执行。

   * - k
     - MS2 执行完毕。S1 离开挂起状态并开始执行。

   * - l, m, n
     - 由于通道 A 未锁定，S1 离开挂起状态。它再次获得 CPU 并开始执行。由于它确实收到了来自通道 A 的通知，因此执行了一次通道读取（过程简单：锁定、内存拷贝、解锁），继续执行并离开 CPU。

   * - o
     - S1 完成其工作。


下图展示了 T1 向通道 A 发布时 VDED 执行期间所执行的操作。该场景考虑以下优先级：T1 < MS1 < MS2 < S1。

.. figure:: images/zbus_publishing_process_example2.svg
    :alt: ZBus publish processing detail
    :width: 85%

    优先级为 T1 < MS1 < MS2 < S1 时的 ZBus VDED 执行细节。

因此，下表描述了 VDED 执行的各项活动（以字母表示）。

.. list-table:: 优先级为 T1 < MS1 < MS2 < S1 时的 VDED 执行步骤详解。
   :widths: 5 65
   :header-rows: 1

   * - 操作
     - 描述
   * - a
     - T1 启动，并在某一时刻向通道 A 发布。
   * - b
     - 发布（VDED）过程开始。VDED 锁定通道 A。
   * - c
     - VDED 将 T1 的消息拷贝到通道 A 的消息中。

   * - d, e
     - VDED 按相应顺序执行 L1 和 L2。在监听器内部，通常会调用 :c:func:`zbus_chan_const_msg` 函数，它提供对通道 A 消息的直接常量引用。这很快，且此处无需拷贝。

   * - f
     - VDED 拷贝消息并将其发送给 MS1。MS1 抢占 T1 并开始工作。之后，T1 重新获得 CPU。

   * - g
     - VDED 拷贝消息并将其发送给 MS2。MS2 抢占 T1 并开始工作。之后，T1 重新获得 CPU。

   * - h
     - VDED 将通知消息推送到 S1 的队列中。

   * - i
     - VDED 通过解锁通道 A 完成发布。

   * - j, k, l
     - 由于通道 A 未锁定，S1 离开挂起状态。它再次获得 CPU 并开始执行。由于它确实收到了来自通道 A 的通知，因此执行了一次通道读取（过程简单：锁定、内存拷贝、解锁），继续执行并让出 CPU。


HLP 优先级提升
--------------
ZBus 实现了最高锁定者协议，该协议依据观察者线程的优先级来确定发布者的临时优先级。该协议会考虑通道的最高观察者优先级（HOP）；即使观察者当前没有在等待通道上的消息，也会将其纳入计算。VDED 将根据 HOP 提升发布者的优先级，以确保较小的延迟和尽可能少的抢占。

.. note::
    优先级提升默认启用。要停用它，请禁用 :kconfig:option:`CONFIG_ZBUS_PRIORITY_BOOST` 配置选项。

.. warning::
    ZBus 优先级提升在 HOP 计算中不考虑运行时观察者。

下图展示了 T1 向通道 A 发布时 VDED 执行期间所执行的操作。该场景考虑了优先级提升特性，并采用以下优先级：T1 < MS1 < MS2 < S1。

.. figure:: images/zbus_publishing_process_example_HLP.svg
    :alt: 使用优先级提升时的 ZBus 发布过程细节。
    :width: 85%

    启用优先级提升且优先级为 T1 < MS1 < MS2 < S1 时的 ZBus VDED 执行细节。

要正确使用优先级提升，必须将观察者附加到线程。当订阅者附加到线程时，它会采用该线程的优先级，优先级提升算法将考虑该观察者的优先级。以下代码演示了用于附加线程的函数。


.. code-block:: c
   :emphasize-lines: 10

   ZBUS_SUBSCRIBER_DEFINE(s1, 4);
   void s1_thread(void *ptr1, void *ptr2, void *ptr3)
   {
           ARG_UNUSED(ptr1);
           ARG_UNUSED(ptr2);
           ARG_UNUSED(ptr3);

           const struct zbus_channel *chan;

           zbus_obs_attach_to_thread(&s1);

           while (1) {
                   zbus_sub_wait(&s1, &chan, K_FOREVER);

                   /* Subscriber implementation */

           }
   }
   K_THREAD_DEFINE(s1_id, CONFIG_MAIN_STACK_SIZE, s1_thread, NULL, NULL, NULL, 2, 0, 0);

在上面的代码中，:c:func:`zbus_obs_attach_to_thread` 会将 ``s1`` 观察者设置为优先级二，因为该线程具有该优先级。可以通过使用 :c:func:`zbus_obs_detach_from_thread` 分离观察者来撤销该设置。通道 HOP 计算只会考虑已启用的观察者和观察关系。屏蔽通道的特定观察关系将影响通道 HOP。

总之，该特性的优点包括：

* 对于 zbus 而言，HLP 比互斥锁优先级继承更有效；
* 发布者与观察者之间不会发生有界优先级反转；
* 优先级介于 T1 与 S1 之间、且不参与该通信的其他线程无法抢占 T1，从而避免无界优先级反转；
* 消息订阅者将等待 VDED 完成消息投递过程。因此 VDED 的执行将更快、更一致；
* HLP 优先级是动态的，在运行过程中可能发生变化；
* ZBus 操作可以在 ISR 内使用；
* 可以关闭优先级提升特性，并使用普通信号量作为通道锁定机制；
* 最高锁定者协议的主要缺点（与继承相关的优先级反转）在 zbus 场景中是可以接受的，因为它能确保较小的总线延迟。


限制
====

基于开发者可以使用 zbus 解决许多不同问题这一事实，也会出现一些挑战。ZBus 并不能解决所有问题，因此有必要分析具体情况，以确定 zbus 是否适用。例如，根据 zbus 基准测试，它并不适合线程之间的高速字节流场景。:ref:`管道 <pipes_v2>` 内核对象可以满足这类需求。

投递保证
--------

ZBus 始终会将消息投递给监听器、消息订阅者和异步监听器。但是，对于订阅者，消息投递没有任何保证，因为 zbus 只发送通知，而消息的读取取决于订阅者的实现。遵循以下设计建议可以提高投递率：

* 让监听器尽可能快（像对待 ISR 一样处理它们）。如果需要耗时的处理，请考虑使用异步监听器将其部分或全部工作转移到工作队列。
* 尽量为消费者分配较高的优先级，以避免丢失。
* 为观察者留出空闲的 CPU 时间来消费所产生的数据。
* 对于密集的字节传输，请考虑使用消息队列或管道。

.. warning::
   ZBus 使用 :zephyr_file:`include/zephyr/net_buf.h` （网络缓冲区）与消息订阅者交换数据。因此，考虑到消息订阅者和异步监听器，请谨慎选择配置 :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_SIZE` 和 :kconfig:option:`CONFIG_HEAP_MEM_POOL_ADD_SIZE_ZBUS`，这对正确的 VDED 执行（投递保证）至关重要。如果希望为一组特定通道保留独立的池，可以将 :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_ISOLATION` 与专用池一起使用。请查看 :zephyr:code-sample:`zbus-msg-subscriber` 和 :zephyr:code-sample:`zbus-async-listeners` 示例，了解隔离机制的实际应用。

.. warning::
   订阅者只会收到发生变化的通道的引用。如果在订阅者读取之前该通道被发布了两次，就可能察觉到数据丢失。第二次发布将覆盖第一次的值。因此，订阅者会收到两条通知，但其中只有最后一次的数据。


.. _zbus delivery sequence:

消息投递顺序
------------

消息投递将遵循以下优先级顺序：

#. 在通道中使用 :c:macro:`ZBUS_CHAN_DEFINE` 定义的观察者（按定义顺序）；
#. 使用 :c:macro:`ZBUS_CHAN_ADD_OBS` 定义的观察者，依据序列优先级（该宏的参数）排序；
#. 最后是使用 :c:func:`zbus_chan_add_obs` 添加的运行时观察者，按添加顺序排列。

.. note::
    VDED 将忽略所有已禁用的观察者或观察关系。

用法
****

ZBus 操作依赖于通道和观察者。因此，必须在定义通道时确定通道的消息及其观察者列表，观察者可以静态定义（在通道定义中使用 :c:macro:`ZBUS_CHAN_ADD_OBS`），也可以在运行时定义（参见 `runtime observers`_）。消息是常规的 C 结构体；观察者可以是监听器（同步）、异步监听器（异步）、订阅者（异步）或消息订阅者（异步）。

以下代码定义并初始化一个常规通道及其依赖项。例如，该通道用于交换加速度计数据。

.. code-block:: c

    struct acc_msg {
            int x;
            int y;
            int z;
    };

    ZBUS_CHAN_DEFINE(acc_chan,                           /* Name */
             struct acc_msg,                             /* Message type */

             NULL,                                       /* Validator */
             NULL,                                       /* User Data */
             ZBUS_OBSERVERS(my_listener, my_subscriber,
                            my_msg_subscriber),          /* observers */
             ZBUS_MSG_INIT(.x = 0, .y = 0, .z = 0)       /* Initial value */
    );

    void listener_callback_example(const struct zbus_channel *chan)
    {
            const struct acc_msg *acc;
            if (&acc_chan == chan) {
                    acc = zbus_chan_const_msg(chan); // Direct message access
                    LOG_DBG("From listener -> Acc x=%d, y=%d, z=%d", acc->x, acc->y, acc->z);
            }
    }

    ZBUS_LISTENER_DEFINE(my_listener, listener_callback_example);

    ZBUS_LISTENER_DEFINE(my_listener2, listener_callback_example);

    ZBUS_CHAN_ADD_OBS(acc_chan, my_listener2, 3);

    ZBUS_SUBSCRIBER_DEFINE(my_subscriber, 4);
    void subscriber_task(void)
    {
            const struct zbus_channel *chan;

            while (!zbus_sub_wait(&my_subscriber, &chan, K_FOREVER)) {
                    struct acc_msg acc = {0};

                    if (&acc_chan == chan) {
                            // Indirect message access
                            zbus_chan_read(&acc_chan, &acc, K_NO_WAIT);
                            LOG_DBG("From subscriber -> Acc x=%d, y=%d, z=%d", acc.x, acc.y, acc.z);
                    }
            }
    }
    K_THREAD_DEFINE(subscriber_task_id, 512, subscriber_task, NULL, NULL, NULL, 3, 0, 0);

    ZBUS_MSG_SUBSCRIBER_DEFINE(my_msg_subscriber);
    static void msg_subscriber_task(void *ptr1, void *ptr2, void *ptr3)
    {
            ARG_UNUSED(ptr1);
            ARG_UNUSED(ptr2);
            ARG_UNUSED(ptr3);
            const struct zbus_channel *chan;

            struct acc_msg acc = {0};

            while (!zbus_sub_wait_msg(&my_msg_subscriber, &chan, &acc, K_FOREVER)) {
                    if (&acc_chan == chan) {
                            LOG_INF("From msg subscriber -> Acc x=%d, y=%d, z=%d", acc.x, acc.y, acc.z);
                    }
            }
    }
    K_THREAD_DEFINE(msg_subscriber_task_id, 1024, msg_subscriber_task, NULL, NULL, NULL, 3, 0, 0);



可以使用 :c:macro:`ZBUS_CHAN_ADD_OBS` 向通道添加静态观察者。我们将其称为定义后静态观察者。该指令使我们能够指定一个初始化优先级，从而影响观察者的初始化顺序。序列优先级参数仅影响定义后静态观察者。无法覆盖静态观察者的消息投递顺序。

.. note::
   由于事件分发器调用监听器时通知通道已经处于锁定状态，因此在监听器内部访问消息之前无需认领/锁定通道。但是，订阅者在收到通知后必须认领/锁定通道，或使用常规读取操作来访问消息。


通道可以具有一个 *校验函数*，使通道只接受有效的消息。被硬通道判定为无效的发布尝试会立即返回错误码。这允许通道的原始创建者对可能想要借用其通道的其他开发者/发布者行使一定的控制权。以下代码定义并初始化一个 :dfn:`硬通道` 及其依赖项。只有有效的消息才能发布到 :dfn:`硬通道`。之所以能做到这一点，是因为在通道定义中传入了 *校验函数*。在本示例中，只有 ``move`` 等于 0、-1 和 1 的消息才是有效的。发布函数会丢弃 ``move`` 的所有其他值。

.. code-block:: c

    struct control_msg {
            int move;
    };

    bool control_validator(const void* msg, size_t msg_size) {
            const struct control_msg* cm = msg;
            bool is_valid = (cm->move == -1) || (cm->move == 0) || (cm->move == 1);
            return is_valid;
    }

    static int message_count = 0;

    ZBUS_CHAN_DEFINE(control_chan,    /* Name */
             struct control_msg,      /* Message type */

             control_validator,       /* Validator */
             &message_count,          /* User data */
             ZBUS_OBSERVERS_EMPTY,    /* observers */
             ZBUS_MSG_INIT(.move = 0) /* Initial value */
    );

以下各节详细介绍如何使用 zbus 的各项特性。


.. _publishing to a channel:

向通道发布
==========

在 zbus 中，通过调用 :c:func:`zbus_chan_pub` 将消息发布到通道。例如，以下代码基于上面的示例，并向通道 ``acc_chan`` 发布消息。这段代码尝试将消息 ``acc1`` 发布到通道 ``acc_chan``，并最多等待一秒以使消息发布完成；否则该操作失败。从代码示例可以看出，使用栈上分配的消息是可以的，因为 VDED 会在内部复制数据。

.. code-block:: c

        struct acc_msg acc1 = {.x = 1, .y = 1, .z = 1};
        zbus_chan_pub(&acc_chan, &acc1, K_SECONDS(1));

.. warning::
    在 ISR 内使用此函数时，只能使用 :c:macro:`K_NO_WAIT` 超时。

.. _reading from a channel:

从通道读取
==========

在 zbus 中，通过调用 :c:func:`zbus_chan_read` 从通道读取消息。因此，例如，以下代码尝试读取通道 ``acc_chan``，它将最多等待 500 毫秒来读取消息；否则该操作失败。

.. code-block:: c

    struct acc_msg acc = {0};
    zbus_chan_read(&acc_chan, &acc, K_MSEC(500));

.. warning::
    在 ISR 内使用此函数时，只能使用 :c:macro:`K_NO_WAIT` 超时。

.. warning::
   在收到来自 :c:func:`zbus_sub_wait` 的通知后，请谨慎选择 :c:func:`zbus_chan_read` 的超时时间，因为在 VDED 执行期间通道始终不可用。如果订阅者不止一个，使用 ``K_NO_WAIT`` 进行读取极有可能返回超时错误。例如，再次参考 VDED 图示，注意 ``S1`` 的读取尝试在使用 K_NO_WAIT 时肯定会失败。有关更多细节，请查看 `Virtual Distributed Event Dispatcher`_ 一节。

通知通道
========

可以通过调用 :c:func:`zbus_chan_notify` 强制 zbus 通知通道的观察者。例如，以下代码基于上面的示例，强制对通道 ``acc_chan`` 发出通知。注意，这可以发送不带消息的事件，因而无需任何数据交换。当这一点变得有用时，请参见 `Claim and finish a channel`_ 下的代码示例。

.. code-block:: c

    zbus_chan_notify(&acc_chan, K_NO_WAIT);

.. warning::
    在 ISR 内使用此函数时，只能使用 :c:macro:`K_NO_WAIT` 超时。

声明通道和观察者
================

要从定义文件之外的其他文件访问通道或观察者，必须通过调用 :c:macro:`ZBUS_CHAN_DECLARE` 和 :c:macro:`ZBUS_OBS_DECLARE` 来声明它们。换句话说，不同文件中同名通道的 zbus 通道定义和声明将指向同一个（全局）通道。因此，开发者应小心处理已有通道，否则命名新通道或链接将会失败。可以在同一次调用中声明多个通道或观察者。以下代码基于上面的示例，并显示已定义的通道和观察者。

.. code-block:: c

    ZBUS_OBS_DECLARE(my_listener, my_subscriber);
    ZBUS_CHAN_DECLARE(acc_chan, version_chan);


唯一通道标识符
--------------

为了简化与外部实体的集成，可以为通道分配一个唯一的数字标识符。用户随后可以使用该标识符通过 :c:func:`zbus_chan_from_id` 获取通道引用，而无需在编译时通过 :c:macro:`ZBUS_CHAN_DECLARE` 获取引用。使用此特性的通道通过 :c:macro:`ZBUS_CHAN_DEFINE_WITH_ID` 声明。

.. code-block:: c

    ZBUS_CHAN_DEFINE_WITH_ID(control_chan,    /* Name */
        0x12345678,              /* Unique channel identifier */
        struct control_msg,      /* Message type */
        control_validator,       /* Validator */
        &message_count,          /* User data */
        ZBUS_OBSERVERS_EMPTY,    /* observers */
        ZBUS_MSG_INIT(.move = 0) /* Initial value */
    );

    static void channel_retrieve(void)
    {
        const struct zbus_channel *chan = zbus_chan_from_id(0x12345678);

        ...
    }

运行时创建通道
--------------

启用 :kconfig:option:`CONFIG_ZBUS_RUNTIME_CHANNEL_REGISTRATION` 后，ZBus 允许在运行时创建通道。这在通道数量或其配置在编译时未知的场景中很有用。以下代码演示了如何在运行时创建通道。请注意，传递给 :c:func:`zbus_runtime_channel_register` 的 :c:struct:`zbus_runtime_channel`、:c:struct:`zbus_channel_data` 以及消息结构体必须在内存中保持有效，直到调用 :c:func:`zbus_runtime_channel_unregister`。

.. code-block:: c

    struct runtime_msg {
        int data;
    };

    void create_runtime_channel(void)
    {
        struct zbus_runtime_channel runtime_chan;
        struct zbus_channel_data data;
        struct runtime_msg msg = {0};
        int ret;

        /* Initialise and register the runtime channel */
        zbus_runtime_channel_init(&runtime_chan, &data, "chan", 0x12345678, NULL, &msg,
                                  sizeof(msg), NULL);
        ret = zbus_runtime_channel_register(&runtime_chan);
        if (ret < 0) {
            LOG_ERR("Failed to register runtime channel (%d)", ret);
            return;
        }

        /* Use the runtime channel here */
        struct runtime_msg pub_data = {42};

        zbus_chan_pub(&runtime_chan.channel, &pub_data, K_MSEC(100));
        ...

        /* Unregister the runtime channel when done */
        zbus_runtime_channel_unregister(&runtime_chan);
    }

遍历通道和观察者
================

ZBus 子系统还为通道和观察者实现了 :ref:`可迭代段 <iterable_sections_api>`，并提供了诸如 :c:func:`zbus_iterate_over_channels`、:c:func:`zbus_iterate_over_channels_with_user_data`、:c:func:`zbus_iterate_over_observers` 和 :c:func:`zbus_iterate_over_observers_with_user_data` 等支持 API。此特性使开发者能够对所有已声明的通道调用某个过程，该过程的参数为 :c:struct:`zbus_channel`。执行顺序按通道名称的字母顺序排列（详情参见 :ref:`可迭代段 <iterable_sections_api>` 文档）。ZBus 还为 :c:struct:`zbus_observer` 实现了此特性。

.. code-block:: c

   static bool print_channel_data_iterator(const struct zbus_channel *chan, void *user_data)
   {
         int *count = user_data;

         LOG_INF("%d - Channel %s:", *count, zbus_chan_name(chan));
         LOG_INF("      Message size: %d", zbus_chan_msg_size(chan));
         LOG_INF("      Observers:");

         ++(*count);

         struct zbus_channel_observation *observation;

         for (int16_t i = *chan->observers_start_idx, limit = *chan->observers_end_idx; i < limit;
               ++i) {
               STRUCT_SECTION_GET(zbus_channel_observation, i, &observation);

               LOG_INF("      - %s", observation->obs->name);
         }

         struct zbus_observer_node *obs_nd, *tmp;

         SYS_SLIST_FOR_EACH_CONTAINER_SAFE(chan->observers, obs_nd, tmp, node) {
               LOG_INF("      - %s", obs_nd->obs->name);
         }

         return true;
   }

   static bool print_observer_data_iterator(const struct zbus_observer *obs, void *user_data)
   {
         int *count = user_data;

         LOG_INF("%d - %s %s", *count, obs->queue ? "Subscriber" : "Listener", zbus_obs_name(obs));

         ++(*count);

         return true;
   }

   int main(void)
   {
         int count = 0;

         LOG_INF("Channel list:");

         zbus_iterate_over_channels_with_user_data(print_channel_data_iterator, &count);

         count = 0;

         LOG_INF("Observers list:");

         zbus_iterate_over_observers_with_user_data(print_observer_data_iterator, &count);

         return 0;
   }


代码将输出以下日志：

.. code-block:: console

    D: Channel list:
    D: 0 - Channel acc_chan:
    D:       Message size: 12
    D:       Observers:
    D:       - my_listener
    D:       - my_subscriber
    D: 1 - Channel version_chan:
    D:       Message size: 4
    D:       Observers:
    D: Observers list:
    D: 0 - Listener my_listener
    D: 1 - Subscriber my_subscriber


.. _Claim and finish a channel:

高级通道控制
============

ZBus 在设计上尽可能灵活且可扩展。因此，有些特性旨在为总线提供一定的控制和扩展能力。

监听器消息访问
--------------

出于性能考虑，监听器可以直接访问所接收通道的消息，因为它们已经为该通道加锁。要访问通道的消息，监听器应使用 :c:func:`zbus_chan_const_msg`，因为作为参数传递给监听器函数的通道是指向该通道的常量指针。常量指针返回类型告诉开发者不要修改消息。

.. code-block:: c

    void listener_callback_example(const struct zbus_channel *chan)
    {
            const struct acc_msg *acc;
            if (&acc_chan == chan) {
                    acc = zbus_chan_const_msg(chan); // Use this
                    // instead of zbus_chan_read(chan, &acc, K_MSEC(200))
                    // or zbus_chan_msg(chan)

                    LOG_DBG("From listener -> Acc x=%d, y=%d, z=%d", acc->x, acc->y, acc->z);
            }
    }


异步监听器消息访问
------------------

异步监听器是通过利用已有的消息订阅者基础设施实现的。它们在工作队列上下文中执行，而不是在发布者的上下文中执行。使用系统工作队列时，用户会体验到与常规监听器类似的行为。由于系统工作队列默认是优先级为 -1 的协作式线程，因此异步监听器会在 VDED 执行之后、所有其他应用线程（通常是抢占式线程）之前运行。

异步监听器可以通过传递给回调的消息副本引用直接访问所接收通道的消息。请注意，消息副本会在异步监听器执行后立即释放。要访问通道的消息，异步监听器只应将其转换为适当的常量消息格式。以下示例演示了如何从异步监听器访问消息。


.. code-block:: c

   static void async_listener_callback(const struct zbus_channel *chan, const void *message)
   {
           if (chan != &chan_event) {
                   LOG_ERR("Unexpected channel");
                   return;
           }

           const struct msg_event *msg = message;

           LOG_INF("From async listener -> Evt=%d | %s", msg->type,
                   k_thread_name_get(k_current_get()));
   }


用户数据
--------
可以将自定义数据传入通道的 ``user_data``，用于各种目的，例如写入通道元数据。这可以通过向通道定义宏的 ``user_data`` 字段传递一个指针来实现，之后其他实体即可访问该数据。请注意，``user_data`` 对每个通道是独立的。另外请注意，访问 ``user_data`` 不是线程安全的。要实现对 ``user_data`` 的线程安全访问，请参见下一节。


认领和完成通道
--------------

为了更好地控制通道，新增了两个函数：:c:func:`zbus_chan_claim` 和 :c:func:`zbus_chan_finish`。借助这些函数，可以安全地访问通道的元数据。当通道被认领时，该通道上没有任何可用操作。完成通道后，所有操作将再次可用。

.. warning::
   切勿直接更改通道结构体的字段。这可能导致 zbus 行为不一致和调度问题。

.. warning::
    在 ISR 内使用此函数时，只能使用 :c:macro:`K_NO_WAIT` 超时。

以下代码基于上面的示例，认领 ``acc_chan`` 并向通道设置 ``user_data``。假设我们想统计通道交换消息的次数。我们将 ``user_data`` 定义为 32 位整数。这段代码可以添加到上面描述的监听器代码中。

.. code-block:: c

    if (!zbus_chan_claim(&acc_chan, K_MSEC(200))) {
            int *message_counting = (int *) zbus_chan_user_data(&acc_chan);
            *message_counting += 1;
            zbus_chan_finish(&acc_chan);
    }

以下代码的行为与 :ref:`publishing to a channel` 中的代码完全一致。

.. code-block:: c

    if (!zbus_chan_claim(&acc_chan, K_MSEC(200))) {
            struct acc_msg *acc1 = (struct acc_msg *) zbus_chan_msg(&acc_chan);
            acc1->x = 1;
            acc1->y = 1;
            acc1->z = 1;
            zbus_chan_finish(&acc_chan);
            zbus_chan_notify(&acc_chan, K_SECONDS(1));
    }

以下代码的行为与 :ref:`reading from a channel` 中的代码完全一致。

.. code-block:: c

    if (!zbus_chan_claim(&acc_chan, K_MSEC(200))) {
            const struct acc_msg *acc1 = (const struct acc_msg *) zbus_chan_const_msg(&acc_chan);
            // access the acc_msg fields directly.
            zbus_chan_finish(&acc_chan);
    }

.. _runtime observers:

运行时观察者注册
----------------

可以在运行时向通道添加观察者。设置 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS` 以启用该特性。该特性使用堆动态分配节点、使用内存块池静态分配节点，或使用用户提供的节点。它取决于 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC`，该选项可以是 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_DYNAMIC`、:kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_STATIC` 和 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_NONE`。默认为动态分配。启用 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_STATIC` 时，需要通过 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_POOL_SIZE` 配置来设置将要使用的运行时观察者数量。以下示例演示了运行时注册的用法。

.. code-block:: c

    ZBUS_LISTENER_DEFINE(my_listener, callback);
    // ...

    void thread_entry(void) {
            // ...
            /* Adding the observer to channel chan1 */
            zbus_chan_add_obs(&chan1, &my_listener, K_NO_WAIT);
            /* Removing the observer from channel chan1 */
            zbus_chan_rm_obs(&chan1, &my_listener, K_NO_WAIT);
    }


.. warning::

  只有在通过 :c:func:`zbus_chan_rm_obs` 移除最初关联的通道观察者之后，:c:struct:`zbus_observer_node` 才能在 :c:func:`zbus_chan_add_obs_with_node` 中重用。

.. _zbus_proxy_agent:

代理 agent 通信（实验性）
*************************

.. warning::
  代理 agent 通信是实验性的，可能在不经过弃用流程的情况下发生变化。

ZBus 支持代理 agent 转发，可在不同执行域（例如 CPU 核或独立设备）之间传递消息。

.. figure:: images/zbus_proxy_agent.svg
    :alt: ZBus 代理 agent 通信
    :width: 75%

..
  Image illustrating zbus proxy agent communication between domains.

Concepts
========

代理 agent 通信引入了几个关键概念：

* **影子通道**：只读通道，用于镜像来自其他域的通道
* **代理 agent**：在域之间同步通道数据的后台服务
* **传输后端**：代理 agent 使用的通信机制

代理 agent 使用 :c:macro:`ZBUS_PROXY_AGENT_DEFINE` 在代码中进行设置，并指定传输后端和配置参数。通道使用标准 zbus 宏（:c:macro:`ZBUS_CHAN_DEFINE` 或 :c:macro:`ZBUS_CHAN_DEFINE_WITH_ID`）定义，影子通道则使用 :c:macro:`ZBUS_SHADOW_CHAN_DEFINE` 创建链接到特定代理 agent 的只读镜像。

传输后端
========

ZBus 代理 agent 通信依赖传输后端在不同执行域之间转发消息。

IPC 后端
--------

IPC 后端使用进程间通信机制在同一系统内的 CPU 核之间转发消息。

完整实现请参见 :zephyr:code-sample:`zbus-proxy-agent-ipc` 示例。

Usage
=====

1. 启用 :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT` 以及所需的后端选项。
2. 在 devicetree 中提供后端设备。
3. 实例化代理 agent：

.. code-block:: c

    #include <zephyr/zbus/proxy_agent/zbus_proxy_agent.h>
    #include <zephyr/zbus/proxy_agent/zbus_proxy_agent_ipc.h>

    #define IPC_DEV_NODE DT_NODELABEL(ipc0)

    ZBUS_PROXY_AGENT_DEFINE(proxy_agent,                   /* Proxy agent name */
                            ZBUS_PROXY_AGENT_BACKEND_IPC,  /* Proxy agent type */
                            IPC_DEV_NODE                   /* Backend node */
    );

位置：

- “proxy_agent”：代理 agent 实例的名称
- “ZBUS_PROXY_AGENT_BACKEND_IPC”：传输后端类型（此处为 IPC）
- “IPC_DEV_NODE”：后端设备的设备树节点

4. 通过代理 agent 转发本地通道：

.. code-block:: c

    ZBUS_CHAN_DEFINE(my_channel, struct my_msg, NULL, NULL,
                     ZBUS_OBSERVERS_EMPTY, ZBUS_MSG_INIT(0));
    ZBUS_PROXY_ADD_CHAN(proxy_agent, my_channel);

    zbus_chan_pub(&my_channel, &msg, K_MSEC(100));

任何发布到 “my_channel” 的消息都将由 “proxy_agent” 转发到远程域。

5. 使用影子通道镜像远程通道：

.. code-block:: c

    ZBUS_SHADOW_CHAN_DEFINE(my_channel_shadow, struct my_msg,
                            proxy_agent, NULL, ZBUS_OBSERVERS_EMPTY,
                            ZBUS_MSG_INIT(0));

其中影子通道可以像任何常规通道一样使用，但它是只读的。例如，添加一个监听器：

.. code-block:: c

    void my_listener_cb(const struct zbus_channel *chan)
    {
        const struct my_msg *data = zbus_chan_const_msg(chan);
        printk("Received: %d\n", data->data);
    }

    ZBUS_LISTENER_DEFINE(my_listener, my_listener_cb);
    ZBUS_CHAN_ADD_OBS(my_channel_shadow, my_listener, 0);

示例
****

要全面了解 zbus 的用法，请查看示例。目前有以下示例可用：

* :zephyr:code-sample:`zbus-hello-world` 演示了上文所用代码的实际效果；
* :zephyr:code-sample:`zbus-work-queue` 展示了如何定义和使用不同类型的观察者。注意其中有一个示例：使用工作队列作为执行选项，而不是直接执行监听器；
* :zephyr:code-sample:`zbus-msg-subscriber` 演示了如何使用消息订阅者；
* :zephyr:code-sample:`zbus-async-listeners` 演示了如何使用异步监听器；
* :zephyr:code-sample:`zbus-dyn-channel` 演示了如何在 zbus 中使用动态分配的交换数据；
* :zephyr:code-sample:`zbus-uart-bridge` 展示了通过串口将通道的操作发送到主机的示例；
* :zephyr:code-sample:`zbus-remote-mock` 演示了如何实现一个外部 mock（位于主机上）来向总线发送消息和从总线接收消息；
* :zephyr:code-sample:`zbus-priority-boost` 演示了 zbus 优先级提升特性及一个优先级反转场景；
* :zephyr:code-sample:`zbus-runtime-obs-registration` 演示了使用运行时观察者注册特性的一种方式；
* :zephyr:code-sample:`zbus-confirmed-channel` 实现了一种仅使用订阅者的确认通道实现方式；
* :zephyr:code-sample:`zbus-benchmark` 实现了一个使用不同输入组合的基准测试。
* :zephyr:code-sample:`zbus-proxy-agent-ipc` 演示了使用 IPC 代理 agent 的多核通信；

建议用法
********

使用 zbus 在线程之间以一对一、一对多和多对多的方式同步或异步地传输数据（消息）。选择合适的观察者类型至关重要。对于可以容忍消息丢失和重复的场景，请使用订阅者；如果不能容忍，请使用消息订阅者（如果需要线程）或监听器（如果需要轻量且快速）。除了监听器之外，可能还需要另一种异步消息处理机制（例如 :ref:`消息队列 <message_queues_v2>`），以保留挂起的消息直到其被处理。

对于代理 agent 场景，请使用 zbus 实现跨执行边界的通信：

* **多核系统**：使用 IPC 后端代理 agent 在应用处理器与网络处理器之间进行协调，或将工作负载分布到多个 CPU 核上。

.. note::
   ZBus 可用于将数据流从生产者传输到消费者。但是，这可能会增加 zbus 的通信延迟。因此，对于这种通信拓扑，可以考虑使用管道作为良好的替代方案。

配置选项
********

要启用 zbus，必须启用 :kconfig:option:`CONFIG_ZBUS` 选项。

相关配置选项：

* :kconfig:option:`CONFIG_ZBUS_PRIORITY_BOOST` zbus 最高锁定者协议实现；

* :kconfig:option:`CONFIG_ZBUS_CHANNELS_SYS_INIT_PRIORITY` 确定 zbus 用于按通道组织通道观察关系的 :c:macro:`SYS_INIT` 优先级；
* :kconfig:option:`CONFIG_ZBUS_CHANNEL_NAME` 使通道名称可在通道元数据中获取。日志利用该信息显示通道名称；
* :kconfig:option:`CONFIG_ZBUS_OBSERVER_NAME` 使观察者名称可在通道元数据中获取；
* :kconfig:option:`CONFIG_ZBUS_PREFER_DYNAMIC_ALLOCATION` 指示 zbus 对其内部结构使用动态分配。用户可以禁用此项并在之后进行调整；
* :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER` 启用消息订阅者观察者类型；
* :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_BUF_ALLOC_DYNAMIC` 使用堆分配消息缓冲区；
* :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_BUF_ALLOC_STATIC` 使用栈分配消息缓冲区；
* :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_SIZE` 可同时使用的消息缓冲区数量；
* :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_ISOLATION` 使开发者可以为某一组通道隔离消息订阅者的池；只有对某个通道调用 :c:func:`zbus_chan_set_msg_sub_pool` 后，该通道才会切换到专用池；
* :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_STATIC_DATA_SIZE` 可传输到消息缓冲区中的最大 zbus 通道消息；
* :kconfig:option:`CONFIG_HEAP_MEM_POOL_ADD_SIZE_ZBUS` 为 ZBus 预留的总堆大小，包括消息缓冲区分配；
* :kconfig:option:`CONFIG_ZBUS_ASYNC_LISTENER` 启用异步监听器观察者类型；
* :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS` 启用运行时观察者注册；
* :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_DYNAMIC` 使用堆动态分配运行时观察者；
* :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_STATIC` 使用内存块池静态分配运行时观察者；
* :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_POOL_SIZE` 静态分配的已启用运行时观察者数量；
* :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_NONE` 使用用户提供的运行时观察者节点；
* :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT` 启用代理 agent 通信支持。

代理 agent 配置选项
===================

* :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT_LOG_LEVEL` 代理 agent 通信的日志级别；
* :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT_IPC` 为代理 agent 通信启用 IPC 后端；
* :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT_IPC_LOG_LEVEL` IPC 后端代理 agent 通信的日志级别；
* :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT_MAX_MESSAGE_SIZE` 代理 agent 通道的最大消息大小；
* :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT_MAX_CHANNEL_NAME_SIZE` 代理 agent 通信中通道名称的最大长度；
* :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT_INIT_PRIORITY` 代理 agent 设置的初始化优先级。
* :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT_WORK_QUEUE_STACK_SIZE` 代理 agent 接收工作队列线程的栈大小；
* :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT_WORK_QUEUE_PRIORITY` 代理 agent 接收工作队列线程的优先级。
* :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT_RX_QUEUE_DEPTH` 用于接收来自远程域传入消息的代理 agent 接收队列深度。

API 参考
********

.. doxygengroup:: zbus_apis
