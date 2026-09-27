.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _toolchain_iar_arm:

IAR Arm 工具链
##############

#. 在主机上下载安装 v9.70 或更新版本的 `IAR Arm Toolchain`_，可以是 IAR Embedded Workbench 或 IAR Build Tools，采用永久或订阅许可。

#. 确保主机上已安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>`。

#. :ref:`设置以下环境变量 <env_vars>`：

    - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为 ``iar``。
    - 将 :envvar:`IAR_TOOLCHAIN_PATH` 设为工具链安装目录。

#. IAR 工具链的云许可变体需要将 :envvar:`IAR_LMS_BEARER_TOKEN` 环境变量设为有效的 ``license bearer token``，用于订阅许可。

例如：

.. code-block:: bash

    # Linux (default installation path):
    export IAR_TOOLCHAIN_PATH=/opt/iar/cxarm-<version>/arm
    export ZEPHYR_TOOLCHAIN_VARIANT=iar
    export IAR_LMS_BEARER_TOKEN="<BEARER-TOKEN>"

.. code-block:: batch

    # Windows:
    set IAR_TOOLCHAIN_PATH=c:\<path>\cxarm-<version>\arm
    set ZEPHYR_TOOLCHAIN_VARIANT=iar
    set IAR_LMS_BEARER_TOKEN="<BEARER-TOKEN>"

.. note::

    已知限制：

    - IAR 工具链使用 ``ilink`` 链接，并依赖 Zephyr 的 CMAKE_LINKER_GENERATOR。``ilink`` 与适用于 GNU ld 的 Zephyr 链接器脚本模板不兼容。

    - ``.S-files`` 使用 Zephyr SDK 附带的 GNU 汇编器。

    - C 库仅支持 ``Minimal libc``，不支持 C++。

    - 某些 Zephyr 子系统或模块可能包含依赖 GNU 内建特性的 C 或汇编代码，尚未更新到完全兼容 ``iar``。

    - 不支持 TrustedFirmware。

.. _IAR Arm Toolchain: https://www.iar.com/products/architectures/arm/
