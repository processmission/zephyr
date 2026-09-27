.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：Basic Audio Profile：Scan Delegator Shell
###############################################

本文档介绍如何运行 Scan Delegator 功能。请注意，在下面的示例中，已删除部分调试信息行，以便缩短篇幅并提供更清晰的概览。

Scan Delegator 可以选择支持周期性广播同步传输（PAST）协议。

Scan Delegator 服务器通常位于具有输入或输出的设备上。

要以交互方式使用 Scan Delegator，必须启用 :kconfig:option:`CONFIG_BT_BAP_SCAN_DELEGATOR_LOG_LEVEL_DBG`。

Scan Delegator 目前只能设置接收状态的同步状态，尚不支持与周期性广播同步。

.. code-block:: console

   bap_scan_delegator --help
   bap_scan_delegator - Bluetooth BAP Scan Delegator shell commands
   Subcommands:
     init                : Initialize the service and register callbacks
     set_past_pref       : Set PAST preference <true || false>
     sync_pa             : Sync to PA <src_id>
     term_pa             : Terminate PA sync <src_id>
     add_src             : Add a PA as source <addr> <sid> <broadcast_id>
                          <enc_state> [bis_sync [metadata]]
     add_src_by_pa_sync  : Add a PA as source <broadcast_id> <enc_state> [bis_sync
                          [metadata]]
     mod_src             : Modify source <src_id> <broadcast_id> <enc_state>
                          [bis_sync [metadata]]
     rem_src             : Remove source <src_id>
     synced              : Set server scan state <src_id> <bis_syncs>




用法示例
********

设置
====

.. code-block:: console

   uart:~$ bt init
   uart:~$ bap_scan_delegator init
   uart:~$ bt advertise on
   Advertising started

添加源端
========

.. code-block:: console

   uart:~$ bap_scan_delegator add_src P:11:22:33:44:55:66 0 1234 0
   Receive state with ID 0 updated

通过 PA 同步添加源端
====================

.. code-block:: console

   uart:~$ bt scan on
   Found broadcaster with ID 0x681A22 and addr R:2C:44:05:82:EB:82 and sid 0x00 (looking for 0x1000000)
   uart:~$ bt scan off
   uart:~$ bt per-adv-sync-create R:2C:44:05:82:EB:82 0
   PA 0x2003e9b0 synced
   uart:~$ bap_scan_delegator add_src_by_pa_sync 0x681A22 0
   Receive state with ID 0 updated

连接后
======

设置源端的同步状态：

.. code-block:: console

   uart:~$ bap_scan_delegator synced 0 1 3 0
