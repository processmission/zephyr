.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _control_flow_integrity:

控制流完整性
############

控制流完整性（CFI）是一项安全特性，可确保程序的控制流遵循预定义的路径，从而防止攻击者将执行流重定向到恶意代码。CFI 在防御控制流劫持攻击（例如返回导向编程（ROP）和跳转导向编程（JOP））方面特别有用。

CFI 通过在运行时验证程序的控制流，确保函数调用和返回都指向合法的目标。这通常通过对代码进行插桩来实现，即在代码中加入检查，以验证控制流是否遵循程序的控制流图所定义的预期路径。

前向边与返回边
--------------

在 CFI 的语境中，控制流边可分为两类：

1. **前向边**：这些边表示从一个函数到另一个函数的控制流，例如函数调用。通常会验证前向边，以确保调用的目标是程序中的合法函数。
2. **返回边**：这些边表示从函数返回到调用者。验证返回边可确保返回地址是合法的，并对应于有效的调用点。

前向边可以通过编译器插桩来支持，即由编译器加入检查，以验证函数调用的目标是否有效。返回边可以通过维护影子栈或使用其他机制来支持，以确保返回地址合法。

Zephyr 确实支持维护影子栈，可通过 :kconfig:option:`CONFIG_HW_SHADOW_STACK` 启用。随后，内核会使用 :c:macro:`K_THREAD_HW_SHADOW_STACK_DEFINE` 之类的宏，并配合其他线程栈相关宏，为线程使用的影子栈提供区域。通常，应用程序只需启用 :kconfig:option:`CONFIG_HW_SHADOW_STACK` 以及相关的 :kconfig:option:`CONFIG_HW_SHADOW_STACK_PERCENTAGE_SIZE` 和 :kconfig:option:`CONFIG_HW_SHADOW_STACK_MIN_SIZE` 等选项即可启用影子栈支持。此后，内核将自动管理每个线程的影子栈。

实现细节
********

``K_THREAD_HW_SHADOW_STACK*`` 系列宏会完成影子栈参数的最小化设置，然后调用架构专用的 ``ARCH_THREAD_HW_SHADOW_STACK*`` 宏来执行实际设置。

硬件支持
--------

虽然 CFI 可以用软件实现，但硬件支持可以显著提升其有效性和性能。目前，Zephyr 支持 Intel 控制流强制技术（CET），可为 CFI 提供基于硬件的支持。

Intel CET
*********

Intel 控制流强制技术（CET）是一组硬件特性，通过为 CFI 提供支持来增强应用程序的安全性。CET 包含两个主要组件：

1. **影子栈**：此特性为返回地址维护一个单独的栈，确保返回地址无法被篡改。当函数返回时，返回地址会从影子栈中弹出，并与常规栈中的返回地址进行比较，从而为防御控制流劫持提供额外保护层。
2. **间接分支跟踪（IBT）**：此特性会跟踪间接分支（例如函数指针），并确保它们只指向代码中的有效位置。它可以防止攻击者通过 ROP 等技术将执行流重定向到任意代码。

这两个特性分别提供了返回边和前向边验证。要在 Zephyr 中启用影子栈支持，在受支持的硬件上，可以使用 :kconfig:option:`CONFIG_HW_SHADOW_STACK` Kconfig 选项。要启用 IBT，请使用 :kconfig:option:`CONFIG_X86_CET_IBT`。

由于 IBT 实际上由编译器实现，因此需要工具链支持。目前，可以使用 Zephyr SDK x86 工具链构建支持 IBT 的应用程序。但是，其预编译产物（例如 ``libc`` 和 ``libgcc``）并未启用 IBT。因此，对于 ``libc``，需要将其作为模块构建，例如使用 :kconfig:option:`CONFIG_PICOLIBC_USE_MODULE`。对于其他部分，则需要自定义工具链。

Intel CET 的限制
^^^^^^^^^^^^^^^^

目前，后台创建的影子栈位于全局命名空间中。因此，即使跨不同的编译单元，也 *不能* 重用线程栈名称。

ARM 指针认证与分支目标识别
**************************

ARM 平台通过指针认证（PAC）和分支目标识别（BTI）提供基于硬件的 CFI 特性，这些特性在 Cortex-M 和 ARM64（Cortex-A/R）架构上均可用：

1. **指针认证（PAC）**：使用密码学签名对返回地址和其他指针进行签名。当返回地址压入栈时，会使用每个线程独有的密钥对其进行签名。在返回之前，会验证签名，确保返回地址未被篡改。这可以防御返回导向编程（ROP）攻击。适用于 ARMv8.1-M Mainline（Cortex-M）以及 ARMv8.3-A 及更高版本（ARM64）。

2. **分支目标识别（BTI）**：使用特殊的 BTI 着陆垫指令标记合法的间接分支目标。处理器会验证间接分支是否仅落在带有 BTI 指令标记的有效目标上。这可以防御跳转导向编程（JOP）攻击。适用于 ARMv8.1-M Mainline（Cortex-M）以及 ARMv8.5-A 及更高版本（ARM64）。

这两个特性分别提供返回边和前向边验证。可以通过 :kconfig:option:`ARM_PACBTI` 菜单启用 PAC 和 BTI。可用选项包括 :kconfig:option:`CONFIG_ARM_PACBTI_STANDARD` （同时启用 PAC 和 BTI）、:kconfig:option:`CONFIG_ARM_PACBTI_PACRET` （仅 PAC）、:kconfig:option:`CONFIG_ARM_PACBTI_BTI` （仅 BTI）以及其他变体。这两个特性可以独立使用，也可以组合使用，以实现全面的控制流完整性。

与 x86 CET IBT 类似，这些特性需要编译器支持以及正确的 C 库插桩。PAC 要求函数使用相应的签名和验证指令，而 BTI 要求所有合法分支目标都包含 BTI 着陆垫指令。工具链提供的预编译 C 库通常缺少这类插桩。

对于 BTI 支持，C 库必须使用 ``-mbranch-protection`` 标志编译，以便在所有函数中包含 BTI 着陆垫。因此，当使用任何启用 BTI 的选项时，只能使用 :kconfig:option:`CONFIG_MINIMAL_LIBC`，或通过 :kconfig:option:`CONFIG_PICOLIBC_USE_MODULE` 作为模块构建的 picolibc。工具链中的 Newlib 不支持 BTI。

PAC 的要求没有那么严格，因为它主要影响函数序言和尾声，但为了获得最佳安全性，建议构建支持 PAC 的 C 库。
