.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _flash_map_api:

Flash 映射
##########

``<zephyr/storage/flash_map.h>`` API 允许通过 :c:struct:`flash_area` 结构访问有关设备 flash 分区的信息。

每个 :c:struct:`flash_area` 描述一个 flash 分区。该 API 提供对“flash 映射”的访问，其中包含可通过全局唯一 ID 号访问的预定义 flash 区域。映射根据 DTS 文件中的 “fixed-partitions” 和 “zephyr,mapped-partition” compatible 条目创建。用户还可以在运行时为特定于应用的目的创建 :c:struct:`flash_area` 对象。

本文档在指代单个“fixed-partitions”或“zephyr,mapped-partition”实体时使用“flash 区域”一词。

:c:struct:`flash_area` 包含一个指向 :c:struct:`device` 的指针，该指针可用于直接通过 :ref:`flash API <flash_api>` 访问该区域所在的 flash 设备。每个 flash 区域由其所在的设备、相对于设备起始位置的偏移量以及设备上的大小来表征。:c:func:`flash_area_open` 函数使用一个额外的标识符参数在 flash 映射中查找 flash 区域。

flash_map.h API 提供用于操作 :c:struct:`flash_area` 的函数。主要示例是 :c:func:`flash_area_read` 和 :c:func:`flash_area_write`。这些函数基本上是 flash API 的封装，并增加了偏移量和大小检查，以将 flash 操作限制在预定义区域内。

大多数 ``<zephyr/storage/flash_map.h>`` API 函数都需要一个 :c:struct:`flash_area` 对象指针，用于表征它们将操作的 flash 区域。获取此类指针有两种可能的方法：

 * 使用 :c:func:`flash_area_open` 获取；

 * 定义一个 :c:struct:`flash_area` 类型的对象，这需要提供一个有效的 :c:struct:`device` 对象指针，以及 flash 设备内该区域的偏移量和大小。

:c:func:`flash_area_open` 使用数字标识符在 flash 映射中搜索 :c:struct:`flash_area` 对象，如果找到，则返回指向表示具有给定 ID 的区域的对象的指针。flash 区域的 ID 号可以从 “fixed-partitions” 或 “zephyr,mapped-partition” DTS 节点标签使用 :c:macro:`PARTITION_ID()` 获得；这些标签从 devicetree 获取，如下所述。

与 devicetree 的关系
********************

flash_map.h API 使用从 :ref:`devicetree_api` 生成的数据，特别是其 :ref:`devicetree-flash-api`。Zephyr 还为通过 MCUboot 引导加载程序进行的 :ref:`dfu` 提供了一些分区约定，并定义了可供 :ref:`file systems <file_system_api>` 或其他非易失性 :ref:`storage <storage_services>` 使用的分区。

以下示例 devicetree 片段对 MCUboot 和存储分区均使用固定 flash 分区。为清晰起见，省略了一些细节。

.. literalinclude:: example_fragment.dts
   :language: DTS
   :start-after: start-after-here

分区偏移量应相对于该分区所属的 flash 存储器起始地址来表示。

``boot_partition``、``slot0_partition``、``slot1_partition`` 和 ``scratch_partition`` 节点标签是为 MCUboot 定义的，但并非所有 MCUboot 配置都要求定义所有这些标签。有关更多详细信息，请参阅 `MCUboot documentation`_。

``storage_partition`` 节点定义为供文件系统或其他非易失性存储 API 使用。

.. _MCUboot documentation: https://docs.mcuboot.com

通过将 DTS 节点标签传递给 :c:macro:`PARTITION_ID()` 可获得数字 flash 区域 ID；例如，要获得 ``slot0_partition`` 的 ID 号，用户可以调用 ``PARTITION_ID(slot0_partition)``。

所有 :code:`PARTITION_*` 宏都将 DTS 节点标签作为分区标识符。

如果某个区域在 DTS 文件中定义，用户不必使用 :c:func:`flash_map_open` 获取 :c:struct:`flash_area` 对象指针来获取 flash 区域大小、偏移量或设备信息。知道某个区域的 DTS 节点标签后，用户可以分别使用 :c:macro:`PARTITION_OFFSET()`、:c:macro:`PARTITION_SIZE()` 或 :c:macro:`PARTITION_DEVICE()` 直接从 DTS 节点定义中获取这些信息。例如，要获取 ``storage_partition`` 的偏移量，只需调用 ``PARTITION_OFFSET(storage_partition)``。

以下示例展示如何使用 :c:func:`flash_area_open` 和 DTS 节点标签获取 :c:struct:`flash_area` 对象指针：

.. code-block:: c

   const struct flash_area *my_area;
   int err = flash_area_open(PARTITION_ID(slot0_partition), &my_area);

   if (err != 0) {
        handle_the_error(err);
   } else {
        flash_area_read(my_area, ...);
   }

API 参考
********

.. doxygengroup:: flash_area_api
