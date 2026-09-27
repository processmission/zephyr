.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _cpu_load:

CPU 负载
########

CPU 负载模块跟踪 CPU 处于非空闲状态的时间占比。可用两种测量后端，通过 ``CPU_LOAD_BACKEND`` Kconfig 选项选择：

调度器运行时统计
   :kconfig:option:`CONFIG_CPU_LOAD_BACKEND_RUNTIME_STATS` 根据调度器的每 CPU 运行时统计推导负载。它可跨架构移植，并支持多 CPU。

架构空闲钩子
   :kconfig:option:`CONFIG_CPU_LOAD_BACKEND_IDLE_HOOK` 使用在 CPU 进入空闲之前和之后调用的架构空闲钩子来测量负载。它比运行时统计后端的开销更低，并可以使用 :ref:`counter_api` 设备获得更高精度（计数器方式仅支持单 CPU）。任何会发出空闲钩子的架构都可以使用它（:kconfig:option:`CONFIG_ARCH_HAS_CPU_IDLE_HOOKS`）。与 :ref:`thread_analyzer` 相比，它更准确，因为它还把在中断上下文中花费的时间计算在内。此后端不依赖跟踪子系统。

可以使用 :c:func:`cpu_load_get` 获取当前 CPU 的负载，或使用 :c:func:`cpu_load_get_cpu` 获取指定 CPU 的负载。两者都以千分比（0...1000）返回负载，并可以重置测量窗口。使用 :c:macro:`CPU_LOAD_PERMILLE_TO_PERCENT` 可以把该值转换为整数百分比。

负载也可以通过日志消息定期上报。周期通过 :kconfig:option:`CONFIG_CPU_LOAD_LOG_PERIODICALLY` 配置。

示例请参见 :zephyr:code-sample:`cpu_freq_on_demand` 示例。

使用计数器设备
**************

空闲钩子后端默认使用 :c:func:`k_cycle_get_32`。当需要更高精度时，可以启用 :kconfig:option:`CONFIG_CPU_LOAD_USE_COUNTER` 并在 devicetree 中设置 chosen 节点，从而使用 :ref:`counter_api` 设备。

.. code-block:: devicetree

   chosen {
     zephyr,cpu-load-counter = &counter_device;
   };
