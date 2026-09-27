.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _hwspinlock_api:

硬件自旋锁（HWSPINLOCK）
########################

概述
****

HWSPINLOCK 设备是一种外设，用于保护系统中跨集群共享的资源。每个 HWSPINLOCK 实例提供一个或多个自旋锁。其 API 与常规 Zephyr 自旋锁的 API 类似。

.. doxygengroup:: spinlock_apis

由于还需要保护同一集群中多个核心使用的自旋锁资源，因此每个 HWSPINLOCK 设备都包含一个常规 Zephyr 自旋锁，并使用它对 HWSPINLOCK 硬件的访问进行加锁。

API 参考
********

.. doxygengroup:: hwspinlock_interface
