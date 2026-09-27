.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _object_cores_api:

对象核心
########

对象核心是一种内核调试工具，可用于标识已注册的对象并对其执行操作。

.. contents::
    :local:
    :depth: 2

对象核心概念
************

每个对象实例都嵌入一个名为 ``obj_core`` 的对象核心字段。同一类型的对象通过各自的对象核心连接为单向链表。每个对象核心还链接到其所属的对象类型。每个对象类型包含一条单向链表，将该类型的所有对象核心连接起来。对象类型之间也通过单向链表连接。这些链接使调试工具能够遍历系统中的所有对象。

对象核心已集成到以下内核对象中：

* :ref:`条件变量 <condvar>`
* :ref:`事件 <events>`
* :ref:`FIFO <fifos_v2>` 和 :ref:`LIFO <lifos_v2>`
* :ref:`邮箱 <mailboxes_v2>`
* :ref:`内存 slab <memory_slabs_v2>`
* :ref:`消息队列 <message_queues_v2>`
* :ref:`互斥锁 <mutexes_v2>`
* :ref:`管道 <pipes_v2>`
* :ref:`信号量 <semaphores_v2>`
* :ref:`线程 <threads_v2>`
* :ref:`定时器 <timers_v2>`
* :ref:`系统内存块 <sys_mem_blocks>`

开发者也可以按需将对象核心集成到项目中的其他对象中。

对象核心统计概念
****************
多种内核对象支持收集和报告统计信息。对象核心通过对象核心统计机制，提供统一的信息获取方式。启用此功能后，对象类型包含一个指向统计描述符的指针，该描述符定义了已启用的、用于访问对象统计信息的各种操作。此外，对象核心还包含一个指向该对象“原始”统计信息的指针。原始数据是与统计信息相关的、未经处理的数据。查询数据可能是“原始”数据，也可能经过某种计算处理，例如求平均值。

下表列出了已集成对象核心统计功能的对象，以及各自用于“原始”数据和“查询”数据的结构体。

+-----------------------+--------------------------------+--------------------------------+
| 对象                  | 原始数据类型                   | 查询数据类型                   |
+=======================+================================+================================+
| struct mem_slab       | struct mem_slab_info           | struct sys_memory_stats        |
+-----------------------+--------------------------------+--------------------------------+
| struct sys_mem_blocks | struct sys_mem_blocks_info     | struct sys_memory_stats        |
+-----------------------+--------------------------------+--------------------------------+
| struct k_thread       | struct k_cycle_stats           | struct k_thread_runtime_stats  |
+-----------------------+--------------------------------+--------------------------------+
| struct _cpu           | struct k_cycle_stats           | struct k_thread_runtime_stats  |
+-----------------------+--------------------------------+--------------------------------+
| struct z_kernel       | struct k_cycle_stats[num CPUs] | struct k_thread_runtime_stats  |
+-----------------------+--------------------------------+--------------------------------+

实现
****

定义新的对象类型
================

使用 :c:struct:`k_obj_type` 类型的全局变量定义对象类型。必须在初始化该类型的任何对象之前初始化对象类型。以下代码展示如何初始化新的对象类型，使其可用于对象核心和对象核心统计。

.. code-block:: c

    /* Unique object type ID */

    #define K_OBJ_TYPE_MY_NEW_TYPE  K_OBJ_TYPE_ID_GEN("UNIQ")
    struct k_obj_type  my_obj_type;

    struct my_obj_type_raw_info {
        ...
    };

    struct my_obj_type_query_stats {
        ...
    };

    struct my_new_obj {
        ...
        struct k_obj_core obj_core;
        struct my_obj_type_raw_info  info;
    };

    struct k_obj_core_stats_desc my_obj_type_stats_desc = {
        .raw_size = sizeof(struct my_obj_type_raw_stats),
        .query_size = sizeof(struct my_obj_type_query_stats),
        .raw = my_obj_type_stats_raw,
        .query = my_obj_type_stats_query,
        .reset = my_obj_type_stats_reset,
        .disable = NULL,    /* Stats gathering is always on */
        .enable = NULL,     /* Stats gathering is always on */
    };

    void my_obj_type_init(void)
    {
        z_obj_type_init(&my_obj_type, K_OBJ_TYPE_MY_NEW_TYPE,
                        offsetof(struct my_new_obj, obj_core);
        k_obj_type_stats_init(&my_obj_type, &my_obj_type_stats_desc);
    }

初始化新的对象核心
==================

对于已集成对象核心框架的内核对象，其对象核心会在对象初始化时自动初始化。但是，要将自定义对象加入框架，开发者需要初始化对象核心并将其链接起来。以下代码在上例的基础上初始化对象核心。

.. code-block:: c

    void my_new_obj_init(struct my_new_obj *new_obj)
    {
        ...
        k_obj_core_init(K_OBJ_CORE(new_obj), &my_obj_type);
        k_obj_core_link(K_OBJ_CORE(new_obj));
        k_obj_core_stats_register(K_OBJ_CORE(new_obj), &new_obj->raw_stats,
                                  sizeof(struct my_obj_type_raw_info));
    }

遍历对象核心列表
================

有两个函数可用于遍历链接到某个对象类型的对象核心列表：:c:func:`k_obj_type_walk_locked` 和 :c:func:`k_obj_type_walk_unlocked`。以下代码在上例的基础上，打印该新对象类型的所有对象的地址。

.. code-block:: c

    int walk_op(struct k_obj_core *obj_core, void *data)
    {
        uint8_t *ptr;

        ptr = obj_core;
        ptr -= obj_core->type->obj_core_offset;

        printk("%p\n", ptr);

        return 0;
    }

    void print_object_addresses(void)
    {
        struct k_obj_type *obj_type;

        /* Find the object type */

        obj_type = k_obj_type_find(K_OBJ_TYPE_MY_NEW_TYPE);

        /* Walk the list of objects */

        k_obj_type_walk_unlocked(obj_type, walk_op, NULL);
    }

查询对象核心统计信息
====================

以下代码在前述示例的基础上，展示已集成对象核心统计框架的对象如何获取查询数据，以及如何重置对象的统计信息。

.. code-block:: c

    struct my_new_obj my_obj;

    ...

    void my_func(void)
    {
        struct my_obj_type_query_stats  my_stats;
        int  status;

        my_obj_type_init(&my_obj);

        ...

        status = k_obj_core_stats_query(K_OBJ_CORE(&my_obj),
                                        &my_stats, sizeof(my_stats));
        if (status != 0) {
            /* Failed to get stats */
            ...
        } else {
            k_obj_core_stats_reset(K_OBJ_CORE(&my_obj));
        }

        ...
    }

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_OBJ_CORE`
* :kconfig:option:`CONFIG_OBJ_CORE_CONDVAR`
* :kconfig:option:`CONFIG_OBJ_CORE_EVENT`
* :kconfig:option:`CONFIG_OBJ_CORE_FIFO`
* :kconfig:option:`CONFIG_OBJ_CORE_LIFO`
* :kconfig:option:`CONFIG_OBJ_CORE_MAILBOX`
* :kconfig:option:`CONFIG_OBJ_CORE_MEM_SLAB`
* :kconfig:option:`CONFIG_OBJ_CORE_MSGQ`
* :kconfig:option:`CONFIG_OBJ_CORE_MUTEX`
* :kconfig:option:`CONFIG_OBJ_CORE_PIPE`
* :kconfig:option:`CONFIG_OBJ_CORE_SEM`
* :kconfig:option:`CONFIG_OBJ_CORE_STACK`
* :kconfig:option:`CONFIG_OBJ_CORE_THREAD`
* :kconfig:option:`CONFIG_OBJ_CORE_TIMER`
* :kconfig:option:`CONFIG_OBJ_CORE_SYS_MEM_BLOCKS`
* :kconfig:option:`CONFIG_OBJ_CORE_STATS`
* :kconfig:option:`CONFIG_OBJ_CORE_STATS_MEM_SLAB`
* :kconfig:option:`CONFIG_OBJ_CORE_STATS_THREAD`
* :kconfig:option:`CONFIG_OBJ_CORE_STATS_SYSTEM`
* :kconfig:option:`CONFIG_OBJ_CORE_STATS_SYS_MEM_BLOCKS`

API 参考
********

.. doxygengroup:: obj_core_apis
.. doxygengroup:: obj_core_stats_apis
