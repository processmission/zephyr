.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _other_x_compilers:

其他交叉编译器
##############

此工具链变体借鉴 Linux 内核构建系统的机制，通过 ``CROSS_COMPILE`` 环境变量设置基于 GNU 的交叉工具链。

这类“其他交叉编译器”包括 Linux 发行版打包的工具链、自行编译的工具链或从网络下载的工具链。与 :ref:`toolchains` 中明确列出的工具链不同，Zephyr 构建系统可能未对其进行测试，也不提供正式支持，但工具链设置机制本身受支持。

按照以下步骤使用这类工具链。

#. 安装适合主机和目标系统的交叉编译器。

   例如，在基于 Debian 的 Linux 上安装 ``gcc-arm-none-eabi``，或在 Fedora、Red Hat 上安装 ``arm-none-eabi-newlib``：

   .. code-block:: console

      # On Debian or Ubuntu
      sudo apt-get install gcc-arm-none-eabi
      # On Fedora or Red Hat
      sudo dnf install arm-none-eabi-newlib

#. :ref:`设置以下环境变量 <env_vars>`：

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为 ``cross-compile``。
   - 将 ``CROSS_COMPILE`` 设为工具链二进制文件的公共路径前缀，例如编译器所在目录加上目标三元组和结尾的连字符。

#. 按照以下 shell 会话示例检查当前环境变量是否正确设置；系统上的 ``CROSS_COMPILE`` 值可能不同。

   .. code-block:: console

      # Linux, macOS:
      $ echo $ZEPHYR_TOOLCHAIN_VARIANT
      cross-compile
      $ echo $CROSS_COMPILE
      /usr/bin/arm-none-eabi-

   也可以将 ``CROSS_COMPILE`` 设为 CMake 变量。

采用此方式时，所有工具链二进制文件必须位于同一目录，且具有共同的文件名前缀。``CROSS_COMPILE`` 为目录与文件名前缀的拼接。上述 Debian 示例中，``gcc-arm-none-eabi`` 包将 ``arm-none-eabi-gcc``、``arm-none-eabi-ld`` 等安装在 ``/usr/bin/``，因此公共前缀为 ``/usr/bin/arm-none-eabi-``，包括末尾连字符 ``-``。如果工具链安装在 ``/opt/mytoolchain/bin``，文件名以目标三元组 ``myarch-none-elf`` 开头，则将 ``CROSS_COMPILE`` 设为 ``/opt/mytoolchain/bin/myarch-none-elf-``。
