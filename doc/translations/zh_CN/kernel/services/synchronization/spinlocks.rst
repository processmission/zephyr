.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _spinlocks:

自旋锁
######

.. contents::
  :local:
  :depth: 2

自旋锁是 Zephyr 中最底层的互斥原语。它保护一小段临界区，确保同一时刻只有一个执行上下文能够访问共享资源。如果发现锁已被持有，当前上下文会“自旋”，即忙等直到锁可用，而不会阻塞并让出 CPU。因此，自旋锁只适合保护短小的临界区。

获取自旋锁还会在持锁期间屏蔽本地 CPU 的中断。这使得线程和中断处理程序能够安全地共用自旋锁：某个上下文持锁时，同一 CPU 上的 ISR 无法抢占它，其他 CPU 也无法获取同一把锁，因此它们都无法在受保护数据更新到一半时读取或破坏这些数据。基于这些特性，:c:struct:`k_spinlock` 是 Zephyr 内核自身使用的主要同步原语，用于保护其核心数据结构。

应用代码也可以直接使用自旋锁，但通常建议使用 :c:struct:`k_mutex` 或 :c:struct:`k_sem` 等更高层的同步原语。

用法
****

为每个需要保护的独立资源声明一个 :c:struct:`k_spinlock`。使用 :c:func:`k_spin_lock` 获取锁，该函数返回一个 :c:type:`k_spinlock_key_t`，释放锁时必须将其传给 :c:func:`k_spin_unlock`：

.. code-block:: c

   static struct k_spinlock lock;

   void update_shared_state(void)
   {
           k_spinlock_key_t key = k_spin_lock(&lock);

           /* critical section: exclusive access */

           k_spin_unlock(&lock, key);
   }

辅助宏 :c:macro:`K_SPINLOCK` 会在所包围的代码块执行期间持锁，并在退出代码块时自动释放锁。

.. code-block:: c

        K_SPINLOCK(&lock) {
                /* critical section: exclusive access */
        }

代码块必须执行到末尾，或使用 :c:macro:`K_SPINLOCK_BREAK` 退出。使用普通的 ``break``、``goto`` 或 ``return`` 退出会跳过释放操作，导致锁一直被持有：

.. code-block:: c

   K_SPINLOCK(&lock) {
           if (nothing_to_do) {
                   K_SPINLOCK_BREAK;
           }

           /* critical section: exclusive access */
   }

不自旋地尝试获取锁
==================

:c:func:`k_spin_trylock` 只尝试获取锁一次，失败时直接报告失败而不等待，适用于调用者还有其他工作要做或不能停滞的情况。成功时，它会保存锁的 key，释放方式与 :c:func:`k_spin_lock` 完全相同：

.. code-block:: c

   k_spinlock_key_t key;

   if (k_spin_trylock(&lock, &key) == 0) {
           /* critical section: exclusive access */
           k_spin_unlock(&lock, key);
   } else {
           /* lock is held elsewhere, do something else */
   }

使用规则
========

使用自旋锁时应遵循以下规则：

* 尽量缩短临界区。持锁期间，本地 CPU 的中断被屏蔽，其他 CPU 也可能在等待这把锁时自旋。
* 持有自旋锁时，绝不能执行阻塞或睡眠操作。
* 不要递归获取自旋锁。已经持锁的上下文不得再次尝试获取同一把锁，否则会发生死锁。可以嵌套使用 **不同的** 自旋锁，但必须遵循一致的加锁顺序，以避免死锁。

单处理器系统上的自旋锁
**********************

在未启用 :kconfig:option:`CONFIG_SMP` 的内核中，自旋锁实际上不会自旋。系统只有一个 CPU，不存在 CPU 之间的竞争，因此 :c:func:`k_spin_lock` 只需屏蔽本地 CPU 的中断。这样可以防止 ISR 或上下文切换在受保护数据更新到一半时访问这些数据，足以在单处理器上实现互斥。

自旋锁校验
**********

启用 :kconfig:option:`CONFIG_SPIN_VALIDATE` 可以使用校验层来检测各种自旋锁误用，包括：

* 递归获取自旋锁
* 释放当前上下文未持有的自旋锁
* 未按顺序释放自旋锁（仍持有内层锁时就释放外层锁）
* 持有自旋锁时，或中断被嵌套的 :c:func:`irq_lock` 屏蔽时，发生上下文切换

在单处理器系统上，只有递归获取检查有意义。由于不存在竞争且持锁期间中断被屏蔽，其他误用情况不会发生。

公平自旋锁
**********

默认的自旋锁实现基于单个 ``atomic_t`` 变量，不保证竞争 CPU 之间的公平性：某个 CPU 可能反复赢得竞争，使其他 CPU 饥饿。如果需要公平性，可以启用 :kconfig:option:`CONFIG_TICKET_SPINLOCKS`，切换到基于票据的实现。该实现按 FIFO 顺序将有竞争的锁授予请求它的 CPU，代价是锁对象略大。

使用建议
********

使用自旋锁保护线程与中断处理程序之间，或 SMP 系统的 CPU 之间共享的短小临界区。

如果其他原语更合适，应优先使用：

* :c:struct:`k_mutex` 适用于可能执行较长时间、阻塞或睡眠的临界区。只有线程可以获取互斥量。
* :c:struct:`k_sem` 用于在上下文之间发送信号，以及对资源池的访问进行计数。
* 如果共享状态只有一个字，且可用一次原子操作更新，则使用 :ref:`原子服务 <atomic_v2>`，无需加锁。

API 参考
********

.. doxygengroup:: spinlock_apis
