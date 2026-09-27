.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models_rpr_cli:

远程配网客户端
##############

远程配网客户端模型是由 Bluetooth Mesh 规范定义的基础模型。它通过 :kconfig:option:`CONFIG_BT_MESH_RPR_CLI` 选项启用。

远程配网客户端模型是在 Bluetooth Mesh Protocol Specification 1.1 版中引入的。该模型提供将设备远程配网到 Mesh 网络的功能，并通过与支持 :ref:`bluetooth_mesh_models_rpr_srv` 模型的 Mesh 节点交互来执行节点配网协议接口（Node Provisioning Protocol Interface，NPPI）过程。

远程配网客户端模型使用包含目标远程配网服务器模型实例的节点的设备密钥，与远程配网服务器模型通信。

如果存在，远程配网客户端模型必须实例化在主元素上。

扫描
****

扫描过程用于扫描远程配网服务器附近的未配网设备。远程配网客户端通过调用 :c:func:`bt_mesh_rpr_scan_start` 启动扫描过程：

.. code-block:: C

      static void rpr_scan_report(struct bt_mesh_rpr_cli *cli,
                  const struct bt_mesh_rpr_node *srv,
                  struct bt_mesh_rpr_unprov *unprov,
                  struct net_buf_simple *adv_data)
      {

      }

      struct bt_mesh_rpr_cli rpr_cli = {
         .scan_report = rpr_scan_report,
      };

      const struct bt_mesh_rpr_node srv = {
         .addr = 0x0004,
         .net_idx = 0,
         .ttl = BT_MESH_TTL_DEFAULT,
      };

      struct bt_mesh_rpr_scan_status status;
      uint8_t *uuid = NULL;
      uint8_t timeout = 10;
      uint8_t max_devs = 3;

      bt_mesh_rpr_scan_start(&rpr_cli, &srv, uuid, timeout, max_devs, &status);

上述示例显示了在目标远程配网服务器节点上启动扫描过程的伪代码。该过程将启动一次持续十秒的多设备扫描，生成的扫描报告最多包含三个未配网设备。如果指定了 UUID 参数，则同一过程将仅扫描具有对应 UUID 的设备。过程完成后，服务器会发送扫描报告，该报告将在客户端的 :c:member:`bt_mesh_rpr_cli.scan_report` 回调中处理。

此外，远程配网客户端模型还通过 :c:func:`bt_mesh_rpr_scan_start_ext` 调用支持扩展扫描。扩展扫描通过允许远程配网服务器报告特定设备的附加数据来补充常规扫描。如果未配网设备支持主动扫描，则远程配网服务器将使用主动扫描向该设备请求扫描响应。

配网
****

远程配网客户端通过调用 :c:func:`bt_mesh_provision_remote` 启动配网过程：

.. code-block:: C

      struct bt_mesh_rpr_cli rpr_cli;

      const struct bt_mesh_rpr_node srv = {
         .addr = 0x0004,
         .net_idx = 0,
         .ttl = BT_MESH_TTL_DEFAULT,
      };

      uint8_t uuid[16] = { 0xaa };
      uint16_t addr = 0x0006;
      uint16_t net_idx = 0;

      bt_mesh_provision_remote(&rpr_cli, &srv, uuid, net_idx, addr);

上述示例显示了通过远程配网服务器节点远程配网设备的伪代码。该过程将尝试为具有对应 UUID 的设备配网，并使用位于索引 0 的网络密钥将地址 0x0006 分配给其主元素。

.. note::
   在远程配网期间，会触发与普通配网相同的 :c:struct:`bt_mesh_prov` 回调。更多详细信息请参见 :ref:`bluetooth_mesh_provisioning` 一节。

重新配网
********

除了扫描和配网功能之外，远程配网客户端还提供了在支持 :ref:`bluetooth_mesh_models_rpr_srv` 模型的设备上重新配置节点地址、设备密钥和 Composition Data 的方法。这通过支持以下三种过程的节点配网协议接口（Node Provisioning Protocol Interface，NPPI）提供：

* 设备密钥刷新过程：用于更改目标节点的设备密钥，而无需重新配置节点。
* 节点地址刷新过程：用于更改节点的设备密钥和单播地址。
* 节点 Composition 刷新过程：用于更改节点的设备密钥，以及添加或删除节点的模型或功能。

这三种 NPPI 过程可通过调用 :c:func:`bt_mesh_reprovision_remote` 启动：

.. code-block:: C

      struct bt_mesh_rpr_cli rpr_cli;
      struct bt_mesh_rpr_node srv = {
         .addr = 0x0006,
         .net_idx = 0,
         .ttl = BT_MESH_TTL_DEFAULT,
      };

      bool composition_changed = false;
      uint16_t new_addr = 0x0009;

      bt_mesh_reprovision_remote(&rpr_cli, &srv, new_addr, composition_changed);

上述示例显示了在目标节点上触发节点地址刷新过程的伪代码。具体过程并非直接选择，而是通过传入的其他参数决定。在示例中可以看到，目标节点的当前单播地址为 0x0006，而新地址设置为 0x0009。如果两个地址相同，且 ``composition_changed`` 标志设置为 true，则此代码将改为触发节点 Composition 刷新过程。如果两个地址相同，且 ``composition_changed`` 标志设置为 false，则此代码将触发设备密钥刷新过程。

API 参考
********

.. doxygengroup:: bt_mesh_rpr_cli
