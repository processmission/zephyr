.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _usb_device_stack_api:

USB 设备协议栈 API（已弃用）
############################

API 参考
********

传输数据有两种方式：使用“低”层读/写 API 或“高”层传输 API。

低层 API
  要向主机传输数据，类驱动应调用 usb_write()。完成后将调用注册的端点回调。在发送下一个数据包之前，类驱动应等待上一次写入完成。收到数据时，会调用注册的端点回调。应使用 usb_read() 获取接收到的数据。对于 CDC ACM 示例驱动，这一过程通过端点数组（cdc_acm_ep_data）中提到的 OUT 批量端点处理程序（cdc_acm_bulk_out）完成。

高层 API
  usb_transfer 方法可用于向主机传输数据或从主机接收数据。传输 API 会根据端点最大数据包大小，自动将数据传输拆分为一个或多个 USB 事务。类驱动不必实现端点回调，而应将此回调设置为通用的 usb_transfer_ep_callback。

.. doxygengroup:: _usb_device_core_api
