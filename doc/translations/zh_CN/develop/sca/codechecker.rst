.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _codechecker:

CodeChecker 支持
################

`CodeChecker <https://codechecker.readthedocs.io/>`__ 是静态分析基础设施，会运行构建系统上可用的分析工具，例如 `Clang-Tidy <https://clang.llvm.org/extra/clang-tidy/>`__、`Clang Static Analyzer <https://clang-analyzer.llvm.org/>`__ 和 `Cppcheck <https://cppcheck.sourceforge.io/>`__。安装方法参见各分析器的网站。

安装 CodeChecker
****************

CodeChecker 本身是 Python 包，可从 `pypi <https://pypi.org/project/codechecker/>`__ 获取。

.. code-block:: shell

    pip install codechecker

使用 CodeChecker 构建
*********************

运行 CodeChecker 时，调用 :ref:`west build <west-building>` 并传入 ``-DZEPHYR_SCA_VARIANT=codechecker``，例如：

.. code-block:: shell

    west build -b mimxrt1064_evk samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=codechecker


配置 CodeChecker
****************

CodeChecker 使用多个命令步骤，每个步骤都有自己的配置参数，下表列出全部选项。

.. list-table::
   :header-rows: 1

   * - 参数
     - 描述
   * - ``CODECHECKER_ANALYZE_JOBS``
     - 分析使用的线程数。（默认值：<CPU count>）
   * - ``CODECHECKER_ANALYZE_OPTS``
     - 直接传给 ``analyze`` 命令的参数，例如 ``--timeout;360``。
   * - ``CODECHECKER_CLEANUP``
     - 解析或存储后执行清理，删除所有 ``plist`` 文件。
   * - ``CODECHECKER_CONFIG_FILE``
     - 包含配置选项的 JSON 或 YAML 文件，传给所有命令。
   * - ``CODECHECKER_EXPORT``
     - 以逗号分隔的报告类型列表。允许的类型为 ``html,json,codeclimate,gerrit,baseline``。
   * - ``CODECHECKER_NAME``
     - CodeChecker 运行元数据名称，默认为 ``zephyr``。
   * - ``CODECHECKER_PARSE_EXIT_STATUS``
     - 默认情况下，CodeChecker 发现问题不会使构建失败。设置此选项可使分析阶段失败。
   * - ``CODECHECKER_PARSE_OPTS``
     - 直接传给 ``parse`` 命令的参数，例如 ``--verbose;debug``。
   * - ``CODECHECKER_PARSE_SKIP``
     - 跳过分析结果解析，适用于只需存储结果的情况。
   * - ``CODECHECKER_STORE``
     - 分析后运行 ``store`` 命令。
   * - ``CODECHECKER_STORE_OPTS``
     - 直接传给 ``store`` 命令的参数，隐含启用 ``CODECHECKER_STORE``，例如 ``--url;localhost:8001/Default``。
   * - ``CODECHECKER_STORE_TAG``
     - 向 ``store`` 命令传递 ``--tag`` 标识符。
   * - ``CODECHECKER_TRIM_PATH_PREFIX``
     - 从分析结果中移除指定路径前缀，例如 ``/home/user/zephyrproject``。默认加入 ``west topdir`` 的值。

这些参数可以通过命令行传递，也可以设置为环境变量。


配合 CodeChecker 运行 twister
*****************************

通过 ``twister`` 运行 CodeChecker 时，会设置以下默认选项：

.. list-table::
   :header-rows: 1

   * - 参数
     - 值
   * - ``CODECHECKER_ANALYZE_JOBS``
     - ``1``
   * - ``CODECHECKER_NAME``
     - ``<board target>:<testsuite name>``
   * - ``CODECHECKER_STORE_TAG``
     - 应用源码目录中 ``git describe`` 的输出值。

设置环境变量或将其作为额外参数传入，即可覆盖这些值。
