.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _clion_ide:

CLion
#####

.. note::

   本指南介绍如何利用 CLion 的 CMake 集成，设置、构建和调试 Zephyr 示例应用。这已不再是最佳方式。

   CLion 现已提供 `native Zephyr West integration`_，可以更简单、直观地打开、构建、运行和调试 Zephyr 项目。本指南将尽快更新；如果你更喜欢使用 CMake，以下方法仍然有效。

CLion_ 是跨平台 C/C++ IDE，支持多线程 RTOS 调试。

本指南介绍在 CLion 中设置、构建和调试 Zephyr :zephyr:code-sample:`multi-thread-blinky` 示例的过程。

这些说明已在 Windows 上测试。macOS 和 Linux 上的 CLion 工作流程相同，但请选用正确的环境文件，并调整路径。

获取 CLion
**********

通过 `Download CLion`_ 下载安装。

初始化新工作区
**************

本指南详细说明如何构建和调试 :zephyr:code-sample:`multi-thread-blinky` 示例，其他 Zephyr 项目和 :ref:`工作区布局 <west-workspaces>` 也可采用类似步骤。

开始之前，请按照 :ref:`getting_started` 确保 Zephyr 开发环境正常工作。

在 CLion 中打开项目
*******************

#. 在 CLion 欢迎页面点击 :guilabel:`Open`，或在主菜单选择 :menuselection:`File --> Open`。

#. 进入 Zephyr 工作区；如果遵循入门指南，它位于 HOME 目录中的 :file:`zephyrproject`。然后选择 :file:`zephyr/samples/basic/threads` 或其他示例项目目录。

   点击 :guilabel:`OK`。

#. 如果出现提示，点击 :guilabel:`Trust Project`。

   项目安全性的更多信息，见 CLion 在线帮助的 `Project security`_ 一节。

配置工具链和 CMake 配置
***********************

CLion 会打开含有 CMake 配置设置的 :guilabel:`Open Project Wizard`。如果未打开，请进入 :menuselection:`Settings --> Build, Execution, Deployment --> CMake`。

#. 点击 :guilabel:`Toolchain` 字段旁的 :guilabel:`Manage Toolchains`，打开 :guilabel:`Toolchain` 设置对话框。

#. 建议 Windows 使用默认设置的 :guilabel:`Bundled MinGW` 工具链，Unix 系统使用默认的 :guilabel:`System` 工具链。

#. 点击 :menuselection:`Add environment --> From file`，选择 ``..\.venv\Scripts\activate.bat``。

   .. figure:: img/clion_toolchain_mingw.webp
      :width: 600px
      :align: center
      :alt: 使用环境脚本的 MinGW 工具链

   点击 :guilabel:`Apply` 保存修改。

#. 返回 CMake 配置设置对话框，在 :guilabel:`CMake options` 中指定开发板，例如：

   .. code-block::

      -DBOARD=nrf52840dk/nrf52840

   .. figure:: img/clion_cmakeprofile.webp
      :width: 600px
      :align: center
      :alt: CMake 配置

#. 点击 :guilabel:`Apply` 保存修改。

   CMake 加载应能顺利完成。

配置调试所需的 Zephyr 参数
**************************

#. 在右上角的配置切换器中选择 :guilabel:`guiconfig`，点击锤子图标。

#. 使用图形界面应用设置以下标志：

   .. code-block::

      DEBUG_THREAD_INFO
      THREAD_RUNTIME_STATS
      DEBUG_OPTIMIZATIONS

构建项目
********

在配置切换器中选择 **zephyr_final**，点击锤子图标。

此时也可以调用 ``puncover``、``hardenconfig`` 等其他 CMake 目标。


启用 RTOS 集成
**************

#. 进入 :menuselection:`Settings --> Build, Execution, Deployment --> Embedded Development --> RTOS Integration`。

#. 勾选 :guilabel:`Enable RTOS Integration`。

   此选项使调试期间可以查看 Zephyr 任务。详情见 CLion 在线帮助中的 `Multi-threaded RTOS debug`_。

   可以保持 :guilabel:`Auto` 设置，CLion 会自动检测 Zephyr。

创建 Embedded GDB Server 配置
*****************************

在 CLion 中调试 Zephyr 应用，需要基于 Embedded GDB Server 模板创建运行／调试配置。

以下说明以 Nordic Semiconductor 开发板和 Segger J-Link 调试探针为例。如果你的环境不同，请相应调整配置。

#. 在主菜单选择 :menuselection:`Run --> New Embedded Configuration`。

#. 配置以下设置：

    .. list-table::
        :header-rows: 1

        * - 选项
          - 值

        * - :guilabel:`Name` （可选）
          - Zephyr-threads

        * - :guilabel:`GDB Server Type`
          - Segger JLink

        * - :guilabel:`Location`
          - Windows 上 ``JLinkGDBServerCL.exe`` 的路径，或 macOS/Linux 上 ``JLinkGDBServer`` 二进制文件的路径。

        * - :guilabel:`Debugger`
          - Bundled GDB

            .. note:: 对于非 ARM、非 x86 架构，使用 Zephyr SDK 中的 GDB 可执行文件。请选用支持 Python 的版本，例如 **riscv64-zephyr-elf-gdb-py**，并检查系统 ``PATH`` 中存在 Python。

        * - :guilabel:`Target`
          - zephyr-final

        * - :guilabel:`Executable binary`
          - zephyr-final

        * - :guilabel:`Download binary`
          - Always

        * - :guilabel:`TCP/IP port`
          - Auto

    .. figure:: img/clion_gdbserverconfig.webp
       :width: 500px
       :align: center
       :alt: Embedded GDB Server 配置

#. 点击 :guilabel:`Next`，设置 Segger J-Link 参数。

    .. figure:: img/clion_segger_settings.webp
       :width: 500px
       :align: center
       :alt: Segger J-Link 参数

#. 准备就绪后点击 :guilabel:`Create`。

开始调试
********

#. 点击代码行左侧边栏，设置断点。

#. 确保配置切换器中选择了 **Zephyr-threads**，然后点击虫子图标或按 :kbd:`Ctrl+D`。

#. 命中断点后，CLion 会打开 Debug 工具窗口。

   Zephyr 任务列在 :guilabel:`Threads & Variables` 面板中，可以在任务间切换并查看各自变量。

    .. figure:: img/clion_debug_threads.webp
       :width: 800px
       :align: center
       :alt: 调试会话中查看 Zephyr 任务

   IDE 调试功能的详细说明，参见 `CLion web help`_。

.. _native Zephyr West integration: https://jb.gg/cl_zephyr_doc
.. _CLion: https://www.jetbrains.com/clion/
.. _Download CLion: https://www.jetbrains.com/clion/download
.. _Project security: https://www.jetbrains.com/help/clion/project-security.html#projects_security
.. _Multi-threaded RTOS debug: https://www.jetbrains.com/help/clion/rtos-debug.html
.. _CLion web help: https://www.jetbrains.com/help/clion/debugging-code.html
