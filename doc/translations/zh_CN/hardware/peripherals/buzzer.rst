.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _buzzer_api:

蜂鸣器
######

蜂鸣器子系统提供统一的 API 来驱动蜂鸣器硬件，无论底层器件是由 PWM 通道驱动的无源压电蜂鸣器，还是由单根 GPIO 信号线控制的有源蜂鸣器。

基本操作
********

应用通过 Devicetree 获取蜂鸣器设备，并通过 :zephyr_file:`include/zephyr/drivers/buzzer.h` 中的函数驱动该设备：

蜂鸣器 API 调用不会等待请求的音调持续时间结束。持续时间表示硬件应持续发声的时长，而非调用线程应休眠的时长；使用 :c:macro:`BUZZER_DURATION_FOREVER` 可持续播放，直到显式停止。

- :c:func:`buzzer_tone` 以指定频率播放指定时长的音调。硬件会在请求的持续时间内保持发声，随后由驱动程序自动停止发声。
- :c:func:`buzzer_beep` 以蜂鸣器的固有工作频率发声，该频率由开发板文件中的 ``pwms`` Devicetree 属性的周期单元编码（通常为压电器件的机械谐振频率，此时器件发出的声音最响）。对于有源蜂鸣器，此调用等效于将 GPIO 信号线置为有效状态，因为实际音高由硬件振荡器决定。
- :c:func:`buzzer_set_volume` 调整感知响度。零值会立即静音；非零值会被保存，并在下一次播放音调时应用。有源蜂鸣器不具备模拟音量控制功能，因此将零值映射为静音，将任意非零值映射为其唯一的发声音量。
- :c:func:`buzzer_stop` 立即取消正在播放的音调。

后端
****

提供以下两种可通过 Devicetree 发现的后端：

- :dtcompatible:`pwm-buzzer` 用于由 PWM 通道驱动的无源压电蜂鸣器。PWM 通道的周期决定音频频率，占空比决定感知音量；驱动程序根据应用请求的音调和音量计算这两个参数。
- :dtcompatible:`gpio-buzzer` 用于通过单根 GPIO 信号线驱动的有源蜂鸣器。对于任意非零频率，驱动程序将信号线置为有效状态；对于 :c:macro:`BUZZER_FREQ_REST` ，则将其置为无效状态。

API 参考
********

.. doxygengroup:: buzzer_interface
