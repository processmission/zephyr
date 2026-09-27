.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

Trusted Firmware-M 集成
#######################

Trusted Firmware-M (TF-M) 部分介绍了 TF-M 与 Zephyr RTOS 之间的集成。你可以借助这些信息了解如何在 Cortex-M 平台上将 TF-M 与 Zephyr 集成，并在 Zephyr 应用中使用其安全运行时服务。

开发板定义
**********

如果将 :kconfig:option:`CONFIG_BUILD_WITH_TFM` 标志设置为 ``y``，TF-M 将与 Zephyr 一起为安全处理环境构建。

不过一般来说，不应在应用层级设置该值；TF-M 所需的所有配置标志都应在带有 ``_ns`` 后缀的开发板变体中设置。

该开发板变体必须定义恰当的 flash、SRAM 和外设配置，并将安全处理环境中的初始化过程考虑在内。此外，还必须将 :kconfig:option:`CONFIG_TFM_BOARD` 通过 `modules/trusted-firmware-m/Kconfig.tfm <https://github.com/zephyrproject-rtos/zephyr/blob/main/modules/trusted-firmware-m/Kconfig.tfm>`__ 设置为 TF-M 对该目标所期望的开发板名称，以便 TF-M 知道要为安全处理环境构建哪个目标。

示例：``mps2/an521/cpu0/ns``
============================

``mps2/an521/cpu0`` 开发板目标是一块双核 Arm Cortex-M33 评估板，会生成安全的 Zephyr 二进制文件。

而可选的 ``mps2/an521/cpu0/ns`` 开发板目标则会设置以下额外的 Kconfig 标志，表明 Zephyr 应构建为非安全镜像，作为外部项目与 TF-M 链接，并可选择链接安全 bootloader：

* :kconfig:option:`CONFIG_TRUSTED_EXECUTION_NONSECURE` ``y``
* :kconfig:option:`CONFIG_ARM_TRUSTZONE_M` ``y``

对比 :zephyr_file:`boards/arm/mps2/mps2_an521_cpu0.dts` 和 :zephyr_file:`boards/arm/mps2/mps2_an521_cpu0_ns.dts` 文件可以看出，``ns`` 版本定义了 flash 和 SRAM 内存中的偏移，从而为 TF-M 和安全 bootloader 留出所需空间：

::

    reserved-memory {
                #address-cells = <1>;
                #size-cells = <1>;
                ranges;

                /* The memory regions defined below must match what the TF-M
                 * project has defined for that board - a single image boot is
                 * assumed. Please see the memory layout in:
                 * https://git.trustedfirmware.org/TF-M/trusted-firmware-m.git/tree/platform/ext/target/mps2/an521/partition/flash_layout.h
                 */

                code: memory@100000 {
                        reg = <0x00100000 DT_SIZE_K(512)>;
                };

                ram: memory@28100000 {
                        reg = <0x28100000 DT_SIZE_M(1)>;
                };
        };

这样便为安全启动和 TF-M 预留了 1 MB 代码内存和 1 MB RAM，使我们的非安全 Zephyr 应用代码从 0x10000 开始，RAM 起始于 0x28100000。NS Zephyr 镜像可使用 512 KB 代码内存以及 1 MB RAM。

这与我们在 TF-M 的 ``flash_layout.h`` 中看到的 flash 内存布局一致：

::

    * 0x0000_0000 BL2 - MCUBoot (0.5 MB)
    * 0x0008_0000 Secure image     primary slot (0.5 MB)
    * 0x0010_0000 Non-secure image primary slot (0.5 MB)
    * 0x0018_0000 Secure image     secondary slot (0.5 MB)
    * 0x0020_0000 Non-secure image secondary slot (0.5 MB)
    * 0x0028_0000 Scratch area (0.5 MB)
    * 0x0030_0000 Protected Storage Area (20 KB)
    * 0x0030_5000 Internal Trusted Storage Area (16 KB)
    * 0x0030_9000 NV counters area (4 KB)
    * 0x0030_A000 Unused (984 KB)

``mps2/an521`` 将作为开发板目标传给 Tf-M，由 :kconfig:option:`CONFIG_TFM_BOARD` 指定。
