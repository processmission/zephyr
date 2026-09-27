.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _usb_hid_common:

人机接口设备（Human Interface Devices，HID）
############################################

可在 USB 支持之外使用的通用 USB HID 部分，定义在头文件 :zephyr_file:`include/zephyr/usb/class/hid.h` 中。

HID 类型参考
************

.. doxygengroup:: usb_hid_definitions

HID 项参考
**********

.. doxygengroup:: usb_hid_items

HID 鼠标和键盘报告描述符
************************

预定义的鼠标和键盘报告描述符可供 HID 设备实现使用，也可以仅作为示例。

.. doxygengroup:: usb_hid_mk_report_desc
