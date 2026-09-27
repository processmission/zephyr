.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models_brg_cfg_srv:

桥接配置服务器
##############

桥接配置服务器模型是由 Bluetooth Mesh 规范定义的基础模型。它是一个可选模型，通过 :kconfig:option:`CONFIG_BT_MESH_BRG_CFG_SRV` 配置选项启用。该模型扩展了 :ref:`bluetooth_mesh_models_cfg_srv` 模型。

桥接配置服务器模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，用于支持和配置子网桥接功能。

桥接配置服务器模型依赖 :ref:`bluetooth_mesh_models_brg_cfg_cli` 对其进行配置。桥接配置服务器模型仅接受使用节点设备密钥加密的消息。

如果存在，桥接配置服务器模型必须实例化在主元素上。

桥接配置服务器模型提供以下三种状态：

* 子网桥接
* 桥接表
* 桥接表大小

有关这些状态的更多信息，请参见 :ref:`bluetooth_mesh_brg_cfg_states`。

API 参考
********

.. doxygengroup:: bt_mesh_brg_cfg_srv
