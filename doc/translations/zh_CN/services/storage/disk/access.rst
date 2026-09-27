.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _disk_access_api:

磁盘访问
########

概述
****

磁盘访问 API 提供对存储设备的访问。

初始化磁盘
**********

由于许多磁盘设备（例如 SD 卡）支持热插拔，磁盘访问 API 提供了用于初始化和取消初始化磁盘的 IOCTL。它们如下所示：

* :c:macro:`DISK_IOCTL_CTRL_INIT`：初始化磁盘。必须在磁盘设备上运行其他 I/O 操作之前调用。等效于调用旧版函数 :c:func:`disk_access_init`。

* :c:macro:`DISK_IOCTL_CTRL_DEINIT`：取消初始化磁盘。一旦发出此 IOCTL，必须先发出 :c:macro:`DISK_IOCTL_CTRL_INIT`，然后才能将磁盘用于其他 I/O 操作。

init/deinit IOCTL 调用是平衡的，因此在发出的 deinit IOCTL 数量与 init IOCTL 数量相等之前，磁盘不会取消初始化。

还可以通过将指向设置为 ``true`` 的布尔值的指针作为参数传递给 :c:macro:`DISK_IOCTL_CTRL_DEINIT` IOCTL 来强制取消初始化磁盘。这是一种不安全操作，每个磁盘驱动的处理方式可能不同，但它始终会返回表示成功的值。

请注意，取消初始化磁盘是一种底层操作——通常应将取消初始化和初始化调用留给文件系统实现，用户应用无需手动取消初始化磁盘，而可以改为调用 :c:func:`fs_unmount`。

SD 卡支持
*********

Zephyr 支持某些 SD 卡控制器，并支持通过 SPI 连接 SD 卡。这些驱动使用磁盘驱动接口，文件系统可以通过磁盘访问 API 访问 SD 卡。支持标准容量和高容量 SD 卡。

.. note:: FAT 文件系统不具备掉电安全性，因此如果断电或在未卸载文件系统的情况下取出卡，文件系统可能会损坏

SD 存储卡子系统
===============

Zephyr 通过磁盘驱动 API 或 SDMMC 子系统支持 SD 存储卡。该子系统可以通过磁盘驱动 API 透明使用，但也支持对卡进行直接的块级访问。SDMMC 子系统与 :ref:`SD 主机控制器 API <sdhc_api>` 交互，以与连接的 SD 卡通信。


通过 SPI 支持 SD 卡
===================

下面的示例 devicetree 片段展示如何将 SD 卡节点添加到 ``spi1`` 接口。示例使用引脚 ``PA27`` 作为片选，并在 SD 卡初始化后以 24 MHz 运行 SPI 总线：

.. code-block:: devicetree

    &spi1 {
            status = "okay";
            cs-gpios = <&porta 27 GPIO_ACTIVE_LOW>;

            sdhc0: sdhc@0 {
                    compatible = "zephyr,sdhc-spi-slot";
                    reg = <0>;
                    status = "okay";
                    mmc {
                        compatible = "zephyr,sdmmc-disk";
                        disk-name = "SD";
                        status = "okay";
                    };
                    spi-max-frequency = <24000000>;
            };
    };

当板启动时，文件系统驱动将自动检测并初始化 SD 卡。

要读写文件和目录，请参见 :zephyr_file:`include/zephyr/fs/fs.h` 中的 :ref:`file_system_api`，例如 :c:func:`fs_open()`、:c:func:`fs_read()` 和 :c:func:`fs_write()`。

eMMC 设备支持
*************

Zephyr 还通过磁盘访问 API 支持 eMMC 设备。Zephyr 中的 MMC 使用 SD 子系统实现，因为 MMC 总线与 SD 总线有很多相似之处。MMC 控制器也使用 SDHC 设备驱动 API。

基于 flash 分区的仿真块设备支持
*******************************

Zephyr flashdisk 驱动可以将 flash 存储器分区用作块设备。flashdisk 实例在 devicetree 中定义：

.. code-block:: devicetree

    / {
        msc_disk0 {
            compatible = "zephyr,flash-disk";
            partition = <&storage_partition>;
            disk-name = "NAND";
            cache-size = <4096>;
        };
    };

:dtcompatible:`zephyr,flash-disk` 节点中指定的缓存大小应等于后备分区的最小可擦除块大小。

NVMe 磁盘支持
=============

也支持 NVMe 磁盘

.. toctree::
    :maxdepth: 1

    nvme.rst

VirtIO 块设备支持
*****************

也支持 VirtIO 块设备

.. toctree::
    :maxdepth: 1

    virtio_blk.rst


磁盘访问 API 配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_DISK_ACCESS`

API 参考
********

.. doxygengroup:: disk_access_interface

磁盘驱动配置选项
****************

相关驱动配置选项：

* :kconfig:option:`CONFIG_DISK_DRIVERS`

磁盘驱动接口
************

.. doxygengroup:: disk_driver_interface
