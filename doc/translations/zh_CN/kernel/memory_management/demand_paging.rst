.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _memory_management_api_demand_paging:

按需分页
########

按需分页仅在当前执行上下文需要时，才将数据调入物理内存。从概念上看，物理内存被划分为页大小的页框，用于容纳数据。

Zephyr 内核映像自身始终驻留在物理内存中，绝不会成为换出候选。按需分页仅适用于：

* 运行时通过 :c:func:`k_mem_map()` 创建的匿名内存映射，以及
* 启用 :kconfig:option:`CONFIG_LINKER_USE_ONDEMAND_SECTION` 时，通过 ``__ondemand_func`` / ``__ondemand_rodata`` 属性显式放入按需链接器段的内存。

这与主流操作系统采用的模型相同：异常或中断的分派路径绝不位于可换出的页上，因此从结构上杜绝了在处理缺页时再次缺页。将代码或数据加入 ``__ondemand_*`` 段，表示贡献者明确选择允许该区域参与分页，同时有责任确保缺页处理程序自身的执行路径不会访问它。

.. note::

   早期 Zephyr 还支持基于 ``__pinned_*`` 链接器属性的选择性固定方案：仅让内核映像中带标记的部分常驻，其余部分按需分页。实践发现，该模型不够安全，并且可能需要大范围侵入式修改：CPU 异常分派可能使用线程位于可换出页上的特权栈；如果该页已被换出，x86 上会升级为双重故障，ARM64 上则会发生嵌套中止。此外，要穷尽标记缺页处理程序可达范围内的每个字节，包括调度器、驱动程序、libc 和加锁原语，既难以一次性建立这种保证，也无法持续维护。Zephyr 4.4 已移除 ``__pinned_*`` 属性系列、相应 Kconfig 选项（``LINKER_USE_PINNED_SECTION`` / ``LINKER_GENERIC_SECTIONS_PRESENT_AT_BOOT``）以及 ``K_*_PINNED_STACK_*`` 栈宏。完整分析见 :github:`108773`。

* 处理器尝试访问数据时，如果对应数据页已位于某个页框中，程序会继续执行，不会被打断。

* 处理器尝试访问的数据页不在任何页框中时，会发生缺页异常。如果有空闲页框，分页代码会将相应数据页从后备存储调入物理内存。如果没有空闲页框，则调用换出算法选择一个数据页，将其换出以腾出页框。如果该数据页自首次调入后被修改过，就将数据写回后备存储；如果未被修改，或已完成写回，该数据页便视为已换出，相应页框成为空闲。随后，分页代码调用后备存储，将所请求数据对应的数据页调入。后备存储将该页复制到空闲页框后，数据页就位于物理内存中，程序可以继续执行。

也可以通过 :c:func:`k_mem_page_in()` 和 :c:func:`k_mem_page_out()` 手动调入或换出页面。如果预计近期会需要某些数据页，可以使用 :c:func:`k_mem_page_in()` 提前调入，让它们预先驻留物理内存，从而减少缺页次数和延迟。对于预计较长时间不会访问的数据页，可以使用 :c:func:`k_mem_page_out()` 将其换出，释放页框。这样下一次调入时无需调用换出算法，速度更快。

也可以使用 :c:func:`k_mem_pin()` 将数据区域 **固定** 在物理内存中。必要时，该函数先调入该区域，再标记其页框，使换出算法永远不会选中它们，从而保证该区域常驻且访问不会引发缺页。这比 :c:func:`k_mem_page_in()` 提供更强的保证，适合必须始终可用、对延迟或安全性至关重要的数据。之后可使用 :c:func:`k_mem_unpin()` 解除固定，使页框重新成为可换出对象；解除固定本身不会换出该区域，如需立即换出，可随后调用 :c:func:`k_mem_page_out()`。

术语
****

数据页
  数据页是一块页大小的数据区域。它可以位于页框中，也可以被换出到某种后备存储。无论位于何处，都可以通过虚拟地址在 CPU 页表或等效结构中查找。其数据类型始终为 ``void *``，在需要指针运算的某些情况下则为 ``uint8_t *``。

页框
  页框是 RAM 中一块页大小的物理内存区域，是容纳数据页的容器，始终通过物理地址引用。Zephyr 约定使用 ``uintptr_t`` 表示物理地址。每个页框都对应一个 ``struct k_mem_page_frame`` 实例，用于存储元数据。页框具有以下标志：

  * ``K_MEM_PAGE_FRAME_FREE`` 表示页框尚未使用，位于空闲页框链表中。设置该标志时，其他标志都没有意义，且不得修改。

  * ``K_MEM_PAGE_FRAME_PINNED`` 表示页框被固定在内存中，绝不能换出。

  * ``K_MEM_PAGE_FRAME_RESERVED`` 表示该物理页由硬件保留，完全不应使用。

  * 物理页映射到虚拟内存地址时，设置 ``K_MEM_PAGE_FRAME_MAPPED``。

  * ``K_MEM_PAGE_FRAME_BUSY`` 表示页框当前正参与调入或换出操作。

  * ``K_MEM_PAGE_FRAME_BACKED`` 表示页框在后备存储中具有一份未修改的副本。

K_MEM_SCRATCH_PAGE
  这是提供给后备存储的特殊页的虚拟地址，用于：* 将数据页从 ``k_MEM_SCRATCH_PAGE`` 复制到指定位置；或 * 将数据页从指定位置复制到 ``K_MEM_SCRATCH_PAGE``。它作为调入和换出操作的中间页使用，必须映射为可读写，供后备存储代码访问。而数据页本身在虚拟地址空间中可能只映射为只读。如果将数据页直接提供给后备存储，就必须将其重新映射为可读写，这会带来安全问题，因为应用其他部分也将不再受只读限制。

分页统计
********

启用 :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM_NUM_BINS` 时，可以通过以下函数获取分页统计：

* 通过 :c:func:`k_mem_paging_stats_get()` 获取总体统计

* 启用 :kconfig:option:`CONFIG_DEMAND_PAGING_THREAD_STATS` 时，通过 :c:func:`k_mem_paging_thread_stats_get()` 获取各线程的统计

* 启用 :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM` 并定义 :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM_NUM_BINS` 后，可以获取执行时间直方图。注意，计时结果高度依赖架构、SoC 或开发板。强烈建议为具体应用定义 ``k_mem_paging_eviction_histogram_bounds[]`` 和 ``k_mem_paging_backing_store_histogram_bounds[]``。

  * 通过 :c:func:`k_mem_paging_histogram_eviction_get()` 获取换出算法的执行时间直方图

  * 通过 :c:func:`k_mem_paging_histogram_backing_store_page_in_get()` 获取后备存储执行调入操作的时间直方图

  * 通过 :c:func:`k_mem_paging_histogram_backing_store_page_out_get()` 获取后备存储执行换出操作的时间直方图

换出算法
********

换出算法决定哪个数据页及其对应页框可以被换出，以便为下一次调入操作腾出页框。内核分页代码会调用以下四个函数：

* :c:func:`k_mem_paging_eviction_init()` 用于初始化换出算法，在 ``POST_KERNEL`` 阶段调用。

* 每当数据页变为未来可换出的对象时，调用 :c:func:`k_mem_paging_eviction_add()`。

* 数据页不再允许换出时，调用 :c:func:`k_mem_paging_eviction_remove()`。这可能发生在数据页被固定、解除映射或即将换出时。

* :c:func:`k_mem_paging_eviction_select()` 用于选择要换出的数据页。函数通过写入参数 ``dirty``，告知调用者所选数据页自首次调入后是否被修改。如果返回时 ``dirty`` 位已设置，分页代码就会通知后备存储将数据页写回，更新其内容。函数返回指向所选数据页对应页框的指针。

还有一个由架构内存管理代码调用的函数 :c:func:`k_mem_paging_eviction_accessed()`，用于在数据页触发访问异常时对其进行标记。LRU 算法通过它将“已使用”的页重新入队。

目前提供两种换出算法：

* NRU（Not-Recently-Used，最近未使用）换出算法作为示例提供。它非常简单，根据数据页是否被访问和修改进行分级，再按级别选择换出页。

* 还提供 LRU（Least-Recently-Used，最近最少使用）换出算法，基于有序数据页队列实现。LRU 代码比 NRU 更复杂，但效率也显著更高，推荐用于生产环境。

实现新的换出算法时，必须实现 :c:func:`k_mem_paging_eviction_init()` 和 :c:func:`k_mem_paging_eviction_select()`。如果为算法启用 :kconfig:option:`CONFIG_EVICTION_TRACKING`，还必须实现 :c:func:`k_mem_paging_eviction_add()`、:c:func:`k_mem_paging_eviction_remove()` 和 :c:func:`k_mem_paging_eviction_accessed()`。

后备存储
********

后备存储负责在数据页对应的页框与存储介质之间调入或换出数据页。必须实现以下函数：

* :c:func:`k_mem_paging_backing_store_init()` 在 ``POST_KERNEL`` 阶段调用，用于初始化后备存储。

* :c:func:`k_mem_paging_backing_store_location_get()` 用于保留一个后备存储位置，以便换出数据页。该位置的 ``location`` 标记会传给 :c:func:`k_mem_paging_backing_store_page_out()`，执行实际换出操作。

* :c:func:`k_mem_paging_backing_store_location_free()` 用于释放后备存储位置（由 ``location`` 标记表示），使其可供后续换出操作使用。

* :c:func:`k_mem_paging_backing_store_location_query()` 用于获取与存储内容对应的 ``location`` 标记，以便将该内容映射到虚拟地址并按需调入。它尤其适合与 :kconfig:option:`CONFIG_DEMAND_MAPPING` 配合使用。

* :c:func:`k_mem_paging_backing_store_page_in()` 将数据页从给定 ``location`` 标记对应的后备存储位置，复制到 ``K_MEM_SCRATCH_PAGE`` 指向的页。

* :c:func:`k_mem_paging_backing_store_page_out()` 将数据页从 ``K_MEM_SCRATCH_PAGE`` 复制到给定 ``location`` 标记对应的后备存储位置。

* :c:func:`k_mem_paging_backing_store_page_finalize()` 在 :c:func:`k_mem_paging_backing_store_page_in()` 之后调用，以便更新页框结构体中的内部管理信息。它可以不执行任何操作。

实现新的后备存储时，必须实现上述函数。如有需要，:c:func:`k_mem_paging_backing_store_page_finalize()` 可以是空函数。

API 参考
********

.. doxygengroup:: mem-demand-paging

换出算法 API
============

.. doxygengroup:: mem-demand-paging-eviction

后备存储 API
============

.. doxygengroup:: mem-demand-paging-backing-store
