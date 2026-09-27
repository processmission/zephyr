.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _disk_virtio_blk:

VirtIO 块设备
#############

VirtIO 是一种标准化接口，用于向客户机公开虚拟设备，通常运行在 QEMU 等虚拟机监控程序下。``virtio,blk`` 驱动将 VirtIO 块设备呈现为 Zephyr 磁盘：可以通过 :ref:`磁盘访问 API <disk_access_api>` 访问它，并进而通过 :ref:`文件系统 API <file_system_api>` 访问。

该驱动与传输层无关，可在 Zephyr 支持的两种 VirtIO 传输（PCI 和 MMIO）上不加更改地运行（参见 :ref:`VirtIO <virtio>`）。每个启用的 ``virtio,blk`` devicetree 节点都会创建一个实例。

驱动程序设计
************

该驱动位于 :zephyr_file:`drivers/disk/virtio_blk.c`，并构建在通用 VirtIO API 之上。``virtio,blk`` 节点是 VirtIO 传输设备（``DT_INST_PARENT``）的子节点，因此同一份代码无需更改即可服务于 PCI 或 MMIO 设备。

单次在途请求
============

``disk_access`` 读/写 API 是同步且阻塞的。该驱动还使用互斥锁串行化调用者，因此每个设备始终只保留一个在途请求：它向请求 virtqueue 添加单个描述符链，通知设备，然后阻塞在一个信号量上，该信号量由完成回调从中断上下文发出。

由于没有请求流水线，整个 virtqueue 都用于单个请求的分散-聚集链。面向用户的调节参数是每个请求的最大数据段数（:kconfig:option:`CONFIG_DISK_VIRTIO_BLK_MAX_SEGMENTS`）；驱动通过将 ``MAX_SEGMENTS + 2`` 向上取整到 2 的幂来确定 virtqueue 的大小，从而为请求头和状态字节留出空间。

块大小
======

VirtIO 块协议始终以固定的 512 字节扇区对设备进行寻址，并以这些单位报告设备容量。向 ``disk_access`` 公开的逻辑块大小可能不同：

* 当设备提供 ``VIRTIO_BLK_F_BLK_SIZE`` 时，驱动会协商该特性，并公开设备通告的 ``blk_size``。
* 否则，它会回退到 :kconfig:option:`CONFIG_DISK_VIRTIO_BLK_SECTOR_SIZE`。

所有寻址在内部都会转换为 512 字节的 VirtIO 扇区。块大小必须是 512 的倍数，并且在 :kconfig:option:`CONFIG_MMU` 下不得超过 MMU 页大小；不支持的值会在初始化时被拒绝。

零拷贝传输
==========

调用者的缓冲区会直接交给设备，而不使用回弹缓冲区。在 :kconfig:option:`CONFIG_MMU` 下，缓冲区可能位于内核线性 RAM 映射之外（例如 ``f_mkfs()`` 向下传递的线程栈工作区），并且不必物理连续。驱动使用 ``arch_page_phys_get()`` 逐页遍历这样的缓冲区，将物理上相邻的连续区域合并为分散-聚集段，并且当传输的碎片程度超过段预算允许的范围时，将其拆分为多个设备请求。

特性协商
========

除了 ``VIRTIO_BLK_F_BLK_SIZE`` 之外，该驱动还会协商：

* ``VIRTIO_BLK_F_RO`` — 只读设备会报告为 ``DISK_STATUS_WR_PROTECT``，写请求会被拒绝并返回 ``-EROFS``。
* ``VIRTIO_BLK_F_FLUSH`` — ``DISK_IOCTL_CTRL_SYNC`` 会向设备发出刷新。当设备未提供 ``FLUSH`` 时，没有回写缓存需要刷新，因此该 ioctl 是成功的空操作，而不是错误。

已完成但状态字节不是 ``OK`` 的请求会被记录，并映射为 errno：不支持的请求变为 ``-ENOTSUP``，I/O 错误变为 ``-EIO``。

VirtIO 块设备配置
*****************

DTS
===

``virtio,blk`` 节点放置在其 VirtIO 传输父节点下，并需要一个供 ``disk_access`` API 使用的 ``disk-name``。在 PCI 传输上：

.. code-block:: devicetree

    #include <zephyr/dt-bindings/pcie/pcie.h>

    / {
        pcie0 {
            virtio-blk-pci {
                compatible = "virtio,pci";
                vendor-id = <0x1af4>;
                device-id = <0x1001>;
                interrupts = <0xb 0x0 0x0>;
                interrupt-parent = <&intc>;
                status = "okay";

                virtio_blk: virtio-blk {
                    compatible = "virtio,blk";
                    disk-name = "VIRTIOBLK0";
                    status = "okay";
                };
            };
        };
    };

在 MMIO 传输上，该节点是现有 ``virtio,mmio`` 总线的子节点：

.. code-block:: devicetree

    &virtio_mmio4 {
        status = "okay";

        virtio_blk: virtio-blk {
            compatible = "virtio,blk";
            disk-name = "VIRTIOBLK0";
            status = "okay";
        };
    };

选项
----

* :kconfig:option:`CONFIG_DISK_DRIVER_VIRTIO_BLK`
* :kconfig:option:`CONFIG_DISK_VIRTIO_BLK_MAX_SEGMENTS`
* :kconfig:option:`CONFIG_DISK_VIRTIO_BLK_SECTOR_SIZE`

QEMU 选项
---------

当在 QEMU 板上启用 :kconfig:option:`CONFIG_DISK_DRIVER_VIRTIO_BLK` 时，仿真层会创建一个原始后备映像，并将其附加到仿真 virtio-blk 设备。PCI 传输由通用 QEMU 仿真代码附加；``qemu_cortex_a53`` 板将 MMIO ``virtio-blk-device`` 附加到 ``virtio-mmio-bus.4``。

* :kconfig:option:`CONFIG_QEMU_VIRTIO_BLK_LOGICAL_BLOCK_SIZE`
* :kconfig:option:`CONFIG_QEMU_VIRTIO_BLK_DISK_SIZE`

限制
****

* 同一时间恰好只有一个请求在途。这符合同步 ``disk_access`` 约定，因此不会给该使用方造成吞吐量损失，但该驱动不提供请求流水线。
* 与 Zephyr 其余 VirtIO 子系统一样，该驱动假定 DMA 是一致的，并且不对描述符、环或数据缓冲区执行缓存维护。
* 在 MMU 下，逻辑块大小不能超过 MMU 页大小。
