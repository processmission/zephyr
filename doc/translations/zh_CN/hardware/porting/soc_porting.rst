.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _soc_porting_guide:

SoC 移植指南
############

本页介绍如何为 Zephyr 添加对新 :term:`SoC` 的支持，既适用于上游 Zephyr 项目，也适用于你自己的本地仓库。

SoC 定义
********

本文假定你已熟悉 Zephyr 中的开发板概念。有关硬件支持层次结构和 Zephyr 文档所用术语的概述，请参阅 :ref:`hw_support_hierarchy` 。

对于 SoC 移植，最重要的术语如下：

- SoC：开发板上的 CPU 所属的具体片上系统。
- SoC 系列：一组紧密相关的 SoC。
- SoC 系列族：一组范围更广、具有相似特征的 SoC。
- CPU 集群：由一个或多个 CPU 核心组成的集群。
- CPU 核心：采用某种架构的具体 CPU 实例。
- 架构：指令集架构。

架构
====

参阅 :ref:`architecture_porting_guide` 。


创建 SoC 目录
*************

每个 SoC 都必须具有唯一的名称。请使用 SoC 厂商提供的官方名称，并检查该名称是否已被使用。有时，其他人可能已经贡献了同名的 SoC。如果 SoC 名称已被使用，通常应当改进现有的 SoC，而不是创建新的 SoC。可以使用脚本 ``list_hardware`` 获取 Zephyr 中所有已知 SoC 的列表，例如，在 Zephyr 根目录下运行 ``./scripts/list_hardware.py --soc-root=. --socs`` ，即可列出已被使用的名称。

首先创建目录 ``zephyr/soc/<VENDOR>/soc1`` ，其中 ``<VENDOR>`` 是厂商子目录。

.. note::
  如果要将 SoC 贡献给 Zephyr，则必须使用 ``<VENDOR>`` 子目录；如果 SoC 位于本地仓库中，则允许在 ``<your-repo>/soc`` 下采用任意目录结构。 ``<VENDOR>`` 子目录必须与 :zephyr_file:`dts/bindings/vendor-prefixes.txt` 列表中定义的厂商相匹配。如果该列表中没有此 SoC 厂商的前缀，则必须添加一个。

.. note::

  SoC 目录名不必与 SoC 名称一致。一个目录中甚至可以定义多个 SoC。在 Zephyr 中，SoC 通常按子目录组织在同一个 SoC 系列族或 SoC 系列的目录树中。

SoC 目录的结构应如下所示：

.. code-block:: none

   soc/<VENDOR>/<soc-name>
   ├── soc.yml
   ├── soc.h
   ├── CMakeLists.txt
   ├── Kconfig
   ├── Kconfig.soc
   └── Kconfig.defconfig

将 ``<soc-name>`` 替换为你的 SoC 名称。


必需文件如下：

#. :file:`soc.yml` ：一个 YAML 文件，用于描述 SoC 的高层元数据，例如：

   - SoC 名称：SoC 的名称
   - CPU 集群：如果 SoC 包含一个或多个 CPU 集群，则列出这些集群
   - SoC 系列：SoC 所属的 SoC 系列
   - SoC 系列族：该系列所属的 SoC 系列族

#. :file:`soc.h` ：一个头文件，可用于描述 SoC 或为其提供配置宏。Zephyr 中的驱动程序、子系统、开发板及其他源代码通常会包含 :file:`soc.h` 。

#. :file:`Kconfig.soc` ：SoC 的基础配置，以 ``config SOC_<soc-name>`` 的形式定义 Kconfig SoC 符号，并为 Kconfig 的 ``SOC`` 配置项提供 SoC 名称。如果 ``soc.yml`` 描述了 SoC 系列族和 SoC 系列，则也必须在此文件中定义它们。不得在此文件中选择 SoC 目录树之外的 Kconfig 配置项。要选择通用的 Zephyr Kconfig 配置项，必须使用 :file:`Kconfig` 文件。

#. :file:`CMakeLists.txt` ：由 Zephyr 构建系统加载的 CMake 文件。此文件可以定义以该 SoC 为目标进行构建时使用的额外头文件搜索路径和源文件。此外，还必须定义所使用的基础链接器脚本。

可选文件如下：

- :file:`Kconfig` 、 :file:`Kconfig.defconfig` ：采用 :ref:`kconfig` 格式的软件配置。这些文件用于选择架构和可用的外设。

编写 SoC YAML 文件
******************

SoC YAML 文件从高层描述 SoC 系列族、SoC 系列和 SoC。

硬件描述和配置等详细配置在 Devicetree 和 Kconfig 中完成。

仅包含一个 SoC 的简单 SoC YAML 文件框架如下：

.. code-block:: yaml

   socs:
     - name: <soc1>

SoC 目录中可以包含多个 SoC。例如，如果这些 SoC 属于同一个系列族或系列，建议将它们放在同一个目录树中。同一目录中的多个 SoC 和 SoC 系列可以在 :file:`soc.yml` 文件中描述如下：

.. code-block:: yaml

   family:
     - name: <family-name>
       series:
         - name: <series-1-name>
           socs:
             - name: <soc1>
               cpuclusters:
                 - name: <coreA>
                 - name: <coreB>
                   ...
             - name: <soc2>
         - name: <series-2-name>
           ...


编写 SoC Devicetree
*******************

SoC Devicetree 包含文件位于 :file:`<zephyr-repo>/dts` 文件夹下对应的 :file:`<ARCH>/<VENDOR>` 目录中。

SoC 的 :file:`dts/<ARCH>/<VENDOR>/<soc>.dtsi` 文件以 Devicetree 源文件（DTS）格式描述 SoC 硬件，所有使用该 SoC 的开发板都必须包含此文件。

如果存在高层 :file:`<arch>.dtsi` 文件，可以先在 :file:`<soc>.dtsi` 中包含此文件。

通常，:file:`<soc>.dtsi` 应如下所示：

.. code-block:: devicetree

   #include <arch>/<arch>.dtsi

   / {
           chosen {
                   /* common chosen settings for your SoC */
           };

           cpus {
                   #address-cells = <m>;
                   #size-cells = <n>;

                   cpu@0 {
                   device_type = "cpu";
                   compatible = "<compatibles>";
                   /* ... your CPU definitions ... */
           };

           soc {
                   /* Your SoC definitions and peripherals */
                   /* such as ram, clock, buses, peripherals. */
           };
   };

.. hint::
   可以将多个 :file:`<VENDOR>/<soc>.dtsi` 文件组织到子目录中，使文件系统结构更清晰。例如，按 SoC 系列组织为：:file:`<VENDOR>/<SERIES>/<soc>.dtsi` 。


多个 CPU 集群
=============

Devicetree 反映硬件结构。不同 CPU 集群可用的内存空间和外设可能差异很大，因此每个 CPU 集群通常都有自己的 :file:`.dtsi` 文件。

CPU 集群的 :file:`.dtsi` 文件应遵循 :file:`<soc>_<cluster>.dtsi` 命名规则。:file:`<soc>_<cluster>.dtsi` 文件的内容与不含 CPU 集群的 SoC :file:`.dtsi` 文件类似。

编写 Kconfig 文件
*****************

Zephyr 使用 Kconfig 语言配置软件功能。必须先为 SoC 提供一些 Kconfig 设置，才能为其编译 Zephyr 应用。

:ref:`setting_configuration_values` 详细介绍了如何设置 Kconfig 配置值。

对于一个 SoC，其目录中有一个必需的 Kconfig 文件和两个可选文件：

.. code-block:: none

   soc/<vendor>/<your soc>
   ├── Kconfig.soc
   ├── Kconfig
   └── Kconfig.defconfig

:file:`Kconfig.soc`
  一个共享的 Kconfig 文件，可同时由 Zephyr Kconfig 和 sysbuild Kconfig 树引入。

  此文件在 Kconfig 树中选择 SoC 系列族和系列，以及可能存在的其他 SoC 相关 Kconfig 设置。在某些情况下，还会选择 SOC_PART_NUMBER。此文件不得选择可复用的 Kconfig SoC 树之外的任何设置。

  :file:`Kconfig.soc` 可以如下所示：

  .. code-block:: kconfig

     config SOC_FAMILY_<SOC_FAMILY_NAME>
             bool

     config SOC_SERIES_<SOC_SERIES_NAME>
             bool
             select SOC_FAMILY_<SOC_FAMILY_NAME>

     config SOC_<SOC_NAME>
             bool
             select SOC_SERIES_<SOC_SERIES_NAME>

     config SOC_FAMILY
             default "<soc_family_name>" if SOC_FAMILY_<SOC_FAMILY_NAME>

     config SOC_SERIES
             default "<soc_series_name>" if SOC_SERIES_<SOC_SERIES_NAME>

     config SOC
             default "<soc_name>" if SOC_<SOC_NAME>

  注意，``SOC_NAME`` 是 SoC 名称的全大写形式，``SOC_SERIES_NAME`` 是 SoC 系列名称的全大写形式，``SOC_FAMILY_NAME`` 是 SoC 系列族名称的全大写形式。如果这些字段未出现在 :file:`soc.yml` 文件中，则也不应出现在 :file:`Kconfig.soc` 文件中。

  Kconfig 设置 ``SOC`` 、``SOC_SERIES`` 和 ``SOC_FAMILY`` 已在全局定义为字符串类型，因此 :file:`Kconfig.soc` 文件只能定义其默认字符串值，不能定义其类型。注意，这些字符串值必须与 :file:`soc.yml` 文件中使用的值一致。

.. note::
  构建系统支持 ``soc_name`` 、``soc_series_name`` 和 ``soc_family_mame`` 使用任意大小写形式，但在提交开发板以纳入 Zephyr 项目时，这些名称必须是对应 Kconfig 名称的全小写形式。

:file:`Kconfig`
  由 :zephyr_file:`soc/Kconfig` 包含。

  此文件可添加当前 SoC 特有的 Kconfig 设置。

  :file:`Kconfig` 通常使用形如 ``HAS_<support>`` 的设置来表明对某项硬件功能的支持。

  .. code-block:: kconfig

     config SOC_<SOC_NAME>
             select ARM
             select CPU_HAS_FPU

  如果设置名称与 Zephyr 中现有的 Kconfig 设置相同，且仅修改该设置的默认值，则应改用 :file:`Kconfig.defconfig` 。

:file:`Kconfig.defconfig`
  SoC 特定的 Kconfig 选项默认值。

  并非所有 SoC 都有 :file:`Kconfig.defconfig` 文件。

  整个文件的内容都应放在一对 ``if SOC_<SOC_NAME>`` / ``endif`` 或 ``if SOC_SERIES_<SERIES_NAME>`` / ``endif`` 中，如下所示：

  .. code-block:: kconfig

     if SOC_<SOC_NAME>

     config NUM_IRQS
             default 32

     endif # SOC_<SOC_NAME>

Multiple CPU clusters
=====================

CPU 集群必须在 :file:`Kconfig.soc` 文件中提供额外的 Kconfig 设置。这些设置通常采用 ``SOC_<SOC_NAME>_<CLUSTER>`` 的形式，因此，对于包含 ``clusterA`` 和 ``clusterB`` 两个集群的 ``soc1`` ，其设置如下所示：

当 SoC 定义 CPU 集群时

  .. code-block:: kconfig

     config SOC_SOC1_CLUSTERA
             bool
             select SOC_SOC1

     config SOC_SOC1_CLUSTERB
             bool
             select SOC_SOC1
