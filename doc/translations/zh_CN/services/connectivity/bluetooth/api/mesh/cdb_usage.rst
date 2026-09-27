.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_cdb_usage:

配置数据库（CDB）
#################

.. contents::
   :local:
   :depth: 2

概述
****

配置数据库（CDB）是用于 Bluetooth® Mesh 配网器设备的子系统。它存储并管理 Mesh 网络的信息，包括已配网节点、网络密钥和应用密钥。CDB 使配网器能够跟踪网络拓扑、分配地址并有条理地配置节点。

.. note::

   CDB 实现采用专有设计，不遵循 Bluetooth SIG 规范。

CDB 通过 :kconfig:option:`CONFIG_BT_MESH_CDB` 配置选项启用，通常仅在网络中的配网器设备上使用。为避免冲突，Mesh 网络中应只有一个设备启用 CDB。

关键特性
========

* **持久存储**：启用 :kconfig:option:`CONFIG_BT_SETTINGS` 时，所有 CDB 数据都会持久保存，使配网器能够在重启后恢复网络状态。
* **地址管理**：自动分配并跟踪已配网节点的单播地址。
* **密钥管理**：存储并同步网络密钥和应用密钥。
* **节点跟踪**：维护每个已配网节点的信息，包括 UUID、地址、元素数量、设备密钥和配置状态。
* **IV Index 管理**：跟踪网络的 IV Index 和 IV Update 状态。

配置选项
********

以下 Kconfig 选项控制 CDB 容量：

* :kconfig:option:`CONFIG_BT_MESH_CDB_NODE_COUNT` - CDB 能处理的最大节点数。
* :kconfig:option:`CONFIG_BT_MESH_CDB_SUBNET_COUNT` - CDB 能处理的最大子网数。
* :kconfig:option:`CONFIG_BT_MESH_CDB_APP_KEY_COUNT` - CDB 能处理的最大应用密钥数。

其他选项：

* :kconfig:option:`CONFIG_BT_MESH_CDB_KEY_SYNC` - 启用配网器节点上的 Mesh 密钥与 CDB 密钥之间的自动同步。启用该选项后，通过 :ref:`bluetooth_mesh_models_cfg_srv` 执行的密钥操作会自动同步到 CDB。

数据结构
********

CDB 旨在处理由多种数据结构收集的数据。这些结构分别表示节点、子网、应用密钥以及整个数据库状态。

节点结构
========

.. literalinclude:: ../../../../../../include/zephyr/bluetooth/mesh/cdb.h
   :language: c
   :dedent:
   :start-after: doc string cdb node start
   :end-before: doc string cdb node end

节点标志：

* ``BT_MESH_CDB_NODE_CONFIGURED`` - 当节点已配置密钥和绑定时设置。

子网结构
========

.. literalinclude:: ../../../../../../include/zephyr/bluetooth/mesh/cdb.h
   :language: c
   :dedent:
   :start-after: doc string cdb subnet start
   :end-before: doc string cdb subnet end

应用密钥结构
============

.. literalinclude:: ../../../../../../include/zephyr/bluetooth/mesh/cdb.h
   :language: c
   :dedent:
   :start-after: doc string cdb app key start
   :end-before: doc string cdb app key end

主 CDB 结构
===========

.. literalinclude:: ../../../../../../include/zephyr/bluetooth/mesh/cdb.h
   :language: c
   :dedent:
   :start-after: doc string cdb start
   :end-before: doc string cdb end

使用场景
********

以下模式演示常见的 CDB 使用场景：

* :ref:`cdb_pattern_1` - 创建并初始化 CDB
* :ref:`cdb_pattern_2` - 管理节点配网和地址
* :ref:`cdb_pattern_3` - 管理网络密钥和子网
* :ref:`cdb_pattern_4` - 查找并移除子网
* :ref:`cdb_pattern_5` - 向 CDB 添加应用密钥
* :ref:`cdb_pattern_6` - 查找并移除应用密钥
* :ref:`cdb_pattern_7` - 配置已配网节点
* :ref:`cdb_pattern_8` - 使用回调处理节点
* :ref:`cdb_pattern_9` - 查找并移除节点
* :ref:`cdb_pattern_10` - 管理 IV Index 更新
* :ref:`cdb_pattern_11` - 导入/导出设备密钥
* :ref:`cdb_pattern_12` - 重置数据库

.. note::

   下文提供的场景源代码应视为概念性模式，而非精确实现。它们需要根据应用场景进行调整并经过测试。请阅读 CDB API 描述以了解正确用法。

.. _cdb_pattern_1:

配网器初始化
============

在嵌入式配网器节点上，必须在 Mesh 协议栈配网之前初始化 CDB，应用才能将其用于密钥存储、节点跟踪和配置。此步骤建立主网络密钥、初始子网以及起始 IV Index 和地址空间，使后续所有 CDB 操作都在定义明确的网络上下文中进行，并可跨重启持久保存。

典型的配网器会在启动期间初始化 CDB：

.. code-block:: c

   #include <zephyr/bluetooth/mesh.h>

   static int provisioner_init(void)
   {
       uint8_t net_key[16];
       int err;

       /* Initialize Bluetooth Mesh */
       err = bt_mesh_init(&prov, &comp);
       if (err) {
           return err;
       }

       /* Load settings if persistent storage is enabled */
       if (IS_ENABLED(CONFIG_BT_SETTINGS)) {
           settings_load();
       }

       /* Generate or use predefined network key */
       bt_rand(net_key, 16);

       /* Create CDB with primary network key */
       err = bt_mesh_cdb_create(net_key);
       if (err == -EALREADY) {
           printk("Using stored CDB\n");
       } else if (err) {
           printk("Failed to create CDB (err %d)\n", err);
           return err;
       } else {
           printk("Created new CDB\n");
       }

       return 0;
   }

要点：

* 使用主网络密钥调用 :c:func:`bt_mesh_cdb_create` 函数。
* 如果 CDB 已存在（从持久存储加载），则返回错误码。
* 该函数会自动创建一个 ``NetIdx = 0`` 的子网。
* 将 IV Index 设为 ``0``，并将最低可用地址设为 ``1``。

.. _cdb_pattern_2:

配网与节点分配
==============

向 Mesh 添加新设备时，其地址、设备密钥和基本元数据必须一致地记录在配网器数据库中。在 PB-ADV/PB-GATT 配网期间自动分配节点可使 CDB 与实际网络保持同步。配网新设备时，CDB 会在配网过程中自动分配节点。

不过，也可以手动分配节点或检查分配情况。手动节点分配适用于高级场景，例如从外部源导入节点、预先分配地址范围或根据已知信息恢复网络。

.. code-block:: c

   /* Provisioning callback - node is automatically added to CDB */
   static void node_added(uint16_t idx, uint8_t uuid[16], uint16_t addr,
                          uint8_t num_elem)
   {
       printk("Node added: addr=0x%04x, elements=%d\n", addr, num_elem);
       /* The CDB node is created automatically by the provisioning subsystem */
   }

   static const struct bt_mesh_prov prov = {
       .uuid = dev_uuid,
       .node_added = node_added,
       /* ... other callbacks ... */
   };

   /* Manual node allocation (if needed) */
   static struct bt_mesh_cdb_node *allocate_node(const uint8_t uuid[16],
                                                   uint8_t num_elem)
   {
       struct bt_mesh_cdb_node *node;
       uint16_t addr;

       /* Get free address or specify one (0 = auto-allocate) */
       addr = bt_mesh_cdb_free_addr_get(num_elem);
       if (addr == BT_MESH_ADDR_UNASSIGNED) {
           printk("No free addresses available\n");
           return NULL;
       }

       /* Allocate node in CDB */
       node = bt_mesh_cdb_node_alloc(uuid, addr, num_elem, net_idx);
       if (node == NULL) {
           printk("Failed to allocate node\n");
           return NULL;
       }

       return node;
   }

要点：

* 在正常的 PB-ADV/PB-GATT 配网过程中，节点会自动添加到 CDB。
* :c:func:`bt_mesh_cdb_node_alloc` 函数使用指定参数创建 CDB 条目。
* 将 :c:macro:`BT_MESH_ADDR_UNASSIGNED` 作为地址传入，让 CDB 自动分配最低可用地址。
* :c:func:`bt_mesh_cdb_free_addr_get` 函数为给定元素数量查找可用地址范围。
* 地址分配会检查冲突，并确保单播地址有效。

.. _cdb_pattern_3:

子网与密钥管理
==============

大型或分段 Mesh 网络通常使用多个子网来分隔流量域、支持安全迁移或支持 Key Refresh 过程。在 CDB 中管理子网及其网络密钥，使配网器在配网和配置节点时能够创建新子网、轮换密钥并推导正确的标志和 IV Index。

在 CDB 中管理网络密钥和子网：

.. code-block:: c

   /* Add a new subnet */
   static int add_subnet(uint16_t net_idx)
   {
       struct bt_mesh_cdb_subnet *sub;
       uint8_t net_key[16];
       int err;

       /* Allocate subnet in CDB */
       sub = bt_mesh_cdb_subnet_alloc(net_idx);
       if (sub == NULL) {
           printk("Failed to allocate subnet\n");
           return -ENOMEM;
       }

       /* Generate network key */
       bt_rand(net_key, 16);

       /* Import key value */
       err = bt_mesh_cdb_subnet_key_import(sub, 0, net_key);
       if (err) {
           bt_mesh_cdb_subnet_del(sub, false);
           return err;
       }

       /* Store subnet */
       if (IS_ENABLED(CONFIG_BT_SETTINGS)) {
           bt_mesh_cdb_subnet_store(sub);
       }

       return 0;
   }

   /* Get subnet for provisioning */
   static int get_subnet_flags(uint16_t net_idx)
   {
       struct bt_mesh_cdb_subnet *sub;
       uint8_t flags;

       sub = bt_mesh_cdb_subnet_get(net_idx);
       if (sub == NULL) {
           return -ENOENT;
       }

       flags = bt_mesh_cdb_subnet_flags(sub);
       printk("Subnet flags: KR=%d IVU=%d\n",
              !!(flags & BT_MESH_NET_FLAG_KR),
              !!(flags & BT_MESH_NET_FLAG_IVU));

       return 0;
   }

要点：

* :c:func:`bt_mesh_cdb_subnet_alloc` 函数按 NetIdx 分配子网。
* :c:func:`bt_mesh_cdb_subnet_key_import` 函数设置实际密钥值。
* :c:func:`bt_mesh_cdb_subnet_flags` 函数返回配网数据所需的标志。
* 这些标志包括来自 CDB 的 Key Refresh 和 IV Update 状态。

.. _cdb_pattern_4:

子网查找与移除
==============

有时可能需要检查现有子网（用于诊断或工具）或将其完全移除（例如停用某个网段、轮换到新子网或清理实验环境）。CDB 提供查找和删除辅助函数，使配网器能够保持其对活动子网的视图与节点实际使用的子网一致。

在 CDB 中查找和管理子网：

.. code-block:: c

   /* Get subnet by NetIdx */
   static void lookup_subnet(uint16_t net_idx)
   {
       struct bt_mesh_cdb_subnet *sub;

       sub = bt_mesh_cdb_subnet_get(net_idx);
       if (sub == NULL) {
           printk("Subnet 0x%03x not found\n", net_idx);
           return;
       }

       printk("Subnet 0x%03x: kr_phase=%d\n", net_idx, sub->kr_phase);
   }

   /* Remove a subnet from the CDB */
   static void remove_subnet(uint16_t net_idx)
   {
       struct bt_mesh_cdb_subnet *sub;

       sub = bt_mesh_cdb_subnet_get(net_idx);
       if (sub == NULL) {
           printk("Subnet not found\n");
           return;
       }

       /* First, remove the subnet from all nodes in the network */
       /* ... send NetKey Delete to all nodes using Config Client ... */

       /* Delete subnet from CDB */
       bt_mesh_cdb_subnet_del(sub, true);

       printk("Subnet 0x%03x removed\n", net_idx);
   }

   /* Export subnet key for external use */
   static int export_subnet_key(uint16_t net_idx, int key_idx)
   {
       struct bt_mesh_cdb_subnet *sub;
       uint8_t net_key[16];
       int err;

       sub = bt_mesh_cdb_subnet_get(net_idx);
       if (sub == NULL) {
           return -ENOENT;
       }

       err = bt_mesh_cdb_subnet_key_export(sub, key_idx, net_key);
       if (err) {
           printk("Failed to export subnet key (err %d)\n", err);
           return err;
       }

       printk("NetKey[%d] for subnet 0x%03x: ", key_idx, net_idx);
       for (int i = 0; i < 16; i++) {
           printk("%02x", net_key[i]);
       }
       printk("\n");

       return 0;
   }

要点：

* :c:func:`bt_mesh_cdb_subnet_get` 函数通过 NetKeyIndex 获取子网。
* 向 :c:func:`bt_mesh_cdb_subnet_del` 函数传入 ``true`` 以清除持久存储。
* 从 CDB 删除子网之前，务必先从所有节点移除该子网。
* 使用 :c:func:`bt_mesh_cdb_subnet_key_export` 函数安全地获取密钥材料。
* ``key_idx`` 参数（``0`` 或 ``1``）在 Key Refresh 过程中选择旧密钥或新密钥。

.. _cdb_pattern_5:

设置应用密钥
============

应用密钥定义哪些应用流量可以加密以及可以绑定到何处。CDB 初始化后，配网器必须创建一个或多个应用密钥，以便在节点上绑定模型并启用实际的应用级通信（例如照明或传感器数据）。

创建 CDB 后，添加应用密钥以进行节点配置：

.. code-block:: c

   static void setup_cdb_keys(void)
   {
       struct bt_mesh_cdb_app_key *key;
       uint8_t app_key[16];
       int err;

       /* Allocate application key in CDB */
       key = bt_mesh_cdb_app_key_alloc(net_idx, app_idx);
       if (key == NULL) {
           printk("Failed to allocate app-key\n");
           return;
       }

       /* Generate random key value */
       bt_rand(app_key, 16);

       /* Import the key into CDB */
       err = bt_mesh_cdb_app_key_import(key, 0, app_key);
       if (err) {
           printk("Failed to import appkey (err %d)\n", err);
           return;
       }

       /* Store to persistent storage */
       if (IS_ENABLED(CONFIG_BT_SETTINGS)) {
           bt_mesh_cdb_app_key_store(key);
       }
   }

要点：

* :c:func:`bt_mesh_cdb_app_key_alloc` 函数在 CDB 中分配一个槽位。
* :c:func:`bt_mesh_cdb_app_key_import` 函数设置实际密钥值。
* 导入函数的第二个参数（``0``）是用于 Key Refresh 过程的密钥索引（``0`` = 当前密钥）。
* 使用持久存储时，创建后务必保存密钥。

.. _cdb_pattern_6:

应用密钥查找与移除
==================

随着时间推移，可能需要检查某个应用密钥绑定到哪个网络密钥、轮换或撤销应用密钥，或清理不再使用的密钥。通过 CDB 正确查找和移除有助于避免悬空绑定，并确保节点和配网器对可用应用密钥具有一致的视图。

在 CDB 中查找和管理应用密钥：

.. code-block:: c

   /* Get application key by AppIdx */
   static void lookup_app_key(uint16_t app_idx)
   {
       struct bt_mesh_cdb_app_key *key;

       key = bt_mesh_cdb_app_key_get(app_idx);
       if (key == NULL) {
           printk("AppKey 0x%03x not found\n", app_idx);
           return;
       }

       printk("AppKey 0x%03x: bound to NetIdx 0x%03x\n",
              app_idx, key->net_idx);
   }

   /* Remove an application key from the CDB */
   static void remove_app_key(uint16_t app_idx)
   {
       struct bt_mesh_cdb_app_key *key;

       key = bt_mesh_cdb_app_key_get(app_idx);
       if (key == NULL) {
           printk("AppKey not found\n");
           return;
       }

       /* First, remove the app key from all nodes in the network */
       /* ... send AppKey Delete to all nodes using Config Client ... */

       /* Delete app key from CDB */
       bt_mesh_cdb_app_key_del(key, true);

       printk("AppKey 0x%03x removed\n", app_idx);
   }

   /* Export application key for external use */
   static int export_app_key(uint16_t app_idx, int key_idx)
   {
       struct bt_mesh_cdb_app_key *key;
       uint8_t app_key[16];
       int err;

       key = bt_mesh_cdb_app_key_get(app_idx);
       if (key == NULL) {
           return -ENOENT;
       }

       err = bt_mesh_cdb_app_key_export(key, key_idx, app_key);
       if (err) {
           printk("Failed to export app key (err %d)\n", err);
           return err;
       }

       printk("AppKey[%d] 0x%03x: ", key_idx, app_idx);
       for (int i = 0; i < 16; i++) {
           printk("%02x", app_key[i]);
       }
       printk("\n");

       return 0;
   }

   /* Update application key binding */
   static int update_app_key_binding(uint16_t app_idx, uint16_t new_net_idx)
   {
       struct bt_mesh_cdb_app_key *key;

       key = bt_mesh_cdb_app_key_get(app_idx);
       if (key == NULL) {
           return -ENOENT;
       }

       /* Verify the new subnet exists */
       if (bt_mesh_cdb_subnet_get(new_net_idx) == NULL) {
           printk("Target subnet 0x%03x not found\n", new_net_idx);
           return -ENOENT;
       }

       key->net_idx = new_net_idx;

       /* Store updated binding */
       if (IS_ENABLED(CONFIG_BT_SETTINGS)) {
           bt_mesh_cdb_app_key_store(key);
       }

       printk("AppKey 0x%03x rebound to NetIdx 0x%03x\n",
              app_idx, new_net_idx);

       return 0;
   }

要点：

* :c:func:`bt_mesh_cdb_app_key_get` 函数通过 AppKeyIndex 获取应用密钥。
* 向 :c:func:`bt_mesh_cdb_app_key_del` 函数传入 ``true`` 以清除持久存储。
* 从 CDB 删除应用密钥之前，务必先从所有节点移除该应用密钥。
* 使用 :c:func:`bt_mesh_cdb_app_key_export` 函数安全地获取密钥材料。
* ``key_idx`` 参数（``0`` 或 ``1``）在 Key Refresh 过程中选择旧密钥或新密钥。
* 应用密钥通过 ``net_idx`` 字段绑定到网络密钥。

.. _cdb_pattern_7:

节点配置
========

配网只是将节点加入网络，并不会使其参与应用。配网后，必须配置节点：添加网络/应用密钥、绑定模型以及设置订阅/发布。CDB 存储密钥和配置状态，使配网器在重启后能够继续配置，并避免重新配置已完成的节点。

配网后，通过添加密钥和绑定模型来配置节点：

.. code-block:: c

   static void configure_node(struct bt_mesh_cdb_node *node)
   {
       NET_BUF_SIMPLE_DEFINE(buf, BT_MESH_RX_SDU_MAX);
       struct bt_mesh_cdb_app_key *key;
       uint8_t app_key[16];
       uint8_t status;
       int err;

       printk("Configuring node 0x%04x\n", node->addr);

       /* Get application key from CDB */
       key = bt_mesh_cdb_app_key_get(app_idx);
       if (key == NULL) {
           printk("App-key not found\n");
           return;
       }

       /* Export key value from CDB */
       err = bt_mesh_cdb_app_key_export(key, 0, app_key);
       if (err) {
           printk("Failed to export key (err %d)\n", err);
           return;
       }

       /* Add application key to the node */
       err = bt_mesh_cfg_cli_app_key_add(net_idx, node->addr,
                                         net_idx, app_idx,
                                         app_key, &status);
       if (err || status) {
           printk("Failed to add app-key (err %d, status %d)\n",
                  err, status);
           return;
       }

       /* Get composition data and bind models */
       err = bt_mesh_cfg_cli_comp_data_get(net_idx, node->addr, 0,
                                           &status, &buf);
       if (err || status) {
           printk("Failed to get composition data\n");
           return;
       }

       /* Parse composition and bind models to app key */
       /* ... model binding code ... */

       /* Mark node as configured */
       atomic_set_bit(node->flags, BT_MESH_CDB_NODE_CONFIGURED);

       /* Persist configuration status */
       if (IS_ENABLED(CONFIG_BT_SETTINGS)) {
           bt_mesh_cdb_node_store(node);
       }
   }

要点：

* 使用 :c:func:`bt_mesh_cdb_app_key_get` 和 :c:func:`bt_mesh_cdb_app_key_export` 函数获取密钥。
* 配置客户端模型用于配置远程节点。
* 配置成功后设置 ``BT_MESH_CDB_NODE_CONFIGURED`` 标志。
* 务必调用 :c:func:`bt_mesh_cdb_node_store` 函数以持久保存已配置状态。

.. _cdb_pattern_8:

遍历节点
========

许多管理任务需要对所有节点（或经过筛选的子集）执行操作：检查哪些节点仍需配置、生成统计信息或执行批量操作。CDB 迭代器使配网器能够以安全、抽象的方式遍历所有已知节点，而无需依赖内部存储细节。

CDB 提供迭代器来处理所有已分配的节点：

.. code-block:: c

   /* Check for unconfigured nodes */
   static uint8_t check_unconfigured(struct bt_mesh_cdb_node *node,
                                      void *user_data)
   {
       if (!atomic_test_bit(node->flags, BT_MESH_CDB_NODE_CONFIGURED)) {
           printk("Node 0x%04x needs configuration\n", node->addr);
           configure_node(node);
       }

       return BT_MESH_CDB_ITER_CONTINUE;
   }

   static void process_nodes(void)
   {
       bt_mesh_cdb_node_foreach(check_unconfigured, NULL);
   }

   /* Example: Count nodes on a specific subnet */
   static uint8_t count_subnet_nodes(struct bt_mesh_cdb_node *node,
                                      void *user_data)
   {
       uint16_t *net_idx = user_data;
       static int count = 0;

       if (node->net_idx == *net_idx) {
           count++;
       }

       return BT_MESH_CDB_ITER_CONTINUE;
   }

要点：

* :c:func:`bt_mesh_cdb_node_foreach` 函数会为每个已分配节点调用回调。
* 返回 ``BT_MESH_CDB_ITER_CONTINUE`` 以继续迭代。
* 返回 ``BT_MESH_CDB_ITER_STOP`` 可提前停止迭代。
* 仅对 ``addr != BT_MESH_ADDR_UNASSIGNED`` 的节点调用回调。

.. _cdb_pattern_9:

节点查找与移除
==============

有时需要检查单个节点（例如调试时）或将其从网络中移除（例如设备物理停用或更换时）。使用 CDB 节点查找和删除可使 Mesh 的逻辑视图与实际设备保持一致，并防止地址重用冲突。

在 CDB 中查找和管理节点：

.. code-block:: c

   /* Get node by address */
   static void lookup_node(uint16_t addr)
   {
       struct bt_mesh_cdb_node *node;

       node = bt_mesh_cdb_node_get(addr);
       if (node == NULL) {
           printk("Node 0x%04x not found\n", addr);
           return;
       }

       printk("Node 0x%04x: %d elements, net_idx=0x%03x\n",
              node->addr, node->num_elem, node->net_idx);
   }

   /* Remove a node from the network */
   static void remove_node(uint16_t addr)
   {
       struct bt_mesh_cdb_node *node;

       node = bt_mesh_cdb_node_get(addr);
       if (node == NULL) {
           printk("Node not found\n");
           return;
       }

       /* First, send Node Reset to the device (recommended) */
       /* ... send reset command using Config Client ... */

       /* Delete node from CDB */
       bt_mesh_cdb_node_del(node, true);

       printk("Node 0x%04x removed\n", addr);
   }

要点：

* :c:func:`bt_mesh_cdb_node_get` 函数按元素地址搜索（适用于任何元素地址）。
* 移除节点前务必发送 ``Node Reset`` 命令，以避免产生孤立设备。
* 向 :c:func:`bt_mesh_cdb_node_del` 函数传入 ``true`` 以清除持久存储。
* 删除节点时，如果合适，可能会更新 ``lowest_avail_addr`` （详情请阅读 CDB API）。

.. _cdb_pattern_10:

IV Index 管理
=============

IV Index 是 Bluetooth Mesh 安全性和重放保护的核心部分。发生 IV Update 过程时，配网器必须更新其存储的 IV Index，以便后续配网和配置使用正确的值和地址空间。将其存储在 CDB 中可确保网络状态在重启后以及各次配网操作之间保持一致。

更新网络的 IV Index：

.. code-block:: c

   /* Update IV Index when IV Update procedure occurs */
   static void handle_iv_update(uint32_t iv_index, bool iv_update)
   {
       bt_mesh_cdb_iv_update(iv_index, iv_update);

       printk("IV Index updated: %u (IV Update: %s)\n",
              iv_index, iv_update ? "in progress" : "normal");
   }

   /* The IV Index is automatically used during provisioning */
   static void provision_with_current_iv(void)
   {
       /* The provisioner automatically uses bt_mesh_cdb.iv_index
        * and bt_mesh_cdb_subnet_flags() when sending provisioning data
        */
   }

要点：

* :c:func:`bt_mesh_cdb_iv_update` 函数同时更新 IV Index 和 IV Update 标志。
* CDB 在 IV Index 更新期间会自动重置 ``lowest_avail_addr``。
* 配网器子系统会自动为新节点使用 CDB 的 IV Index。

.. _cdb_pattern_11:

使用设备密钥
============

设备密钥属于敏感信息，通常通过安全密钥存储（例如 PSA crypto）处理。CDB 的密钥导入/导出 API 抽象了密钥的存储方式，使应用在需要时（用于配置或外部工具）可以使用设备密钥，而不会破坏安全模型，也不依赖直接指向密钥存储的指针。

使用密钥管理 API 导入和导出设备密钥：

.. code-block:: c

   /* Import a known device key */
   static int import_dev_key(struct bt_mesh_cdb_node *node,
                             const uint8_t dev_key[16])
   {
       int err;

       err = bt_mesh_cdb_node_key_import(node, dev_key);
       if (err) {
           printk("Failed to import device key (err %d)\n", err);
           return err;
       }

       /* Store updated node */
       if (IS_ENABLED(CONFIG_BT_SETTINGS)) {
           bt_mesh_cdb_node_store(node);
       }

       return 0;
   }

   /* Export device key for external use */
   static int export_dev_key(struct bt_mesh_cdb_node *node)
   {
       uint8_t dev_key[16];
       int err;

       err = bt_mesh_cdb_node_key_export(node, dev_key);
       if (err) {
           printk("Failed to export device key (err %d)\n", err);
           return err;
       }

       /* Use the exported key */
       printk("Device key: ");
       for (int i = 0; i < 16; i++) {
           printk("%02x", dev_key[i]);
       }
       printk("\n");

       return 0;
   }

要点：

* 处理密钥时务必使用导入/导出函数（PSA crypto 有此要求）。
* 密钥安全存储，不能通过指针直接访问。
* 配网器在配网期间自动生成并导入设备密钥。

.. _cdb_pattern_12:

清除 CDB
========

对于恢复出厂设置、测试或启动全新网络，可能需要擦除所有配网和配置数据。清除 CDB 会重置逻辑网络状态，以便安全地从头重新创建，同时避免与过期密钥或节点条目产生不一致。

重置整个配置数据库：

.. code-block:: c

   static void reset_network(void)
   {
       printk("Clearing CDB...\n");

       /* Clear all CDB data */
       bt_mesh_cdb_clear();

       printk("CDB cleared\n");
   }

要点：

* :c:func:`bt_mesh_cdb_clear` 函数移除所有节点、子网和应用密钥。
* 如果启用了 :kconfig:option:`CONFIG_BT_SETTINGS` Kconfig 选项，则清除持久存储。
* 将 CDB 标记为无效（必须调用 :c:func:`bt_mesh_cdb_create` 函数才能再次使用）。

最佳实践
********

* **错误处理** - 检查所有 CDB 函数的返回值，尤其是容量耗尽时可能失败的分配函数。

* **地址管理** - 除非有特定寻址需求，否则将 ``0`` 传给 :c:func:`bt_mesh_cdb_node_alloc` 函数，让 CDB 管理地址分配。

* **配置跟踪** - 配置成功后务必设置 ``BT_MESH_CDB_NODE_CONFIGURED`` 标志并存储节点，以避免不必要地重新配置节点。

* **密钥安全** - 生产代码中切勿记录或暴露密钥。使用导入/导出函数安全地处理密钥材料。

* **迭代安全** - 在 :c:func:`bt_mesh_cdb_node_foreach` 迭代期间不要修改 CDB（添加/移除节点）。先收集地址，然后再修改。

常见陷阱
********

多个配网器之间的 CDB 同步
   如果网络中存在多个配网器，请确保它们同步各自的 CDB 以避免冲突。使用应用层机制在多个配网器之间共享 CDB。没有用于 CDB 同步的内置机制。

忘记存储
   CDB 修改不会自动持久保存。使用持久存储时，更改后务必调用相应的 ``_store()`` 函数。

密钥索引错误
   导入/导出密钥时，密钥索引参数（``0`` 或 ``1``）指的是 Key Refresh 密钥数组中的位置，而不是 NetIdx 或 AppIdx。

地址冲突
   如果手动指定地址，请确保它们不与现有节点冲突。使用 :c:func:`bt_mesh_cdb_free_addr_get` 函数查找可用地址。

容量超限
   CDB 的固定容量由 Kconfig 定义。超出容量会导致分配失败。请监控 CDB 使用情况，并在需要时增加容量。

访问无效节点
   在解引用 ``_get()`` 或 ``_alloc()`` 函数返回的指针之前，务必检查指针是否为 ``NULL``。

API 参考
********

有关完整的 API 文档，请参阅：

* 头文件：:file:`include/zephyr/bluetooth/mesh/cdb.h`
* 实现：:file:`subsys/bluetooth/mesh/cdb.c`

相关文档
********

* :ref:`bluetooth_mesh`
* :ref:`bluetooth_mesh_provisioning`
* Mesh Shell 命令：:ref:`bluetooth_mesh_shell`
