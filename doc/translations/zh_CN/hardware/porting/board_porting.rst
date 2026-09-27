.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _board_porting_guide:

开发板移植指南
##############

要为新的 :term:`开发板 <board>` 添加 Zephyr 支持，至少需要一个包含各种文件的 *开发板目录* 。开发板目录中的文件会继承对至少一个 SoC 及其所有功能的支持。因此，Zephyr 也必须支持你使用的 :term:`SoC` 。

.. _hw_model_v2:

迁移到当前硬件模型
******************

Zephyr 3.6.0 发布后不久，Zephyr 引入了新的硬件模型。新模型全面调整了 SoC 和开发板的命名与定义方式，并增加了对多年来被认为重要的功能的支持。其中包括：

- 支持多核心、多架构的 AMP（非对称多处理）SoC
- 支持包含多个 SoC 的开发板
- 支持在 Zephyr 构建系统之外复用 SoC 和开发板的 Kconfig 树
- 支持使用 :ref:`sysbuild` 的高级用例
- 消除所有现有的 Kconfig 和文件夹命名中随意且不一致的用法

本页所有文档均针对当前硬件模型。有关先前现已废弃的硬件模型的信息，请参阅 Zephyr v3.6.0 或更早版本的文档。

有关新模型的设计依据、开发过程和相关概念的更多信息，请参阅 :github:`最初的议题 <51831>` 和 :github:`最初的拉取请求 <50305>` ；若要查看引入的完整变更，请参阅 `hardware model v2 commit`_ 。

新硬件模型的一些非关键功能、增强和改进仍在开发中。完整列表请参阅 :github:`硬件模型 v2 增强议题 <69546>` 。

从先前的硬件模型迁移到当前模型（通常称为“硬件模型 v2”）需要修改所有现有的开发板和 SoC 定义。项目决定不为先前的模型提供直接的向后兼容支持。因此，对于拥有树外开发板或 SoC 的用户，从早期 Zephyr 版本迁移到包含新模型的版本（v3.7.0 及更高版本）时有两种选择：

#. 将树外开发板转换为当前硬件模型（推荐）
#. 从 Zephyr v3.6.0 中取出 SoC 定义，将其复制到你的下游仓库中，并确保构建系统能通过 :ref:`Zephyr 模块 <modules>` 或 ``SOC_ROOT`` 找到它。这样，使用先前硬件模型定义的开发板就能继续工作

将开发板从先前的硬件模型转换为当前模型时，建议先通读本页，详细了解该模型。然后，可以参考 `example-application conversion Pull Request`_ ，了解如何移植一个简单的开发板。此外，还提供了 `conversion script`_ ，在许多情况下都能可靠地完成转换，但可能无法完整处理多核心 SoC。最后，`hardware model v2 commit`_ 包含了所有现有开发板从旧模型转换为当前模型的完整变更，可作为完整的转换参考。

.. _hardware model v2 commit: https://github.com/zephyrproject-rtos/zephyr/commit/8dc3f856229ce083c956aa301c31a23e65bd8cd8
.. _example-application conversion Pull Request: https://github.com/zephyrproject-rtos/example-application/pull/58
.. _conversion script: https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/utils/board_v1_to_v2.py

.. _hw_support_hierarchy:

硬件支持层次结构
****************

Zephyr 的硬件支持基于一系列分层抽象。首先，每个 :term:`开发板 <board>` 都包含一个或多个 :term:`SoC` 。每个 SoC 都可以选择归入某个 :term:`SoC 系列 <SoC series>` ，而每个 SoC 系列又可以选择归属某个 :term:`SoC 系列族 <SoC family>` 。每个 SoC 包含一个或多个 :term:`CPU 集群 <CPU cluster>` ，每个 CPU 集群包含一个或多个采用特定 :term:`架构 <architecture>` 的 :term:`CPU 核心 <CPU core>` 。

下图直观展示了这一层次结构：

.. figure:: board/hierarchy.png
   :width: 500px
   :align: center
   :alt: Hardware support Hierarchy

   硬件支持层次结构

下面列出了本节所述层次结构的一些示例，每行展示一个 :term:`开发板 <board>` 及其对应的各层级条目。请注意，并非所有示例都使用 :term:`SoC 系列 <SoC series>` 和 :term:`SoC 系列族 <SoC family>` 层级。

.. table::

   +----------------------------------------------+----------------------------+---------------+----------------------+----------------------+------------------+------------------------+
   | :term:`board name`                           | :term:`board qualifiers`   | :term:`SoC`   | :term:`SoC Series`   | :term:`SoC family`   | CPU 核心         | :term:`architecture`   |
   +==============================================+============================+===============+======================+======================+==================+========================+
   | :zephyr:board:`nrf52dk`                      | nrf52832                   | nRF52832      | nRF52                | Nordic nRF           | Arm Cortex-M4    | ARMv7-M                |
   +----------------------------------------------+----------------------------+---------------+----------------------+----------------------+------------------+------------------------+
   | :zephyr:board:`frdm_k64f <frdm_k64f>`        | mk64f12                    | MK64F12       | Kinetis K6x          | NXP Kinetis          | Arm Cortex-M4    | ARMv7-M                |
   +----------------------------------------------+----------------------------+---------------+----------------------+----------------------+------------------+------------------------+
   | :zephyr:board:`rv32m1_vega <rv32m1_vega>`    | openisa_rv32m1/ri5cy       | RV32M1        | （未使用）           | （未使用）           | RI5CY            | RISC-V RV32            |
   +----------------------------------------------+----------------------------+---------------+----------------------+----------------------+------------------+------------------------+
   | :zephyr:board:`nrf5340dk`                    | nrf5340/cpuapp             | nRF5340       | nRF53                | Nordic nRF           | Arm Cortex-M33   | ARMv8-M                |
   |                                              +----------------------------+---------------+----------------------+----------------------+------------------+------------------------+
   |                                              | nrf5340/cpunet             | nRF5340       | nRF53                | Nordic nRF           | Arm Cortex-M33   | ARMv8-M                |
   +----------------------------------------------+----------------------------+---------------+----------------------+----------------------+------------------+------------------------+
   | :zephyr:board:`mimx8mp_evk <imx8mp_evk>`     | mimx8ml8/a53               | i.MX8M Plus   | i.MX8M               | NXP i.MX             | Arm Cortex-A53   | ARMv8-A                |
   |                                              +----------------------------+---------------+----------------------+----------------------+------------------+------------------------+
   |                                              | mimx8ml8/m7                | i.MX8M Plus   | i.MX8M               | NXP i.MX             | Arm Cortex-M7    | ARMv7-M                |
   |                                              +----------------------------+---------------+----------------------+----------------------+------------------+------------------------+
   |                                              | mimx8ml8/adsp              | i.MX8M Plus   | i.MX8M               | NXP i.MX             | Cadence HIFI4    | Xtensa LX6             |
   +----------------------------------------------+----------------------------+---------------+----------------------+----------------------+------------------+------------------------+

有关术语的更多详细信息，请参阅下一节。

.. _board_terminology:

开发板术语
**********

上一节介绍了 Zephyr 对硬件支持进行分类和实现的层次结构。本节重点介绍硬件支持相关的术语，尤其是定义和使用开发板与 SoC 时涉及的术语。

下图以 :zephyr:board:`bl5340_dvk` 开发板为例，展示了 Zephyr 中与开发板概念相关的全部术语。

.. figure:: board/board-terminology.svg
   :width: 500px
   :align: center
   :alt: Board terminology diagram

   开发板术语示意图

该图展示了用于描述开发板的不同术语：

- :term:`开发板名称 <board name>` ：``bl5340_dvk``
- 可选的 :term:`开发板修订版 <board revision>` ：``1.2.0``
- :term:`开发板限定符 <board qualifiers>` ，可用于描述 :term:`SoC` 、:term:`CPU 集群 <CPU cluster>` 和 :term:`变体 <variant>` ：``nrf5340/cpuapp/ns``
- :term:`开发板目标 <board target>` ，用于唯一标识上述各项的一种组合，并可在使用 Zephyr 提供的工具时指定构建所面向的硬件：``bl5340_dvk@1.2.0/nrf5340/cpuapp/ns``

从形式上看，也可以将其表示为 :samp:`{board name}[@{revision}][/{board qualifiers}]` ，进一步展开为 :samp:`{board name}[@{revision}][/{SoC}[/{CPU cluster}][/{variant}]]` 。

如果开发板仅包含一个单核 SoC，则可以在开发板目标中省略 SoC。这意味着，如果开发板未定义任何开发板限定符，就可以将开发板名称用作开发板目标。反之，如果开发板定义中包含开发板限定符，则可以省略 SoC，但必须保留相应的正斜杠：``//`` 。

继续以上面的示例说明，:zephyr:board:`bl5340_dvk` 开发板只包含一个 SoC，该 SoC 定义了两个 CPU 集群：``cpuapp`` 和 ``cpunet`` 。其中，CPU 集群 ``cpuapp`` 还定义了一个非安全开发板变体 ``ns`` 。

开发板限定符 ``nrf5340/cpuapp/ns`` 可以解读为：


- ``nrf5340`` ：SoC，此处为 Nordic nRF5340 双核 SoC。
- ``cpuapp`` ：CPU 集群 ``cpuapp`` ，由一个 Cortex-M33 CPU 核心组成。无法从开发板限定符判断 CPU 集群中的核心数量。
- ``ns`` ：变体，此处的 ``ns`` 是 Zephyr 中常用的变体名称，表示面向支持 :ref:`tfm` 的开发板的非安全构建。

并非所有 SoC 都定义了 CPU 集群或变体。例如，:zephyr:board:`thingy52` 这样的简单开发板仅包含一个 SoC，未定义 CPU 集群或变体。对于 ``thingy52`` ，开发板目标 ``thingy52/nrf52832`` 可以解读为：

- ``thingy52`` ：开发板名称。
- ``nrf52832`` ：开发板限定符，此处与 SoC 名称相同，即 Nordic nRF52832。


确保你的 SoC 已受支持
*********************

首先确认 Zephyr 是否支持你的 SoC。如果支持，就可以 :ref:`创建开发板目录 <create-your-board-directory>` 。如果不确定，可以尝试：

- 在 :ref:`boards` 中查找可能相关的名称，并阅读各开发板的文档以确认。
- 咨询你的 SoC 供应商

如果你需要添加对 SoC、CPU 集群甚至架构的支持，本页不适用于此类工作，但下面提供了一些通用建议。

架构
====

请参阅 :ref:`architecture_porting_guide` 。

CPU 核心
========

CPU 核心支持文件位于 :zephyr_file:`arch` 下的 ``core`` 子目录中，例如 :zephyr_file:`arch/x86/core` 。

有关 Zephyr 支持的工具链（编译器、链接器等）的信息，请参阅 :ref:`gs_toolchain` 。如果需要支持新的工具链，可以从 :ref:`build_overview` 开始了解构建系统。如果需要建议或希望合作开展工具链支持工作，请联系社区。

SoC
===

Zephyr 的 SoC 支持文件位于 :zephyr_file:`soc` 下各架构专用的子目录中。这些文件通常按 SoC 系列族分组。

为 Zephyr 已支持其 SoC 的厂商添加新的 SoC 系列族或 SoC 系列时，请尽量将通用功能提取到共享文件中，以避免重复。如果尚未支持你的厂商，可以在新目录 ``zephyr/soc/<VENDOR>/<YOUR-SOC>`` 中添加支持；请使用含义明确的目录名称。

.. _create-your-board-directory:

创建开发板目录
**************

找到使用相同 SoC 的现有开发板后，通常可以先复制其开发板目录，再根据你的硬件修改其中的内容。

你需要为开发板指定一个唯一的名称。运行 ``west boards`` 查看已被使用的名称列表，然后选择一个未被使用的名称。假设你的开发板名为 ``plank`` （请不要实际使用这个名称）。

首先创建开发板目录 ``zephyr/boards/<VENDOR>/plank`` ，其中 ``<VENDOR>`` 是你的厂商子目录。（你不一定要将开发板目录放在 Zephyr 仓库中，但这是最容易上手的方式。开发板正常工作后，可以参阅 :ref:`custom_board_definition` ，了解如何将开发板目录移至独立仓库。）

.. note::
  如果要将开发板贡献给 Zephyr，则必须使用 ``<VENDOR>`` 子目录；但如果开发板位于本地仓库中，则可以在 ``<your-repo>/boards`` 下使用任意目录结构。如果 :zephyr_file:`dts/bindings/vendor-prefixes.txt` 的列表中已定义该厂商，则必须使用对应的厂商前缀作为 ``<VENDOR>`` 。如果未定义该厂商，则可以使用 ``others`` 作为厂商前缀。

.. note::

  开发板目录名称不必与开发板名称一致。甚至可以在同一个目录中定义多个开发板。

你的开发板目录应如下所示：

.. code-block:: none

   boards/<VENDOR>/plank
   ├── board.yml
   ├── board.cmake
   ├── CMakeLists.txt
   ├── doc
   │   ├── plank.webp
   │   └── index.rst
   ├── Kconfig.plank
   ├── Kconfig.defconfig
   ├── plank_<qualifiers>_defconfig
   ├── plank_<qualifiers>.dts
   └── plank_<qualifiers>.yaml

当然，请将 ``plank`` 替换为你的开发板名称。

必需的文件包括：

#. :file:`board.yml` ：一个 YAML 文件，用于描述开发板的高层元数据，例如开发板名称、所用的 SoC 以及变体。多核 SoC 的 CPU 集群不在此文件中描述，而是继承自 SoC 的 YAML 描述。

#. :file:`plank_<qualifiers>.dts` ：采用 :ref:`Devicetree <dt-guide>` 格式的硬件描述。它声明你的 SoC、连接器以及其他硬件组件，例如 LED、按钮、传感器或通信外设（USB、蓝牙控制器等）。

#. :file:`Kconfig.plank` ：用于选择 SoC 以及其他开发板和 SoC 相关设置的基础软件配置。不得选择开发板和 SoC 目录树之外的 Kconfig 设置。要选择通用的 Zephyr Kconfig 设置，必须使用 :file:`Kconfig` 文件。


可选的文件包括：

- :file:`Kconfig` 、 :file:`Kconfig.defconfig` ：采用 :ref:`kconfig` 格式的软件配置，为软件功能和外设驱动提供默认设置。
- :file:`plank_defconfig` 和 :file:`plank_<qualifiers>_defconfig` ：采用 Kconfig ``.conf`` 格式的软件配置。
- :file:`board.cmake` ：用于 :ref:`flash-and-debug-support`
- :file:`CMakeLists.txt` ：需要向构建中添加额外源文件时使用。
- :file:`doc/index.rst` 、 :file:`doc/plank.webp` ：开发板的文档和图片。只有在向 Zephyr :ref:`contributing-your-board` 时才需要这些文件。
- :file:`plank_<qualifiers>.yaml` ：一个 YAML 文件，包含 :ref:`twister_script` 使用的各类元数据。

形式为 ``<soc>/<cpucluster>/<variant>`` 的开发板限定符用于文件名时，会经过规范化处理，将 ``/`` 替换为 ``_`` 。例如， ``soc1/foo`` 用于文件名时会变为 ``soc1_foo`` 。

.. _board_description:

编写开发板 YAML 文件
********************

开发板 YAML 文件从高层次描述开发板，包括 SoC、开发板变体和开发板修订版。

硬件描述和配置等详细配置在 Devicetree 和 Kconfig 中完成。

开发板 YAML 文件的基本结构如下：

.. code-block:: yaml

   board:
     name: <board-name>
     full_name: <board-full-name>
     vendor: <board-vendor>
     revision:
       format: <major.minor.patch|letter|number|custom>
       default: <default-revision-value>
       exact: <true|false>
       revisions:
       - name: <revA>
       - name: <revB>
         ...
     socs:
     - name: <soc-1>
       variants:
       - name: <variant-1>
       - name: <variant-2>
         variants:
         - name: <sub-variant-2-1>
           ...
     - name: <soc-2>
       ...

一个开发板文件夹中可以包含多个开发板。如果将多个开发板放在同一个开发板文件夹中，则 :file:`board.yml` 文件必须以列表形式描述这些开发板，如下所示：

.. code-block:: yaml

   boards:
   - name: <board-name-1>
     vendor: <board-vendor>
     full_name: <board-full-name>
     ...
   - name: <board-name-2>
     vendor: <board-vendor>
     full_name: <board-full-name>
     ...
   ...


.. _default_board_configuration:

编写 Devicetree
***************

Devicetree 文件 :file:`boards/<vendor>/plank/plank_<qualifiers>.dts` 使用 Devicetree 源文件（DTS）格式描述开发板硬件（照例，将 ``plank`` 替换为你的开发板名称）。如果你刚接触 Devicetree，请参阅 :ref:`devicetree-intro` 。

通常，:file:`plank_<qualifiers>.dts` 应具有如下结构：

.. code-block:: devicetree

   /dts-v1/;
   #include <your_soc_vendor/your_soc.dtsi>

   / {
           model = "A human readable name";
           compatible = "yourcompany,plank";

           chosen {
                   zephyr,console = &your_uart_console;
                   zephyr,sram = &your_memory_node;
                   /* other chosen settings  for your hardware */
           };

           /*
            * Your board-specific hardware: buttons, LEDs, sensors, etc.
            */

           leds {
                   compatible = "gpio-leds";
                   led0: led_0 {
                           gpios = </* GPIO your LED is hooked up to */>;
                           label = "LED 0";
                   };
                   /* ... other LEDs ... */
           };

           buttons {
                   compatible = "gpio-keys";
                   /* ... your button definitions ... */
           };

           /* These aliases are provided for compatibility with samples */
           aliases {
                   led0 = &led0; /* now you support the blinky sample! */
                   /* other aliases go here */
           };
   };

   &some_peripheral_you_want_to_enable { /* like a GPIO or SPI controller */
           status = "okay";
   };

   &another_peripheral_you_want {
           status = "okay";
   };

如果开发板只有一个 SoC，且没有任何开发板变体，则也可以将 dts 文件命名为 :file:`<plank>.dts` 。不过，不建议这样做，因为一旦为开发板添加变体或其他 SoC，该文件就会被忽略，且不会有任何提示。

如果时间紧迫，通常可以通过复制粘贴并反复试错来支持简单的硬件。如果想了解细节，则需要阅读其余的 Devicetree 文档以及 Devicetree 规范。

.. _dt_k6x_example:

示例：FRDM-K64F 和 Hexiwear K64
===============================

.. Give the filenames instead of the full paths below, as it's easier to read.
   The cramped 'foo.dts<path>' style avoids extra spaces before commas.

本节提供了编写开发板 Devicetree 的具体示例。

FRDM-K64F 和 Hexiwear K64 开发板的 Devicetree 分别定义在 :zephyr_file:`frdm_k64fs.dts <boards/nxp/frdm_k64f/frdm_k64f.dts>` 和 :zephyr_file:`hexiwear_k64.dts <boards/mikroe/hexiwear/hexiwear_mk64f12.dts>` 中。这两块开发板都采用 NXP 的 SoC，属于同一个 Kinetis SoC 系列族 K6X。

K6X 的通用 Devicetree 定义存储在 :zephyr_file:`nxp_k6x.dtsi <dts/arm/nxp/kinetis/k6x/nxp_k6x.dtsi>` 中，两个开发板的 :file:`.dts` 文件均包含该文件。:zephyr_file:`nxp_k6x.dtsi<dts/arm/nxp/kinetis/k6x/nxp_k6x.dtsi>` 又包含 :zephyr_file:`armv7-m.dtsi<dts/arm/armv7-m.dtsi>` ，其中提供了 Arm v7-M 核心的通用定义。

由于 :zephyr_file:`nxp_k6x.dtsi<dts/arm/nxp/kinetis/k6x/nxp_k6x.dtsi>` 旨在供各类基于 K6X 的开发板通用，因此它通过 ``status`` 属性默认禁用了许多设备。例如，其中一个 CAN 控制器的定义如下（省略了无关部分）：

.. code-block:: devicetree

   can0: can@40024000 {
        ...
        status = "disabled";
        ...
   };

开发板的 :file:`.dts` 文件或应用的 overlay 文件负责根据需要，通过设置 ``status = "okay"`` 来启用这些设备。开发板的 :file:`.dts` 文件还负责设备的所有开发板专属配置，例如为板载传感器、LED、按钮等添加节点。

例如，FRDM-K64（但 Hexiwear K64 除外）的 :file:`.dts` 启用了 CAN 控制器并设置总线速率：

.. code-block:: devicetree

   &can0 {
        status = "okay";
   };

``&can0 { ... };`` 语法用于添加或覆盖标签为 ``can0`` 的节点上的属性，即 :file:`.dtsi` 文件中定义的 ``can@4002400`` 节点。

其他开发板专属定制的示例包括：将 ``aliases`` 和 ``chosen`` 中的属性指向正确的节点（参阅 :ref:`dt-alias-chosen` ），以及进行 GPIO/pinmux 分配。

.. _board_kconfig_files:

编写 Kconfig 文件
*****************

Zephyr 使用 Kconfig 语言配置软件功能。在为开发板编译 Zephyr 应用之前，需要为其提供一些 Kconfig 设置。

:ref:`setting_configuration_values` 中详细介绍了如何设置 Kconfig 配置值。

对于名为 ``plank`` 的开发板，其开发板目录中有一个必需的 Kconfig 文件和几个可选文件：

.. code-block:: none

   boards/<vendor>/plank
   ├── Kconfig
   ├── Kconfig.plank
   ├── Kconfig.defconfig
   └── plank_<qualifiers>_defconfig

:file:`Kconfig.plank`
  一个共享的 Kconfig 文件，可在 Zephyr Kconfig 树和 sysbuild Kconfig 树中引入。

  此文件在 Kconfig 树中选择 SoC，以及可能需要的其他 SoC 相关 Kconfig 设置。此文件不得选择可复用的开发板和 SoC Kconfig 树以外的任何选项。

  :file:`Kconfig.plank` 的内容可能如下所示：

  .. code-block:: kconfig

     config BOARD_PLANK
             select SOC_SOC1

  Kconfig 符号 :samp:`BOARD_{board}` 和 :samp:`BOARD_{normalized_board_target}` 由构建系统构造，因此不得在上述代码片段中定义类型。

:file:`Kconfig`
  由 :zephyr_file:`boards/Kconfig` 包含。

  此文件可以添加当前开发板专属的 Kconfig 设置。

  并非所有开发板都有 :file:`Kconfig` 文件。

  开发板专属设置应定义为自定义设置，通常还应带有提示文本，如下所示：

  .. code-block:: kconfig

     config BOARD_FEATURE
             bool "Board specific feature"

  如果设置名称与 Zephyr 中现有的 Kconfig 设置相同，且仅修改该设置的默认值，则应改用 :file:`Kconfig.defconfig` 。

:file:`Kconfig.defconfig`
  开发板特定的 Kconfig 选项默认值。

  并非所有开发板都有 :file:`Kconfig.defconfig` 文件。

  整个文件的内容都应位于 ``if BOARD_PLANK`` / ``endif`` 这一对语句行之间，如下所示：

  .. code-block:: kconfig

     if BOARD_PLANK

     config FOO
             default y

     if NETWORKING

     config SOC_ETHERNET_DRIVER
             default y

     endif # NETWORKING

     endif # BOARD_PLANK

:file:`plank_<qualifiers>_defconfig` （或在有限情况下使用 :file:`plank_defconfig` ）
  一个 Kconfig 片段，每当为你的开发板编译应用时，都会将其原样合并到最终构建目录中的 :file:`.config` 文件中。

  :file:`plank_defconfig` 仅可用于没有限定符、没有变体且仅有一个 SoC 的开发板。不过，不推荐使用这种命名方式，因为如果在上游 Zephyr 中为开发板添加新的 SoC 或开发板变体/限定符，可能会导致示例、测试或下游使用在毫无预警的情况下突然失效。

.. note::
  多个文件不会合并，也没有文件回退机制。这意味着，如果一个开发板具有 2 个不同的 SoC，且每个 SoC 都有 2 个开发板变体，那么 :file:`plank_defconfig` 文件将完全不会被使用；对于第一个限定符和变体，将使用 :file:`plank_<soc1>_<variant1>_defconfig` ，而不会包含其他文件。

  ``_defconfig`` 应包含 UART、控制台等所必需的设置。具体内容取决于架构，但通常类似如下：

  .. code-block:: cfg

     CONFIG_GPIO=y
     CONFIG_CONSOLE=y
     CONFIG_UART_CONSOLE=y
     CONFIG_SERIAL=y

:file:`plank_x_y_z_defconfig` / :file:`plank_<qualifiers>_x_y_z_defconfig`
  一个 Kconfig 片段，每当为你的开发板修订版 ``x.y.z`` 编译应用时，都会将其原样合并到最终构建目录中的 :file:`.config` 文件中。

构建、测试和修复
****************

现在可以构建并测试你希望在开发板上运行的应用，直到满意为止。

例如：

.. code-block:: console

   west build -b plank samples/hello_world
   west flash

要使 ``west flash`` 正常工作，请参阅下文的 :ref:`flash-and-debug-support` 。你也可以使用任何其他喜欢的工具直接烧录 :file:`build/zephyr/zephyr.elf` 、 :file:`zephyr.hex` 或 :file:`zephyr.bin` 。

在向上游提交开发板支持之前，请验证你添加的每个开发板目标都能仅使用 Zephyr 主线仓库及其模块中的代码，通过项目的最低要求开源测试套件。该套件目前包括：

- :file:`samples/philosophers`
- :file:`tests/kernel`

例如，使用以下命令为某个开发板目标构建该套件：

.. code-block:: console

   west twister -p plank -T samples/philosophers -T tests/kernel

对于具有多个 SoC、CPU 集群、变体或修订版的开发板，请针对每个新增的开发板目标重复运行该测试套件。还建议构建 :zephyr:code-sample:`hello_world` 以进行快速冒烟检查，例如：

.. code-block:: console

   west build -p always -b plank/soc1/foo samples/hello_world
   west build -p always -b plank@1.0.0/soc1/foo samples/hello_world

如果开发板目标需要，请使用 :ref:`sysbuild` 。使用开发板测试元数据（例如开发板目标 YAML 文件中的 ``testing: only_tags`` ）时，请确保仍在本地测试或 CI 中使用最低要求测试套件验证该目标。

.. _porting-general-recommendations:

一般建议
********

为保持一致性，并方便用户构建不依赖特定开发板的应用，在移植计划贡献给 Zephyr 的开发板时，请遵循以下准则：

在 Devicetree 中启用有用的组件
  有用的板载组件（LED、按钮、传感器、板载 USB/以太网/BLE/Wi-Fi 等）的 Devicetree 节点必须 **默认启用** ，并具有正确的引脚控制和驱动配置，以便开箱即用。

保持子系统默认禁用（Kconfig）
  不要在开发板 defconfig 中启用子系统，除非它们是开发板基本运行所必需的，或在这些建议中被明确列为例外。

配置系统时钟和时钟节拍源
  配置可正常工作的系统时钟和时钟节拍源。

提供默认控制台
  使用 ``zephyr,console`` chosen 节点指向用于控制台输出的 UART 控制器。

  具有内置调试适配器或 USB 转 UART 适配器的开发板，应将控制台设置为连接到该适配器的 UART 控制器。

  仅支持 USB 且没有任何调试适配器的开发板，必须包含通用的 USB CDC-ACM :zephyr_file:`Kconfig <boards/common/usb/Kconfig.cdc_acm_serial.defconfig>` 和 :zephyr_file:`DTS <boards/common/usb/cdc_acm_serial.dtsi>` 片段，以启用 CDC-ACM UART 作为日志和 shell 的默认后端。

添加 :ref:`扩展板接口 <shield-interfaces>` 定义
  对于提供标准扩展排针的开发板，添加连接器节点和引脚复用配置。仅启用连接器预期功能或标准功能所需的外设。

配置引脚和外设实例
  将外设映射到正确的引脚（例如，将 SPI 映射到 Arduino SPI 引脚），并提供支持开发板功能的默认引脚复用配置项。

启用网络接口
  如果具备网络硬件，请为每种受支持的技术配置默认接口，使网络示例能够开箱即用。

启用 GPIO 控制器
  应启用所有连接到板载组件或扩展排针的 GPIO 端口。

启用 MPU 和栈保护
  建议在 MPU 可用时启用它（除非内存资源过于有限）。启用 MPU 后，建议同时启用硬件栈保护（ :kconfig:option:`CONFIG_HW_STACK_PROTECTION` ），使内核能够检测栈溢出，从而简化调试。

.. _flash-and-debug-support:

烧录和调试支持
**************

Zephyr 通过 west 扩展命令支持 :ref:`west-build-flash-debug` 。

要为开发板添加 ``west flash`` 和 ``west debug`` 支持，需要在开发板目录中创建一个 :file:`board.cmake` 文件。该文件用于为开发板配置一个“runner”。（要让开发板支持 ``west build`` ，无需执行任何特殊操作。）

“runner”是 Zephyr 专用的 Python 类，用于封装 :ref:`烧录和调试主机工具 <flash-debug-host-tools>` ，并与 west 和 Zephyr 构建系统集成，以支持 ``west flash`` 及相关命令。每个 runner 支持烧录、调试或同时支持两者。你需要在 :file:`board.cmake` 中配置这些 Python 脚本的参数，以支持这些命令，如下面的 :file:`board.cmake` 示例所示：

.. code-block:: cmake

   board_runner_args(jlink "--device=nrf52" "--speed=4000")
   board_runner_args(pyocd "--target=nrf52" "--frequency=4000000")

   include(${ZEPHYR_BASE}/boards/common/nrfutil.board.cmake)
   include(${ZEPHYR_BASE}/boards/common/nrfjprog.board.cmake)
   include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
   include(${ZEPHYR_BASE}/boards/common/pyocd.board.cmake)

此示例配置了 ``nrfutil`` 、 ``nrfjprog`` 、 ``jlink`` 和 ``pyocd`` runner。

.. warning::

   runner 的名称通常与其封装的工具名称一致，例如， ``jlink`` runner 封装了 Segger 的 J-Link 工具，其他 runner 以此类推。不过， ``--speed`` 等 runner 命令行选项是这些 Python 脚本特有的。

.. note::

   如果工具支持多个操作系统，编写 runner 和开发板配置时就不应仅针对某一个操作系统，也不应依赖特殊的系统设置或配置。例如，不要假定用户具备相关知识、已完成相关配置，或在使用 Linux 时已安装特殊的 udev 规则；不要假定所有平台都使用某个特定的 ``/dev/X`` 设备，因为这与 Windows 或 macOS 不兼容；还应允许覆盖所选设备，以便将多个开发板连接到同一系统，并由用户选择要烧录或调试的开发板。

更多详细信息：

- 运行 ``west flash --context`` 可查看支持烧录的可用 runner 列表，运行 ``west flash --context -r <RUNNER>`` 可查看某个 runner 的具体可用选项。
- 运行 ``west debug --context`` 和 ``west debug --context <RUNNER>`` 可获取支持调试的 runner 的相同信息。
- 运行 ``west flash --help`` 和 ``west debug --help`` 可查看烧录和调试的顶层选项。
- 有关 Python API，请参阅 :ref:`west-runner` 。
- 查阅与你的开发板类似的其他开发板的 :file:`board.cmake` 文件，以获取更多示例。

要查看 ``west flash`` 或 ``west debug`` 命令具体执行了哪些操作，请以详细模式运行：

.. code-block:: sh

   west --verbose flash
   west --verbose debug

详细模式会打印 runner 使用的所有主机工具命令。

:file:`board.cmake` 中 ``include()`` 调用的顺序很重要。如果尚未设置默认 runner，第一个 ``include`` 会设置默认 runner。例如，首先包含 ``nrfjprog.board.cmake`` 意味着 ``nrfjprog`` 是此开发板的默认烧录 runner。由于 ``nrfjprog`` 不支持调试，因此 ``jlink`` 是默认调试 runner。

.. _porting_board_revisions:

多个开发板修订版
****************

有关此功能面向用户的基础知识，请参阅 :ref:`application_board_version` 。

开发板修订版在 :file:`board.yml` 的 ``revision`` 条目中描述。

.. code-block:: yaml

   board:
     revision:
       format: <major.minor.patch|letter|number|custom>
       default: <default-revision-value>
       exact: <true|false>
       revisions:
       - name: <revA>
       - name: <revB>

Zephyr 原生支持以下修订版格式：

- ``major.minor.patch``：匹配由三个数字部分组成的修订版，例如 ``1.2.3`` 。
- ``number``：匹配整数修订版
- ``letter``：仅匹配从 ``A`` 到 ``Z`` 的单字母修订版

.. _board_fuzzy_revision_matching:

修订版模糊匹配
==============

默认启用修订版模糊匹配。

如果用户选择的修订版介于可用修订版之间，则使用不大于用户所选修订版的最接近修订版号。例如，如果开发板 ``plank`` 定义了修订版 ``0.5.0`` 和 ``1.5.0`` ，而用户为 ``plank@0.7.0`` 构建，则构建系统将以修订版 ``0.5.0`` 为目标。

构建系统将在 CMake 配置阶段打印以下内容：

.. code-block:: console

   -- Board: plank, Revision: 0.7.0 (Active: 0.5.0)

这样，你只需为引入不兼容变更的开发板修订版号创建修订版配置文件。

同样，对于 ``letter`` 修订版格式，如果定义了修订版 ``A`` 、 ``D`` 和 ``F`` ，而用户为 ``plank@E`` 构建，则构建系统将以修订版 ``D`` 为目标。

修订版精确匹配
==============

在 :file:`board.yml` 的 revision 部分中指定 ``exact: true`` 时，将启用修订版精确匹配。

启用精确匹配后，在上述示例中为 ``plank@0.7.0`` 构建将产生以下错误消息：

.. code-block:: console

   Board revision `0.7.0` not found.  Please specify a valid board revision.

开发板修订版配置调整
====================

当用户为开发板 ``plank@<revision>`` 构建时，可以调整开发板的常规配置。

如 :ref:`default_board_configuration` 和 :ref:`board_kconfig_files` 小节所述，开发板默认配置由 :file:`<board>.dts` / :file:`<board>_<qualifiers>.dts` 和 :file:`<board>_defconfig` / :file:`<board>_<qualifiers>_defconfig` 文件创建。为特定开发板修订版构建时，以上文件用作基础，此外还将使用以下开发板文件：

- :file:`<board>_<qualifiers>_<revision>_defconfig`：特定修订版的 defconfig，仅用于 ``<board>_<qualifiers>`` 标识的开发板及 SoC / 变体。

- :file:`<board>_<qualifiers>_<revision>.overlay`：特定修订版的 dts overlay，仅用于 ``<board>_<qualifiers>`` 标识的开发板及 SoC / 变体。

这种划分使具有多个 SoC、多核 SoC 或变体的开发板能够将适用于所有 SoC 和变体的通用修订版调整放在一个文件中，同时仍可将特定于某个 SoC 或变体的调整放在专用的修订版文件中。

以前面小节中的 ``plank`` 开发板为例，可以进行以下修订版调整：

.. code-block:: none

   boards/zephyr/plank
   ├── plank_soc1_foo_1_5_0.overlay   # DTS overlay for plank board when building for soc1 variant foo on revision 1.5.0
   └── plank_soc1_foo_1_5_0_defconfig # Kconfig adjustment for plank board when building for soc1 variant foo on revision 1.5.0

自定义 revision.cmake 文件
**************************

某些开发板可能使用 Zephyr 原生支持范围之外的开发板修订版，例如字符串修订版。

Zephyr 不支持字符串修订版的一个原因是，字符串可以有多种形式，而且不一定能明确判断给定字符串是否只是普通字符串，例如 ``blue`` 、 ``green`` 、 ``red`` 等，还是具有可用于匹配更高或更低修订版的顺序，例如 ``alpha`` 、 ``beta`` 、 ``gamma`` 。

由于字符串存在大量可能的用法，包括在内部进行正则表达式匹配，因此字符串修订版必须使用 ``custom`` 修订版类型实现。

要向构建系统表明使用的是 ``custom`` 修订版，必须将 :file:`board.yml` 中 ``revision`` 部分的 format 字段写为：

.. code-block:: yaml

   board:
     revision:
       format: custom

使用自定义修订版时，必须在开发板目录中创建 :file:`revision.cmake` 。

为该开发板构建时，构建系统将包含 :file:`revision.cmake` ，该文件负责验证用户指定的修订版。

:makevar:`BOARD_REVISION` 变量保存用户指定的修订版值。

要告知构建系统使用不同于用户指定的修订版，:file:`revision.cmake` 可以将 CMake 变量 :cmake:variable:`ACTIVE_BOARD_REVISION` 设置为要使用的修订版。相应的 Kconfig 文件和 Devicetree overlay 文件必须命名为 :file:`<board>_<ACTIVE_BOARD_REVISION>_defconfig` 和 :file:`<board>_<ACTIVE_BOARD_REVISION>.overlay` 。

.. _contributing-your-board:

贡献你的开发板
**************

如果你想向 Zephyr 贡献开发板支持，首先感谢你的贡献！

你还需要完成一些额外的工作：

#. 确保你已遵循所有 :ref:`porting-general-recommendations` 。这些是纳入 Zephyr 的开发板必须满足的要求。

#. 使用模板文件 :zephyr_file:`doc/templates/board.tmpl` 为你的开发板添加文档。有关如何在提交拉取请求之前构建文档的信息，请参阅 :ref:`zephyr_doc` 。

#. 按照 :ref:`contribute_guidelines` 准备一个添加你的开发板的拉取请求。

.. _extend-board:

开发板扩展
**********

Zephyr 的开发板硬件模型允许你通过添加新的开发板变体来扩展现有开发板。这类开发板扩展可以在你的自定义仓库中完成，因此可以位于 Zephyr 仓库之外。

通过添加额外变体来扩展现有开发板，你可以对现有开发板进行调整，并在构建时选择为原有的、未经修改的开发板构建，或为新变体构建。

要扩展现有开发板，首先在开发板扩展目录中创建 :file:`board.yml` 。确保使用 :ref:`create-your-board-directory` 中描述的目录结构。

用于扩展开发板的开发板 YAML 文件基本结构如下：

.. code-block:: yaml

   board:
     extend: <existing-board-name>
     variants:
       - name: <new-variant>
         qualifier: <existing-qualifier>

扩展开发板时，你的开发板目录应如下所示：

.. code-block:: none

   boards/<VENDOR>/plank
   ├── board.yml
   ├── plank_<new-qualifiers>_defconfig
   └── plank_<new-qualifiers>.dts

将 ``plank`` 替换为你要扩展的开发板的实际名称。

在某些情况下，你可能还希望调整其他设置，例如 :file:`Kconfig.defconfig` 或 :file:`Kconfig.{board}` 。因此，扩展开发板时也可以额外提供以下文件。

.. code-block:: none

   boards/<VENDOR>/plank
   ├── board.cmake
   ├── Kconfig
   ├── Kconfig.plank
   ├── Kconfig.defconfig
   └── plank_<new-qualifiers>.yaml
