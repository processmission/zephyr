.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _queues:

队列
####

Zephyr 中的队列是实现传统队列的内核对象，允许线程和 ISR 添加或移除任意大小的数据项。队列与 FIFO 类似，是 :ref:`k_fifo <fifos_v2>` 和 :ref:`k_lifo <lifos_v2>` 的底层实现。使用方法详见 :ref:`k_fifo <fifos_v2>`。

取消等待
********

当线程阻塞等待从队列中获取数据项时，其他线程或 ISR 可以调用 :c:func:`k_queue_cancel_wait`，使其在未取得数据项的情况下解除阻塞。队列上第一个挂起等待的线程会从 :c:func:`k_queue_get` 返回 ``NULL``，与超时的行为完全相同。如果通过 :c:func:`k_poll` 等待该队列，则该调用返回 ``-EINTR``，并将轮询事件设为已取消状态。

基于队列的原语也可通过 :c:macro:`k_fifo_cancel_wait` 和 :c:macro:`k_lifo_cancel_wait` 使用此机制。

配置选项
********

相关配置选项：

* 无

API 参考
********

.. doxygengroup:: queue_apis
