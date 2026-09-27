.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _dlist_api:

双向链表
========

Zephyr 还提供双向链表实现，它在许多方面与单链表相似。对于已有的 slist 操作，它具有相同的算法特性，并且支持在任意位置以常数时间删除或插入节点，包括头节点、尾节点或任意内部节点的前后。为此，每个节点存储两个指针，因此运行时代码和内存空间需求略高。

用户可以在任意可访问的内存中实例化 :c:type:`sys_dlist_t` 结构体。使用前必须通过 :c:func:`sys_dlist_init` 或 :c:macro:`SYS_DLIST_STATIC_INIT` 初始化。对于加入链表的每个节点，用户需提供 :c:type:`sys_dnode_t` 结构体，通常将其嵌入需要跟踪的结构体中，如上所述。使用前，节点必须位于已清零的内存或 bss 中，或通过 :c:func:`sys_dnode_init` 初始化。

可以使用 :c:func:`sys_dlist_peek_head`、:c:func:`sys_dlist_peek_tail`、:c:func:`sys_dlist_peek_next` 和 :c:func:`sys_dlist_peek_prev` 等基本操作，获取链表的头尾节点以及节点的前后指针。在相应情况下，这些操作均可返回 NULL，例如链表为空或节点位于链表端点时。

可以通过 :c:func:`sys_dlist_remove` 删除节点，通过 :c:func:`sys_dlist_prepend` 和 :c:func:`sys_dlist_append` 在链表头尾添加节点，或通过 :c:func:`sys_dlist_insert` 在已有节点之前插入节点。这些修改操作均为常数时间。

与 slist 一样，可以使用 :c:macro:`SYS_DLIST_FOR_EACH_NODE`，以自然的代码块形式处理 dlist 中的每个节点。该宏还提供多种变体：“FROM_NODE”从已知起点开始遍历；“SAFE”允许在代码块中删除正在检查的节点；“CONTAINER”提供包含节点的结构体指针，而非原始节点指针；“CONTAINER_SAFE”则兼具后两者的特性。

dlist 提供的辅助工具包括 :c:func:`sys_dlist_insert_at`，它通过线性搜索寻找合适的位置插入节点，插入位置判定逻辑由用户通过 C 回调函数指针提供；还有 :c:func:`sys_dnode_is_linked`，可以明确判断节点当前是否已链接到某个 dlist 中，其实现相较普通链表处理不增加额外开销。

双向链表内部实现
----------------

dlist 的内部实现非常精简：:c:type:`sys_dlist_t` 结构体包含“head”和“tail”指针字段，:c:type:`sys_dnode_t` 包含“prev”和“next”指针，不存储其他数据。实际上，这两个结构体的内部布局相同，链表结构体本身也作为一个节点插入链表。这使各项操作具有简洁的对称性：

* 空链表的链表结构体中，指针回指自身，因此很容易检测。

* 将节点的 prev/next 指针与链表结构体地址比较，即可识别链表的头尾。

* 插入或删除时，无需检查是否在头尾操作这一特殊情况。链表内部从不出现需要避开的 NULL 指针。所有链表修改原语都执行完全相同的操作，无需测试或分支。

因此，具有 N 个节点的 dlist 可以视为一个包含“N+1”个节点的“环”，其中一个节点就是用于跟踪链表的结构体。

.. figure:: dlist.png
    :align: center
    :alt: dlist 示例
    :figclass: align-center

    包含三个元素的 dlist。注意，链表结构体作为第四个“元素”出现在链表中。

.. figure:: dlist-single.png
    :align: center
    :alt: 单元素 dlist 示例
    :figclass: align-center

    仅包含一个元素的 dlist。

.. figure:: dlist-empty.png
    :align: center
    :alt: dlist example
    :figclass: align-center

    空 dlist。


双向链表 API 参考
-----------------

.. doxygengroup:: doubly-linked-list_apis
