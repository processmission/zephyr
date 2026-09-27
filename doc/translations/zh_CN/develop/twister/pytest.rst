.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _integration_with_pytest:

与 pytest 测试框架集成
######################

*请注意，Twister 与 pytest 的集成仍在开发中，尚不支持所有平台类型。如果发现问题或有改进建议，请创建 GitHub 问题或增强请求。*

简介
****

Pytest 是 Python 框架，*使小型、易读的测试易于编写，也能扩展以支持应用和库的复杂功能测试* （参见 `pytest 文档 <https://docs.pytest.org/en/7.3.x/>`_）。Python 拥有丰富的免费库，也便于编写脚本。pytest 通过插件和 fixture 提升扩展性及复用性。``pytest-twister-harness`` 插件将 pytest 与 Twister 集成，使 Zephyr 社区在保留 Twister 为主框架的同时使用 pytest 功能。

与 Twister 集成
***************

默认无需额外操作即可在 Twister 中使用 pytest。插件在 Zephyr 代码树内开发；为实现免安装运行，Twister 先将插件路径加入 ``PYTHONPATH``，再在 pytest 命令中添加 ``-p twister_harness.plugin``。若希望使用已安装版本，应给 Twister 添加 ``--allow-installed-plugin``。

基于 pytest 的套件与其他测试一样，通过 tests.yaml 文件发现。其中 ``harness`` 键决定 Twister 如何处理测试。使用 ``harness: pytest`` 时，套件发现、并行化、构建和报告等流程保持不变，仅执行阶段不同。下图展示集成的简化概览。

.. figure:: figures/twister_and_pytest.svg
   :figclass: align-center


使用 ``harness: pytest`` 时，Twister 以子进程调用 pytest，将测试执行交给它。构建目录、设备等参数通过 YAML 配置传入。pytest 完成后，Twister 查找其报告 results.xml，并据此设置测试结果。

如何创建 pytest 测试
********************

包含 pytest 测试、应用源代码和 Twister YAML 配置的目录示例如下：

.. code-block:: none

   test_foo/
   ├─── pytest/
   │    └─── test_foo.py
   ├─── src/
   │    └─── main.c
   ├─── CMakeList.txt
   ├─── prj.conf
   └─── testcase.yaml

pytest 测试示例见 :zephyr_file:`samples/subsys/testsuite/pytest/shell/pytest/test_shell.py`。Twister 根据 ``testcase.yaml`` 配置构建 ``src`` 中的应用；若 YAML 中有 ``harness: pytest``，则在独立子进程调用 pytest。配置示例如下：

.. code-block:: yaml

   tests:
      some.foo.test:
         harness: pytest
         tags: foo

默认在与二进制源代码目录同级的 ``pytest`` 目录查找测试。可用 YAML 的 ``harness_config`` 下的 ``pytest_root`` 指向其他文件、目录或子测试，详见 :ref:`此处 <pytest_root>`。

pytest 按默认的 `discovery rules <https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#conventions-for-python-test-discovery>`_ 扫描指定位置查找测试。

传入附加参数
============

有两种方式向 pytest 子进程传入附加参数：

#. 在 YAML 的 ``harness_config`` 下使用 ``pytest_args``，详见 :ref:`此处 <pytest_args>`。
#. 通过 Twister 命令行的 ``--pytest-args`` 参数。这尤其适合从套件中选择特定用例，例如：

   .. code-block:: console

      $ west twister --platform native_sim -T samples/subsys/testsuite/pytest/shell \
      -s samples/subsys/testsuite/pytest/shell/sample.pytest.shell \
      --pytest-args='-k test_shell_print_version'

   命令行参数会补充 YAML 参数。同一参数同时出现在两处时，命令行优先。

Fixture
*******

dut
===

提供代表被测设备的 `DeviceAdapter`_ 对象，是 pytest 适配器插件的核心 fixture。启动 DUT，包括初始化日志、烧录和连接串口等，均需要它。它按请求类型（``native``、``qemu``、``hardware`` 等）返回准备好的设备。所有设备共享相同 API，便于编写不依赖设备类型的测试。作用域由 ``harness_config`` 下的 ``pytest_dut_scope`` 决定，详见 :ref:`此处 <pytest_dut_scope>`。


.. code-block:: python

   from twister_harness import DeviceAdapter

   def test_sample(dut: DeviceAdapter):
      dut.readlines_until(regex='Hello world')

shell
=====

提供 `Shell <shell_class_>`_ 对象及与 shell 应用交互的方法。它调用 ``wait_for_promt``，等待 DUT 就绪后才开始场景。shell fixture 调用 ``dut``，因此可使用其全部方法。``shell`` 还添加针对 shell 交互优化的方法，可代替 ``dut`` 用于测试。作用域由 ``harness_config`` 下的 ``pytest_dut_scope`` 决定，详见 :ref:`此处 <pytest_dut_scope>`。

.. code-block:: python

   from twister_harness import Shell

   def test_shell(shell: Shell):
      shell.exec_command('help')

mcumgr
======

封装远程设备管理命令行工具 ``mcumgr`` 的示例 fixture。MCUmgr 详情见 :ref:`mcu_mgr`。

.. note::
   此 fixture 要求系统 PATH 中可找到 ``mcumgr``。

此 fixture 仅封装 MCUmgr 的部分功能。使用 ``mcumgr`` fixture 的测试示例如下：

.. code-block:: python

   from twister_harness import DeviceAdapter, Shell, McuMgr

   def test_upgrade(dut: DeviceAdapter, shell: Shell, mcumgr: McuMgr):
      # free the serial port for mcumgr
      dut.disconnect()
      # upload the signed image
      mcumgr.image_upload('path/to/zephyr.signed.bin')
      # obtain the hash of uploaded image from the device
      second_hash = mcumgr.get_hash_to_test()
      # test a new upgrade image
      mcumgr.image_test(second_hash)
      # reset the device remotely
      mcumgr.reset_device()
      # continue test scenario, check version etc.


unlaunched_dut
==============

类似 ``dut``，但不初始化设备。需要更细致地控制构建过程时可使用它，初始化设备由测试负责。

.. code-block:: python

   from twister_harness import DeviceAdapter

   def test_sample(unlaunched_dut: DeviceAdapter):
      unlaunched_dut.launch()
      unlaunched_dut.readlines_until(regex='Hello world')

多 DUT 场景的 fixture
*********************

多 DUT fixture 对应单 DUT 的 ``unlaunched_dut``、``dut``、``shell``，但操作设备列表。支持硬件和 ``native_sim``，不支持 QEMU。要求 ``twister_pytest_config.yaml`` 包含 ``duts`` 条目。Twister 自动生成此文件并调用 pytest；仿真目标会自动创建占位 DUT，无需硬件映射。不通过 Twister 手动重跑 pytest 时复用同一配置，见常见问题。配置详情见 :ref:`twister_multi_duts_testing`。

unlaunched_duts
===============

类似 ``unlaunched_dut``，但返回 `DeviceAdapter`_ 对象列表，每个预留 DUT 一个，日志文件已初始化，设备尚未启动。

.. code-block:: python

   from twister_harness import DeviceAdapter

   def test_sample(unlaunched_duts: list[DeviceAdapter]):
      for dut in unlaunched_duts:
         dut.launch()
      unlaunched_duts[0].readlines_until(regex='Hello world')

duts
====

类似 ``dut``，但返回已启动的 `DeviceAdapter`_ 对象列表。所有设备并行烧录以缩短准备时间。若需顺序烧录，在 ``conftest.py`` 中覆盖此 fixture。

.. code-block:: python

   from twister_harness import DeviceAdapter

   def test_sample(duts: list[DeviceAdapter]):
      assert len(duts) > 1
      duts[0].readlines_until(regex='Hello world')
      duts[1].readlines_until(regex='Hello world')

shells
======

类似 ``shell``，但返回 `Shell <shell_class_>`_ 对象列表，每个预留 DUT 一个，均已等待 shell 提示符。

.. code-block:: python

   from twister_harness import Shell

   def test_sample(shells: list[Shell]):
      assert len(shells) > 1
      shells[0].exec_command('help')
      shells[1].exec_command('help')


类
***

DeviceAdapter
=============

.. autoclass:: twister_harness.DeviceAdapter

   .. automethod:: launch

   .. automethod:: close

   .. automethod:: readline

   .. automethod:: readlines

   .. automethod:: readlines_until

   .. automethod:: write

.. _shell_class:

Shell
=====

.. autoclass:: twister_harness.Shell

   .. automethod:: exec_command

   .. automethod:: wait_for_prompt

   .. automethod:: get_filtered_output


Zephyr 项目中的 pytest 测试示例
*******************************

* :zephyr:code-sample:`pytest_shell`
* MCUmgr 测试：:zephyr_file:`tests/boot/with_mcumgr`
* LwM2M 测试：:zephyr_file:`tests/net/lib/lwm2m/interop`
* GDB 桩测试：:zephyr_file:`tests/subsys/debug/gdbstub`


常见问题
********

如何在每次 pytest 会话中只烧录／运行一次应用？
==============================================

   ``dut`` fixture 负责烧录和运行应用，默认作用域为 ``function``。可在 YAML 的 ``harness_config`` 下添加 ``pytest_dut_scope`` 更改：

   .. code-block:: yaml

      harness: pytest
      harness_config:
         pytest_dut_scope: session

   更多信息见 :ref:`此处 <pytest_dut_scope>`。

如何仅运行 Python 文件中的某一测试？
====================================

   有多种方式。可在 YAML 的 ``harness_config`` 下添加 ``pytest_root``，列出要运行的测试：

   .. code-block:: yaml

      harness: pytest
      harness_config:
         pytest_root:
            - "pytest/test_shell.py::test_shell_print_help"

   也可使用 pytest 的 ``-k`` 选项选择测试，关键字过滤详情见 `here <https://docs.pytest.org/en/latest/example/markers.html#using-k-expr-to-select-tests-based-on-their-name>`_。在 YAML 的 ``pytest_args`` 中添加 ``-k`` 过滤条件即可：

   .. code-block:: yaml

      harness: pytest
      harness_config:
         pytest_args:
            - "-k test_shell_print_help"

   或将其加入 Twister 命令，覆盖 YAML 参数：

   .. code-block:: console

      $ west twister ... --pytest-args='-k test_shell_print_help'

如何在测试中获取所用设备类型？
==============================

   可从代表 `DeviceAdapter`_ 对象的 ``dut`` fixture 获取：

   .. code-block:: python

      device_type: str = dut.device_config.type
      if device_type == 'hardware':
         ...
      elif device_type == 'native':
         ...

如何在本地重跑 pytest 测试，而不让 Twister 重新构建应用？
=========================================================

   再次运行 Twister 并添加 ``--test-only`` 即可。也可用最高详细级别 ``-vv`` 运行 Twister，再从以 ``Running pytest command: ...`` 开头的日志中复制启动 pytest 的命令。

   首先通过 Twister 运行场景：

   .. code-block:: console

      $ west twister -vv -ll debug -T samples/subsys/testsuite/pytest/shell \
      -s sample.pytest.shell --device-testing -p nrf54l15dk/nrf54l15/cpuapp --device-serial \
      /dev/ttyACM1 --west-flash=--erase

   Twister 在构建目录自动生成 ``twister_pytest_config.yaml``，包含设备配置等全部测试参数。

   若尚未设置，导出所需 PYTHONPATH 环境变量：

   .. code-block:: console

      $ export PYTHONPATH=$ZEPHYR_BASE/scripts/pylib/pytest-twister-harness/src

   最后运行 pytest 命令：

   .. code-block:: console

      $ pytest -s -v -p twister_harness.plugin \
      --twister-config=twister-out/.../sample.pytest.shell/twister_pytest_config.yaml \
      samples/subsys/testsuite/pytest/shell/pytest


能否并行运行 pytest 测试？
==========================

   ``pytest-harness-plugin`` 最初并未针对并行运行 pytest 测试设计，尤其是硬件测试。它假定 Twister 负责测试并行化及可用任务和硬件资源管理。如果因某些原因要自行并行执行，例如使用 `pytest-xdist plugin <https://pytest-xdist.readthedocs.io/en/stable/>`_，需要自行承担相关风险。


限制
****

* 插件尚不支持所有平台类型。
