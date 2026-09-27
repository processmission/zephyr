.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models_op_agg_cli:

Opcodes Aggregator 客户端
#########################

Opcodes Aggregator 客户端模型是由 Bluetooth Mesh 规范定义的基础模型。它是一个可选模型，通过 :kconfig:option:`CONFIG_BT_MESH_OP_AGG_CLI` 选项启用。

Opcodes Aggregator 客户端模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，用于支持向支持 :ref:`bluetooth_mesh_models_op_agg_srv` 模型的节点分发一系列访问层消息。

Opcodes Aggregator 客户端模型使用目标节点的设备密钥或由配置客户端配置的应用密钥，与 Opcodes Aggregator 服务器模型通信。

如果存在，Opcodes Aggregator 客户端模型只能实例化在主元素上。

Opcodes Aggregator 客户端模型在初始化时隐式绑定到设备密钥。它应绑定到与用于生成消息序列的客户端模型相同的应用密钥。

为了能够聚合来自客户端模型的消息，该客户端模型应支持异步 API，例如通过回调。

API 参考
********

.. doxygengroup:: bt_mesh_op_agg_cli
