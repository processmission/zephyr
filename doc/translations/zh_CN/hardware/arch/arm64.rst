.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _arm64_developer_guide:

ARM64 开发者指南
################

带超时的等待（WFxT）
********************

Arm WFxT 扩展提供 WFET 和 WFIT 指令，这些指令使用绝对虚拟计数器值作为超时期限。Zephyr 在运行时通过读取 ``ID_AA64ISAR2_EL1`` 中的 ``WFxT`` 字段来检测此扩展。Arm64 架构代码可以通过 ``is_wfxt_implemented()`` 查询是否支持此扩展，该函数声明于 :zephyr_file:`include/zephyr/arch/arm64/lib_helpers.h`。

当 Arm 架构定时器实现 :c:func:`arch_busy_wait` 时，如果处理器实现了 WFxT，Arm64 代码路径就会使用 WFET 来实现 :c:func:`k_busy_wait`。它根据 ``CNTVCT_EL0`` 计算截止时间，并重复执行 WFET，直到计数器达到该截止时间。由于允许 WFET 在超时前返回，因此必须使用循环。不支持 WFxT 的 CPU 则使用计数器轮询。具体实现请参见 :zephyr_file:`drivers/timer/arm_arch_timer.c`。

默认的 Arm64 :c:func:`arch_cpu_idle` 实现继续使用 WFI。使用 Arm 架构定时器时，内核的下一个超时会被设置到系统定时器中，由定时器中断唤醒 CPU。在保留该中断的情况下将 WFI 替换为 WFIT，并不能省去定时器设置或中断处理。若要避免该中断，就需要对内核超时记账、重新调度和 SMP 截止时间协调进行复杂的修改，这会带来显著的风险和维护成本，而收益尚未得到证实。

.. _arm64_mmu_dt_regions:

基于 Devicetree 的 MMU 区域映射
*******************************

在 ARM64 平台上，可以在编译时根据 Devicetree 自动填充 MMU 页表。任何具有 ``compatible = "zephyr,memory-region"`` 且同时带有 ``zephyr,memory-attr`` 属性的节点，都会由架构启动代码转换为静态的 ``arm_mmu_region`` 条目，无需针对各个 SoC 修改 ``mmu_regions.c``。

支持的内存属性
==============

仅接受 **普通** 内存类型。设备内存（外设 MMIO）必须通过 ``DEVICE_MMIO`` API 进行映射（参见 :ref:`device_model_api`）。

属性宏定义在 :zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr-arm64.h` 中，由通用的 ``DT_MEM_CACHEABLE`` 标志与架构特定的子属性组合而成：

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - DT 宏
     - 描述
   * - ``DT_MEM_ARM64_MMU_NORMAL``
     - 普通可缓存内存，采用写回策略（ ``DT_MEM_CACHEABLE | ATTR_ARM64_CACHE_WB`` ）
   * - ``DT_MEM_ARM64_MMU_NORMAL_NC``
     - 普通不可缓存内存（ ``0`` ）
   * - ``DT_MEM_ARM64_MMU_NORMAL_WT``
     - 普通可缓存内存，采用直写策略（ ``DT_MEM_CACHEABLE`` ）

Devicetree overlay 示例
=======================

.. code-block:: devicetree

   #include <zephyr/dt-bindings/memory-attr/memory-attr.h>
   #include <zephyr/dt-bindings/memory-attr/memory-attr-arm64.h>

   / {
       soc {
           /* Cacheable shared memory pool */
           shm0: memory@42000000 {
               compatible = "zephyr,memory-region";
               reg = <0x0 0x42000000 0x0 0x1000>;
               zephyr,memory-region = "SHM0";
               zephyr,memory-attr = <DT_MEM_ARM64_MMU_NORMAL>;
           };

           /* Non-cacheable DMA buffer */
           dma_buf: memory@43000000 {
               compatible = "zephyr,memory-region";
               reg = <0x0 0x43000000 0x0 0x1000>;
               zephyr,memory-region = "DMA_BUF";
               zephyr,memory-attr = <DT_MEM_ARM64_MMU_NORMAL_NC>;
           };
       };
   };

映射每个区域时，都会将 ``MT_P_RW_U_NA | MT_DEFAULT_SECURE_STATE`` 与根据 ``zephyr,memory-attr`` 得到的内存类型组合使用。

地址转换表大小设置
==================

每个位于不同 2 MB 边界范围内的映射区域，都需要额外分配一个三级页表。如果添加新区域后启动过程挂起且没有任何提示，请在开发板或测试配置中增大 :kconfig:option:`CONFIG_MAX_XLAT_TABLES` 的值：

.. code-block:: kconfig

   CONFIG_MAX_XLAT_TABLES=16

支持的属性组合
==============

所有非设备内存的属性组合均有效：通用的 ``DT_MEM_CACHEABLE`` 位用于选择可缓存或不可缓存；对于可缓存内存，架构特定的 ``ATTR_ARM64_CACHE_WB`` 子位用于选择写回或直写策略。
