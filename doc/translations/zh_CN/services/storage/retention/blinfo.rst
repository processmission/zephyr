.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _blinfo_api:

引导加载程序信息
################

引导加载程序信息（缩写为 blinfo）子系统是 :ref:`retention_api` 的扩展，它允许从引导加载程序读取共享数据，并允许应用查询这些数据。它有一个可选功能：将从引导加载程序获取的信息整理并存储到 :ref:`settings_api` 中，使用 ``blinfo/`` 前缀。

Devicetree 设置
***************

要使用引导加载程序信息子系统，需要创建一个保留区域，其父节点为保留数据区域；通常为此使用 non-init RAM。请参见以下示例（本指南中的示例基于 :zephyr:board:`nrf52840dk` 板和内存布局）：

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

                                boot_info0: boot_info@0 {
                                        compatible = "zephyr,retention";
                                        status = "okay";
                                        reg = <0x0 0x100>;
                                };
                        };
                };

                chosen {
                        zephyr,bootloader-info = &boot_info0;
                };
        };


        /* Reduce SRAM0 usage by 1KB to account for non-init area */
        &sram0 {
                reg = <0x20000000 DT_SIZE_K(255)>;
        };

请注意，此配置需要同时应用于引导加载程序（MCUboot）和应用才能使用。它可以与其他保留系统 API（如 :ref:`boot_mode_api`）结合使用。

MCUboot 设置
************

应用上述 devicetree 配置后，需要配置 MCUboot 以将共享数据存储在此区域；为此需要设置以下 Kconfig：

* :kconfig:option:`CONFIG_RETAINED_MEM` - 启用保留内存驱动
* :kconfig:option:`CONFIG_RETENTION` - 启用保留系统
* :kconfig:option:`CONFIG_BOOT_SHARE_DATA` - 启用共享数据
* :kconfig:option:`CONFIG_BOOT_SHARE_DATA_BOOTINFO` - 启用启动信息共享数据类型
* :kconfig:option:`CONFIG_BOOT_SHARE_BACKEND_RETENTION` - 使用 retention/blinfo 子系统存储共享数据

应用设置
********

应用必须启用以下基础 Kconfig 选项，引导加载程序信息子系统才能正常工作：

* :kconfig:option:`CONFIG_RETAINED_MEM`
* :kconfig:option:`CONFIG_RETENTION`
* :kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO`
* :kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO_TYPE_MCUBOOT`

使用引导加载程序信息子系统需要包含以下头文件：

.. code-block:: C

        #include <zephyr/retention/blinfo.h>

默认情况下，仅提供查找函数：:c:func:`blinfo_lookup`，应用可以调用它来查询来自引导加载程序的信息。该函数通过 :kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO_OUTPUT_FUNCTION` 默认启用；不过，应用也可以选择改用 settings 存储功能。在此模式下，可以使用 settings 键查询引导加载程序信息；此模式需要启用以下 Kconfig 选项：

* :kconfig:option:`CONFIG_SETTINGS`
* :kconfig:option:`CONFIG_SETTINGS_RUNTIME`
* :kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO_OUTPUT_SETTINGS`

这样可以通过 :c:func:`settings_runtime_get` 函数使用以下键来查询信息：

* ``blinfo/mode`` MCUboot 配置的模式（``enum mcuboot_mode`` 值）
* ``blinfo/signature_type`` MCUboot 配置的签名类型（``enum mcuboot_signature_type`` 值）
* ``blinfo/recovery`` MCUboot 中启用的恢复类型（``enum mcuboot_recovery_mode`` 值）
* ``blinfo/running_slot`` 正在运行的槽位，对于 direct-XIP 模式了解更新应使用哪个槽位很有用
* ``blinfo/bootloader_version`` 引导加载程序的版本（``struct image_version`` 对象）
* ``blinfo/max_application_size`` 可加载应用的最大大小（以字节为单位）

除了前面的头文件之外，此模式还需要包含以下头文件：

.. code-block:: C

        #include <bootutil/boot_status.h>
        #include <bootutil/image.h>
        #include <zephyr/mcuboot_version.h>
        #include <zephyr/settings/settings.h>

API 参考
********

引导加载程序信息 API
====================

.. doxygengroup:: bootloader_info_interface
