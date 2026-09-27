.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _memory_domain:

内存保护设计
############

Zephyr 的内存保护设计面向具有 MPU（内存保护单元）硬件的微控制器。我们也支持 x86 等带分页 MMU（内存管理单元）的架构，但此时会使用恒等映射页表，将 MMU 当作 MPU 使用。

下文统一使用 MPU 术语；具有 MMU 的系统可视为拥有无限数量可编程区域的 MPU。

启用 Zephyr 内存保护功能后，内存访问配置分为几个不同层次，下面逐一说明：

启动时内存配置
**************

这是内核启动后的 MPU 配置，应包含以下内容：

- 为基本硬件和驱动程序功能所需的特殊缓存或回写策略配置内存区域。注意，大多数 MPU 都具有默认内存访问策略映射的概念，可以将其启用为“背景”映射，覆盖未由 MPU 区域配置的内存。强烈建议使用这一功能，以便为最终用户保留尽可能多的可用 MPU 区域。在 ARMv7-M/ARMv8-M 上，它称为系统地址映射（System Address Map），其他 CPU 可能具有类似能力。有关如何在设备树中标注系统映射的信息，请参阅 :ref:`mem_mgmt_api`。

- 为程序代码和只读数据配置一个或多个只读、可执行且用户模式可访问的区域。也可以进一步细分为用于只读数据的只读区域，以及用于代码的只读、可执行区域，但这需要额外的 MPU 区域。这是用户模式线程读取只读数据和取指的必要条件。

- 根据配置，还可能需要用户可访问的读写区域，以支持 GCOV、HEP 等额外功能。

假定存在允许特权模式访问所需任意内存的背景映射，并已定义允许用户模式访问代码和只读数据的区域，则这些配置已足以满足启动时需求。

硬件栈溢出检测
**************

:kconfig:option:`CONFIG_HW_STACK_PROTECTION` 是一项可选功能，用于检测系统在特权模式下运行时的栈缓冲区溢出。它检测的是整个栈缓冲区溢出，而非单个栈帧溢出；后者应使用编译器辅助的 :kconfig:option:`CONFIG_STACK_CANARIES`。

与特权模式下的任何崩溃一样，特权模式栈溢出后无法保证系统整体状态正常，因此任何此类情况都应视为严重错误。但知道何时发生了这些溢出仍然很有用，因为若无可靠的检测逻辑，栈缓冲区溢出时系统可能以难以理解的方式崩溃，或出现未定义行为。

有些系统在运行时创建一个只读的 MPU“保护”区域，位于特权模式栈缓冲区的起始位置或紧邻其前方，以实现此功能。栈溢出时会产生异常。

此功能是可选的，检测用户模式栈溢出并不需要它；根据 MPU 设计的不同，禁用它可能释放 1 至 2 个 MPU 区域。

其他系统可能具有专门检测栈溢出的 CPU 支持，因此不需要额外的 MPU 区域。

线程栈
******

任何在用户模式下运行的线程都需要访问自身的栈缓冲区。上下文切换到用户模式线程时，会根据栈缓冲区边界设置专用 MPU 区域或 MMU 页表项。线程超出栈缓冲区后，会开始将数据压入无权访问的内存，从而产生内存访问违规异常。

注意，用户线程可以访问同一内存域中其他用户线程的栈。这是架构支持内存域的最低要求。如果架构通过 :kconfig:option:`CONFIG_ARCH_MEM_DOMAIN_SUPPORTS_ISOLATED_STACKS` 声明此能力，则可以进一步限制栈访问，使每个用户线程只能访问自身栈。受支持时，此行为默认启用；如果架构支持两种运行模式，可以通过 :kconfig:option:`CONFIG_MEM_DOMAIN_ISOLATED_STACKS` 选择禁用。但有些架构可能始终启用此行为，因此无法禁用该选项。无论这些 Kconfig 如何设置，用户线程都不能访问其内存域之外其他用户线程的栈。

线程资源池
**********

少数作为系统调用执行的内核 API 需要分配堆内存。这些内存仅供内核使用，用户模式不能直接访问。要使用这些系统调用，调用线程必须为自身分配一个资源池，即 :c:struct:`k_heap` 对象。通过 :c:func:`z_thread_malloc` 从线程资源池分配内存，并通过 :c:func:`k_free` 释放。

使用资源池的 API 如下；对于不希望应用程序进行堆分配的用户，也列出了可用的替代方案：

 - :c:func:`k_stack_alloc_init` 创建 k_stack，使用从资源池分配的存储缓冲区，而不是用户提供的缓冲区。替代方案是通过 :c:macro:`K_STACK_DEFINE()` 声明在启动时自动初始化的 k_stack，或在特权模式下通过 :c:func:`k_stack_init` 初始化 k_stack。

 - :c:func:`k_msgq_alloc_init` 创建 k_msgq 对象，使用从资源池分配的存储缓冲区，而不是用户提供的缓冲区。替代方案是通过 :c:macro:`K_MSGQ_DEFINE()` 声明在启动时自动初始化的 k_msgq，或在特权模式下通过 :c:func:`k_msgq_init` 初始化 k_msgq。

 - 从用户模式调用 :c:func:`k_poll` 时，需要在等待事件期间为传入的 events 数组创建内核侧副本。无论 :c:func:`k_poll` 因何原因返回，该副本都会被释放。

 - :c:func:`k_queue_alloc_prepend` 和 :c:func:`k_queue_alloc_append` 会分配容器结构体来放置数据，因为定义队列的内部管理信息不能放在用户提供的内存中。

 - :c:func:`k_object_alloc` 允许在运行时动态分配整个内核对象，并向调用者返回可用的对象指针。

相关 API 为 :c:func:`k_thread_heap_assign`，它为目标线程指定用于这些分配的 k_heap。

如果启用了系统堆，则可通过 :c:func:`k_thread_system_pool_assign` 使用系统堆，但最好让系统上运行的不同逻辑应用程序拥有各自的池。

内存域
******

内核确保每个用户线程都能访问自身的栈缓冲区、程序代码和只读数据。内存域 API 用于授予用户线程对额外内存块的访问权限。

从概念上说，内存域是由若干内存分区构成的集合。域内内存分区的最大数量受可用 MPU 区域数量限制，因此应尽量减少启动时占用的 MPU 区域数量。

内存域 *并非* 用于控制特权模式的内存访问。某些情况下，这种影响可能无法避免；例如，有些架构不允许定义用户模式只读、特权模式可读写的区域。处理此类区域时必须格外谨慎，以免内核访问该区域时意外崩溃。任何试图通过内存域 API 控制特权模式访问的做法，充其量也只是未定义行为；特权模式访问策略只应由启动时内存区域控制。

内存域 API 仅供特权模式使用。用户模式对内存域唯一的控制方式，是用户线程创建的子线程会自动成为父线程所属域的成员。

所有线程都是某个内存域的成员，包括特权线程（尽管这不影响其内存访问）。如果没有为线程明确分配内存域，也没有从父线程继承内存域成员关系，则会将其分配到默认域 ``k_mem_domain_default``。主线程启动时属于默认域。

内存分区
========

每个内存分区由内存地址、大小和访问属性组成，用于控制系统内存访问。定义内存分区需遵守以下约束：

- 分区必须代表底层内存管理硬件可编程的内存区域，并满足底层硬件的约束。例如，许多基于 MPU 的系统要求分区大小为 2 的某次幂，并按自身大小对齐。对于基于 MMU 的系统，分区必须按页对齐，且大小为页大小的整数倍。

- 同一内存域内的分区不得相互重叠，分区之间没有优先级之分。内存域中的分区被视为具有高于启动时内存区域的优先级，但内存域分区是否可以与启动时内存区域重叠，取决于架构。

- 同一个分区可以在多个内存域中指定。例如，多个域可以授予对同一共享内存区域的访问权限。

- 必须谨慎决定通过分区暴露哪些内存。不应让用户模式直接访问包含内核私有数据的内存。

- 内存域分区用于控制系统 RAM 访问。架构可能不支持配置不对应 RAM 的内存分区；基于 MMU 的系统就是如此。

内存分区有两种定义方式：手动或自动。

手动内存分区
------------

以下代码声明一个全局数组 ``buf``，然后为其声明一个可加入内存域的读写分区：

.. code-block:: c

    uint8_t __aligned(32) buf[32];

    K_MEM_PARTITION_DEFINE(my_partition, buf, sizeof(buf),
                           K_MEM_PARTITION_P_RW_U_RW);

如果希望将分散在多个 C 文件中的多个对象放入单一分区，这种方法的扩展性并不好。

自动内存分区
------------

自动内存分区由构建系统创建。所有需要放入分区的全局变量都会标记其目标分区。构建系统随后将它们合并到一个连续内存块中，在启动时将其中的 BSS 变量清零，并定义一个基址和大小适当、包含所有已标记数据的内存分区。

.. figure:: auto_mem_domain.png
   :alt: Automatic Memory Domain build flow
   :align: center

   自动内存域构建流程

自动内存分区只能配置为读写区域，使用 :c:macro:`K_APPMEM_PARTITION_DEFINE()` 定义。随后，已初始化数据通过 :c:macro:`K_APP_DMEM()`、BSS 通过 :c:macro:`K_APP_BMEM()` 将全局变量放入该分区。

.. code-block:: c

    #include <zephyr/app_memory/app_memdomain.h>

    /* Declare a k_mem_partition "my_partition" that is read-write to
     * user mode. Note that we do not specify a base address or size.
     */
    K_APPMEM_PARTITION_DEFINE(my_partition);

    /* The global variable var1 will be inside the bounds of my_partition
     * and be initialized with 37 at boot.
     */
    K_APP_DMEM(my_partition) int var1 = 37;

    /* The global variable var2 will be inside the bounds of my_partition
     * and be zeroed at boot size K_APP_BMEM() was used, indicating a BSS
     * variable.
     */
    K_APP_BMEM(my_partition) int var2;

构建系统会确保 ``my_partition`` 的基址正确对齐，区域总大小符合内存管理硬件要求，必要时会加入填充。

创建多个分区时，可以使用 ``app_macro_support.h`` 中提供的可变参数预处理器宏：

.. code-block:: c

    FOR_EACH(K_APPMEM_PARTITION_DEFINE, part0, part1, part2);

静态库全局变量的自动分区
~~~~~~~~~~~~~~~~~~~~~~~~

设置自动内存分区的构建时逻辑位于 ``scripts/build/gen_app_partitions.py``。如果静态库链接进 Zephyr，可以使用 ``--library`` 参数将该库中的所有全局变量放入指定内存分区。

例如，启用 Newlib C 库时，其全部全局变量都需要放入 ``z_libc_partition``。顶层 ``CMakeLists.txt`` 中对该脚本的调用会加入以下内容：

.. code-block:: none

    gen_app_partitions.py ... --library libc.a z_libc_partition ..

对于预编译库，不支持在项目级配置或构建文件中表达此设置；必须编辑顶层 ``CMakeLists.txt``。

对于通过 ``zephyr_library`` 或 ``zephyr_library_named`` 创建的 Zephyr 库，可以使用 ``zephyr_library_app_memory`` 函数指定库中所有全局变量应放入的内存分区。

.. _memory_domain_predefined_partitions:

预定义内存分区
--------------

系统预定义了几个内存分区：

 - ``z_malloc_partition``：此分区包含 libc malloc() 使用的系统级内存池。由于可能发生资源饥饿，不建议从全局池分配堆内存；最好定义多个 sys_heap 对象，并将其分配给特定内存域。

 - ``z_libc_partition``：包含 C 库和运行时所需的全局变量。使用 Minimal C 库或 Newlib C 库时需要它。启用 :kconfig:option:`CONFIG_STACK_CANARIES` 时也需要它。

库专用分区列在 :zephyr_file:`include/zephyr/app_memory/partitions.h` 中。例如，要从用户模式使用 MBEDTLS 库，必须将 ``k_mbedtls_partition`` 加入内存域。

内存域用法
==========

创建内存域
----------

内存域使用 :c:struct:`k_mem_domain` 类型的变量定义，随后必须调用 :c:func:`k_mem_domain_init` 初始化。

以下代码定义并初始化一个空内存域。

.. code-block:: c

    struct k_mem_domain app0_domain;

    k_mem_domain_init(&app0_domain, 0, NULL);

向内存域添加内存分区
--------------------

向内存域添加内存分区有两种方式。

第一个代码示例展示如何在创建内存域时添加内存分区。

.. code-block:: c

    /* the start address of the MPU region needs to align with its size */
    uint8_t __aligned(32) app0_buf[32];
    uint8_t __aligned(32) app1_buf[32];

    K_MEM_PARTITION_DEFINE(app0_part0, app0_buf, sizeof(app0_buf),
                           K_MEM_PARTITION_P_RW_U_RW);

    K_MEM_PARTITION_DEFINE(app0_part1, app1_buf, sizeof(app1_buf),
                           K_MEM_PARTITION_P_RW_U_RO);

    struct k_mem_partition *app0_parts[] = {
        app0_part0,
        app0_part1
    };

    k_mem_domain_init(&app0_domain, ARRAY_SIZE(app0_parts), app0_parts);

第二个代码示例展示如何将内存分区逐个添加到已初始化的内存域中。

.. code-block:: c

    /* the start address of the MPU region needs to align with its size */
    uint8_t __aligned(32) app0_buf[32];
    uint8_t __aligned(32) app1_buf[32];

    K_MEM_PARTITION_DEFINE(app0_part0, app0_buf, sizeof(app0_buf),
                           K_MEM_PARTITION_P_RW_U_RW);

    K_MEM_PARTITION_DEFINE(app0_part1, app1_buf, sizeof(app1_buf),
                           K_MEM_PARTITION_P_RW_U_RO);

    k_mem_domain_add_partition(&app0_domain, &app0_part0);
    k_mem_domain_add_partition(&app0_domain, &app0_part1);

.. note::
    内存分区的最大数量受 MPU 区域或 MMU 表的最大数量限制。

内存域分配
----------

任意线程都可以加入内存域，任意内存域也可以分配给多个线程。通过 API 调用将线程分配到内存域：

.. code-block:: c

    k_mem_domain_add_thread(&app0_domain, app_thread_id);

如果线程已属于其他域（包括默认域），则会将其从原域中移除并加入新域。

此外，如果线程属于某个内存域，它创建的子线程也会属于该域。

从内存域移除内存分区
--------------------

以下代码展示如何从内存域移除内存分区。

.. code-block:: c

    k_mem_domain_remove_partition(&app0_domain, &app0_part1);

k_mem_domain_remove_partition() API 查找与给定参数匹配的内存分区，并将其从内存域中移除。

可用分区属性
------------

定义分区时，需要为分区设置访问权限属性。由于内存分区的访问控制依赖 MPU 或 MMU，可用分区属性取决于架构。

某个架构的完整可用分区属性列表位于其专用头文件 ``include/zephyr/arch/<arch name>/arch.h`` 中（例如 :zephyr_file:`include/zephyr/arch/arm/arch.h`）。以下是一些分区属性示例：

.. code-block:: c

    /* Denote partition is privileged read/write, unprivileged read/write */
    K_MEM_PARTITION_P_RW_U_RW
    /* Denote partition is privileged read/write, unprivileged read-only */
    K_MEM_PARTITION_P_RW_U_RO

几乎所有情况下，``K_MEM_PARTITION_P_RW_U_RW`` 都是正确选择。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_MAX_DOMAIN_PARTITIONS`

API 参考
********

以下内存域 API 由 :zephyr_file:`include/zephyr/kernel.h` 提供：

.. doxygengroup:: mem_domain_apis
