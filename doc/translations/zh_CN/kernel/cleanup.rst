.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _cleanup_api:

基于作用域的清理辅助工具
########################

.. contents::
    :local:
    :depth: 2

概述
****

清理辅助 API 提供在变量离开作用域时自动清理资源的机制，类似于 C++ 的 RAII 或 Go 的 defer 语句。该 API 利用编译器对 ``__cleanup`` 属性的支持，确保清理代码自动执行，从而防止资源泄漏并简化错误处理。

必须设置 :kconfig:option:`CONFIG_SCOPE_CLEANUP_HELPERS` 才能启用此功能。它尤其适用于：

* 自动释放互斥量和信号量
* 自动释放动态分配的内存
* 确保所有代码路径（包括提前返回）都会执行清理操作
* 减少重复的清理代码

.. warning::

   清理机制使用 ``__cleanup`` 属性实现。如果工具链不支持此属性，则该 API 不可用。

   因此，该 API 仅供用户应用程序使用，不供内核本身或其他子系统使用。

核心概念
********

清理 API 提供三种主要抽象：

作用域变量
==========

作用域变量定义一种具备自动初始化和退出行为的类型。以作用域变量类型声明的变量由初始化函数初始化，并在离开作用域时由退出函数自动清理。

作用域守卫
==========

作用域守卫是一种专用的作用域变量，在初始化时自动获取锁或资源，并在离开作用域时释放。这种模式常用于互斥量、信号量及其他同步原语。

作用域延迟操作
==============

作用域延迟操作在变量离开作用域时执行指定函数，初始化时不获取任何资源。这类似于 Go 等语言中的 ``defer`` 语句。

定义作用域类型
**************

自定义作用域变量
================

使用 :c:macro:`SCOPE_VAR_DEFINE` 定义带有初始化函数和退出函数的自定义作用域变量类型：

.. code-block:: c

    static inline struct flash_area *flash_area_init(int area_id)
    {
        struct flash_area *fa;

        if (flash_area_open(area_id, &fa) < 0) {
            return NULL;
        }

        return fa;
    }

    static inline void flash_area_exit(struct flash_area *fa)
    {
        if (fa != NULL) {
            flash_area_close(fa);
        }
    }

    // Define the scoped variable type
    SCOPE_VAR_DEFINE(flash_area, struct flash_area *, flash_area_exit(_T),
                     flash_area_init(area_id), int area_id);

    static int some_function(void)
    {
        // Declare 'fa' with automatic cleanup
        scope_var(flash_area, fa)(PARTITION_ID(storage_partition));
        if (fa == NULL) {
            return -EINVAL;  // Exit function is still called
        }

        // Use fa normally
        printk("Has driver: %d\n", flash_area_has_driver(fa));

        // No need to manually close - exit function is called automatically
        return 0;
    }

退出函数表达式中的 ``_T`` 变量包含正在清理的变量的值。

Scoped Guards
=============

使用 :c:macro:`SCOPE_GUARD_DEFINE` 定义一个守卫，在初始化时获取锁，在退出作用域时释放锁：

.. code-block:: c

    // Example guard definition (already provided by <zephyr/cleanup/kernel.h>)
    SCOPE_GUARD_DEFINE(k_mutex, struct k_mutex *,
                       (void)k_mutex_lock(_T, K_FOREVER),
                       (void)k_mutex_unlock(_T));

    static K_MUTEX_DEFINE(lock);

    void critical_section(void)
    {
        scope_guard(k_mutex)(&lock);

        // Lock is held here
        // Perform critical operations

        // Lock is automatically released when guard goes out of scope
    }

块作用域守卫
============

:c:macro:`scope_guard` 将守卫保持到 *外围* 作用域结束，而 :c:macro:`scoped_guard` 将守卫绑定到紧随其后的花括号块，并在退出该块时立即释放。这样可以明确标出短小的临界区，并将锁对象放在其保护的代码旁边：

.. code-block:: c

    static K_MUTEX_DEFINE(lock);

    void worker(void)
    {
        // ... work that does not need the lock ...

        scoped_guard(k_mutex, &lock) {
            // lock held only inside these braces
        }
        // lock released here

        // ... more work without the lock held ...
    }

该块恰好执行一次。无论以何种方式退出该块，包括 ``break``、``return`` 和 ``goto``，都会释放锁。注意，``continue`` 会离开该块（行为与 ``break`` 相同），而不会重新执行该块。

条件守卫
========

使用 :c:macro:`SCOPE_GUARD_DEFINE` 定义的守卫总会获取锁（以 ``K_FOREVER`` 阻塞）。要表示可能获取失败的守卫（例如使用非阻塞的 ``K_NO_WAIT`` 尝试加锁），请将 :c:macro:`SCOPE_COND_GUARD_DEFINE` 与 :c:macro:`scoped_cond_guard` 配合使用。获取表达式会被求值以判定是否成功：失败时，守卫保存 ``NULL``，执行提供的失败语句，并跳过该块。

.. code-block:: c

    // Example guard definition (already provided by <zephyr/cleanup/kernel.h>)
    SCOPE_COND_GUARD_DEFINE(k_mutex_try, struct k_mutex *,
                            k_mutex_lock(_T, K_NO_WAIT) == 0,
                            (void)k_mutex_unlock(_T));

    static K_MUTEX_DEFINE(lock);

    int try_critical_section(void)
    {
        scoped_cond_guard(k_mutex_try, return -EBUSY, &lock) {
            // runs only if the lock was acquired
            // released automatically when the block is exited
        }

        return 0;
    }

失败语句可以是任意语句，例如 ``break``、``return -EBUSY``，或用于静默跳过该块的 ``{}``。

Scoped Defers
=============

使用 :c:macro:`SCOPE_DEFER_DEFINE` 定义执行清理函数的延迟操作：

.. code-block:: c

    // Define a defer for a custom cleanup function
    static void cleanup_resources(void)
    {
        // Cleanup code here
    }

    SCOPE_DEFER_DEFINE(cleanup_resources);

    void some_function(void)
    {
        scope_defer(cleanup_resources)();

        // Do work...

        // cleanup_resources() is called automatically
    }

对于带参数的函数：

.. code-block:: c

    // Example deferred k_free (already provided by <zephyr/cleanup/kernel.h>)
    SCOPE_DEFER_DEFINE(k_free, void *);

    void allocate_and_use(void)
    {
        void *ptr = k_malloc(100);
        scope_defer(k_free)(ptr);

        // Use ptr...

        // k_free(ptr) is called automatically
    }

使用说明
********

清理顺序
========

清理函数按照声明的逆序调用（LIFO，后进先出），与资源自然嵌套的顺序一致：

.. code-block:: c

    {
        scope_guard(k_mutex)(&lock);           // Acquired first
        void *ptr = k_malloc(100);
        scope_defer(k_free)(ptr);              // Registered second

        // Do work...

    }  // ptr is freed first, then mutex is unlocked

作用域规则
==========

变量离开作用域时会执行清理，包括：

* 到达块的末尾
* 提前返回语句
* 循环中的 break 或 continue
* 跳出作用域的 goto 语句

.. code-block:: c

    void example_with_early_exit(struct k_mutex *lock)
    {
        scope_guard(k_mutex)(lock);

        if (error_condition) {
            return;  // Guard cleanup happens here
        }

        // Normal path

    }  // Guard cleanup also happens here

API 参考
********

.. doxygengroup:: cleanup_interface
