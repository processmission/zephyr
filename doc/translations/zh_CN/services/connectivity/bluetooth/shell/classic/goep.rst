.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：经典：GOEP Shell
######################

本文档介绍如何运行蓝牙经典 GOEP 功能。 :code:`goep` 命令提供蓝牙经典 GOEP Shell 命令。

命令
****

:code:`goep` 命令：

.. code-block:: console

   uart:~$ goep
   goep - Bluetooth GOEP shell commands
   Subcommands:
     register-rfcomm    : <channel>
     connect-rfcomm     : <channel>
     disconnect-rfcomm  :
     register-l2cap     : <psm>
     connect-l2cap      : <psm>
     disconnect-l2cap   :
     alloc-buf          : Alloc tx buffer
     release-buf        : Free allocated tx buffer
     add-header         : Adding header sets
     client             : Client sets
     server             : Server sets

:code:`goep client` 命令：

.. code-block:: console

   uart:~$ goep client
   client - Client sets
   Subcommands:
     conn     : <mopl>
     disconn  :
     put      : <final: true, false>
     get      : <final: true, false>
     abort    :
     setpath  : [parent] [create]
     action   : <final: true, false>

:code:`goep server` 命令：

.. code-block:: console

   uart:~$ goep server
   server - Server sets
   Subcommands:
     reg      : [UUID 128]
     unreg    :
     conn     : <rsp: continue, success, error> <mopl> [rsp_code]
     disconn  : <rsp: continue, success, error> [rsp_code]
     put      : <rsp: continue, success, error> [rsp_code]
     get      : <rsp: continue, success, error> [rsp_code]
     abort    : <rsp: continue, success, error> [rsp_code]
     setpath  : <rsp: continue, success, error> [rsp_code]
     action   : <rsp: continue, success, error> [rsp_code]


连接 GOEP 传输
**************

在创建 GOEP 传输连接之前，应先建立 ACL 连接。

该传输基于 L2CAP 通道：

.. tabs::

   .. group-tab:: L2CAP 服务器

      .. code-block:: console

         uart:~$ goep register-l2cap 0
         L2CAP server (psm 1001) is registered
         Security changed: XX:XX:XX:XX:XX:XX level 2
         GOEP 0x20005600 transport connected on 0x20004dc8
         uart:~$

   .. group-tab:: L2CAP 客户端

      .. code-block:: console

         uart:~$ goep connect-l2cap 1001
         GOEP L2CAP connection pending
         Security changed: XX:XX:XX:XX:XX:XX level 2
         GOEP 0x20005600 transport connected on 0x20004dc8
         uart:~$


该传输基于 RFCOMM 通道：

.. tabs::

   .. group-tab:: RFCOMM 服务器

      .. code-block:: console

         uart:~$ goep register-rfcomm 0
         RFCOMM server (channel 06) is registered
         Security changed: XX:XX:XX:XX:XX:XX level 2
         GOEP 0x20005600 transport connected on 0x20004dc8
         uart:~$

   .. group-tab:: RFCOMM 客户端

      .. code-block:: console

         uart:~$ goep connect-rfcomm 6
         GOEP RFCOMM connection pending
         Security changed: XX:XX:XX:XX:XX:XX level 2
         GOEP 0x20005600 transport connected on 0x20004dc8
         uart:~$


断开 GOEP 传输
**************

该传输基于 L2CAP 通道：

.. tabs::

   .. group-tab:: 一侧

      .. code-block:: console

         GOEP 0x20005600 transport disconnected
         uart:~$

   .. group-tab:: 另一侧

      .. code-block:: console

         uart:~$ goep disconnect-l2cap
         GOEP L2CAP disconnection pending
         GOEP 0x20005600 transport disconnected
         uart:~$


该传输基于 RFCOMM 通道：

.. tabs::

   .. group-tab:: 一侧

      .. code-block:: console

         GOEP 0x20005600 transport disconnected
         uart:~$

   .. group-tab:: 另一侧

      .. code-block:: console

         uart:~$ goep disconnect-rfcomm
         GOEP RFCOMM disconnection pending
         GOEP 0x20005600 transport disconnected
         uart:~$


连接到 OBEX 服务器
******************

.. tabs::

   .. group-tab:: OBEX 服务器

      .. code-block:: console

         uart:~$ goep server reg
         uart:~$
         OBEX server 0x20005850 conn req, version 10, mopl 00ff
         uart:~$ goep server conn success 255
         uart:~$

   .. group-tab:: OBEX 客户端

      .. code-block:: console

         uart:~$ goep client conn 255
         OBEX client 0x20005818 conn rsp, rsp_code Success, version 10, mopl 00ff
         uart:~$


断开与 OBEX 服务器的连接
************************

.. tabs::

   .. group-tab:: OBEX 服务器

      .. code-block:: console

         OBEX server 0x20005850 disconn req
         uart:~$ goep server disconn success
         uart:~$

   .. group-tab:: OBEX 客户端

      .. code-block:: console

         uart:~$ goep client disconn
         OBEX client 0x20005818 disconn rsp, rsp_code Success
         uart:~$


OBEX Put 操作
*************

.. tabs::

   .. group-tab:: OBEX 服务器

      .. code-block:: console

         uart:~$
         OBEX server 0x20005850 put req, final false, data len 12
         HI c3 Len 4
         00000000: 00 00 00 09                                      |....             |
         HI 48 Len 4
         00000000: 12 34 56 78                                      |.4Vx             |
         uart:~$ goep server put continue
         OBEX server 0x20005850 put req, final true, data len 8
         HI 49 Len 5
         00000000: 12 34 56 78 90                                   |.4Vx.            |
         uart:~$ goep server put success
         uart:~$

   .. group-tab:: OBEX 客户端

      .. code-block:: console

         uart:~$ goep alloc-buf
         uart:~$ goep add-header len 9
         uart:~$ goep add-header body 12345678
         uart:~$ goep client put false
         OBEX client 0x20005818 put rsp, rsp_code Continue, data len 0
         uart:~$ goep alloc-buf
         uart:~$ goep add-header end_body 1234567890
         uart:~$ goep client put true
         OBEX client 0x20005818 put rsp, rsp_code Success, data len 0
         uart:~$


OBEX Get 操作
*************

.. tabs::

   .. group-tab:: OBEX 服务器

      .. code-block:: console

         uart:~$ goep alloc-buf
         uart:~$ goep add-header len 9
         uart:~$ goep add-header body 12345678
         uart:~$ goep server get continue
         OBEX server 0x20005850 get req, final true, data len 0
         uart:~$ goep alloc-buf
         uart:~$ goep add-header end_body 1234567890
         uart:~$
         uart:~$ goep server get success
         uart:~$

   .. group-tab:: OBEX 客户端

      .. code-block:: console

         uart:~$ goep client get true
         OBEX client 0x20005818 get rsp, rsp_code Continue, data len 12
         HI c3 Len 4
         00000000: 00 00 00 09                                      |....             |
         HI 48 Len 4
         00000000: 12 34 56 78                                      |.4Vx             |
         uart:~$ goep client get true
         OBEX client 0x20005818 get rsp, rsp_code Success, data len 8
         HI 49 Len 5
         00000000: 12 34 56 78 90                                   |.4Vx.            |
         uart:~$
