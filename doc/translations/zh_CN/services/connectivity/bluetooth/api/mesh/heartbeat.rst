.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_heartbeat:

心跳
####

心跳（Heartbeat）功能提供监控 Bluetooth Mesh 节点并确定节点之间距离的功能。

心跳功能通过 :ref:`bluetooth_mesh_models_cfg_srv` 模型进行配置。

心跳消息
********

心跳消息作为传输控制数据包通过网络发送，并且仅使用网络密钥加密。心跳消息包含发送该消息时使用的原始 Time To Live (TTL) 值以及节点上活动功能的位域。接收节点据此可以确定消息到达接收方需要经过多少次中继，以及该节点支持哪些功能。

可用的心跳功能标志：

- :c:macro:`BT_MESH_FEAT_RELAY`
- :c:macro:`BT_MESH_FEAT_PROXY`
- :c:macro:`BT_MESH_FEAT_FRIEND`
- :c:macro:`BT_MESH_FEAT_LOW_POWER`

心跳发布
********

心跳发布通过配置模型控制，可以通过两种方式触发：

周期性发布
   节点按固定间隔发布新的心跳消息。可以将发布配置为在发送一定数量的消息后停止，或者无限期持续。

触发式发布
   每当功能发生变化时，节点都会发布新的心跳消息。可以配置能够触发发布的功能集合。

这两种发布类型可以组合使用。

心跳订阅
********

可以将一个节点配置为一次订阅来自一个节点的心跳消息。要接收心跳消息，源和目的地都必须与配置的订阅参数匹配。

心跳订阅始终具有时间限制，在整个订阅期间，节点会记录收到的心跳数量以及收到的最小和最大跳数。

所有使用配置的订阅参数收到的心跳都会传递给 :cpp:member:`bt_mesh_hb_cb::recv` 事件处理程序。

心跳订阅期结束时，将调用 :cpp:member:`bt_mesh_hb_cb::sub_end` 回调。

API 参考
********

.. doxygengroup:: bt_mesh_heartbeat
