.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models_op_agg_srv:

Opcodes Aggregator 服务器
#########################

Opcodes Aggregator 服务器模型是由 Bluetooth Mesh 规范定义的基础模型。它是一个可选模型，通过 :kconfig:option:`CONFIG_BT_MESH_OP_AGG_SRV` 选项启用。

Opcodes Aggregator 服务器模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，用于支持处理一系列访问层消息。

Opcodes Aggregator 服务器模型接受使用节点设备密钥或应用密钥加密的消息。

如果存在，Opcodes Aggregator 服务器模型只能实例化在主元素上。

目标服务器模型应绑定到用于加密发送给 Opcodes Aggregator 服务器的访问层消息序列的同一应用密钥。

Opcodes Aggregator 服务器处理聚合消息，并将它们分派到相应的模型及其消息处理程序。当前实现假定响应从接收消息的同一执行上下文发送，不允许发送延迟响应，例如从工作队列发送。

API 参考
********

.. doxygengroup:: bt_mesh_op_agg_srv
