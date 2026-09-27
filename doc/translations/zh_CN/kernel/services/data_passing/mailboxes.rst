.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mailboxes_v2:

邮箱
####

:dfn:`邮箱` 是提供增强消息队列功能的内核对象，其能力超出了消息队列对象。邮箱允许线程以同步或异步方式发送和接收任意大小的消息。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的邮箱（仅受可用 RAM 限制）。每个邮箱都通过其内存地址引用。

邮箱具有以下主要属性：

* 一个 **发送队列**，存放已发送但尚未接收的消息。

* 一个 **接收队列**，存放正在等待接收消息的线程。

邮箱必须初始化后才能使用。初始化会将两个队列都置空。

邮箱允许线程交换消息，但不允许 ISR 使用。发送消息的线程称为 **发送线程**，接收消息的线程称为 **接收线程**。每条消息只能由一个线程接收，即不支持点对多点和广播消息。

通过邮箱交换消息时，参与交换的线程不是匿名的，双方都可以获知甚至指定对方的身份。

消息格式
========

**消息描述符** 是指定消息数据位置及邮箱处理方式的数据结构。发送线程和接收线程访问邮箱时都要提供消息描述符。邮箱利用这些描述符，在相互兼容的发送线程和接收线程之间交换消息。交换过程中，邮箱还会更新某些消息描述符字段，使双方了解交换结果。

邮箱消息包含零个或多个字节的 **消息数据**。消息数据的大小和格式由应用定义，不同消息可以各不相同。

**消息缓冲区** 是由发送或接收消息数据的线程提供的一块内存区域，通常可以使用数组或结构体变量。

不包含任何形式消息数据的消息称为 **空消息**。

.. note::
    存在消息缓冲区但其中实际数据为零字节的消息，*不是* 空消息。

消息生命周期
============

消息的生命周期很简单。发送线程将消息交给邮箱时，消息即被创建。随后，消息由邮箱持有，直到被交给接收线程。接收线程可以在从邮箱接收消息的同时取回消息数据，也可以在后续第二次邮箱操作中取回数据。只有完成数据取回后，邮箱才会删除消息。

线程兼容性
==========

发送线程可以指定目标线程的地址，也可以指定 :c:macro:`K_ANY`，将消息发送给任意线程。同样，接收线程可以指定希望接收消息的来源线程地址，也可以指定 :c:macro:`K_ANY`，接收来自任意线程的消息。只有同时满足发送线程与接收线程的要求时，才会交换消息；这样的线程称为 **兼容线程**。

例如，线程 A 向线程 B（且仅向线程 B）发送消息时，如果线程 B 尝试接收来自线程 A 或任意线程的消息，就能收到这条消息。如果线程 B 尝试接收来自线程 C 的消息，则不会发生交换。线程 C 永远无法收到这条消息，即使它尝试接收来自线程 A 或任意线程的消息。

消息流量控制
============

邮箱消息可以 **同步** 或 **异步** 交换。同步交换时，发送线程会阻塞，直到接收线程完整处理该消息。异步交换时，发送线程无需等待消息被其他线程接收即可继续执行，因此可以在消息交给接收线程并被完整处理 *之前* 做其他工作，例如收集下一条消息所需的数据。每次消息交换采用哪种方式，由发送线程决定。

同步交换提供隐式流量控制，防止发送线程生成消息的速度超过接收线程的消费速度。异步交换提供显式流量控制，允许发送线程在发送下一条消息之前判断先前发送的消息是否仍然存在。

实现
****

定义邮箱
========

邮箱使用 :c:struct:`k_mbox` 类型的变量定义，随后必须调用 :c:func:`k_mbox_init` 进行初始化。

以下代码定义并初始化一个空邮箱。

.. code-block:: c

    struct k_mbox my_mailbox;

    k_mbox_init(&my_mailbox);

也可以使用 :c:macro:`K_MBOX_DEFINE` 在编译时定义并初始化邮箱。

以下代码与上面的代码片段效果相同。

.. code-block:: c

    K_MBOX_DEFINE(my_mailbox);

消息描述符
==========

消息描述符是 :c:struct:`k_mbox_msg` 类型的结构体。只能使用下列字段；其他字段仅供邮箱内部使用。

*info*
    由消息发送者和接收者交换的 32 位值，其含义由应用定义。此交换是双向的：发送者可以在任意消息交换中向接收者传递一个值，接收者则可以在同步消息交换中向发送者传递一个值。

*size*
    消息数据的大小，以字节为单位。发送空消息或不含实际数据的消息缓冲区时，将其设为零。接收消息时，将其设为希望接收的最大数据量；如果不需要消息数据，则设为零。消息被接收后，邮箱会将此字段更新为实际交换的数据字节数。

*tx_data*
    指向发送线程消息缓冲区的指针。发送空消息时将其设为 ``NULL``。接收消息时无需初始化此字段。

*tx_target_thread*
    期望接收线程的地址。设为 :c:macro:`K_ANY` 可允许任意线程接收消息。接收消息时无需初始化此字段。消息被接收后，邮箱会将此字段更新为实际接收者的地址。

*rx_source_thread*
    期望发送线程的地址。设为 :c:macro:`K_ANY` 可接收任意线程发送的消息。发送消息时无需初始化此字段。消息放入邮箱时，邮箱会将此字段更新为实际发送者的地址。

发送消息
========

线程发送消息时，首先创建消息数据（如果有）。

接着，发送线程创建用于描述待发消息的消息描述符，具体见上一节。

最后，发送线程调用邮箱发送 API，发起消息交换。如果当前有兼容的接收线程在等待，消息会立即交给它；否则，消息会被加入邮箱的发送队列。

发送队列可以同时存放任意数量的消息。队列中的消息按发送线程的优先级排序；相同优先级的消息按时间排序，使最早的消息能够最先被接收。

对于同步发送操作，通常要等接收线程既接收了消息又取回了消息数据后，操作才会完成。如果发送线程指定的等待时间结束时消息仍未被接收，消息会从邮箱的发送队列中移除，发送操作失败。发送操作成功完成后，发送线程可以检查消息描述符，确定哪个线程接收了消息、交换了多少数据，以及接收线程提供的应用自定义 info 值。

.. note::
   即使线程指定了最大等待时间，同步发送操作也可能无限期阻塞发送线程。等待时间仅限制邮箱等待另一个线程接收消息的时长。一旦消息被接收，接收线程用于取回消息数据并解除发送线程阻塞的时间就 *没有* 上限。

异步发送操作总是立即完成。无论消息立即交给了接收线程，还是被加入发送队列，发送线程都可以继续处理。发送线程还可以指定一个信号量，邮箱删除消息时会释放该信号量，例如消息已被接收且接收线程已取回其数据时。借助信号量，发送线程可以方便地实现流量控制，确保邮箱在任意时刻持有的、来自某个发送线程或一组发送线程的消息数不超过应用规定的上限。

.. note::
   异步发送消息的线程无法确定哪个线程接收了消息、交换了多少数据，也无法获知接收线程提供的应用自定义 info 值。

发送空消息
----------

以下代码使用邮箱，将 4 字节随机值同步传递给任意需要它的消费者线程。消息的“info”字段足以容纳待交换的信息，因此无需使用消息的数据部分。

.. code-block:: c

    void producer_thread(void)
    {
        struct k_mbox_msg send_msg;

        while (1) {

            /* generate random value to send */
            uint32_t random_value = sys_rand32_get();

            /* prepare to send empty message */
            send_msg.info = random_value;
            send_msg.size = 0;
            send_msg.tx_data = NULL;
            send_msg.tx_target_thread = K_ANY;

            /* send message and wait until a consumer receives it */
            k_mbox_put(&my_mailbox, &send_msg, K_FOREVER);
        }
    }

使用消息缓冲区发送数据
----------------------

以下代码使用邮箱，将变长请求从生产者线程同步传递给任意需要它的消费者线程。消息的“info”字段用于交换各线程能够处理的消息缓冲区最大容量信息。

.. code-block:: c

    void producer_thread(void)
    {
        char buffer[100];
        int buffer_bytes_used;

        struct k_mbox_msg send_msg;

        while (1) {

            /* generate data to send */
            ...
            buffer_bytes_used = ... ;
            memcpy(buffer, source, buffer_bytes_used);

            /* prepare to send message */
            send_msg.info = buffer_bytes_used;
            send_msg.size = buffer_bytes_used;
            send_msg.tx_data = buffer;
            send_msg.tx_target_thread = K_ANY;

            /* send message and wait until a consumer receives it */
            k_mbox_put(&my_mailbox, &send_msg, K_FOREVER);

            /* info, size, and tx_target_thread fields have been updated */

            /* verify that message data was fully received */
            if (send_msg.size < buffer_bytes_used) {
                printf("some message data dropped during transfer!");
                printf("receiver only had room for %d bytes", send_msg.info);
            }
        }
    }

接收消息
========

线程接收消息时，首先创建消息描述符，描述希望接收的消息，然后调用某个邮箱接收 API。邮箱会搜索发送队列，从找到的第一个兼容线程那里取出消息。如果没有兼容线程，接收线程可以选择等待。如果在接收线程指定的等待时间内没有出现兼容线程，接收操作失败。接收操作成功完成后，接收线程可以检查消息描述符，确定哪个线程发送了消息、交换了多少数据，以及发送线程提供的应用自定义 info 值。

任意数量的接收线程都可以同时在邮箱的接收队列中等待。线程按优先级排序；相同优先级的线程按开始等待的时间排序，使最早开始等待的线程能够最先接收消息。

.. note::
    由于消息描述符指定了线程兼容性约束，接收线程并不总是按照先进先出（FIFO）的顺序接收消息。例如，线程 A 先等待仅来自线程 X 的消息，随后线程 B 等待来自线程 Y 的消息；此时，线程 Y 向任意线程发送的消息会被交给线程 B，而线程 A 继续等待。

接收线程决定从到达消息中取回多少数据，以及将数据放在哪里。它可以取回全部数据、仅取回开头的一部分，也可以不取回任何数据。同样，它可以选择将数据复制到自己指定的消息缓冲区。

以下各节介绍接收线程取回消息数据的几种方式。

接收时取回数据
--------------

线程取回消息数据最直接的方式，是在接收消息时指定消息缓冲区。线程需同时给出缓冲区的位置（不能为 ``NULL``）和大小。

邮箱在接收操作中将消息数据复制到消息缓冲区。如果缓冲区不足以容纳全部消息数据，未复制的数据会丢失。如果消息数据不足以填满缓冲区，缓冲区未使用的部分保持不变。无论哪种情况，邮箱都会更新接收线程的消息描述符，指明实际复制的数据字节数（可能为零）。

立即取回数据的方式最适合事先已知最大消息大小的小消息。

以下代码使用邮箱，采用立即取回数据的方式，处理来自任意生产者线程的变长请求。消息的“info”字段用于交换各线程能够处理的消息缓冲区最大容量信息。

.. code-block:: c

    void consumer_thread(void)
    {
        struct k_mbox_msg recv_msg;
        char buffer[100];

        int i;
        int total;

        while (1) {
            /* prepare to receive message */
            recv_msg.info = 100;
            recv_msg.size = 100;
            recv_msg.rx_source_thread = K_ANY;

            /* get a data item, waiting as long as needed */
            k_mbox_get(&my_mailbox, &recv_msg, buffer, K_FOREVER);

            /* info, size, and rx_source_thread fields have been updated */

            /* verify that message data was fully received */
            if (recv_msg.info != recv_msg.size) {
                printf("some message data dropped during transfer!");
                printf("sender tried to send %d bytes", recv_msg.info);
            }

            /* compute sum of all message bytes (from 0 to 100 of them) */
            total = 0;
            for (i = 0; i < recv_msg.size; i++) {
                total += buffer[i];
            }
        }
    }

稍后使用消息缓冲区取回数据
--------------------------

接收线程可以在收到消息时选择推迟取回消息数据，以便稍后再将数据取回到消息缓冲区。为此，线程将消息缓冲区位置设为 ``NULL``，并将大小设为稍后愿意取回的最大数据量。

此时邮箱在接收操作中不复制任何消息数据。不过，它仍会更新接收线程的消息描述符，指明可供取回的数据字节数。

接收线程随后必须按以下情况处理：

* 如果消息描述符中的大小为零，说明发送者的消息不含数据，或接收线程不希望接收任何数据。此时接收线程无需进一步操作，因为邮箱已经完成数据取回并删除了消息。

* 如果消息描述符中的大小非零，且接收线程仍希望取回数据，则线程必须调用 :c:func:`k_mbox_data_get`，并提供足以容纳数据的消息缓冲区。邮箱会将数据复制到缓冲区，然后删除消息。

* 如果消息描述符中的大小非零，但接收线程 *不再* 希望取回数据，则线程必须调用 :c:func:`k_mbox_data_get`，并将消息缓冲区指定为 ``NULL``。邮箱会直接删除消息，不复制数据。

延后取回数据的方式适用于不宜立即取回消息数据的应用。例如，受内存限制，接收线程无法始终提供足以容纳最大可能消息的缓冲区时，就可以使用此方式。

以下代码使用邮箱的延后数据取回机制，仅在消息满足特定条件时才从生产者线程取回消息数据，从而省去不必要的数据复制。发送者提供的消息“info”字段用于对消息分类。

.. code-block:: c

    void consumer_thread(void)
    {
        struct k_mbox_msg recv_msg;
        char buffer[10000];

        while (1) {
            /* prepare to receive message */
            recv_msg.size = 10000;
            recv_msg.rx_source_thread = K_ANY;

            /* get message, but not its data */
            k_mbox_get(&my_mailbox, &recv_msg, NULL, K_FOREVER);

            /* get message data for only certain types of messages */
            if (is_message_type_ok(recv_msg.info)) {
                /* retrieve message data and delete the message */
                k_mbox_data_get(&recv_msg, buffer);

                /* process data in "buffer" */
                ...
            } else {
                /* ignore message data and delete the message */
                k_mbox_data_get(&recv_msg, NULL);
            }
        }
    }

使用建议
********

当消息队列的能力不足以满足需求时，可使用邮箱在线程之间传递数据项。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_NUM_MBOX_ASYNC_MSGS`

API 参考
********

.. doxygengroup:: mailbox_apis
