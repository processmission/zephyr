.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _toolchain_intel_oneapi_toolkit:

Intel oneAPI 工具包
###################

#. 下载 `Intel oneAPI Base Toolkit <https://software.intel.com/content/www/us/en/develop/tools/oneapi/all-toolkits.html>`_。

#. 假定工具包安装在 ``/opt/intel/oneApi``，使用以下命令设置环境::

        # Linux, macOS:
        export ONEAPI_TOOLCHAIN_PATH=/opt/intel/oneapi
        source $ONEAPI_TOOLCHAIN_PATH/compiler/latest/env/vars.sh

        # Windows:
        > set ONEAPI_TOOLCHAIN_PATH=C:\Users\Intel\oneapi

   设置完整 oneApi 环境，请使用::

        source  /opt/intel/oneapi/setvars.sh

   上述操作还会将 Python 环境切换为工具链使用的环境，可能与 Zephyr 使用的环境冲突。

#. 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为 ``oneApi``。
