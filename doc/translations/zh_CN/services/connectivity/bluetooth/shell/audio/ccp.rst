.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：Call Control Profile Shell
################################

呼叫控制服务器
**************
呼叫控制服务器是一种角色，通常位于能够发起呼叫的设备上，包括来自 Skype 等应用的呼叫，例如（智能）手机和 PC，这些设备通常是 GAP 中心设备。

使用呼叫控制服务器
==================
服务器可以在本地控制，也可以由远端设备控制（在通话中时）。例如，远端设备可以向服务器发起呼叫，服务器也可以在没有客户端的情况下向远端设备发起呼叫。

对于所有接受可选 :code:`index` 的命令，如果未提供索引，则默认为 :code:`0`，即 GTBS 承载。

.. code-block:: console

   ccp_call_control_server --help
   ccp_call_control_server - Bluetooth CCP Call Control Server shell commands
   Subcommands:
     init                    : Initialize CCP Call Control Server
     set_bearer_name         : Set bearer name [index] <name>
     get_bearer_name         : Get bearer name [index]
     get_bearer_uci          : Get bearer UCI [index]
     set_bearer_tech         : Set bearer technology [index] <technology>
     get_bearer_tech         : Get bearer technology [index]
     set_bearer_uri_schemes  : Set bearer URI schemes supported list [index] <URI schemes>
                              (e.g. "tel,skype")
     get_bearer_uri_schemes  : Get bearer URI schemes supported list [index]


用法示例
========

设置
----

.. code-block:: console

   uart:~$ bt init
   uart:~$ ccp_call_control_server init
   Registered GTBS bearer
   Registered bearer[1]
   uart:~$ bt connect P:xx:xx:xx:xx:xx:xx

设置和获取承载名称
------------------

.. code-block:: console

   uart:~$ ccp_call_control_server get_bearer_name
   Bearer[0] name: Generic TBS
   uart:~$ ccp_call_control_server set_bearer_name "New name"
   Bearer[0] name: New name
   uart:~$ ccp_call_control_server get_bearer_name
   Bearer[0] name: New name
   uart:~$ ccp_call_control_server get_bearer_name 1
   Bearer[1] name: Telephone Bearer #1
   uart:~$ ccp_call_control_server set_bearer_name 1 "New TBS name"
   Bearer[1] name: New TBS name
   uart:~$ ccp_call_control_server get_bearer_name 1
   Bearer[1] name: New TBS name

获取承载 UCI
------------

.. code-block:: console

   uart:~$ ccp_call_control_server get_bearer_uci
   Bearer[0] UCI: un999
   uart:~$ ccp_call_control_server get_bearer_uci 1
   Bearer[1] UCI: skype


设置和获取承载技术
------------------

.. code-block:: console

   uart:~$ ccp_call_control_server get_bearer_tech
   Bearer[0] technology: 3G (0x01)
   uart:~$ ccp_call_control_server set_bearer_tech 0x02
   Bearer[0] new technology: 4G (0x02)

设置和获取承载 URI 支持的方案列表
---------------------------------

.. code-block:: console

   uart:~$ ccp_call_control_server get_bearer_uri_schemes
   Bearer[0] URI schemes supported list: tel,skype
   uart:~$ ccp_call_control_server set_bearer_uri_schemes "tel,teamspeak"
   Bearer[0] new URI schemes supported list: tel,teamspeak

呼叫控制客户端
**************
呼叫控制客户端是一种角色，通常位于耳塞或耳机等资源受限设备上。

使用呼叫控制客户端
==================
客户端可以控制远端 CCP 服务器设备。例如，远端设备可能有来电，客户端可以接听。

.. code-block:: console

   uart:~$ ccp_call_control_client --help
   ccp_call_control_client - Bluetooth CCP Call Control Client shell commands
   Subcommands:
     discover  : Discover GTBS and TBS on remote device

连接后的用法示例
================

.. code-block:: console

   uart:~$ ccp_call_control_client discover
   Discovery completed with GTBS and 1 TBS bearers

.. code-block:: console

   uart:~$ ccp_call_control_client read_bearer_name
   Bearer 0x20046254 name: Generic TBS
   uart:~$ ccp_call_control_client read_bearer_name 1
   Bearer 0x20046256 name: Telephone Bearer #1
   uart:~$ ccp_call_control_client read_bearer_uci
   Bearer 0x20046254 UCI: un999
   uart:~$ ccp_call_control_client read_bearer_uci 1
   Bearer 0x20046256 UCI: skype
