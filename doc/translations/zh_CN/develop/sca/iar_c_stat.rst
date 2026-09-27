.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _icstat:

IAR C-STAT 支持
###############

`IAR C-STAT <https://iar.com/cstat>`__ 是全面的 C/C++ 源码静态分析工具，可发现错误和漏洞，支持 MISRA C、MISRA C++、CERT C/C++ 和 CWE 等多种编码标准。

安装 IAR C-STAT
***************

IAR C-STAT 随 IAR Build Tools 和 IAR Embedded Workbench 预装，详情见对应产品文档。

使用 IAR C-STAT 构建
********************

运行 IAR C-STAT 需要 CMake 4.1.0 或更新版本。使用 :ref:`west build <west-building>` 构建时，追加 ``-DZEPHYR_SCA_VARIANT=iar_c_stat`` 选择该工具，例如：

.. zephyr-app-commands::
   :zephyr-app: samples/basic/blinky
   :board: stm32f429ii_aca
   :gen-args: -DZEPHYR_SCA_VARIANT=iar_c_stat
   :goals: build
   :compact:

配置 IAR C-STAT
***************

IAR C-STAT 接受用于定制分析的参数，下表列出支持的选项。

.. list-table::
   :header-rows: 1

   * - 参数
     - 描述
   * - ``CSTAT_RULESET``
     - 要使用的预定义规则集。默认值为 ``stdchecks``，可用值为 ``all,cert,misrac2004,misrac2012,misrac++2008,stdchecks,security``。
   * - ``CSTAT_ANALYZE_THREADS``
     - 分析使用的线程数。（默认值：<CPU count>）
   * - ``CSTAT_ANALYZE_OPTS``
     - 直接传给 ``analyze`` 命令的参数，例如 ``--timeout=900;--deterministic;--fpe``。
   * - ``CSTAT_DB``
     - 覆盖 C-STAT SQLite 数据库的默认位置，例如 ``/home/user/cstat.db``。
   * - ``CSTAT_CLEANUP``
     - 清理 C-STAT SQLite 数据库，例如 ``true``。

这些参数可以通过命令行传递，也可以设置为环境变量。以下示例展示如何按需启用和组合非标准规则集：

.. zephyr-app-commands::
   :zephyr-app: samples/basic/blinky
   :board: stm32f429ii_aca
   :gen-args: -DZEPHYR_SCA_VARIANT=iar_c_stat -DCSTAT_RULESET=misrac2012,cert
   :goals: build
