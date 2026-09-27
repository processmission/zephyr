.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _nothread:

无线程运行
##########

某些应用程序不需要线程支持：

* 引导加载程序
* 简单的事件驱动应用程序
* 用于演示核心功能的示例

将 :kconfig:option:`CONFIG_MULTITHREADING` 设置为 ``n`` 可以禁用线程支持。由于此配置会显著影响 Zephyr 的功能，且相关测试有限，因此能够正常工作的功能受到一定限制。

预期可以正常工作的功能
**********************

禁用 :kconfig:option:`CONFIG_MULTITHREADING` 时，以下核心功能应能正常工作：

* :ref:`构建系统 <application>`

* 将应用程序引导至 ``main()`` 的能力

* :ref:`中断管理 <interrupts_v2>`

* 系统时钟，包括 :c:func:`k_uptime_get`

* 定时器，即 :c:func:`k_timer`

* 不休眠的延时，例如 :c:func:`k_busy_wait`。

* 通过 :c:func:`k_cpu_idle` 休眠。

* 在 ``main()`` 之前初始化驱动程序和子系统，例如 :c:macro:`SYS_INIT`。

* :ref:`kernel_memory_management_api`

* 下文列出的特定子系统中的指定驱动程序。

上述预期会影响其他功能的选择；例如，不能将 :kconfig:option:`CONFIG_SYS_CLOCK_EXISTS` 设置为 ``n``。

无法保证正常工作的功能
**********************

禁用 :kconfig:option:`CONFIG_MULTITHREADING` 时无法工作的功能包括大多数内核 API：

* :ref:`threads_v2`

* :ref:`scheduling_v2`

* :ref:`workqueues_v2`

* :ref:`polling_v2`

* :ref:`semaphores_v2`

* :ref:`mutexes_v2`

* :ref:`condvar`

* :ref:`kernel_data_passing_api`

.. contents::
    :local:
    :depth: 1

无线程支持时的子系统行为
************************

以下各节列出禁用 :kconfig:option:`CONFIG_MULTITHREADING` 时预期仍能提供部分功能的驱动程序和功能子系统。未列出的子系统不应被认为能够正常工作。

所列子系统中的某些现有驱动程序在禁用线程时无法工作，但它们因所属子系统而处于支持范围内，或者具有足够的独立性，使得在特定平台上支持它们只需很小的改动。对于原本未实现无线程运行的现有功能，将考虑接受增加此类支持的增强改动。

Flash
=====

所有 SoC 闪存外设驱动程序的 :ref:`flash_api` 预期都能正常工作。通过总线访问的设备（例如串行存储器）可能不受支持。

*此处将列出受支持驱动程序的列表或表格*

GPIO
====

所有 SoC GPIO 外设驱动程序的 :ref:`gpio_api` 预期都能正常工作。通过总线访问的设备（例如 GPIO 扩展器）可能不受支持。

*此处将列出受支持驱动程序的列表或表格*

UART
====

所有 SoC UART 外设驱动程序预期都能支持 :ref:`uart_api` 的一部分功能。

* 选择 :kconfig:option:`CONFIG_UART_INTERRUPT_DRIVEN` 的应用程序可能可以正常工作，具体取决于驱动程序实现。

* 选择 :kconfig:option:`CONFIG_UART_ASYNC_API` 的应用程序可能可以正常工作，具体取决于驱动程序实现。

* 既未选择 :kconfig:option:`CONFIG_UART_ASYNC_API` 也未选择 :kconfig:option:`CONFIG_UART_INTERRUPT_DRIVEN` 的应用程序预期可以正常工作。

*此处将列出受支持驱动程序的列表或表格，包括支持的 API 选项*
