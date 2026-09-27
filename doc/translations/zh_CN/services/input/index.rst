.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _input:

输入
####

输入子系统提供了一套 API，用于把输入事件从输入设备分发到应用。

输入事件
********

该子系统围绕 :c:struct:`input_event` 结构构建。一个输入事件表示某个单独事件实体的变化，例如单个按键的状态，或者单个轴上的移动。

:c:struct:`input_event` 结构描述具体的事件，并包含一个同步位，用于表明设备已进入稳定状态，例如多轴设备各轴对应的事件都已上报时。

输入设备
********

输入设备可以使用 :c:func:`input_report` 或任何相关函数直接上报输入事件；例如按键或其他开关型输入实体可以使用 :c:func:`input_report_key`。

复杂设备可以组合多个事件，并在输出稳定后设置 ``sync`` 位。

``input_report*`` 函数接收一个 :c:struct:`device` 指针，用于表明是哪个设备上报了该事件，订阅者可以借此只接收来自特定设备的事件。如果事件没有关联的实际设备，可以把它设为 ``NULL``，此时只有未设置设备过滤的订阅者才会收到该事件。

应用 API
********

应用可以使用 :c:macro:`INPUT_CALLBACK_DEFINE` 宏注册回调。如果指定了设备节点，则只有来自该特定设备的事件才会触发该回调；否则回调会收到系统中的所有事件。这是唯一支持的过滤方式，任何更复杂的过滤逻辑都必须在回调自身中实现。

子系统可以同步运行，也可以使用事件队列运行，具体取决于 :kconfig:option:`CONFIG_INPUT_MODE` 选项。如果使用输入线程，所有事件都会被加入队列，并在一个公共的 ``input`` 线程中执行。如果不使用线程，回调会在输入驱动的上下文中直接调用。

同步模式可用于希望保持最小资源占用的简单应用，也可用于已有事件模型的复杂应用：此时回调只是把事件回传到更复杂的应用专用事件系统的包装层。

HID 代码映射
************

输入设备的一个常见用途是生成 HID 报告。为此，可以使用 :c:func:`input_to_hid_code` 和 :c:func:`input_to_hid_modifier` 函数把输入代码映射为 HID 代码和修饰键。

通用驱动
********

- :dtcompatible:`adc-keys`：用于连接到电阻梯的按键。
- :dtcompatible:`analog-axis`：用于连接到 ADC 输入的绝对位置设备（摇杆、滑块等）。
- :dtcompatible:`gpio-kbd-matrix`：用于连接到 GPIO 的键盘矩阵。
- :dtcompatible:`gpio-keys`：用于直接连接到 GPIO 的开关，实现了按键去抖。
- :dtcompatible:`gpio-qdec`：用于连接到 GPIO 的正交编码器。
- :dtcompatible:`input-keymap`：把键盘矩阵的行/列/触摸事件映射为按键事件。
- :dtcompatible:`zephyr,input-longpress`：监听按键事件，为短按和长按发出事件。
- :dtcompatible:`zephyr,input-double-tap`：监听按键事件，为输入双击发出事件
- :dtcompatible:`zephyr,lvgl-button-input` :dtcompatible:`zephyr,lvgl-encoder-input` :dtcompatible:`zephyr,lvgl-keypad-input` :dtcompatible:`zephyr,lvgl-pointer-input`：监听输入事件并把它们转换为各种类型的 LVGL 输入设备。

驱动详细文档
************

.. toctree::
   :maxdepth: 1

   gpio-kbd.rst


API 参考
********

.. doxygengroup:: input_interface

输入事件定义
************

.. doxygengroup:: input_events

模拟轴 API 参考
***************

.. doxygengroup:: input_analog_axis

触摸屏 API 参考
***************

.. doxygengroup:: touch_events
