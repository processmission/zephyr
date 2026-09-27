.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _iwyu:

include-what-you-use（IWYU）支持
################################

`include-what-you-use <https://include-what-you-use.org/>`__ （IWYU）基于 Clang 和 LLVM，分析 C/C++ 源文件的 ``#include`` 指令。它针对每个翻译单元报告包含但未使用的头文件，以及虽被使用、但其定义头文件仅被间接包含的符号。采纳这些建议可使头文件包含关系保持精简、明确。

安装 include-what-you-use
*************************

大多数 Linux 发行版提供 ``include-what-you-use``，在 Ubuntu 上：

.. code-block:: shell

    sudo apt-get install iwyu

确保 :envvar:`PATH` 中可以找到 ``include-what-you-use`` 二进制文件。

运行 include-what-you-use
*************************

.. note::

   IWYU 基于 Clang，因此使用 LLVM 工具链构建能得到最准确的结果。

调用 :ref:`west build <west-building>` 时传入 ``-DZEPHYR_SCA_VARIANT=iwyu``，即可运行 include-what-you-use，例如：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: native_sim
   :gen-args: -DZEPHYR_SCA_VARIANT=iwyu
   :goals: build
   :compact:

分析随各源文件编译执行，建议的头文件包含修改会输出到构建输出的标准错误流。

配置 include-what-you-use
*************************

可以通过专用选项控制 include-what-you-use。完整列表见 `IWYU documentation <https://github.com/include-what-you-use/include-what-you-use/blob/master/README.md>`__。

.. list-table::
   :header-rows: 1

   * - 参数
     - 描述
   * - ``IWYU_OPTS``
     - 以分号分隔的 include-what-you-use 选项列表。每个选项都会自动加上所需的 ``-Xiwyu`` 前缀后传给工具。

这些参数可以通过命令行传递，也可以设置为环境变量。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: native_sim
   :gen-args: -DZEPHYR_SCA_VARIANT=iwyu -DIWYU_OPTS="--no_comments;--verbose=3"
   :goals: build
   :compact:
