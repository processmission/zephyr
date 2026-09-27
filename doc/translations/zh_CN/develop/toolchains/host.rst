.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _host_toolchains:

主机工具链
##########

在某些配置下，例如在 Linux 主机上为非 MCU 的 x86 目标构建时，可以复用操作系统提供的原生开发工具。

使用主机 gcc 时，将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` :ref:`环境变量 <env_vars>` 设为 ``host/gnu``。使用 clang 时，将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为 ``host/llvm``。
