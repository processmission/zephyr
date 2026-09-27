.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _virtio:

虚拟 I/O（VIRTIO）
##################

概述
****

虚拟 I/O（VIRTIO）是一种用于与各种设备通信的协议，通常用于虚拟化环境。其主要目标是提供一种高效、标准化的机制，让虚拟机能够与虚拟设备交互。通信依赖于 virtqueue 以及 PCI 或 MMIO 等标准传输方式。

概念
****

Virtio 定义了通信和初始化过程中使用的各种组件，并对宿主机端（在规范中称为“设备”）和客户机端（在规范中称为“驱动”）都作了规定。目前 Zephyr 只能作为客户机运行。在 Virtio 驱动提供的功能基础上，可以实现特定设备（例如网卡）的驱动。

下图展示了包含 Virtio 设备的系统的总体概况。

.. graphviz::
   :caption: 虚拟 I/O 概述

   digraph {

        subgraph cluster_host {
            style=filled;
            color=lightgrey;
            label = "Host";
            labeljust=r;

            virtio_device [label = "virtio device"];
        }

        transfer_method [label = "virtio transfer method"];

        subgraph cluster_guest {
            style=filled;
            color=lightgrey;
            label = "Guest";
            labeljust=r;

            virtio_driver [label = "virtio driver"];
            specific_device_driver [label = "specific device driver"];
            device_user [label = "device user"];
        }

        virtio_device -> transfer_method;
        transfer_method -> virtio_device;
        transfer_method -> virtio_driver;
        virtio_driver -> transfer_method;
        virtio_driver -> specific_device_driver;
        specific_device_driver -> virtio_driver;
        specific_device_driver -> device_user;
        device_user -> specific_device_driver;
   }

配置空间
========
每个设备都提供用于初始化和配置的配置空间。通过配置空间，可以选择设备和驱动的特性、启用特定的 virtqueue 并设置其地址。设备配置完成后，大部分配置只有在重置设备后才能更改。配置空间的具体布局取决于传输方式。

驱动和设备特性
--------------
配置空间提供了协商特性位的方式，用于确定设备的一些可选功能。具体可用的特性位取决于设备和平台。

设备专用配置
------------
某些设备提供设备专用配置空间，以提供额外的配置选项。

虚拟队列（virtqueue）
=====================
宿主机与客户机之间传输数据的主要机制是 virtqueue。不同设备的 virtqueue 数量各不相同，例如，支持双向传输的设备通常具有一对或多对发送/接收 virtqueue。Virtio 规定了两种 virtqueue：分离式 virtqueue 和紧凑式 virtqueue。Zephyr 目前仅支持分离式 virtqueue。

分离式 virtqueue
----------------
分离式 virtqueue 由三部分组成：描述符表、可用环和已用环。

描述符表保存缓冲区的描述符，即缓冲区的物理地址、长度和标志。每个描述符对应的缓冲区要么可由设备写入，要么可由驱动写入。描述符可以串联起来，形成描述符链。通常，描述符链以包含供设备读取的数据的描述符开头，以设备可写部分结尾，设备在该部分放置响应。

可用环的主体是一个循环缓冲区，其中保存了对描述符表中描述符的引用（以索引形式表示）。当客户机决定向宿主机发送数据时，会将描述符链头部的索引添加到可用环的顶部。

已用环与可用环类似，但由宿主机用于向客户机归还描述符。除了保存描述符索引外，它还提供写入对应缓冲区的数据量信息。

通用 Virtio 库
**************

Zephyr 提供了用于与 Virtio 设备和 virtqueue 交互的 API，可在 Virtio 设备的整个生命周期内执行必要的操作。

设备初始化
==========
Virtio 驱动首先完成使用给定传输方式的所有设备所共有的底层初始化，例如在总线上查找设备并映射 Virtio 结构。随后，设备专用驱动接手，借助 Virtio API 执行后续的初始化步骤。

设备专用驱动首先进行特性位协商。它使用 :c:func:`virtio_read_device_feature_bit` 确定设备提供哪些特性，然后使用 :c:func:`virtio_write_driver_feature_bit` 选择所需的特性。选定所有必需的特性后，设备专用驱动调用 :c:func:`virtio_commit_feature_bits` 。接着，使用 :c:func:`virtio_init_virtqueues` 初始化 virtqueue。此函数会枚举 virtqueue，并调用提供的回调 :c:type:`virtio_enumerate_queues` 来确定每个 virtqueue 所需的大小。最后，调用 :c:func:`virtio_finalize_init` 完成初始化过程。此时，如果所有函数均未返回错误，virtqueue 就可以正常工作了。如果设备提供了设备专用配置，可以通过调用 :c:func:`virtio_get_device_specific_config` 获取。

virtqueue 操作
==============
virtqueue 可以正常工作后，就能用于发送和接收数据。为此，必须使用 :c:func:`virtio_get_virtqueue` 获取指向第 n 个 virtqueue 的指针。要发送由描述符链表示的数据，必须使用 :c:func:`virtq_add_buffer_chain` 。除了描述符链，该函数还接收一个回调指针，设备归还该描述符链时会调用此回调。之后，必须使用 Virtio API 中的 :c:func:`virtio_notify_virtqueue` 通知该 virtqueue。

客户机端 Virtio 驱动
********************
目前，Zephyr 提供了基于 PCI 和基于 MMIO 的 Virtio 驱动，以及三种使用 virtio 的设备的驱动：用于访问宿主机文件系统的 virtiofs、用作熵源的 virtio-entropy，以及用于访问块设备的 virtio-blk。

Virtiofs
========
此驱动支持 `virtiofs <https://virtio-fs.gitlab.io/>`_ ，这是一种允许虚拟机客户机访问宿主机目录的文件系统。它使用 FUSE 消息在宿主机与客户机之间通信，以执行打开和读取文件等文件系统操作。每当客户机需要执行文件系统操作时，都会在 virtqueue 中放置一条描述符链。该链以设备可读部分开头，其中包含 FUSE 输入头和输入数据；以设备可写部分结尾，其中预留了存放 FUSE 输出头和输出数据的空间。

Virtio-entropy
==============
此驱动允许在 Zephyr 中使用 virtio-entropy 作为熵源。该设备的工作方式很简单：驱动将一个缓冲区放入 virtqueue，随后收回已填满随机数据的缓冲区。

Virtio-blk
==========
此驱动将 virtio-blk 块设备暴露给 Zephyr 的磁盘访问层，使其可以通过 :ref:`磁盘访问 API <disk_access_api>` 及其上层的文件系统使用。它同一时间仅处理一个请求，提交的描述符链由请求头、以一个或多个分散/聚集段表示的调用者数据缓冲区，以及一个状态字节组成。详情请参阅 :ref:`disk_virtio_blk` 。

Virtio 示例
***********
:zephyr:code-sample:`virtiofs` 提供了一个示例，展示如何使用依赖 Virtio 的驱动。如果希望查看直接与 Virtio 驱动交互的代码，可以查看 virtiofs 驱动，尤其是用于初始化的 :c:func:`virtiofs_init` ，以及配合 :c:func:`virtiofs_recv_cb` 向 Virtio 设备发送数据和从中接收数据的 :c:func:`virtiofs_send_receive` 。

API 参考
********

.. doxygengroup:: virtio_interface
.. doxygengroup:: virtqueue_interface
