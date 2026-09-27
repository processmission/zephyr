.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _env_vars:

环境变量
========

本文档中的多个页面都涉及设置 Zephyr 特定的环境变量。本页介绍具体的设置方法。

设置变量
********

选项 1：仅设置一次
------------------

要在当前终端窗口的整个生命周期内将环境变量 ``MY_VARIABLE`` 设置为 ``foo`` ，请执行以下操作：

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         export MY_VARIABLE=foo

   .. group-tab:: Windows

      .. code-block:: console

         set MY_VARIABLE=foo

.. warning::

  这种方式最适合进行试验。如果关闭终端窗口、改用另一个终端窗口或标签页、重启计算机等，该设置将永久丢失。

  如果要继续使用该设置，建议使用选项 2 或选项 3。

选项 2：在所有终端中
--------------------

.. tabs::

   .. group-tab:: Linux/macOS

      将 ``export MY_VARIABLE=foo`` 这一行添加到主目录中的 shell 启动脚本里。对于 Bash，在 Linux 上通常是 :file:`~/.bashrc` ，在 macOS 上通常是 :file:`~/.bash_profile` 。这些启动脚本中的更改不会影响已经启动的 shell 实例；请尝试打开新的终端窗口以获取新设置。

   .. group-tab:: Windows

      你可以使用 ``cmd.exe`` 中的 ``setx`` 程序，或使用第三方程序 RapidEE。

      使用 ``setx`` 时，请键入以下命令，然后关闭终端窗口。任何新建的 ``cmd.exe`` 窗口都会将 ``MY_VARIABLE`` 设置为 ``foo`` 。

      .. code-block:: console

         setx MY_VARIABLE foo

      要安装 RapidEE（一款免费的图形化环境变量编辑器），请在管理员命令提示符中使用 `using Chocolatey`_ 进行安装：

      .. code-block:: console

         choco install rapidee

      随后，你可以在终端中运行 ``rapidee`` 来启动该程序并设置环境变量。请务必使用 “User” 环境变量区域——否则必须以管理员身份运行 RapidEE。另请确保在退出前点击左上角的 Save 按钮保存更改。你在 RapidEE 中所做的设置将在每次打开新的终端窗口时生效。

.. _env_vars_zephyrrc:

选项 3：使用 ``zephyrrc`` 文件
------------------------------

如果你不希望变量的设置可供所有终端使用，但仍希望保存该值，以便在使用 Zephyr 时将其加载到环境中，请选择此选项。

.. tabs::

   .. group-tab:: Linux/macOS

      Zephyr 支持将 :file:`zephyrrc` 文件放置在多个位置，并在可能时遵循 XDG Base Directory Specification。请在以下某个位置创建 zephyrrc 文件（这些位置将按顺序检查）：

      #. :file:`$XDG_CONFIG_HOME/zephyr/zephyrrc`
      #. :file:`$HOME/.config/zephyr/zephyrrc`
      #. :file:`$HOME/.zephyrrc`

      将以下行添加到首选位置的文件中：

      .. code-block:: console

         export MY_VARIABLE=foo

      要将该值重新加载到当前终端环境中，**你必须运行** 主 ``zephyr`` 仓库中的 ``source zephyr-env.sh`` 。除此之外，该脚本还会 source 你的 :file:`zephyrrc` 文件（它会从上述位置列表中找到第一个文件）。

      如果关闭窗口等，该值将会丢失；请再次运行 ``source zephyr-env.sh`` 以将其恢复。

   .. group-tab:: Windows

      使用 Notepad 等文本编辑器，将 ``set MY_VARIABLE=foo`` 这一行添加到 :file:`%userprofile%\\zephyrrc.cmd` 文件中以保存该值。

      要将该值重新加载到当前终端环境中，**你必须** 先切换到主 ``zephyr`` 仓库目录，然后在 ``cmd.exe`` 窗口中运行 ``zephyr-env.cmd`` 。除此之外，该脚本还会运行 :file:`%userprofile%\\zephyrrc.cmd` 。

      如果关闭窗口等，该值将会丢失；请再次运行 ``zephyr-env.cmd`` 以将其恢复。

      这些脚本会：

      - 将 :envvar:`ZEPHYR_BASE` 设置为 zephyr 仓库所在位置
      - 将一些 Zephyr 特定位置（例如 zephyr 的 :file:`scripts` 目录）添加到 :envvar:`PATH` 环境变量中
      - 加载上述 :ref:`env_vars_zephyrrc` 中描述的 ``zephyrrc`` 文件中的任何设置。

      因此，你可以在需要这些设置时随时使用它们。

.. _zephyr-env:

Zephyr 环境脚本
***************

你可以使用 zephyr 仓库中的脚本 ``zephyr-env.sh`` （适用于 macOS 和 Linux）和 ``zephyr-env.cmd`` （适用于 Windows），将 Zephyr 特定设置加载到当前终端的环境中。为此，请从 zephyr 仓库运行以下命令：

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         source zephyr-env.sh

   .. group-tab:: Windows

      .. code-block:: console

         zephyr-env.cmd

这些脚本会：

- 将 :envvar:`ZEPHYR_BASE` 设置为 zephyr 仓库所在位置
- 将一些 Zephyr 特定位置（例如 zephyr 的 :file:`scripts` 目录）添加到你的 ``PATH`` 环境变量中
- 加载上述 :ref:`env_vars_zephyrrc` 中描述的 ``zephyrrc`` 文件中的任何设置。

因此，你可以在需要这些设置时随时使用它们。

.. _env_vars_important:

重要的环境变量
**************

某些 :ref:`important-build-vars` 也可以在环境中设置。下面介绍其中一些重要的环境变量。这并不是一份完整的列表。

.. envvar:: BOARD

   参见 :ref:`important-build-vars` 。

.. envvar:: CONF_FILE

   参见 :ref:`important-build-vars` 。

.. envvar:: SHIELD

   参见 :ref:`shields` 。

.. envvar:: ZEPHYR_BASE

   参见 :ref:`important-build-vars` 。

.. envvar:: EXTRA_ZEPHYR_MODULES

   参见 :ref:`important-build-vars` 。

.. envvar:: ZEPHYR_MODULES

   参见 :ref:`important-build-vars` 。

.. envvar:: ZEPHYR_BOARD_ALIASES

   参见 :ref:`gs-board-aliases`

在配置用于构建 Zephyr 应用的 :ref:`工具链 <gs_toolchain>` 时，以下附加环境变量非常重要。

.. envvar:: ZEPHYR_SDK_INSTALL_DIR

   Zephyr SDK 的安装路径。

.. envvar:: ZEPHYR_TOOLCHAIN_VARIANT

   要使用的工具链名称。

.. envvar:: {TOOLCHAIN}_TOOLCHAIN_PATH

   由 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 指定的工具链路径。例如，如果 ``ZEPHYR_TOOLCHAIN_VARIANT=host/llvm`` ，则应使用 ``LLVM_TOOLCHAIN_PATH`` 。（请注意在构成环境变量名时的大小写。）

当你 :ref:`更新 Zephyr SDK 工具链 <gs_toolchain_update>` 时，可能需要更新其中一些变量。

模拟器和开发板还可能依赖其他程序。构建系统会尝试自动定位这些程序，但可能依赖额外的 CMake 或环境变量来完成定位。有关更多信息，请查阅模拟器或开发板的文档。在此类情况下，以下环境变量可能会有所帮助：

.. envvar:: PATH

   ``PATH`` 是在类 Unix 或 Microsoft Windows 操作系统上使用的一种环境变量，用于指定可执行程序所在的一组目录。

.. _using Chocolatey: https://chocolatey.org/packages/RapidEE
