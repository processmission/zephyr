.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _udc_api:

USB 设备控制器（UDC）驱动 API
#############################

USB 设备控制器驱动 API 在 :zephyr_file:`include/zephyr/drivers/usb/udc.h` 中描述，称为 ``UDC driver`` API。

UDC 驱动 API 尚不稳定，可能随时更改，恕不另行通知。它取代了 :ref:`usb_dc_api`。如果你希望将现有驱动移植到 UDC 驱动 API，或添加新驱动，请以 :zephyr_file:`drivers/usb/udc/udc_skeleton.c` 为起点。

API 参考
********

.. doxygengroup:: udc_api

.. doxygengroup:: usb_buf
