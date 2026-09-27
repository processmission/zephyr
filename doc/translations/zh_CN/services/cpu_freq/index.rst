.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _cpu_freq:

CPU 频率调节
############

.. toctree::
   :maxdepth: 1

   policies/index.rst
   thermal_cap.rst

概述
****

Zephyr 中的 CPU 频率调节子系统为 SoC 提供了一个框架，使其能够根据受监控的指标和性能状态（P-state）策略算法动态调整处理器频率。

设计目标
********

CPU 频率调节子系统旨在提供一个框架，使任何策略算法都能与任何 P-state 驱动配合工作，并允许每个策略使用一个或多个指标来确定最优 CPU 频率。该子系统应足够灵活，以便 SoC 厂商定义自定义 P-state、阈值和指标。

P-state 策略
************

P-state 策略是一种算法，它根据所使用的指标以及针对每个 P-state 定义的阈值，确定 CPU 的最优 P-state。策略可以使用一个或多个指标，根据系统期望的统计数据确定最优 CPU 频率。

有关标准策略的列表，请参阅 :ref:`策略 <cpu_freq_policies>`。

指标
****

P-state 策略应包含一个或多个用于决策的指标。指标示例可以包括 CPU 负载百分比、SoC 温度等。

有关使用指标的示例，请参阅 :ref:`按需 <on_demand_policy>` 策略。

温度上限
********

可选的 :ref:`CPU 频率温度上限 <cpu_freq_thermal_cap>` 根据温度触发点约束活动策略所允许的最高性能 P-state。它是一个约束层，而不是 P-state 策略，用于减少过多热量产生并保护 SoC 免受热应力影响。

P-state 驱动
************

支持 CPU 频率调节子系统的 SoC 必须实现一个 P-state 驱动，该驱动实现 :c:func:`cpu_freq_pstate_set`，在调用时将传入的 ``p_state`` 应用到 CPU。

SoC 还必须通过在 devicetree 中提供一个 :dtcompatible:`zephyr,pstate` 兼容节点来提供可用的 P-state。SoC 也可以定义自己的 P-state 绑定，该绑定扩展 :dtcompatible:`zephyr,pstate`，以包含可供 SoC 的 P-state 驱动使用的其他属性。

使用注意事项
************

CPU 频率调节子系统设计为可在 UP 和 SMP 系统上工作。在 SMP 系统上，默认假定每个 CPU 都以相同频率运行。因此，如果一个 CPU 发生 P-state 转换，则所有其他 CPU 也会发生相同的 P-state 转换。SoC 可以通过启用 :kconfig:option:`CONFIG_CPU_FREQ_PER_CPU_SCALING` 配置选项来覆盖此行为，从而允许每个 CPU 独立设置时钟频率。

支持 CPU 频率调节的 SoC 必须遵守 Zephyr 的要求，即在程序整个生命周期内系统定时器频率保持稳定。有关更多信息，请参阅 :ref:`内核定时 <kernel_timing>`。

CPU 频率调节子系统作为 ``k_timer`` 的处理函数运行，这意味着它在中断上下文（IRQ）中运行。SoC P-state 驱动必须确保其 :c:func:`cpu_freq_pstate_set` 的实现对 IRQ 上下文安全。如果 P-state 转换无法在 IRQ 上下文中合理地完成，建议 SoC 的 P-state 驱动将其任务实现为一个工作队列项。
