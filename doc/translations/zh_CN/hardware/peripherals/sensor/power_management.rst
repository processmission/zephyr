.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

电源管理
========

传感器的电源管理通常并不简单，因为传感器的各个通道可能具有多种电源状态。有些传感器可能支持低噪声模式、低功耗模式或挂起通道，从而以牺牲噪声性能或采样速度为代价，大幅降低功耗。在极低功耗状态下，传感器甚至可能关闭设备的数字逻辑部分，从而丢失其状态。

这意味着传感器的电源管理通常取决于具体应用！通道状态通常可以通过 :ref:`sensor-attribute` 修改。如果设备实现了必要的功能，则可以使用电源管理引用计数 API 来挂起和恢复整个设备。

对于完全挂起和恢复这两种电源状态，传感器通常应使用 :ref:`pm-device-runtime` API，由应用层显式调用 :c:func:`pm_device_runtime_get` 和 :c:func:`pm_device_runtime_put` 。

未来，借助 :ref:`sensor-read-and-decode` ，在流式传输场景下或许可以自动管理设备电源，因为应用会通过请求在指定事件发生时读取数据，持续向驱动程序表明设备的使用需求。
