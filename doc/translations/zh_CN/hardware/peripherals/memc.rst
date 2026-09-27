.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _memc_api:

存储器控制器（MEMC）
####################

概述
****

MEMC API 提供了访问 PSRAM 和 NOR 型存储器等外部存储设备的通用接口。它支持两种访问模式：

- **内存映射：** 控制器通过 CPU 可直接访问的地址窗口暴露设备。驱动可以实现 :c:member:`memc_driver_api.get_mem_base` 来提供映射基地址，使 :c:func:`memc_read` 和 :c:func:`memc_write` 自动使用 ``memcpy``。此外，如果硬件以透明方式映射内存，驱动也可以完全不提供运行时 API，此时上层使用平台特定的基地址直接访问设备。

- **总线事务：** 控制器为每次传输发出显式总线命令（例如 MSPI 命令）。驱动实现 :c:member:`memc_driver_api.read` 和 :c:member:`memc_driver_api.write`。此模式用于控制器没有内存映射窗口的情况。

:c:func:`memc_read` 和 :c:func:`memc_write` 在内存映射访问路径可用时自动选择该路径，否则回退到总线事务。

此外，还提供了用于查询设备自身信息的可选 API：:c:func:`memc_get_size` 返回设备容量，:c:func:`memc_read_id` 返回设备标识字节。

旧版（仅初始化）驱动
********************

将 ``NULL`` 作为 API 指针传给 ``DEVICE_DT_INST_DEFINE`` 的现有 memc 驱动不受此 API 的影响。调用方应在调用任何 memc 函数之前，使用 :c:macro:`DEVICE_API_IS` 检查设备是否实现了 memc 接口：

.. code-block:: c

   if (DEVICE_API_IS(memc, dev)) {
      memc_read(dev, offset, buf, sizeof(buf));
   } else {
      /* Legacy init-only driver - device is memory-mapped.
       * Access via platform-specific base address.
       */
      memcpy(buf, (const uint8_t *)MEMC_BASE + offset, sizeof(buf));
   }

在未实现 memc API 的设备上调用 :c:func:`memc_read` 或 :c:func:`memc_write` 会返回 ``-ENOTSUP``。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_MEMC`
* :kconfig:option:`CONFIG_MEMC_INIT_PRIORITY`

API 参考
********

.. doxygengroup:: memc_interface
