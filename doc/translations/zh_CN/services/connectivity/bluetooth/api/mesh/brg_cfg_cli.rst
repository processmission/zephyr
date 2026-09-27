.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models_brg_cfg_cli:

桥接配置客户端
##############

桥接配置客户端是由 Bluetooth Mesh 规范定义的基础模型。该模型是可选的，通过 :kconfig:option:`CONFIG_BT_MESH_BRG_CFG_CLI` 选项启用。

桥接配置客户端模型提供用于配置另一个包含 :ref:`bluetooth_mesh_models_brg_cfg_srv` 的 Mesh 节点的子网桥接功能。包含目标桥接配置服务器的节点的设备密钥用于访问层安全。

如果存在，桥接配置客户端模型只能实例化在主元素上。

API 参考
********

.. doxygengroup:: bt_mesh_brg_cfg_cli
