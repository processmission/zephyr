.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _fcb_api:

Flash 循环缓冲区（FCB）
#######################

Flash 循环缓冲区提供了一种抽象，通过它可以将 flash 视为 FIFO。你将条目追加到末尾，并从开头读取数据。

描述
****

flash 中的条目包含条目长度、条目内的数据以及针对条目内容的校验和。

flash 中条目的存储采用 FIFO 方式。当你为下一个条目请求空间时，空间位于已使用区域的末尾。当你开始读取时，最先提供的条目是 flash 中最旧的条目。

条目可以追加到区域的末尾，直到存储空间耗尽。你可以控制接下来发生的情况：要么擦除最旧的数据块，从而释放一些空间；要么停止写入新数据，直到已收集现有数据。FCB 将底层存储视为 flash 扇区数组；当它擦除旧数据时，一次擦除一个扇区。

flash 中的条目都带有校验和。FCB 就是这样检测条目写入 flash 是否成功完成的。它会跳过校验和无效的条目。

用法
****

要向循环缓冲区添加条目：

- 调用 :c:func:`fcb_append` 获取可以写入数据的位置。如果由于空间不足而失败，可以调用 :c:func:`fcb_rotate` 擦除最旧的扇区，从而腾出空间。然后再次调用 :c:func:`fcb_append`。
- 使用 :c:func:`flash_area_write` 写入条目内容。
- 完成后调用 :c:func:`fcb_append_finish`。它会通过计算校验和来完成条目写入。

要读取循环缓冲区的内容：

- 使用指向你的回调函数的指针调用 :c:func:`fcb_walk`。
- 在回调函数中，使用 :c:func:`flash_area_read` 复制条目中的数据。你可以通过监视所返回条目的区域指针来判断何时已读取完某个扇区内的所有数据。然后，如果已处理完该数据，可以调用 :c:func:`fcb_rotate`。

或者：

- 使用条目偏移量为 0 调用 :c:func:`fcb_getnext` 以获取指向最旧条目的指针。
- 使用 :c:func:`flash_area_read` 读取条目内容。
- 使用指向当前条目的指针调用 :c:func:`fcb_getnext` 以获取下一个条目。依此类推。

API 参考
********

FCB 子系统 API 由 ``fcb.h`` 提供：

数据结构
========
.. doxygengroup:: fcb_data_structures

API 函数
========
.. doxygengroup:: fcb_api
