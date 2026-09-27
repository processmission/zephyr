.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _kconfig_style:

Kconfig 风格指南
################

本文档提供在 Zephyr 项目中编写 Kconfig 文件的风格指南。遵循这些指南可确保整个代码库的一致性和可读性，使开发者更容易理解和维护配置选项。

以下各节给出指南和示例，以说明正确的 Kconfig 格式和命名约定。


基本格式规则
************

编写 Kconfig 文件时，请遵循以下基本格式规则：

* **行长**：将每行控制在 100 列以内。
* **缩进**：使用制表符缩进，``help`` 条目的文本除外，它应置于一个制表符再加两个空格处。
* **间距**：在各选项声明之间留一个空行。
* **注释**：注释格式写成 ``# Comment`` 而不是 ``#Comment``。
* **条件块**：在每个顶层 ``if`` 和 ``endif`` 语句的前后各插入一个空行。
* **文件结尾**：文件以恰好一个换行符结尾。

有关使用 ``select`` 等语句的指导，请参阅 :ref:`kconfig_tips_and_tricks` 以获取更多信息。

这些格式规则由 CI 中的 ``KconfigFormat`` 合规检查强制执行。你可以在本地使用 ``scripts/kconfig/kconfig_style.py`` 脚本检查 Kconfig 文件，该脚本会报告任何风格问题（会递归搜索目录中的 Kconfig 文件）：

.. code-block:: console

   ./scripts/kconfig/kconfig_style.py path/to/Kconfig
   ./scripts/kconfig/kconfig_style.py drivers/sensor/

符号命名与结构
**************

以下示例演示了正确的 Kconfig 符号命名和结构：

.. literalinclude:: kconfig_demo_simple.txt
   :language: kconfig
   :start-after: start-after-here

.. literalinclude:: kconfig_demo_complex.txt
   :language: kconfig
   :start-after: start-after-here


命名约定
********

* 通常而言，与同一组件相关的符号应与其他符号区分开。这通常可以通过使用公共前缀来实现。该前缀可以是一个简单的关键字，也可以像驱动程序那样使用多个关键字以提高精确度。

* 公共前缀通常表示该符号所属的子系统或组件。

* 启用符号的名称应由若干关键字组成，以从最一般到最具体的范围提供该符号的上下文（例如 *Driver Type* -> *Driver Name*）。

* 启用符号的提示信息应使用与符号名称本身相同的逻辑，但关键字的顺序相反。

   * 遵循这一风格可以使在 UI 中搜索符号更容易，因为可以按范围关键字进行过滤。

* 当启用符号依赖于某个 devicetree 节点时，可以考虑依赖于 :ref:`自动创建 <auto-dts-kconfig>` 的 ``DT_HAS_<node>_ENABLED`` 符号。

* 在基于 devicetree 节点 compatible 构建复杂表达式时，请使用 :ref:`自动定义 <auto-dts-kconfig>` 的 :samp:`DT_COMPAT_{VND_DEVICE}`，而不要手动定义一个等于 :samp:`{vnd,device}` 的变量。

各子树的具体格式：

* **驱动程序（/drivers）**：符号使用 ``{Driver Type}_{Driver Name}`` 格式，提示信息使用 ``{Driver Name} {Driver Type} driver`` 格式。

* **传感器（/drivers/sensors）**：符号使用 ``SENSOR_{Sensor Name}`` 格式，提示信息使用 ``{Sensor Name} {Sensor Type} sensor driver`` 格式。

* **架构（/arch）**：许多符号在各架构之间共享。在创建新符号之前，请检查其他架构中是否已存在类似的符号。

* **示例（/samples）**：符号使用 ``SAMPLE_``，以避免与外部模块冲突。

* **测试（/tests）**：符号使用 ``TEST_``，以避免与外部模块冲突。

* **开发板（/boards）**：符号使用 ``BOARD_``。

* **SoC（/soc）**：为符号选择最合适的基础：如果涉及某个 SoC 厂商的多个家族，使用 ``SOC_VENDOR_{SoC vendor}_``；如果涉及整个 SoC 家族，使用 ``SOC_FAMILY_{SoC family}_``；如果涉及整个 SoC 系列，使用 ``SOC_SERIES_{SoC series}_``；如果涉及特定的 SoC，请使用 ``SOC_{SoC}_`` - 有关这些术语以及它们必须源自何处的详细信息，请参阅 :ref:`soc_porting_guide`。这是为了避免与其他厂商和外部模块冲突。

示例
====

.. note::

   为简洁起见，以下示例只展示符号行和提示行。

**驱动程序示例：**

.. literalinclude:: kconfig_example_driver.txt
   :language: kconfig
   :start-after: start-after-here

**传感器示例：**

.. literalinclude:: kconfig_example_sensor.txt
   :language: kconfig
   :start-after: start-after-here

**Samples 示例：**

.. literalinclude:: kconfig_example_sample.txt
   :language: kconfig
   :start-after: start-after-here

**Tests 示例：**

.. literalinclude:: kconfig_example_test.txt
   :language: kconfig
   :start-after: start-after-here

**SoC 示例：**

.. literalinclude:: kconfig_example_soc.txt
   :language: kconfig
   :start-after: start-after-here

配置符号的组织
**************

当某个特性使用配置符号来配置其行为时：

* 使用 ``menuconfig`` 而不是 ``config`` 来定义启用特性（即使该配置符号没有提示信息）。

* 将这些配置符号封装在 ``if`` 语句中，以声明它们对启用符号的依赖（这会在 UI 中自动将这些符号归组到启用符号之下）。

* 为配置符号添加启用符号的名称作为前缀，以提供范围和上下文。

* 在配置符号的提示信息中，描述该符号配置的内容，而不要重复范围关键字，因为 UI 中的分组已提供了这一上下文。

文件组织
********

组织 Kconfig 文件时：

* 让 Kconfig 文件尽量靠近它所配置的源文件。

* 处理大型 Kconfig 文件（例如包含许多配置符号）时，可以考虑将其中部分或全部归组到一个单独的文件中，并使用 ``source`` 指令导入，以提高可读性。
