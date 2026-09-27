.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west:

West（Zephyr 元工具）
#####################

Zephyr 项目提供了一个功能丰富的命令行工具 ``west``\ [#west-name]_。West 在独立的 `repository`_ （仓库）中开发。

West 的内置命令提供多仓库管理系统，其功能借鉴了 Google 的 Repo 工具和 Git 子模块。West 还支持“插件”：你可以自行编写 west 扩展命令，为 west 添加功能。Zephyr 借此提供构建应用程序、烧录、调试等便捷功能。

与 ``git`` 和 ``docker`` 类似，顶层 ``west`` 命令接受一些通用选项、要运行的子命令，以及该子命令的选项和参数::

  west [common-opts] <command> [opts] <args>

从 west v0.8 起，也可以这样运行 west::

  python3 -m west [common-opts] <command> [opts] <args>

运行 ``west --help`` （简写为 ``west -h``）可以获取可用 west 命令的顶层帮助；运行 ``west <command> -h`` 可以获取各命令的详细帮助。

.. toctree::
   :maxdepth: 1

   install.rst
   release-notes.rst
   troubleshooting.rst
   basics.rst
   built-in.rst
   workspaces.rst
   manifest.rst
   config.rst
   alias.rst
   extensions.rst
   build-flash-debug.rst
   sign.rst
   zephyr-cmds.rst
   why.rst
   without-west.rst

有关 west 的 Python API，详见 :ref:`west-apis`。

.. rubric:: 脚注

.. [#west-name]

   Zephyr 是拉丁语 `Zephyrus <https://en.wiktionary.org/wiki/Zephyrus>`_ 的英文名称，指古希腊的西风之神。

.. _repository:
   https://github.com/zephyrproject-rtos/west
