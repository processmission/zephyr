.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _memory_management_api_virtual_memory:

虚拟内存
########

Zephyr 的虚拟内存（VM）允许开发者精细控制内存访问。要使用虚拟内存，平台必须支持内存管理单元（MMU），并在构建时启用。由于 Zephyr 主要面向嵌入式系统，其虚拟内存支持与传统操作系统略有不同：

内核映像映射
  未启用按需分页时，默认将内核映像（包括代码和数据）在物理地址空间与虚拟地址空间之间作 1:1 映射。若要采用其他方式，需谨慎调整链接器脚本。

辅助存储
  基本虚拟内存支持不会利用辅助存储扩展可用内存，可用内存上限与物理内存相同。

  * :ref:`memory_management_api_demand_paging` 可以利用辅助存储作为虚拟内存的后备存储，使可用内存大于实际物理内存。注意，必须显式启用按需分页。

  * 虽然虚拟地址空间可以大于物理地址空间，但未启用按需分页时，所有已映射的虚拟内存都必须有物理内存支撑。


Kconfig 选项
************

必选项
======

内核支持虚拟内存所需启用或定义的 Kconfig 选项如下。

* :kconfig:option:`CONFIG_MMU`：必须启用，内核才能支持虚拟内存。

* :kconfig:option:`CONFIG_MMU_PAGE_SIZE`：内存页大小，默认为 4KB。

* :kconfig:option:`CONFIG_KERNEL_VM_BASE`：虚拟地址空间的基地址。

* :kconfig:option:`CONFIG_KERNEL_VM_SIZE`：虚拟地址空间的大小，默认为 8MB。

* :kconfig:option:`CONFIG_KERNEL_VM_OFFSET`：内核映像起点相对于 :kconfig:option:`CONFIG_KERNEL_VM_BASE` 的偏移量。

可选项
======

* :kconfig:option:`CONFIG_KERNEL_DIRECT_MAP`：允许虚拟地址与物理地址之间采用 1:1 映射，而非由内核在虚拟地址空间中选择地址。这适合用于映射设备 MMIO 区域，以便更精确地控制访问。


内存映射概览
************

以下概述虚拟地址空间的内存布局。注意，代码中的 ``Z_*`` 宏可能随架构和 Kconfig 配置而具有不同含义，下面会具体说明。

.. code-block:: none
   :emphasize-lines: 1, 3, 9, 22, 24

   +--------------+ <- K_MEM_VIRT_RAM_START
   | Undefined VM | <- architecture specific reserved area
   +--------------+ <- K_MEM_KERNEL_VIRT_START
   | Mapping for  |
   | main kernel  |
   | image        |
   |              |
   |              |
   +--------------+ <- K_MEM_VM_FREE_START
   |              |
   | Unused,      |
   | Available VM |
   |              |
   |..............| <- grows downward as more mappings are made
   | Mapping      |
   +--------------+
   | Mapping      |
   +--------------+
   | ...          |
   +--------------+
   | Mapping      |
   +--------------+ <- memory mappings start here
   | Reserved     | <- special purpose virtual page(s) of size K_MEM_VM_RESERVED
   +--------------+ <- K_MEM_VIRT_RAM_END

* ``K_MEM_VIRT_RAM_START`` 是虚拟地址空间的起点，必须按页对齐。目前它与 :kconfig:option:`CONFIG_KERNEL_VM_BASE` 相同。

* ``K_MEM_VIRT_RAM_SIZE`` 是虚拟地址空间的大小，必须按页对齐。目前它与 :kconfig:option:`CONFIG_KERNEL_VM_SIZE` 相同。

* ``K_MEM_VIRT_RAM_END`` 就是（``K_MEM_VIRT_RAM_START`` + ``K_MEM_VIRT_RAM_SIZE``）。

* ``K_MEM_KERNEL_VIRT_START`` 与链接器脚本中指定的 ``z_mapped_start`` 相同，表示启动时内核映像起点的虚拟地址。

* ``K_MEM_KERNEL_VIRT_END`` 与链接器脚本中指定的 ``z_mapped_end`` 相同，表示启动时内核映像末尾的虚拟地址。

* ``K_MEM_VM_FREE_START`` 是可供内存映射分配地址的虚拟地址区域起点，其值取决于是否启用了 :kconfig:option:`CONFIG_ARCH_MAPS_ALL_RAM`。

  * 如果启用了该选项，说明所有物理内存均已映射到虚拟地址空间中，该值就等于（:c:macro:`DT_CHOSEN_SRAM_ADDR` + :c:macro:`DT_CHOSEN_SRAM_SIZE`）。

  * 如果未启用该选项，``K_MEM_VM_FREE_START`` 与 ``K_MEM_KERNEL_VIRT_END`` 相同，即内核映像的末尾。

* ``K_MEM_VM_RESERVED`` 是为支持内核功能而保留的区域，例如为按需分页保留部分地址。


虚拟内存映射
************

启动时建立映射
==============

一般而言，大多数受支持的架构会在启动时建立以下内存映射：

* ``.text`` 段只读且可执行，内核模式和用户模式均可访问。

* ``.rodata`` 段只读且不可执行，内核模式和用户模式均可访问。

* 其他内核段，如 ``.data``、``.bss`` 和 ``.noinit``，可读写但不可执行，仅内核模式可访问。

  * 创建线程时，会自动授予相应用户模式线程对其栈的读写权限。

  * 默认情况下，用户模式线程无法访问全局变量。如何在用户模式线程中使用全局变量，以及在线程之间共享数据，请参阅 :ref:`内存域与分区 <memory_domain>`。

这些映射的缓存模式取决于架构，可以是无缓存、回写或直写。

注意，SoC 还会有启动所需的附加映射，定义于各自的 SoC 配置中。这些映射通常包括初始化硬件所需的设备 MMIO 区域。


映射匿名内存
============

未使用的物理内存可以按需映射到虚拟地址空间。从概念上看，这类似于从堆中分配内存，但映射必须按页大小对齐，且具有更精细的访问控制。

* 可以使用 :c:func:`k_mem_map` 映射未使用的物理内存：

  * 请求大小必须为页大小的倍数。

  * 返回地址位于 ``K_MEM_VM_FREE_START`` 与 ``K_MEM_VIRT_RAM_END`` 之间的虚拟地址空间中。

  * 映射区域不保证在物理内存中连续。

  * 内核会自动在映射虚拟区域紧邻的前后位置分配保护页，用于捕获缓冲区下溢或上溢导致的访问问题。

* 可以通过 :c:func:`k_mem_unmap` 解除映射，即释放映射区域：

  * 务必向 :c:func:`k_mem_map` 和 :c:func:`k_mem_unmap` 传入相同的区域大小。解除映射函数在操作前不会检查该区域是否为有效映射。


API 参考
********

.. doxygengroup:: kernel_memory_management
