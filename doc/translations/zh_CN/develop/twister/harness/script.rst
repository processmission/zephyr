.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _twister_script_harness:

脚本
####

``script`` 测试适配器将 shell 脚本作为测试用例执行。它从 ``tests_scripts`` 配置选项解析脚本，以子进程运行每个脚本，并根据退出码分别报告通过或失败。

``script`` 适配器也是 :ref:`bsim <twister_bsim_harness>`、:ref:`pytest <twister_pytest_harness>` 和 :ref:`ctest <twister_ctest_harness>` 的基类，提供共用的子进程执行、流式输出和日志处理功能。

tests_scripts: <list of script paths>（默认 tests_scripts）
    指定测试场景运行时要执行的 shell 脚本路径列表，路径相对于测试源目录。每项可以是单个文件、目录或 glob 模式。若为目录，会收集其中及子目录内所有 ``.sh`` 文件，但排除以 ``_`` 开头的文件。默认为 ``tests_scripts`` 目录。

    .. code-block:: yaml

        harness: script
        harness_config:
          tests_scripts:
            - tests_scripts/test_a.sh
            - ../../test/test_b.sh
            - $ENV_VAR/tests_scripts

在 ``--`` 之后传给 Twister 的附加命令行参数，会作为额外位置参数转发给每个脚本。
