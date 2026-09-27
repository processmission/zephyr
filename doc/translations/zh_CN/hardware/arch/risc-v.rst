.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

Zephyr 对 RISC-V 处理器的支持状态
#################################

概述
****

本页介绍 Zephyr 对 RISC-V 处理器的当前支持情况。目前已支持部分开发板、Qemu，以及 neorv32 和 litex_vexriscv 等 FPGA 实现。

Zephyr 支持 PMP、:ref:`用户模式<usermode_api>` 、多种 ISA 扩展以及 :ref:`半主机<semihost_guide>` 。

用户模式和 PMP 支持
*******************

当平台支持物理内存保护（PMP）时，在 Zephyr 中启用 PMP 后，即可选择启用用户空间支持和栈保护。

ISA 扩展
********

可以通过设置相应的 ``CONFIG_RISCV_ISA_*`` Kconfig 选项，在 Zephyr 中指定给定平台可用的 ISA 扩展（RV32/64I(E)MAFD(G)QC）。更多信息请参阅 :file:`arch/riscv/Kconfig.isa` 。

请注意，Zephyr SDK 工具链可能并未支持所有组合。

监管模式（S-mode）
******************

启用 :kconfig:option:`CONFIG_RISCV_S_MODE` 后，Zephyr 内核运行在 RISC-V 监管模式（S-mode）下，而非机器模式（M-mode）。这遵循应用级操作系统所采用的标准 RISC-V 特权架构，也是支持 MMU 的必要条件。

源码树内的一个最小 M-mode 运行时（ ``arch/riscv/core/sbi.S`` ）充当固件。它在启动时完成最初的 M-mode 到 S-mode 切换，并通过 RISC-V 监管二进制接口（SBI）处理 S-mode 请求：

- **启动顺序** ：M-mode 配置 PMP、 ``medeleg`` 、 ``mideleg`` 、 ``mcounteren`` 和 ``mtvec`` ；若存在 Zkr 扩展，则通过 ``mseccfg`` 授予 S-mode 对 ``seed`` CSR 的访问权限，然后通过 ``mret`` 降至 S-mode。
- **定时器** ：机器定时器中断（MTIP）以监管定时器中断（STIP）的形式转发至 S-mode。S-mode 通过 SBI 的 ``TIME`` 扩展（ ``sbi_set_timer`` ）设置定时器的下一次到期时间。
- **Ecall** ：S-mode ecall（异常原因码 9）通过 ``medeleg`` 路由至 M-mode 运行时；其他所有异常和中断均委托给 S-mode。请参阅下文的 :ref:`riscv-smode-ecall-constraint` 。

无需外部固件；源码树内的运行时可独立工作。

已知限制
========

**PLIC 外部中断** ：PLIC 驱动始终为 hart 0 配置 M-mode 上下文。在 S-mode 下，正确的上下文应为监管上下文，因此由 PLIC 传递的外部中断（UART、GPIO、SPI、I2C 等）无法到达 CPU。定时器中断不受影响，因为它由 M-mode 运行时通过 ``sip.STIP`` 直接转发，绕过了 PLIC。

.. _riscv-smode-ecall-constraint:

S-mode ecall 约束
=================

在 M-mode 下，Zephyr 使用 ``ecall`` 指令作为内核内部主动触发陷阱的机制：由于内核无条件掌控 M-mode， ``ecall`` 会触发原因码为 11 的异常（M-mode ecall），随后由 ``_isr_wrapper`` 将其分派给所请求的内核服务（致命错误、 ``irq_offload`` 、上下文切换）。

在 S-mode 下，此机制不可用。从 S-mode 执行 ``ecall`` 始终会触发原因码为 9 的异常，而原因码 9 **不会** 被委托给 S-mode（ ``medeleg`` 位 9 = 0），因为它必须到达 M-mode SBI 处理程序，这是 S-mode 请求 M-mode 服务的唯一途径，例如通过 ``sbi_set_timer`` 设置定时器。 ``medeleg`` 中的该位无法根据寄存器值进行区分：将原因码 9 委托给 S-mode 会破坏 SBI；将其保留在 M-mode 则意味着原因码 9 无法用于内核内部。

S-mode 移植的实际规则如下：

   ``ecall`` 专用于 SBI 接口。任何在 M-mode 下使用 ``ecall`` 的内核机制，都必须通过直接在 S-mode 中执行的路径重新实现。

此移植中的两个具体示例：

- :c:macro:`ARCH_EXCEPT` （ ``include/zephyr/arch/riscv/error.h`` ）——直接调用 :c:func:`z_riscv_fatal_error` ，不再执行 ``ecall`` 经由 ``_isr_wrapper`` 进入致命错误处理流程。

- ``arch_irq_offload`` （ ``arch/riscv/core/irq_offload.c`` ）——直接模拟 ISR 上下文，不再执行 ``ecall`` 进入 ``_isr_wrapper`` 的 ``do_irq_offload`` 路径：禁用中断，递增 ``nested`` ，调用例程，递减 ``nested`` ，重新启用中断，然后调用 :c:func:`z_reschedule_unlocked` 以处理在该例程内变为就绪状态的线程。

将 `OpenSBI`_ 等外部 SBI 实现作为 west 模块使用的支持，留待后续实现。

SMP 支持
********

RISC-V 的 QEMU 虚拟化平台和硬件平台均支持 SMP。要测试 SMP 支持，可在基于 QEMU 的平台上使用 :zephyr:board:`qemu_riscv32` 或 :zephyr:board:`qemu_riscv64` ，在硬件平台上使用 :zephyr:board:`beaglev_fire` 或 :zephyr:board:`mpfs_icicle` 。

.. _OpenSBI: https://github.com/riscv-software-src/opensbi
