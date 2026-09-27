.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _twister_power_harness:

功耗
####

``power`` 测试适配器用于测量和验证电流消耗。它与 pytest 集成，使用硬件功耗监测器自动采集和分析数据。

该适配器执行以下步骤：

1. 通过 ``PowerMonitor`` 抽象接口初始化功耗监测设备，例如 ``stm_powershield``。
#. 开始测量电流，持续指定的 ``measurement_duration``。
#. 采集原始电流波形数据。
#. 使用峰值检测算法，根据功耗变化将数据划分为定义的执行阶段。
#. 使用辅助函数计算每个阶段的电流有效值（RMS）。
#. 将计算值与用户定义的预期 RMS 值比较。

.. code-block:: yaml

    harness: power
    harness_config:
      fixture: pm_probe
      power_measurements:
        elements_to_trim: 100
        min_peak_distance: 40
        min_peak_height: 0.008
        peak_padding: 40
        measurement_duration: 6
        num_of_transitions: 4
        expected_rms_values: [56.0, 4.0, 1.2, 0.26, 140]
        tolerance_percentage: 20

- **elements_to_trim**：测量开始时丢弃的采样数，用于消除噪声。
- **min_peak_distance**：检测到的电流峰值之间的最小距离，有助于识别独立的变化。
- **min_peak_height**：判定为峰值的最小电流阈值，单位为安培。
- **peak_padding**：在每个检测到的峰值周围扩展的采样数。
- **measurement_duration**：记录电流数据的总时长，单位为秒。
- **num_of_transitions**：测试执行期间 DUT 预期发生的功耗状态转换次数。
- **expected_rms_values**：每个识别出的执行阶段的目标 RMS 值，单位为毫安。
- **tolerance_percentage**：相对于预期 RMS 值允许的偏差百分比。
