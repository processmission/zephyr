.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _toolchain_gnuarmemb:

GNU Arm Embedded
################

#. 下载适用于当前操作系统的 `GNU Arm Embedded`_，并解压到文件系统中。

   .. note::

      在 Windows 上，本指南假定安装到 :file:`C:\\gnu_arm_embedded`。也可以使用 ARM GCC 安装程序的默认路径，但需要相应调整以下指南中的路径。

   .. warning::

      在 macOS Catalina 及之后版本上，可能需要 :ref:`修改安全策略 <mac-gatekeeper>`，才能从终端运行工具链。

#. :ref:`设置以下环境变量 <env_vars>`：

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为 ``gnuarmemb``。
   - 将 :envvar:`GNUARMEMB_TOOLCHAIN_PATH` 设为工具链安装目录。

#. 按照以下 shell 会话示例检查当前环境变量是否正确设置；系统上的 :envvar:`GNUARMEMB_TOOLCHAIN_PATH` 值可能不同。

   .. code-block:: console

      # Linux, macOS:
      $ echo $ZEPHYR_TOOLCHAIN_VARIANT
      gnuarmemb
      $ echo $GNUARMEMB_TOOLCHAIN_PATH
      /home/you/Downloads/gnu_arm_embedded

      # Windows:
      > echo %ZEPHYR_TOOLCHAIN_VARIANT%
      gnuarmemb
      > echo %GNUARMEMB_TOOLCHAIN_PATH%
      C:\gnu_arm_embedded

   .. warning::

      在 macOS 上，如果上述步骤遇到问题，可以尝试 brew 中的非官方软件包。运行 ``brew install gcc-arm-embedded``，并配置变量。

      - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为 ``gnuarmemb``。
      - 将 :envvar:`GNUARMEMB_TOOLCHAIN_PATH` 设为 brew 安装目录，例如 ``/usr/local``。

.. _GNU Arm Embedded: https://developer.arm.com/open-source/gnu-toolchain/gnu-rm
