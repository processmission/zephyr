.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _cpu_freq_thermal_cap:

CPU 频率温度上限
################

CPU 频率温度上限是 CPU 频率调节子系统的一个可选约束层。活动策略选择请求的 P-state，而温度上限在配置的温度触发点处于活动状态时限制所允许的最高性能 P-state。

这样可以将性能需求与热缓解分开：

* CPU 频率策略根据自身的指标和阈值选择请求的 P-state。
* 温度上限将该请求钳制到当前温度所允许的最高性能 P-state。

钳制后，得到的 P-state 将传递给 SoC P-state 驱动。

设备树
******

通过添加 :dtcompatible:`zephyr,cpu-freq-thermal-cap` 节点并启用 :kconfig:option:`CONFIG_CPU_FREQ_THERMAL_CAP` 来启用温度上限。

示例：

.. code-block:: devicetree

   cpu_freq_thermal_cap: cpu_freq_thermal_cap {
           compatible = "zephyr,cpu-freq-thermal-cap";
           sensor = <&temp0>;
           sensor-channel = "die-temp";
           polling-delay-ms = <1000>;
           trip-active-polling-delay-ms = <100>;

           trip_0 {
                   temperature-millicelsius = <85000>;
                   hysteresis-millicelsius = <5000>;
                   cap-pstate = <&pstate_1>;
           };

           trip_1 {
                   temperature-millicelsius = <95000>;
                   hysteresis-millicelsius = <3000>;
                   cap-pstate = <&pstate_2>;
           };
   };

当 ``trip_0`` 处于活动状态时，CPU 频率请求被限制为 ``pstate_1`` 或更低。当 ``trip_1`` 处于活动状态时，请求被限制为 ``pstate_2`` 或更低。上限不会强制 CPU 运行在该 P-state；对于较低性能 P-state 的策略请求保持不变。

温度上限约束使用 CPU 频率的 P-state 索引顺序。索引较低的 P-state 性能较高，索引较高的 P-state 性能较低且约束更强。每个 ``cap-pstate`` 都必须通过 phandle 引用该有序表中的 P-state。

运行时行为
**********

温度采样通过可延迟的工作项完成，因为传感器驱动可能使用阻塞操作。CPU 频率定时器在应用策略结果时仅读取缓存的上限。

如果温度采样反复失败，上限将应用最低性能的 P-state（表中索引最高）作为故障安全约束。
