.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _workbench_for_zephyr:

Workbench for Zephyr
####################

Workbench for Zephyr 是 Visual Studio Code（VS Code）扩展，提供 Zephyr 开发支持，包括 **SDK 管理**、**项目创建向导**、**构建和烧录** 以及 **调试**。

逐步操作说明见 `Getting started tutorial`_。

主要功能
********

- 安装原生主机工具，例如 Python、CMake 等。
- 安装并指定工具链，例如 Zephyr SDK、IAR 等。
- 导入 West 工作区
- 创建和导入 Zephyr 应用
- 构建和烧录应用
- 调试应用
- 自动安装运行器
- 执行内存分析和静态分析

兼容性
******

- Windows 10-11
- Linux（x86_64）

  - Ubuntu
  - Debian
  - Fedora
  - 其他发行版也可能可用，但未经测试。

- macOS

入门
****

#. 安装扩展

   从 VS Code Marketplace 安装 `Workbench for Zephyr`_。

#. 打开 Workbench for Zephyr 扩展

   点击活动栏中的 :guilabel:`Workbench for Zephyr` 图标。

#. 安装主机工具

   点击 :guilabel:`Install Host Tools` 下载并安装原生工具，通常安装到 ``${HOME}/.zinstaller``。

   .. figure:: img/workbench_for_zephyr_install_host_tools.webp
      :align: center
      :alt: 在 Workbench for Zephyr 中安装主机工具

   .. note::

      某些主机工具需要管理员权限。Windows 上安装 7z 时需要；Linux 上通过包管理器安装工具时需要，例如运行 :command:`apt install`。

#. 导入工具链

   点击 :guilabel:`Import Toolchain`，选择工具链及目标目录。

   工具链提供构建和调试 Zephyr 应用所需的编译器及调试器。推荐使用 Zephyr SDK，可安装完整套件或面向特定目标的最小版本。Workbench 也支持 IAR 等其他工具链。

#. 初始化或导入 West 工作区

   点击 :guilabel:`Initialize workspace` 并填写工作区信息。

   .. figure:: img/workbench_for_zephyr_west_workspace.webp
      :align: center
      :width: 600px
      :alt: 在 Workbench for Zephyr 中初始化 West 工作区

   Workbench 会创建工作区，并解析 west 清单以配置项目。

#. 创建新应用

   Workbench for Zephyr 中的新项目基于 Zephyr 源码中的示例创建。

   - 点击 :guilabel:`Create New Application`。
   - 选择要关联的 :guilabel:`West Workspace`。
   - 选择要使用的 :guilabel:`Zephyr SDK`。
   - 选择目标 :guilabel:`Board`，例如 ``ST STM32F4 Discovery``。
   - 选择作为基础的 :guilabel:`Sample` 项目，例如 ``hello_world``。
   - 输入项目名称。
   - 输入项目位置。

   .. figure:: img/workbench_for_zephyr_application.webp
      :align: center
      :width: 600px
      :alt: 在 Workbench for Zephyr 中基于示例创建新应用

#. 构建应用

   点击状态栏中的 :guilabel:`Build`，或选择要构建的应用目录。构建输出显示在集成终端中。

#. 配置并运行调试会话

   使用 :guilabel:`Debug Manager` 生成或更新调试配置（:file:`.vscode/launch.json`）：

   - 生成的 ELF（程序路径）
   - SVD 文件（可选）
   - GDB、端口和地址（如需要）
   - 调试服务器／运行器，例如 OpenOCD、J-Link、LinkServer、pyOCD 等

   .. figure:: img/workbench_for_zephyr_debug_manager.webp
      :align: center
      :width: 600px
      :alt: Workbench for Zephyr 的 Debug Manager

   然后通过 :guilabel:`Run and Debug` 正常启动调试。

安装运行器
**********

Workbench for Zephyr 可为某些运行器提供安装程序，例如 OpenOCD 和 STM32CubeProgrammer。使用 :guilabel:`Install Runners` 查看支持的工具并安装，或打开厂商网站。

实用链接
********

- 可以浏览 `Extension repository`_。
- 更多信息见 `Full documentation`_。

.. _Extension repository: https://github.com/Ac6Embedded/vscode-zephyr-workbench
.. _Full documentation: https://z-workbench.com/
.. _Workbench for Zephyr: https://marketplace.visualstudio.com/items?itemName=Ac6.zephyr-workbench
.. _Getting started tutorial: https://youtu.be/1RB0GI6rJk0?si=_D2AA3KurzCwLtRv
