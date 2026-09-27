.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _vscode_ide:

Visual Studio Code
##################

`Visual Studio Code`_，简称 VS Code，是流行的跨平台 IDE，支持 C 项目并提供丰富的扩展。

本指南介绍如何为 Zephyr :zephyr:code-sample:`blinky` 示例配置 VS Code。

这些说明已在 Linux 上测试，macOS 和 Windows 步骤应相同，只需按需调整路径。

获取 VS Code
************

通过 `Download VS Code`_ 下载安装。

通过左侧面板的 :guilabel:`Extensions` 扩展市场安装所需扩展。搜索并安装 `C/C++ Extension Pack`_。

初始化新工作区
**************

本指南详细介绍 :zephyr:code-sample:`blinky` 示例的配置；其他 Zephyr 项目和 :ref:`工作区布局 <west-workspaces>` 也可采用类似步骤。

开始之前，请按照 :ref:`getting_started` 确保 Zephyr 开发环境正常工作。

在 VS Code 中打开项目
*********************

#. 在 VS Code 主菜单选择 :menuselection:`File --> Open Folder`。

#. 进入并选择 Zephyr 工作区。如果遵循入门指南，它位于 HOME 目录中的 :file:`zephyrproject`。

#. 如果出现提示，请启用工作区信任。

生成编译命令
************

为支持代码导航和静态检查，必须先编译一次项目，生成 :file:`compile_commands.json`，向 C/C++ 扩展提供包含路径等所需信息。可以使用 VS Code 集成终端：通过顶部菜单或命令面板（:kbd:`Ctrl+Shift+P`）选择 :menuselection:`Terminal --> New Terminal`，然后输入：

.. code-block:: console

   $ cd zephyr
   $ west build -p always -b native_sim/native/64 samples/basic/blinky


配置 C/C++ 扩展
***************

接下来需要指定生成的 :file:`compile_commands.json`，以启用 VS Code 的静态检查和代码导航。

#. 在 VS Code 顶部菜单进入 :menuselection:`File --> Preferences --> Settings`。

#. 搜索 :guilabel:`C_Cpp > Default: Compile Commands`，将其设为 ``zephyr/build/compile_commands.json``。

   现在代码中的静态检查错误应已消失，并且可以使用代码导航。

其他资源
********

还有许多扩展可帮助在 VS Code 中开发 Zephyr。本指南尚未介绍它们，但可以按照各自文档配置：

贡献辅助工具
============

- `Checkpatch Extension`_
- `EditorConfig Extension`_

文档语言扩展
============

- `reStructuredText Extension Pack`_

IDE 扩展
========

- `CMake Extension documentation`_
- `nRF Kconfig Extension`_
- `nRF DeviceTree Extension`_
- `GNU Linker Map files Extension`_

其他指南
========

- `How to Develop Zephyr Apps with a Modern, Visual IDE`_

.. note::

   请注意，这些扩展的质量和维护程度可能不尽相同。

.. _Visual Studio Code: https://code.visualstudio.com/
.. _Download VS Code: https://code.visualstudio.com/Download
.. _VS Code documentation: https://code.visualstudio.com/docs
.. _C/C++ Extension Pack: https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools-extension-pack
.. _C/C++ Extension documentation: https://code.visualstudio.com/docs/languages/cpp
.. _CMake Extension documentation: https://code.visualstudio.com/docs/cpp/cmake-linux

.. _Checkpatch Extension: https://marketplace.visualstudio.com/items?itemName=idanp.checkpatch
.. _EditorConfig Extension: https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig

.. _reStructuredText Extension Pack: https://marketplace.visualstudio.com/items?itemName=lextudio.restructuredtext-pack

.. _nRF Kconfig Extension: https://marketplace.visualstudio.com/items?itemName=nordic-semiconductor.nrf-kconfig
.. _nRF DeviceTree Extension: https://marketplace.visualstudio.com/items?itemName=nordic-semiconductor.nrf-devicetree
.. _GNU Linker Map files Extension: https://marketplace.visualstudio.com/items?itemName=trond-snekvik.gnu-mapfiles

.. _How to Develop Zephyr Apps with a Modern, Visual IDE: https://github.com/beriberikix/zephyr-vscode-example
