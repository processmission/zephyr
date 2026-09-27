.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models_priv_beacon_cli:

Private Beacon 客户端
#####################

Private Beacon 客户端模型是由 Bluetooth Mesh 规范定义的基础模型。它通过 :kconfig:option:`CONFIG_BT_MESH_PRIV_BEACON_CLI` 选项启用。

Private Beacon 客户端模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，提供配置 :ref:`bluetooth_mesh_models_priv_beacon_srv` 模型的功能。

Private Beacon 功能通过定期随机化信标输入数据，为各种 Bluetooth Mesh 信标增加隐私性。这可保护 Mesh 节点不被 Mesh 网络外部的设备跟踪，并隐藏网络的 IV 索引、IV 更新和密钥刷新状态。

Private Beacon 客户端模型使用目标节点的设备密钥与 :ref:`bluetooth_mesh_models_priv_beacon_srv` 模型通信。Private Beacon 客户端模型可以与其他节点上的服务器通信，也可以通过本地 Private Beacon 服务器模型进行自我配置。

Private Beacon 客户端 API 中的所有配置函数的第一个参数都是 ``net_idx`` 和 ``addr``。这些参数应设置为目标节点配网时使用的网络索引和主单播地址。

如果存在，Private Beacon 客户端模型只能实例化在主元素上。

API 参考
********

.. doxygengroup:: bt_mesh_priv_beacon_cli
