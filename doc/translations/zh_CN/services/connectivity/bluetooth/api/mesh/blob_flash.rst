.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_blob_flash:

BLOB 闪存
#########

BLOB 闪存读取器和写入器实现了对 :ref:`闪存映射 <flash_map_api>` 中定义的闪存分区进行 BLOB 读取和写入的功能。


BLOB 闪存读取器
***************

BLOB 闪存读取器与 BLOB 传输客户端交互，直接从闪存读取 BLOB 数据。在将其传递给 BLOB 传输客户端之前，必须调用 :c:func:`bt_mesh_blob_flash_rd_init` 进行初始化。每个 BLOB 闪存读取器一次只支持一个传输。


BLOB 闪存写入器
***************

BLOB 闪存写入器与 BLOB 传输服务器交互，将 BLOB 数据直接写入闪存。在将其传递给 BLOB 传输服务器之前，必须调用 :c:func:`bt_mesh_blob_flash_rd_init` 进行初始化。每个 BLOB 闪存写入器一次只支持一个传输，并且要求块大小是闪存页大小的倍数。如果启动传输时使用的块大小小于闪存页大小，则该传输将被拒绝。

BLOB 闪存写入器将分块数据复制到缓冲区中，以处理与闪存写入块大小不对齐的分块。如果分块的起始位置或长度不对齐，缓冲区数据将用 ``0xff`` 填充。

API 参考
********

.. doxygengroup:: bt_mesh_blob_io_flash
