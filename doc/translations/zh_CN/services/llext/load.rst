.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

加载扩展
########

扩展构建完成并生成 ELF 文件后，可以使用 LLEXT API 将其加载到 Zephyr 应用程序中。LLEXT API 提供了将扩展加载到内存、访问其符号以及调用其函数的方法。

加载扩展
========

可以使用 :c:struct:`llext_loader` 的任意实现来加载扩展，该结构体包含一组函数指针，提供读取 ELF 数据所需的功能。加载器还提供 :c:func:`llext_load` 函数所需的一些最小上下文（内存）。系统已经提供了以下几种加载器：

 * 一种基于缓冲区的实现可用于处理位于可寻址内存中的 ELF，称为 :c:struct:`llext_buf_loader` 。要使用这种加载器，可以借助 :c:macro:`LLEXT_TEMPORARY_BUF_LOADER` 、 :c:macro:`LLEXT_PERSISTENT_BUF_LOADER` 或 :c:macro:`LLEXT_WRITABLE_BUF_LOADER` 宏之一，告知 LLEXT 相应的内存缓冲区类型。

 * 一种从文件系统中的文件读取数据的实现称为 :c:struct:`llext_fs_loader` 。使用 :c:macro:`LLEXT_FS_LOADER` 宏创建加载器时，必须提供文件路径。

 * 一种使用 semihosting 从主机文件系统读取文件的实现称为 :c:struct:`llext_semihost_loader` 。使用 :c:macro:`LLEXT_SEMIHOST_LOADER` 宏创建加载器时，必须提供文件路径。

通过调用 :c:func:`llext_load` 函数并传入扩展名称和已配置的加载器来加载扩展。调用成功完成后，扩展即被加载到内存中，随时可以使用。

.. note::
   启用 :ref:`用户模式 <usermode_api>` 时，扩展不会包含在任何用户内存域中。要允许从用户模式访问，必须调用 :c:func:`llext_add_domain` 函数。

初始化与清理扩展
================

扩展可以定义若干初始化函数，这些函数必须在加载之后、使用扩展中任何函数之前调用；这是 C++ 等支持对象构造函数概念的语言的常见做法。清理函数也是如此，必须在卸载扩展之前调用。

LLEXT 支持使用 :c:func:`llext_bringup` 函数调用 ELF 文件中 ``.preinit_array`` 和 ``.init_array`` 段列出的函数，并使用 :c:func:`llext_teardown` 函数调用 ``.fini_array`` 段列出的函数。这些 API 与 :ref:`用户模式 <usermode_api>` 兼容，因此既可以从内核上下文调用，也可以从用户上下文调用。

.. important::
   这些函数运行的代码完全由 ELF 文件的内容决定。如果其来源不可信，可能会带来安全隐患。

如果扩展需要专用线程，可以使用 :c:func:`llext_bootstrap` 函数来尽量减少样板代码。该函数的签名与 :c:func:`k_thread_create` API 兼容，它会先调用 :c:func:`llext_bringup` ，然后在同一上下文中调用用户指定的函数，最后在返回前调用 :c:func:`llext_teardown` 。

访问代码与数据
==============

要与新加载的扩展交互，宿主应用程序必须使用 :c:func:`llext_find_sym` 函数获取导出符号的地址。然后可以将返回的 ``void *`` 转换为适当的类型并使用。

调用无参数函数的包装器由 :c:func:`llext_call_fn` 提供。

需要直接访问新加载扩展各区域的高级用户，可以参考 :c:func:`llext_get_section_info` 和其他 LLEXT 检查 API。

使用后清理
==========

当扩展不再需要时，必须调用 :c:func:`llext_unload` 函数来释放扩展占用的内存。此调用完成后，之前获取的所有指向扩展中符号的指针都将失效。

故障排查
########

此功能正在积极开发中，因此可能会遇到一些问题。由于链接操作会修改二进制代码，出错时结果难以预测。一些常见问题包括：

* :c:func:`llext_find_sym` 的结果指向无效地址；

* 扩展中定义的常量和变量没有预期的值；

* 调用扩展中定义的函数会导致硬故障，或者从该函数返回后主应用程序的内存被破坏。

如果出现上述任何情况，以下提示可能有助于弄清问题：

* 确保将 :kconfig:option:`CONFIG_LLEXT_LOG_LEVEL` 设置为 ``DEBUG`` ，然后获取 :c:func:`llext_load` 调用的日志。

* 如果可能，请禁用内存保护（MMU/MPU），看看行为是否会有所不同。

* 尝试将扩展简化到能够复现该问题的最小代码。

* 使用调试器检查内存和寄存器，尝试了解正在发生的情况。有关详细信息，请参阅 :ref:`调试扩展 <llext_debug>` 。

如果问题仍然存在，请在 GitHub 仓库中提交 issue，并附上上述所有信息。
