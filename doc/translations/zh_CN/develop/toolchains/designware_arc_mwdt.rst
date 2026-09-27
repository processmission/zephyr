.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _toolchain_designware_arc_mwdt:

DesignWare ARC MetaWare 开发工具包（MWDT）
##########################################

#. 主机上需要安装 `ARC MWDT <https://www.synopsys.com/dw/ipdir.php?ds=sw_metaware>`_。

#. 主机上需要安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>`。

   .. note::
      Zephyr SDK 提供设备树编译器（DTC）、QEMU 等工具。即使使用 ARC MWDT 构建 Zephyr RTOS，设备树预处理和 ``.bin`` 文件生成等步骤仍可能使用 GNU 预处理器与 GNU objcopy。这里也使用 Zephyr SDK 提供这些 ARC GNU 工具。请使用完整或最小 SDK 套件设置 ARC GNU 工具链，不要手动安装单独压缩包。套件会在系统中安装并注册工具链和主机工具，避免构建 Zephyr 时出现工具链相关问题。

#. :ref:`设置以下环境变量 <env_vars>`：

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为 ``arcmwdt``。
   - 将 :envvar:`ARCMWDT_TOOLCHAIN_PATH` 设为工具链安装目录。MWDT 安装会提供 :envvar:`METAWARE_ROOT`，因此只需将 :envvar:`ARCMWDT_TOOLCHAIN_PATH` 设为 ``$METAWARE_ROOT/../`` （Linux）或 ``%METAWARE_ROOT%\..\`` （Windows）。

   .. tip::
      如果机器上只安装了一个版本的 ARC MWDT，可以不设置 :envvar:`ARCMWDT_TOOLCHAIN_PATH`，系统会自动检测。

#. 按照以下 shell 会话示例检查当前环境变量是否正确设置；系统上的 :envvar:`ARCMWDT_TOOLCHAIN_PATH` 值可能不同。

   .. code-block:: console

      # Linux:
      $ echo $ZEPHYR_TOOLCHAIN_VARIANT
      arcmwdt
      $ echo $ARCMWDT_TOOLCHAIN_PATH
      /home/you/ARC/MWDT_2023.03/

      # Windows:
      > echo %ZEPHYR_TOOLCHAIN_VARIANT%
      arcmwdt
      > echo %ARCMWDT_TOOLCHAIN_PATH%
      C:\ARC\MWDT_2023.03\
