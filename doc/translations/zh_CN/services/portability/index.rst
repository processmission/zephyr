.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _osal:

操作系统抽象
############

操作系统抽象层（OSAL）提供包装函数 API，用于封装任意操作系统都提供的通用系统功能。这些 API 使面向多个软件和硬件平台进行开发和代码移植变得更轻松、更快捷。

以下几节介绍 Zephyr RTOS 所支持的软件和硬件抽象层。

.. toctree::
   :maxdepth: 1

   posix/index.rst
   cmsis_rtos_v1.rst
   cmsis_rtos_v2.rst
