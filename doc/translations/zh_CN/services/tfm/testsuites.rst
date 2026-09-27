.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

测试套件
########

TF-M 包含两套测试套件：

* tf-m-tests - 标准的 TF-M 专用回归测试
* psa-arch-tests - 针对特定 PSA API（如安全存储等）的测试套件

可以从 Zephyr 运行这些测试套件，只需使用 samples/tfm_integration 文件夹中相应的示例应用。

TF-M 回归测试
*************

回归测试套件可以通过 :zephyr_file:`tests/modules/tf-m/regression` 测试来运行。

它通过 PSA API 测试跨越 NS/S 边界的各种服务和通信机制。这些测试为 NS RTOS（此处为 Zephyr）与安全应用（TF-M）之间的正确集成提供了有用的健全性检查。

PSA 架构测试
************

PSA 架构测试套件可通过 :ref:`tfm_psa_test` 获取，其中包含多个测试套件，可用于验证安全应用是否遵循 PSA API 规范，TF-M 正是平台安全架构（PSA）的一种实现。

一次只能运行其中一个套件，可用的测试套件通过 ``CONFIG_TFM_PSA_TEST_*`` KConfig 标志描述：

用途
****

要为你特定的开发板、RTOS（此处为 Zephyr）和 PSA 实现（此处为 TF-M）获得 PSA 认证，需要这些测试套件的输出。

它们还提供了一个有用的测试用例，可用于验证对 TF-M 做出有意义更改的任何 PR，例如启用新的 TF-M 开发板目标，或修改 TF-M 核心模块。通常应在发布新开发板支持等新 PR 之前运行它们，作为一致性检查。
