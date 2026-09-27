.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _beyond-gsg:

入门指南之外
############

:ref:`getting_started` 为搭建用于 Zephyr 开发的 Linux、macOS 或 Windows 环境提供了一条直接路径。本文深入探讨 Zephyr 开发环境搭建中的问题与替代方案。

.. _python-pip:

Python 与 pip
*************

Python 3 及其软件包管理器 pip\ [#pip]_ 被 Zephyr 广泛用于安装和运行编译、运行 Zephyr 应用所需的脚本，搭建和维护 Zephyr 开发环境，以及构建项目文档。

根据操作系统的不同，在安装新软件包时你可能需要为 ``pip3`` 命令加上 ``--user`` 选项。本文档各处的说明中都有相关介绍。有关 pip\ [#pip]_ 的更多信息（包括 `information on -\\-user <Installing Packages_>`_），请参阅 Python Packaging User Guide 中的 `Installing Packages <information on -\\-user_>`_。

- 在 Linux 上，请确保 ``~/.local/bin`` 位于 :envvar:`PATH` :ref:`环境变量 <env_vars>` 的最前面，否则使用 ``--user`` 安装的程序将无法找到。使用 ``--user`` 安装可以避免 pip 与系统软件包管理器之间的冲突，这也是基于 Debian 的发行版上的默认做法。

- 在 macOS 上，`Homebrew disables -\\-user`_。

- 在 Windows 上，如需使用 ``--user`` 选项，请参阅 `Installing Packages`_ 中的相关信息。

在所有操作系统上，如果某个软件包已在本地安装，但有更新的版本可用，pip 的 ``-U`` 选项会安装或更新该软件包。如果需要使用某个软件包的最新版本，建议使用该选项。（查看 :zephyr_file:`scripts/requirements.txt` 文件，了解是否要求特定的 Python 软件包版本。）

高级平台设置
************

以下是一些替代说明，用于在受支持的开发平台上进行更高级的平台设置：

.. toctree::
   :maxdepth: 1

   Linux 设置替代方案 <getting_started/installation_linux.rst>
   macOS 设置替代方案 <getting_started/installation_mac.rst>
   Windows 设置替代方案 <getting_started/installation_win.rst>

.. _gs_toolchain:

安装工具链
**********

Zephyr 二进制文件由 *工具链* 编译和链接，工具链由交叉编译器及相关工具组成，它们与用于开发在主机操作系统上原生运行的软件的编译器和工具不同。

你可以安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>` 以获得适用于所有受支持架构的工具链，也可以安装由 SoC 厂商或特定开发板推荐的 :ref:`替代工具链 <toolchains>`；请查看你所使用开发板的 :ref:`开发板级文档 <boards>`。

你可以设置 :ref:`环境变量 <env_vars>`，例如 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT <{TOOLCHAIN}_TOOLCHAIN_PATH>`，把它设置为受支持的值，并设置该工具链变体专有的其他变量，从而配置 Zephyr 构建系统使用特定的工具链。

.. _gs_toolchain_update:

更新 Zephyr SDK 工具链
**********************

更新 Zephyr SDK 时，请检查 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 或 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量是否已经设置。

* 如果这些变量未设置，默认会选择最新兼容的 Zephyr SDK 版本。无需做任何更改，直接进行下一步。

* 如果设置了 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`，构建时会选择对应的工具链。Zephyr SDK 通过值 ``zephyr`` 来标识。如果 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 环境变量的值不是 ``zephyr``，请取消设置该变量或将其值改为 ``zephyr``，以确保选中 Zephyr SDK。

* 如果设置了 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量，它将覆盖 Zephyr SDK 的默认查找位置。如果你把 Zephyr SDK 安装到 :ref:`推荐位置 <toolchain_zephyr_sdk_bundle_variables>` 之一，可以取消设置该变量。否则，请将其设置为你选定的安装位置。

有关 Zephyr 中这些环境变量的更多信息，请参阅 :ref:`env_vars_important`。

克隆 Zephyr 仓库
****************

Zephyr 项目源代码维护在 `GitHub zephyr repo <https://github.com/zephyrproject-rtos/zephyr>`_ 中。Zephyr 使用的外部模块位于其上级 `GitHub Zephyr project <https://github.com/zephyrproject-rtos/>`_ 中。由于这些依赖关系，使用 Zephyr 提供的 :ref:`west <west>` 工具来获取和管理 Zephyr 及外部模块的源代码会很方便。更多细节请参阅 :ref:`west-basics`。

开发工具安装完成后，使用 :ref:`west` 创建、初始化并从 zephyr 和外部模块仓库下载源代码。我们将使用名称 ``zephyrproject``，但你可以选择任何在路径中不含空格的名称。

.. code-block:: console

   west init zephyrproject
   cd zephyrproject
   west update

``west update`` 命令会获取 :ref:`modules`，并使 :file:`zephyrproject` 目录中的内容与本地 zephyr 仓库中的代码保持同步。

.. warning::

   每当 :file:`zephyr/west.yml` 发生变化时，你都必须运行 ``west update``，例如在拉取 :file:`zephyr` 仓库、在其中切换分支或对它执行 ``git bisect`` 时。

保持 Zephyr 更新
================

要更新 Zephyr 项目源代码，你需要通过 ``git`` 获取最新更改。然后，如上一段所述运行 ``west update``。此外，还要检查是否有更新或新增的 Python 依赖项。

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         # replace zephyrproject with the path you gave west init
         cd zephyrproject/zephyr
         git pull
         west update
         west packages pip --install

   .. group-tab:: Windows

      .. tabs::

         .. code-tab:: bat

            :: replace zephyrproject with the path you gave west init
            cd zephyrproject\zephyr
            git pull
            west update
            cmd /c scripts\utils\west-packages-pip-install.cmd

         .. code-tab:: powershell

            # replace zephyrproject with the path you gave west init
            cd zephyrproject\zephyr
            git pull
            west update
            python -m pip install @((west packages pip) -split ' ')

导出 Zephyr CMake 包
********************

如果尚未在 :ref:`getting_started` 中完成，可以将 :ref:`cmake_pkg` 导出到 CMake 的用户包注册表。

.. _gs-board-aliases:

开发板别名
**********

需要使用多个开发板的开发者可能会觉得显式的开发板名称很繁琐，希望为常用目标使用别名。CMake 文件支持这种做法，其内容类似如下：

.. code-block:: cmake

   # Variable foo_BOARD_ALIAS=bar replaces BOARD=foo with BOARD=bar and
   # sets BOARD_ALIAS=foo in the CMake cache.
   set(pca10028_BOARD_ALIAS nrf51dk/nrf51822)
   set(pca10056_BOARD_ALIAS nrf52840dk/nrf52840)
   set(k64f_BOARD_ALIAS frdm_k64f)
   set(sltb004a_BOARD_ALIAS efr32mg_sltb004a)

并在 :envvar:`ZEPHYR_BOARD_ALIASES` 中指定其位置。这样就可以在 ``cmake -DBOARD=pca10028`` 和 ``west -b pca10028`` 等场景中使用别名 ``pca10028``。

构建并运行应用
**************

在受支持的主机系统上，你可以在真实硬件上构建、烧录并运行 Zephyr 应用。根据操作系统的不同，你还可以使用 QEMU 以仿真方式运行应用，或者使用 :zephyr:board:`native_sim <native_sim>` 将其作为原生应用运行。有关构建应用的更多信息，请参阅 :ref:`build_an_application` 章节。

构建 Blinky
===========

下面构建 :zephyr:code-sample:`blinky` 示例应用。

Zephyr 应用是为在特定硬件上运行而构建的，这种硬件称为“开发板”\ [#board_misnomer]_。这里我们使用 Phytec 的 :zephyr:board:`reel_board<reel_board>`，如果你使用其他开发板，可以把 ``reel_board`` 构建目标改为其他值。参见 :ref:`boards`，或在 ``zephyrproject`` 目录下的任意位置运行 ``west boards``，以获取受支持开发板的列表。

#. 转到 zephyr 仓库：

   .. code-block:: console

      cd zephyrproject/zephyr

#. 为 ``reel_board`` 构建 blinky 示例：

   .. zephyr-app-commands::
      :zephyr-app: samples/basic/blinky
      :board: reel_board
      :goals: build

主要的构建产物将位于 :file:`build/zephyr` 中；:file:`build/zephyr/zephyr.elf` 是 blinky 应用的 ELF 格式二进制文件。根据开发板的不同，可能还会存在其他二进制格式、反汇编文件和 map 文件。

:zephyr_file:`samples` 目录中的其他示例应用记录在 :zephyr:code-sample-category:`samples` 中。

.. note:: 如果你想为其他开发板或应用重用现有的构建目录，需要在 ``west build`` 中添加参数 ``-p=auto``，以清除上一次构建的设置和产物。

通过烧录到开发板运行应用
========================

Zephyr 支持的大多数硬件开发板都可以通过运行 ``west flash`` 来烧录。这可能需要安装和配置开发板专用的工具才能正常工作。

更多细节请参阅 :ref:`application_run` 以及 :ref:`boards` 中你所使用开发板的文档。

.. _setting-udev-rules:

设置 udev 规则
==============

烧录开发板需要对开发板硬件的直接访问权限，通常由烧录工具的安装过程来管理。在 Linux 系统中，如果 ``west flash`` 命令失败，你很可能需要定义 udev 规则来授予所需的访问权限。

udev 是 Linux 内核的设备管理器，udev 守护进程处理硬件设备加入（或移出）系统时引发的所有用户空间事件。我们可以添加一个规则文件，为非 root 用户授予访问某些 USB 连接设备的权限。

OpenOCD（On-Chip Debugger）项目提供了一份规则文件，其中为大多数 Zephyr 支持的基于 Arm 的开发板定义了开发板专用规则，因此我们建议安装这份规则文件：可以从其 sourceforge 仓库下载，或者在你已安装 Zephyr SDK 时，SDK 文件夹中也有一份该规则文件的副本：

* 下载 OpenOCD 规则文件并将其复制到正确位置::

     wget -O 60-openocd.rules https://sf.net/p/openocd/code/ci/master/tree/contrib/60-openocd.rules?format=raw
     sudo cp 60-openocd.rules /etc/udev/rules.d

* 或者从 Zephyr SDK 文件夹复制该规则文件::

     sudo cp ${ZEPHYR_SDK_INSTALL_DIR}/sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d

然后，无论采用哪种方式，都让 udev 守护进程重新加载这些规则::

   sudo udevadm control --reload

拔下并重新插入开发板的 USB 连接，这样你就应该有权访问开发板硬件进行烧录。如果需要更多信息，请查看开发板专用文档（:ref:`boards`）。

在 QEMU 中运行应用
==================

当目标架构为 x86 或 ARM Cortex-M3 时，你可以在主机系统上使用 `QEMU <https://www.qemu.org/>`_ 以仿真方式运行 Zephyr 应用。QEMU 随 Zephyr SDK 一起提供。

如果手动安装 QEMU，请确保它位于系统 ``PATH`` 环境变量中。

``QEMU_BIN_PATH`` 可用作可选覆盖项，用于指定 Twister 使用的 QEMU 二进制文件位置。提供该变量时，Twister 会验证指定的路径是否存在。否则，Twister 将依赖 SDK 或其他 QEMU 发现机制。

例如，你可以使用 x86 仿真开发板配置（``qemu_x86``）构建并运行 :zephyr:code-sample:`hello_world` 示例，命令如下：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :host-os: unix
   :board: qemu_x86
   :goals: build run

要退出 QEMU，请键入 :kbd:`Ctrl-a`，然后键入 :kbd:`x`。

使用 ``qemu_cortex_m3`` 以仿真 Arm Cortex-M3 目标运行示例。

.. _gs_native:

以原生方式运行示例应用（Linux）
===============================

你可以编译一些示例，使其作为主机程序在 Linux 上运行。更多信息请参阅 :zephyr:board:`native_sim`。在 64 位主机操作系统上，你需要安装 32 位 C 库，或针对 :ref:`native_sim/native/64<native_sim32_64>` 进行构建。

首先，为 ``native_sim`` 构建 Hello World。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :host-os: unix
   :board: native_sim
   :goals: build

接下来，运行该应用。

.. code-block:: console

   west build -t run
   # or just run zephyr.exe directly:
   ./build/zephyr/zephyr.exe

按 :kbd:`Ctrl-C` 退出。

你可以运行 ``./build/zephyr/zephyr.exe --help`` 来获取可用选项列表。

你可以使用 gdb 或 valgrind 等标准工具对该可执行文件进行插桩分析。

.. rubric:: 脚注

.. [#pip]

   pip 是 Python 的软件包安装程序。它的 ``install`` 命令会首先尝试复用你计算机上已安装的软件包和软件包依赖项。如果无法复用，``pip install`` 会从互联网上的 Python Package Index（PyPI）下载它们。

   Zephyr 的 :file:`requirements.txt` 所要求的软件包版本可能会与你系统中的其他依赖要求冲突，此时你可能需要为 Zephyr 开发设置一个 virtualenv。

.. [#board_misnomer]

   随着时间的推移，这个称呼已经有些名不副实。虽然目标可以是、而且往往是运行在专用硬件开发板上的微处理器，但 Zephyr 还支持使用 QEMU 以仿真方式运行面向其他架构构建的目标，支持那些生成原生主机系统二进制文件、并通过 POSIX API 实现 Zephyr 驱动程序接口的目标，甚至支持在同一块物理芯片的不同架构 CPU 核上运行不同的基于 Zephyr 的二进制文件。这些硬件配置中的每一种都被称为“开发板”，尽管这一称呼在具体语境中并不总是完全说得通。

.. _information on -\\-user:
 https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site
.. _Homebrew disables -\\-user:
 https://docs.brew.sh/Homebrew-and-Python#note-on-pip-install---user
.. _Installing Packages:
 https://packaging.python.org/tutorials/installing-packages/
