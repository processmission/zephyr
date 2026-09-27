.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _tcpc_api:

USB Type-C 端口控制器（TCPC）
#############################

概述
****

`TCPC <tcpc-specification_>`_ （USB Type-C 端口控制器）是一种通过提供以下三项功能来简化 USB-C 系统实现的设备：

* VBUS 和 VCONN 控制 `USB Type-C <usb-type-c-specification_>`_ ：TCPC 可为供电设备提供控制 VBUS 供电的机制，并为受电设备提供控制 VBUS 受电的机制。VCONN 的控制也采用类似的机制。

* CC 控制与检测：TCPC 实现了用于控制 CC 引脚上拉和下拉电阻的逻辑，还提供了检测并报告 CC 引脚上所接电阻的方法。

* 电力传输消息的接收与发送 `USB Power Delivery <usb-pd-specification_>`_ ：TCPC 负责收发消息，并将 TCPM 中构建的消息发送到 CC 线上。

.. _tcpc-api:

TCPC API
========

TCPC 设备驱动程序充当 TCPC 设备与应用软件之间的桥梁；这一功能通过设备驱动程序提供的 Zephyr API 实现，该 API 用于与 TCPC 设备通信并对其进行控制。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_USBC_TCPC_DRIVER`

API 参考
********

.. doxygengroup:: usb_type_c
.. doxygengroup:: usb_type_c_port_controller_api
.. doxygengroup:: usb_power_delivery

.. _tcpc-specification:
   https://www.usb.org/document-library/usb-type-cr-port-controller-interface-specification

.. _usb-type-c-specification:
   https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification-revision-21

.. _usb-pd-specification:
   https://www.usb.org/document-library/usb-power-delivery
