.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _timing_noise_policy:

时序噪声 CPU 频率调节策略
#########################

概述
####

时序噪声策略是一种 CPU 频率调节策略，它会定期选择随机的性能状态（P-state）。其目的是通过抖动 CPU 时钟来注入时序可变性，从而干扰那些假设频率稳定的简单周期计数或挂钟测量。

这是一种随机化 P-state 策略。它不是通用的侧信道对策。

主要缓解措施
############

经过侧信道泄漏审查的恒定时间和恒定流实现，仍是抵御时序攻击的主要缓解措施。该策略不能取代这些做法。它最多只能增加某一类测量的复杂度。

攻击者模型
##########

该策略考虑的攻击者具有以下行为：

* 通过周期计数器、挂钟定时器或类似的软件可见时间戳观察相对执行时间
* 依赖稳定的 CPU 频率，以便指令数或数据相关路径的微小差异在不同试验之间仍可区分

随机化 P-state 选择无法抵御此类攻击。只要有足够多的样本，攻击者通常可以通过平均来消除噪声。该策略只会让这些测量变得更不方便、更难以重复。

用例
####

当应用希望在已经可靠的软件之上，将额外的时序可变性作为第二层防护时，此策略可能会很有用。应将其视为干扰某些分析的手段，而不是独立的安全解决方案。

它不适合以下场景：

* 需要确定性执行时间的硬实时系统
* 将时序可预测性作为安全案例一部分的安全相关系统
* 无法容忍意外缓慢 P-state 的延迟敏感工作负载
* 严格的功率预算设计，因为频繁的 P-state 变化可能会增加平均功耗

配置
####

启用 CPU 频率子系统并选择时序噪声策略：

.. code-block:: kconfig

   CONFIG_CPU_FREQ=y
   CONFIG_CPU_FREQ_POLICY_TIMING_NOISE=y

该策略使用标准的 CPU 频率子系统更新间隔，可通过以下配置设置：

.. code-block:: kconfig

   CONFIG_CPU_FREQ_INTERVAL_MS=<interval>

较小的更新间隔会增加时序可变性，但也会增加频率转换的次数。

随机数生成
##########

该策略使用 :c:func:`sys_rand32_get()` 选择性能状态。在具有硬件熵源的平台上，选择 ``CONFIG_CPU_FREQ_POLICY_TIMING_NOISE`` 会启用熵驱动。当有 TRNG 可用时，优先通过该驱动获取随机抽取结果：

.. code-block:: kconfig

   CONFIG_ENTROPY_DEVICE_RANDOM_GENERATOR=y

限制
####

* 它不能消除时序侧信道
* 它无法弥补本质上不安全的软件
* 它可能会降低整体系统性能
* 由于频繁的性能状态变化，它可能会增加功耗
* 对于有决心的或具备完善测量手段的攻击者，它不提供任何保证

有关时序噪声策略的示例，请参阅 :zephyr:code-sample:`cpu_freq_timing_noise` 示例。
