.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models_priv_beacon_srv:

Private Beacon 服务器
#####################

Private Beacon 服务器模型是由 Bluetooth Mesh 规范定义的基础模型。它通过 :kconfig:option:`CONFIG_BT_MESH_PRIV_BEACON_SRV` 选项启用。

Private Beacon 服务器模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，用于控制 Mesh 节点的 Private Beacon 状态、Private GATT Proxy 状态和 Private Node Identity 状态。

Private Beacon 功能通过定期随机化信标输入数据，为各种 Bluetooth Mesh 信标增加隐私性。这可保护 Mesh 节点不被 Mesh 网络外部的设备跟踪，并隐藏网络的 IV 索引、IV 更新和密钥刷新状态。必须实例化 Private Beacon 服务器，设备才能支持发送私有信标；但节点即使没有该服务器，也会处理收到的私有信标。

Private Beacon 服务器没有自己的 API，而是依赖 :ref:`bluetooth_mesh_models_priv_beacon_cli` 对其进行控制。Private Beacon 服务器模型只接受使用节点设备密钥加密的消息。

应用程序可以通过传递给 :c:macro:`BT_MESH_MODEL_PRIV_BEACON_SRV` 的 :c:struct:`bt_mesh_priv_beacon_srv` 实例，配置 Private Beacon 服务器模型的初始参数。请注意，如果 Mesh 节点在设置子系统中存储了对此配置的更改，则初始值可能会在加载时被覆盖。

如果存在，Private Beacon 服务器模型只能实例化在主元素上。

API 参考
********

.. doxygengroup:: bt_mesh_priv_beacon_srv
