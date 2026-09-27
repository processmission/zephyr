.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：L2CAP Shell
#################

:code:`l2cap` 命令公开部分 L2CAP API。以下示例展示如何注册 LE PSM、从另一台设备连接到该 PSM，并发送 3 个各 14 个八位字节的数据包。

该示例假设两台设备已连接。

在设备 A 上注册 LE PSM：

.. code-block:: console

        uart:~$ l2cap register 29
        L2CAP psm 41 sec_level 1 registered

在设备 B 上连接到已注册的 LE PSM 并发送数据：

.. code-block:: console

        uart:~$ l2cap connect 29
        Chan sec: 1
        L2CAP connection pending
        Channel 0x20000210 connected
        Channel 0x20000210 status 1
        uart:~$ l2cap send 3 14
        Rem 2
        Rem 1
        Rem 0
        Outgoing data channel 0x20000210 transmitted
        Outgoing data channel 0x20000210 transmitted
        Outgoing data channel 0x20000210 transmitted

在设备 A 上，您应已收到数据：

.. code-block:: console

        Incoming conn 0x20002398
        Channel 0x20000210 status 1
        Channel 0x20000210 connected
        Channel 0x20000210 requires buffer
        Incoming data channel 0x20000210 len 14
        00000000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff       |........ ......  |
        Channel 0x20000210 requires buffer
        Incoming data channel 0x20000210 len 14
        00000000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff       |........ ......  |
        Channel 0x20000210 requires buffer
        Incoming data channel 0x20000210 len 14
        00000000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff       |........ ......  |
