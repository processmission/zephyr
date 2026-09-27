.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _disk_nvme:

NVMe
####

NVMe 是 PCIe 总线上一种标准化的逻辑设备接口，用于公开存储设备。

支持 NVMe 控制器和磁盘。可以通过磁盘公开的 :ref:`磁盘访问 API <disk_access_api>` 访问磁盘，从而通过 :ref:`文件系统 API <file_system_api>` 使用它们。

驱动程序设计
************

该驱动分为 3 个主要部分：

- NVMe 控制器：:zephyr_file:`drivers/disk/nvme/nvme_controller.c`
- NVMe 命令：:zephyr_file:`drivers/disk/nvme/nvme_cmd.c`
- NVMe 命名空间：:zephyr_file:`drivers/disk/nvme/nvme_namespace.c`

其中，NVMe 控制器是设备驱动的根。它将获得设备驱动实例。请注意，这只是 DTS 所描述的内容：NVMe 控制器，而不包括其任何命名空间（磁盘）。NVMe 命令是用于与控制器及其公开的命名空间通信的通用逻辑。最后，NVMe 命名空间是处理实际命名空间的专用部分，它进而使应用能够通过磁盘访问 API :zephyr_file:`drivers/disk/nvme/nvme_disk.c` 访问每个命名空间。

如果控制器公开的命名空间（磁盘）超过 1 个，则可以通过调整配置选项 CONFIG_NVME_MAX_NAMESPACES（见下文）来提高内置命名空间支持的数量。

每个公开的磁盘通过其相关的 disk_info 结构，由其名称来区分，该名称继承自其相关的命名空间。因此，磁盘名称遵循 NVMe 命名规则，即 nvme<k>n<n>，其中 k 是控制器编号，n 是命名空间编号。大多数情况下，如果系统中只插入一个 NVMe 磁盘，将会看到 “nvme0n0” 作为公开的磁盘。

NVMe 配置
*********

DTS
===

任何公开 NVMe 磁盘的板都应提供 DTS overlay，以便在 Zephyr 中使用它

.. code-block:: devicetree

    #include <zephyr/dt-bindings/pcie/pcie.h>
    / {
        pcie0 {
            nvme0: nvme0 {
                compatible = "nvme-controller";
                vendor-id = <VENDOR_ID>;
                device-id = <DEVICE_ID>;
                status = "okay";
            };
        };
    };

其中 VENDOR_ID 和 DEVICE_ID 来自所公开的 NVMe 控制器。

选项
====

* :kconfig:option:`CONFIG_NVME`

请注意，NVME 需要目标平台支持 PCIe 多向量 MSI-X 才能正常工作。

* :kconfig:option:`CONFIG_NVME_MAX_NAMESPACES`

用户重要说明
************

NVMe 规范要求数据缓冲区放置在 dword（4 字节）对齐的地址处。虽然对于在用户进程之下管理虚拟内存和动态分配的高级操作系统而言这不是问题，但在 Zephyr 中，一旦缓冲区地址直接映射到物理内存，这就可能成为问题。

因此，在此阶段，用户需要确保提供给 :c:func:`disk_access_read` 和 :c:func:`disk_access_write` 的缓冲区地址是 dword 对齐的。
