.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_dfd_srv:

固件分发服务器
##############

固件分发服务器模型实现 :ref:`bluetooth_mesh_dfu` 子系统的分发器角色。它扩展了 :ref:`bluetooth_mesh_blob_srv`，并借此从发起者节点接收固件映像二进制数据。它还实例化一个 :ref:`bluetooth_mesh_dfu_cli`，并借此在整个 Mesh 网络中分发固件更新。

.. note::

   目前，固件分发服务器仅支持通过 SMP 服务以带外（out-of-band，OOB）方式获取固件映像。

固件分发服务器没有自己的 API，而是依赖不同设备上的固件分发客户端模型为其提供信息并触发映像分发和上传。

固件槽位
********

固件分发服务器能够存储多个固件映像用于分发。每个槽位包含一个带有元数据的独立固件映像，并且可以按任意顺序分发到网络中的其他 Mesh 节点。固件映像的内容、格式和大小因供应商而异，并且可能包含来自其他供应商的数据。应用程序绝不应尝试执行或修改它们。

这些槽位由固件分发客户端远程管理，该客户端既可以上传新槽位，也可以删除旧槽位。应用程序通过固件分发服务器的回调（:cpp:type:`bt_mesh_fd_srv_cb`）获知槽位的变化。虽然每个固件槽位的元数据存储在内部，但应用程序必须提供 :ref:`bluetooth_mesh_blob_stream` 来读取和写入固件映像。

API 参考
********

.. doxygengroup:: bt_mesh_dfd_srv
