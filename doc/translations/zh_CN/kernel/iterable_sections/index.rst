.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _iterable_sections_api:

可迭代段
########

本页提供可迭代段 API 的参考文档。这些 API 用于定义由大小相同的数据结构组成的可迭代区域，可使用 :c:macro:`STRUCT_SECTION_FOREACH` 遍历这些区域。

概述
****

可迭代段是一组同一结构体类型的静态实例，链接器将它们放入单个连续的输出段中。运行时即可遍历所有实例，无需维护显式列表。

Zephyr 目前支持两种链接脚本处理流程：一种基于模板，使用通过 ``zephyr_linker_sources()`` 注册的 ``.ld`` 脚本；另一种由 CMake 生成，使用 ``zephyr_iterable_section()`` 调用。为适用于所有受支持的工具链，新增可迭代段目前必须在两者中都进行声明。

当 ``CONFIG_CMAKE_LINKER_GENERATOR=y`` 时，可迭代段的输出段由 ``zephyr_iterable_section()`` 调用生成。通过 ``zephyr_linker_sources()`` 注册的 ``.ld`` 片段中的所有 ``ITERABLE_SECTION_RAM/ROM`` 定义都会被忽略。当 ``CONFIG_CMAKE_LINKER_GENERATOR=n`` 时则相反：不处理 ``zephyr_iterable_section()`` 调用，由 ``.ld`` 脚本提供段定义。

由于 Zephyr 上游必须能够在这两种配置下构建，新增可迭代段必须在两处都进行声明。

创建可迭代段需要以下三个部分，它们使用的结构体名称以及 RAM 或 ROM 存放位置必须一致：

1. **C 代码**：定义结构体，并使用 :c:macro:`STRUCT_SECTION_ITERABLE` （或用于 ROM 的 ``const`` 变体）实例化条目。

2. **链接器布局**：通过以下两种方式声明（*上游要求两者都提供*）：

   - **CMake**：使用 ``zephyr_iterable_section()``，由 CMake 生成流程处理。
   - **链接脚本**：使用通过 ``zephyr_linker_sources()`` 注册的 ``ITERABLE_SECTION_RAM/ROM``，由基于模板的流程处理。


步骤 1：在 C 中定义数据
***********************

在公共头文件中定义结构体，并提供辅助宏，使用 :c:macro:`STRUCT_SECTION_ITERABLE` 实例化条目：

.. code-block:: c

    struct my_data {
             int a, b;
    };

    #define DEFINE_DATA(name, _a, _b) \
             STRUCT_SECTION_ITERABLE(my_data, name) = { \
                     .a = _a, \
                     .b = _b, \
             }

    ...

    DEFINE_DATA(d1, 1, 2);
    DEFINE_DATA(d2, 3, 4);
    DEFINE_DATA(d3, 5, 6);

对于存放于 ROM 的可迭代段，实例必须声明为 ``const``，以便编译器将其放入只读输入段。C 声明与 CMake 布局（参见步骤 2）必须一致地选择 RAM 或 ROM 作为存放位置。

步骤 2：在 CMake 中声明段
*************************

``zephyr_iterable_section()`` 的 ``NAME`` 参数必须与传给 :c:macro:`STRUCT_SECTION_ITERABLE` 的结构体名称一致。``GROUP`` 参数选择用于容纳所生成输出段的链接器分组。

存放于 RAM 的示例：

.. code-block:: cmake

   # CMakeLists.txt
   zephyr_iterable_section(NAME my_data GROUP DATA_REGION ${XIP_ALIGN_WITH_INPUT})

存放于 ROM 的示例（实例在 C 中声明为 ``const``）：

.. code-block:: cmake

   # CMakeLists.txt
   zephyr_iterable_section(NAME my_data GROUP RODATA_REGION)


完整参数列表及可用 ``GROUP`` 选项的详细说明，参见 ``cmake/modules/extensions.cmake`` 中的 ``zephyr_iterable_section()``。

步骤 3：提供链接脚本
********************

链接脚本使用 :c:macro:`ITERABLE_SECTION_RAM` 或 :c:macro:`ITERABLE_SECTION_ROM` 生成实际的段。

存放于 RAM：

.. code-block:: c

   /* sections-ram.ld */
   #include <zephyr/linker/iterable_sections.h>

   ITERABLE_SECTION_RAM(my_data, Z_LINK_ITERABLE_SUBALIGN)

存放于 ROM：

.. code-block:: c

   /* sections-rom.ld */
   #include <zephyr/linker/iterable_sections.h>

   ITERABLE_SECTION_ROM(my_data, Z_LINK_ITERABLE_SUBALIGN)

在 ``CMakeLists.txt`` 中注册链接脚本：

.. code-block:: cmake

   zephyr_linker_sources(<location> <path-to-ld-file>)

完整参数列表及可用 ``<location>`` 选项的详细说明，参见 ``cmake/modules/extensions.cmake`` 中的 ``zephyr_linker_sources()``。

遍历条目
********

段配置完成后，使用 :c:macro:`STRUCT_SECTION_FOREACH` 遍历其中的条目：

.. code-block:: c

   STRUCT_SECTION_FOREACH(my_data, data) {
           printk("%p: a: %d, b: %d\n", data, data->a, data->b);
   }

.. note::
   链接器按名称排序放置条目，因此上例将依次访问 ``d1``、``d2`` 和 ``d3``，与代码中定义它们的顺序无关。

API 参考
********

.. doxygengroup:: iterable_section_apis
