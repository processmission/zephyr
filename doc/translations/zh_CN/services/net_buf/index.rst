.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_buf_interface:

网络缓冲区
##########

.. contents::
    :local:
    :depth: 2


概述
****

网络缓冲区是网络协议栈（以及蓝牙协议栈）传递数据的核心概念。这些缓冲区的 API 定义在 :zephyr_file:`include/zephyr/net_buf.h` 中。

创建缓冲区
**********

要创建网络缓冲区，首先需要定义一个存放它们的缓冲区池：

.. code-block:: c

   NET_BUF_POOL_DEFINE(pool_name, buf_count, buf_size, user_data_size, NULL);

该池是一个静态变量，因此如果需要将其导出到另一个模块，则需要一个单独的指针。

定义池后，就可以使用以下方式从中分配缓冲区：

.. code-block:: c

   buf = net_buf_alloc(&pool_name, timeout);

池及其缓冲区都没有显式的初始化函数，而是在调用 :c:func:`net_buf_alloc` 时隐式完成初始化。

如果需要在缓冲区中预留空间，以便稍后在前面添加协议报头，则可以通过以下方式预留这部分 headroom：

.. code-block:: c

   net_buf_reserve(buf, headroom);

除了实际的协议数据和通用解析上下文之外，网络缓冲区还可以包含协议特定的上下文，即用户数据。缓冲区的最大数据容量和用户数据容量都在声明缓冲区池时于编译期定义。

这些缓冲区原生支持通过 k_fifo 内核对象传递。可以使用 :c:func:`k_fifo_put` 和 :c:func:`k_fifo_get` 将缓冲区从一个线程传递到另一个线程。

对于单链表中的缓冲区，提供了专门的函数，此时必须使用 :c:func:`net_buf_slist_put` 和 :c:func:`net_buf_slist_get` 函数，而不能使用 :c:func:`sys_slist_append` 和 :c:func:`sys_slist_get`。

常见操作
********

网络缓冲区 API 提供了一些有用的辅助函数，用于在缓冲区中编码和解码数据。要完全理解这些辅助函数，最好先了解与它们配合使用的基本操作名称：

添加
  将数据添加到缓冲区的末尾。修改数据长度值，但保持实际数据指针不变。要求缓冲区中有足够的 tailroom。以下是一些用于添加数据的 API 示例：

  .. code-block:: c

     void *net_buf_add(struct net_buf *buf, size_t len);
     void *net_buf_add_mem(struct net_buf *buf, const void *mem, size_t len);
     uint8_t *net_buf_add_u8(struct net_buf *buf, uint8_t value);
     void net_buf_add_le16(struct net_buf *buf, uint16_t value);
     void net_buf_add_le32(struct net_buf *buf, uint32_t value);

移除
  从缓冲区的末尾移除数据。修改数据长度值，但保持实际数据指针不变。以下是一些用于移除数据的 API 示例：

  .. code-block:: c

     void *net_buf_remove_mem(struct net_buf *buf, size_t len);
     uint8_t net_buf_remove_u8(struct net_buf *buf);
     uint16_t net_buf_remove_le16(struct net_buf *buf);
     uint32_t net_buf_remove_le32(struct net_buf *buf);

推入
  在缓冲区的开头添加数据。同时修改数据长度值和数据指针。要求缓冲区中有足够的 headroom。以下是一些用于推入数据的 API 示例：

  .. code-block:: c

     void *net_buf_push(struct net_buf *buf, size_t len);
     void *net_buf_push_mem(struct net_buf *buf, const void *mem, size_t len);
     void net_buf_push_u8(struct net_buf *buf, uint8_t value);
     void net_buf_push_le16(struct net_buf *buf, uint16_t value);

拉取
  从缓冲区的开头移除数据。同时修改数据长度值和数据指针。以下是一些用于拉取数据的 API 示例：

  .. code-block:: c

     void *net_buf_pull(struct net_buf *buf, size_t len);
     void *net_buf_pull_mem(struct net_buf *buf, size_t len);
     uint8_t net_buf_pull_u8(struct net_buf *buf);
     uint16_t net_buf_pull_le16(struct net_buf *buf);
     uint32_t net_buf_pull_le32(struct net_buf *buf);

将数据编码到缓冲区时使用 Add 和 Push 操作，而从缓冲区解码数据时使用 Remove 和 Pull 操作。

引用计数
********

每个网络缓冲区都采用引用计数。缓冲区最初通过调用 :c:func:`net_buf_alloc()` 从空闲缓冲区池中获取，此时引用计数为 1。可以使用 :c:func:`net_buf_ref()` 递增引用计数，或使用 :c:func:`net_buf_unref()` 递减引用计数。当计数降为零时，缓冲区会自动放回空闲缓冲区池。


API 参考
********

.. doxygengroup:: net_buf
