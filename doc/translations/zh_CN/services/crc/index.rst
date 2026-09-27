.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _crc:

CRC
###

概述
****

CRC 子系统提供了各种循环冗余校验（Cyclic Redundancy Check）算法的软件实现，用于验证数据完整性。CRC 通常用于检测存储和通信系统中数据的意外变化。

该子系统提供了一套全面的 CRC 算法，包括 CRC-4、CRC-7、CRC-8、CRC-16、CRC-24 和 CRC-32 变体，并在硬件支持时提供可选的硬件加速支持。

.. note::
   此库不同于 :ref:`CRC 硬件驱动 API <crc_api>`，后者提供访问硬件 CRC 加速外设的接口。

   当硬件 CRC 单元可用，并且在 Devicetree 的 ``/chosen`` 节点中设置了 ``zephyr,crc`` 属性时，库函数将默认使用硬件加速来提升性能（可通过将 :kconfig:option:`CONFIG_CRC_HW_HANDLER` 设为 ``n`` 来禁用）。

用法
====

要计算 CRC，请包含相应的头文件并调用所需的函数：

.. code-block:: c

   #include <zephyr/sys/crc.h>

   uint8_t data[] = {0x01, 0x02, 0x03, 0x04};
   uint32_t checksum = crc32_ieee(data, sizeof(data));

对于分块处理的流式数据，请使用 “update” 变体：

.. code-block:: c

   uint32_t crc = 0;
   crc = crc32_ieee_update(crc, chunk1, len1);
   crc = crc32_ieee_update(crc, chunk2, len2);
   /* Final CRC value is in 'crc' */

通用的 :c:func:`crc_by_type` 函数提供了统一的接口，可在运行时选择 CRC 算法。

配置
****

相关配置选项：

* :kconfig:option:`CONFIG_CRC` - 启用 CRC 支持
* :kconfig:option:`CONFIG_CRC_HW_HANDLER` - 启用硬件 CRC 加速
* :kconfig:option:`CONFIG_CRC_SHELL` - 启用 CRC shell 命令
* :kconfig:option-regex:`CONFIG_CRC[0-9].*` - 启用特定 CRC 算法的软件实现

API 参考
********

.. doxygengroup:: crc
