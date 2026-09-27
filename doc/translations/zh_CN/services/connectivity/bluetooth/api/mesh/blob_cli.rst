.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_blob_cli:

BLOB 传输客户端
###############

Binary Large Object (BLOB) 传输客户端是 BLOB 传输的发送方。它支持以 Push BLOB 传输模式和 Pull BLOB 传输模式向任意数量的目标节点发送任意大小的 BLOB。

用法
****

初始化
======

BLOB 传输客户端实例化在元素上，并带有一组事件处理回调：

.. code-block:: C

   static const struct bt_mesh_blob_cli_cb blob_cb = {
         /* Callbacks */
   };

   static struct bt_mesh_blob_cli blob_cli = {
         .cb = &blob_cb,
   };

   static const struct bt_mesh_model models[] = {
         BT_MESH_MODEL_BLOB_CLI(&blob_cli),
   };

传输上下文
==========

传输能力获取过程和 BLOB 传输都使用 :c:struct:`bt_mesh_blob_cli_inputs` 实例来确定如何执行传输。在将 BLOB Transfer Client Inputs 结构用于过程之前，至少必须使用目标列表、应用密钥和 time to live（TTL，生存时间）值对其进行初始化：

.. code-block:: c

   static struct bt_mesh_blob_target targets[3] = {
           { .addr = 0x0001 },
           { .addr = 0x0002 },
           { .addr = 0x0003 },
   };
   static struct bt_mesh_blob_cli_inputs inputs = {
           .app_idx = MY_APP_IDX,
           .ttl = BT_MESH_TTL_DEFAULT,
   };

   sys_slist_init(&inputs.targets);
   sys_slist_append(&inputs.targets, &targets[0].n);
   sys_slist_append(&inputs.targets, &targets[1].n);
   sys_slist_append(&inputs.targets, &targets[2].n);

请注意，传输中的所有 BLOB 传输服务器都必须绑定到所选的应用密钥。


组地址
------

应用还可以在上下文结构中指定组地址。如果组地址不是 :c:macro:`BT_MESH_ADDR_UNASSIGNED`，则传输中的消息将发送到组地址，而不是逐个发送到每个目标节点。Mesh Manager 必须确保所有具有 BLOB 传输服务器模型的目标节点都订阅该组地址。

使用组地址传输 BLOB 通常可以提高传输速度，因为 BLOB 传输客户端会同时将每条消息发送到所有目标节点。然而，在 Bluetooth Mesh 中向组地址发送大型分段消息通常不如向单播地址发送可靠，因为组没有传输层确认机制。这可能导致每个块结束时恢复时间更长，并增加丢失目标节点的风险。只有当目标节点列表很大时，使用组地址进行 BLOB 传输通常才有收益，而且每种寻址策略的效果会因部署和分块大小的不同而有很大差异。

传输超时
--------

如果目标节点未能在 BLOB 传输客户端的时间限制内响应确认消息，该目标节点将被移出传输。应用可以通过上下文结构为 BLOB 传输客户端提供额外时间，从而降低发生这种情况的可能性。额外时间可以按 10 秒递增设置，最长可达 182 小时，并叠加在 20 秒的基础时间之上。等待时间会随传输 TTL 自动缩放。

请注意，BLOB 传输客户端仅在以下情况下才会继续推进传输：

* 所有目标节点都已响应。
* 某个节点已从目标节点列表中移除。
* BLOB 传输客户端超时。

增加等待时间会延长此延迟。

BLOB 传输能力获取
=================

通常建议在开始传输前获取 BLOB 传输能力。该过程会汇总所有目标节点的传输能力，并选取能允许所有目标节点参与传输的最宽松参数集。未能响应或响应了不兼容传输参数的目标节点将被移出。

目标节点按照它们在目标节点列表中的顺序确定优先级。如果发现某个目标节点与之前的任何目标节点不兼容，例如报告了不重叠的块大小范围，该节点将被移出。丢失的目标节点将通过 :c:member:`lost_target <bt_mesh_blob_cli_cb.lost_target>` 回调报告。

过程的结束通过 :c:member:`caps <bt_mesh_blob_cli_cb.caps>` 回调通知，得到的能力可用于确定 BLOB 传输所需的块大小和分块大小。

BLOB 传输
=========

BLOB 传输通过调用 :c:func:`bt_mesh_blob_cli_send` 函数启动，除前述传输输入外，该函数还需要一组传输参数和一个 BLOB 流实例。传输参数包括 64 位 BLOB ID、BLOB 大小、传输模式、以对数表示的块大小以及分块大小。BLOB ID 由应用定义，但必须与 BLOB 传输服务器启动时使用的 BLOB ID 匹配。

传输会一直运行，直到至少一个目标节点成功完成传输，或者传输被取消。传输结束会通过 :c:member:`end <bt_mesh_blob_cli_cb.end>` 回调通知应用。丢失的目标节点将通过 :c:member:`lost_target <bt_mesh_blob_cli_cb.lost_target>` 回调报告。

API 参考
********

.. doxygengroup:: bt_mesh_blob_cli
