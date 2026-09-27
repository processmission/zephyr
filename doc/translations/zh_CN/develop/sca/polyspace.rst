.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _polyspace:

Polyspace 支持
##############

`Polyspace® <https://mathworks.com/products/polyspace.html>`__ 是 MathWorks 的商业静态代码分析工具，经过最高安全等级使用场景认证。它可检查 MISRA C、CERT C 等编码指南符合性，发现 CWE 弱点和缺陷，并计算代码复杂度指标。还可选择运行形式化证明，验证不存在数组越界、溢出、竞态等运行时错误，从而帮助实现内存安全。

安装
****

必须安装 Polyspace 工具，并将其加入操作系统或容器的 PATH。具体而言，列表中必须包含 ``<polyspace_root>/polyspace/bin``。

安装说明见 `here <https://mathworks.com/help/bugfinder/install-polyspace.html>`__。要使用形式化验证，证明缺陷 *不存在*，还需安装 `this <https://mathworks.com/help/codeprover/install-polyspace.html>`__。

安装目录中必须有许可证文件。申请试用许可证，请访问 `this page <https://www.mathworks.com/campaigns/products/trials.html>`__。

运行
****

使用 ``west`` 构建时追加 ``-DZEPHYR_SCA_VARIANT=polyspace``，即可触发代码分析，例如：

.. code-block:: shell

   west build -b qemu_x86 samples/hello_world -- -DZEPHYR_SCA_VARIANT=polyspace

审查结果
********

构建结束时，控制台会汇总发现的问题，并输出详细结果所在目录。

为了高效审查，可在 `Polyspace user interface <https://mathworks.com/help/bugfinder/review-results-1.html>`__ 中打开该目录，或通过 `uploaded to the web interface <https://mathworks.com/help/bugfinder/gs/run-bug-finder-on-server.html>`__ 上传后审查。

为便于在 CI 流水线等场景中以程序读取结果，结果目录中的 CSV 文件也记录了各个问题。

配置
****

默认情况下，Polyspace 扫描所有 C/C++ 源码中的常见编程缺陷。可使用以下选项定制行为：

.. list-table::
   :widths: 20 40 30
   :header-rows: 1

   * - 选项
     - 作用
     - 示例
   * - ``POLYSPACE_ONLY_APP``
     - 设置后仅分析用户代码，忽略 Zephyr 源码。
     - ``-DPOLYSPACE_ONLY_APP=1``
   * - ``POLYSPACE_OPTIONS``
     - 提供额外命令行标志，例如选择编码规则。选项及其值以分号分隔。选项列表见 `here <https://mathworks.com/help/bugfinder/referencelist.html?type=analysisopt&s_tid=CRUX_topnav>`__。
     - ``-DPOLYSPACE_OPTIONS="-misra3;mandatory-required;-checkers;all"``
   * - ``POLYSPACE_OPTIONS_FILE``
     - 也可以在文本文件中逐行提供命令行标志，需指定文件绝对路径。
     - ``-DPOLYSPACE_OPTIONS_FILE=/workdir/zephyr/myoptions.txt``
   * - ``POLYSPACE_MODE``
     - 切换缺陷查找与证明模式，默认为缺陷查找。详情见 `here <https://mathworks.com/help/bugfinder/gs/use-bug-finder-and-code-prover.html>`__。
     - ``-DPOLYSPACE_MODE=prove``
   * - ``POLYSPACE_PROG_NAME``
     - 覆盖被分析应用的名称，默认由开发板名称和应用名称组成。
     - ``-DPOLYSPACE_PROG_NAME=myapp``
   * - ``POLYSPACE_PROG_VERSION``
     - 覆盖被分析应用的版本，默认取自 git-describe。
     - ``-DPOLYSPACE_PROG_VERSION=v1.0b-28f023``
