.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _interrupts_v2:

中断
####

:dfn:`中断服务程序` （ISR）是响应硬件或软件中断而异步执行的函数。ISR 通常会抢占当前线程，从而以很低的延迟响应。只有所有 ISR 工作完成后，线程才恢复执行。

.. contents::
    :local:
    :depth: 2

概念
****

在底层硬件约束允许的范围内，可以定义任意数量的 ISR，仅受可用 RAM 限制。

ISR 具有以下主要属性：

* 触发 ISR 的 **中断请求（IRQ）信号**。
* 与 IRQ 关联的 **优先级**。
* 被调用以处理中断的 **中断服务程序**。
* 传给该函数的 **参数值**。

:abbr:`IDT (Interrupt Descriptor Table)` 或向量表用于将给定中断源关联到相应 ISR。同一时刻，一个特定 IRQ 只能关联一个 ISR。

多个 ISR 可以使用同一个函数处理中断，使单个函数既能服务于产生多种中断的设备，也能服务于多个设备，通常是同类设备。传给 ISR 函数的参数值可供函数判断当前触发了哪个中断。

内核为所有未使用的 IDT 表项提供默认 ISR。如果触发了意外中断，该 ISR 会产生致命系统错误。

内核支持 **中断嵌套**。如果触发了更高优先级的中断，正在执行的 ISR 可以被抢占。高优先级 ISR 处理完毕后，低优先级 ISR 恢复执行。

ISR 在内核的 **中断上下文** 中执行。该上下文有专用栈区域，在某些架构上则有多个栈区域。如果启用中断嵌套支持，中断上下文的栈必须足以容纳多个并发 ISR 的执行。

.. important::
    许多内核 API 只能由线程使用，ISR 不能使用。如果某个函数可能同时由线程和 ISR 调用，可以通过内核提供的 :c:func:`k_is_in_isr` API 判断当前执行上下文，从而调整行为。

.. _multi_level_interrupts:

多级中断处理
============

硬件平台可以使用一个或多个嵌套中断控制器，支持超过原生数量的中断线。多个硬件中断源会汇聚为一条中断线，再路由到上级控制器。

支持嵌套中断控制器时，应启用 :kconfig:option:`CONFIG_MULTI_LEVEL_INTERRUPTS`，并根据硬件架构配置 :kconfig:option:`CONFIG_2ND_LEVEL_INTERRUPTS` 和 :kconfig:option:`CONFIG_3RD_LEVEL_INTERRUPTS`。

每个中断会分配一个唯一的 32 位编号，其中嵌入了选择和调用正确中断服务程序（ISR）所需的信息。每一级占用该编号中的一个字节，因此这种结构最多支持四级中断，如下图及后续说明所示：

.. code-block:: none

              9                           2       0
    ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
    │   │   │ ╷ │   │   │   │   │ A │   │ ╷ │   │   │               (LEVEL 1)
    └───┴───┴─│─┴───┴───┴───┴───┴───┴───┴─│─┴───┴───┘
              └─────────────────┐         └─────────────────────┐
          5                     v                               v
    ┌───┬───┬───┬───┬───┬───┬───┐   ┌───┬───┬───┬───┬───┬───┬───┐
    │   │ ╷ │   │ C │   │   │   │   │   │   │   │   │ B │   │   │   (LEVEL 2)
    └───┴─│─┴───┴───┴───┴───┴───┘   └───┴───┴───┴───┴───┴───┴───┘
          └─────────────────────┐
                                v
    ┌───┬───┬───┬───┬───┬───┬───┐
    │   │   │   │   │ D │   │   │                                   (LEVEL 3)
    └───┴───┴───┴───┴───┴───┴───┘

图中展示了三级中断。

* 每个单元格代表一条中断线，从最右侧的 0 开始编号。
* LEVEL 1 有 12 条中断线，其中两条（2 和 9）连接到嵌套控制器，设备“A”连接到第 4 条线。
* 其中一个 LEVEL 2 控制器的第 5 条中断线连接到 LEVEL 3 嵌套控制器，设备“C”连接到第 3 条线。
* 另一个 LEVEL 2 控制器没有嵌套控制器，设备“B”连接到第 2 条线。
* LEVEL 3 控制器的第 2 条线连接设备“D”。

下面说明如何为每个硬件中断生成唯一编号。以上图中的 A、B、C、D 四个中断为例：

.. code-block:: none

   A -> 0x00000004
   B -> 0x00000302
   C -> 0x00000409
   D -> 0x00030609

.. note::
   从 LEVEL 2 开始，各级编码值都需加 1，因为 0 表示该级不存在中断编号。在本例中，设备 D 位于 LEVEL 3 控制器的第 2 条线，该控制器连接到 LEVEL 2 的第 5 条线，后者又连接到 LEVEL 1 的第 9 条线，即 2 -> 5 -> 9。考虑 LEVEL 2 及更深层级的编码偏移后，设备 D 的编号为 0x00030609。

防止中断
========

某些情况下，当前线程执行对时间敏感的操作或临界区操作时，可能需要阻止 ISR 执行。

线程可以使用 **IRQ 锁** 临时阻止系统处理所有 IRQ。该锁允许重复锁定，因此函数无需知道它此前是否已经生效。线程必须执行与加锁次数相同的解锁操作，内核才能在线程运行期间重新处理中断。

.. important::
    线程持有 IRQ 锁时不允许 :ref:`睡眠 <thread_sleeping>`，只能调用 :ref:`isr-ok <api_term_isr-ok>` 函数。

线程也可以临时 **禁用** 指定 IRQ，使其触发时不执行关联的 ISR。之后必须重新 **启用** IRQ，才能允许 ISR 执行。

.. important::
    禁用 IRQ 会阻止关联 ISR 抢占系统中的 *所有* 线程，而不仅仅是禁用它的那个线程。

.. _zlis:

零延迟中断
----------

通过 IRQ 锁阻止中断可能增加实际观察到的中断延迟，而某些低延迟场景无法接受较高的中断延迟。

为满足这类需求，内核允许对延迟有严格限制的中断在不受中断锁屏蔽的优先级上执行，这类中断称为 *零延迟中断*。使用该功能需启用 :kconfig:option:`CONFIG_ZERO_LATENCY_IRQS`。由于普通 ISR 会与内核交互，配置为零延迟的中断还必须声明为 :ref:`直接 ISR <direct_isrs>`，且其中不得使用 :c:macro:`ISR_DIRECT_PM`。此外，必须向 :c:macro:`IRQ_DIRECT_CONNECT` 传入 :c:macro:`IRQ_ZERO_LATENCY` 标志，将相应中断配置为零延迟。某些架构允许将零延迟 ISR 同时声明为直接中断和动态中断，详见 :ref:`direct_isrs`。

零延迟中断用于直接处理硬件事件，不应与内核代码交互。应将其中调用任何内核 API 的行为视为未定义行为：如果应用在零延迟中断上下文中使用这些 API，就有责任直接验证其行为是否正确。零延迟中断不得修改普通 Zephyr 上下文所调用内核 API 会访问的数据，也不得产生需要同步处理的异常，例如内核 panic。

系统电源管理在 PM 恢复期间持续锁定中断时，零延迟中断不受这种锁定恢复顺序约束，可能在 PM 挂起或恢复逻辑执行期间、PM 恢复管理工作和 SoC／设备硬件恢复完成之前被分派。这类 ISR 必须能够在电源唤醒过程中安全执行；否则，在系统状态不允许其执行时，必须屏蔽或禁用中断源。当可能产生零延迟中断的设备路径处于活动状态时，如何避免电源策略选中不安全状态，可参阅 :ref:`设备电源策略约束 <pm-device-constraint>`。

.. important::
    零延迟中断的支持取决于架构。目前该功能已在 ARM Cortex-M 架构变体中实现。

.. tip::
    为降低闪存访问延迟，可以考虑将 ISR 及其所有相关符号重定位到 RAM。

将 ISR 工作转交线程
===================

ISR 应尽快执行完毕，以确保系统行为可预测。如果需要耗时的处理，ISR 应将部分或全部工作转交线程，从而恢复内核响应其他中断的能力。

内核支持多种机制，可将与中断相关的处理转交线程。

* ISR 可以使用 FIFO、LIFO 或信号量等内核对象，通知辅助线程执行与中断相关的处理。

* ISR 可以通知系统工作队列线程执行一个工作项，见 :ref:`workqueues_v2`。

ISR 将工作转交线程后，通常在 ISR 完成时只需一次上下文切换即可进入该线程，让中断相关处理几乎立即继续。不过，具体取决于承接线程的优先级，当前执行的协作式线程或其他更高优先级线程可能会先执行，然后才调度承接工作的线程。

共享中断线
==========

在某些硬件平台上，不同 IP 模块可能使用同一条中断线。例如，中断 17 既可能由 DMA 控制器用于通知数据传输完成，也可能由 DAI 控制器用于通知传输 FIFO 已达到水位线。要支持这种情况，往往需要特殊逻辑或变通方案，例如使用 shared_irq 中断控制器，但这些方式的扩展性不佳。

可以通过 :kconfig:option:`CONFIG_SHARED_INTERRUPTS` 启用共享中断来解决此问题。每当使用 :c:macro:`IRQ_CONNECT` 或 :c:func:`irq_connect_dynamic` 尝试在同一条中断线上注册第二组 ISR／参数时，该中断线就会变为共享状态。此后每次触发中断，都会调用原有和新注册的两组 ISR／参数。共享中断上下文中使用某条中断线的实体称为客户端，每个中断允许的客户端最大数量由 :kconfig:option:`CONFIG_SHARED_IRQ_MAX_NUM_CLIENTS` 控制。

中断共享对用户透明。用户仍可像平常一样通过 :c:macro:`IRQ_CONNECT` 和 :c:func:`irq_connect_dynamic` 注册中断，共享机制会在内部自动处理。

同时启用共享中断与动态中断支持后，用户可以通过 :c:func:`irq_disconnect_dynamic` 动态解除 ISR 关联。解除后，原注册中断线再次触发时，该 ISR 将不再被调用。

注意，启用 :kconfig:option:`CONFIG_SHARED_INTERRUPTS` 会使二进制大小明显增加，应谨慎使用。

实现
****

定义普通 ISR
============

在运行时调用 :c:macro:`IRQ_CONNECT` 定义 ISR，然后必须调用 :c:func:`irq_enable` 将其启用。

.. note::
    :c:func:`irq_enable`、:c:func:`irq_lock` 等无前缀的中断控制 API 是旧名称。新代码应使用带命名空间前缀的对应名称，例如 :c:func:`k_irq_enable`、:c:func:`k_irq_lock` 等。无前缀名称仍受到完整支持。

.. important::
    IRQ_CONNECT() 不是 C 函数，其内部使用了内联汇编技巧。它的所有参数都必须在构建时已知。具有多个实例的驱动程序可能需要为每个实例定义配置函数，以配置各自的中断。

以下代码定义并启用一个 ISR。

.. code-block:: c

    #define MY_DEV_IRQ  24       /* device uses IRQ 24 */
    #define MY_DEV_PRIO  2       /* device uses interrupt priority 2 */
    /* argument passed to my_isr(), in this case a pointer to the device */
    #define MY_ISR_ARG  DEVICE_GET(my_device)
    #define MY_IRQ_FLAGS 0       /* IRQ flags */

    void my_isr(void *arg)
    {
       ... /* ISR code */
    }

    void my_isr_installer(void)
    {
       ...
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_PRIO, my_isr, MY_ISR_ARG, MY_IRQ_FLAGS);
       irq_enable(MY_DEV_IRQ);
       ...
    }

:c:macro:`IRQ_CONNECT` 要求所有参数在构建时已知，某些场景可能无法满足。也可以通过 :c:func:`irq_connect_dynamic` 在运行时安装中断，其用法与 :c:macro:`IRQ_CONNECT` 完全相同：

.. code-block:: c

    void my_isr_installer(void)
    {
       ...
       irq_connect_dynamic(MY_DEV_IRQ, MY_DEV_PRIO, my_isr, MY_ISR_ARG,
                           MY_IRQ_FLAGS);
       irq_enable(MY_DEV_IRQ);
       ...
    }

动态中断要求启用 :kconfig:option:`CONFIG_DYNAMIC_INTERRUPTS`。目前不支持移除或重新配置动态中断。

.. _direct_isrs:

定义直接 ISR
============

普通 Zephyr 中断会引入一定开销，某些低延迟场景可能无法接受。具体包括：

* 获取 ISR 参数并将其传给 ISR

* 如果启用了电源管理且系统此前处于空闲状态，执行 ISR 之前必须先将所有硬件从低功耗状态恢复，这可能十分耗时

* 某些架构由硬件完成中断栈切换，其他架构则需要通过代码切换

* 中断处理完成后，操作系统还会执行一些逻辑，可能据此作出调度决定

* :ref:`zlis` 必须始终声明为直接 ISR，因为普通 ISR 会与内核交互

Zephyr 支持所谓的“直接”中断，通过 :c:macro:`IRQ_DIRECT_CONNECT` 安装，并使用 :c:macro:`ISR_DIRECT_DECLARE` 声明处理程序。这类中断有特殊的实现要求，功能也有所精简；详见 :c:macro:`IRQ_DIRECT_CONNECT` 和 :c:macro:`ISR_DIRECT_DECLARE` 的定义。

只有选择了 :kconfig:option:`CONFIG_ARCH_HAS_DIRECT_INTERRUPTS` 的架构才支持直接中断。在其他架构上使用 :c:macro:`IRQ_DIRECT_CONNECT` 或 :c:macro:`ISR_DIRECT_DECLARE` 会导致构建失败。

以下代码演示直接 ISR：

.. code-block:: c

    #define MY_DEV_IRQ  24       /* device uses IRQ 24 */
    #define MY_DEV_PRIO  2       /* device uses interrupt priority 2 */
    #define MY_IRQ_FLAGS 0       /* IRQ flags */

    ISR_DIRECT_DECLARE(my_isr)
    {
       do_stuff();
       /* PM done after servicing interrupt for best latency. This cannot be
       used for zero-latency IRQs because it accesses kernel data. */
       ISR_DIRECT_PM();
       /* Ask the kernel to check if scheduling decision should be made. If the
       ISR is for a zero-latency IRQ then the return value must always be 0. */
       return 1;
    }

    void my_isr_installer(void)
    {
       ...
       IRQ_DIRECT_CONNECT(MY_DEV_IRQ, MY_DEV_PRIO, my_isr, MY_IRQ_FLAGS);
       irq_enable(MY_DEV_IRQ);
       ...
    }

动态直接中断的安装支持取决于架构。目前 Arm Cortex-M 架构变体通过 :c:macro:`ARM_IRQ_DIRECT_DYNAMIC_CONNECT` 宏实现此功能，可用它声明同时为直接和动态的中断。

在 RAM 中执行 ISR
=================

为实现极低延迟，可以将 ISR 和向量表重定位到 RAM，以消除闪存访问延迟。启用 :kconfig:option:`CONFIG_SRAM_VECTOR_TABLE` 和 :kconfig:option:`CONFIG_SRAM_SW_ISR_TABLE` 可将向量表放入 RAM，再利用 Zephyr 的 :ref:`代码与数据重定位 <code_data_relocation>` 功能，将 ISR 代码及所有相关符号也重定位到 RAM。

共享一条中断线
==============

以下代码定义两个使用相同中断号的 ISR。

.. code-block:: c

    #define MY_DEV_IRQ 24               /* device uses INTID 24 */
    #define MY_DEV_IRQ_PRIO 2           /* device uses interrupt priority 2 */
    /*  this argument may be anything */
    #define MY_FST_ISR_ARG INT_TO_POINTER(1)
    /*  this argument may be anything */
    #define MY_SND_ISR_ARG INT_TO_POINTER(2)
    #define MY_IRQ_FLAGS 0              /* IRQ flags */

    void my_first_isr(void *arg)
    {
       ... /* some magic happens here */
    }

    void my_second_isr(void *arg)
    {
       ... /* even more magic happens here */
    }

    void my_isr_installer(void)
    {
       ...
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_first_isr, MY_FST_ISR_ARG, MY_IRQ_FLAGS);
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_second_isr, MY_SND_ISR_ARG, MY_IRQ_FLAGS);
       ...
    }

`定义普通 ISR`_ （定义普通 ISR）一节中介绍的 :c:macro:`IRQ_CONNECT` 限制同样适用。如果未启用 :kconfig:option:`CONFIG_SHARED_INTERRUPTS`，上述代码会产生构建错误；否则，每次触发中断 24 时，两个 ISR 都会被调用。

如果 :kconfig:option:`CONFIG_SHARED_IRQ_MAX_NUM_CLIENTS` 的值小于 2，即当前客户端数量，则会产生构建错误。

如果启用了动态中断，:c:func:`irq_connect_dynamic` 允许在运行时共享中断。超过配置允许的客户端最大数量会触发断言失败。

动态解除 ISR 关联
=================

以下代码定义两个使用相同中断号的 ISR，并在运行时解除第二个 ISR 的关联。

.. code-block:: c

    #define MY_DEV_IRQ 24               /* device uses INTID 24 */
    #define MY_DEV_IRQ_PRIO 2           /* device uses interrupt priority 2 */
    /*  this argument may be anything */
    #define MY_FST_ISR_ARG INT_TO_POINTER(1)
    /*  this argument may be anything */
    #define MY_SND_ISR_ARG INT_TO_POINTER(2)
    #define MY_IRQ_FLAGS 0              /* IRQ flags */

    void my_first_isr(void *arg)
    {
       ... /* some magic happens here */
    }

    void my_second_isr(void *arg)
    {
       ... /* even more magic happens here */
    }

    void my_isr_installer(void)
    {
       ...
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_first_isr, MY_FST_ISR_ARG, MY_IRQ_FLAGS);
       IRQ_CONNECT(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_second_isr, MY_SND_ISR_ARG, MY_IRQ_FLAGS);
       ...
    }

    void my_isr_uninstaller(void)
    {
       ...
       irq_disconnect_dynamic(MY_DEV_IRQ, MY_DEV_IRQ_PRIO, my_first_isr, MY_FST_ISR_ARG, MY_IRQ_FLAGS);
       ...
    }

调用 :c:func:`irq_disconnect_dynamic` 会使中断 24 不再共享，系统行为将如同从未执行第一次 :c:macro:`IRQ_CONNECT` 调用。这仅在启用 :kconfig:option:`CONFIG_DYNAMIC_INTERRUPTS` 时才允许，否则会产生链接错误。

实现细节
========

中断表在构建时通过专用工具建立。这里介绍的细节适用于除 x86 以外的所有架构；x86 的情况见下文的 `x86 细节`_ （x86 细节）一节。

调用 :c:macro:`IRQ_CONNECT` 会声明一个 struct _isr_list 实例，并将其放入特殊的 .intList 段。该段只存在于预编译阶段的编译产物中，供 Zephyr 脚本生成中断表使用，最终构建产物会将它移除。脚本实现了不同的解析器，用于处理 .intList 段的数据并生成所需输出。

默认解析器生成 C 数组，其中的参数和中断处理程序以直接从 .intList 表项取得的地址表示。除了上述例外，它适用于所有架构和编译器。其限制在于：数组生成后，代码不能再重定位，否则中断数组中的表项可能不再指向预期函数。因此，该解析器虽然兼容性更强，却限制了链接时优化的使用。

本地 ISR 声明解析器使用另一种方式，在二进制层面构建相同的数组。所有数组表项都直接在使用 :c:macro:`IRQ_CONNECT` 的文件中就地声明和定义，并放入名称唯一、自动生成的段。该段名随后被写入 .intList 段，用于生成链接器脚本片段，将表项放到正确地址。该解析器目前仅适用于受支持的架构和工具链，但能为链接器保留对象关系信息，从而支持链接时优化。

使用 C 数组的实现
-----------------

这是 Zephyr 所有受支持架构都可用的默认配置。

每次调用 :c:macro:`IRQ_CONNECT` 都会声明一个 struct _isr_list 实例，并将其放入特殊的 .intList 段：

.. code-block:: c

    struct _isr_list {
        /** IRQ line number */
        int32_t irq;
        /** Flags for this IRQ, see ISR_FLAG_* definitions */
        int32_t flags;
        /** ISR to call */
        void *func;
        /** Parameter for non-direct IRQs */
        void *param;
    };

Zephyr 分两个阶段构建。第一阶段生成 ``${ZEPHYR_PREBUILT_EXECUTABLE}``.elf，其中包含 .intList 段的所有表项，并在它们之前放置一个头部：

.. code-block:: c

    struct {
        void *spurious_irq_handler;
        void *sw_irq_handler;
        uint32_t num_isrs;
        uint32_t num_vectors;
        struct _isr_list isrs[];  <- of size num_isrs
    };

gen_isr_tables.py 脚本随后读取 ``${ZEPHYR_PREBUILT_EXECUTABLE}``.elf 中的头部和 struct _isr_list 实例，生成定义向量表和软件 ISR 表的 C 文件。这些表再被编译并链接到最终应用中。

中断优先级不编码在这些表中。:c:macro:`IRQ_CONNECT` 还包含运行时部分，将所需中断优先级写入中断控制器。某些架构不支持中断优先级，此时会忽略优先级参数。

向量表
~~~~~~
启用 :kconfig:option:`CONFIG_GEN_IRQ_VECTOR_TABLE` 时，会生成向量表。CPU 原生使用这一数据结构，它是一个函数指针数组，第 n 个元素对应第 n 条 IRQ 线的处理程序。函数指针按以下方式填入：

#. 对于通过 :c:macro:`IRQ_DIRECT_CONNECT` 声明的直接中断，此处存放处理函数。
#. 对于通过 :c:macro:`IRQ_CONNECT` 声明的普通中断，此处存放通用软件 IRQ 处理程序的地址。该代码执行内核通用中断管理操作，并从软件 ISR 表中查找 ISR 及其参数。
#. 对于完全未配置的中断线，此处存放伪中断处理程序的地址。执行该处理程序会导致致命系统错误。

某些架构为所有中断使用同一个入口，不支持向量表，此时应禁用 :kconfig:option:`CONFIG_GEN_IRQ_VECTOR_TABLE`。

某些架构会为系统异常保留开头的若干向量，并在其他位置的表中声明它们。此时需要设置 CONFIG_GEN_IRQ_START_VECTOR，为表内索引提供正确偏移。

软件 ISR 表
~~~~~~~~~~~
这是一个 struct _isr_table_entry 数组：

.. code-block:: c

    struct _isr_table_entry {
        void *arg;
        void (*isr)(void *);
    };

通用软件 IRQ 处理程序通过此表查找 ISR 及其参数，然后执行 ISR。当前 IRQ 线从中断控制器寄存器中读取，并用作该表的索引。

共享软件 ISR 表
~~~~~~~~~~~~~~~

这是一个 struct z_shared_isr_table_entry 数组：

.. code-block:: c

    struct z_shared_isr_table_entry {
        struct _isr_table_entry clients[CONFIG_SHARED_IRQ_MAX_NUM_CLIENTS];
        size_t client_num;
    };

该表跟踪每条中断线已注册的客户端。中断线变为共享状态时，:c:func:`z_shared_isr` 会替换 _sw_isr_table 中当前注册的 ISR。这个特殊 ISR 遍历已注册客户端列表，并调用各自的 ISR。

使用链接器脚本的实现
--------------------

这种通过准备和解析 .isrList 段来实现中断向量数组的方式称为本地 ISR 声明。名称源于：组成中断向量数组的所有表项都在调用 :c:macro:`IRQ_CONNECT` 宏的位置就地创建，再由自动生成的链接器脚本将其放到正确的内存位置。

选择 :kconfig:option:`CONFIG_ISR_TABLES_LOCAL_DECLARATION` 可启用此功能。如果所用架构和工具链支持该配置，会设置 :kconfig:option:`CONFIG_ISR_TABLES_LOCAL_DECLARATION_SUPPORTED`。当前支持哪些配置，详见该选项的说明。

每次调用 :c:macro:`IRQ_CONNECT` 或 :c:macro:`IRQ_DIRECT_CONNECT` 都会声明一个 ``struct _isr_list_sname`` 实例，并将其放入特殊的 .intList 段：

.. code-block:: c

    struct _isr_list_sname {
        /** IRQ line number */
        int32_t irq;
        /** Flags for this IRQ, see ISR_FLAG_* definitions */
        int32_t flags;
        /** The section name */
        const char sname[];
    };

注意，段名存储在柔性数组成员中，因此初始化后结构体的大小会随名称长度而变化。应用构建期间，脚本会使用整个表项，其中包含正确放置中断所需的全部信息。

除了 _isr_list_sname，:c:macro:`IRQ_CONNECT` 宏还会生成一个中断数组表项：

.. code-block:: c

    struct _isr_table_entry {
        const void *arg;
        void (*isr)(const void *);
    };

该数组放入指定段中，段名保存在 _isr_list_sname 结构体内。

:c:macro:`IRQ_DIRECT_CONNECT` 宏生成的内容取决于架构。它可以是指向中断处理程序的变量：

.. code-block:: c

    static uintptr_t <unique name> = ((uintptr_t)func);

也可以是一个执行跳转至中断处理程序的裸函数：

.. code-block:: c

    static void <unique name>(void)
    {
        __asm(ARCH_IRQ_VECTOR_JUMP_CODE(func));
    }

与 :c:macro:`IRQ_CONNECT` 类似，所创建的变量或函数会放入一个段中，其段信息保存在 _isr_list_sname 中。

脚本生成的文件
~~~~~~~~~~~~~~

中断表生成脚本创建三个文件：:file:`isr_tables.c`、:file:`isr_tables_swi.ld` 和 :file:`isr_tables_vt.ld`。

:file:`isr_tables.c` 包含普通中断、直接中断和共享中断（若启用）所需的结构。它只实现应用尚未实现的结构，对于未在此处实现的中断，会用注释指明其所在位置。

随后使用两个链接器文件。:file:`isr_tables_vt.ld` 被包含在所选架构要求放置中断向量的位置；:file:`isr_tables_swi.ld` 描述软件中断表元素的布局。由于软件中断表可能根据当前配置放在可写或不可写的段中，因此需要单独的文件。

x86 细节
--------

x86 架构有一种称为中断描述符表（IDT）的特殊向量表，其布局必须符合 x86 处理器文档的要求。它本质上仍是向量表，:ref:`gen_idt.py` 工具通过 .intList 段创建该表。不过，在基于 APIC 的系统上，向量表索引并不对应 IRQ 线。前 32 个向量保留给 CPU 异常，其余向量直到索引 255，按每组 16 个对应不同优先级。因此，优先级 0 的中断位于向量 32—47，优先级 1 位于 48—63，依此类推。:ref:`gen_idt.py` 构建 IDT 并配置某个中断时，会在请求优先级对应的范围内寻找空闲向量，并在那里设置处理程序。

在 x86 上，CPU 执行中断或异常向量时，没有万无一失的方法确定触发了哪个向量，因此不使用按 IRQ 线索引的软件 ISR 表。相反，:c:macro:`IRQ_CONNECT` 会创建一个小型汇编函数，以 ISR 及其参数为参数，调用 :c:func:`_interrupt_enter` 中的通用中断代码。IDT 中放置的是该汇编中断桩的地址。对于通过 :c:macro:`IRQ_DIRECT_CONNECT` 声明的中断，则将无参数 ISR 直接放入 IDT。

在向量表位置对应中断优先级的系统上，中断控制器需要在运行时知道某条 IRQ 线关联哪个向量。:ref:`gen_idt.py` 还会创建 _irq_to_interrupt_vector 数组，将 IRQ 线映射到它在 IDT 中配置的向量。运行时，:c:macro:`IRQ_CONNECT` 使用该数组向中断控制器写入 IRQ 与向量的关联。

对于动态中断，构建过程必须生成一些 4 字节的动态中断桩，每个使用中的动态中断对应一个。桩数量由 :kconfig:option:`CONFIG_X86_DYNAMIC_IRQ_STUBS` 控制。每个桩会压入一个唯一标识符，再利用该标识符，从动态中断关联时填充的表中获取相应处理函数和参数。

超出默认支持的中断数量
----------------------

生成多级中断配置时，默认每级使用 8 位掩码，以确定给定中断编码所属的层级。对于单个汇聚器支持超过 255 个中断的 CPU，这可能成为限制。此时可以覆盖默认值，为每级使用自定义位数。无论如何分配，各级总位数必须小于或等于 32，能够放入单个 32 位整数。要修改各级位数，可分别设置第一级的 :kconfig:option:`CONFIG_1ST_LEVEL_INTERRUPT_BITS`、第二级的 :kconfig:option:`CONFIG_2ND_LEVEL_INTERRUPT_BITS` 和第三级的 :kconfig:option:`CONFIG_3RD_LEVEL_INTERRUPT_BITS`，覆盖 :file:`Kconfig.multilevel` 中默认的 8。这些掩码决定生成中断值、检查中断层级以及在层级之间转换时所用的掩码长度和移位量。相关逻辑见 :file:`irq_multilevel.h`。

使用建议
********

需要快速响应，且能够在不阻塞的情况下迅速完成的中断处理，可使用普通 ISR 或直接 ISR。

.. note::
    耗时或涉及阻塞的中断处理应转交线程。应用可以采用的各种方式见 `将 ISR 工作转交线程`_ （将 ISR 工作转交线程）。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_ISR_STACK_SIZE`

此外，还有针对具体架构和设备的配置选项。

API 参考
********

.. doxygengroup:: isr_apis
