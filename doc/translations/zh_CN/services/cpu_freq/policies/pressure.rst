.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _pressure_policy:

基于压力的 CPU 频率调节策略
###########################

压力策略评估就绪队列的当前压力，以便指导系统 P-state 转换。

线程压力通过以下公式计算：

.. math::

   P_{sys} = \frac{\sum_{t \in R} (P_{min} - prio_t + 1)}
                   {\sum_{t \in T} (P_{min} - prio_t + 1)} \times 100

其中

- :math:`R` 是可运行（已排队）线程的集合
- :math:`T` 是纳入压力计算的所有线程的集合
- :math:`w_t = P_{min} - \text{prio}_t + 1` 是线程 :math:`t` 的权重
- :math:`P_{min}` 是纳入考虑的最小优先级（数值上最大）

这会生成一个介于 0 和 100 之间的归一化系统压力，然后用于选择由 SoC 或 overlay 文件定义的合适 P-state。

计算出归一化系统压力后，会将其视为系统“负载”，然后策略将遍历 SoC 可用的 P-state，并选择第一个满足归一化压力大于或等于所定义阈值的 P-state。

如果没有 P-state 匹配（即归一化压力低于所有阈值），策略将选择 soc_pstates 数组中的最后一个 P-state（性能最低的状态）。

用户可以通过调整 :kconfig:option:`CONFIG_CPU_FREQ_POLICY_PRESSURE_LOWEST_PRIO` 选项来调节此策略的响应速度；该选项应设置为系统中最低优先级线程的优先级（数值上最大）。压力策略将忽略优先级低于该选项的线程，并且根据上述公式，会改变高优先级线程运行所带来的感知影响。

有关压力策略的示例，请参阅 :zephyr:code-sample:`cpu_freq_pressure` 示例。

该策略尝试主动评估已排队任务，并在其执行时间之前调整时钟频率，但该策略不保证性能，也不保证线程能够满足截止时间并避免饥饿。

请注意，:kconfig:option:`CONFIG_CPU_FREQ_POLICY_PRESSURE_LOWEST_PRIO` 包含 :kconfig:option:`CONFIG_TRACING`，会给上下文切换带来开销。
