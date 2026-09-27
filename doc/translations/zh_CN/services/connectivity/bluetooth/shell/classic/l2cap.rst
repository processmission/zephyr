.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：经典：L2CAP Shell
#######################

本文档介绍如何运行蓝牙经典 L2CAP 功能。 :code:`br l2cap` 命令提供蓝牙经典 L2CAP Shell 命令。

命令
****

:code:`br l2cap` 命令：

.. code-block:: console

   uart:~$ br l2cap
   l2cap - [none]
   Subcommands:
     register    : <psm> <mode: none, ret, fc, eret, stream> [hold_credit]
                   [mode_optional] [extended_control]
     connect     : <psm> <mode: none, ret, fc, eret, stream> [hold_credit]
                   [mode_optional] [extended_control]
     disconnect  : [none]
     send        : [number of packets] [length of packet(s)]
     credits     : [none]
     echo        : L2CAP BR ECHO commands
     connless    : L2CAP connectionless commands

:code:`br l2cap echo` 命令：

.. code-block:: console

   uart:~$ br l2cap echo
   echo - L2CAP BR ECHO commands
   Subcommands:
     register    : [none]
     unregister  : [none]
     req         : <length of data>
     rsp         : <identifier> <length of data>

:code:`br l2cap connless` 命令：

.. code-block:: console

   uart:~$ br l2cap connless
   connless - L2CAP connectionless commands
   Subcommands:
     register    : <psm> [sec level]
     unregister  : [none]
     send        : <psm> <length of data>

面向连接的 L2CAP
****************

1. [服务器] 注册 L2CAP 服务器：

蓝牙协议栈初始化（ :code:`bt init` ）后，可以调用 :code:`br l2cap register` 注册 L2CAP 服务器。

.. code-block:: console

   uart:~$ br l2cap register 1001 none
   L2CAP psm 4097 registered

2. [客户端] 创建 L2CAP 连接：

只有在建立 ACL 连接后才能使用该命令。

.. code-block:: console

   uart:~$ br l2cap connect 1001 none
   L2CAP connection pending

3. 已建立 L2CAP 连接：

.. code-block:: console

   uart:~$
   Security changed: XX:XX:XX:XX:XX:XX level 2
   Incoming BR/EDR conn 0x20004848
   Channel 0x20000b18 connected
   It is basic mode

3. 向远端发送 L2CAP 数据：

.. code-block:: console

   uart:~$ br l2cap send
   Rem 0

4. 已收到 L2CAP 数据：

.. code-block:: console

   uart:~$
   Incoming data channel 0x20000b18 len 200
   00000000: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   00000010: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   00000020: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   00000030: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   00000040: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   00000050: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   00000060: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   00000070: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   00000080: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   00000090: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   000000A0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   000000B0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   000000C0: 00 00 00 00 00 00 00 00                          |........         |

5. 断开 L2CAP 连接：

.. code-block:: console

   uart:~$ br l2cap disconnect

6. L2CAP 连接已断开：

.. code-block:: console

   Channel 0x20000b18 disconnected


L2CAP 回显
**********

echo 子命令提供蓝牙经典中 L2CAP 回显请求和响应的功能。

只有在建立 ACL 连接后才能使用这些命令。

1. 监听 L2CAP 回显请求和 L2CAP 回显响应：

.. code-block:: console

   uart:~$ br l2cap echo register

2. 停止监听 L2CAP 回显请求和 L2CAP 回显响应：

.. code-block:: console

   uart:~$ br l2cap echo unregister

3. 发送 L2CAP 回显请求：

.. code-block:: console

   uart:~$ br l2cap echo req 1

4. 已收到回显请求：

.. code-block:: console

   Incoming ECHO REQ data identifier 4 len 1
   00000000: 00                                               |.                |

5. 发送 L2CAP 回显响应：

.. code-block:: console

   uart:~$ br l2cap echo rsp 4 1

6. 已收到回显响应：

.. code-block:: console

   uart:~$
   Incoming ECHO RSP data len 1
   00000000: 00                                               |.                |


无连接 L2CAP
************

connless 子命令提供蓝牙经典中无连接 L2CAP 通信的功能，允许在不建立 L2CAP 连接的情况下传输数据包。

该子命令由 :kconfig:option:`CONFIG_BT_L2CAP_CONNLESS` 控制。

只有在建立 ACL 连接后才能使用这些命令。

1. 监听无连接 L2CAP 数据包：

.. code-block:: console

   uart:~$ br l2cap connless register 1001
   Register connectionless callbacks with PSM 0x1001

2. 发送数据

.. code-block:: console

   uart:~$ br l2cap connless send 1001 1
   Sending connectionless data with PSM 0x1001

3. 已收到无连接数据：

.. code-block:: console

   Incoming connectionless data psm 0x1001 len 1
   00000000: 00                                               |.                |
