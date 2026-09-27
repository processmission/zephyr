.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _condvar:

条件变量
########

:dfn:`条件变量` 是一种同步原语，使线程能够等待特定条件成立。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的条件变量（仅受可用 RAM 限制）。每个条件变量都通过其内存地址引用。

线程可以使用条件变量来等待某个条件成立。

条件变量本质上是一个线程队列。当某种执行状态（即某个条件）不符合预期时，线程可以通过等待该条件将自身加入队列。函数 :c:func:`k_condvar_wait` 以原子方式执行以下步骤：

#. 释放最近获取的互斥量。
#. 将当前线程加入条件变量的队列。

其他线程改变上述状态后，可以调用 :c:func:`k_condvar_signal` 或 :c:func:`k_condvar_broadcast` 发出条件通知，唤醒一个或多个等待线程，使其继续执行。被唤醒的线程随后会：

#. 重新获取先前释放的互斥量。
#. 从 :c:func:`k_condvar_wait` 返回。

无论等待因何结束——线程收到通知、指定的超时时间已到，或本次请求为非阻塞等待——:c:func:`k_condvar_wait` 返回时，调用线程始终已经重新锁定关联的互斥量。

条件变量必须初始化后才能使用。


实现
****

定义条件变量
============

条件变量使用 :c:struct:`k_condvar` 类型的变量定义，随后必须调用 :c:func:`k_condvar_init` 进行初始化。

以下代码定义一个条件变量：

.. code-block:: c

    struct k_condvar my_condvar;

    k_condvar_init(&my_condvar);

也可以使用 :c:macro:`K_CONDVAR_DEFINE` 在编译时定义并初始化条件变量。

以下代码与上面的代码片段效果相同。

.. code-block:: c

    K_CONDVAR_DEFINE(my_condvar);

等待条件变量
============

线程可以调用 :c:func:`k_condvar_wait` 等待条件成立。

以下代码等待条件变量。


.. code-block:: c

    K_MUTEX_DEFINE(mutex);
    K_CONDVAR_DEFINE(condvar)

    int main(void)
    {
        k_mutex_lock(&mutex, K_FOREVER);

        /* block this thread until another thread signals cond. While
         * blocked, the mutex is released, then re-acquired before this
         * thread is woken up and the call returns.
         */
        k_condvar_wait(&condvar, &mutex, K_FOREVER);
        ...
        k_mutex_unlock(&mutex);
    }

通知条件变量
============

调用 :c:func:`k_condvar_signal` 可以向一个线程发出条件变量通知；调用 :c:func:`k_condvar_broadcast` 则可以通知多个线程。

以下代码延续上面的示例。

.. code-block:: c

    void worker_thread(void)
    {
        k_mutex_lock(&mutex, K_FOREVER);

        /*
         * Do some work and fulfill the condition
         */
        ...
        ...
        k_condvar_signal(&condvar);
        k_mutex_unlock(&mutex);
    }

使用建议
********

将条件变量与互斥量配合使用，可以在线程之间通知状态（条件）的变化。条件变量并非条件本身，也不是事件。实际条件由周围的程序逻辑表达。

互斥量本身并不是用于通知或同步的机制，其用途仅限于提供对共享资源的互斥访问。

配置选项
********

相关配置选项：

* 无。

API 参考
********

.. doxygengroup:: condvar_apis
