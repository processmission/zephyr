.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ring_buffers_v2:

环形缓冲区
##########

:dfn:`环形缓冲区` 是一种首尾相接的缓冲区，其内容按先进先出的顺序存储。

对于需要异步“流式”复制数据的应用，Zephyr 提供 ``struct ring_buf`` 抽象，用于管理数据与共享内存缓冲区之间的复制。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的环形缓冲区（仅受可用 RAM 限制）。每个环形缓冲区都通过其内存地址引用。

环形缓冲区具有以下主要属性：

* 一个按字节组织的 **数据缓冲区**，保存已加入环形缓冲区但尚未移除的原始字节。

* **数据缓冲区大小**，以字节为单位，决定环形缓冲区能容纳的最大数据量。

环形缓冲区必须初始化后才能使用。初始化会将其数据缓冲区置空。

``struct ring_buf`` 可以放在任意用户可访问的内存中，使用前必须通过 :c:func:`ring_buf_init` 初始化，并提供一块由用户管理的内存作为缓冲区。需特别注意，传入的缓冲区大小单位可能为字节或字，取决于之后的使用方式。为方便使用，库提供宏将这些步骤合并为一次静态声明。:c:macro:`RING_BUF_DECLARE` 可按指定字节数声明并静态初始化环形缓冲区。

传入数据指针和字节数后，可以使用 :c:func:`ring_buf_put` 将“字节”数据复制到环形缓冲区。字节会按顺序写入，直到分配的缓冲区无法容纳更多数据。函数返回实际复制的总字节数，可能少于请求值。同样，:c:func:`ring_buf_get` 按写入顺序将字节从环形缓冲区复制到用户提供的缓冲区，并返回实际传输的字节数。

为避免数据多次复制，库提供零复制的“指针”API。:c:func:`ring_buf_put_ptr` 返回指向环形缓冲区内部可接收字节区域的指针，以及可写连续区域的大小；如果发生回绕，该大小可能小于总空闲空间。用户可以直接向该区域写入数据，例如通过 DMA，而无需先将全部字节汇集到一个区域。完成后，调用 :c:func:`ring_buf_commit` 并传入实际传输的字节数，通知缓冲区传输已完成，此后即可开始新的传输。类似地，:c:func:`ring_buf_get_ptr` 返回内部数据的指针，用户可直接读取而无需完整复制；:c:func:`ring_buf_consume` 则通知缓冲区已消费多少字节，使新的传输可以开始。

旧版 :c:func:`ring_buf_put_claim` / :c:func:`ring_buf_put_finish` 以及 :c:func:`ring_buf_get_claim` / :c:func:`ring_buf_get_finish` API 提供类似功能，但会将认领的区域保留到操作完成，因此增加代码体积和运行时开销。这些 API 已弃用，将在未来版本移除；新代码应使用上述 ``_ptr`` / ``_commit`` / ``_consume`` 版本。

用户可以在不修改环形缓冲区的情况下检查容量：:c:func:`ring_buf_space_get` 返回空闲字节数，:c:func:`ring_buf_is_empty` 则用于判断缓冲区是否为空。

最后，可以调用 :c:func:`ring_buf_reset` 立即清空环形缓冲区，丢弃对已写入字节的跟踪信息。不过，它不会修改缓冲区自身的内存内容。


实例化与用法
============

使用 :c:macro:`RING_BUF_DECLARE()` 声明环形缓冲区实例，并通过 :c:func:`ring_buf_put_ptr`、:c:func:`ring_buf_commit`、:c:func:`ring_buf_get_ptr`、:c:func:`ring_buf_consume`、:c:func:`ring_buf_put` 和 :c:func:`ring_buf_get` 访问。

数据可以复制到环形缓冲区（见 :c:func:`ring_buf_put`），也可以由用户直接使用环形缓冲区的内存。后一种方式分为三个阶段：

1. 通过 :c:func:`ring_buf_put_ptr` 访问内部缓冲区，获取下一个可写位置的指针，以及该位置可用连续空间的大小。
#. 由用户写入数据，例如通过 DMA 写入缓冲区。
#. 通过 :c:func:`ring_buf_commit` 指明写入所提供缓冲区的数据量。提交量可以小于或等于 :c:func:`ring_buf_put_ptr` 提供的大小。


可以通过复制从环形缓冲区获取数据（见 :c:func:`ring_buf_get`），也可以直接通过地址访问。后一种方式分为三个阶段：

1. 通过 :c:func:`ring_buf_get_ptr` 访问内部缓冲区，获取下一个可读位置的指针，以及该位置可用连续数据的大小。
#. 处理数据
#. 通知环形缓冲区数据已被消费（见 :c:func:`ring_buf_consume`）。消费量可以小于或等于 :c:func:`ring_buf_get_ptr` 提供的大小。

并发
====

环形缓冲区 API 不提供内部并发控制。应用可能需要根据使用方式，尤其是并发读写者的数量，使用互斥量保护环形缓冲区，并且／或者使用信号量通知消费者有数据可读。

分别运行于不同执行上下文中的单个生产者和单个消费者，例如两个线程，或一个线程与一个 ISR，可以并发使用同一环形缓冲区，无需额外加锁。生产者只更新 ``put`` 索引，消费者只更新 ``get`` 索引，双方不会写入同一字段。这既适用于复制 API（:c:func:`ring_buf_put` / :c:func:`ring_buf_get`），也适用于零复制的“认领”API（:c:func:`ring_buf_put_claim` / :c:func:`ring_buf_put_finish` 和 :c:func:`ring_buf_get_claim` / :c:func:`ring_buf_get_finish`）。

生产者和消费者在不同 CPU 上运行（SMP）时，应用仍须确保数据写入在发布这些数据的索引更新之前已经可见。实际中，如果双方使用内核同步原语协调，例如由生产者释放、消费者等待的 :c:struct:`k_sem`，这些原语所包含的内存屏障就能保证这一点，无需额外操作。

只要存在多个并发生产者或多个并发消费者，就必须在外部将相应访问串行化，例如使用互斥量或禁止抢占。

内部工作方式
============

流经环形缓冲区的数据始终写入下一个字节位置，到达末尾后回绕至第一个元素，由此形成“环”。``struct ring_buf`` 内部保存缓冲区指针、大小，以及表示下一次读写位置的一组“head”和“tail”索引。

使用普通 put/get API 时，用户看不到这个边界；但对于“认领”API，它构成了限制，因为返回的连续区域显然不能跨越缓冲区末尾。这可能出乎应用代码的预料，并影响接近缓冲区末尾处的传输性能，因为这些传输所需的 claim/finish 调用次数会加倍。


实现
****

定义环形缓冲区
==============

环形缓冲区使用 :c:struct:`ring_buf` 类型的变量定义，随后必须调用 :c:func:`ring_buf_init` 进行初始化。

可以在文件作用域使用宏，在编译时定义并初始化环形缓冲区。宏会同时定义环形缓冲区自身及其数据缓冲区。

以下代码定义一个环形缓冲区：

.. code-block:: c

    #define MY_RING_BUF_BYTES 93
    RING_BUF_DECLARE(my_ring_buf, MY_RING_BUF_BYTES);

数据入队
========

调用 :c:func:`ring_buf_put` 可以将字节复制到环形缓冲区。

.. code-block:: c

    uint8_t my_data[MY_RING_BUF_BYTES];
    uint32_t ret;

    ret = ring_buf_put(&ring_buf, my_data, MY_RING_BUF_BYTES);
    if (ret != MY_RING_BUF_BYTES) {
        /* not enough room, partial copy. */
        ...
    }

也可以直接访问环形缓冲区的内存来添加数据。例如：

.. code-block:: c

    uint32_t size;
    uint32_t rx_size;
    uint8_t *data;

    /* Get pointer to writable area within the ring buffer memory. */
    size = ring_buf_put_ptr(&ring_buf, &data, 0);

    /* Work directly on a ring buffer memory. */
    rx_size = uart_rx(data, size);

    /* Indicate amount of valid data. rx_size must be equal or less than size. */
    ring_buf_commit(&ring_buf, rx_size);


取回数据
========

调用 :c:func:`ring_buf_get` 可以将数据字节从环形缓冲区复制出来。例如：

.. code-block:: c

    uint8_t my_data[MY_DATA_BYTES];
    size_t  ret;

    ret = ring_buf_get(&ring_buf, my_data, sizeof(my_data));
    if (ret != sizeof(my_data)) {
        /* Fewer bytes copied. */
    } else {
        /* Requested amount of bytes retrieved. */
        ...
    }

也可以直接操作环形缓冲区的内存来取回数据。例如：

.. code-block:: c

    uint32_t size;
    uint32_t proc_size;
    uint8_t *data;

    /* Get pointer to readable data within the ring buffer memory. */
    size = ring_buf_get_ptr(&ring_buf, &data, 0);

    /* Work directly on a ring buffer memory. */
    proc_size = process(data, size);

    /* Indicate amount of data that has been consumed. proc_size must be equal
     * or less than size.
     */
    ring_buf_consume(&ring_buf, proc_size);

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_RING_BUFFER`：恢复已弃用的旧版环形缓冲区 API，包括 claim/finish 和固定大小数据项 API。环形缓冲区自身完全由头文件实现，始终可用，正常使用无需启用此选项。
* :kconfig:option:`CONFIG_RING_BUFFER_LARGE`：将缓冲区大小上限从 32KB 提高到 1GB。

API 参考
********

:zephyr_file:`include/zephyr/sys/ring_buffer.h` 提供以下环形缓冲区 API：

.. doxygengroup:: ring_buffer_apis
