.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _coverage:

生成覆盖率报告
##############

Zephyr 可以生成代码覆盖率报告，分析指定测试或应用覆盖了哪些代码。

有两种方式：

* 在真实嵌入式目标或 QEMU 中使用 Zephyr 集成的 gcov
* 针对 POSIX 架构编译应用，直接在主机上运行

嵌入式设备或 QEMU 中的测试覆盖率报告
************************************

概述
====
`GCC GCOV <gcov_>`_ 是与 GCC 编译器配合使用的测试覆盖率程序，可分析程序并创建覆盖率报告，帮助编写更高效、更快速的代码，发现未经测试的代码路径。

在 Zephyr 中，gcov 在应用运行时将覆盖率分析数据收集到 RAM 而非文件系统。收集和报告能力受可用 RAM 限制，因此目前仅在嵌入式目标的 QEMU 仿真中启用。

详情
====
启用此功能分两步：先为设备启用覆盖率，再为测试应用启用。前述 gcov 覆盖率受可用 RAM 影响，因此启用时必须确保设备有足够 RAM。例如 frdm_k64f 等小型设备可运行简单测试应用，但启用覆盖率后，更复杂且耗用更多 RAM 的测试可能崩溃。

为设备启用覆盖率时，在 Kconfig.board 中选择 :kconfig:option:`CONFIG_HAS_COVERAGE_SUPPORT`。

要报告特定测试应用的覆盖率，设置 :kconfig:option:`CONFIG_COVERAGE`。

生成代码覆盖率报告的步骤
========================

以下步骤为单个应用生成 HTML 覆盖率报告。

1. 使用 CONFIG_COVERAGE=y 构建代码。

   .. zephyr-app-commands::
      :board: mps2/an385
      :gen-args: -DCONFIG_COVERAGE=y -DCONFIG_COVERAGE_DUMP=y
      :goals: build
      :compact:

#. 将仿真器输出保存到日志文件。覆盖率转储打印完毕后，可能需要用 :kbd:`Ctrl-A X` 终止仿真器，才能完成此步骤：

   .. code-block:: console

     $ ninja -Cbuild run | tee log.log

#. 从保存的日志生成 gcov ``.gcda`` 和 ``.gcno`` 文件：

   .. code-block:: console

     $ python3 scripts/gen_gcov_files.py -i log.log

#. 找到 SDK 中的 gcov 可执行文件。稍后调用 ``gcovr`` 时，需要传入对应架构的 gcov 路径：

   .. code-block:: console

     $ find $ZEPHYR_SDK_INSTALL_DIR -iregex ".*gcov"

#. 创建报告输出目录：

   .. code-block:: console

     $ mkdir -p coverage-report

#. 运行 ``gcovr`` 获取报告：

   .. code-block:: console

     $ gcovr -r $ZEPHYR_BASE . --html -o coverage-report/coverage.html --html-details --gcov-executable <gcov_path_in_SDK>

   .. _coverage_posix:

使用 POSIX 架构的覆盖率报告
***************************

针对 POSIX 架构编译时，使用主机原生工具生成包含应用、Zephyr 操作系统和基本硬件仿真的原生可执行文件。

因此可以使用开发其他桌面应用时的相同工具。

要为应用启用 ``gcc`` 的 `gcov`_，只需在编译前设置 :kconfig:option:`CONFIG_COVERAGE`。运行应用时，``gcov`` 覆盖率数据会转储到相应的 ``gcda`` 和 ``gcno`` 文件，可用偏好的工具后处理。例如：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :gen-args: -DCONFIG_COVERAGE=y
   :host-os: unix
   :board: native_sim
   :goals: build
   :compact:

.. code-block:: console

   $ ./build/zephyr/zephyr.exe
   # Press Ctrl+C to exit
   $ lcov --capture --directory ./ --output-file lcov.info -q --rc lcov_branch_coverage=1
   $ genhtml lcov.info --output-directory lcov_html -q --ignore-errors source --branch-coverage --highlight --legend

.. note::

   需要支持中间文本格式的较新 lcov，至少为 1.14。较新的 Linux 发行版提供相应软件包。

   也可使用至少 4.2 版本的 gcovr。

使用 Twister 生成覆盖率报告
***************************

Zephyr 的 :ref:`twister 脚本 <twister_script>` 可根据已执行测试自动生成覆盖率报告，只需传入 ``--coverage`` 命令行选项。

例如，可运行：

.. code-block:: console

    $ west twister --coverage -p qemu_x86 -T tests/kernel

或：

.. code-block:: console

    $ west twister --coverage -p native_sim -T tests/bluetooth

这会生成 ``twister-out/coverage/index.html`` 报告，并将 ``gcovr`` 工具收集的覆盖率数据保存为 ``twister-out/coverage.json``。

可通过 ``--coverage-tool`` 和 ``--coverage-formats`` 命令行选项选择其他报告。

要生成同时包含 Zephyr 源代码和仓库之外应用代码（见 :ref:`应用类型 <zephyr-app-types>`）的报告，应从项目目录调用 Twister，并传入 ``--coverage-basedir $ZEPHYR_BASE``，例如：

.. code-block:: console

   $ west twister --coverage -p native_sim --coverage-basedir $ZEPHYR_BASE -T your_project_dir

.. note::

   默认情况下，Twister 调用 ``gcovr``。该工具过滤源文件时假定所有路径均为真实路径，即 `all symlinks resolved <gcovr_symlinks_>`_。如果开发环境的目录带符号链接，为避免 ``gcovr`` 报告不完整，应确保 :ref:`ZEPHYR_BASE <important-build-vars>` 为真实路径；或者用 ``lcov`` 代替 ``gcovr``，添加 Twister 选项 ``--coverage-tool lcov``。

单元测试使用主机工具链构建，并需要不同的开发板，因此流程有所不同：

.. code-block:: console

   $ west twister --coverage -p unit_testing -T tests/unit

报告生成位置与非单元测试相同。

逐测试覆盖率矩阵
================

默认按测试场景汇总覆盖率。若要归因到各个 :ref:`Ztest <test-framework>` 测试用例，例如回答“哪些测试执行了 ``foo.c`` 的第 X 行”，请传入 ``--coverage-per-test``：

.. code-block:: console

   $ west twister -p mps2/an385 -T tests/kernel --coverage --coverage-tool lcov \
       --coverage-per-test

这会启用 :kconfig:option:`CONFIG_ZTEST_COVERAGE_PER_TEST`，在每个用例前重置 gcov 计数器，并在其结束后转储独立且带测试标记的覆盖率产物。支持半主机模式的平台，例如 QEMU 下的 ARM、RISC-V 和 Xtensa 目标 ``mps2/an385``，会将逐测试数据直接写入主机文件系统，避免大量串行控制台流量；其他平台则退回串行控制台传输。

除常规汇总报告外，还会生成：

* 每个测试一个 ``<scenario>.<test>.info`` 跟踪文件，位于各构建的 ``coverage/tests/`` 目录；以及
* ``twister-out/coverage/test_matrix.json``，机器可读的矩阵，包含 ``by_line`` 视图（``{file: {line: [tests]}}``）和 ``by_test`` 视图（``{test: {file: [lines]}}``）。

逐测试归因由矩阵及其仪表盘提供，而非汇总的 lcov 报告。每个实例的覆盖率会先合并为一个跟踪文件再汇总，因此最终报告的处理规模随实例数而非测试用例总数增长。

.. note::

   ``--coverage-per-test`` 需要 ``lcov`` 工具，因为矩阵依赖 lcov 跟踪文件中的逐测试 ``TN`` 记录，``gcovr`` 没有等效功能。此选项也隐含启用 ``--coverage``。

可视化矩阵
----------

可通过独立脚本 :zephyr_file:`scripts/gen_test_matrix_dashboard.py`，将 ``test_matrix.json`` 转换为自包含的交互式 HTML 仪表盘。该脚本不依赖 Twister，也可处理此前生成的任意矩阵：

.. code-block:: console

   $ scripts/gen_test_matrix_dashboard.py -i twister-out/coverage/test_matrix.json

这会写入 ``twister-out/coverage/test_matrix.html``，逐项列出每个测试覆盖的文件数、行数以及 *独占* 覆盖的行数（即其他测试未触及的行，有助于识别冗余测试或承担关键覆盖的测试）。还可深入查看测试覆盖的文件，或查询某文件某行由哪些测试覆盖。

.. _gcovr_symlinks:
   https://github.com/gcovr/gcovr/blob/main/doc/source/guide/filters.rst#filters-for-symlinks

.. _gcov:
   https://gcc.gnu.org/onlinedocs/gcc/Gcov.html

使用不同工具链
==============

Twister 根据环境变量 ``ZEPHYR_TOOLCHAIN_VARIANT`` 决定默认使用哪个 gcov 工具。``--gcov-tool`` 参数的默认值如下：

+-------------+-------------------------+
| 工具链      | ``--gcov-tool`` 的值    |
+-------------+-------------------------+
| host        | ``gcov``                |
+-------------+-------------------------+
| llvm        | ``llvm-cov gcov``       |
+-------------+-------------------------+
| zephyr      | ``gcov``                |
+-------------+-------------------------+
