.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bt_l2cap:

逻辑链路控制与适配协议（L2CAP）
###############################

L2CAP 层支持面向连接的通道，可通过配置选项 :kconfig:option:`CONFIG_BT_L2CAP_DYNAMIC_CHANNEL` 启用。这些通道透明地支持分段与重组，还支持基于信用的流控（credit based flow control），因此适用于数据流。

通道实例由 :c:struct:`bt_l2cap_chan` 结构体表示，该结构体包含 :c:struct:`bt_l2cap_chan_ops` 结构体中的回调，用于在通道已连接、已断开或加密状态发生变化时发出通知。除此之外，它还包含 ``recv`` 回调，每当收到传入数据时都会调用。通过返回 0，或在处理是异步的时使用 :c:func:`bt_l2cap_chan_recv_complete` API，可以将这样接收到的数据标记为已处理。

.. note::
  ``recv`` 回调直接从 RX 线程调用，因此不建议在其中长时间阻塞。

发送数据可使用 :c:func:`bt_l2cap_chan_send` API；注意，当没有可用信用额度时该 API 可能会阻塞，并在有更多信用额度可用时立即恢复。

可使用 :c:func:`bt_l2cap_server_register` API 注册服务器，并传入 :c:struct:`bt_l2cap_server` 结构体，其中指定了它应监听的 ``psm``、所需的安全级别 ``sec_level``，以及用于授权传入连接请求并分配通道实例的回调 ``accept``。分配的对象必须是 :c:struct:`bt_l2cap_le_chan` 类型，通过 ``accept`` 回调返回的通道引用应指向该对象的 ``chan`` 成员，如下例所示。

.. literalinclude:: ../../../../../samples/bluetooth/l2cap_coc_acceptor/src/main.c
   :language: c
   :start-after: doc l2cap server start
   :end-before: doc l2cap server end
   :dedent:

acceptor（服务器）示例中提供了演示 L2CAP 动态通道的完整可运行示例：:zephyr:code-sample:`bluetooth_l2cap_coc_acceptor`

固定通道
--------

用户还可以使用 :c:macro:`BT_L2CAP_FIXED_CHANNEL_DEFINE` 宏定义固定通道。固定通道在连接时初始化，不支持分段。注意，即使 ``accept`` 回调以 :c:struct:`bt_l2cap_chan` 形式传递通道引用，分配的对象也必须是 :c:struct:`bt_l2cap_le_chan` 类型，且该引用应指向其 ``chan`` 成员。下面给出了定义固定通道的示例。

.. code-block:: c

   static struct bt_l2cap_le_chan fixed_chan[CONFIG_BT_MAX_CONN];

   /* Callbacks are assumed to be defined prior. */
   static struct bt_l2cap_chan_ops ops = {
       .recv = recv_cb,
       .sent = sent_cb,
       .connected = connected_cb,
       .disconnected = disconnected_cb,
   };

   static int l2cap_fixed_accept(struct bt_conn *conn, struct bt_l2cap_chan **chan)
   {
       uint8_t conn_index = bt_conn_index(conn);

       fixed_chan[conn_index] = (struct bt_l2cap_le_chan){
           .chan.ops = &ops,
       };

       *chan = &fixed_chan[conn_index].chan;

       return 0;
   }

   BT_L2CAP_FIXED_CHANNEL_DEFINE(fixed_channel) = {
       .cid = 0x0010,
       .accept = l2cap_fixed_accept,
   };

客户端通道
----------

可使用 :c:func:`bt_l2cap_chan_connect` API 发起客户端通道，并使用 :c:func:`bt_l2cap_chan_disconnect` API 断开。注意，后者也可以断开由服务器创建的通道实例。

完整示例请参见 initiator（客户端）示例：:zephyr:code-sample:`bluetooth_l2cap_coc_initiator`

API 参考
********

.. doxygengroup:: bt_l2cap
