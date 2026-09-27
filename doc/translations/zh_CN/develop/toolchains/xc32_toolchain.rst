.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _toolchain_xc32:

MPLAB XC32
##########

#. 下载并安装适用于当前操作系统的 `MPLAB XC32 Compiler`_。

#. :ref:`设置以下环境变量 <env_vars>`：

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为 ``xc32``。
   - 将 :envvar:`XC32_TOOLCHAIN_PATH` 设为工具链安装目录。

#. 按照以下 shell 会话示例检查当前环境变量是否正确设置；系统上的 :envvar:`XC32_TOOLCHAIN_PATH` 值可能不同。

   .. code-block:: console

      # Linux, macOS:
      $ echo $ZEPHYR_TOOLCHAIN_VARIANT
      xc32
      $ echo $XC32_TOOLCHAIN_PATH
      /opt/microchip/xc32/v5.00

      # Windows:
      > echo %ZEPHYR_TOOLCHAIN_VARIANT%
      xc32
      > echo %XC32_TOOLCHAIN_PATH%
      C:\Microchip\xc32\v5.00

#. 对于 Microchip SoC，将 :envvar:`XC_PACK_DIR` 设为已安装 Microchip 设备系列包（DFP）所在的根目录。

   .. note::

      Zephyr 通过 :envvar:`XC_PACK_DIR` 查找与所选 SoC 匹配的 DFP，并向 XC32 工具链传递所需的 ``-mdfp`` 和 ``-mprocessor`` 标志。

   例如：

   .. code-block:: console

      # Linux, macOS:
      $ export XC_PACK_DIR=/home/path/.packs/microchip

      # Windows:
      > set XC_PACK_DIR=C:\Users\path\.mchp_packs\Microchip

.. _MPLAB XC32 Compiler: https://www.microchip.com/en-us/tools-resources/develop/mplab-xc-compilers
