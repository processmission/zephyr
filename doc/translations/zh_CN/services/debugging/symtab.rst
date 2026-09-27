.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _symtab:

符号表 (Symtab)
###############

启用 Symtab 模块后，它将在 Zephyr 链接阶段生成完整的符号表，记录函数的名称和地址信息；对于包含大量函数的高级应用，预计会占用相当多的 ROM。

目前，在支持的架构上，它被用于在堆栈回溯期间查找函数名。


用法
****

应用程序可以通过包含 :file:`symtab.h` 头文件并调用 :c:func:`symtab_get` 来访问符号表数据结构。目前，我们仅提供 :c:func:`symtab_find_symbol_name` 函数，用于查找某个地址的符号名和偏移量。更高级的功能可以通过直接访问该数据结构的成员来实现。

配置
****

使用以下选项配置此模块。

* :kconfig:option:`CONFIG_SYMTAB` 启用符号表的生成。

API 文档
********

.. doxygengroup:: symtab_apis
