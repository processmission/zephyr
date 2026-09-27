.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _twister_shell_harness:

Shell
#####

shell 测试适配器使用 pytest 框架和 Twister 的 pytest 适配器执行 shell 命令并解析输出。

以下选项适用于 shell 适配器：

shell_commands: <list of pairs of commands and their expected output>（默认为空）
    指定要执行的 shell 命令及其预期输出列表，例如：

    .. code-block:: yaml

        harness_config:
          shell_commands:
          - command: "kernel cycles"
            expected: "cycles: .* hw cycles"
          - command: "kernel version"
            expected: "Zephyr version .*"
          - command: "kernel sleep 100"


    若未提供预期输出，会执行命令并记录输出。

shell_commands_file: <string>（默认为空）
    指定包含测试参数的文件，内容应为命令及其预期输出的列表，例如：

    .. code-block:: yaml

      - command: "mpu mtest 1"
        expected: "The value is: 0x.*"
      - command: "mpu mtest 2"
        expected: "The value is: 0x.*"


    未指定文件时，shell 适配器使用测试目录中的默认文件 ``test_shell.yml``。``shell_commands`` 优先于 ``shell_commands_file``。
