.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _slist_api:

单链表
======

Zephyr 提供 :c:type:`sys_slist_t` 类型，用于存储简单的单链表数据，即每个元素只保存指向下一个元素的指针，不保存指向前一个元素的指针。它支持以常数时间访问链表首尾元素、在头部之前或尾部之后插入元素，以及删除头节点。删除后续节点需要找到其“前一个”节点，因此必须以线性时间搜索链表。

用户可以在任意可访问的内存中实例化 :c:type:`sys_slist_t` 结构体。使用前应调用 :c:func:`sys_slist_init`，或通过 SYS_SLIST_STATIC_INIT 静态赋值进行初始化。内部字段是不透明的，用户代码不应访问。

可以使用 :c:func:`sys_slist_peek_head` 和 :c:func:`sys_slist_peek_tail` 获取链表两端的节点。链表为空时返回 NULL，否则返回指向 :c:type:`sys_snode_t` 结构体的指针。

:c:type:`sys_snode_t` 结构体表示待插入的节点，通常由用户分配和管理，并嵌入需要加入链表的结构体中。使用 :c:macro:`SYS_SLIST_CONTAINER`，传入包含该节点的结构体名称及节点字段名，即可从链表节点取得外层结构体指针。:c:type:`sys_snode_t` 内部仅含一个 next 指针，可通过 :c:func:`sys_slist_peek_next` 访问。

可以通过 :c:func:`sys_slist_prepend` 和 :c:func:`sys_slist_append` 在链表头尾添加单个节点，也可以通过 :c:func:`sys_slist_insert` 在已有节点之后插入新节点。同样，给定前驱节点的指针，:c:func:`sys_slist_remove` 即可删除相应节点。这些操作均为常数时间。

对于更复杂的链表修改，库也提供了辅助函数。:c:func:`sys_slist_merge_slist` 将整个链表追加到已有链表；:c:func:`sys_slist_append_list` 以常数时间追加已有链表中界限确定的一段；:c:func:`sys_slist_find_and_remove` 则以线性时间查找指定节点，并在找到时将其移除。

最后，slist 提供了一组“for each”宏，可以自然地遍历链表，无需手动沿 next 指针前进。:c:macro:`SYS_SLIST_FOR_EACH_NODE` 使用一个存储节点指针的局部变量，枚举链表中的每个节点。:c:macro:`SYS_SLIST_FOR_EACH_NODE_SAFE` 行为相似，但实现更复杂，需要额外的临时变量，并允许在遍历过程中删除当前节点。这两个宏还各有“container”变体：:c:macro:`SYS_SLIST_FOR_EACH_CONTAINER` 和 :c:macro:`SYS_SLIST_FOR_EACH_CONTAINER_SAFE`。它们在内部完成偏移计算，为与用户外层结构体类型匹配的局部变量赋值，而非使用节点结构体类型。:c:macro:`SYS_SLIST_ITERATE_FROM_NODE` 则允许只枚举指定节点及其所有后继，而不遍历链表前面的部分。

单链表内部实现
--------------

slist 代码采用精简的常规设计。:c:type:`sys_slist_t` 结构体内部只有“head”和“tail”两个指针字段，:c:type:`sys_snode_t` 则只存储一个“next”指针。

.. figure:: slist.png
    :align: center
    :alt: slist 示例
    :figclass: align-center

    包含三个元素的 slist。

.. figure:: slist-empty.png
    :align: center
    :alt: 空 slist 示例
    :figclass: align-center

    空 slist

链表代码具体通过内部的“Z_GENLIST”模板 API 实现，该 API 可以从任意结构中提取这些字段，并生成一组可任意命名的函数。因此，可以使用相同的基本原语实现更复杂的单链表变体。genlist 的实现者只需自定义基本操作：每个结构体的“init”步骤，以及相关结构体中 head、tail 和 next 指针各自的“get”和“set”原语。这些内联函数作为参数传入 genlist 宏展开。

目前，Zephyr 中只有 sflist 这一种变体。


带标志位的链表
--------------

:c:type:`sys_sflist_t` 使用上述 genlist 模板 API 实现。除了符号命名不同（使用“sflist”而非“slist”），以及下面介绍的附加 API 外，其所有操作都与 slist API 相同。

它允许每个链表节点关联恰好两个用户定义的“标志”位，可通过 :c:func:`sys_sfnode_flags_get` 和 :c:func:`sys_sfnode_flags_set` 访问和修改。在内部，这些标志与 next 指针的低位合并存储，因此相较更简单的 slist 实现，不增加 SRAM 存储开销。


单链表 API 参考
---------------

.. doxygengroup:: single-linked-list_apis

带标志位链表 API 参考
---------------------

.. doxygengroup:: flagged-single-linked-list_apis
