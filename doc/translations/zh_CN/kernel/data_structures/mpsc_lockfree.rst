.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mpsc_lockfree:

多生产者单消费者无锁队列
========================

:dfn:`多生产者单消费者无锁队列（MPSC）` 是一种基于原子指针交换的侵入式无锁队列，其算法由 Dmitry Vyukov 在 `1024cores <https://www.1024cores.net/home/lock-free-algorithms/queues/intrusive-mpsc-node-based-queue>`_ 上介绍。


API 参考
********

.. doxygengroup:: mpsc_lockfree
