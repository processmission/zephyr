.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：电话承载服务 Shell
########################

本文档介绍如何以客户端和（电话承载服务（TBS））服务器两种角色运行呼叫控制功能。请注意，在下面的示例中，已删除部分调试信息行，以便缩短篇幅并提供更清晰的概览。

电话承载服务客户端
******************

电话承载服务客户端通常存在于资源受限设备上，例如耳机，但也可能存在于手机或笔记本电脑等设备上。因此，呼叫控制客户端通常也是广播者。客户端可以使用呼叫控制点控制服务器上的通话状态。

要以交互方式使用客户端，必须启用 :kconfig:option:`CONFIG_BT_TBS_CLIENT_LOG_LEVEL_DBG`。

使用电话承载服务客户端
======================

蓝牙协议栈初始化（ :code:`bt init` ）并连接设备后，电话承载服务客户端可以调用 :code:`tbs_client discover` 发现已连接设备上的 TBS；该命令会开始发现 TBS UUID 并存储句柄，并可选择订阅所有通知（默认订阅所有通知）。

由于服务器可能有多个 TBS 实例，大多数 tbs_client 命令会将索引（从 0 开始）作为输入。加入通话至少需要 2 个通话 ID，并且所有通话索引应位于同一个 TBS 实例上。

服务器还会有一个 GTBS 实例，它是服务器上所有电话承载的抽象层。如果服务器同时具有 GTBS 和 TBS，则启用 :code:`BT_TBS_CLIENT_GTBS` 时，客户端可以订阅并在发送请求时使用其中任意一个。

.. code-block:: console

   tbs_client --help
   tbs_client - Bluetooth TBS_CLIENT shell commands
   Subcommands:
      discover                       :Discover TBS [subscribe]
      set_signal_reporting_interval  :Set the signal reporting interval
                                       [<{instance_index, gtbs}>] <interval>
      originate                      :Originate a call [<{instance_index, gtbs}>]
                                       <uri>
      terminate                      :terminate a call [<{instance_index, gtbs}>]
                                       <id>
      accept                         :Accept a call [<{instance_index, gtbs}>] <id>
      hold                           :Place a call on hold [<{instance_index,
                                       gtbs}>] <id>
      retrieve                       :Retrieve a held call [<{instance_index,
                                       gtbs}>] <id>
      read_provider_name             :Read the bearer name [<{instance_index,
                                       gtbs}>]
      read_bearer_uci                :Read the bearer UCI [<{instance_index, gtbs}>]
      read_technology                :Read the bearer technology [<{instance_index,
                                       gtbs}>]
      read_uri_list                  :Read the bearer's supported URI list
                                       [<{instance_index, gtbs}>]
      read_signal_strength           :Read the bearer signal strength
                                       [<{instance_index, gtbs}>]
      read_signal_interval           :Read the bearer signal strength reporting
                                       interval [<{instance_index, gtbs}>]
      read_current_calls             :Read the current calls [<{instance_index,
                                       gtbs}>]
      read_ccid                      :Read the CCID [<{instance_index, gtbs}>]
      read_status_flags              :Read the in feature and status value
                                       [<{instance_index, gtbs}>]
      read_uri                       :Read the incoming call target URI
                                       [<{instance_index, gtbs}>]
      read_call_state                :Read the call state [<{instance_index, gtbs}>]
      read_remote_uri                :Read the incoming remote URI
                                       [<{instance_index, gtbs}>]
      read_friendly_name             :Read the friendly name of an incoming call
                                       [<{instance_index, gtbs}>]
      read_optional_opcodes          :Read the optional opcodes [<{instance_index,
                                       gtbs}>]


在以下示例中，除非另有说明，否则会忽略来自 GTBS 的通知。

用法示例
========

设置
----

.. code-block:: console

   uart:~$ bt init
   uart:~$ bt advertise on
   Advertising started

连接后
------

拨打电话：

.. code-block:: console

   uart:~$ tbs_client discover
   <dbg> bt_tbs_client.primary_discover_func: Discover complete, found 1 instances (GTBS found)
   <dbg> bt_tbs_client.discover_func: Setup complete for 1 / 1 TBS
   <dbg> bt_tbs_client.discover_func: Setup complete GTBS
   uart:~$ tbs_client originate 0 tel:123
   <dbg> bt_tbs_client.notify_handler: Index 0
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x01 is in the dialing state with URI tel:123
   <dbg> bt_tbs_client.call_cp_notify_handler: Status: success for the originate opcode for call 0x00
   <dbg> bt_tbs_client.notify_handler: Index 0
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x01 is in the alerting state with URI tel:123
   <call answered by peer device, and status notified by TBS server>
   <dbg> bt_tbs_client.notify_handler: Index 0
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x01 is in the active state with URI tel:123

在 GTBS 上拨打电话：

.. code-block:: console

   uart:~$ tbs_client originate 0 tel:123
   <dbg> bt_tbs_client.notify_handler: Index 0
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x01 is in the dialing state with URI tel:123
   <dbg> bt_tbs_client.call_cp_notify_handler: Status: success for the originate opcode for call 0x00
   <dbg> bt_tbs_client.notify_handler: Index 0
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x01 is in the alerting state with URI tel:123
   <call answered by peer device, and status notified by TBS server>
   <dbg> bt_tbs_client.notify_handler: Index 0
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x01 is in the active state with URI tel:123

拨打电话前必须设置去电主叫号码。

接听来自对端设备的来电：

.. code-block:: console

   <dbg> bt_tbs_client.incoming_uri_notify_handler: tel:123
   <dbg> bt_tbs_client.in_call_notify_handler: tel:456
   <dbg> bt_tbs_client.friendly_name_notify_handler: Peter
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x05 is in the incoming state with URI tel:456
   uart:~$ tbs_client accept 0 5
   <dbg> bt_tbs_client.call_cp_callback_handler: Status: success for the accept opcode for call 0x05
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x05 is in the active state with URI tel


终止通话：

.. code-block:: console

   uart:~$ tbs_client terminate 0 5
   <dbg> bt_tbs_client.termination_reason_notify_handler: ID 0x05, reason 0x06
   <dbg> bt_tbs_client.call_cp_notify_handler: Status: success for the terminate opcode for call 0x05
   <dbg> bt_tbs_client.current_calls_notify_handler:

电话承载服务（TBS）
*******************
电话承载服务是一种服务，通常位于能够拨打和接听电话的设备上，包括来自 Skype 等应用的呼叫，例如（智能）手机和 PC。

要以交互方式使用 TBS 服务器，必须启用 :kconfig:option:`CONFIG_BT_TBS_LOG_LEVEL_DBG`。

使用电话承载服务
================
TBS 可以在本地控制，也可以由远端设备控制（在通话中时）。例如，远端设备可以向具有 TBS 服务器的设备发起呼叫，TBS 服务器也可以在没有 TBS_CLIENT 客户端的情况下向远端设备发起呼叫。TBS 实现能够完全控制任何通话。对于可以传入 :code:`<instance_index>` 的命令，如果省略索引，则默认为 GTBS 承载。

.. code-block:: console

   tbs --help
   tbs - Bluetooth TBS shell commands
   Subcommands:
      init                        :Initialize TBS
      authorize                   :Authorize the current connection
      accept                      :Accept call <call_index>
      terminate                   :Terminate call <call_index>
      hold                        :Hold call <call_index>
      retrieve                    :Retrieve call <call_index>
      originate                   :Originate call [<instance_index>] <uri>
      join                        :Join calls <id> <id> [<id> [<id> [...]]]
      incoming                    :Simulate incoming remote call [<{instance_index,
                                    gtbs}>] <local_uri> <remote_uri>
                                    <remote_friendly_name>
      remote_answer               :Simulate remote answer outgoing call <call_index>
      remote_retrieve             :Simulate remote retrieve <call_index>
      remote_terminate            :Simulate remote terminate <call_index>
      remote_hold                 :Simulate remote hold <call_index>
      set_bearer_provider_name    :Set the bearer provider name [<{instance_index,
                                    gtbs}>] <name>
      set_bearer_technology       :Set the bearer technology [<{instance_index,
                                    gtbs}>] <technology>
      set_bearer_signal_strength  :Set the bearer signal strength [<{instance_index,
                                    gtbs}>] <strength>
      set_status_flags            :Set the bearer feature and status value
                                    [<{instance_index, gtbs}>] <feature_and_status>
      set_uri_scheme              :Set the URI prefix list <bearer_idx> <uri1[,uri2[,uri3[,...]]]>
      print_calls                 :Output all calls in the debug log

用法示例
========

Setup
-----

.. code-block:: console

   uart:~$ bt init
   uart:~$ bt connect P:xx:xx:xx:xx:xx:xx

When connected
--------------

接听由客户端发起的、对端设备上的通话：

.. code-block:: console

   <dbg> bt_tbs.write_call_cp: Index 0: Processing the originate opcode
   <dbg> bt_tbs.originate_call: New call with call index 1
   <dbg> bt_tbs.write_call_cp: Index 0: Processed the originate opcode with status success for call index 1
   uart:~$ tbs remote_answer 1
   TBS succeeded for call_id: 1

来自对端设备的来电，由客户端接听：

.. code-block:: console

   uart:~$ tbs incoming 0 tel:123 tel:456 Peter
   TBS succeeded for call_id: 4
   <dbg> bt_tbs.bt_tbs_remote_incoming: New call with call index 4
   <dbg> bt_tbs.write_call_cp: Index 0: Processed the accept opcode with status success for call index 4
