.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models_rpr_srv:

远程配网服务器
##############

远程配网服务器模型是由 Bluetooth Mesh 规范定义的基础模型。它通过 :kconfig:option:`CONFIG_BT_MESH_RPR_SRV` 选项启用。

远程配网服务器模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的，用于支持将设备远程配网到 Mesh 网络的功能。

远程配网服务器没有自己的 API，而是依赖 :ref:`bluetooth_mesh_models_rpr_cli` 对其进行控制。远程配网服务器模型仅接受使用节点的设备密钥加密的消息。

如果存在，远程配网服务器模型必须实例化在主元素上。

请注意，通过节点配网协议接口（Node Provisioning Protocol Interface，NPPI）过程刷新设备密钥、节点地址或 Composition Data 后，将触发 :c:member:`bt_mesh_prov.reprovisioned` 回调。更多详细信息请参见 :ref:`bluetooth_mesh_models_rpr_cli` 一节。

如何将模型集成到应用中
----------------------

要在应用中添加远程配网服务器模型，请执行以下操作：

1. 在项目配置中启用 Kconfig：

   .. code-block:: cfg

      CONFIG_BT_MESH_RPR_SRV=y

2. 使用 :c:macro:`BT_MESH_MODEL_RPR_SRV` 宏将模型实例添加到主元素的模型列表 :c:member:`bt_mesh_elem.models` 中，例如：

   .. code-block:: c

      static const struct bt_mesh_model models[] = {
              BT_MESH_MODEL_CFG_SRV,
              BT_MESH_MODEL_HEALTH_SRV(&health_srv, &health_pub),
              BT_MESH_MODEL_RPR_SRV,
              /* ... */
      };

      static const struct bt_mesh_elem elements[] = {
              BT_MESH_ELEM(0, models, BT_MESH_MODEL_NONE),
      };

3. 通过调用 :c:func:`bt_mesh_prov_enable` 并传入 :c:enumerator:`BT_MESH_PROV_REMOTE` 来启用 PB-Remote：

   .. code-block:: c

      err = bt_mesh_prov_enable(BT_MESH_PROV_REMOTE);
      if (err) {
              printk("PB-Remote enable failed (err %d)\n", err);
      }

限制
----

以下限制适用于远程配网服务器模型：

* 不支持使用 PB-GATT 对未配网设备进行配网。
* 支持所有节点配网协议接口（Node Provisioning Protocol Interface，NPPI）过程。但是，如果设备的 Composition Data 在设备固件更新后发生变化（请参见 :ref:`固件效果 <bluetooth_mesh_dfu_firmware_effect>` 一节），则设备无法保持已配网状态。如果预计设备的 Composition Data 会发生变化，则应将该设备取消配网。


API 参考
********

.. doxygengroup:: bt_mesh_rpr_srv
