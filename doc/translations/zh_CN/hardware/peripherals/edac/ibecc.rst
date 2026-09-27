.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _edac_ibecc:

带内纠错码（IBECC）
###################

概述
****

该机制最初出现在 Intel Elkhart Lake SoC 及后续开发板上，由支持 IBECC 的集成内存控制器实现。

带内纠错码（IBECC）通过提供错误检测和纠正功能来提高可靠性。IBECC 可以作用于整个物理内存空间，也可以仅作用于特定区域。IBECC 适用于不支持带外 ECC 的内存技术。

IBECC 会增加相当于内存容量 1/32 的内存开销。这部分内存不可访问，用于存储 ECC 伴随式数据。IBECC 将读写事务转换为两个独立的事务：一个用于实际数据，另一个用于包含 ECC 值的缓存行。

IBECC 提供错误注入调试功能，帮助调试和验证 IBECC 功能。ECC 错误在写入路径上注入，并在读取路径上引发 ECC 错误。

IBECC 配置
**********

IBECC 有三种工作模式，可由引导加载程序选择，具体如下：

* OPERATION_MODE = 0x0 将工作模式设置为根据地址范围保护请求

* OPERATION_MODE = 0x1 将工作模式设置为不保护任何请求，并忽略范围检查

* OPERATION_MODE = 0x2 将工作模式设置为保护所有请求，并忽略范围检查

IBECC 的工作模式通过 BIOS 或引导加载程序配置。对于工作模式 0，BIOS 还提供内存区域等更多配置选项。

由于存在较高的安全风险，生产环境中不应启用错误注入功能。错误注入仅在测试时启用。

IBECC 日志记录
**************

IBECC 记录以下字段：

* 错误地址

* 错误伴随式

* 错误类型

  * 可纠正错误（CE）—— IBECC 模块检测到错误并将其纠正。

  * 不可纠正错误（UE）—— IBECC 模块检测到错误，但不会自动纠正。

IBECC 驱动提供错误类型，供上层应用实现所需的内存错误处理策略。IBECC 驱动不使用错误伴随式，但会将其提供给上层应用。

使用注意事项
************

处理不可屏蔽中断（NMI）时需要格外小心。NMI 随时可能到来，即使本地 CPU 已禁用中断也是如此。这意味着任何锁机制都无法保护代码免受 NMI 的影响。Zephyr 的 IPC 机制普遍使用本地 IRQ 锁定作为所有高层同步原语的底层基础。因此，不能与 NMI 共享任何受锁“保护”的内容，因为这种保护对 NMI 不起作用。Zephyr API 中唯一可用于与 NMI 同步的工具是原子操作层。这也适用于由 NMI 处理程序调用的回调函数。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_EDAC_IBECC`
