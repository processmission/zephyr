.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _installation_linux:

安装 Linux 主机依赖
###################

以下 Linux 发行版提供了对应的安装说明：

* Ubuntu
* Fedora
* Clear Linux
* Arch Linux

对于非滚动发布的发行版，包管理器提供的某些依赖可能不满足要求。此时请按照文中给出的额外说明，从包管理器之外的来源获取所需软件。

.. note:: 如果你处于企业防火墙之后，可能需要先配置代理才能访问互联网。有些工具通过环境变量 ``http_proxy`` 和 ``https_proxy`` 获取代理设置，另一些工具（尤其是 ``apt`` 和 ``git``）则使用各自的配置文件。

更新操作系统
************

确保主机系统已更新到最新状态。

.. tabs::

   .. group-tab:: Ubuntu

      .. code-block:: console

         sudo apt-get update
         sudo apt-get upgrade

   .. group-tab:: Fedora

      .. code-block:: console

         sudo dnf upgrade

   .. group-tab:: Clear Linux

      .. code-block:: console

         sudo swupd update

   .. group-tab:: Arch Linux

      .. code-block:: console

         sudo pacman -Syu

.. _linux_requirements:

安装必需组件与依赖
******************

.. NOTE FOR DOCS AUTHORS: DO NOT PUT DOCUMENTATION BUILD DEPENDENCIES HERE.

   This section is for dependencies to build Zephyr binaries, *NOT* this
   documentation. If you need to add a dependency only required for building
   the docs, add it to doc/README.rst. (This change was made following the
   introduction of LaTeX->PDF support for the docs, as the texlive footprint is
   massive and not needed by users not building PDF documentation.)

注意：这些说明会同时安装 Ninja 和 Make，你只需要其中一种。

.. tabs::

   .. group-tab:: Ubuntu

      .. code-block:: console

         sudo apt-get install --no-install-recommends git cmake ninja-build gperf \
           ccache dfu-util device-tree-compiler wget \
           python3-dev python3-pip python3-setuptools python3-tk python3-wheel xz-utils file \
           make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1

   .. group-tab:: Fedora

      .. code-block:: console

         sudo dnf group install development-tools c-development
         sudo dnf install cmake ninja-build gperf dfu-util dtc wget which \
           python3-pip python3-tkinter xz file python3-devel SDL2-devel \
           libusb1-devel

   .. group-tab:: Clear Linux

      .. code-block:: console

         sudo swupd bundle-add c-basic dev-utils dfu-util dtc \
           os-core-dev python-basic python3-basic python3-tcl

      Clear Linux 侧重 **本机性能与安全性**，而不是交叉编译，因此它默认会向所有用户的 :ref:`环境 <env_vars>` 导出一组编译器和链接器标志，这会导致 Zephyr 的 CMake 构建系统产生警告甚至失败。要清除其中的 C/C++ 标志以修复 Zephyr 构建，请以 root 身份运行以下命令，然后注销并重新登录：

      .. code-block:: console

         echo 'unset CFLAGS CXXFLAGS' >> /etc/profile.d/unset_cflags.sh

      注意：该命令会清除 **系统中所有用户** 的 C/C++ 标志。每个 Linux 发行版的 bash 初始化文件加载顺序都不相同，往往比较复杂且可能变化，Clear Linux 也不例外。如果需要更灵活的方案，可以从 ``/usr/share/defaults/etc/profile`` 中的逻辑入手。

   .. group-tab:: Arch Linux

      .. code-block:: console

         sudo pacman -S git cmake ninja gperf ccache dfu-util dtc wget \
             python-pip python-setuptools python-wheel tk xz file make which

CMake
=====

需要 :ref:`较新的 CMake 版本 <install-required-tools>`。可用 ``cmake --version`` 查看当前版本。如果版本过旧，可以通过以下几种方式获取更新版本：

* 在 Ubuntu 上，可以按照 `kitware third-party apt repository <https://apt.kitware.com/>`_ 的说明，通过 apt 获取更新版本的 cmake。

* 从 CMake 项目网站下载并安装打包好的 cmake。（注意：这不会卸载旧版本的 cmake。）

  .. code-block:: console

     cd ~
     wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-Linux-x86_64.sh
     chmod +x cmake-3.21.1-Linux-x86_64.sh
     sudo ./cmake-3.21.1-Linux-x86_64.sh --skip-license --prefix=/usr/local
     hash -r

  如果安装脚本把 cmake 安装到了 PATH 中的新位置，可能需要执行 ``hash -r`` 命令刷新缓存。

* 从 `CMake Downloads`_ 页面下载并安装 CMake 项目提供的预编译二进制文件。例如，把 3.21.1 版安装到 :file:`~/bin/cmake`：

  .. code-block:: console

     mkdir $HOME/bin/cmake && cd $HOME/bin/cmake
     wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-Linux-x86_64.sh
     yes | sh cmake-3.21.1-Linux-x86_64.sh | cat
     echo "export PATH=$PWD/cmake-3.21.1-Linux-x86_64/bin:\$PATH" >> $HOME/.zephyrrc

* 使用 ``pip3``：

  .. code-block:: console

     pip3 install --user cmake

  注意：这不会卸载旧版本的 cmake，新版本会安装到 ~/.local/bin 目录，因此需要把 ~/.local/bin 加入 PATH。（详情见 :ref:`python-pip`。）

* 可以在你的发行版的测试版（beta）或不稳定版（unstable）软件仓库中查找更新。

* 在 Ubuntu 上还可以使用 snap 获取最新版本：

  .. code-block:: console

     sudo snap install cmake

更新 cmake 后，请用 ``cmake --version`` 确认找到的是新安装的版本。为避免冲突，你也可以卸载包管理器提供的 CMake。（可用 ``whereis cmake`` 查找其他已安装的版本。）

DTC（设备树编译器）
===================

需要 :ref:`较新的 DTC 版本 <install-required-tools>`。可用 ``dtc --version`` 查看当前版本。如果版本过旧，可以从源码构建安装较新的版本，或者安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>` 并使用其中自带的 DTC。

Python
======

需要 :ref:`较新的 Python 3 版本 <install-required-tools>`。可用 ``python3 --version`` 查看当前版本。

如果版本过旧，需要安装较新的 Python 3。可以从源码构建，也可以使用发行版软件源中提供的 backport（如果有）。建议将该 Python 隔离在虚拟环境中，以免影响系统自带的 Python。

.. _pyenv: https://github.com/pyenv/pyenv

安装 Zephyr 软件开发工具包（SDK）
*********************************

Zephyr 软件开发工具包（SDK）包含 Zephyr 所支持的每种架构的工具链，还包含定制 QEMU、OpenOCD 等额外的主机工具。

强烈建议使用 Zephyr SDK，在某些情况下甚至是必需的（例如在某些架构上通过 QEMU 运行测试）。

安装 SDK 请按照 :ref:`Zephyr SDK 安装指南 <linux_zephyr_sdk>` 中的 Linux 步骤操作。

.. _sdkless_builds:

在 Linux 上不使用 Zephyr SDK 进行构建
*************************************

提供 Zephyr SDK 是为了方便和易用。它包含所有 Zephyr 目标架构的工具链，构建应用或运行测试时无需额外参数；除交叉编译器外，还提供预编译的主机工具。不过，也可以不使用 SDK 工具链，改用 :ref:`工具链 <toolchains>` 一节中介绍的其他工具链进行构建。

如前所述，SDK 还包含预编译的主机工具。要在使用其他来源的工具链时同时使用 SDK 的预编译主机工具，必须把 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量设置为 Zephyr SDK 的安装目录；如果不使用 SDK 的预编译主机工具，则必须取消 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 的设置。

要确保该变量未设置，请运行：

.. code-block:: console

   unset ZEPHYR_SDK_INSTALL_DIR

.. _Zephyr SDK Releases: https://github.com/zephyrproject-rtos/sdk-ng/tags
.. _CMake Downloads: https://cmake.org/download
