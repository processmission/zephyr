.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _haptics_api:

触觉反馈
########

概述
****

触觉反馈 API 用于控制触觉驱动设备，以执行触觉反馈事件。

在触觉反馈事件期间，触觉设备向执行器输出驱动信号。触觉事件信号的来源因触觉设备的能力而异。

触觉信号源的示例包括模拟信号、预编程（ROM）波形表、合成（RAM）波形表和数字音频流。

此外，触觉驱动设备通常提供驱动信号的调整和调谐功能，以满足各自执行器的电气要求。

API 参考
********

.. doxygengroup:: haptics_interface
