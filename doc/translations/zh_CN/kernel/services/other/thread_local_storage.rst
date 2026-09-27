.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _thread_local_storage:

线程局部存储（TLS）
###################

线程局部存储（TLS）允许按线程分配变量。这些变量存储在线程栈中，因此每个线程都有这些变量的独立副本。

Zephyr 目前要求工具链支持 TLS。


配置
****

要在 Zephyr 中启用线程局部存储，需要启用 :kconfig:option:`CONFIG_THREAD_LOCAL_STORAGE`。注意，如果架构或 SoC 未启用隐藏选项 :kconfig:option:`CONFIG_ARCH_HAS_THREAD_LOCAL_STORAGE`，则此选项可能不可用。这意味着该架构或 SoC 缺少支持线程局部存储所需的代码，和／或工具链不支持 TLS。

可以同时启用 :kconfig:option:`CONFIG_ERRNO_IN_TLS` 和 :kconfig:option:`CONFIG_ERRNO`，使变量 ``errno`` 成为线程局部变量。这样，用户线程无需进行系统调用即可访问 ``errno`` 的值。


声明和使用线程局部变量
**********************

可以使用宏 ``Z_THREAD_LOCAL`` 声明线程局部变量。

例如，在头文件中声明线程局部变量：

.. code-block:: c

   extern Z_THREAD_LOCAL int i;

并在源文件中定义实际变量：

.. code-block:: c

   Z_THREAD_LOCAL int i;

还可以使用关键字 ``static`` 将变量的作用域限制在一个源文件内：

.. code-block:: c

   static Z_THREAD_LOCAL int j;

线程局部变量的用法与其他变量相同，例如：

.. code-block:: c

   void testing(void) {
       i = 10;
   }
