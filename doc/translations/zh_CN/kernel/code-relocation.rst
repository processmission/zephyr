.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _code_data_relocation:

代码与数据重定位
################

概述
****
此功能可将所需文件中的 .text、.rodata、.data 和 .bss 段重定位到所需内存区域。内存区域和文件以字符串形式传给 :ref:`gen_relocate_app.py` 脚本，该脚本始终由 CMake 内部调用。

此脚本提供一种可靠的方法，无需修改代码即可重新安排内存内容。简单来说，它为一组文件统一完成 ``__attribute__((section("name")))`` 的工作。

可以使用正则表达式过滤器，仅选择需要重定位的段。

详情
****
内存区域和文件通过一个文件传给 :ref:`gen_relocate_app.py` 脚本，其中每行指定要放入给定区域的文件列表。

此类文件的示例如下：

  .. code-block:: none

     SRAM2:/home/xyz/zephyr/samples/hello_world/src/main.c,
     SRAM1:/home/xyz/zephyr/samples/hello_world/src/main2.c,

脚本使用以下参数调用：``python3 gen_relocate_app.py -i input_file -o generated_linker -c generated_code``

在 ``prj.conf`` 中启用 Kconfig 选项 :kconfig:option:`CONFIG_CODE_DATA_RELOCATION` 后，就会调用此脚本并执行所需的重定位。

此脚本还会触发生成 ``linker_relocate.ld`` 和 ``code_relocation.c`` 文件。``linker_relocate.ld`` 创建适当的段，并链接所有选定文件中所需的函数或变量。

.. note::

   主链接器脚本中的 text 段分为两部分：第一部分包含向量表及其他调试相关信息，第二部分包含完整的 text 段。这样才能强制将所需函数和数据变量放到正确位置。这是由链接器行为决定的：链接器只执行一次链接，因此必须拆分 text 段，为生成的链接器脚本留出位置。

``code_relocation.c`` 文件包含初始化 data 段和复制 text 段（启用 XIP 时）所需的代码，还包含将 bss 清零以及将数据从 ROM 复制到所需内存类型的代码。

**启用此功能的步骤如下：**

* 在 ``prj.conf`` 文件中启用 :kconfig:option:`CONFIG_CODE_DATA_RELOCATION`。

* 在项目的 ``CMakeLists.txt`` 文件中指定所有需要重定位的文件。

  ``zephyr_code_relocate(FILES src/main.c LOCATION SRAM2)``

  其中，第一个参数指定一个或多个文件，第二个参数指定其必须放置的内存。

  .. note::

     可按需多次调用 ``zephyr_code_relocate()`` 函数。

其他配置
========
本节介绍可在 ``CMakeLists.txt`` 中设置的其他配置选项。

* 如果内存为 ``SRAM1``、``SRAM2``、``CCD`` 或 ``AON``，则将整个目标文件放入相应的段。例如：

  .. code-block:: cmake

     zephyr_code_relocate(FILES src/file1.c LOCATION SRAM2)
     zephyr_code_relocate(FILES src/file2.c LOCATION SRAM1)

* 如果内存类型后附加 ``_DATA``、``_TEXT``、``_RODATA``、``_BSS`` 或 ``_NOINIT``，则仅将所选部分放入所需内存区域。例如：

  .. code-block:: cmake

     zephyr_code_relocate(FILES src/file1.c LOCATION SRAM2_DATA)
     zephyr_code_relocate(FILES src/file2.c LOCATION SRAM2_TEXT)

* 也可以同时附加多个区域，例如 ``SRAM2_DATA_BSS_NOINIT``。这会将所有数据，包括按值初始化、零初始化及未初始化的数据，都放入 ``SRAM2``。

* 可以向 ``FILES`` 参数传入多个文件，或使用 CMake 生成器表达式重定位以逗号分隔的文件列表。

  .. code-block:: cmake

     file(GLOB sources "file*.c")
     zephyr_code_relocate(FILES ${sources} LOCATION SRAM2)
     zephyr_code_relocate(FILES $<TARGET_PROPERTY:my_tgt,SOURCES> LOCATION SRAM2)

段过滤
======

默认情况下，指定文件的所有段都会被重定位。使用 ``FILTER`` 时，可提供正则表达式，仅选择需要重定位的段。

正则表达式匹配段名称。当文件使用 ``-ffunction-sections`` 和 ``-fdata-sections`` 构建时，可以借此选择文件中的符号；默认情况下就是如此。

  .. code-block:: cmake

     zephyr_code_relocate(FILES src/file1.c FILTER ".*\\.func1|.*\\.func2" LOCATION SRAM2_TEXT)

上述示例只会重定位文件 ``src/file1.c`` 中的 ``func1()`` 和 ``func2()``。

NOKEEP 标志
===========

默认情况下，生成 ``linker_relocate.ld`` 时，所有重定位的函数和变量都会标记为 ``KEEP()``。因此，如果输入文件含有未使用的符号，即使使用 ``--gc-sections`` 调用链接器，也不会丢弃它们。要覆盖此行为，可向 ``zephyr_code_relocate()`` 调用传入 ``NOKEEP``。

  .. code-block:: cmake

     zephyr_code_relocate(FILES src/file1.c LOCATION SRAM2_TEXT NOKEEP)

上述示例有助于确保 ``file1.c`` 的 .text 段中未使用的代码不会保留在 SRAM2 中。

NOCOPY 标志
===========

向 ``zephyr_code_relocate()`` 函数传入 ``NOCOPY`` 选项后，就不会在 ``code_relocation.c`` 中生成重定位代码。需要将特定文件或一组文件的内容移入 XIP 区域时，可以使用此标志。

此示例将 ``xip_external_flash.c`` 文件的 .text 段放入 ``EXTFLASH`` 内存区域，并直接从该区域执行（XIP）。.data 段则照常重定位到 SRAM。

  .. code-block:: cmake

     zephyr_code_relocate(FILES src/xip_external_flash.c LOCATION EXTFLASH_TEXT NOCOPY)
     zephyr_code_relocate(FILES src/xip_external_flash.c LOCATION SRAM_DATA)

重定位库
========

可以通过 ``zephyr_code_relocation()`` 的 LIBRARY 参数指定库名称来重定位库。例如，以下代码片段会将串口驱动程序重定位到 SRAM2：

  .. code-block:: cmake

    zephyr_code_relocate(LIBRARY drivers__serial LOCATION SRAM2)

提示
====

重定位 kernel/arch 文件时需要谨慎，其中某些文件包含在代码重定位之前执行的早期初始化代码。

可能需要额外配置 MPU/MMU，以确保目标内存区域允许执行代码。

示例与测试
==========

展示此功能的测试位于 ``$ZEPHYR_BASE/tests/application_development/code_relocation``。

此测试展示如何使用代码重定位功能。

此测试使用从 ``include/zephyr/arch/arm/cortex_m/scripts/linker.ld`` 派生的自定义链接器文件，将三个文件中的 .text、.data 和 .bss 放入 SRAM 的不同位置。

展示 NOCOPY 标志的示例位于：:zephyr:code-sample:`code_relocation_nocopy`。
