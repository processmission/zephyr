.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _sca:

静态代码分析（SCA）
###################

Zephyr 通过 CMake 支持静态代码分析工具。

构建设置 :makevar:`ZEPHYR_SCA_VARIANT` 用于指定静态分析工具，也支持将 :envvar:`ZEPHYR_SCA_VARIANT` 设置为 :ref:`环境变量 <env_vars>`。

使用 ``-DZEPHYR_SCA_VARIANT=<tool>`` 启用工具，例如 ``-DZEPHYR_SCA_VARIANT=sparse`` 启用 ``sparse``。

.. _sca_infrastructure:

静态分析工具基础设施
********************

工具支持实现在 :file:`sca.cmake` 中，:file:`sca.cmake` 必须位于 :file:`{SCA_ROOT}/cmake/sca/{tool}/sca.cmake`。Zephyr 自身始终加入 :makevar:`SCA_ROOT`，构建系统也允许向 :makevar:`SCA_ROOT` 添加其他目录。

创建以下结构，即可支持源码树外的静态分析工具：

.. code-block:: none

   <sca_root>/                 # Custom SCA root
   └── cmake/
       └── sca/
           └── <tool>/         # Name of SCA tool, this is the value given to ZEPHYR_SCA_VARIANT
               └── sca.cmake   # CMake code that configures the tool to be used with Zephyr

要在 ``/path/to/my_tools/cmake/sca`` 下添加 ``foo``，请创建以下结构：

.. code-block:: none

   /path/to/my_tools
            └── cmake/
                └── sca/
                    └── foo/
                        └── sca.cmake

随后指定 ``-DZEPHYR_SCA_VARIANT=foo``，即可使用 ``foo`` 进行静态分析。

记得将 ``/path/to/my_tools`` 加入 :makevar:`SCA_ROOT`。

:makevar:`SCA_TOOL` 可以通过 ``-DSCA_ROOT=<sca_root>`` 设为普通 CMake 设置，也可以由 Zephyr 模块在 :file:`module.yml` 中添加，参见 :ref:`Zephyr 模块——构建设置 <modules_build_settings>`。

编译器与链接器启动器
====================

需要观察或包装编译和链接命令的静态分析工具，应在 :file:`sca.cmake` 中设置 ``CMAKE_<LANG>_COMPILER_LAUNCHER`` 和 ``CMAKE_<LANG>_LINKER_LAUNCHER``。必须将其设为普通变量，而非缓存条目。

如此设置的启动器会替换先前配置的任何启动器，包括 ``ccache``。如果工具是透明包装器，即原样执行收到的命令，则可通过追加方式保留原启动器：

.. code-block:: cmake

   set(CMAKE_C_COMPILER_LAUNCHER ${my_wrapper} ${CMAKE_C_COMPILER_LAUNCHER})

.. _sca_native_tools:

原生静态分析工具支持
********************

以下列出 Zephyr 构建系统原生支持的静态分析工具。

.. toctree::
   :maxdepth: 1
   :glob:

   *
