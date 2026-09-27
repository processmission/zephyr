.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _file_system_api:

文件系统
########

Zephyr RTOS 虚拟文件系统交换机（VFS）允许应用在不同的挂载点（例如 ``/fatfs`` 和 ``/lfs``）挂载多个文件系统。挂载点数据结构包含实例化、挂载和操作文件系统所需的全部信息。文件系统交换机通过引入文件系统注册机制，使应用无需直接访问单个文件系统的特定 API 或内部函数。

在 Zephyr 中，任何文件系统实现或库都可以通过文件系统注册 API 插入或移除。每个文件系统实现都必须具有全局唯一的整数标识符；请使用 :c:enumerator:`FS_TYPE_EXTERNAL_BASE` 以避免与树内标识符冲突。

.. code-block:: c

        int fs_register(int type, const struct fs_file_system_t *fs);

        int fs_unregister(int type, const struct fs_file_system_t *fs);

Zephyr RTOS 通过将挂载点用作磁盘卷名来支持一个文件系统的多个实例，文件系统库在格式化或挂载磁盘时会使用该卷名。

文件系统的声明方式如下：

.. code-block:: c

        static struct fs_mount_t mp = {
        .type = FS_FATFS,
        .mnt_point = FATFS_MNTP,
        .fs_data = &fat_fs,
        };

其中

- ``FS_FATFS`` 是文件系统类型，例如 FATFS 或 LittleFS。
- ``FATFS_MNTP`` 是文件系统将要挂载到的挂载点。
- ``fat_fs`` 是将由 fs_mount() API 使用的文件系统数据。



示例
****

VFS 的示例主要位于 ``samples/subsys/fs`` 中，不过不同子系统的示例中也提供了 VFS 用法的各种示例，作为重要功能。以下是一些值得查看的示例：

- :zephyr:code-sample:`fs` 是使用 SDHC 介质的 FAT 文件系统用法示例；
- :zephyr:code-sample:`shell-fs` 是 Shell fs 子系统的示例，使用格式化为 LittleFS 的内部 flash 分区；
- :zephyr:code-sample:`usb-mass` 是 USB 大容量存储设备示例，根据示例配置不同，使用带 RAM 的 FAT FS 驱动、SPI 连接的 FLASH，或 flash 中的 LittleFS。

API 参考
********

.. doxygengroup:: file_system_api
