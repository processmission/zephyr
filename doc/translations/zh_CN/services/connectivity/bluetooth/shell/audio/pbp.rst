.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：Public Broadcast Profile Shell
####################################

本文档介绍如何运行 Public Broadcast Profile 功能。PBP 没有关联的服务。其目的是更快速、更高效地发现使用常用编解码器配置传输音频的广播源端。

使用 PBP Shell
**************

蓝牙协议栈初始化（ :code:`bt init` ）后，Public Broadcast Profile 即可运行。要设置 Public Broadcast Announcement 功能，请调用 :code:`pbp set_features`。

.. code-block:: console


   pbp --help
   pbp - Bluetooth PBP shell commands
   Subcommands:
     set_features    :Set the Public Broadcast Announcement features
