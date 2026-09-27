.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_od_srv:

按需私有代理服务器
##################

按需私有代理服务器模型是由 Bluetooth Mesh 规范定义的基础模型。它通过 :kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_SRV` 选项启用。

按需私有代理服务器模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，它通过管理节点的按需私有 GATT 代理状态，支持配置作为 Solicitation PDU 接收方的节点使用 Private Network Identity 类型进行广播。

启用后，会同时启用 :ref:`bluetooth_mesh_srpl_srv`。按需私有代理服务器要求节点上存在 :ref:`bluetooth_mesh_models_priv_beacon_srv`。

按需私有代理服务器没有自己的 API，而是依赖 :ref:`bluetooth_mesh_od_cli` 对其进行控制。按需私有代理服务器模型只接受使用节点设备密钥加密的消息。

如果存在，按需私有代理服务器模型只能实例化在主元素上。

API 参考
********

.. doxygengroup:: bt_mesh_od_priv_proxy_srv
