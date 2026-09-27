.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _task_wdt_api:

任务看门狗
##########

概述
****

许多微控制器都带有硬件看门狗定时器外设。其作用是在软件出现严重故障时触发某个动作（通常是系统复位）。看门狗定时器一旦初始化，就必须定期重新启动（“喂狗”），以防止其超时。如果软件卡死，无法再为看门狗喂狗，就会触发纠正动作，使系统恢复正常运行。

在多个任务并行运行的实时操作系统中，单个看门狗实例可能不再够用，因为它只能用于一个任务。这种基于内核定时器的软件看门狗提供了一种监视多个线程或任务的方法（称为看门狗通道）。

如果任务看门狗本身或调度器出现故障，可以将已有的硬件看门狗用作可选的后备方案。

任务看门狗以内核定时器作为其后端。如果配置得当，正常运行时定时器 ISR 实际上永远不会被调用，因为定时器会在喂狗调用中不断更新。

目前还无法拥有多个任务看门狗实例。取而代之的是，任务看门狗 API 可以全局访问，从而在固件中新增或删除通道时，无需传递上下文或设备指针。

通道的最大数量通过 Kconfig 预定义，应将其调整为与应用程序所需的通道数量完全一致。

配置选项
********

相关的配置选项见 :zephyr_file:`subsys/task_wdt/Kconfig`。

* :kconfig:option:`CONFIG_TASK_WDT`

* :kconfig:option:`CONFIG_TASK_WDT_CHANNELS`

* :kconfig:option:`CONFIG_TASK_WDT_HW_FALLBACK`

* :kconfig:option:`CONFIG_TASK_WDT_MIN_TIMEOUT`

* :kconfig:option:`CONFIG_TASK_WDT_HW_FALLBACK_DELAY`

API 参考
********

.. doxygengroup:: task_wdt_api
