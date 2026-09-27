.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models_cfg_cli:

配置客户端
##########

配置客户端模型是由 Bluetooth Mesh 规范定义的基础模型。它提供用于配置 Mesh 节点大多数参数的功能，包括加密密钥、模型配置和功能启用。

配置客户端模型使用目标节点的设备密钥与 :ref:`bluetooth_mesh_models_cfg_srv` 模型通信。配置客户端模型可以与其他节点上的服务器通信，也可以通过本地配置服务器模型进行自我配置。

配置客户端 API 中的所有配置函数的第一个参数都是 ``net_idx`` 和 ``addr``。这些参数应设置为目标节点配网时使用的网络索引和主单播地址。

配置客户端模型是可选的，如果存在于组合数据中，则只能实例化在主元素上。

API 参考
********

.. doxygengroup:: bt_mesh_cfg_cli
