.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _fixed_size_ringq_api:

sys_ringq 数据结构
##################

.. contents::
  :local:
  :depth: 2

概述
****

环形队列（或环形缓冲区）使用一个固定大小的缓冲区，并将其视为首尾相连。这种结构尤其适合按顺序缓冲数据项。

需要将离散数据项的生产者与消费者解耦，同时无需处理部分读取或变长载荷时，可以使用 ringq。这也是它与面向字节流的 :ref:`ring_buffer <ring_buffers_v2>` 数据结构的区别。

并发
====

sys_ringq API 不提供任何并发控制。应用应根据使用方式，采用适当的同步机制（例如互斥量、信号量）保护 sys_ringq 结构，确保多个线程访问时的线程安全。

实例化与用法
************

可以使用 ``SYS_RINGQ_DEFINE(name, item_size, item_capacity)`` 宏声明 ``sys_ringq``，也可以在运行时使用 ``sys_ringq_init(struct sys_ringq *ringq, uint8_t *data, size_t data_size, size_t item_size);`` 函数初始化。

.. code-block:: c

   SYS_RINGQ_DEFINE(my_ringq, item_size, item_capacity);
   /* equivalent to */

   static struct sys_ringq my_ringq;
   static uint8_t buffer[item_size * item_capacity];
   void init_fn (void) {
      sys_ringq_init(&my_ringq, buffer, sizeof(buffer), item_size);
      ....
   }

``sys_ringq`` 初始化后，可以使用 ``sys_ringq_put()`` 添加数据项，使用 ``sys_ringq_get()`` 移除数据项。ringq 会维护数据项的顺序，并对底层数据缓冲区进行适当的边界检查。

.. code-block:: c

    struct my_item item_to_add = { ... };
    struct my_item item_removed;

    /* Add an item to the queue */
    if (sys_ringq_put(&my_ringq, &item_to_add) == 0) {
        // Item added successfully
    } else {
        // ringq is full
    }

    /* Remove an item from the queue */
    if (sys_ringq_get(&my_ringq, &item_removed) == 0) {
        // Item removed successfully
    } else {
        // ringq is empty
    }

除了标准数据操作 sys_ringq_put() 和 sys_ringq_get()，sys_ringq API 还提供一组辅助函数，用于管理和检查数据结构的状态。

* sys_ringq_capacity() —— 返回 sys_ringq 的总容量，以可容纳的数据项数量表示。
* sys_ringq_empty() —— 如果 sys_ringq 不含任何数据项，则返回 true。
* sys_ringq_full() —— 如果 sys_ringq 无法再接收数据项，则返回 true。
* sys_ringq_space() —— 返回剩余空闲槽位的数量。
* sys_ringq_size() —— 返回当前存储的数据项数量。
* sys_ringq_reset() —— 将 sys_ringq 重置为空状态。

API 参考
********
.. doxygengroup:: sys_ringq_apis
