.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _twister_pytest_harness:

Pytest
######

:ref:`pytest 测试适配器 <integration_with_pytest>` 用于在 Zephyr 测试中执行 pytest 测试套件。以下选项适用于该适配器：

.. _pytest_root:

pytest_root: <list of pytest testpaths>（默认 pytest）
    指定测试场景开始运行时要执行的 pytest 目录、文件或子测试列表。默认 pytest 目录为 ``pytest``。运行结束后，Twister 根据 pytest 报告判断测试场景通过或失败。支持展开环境变量和 Zephyr 模块目录变量（见 :ref:`twister_module_dir_vars`）。以下是有效 pytest 根路径的示例：

    .. code-block:: yaml

        harness_config:
          pytest_root:
            - "pytest/test_shell_help.py"
            - "../shell/pytest/test_shell.py"
            - "/tmp/test_shell.py"
            - "~/tmp/test_shell.py"
            - "$ZEPHYR_BASE/samples/subsys/testsuite/pytest/shell/pytest/test_shell.py"
            - "$ZEPHYR_HAL_NORDIC_MODULE_DIR/tests/pytest/test_hal.py"  # path inside a module
            - "pytest/test_shell_help.py::test_shell2_sample"  # select pytest subtest
            - "pytest/test_shell_help.py::test_shell2_sample[param_a]"  # select pytest parametrized subtest

.. _pytest_args:

pytest_args: <list of arguments>（默认为空）
    指定传给 ``pytest`` 的附加参数列表，例如 ``pytest_args: [‘-k=test_method’, ‘--log-level=DEBUG’]``。可以多次传入 ``--pytest-args``，向 pytest 提供多个参数。

.. _pytest_dut_scope:

pytest_dut_scope: <function|class|module|package|session>（默认 function）
    共享 ``dut`` 和 ``shell`` pytest fixture 的作用域。设为 ``function`` 时，Python 脚本的每个测试用例都会启动 DUT；设为 ``session`` 时，DUT 只启动一次。


  以下 YAML 示例包含 pytest harness_config 选项。未指定 pytest_root 时，使用默认目录名“pytest”。示例参见 samples/subsys/testsuite/pytest/。

  .. code-block:: yaml

      common:
        harness: pytest
      tests:
        pytest.example.directories:
          harness_config:
            pytest_root:
              - pytest_dir1
              - $ENV_VAR/samples/test/pytest_dir2
        pytest.example.files_and_subtests:
          harness_config:
            pytest_root:
              - pytest/test_file_1.py
              - test_file_2.py::test_A
              - test_file_2.py::test_B[param_a]

.. _required_devices:

required_devices: <list of required device entries>（默认为空）
    指定多 DUT 测试场景额外需要的 DUT。每个条目配置一个与主 DUT 一同预留和烧录的附加设备。空条目 ``{}`` 表示预留一个与主 DUT 使用相同平台和应用的第二设备。

    多 DUT 测试支持硬件设备和 ``native_sim`` 仿真，不支持 QEMU。对于仿真目标，Twister 自动创建所需的占位 DUT 条目，无需硬件映射。硬件测试则需提供硬件映射文件（``--hardware-map``），其中每个所需设备均有匹配条目。详见 :ref:`twister_multi_duts_testing`。

    每个条目支持以下可选字段：


    platform: <string>（可选，默认当前测试的平台）
        此设备使用的平台。未指定时，使用与主 DUT 相同的平台。

    application: <string>（可选，默认当前测试应用）
        要烧录到此设备的测试应用 ID。指定后，Twister 单独构建该应用，并在烧录前将其构建目录分配给预留 DUT。未指定时，使用与主 DUT 相同的应用。

        其机制与 :ref:`required_applications <required_applications>` 相同。

    path: <string>（可选）
        Twister 搜索 ``application`` 指定应用的目录路径。可以是绝对路径，或相对于测试 YAML 所在目录的路径。支持展开环境变量和 Zephyr 模块目录变量（见 :ref:`twister_module_dir_vars`）。未指定时，在引用该应用的测试 YAML 所在目录中搜索。

    fixture: <list of fixture names>（可选，默认为空）
        预留设备必须具备的 fixture 名称列表。详见 :ref:`Fixtures <twister_fixtures>`。

        fixture 支持 ``name:param`` 形式的可选参数后缀，例如 ``io_adapter:channel_a``。如果主 DUT 的 fixture 带参数，Twister 会使用该参数值匹配所需设备，只考虑同名 fixture 具有 **相同参数** 的设备。这确保物理连接的 DUT 对（例如两块相连、在硬件映射中登记了相同 fixture 参数的开发板）始终一同预留，不会与无关开发板混配。

        成对设备的硬件映射条目示例：

        .. code-block:: yaml

            - id: "01"
              platform: nrf52840dk/nrf52840
              serial: /dev/ttyACM0
              fixtures:
                - io_adapter:channel_a
            - id: "02"
              platform: nrf52840dk/nrf52840
              serial: /dev/ttyACM1
              fixtures:
                - io_adapter:channel_a

        主 DUT 和所需设备均配置 ``fixture: [io_adapter]`` 时，Twister 只选择共享相同 ``channel_a`` 参数的开发板，保证选中物理配对的开发板。


    需要多个设备的配置示例：

    .. code-block:: yaml

        tests:
          # Two DUTs, same platform and application
          multidut.basic:
            harness_config:
              required_devices:
                - {}
          # Second DUT fixed to a specific platform
          multidut.fixed_platform:
            harness_config:
              required_devices:
                - platform: nrf52840dk/nrf52840
          # Second DUT flashed with a different application
          multidut.other_app:
            harness_config:
              required_devices:
                - application: multidut.basic
