.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _toolchain_zephyr_sdk:

Zephyr SDK
##########

Zephyr 软件开发工具包（SDK）为 Zephyr 支持的各架构提供 GNU 和 LLVM 工具链，还包含定制 QEMU、OpenOCD 等主机工具。

强烈建议使用 Zephyr SDK，在某些情况下甚至是必需的（例如在某些架构上通过 QEMU 运行测试）。

支持的架构
**********

Zephyr SDK 支持以下目标架构：

* ARC（32 位和 64 位；ARCv1、ARCv2、ARCv3）
* ARM（32 位和 64 位；ARMv6、ARMv7、ARMv8；A/R/M 配置）
* Microblaze（32 位）
* MIPS（32 位和 64 位）
* RISC-V（32 位和 64 位；RV32I、RV32E、RV64I）
* RX
* SPARC（32 位和 64 位；SPARC V8、SPARC V9）
* x86（32 位和 64 位）
* Xtensa

.. _toolchain_zephyr_sdk_bundle_variables:

安装套件与变量
**************

Zephyr SDK 套件支持 Linux、macOS 和 Windows 等主要操作系统，以压缩文件形式分发。

为方便分发，SDK 提供三种预打包变体可供下载：

.. list-table:: SDK 套件变体
   :widths: 20 20 60
   :header-rows: 1

   * - 变体
     - 主机工具
     - 所含工具链
   * - ``gnu``
     - 是
     - 适用于所有受支持架构的 GNU 工具（Binutils、GCC 和 GDB）
   * - ``llvm``
     - 是
     - LLVM/Clang
   * - ``minimal``
     - 是
     - 无

安装过程包括解压下载的套件，并运行其中的安装脚本。

无论下载哪个套件，安装时都会询问需要安装哪些工具链。如果运行安装脚本的本地目录中找不到所选工具链，会在安装过程中下载。也可以将 GNU 和 LLVM SDK 套件都下载并解压到同一个目录树，从而同时安装两者，而无需在运行安装脚本时再下载。

各操作系统的附加说明见以下各节。

未选择工具链时，构建系统会查找 Zephyr SDK 并使用其中的工具链。将环境变量 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为 ``zephyr`` 可强制采用此方式。

如果将 Zephyr SDK 安装在默认位置之外（默认位置见下方各操作系统说明），又希望能够自动发现它，则必须运行安装脚本，将 SDK 注册到 CMake 包注册表。如果不注册，可使用 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 指向 SDK 安装目录。

也可以将 :envvar:`ZEPHYR_SDK_INSTALL_DIR` 指向包含多个 Zephyr SDK 的目录，以自动选择工具链。例如，将 ``ZEPHYR_SDK_INSTALL_DIR`` 设为 ``/company/tools``，其中 ``company/tools`` 包含以下子目录：

* ``/company/tools/zephyr-sdk-0.13.2``
* ``/company/tools/zephyr-sdk-a.b.c``
* ``/company/tools/zephyr-sdk-x.y.z``

这样既可以将多个 Zephyr SDK 集中存放在指定路径，也能让构建系统选择正确版本。

.. _toolchain_zephyr_sdk_compatibility:

Zephyr SDK 版本兼容性
*********************

一般而言，本页引用的 Zephyr SDK 版本可视为对应 Zephyr 版本的推荐版本。

完整的 Zephyr 与 SDK 版本兼容列表见 `Zephyr SDK Version Compatibility Matrix`_。

.. _toolchain_zephyr_sdk_install:

安装 Zephyr SDK
***************

.. toolchain_zephyr_sdk_install_start

.. note:: 如有需要，可以将以下说明中的 |sdk-version-literal| 换成其他版本；所有可用 SDK 版本见 `Zephyr SDK Releases`_ 页面。

.. note:: 以下说明使用 Zephyr GNU SDK 套件安装，其中包含所有受支持架构的 GNU 工具链及主机工具。使用 Zephyr LLVM SDK 套件时，将套件文件名中的 ``_gnu`` 后缀替换为 ``_llvm``。

.. note:: 卸载 SDK 时，只需删除其安装目录。

.. tabs::

   .. group-tab:: Linux

      .. _linux_zephyr_sdk:

      #. 下载并验证 `Zephyr SDK bundle`_：

         .. parsed-literal::

            cd ~
            wget |sdk-url-linux|
            wget -O - |sdk-url-linux-sha| | shasum --check --ignore-missing

         如果主机架构是 64 位 ARM，例如 Raspberry Pi，请将 ``x86_64`` 替换为 ``aarch64``，下载 64 位 ARM Linux SDK。

      #. 解压 Zephyr SDK 套件：

         .. parsed-literal::

            tar xvf zephyr-sdk- |sdk-version-trim| _linux-x86_64_gnu.tar.xz

         .. note::
            建议将 Zephyr SDK 套件解压到以下某个位置：

            * ``$HOME``
            * ``$HOME/.local``
            * ``$HOME/.local/opt``
            * ``$HOME/bin``
            * ``/opt``
            * ``/usr/local``

            SDK 套件压缩包包含 ``zephyr-sdk-<version>`` 目录，因此解压到 ``$HOME`` 后，安装路径为 ``$HOME/zephyr-sdk-<version>``。

      #. 运行 Zephyr SDK 套件安装脚本：

         .. parsed-literal::

            cd zephyr-sdk- |sdk-version-ltrim|
            ./setup.sh

         .. note::
            解压 Zephyr SDK 套件后，只需运行一次安装脚本。

            首次设置后，如果移动了 Zephyr SDK 套件目录，必须重新运行安装脚本。

      #. 安装 `udev <https://en.wikipedia.org/wiki/Udev>`_ 规则，以便普通用户烧录大多数 Zephyr 开发板：

         .. parsed-literal::

            sudo cp ~/zephyr-sdk- |sdk-version-trim| /hosttools/sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d
            sudo udevadm control --reload

   .. group-tab:: macOS

      .. _macos_zephyr_sdk:

      #. 下载并验证 `Zephyr SDK bundle`_：

         .. parsed-literal::

            cd ~
            curl -L -O |sdk-url-macos|
            curl -L |sdk-url-macos-sha| | shasum --check --ignore-missing

      #. 解压 Zephyr SDK 套件：

         .. parsed-literal::

            tar xvf zephyr-sdk- |sdk-version-trim| _macos-aarch64_gnu.tar.xz

         .. note::
            建议将 Zephyr SDK 套件解压到以下某个位置：

            * ``$HOME``
            * ``$HOME/.local``
            * ``$HOME/.local/opt``
            * ``$HOME/bin``
            * ``/opt``
            * ``/usr/local``

            SDK 套件压缩包包含 ``zephyr-sdk-<version>`` 目录，因此解压到 ``$HOME`` 后，安装路径为 ``$HOME/zephyr-sdk-<version>``。

      #. 运行 Zephyr SDK 套件安装脚本：

         .. parsed-literal::

            cd zephyr-sdk- |sdk-version-ltrim|
            ./setup.sh

         .. note::
            解压 Zephyr SDK 套件后，只需运行一次安装脚本。

            首次设置后，如果移动了 Zephyr SDK 套件目录，必须重新运行安装脚本。

   .. group-tab:: Windows

      .. _windows_zephyr_sdk:

      #. **以普通用户身份** 打开 ``cmd.exe`` 终端窗口。

      #. 下载 `Zephyr SDK bundle`_：

         .. parsed-literal::

            cd %HOMEPATH%
            wget |sdk-url-windows|

      #. 解压 Zephyr SDK 套件：

         .. parsed-literal::

            7z x zephyr-sdk- |sdk-version-trim| _windows-x86_64_gnu.7z

         .. note::
            建议将 Zephyr SDK 套件解压到以下某个位置：

            * ``%HOMEPATH%``
            * ``%PROGRAMFILES%``

            SDK 套件压缩包包含 ``zephyr-sdk-<version>`` 目录，因此解压到 ``%HOMEPATH%`` 后，安装路径为 ``%HOMEPATH%\zephyr-sdk-<version>``。

      #. 运行 Zephyr SDK 套件安装脚本：

         .. parsed-literal::

            cd zephyr-sdk- |sdk-version-ltrim|
            setup.cmd

         .. note::
            解压 Zephyr SDK 套件后，只需运行一次安装脚本。

            首次设置后，如果移动了 Zephyr SDK 套件目录，必须重新运行安装脚本。

.. _Zephyr SDK Releases: https://github.com/zephyrproject-rtos/sdk-ng/tags
.. _Zephyr SDK Version Compatibility Matrix: https://github.com/zephyrproject-rtos/sdk-ng/wiki/Zephyr-Version-Compatibility#zephyr-sdk-version-compatibility-matrix

.. toolchain_zephyr_sdk_install_end
