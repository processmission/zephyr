.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_cfg:

运行时配置
##########

运行时配置 API 允许应用程序直接更改其运行时配置，而无需通过配置模型。

Bluetooth Mesh 节点通常应由带有 :ref:`bluetooth_mesh_models_cfg_cli` 模型的中央网络配置器设备进行配置。每个 Mesh 节点都会实例化一个 :ref:`bluetooth_mesh_models_cfg_srv` 模型，配置客户端可以与其通信以更改节点配置。在某些情况下，Mesh 节点无法依赖配置客户端来检测或确定本地约束，例如电池电量低或拓扑变化。对于这些场景，可以使用此 API 在本地更改配置。

.. note::
   节点配网之前的运行时配置更改不会存储在 :ref:`持久存储 <bluetooth_mesh_persistent_storage>` 中。

API 参考
********

.. doxygengroup:: bt_mesh_cfg
