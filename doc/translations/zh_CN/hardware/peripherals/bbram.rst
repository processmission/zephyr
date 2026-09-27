.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bbram_api:

电池备份 RAM（BBRAM）
#####################

BBRAM API 可用于访问此内存区域的特有属性。通过此 API，可以轻松访问以下常见的 BBRAM 属性：

- IBBR（无效）状态——检查 BBRAM 是否完好无损。
- VSBY（待机电压）状态——检查 BBRAM 是否使用待机电压供电。
- VCC（工作电源）状态——检查 BBRAM 是否使用正常电源供电。
- 大小——获取 BBRAM 区域的大小（以字节为单位）。

除此之外，API 还提供了访问此内存区域的方法，分别通过 :c:func:`bbram_read` 和 :c:func:`bbram_write` 进行读取和写入。这两个函数应仅在 BBRAM 处于有效状态且操作未超出此内存区域的边界时成功。

API 参考
********

.. doxygengroup:: bbram_interface
