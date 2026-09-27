.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_lcd_cli:

大型组合数据客户端
##################

大型组合数据客户端模型是由 Bluetooth Mesh 规范定义的基础模型。该模型是可选的，通过 :kconfig:option:`CONFIG_BT_MESH_LARGE_COMP_DATA_CLI` 选项启用。

大型组合数据客户端模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，支持读取无法装入一条 Config Composition Data Status 消息的组合数据页面，以及读取支持 :ref:`bluetooth_mesh_lcd_srv` 模型的节点上模型实例的元数据。

大型组合数据客户端模型使用包含目标大型组合数据服务器模型实例的节点的设备密钥，与大型组合数据服务器模型通信。

如果存在，大型组合数据客户端模型只能实例化在主元素上。

API 参考
********

.. doxygengroup:: bt_mesh_large_comp_data_cli
