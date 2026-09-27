.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models_cfg_srv:

配置服务器
##########

配置服务器模型是由 Bluetooth Mesh 规范定义的基础模型。配置服务器模型控制 Mesh 节点的大多数参数。它没有自己的 API，而是依赖 :ref:`bluetooth_mesh_models_cfg_cli` 对其进行控制。

配置服务器模型在所有 Bluetooth Mesh 节点上都是必需的，并且只能实例化在主元素上。

API 参考
********

.. doxygengroup:: bt_mesh_cfg_srv
