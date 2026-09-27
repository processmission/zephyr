.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _cmsis_rtos_v2:

CMSIS RTOS v2
#############

Cortex-M 软件接口标准（CMSIS）RTOS 是一个厂商无关的硬件抽象层，面向 ARM Cortex-M 处理器系列，并定义了通用工具接口。虽然它最初仅针对 ARM Cortex-M 微控制器定义，但可以轻松扩展到其他微控制器，从而使其具有通用性。有关 CMSIS RTOS v2 的更多信息，请参阅 `CMSIS-RTOS2 Documentation <https://arm-software.github.io/CMSIS_6/latest/RTOS2/index.html>`_。

Zephyr 实现中不支持的功能
*************************

内核
   不支持 ``osKernelGetState``、``osKernelSuspend``、``osKernelResume``、``osKernelInitialize`` 和 ``osKernelStart``。

互斥量
   ``osMutexPrioInherit`` 默认受支持且不可配置，你无法选择或取消选择该属性。

   ``osMutexRecursive`` 默认也受支持。如果未设置该属性，同一线程第二次尝试获取它时会抛出错误。

   Zephyr 不支持 ``osMutexRobust``。

Zephyr 实现中不支持的返回值
***************************

``osKernelUnlock``, ``osKernelLock``, ``osKernelRestoreLock``
   不支持 ``osError`` （未指定的错误）。

``osSemaphoreDelete``
   不支持 ``osErrorResource`` （参数 semaphore_id 指定的信号量处于无效的信号量状态）。

``osMutexDelete``
   不支持 ``osErrorResource`` （参数 mutex_id 指定的互斥量处于无效的互斥量状态）。

``osTimerDelete``
   不支持 ``osErrorResource`` （参数 timer_id 指定的定时器处于无效的定时器状态）。

``osMessageQueueReset``
   不支持 ``osErrorResource`` （参数 msgq_id 指定的消息队列处于无效的消息队列状态）。

``osMessageQueueDelete``
   不支持 ``osErrorResource`` （参数 msgq_id 指定的消息队列处于无效的消息队列状态）。

``osMemoryPoolFree``
   不支持 ``osErrorResource`` （参数 mp_id 指定的内存池处于无效的内存池状态）。

``osMemoryPoolDelete``
   不支持 ``osErrorResource`` （参数 mp_id 指定的内存池处于无效的内存池状态）。

``osEventFlagsSet``, ``osEventFlagsClear``
   不支持 ``osFlagsErrorUnknown`` （未指定的错误）和 osFlagsErrorResource（参数 ef_id 指定的事件标志对象尚未准备好，无法使用）。

``osEventFlagsDelete``
   不支持 ``osErrorParameter`` （参数 ef_id 的值不正确）。

``osThreadFlagsSet``
   不支持 ``osFlagsErrorUnknown`` （未指定的错误）和 ``osFlagsErrorResource`` （参数 thread_id 指定的线程未处于活动状态，无法接收标志）。

``osThreadFlagsClear``
   不支持 ``osFlagsErrorResource`` （运行中的线程未处于活动状态，无法接收标志）。

``osDelayUntil``
   不支持 ``osParameter`` （无法处理该时间）。
