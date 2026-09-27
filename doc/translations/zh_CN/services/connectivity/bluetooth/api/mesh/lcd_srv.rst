.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_lcd_srv:

大型组合数据服务器
##################

大型组合数据服务器模型是由 Bluetooth Mesh 规范定义的基础模型。该模型是可选的，通过 :kconfig:option:`CONFIG_BT_MESH_LARGE_COMP_DATA_SRV` 选项启用。

大型组合数据服务器模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，用于公开无法装入一条 Config Composition Data Status 消息的组合数据页面，并公开模型实例的元数据。

大型组合数据服务器没有自己的 API，而是依赖 :ref:`bluetooth_mesh_lcd_cli` 对其进行控制。该模型只接受使用节点设备密钥加密的消息。

如果存在，大型组合数据服务器模型只能实例化在主元素上。

模型元数据
==========

大型组合数据服务器模型允许每个模型拥有一个由大型组合数据客户端模型读取的模型特定元数据列表。该元数据列表可以通过 :c:member:`bt_mesh_model.metadata` 字段与 :c:struct:`bt_mesh_model` 关联。元数据列表由一个或多个 :c:struct:`bt_mesh_models_metadata_entry` 结构定义的条目组成。每个条目包含元数据的长度和 ID，以及指向原始数据的指针。可以使用 :c:macro:`BT_MESH_MODELS_METADATA_ENTRY` 宏创建条目。:c:macro:`BT_MESH_MODELS_METADATA_END` 宏标记元数据列表的结尾，并且必须始终存在。如果模型没有元数据，可以改用辅助宏 :c:macro:`BT_MESH_MODELS_METADATA_NONE`。

API 参考
********

.. doxygengroup:: bt_mesh_large_comp_data_srv
