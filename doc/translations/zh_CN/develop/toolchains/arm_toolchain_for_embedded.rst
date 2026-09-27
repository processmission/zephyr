.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _toolchain_atfe:

Arm 嵌入式工具链（ATfE）
########################


Arm 嵌入式工具链（ATfE）是 Arm 提供的 C/C++ 工具链，基于
   自由开源的 LLVM 编译器基础设施和面向裸机目标的 Picolib C 库。

ATfE 经过专门调优，尤其注重新一代
   ARM 产品（2024 年后）的性能，例如 64 位 Arm 架构（AArch64）或 M-Profile 向量扩展（MVE，一种 32 位 Armv8.1-M 扩展）。

安装
****

#. 下载适用于当前操作系统的 `Arm toolchain for embedded`_，并解压到文件系统中。

#. :ref:`设置以下环境变量 <env_vars>`：

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为 ``host/llvm``。
   - 将 :envvar:`LLVM_TOOLCHAIN_PATH` 设为工具链安装目录。

#. 按照以下 shell 会话示例检查当前环境变量是否正确设置；系统上的 :envvar:`LLVM_TOOLCHAIN_PATH` 值可能不同。

   .. tabs::

      .. group-tab:: Ubuntu

         .. code-block:: bash

            echo $ZEPHYR_TOOLCHAIN_VARIANT
            host/llvm
            echo $LLVM_TOOLCHAIN_PATH
            /home/you/Downloads/ATfE

      .. group-tab:: macOS

         .. code-block:: bash

            echo $ZEPHYR_TOOLCHAIN_VARIANT
            host/llvm
            echo $LLVM_TOOLCHAIN_PATH
            /home/you/Downloads/ATfE

      .. group-tab:: Windows

         .. code-block:: powershell

            > echo %ZEPHYR_TOOLCHAIN_VARIANT%
            host/llvm
            > echo %LLVM_TOOLCHAIN_PATH%
            C:\ATfE

   .. _toolchain_env_var:

#. 为 Zephyr 应用生成构建系统时，也可以将 ``ZEPHYR_TOOLCHAIN_VARIANT`` 和 ``LLVM_TOOLCHAIN_PATH`` 设为 CMake 变量，如下所示：

   .. code-block:: console

      west build ... -- -DZEPHYR_TOOLCHAIN_VARIANT=host/llvm -DLLVM_TOOLCHAIN_PATH=...

工具链设置
**********

由于 LLVM 广泛兼容 GNU 工具，使用任何 LLVM 工具链构建时，都需要指定一些设置，告知编译器应使用哪些工具：

链接器
   * 设置 :envvar:`CONFIG_LLVM_USE_LLD=y`，使用 LLVM 链接器。
   * 设置 :envvar:`CONFIG_LLVM_USE_LD=y`，使用 GNU LD 链接器。

运行时库
   * 设置 :envvar:`CONFIG_COMPILER_RT_RTLIB=y`，使用 LLVM 运行时库。
   * 设置 :envvar:`CONFIG_LIBGCC_RTLIB=y`，使用 LibGCC 运行时库。

.. code-block:: console

   west build ... -- -DZEPHYR_TOOLCHAIN_VARIANT=host/llvm -DLLVM_TOOLCHAIN_PATH=... -DCONFIG_LLVM_USE_LLD=y -DCONFIG_COMPILER_RT_RTLIB=y

.. _Arm Toolchain for Embedded: https://developer.arm.com/Tools%20and%20Software/Arm%20Toolchain%20for%20Embedded
