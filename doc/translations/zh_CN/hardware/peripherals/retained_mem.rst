.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _retained_mem_api:

保持内存
########

概述
****

保持内存驱动 API 提供了读写特定内存区域的方法，这些区域的内容在设备供电期间得以保留（在低功耗模式下数据可能丢失）。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_RETAINED_MEM`
* :kconfig:option:`CONFIG_RETAINED_MEM_INIT_PRIORITY`
* :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE`

互斥锁保护
**********

当应用编译时启用多线程支持，保持内存驱动的互斥锁保护默认启用。这意味着不同线程可以安全地调用保持内存函数，而不会与其他线程的并发函数调用发生冲突，但也意味着无法在中断服务例程（ISR）中使用保持内存函数。通过启用 :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE` 可以全局禁用所有保持内存驱动的互斥锁保护，此时用户需自行确保各函数调用之间不会发生冲突。

API 参考
********

.. doxygengroup:: retained_mem_interface
