.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _llext:

可链接可加载扩展（LLEXT）
#########################

LLEXT 子系统提供了一个工具箱，可利用可链接可加载代码在运行时扩展应用程序的功能。

扩展是 ELF 格式的预编译可执行文件，可以经过验证、加载，并与主 Zephyr 二进制文件链接。扩展可以在一定程度上被操作和自省，也可以在不再需要时卸载。

.. toctree::
   :maxdepth: 1

   config
   build
   load
   debug
   api

.. note::

   LLEXT 子系统需要特定架构支持，目前仅在 RISC-V、ARM、ARM64、ARC、x86 和 Xtensa 内核上可用。
