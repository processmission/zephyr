.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _toolchain_eld:

嵌入式链接器（ELD）
###################

`ELD`_ 是 Qualcomm 开源的链接器，基于 LLVM 且兼容 GNU。使用 LLVM 工具链（例如 :ref:`Arm 嵌入式工具链 <toolchain_atfe>` 或主机 clang）构建 Zephyr 时，可用它替代 LLD 或 GNU ld。ELD 本身的详情见 `ELD user guide`_。

ELD 只是链接器（``ld.eld``），仍需单独的 C/C++ 工具链编译源码。

安装
****

获取 ELD 有三种方式：

#. **每日二进制发布版。** 预编译 ``ld.eld`` 二进制文件发布于 `ELD releases`_ 页面。

#. **从源码构建。** 按照 `ELD README`_，结合 LLVM 源码树构建 ELD；集成式 ``llvm-project`` 构建会在构建树的 ``bin/`` 目录生成 ``ld.eld``。

#. **通过 cpullvm 获取完整工具链。** `cpullvm`_ 是面向 Arm、AArch64 和 RISC-V 嵌入式目标的完整 LLVM 工具链，附带 ``ld.eld``、``ld.lld``、clang、运行时库和头文件。Linux 和 Windows 的预编译包发布于 `cpullvm releases page`_，cpullvm 22.1.1 已在 ELD CI 中与 Zephyr 配合测试。

方式 1 和 2 仅提供 ``ld.eld``，构建 Zephyr 仍需另备 LLVM 工具链，即 clang、运行时库和头文件。

验证安装：

.. code-block:: console

   $ ld.eld --version
   eld 22.0 (GNU Compatible linker)

需要 ELD 22.0 或更新版本。

用法
****

ELD 通过 ``host/llvm`` 工具链变体选择。将 :envvar:`LLVM_TOOLCHAIN_PATH` 指向 LLVM 工具链，例如 cpullvm 安装目录，或其他在 ``bin/`` 目录或 :envvar:`PATH` 中提供 ``ld.eld`` 的工具链，然后将 :kconfig:option:`CONFIG_LLVM_USE_ELD` 设为 ``y`` 以启用 ELD。

例如：

.. code-block:: console

   west build ... -- -DZEPHYR_TOOLCHAIN_VARIANT=host/llvm \
                     -DLLVM_TOOLCHAIN_PATH=<path-to-llvm-toolchain> \
                     -DCONFIG_LLVM_USE_ELD=y

配置 LLVM 工具链的更多信息，见 :ref:`toolchain_atfe` 或 :ref:`toolchain_zephyr_sdk`。

.. _ELD: https://github.com/qualcomm/eld
.. _ELD user guide: https://qualcomm.github.io/eld/
.. _ELD releases: https://github.com/qualcomm/eld/releases
.. _ELD README: https://github.com/qualcomm/eld#building-eld-and-running-tests
.. _cpullvm: https://github.com/qualcomm/cpullvm-toolchain
.. _cpullvm releases page: https://github.com/qualcomm/cpullvm-toolchain/releases
