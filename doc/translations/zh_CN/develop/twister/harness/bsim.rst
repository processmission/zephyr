.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _twister_bsim_harness:

Bsim
####

``bsim`` 测试适配器扩展了 :ref:`脚本测试适配器 <twister_script_harness>`，以支持 BabbleSim 测试。构建阶段会将最终可执行文件（``zephyr.exe``）从构建目录复制到 BabbleSim 的 ``bin`` 目录（``${BSIM_OUT_PATH}/bin``）。运行阶段执行 ``tests_scripts`` 中列出的测试脚本。

默认可执行文件名为 ``bs_<platform_name>_<test_path>_<test_scenario_name>``，其中点和斜杠替换为下划线。可通过 ``harness_config`` 中的 ``bsim_exe_name`` 选项覆盖此名称。

``bsim`` 在 :ref:`脚本测试适配器 <twister_script_harness>` 基础上增加的配置键：

bsim_exe_name: <string>
    如果提供此项，复制到 BabbleSim bin 目录的可执行文件将命名为 ``bs_<platform_name>_<bsim_exe_name>``，而非默认的基于测试路径和场景名称的名称。

以下配置示例包含多个镜像的 BabbleSim 测试：广播者仅构建，扫描者通过 :ref:`required_applications <required_applications>` 引用它：

.. code-block:: yaml

    common:
      platform_allow:
        - nrf52_bsim/native
      harness: bsim
    tests:
      bluetooth.host.adv.extended.advertiser:
        build_only: true
        harness_config:
          bsim_exe_name: tests_bsim_bluetooth_host_adv_extended_prj_advertiser_conf
        extra_args:
          CONF_FILE=prj_advertiser.conf
      bluetooth.host.adv.extended.scanner:
        harness_config:
          bsim_exe_name: tests_bsim_bluetooth_host_adv_extended_prj_scanner_conf
          tests_scripts:
            - tests_scripts/run_adv_extended.sh
        extra_args:
          CONF_FILE=prj_scanner.conf
        required_applications:
          - application: bluetooth.host.adv.extended.advertiser
