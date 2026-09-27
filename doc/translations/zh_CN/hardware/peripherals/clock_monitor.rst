.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _clock_monitor_api:

时钟监测器
##########

概述
****

时钟监测器 API 提供对硬件外设的访问，这些外设在运行时监测时钟信号，并在其频率漂移超出预期范围或信号完全停止时报告。该 API 适用于功能安全和诊断场景，用于检测关键时钟树中的振荡器故障、参考时钟丢失或超出规格范围的频率漂移。

工作模式
********

两种模式采用相同的生命周期：使用 :c:func:`clock_monitor_configure` 进行配置，使用 :c:func:`clock_monitor_start` 开始运行，使用 :c:func:`clock_monitor_stop` 结束运行。

该 API 提供两种工作模式：

``CLOCK_MONITOR_MODE_WINDOW``
   持续进行阈值检查。硬件将受监测时钟的频率与可编程的上限和下限进行比较，这两个限值根据 :c:member:`clock_monitor_window_cfg.expected_hz` 和 :c:member:`clock_monitor_window_cfg.tolerance_ppm` 确定。频率越过阈值的事件通过配置时设置的用户回调异步传递。

``CLOCK_MONITOR_MODE_MEASURE``
   每次调用 :c:func:`clock_monitor_start` 执行一次频率测量，并通过配置时设置的回调传递结果（包括 ``CLOCK_MONITOR_EVT_MEASURE_DONE`` 和以 Hz 为单位的测量值）。设备会在回调运行之前自动返回已配置（已停止）状态，因此正常流程中无需调用 :c:func:`clock_monitor_stop` 。如需重复测量，可在回调中再次调用 :c:func:`clock_monitor_start` —— :c:func:`clock_monitor_start` 和 :c:func:`clock_monitor_stop` 均可在 ISR 中安全调用（与在计数器告警回调中重新设置告警的用法相同）。

对于 MEASURE 模式，API 不提供阻塞等待功能，超时由应用负责处理。常见做法是使用应用自行选择的超时时间，等待由回调释放的信号量，并在超时时调用 :c:func:`clock_monitor_stop` 以中止正在进行的测量。也可以通过 :c:func:`clock_monitor_get_rate` 轮询最近一次的结果；这也是用户模式线程获取结果的方式，因为用户模式线程不允许设置回调。

事件
****

事件以位掩码形式通过 :c:member:`clock_monitor_event_data.events` 传递：

* ``CLOCK_MONITOR_EVT_FREQ_HIGH`` —— 受监测频率超过上限阈值（WINDOW 模式）。
* ``CLOCK_MONITOR_EVT_FREQ_LOW`` —— 受监测频率低于下限阈值（WINDOW 模式）。
* ``CLOCK_MONITOR_EVT_CLOCK_LOST`` —— 受监测时钟在测量窗口内停止产生边沿（MEASURE 模式下的硬件故障）。
* ``CLOCK_MONITOR_EVT_MEASURE_DONE`` —— 测量成功完成（MEASURE 模式）； :c:member:`clock_monitor_event_data.measured_hz` 保存测量结果。

配置时设置的回调是唯一的事件传递途径。对于 MEASURE 模式，还可以通过轮询 :c:func:`clock_monitor_get_rate` 获取最近一次完成的测量结果。在 WINDOW 模式下，用户模式的观察者不允许设置回调，因此需通过特权模式端的中转机制接收事件（例如，由回调向 :c:struct:`k_msgq` 发送消息）。

配置
****

时钟监测器必须先通过 :c:func:`clock_monitor_configure` 配置，然后才能启动。配置包含工作模式、该模式特有的参数（预期频率、容差、测量窗口）以及可选的异步回调。只有在监测器停止时才能进行配置；重新配置时，使用新的模式和参数集再次调用 :c:func:`clock_monitor_configure` 即可，无需单独执行清理操作。完整的返回码列表请参见 `API 参考`_ 中的 :c:func:`clock_monitor_configure` 。

相关配置选项：

* :kconfig:option:`CONFIG_CLOCK_MONITOR`

API 参考
********

.. doxygengroup:: clock_monitor_interface
