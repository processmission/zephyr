.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _clang:

Clang 静态分析器支持
####################

Clang 静态分析器基于 Clang 和 LLVM。严格来说，它是 Clang 的一部分，因为 Clang 由一组可复用的 C++ 库组成，用于构建强大的源码级工具。Clang 静态分析器使用的分析引擎也是一个 Clang 库，可以在不同上下文中由不同客户端复用。

LLVM 提供多种方式对代码库运行分析器：使用专用工具 scan-build 和 analyze-build，或向 clang 传递 --analyze 命令行参数。

- 对于通过简单的 $CC makefile 变量选择编译器的项目，scan-build 最方便，它通过包装并替换编译器调用进行分析。

- analyze-build 是 scan-build 的子工具，仅依赖 compile_commands.json 数据库进行分析。

- clang 的 --analyze 选项会在构建期间运行分析器，但不生成目标文件，因此无法执行链接。在这里，第一次链接就会失败并停止分析。

由于 Zephyr 构建基础设施较复杂，通过 analyze-build 调用 clang 分析器是最简单的分析方式。

`Clang static analyzer documentation <https://clang.llvm.org/docs/ClangStaticAnalyzer.html>`__ （Clang 静态分析器文档）

安装 clang 分析器
*****************

scan-build 及其子工具 analyze-build 随 LLVM 二进制发行版提供。确保其二进制目录位于 PATH 中。

scan-build 也以独立 Python 包形式提供，可从 `pypi <https://pypi.org/project/scan-build/>`__ 获取。

.. code-block:: shell

    pip install scan-build

运行 clang 静态分析器
*********************

.. note::

  分析器要求项目使用 LLVM 工具链构建，并生成 compile_commands.json 数据库。

运行 clang 静态分析器时，调用 :ref:`west build <west-building>`，同时传入 ``-DZEPHYR_SCA_VARIANT=clang`` 和 LLVM 工具链参数，例如：

.. zephyr-app-commands::
   :zephyr-app: samples/userspace/hello_world_user
   :board: qemu_x86
   :gen-args: -DZEPHYR_TOOLCHAIN_VARIANT=host/llvm -DLLVM_TOOLCHAIN_PATH=... -DZEPHYR_SCA_VARIANT=clang
   :goals: build
   :compact:

.. note::

  默认生成 HTML 报告，也可以通过选项选择其他输出格式，如 sarif、plist、html。

配置 clang 静态分析器
*********************

可以通过专用选项控制 Clang 静态分析器。完整选项列表见 analyze-build 和 scan-build 的帮助。

.. code-block:: shell

    analyze-build --help

默认已启用的选项：

* --analyze-headers：同时分析通过 #include 包含的文件中的函数。

.. list-table::
   :header-rows: 1

   * - 参数
     - 描述
   * - ``CLANG_SCA_OPTS``
     - 以分号分隔的 analyze-build 选项列表。

这些参数可以通过命令行传递，也可以设置为环境变量。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: stm32h573i_dk
   :gen-args: -DZEPHYR_TOOLCHAIN_VARIANT=host/llvm -DLLVM_TOOLCHAIN_PATH=... -DZEPHYR_SCA_VARIANT=clang -DCLANG_SCA_OPTS="--sarif;--verbose"
   :goals: build
   :compact:
