.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mem_mgmt_api:

内存属性
########

在 devicetree 中可以使用 ``zephyr,memory-attr`` 属性为内存区域标注属性。之后可以在运行时借助所提供的辅助库获取该属性及相关的内存区域。

该属性中可指定的一般属性集合在 :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr.h` 中定义并说明。

例如，要把 devicetree 中的某个内存区域标注为非易失、可缓存、乱序：

.. code-block:: devicetree

   mem: memory@10000000 {
       compatible = "mmio-sram";
       reg = <0x10000000 0x1000>;
       zephyr,memory-attr = <(DT_MEM_NON_VOLATILE | DT_MEM_CACHEABLE | DT_MEM_OOO)>;
   };

.. note::

   使用 ``zephyr,memory-attr`` 并不会真正创建任何内存区域。当需要根据 devicetree 定义的内存区域创建实际的段时，可以使用兼容项 :dtcompatible:`zephyr,memory-region`，它会在架构支持的情况下生成一个新的链接器段和区域。

``zephyr,memory-attr`` 属性还可用于设置可在运行时解释的架构相关和软件相关的自定义属性。其中之一便是根据 devicetree 定义的内存区域创建 MPU 区域，例如：

.. code-block:: devicetree

   mem: memory@10000000 {
       compatible = "mmio-sram";
       reg = <0x10000000 0x1000>;
       zephyr,memory-region = "NOCACHE_REGION";
       zephyr,memory-attr = <DT_MEM_ARM_MPU_RAM_NOCACHE>;
   };

有关 MPU 用法的更多细节，请参见 :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr-arm.h` 以及 :ref:`arm_cortex_m_developer_guide` 中的 :ref:`arm_cortex_m_mpu_considerations`。有关 Zephyr 如何处理缓存的细节，请参见 :ref:`cache_guide`。

处理和标注了属性的内存区域的常规且推荐的方式是使用所提供的 ``mem-attr`` 辅助库，即启用 :kconfig:option:`CONFIG_MEM_ATTR`。启用该选项后，内存区域列表及其属性会被编译到一个用户可访问的数组中，并提供一组函数，可用于查询、探测和操作这些区域与属性（更多细节见下一节）。

.. note::

   ``zephyr,memory-attr`` 属性只是对相关内存区域能力的描述，并不会对内存做任何实际设置。希望利用这些信息执行某些工作（例如根据该属性创建 MPU 区域）的用户、代码或子系统，必须使用所提供的 ``mem-attr`` 库或常规的 devicetree 辅助宏来完成所需的工作或设置。但请注意，对于某些架构（例如 ARM 和 ARM64），MPU 驱动会使用这些信息在启动时正确初始化缓存。参见 :kconfig:option:`CONFIG_ARM_MPU`、:kconfig:option:`CONFIG_RISCV_PMP` 等。

``mem-attr`` 库及其用法的测试位于 ``tests/subsys/mem_mgmt/mem_attr/``。

内存属性堆分配器
****************

可以利用内存属性 ``zephyr,memory-attr`` 来定义和创建一组内存堆，用户可以从具有特定属性或能力的内存堆中分配内存。

设置 :kconfig:option:`CONFIG_MEM_ATTR_HEAP` 后，每个标注了 :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr-sw.h` 中所列内存属性之一的内存区域都会被加入内存堆池，用于动态分配具有特定属性的内存缓冲区。

下面列出了一些可能的属性（并非完整列表）：

.. code-block:: none

   DT_MEM_SW_ALLOC_CACHE
   DT_MEM_SW_ALLOC_NON_CACHE
   DT_MEM_SW_ALLOC_DMA

例如，我们可以定义若干具有不同属性的内存区域，并使用相应的属性表明可以从这些区域动态分配内存：

.. code-block:: devicetree

   mem_cacheable: memory@10000000 {
       compatible = "mmio-sram";
       reg = <0x10000000 0x1000>;
       zephyr,memory-attr = <(DT_MEM_CACHEABLE | DT_MEM_SW_ALLOC_CACHE)>;
   };

   mem_non_cacheable: memory@20000000 {
       compatible = "mmio-sram";
       reg = <0x20000000 0x1000>;
       zephyr,memory-attr = <(DT_MEM_NON_CACHEABLE | ATTR_SW_ALLOC_NON_CACHE)>;
   };

   mem_cacheable_big: memory@30000000 {
       compatible = "mmio-sram";
       reg = <0x30000000 0x10000>;
       zephyr,memory-attr = <(DT_MEM_CACHEABLE | DT_MEM_OOO | DT_MEM_SW_ALLOC_CACHE)>;
   };

   mem_cacheable_dma: memory@40000000 {
       compatible = "mmio-sram";
       reg = <0x40000000 0x10000>;
       zephyr,memory-attr = <(DT_MEM_CACHEABLE      | DT_MEM_DMA |
                              DT_MEM_SW_ALLOC_CACHE | DT_MEM_SW_ALLOC_DMA)>;
   };

随后用户可以使用所提供的函数从这些区域中动态划分内存，库会根据给定的属性和大小负责从正确的堆中分配内存：

.. code-block:: c

   // Init the pool
   mem_attr_heap_pool_init();

   // Allocate 0x100 bytes of cacheable memory from `mem_cacheable`
   block = mem_attr_heap_alloc(DT_MEM_SW_ALLOC_CACHE, 0x100);

   // Allocate 0x200 bytes of non-cacheable memory aligned to 32 bytes
   // from `mem_non_cacheable`
   block = mem_attr_heap_aligned_alloc(ATTR_SW_ALLOC_NON_CACHE, 0x100, 32);

   // Allocate 0x100 bytes of cacheable and dma-able memory from `mem_cacheable_dma`
   block = mem_attr_heap_alloc(DT_MEM_SW_ALLOC_CACHE | DT_MEM_SW_ALLOC_DMA, 0x100);

当多个区域标注了相同的属性时，内存按如下方式分配：

1. 从 ``zephyr,memory-attr`` 属性包含所请求属性的那些区域中分配。

2. 在第 1 点所列的区域中，如果存在满足所请求大小的未分配空间，则优先从最小的区域分配

3. 如果没有足够的空间，则从下一个能够容纳所请求大小的更大区域分配

下面的示例说明了第 3 点：

.. code-block:: c

   // This memory is allocated from `mem_non_cacheable`
   block = mem_attr_heap_alloc(DT_MEM_SW_ALLOC_NON_CACHE, 0x100);

   // This memory is allocated from `mem_cacheable_big`
   block = mem_attr_heap_alloc(DT_MEM_SW_ALLOC_CACHE, 0x5000);

.. note::

    该框架假定用于创建堆的内存区域对代码可用，并且在初始化时就已存在。用户必须先初始化并设置好内存区域，然后才能调用 :c:func:`mem_attr_heap_pool_init`。

    这意味着该区域必须按 MPU / MMU 的要求正确配置（如有需要），并且能够从中真正创建堆，例如通过利用 ``zephyr,memory-region`` 属性创建合适的链接器段来容纳该堆。

API 参考
********

.. doxygengroup:: memory_attr_interface
.. doxygengroup:: memory_attr_heap
