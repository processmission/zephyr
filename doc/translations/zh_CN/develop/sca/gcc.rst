.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _gcc:

GCC 静态分析支持
################

`GCC <https://gcc.gnu.org/>`__ 10 引入静态分析，通过 ``-fanalyzer`` 启用。与传统警告相比，它执行的代码分析更全面，开销也更高。

运行 GCC 静态分析
*****************

调用 :ref:`west build <west-building>` 时传入 ``-DZEPHYR_SCA_VARIANT=gcc``，即可运行 GCC 静态分析，例如：

.. zephyr-app-commands::
   :zephyr-app: samples/userspace/hello_world_user
   :board: qemu_x86
   :gen-args: -DZEPHYR_SCA_VARIANT=gcc
   :goals: build
   :compact:

配置 GCC 静态分析器
*******************

可以通过专用选项控制 GCC 静态分析器。

* `Options controlling the analyzer <https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html>`__ （分析器控制选项）
* `Options controlling the diagnostic message formatting <https://gcc.gnu.org/onlinedocs/gcc/Diagnostic-Message-Formatting-Options.html>`__ （诊断消息格式选项）

.. list-table::
   :header-rows: 1

   * - 参数
     - 描述
   * - ``GCC_SCA_OPTS``
     - 以分号分隔的 GCC 分析器选项列表。

这些参数可以通过命令行传递，也可以设置为环境变量。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: stm32h573i_dk
   :gen-args: -DZEPHYR_SCA_VARIANT=gcc -DGCC_SCA_OPTS="-fdiagnostics-format=json;-fanalyzer-verbosity=3"
   :goals: build
   :compact:

.. note::

   GCC 静态分析器仍在积极开发，每个新版本都会增加选项。此 `page <https://gcc.gnu.org/wiki/StaticAnalyzer>`__ 概述各版本新增的选项和修复。


最新分析器版本
**************

Zephyr 工具链可能未包含最新版 GCC 静态分析器，因此可以使用更新的 `GNU Arm embedded toolchain <https://docs.zephyrproject.org/latest/develop/toolchains/gnu_arm_embedded.html>`__ 运行分析，以利用最新版分析器。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: stm32h573i_dk
   :gen-args: -DZEPHYR_SCA_VARIANT=gcc -DZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb -DGNUARMEMB_TOOLCHAIN_PATH=...
   :goals: build
   :compact:
