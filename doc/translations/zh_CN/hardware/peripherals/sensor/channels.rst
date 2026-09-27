.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _sensor-channel:

传感器通道
##########

:dfn:`Channels` （通道）是传感器设备可以测量的量，在 :c:enum:`sensor_channel` 中枚举。

传感器可以具有多个通道，用于表示同一物理属性（例如加速度）的不同轴，或用于测量不同的属性（例如环境温度、压力和湿度）。传感器也可以具有多个测量类型相同的通道，以便获取温度、光强、电流、电压或电容等量的多个读数。

在 Zephyr 中，使用 :c:struct:`sensor_chan_spec` 指定通道，该结构体包含通道类型（ :c:enum:`sensor_channel` ）和通道索引。有时也仅使用 :c:enum:`sensor_channel` ，但自 Zephyr 3.7 引入 :c:struct:`sensor_chan_spec` 以来，这种用法应视为历史遗留用法。
