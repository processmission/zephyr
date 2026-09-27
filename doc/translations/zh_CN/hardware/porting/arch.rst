.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _architecture_porting_guide:

架构移植指南
############

要使 Zephyr 能够在当前尚不支持的 :abbr:`ISA (instruction set architecture)` 或 :abbr:`ABI (Application Binary Interface)` 上运行，需要进行架构移植。

以下是 Zephyr 支持的 ISA 和 ABI 的示例：

* 采用 System V ABI 的 x86_32 ISA
* 采用 Thumb2 指令集和 ARM 嵌入式 ABI (aeabi) 的 ARMv7-M ISA
* ARCv2 ISA

有关 Kconfig 配置的信息，请参阅 :ref:`setting_configuration_values` 。架构采用与开发板类似的 Kconfig 配置方案。

架构移植可分为几个部分；其中大多数是必需的，部分是可选的：

* **早期启动序列** ：CPU 退出复位状态时，各架构必须执行的步骤有所不同（必需）。

* **中断和异常处理** ：各架构以特定方式处理异步事件和非主动请求的事件（必需）。

* **线程上下文切换** ：Zephyr 的上下文切换依赖于 ABI，且各 ISA 需要保存的寄存器集合不同（必需）。

* **线程创建和终止** ：线程的初始栈帧依赖于 ABI 和架构，线程中止也可能如此（必需）。

* **设备驱动程序** ：系统时钟定时器和中断控制器通常与架构相关（部分必需，部分可选）。

* **实用程序库** ：出于性能考虑，一些通用内核 API 依赖于架构特定的实现（必需）。

* **CPU 空闲与电源管理** ：大多数架构都实现了使 CPU 进入睡眠状态的指令（部分可选，但通常非常需要）。

* **故障管理** ：用于实现架构特定的调试辅助功能，以及处理线程中的致命错误（部分可选）。

* **链接器脚本和工具链** ：构建系统和映像链接过程通常需要处理架构特定的细节（必需）。

* **内存管理和内存映射** ：用于处理支持内存管理和内存映射所涉及的架构特定细节。

* **栈对象** ：用于处理内存保护硬件在栈对象方面的架构特定细节。

* **用户模式线程** ：用于支持在用户模式下运行的线程。

* **GDB Stub** ：用于支持 GDB stub，以实现远程调试。

早期启动序列
************

早期启动序列的目标是将系统从复位后的状态转换到能够运行 C 代码的状态，从而执行通用内核初始化序列。大多数情况下，只需执行很少的步骤，但某些架构需要完成更多工作。

所有架构的通用步骤：

* 设置初始栈。
* 如果运行的是 :abbr:`XIP (eXecute-In-Place)` 内核，则将已初始化的数据从 ROM 复制到 RAM。
* 如果未使用 ELF 加载器，则将 BSS 段清零。
* 跳转到 :code:`z_cstart()` ，执行早期内核初始化

  * :code:`z_cstart()` 负责执行上下文切换，从启动时运行的伪上下文切换到主线程。

以下是必须执行的架构特定步骤的一些示例：

* 如果在 x86_32 上获得控制权时处于实模式，则切换到 32 位保护模式。
* 在 x86_32 上设置段寄存器，以处理引导加载程序将这些寄存器留在未知或错误状态的情况。
* 在 Cortex-M3/4 上初始化开发板特定的看门狗。
* 在 Cortex-M 上将栈从 MSP 切换到 PSP。
* 在 Cortex-M 上采用调用 z_swap() 以外的方法，以避免竞态条件。
* 在 ARCv2 上设置 FIRQ 和常规 IRQ 处理。

早期启动序列钩子
================

Zephyr 提供了多个钩子（在 :zephyr_file:`include/zephyr/platform/hooks.h` 中有说明），允许在启动过程的特定时刻执行 SoC 或开发板特定的代码。

内核负责从架构无关的代码中调用大多数钩子。不过，某些钩子必须在早期启动序列中调用；由于该序列由架构特定的代码实现，因此也必须在这些代码中调用钩子。下面简要介绍早期启动序列，以及架构特定的代码应在何时调用钩子：

#. 执行从架构特定的入口点开始，其名称与 :kconfig:option:`CONFIG_KERNEL_ENTRY` 匹配。

#. 立即重新初始化架构特定的状态（如果启用了 :kconfig:option:`CONFIG_INIT_ARCH_HW_AT_BOOT` ）。

#. 调用 :c:func:`soc_early_reset_hook` 。

   .. note::
    调用此钩子前不必设置有效的栈。不过，允许该钩子在返回前覆盖栈指针。架构特定的代码不得假定栈指针寄存器的值在调用 :c:func:`soc_early_reset_hook` 前后保持不变。

    在具有多个栈指针的架构上，通常有一个可以直接访问的 *“主”* 栈指针，以及一个或多个 *“次”* 栈指针寄存器。:c:func:`soc_early_reset_hook` 的实现可以覆盖 *“主”* 栈指针，但 **不得** 读取或修改任何 *“次”* 栈指针的值。（这样，架构特定的代码就可以在调用 :c:func:`soc_early_reset_hook` 之前，按需设置任意 *“次”* 栈指针。）

    例如，ARM Cortex-A 架构定义了多种执行模式，每种模式都有自己的栈指针寄存器 :samp:`sp_{mode}` 。当处理器在 :samp:`{X}` 模式下执行时，涉及通用寄存器 ``sp`` 的操作实际作用于 :samp:`sp_{X}` 。在此架构上，假设调用 :c:func:`soc_early_reset_hook` 时处理器正在 :samp:`{M}` 模式下执行，则允许该钩子覆盖 :samp:`sp_{M}` （可通过 ``sp`` 访问），但 **不得** 读取或覆盖任何其他 :samp:`sp_{mode}` （其中 :samp:`{mode} != {M}` ）。

    :c:func:`soc_early_reset_hook` 的实现可以不将执行控制权交还给架构特定的代码，在这种情况下，它会“接管”系统。此类钩子不受上述规则约束，可以读取或覆盖任意栈指针。不过，提供此类实现时，早期启动序列的其余部分显然不会执行。

#. 设置初始栈，供早期启动序列的后续步骤使用。

#. 执行架构特定的“ *从挂起到 RAM 状态恢复* ”逻辑

   .. note::
    更多细节请参阅 :kconfig:option:`CONFIG_PM_S2RAM` 和架构特定的实现，但请注意，如果此逻辑确定正在退出挂起到 RAM 状态，则不会执行早期启动序列的其余部分。

#. 调用 :c:func:`soc_reset_hook` 。

#. *在此处执行架构特定的操作（使用汇编）……*

#. 调用 :c:func:`z_prep_c` 。此架构特定的函数使用 C 实现。

#. :c:func:`z_prep_c` 立即调用 :c:func:`soc_prep_hook` 。

#. *在此处执行架构特定的操作（使用 C）……*

#. 调用 :c:func:`z_cstart` 。架构无关的代码开始执行。

中断和异常处理
**************

各架构对中断和异常处理的定义各不相同。

当设备需要通知处理器有工作需要代为完成时，就会触发中断。当线程执行了软件自身的顺序执行流程无法处理的操作时，就会触发异常。中断和异常都会将控制权交给处理程序。对于中断，该处理程序称为 :abbr:`ISR (Interrupt Service Routine)` 。处理程序完成异常或中断所需的工作。对于中断，这些工作与具体设备有关。对于异常，则取决于异常本身，但通常由内核核心本身负责提供处理程序。

除了处理程序本身执行的工作外，内核还必须完成一些工作。例如：

* 将控制权交给处理程序之前：

  * 保存当前正在执行的上下文。
  * 可能需要退出节能模式，这包括唤醒设备。
  * 如果退出无时钟节拍空闲模式，则更新内核运行时间。

* 从处理程序重新获得控制权后：

  * 决定是否执行上下文切换。
  * 执行上下文切换时，恢复即将切入的上下文。

这项工作在各架构上的概念相同，但细节完全不同：

* 需要保存和恢复的寄存器。
* 执行这项工作所需的处理器指令。
* 异常的编号。
* 等等。

因此，这需要一个架构专用的实现，称为中断/异常桩代码。

另一个问题是，内核将 ISR 的签名定义为：

.. code-block:: C

    void (*isr)(void *parameter)

各架构没有统一的方式或原生机制来处理传递给 ISR 的参数。因此，通常使用以下两种方法来处理参数。

* 使用架构定义的某种机制，在桩代码中强制设置参数值。这常见于基于 X86 的架构。

* 通过单独的表插入和跟踪 ISR 的参数，这要求架构在运行时确定当前正在执行哪个中断。实际中断向量表的所有条目都安装一个通用的中断分发处理程序，再由该程序从单独的表中获取设备的 ISR 和参数。ARC 和 ARM 架构通常通过 :kconfig:option:`CONFIG_GEN_ISR_TABLES` 的实现来使用这种方法。桩代码的示例可参见 x86 中的 ``_interrupt_enter()`` 、ARM 中的 ``_isr_wrapper()`` ，或者 :zephyr_file:`arch/arc/core/isr_wrapper.S` 中针对 ARC 的完整实现说明。

每种架构还必须实现用于中断控制的原语：

* 锁定中断： :c:macro:`irq_lock()` 、 :c:macro:`irq_unlock()` 。
* 注册中断： :c:macro:`IRQ_CONNECT()` 。
* 在支持的情况下设置优先级： :c:func:`irq_priority_set` 。
* 启用/禁用中断： :c:macro:`irq_enable()` 、 :c:macro:`irq_disable()` 。

.. note::

  :c:macro:`IRQ_CONNECT` 是一个宏，它利用汇编器和/或链接器脚本技巧在构建时连接中断，从而缩短启动时间并减小代码段大小。

向量表应为每个可能发生的中断和异常提供处理程序。处理程序可以简单到只有一个自旋循环。不过，我们强烈建议处理程序至少打印一些调试信息。当遇到除零或无效内存访问等故障异常，或意外中断（ :dfn:`spurious interrupt` ）时，这些信息有助于查明问题所在。示例可参见 :zephyr_file:`arch/arm/core/cortex_m/fault.c` 中的 ARM 实现。

线程上下文切换
**************

支持多线程是内核存在的基本目的。Zephyr 支持两种线程：抢占式线程和协作式线程。决定下一个待调度线程的规则由内核处理。不过，上下文切换本身的实现方式由架构移植代码负责。

Zephyr 提供了两个互斥的上下文切换接口。首选接口是 :code:`arch_switch` ，启用 :kconfig:option:`CONFIG_USE_SWITCH` 时会选择该接口。另一个接口是 :code:`arch_swap` ，禁用 :kconfig:option:`CONFIG_USE_SWITCH` 时会选择该接口。移植到新架构时，只需实现其中一个；但对于 SMP 平台，必须实现 :code:`arch_switch` 。

上下文切换可能发生在以下几种情况下：

* 线程执行阻塞操作时，例如获取当前不可用的信号量。

* 抢占式线程释放某个对象，使阻塞于该对象的更高优先级线程解除阻塞时。

* 中断使优先级高于当前执行线程的线程解除阻塞，且当前执行线程为抢占式线程时。

* 当线程运行至结束时。

* 当线程引发致命异常并从运行线程中移除时。例如，引用无效内存，

因此，上下文切换必须能够处理所有这些情况。

上下文切换有两种类型：协作式（ :dfn:`cooperative` ）和抢占式（ :dfn:`preemptive` ）。

* 当线程主动将控制权交给另一个线程时，就会发生 *协作式* 上下文切换。以下两种情况会发生这种切换

  * 当线程显式让出执行权时。
  * 当线程尝试获取当前不可用的对象，并愿意等待该对象变为可用时。

* 如果当前运行的线程可被抢占，当 ISR 或线程执行某项操作，使优先级高于当前线程的另一个线程被调度运行时，就会发生 *抢占式* 上下文切换。例如，释放高优先级线程正在等待的对象。

.. note::

  当协作式线程正在运行时，控制权不会被强行夺走。

协作式上下文切换始终由线程调用内核内部例程 :code:`z_swap` （或其某个变体）来完成。该例程随后会根据情况调用 :code:`arch_switch` 或 :code:`arch_swap` 。调用这些例程时，不会检查是否需要进行上下文切换——此时必须进行上下文切换。

.. note::

  在 32 位 x86 上， :code:`arch_swap` 足够通用，架构也足够灵活，因此可以在退出中断时调用它来触发上下文切换。但不应将此视为通用规则，因为 ARM Cortex-M 和 ARCv2 移植均未采用这种方式。

由于 :code:`z_swap` 执行协作式切换，ABI 规定由调用者保存的寄存器已经保存在栈上，无需再将它们保存到 k_thread 结构体中。

上下文切换也可以通过抢占方式执行。这发生在退出 ISR 时，由内核的中断退出桩代码执行：

* x86 上的 :code:`_interrupt_enter` ，在调用处理程序之后执行。
* ARM 上的 :code:`z_arm_exc_exit` 和 :code:`z_arm_int_exit` 。
* ARCv2 上的 ``_firq_exit`` 和 ``_rirq_exit`` 。

决定是否执行上下文切换的逻辑很简单，并且仅在退出非嵌套中断时执行：

启用 :kconfig:option:`CONFIG_USE_SWITCH` 时……

* 中断退出代码应调用 :c:func:`z_get_next_switch_handle` ，并返回到所返回的切换句柄标识的线程上下文

未启用 :kconfig:option:`CONFIG_USE_SWITCH` 时……

* 中断退出代码应从就绪队列中获取缓存的线程，并执行以下操作：

  * 如果缓存的线程不是当前线程，则执行上下文切换。
  * 否则，不执行上下文切换。

这虽然简单，却至关重要：如果实现不正确，内核将无法按预期工作，并会出现异常崩溃，其中大多数由栈损坏引起。

线程的创建与终止
****************

要启动新线程，必须构造一个栈帧，使上下文切换能够像弹出先前被切换出去的线程的栈帧一样将其弹出。这需要在架构特定的内部例程 :code:`_new_thread` 中实现。

线程入口点也不能直接调用，即不应将其设置为新线程的 :abbr:`PC (program counter)` 。而是必须通过 ``_thread_entry`` 进行封装。这意味着，栈帧中的 PC 应设置为 ``_thread_entry`` ，而线程入口点应作为第一个参数传递给 ``_thread_entry`` 。具体细节取决于 ABI。

是否需要架构特定的线程终止实现取决于该架构。虽然已有通用实现，但它可能不适用于某些架构。

实践中需要提供架构特定的线程终止实现的一个原因是：线程正常退出时与因异常而中止时，所需的处理可能不同。ARM Cortex-M 就是如此：如果线程触发了致命异常，就必须使 CPU 退出处理程序模式；如果线程从其入口点函数正常退出，则无需这样做。

这意味着需要实现架构特定版本的 :c:func:`k_thread_abort` ，并根据架构需要设置 Kconfig 选项 :kconfig:option:`CONFIG_ARCH_HAS_THREAD_ABORT` （例如，参见 :zephyr_file:`arch/arm/core/cortex_m/Kconfig` ）。

线程局部存储
************

要在新架构上启用线程局部存储：

#. 实现 :c:func:`arch_tls_stack_setup`，以在栈中设置 TLS 存储区。有关存储区的布局要求，请参阅工具链文档。可以使用以下辅助函数：

   * 函数 :c:func:`z_tls_data_size` 返回线程局部变量所需的大小（不包括工具链和架构所需的任何额外数据）。
   * 函数 :c:func:`z_tls_copy` 为线程局部变量准备 TLS 存储区。此函数仅复制变量本身，不处理架构和/或工具链特定的数据。

#. 在上下文切换时，获取新线程的 ``struct k_thread`` 中的 ``tls`` 字段，并将其存入适当的寄存器（或其他变量），以便访问 TLS 存储区。有关应使用哪些寄存器，请参阅工具链和架构文档。
#. 在与新架构相关的 Kconfig 中添加 ``select ARCH_HAS_THREAD_LOCAL_STORAGE``。
#. 运行 ``tests/kernel/threads/tls``，确保新代码正常工作。

设备驱动程序
************

内核运行所需的硬件设备很少。理论上，唯一必需的设备是中断控制器，因为内核可以在没有系统时钟的情况下运行。实际上，要运行基本健全性检查测试套件中的大多数乃至全部测试，还需要系统时钟。由于这两者通常与架构紧密相关，因此它们也是架构移植的一部分。

中断控制器
==========

不同架构的中断控制器和中断概念之间可能存在显著差异。

例如，x86 具有 :abbr:`IDT (Interrupt Descriptor Table)` 的概念，并支持不同的中断控制器。中断在 IDT 中的位置决定了它的优先级。

另一方面，ARM Cortex-M 将 :abbr:`NVIC (Nested Vectored Interrupt Controller)` 作为架构定义的一部分。不需要在 NVIC 向量表之外再设置类似 IDT 的表。IRQ 在表中的位置与其优先级无关：每个表项的优先级都可以通过编程设置。

ARCv2 将其中断单元作为架构定义的一部分，这与 NVIC 有些相似。不过，ARC 定义的异常编号与中断编号是一一对应的（即异常 1 对应 IRQ1，设备 IRQ 从 16 开始），而 ARM 的 IRQ0 对应异常 16（更特别的是，异常 1 可以视为 IRQ-15）。

这些差异意味着，在中断控制器方面，各架构之间几乎没有可以共享的内容。

系统时钟
========

x86 将 APIC 定时器和 HPET 作为其架构定义的一部分。ARM Cortex-M 具有 SYSTICK 异常。最后，ARCv2 具有 timer0/1 设备。

内核超时在系统时钟定时器驱动程序的中断处理程序上下文中处理。


串口控制台
==========

还有一种设备几乎是架构移植的必需品，因为它对调试非常有用。它是一个简单的、采用轮询方式且仅支持输出的串口驱动程序，用于发送控制台（ :code:`printk`、 :code:`printf` ）输出。

它并非必需，也可以使用 RAM 控制台（ :kconfig:option:`CONFIG_RAM_CONSOLE` ），将所有输出发送到可由调试器读取的环形缓冲区。

实用程序库
**********

内核依赖少量函数，在现代处理器上，这些函数可以用极少的指令或以无锁方式实现。因此，应将这些函数的实现作为架构移植的一部分。

* 原子操作。

  * 如果给定架构具有相应的指令，则使用 :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_ARCH` Kconfig 选项配置其实现。

  * 如果给定架构没有相应的指令，可以使用通用实现，在非原子操作周围调用 :c:func:`irq_lock` 或 :c:func:`irq_unlock`。使用 :kconfig:option:`CONFIG_ATOMIC_OPERATIONS_C` Kconfig 选项配置此实现。

* 查找置位的最低有效位和最高有效位。

  * 如果给定架构没有相应的指令，始终可以将这些函数实现为通用 C 函数。

可以使用编译器内建函数来实现这些功能，但务必确保使用了所需的编译器屏障。

CPU 空闲与电源管理
******************

内核通过两个函数提供 CPU 电源管理支持：:c:func:`arch_cpu_idle` 和 :c:func:`arch_cpu_atomic_idle` 。

:c:func:`arch_cpu_idle` 的实现可以很简单，只需在中断未锁定的情况下执行该架构的节能指令，例如 x86 上的 :code:`hlt` 、ARM 上的 :code:`wfi` 或 :code:`wfe` ，以及 ARC 上的 :code:`sleep` 。如果某个上下文不关心进入休眠前是否被中断打断，就可以在其中循环调用此函数。基本上，以下两种场景适合使用此函数：

* 在单线程系统的唯一线程中，且该线程在初始化后不再执行实际工作，即在应用的整个运行期间都处于不执行任何操作的循环中。

* 在空闲线程中。

另一方面，:c:func:`arch_cpu_atomic_idle` 必须能够以原子方式重新启用中断并执行节能指令。因此，它可以用于实际的应用代码中，但同样仅限于单线程系统。

通常，应由空闲线程负责让 CPU 进入空闲状态，但在某些非常特殊的场景下，应用也可以使用这些 API。

对于任何给定的架构，这两个函数都必须存在。不过，如果需要，也可以仅通过以下步骤实现：

#. 解锁中断
#. NOP

不过，强烈建议提供具有实际功能的实现。

故障管理
********

发生未处理的 CPU 异常时，架构代码必须调用 :c:func:`z_fatal_error` 。此函数会输出与架构无关的信息，并通过调用 :c:func:`k_sys_fatal_error` 来决定后续处理策略。可以覆盖后者以实现应用特定的策略，例如锁定中断并永久自旋（默认实现），甚至关闭系统电源（如果支持）。

工具链与链接
************

必须在构建系统中添加工具链支持。

需要在 :zephyr_file:`include/zephyr/toolchain/gcc.h` 中添加一些架构特定的定义。可参考该文件中现有受支持架构的相关内容。

每种架构还需要自己的链接脚本，即使其中大部分段都可以借鉴其他架构的链接脚本。某些段可能是新架构特有的，例如 ARM 上的 SCB 段和 x86 上的 IDT 段。

内存管理与内存映射
******************

如果目标平台启用了分页，并且要求驱动程序对其 I/O 区域进行内存映射，则需要启用 :kconfig:option:`CONFIG_MMU` 并实现以下 API：

- :c:func:`arch_mem_map`
- :c:func:`arch_mem_unmap`
- :c:func:`arch_page_phys_get`

栈对象
******

是否具备内存保护硬件会影响栈对象的创建方式。所有架构移植都必须指定栈指针所需的对齐方式，这由 CPU 和 ABI 的要求共同决定。该对齐要求通过架构头文件中的 :c:macro:`ARCH_STACK_PTR_ALIGN` 定义，通常是 4、8 或 16 字节这样较小的值。

线程栈有两种类型：

- 使用 :c:macro:`K_KERNEL_STACK_DEFINE()` 及相关 API 定义的“内核”栈，可供在监督模式下运行的内核线程使用，也可用作中断或异常处理的栈。这类栈的对齐要求宽松得多，预留数据也更少。它们不会为特权提升栈预留内存。

- “线程”栈通常占用更多内存，但既可供在用户模式下运行的线程使用，也适用于内核栈的所有使用场景。

如果未启用 :kconfig:option:`CONFIG_USERSPACE` ，“线程”栈与“内核”栈等价。

可以在架构层定义额外的宏，用于指定栈对象基址的对齐要求、栈对象内部不用于线程栈缓冲区的预留数据，以及为支持用户模式线程而向上取整栈大小的方式。如果没有定义这些宏，则采用以下默认值：

- :c:macro:`ARCH_KERNEL_STACK_RESERVED` ：默认不预留空间
- :c:macro:`ARCH_THREAD_STACK_RESERVED`：默认不预留空间
- :c:macro:`ARCH_KERNEL_STACK_OBJ_ALIGN`：默认按 :c:macro:`ARCH_STACK_PTR_ALIGN` 对齐
- :c:macro:`ARCH_THREAD_STACK_OBJ_ALIGN`：默认按 :c:macro:`ARCH_STACK_PTR_ALIGN` 对齐
- :c:macro:`ARCH_THREAD_STACK_SIZE_ALIGN`：默认向上取整为 :c:macro:`ARCH_STACK_PTR_ALIGN` 的整数倍

所有栈创建宏都基于这些宏定义。

所有栈对象都具有以下布局，其中某些区域的大小可能因配置而为零。栈对象始终包含两个主要部分：起始处的预留内存，以及随后的栈缓冲区本身。某些区域的边界只能在运行时根据其关联的线程对象确定。其他区域则完全可以在构建时计算确定。

某些架构可能需要在运行时从栈缓冲区中划出预留内存，而不是在构建时无条件预留，也可能需要补充已有的预留区域（ARM FPU 就是这种情况）。这些划分始终会记录在 ``thread.stack_info.start`` 中。由 ``thread.stack_info.start`` 和 ``thread.stack_info.size`` 指定的区域始终可由用户模式线程完全访问。``thread.stack_info.delta`` 表示一个偏移量，可用于从栈对象的最末端计算初始栈指针，同时考虑 TLS 存储空间和 ASLR 随机偏移量。

.. code-block:: none

   +---------------------+ <- thread.stack_obj
   | Reserved Memory     | } K_(THREAD|KERNEL)_STACK_RESERVED
   +---------------------+
   | Carved-out memory   |
   |.....................| <- thread.stack_info.start
   | Unused stack buffer |
   |                     |
   |.....................| <- thread's current stack pointer
   | Used stack buffer   |
   |                     |
   |.....................| <- Initial stack pointer. Computable
   | ASLR Random offset  |      with thread.stack_info.delta
   +---------------------| <- thread.userspace_local_data
   | Thread-local data   |
   +---------------------+ <- thread.stack_info.start + thread.stack_info.size


目前，Zephyr 不支持向上增长的栈。

无内存保护
==========

如果未使用内存保护，默认设置就足够了。

基于硬件的栈溢出检测
====================

此选项利用硬件功能，在线程于特权模式下发生栈溢出时产生致命错误。这有助于调试，但出于以下原因，发生栈溢出后，无法对系统状态作出任何可靠的判断：

* 发生溢出时，内核可能正处于临界区中，导致重要的全局数据结构处于损坏状态。

* 对于使用保护内存区域实现栈保护的系统，栈有可能越过保护区域，在硬件检测到这种情况之前就破坏了相邻的数据结构。

要启用 :kconfig:option:`CONFIG_HW_STACK_PROTECTION` 功能，系统必须提供某种基于硬件的栈溢出保护，并启用 :kconfig:option:`CONFIG_ARCH_HAS_STACK_PROTECTION` 选项。

支持两种形式的硬件栈溢出检测：使用专门用于此目的的 CPU 功能，或使用紧邻栈缓冲区之前的特殊只读保护区域。

:kconfig:option:`CONFIG_HW_STACK_PROTECTION` 仅检测特权线程的栈溢出。检测用户线程的栈溢出不需要此功能；:kconfig:option:`CONFIG_USERSPACE` 与此功能相互独立。

此功能仅检测特权模式下的栈溢出，包括处理系统调用时发生的栈溢出。它无法保证内核未遭到破坏。特权模式下的任何栈溢出都应视为致命错误，此时无法对整个系统的完整性作出任何判断。

从内核的角度看，用户模式下的栈溢出是可恢复的，且无需特殊配置；:kconfig:option:`CONFIG_HW_STACK_PROTECTION` 仅用于检测 CPU 处于特权模式时发生的栈溢出。

基于 CPU 的栈溢出检测
---------------------

如果通过特殊的 CPU 寄存器（例如 ARM 的 SPLIM）检测特权模式下的栈溢出，那么默认设置就足够了。



基于保护区域的栈溢出检测
------------------------

通过位于栈缓冲区紧前方的特殊内存保护区域来检测特权模式下的栈溢出，写入该区域会触发异常。预留内存将用于此保护区域。

:c:macro:`ARCH_KERNEL_STACK_RESERVED` 应定义为内存保护区域的最小大小。在大多数 ARM CPU 上，此大小为 32 字节。:c:macro:`ARCH_KERNEL_STACK_OBJ_ALIGN` 也应设置为此区域要求的对齐值。

基于 MMU 的系统不应为保护区域预留 RAM，只需在将每个栈映射到地址空间时，在其下方留出一个不存在的虚拟页。栈对象仍需按页粒度正确对齐，并将大小调整为页大小的整数倍。

.. code-block:: none

   +-----------------------------+ <- thread.stack_obj
   | Guard reserved memory       | } K_KERNEL_STACK_RESERVED
   +-----------------------------+
   | Guard carve-out             |
   |.............................| <- thread.stack_info.start
   | Stack buffer                |
   .                             .

从内核栈中划出保护区域的情况并不常见，应尽可能避免。通常在以下两种情况下才需要这样做：

* 同一个栈可能被改用于承载用户线程，此时不需要保护区域，因此不应无条件预留。当权限提升栈不在栈对象内部时，就属于这种情况。

* 所需的保护区域大小可变，取决于上下文。例如，某些 ARM CPU 在异常处理期间采用浮点寄存器延迟入栈机制，可能将栈指针减去一个较大的值，却不写入任何内容，从而完全越过最小大小的保护区域并破坏相邻内存。因此，仅在线程使用浮点运算时划出额外内存，而不无条件预留更大的保护区域。

已启用用户模式
==============

启用用户模式会引入两项新要求：

* 必须分配一个独立的、大小固定且用户线程无法访问的特权模式栈，其大小由 :kconfig:option:`CONFIG_PRIVILEGED_STACK_SIZE` 指定。内核处理系统调用时使用此栈。如果实现了栈保护，则必须能够在该栈之前放置栈保护区域，必要时还需支持划出专用区域。

* 内存保护硬件必须能够配置一个恰好覆盖线程栈缓冲区的区域，该缓冲区由 ``thread.stack_info`` 记录。这意味着 :c:macro:`ARCH_THREAD_STACK_SIZE_ADJUST()` 需要将请求的栈大小向上取整，以便用一个区域覆盖它，同时还需根据内存保护硬件的粒度定义 :c:macro:`ARCH_THREAD_STACK_OBJ_ALIGN()` 。

如果内存保护硬件要求所有内存区域的大小均为 2 的幂，且按自身大小对齐，情况就会更加复杂。这在较旧的 MPU 上很常见，通过 :kconfig:option:`CONFIG_MPU_REQUIRES_POWER_OF_TWO_ALIGNMENT` 标识。

``thread.stack_info`` 始终记录栈对象中用户可访问的部分，使用其中存储的范围配置允许用户访问的内存保护区域，必须始终是正确的。

无 2 的幂约束的内存区域要求
---------------------------

在不要求区域大小为 2 的幂的系统上，可以使用 :c:macro:`K_THREAD_STACK_RESERVED` 定义的线程栈预留内存区域来存放特权模式栈。布局可以如下所示：

.. code-block:: none

   +------------------------------+ <- thread.stack_obj
   | Other platform data          |
   +------------------------------+
   | Guard region (if enabled)    |
   +------------------------------+
   | Guard carve-out (if needed)  |
   |..............................|
   | Privilege elevation stack    |
   +------------------------------| <- thread.stack_obj +
   | Stack buffer                 |      K_THREAD_STACK_RESERVED =
   .                              .      thread.stack_info.start

在线程创建时，保护区域以及任何划出的专用区域（如有需要）都将配置为只读区域。

* 如果线程是监管模式线程，权限提升区域就只是额外的栈内存。栈溢出最终会触及保护区域。

* 如果线程在用户模式下运行，则会配置一个内存保护区域，允许用户线程访问栈缓冲区，但不允许访问它之前或之后的任何内存。用户模式下的栈溢出会触及权限提升栈，而用户线程无权访问该栈。处理系统调用时的栈溢出则会触及保护区域。

在 MMU 系统上，不应存在物理保护区域；特权模式栈将映射到内核内存，栈缓冲区则映射到内存的用户部分，两者下方均设置标记为不存在的虚拟保护页，以捕获运行时的栈溢出。

其他平台数据可以存储在保护区域之前，但如果这些数据可以存储在 ``thread.arch`` 中的某处，则强烈不建议这样做。

需要定义 :c:macro:`ARCH_THREAD_STACK_RESERVED` ，以表示包含平台数据、权限提升栈和保护区域的预留区域大小。其大小必须设置得当，使得用于授予用户模式对栈缓冲区访问权限的 MPU 区域能够紧接在该预留区域之后。

具有 2 的幂约束的内存区域要求
-----------------------------

线程栈对象的大小和对齐值必须为同一个 2 的幂，且不包含任何预留内存，以便在内存中紧凑排列。因此，线程栈中的任何保护区域都必须完全从栈对象内部划出，而权限提升栈必须在其他位置分配。

:c:macro:`ARCH_THREAD_STACK_SIZE_ADJUST()` 和 :c:macro:`ARCH_THREAD_STACK_OBJ_ALIGN()` 都应定义为 :c:macro:`Z_POW2_CEIL()` 。:c:macro:`K_THREAD_STACK_RESERVED` 必须为 0。

对于特权栈，必须启用 :kconfig:option:`CONFIG_GEN_PRIV_STACKS` 。对于系统中找到的每个线程栈，都会生成一个对应的、大小固定的内核栈，用于处理系统调用。在运行时，可以使用 :c:func:`z_priv_stack_find()` 根据线程栈地址快速查找特权栈的地址。这些栈的布局与其他仅供内核使用的栈相同。

.. code-block:: none

   +-----------------------------+ <- z_priv_stack_find(thread.stack_obj)
   | Reserved memory             | } K_KERNEL_STACK_RESERVED
   +-----------------------------+
   | Guard carve-out (if needed) |
   |.............................|
   | Privilege elevation stack   |
   |                             |
   +-----------------------------+ <- z_priv_stack_find(thread.stack_obj) +
                                        K_KERNEL_STACK_RESERVED +
                                        CONFIG_PRIVILEGED_STACK_SIZE

   +-----------------------------+ <- thread.stack_obj
   | MPU guard carve-out         |
   | (supervisor mode only)      |
   |.............................| <- thread.stack_info.start
   | Stack buffer                |
   .                             .

线程栈对象中划出的保护区域仅在线程以监管模式运行时使用。如果线程降至用户模式，则不再设置保护区域，整个对象都用作栈缓冲区，关联的用户模式线程对其拥有完整访问权限，同时相应更新 ``thread.stack_info`` 。

用户模式线程
************

要支持用户模式线程，需要实现若干供内核调用的架构 API，并且系统必须启用 :kconfig:option:`CONFIG_ARCH_HAS_USERSPACE` 选项。有关详细信息，请参阅各函数的文档：

* :c:func:`arch_buffer_validate` 用于检查当前线程是否具有对特定内存区域的访问权限

* :c:func:`arch_user_mode_enter` 将监管模式线程降至用户模式权限，此过程不可逆。必须清空栈。

* :c:func:`arch_syscall_oops` 在无法验证系统调用参数时生成内核 oops，并使该 oops 看起来像是在用户线程中调用该系统调用的位置产生的

* :c:func:`arch_syscall_invoke0` 至 :c:func:`arch_syscall_invoke6` 使用相应数量的参数发起系统调用，所有参数都必须在权限提升期间通过寄存器传递。

* :c:func:`arch_is_user_context` 在 CPU 当前运行于用户模式时返回非零值

* :c:func:`arch_mem_domain_max_partitions_get` 指示内存域可包含的最大区域数量。MMU 系统对此数量没有限制，而 MPU 系统则有限制。

在调用内存域 API 时，某些架构可能需要更新另一个 CPU 上的软件内存管理结构或修改其硬件寄存器。在这种情况下，架构必须选择 :kconfig:option:`CONFIG_ARCH_MEM_DOMAIN_SYNCHRONOUS_API` ，并实现一些额外的 API。这在 MMU 系统上很常见，而在 MPU 系统上较少见：

* :c:func:`arch_mem_domain_thread_add`

* :c:func:`arch_mem_domain_thread_remove`

* :c:func:`arch_mem_domain_partition_add`

* :c:func:`arch_mem_domain_partition_remove`

详情请参阅这些 API 的 Doxygen 文档。

除了实现这些 API，还需要完成其他一些任务：

* :c:func:`_new_thread` 需要在用户模式下创建带有 :c:macro:`K_USER` 标志的线程

* 在上下文切换时，应通过对内存管理硬件进行适当的配置更改，将切出线程的栈内存标记为用户模式不可访问。同样，应将切入线程的栈内存标记为可访问。这样可以确保线程无法干扰其他线程的栈。

* 在上下文切换时，系统需要在切出线程和切入线程的内存域之间进行切换。

* 线程栈区域必须包含一个内核栈区域。用户线程在任何时候都不应能够访问此区域。进行系统调用时将使用此栈。所有线程的内核栈都应采用相同的固定大小，且必须足够大，能够处理任何系统调用。

* 需要建立软件中断或某种特权提升机制。这与 _arch_syscall_invoke 宏的实现方式密切相关。发生系统调用时，需要在 _k_syscall_table 中查找相应的处理函数。无效的系统调用 ID 应跳转到 :c:enum:`K_SYSCALL_BAD` 处理函数。系统调用完成后，必须注意避免将任何寄存器状态泄露到用户模式。

GDB 存根
********

要在新架构上启用 GDB 存根以进行远程调试：

#. 在相应架构的头文件目录下创建新的 ``gdbstub.h`` 头文件（ :file:`include/zephyr/arch/<arch>/gdbstub.h` ）。

   * 创建新的结构体 ``struct gdb_ctx`` 作为 GDB 上下文。

     * 必须定义一个名为 ``exception`` 、类型为 ``unsigned int`` 的成员，用于存储 GDB 异常原因。此值需要在进入 :c:func:`z_gdb_main_loop` 之前设置。

     * 架构可以根据需要定义任意数量的成员，以支持 GDB 存根正常工作。

     * 需要将指向此结构体的指针传递给 :c:func:`z_gdb_main_loop` ，该函数会将此指针传递给其他 GDB 存根函数。

#. 用于进入和退出 GDB 存根主循环的函数。

   * 如果架构依赖中断来处理断点，则需要实现中断服务例程（ISR），作为 GDB 存根主循环的入口。

   * 这些函数需要保存和恢复上下文，使代码能够继续执行，如同未遇到断点一样。

   * 这些函数需要在保存执行上下文后调用 :c:func:`z_gdb_main_loop` ，进入 GDB 存根主循环以接收来自 GDB 的命令。

   * 在调用 :c:func:`z_gdb_main_loop` 之前，必须设置 :c:member:`gdb_ctx.exception` 以指定异常原因。

#. 实现支持 GDB 存根功能所必需的函数：

   * :c:func:`arch_gdb_init`

     * 此函数需要完成支持 GDB 存根功能所必需的初始化，例如设置 GDB 上下文和连接调试中断。

     * 此函数必须通过架构特定的方法（例如触发调试中断）停止代码执行，以便 GDB 在启动期间连接。

   * :c:func:`arch_gdb_continue`

     * 当 GDB 发送 ``c`` 或 ``continue`` 命令以继续执行代码时，会调用此函数。

   * :c:func:`arch_gdb_step`

     * 当 GDB 发送 ``si`` 或 ``stepi`` 命令时，会调用此函数执行一条机器指令，然后返回 GDB 提示符。

   * 硬件寄存器读写函数：

     * 由于 GDB 存根在目标设备上运行，因此需要通过缓存副本操作硬件寄存器，以免影响 GDB 存根的执行。可以将此过程视为上下文切换，即执行上下文切换到 GDB 存根。因此，需要保存上下文切换前正在运行的线程的寄存器值。对寄存器值的操作必须仅针对这一缓存副本进行。在切换回先前运行的线程之前，再将更新后的值写入硬件寄存器。

     * :c:func:`arch_gdb_reg_readall`

       * 此函数收集将发回 GDB 的 ``g`` / ``G`` 数据包中包含的所有硬件寄存器值。G 数据包的格式取决于架构。有关预期格式，请查阅 GDB 文档。

       * 请注意，对于大多数架构，必须返回有效的 G 数据包并将其发送给 GDB。如果发送给 GDB 的数据包长度不正确，GDB 将中止调试会话。

     * :c:func:`arch_gdb_reg_writeall`

       * 此函数接收 GDB 发送的 G 数据包，并将其中的值写入硬件寄存器。

     * :c:func:`arch_gdb_reg_readone`

       * 此函数读取一个硬件寄存器的值，并将结果发送给 GDB。

     * :c:func:`arch_gdb_reg_writeone`

       * 此函数将从 GDB 接收的值写入一个硬件寄存器。

   * 断点：

     * :c:func:`arch_gdb_add_breakpoint` 和 :c:func:`arch_gdb_remove_breakpoint`

     * GDB 可能会选择使用软件断点，通过修改断点位置的内存，将指令替换为软件断点指令或陷阱指令。当执行到达断点时，GDB 会恢复内存内容。GDB 默认支持此功能，通常无需在架构代码中处理软件断点（断点类型为 ``0`` ）。

     * 如果代码位于运行时无法修改的 ROM 或闪存中，则需要使用硬件断点（类型为 ``1`` ）。有关如何启用硬件断点，请查阅架构数据手册。

     * 如果架构不支持硬件断点，则无需在架构代码中实现这些功能。此时 GDB 将依赖软件断点。

#. 对于某些内存区域不可访问的架构，需要定义一个名为 :c:var:`gdb_mem_region_array` 、元素类型为 :c:struct:`gdb_mem_region` 的数组，用于指定可访问的区域。对于每个数组元素：

   * :c:member:`gdb_mem_region.start` 指定内存区域的起始地址。

   * :c:member:`gdb_mem_region.end` 指定内存区域的结束地址。

   * :c:member:`gdb_mem_region.attributes` 指定内存区域的访问权限。

     * :c:macro:`GDB_MEM_REGION_RO` ：区域为只读。

     * :c:macro:`GDB_MEM_REGION_RW` ：区域可读写。

   * :c:member:`gdb_mem_region.alignment` 指定内存区域的读写对齐要求。如果没有对齐要求，且可以逐字节读写，则使用 ``0`` 。

API 参考
********

计时
====

.. doxygengroup:: arch-timing

线程
====

.. doxygengroup:: arch-threads

.. doxygengroup:: arch-tls

电源管理
========

.. doxygengroup:: arch-pm

对称多处理
==========

.. doxygengroup:: arch-smp

中断
====

.. doxygengroup:: arch-irq

用户空间
========

.. doxygengroup:: arch-userspace

内存管理
========

.. doxygengroup:: arch-mmu

其他架构 API
============

.. doxygengroup:: arch-misc

GDB 桩 API
==========

.. doxygengroup:: arch-gdbstub
