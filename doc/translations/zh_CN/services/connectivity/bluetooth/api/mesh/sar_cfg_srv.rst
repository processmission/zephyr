.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_sar_cfg_srv:

SAR 配置服务器
##############

SAR 配置服务器模型是由 Bluetooth Mesh 规范定义的基础模型。它是一个可选模型，通过 :kconfig:option:`CONFIG_BT_MESH_SAR_CFG_SRV` 配置选项启用。

SAR 配置服务器模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，支持配置 Bluetooth Mesh 节点的 :ref:`分段与重组（SAR） <bluetooth_mesh_sar_cfg>` 行为。该模型定义了一组用于 SAR 配置的状态和消息。

SAR 配置服务器模型定义了两个状态：SAR 发送器状态和 SAR 接收器状态。有关这两种状态的更多信息，请参见 :ref:`bt_mesh_sar_cfg_states`。

该模型还支持 SAR 发送器和 SAR 接收器的 get 和 set 消息。

SAR 配置服务器模型没有自己的 API，而是依赖 :ref:`bluetooth_mesh_sar_cfg_cli` 对其进行控制。SAR 配置服务器模型只接受使用节点设备密钥加密的消息。

如果存在，SAR 配置服务器模型只能实例化在主元素上。

API 参考
********

.. doxygengroup:: bt_mesh_sar_cfg_srv
