.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _nvs_api:

非易失性存储（NVS）
###################

以 id-data 对表示的元素使用 FIFO 管理的循环缓冲区存储在 flash 中。flash 区域被划分为扇区。元素会追加到某个扇区，直到该扇区中的存储空间耗尽。然后，将 flash 区域中的一个新扇区准备好（擦除）以供使用。在擦除该扇区之前，会检查在用扇区中是否存在标识符-数据对，如果不存在，则复制该 id-data 对。

id 是一个 16 位无符号数。NVS 确保对于每个已使用的 id，flash 中始终至少存储一个 id-data 对。

NVS 支持存储二进制块、字符串、整数、长整数及其任意组合。

每个元素在 flash 中存储为元数据（8 字节）和数据。元数据写入从 NVS 扇区末尾开始的表中，数据则从扇区开头开始依次写入。元数据由以下部分组成：id、扇区中的数据偏移量、数据长度、part（未使用）和 CRC。此 CRC 仅根据元数据计算，仅用于确保写入已完成。元素的实际数据可以通过另一个（可选的）CRC-32 进行保护。使用 :kconfig:option:`CONFIG_NVS_DATA_CRC` 配置项启用数据部分 CRC。

.. note:: 仅在读取元素的完整数据时才会检查数据 CRC。部分读取不会检查数据 CRC，因为它存储在元素数据区域的末尾。

.. note:: 在以前没有数据 CRC 的现有 NVS 内容上启用数据 CRC 功能，将使所有现有数据失效。

向 NVS 写入数据总是先写入数据，然后写入元数据。初始化期间，写入 flash 但没有元数据的数据会被忽略。

初始化期间，NVS 将验证存储在 flash 中的数据；如果遇到错误，将忽略缺失或不正确元数据的任何数据。

NVS 在将数据写入 flash 之前检查 id-data 对。如果 id-data 对未更改，则不会执行对 flash 的写入。

为了保护 flash 区域免受频繁擦除的影响，必须有足够的可用空间。当可用空间有限时，NVS 具有保护机制以避免陷入 flash 页擦除的无限循环。检测到这种循环时，NVS 会返回没有更多可用空间。

对于 NVS，文件系统声明方式如下：

.. code-block:: c

        static struct nvs_fs fs = {
        .flash_device = NVS_FLASH_DEVICE,
        .sector_size = NVS_SECTOR_SIZE,
        .sector_count = NVS_SECTOR_COUNT,
        .offset = NVS_STORAGE_OFFSET,
        };

其中

- ``NVS_FLASH_DEVICE`` 是对将要使用的 flash 设备的引用。该设备必须处于可操作状态。
- ``NVS_SECTOR_SIZE`` 是扇区大小，它必须是 flash 擦除页大小的倍数，并且是 2 的幂。
- ``NVS_SECTOR_COUNT`` 是扇区数量，至少为 2；始终保留一个空扇区，以便复制现有数据。
- ``NVS_STORAGE_OFFSET`` 是 flash 中存储区域的偏移量。


Flash 磨损
**********

将数据写入 flash 时，研究 flash 磨损很重要。flash 的寿命有限，由 flash 可被擦除的次数决定。flash 一次擦除一页，页大小由硬件决定。例如，nRF51822 设备的页大小为 1024 字节，每页可以擦除约 20,000 次。

计算预期设备寿命
================

假设我们使用一个 4 字节的状态变量，它每分钟更改一次，并且需要在重启后恢复。NVS 定义的 sector_size 等于页大小（1024 字节），并且定义了 2 个扇区。

状态变量的每次写入需要 12 字节的 flash 存储：8 字节用于元数据，4 字节用于数据。存储数据时，第一个扇区将在 1024/12 = 85.33 分钟后存满。再过 85.33 分钟后，第二个扇区也会存满。此时，由于我们只使用两个扇区，第一个扇区将用于存储，并将在系统运行 171 分钟后被擦除。在预期设备寿命为 20,000 次写入的情况下，两个扇区每 171 分钟写入一次，设备应能持续约 171 * 20,000 分钟，即约 6.5 年。

更一般地，其中

- ``NS`` 为每分钟的存储请求数，
- ``DS`` 为数据大小（字节），
- ``SECTOR_SIZE`` 以字节为单位，并且
- ``PAGE_ERASES`` 为页可被擦除的次数，

预期设备寿命（以分钟为单位）可以按如下方式计算::

   SECTOR_COUNT * SECTOR_SIZE * PAGE_ERASES / (NS * (DS+8)) minutes

从该公式还可以清楚地看出，如果预期寿命太短应该怎么做：增大 ``SECTOR_COUNT`` 或 ``SECTOR_SIZE``。

Flash 写入块大小迁移
********************
在 DFU 过程中，NVS 使用的 flash 驱动可能会改变所支持的最小写入块大小。除非物理 ATE 大小发生变化，否则 NVS 的 flash 镜像将保持兼容。特别允许在 1、2、4、8 字节写入块大小之间迁移。

示例
****

``samples/subsys/kvss/nvs`` 中提供了如何使用 NVS 的示例。

故障排查
********

使用 NVS 时出现 MPU 故障，或返回 ``-ETIMEDOUT`` 错误
   NVS 可以使用 SoC 的内部 flash。启用 MPU 时，flash 驱动需要对 flash 存储器具有 MPU RWX 访问权限，这通过 :kconfig:option:`CONFIG_MPU_ALLOW_FLASH_WRITE` 配置。如果禁用该选项，当 NVS 应用引用内部 SoC flash 并且是唯一运行的线程时，将出现 MPU 故障。在多线程应用中，另一个线程可能会截获该故障，NVS API 将返回 ``-ETIMEDOUT`` 错误。


API 参考
********

NVS 子系统 API 由 ``nvs.h`` 提供：

.. doxygengroup:: nvs_data_structures

.. doxygengroup:: nvs_high_level_api

.. comment
   not documenting
   .. doxygengroup:: nvs
