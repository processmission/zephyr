.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_sar_cfg_cli:

SAR 配置客户端
##############

SAR 配置客户端模型是由 Bluetooth Mesh 规范定义的基础模型。它是一个可选模型，通过 :kconfig:option:`CONFIG_BT_MESH_SAR_CFG_CLI` 配置选项启用。

SAR 配置客户端模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，支持配置支持 :ref:`bluetooth_mesh_sar_cfg_srv` 模型的节点的下层传输层行为。

该模型可以发送 SAR Configuration 消息，以查询或更改 SAR 配置服务器支持的状态（SAR 发送器状态和 SAR 接收器状态）。

SAR 发送器过程用于确定和配置 SAR 配置服务器的 SAR 发送器状态。可以分别使用 :c:func:`bt_mesh_sar_cfg_cli_transmitter_get` 和 :c:func:`bt_mesh_sar_cfg_cli_transmitter_set` 函数调用获取和设置目标节点的 SAR 发送器状态。

SAR 接收器过程用于确定和配置 SAR 配置服务器的 SAR 接收器状态。可以分别使用 :c:func:`bt_mesh_sar_cfg_cli_receiver_get` 和 :c:func:`bt_mesh_sar_cfg_cli_receiver_set` 函数调用获取和设置目标节点的 SAR 接收器状态。

有关这两种状态的更多信息，请参见 :ref:`bt_mesh_sar_cfg_states`。

元素可以随时向对等节点的 SAR 配置服务器模型发送任何 SAR 配置客户端消息，以查询或更改其支持的状态。SAR 配置客户端模型只接受使用支持 SAR 配置服务器模型的节点的设备密钥加密的消息。

如果存在，SAR 配置客户端模型只能实例化在主元素上。

API 参考
********

.. doxygengroup:: bt_mesh_sar_cfg_cli
