.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _toolchain_hexagon:

Qualcomm Hexagon LLVM 工具链
############################

#. 从 `toolchain_for_hexagon releases page <https://github.com/quic/toolchain_for_hexagon/releases>`_ 下载预编译的 Hexagon LLVM 交叉工具链，解压到例如 ``/opt/hexagon-toolchain``。安装目录是包含 ``bin/clang`` 的目录。

   请使用基于 LLVM 23 或更新版本构建的发布版。早期版本会错误编译 ``~BIT(n)``，修复已合入 `#205489 <https://github.com/llvm/llvm-project/pull/205489>`_。

#. 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为 ``hexagon``，将 :envvar:`HEXAGON_TOOLCHAIN_PATH` 设为该目录：

   .. code-block:: bash

      export ZEPHYR_TOOLCHAIN_VARIANT=hexagon
      export HEXAGON_TOOLCHAIN_PATH=/opt/hexagon-toolchain

.. envvar:: HEXAGON_TOOLCHAIN_PATH

   Hexagon LLVM 交叉工具链安装目录。

该工具链是标准 LLVM 安装，因此此变体相当于使用另一套编译器的 :ref:`host_toolchains` ``llvm`` 变体。它使用独立路径变量，因为 Hexagon clang 只注册 Hexagon 目标，无法构建 :zephyr:board:`native_sim` 等由主机编译的目标。需要同时支持两类目标的环境，必须分别指定两套 LLVM 安装；Zephyr CI 在一次 Twister 运行覆盖两类平台时也这样做。

只要指定的是 Hexagon 安装，使用 ``ZEPHYR_TOOLCHAIN_VARIANT=host/llvm`` 和 :envvar:`LLVM_TOOLCHAIN_PATH` 构建 Hexagon 目标是等效的，且仍受支持。
