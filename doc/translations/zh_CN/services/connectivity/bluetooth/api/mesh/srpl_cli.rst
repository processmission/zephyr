.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_srpl_cli:

Solicitation PDU RPL 配置客户端
###############################

Solicitation PDU RPL 配置客户端模型是由 Bluetooth Mesh 规范定义的基础模型。该模型是可选的，通过 :kconfig:option:`CONFIG_BT_MESH_SOL_PDU_RPL_CLI` 选项启用。

Solicitation PDU RPL 配置客户端模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，支持从支持 :ref:`bluetooth_mesh_srpl_srv` 模型的节点的 Solicitation Replay Protection List（SRPL）中删除地址。

Solicitation PDU RPL 配置客户端模型使用由配置客户端配置的应用密钥，与 Solicitation PDU RPL 配置服务器模型通信。

如果存在，Solicitation PDU RPL 配置客户端模型只能实例化在主元素上。

配置
****

Solicitation PDU RPL 配置客户端模型的行为可以通过传输超时选项 :kconfig:option:`CONFIG_BT_MESH_SOL_PDU_RPL_CLI_TIMEOUT` 进行配置。:kconfig:option:`CONFIG_BT_MESH_SOL_PDU_RPL_CLI_TIMEOUT` 控制 Solicitation PDU RPL 配置客户端等待响应消息到达的时长，单位为毫秒。该值可以在运行时使用 :c:func:`bt_mesh_sol_pdu_rpl_cli_timeout_set` 更改。

API 参考
********

.. doxygengroup:: bt_mesh_sol_pdu_rpl_cli
