.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _toolchain_armclang:

Arm Compiler 6
##############

#. 下载并安装适用于当前操作系统、包含 `Arm Compiler 6`_ 的开发套件。

#. :ref:`设置以下环境变量 <env_vars>`：

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为 ``armclang``。
   - 将 :envvar:`ARMCLANG_TOOLCHAIN_PATH` 设为工具链安装目录。

#. Arm Compiler 6 需要通过 :envvar:`ARMLMD_LICENSE_FILE` 环境变量指定许可证文件或服务器。

例如：

   .. code-block:: bash

      # Linux, macOS, license file:
      export ARMLMD_LICENSE_FILE=/<path>/license_armds.dat
      # Linux, macOS, license server:
      export ARMLMD_LICENSE_FILE=8224@myserver

   .. code-block:: batch

      # Windows, license file:
      set ARMLMD_LICENSE_FILE=c:\<path>\license_armds.dat
      # Windows, license server:
      set ARMLMD_LICENSE_FILE=8224@myserver

#. 如果 Arm Compiler 6 随 Arm Development Studio 安装，还必须将 :envvar:`ARM_PRODUCT_DEF` 指向产品定义文件，参见 `Product and toolkit configuration <https://developer.arm.com/tools-and-software/software-development-tools/license-management/resources/product-and-toolkit-configuration>`_。例如，Arm Development Studio 安装在 ``/opt/armds-2020-1``，且使用 Gold 许可证时，应将 :envvar:`ARM_PRODUCT_DEF` 指向 ``/opt/armds-2020-1/gold.elmap``。

   .. note::

      Arm Compiler 6 使用 ``armlink`` 链接，与适用于 GNU ld 的 Zephyr 链接器脚本模板不兼容。Zephyr 对 Arm Compiler 6 的支持使用 CMake 链接器脚本生成器，可生成 scatter 文件。目前已具备基本 scatter 文件支持，但 ld 模板覆盖的部分功能尚未被 CMake 生成器完整支持。

      某些 Zephyr 子系统或模块可能包含依赖 GNU 内建特性的 C 或汇编代码，尚未更新到完全兼容 ``armclang``。

.. _Arm Compiler 6: https://developer.arm.com/tools-and-software/embedded/arm-compiler/downloads/version-6
