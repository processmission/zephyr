.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _twister_robot_harness:

Robot
#####
Zephyr 支持将 `Robot Framework <https://robotframework.org/>`_ 用作自动化测试方案之一。

Robot 文件以人类可读的文本描述交互式测试场景，并可在仿真环境或硬件上执行。目前 Zephyr 集成支持在 `Renode <https://renode.io/>`_ 仿真框架、QEMU 和原生模拟器上运行 Robot 测试。

使用 twister 执行 Robot 测试套件的命令如下：

.. code-block:: console

   $ west twister --platform hifive1 --test samples/subsys/shell/shell_module/sample.shell.shell_module.robot

编写 Robot 测试
===============

Robot Framework 自身提供的关键字列表，参见 `the official Robot documentation <https://robotframework.org/robotframework/>`_。

在 Renode 中编写和运行 Robot Framework 测试的信息，参见其文档的 `the testing section <https://renode.readthedocs.io/en/latest/introduction/testing.html>`_，其中列出常用关键字，并链接到定义它们的源代码。

可通过添加关键字扩展框架：直接在 Robot 测试套件文件中编写、使用外部 Python 库，或像 Renode 一样通过 XML-RPC 动态提供。详情参见官方文档的 `extending Robot Framework <https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#extending-robot-framework>`_ 一节。

运行单个测试套件
================

要运行单个测试套件而非整组测试，可执行：

.. code-block:: bash

   $ west twister -p qemu_riscv32 -s arch.shared_interrupt

``robot`` 适配器用于在仿真目标（QEMU、原生模拟器、Renode）上执行 Robot Framework 测试套件。

robot_testsuite: <robot file path>（默认为空）
    指定一个或多个包含待运行 Robot Framework 测试套件的文件路径。

robot_option: <robot option>（默认为空）
    传给 robotframework 的一个或多个选项。
