.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ipc_service_backend_icbmsg:

使用动态分配缓冲区的 ICMsg 后端
###############################

通过此后端传输的数据以动态分配的缓冲区形式在共享内存中传递。分配是线程安全的，并且可以在任何上下文中进行。该后端支持：

* 多个端点。
* 零拷贝发送。
* 持有 RX 缓冲区。
* 从中断上下文发送。
* 两级端点优先级。
* 统计信息以及可选的、带利用率报告的 shell 命令
* 最多支持 32 个块。
* 支持数据缓存。
* 内存占用低（代码约 2 kB）。

概述
====

每个方向都会预留一个共享内存区域，并且每个区域划分为两部分。一部分构成固定大小缓冲区的池，分配器会从池中的相邻缓冲区构建可变大小的缓冲区。另一部分用于控制路径，由两个消息队列组成（每个方向各有一个）。其中有一个生产者队列，由发送方写入、接收方读取；还有一个消费者队列，由接收方写入、发送方读取。生产者队列包含下一条消息在池中位置的信息。消费者队列包含已消费消息在池中位置的信息。

数据发送流程如下：

* 发送方从池中分配一个或多个块。如果没有足够的连续块，则线程上下文会使用参数中提供的超时进行等待，该超时值还包括 K_FOREVER 和 K_NO_WAIT。
* 分配的块会被数据填充。第一个块的开头有一个 32 位消息头部，包含长度、端点 ID 和自身的块索引。对于零拷贝情况，这部分由调用方完成；否则会自动复制。在此期间，只要其他线程有足够的空闲块，就不会以任何方式被阻塞。它们可以分配、发送数据和接收数据。
* 将带有消息起始位置的块索引写入生产者队列。端点优先级的信息会附加到该块索引之后。:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_MAX_ACTIVE_COUNT` 定义队列中的槽位数。向接收方发送 MBOX 通知。
* 接收方读取生产者队列。优先级较高的消息会优先处理。接收方可以按需长时间持有数据。同样，只要其他线程有足够的空闲块，就不会被阻塞。
* 当不再需要数据时，接收方会将块索引写入消费者队列。
* 发送方通过读取消费者队列并释放缓冲区来执行垃圾回收。在发送任何消息之后，或者没有可用缓冲区时，都会执行垃圾回收。

配置
====

该后端使用 Kconfig 和 devicetree 进行配置。

以下是相关的 Kconfig 选项：

:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_NUM_EP` - 已注册端点的最大数量。

:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_MAX_ACTIVE_COUNT` - 队列中的槽位数。

:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_DEINIT` - 支持注销和关闭。

:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_SHELL` - 支持 shell 命令。

配置该后端时，请执行以下操作：

* 如果至少有一个核在共享内存上使用数据缓存，请设置 ``dcache-alignment`` 的值。该值必须是通信双方的失效大小和回写大小中的最大值。如果通信双方都不在共享内存上使用数据缓存，则可以跳过该项。
* 定义两个内存区域，并将它们分别分配给某个实例的 ``tx-region`` 和 ``rx-region``。确保用于数据交换的内存区域是唯一的（不与其他任何区域重叠），并且两个域（或 CPU）都能访问。
* 使用 ``tx-blocks`` 和 ``rx-blocks`` 为每个区域定义可分配的块数。
* 定义 MBOX 设备，用于发送信号以通知另一个域（或 CPU）数据已写入。确保另一个域（或 CPU）能够接收该信号。

.. caution::

    请确保为 ``dcache-alignment`` 设置正确的值。错误的值起初可能没有任何表现，从而让人误以为一切正常。但不稳定的行为迟早会出现。

如果使用了 ``dcache-alignment``，则应仔细选择块数的配置，以避免内存使用效率低下。这是因为块会按缓存对齐进行对齐，如果块数不是缓存对齐值的倍数，则最后一个块将无法被高效使用。这是因为块和控制数据都按缓存对齐进行对齐。例如，如果 ``dcache-alignment`` 为 32，并且一个方向使用 1024 字节共享内存。控制数据将占用 64 字节，剩余 960 字节可用于缓冲区。使用 16 个块将导致每个块 32 字节（受缓存对齐影响）。使用 15 个块将导致每个块 64 字节（受缓存对齐影响），内存利用率会高得多。


参见以下其中一个实例的配置示例：

.. code-block:: devicetree

   reserved-memory {
      tx: memory@20070000 {
         reg = <0x20070000 0x0800>;
      };

      rx: memory@20078000 {
         reg = <0x20078000 0x0800>;
      };
   };

   ipc {
      ipc0: ipc0 {
         compatible = "zephyr,ipc-icbmsg";
         dcache-alignment = <32>;
         tx-region = <&tx>;
         rx-region = <&rx>;
         tx-blocks = <16>;
         rx-blocks = <16>;
         mboxes = <&mbox 0>, <&mbox 1>;
         mbox-names = "tx", "rx";
         status = "okay";
      };
   };


您必须为通信的另一侧（域或 CPU）提供类似的配置。请交换 MBOX 通道、内存区域（``tx-region`` 和 ``rx-region``）以及块数（``tx-blocks`` 和 ``rx-blocks``）。

限制
====

* 要求通信双方使用相同的字节序。
* 不支持检测意外的远程复位。

示例
====

* :zephyr:code-sample:`ipc_multi_endpoint`

详细协议规范
============

ICBMsg 协议使用共享内存中动态分配的块来传输消息。

共享内存组织
------------

ICBMsg 使用两个共享内存区域，其中 ``rx-region`` 用于接收消息，``tx-region`` 用于发送消息。这些区域不需要彼此相邻、按任何特定顺序排列，也不需要大小相同。这些区域在每个核上互换。

每个共享内存区域都划分为以下两部分：

* **控制区域** - 为生产者队列和消费者队列保留的区域。
* **块区域** - 包含可分配块的区域，这些块承载消息内容。该区域划分为大小均匀、按缓存边界对齐的块。

每个区域的位置都经过计算，以满足缓存边界要求并实现最佳的区域利用率。使用以下算法进行计算：

输入：

* ``region_begin`` 和 ``region_end`` - 区域的边界。
* ``local_blocks`` - 此区域中的块数。
* ``remote_blocks`` - 对端区域中的块数。
* ``alignment`` - 内存缓存对齐。

算法：

#. 将区域边界按缓存对齐：

   * ``region_begin_aligned = ROUND_UP(region_begin, alignment)``
   * ``region_end_aligned = ROUND_DOWN(region_end, alignment)``
   * ``region_size_aligned = region_end_aligned - region_begin_aligned``

#. 计算控制区域所需的最小大小：

   * 每个队列有 :kconfig:option:`IPC_SERVICE_BACKEND_ICBMSG_MAX_ACTIVE_COUNT` 字节，以及 8 字节的队列头部。
   * 通常，每个方向的控制数据占用不到 64 字节。

#. 计算块区域的可用大小。注意，由于块对齐，实际大小可能更小：

   ``blocks_area_available_size = region_size_aligned - control_area``

#. 计算单个块大小：

   ``block_size = ROUND_DOWN(blocks_area_available_size / local_blocks, alignment)``

#. 计算实际块区域大小：

   ``blocks_area_size = block_size * local_blocks``

#. 计算块区域起始地址：

   ``blocks_area_begin = region_end_aligned - blocks_area_size``

结果：

* ``region_begin_aligned`` - ICMsg 区域的起始位置。
* ``blocks_area_begin`` - ICMsg 区域的结束位置，也是块区域的起始位置。
* ``block_size`` - 单个块的大小。
* ``region_end_aligned`` - 块区域的结束位置。

.. image:: icbmsg_memory.svg
   :align: center

|

消息传输
--------

ICBMsg 使用以下两种类型的消息：

* **控制消息** - 绑定或解绑等消息。
* **数据消息** - 承载实际用户数据的消息。

它们的用途不同，但生命周期和数据流相同。以下步骤对此进行了说明：

#. 发送方要发送一条包含 ``K`` 字节的消息。
#. 发送方从自己的 ``tx-region`` 块区域中预留能够容纳至少 ``K + 4`` 字节的块。额外的 ``+ 4`` 字节是为头部预留的。这些块必须是连续的（一个接一个）。发送方负责块分配管理。如果块不可用，则线程上下文可能会阻塞，而中断上下文会返回错误。
#. 发送方填写头部。
#. 发送方用其数据填充块的剩余部分。未使用的空间会被忽略。
#. 发送方将消息写入生产者队列，并发送 MBOX 信号。
#. 接收方在 MBOX 中断上下文中执行 MBOX 回调，并读取生产者队列。
#. 接收方读取块索引，并在自己的 ``rx-region`` 中定位该消息。
#. 接收方读取端点以及消息长度，并处理该消息。
#. 接收方通过将消息的块索引写入消费者队列来消费该消息。不会发送 MBOX 信号。
#. 发送方在每次发送之后或发送失败时检查消费者队列。消息会从消费者队列中读取，并释放回池中。

.. image:: icbmsg_message.svg
   :align: center

|

绑定实例
--------

打开后端实例时，会发送一条包含 64 位 magic number 的绑定消息。MBOX 回调会被启用，实例会等待绑定消息。收到绑定消息后，实例便绑定到远程实例，随后可以注册端点。

绑定端点
--------

端点绑定消息包含端点名称的 SHA 以及端点 ID，后者是本地端点数据数组中的索引。

有以下两种可能的情况：

* 远程实例在端点注册之前就发送了该端点的绑定消息。
* 在收到远程实例的绑定消息之前，端点已经注册。

收到绑定消息时，会将 SHA 与端点数据数组中存储的 SHA 进行比较。如果找到匹配项，则表明该端点已由本地实例注册。此时会将端点 ID 存储在端点数据中，并调用 bound 回调。如果未找到匹配项，则寻找空槽，并将端点 ID 和 SHA 存储在可用槽中。

端点注册时，会计算其名称的 SHA，并与端点数据数组中存储的 SHA 进行比较。如果找到匹配项，则表明已收到该端点的远程绑定消息。在这种情况下，会将绑定消息发送到远程实例，并调用 bound 回调。如果未找到匹配项，则寻找空槽，并将端点 ID 和 SHA 存储在可用槽中。绑定消息会发送到远程实例，但端点尚未绑定。

之后，数据消息会使用远程端点 ID 来标识端点。

解绑端点
--------

端点注销时，会发送解绑控制消息，并将该端点从端点数据数组中移除。收到解绑消息时，会将端点槽标记为空，并调用解绑回调。
