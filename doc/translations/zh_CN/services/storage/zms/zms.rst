.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _zms_api:

Zephyr 内存存储（ZMS）
######################

Zephyr 内存存储是一种新的键值存储系统，设计用于支持所有类型的非易失性存储技术。它支持经典的片上 NOR flash，以及 RRAM、MRAM 等完全不需要单独擦除操作的新技术；也就是说，这类设备上的数据可以随时直接覆盖。

一般行为
********

ZMS 将存储空间划分为扇区（至少 2 个），每个扇区会填充键值对，直到填满为止。

键值对分为两部分：

- 键部分写入称为 “ID-ATE” 的 ATE（分配表项）中，该 ATE 从扇区底部开始存储。
- 值部分定义为 “data”，并从扇区顶部开始以原始形式存储。

此外，对于每个扇区，我们在最后几个位置存储头 ATE；这些 ATE 用于描述扇区状态（已关闭、打开）以及当前的 ZMS 版本。

当前扇区已满时，我们首先验证下一个扇区为空；然后通过将有效 ATE 移动到第 N+1 个空扇区来对第 N+2 个扇区（其中 N 是当前扇区编号）进行垃圾回收，擦除已回收的扇区，然后通过写入 garbage_collect_done ATE 和 close ATE（头条目之一）来关闭当前扇区。之后，我们前进到下一个扇区并重新开始写入条目。

此行为会重复，直到到达分区末尾。然后，在对第一个扇区进行垃圾回收并擦除其内容后，从该扇区重新开始。

扇区的组成
==========

扇区按以下形式组织（以 3 个扇区为例）：

.. list-table::
   :widths: 25 25 25
   :header-rows: 1

   * - 扇区 0（已关闭）
     - 扇区 1（打开）
     - 扇区 2（空）
   * - Data_a0
     - Data_b0
     - Data_c0
   * - Data_a1
     - Data_b1
     - Data_c1
   * - Data_a2
     - Data_b2
     - Data_c2
   * - GC_done
     -    .
     -    .
   * -    .
     -    .
     -    .
   * -    .
     -    .
     -    .
   * -    .
     - ID ATE_b2
     - ID ATE_c2
   * - ID ATE_a2
     - ID ATE_b1
     - ID ATE_c1
   * - ID ATE_a1
     - ID ATE_b0
     - ID ATE_c0
   * - ID ATE_a0
     - GC_done ATE
     - GC_done ATE
   * - Close ATE (cyc=1)
     - Close ATE (cyc=1)
     - Close ATE (cyc=1)
   * - Empty ATE (cyc=1)
     - Empty ATE (cyc=2)
     - Empty ATE (cyc=2)

扇区中每个元素的定义
====================

擦除扇区时会写入 ``Empty ATE`` （位于扇区的最后一个位置）。

关闭扇区时会写入 ``Close ATE`` （位于扇区的倒数第二个位置）。

写入 ``GC_done ATE`` 以指示下一个扇区已经过垃圾回收。此 ATE 可以位于扇区的任意位置。

``ID ATE`` 包含一个 :c:type:`zms_id_t` 类型的键，并描述数据的存储位置、大小及其 CRC32。

``Data`` 是与 ID-ATE 关联的实际值。

ZMS 如何工作？
**************

挂载存储系统
============

挂载存储系统首先要获取 flash 参数，检查文件系统属性是否正确（sector_size、sector_count 等），然后调用 zms_init 函数使存储就绪。

默认情况下，如果无法挂载分区，:c:func:`zms_mount` 会返回错误。对于面向恢复的用例，可以使用 :c:func:`zms_mount_force`，在首次挂载尝试失败时自动擦除并重新初始化分区。

挂载标志
--------

可以使用 ``zms_fs.mount_flags`` 中的可选标志控制 ZMS 的挂载行为。

- 默认行为（未设置可选标志，``mount_flags = 0``）：如果分区已擦除且未找到有效的 ZMS 头，:c:func:`zms_mount` 会通过创建初始 ZMS 头来格式化分区。
- ``ZMS_MOUNT_FLAG_NO_FORMAT``：如果分区已擦除且未找到有效的 ZMS 头，:c:func:`zms_mount` 不会格式化分区，并返回 ``-ENOTSUP``。

要挂载文件系统，必须初始化 :c:struct:`zms_fs` 结构中的以下元素：

.. code-block:: c

        struct zms_fs {
                /** File system offset in flash **/
                off_t offset;

                /** Storage system is split into sectors, each sector size must be multiple of
                 * erase-blocks if the device has erase capabilities
                 */
                uint32_t sector_size;
                /** Number of sectors in the file system */
                uint32_t sector_count;

                /** Optional mount behavior flags (enum zms_mount_flags) */
                uint32_t mount_flags;

                /** Flash device runtime structure */
                const struct device *flash_device;
        };

初始化
======

由于 ZMS 具有快进写入机制，它必须找到上次停止时所处条目的最后一个扇区和最后一个指针。它必须查找一个已关闭扇区后面跟着一个打开扇区，然后在打开扇区内找到（恢复）最后写入的 ATE。之后，它检查此扇区之后的扇区是否为空，否则将其擦除。

ZMS ID/数据写入
===============

为避免用相同的 ID 重写相同的数据，ZMS 必须检查所有扇区中是否存在相同的 ID，然后比较其数据。如果数据相同，则不执行写入。如果必须执行写入，则在该扇区中写入一个 ATE 和数据（如果操作不是删除）。如果扇区已满（无法容纳当前数据 + ATE），ZMS 必须移动到下一个扇区，对新打开的扇区之后的扇区进行垃圾回收，然后将其擦除。

ZMS ID/数据读取（带历史记录）
=============================

默认情况下，ZMS 会从最新到最旧浏览所有已存储的 ATE，以查找具有相同 ID 的最后一条数据。如果找到 ID 匹配的有效 ATE，则检索其数据并返回读取的字节数。如果提供了历史计数且不为 0，则会检索具有相同 ID 的更旧数据。

ZMS 条目枚举（迭代器 API）
==========================

应用无需提供预定义的 ID 列表即可枚举已存储的条目。当 ID 派生自有效载荷数据（例如打包的地址），并且应用未在 flash 中保留单独索引时，这很有用。

这组 API 通常在启动时使用，此时应用会根据持久化在 ZMS 中的 ID/长度元数据重建其内存状态。

迭代器 API 包括：

- :c:func:`zms_iter_init` 用于初始化迭代器状态。
- :c:func:`zms_iter_init_with_config` 用于初始化迭代器状态，并可选使用 ID 掩码、包含边界 ID 范围和谓词过滤器。
- :c:func:`zms_iter_next` 用于一次检索一个活动条目（唯一 ID）。
- :c:func:`zms_iter_next_all` 用于检索所有匹配条目（完整历史记录，包括删除标记）。

在 :c:func:`zms_iter_next` 和 :c:func:`zms_iter_next_all` 之间选择
------------------------------------------------------------------

- :c:func:`zms_iter_next` 返回唯一的活动 ``(id, len)`` 对：

  - 扇区/头条目会被跳过。
  - 删除标记（``len == 0`` 的条目）会被跳过。
  - 如果同一 ID 在存储历史中出现多次，则仅返回最新的有效实例。
  - 为保证唯一性，ZMS 会检查每个候选 ID 是否有更新的条目，这可能需要额外的扫描。

- :c:func:`zms_iter_next_all` 更快，并会在遇到时返回所有匹配的 ``(id, len)`` 对：

  - 返回同一 ID 的历史条目。
  - 返回删除标记（``len == 0`` 的条目）。
  - 不执行唯一性过滤。
  - 应用负责根据自身策略对返回的对进行过滤/压缩。

  当你只想枚举匹配位掩码、特定包含边界 ID 范围、谓词回调或这些过滤器任意组合的 ID 时，请使用 :c:func:`zms_iter_init_with_config`。

迭代器返回值
------------

调用 :c:func:`zms_iter_next` 或 :c:func:`zms_iter_next_all` 会返回：

- 找到条目时返回 ``1``；输出参数包含 ID 和数据长度。
- 没有更多条目可枚举时返回 ``0``。
- 出错时返回负 errno（例如 ``-EINVAL``、``-EIO``、``-ENXIO``）。

迭代器始终报告元数据（ID 和长度）。此外，当调用者提供非 NULL 的 ``data`` 缓冲区时，迭代器还会将条目内容直接复制到其中，但仅适用于小到可以存储在 ATE 内部的条目。对于较大的条目，或未提供缓冲区时，必须显式使用 :c:func:`zms_read` 读取最新值，或使用 :c:func:`zms_read_hist` 读取更旧的修订版本。

.. _zms_iterator_concurrency:

并发与快照行为
--------------

调用 :c:func:`zms_iter_init` 时，迭代器会捕获一个遍历边界。初始化之后写入的条目不在此次遍历范围内。

不要在两次迭代器步进调用（:c:func:`zms_iter_next` 或 :c:func:`zms_iter_next_all`）之间对同一个 :c:struct:`zms_fs` 调用 :c:func:`zms_write` （包括删除操作）。如果写入在迭代期间触发垃圾回收，则迭代器行为未定义。无论是否加锁，此规则都适用于执行迭代的线程：获取下文所述的锁只会阻止 *其他* 线程在遍历期间写入。

锁定并阻止并发写入者
--------------------

:c:struct:`zms_fs` 将其内部写锁公开为普通的 ``struct k_mutex zms_lock`` 字段。:c:func:`zms_write` 和 :c:func:`zms_delete` 会在写入期间在内部获取此互斥锁。具有多个线程且共享同一 :c:struct:`zms_fs` 的应用可以在整个迭代期间持有同一互斥锁，从而在遍历边界必须保持有效的期间阻止 *其他* 线程写入：

.. code-block:: c

  k_mutex_lock(&fs.zms_lock, K_FOREVER);

  rc = zms_iter_init(&fs, &iter);
  /* ... */

  while ((rc = zms_iter_next(&fs, &iter, &id, &len, NULL, 0)) == 1) {
    /* ... */
  }

  k_mutex_unlock(&fs.zms_lock);

用法示例
--------

.. code-block:: c

  struct zms_iter iter;
  bool predicate_id_not_2(zms_id_t id)
  {
    return id != (zms_id_t)2;
  }

  struct zms_iter_config iter_config = {
    .mask_id = (zms_id_t)0x03,
    .min_id = (zms_id_t)0x01,
    .max_id = (zms_id_t)0x03,
    .use_mask = true,
    .use_range = true,
    .use_predicate = true,
    .predicate_func = predicate_id_not_2,
  };
  zms_id_t id;
  size_t len;
  uint8_t data[ZMS_DATA_IN_ATE_SIZE];
  int rc;

  /* Block writes from other threads for the duration of the traversal. */
  k_mutex_lock(&fs.zms_lock, K_FOREVER);

  rc = zms_iter_init_with_config(&fs, &iter, &iter_config);
  if (rc) {
    /* handle error */
  }

  while ((rc = zms_iter_next(&fs, &iter, &id, &len, data, sizeof(data))) == 1) {
    /* id: entry ID matching configured mask/range/predicate, len: current stored size */
    /* data: filled with the entry's content when it is small enough to be
     * stored directly inside the ATE; otherwise left untouched, in which case
     * zms_read() must be used to fetch it.
     */
    printk("id=0x%llx len=%zu\n", (unsigned long long)id, len);
  }

  k_mutex_unlock(&fs.zms_lock);

  if (rc < 0) {
    /* handle iterator error */
  }

当只需要 ``(id, len)`` 对时，可选的 ``data``/``data_len`` 参数可以设置为 ``NULL``/``0``。提供缓冲区时，只会复制 ZMS 直接存储在 ATE 内的数据；较大的条目仍必须使用 :c:func:`zms_read` 检索。

将 :c:struct:`zms_iter_config` 零初始化，或将 ``use_mask``、``use_range`` 和 ``use_predicate`` 保持禁用，以保留默认行为：接受所有 ID 和完整的 ``zms_id_t`` 范围。

要确定迭代器返回的某个 ID 存在多少个修订版本，请使用递增的 ``cnt`` 调用 :c:func:`zms_read_hist`，直到返回 ``-ENOENT``。

ZMS 可用空间计算
================

ZMS 还可以返回分区中剩余的可用空间。但是，此操作非常耗时，因为它需要浏览分区所有扇区中的所有有效 ATE，并且对于每个有效 ATE，尝试查找是否存在更旧的 ATE。不建议应用经常使用此函数，因为它耗时且可能拖慢调用线程。

周期计数器
==========

每个扇区都有一个主导周期计数器，它是一个 ``uint8_t``，用于验证所有其他 ATE。主导周期计数器存储在 empty ATE 中。ATE 要变为有效，其周期计数器必须与 empty ATE 中存储的相同。每次将 ATE 从一个扇区移动到另一个扇区时，它必须获取目标扇区的周期计数器。要擦除扇区，会递增 empty ATE 的周期计数器，并只写入一次 empty ATE。该扇区中的所有 ATE 都会失效。

关闭扇区
========

要关闭扇区，会在扇区末尾添加一个 close ATE，并且它必须与 empty ATE 具有相同的周期计数器。关闭扇区时，所有未使用的剩余空间都会填充垃圾数据，以避免存在周期计数器有效的旧 ATE。

触发垃圾回收
============

某些应用需要确保存储写入具有定义的最大延迟。调用 ZMS 执行写入时，当前扇区可能几乎已满，以至于 ZMS 需要触发 GC 才能切换到下一个扇区。此操作耗时，并会导致某些应用无法满足其实时约束。ZMS 增加了一个 API，使应用可以获取扇区中当前剩余的可用空间。如果当前扇区几乎已满，应用随后可以决定何时切换到下一个扇区。这当然会触发下一个扇区的垃圾回收操作。这将向应用保证下一次写入不会触发垃圾回收。

ATE（分配表项）结构
===================

每个条目使用 16 字节来编码其信息。确切结构由 ATE 格式决定，可针对给定应用选择 ATE 格式。

ZMS 定义了多种针对不同特性集定制的 ATE 格式。运行时，它使用 empty ATE 中的 metadata 字段识别格式，该字段在所有格式中具有相同的字节位置。

.. table:: 32 位 ID 的条目格式

   +-------+------------+----+----+----+----+----+----+----+----+-----+-----+-----+-----+-----+-----+
   | 0     | 1          | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10  | 11  | 12  | 13  | 14  | 15  |
   +=======+============+====+====+====+====+====+====+====+====+=====+=====+=====+=====+=====+=====+
   | crc8  | cycle_cnt  | len     | id                | data (if len <= 8)                          |
   |       |            |         |                   +---------------------+-----------------------+
   |       |            |         |                   | offset              | data_crc              |
   |       |            |         |                   |                     +-----------------------+
   |       |            |         |                   |                     | metadata              |
   +-------+------------+---------+-------------------+---------------------+-----------------------+

这是 :c:struct:`zms_ate` 的 API 文档中记录的默认格式。``data_crc`` 可选包含在内，用于对存储在扇区顶部的数据进行完整性检查。

.. note:: 仅在完整读取数据时才会检查数据的 CRC。部分读取不会检查数据的 CRC，因为它是针对整个元素计算的。

.. warning:: 在以前未启用 CRC 功能的现有 ZMS 内容上启用该功能，将使所有现有数据失效。

.. table:: 64 位 ID 的条目格式

   +-------+------------+----+----+----+----+----+----+----+----+-----+-----+------+------+------+------+
   | 0     | 1          | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10  | 11  | 12   | 13   | 14   | 15   |
   +=======+============+====+====+====+====+====+====+====+====+=====+=====+======+======+======+======+
   | crc8  | cycle_cnt  | len     | id                                      | data (if len <= 4)        |
   |       |            |         |                                         +---------------------------+
   |       |            |         |                                         | offset                    |
   |       |            |         |                                         +---------------------------+
   |       |            |         |                                         | metadata                  |
   +-------+------------+---------+-----------------------------------------+---------------------------+

启用 :kconfig:option:`CONFIG_ZMS_ID_64BIT` 时选择此格式。

.. warning:: 选择与现有 ZMS 内容所使用的 ATE 格式不同的格式，将使所有现有数据失效。

.. note:: 用于 :ref:`设置 <settings_api>` 的 ZMS 后端不支持此格式。

用户数据（键值对）的可用空间
****************************

ZMS 始终需要一个空扇区才能执行垃圾回收（GC）。因此，假设一个分区中存在 4 个扇区，ZMS 将只使用 3 个扇区存储键值对，并保留一个空扇区以执行 GC。该空扇区将在分区的 4 个扇区之间轮换。

.. note:: 一次写入扇区的单个数据最大长度为 64K（这可能会在未来的 ZMS 版本中改变）。

小数据值
========

足够小的值将存储在条目（ATE）本身内，而不会将数据写入扇区顶部。条目内可容纳的数据量取决于所选格式。请参见 `ATE structure <#ate-allocation-table-entry-structure>`_ 一节。

ZMS 的条目大小为 16 字节，这意味着在此场景下，分区中可用于存储数据的最大空间计算如下：

.. math::

   \small\frac{(NUM\_SECTORS - 1) \times (SECTOR\_SIZE - (5 \times ATE\_SIZE)) \times (DATA\_SIZE)}{ATE\_SIZE}

位置：

``NUM_SECTOR``：扇区总数

``SECTOR_SIZE``：扇区大小

``ATE_SIZE``：16 字节

``(5 * ATE_SIZE)``：为头条目和删除项保留的 ATE

``DATA_SIZE``：8 字节或 4 字节，取决于 ATE 格式

例如，对于 4 个 1024 字节的扇区，使用默认 ATE 格式时，8 字节长度数据的可用空间为 :math:`\frac{3 \times 944 \times 8}{16} = 1416 \, \text{ bytes}`。

大数据值
========

超过 ``DATA_SIZE`` 的值存储在 ATE 之外、扇区顶部。在这种情况下，很难估计可用空间，因为这取决于数据大小。但我们可以考虑到，对于添加到扇区顶部的 N 字节数据，必须在扇区底部额外添加 16 字节的 ATE，因此键值对总共占用 :math:`N + 16` 字节。

让我们看一个示例：

对于一个具有 4 个 1024 字节扇区且数据大小为 64 字节的分区。只有 3 个扇区可用于写入，每个扇区容量为 944 字节，因此每个扇区可以存储 11 个键值对（:math:`\frac{944}{64 + 16}`）。在这种情况下，此分区总共可以存储的数据为 :math:`11 \times 3 \times 64 = 2112 \text{ bytes}`。

.. only:: html

  .. raw:: html
     :file: zms-calculator-common.html

.. _zms_available_space_calculator:

可用空间计算器
==============

.. only:: html

  .. raw:: html
     :file: available-space-calculator.html

磨损均衡
********

该存储系统针对不需要擦除的设备进行了优化。依赖擦除值的存储系统（例如 NVS）需要使用写操作来模拟擦除。这会导致这些设备的预期寿命显著缩短，并且会增加写操作延迟以及设备为空时的初始化延迟。ZMS 使用周期计数机制，避免为这些设备模拟擦除操作。它还保证在扇区写入的每个周期内，每个内存位置只写入一次。

例如，在不需要擦除操作的设备上使用 NVS 擦除 4096 字节扇区时，必须执行 256 次 flash 写入（假设 ``write-block-size`` = 16 字节），而使用 ZMS 只需 1 次 16 字节写入。在这种情况下，此操作快 256 倍。

垃圾回收操作还会缩短存储单元寿命，因为它在将块从一个扇区移动到另一个扇区时会执行写操作。为使垃圾回收器不影响设备寿命，建议适当确定分区大小。分区大小应为可能写入存储的数据（包括头部）最大大小的两倍。

请参见 `用户数据可用空间 <#available-space-for-user-data-key-value-pairs>`_。

设备寿命计算
============

存储设备无论是传统 flash 还是 RRAM/MRAM 等新技术，其寿命都是有限的，由存储单元可擦除/写入的次数决定。Flash 设备作为其功能行为的一部分，一次擦除一页（否则无法覆盖存储单元）；而对于不需要擦除操作的存储设备，存储单元可以直接覆盖。

这里展示一个典型场景，用于计算设备寿命：假设我们使用相同的 ID 存储一个 4 字节变量，但其内容每分钟变化一次。分区有 4 个扇区，每个扇区 1024 字节。每次写入该变量需要 16 字节存储。由于每个扇区有 944 字节可用于 ATE，且 ZMS 是快进式存储系统，我们将在 :math:`\frac{(944 \times 4)}{16} = 236 \text{ minutes}` 后重写第一个扇区的第一个位置。

除正常写入外，垃圾回收器还会将仍然有效的数据从旧扇区移动到新扇区。由于我们使用相同的 ID 且分区较大，在这种情况下垃圾回收器不会移动任何数据。对于可写入 20 000 次的存储设备，存储将持续约 4 720 000 分钟（约 9 年）。

为了得出更通用的公式，我们必须先计算典型数据集在 ZMS 中实际使用的大小。对于使用 `小数据值 <#small-data-values>`_ 的 ID/数据对，``effective_size`` 为 ``16`` 字节；而对于使用 `大数据值 <#large-data-values>`_ 的 ID/数据对，``effective_size`` 为 ``16 + sizeof(data)`` 字节。假设 ``total_effective_size`` 是写入存储的数据总大小，并且分区大小适当（有效大小的两倍），以避免垃圾回收器不断移动块。

设备的预期寿命（以分钟为单位）计算如下：

.. math::

   \small\frac{(SECTOR\_EFFECTIVE\_SIZE \times SECTOR\_NUMBER \times MAX\_NUM\_WRITES)}{(TOTAL\_EFFECTIVE\_SIZE \times WR\_MIN)}

位置：

``SECTOR_EFFECTIVE_SIZE``：扇区大小减去头大小（80 字节）

``SECTOR_NUMBER``：扇区数量

``MAX_NUM_WRITES``：存储设备的预期寿命（以写入次数计）

``TOTAL_EFFECTIVE_SIZE``：所写入数据集的总有效大小

``WR_MIN``：每分钟对数据集执行的写入次数

.. _zms_device_lifetime_calculator:

设备寿命计算器
==============

.. only:: html

  .. raw:: html
     :file: device-lifetime-calculator.html

功能
****

与 NVS 等现有存储系统相比，ZMS 引入了许多功能，并将从其初始版本不断演进，以包含更多满足新技术需求（例如低延迟和更大存储空间）的功能。

现有功能
========

版本 1
------

- 支持不需要擦除操作的存储设备（只需一次写操作即可使扇区失效）
- 支持大分区和大扇区大小（64 位地址空间）
- 支持 32 位 ID 和 64 位 ID
- 小数据值存储在 ATE 本身中
- 内置数据 CRC32（包含在 ATE 中）
- ZMS 版本管理（用于处理未来演进）
- 支持较大的 ``write-block-size`` （仅适用于需要它的平台）
- 支持多种 ATE 格式，以满足不同应用的需求
- 支持通过 :c:func:`zms_mount_force` 进行强制挂载恢复（挂载失败时自动擦除并重新初始化分区）
- 支持查找缓存以加速重复的 ID 查找，并提供可选的每实例缓存配置，以便基于每个分区自定义缓存大小
- 支持通过 :c:func:`zms_iter_init` 和 :c:func:`zms_iter_next` 枚举活动条目，而无需预声明 ID 列表

未来功能
========

- 增加挂载具有不同 ATE 格式的多个文件系统的可能性（当前，同一应用中的所有文件系统必须使用相同格式）
- 增加在某些应用场景中跳过垃圾回收器的可能性，这些场景中 ID/值对会定期写入且不超过分区大小的一半（始终存在具有相同 ID 的旧条目）。
- 将 ID 划分为命名空间，并根据应用需求分配 ID，以处理不同子系统或示例所使用的 ID 之间的冲突。
- 增加根据周期计数值检索设备磨损值的可能性
- 增加一个恢复函数，可在出现问题时恢复存储分区
- 增加一个库/应用，以支持从 NVS 条目迁移到 ZMS 条目

ZMS 与 Zephyr 中的其他存储系统
==============================

本节在 Zephyr 存储系统（不是完整文件系统，而是更简单的非分层系统）的更广泛背景下介绍 ZMS。如今 Zephyr 至少还包括两个在范围和功能上具有一定可比性的其他系统：:ref:`NVS <nvs_api>` 和 :ref:`FCB <fcb_api>`。在应用中使用哪一个取决于你的需求和所使用的硬件，本节提供的信息有助于做出选择。

- 如果你使用的是 RRAM 或 MRAM 等不需要擦除操作的设备，:ref:`ZMS <zms_api>` 绝对是存储子系统的最佳选择，因为它设计用于避免在这些设备上使用大块写入来模拟擦除操作，并用单次写入调用取而代之。
- 对于具有较大 ``write_block_size`` 和/或需要不同于传统 flash 页大小（等于 erase_block_size）的扇区大小的设备，:ref:`ZMS <zms_api>` 也是最佳选择，因为可以自定义这些参数并在 ZMS 中添加对这些设备的支持。
- 对于传统 flash 技术设备，推荐使用 :ref:`NVS <nvs_api>`，因为它占用空间小（ATE 更小，头 ATE 也更小）。与 ZMS 相比，NVS 中的 flash 擦除也非常快，并且不需要额外的写操作。对于这些设备，NVS 的读取/写入也会比 ZMS 更快，因为其 ATE 大小更小。
- 如果你的应用需要超过 64K 个 ID 用于存储，这里推荐 :ref:`ZMS <zms_api>`，因为其 ID 字段最多为 64 位。
- 如果你的应用以 FIFO 模式（先进先出）工作，那么 :ref:`FCB <fcb_api>` 是该用例的最佳存储解决方案。

更一般地说，为了在 NVS 和 ZMS 之间做出正确选择，应首先验证所有阻塞因素，以确保应用可以使用其中一个子系统；然后，如果两种解决方案都可以实现，最佳选择应基于本节所述设备寿命的计算：`磨损均衡 <#wear-leveling>`_。

提高性能的建议
**************

扇区大小和数量
==============

- 应适当设置存储分区的总大小，以获得 ZMS 的最佳性能。有关 ZMS 中实际可用空间的所有信息都可以在文档中找到。请参见 `用户数据可用空间 <#available-space-for-user-data-key-value-pairs>`_。建议选择写入存储的键值对大小的两倍作为存储分区大小。
- 需要设置扇区大小，使一个扇区能够容纳将要存储的最大数据大小。增大扇区大小会减慢垃圾回收操作，并使其发生频率降低。相反，减小扇区大小会使垃圾回收操作更快，但也会使其发生更频繁。
- 对于 :ref:`设置 <settings_api>` 等某些子系统，所有路径-值对都会拆分为两个 ZMS 条目（ATE）。在计算所需存储空间时，应考虑这两个条目所需的头。
- 使用 `小数据值 <#small-data-values>`_ 可以提高性能，因为这些数据写入条目内部。例如，对于 :ref:`设置 <settings_api>` 子系统，选择小于或等于 8 字节的路径名可以使读取和写入更快。

缓存大小
========

- 直接使用 ZMS API 时，建议将缓存大小至少设置为将要写入存储的不同条目数量。
- 每个额外的缓存条目都会使 RAM 使用量增加 8 字节。应仔细选择缓存大小。
- 如果通过 :ref:`设置 <settings_api>` 使用 ZMS，必须考虑到每个设置条目都会拆分为两个 ZMS 条目。建议将缓存大小至少设置为设置条目数量的两倍。

手动配置每实例缓存
==================

启用 :kconfig:option:`CONFIG_ZMS_LOOKUP_CACHE_MANUAL` 时，每个 :c:struct:`zms_fs` 实例可以提供自己的查找缓存缓冲区，而不使用全局 :kconfig:option:`CONFIG_ZMS_LOOKUP_CACHE_SIZE` 设置。

在 :c:func:`zms_mount` 之前调用 :c:func:`zms_set_lookup_cache`，为该实例分配缓存缓冲区。如果未分配缓冲区，则该 :c:struct:`zms_fs` 实例的查找缓存保持禁用。

.. code-block:: c

        static struct zms_fs zms_a;
        static struct zms_fs zms_b;
        static uint64_t zms_a_cache[512];
        static uint64_t zms_b_cache[32];

        zms_set_lookup_cache(&zms_a, zms_a_cache, ARRAY_SIZE(zms_a_cache));
        zms_set_lookup_cache(&zms_b, zms_b_cache, ARRAY_SIZE(zms_b_cache));

ID 大小
=======

- 对于大多数应用而言，64 位 ID 空间预计会比所需更大。除非你有特定需求，否则建议继续使用 32 位 ID。这预计会对代码大小和性能产生轻微影响，即使在 64 位系统上也是如此，因为存储中 ID 的字节位置未对齐到 8 字节边界。

API 参考
********

ZMS API 由 ``zms.h`` 提供：

.. doxygengroup:: zms_data_structures

.. doxygengroup:: zms_high_level_api

.. comment
   not documenting .. doxygengroup:: zms
