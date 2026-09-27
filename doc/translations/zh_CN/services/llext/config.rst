.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

配置
####

LLEXT 子系统可以使用以下 Kconfig 选项。

.. _llext_kconfig_heap:

哈佛架构
--------

:kconfig:option:`CONFIG_HARVARD`

        该架构使用独立的指令内存和数据内存。

:kconfig:option:`CONFIG_HARVARD` 不是由 LLEXT 子系统定义的 Kconfig。相反，它必须由开发板或 SoC 定义并选择，以表明 LLEXT 应支持哈佛架构构建。开发板或 SoC 还必须实现 :c:func:`arch_is_instr_mem` 。

堆大小
------

LLEXT 子系统需要为扩展相关数据分配一个堆。在分配静态堆时，以下选项控制此分配。

:kconfig:option:`CONFIG_LLEXT_HEAP_SIZE`

        LLEXT 堆的大小，单位为千字节。

对于使用哈佛架构的开发板，LLEXT 堆分为两个：一个位于指令内存中，另一个位于数据内存中。以下选项控制这些分配。

:kconfig:option:`CONFIG_LLEXT_INSTR_HEAP_SIZE`

        指令内存中 LLEXT 堆的大小，单位为千字节。

:kconfig:option:`CONFIG_LLEXT_DATA_HEAP_SIZE`

        数据内存中 LLEXT 堆的大小，单位为千字节。

或者，应用程序可以使用以下选项配置动态堆。

:kconfig:option:`CONFIG_LLEXT_HEAP_DYNAMIC`

        某些应用程序需要将扩展加载到启动时不存在的内存中，这类内存无法静态分配。让应用程序负责 LLEXT 堆的分配。不要静态分配 LLEXT 堆。

        应用程序必须调用 :c:func:`llext_heap_init` 来分配要用作 LLEXT 堆的缓冲区，否则 LLEXT 模块将无法加载。当应用程序不再需要 LLEXT 功能时，应调用 :c:func:`llext_heap_uninit` ，将缓冲区的控制权交还给应用程序。

.. note::

   启用 :ref:`用户模式 <usermode_api>` 时，堆大小必须足够大，以便扩展段能够按架构要求的对齐方式分配。

.. note::

   在哈佛架构上，应用程序必须调用 :c:func:`llext_heap_init_harvard` 。

LLEXT 堆的底层数据结构默认为 :c:struct:`k_heap` ，但对于非元数据（即扩展区域），可以通过为 :kconfig:option:`CONFIG_LLEXT_HEAP_MANAGEMENT` 选择 :kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK` 将其改为 :c:type:`sys_mem_blocks_t` 。

:kconfig:option:`CONFIG_LLEXT_HEAP_MANAGEMENT`

        选择用于在 LLEXT 堆内存中存储扩展区域的内存管理 API。此选择不会影响 LLEXT 元数据，元数据始终使用 :c:struct:`k_heap` 管理。

:kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK`

        使用 :c:type:`sys_mem_blocks_t` API 管理扩展区域的 LLEXT 堆内存。每个区域至少分配一个块。必须谨慎选择块大小，以确保扩展区域具有正确的对齐。

.. note::

   :kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK` 不支持 :kconfig:option:`CONFIG_LLEXT_HEAP_DYNAMIC` 。

堆将分为两个，每个子堆的大小由以下选项控制。

:kconfig:option:`CONFIG_LLEXT_EXT_HEAP_SIZE`

        可用于 LLEXT 扩展段的堆大小，单位为千字节。必须是 :kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK_BLOCK_SIZE` 的倍数。如果选择 :kconfig:option:`CONFIG_HARVARD` ，则会被 :kconfig:option:`CONFIG_LLEXT_INSTR_HEAP_SIZE` 和 :kconfig:option:`CONFIG_LLEXT_DATA_HEAP_SIZE` 取代。

:kconfig:option:`CONFIG_LLEXT_METADATA_HEAP_SIZE`

        可用于 LLEXT 元数据的堆大小，单位为千字节。

另一个选项控制块大小。

:kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK_BLOCK_SIZE`

        LLEXT :c:type:`sys_mem_blocks_t` 堆的块大小，单位为字节。如果启用 MMU 或 MPU，则必须等于 ``LLEXT_PAGE_SIZE`` 或是其倍数。块大小还必须等于任何扩展区域所需最大对齐值的倍数，或与之相等。如果选择了 :kconfig:option:`CONFIG_MPU_REQUIRES_POWER_OF_TWO_ALIGNMENT` 且区域较大，则可能需要非常大的块大小才能满足对齐要求。

堆的放置
--------

LLEXT 堆具有自定义段。非哈佛堆段（ ``.llext_heap`` ，或者在选择 :kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK` 时的 ``.llext_metadata_heap`` 和 ``.llext_ext_heap`` ）与文件 :file:`include/zephyr/linker/common-noinit.ld` 中的 ``.noinit`` 段放在一起。如果没有任何链接脚本包含此文件，则需要手动放置非哈佛 LLEXT 堆段。一种方法是在链接脚本中将 :file:`snippets-noinit.ld` 包含在 ``.noinit`` 段之后。

.. code-block:: none

   /* Located in generated directory. This file is populated by the
    * zephyr_linker_sources() CMake function.
    */
   #include <snippets-noinit.ld>

在开发板、SoC 或架构的 :file:`CMakeFiles.txt` 中将该文件添加为链接器源文件。

.. code-block:: cmake

   zephyr_linker_sources(NOINIT snippets-noinit.ld)

然后，在与 :file:`CMakeFiles.txt` 相同的目录中创建一个名为 :file:`noinit.ld` 的文件。

.. code-block:: none

   #if defined(CONFIG_LLEXT) && !defined(CONFIG_LLEXT_CUSTOM_HEAP_PLACEMENT)
   *(.llext_heap)
   *(.llext_ext_heap)
   *(.llext_metadata_heap)
   #endif /* CONFIG_LLEXT && !CONFIG_LLEXT_CUSTOM_HEAP_PLACEMENT */

对于 ARC，哈佛指令和数据堆段（ ``.llext_instr_heap`` 和 ``.llext_data_heap`` ）在架构级别放置于指令内存和数据内存中。如果使用具有哈佛架构的非 ARC 开发板，则需要手动放置 ``.llext_instr_heap`` 和 ``.llext_data_heap`` 。

.. warning::

   如果放置 ``.llext_instr_heap`` 的指令内存在加载和链接扩展时不可写，LLEXT 将无法加载扩展。

也可以通过提供自定义链接脚本指定放置位置。

:kconfig:option:`CONFIG_CUSTOM_LINKER_SCRIPT`

        要使用的链接脚本路径，用于替代开发板定义的链接脚本。

        链接脚本必须基于 Zephyr 提供的版本，因为内核可能要求特定的布局或特定区域。

        当应用程序需要在链接脚本中添加段并避免修改 Zephyr 提供的脚本时，这非常有用。

使用自定义链接脚本时，可能需要覆盖默认放置位置。例如，您可能希望在链接脚本中包含 :file:`include/zephyr/linker/common-noinit.ld` ，但将堆段放到其他地方。为此，请选择以下选项。

:kconfig:option:`CONFIG_LLEXT_CUSTOM_HEAP_PLACEMENT`

        移除链接脚本中 LLEXT 堆段的默认放置位置，允许用户自行放置堆。

字粒度访问指令内存堆
--------------------

字粒度访问指令内存是一种可按字节寻址的指令内存，但只能通过字大小且对齐的加载和存储进行访问。LLEXT 子系统目前仅支持在 Xtensa 架构上将指令堆放置在字粒度访问指令内存中。对非 Xtensa 架构的支持将在未来根据请求添加。

要在字粒度访问指令内存中使用带指令堆的 LLEXT，您的 Xtensa SoC 或开发板必须在 :kconfig:option:`CONFIG_HARVARD` 之外选择以下选项。

:kconfig:option:`CONFIG_ARCH_HAS_WORD_GRANULAR_ACCESS_INSTR_MEM`

        此选项支持访问可按字节寻址的字粒度访问指令内存。

如果使用堆的默认底层数据结构 :c:struct:`k_heap` ，请启用以下选项。

:kconfig:option:`CONFIG_SYS_HEAP_BIG_ONLY`

        选择此选项可针对大堆优化代码。它可以适应任何堆大小，但对于小型堆，内存使用效率不会那么高。

如果未选择此选项，在指令堆初始化期间将执行对指令内存的非对齐和窄访问。

接下来，按照上文中的堆放置说明，将 LLEXT 指令堆放置到该指令内存中。请确保您的 SoC 或开发板除实现 :c:func:`arch_is_instr_mem` 外，还实现 :c:func:`arch_memcpy_to_instr` 和 :c:func:`arch_memcpy_from_instr` 。字粒度访问库中的 :c:func:`memcpy_to_word_granular` 和 :c:func:`memcpy_from_word_granular` 函数可能会有所帮助。

您可以将 ELF 缓冲区放在 RAM 中。加载时，LLEXT 子系统会将 text 区域强制放到指令堆上（即使 ELF 缓冲区可写），以便其可执行，并在加载和链接期间访问 text 区域时遵守字粒度访问约束。

.. warning::

   当指令堆位于字粒度访问指令内存中时，只能使用缓冲区加载器（ :c:struct:`llext_buf_loader` ）来加载 ELF。

请注意，扩展自身负责确保此后对指令内存的任何访问也遵守这些约束。

如果仍然遇到加载/存储异常，可以使用以下选项为 Xtensa 启用无符号加载/存储异常处理程序。

:kconfig:option:`CONFIG_XTENSA_EMULATE_UNSUPPORTED_UNSIGNED_LOAD_STORE`

        当无符号加载/存储指令触发不支持的加载/存储异常时，异常处理程序将使用支持的按字大小对齐的加载/存储自行执行该操作。目前不支持 VLIW。

如选项说明所述，要使用此选项，还必须禁用 VLIW，因为启用 VLIW 会导致编译器生成有符号加载/存储指令。

:kconfig:option:`CONFIG_COMPILER_CODEGEN_VLIW_DISABLED`

        明确指示编译器绝不生成 VLIW 指令。

.. _llext_kconfig_type:

ELF 目标文件类型
----------------

LLEXT 子系统支持加载不同类型的扩展；可以通过选择以下 Kconfig 选项之一来设置类型：

:kconfig:option:`CONFIG_LLEXT_TYPE_ELF_OBJECT`

        将可重定位文件构建并用作 LLEXT 子系统的二进制目标文件类型。使用一次编译器调用来生成目标文件。

:kconfig:option:`CONFIG_LLEXT_TYPE_ELF_RELOCATABLE`

        将可重定位（部分链接）文件构建并用作 LLEXT 子系统的二进制目标文件类型。这些目标文件由链接器将多个目标文件合并为一个而生成。

:kconfig:option:`CONFIG_LLEXT_TYPE_ELF_SHAREDLIB`

        将共享库构建并用作 LLEXT 子系统的二进制目标文件类型。使用标准链接过程从多个目标文件生成共享库。

        .. note::

           目前 ARM 架构不支持此功能。

.. _llext_kconfig_storage:

尽量减少分配
------------

LLEXT 子系统的加载机制默认使用 seek/read 抽象，并将所有数据复制到已分配的内存中；这样做是为了让扩展可以从任何存储介质加载。不过，有时数据已经位于 RAM 中的缓冲区里，不需要复制。以下选项允许 LLEXT 子系统在这种情况下优化内存占用。

:kconfig:option:`CONFIG_LLEXT_STORAGE_WRITABLE`

        允许通过直接引用 ELF 缓冲区中的段数据来加载扩展。为使其有效，需要使用支持 ``peek`` 功能的 ELF 加载器，例如 :c:struct:`llext_buf_loader` 。

        .. warning::

           应用程序必须确保用于加载扩展的缓冲区在扩展卸载之前保持已分配状态。

        .. note::

           这会在链接阶段直接修改缓冲区的内容。扩展卸载后，必须重新加载缓冲区，然后才能在对 :c:func:`llext_load` 的调用中再次使用它。

.. _llext_symbol_groups:

符号组
------

所有 LLEXT 符号都属于某个组，每个组是否包含在导出符号表中由相应的 Kconfig 符号控制。可以使用 :c:macro:`EXPORT_GROUP_SYMBOL` 和 :c:macro:`EXPORT_GROUP_SYMBOL_NAMED` 宏将符号作为组的一部分导出。例如，以下代码将符号 ``memcpy`` 作为 ``LIBC`` 组的一部分导出：

.. code:: c

   EXPORT_GROUP_SYMBOL(LIBC, memcpy);

组名称可以任意命名，但必须全部大写。对于 C 代码中使用的每个组， **必须** 有形式如下的对应 Kconfig 符号：

.. code::

   config LLEXT_EXPORT_SYMBOL_GROUP_{GROUP_NAME}
      bool "Export all symbols from the {GROUP_NAME} group"

符号的默认组（使用 :c:macro:`EXPORT_SYMBOL` 或 :c:macro:`EXPORT_SYMBOL_NAMED` 声明的那些符号）是 ``UNASSIGNED`` 组。按照上述规则，该组的包含与否由 :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_UNASSIGNED` 控制。

Zephyr 当前定义的组如下：

.. csv-table:: Zephyr LLEXT 符号组
  :header: 组名称, Kconfig 符号, 描述

  ``UNASSIGNED``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_UNASSIGNED`, 没有显式组的符号
  ``SYSCALL``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_SYSCALL`, Zephyr 内核系统调用
  ``LIBC``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_LIBC`, C 标准库函数（例如 :c:func:`memcpy` 等）
  ``DEVICE``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_DEVICE`, Devicetree 设备

.. _llext_kconfig_slid:

使用 SLID 进行符号查找
----------------------

加载扩展时，LLEXT 子系统必须找到扩展引用的、驻留在主应用程序中的所有符号的地址。为此，主二进制文件包含一个 LLEXT 专用符号表，其中为主应用程序导出给扩展的每个符号保存一个符号名到地址的映射条目。在扩展加载时，LLEXT 链接器可以在该表中搜索。由于字符串比较的特性，此过程相当慢，并且随着导出符号数量的增加，该表占用的空间可能会变得很大。

:kconfig:option:`CONFIG_LLEXT_EXPORT_BUILTINS_BY_SLID`

        对 Zephyr 二进制文件和所有正在构建的扩展执行额外的处理步骤，将符号表中的每个字符串转换为称为符号链接标识符（SLID）的指针大小哈希值，并将其存储在二进制文件中。

        这样可以通过使用基于整数的比较而不是基于字符串的比较来加速符号查找过程。基于 SLID 的链接的另一个好处是，不再需要将符号名称存储在二进制文件中，从而显著减小符号表大小。

        .. note::

           此选项目前与 :ref:`LLEXT EDK <llext_build_edk>` 不兼容。

        .. note::

           不支持在主二进制文件和扩展中对此选项使用不同的值。例如，如果主应用程序使用 ``CONFIG_LLEXT_EXPORT_BUILTINS_BY_SLID=y`` 构建，则禁止加载使用 ``CONFIG_LLEXT_EXPORT_BUILTINS_BY_SLID=n`` 编译的扩展。

EDK 配置
--------

影响 LLEXT EDK 生成和行为的选项在 :ref:`llext_kconfig_edk` 中描述。
