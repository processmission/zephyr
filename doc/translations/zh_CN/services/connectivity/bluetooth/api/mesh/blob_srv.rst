.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_blob_srv:

BLOB 传输服务器
###############

Binary Large Object (BLOB) 传输服务器模型实现大型二进制对象的可靠接收。它作为 :ref:`bluetooth_mesh_dfu_srv` 的后端，但也可用于接收其他二进制镜像。

BLOB
****

如 :ref:`bluetooth_mesh_blob` 中所述，BLOB 传输模型传输的二进制对象被划分为块，块再被划分为分块。由于传输由 BLOB 传输客户端模型控制，BLOB 传输服务器必须允许块以任意顺序到达。一个块内的分块也可以以任意顺序到达，但必须先接收到一个块中的所有分块，才能开始下一个块。

BLOB 传输服务器跟踪已接收的块和分块，并且每个块和分块只处理一次。BLOB 传输服务器还会确保任何缺失的分块由 BLOB 传输客户端重发。

用法
****

BLOB 传输服务器实例化在元素上，并带有一组事件处理回调：

.. code-block:: C

   static const struct bt_mesh_blob_srv_cb blob_cb = {
       /* Callbacks */
   };

   static struct bt_mesh_blob_srv blob_srv = {
       .cb = &blob_cb,
   };

   static const struct bt_mesh_model models[] = {
       BT_MESH_MODEL_BLOB_SRV(&blob_srv),
   };

BLOB 传输服务器一次只能接收一个 BLOB 传输。在 BLOB 传输服务器接收传输之前，必须由用户进行准备。必须在 BLOB 传输客户端启动传输之前，通过 :c:func:`bt_mesh_blob_srv_recv` 函数将传输 ID 传递给 BLOB 传输服务器。该 ID 必须通过某种更高层过程（例如厂商特定的传输管理模型）在 BLOB 传输客户端和 BLOB 传输服务器之间共享。

在 BLOB 传输服务器上设置好传输后，它便准备好接收 BLOB。应用通过事件处理回调获知传输进度，BLOB 数据会被发送到 BLOB 流。

BLOB 传输服务器、BLOB 流和应用之间的交互如下所示：

.. figure:: images/blob_srv.svg
   :align: center
   :alt: BLOB Transfer Server model interaction

   BLOB 传输服务器模型交互

传输暂停
********

BLOB 传输服务器在传输期间维护一个运行中的定时器，每收到一条消息都会将其重置。如果 BLOB 传输客户端在传输定时器到期前未发送消息，BLOB 传输服务器将暂停该传输。

BLOB 传输服务器通过调用 :c:member:`suspended <bt_mesh_blob_srv_cb.suspended>` 回调通知用户传输已暂停。如果 BLOB 传输服务器正在接收某个块，则该块会被丢弃。

BLOB 传输客户端可以通过开始新的块传输来恢复已暂停的传输。BLOB 传输服务器通过调用 :c:member:`resume <bt_mesh_blob_srv_cb.resume>` 回调通知用户。

传输恢复
********

BLOB 传输的状态会持久保存。如果发生重启，BLOB 传输服务器将尝试恢复传输。当 Bluetooth Mesh 子系统启动时（例如通过调用 :c:func:`bt_mesh_init`），BLOB 传输服务器将检查是否有已中止的传输，如果有，则调用 :c:member:`recover <bt_mesh_blob_srv_cb.recover>` 回调。在恢复回调中，用户必须提供一个 BLOB 流，供传输的剩余部分使用。如果恢复回调未能成功返回或未提供 BLOB 流，则放弃该传输。如果未实现恢复回调，则重启后传输始终会被放弃。

传输成功恢复后，BLOB 传输服务器进入暂停状态。它将保持暂停，直到 BLOB 传输客户端恢复传输，或者用户取消传输。

.. note::
   发送该传输的 BLOB 传输客户端必须支持传输恢复，传输才能完成。如果 BLOB 传输客户端已经放弃该传输，BLOB 传输服务器将保持暂停，直到应用调用 :c:func:`bt_mesh_blob_srv_cancel`。

API 参考
********

.. doxygengroup:: bt_mesh_blob_srv
