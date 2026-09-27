.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_dfu_srv:

固件更新服务器
##############

固件更新服务器模型实现 :ref:`bluetooth_mesh_dfu` 子系统的目标节点功能。它扩展了 :ref:`bluetooth_mesh_blob_srv`，并借此从分发器节点接收固件映像二进制数据。

结合扩展的 BLOB 传输服务器模型，固件更新服务器模型实现了通过 Mesh 网络接收固件更新所需的全部功能，但不提供任何用于存储、应用或验证映像的功能。

固件映像
********

固件更新服务器保存设备上所有可更新固件映像的列表。完整列表应通过 :c:macro:`BT_MESH_DFU_SRV_INIT` 中的 ``_imgs`` 参数传递给服务器，并且必须在 Bluetooth Mesh 子系统启动之前填充。映像列表中的每个固件映像必须可独立更新，并且应具有自己的固件 ID。

例如，一个具有可升级引导加载程序、应用程序以及支持固件更新的外设芯片的设备，其固件映像列表中可能有三项，每项都有自己的独立固件 ID。

接收传输
********

固件更新服务器模型使用同一元素上的 BLOB 传输服务器模型来传输二进制映像。固件更新服务器、BLOB 传输服务器和应用程序之间的交互如下所述：

.. figure:: images/dfu_srv.svg
   :align: center
   :alt: Bluetooth Mesh Firmware Update Server transfer

   Bluetooth Mesh 固件更新服务器传输

传输检查
========

传输检查是应用程序可对传入固件映像元数据执行的可选传输前检查。固件更新服务器通过调用 :c:member:`check <bt_mesh_dfu_srv_cb.check>` 回调来执行传输检查。

传输检查的结果是一个通过/失败状态返回值以及预期的 :c:enum:`bt_mesh_dfu_effect`。DFU 效果返回参数将被传回分发器，并应指示固件更新对设备的 Mesh 状态产生何种影响。

.. _bluetooth_mesh_dfu_srv_comp_data_and_models_metadata:

组合数据与模型元数据
--------------------

如果传输会导致设备更改其组合数据或变为未配网状态，则应通过元数据检查的效果参数传达这一点。

当传输会导致组合数据发生变化，并且支持 :ref:`bluetooth_mesh_models_rpr_srv` 时，新固件映像的组合数据将由组合数据页面 128、129 和 130 表示。新固件映像的模型元数据将由模型元数据页面 128 表示。组合数据页面 0、1 和 2，以及模型元数据页面 0，将表示旧固件映像的组合数据和模型元数据，直到使用 :ref:`bluetooth_mesh_models_rpr_cli` 通过节点配网协议接口（Node Provisioning Protocol Interface，NPPI）过程对设备重新配网。

应用程序必须先调用 :c:func:`bt_mesh_comp_change_prepare` 和 :c:func:`bt_mesh_models_metadata_change_prepare` 函数，以在启动到具有更新后的组合数据和模型元数据的固件之前，存储现有的组合数据和模型元数据页面。然后，旧的组合数据将被加载到组合数据页面 0、1 和 2 中，而新固件中的组合数据将被加载到组合数据页面 128、129 和 130 中。旧映像的模型元数据将被加载到模型元数据页面 0 中，新映像的模型元数据将被加载到模型元数据页面 128 中。

限制：

* 在应用新固件映像后，无法更改设备的组合数据，同时让设备保持已配网并继续使用旧固件运行。

开始
====

开始过程为传入的传输准备应用程序。它将包含有关正在更新哪个映像的信息以及更新元数据。

固件更新服务器的 :c:member:`start <bt_mesh_dfu_srv_cb.start>` 回调必须返回一个指向 BLOB 写入器的指针，BLOB 传输服务器将把 BLOB 发送到该写入器。

BLOB 传输
=========

在设置阶段之后，固件更新服务器为传入的传输准备 BLOB 传输服务器。整个固件映像被传输到 BLOB 传输服务器，后者将映像传递给分配给它的 BLOB 写入器。

在 BLOB 传输结束时，固件更新服务器调用其 :c:member:`end <bt_mesh_dfu_srv_cb.end>` 回调。

映像验证
========

在 BLOB 传输完成后，应用程序应尽其所能验证映像，以确保它已准备好被应用。映像验证完成后，应用程序调用 :c:func:`bt_mesh_dfu_srv_verified`。

如果无法验证映像，应用程序调用 :c:func:`bt_mesh_dfu_srv_rejected`。

应用映像
========

最后，如果映像已通过验证，分发器可以指示固件更新服务器应用传输。这通过 :c:member:`apply <bt_mesh_dfu_srv_cb.apply>` 回调传达给应用程序。应用程序应交换映像并开始使用新固件运行。应更新固件映像表，以反映已更新映像的新固件 ID。

当传输应用于 Mesh 应用程序本身时，设备可能需要在交换过程中重启。此重启可以从 apply 回调内部执行，也可以异步执行。在使用新固件启动后，应在 Bluetooth Mesh 子系统启动之前更新固件映像表。

分发器将读取固件映像表，以确认传输已成功应用。如果元数据检查指示设备将变为未配网状态，则目标节点无需响应该检查。

API 参考
********

.. doxygengroup:: bt_mesh_dfu_srv
