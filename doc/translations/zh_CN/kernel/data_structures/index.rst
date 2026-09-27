.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _data_structures:

数据结构
########

Zephyr 提供一个通用数据结构库，这些数据结构用于内核内部，也适用于一般应用代码。其中包括用于存储有序数据的链表和平衡树，以及便于管理“字节流”数据的环形缓冲区。

这些集合通常采用“侵入式”数据结构实现。库代码只使用“节点”结构体，不会在其中保存用于指示节点“拥有”哪些用户数据的指针或其他元数据。相反，节点本身应嵌入用户定义的结构体中。库提供了宏，可方便地从嵌入的节点指针取得用户结构体的地址。这样设计是为了让这些集合可以用于禁止动态分配的场景：内存由用户提供，因此无需再分配节点对象。

还需注意，这些库通常不提供同步，默认情况下访问它们并非线程安全。它们是数据结构，不是同步原语，所需的加锁应由用户实现。某些数据结构在特定使用场景下是线程安全的（见 :ref:`spsc_lockfree` 和 :ref:`mpsc_lockfree`）。

.. toctree::
  :maxdepth: 1

  slist.rst
  dlist.rst
  mpsc_pbuf.rst
  spsc_pbuf.rst
  rbtree.rst
  ring_buffers.rst
  mpsc_lockfree.rst
  spsc_lockfree.rst
  min_heap.rst
  ringq.rst
