.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_srpl_srv:

Solicitation PDU RPL 配置服务器
###############################

Solicitation PDU RPL 配置服务器模型是由 Bluetooth Mesh 规范定义的基础模型。如果节点启用了 :ref:`bluetooth_mesh_od_srv`，则会启用该模型。

Solicitation PDU RPL 配置服务器模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，用于管理保存在设备上的 Solicitation Replay Protection List（SRPL）。SRPL 用于拒绝已被节点处理的 Solicitation PDU。当节点成功处理一条有效的 Solicitation PDU 消息时，该消息的 SSRC 字段和 SSEQ 字段会存储到节点的 SRPL 中。

Solicitation PDU RPL 配置服务器没有自己的 API，而是依赖 :ref:`bluetooth_mesh_srpl_cli` 对其进行控制。该模型只接受使用由配置客户端配置的应用密钥加密的消息。

如果存在，Solicitation PDU RPL 配置服务器模型只能实例化在主元素上。

配置
****

对于 Solicitation PDU RPL 配置服务器模型，可以配置 :kconfig:option:`CONFIG_BT_MESH_PROXY_SRPL_SIZE` 选项来设置 SRPL 的大小。

API 参考
********

.. doxygengroup:: bt_mesh_sol_pdu_rpl_srv
