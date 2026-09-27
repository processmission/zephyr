.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _getting_started:

入门指南
########

按照本指南可以：

- 在 Ubuntu、macOS 或 Windows 上搭建 Zephyr 命令行开发环境（其他 Linux 发行版的安装说明见 :ref:`installation_linux`）
- 获取源代码
- 构建、烧录并运行示例应用

.. _host_setup:

选择并更新操作系统
******************

点击你正在使用的操作系统。

.. tabs::

   .. group-tab:: Ubuntu

      本指南适用于 Ubuntu 24.04 LTS 及更高版本。如果你使用其他 Linux 发行版，请参阅 :ref:`installation_linux`。

      .. code-block:: bash

         sudo apt update
         sudo apt upgrade

   .. group-tab:: macOS

      选择 :menuselection:`System Settings --> General --> Software Update` 并安装所有可用更新。更多细节参见 `this Apple support topic <https://support.apple.com/en-us/HT201541>`_。

      .. note::

         不支持 x86-64 版 macOS。

   .. group-tab:: Windows

      选择 :menuselection:`Start --> Settings --> Update & Security --> Windows Update`，点击 :guilabel:`Check for updates` 并安装所有可用更新。

.. _install-required-tools:

安装依赖
********

接下来安装 Zephyr 配置和构建应用所需的主机工具。下面的说明使用各操作系统推荐的包管理器，安装后即可在终端中使用这些工具。

主要依赖当前要求的最低版本如下：

.. list-table::
   :header-rows: 1

   * - 工具
     - 最低版本

   * - `CMake <https://cmake.org/>`_
     - 3.28.0

   * - `Python <https://www.python.org/>`_
     - 3.12

   * - `Devicetree 编译器 <https://www.devicetree.org/>`_
     - 1.4.6

.. note::

   强烈建议使用 Python 3.12。使用更新的 Python 版本在某些系统上可能会失败，例如在 Windows 上安装所需软件包时。

.. tabs::

   .. group-tab:: Ubuntu

      .. _install_dependencies_ubuntu:

      #. 使用 ``apt`` 安装所需依赖：

         .. code-block:: bash

            sudo apt install --no-install-recommends git cmake ninja-build gperf \
              ccache dfu-util device-tree-compiler wget python3-dev python3-venv python3-tk \
              xz-utils file make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1

         .. note::

            由于 AArch64（ARM64）系统上没有 ``gcc-multilib`` 和 ``g++-multilib``，你可能需要把它们从待安装的软件包列表中移除。

      #. 输入以下命令，确认系统中已安装的主要依赖版本：

         .. code-block:: bash

            cmake --version
            python3 --version
            dtc --version

         将这些版本与本节开头表格中的版本进行对比。有关手动更新依赖的更多信息，请参阅 :ref:`installation_linux` 页面。

   .. group-tab:: macOS

      .. _install_dependencies_macos:

      #. 安装 `Homebrew <https://brew.sh/>`_：

         .. code-block:: bash

            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

      #. Homebrew 安装脚本执行完成后，按照屏幕提示将 Homebrew 加入 PATH。

         .. code-block:: bash

            (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> ~/.zprofile
            source ~/.zprofile

      #. 使用 ``brew`` 安装所需依赖：

         .. code-block:: bash

            brew install cmake ninja gperf python3 python-tk ccache qemu dtc libmagic wget openocd

      #. 将 Homebrew 的 Python 目录加入 PATH，这样就可以直接执行 ``python``、``pip`` 以及 ``python3``、``pip3``。

           .. code-block:: bash

              (echo; echo 'export PATH="'$(brew --prefix)'/opt/python/libexec/bin:$PATH"') >> ~/.zprofile
              source ~/.zprofile

   .. group-tab:: Windows

      .. note::

         本节说明针对原生 Windows 环境。你也可以改用 `Windows Subsystem for Linux (WSL) <https://learn.microsoft.com/windows/wsl/install>`_，并按照本指南中的 Ubuntu 说明操作。此时需要注意，要在 WSL 中烧录和调试硬件，必须先把 USB 设备暴露给 WSL，例如使用 `usbipd-win <https://github.com/dorssel/usbipd-win>`_。

      在较新的 Windows（10 及更高版本）上，从 Microsoft Store 安装 Windows Terminal。下面的说明在 ``cmd.exe`` 和 PowerShell 中均适用。

      本节使用 Windows 官方包管理器 `winget`_。如果无法使用 winget，请从各依赖的官方网站下载安装，并确保它们的命令行工具已加入 :envvar:`PATH` :ref:`环境变量 <env_vars>`。

      |p|

      .. _install_dependencies_windows:

      #. 在较新的 Windows 版本中，winget 默认已经预装，可以在终端窗口中输入 ``winget`` 来确认。如果命令不可用，可以 `install winget`_。

      #. 打开命令提示符（``cmd.exe``）或 PowerShell 终端窗口。按下 Windows 键，输入 ``cmd.exe`` 或 PowerShell，然后点击搜索结果即可打开。

      #. 使用 ``winget`` 安装所需依赖：

         .. code-block:: bat

            winget install Kitware.CMake Ninja-build.Ninja oss-winget.gperf Python.Python.3.12 Git.Git oss-winget.dtc wget 7zip.7zip

      #. 关闭终端窗口。

      .. note::

         你可能需要将 7zip 的安装目录加入 ``PATH``。


.. _winget: https://learn.microsoft.com/en-us/windows/package-manager/
.. _install winget: https://aka.ms/getwinget

.. _get_the_code:
.. _clone-zephyr:
.. _install_py_requirements:
.. _gs_python_deps:

获取 Zephyr 并安装 Python 依赖
******************************

接下来使用 :ref:`west <west>` 创建工作区，并获取 Zephyr 及其 :ref:`模块 <modules>`。

下面的命令使用 :file:`zephyrproject` 作为工作区名称，你可以选择其他名称和位置。你还会把 Zephyr 的 Python 依赖安装到 `Python virtual environment`_ 中，使其与系统 Python 环境相互隔离。

.. _Python virtual environment: https://docs.python.org/3/library/venv.html

#. 创建新的虚拟环境：

   .. tabs::

      .. group-tab:: Ubuntu

         .. code-block:: bash

            python3 -m venv ~/zephyrproject/.venv

      .. group-tab:: macOS

         .. code-block:: bash

            python3 -m venv ~/zephyrproject/.venv

      .. group-tab:: Windows

         打开 ``cmd.exe`` 或 PowerShell 终端窗口（**以普通用户身份**）。

         .. tabs::

            .. code-tab:: bat

               cd %HOMEPATH%
               py -3.12 -m venv zephyrproject\.venv

            .. code-tab:: powershell

               cd $Env:HOMEPATH
               py -3.12 -m venv zephyrproject\.venv

#. 激活虚拟环境：

   .. tabs::

      .. group-tab:: Ubuntu

         .. code-block:: bash

            source ~/zephyrproject/.venv/bin/activate

      .. group-tab:: macOS

         .. code-block:: bash

            source ~/zephyrproject/.venv/bin/activate

      .. group-tab:: Windows

         .. note::

            在 PowerShell 中激活 Python 虚拟环境需要执行脚本，因此必须先允许执行脚本。

            .. code-block:: powershell

               Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

         .. tabs::

            .. code-tab:: bat

               zephyrproject\.venv\Scripts\activate.bat

            .. code-tab:: powershell

               zephyrproject\.venv\Scripts\Activate.ps1

   激活后命令提示符前会出现 ``(.venv)`` 前缀。随时可以通过运行 ``deactivate`` 退出虚拟环境。

   .. note::

      每次打开新的终端会话后，在使用 Zephyr 之前都要记得激活虚拟环境。否则 ``west`` 等命令会找不到，或运行在其他 Python 环境中，从而产生令人困惑的错误。

#. 安装 west：

   west 是 Zephyr 的工作区管理工具，接下来的命令将使用它创建和更新工作区。

   .. code-block:: shell

      pip install west

#. 获取 Zephyr 源代码：

   ``west init`` 会创建一个 :term:`west 工作区 <west workspace>`，并把 ``https://github.com/zephyrproject-rtos/zephyr`` 克隆为其 :term:`清单仓库 <west manifest repository>`。

   ``west update`` 随后会获取 Zephyr 的 :term:`west 清单 <west manifest>` 中列出的各个 :term:`west 项目 <west project>`，也就是前面提到的模块（例如硬件抽象层 HAL、各种库等）。

   .. tabs::

      .. group-tab:: Ubuntu

         .. only:: not release

            .. code-block:: bash

               west init -m https://github.com/zephyrproject-rtos/zephyr ~/zephyrproject
               cd ~/zephyrproject
               west update

         .. only:: release

            .. We need to use a parsed-literal here because substitutions do not work in code
               blocks. This means users can't copy-paste these lines as easily as other blocks but
               should be good enough still :)

            .. parsed-literal::

               west init -m https://github.com/zephyrproject-rtos/zephyr ~/zephyrproject --mr v |zephyr-version-ltrim|
               cd ~/zephyrproject
               west update

      .. group-tab:: macOS

         .. only:: not release

            .. code-block:: bash

               west init -m https://github.com/zephyrproject-rtos/zephyr ~/zephyrproject
               cd ~/zephyrproject
               west update

         .. only:: release

            .. parsed-literal::

               west init -m https://github.com/zephyrproject-rtos/zephyr ~/zephyrproject --mr v |zephyr-version-ltrim|
               cd ~/zephyrproject
               west update

      .. group-tab:: Windows

         .. only:: not release

            .. code-block:: bat

               west init -m https://github.com/zephyrproject-rtos/zephyr zephyrproject
               cd zephyrproject
               west update

         .. only:: release

            .. parsed-literal::

               west init -m https://github.com/zephyrproject-rtos/zephyr zephyrproject --mr v |zephyr-version-ltrim|
               cd zephyrproject
               west update

   .. tip::

      为了减少磁盘占用、避免在初始化时下载不需要的模块或厂商 HAL，可以在运行 ``west update`` 之前配置 :ref:`west-manifest-groups`。

#. 安装 Zephyr 的 Python 依赖：

   ``west packages`` 会从已检出的 Zephyr 工作区（包括其中的模块）读取 Python 依赖要求，因此安装的软件包与所获取的 Zephyr 版本一致。

   .. tabs::

      .. group-tab:: Ubuntu

         .. code-block:: bash

            west packages pip --install

      .. group-tab:: macOS

         .. code-block:: bash

            west packages pip --install

      .. group-tab:: Windows

         .. tabs::

            .. code-tab:: bat

               cmd /c zephyr\scripts\utils\west-packages-pip-install.cmd

            .. code-tab:: powershell

               python -m pip install @((west packages pip) -split ' ')

   .. note::

      安装这些依赖可能会升级或降级 west 本身。

#. 导出 :ref:`Zephyr CMake 包 <cmake_pkg>`。这会把当前的 Zephyr 检出注册到 CMake 的用户包注册表中，使 ``find_package(Zephyr)`` 在构建应用时能够自动找到它。

   .. code-block:: shell

      west zephyr-export

安装 Zephyr SDK
***************

:ref:`Zephyr 软件开发工具包（SDK） <toolchain_zephyr_sdk>` 包含 Zephyr 所支持的每种架构的工具链，其中包括为目标硬件构建 Zephyr 应用所需的编译器、汇编器、链接器以及其他程序。

它还包含额外的主机工具，例如用于仿真、烧录和调试 Zephyr 应用的定制 QEMU 和 OpenOCD。

在 Zephyr 仓库中通过 ``west sdk install`` 安装 Zephyr SDK：

.. tabs::

   .. group-tab:: Ubuntu

      .. code-block:: bash

         cd ~/zephyrproject/zephyr
         west sdk install

   .. group-tab:: macOS

      .. code-block:: bash

         cd ~/zephyrproject/zephyr
         west sdk install

   .. group-tab:: Windows

      .. tabs::

         .. code-tab:: bat

            cd %HOMEPATH%\zephyrproject\zephyr
            west sdk install

         .. code-tab:: powershell

            cd $Env:HOMEPATH\zephyrproject\zephyr
            west sdk install

.. tip::

   可以使用命令选项指定 SDK 的安装位置，或只安装选定架构的工具链。详情请运行 ``west sdk install --help``。

.. note::

    如果不想使用 ``west sdk`` 命令安装 Zephyr SDK，请参阅 :ref:`toolchain_zephyr_sdk_install`。

.. _getting_started_run_sample:

构建 Blinky 示例
****************

.. note::

   :zephyr:code-sample:`blinky` 兼容大多数 :ref:`开发板 <boards>`，但并非全部。如果你的开发板不满足 Blinky 的 :ref:`blinky-sample-requirements`，可以改用 :zephyr:code-sample:`hello_world`。

   如果不确定 west 使用的开发板名称，可以用 ``west boards`` 列出 Zephyr 支持的所有开发板。开发板的 :zephyr:board-catalog:`文档页面 <documentation page>` 也会给出传给 ``west build`` 的准确开发板目标名称。

使用 :ref:`west build <west-building>` 构建 :zephyr:code-sample:`blinky`。将 ``<your-board-name>`` 替换为你的开发板名称：

.. tabs::

   .. group-tab:: Ubuntu

      .. code-block:: bash

         cd ~/zephyrproject/zephyr
         west build -p always -b <your-board-name> samples/basic/blinky

   .. group-tab:: macOS

      .. code-block:: bash

         cd ~/zephyrproject/zephyr
         west build -p always -b <your-board-name> samples/basic/blinky

   .. group-tab:: Windows

      .. tabs::

         .. code-tab:: bat

            cd %HOMEPATH%\zephyrproject\zephyr
            west build -p always -b <your-board-name> samples\basic\blinky

         .. code-tab:: powershell

            cd $Env:HOMEPATH\zephyrproject\zephyr
            west build -p always -b <your-board-name> samples\basic\blinky

``-p always`` 选项会强制执行全新构建，清除之前配置留下的构建产物，在入门阶段可以避免残留文件造成干扰。之后可以使用 ``-p auto``，让 ``west build`` 自行判断何时需要全新构建。详情请运行 ``west build -h``。

.. note::

   一块开发板可能包含一个或多个 SoC，每个 SoC 又可能包含一个或多个 CPU 集群。为这类开发板构建时，需要指定示例要构建到哪个 SoC 或 CPU 集群。例如，要为 :zephyr:board:`nrf5340dk` 上的 ``cpuapp`` 核心构建 :zephyr:code-sample:`blinky`，开发板名称应写成：``nrf5340dk/nrf5340/cpuapp``。更多细节参见 :ref:`board_terminology`。

烧录示例
********

连接开发板（通常通过 USB），如果有电源开关请打开。如果不确定该如何操作，请查看 :ref:`开发板 <boards>` 中对应开发板的页面，因为某些开发板需要特定的设置或烧录步骤。

使用 :ref:`west flash <west-flashing>` 烧录示例。该命令会把刚构建好的应用烧写到已连接的开发板上：

.. code-block:: shell

   west flash

.. note::

    你可能需要为开发板安装额外的 :ref:`主机工具 <flash-debug-host-tools>`。如果缺少必需的依赖，``west flash`` 命令会报错。

.. note::

    在 Linux 上，首次通过调试探针烧录前可能需要配置 udev 规则，参见 :ref:`setting-udev-rules`。

如果使用的是 blinky，LED 会按下图所示开始闪烁：

.. figure:: img/ReelBoard-Blinky.webp
   :width: 400px
   :name: reelboard-blinky

   运行 blinky 的 Phytec :zephyr:board:`reel_board <reel_board>`

后续步骤
********

下面是进一步探索 Zephyr 的一些建议：

* 试用其他 :zephyr:code-sample-category:`示例 <samples>`
* 了解 :ref:`应用 <application>` 和 :ref:`west <west>` 工具
* 了解 west 的 :ref:`烧录与调试 <west-build-flash-debug>` 功能，或进一步了解一般的 :ref:`烧录与调试 <flashing_and_debugging>`
* 查看 :ref:`beyond-GSG`，了解更多环境搭建的替代方案与思路
* 了解如何通过 :ref:`project-resources` 获得 Zephyr 社区的帮助

.. _help:

寻求帮助
********

在寻求帮助之前，请先搜索本文档、Zephyr 项目的 GitHub discussions 与 issues，以及 Discord 聊天记录，你的问题可能已经有答案。你也可以使用每个文档页面都提供的 :ref:`聊天机器人 <kapa_ai>`。

* **邮件列表**：通常可以在 users@lists.zephyrproject.org 上求助。`Search archives and sign up here`_。
* **GitHub**：提问请使用 `GitHub discussions`_，报告缺陷和功能请求请使用 `GitHub issues`_。
* **Discord**：可通过 `Discord invite`_ 加入。

寻求帮助时，请附上：

#. 你想做什么
#. 你尝试过什么，包括运行过的命令
#. 实际结果如何，包括完整的文本输出

请复制并粘贴文本，不要直接发截图。在 Discord 或 GitHub 上，如果终端输出、源代码或日志超过 5 行，请用三个反引号创建代码块。

.. _Search archives and sign up here: https://lists.zephyrproject.org/g/users
.. _GitHub discussions: https://github.com/zephyrproject-rtos/zephyr/discussions
.. _Discord invite: https://chat.zephyrproject.org
.. _GitHub issues: https://github.com/zephyrproject-rtos/zephyr/issues
