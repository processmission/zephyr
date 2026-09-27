.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _on_demand_policy:

按需 CPU 频率调节策略
#####################

按需策略使用 :ref:`CPU 负载 <cpu_load>` 评估当前 CPU 负载，并将其与 SoC P-state 定义所规定的触发阈值进行比较。

按需策略会遍历已定义的 P-state，并选择第一个满足 CPU 负载大于或等于所定义阈值的 P-state。

如果没有 P-state 匹配（即 CPU 负载低于所有阈值），策略将选择 soc_pstates 数组中的最后一个 P-state（性能最低的状态）。这是该策略的固有特性：P-state 必须在 devicetree 中按阈值递减的顺序定义，最后一个 P-state 将用于负载低于所有阈值的情况。

有关按需策略的示例，请参阅 :zephyr:code-sample:`cpu_freq_on_demand` 示例。

该策略是被动的。只有在观察到系统负载变化后才会进行频率调整，因此无法预测突然出现的高负载。该策略不考虑任务截止时间，不应被视为实时策略。
