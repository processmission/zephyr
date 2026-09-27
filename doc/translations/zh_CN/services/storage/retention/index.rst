.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _retention_api:

保留系统
########

保留系统提供一个 API，允许应用从在设备供电期间保持数据的内存区域或设备读取数据以及向其中写入数据。这样可以在不同应用之间或单个应用内部共享信息，而不会在设备重启时丢失状态信息。存储的数据在断电时（或某些设备处于某些低功耗模式时）不应保留，也不应存储到非易失性存储器（如 :ref:`flash_api`、:ref:`eeprom_api` 或电池后备 RAM）中。

保留系统构建在保留数据驱动之上，并为其添加额外的软件层功能以确保数据的有效性。可选地，可以使用魔术头来检查保留数据内存区域的开头是否包含这个特定值，并且可以将存储数据的可选校验和（大小为 1、2 或 4 字节）追加到数据末尾。此外，保留系统 API 允许将保留数据区域划分为多个不同的区域。例如，一个 64 字节的保留数据区域可以划分为 4 字节用于启动模式、16 字节用于时间戳、44 字节用于最后一条日志消息。所有这些区域都可以独立访问或更新。前缀和校验和可以使用 devicetree 按实例设置。

Devicetree 设置
***************

要使用保留系统，必须为所使用的板设置一个保留数据驱动；可以使用一个 Zephyr 驱动，它将一些 RAM 用作 non-init 以达到此目的。随后，将保留系统作为该设备的子节点初始化一次或多次——请注意，需要减少内存区域以考虑 RAM 中这部分保留区域。请参见以下示例（本指南中的示例基于 :zephyr:board:`nrf52840dk` 板和内存布局）：

.. code-block:: devicetree

        / {
                sram@2003FC00 {
                        compatible = "zephyr,memory-region", "mmio-sram";
                        reg = <0x2003FC00 DT_SIZE_K(1)>;
                        zephyr,memory-region = "RetainedMem";
                        status = "okay";

                        retainedmem {
                                compatible = "zephyr,retained-ram";
                                status = "okay";
                                #address-cells = <1>;
                                #size-cells = <1>;

                                /* This creates a 256-byte partition */
                                retention0: retention@0 {
                                        compatible = "zephyr,retention";
                                        status = "okay";

                                        /* The total size of this area is 256
                                         * bytes which includes the prefix and
                                         * checksum, this means that the usable
                                         * data storage area is 256 - 3 = 253
                                         * bytes
                                         */
                                        reg = <0x0 0x100>;

                                        /* This is the prefix which must appear
                                         * at the front of the data
                                         */
                                        prefix = [08 04];

                                        /* This uses a 1-byte checksum */
                                        checksum = <1>;
                                };

                                /* This creates a 768-byte partition */
                                retention1: retention@100 {
                                        compatible = "zephyr,retention";
                                        status = "okay";

                                        /* Start position must be after the end
                                         * of the previous partition. The total
                                         * size of this area is 768 bytes which
                                         * includes the prefix and checksum,
                                         * this means that the usable data
                                         * storage area is 768 - 6 = 762 bytes
                                         */
                                        reg = <0x100 0x300>;

                                        /* This is the prefix which must appear
                                         * at the front of the data
                                         */
                                        prefix = [00 11 55 88 fa bc];

                                        /* If omitted, there will be no
                                         * checksum
                                         */
                                };
                        };
                };
        };

        /* Reduce SRAM0 usage by 1KB to account for non-init area */
        &sram0 {
                reg = <0x20000000 DT_SIZE_K(255)>;
        };

随后，可以使用数据保留 API（在通过 :kconfig:option:`CONFIG_RETENTION` 启用后，该选项要求启用 :kconfig:option:`CONFIG_RETAINED_MEM`）通过以下方式获取设备，从而访问保留区域：

.. code-block:: C

        #include <zephyr/device.h>
        #include <zephyr/retention/retention.h>

        const struct device *retention0 = DEVICE_DT_GET(DT_NODELABEL(retention0));
        const struct device *retention1 = DEVICE_DT_GET(DT_NODELABEL(retention1));

调用写入函数时，魔术头和校验和（如果启用）将在该区域上设置，并且从那时起该区域被标记为有效。

互斥锁保护
**********

当应用以多线程支持进行编译时，默认启用保留区域的互斥锁保护。这意味着不同线程可以安全地调用保留函数，而不会与其他并发线程的函数使用发生冲突，但这也意味着无法从 ISR 中调用保留函数。可以通过启用 :kconfig:option:`CONFIG_RETENTION_MUTEX_FORCE_DISABLE` 全局禁用所有保留区域上的互斥锁保护——此时用户需负责确保函数调用之间不会相互冲突。请注意，要使用此功能，还必须通过启用 :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE` 来禁用保留驱动的互斥锁支持。

.. _boot_mode_api:

启动模式
********

保留子系统的另一个新增功能是启动模式接口，它可用于在设备重启时动态更改应用状态，或使用一组最少的功能运行不同的应用（例如，提供一种从主应用无按钮进入 mcuboot 串行恢复功能的方式）。

要使用启动模式功能，devicetree 中必须存在一个专用于启动模式选择的数据保留条目（用户区域数据大小只需为单个字节），并将该区域分配给 ``zephyr,boot-mode`` 的 chosen 节点。请参见以下示例：

.. code-block:: devicetree

        / {
                sram@2003FFFF {
                        compatible = "zephyr,memory-region", "mmio-sram";
                        reg = <0x2003FFFF 0x1>;
                        zephyr,memory-region = "RetainedMem";
                        status = "okay";

                        retainedmem {
                                compatible = "zephyr,retained-ram";
                                status = "okay";
                                #address-cells = <1>;
                                #size-cells = <1>;

                                retention0: retention@0 {
                                        compatible = "zephyr,retention";
                                        status = "okay";
                                        reg = <0x0 0x1>;
                                };
                        };
                };

                chosen {
                        zephyr,boot-mode = &retention0;
                };
        };

        /* Reduce SRAM0 usage by 1 byte to account for non-init area */
        &sram0 {
                reg = <0x20000000 0x3FFFF>;
        };

启动模式接口可以通过 :kconfig:option:`CONFIG_RETENTION_BOOT_MODE` 启用，然后通过使用启动模式函数来访问。如果将 mcuboot 与串行恢复一起使用，可以在启用 ``CONFIG_MCUBOOT_SERIAL`` 和 ``CONFIG_BOOT_SERIAL_BOOT_MODE`` 的情况下构建它，这将允许通过以下方式直接重启进入串行恢复模式：

.. code-block:: C

        #include <zephyr/retention/bootmode.h>
        #include <zephyr/sys/reboot.h>

        bootmode_set(BOOT_MODE_TYPE_BOOTLOADER);
        sys_reboot(0);

保留系统模块
************

模块可以将保留系统用作传输通道（例如在引导加载程序和应用之间），从而扩展保留系统的功能。

.. toctree::
    :maxdepth: 1

    blinfo.rst

API 参考
********

保留系统 API
============

.. doxygengroup:: retention_api

启动模式接口
============

.. doxygengroup:: boot_mode_interface
