.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：协调集标识配置文件 Shell
##############################

本文档介绍如何以客户端和服务器两种角色运行协调集标识功能。请注意，在下面的示例中，已删除部分调试信息行，以便缩短篇幅并提供更清晰的概览。

集协调者（客户端）
******************

客户端通常是资源丰富的设备，例如智能手机或笔记本电脑。客户端可以锁定和释放协调集的成员。协调集被锁定期间，其他客户端不能锁定该集。

要锁定一个集，客户端必须连接到它想要锁定的每个集成员。此实现始终会尝试同时连接到该集的所有成员。因此，如果集大小为 3，则 :code:`BT_MAX_CONN` 应至少为 3。

如果集成员上的锁定需要在断开连接后保持，则必须与集成员绑定。如果需要与多个集成员绑定，请确保正确配置 :code:`BT_MAX_PAIRED`。

使用集协调者
============

蓝牙协议栈初始化（ :code:`bt init` ）并连接集成员设备后，可以调用 :code:`csip_set_coordinator init` 初始化呼叫控制客户端；该命令会开始发现 TBS UUID 并存储句柄，并可选择订阅所有通知（默认订阅所有通知）。

客户端连接并发现句柄后，即可读取集信息，这是识别其他集成员所必需的信息。然后客户端可以扫描并连接到其余集成员；连接所有成员后，即可锁定和释放该集。

必须启用 :kconfig:option:`CONFIG_BT_CSIP_SET_COORDINATOR_LOG_LEVEL_DBG` 才能正确使用集协调者。

.. code-block:: console

   csip_set_coordinator --help
   csip_set_coordinator - Bluetooth CSIP_SET_COORDINATOR shell commands
   Subcommands:
      init              :Initialize CSIP_SET_COORDINATOR
      discover          :Run discover for CSIS on peer device [member_index]
      discover_members  :Scan for set members <set_pointer>
      lock_set          :Lock set
      release_set       :Release set
      lock              :Lock specific member [member_index]
      release           :Release specific member [member_index]
      lock_get          :Get the lock value of the specific member and instance
                        [member_index [inst_idx]]


用法示例
========

设置
----

.. code-block:: console

   uart:~$ init
   uart:~$ bt connect P:xx:xx:xx:xx:xx:xx

连接后
------

发现设备上的集：

.. code-block:: console

   uart:~$ csip_set_coordinator init
   <dbg> bt_csip_set_coordinator.primary_discover_func: [ATTRIBUTE] handle 0x0048
   <dbg> bt_csip_set_coordinator.primary_discover_func: Discover complete, found 1 instances
   <dbg> bt_csip_set_coordinator.discover_func: Setup complete for 1 / 1
   Found 1 sets on device
   uart:~$ csip_set_coordinator discover_sets
   <dbg> bt_csip_set_coordinator.SIRK
   36 04 9a dc 66 3a a1 a1 |6...f:..
   1d 9a 2f 41 01 73 3e 01 |../A.s>.
   <dbg> bt_csip_set_coordinator.csip_set_coordinator_discover_sets_read_set_size_cb: 2
   <dbg> bt_csip_set_coordinator.csip_set_coordinator_discover_sets_read_set_lock_cb: 1
   <dbg> bt_csip_set_coordinator.csip_set_coordinator_discover_sets_read_rank_cb: 1
   Set size 2 (pointer: 0x566fdfe8)

基于上面的集指针发现集成员：

.. code-block:: console

   uart:~$ csip_set_coordinator discover_members 0x566fdfe8
   <dbg> bt_csip_set_coordinator.csip_found: Found CSIS advertiser with address P:34:02:86:03:86:c0
   <dbg> bt_csip_set_coordinator.is_set_member: hash: 0x33ccb1, prand 0x5bfe6a
   <dbg> bt_csip_set_coordinator.is_discovered: P:34:02:86:03:86:c0
   <dbg> bt_csip_set_coordinator.is_discovered: P:34:13:e8:b3:7f:9e
   <dbg> bt_csip_set_coordinator.csip_found: Found member (2 / 2)
   Discovered 2/2 set members

锁定集成员：

.. code-block:: console

   uart:~$ csip_set_coordinator lock_set
   <dbg> bt_csip_set_coordinator.bt_csip_set_coordinator_lock_set: Connecting to P:34:02:86:03:86:c0
   <dbg> bt_csip_set_coordinator.csip_set_coordinator_connected: Connected to P:34:02:86:03:86:c0
   <dbg> bt_csip_set_coordinator.discover_func: Setup complete for 1 / 1
   <dbg> bt_csip_set_coordinator.csip_set_coordinator_lock_set_init_cb:
   <dbg> bt_csip_set_coordinator.SIRK
   36 04 9a dc 66 3a a1 a1 |6...f:..
   1d 9a 2f 41 01 73 3e 01 |../A.s>.
   <dbg> bt_csip_set_coordinator.csip_set_coordinator_discover_sets_read_set_size_cb: 2
   <dbg> bt_csip_set_coordinator.csip_set_coordinator_discover_sets_read_set_lock_cb: 1
   <dbg> bt_csip_set_coordinator.csip_set_coordinator_discover_sets_read_rank_cb: 2
   <dbg> bt_csip_set_coordinator.csip_set_coordinator_write_lowest_rank: Locking member with rank 1
   <dbg> bt_csip_set_coordinator.notify_func: Instance 0 lock was locked
   <dbg> bt_csip_set_coordinator.csip_set_coordinator_write_lowest_rank: Locking member with rank 2
   <dbg> bt_csip_set_coordinator.notify_func: Instance 0 lock was locked
   Set locked

释放集成员：

.. code-block:: console

   uart:~$ csip_set_coordinator release_set
   <dbg> bt_csip_set_coordinator.csip_set_coordinator_release_highest_rank: Releasing member with rank 2
   <dbg> bt_csip_set_coordinator.notify_func: Instance 0 lock was released
   <dbg> bt_csip_set_coordinator.csip_set_coordinator_release_highest_rank: Releasing member with rank 1
   <dbg> bt_csip_set_coordinator.notify_func: Instance 0 lock was released
   Set released

协调集成员（服务器）
********************
该服务器位于属于某个集的设备上，该集由至少两台设备组成，例如一对耳塞。

使用集成员
==========

.. code-block:: console

   csip_set_member --help
   csip_set_member - Bluetooth CSIP set member shell commands
      Subcommands:
      register           : Initialize the service and register callbacks [size
                           <int>] [rank <int>] [not-lockable] [sirk <data>]
      lock               : Lock the set
      release            : Release the set [force]
      sirk               : Set the currently used SIRK <sirk>
      set_size_and_rank  : Set the currently used size and rank <size> <rank>
      get_info           : Get service info
      sirk_rsp           : Set the response used in SIRK requests <accept,
                           accept_enc, reject, oob>



用法示例
========

Setup
-----

.. code-block:: console

   uart:~$ bt init
   uart:~$ csip_set_member register


设置新的 SIRK
-------------

此命令可以修改当前使用的 SIRK。要让新的 RSI 在空口广播，必须再次调用 :code:`bt adv-data` 或 :code:`bt advertise` 来设置新的广播数据。如果启用了 :code:`CONFIG_BT_CSIP_SET_MEMBER_SIRK_NOTIFIABLE`，这还会通知已连接的客户端。

.. code-block:: console

   uart:~$ csip_set_member sirk 00112233445566778899aabbccddeeff
   SIRK updated

设置新的集大小和排名
--------------------

此命令可以修改服务实例的集大小和排名。此操作应同时对该集中的所有设备执行，且所有设备应具有相同的集大小。如果该集不可锁定，则忽略排名；否则排名应 <= 集大小，并且在该集中对该设备唯一。

.. code-block:: console

   uart:~$ csip_set_member set_size_and_rank 1 1
   Set size and rank updated to 1 and 1

获取当前信息
------------

此命令可以获取当前使用的集信息。

.. code-block:: console

   uart:~$ csip_set_member get_info
   Info for 0x2003b0c8
           SIRK
   00000000: 20 37 0a 00 95 c4 04 20  00 00 00 00 f1 79 09 00 | 7.....  .....y..|
           Set size: 2
           Rank: 1
           Lockable: true
           Locked: false
