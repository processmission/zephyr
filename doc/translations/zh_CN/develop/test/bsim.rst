.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bsim:

BabbleSim
#########

BabbleSim 与 Zephyr
*******************

Zephyr 项目使用 `Babblesim`_ 仿真器测试部分无线协议，包括低功耗蓝牙协议栈、802.15.4 和部分网络协议栈。

BabbleSim_ 是物理层仿真器，结合 Zephyr 的 :ref:`bsim 开发板<bsim boards>` 可仿真低功耗蓝牙和 15.4 设备网络。针对 :ref:`bsim 开发板<bsim boards>` 构建 Zephyr 时，会生成包含应用、Zephyr 操作系统和硬件模型的 Linux 可执行文件。

出现无线活动时，该 Linux 可执行文件会连接 BabbleSim Phy 仿真，以模拟无线信道。

如何获取和构建仿真器，参见 BabbleSim 文档中的 `get <https://babblesim.github.io/fetching.html>`_ 和 `build <https://babblesim.github.io/building.html>`_。:ref:`nrf52_bsim<nrf52_bsim>`、:ref:`nrf5340bsim<nrf5340bsim>` 和 :ref:`nrf54l15bsim<nrf54l15bsim>` 开发板文档介绍了针对这些板构建 Zephyr 的方法和示例。

测试类型
********

无无线活动的测试：通过 twister 运行 bsim 测试
=============================================

:ref:`bsim 开发板<bsim boards>` 可在无无线活动时使用，此时无需连接物理层仿真。因此，这些目标板可以像 :zephyr:board:`native_sim<native_sim>` 一样，配合 :ref:`twister <twister_script>` 运行全部标准 Zephyr twister 测试，同时使用真实 SoC 硬件的模型及驱动程序。

有无线活动的测试
================

存在无线活动时，BabbleSim 测试至少需要运行物理层仿真，多数还需要多个仿真设备。因此，每项测试通过专用脚本执行，脚本会按所需参数启动仿真设备、物理层可执行文件，以及可能需要的其他工具。

要通过 twister 运行它们，应使用 :ref:`bsim 测试适配器 <twister_bsim_harness>`。

这些测试存放在 :zephyr_file:`tests/bsim/` 目录中。

其构建和运行方式及遵循的约定，详见以下各节。

主要有两组测试：

* 自检嵌入式应用／测试：部分仿真设备应用内置检查逻辑，决定测试通过或失败。这些测试使用 :ref:`bs_tests<bsim_boards_bs_tests>` 系统报告结果，并常将多个测试构建到同一二进制文件中。

* 使用 EDTT_ 工具的测试：EDTT（Python）测试通过 RPC 机制控制嵌入式应用，并判定测试结果。目前这些测试包含蓝牙认证测试套件的相当大一部分。

各类测试与 BabbleSim 及 bsim 开发板的关系，详见 :ref:`bsim 开发板测试章节<bsim_boards_tests>`。

测试覆盖率与 BabbleSim
**********************

由于 :ref:`bsim 开发板 <bsim boards>` 基于 POSIX 架构，因此很容易收集测试覆盖率信息。

详情参见 :ref:`覆盖率生成页面 <coverage_posix>`。只需向 twister 传入 ``--coverage``，即可自动启用 :kconfig:option:`CONFIG_COVERAGE` 构建并生成覆盖率报告。

.. _BabbleSim:
   https://BabbleSim.github.io

.. _EDTT:
   https://github.com/EDTTool/EDTT

构建和运行测试
**************

仿真器配置方法参见 :ref:`nrf52_bsim <nrf52bsim_build_and_run>` 页面。

可使用 :ref:`twister <twister_script>` 构建并运行这些测试。多设备测试需要传入 ``--fixture bsim_multi_test`` 选项。

例如，在 ${ZEPHYR_BASE} 中，可用以下命令构建并运行一个蓝牙测试：

.. code-block:: bash

   twister -p nrf52_bsim/native -T tests/bsim/bluetooth/host/adv/chain/ --fixture bsim_multi_test

若测试二进制文件已构建，也可直接通过对应测试脚本运行，例如：

.. code-block:: bash

   BOARD=nrf52_bsim/native tests/bsim/bluetooth/host/adv/chain/tests_scripts/adv_chain.sh

调试或修复问题时，``-n, --no-clean``、``--aggressive-no-clean`` 或 ``-b, --build-only`` 等 :ref:`Twister 命令行选项 <twister_commandline_options>` 可能很有用。

旧版批处理脚本
==============

在加入 twister bsim 适配器之前，多设备 bsim 测试依赖 :zephyr_file:`tests/bsim/` 中的 ``compile.sh`` 和 ``run_parallel.sh`` 构建和运行。CI 使用这些脚本构建所需镜像并批量执行测试，用户也可借助它们构建和执行自己的测试。这些脚本仍可使用，但建议迁移到 :ref:`twister <twister_script>` 和 ``tests.yaml`` 定义。

这些脚本要求设置一些环境变量。例如，在 Zephyr 根目录可运行：

.. code-block:: bash

   # Build all the tests
   ${ZEPHYR_BASE}/tests/bsim/compile.sh

   # Run them (in parallel)
   RESULTS_FILE=${ZEPHYR_BASE}/myresults.xml \
      SEARCH_PATH=${ZEPHYR_BASE}/tests/bsim \
         ${ZEPHYR_BASE}/tests/bsim/run_parallel.sh

若只构建和运行特定子集，例如主机广播测试：

.. code-block:: bash

   # Build the Bluetooth host advertising tests
   ${ZEPHYR_BASE}/tests/bsim/bluetooth/host/adv/compile.sh

   # Run them (in parallel)
   RESULTS_FILE=${ZEPHYR_BASE}/myresults.xml \
      SEARCH_PATH=${ZEPHYR_BASE}/tests/bsim/bluetooth/host/adv \
         ${ZEPHYR_BASE}/tests/bsim/run_parallel.sh

更多批量运行选项和示例，参见 ``run_parallel.sh`` 帮助。

构建测试所需的二进制文件后，可以直接运行对应的测试脚本。

例如，可用以下命令构建网络测试所需二进制文件：

.. code-block:: bash

   WORK_DIR=${ZEPHYR_BASE}/bsim_out ${ZEPHYR_BASE}/tests/bsim/net/compile.sh

然后直接运行其中一个测试：

.. code-block:: bash

   ${ZEPHYR_BASE}/tests/bsim/net/sockets/echo_test/tests_scripts/echo_test_802154.sh

约定
====

测试代码
--------

测试代码约定参见 :zephyr_file:`蓝牙测试示例 <tests/bsim/bluetooth/host/misc/sample_test/README.rst>`。

测试脚本
--------

请遵循现有约定，不要设计一次性的专用运行器，例如 Python 脚本或另一层 shell 抽象。

统一测试运行方式、变量等，可以让维护者更方便快捷地为构建系统或兼容性变更更新整个代码树。

如果有改进测试脚本的好主意，请提交修改 *所有* 测试脚本的 PR，让所有人受益并保持一致。也可以先在 RFC 问题或 babblesim Discord 频道讨论。

以下划线（``_``）开头的脚本不会被自动发现和运行。它们可为主脚本提供辅助函数，也可作为本地开发工具，例如本地构建、运行测试和调试。

约定如下：

- 每项测试由 ``tests_scripts/`` 子目录中扩展名为 ``.sh`` 的 shell 脚本定义。
- 建议每个脚本文件运行一项测试，以便 CI 更好地并行运行。
- 脚本假定所需二进制文件已经构建，不应自行编译。
- 脚本启动每个仿真设备及物理层仿真的进程。
- 测试通过时脚本必须向调用 shell 返回 0，失败时返回非零值。
- 每项测试必须具有唯一仿真 ID，以便并行运行不同测试。
- 脚本和镜像均不得修改 ``${BSIM_OUT_PATH}/results/<simulation_id>/`` 或 ``/tmp/`` 之外的工作站文件系统内容，即不应留下散落文件。
- 需要多个连续仿真的测试，例如模拟设备配对、断电，再以新仿真启动，应为每段仿真使用不同 ID，确保之后可检查各段的无线活动。
- 避免过长的测试。若运行超过 20 秒，应考虑能否拆分为多个独立测试。
- 若测试超过 5 秒，将 ``EXECUTE_TIMEOUT`` 设为至少是实测运行时间 5 倍的值。
- 不要将 ``EXECUTE_TIMEOUT`` 设得低于默认值。
- 测试输出不应过于冗长，预计应少于一百行。可广泛使用 ``LOG_DBG()``，但不要默认启用 ``DBG`` 日志级别。
- 使用物理层仿真的测试脚本，应将收到的额外参数直接传给 Phy 可执行文件。例如，用于让 Phy 在检查模式（``-c``）下运行，验证本次与上次仿真产生完全相同的无线流量。
