.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ide_for_zephyr_vscode_ext:

IDE for Zephyr（VS Code 扩展）
##############################

`IDE for Zephyr`_ 是用于 Zephyr RTOS 开发的 Visual Studio Code（VS Code）扩展，支持 **主机工具管理**、**west 工作区设置**、**SDK 管理**、**项目创建**、**构建和烧录** 以及 **调试**。

.. figure:: img/ide-for-zephyr_main_vscode_ext.webp
   :align: center
   :alt: IDE for Zephyr 主页面及内存报告界面

主要功能
********

- 通过内置 ``zephyr-ide-cortex`` 和 ``zephyr-ide-west`` 调试器类型与 Cortex-Debug 集成，支持 ST-Link、J-Link、OpenOCD、Black Magic Probe 等探针，自动解析 ELF、GDB 和运行器路径。
- 与 clangd 或 C/C++ 集成，提供 IntelliSense。
- 通过 Build Dashboard 查看内存占用、Kconfig 和设备树，无需离开 VS Code 即可用旭日图查看 ROM 和 RAM。
- 使用内置编辑器交互式编辑 Kconfig 选项。
- 通过项目面板添加、运行和重新配置 Twister 测试。
- 在 Linux、macOS 和 Windows 上自动安装 CMake、Python 3、Ninja、DTC、GCC 等原生主机工具。
- 安装和管理 Zephyr SDK 版本及各架构工具链。
- 从现有应用或 Zephyr 示例添加项目，支持多个构建，并为各构建单独覆盖开发板与配置。
- 将项目配置保存在可纳入版本控制的 :file:`.vscode/zephyr-ide.json` 中，可以指定 SDK、软件包和二进制 blob。

兼容性
******

- Windows
- Linux
- macOS

入门
****

#. 安装扩展

   从 `VS Code Marketplace`_ 或 `Open VSX Registry`_ 安装 IDE for Zephyr。

   还可从 `VS Code Marketplace (Extension Pack)`_ 或 `Open VSX Registry (Extension Pack)`_ 安装扩展包，其中包含 Cortex-Debug、C/C++、Serial Monitor、Devicetree LSP 和 CMake 支持。

#. 打开概览页面并安装主机工具

   点击 :guilabel:`Host Tools` 卡片。扩展会检查 PATH 中是否存在所需构建依赖，例如 CMake、Python 3、Ninja、DTC、GCC，并可自动安装缺少的工具。


#. 配置 West 工作区

   点击 :guilabel:`Workspace` 卡片，选择设置方式：

   - **IDE for Zephyr Workspace from Git**：克隆已包含预配置 IDE for Zephyr 工作区的仓库。
   - **West Workspace from Git**：克隆现有的基于 west 的 Zephyr 仓库。
   - **Standard Workspace**：创建新工作区，包括 Python 虚拟环境、west 安装和 Zephyr 仓库初始化。
   - **Open Current Directory**：使用已有 :file:`.west` 目录，或通过 :envvar:`ZEPHYR_BASE` 关联外部 Zephyr 安装。

   此步骤也会在需要时提示安装 Zephyr SDK。之后可以通过概览页面的 :guilabel:`Zephyr SDK` 卡片管理 SDK。

   .. figure:: img/ide_for_zephyr_workspace_setup_vscode_ext.webp
      :align: center
      :alt: IDE for Zephyr 的工作区设置选项

#. 添加项目和构建

   在 Project 面板点击 :guilabel:`Add Project`，添加现有应用或复制 Zephyr 示例作为起点。

   添加项目后，点击 :guilabel:`Add Build` 创建构建配置，选择目标开发板，也可选择运行器配置。每个项目可包含针对不同开发板或配置的多个构建。

#. 构建和烧录应用

   使用状态栏按钮或 :guilabel:`Project Build` 面板构建、烧录或执行 pristine 全新构建。构建输出显示在集成终端中。

#. 配置并运行调试会话

   IDE for Zephyr 内置 ``zephyr-ide-west`` 调试器类型，会读取当前构建的 :file:`runners.yaml` 并自动转换为 Cortex-Debug 会话，无需先添加 :file:`.vscode/launch.json` 条目。``zephyr-ide-west`` 提供器接受原本传给 ``west debugserver`` 的参数，``zephyr-ide-cortex`` 提供器则接受直接传给 ``cortex-debug`` 的参数。也可以自行设置启动配置并绑定构建。扩展提供可在启动时解析的命令。

   手动添加启动配置时，可使用以下最简形式：

   .. code-block:: json

      {
        "name": "Zephyr IDE: Debug",
        "type": "zephyr-ide-west",
        "request": "launch"
      }

   内置提供器从 :file:`runners.yaml` 选择运行器，解析 ELF 和 GDB 路径，再将会话交给 Cortex-Debug。

共享项目配置
************

项目设置、构建、运行器配置、Kconfig overlay、设备树 overlay，以及各构建的 west 和 CMake 参数都保存在 :file:`.vscode/zephyr-ide.json`。该文件易于阅读，可以提交到版本控制，让团队成员共享相同工作区配置。

实用链接
********

- 浏览 `Extension repository`_
- 阅读 `Full documentation`_
- 试用 `Sample project`_

.. _IDE for Zephyr:
   https://marketplace.visualstudio.com/items?itemName=mylonics.zephyr-ide
.. _VS Code Marketplace:
   https://marketplace.visualstudio.com/items?itemName=mylonics.zephyr-ide
.. _Open VSX Registry:
   https://open-vsx.org/extension/mylonics/zephyr-ide
.. _VS Code Marketplace (Extension Pack):
   https://marketplace.visualstudio.com/items?itemName=mylonics.zephyr-ide-extension-pack
.. _Open VSX Registry (Extension Pack):
   https://open-vsx.org/extension/mylonics/zephyr-ide-extension-pack
.. _Extension repository: https://github.com/mylonics/zephyr-ide
.. _Full documentation: https://zephyr-ide.mylonics.com/
.. _Getting started video: https://www.youtube.com/watch?v=Asfolnh9kqM
.. _Sample project: https://github.com/mylonics/zephyr-ide-sample-project
