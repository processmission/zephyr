.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_od_cli:

按需私有代理客户端
##################

按需私有代理客户端模型是由 Bluetooth Mesh 规范定义的基础模型。该模型是可选的，通过 :kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_CLI` 选项启用。

按需私有代理客户端模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，用于设置和获取按需私有 GATT 代理状态。该状态定义节点在收到 Solicitation PDU 后使用 Private Network Identity 类型广播 Mesh Proxy Service 的时长。

按需私有代理客户端模型使用包含目标按需私有代理服务器模型实例的节点的设备密钥，与按需私有代理服务器模型通信。

如果存在，按需私有代理客户端模型只能实例化在主元素上。

配置
****

按需私有代理客户端模型的行为可以通过传输超时选项 :kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_CLI_TIMEOUT` 进行配置。:kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_CLI_TIMEOUT` 控制客户端等待状态响应消息到达的时长，单位为毫秒。该值可以在运行时使用 :c:func:`bt_mesh_od_priv_proxy_cli_timeout_set` 更改。


API 参考
********

.. doxygengroup:: bt_mesh_od_priv_proxy_cli
