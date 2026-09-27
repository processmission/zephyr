.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _eclair:

ECLAIR 支持
###########

Bugseng 的 `ECLAIR <https://www.bugseng.com/eclair/>`__ 是经过认证的静态分析工具及软件验证平台。用途包括编码规则验证（尤其是 MISRA 和 BARR-C）、软件度量计算、检查软件组件的独立性和免受干扰能力，以及自动检测重要类别的软件错误。

前置条件
********

必须安装 ECLAIR 工具，并将其加入操作系统 PATH 变量。

可以运行以下命令验证安装：

.. code-block:: shell

   eclair -version

使用 ECLAIR 需要有效许可证或试用许可证。申请试用请访问 `this page <https://www.bugseng.com/eclair/free-trial>`__。

运行 ECLAIR
***********

调用 :ref:`west build <west-building>` 时传入 ``-DZEPHYR_SCA_VARIANT=eclair``，即可运行 ECLAIR。

.. code-block:: shell

    west build -b mimxrt1064_evk samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=eclair

.. note::
   这只会使用预定义规则集 ``first_analysis`` 进行分析。如需其他规则集，必须提供配置文件，详情见下一节。

配置
****

可以通过 CMake 选项文件，或通过命令行传递调整后的选项，配置 ECLAIR 静态分析环境。

定义 ``ECLAIR_OPTIONS_FILE`` 变量，即可在 ECLAIR 调用中使用 CMake 选项文件，例如：

.. code-block:: shell

    west build -b mimxrt1064_evk samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=eclair -DECLAIR_OPTIONS_FILE=my_options.cmake

未提供配置文件时，默认配置始终为 ``first_analysis``，仅选用少量规则，以验证一切正常工作。

如果希望通过命令行而非选项文件覆盖默认配置，可以传入 ``-DOption=ON|OFF``。

例如：

.. code-block:: shell

    west build -b mimxrt1064_evk samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=eclair -DECLAIR_REPORTS_SARIF=ON

Zephyr 是大型复杂项目，因此将其编码指南（来自 https://docs.zephyrproject.org/latest/contribute/coding_guidelines/index.html）划分为五组配置，便于在个人机器上使用：

* first_analysis（默认）：选取少量项目编码指南，验证一切正常工作。

* STU：通过独立分析各翻译单元即可验证的项目编码指南。

* STU_heavy：较复杂、需要较长时间的 STU 编码指南。

* WP：所有涉及整个程序的编码指南，MISRA 称之为 system。

* std_lib：涉及 C 标准库的项目编码指南。

此外，zephyr_guidelines 规则集包含 `Coding Guidelines <https://docs.zephyrproject.org/latest/contribute/coding_guidelines/index.html>`__ 中列出的所有主要规则。

相关 CMake 选项：

* ``ECLAIR_RULESET_FIRST_ANALYSIS``
* ``ECLAIR_RULESET_STU``
* ``ECLAIR_RULESET_STU_HEAVY``
* ``ECLAIR_RULESET_WP``
* ``ECLAIR_RULESET_STD_LIB``
* ``ECLAIR_RULESET_ZEPHYR_GUIDELINES``

用户定义的规则集
================

要使用自定义规则集代替预定义 Zephyr 编码指南规则集，可设置 :code:`ECLAIR_RULESET_USER=ON`。按 ``analysis_<RULESET>.ecl`` 格式创建 ECLAIR 规则集文件，再通过 CMake 变量 :code:`ECLAIR_USER_RULESET_NAME` 指定规则集名称。如果文件不在应用源码目录，可通过 :code:`ECLAIR_USER_RULESET_PATH` 指定路径，支持相对路径和绝对路径。

相关 CMake 选项和变量：

* ``ECLAIR_RULESET_USER``
* ``ECLAIR_USER_RULESET_NAME``
* ``ECLAIR_USER_RULESET_PATH``

生成其他格式的报告
******************

除默认 ecd 文件外，ECLAIR 还可生成 DOC、ODT、XLSX 等格式及不同类型的报告，包括：

* 电子表格格式的度量数据。

* 电子表格格式的问题报告。

* SARIF 格式的问题报告。

* 纯文本格式的摘要报告。

* DOC 格式的摘要报告。

* ODT 格式的摘要报告。

* HTML 格式的摘要报告。

* txt 格式的详细报告。

* DOC 格式的详细报告。

* ODT 格式的详细报告。

* HTML 格式的详细报告。

相关 CMake 选项：

* ``ECLAIR_METRICS_TAB``
* ``ECLAIR_REPORTS_TAB``
* ``ECLAIR_REPORTS_SARIF``
* ``ECLAIR_SUMMARY_TXT``
* ``ECLAIR_SUMMARY_DOC``
* ``ECLAIR_SUMMARY_ODT``
* ``ECLAIR_SUMMARY_HTML``
* ``ECLAIR_FULL_TXT``
* ``ECLAIR_FULL_DOC``
* ``ECLAIR_FULL_ODT``
* ``ECLAIR_FULL_HTML``

完整报告的详细程度
==================

txt 和 doc 完整报告的详细程度也可通过配置调整，可用配置如下：

* 显示所有区域

* 仅显示第一个区域

相关 CMake 选项：

* ``ECLAIR_FULL_DOC_ALL_AREAS``
* ``ECLAIR_FULL_DOC_FIRST_AREA``
* ``ECLAIR_FULL_TXT_ALL_AREAS``
* ``ECLAIR_FULL_TXT_FIRST_AREA``
