.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _modbus:

Modbus
######

Modbus 是一种工业消息传递协议，针对不同类型的网络或总线进行了规定。Zephyr OS 的实现支持通过串行线路通信，并可用于 RS485 或 RS232 等不同的物理接口。TCP 支持并未直接实现，但提供了辅助函数，以便根据应用需求实现 TCP 支持。

Modbus 通信基于客户端/服务器模型。总线上只能存在一个客户端，客户端可以与多个服务器设备通信。服务器设备本身是被动的，不得发送请求或未经请求的响应。客户端请求的服务由功能码（FCxx）指定，可在规范或下文 API 的文档中找到。

Zephyr RTOS 实现同时支持客户端和服务器两种角色。

有关 Modbus 和 Modbus RTU 的更多信息，请参见网站 `MODBUS Protocol Specifications`_。

示例
****

* :zephyr:code-sample:`modbus-rtu-server` 和 :zephyr:code-sample:`modbus-rtu-client` 示例可以在评估板上试用 RTU 服务器和 RTU 客户端实现。
* :zephyr:code-sample:`modbus-tcp-server` 示例是一个简单的 Modbus TCP 服务器。
* :zephyr:code-sample:`modbus-gateway` 示例展示了如何使用 Zephyr OS 构建 TCP 到串行线路的网关。

API 参考
********

.. doxygengroup:: modbus

.. _`MODBUS Protocol Specifications`: https://www.modbus.org/specs.php
