.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：Telephone and Media Audio Profile Shell
#############################################

本文档介绍如何运行 Telephone and Media Audio Profile 功能。与大多数其他低层配置文件不同，TMAP 在所有设备上都存在并具有服务（TMAS）。因此，发起者和接受者（或中心设备和外围设备）都应发现远端设备的 TMAS，以了解其支持哪些 TMAP 角色。

使用 TMAP Shell
***************

蓝牙协议栈初始化（ :code:`bt init` ）后，可以调用 :code:`tmap init` 注册 TMAS。

.. code-block:: console


   tmap --help
   tmap - Bluetooth TMAP shell commands
   Subcommands:
     init          :Initialize and register the TMAS
     discover      :Discover TMAS on remote device
