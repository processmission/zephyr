.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _sensor-trigger:

传感器触发器
############

:dfn:`Triggers` 是由传感器生成的事件，其类型在 :c:enum:`sensor_trigger_type` 中枚举。通常，传感器允许将这些事件配置为在数字信号线上产生信号，以便微控制器捕获。随后，通常可以通过读取寄存器来检查事件，确定是哪个事件导致数字信号线上产生了信号。

传感器提供多种触发器，既包括数据就绪等通知类事件，也包括轻敲或迈步等物理事件。
