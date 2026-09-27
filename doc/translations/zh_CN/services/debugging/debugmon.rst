.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _debugmon:

Cortex-M 调试监视器
###################

监视器模式调试是 Cortex-M 的一项功能，它提供了一种非停机式的调试方法。借助该功能，即使正在断点处等待，高优先级中断仍可继续执行。这种策略使得调试时间敏感型软件成为可能，否则这些软件会在内核停止时崩溃（例如需要保持通信链路活跃的应用）。

Zephyr 支持启用和配置 Debug Monitor 异常。它还包含一个现成的中断实现，可与 SEGGER J-Link 调试器配合使用。

配置
****

使用以下选项配置此模块。

* :kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK` 启用该模块。仅使用该选项时，需要提供一个调试监视器中断的实现，该中断将在程序每次进入断点时执行。

配合 SEGGER 调试探针，可以使用 SEGGER 提供的现成中断实现。

* :kconfig:option:`CONFIG_SEGGER_DEBUGMON` 启用 SEGGER 调试监视器中断。可与 SEGGER JLinkGDBServer 和 SEGGER 调试探针配合使用。


用法
****

启用监视器模式调试后，进入断点不会暂停处理器，而是会生成一个中断，其 ISR 在 ``z_arm_debug_monitor`` 符号下实现。:kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK` 配置会将该中断配置为可用的最低优先级，这样当处理器在断点处等待时，其他中断仍可执行。

使用 SEGGER 提供的 ISR
======================

随 :kconfig:option:`CONFIG_SEGGER_DEBUGMON` 提供的现成实现提供了使用常规 GDB 命令在监视器模式下调试所需的功能。配置 SEGGER 调试监视器的步骤如下：

1. 构建一个示例，启用 :kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK` 和 :kconfig:option:`CONFIG_SEGGER_DEBUGMON` 配置。

2. 将 JLink GDB 服务器连接到目标。Linux 命令示例：``JLinkGDBServerCLExe -device <device> -if swd``。

3. 使用你的 GDB 安装连接到服务器。Linux 命令示例：``arm-none-eabi-gdb --ex="file build/zephyr.elf" --ex="target remote localhost:2331"``。

4. 使用以下命令在 GDB 中启用监视器模式调试：``monitor exec SetMonModeDebug=1``。

完成这些步骤后，使用常规 GDB 命令调试你的程序。


使用其他自定义 ISR
==================
要提供自定义调试监视器中断，请覆盖 ``z_arm_debug_monitor`` 符号。此外，还需要手动配置一些寄存器（参见 :zephyr:code-sample:`debugmon` 示例）。
