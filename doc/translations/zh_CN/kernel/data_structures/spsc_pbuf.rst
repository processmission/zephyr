.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _spsc_pbuf:

单生产者单消费者包缓冲区
========================

:dfn:`单生产者单消费者包缓冲区（SPSC_PBUF）` 是一种环形缓冲区，按先进先出的顺序存储变长数据包。它要求只有一个上下文生产数据包，且只有一个上下文消费数据。

该实现重点关注性能和内存占用。

使用 :c:func:`spsc_pbuf_write` 向缓冲区添加数据包，该函数会将数据复制到缓冲区。如果缓冲区已满，则返回错误。

使用 :c:func:`spsc_pbuf_read` 将数据包从缓冲区复制出来。
