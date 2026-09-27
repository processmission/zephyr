.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_pkt_interface:

数据包管理
##########

.. contents::
    :local:
    :depth: 2

概述
****

网络数据包是网络协议栈处理的主要数据。此类数据通过 net_pkt 结构体表示，该结构体提供了保存数据包并对其进行读写的方法，以及供核心保存重要信息的必要元数据。在本文档中，此类对象称为 net_pkt。

数据结构及其周围的整个 API（Application Programming Interface）定义在 :zephyr_file:`include/zephyr/net/net_pkt.h` 中。

架构说明
========

协议栈内有两种网络数据包流： **TX** 表示发送（transmission）路径， **RX** 表示接收（reception）路径。在这两种路径中，每个 net_pkt 都从开头到末尾进行写入和读取，更具体地说，是从报头到有效载荷。

并发与线程安全
==============

``net_pkt`` 结构体及其关联 API **不是线程安全的。** 网络协议栈依赖严格的 **独占所有权** 模型。创建或接收网络数据包时，该数据包在任意给定时刻只由一个线程或执行上下文拥有。

并发通过以下主要模式进行管理：

*   **通过 FIFO（First In, First Out，先进先出）转移所有权：** ``net_pkt`` 最常见的生命周期是在相互隔离的执行上下文之间传递（例如，从 RX 驱动线程传递到 IP（Internet Protocol）协议栈）。数据包一旦入队，发送方就会放弃其引用并失去访问权。
*   **浅克隆（ ``net_pkt_shallow_clone`` ）：** 如果为了可能的重传，某一层必须保留数据包（例如 TCP，Transmission Control Protocol），同时另一层又要处理该数据包，则使用 ``net_pkt_shallow_clone()`` 创建一个新的包装器，指向相同的底层只读数据（数据缓冲区本身通过线程安全的引用计数管理）。
*   **粗粒度协议锁：** 当数据包被有意保存在内存队列中时，它们由更高级别的子系统锁（例如连接互斥量）保护。

``struct net_pkt`` 中的 ``atomic_ref`` 字段用于内存生命周期管理（防止释放后使用，Use-After-Free），并不是用于并发修改的锁。

内存管理
********

分配
====

所有 net_pkt 对象都来自预定义的 struct net_pkt 池。该池通过以下方式定义：

.. code-block:: c

    NET_PKT_SLAB_DEFINE(name, count)

不过请注意，很少需要直接使用它，因为核心已经提供了两个池，一个用于 TX 路径，一个用于 RX 路径。

可通过以下方式分配原始 net_pkt：

.. code-block:: c

    pkt = net_pkt_alloc(timeout);

不过，原始 net_pkt 本身在没有缓冲区时毫无用处，还需要各种元数据信息才能发挥作用。它至少要获取该数据包用于发送或接收的网络接口。由于这是非常常见的操作，因此提供了一个辅助函数：

.. code-block:: c

    pkt = net_pkt_alloc_on_iface(iface, timeout);

还有一个更完整的分配器，可以同时分配 net_pkt 及其缓冲区：

.. code-block:: c

    pkt = net_pkt_alloc_with_buffer(iface, size, family, proto, timeout);

缓冲区分配方式见下文。


缓冲区分配
==========

net_pkt 对象不定义自己的缓冲区，而是使用现有对象 :c:struct:`net_buf` 来实现这一点（更多信息见 :ref:`net_buf_interface` ）。不过，它基本上隐藏了此类缓冲区的用法，因为 net_pkt 为缓冲区分配带来了网络感知能力，并且正如稍后将看到的，也为自身操作带来了网络感知能力。

要分配缓冲区，net_pkt 至少需要设置网络接口。如果在分配缓冲区时数据包的地址族未知，仍然可以这样做。此时可以执行以下操作：

.. code-block:: c

    net_pkt_alloc_buffer(pkt, size, proto, timeout);

其中 proto 在未知时可以为 0（不存在 IPPROTO_UNSPEC）。

如前所述，可以通过 :c:func:`net_pkt_alloc_with_buffer` 一次性分配 net_pkt 及其缓冲区。实际上，这是使用最广泛的分配器。

缓冲区分配会使用数据包的网络接口、地址族和协议来确定能否分配请求的大小。分配器会使用网络接口获知最大传输单元（MTU），然后使用地址族和协议确定报头空间（如果只指定了后两者）。如果总大小在 MTU 范围内，则分配的空间为请求大小加上可能的报头空间。如果 MTU 空间不足，则请求大小会被缩减，以便可能的报头空间和新大小能够放入 MTU 内。

例如，在 MTU 为 1500 字节的以太网网络接口上：

.. code-block:: c

    pkt = net_pkt_alloc_with_buffer(iface, 800, NET_AF_INET4, IPPROTO_UDP, K_FOREVER);

将为新的 net_pkt 成功分配 800 + 20 + 8 字节的缓冲区，其中：

.. code-block:: c

    pkt = net_pkt_alloc_with_buffer(iface, 1600, NET_AF_INET4, IPPROTO_UDP, K_FOREVER);

将成功分配 1500 字节，其中 20 + 8 字节（IPv4 + UDP 报头）不会用于有效载荷。

在接收侧，当地址族和协议未知时：

.. code-block:: c

    pkt = net_pkt_rx_alloc_with_buffer(iface, 800, AF_UNSPEC, 0, K_FOREVER);

将分配 800 字节，且没有额外的报头空间。但使用以下调用时：

.. code-block:: c

    pkt = net_pkt_rx_alloc_with_buffer(iface, 1600, AF_UNSPEC, 0, K_FOREVER);

将分配 1514 字节，即 MTU 加上以太网报头空间。

可以调用 :c:func:`net_pkt_alloc_buffer` 增加分配的缓冲区空间量，因为它会考虑现有缓冲区。如果 net_pkt 的地址族有效，它还会计入报头空间以及 proto 参数。在这种情况下，新分配的缓冲区空间会追加到现有缓冲区之后，而不会插入到前面。但请注意，这种用例相当有限。通常，从一开始就应该知道应请求多大的空间。


释放
====

每个 net_pkt 都采用引用计数。分配时，引用计数设置为 1。可以使用 :c:func:`net_pkt_ref()` 递增引用计数，或使用 :c:func:`net_pkt_unref()` 递减引用计数。当计数降为零时，缓冲区也会被解除引用，net_pkt 会自动放回空闲的 net_pkt_slabs 中。

如果 net_pkt 释放后仍需要使用其缓冲区，则需要在调用最后一次 net_pkt_unref 之前，再次引用整个 net_buf 链。更多信息见 :ref:`net_buf_interface`。


操作
****

访问 net_pkt 缓冲区有两种方式，将在以下各节中说明：基本读写访问和数据访问，其中后者是首选方式。

读写访问
========

如前所述，尽管 net_pkt 使用 net_buf 作为其缓冲区，但它提供了自己的 API 来访问缓冲区。实际上，网络数据包可能分散在一系列 net_buf 对象上，而 net_buf 提供的函数在这种情况下能力有限。因此，net_pkt 提供的函数隐藏了潜在非连续访问的全部复杂性。

向缓冲区中移动数据通过每个 net_pkt 内维护的游标完成。所有读写操作都会影响该游标。还要注意，读写函数对其长度参数要求严格：如果无法读写给定长度，操作就会失败。长度不会被解释为上限，而是必须读取或写入的确切数据量。

由于有 TX 和 RX 两条路径，因此有两种访问模式：写入和覆写。这听起来可能有些不寻常，但实际上简单且灵活。

在写入模式下，写入缓冲区的任何内容都会影响缓冲区中实际数据的长度。缓冲区长度不应与缓冲区大小混淆，后者是任何模式都不能超过的限制。而在覆写模式下，写入操作必须在有效数据上进行，并且不会影响缓冲区长度。默认情况下，新分配的 net_pkt 处于写入模式，其游标指向缓冲区的开头。

下面逐步介绍这些函数以及它们在不同模式下的行为。

当新分配的 net_pkt 具有 500 字节的缓冲区时，其长度为 0，这意味着缓冲区中没有有效数据。可以通过以下方式验证：

.. code-block:: c

    len = net_pkt_get_len(pkt);

现在，写入 8 个字节：

.. code-block:: c

    net_pkt_write(pkt, data, 8);

缓冲区长度现在为 8 字节。有多种辅助函数可用于写入一个字节，或写入大端序的 uint16_t、uint32_t。

.. code-block:: c

    net_pkt_write_u8(pkt, &foo);
    net_pkt_write_be16(pkt, &ba);
    net_pkt_write_be32(pkt, &bar);

从逻辑上讲，net_pkt 的长度现在为 15。但如果此时尝试读取，将会失败，因为 net_pkt 中当前游标位置没有可读取的内容。在写入模式下，可以通过重置 net_pkt 的游标来读取已经写入的内容。例如：

.. code-block:: c

    net_pkt_cursor_init(pkt);
    net_pkt_read(pkt, data, 15);

这会将 pkt 的游标重置到缓冲区开头，然后可以读取其中实际存在的 15 个字节。随后游标将再次指向缓冲区末尾。

若要使用同一个字节填充大片区域，可以使用 memset 函数：

.. code-block:: c

    net_pkt_memset(pkt, 0, 5);

现在 net_pkt 的长度为 20 字节。

可以通过 :c:func:`net_pkt_set_overwrite` 函数在模式之间切换。可以随时来回切换模式。net_pkt 将被设置为覆写模式，并且其游标会被重置：

.. code-block:: c

    net_pkt_set_overwrite(pkt, true);
    net_pkt_cursor_init(pkt);

现在可以使用相同的操作符，但只能限于缓冲区中的现有数据，即 20 字节。

如果需要知道 net_pkt 中还有多少可用空间，请调用：

.. code-block:: c

    net_pkt_available_buffer(pkt);

或者，如果需要计入报头空间，请调用：

.. code-block:: c

    net_pkt_available_payload_buffer(pkt, proto);

如果要将游标定位到已知位置，请使用 :c:func:`net_pkt_skip` 函数。例如，要跳到 IP 报头之后，请使用：

.. code-block:: c

    net_pkt_cursor_init(pkt);
    net_pkt_skip(pkt, net_pkt_ip_header_len(pkt));


数据访问
========

尽管前面介绍的 API 相当简单，但它总是涉及在 net_pkt 缓冲区内外复制数据。在许多情况下，以连续方式访问缓冲区中存储的信息更为合适，尤其是对于包含报头的网络数据包。

这些报头大多数时候是已知的固定字节集合。因此，更自然的做法是使用一个表示特定报头类型的结构体。此外，如果已知报头位于缓冲区的连续区域中，那么将缓冲区中的实际位置强制转换为该报头类型会高效得多。无论是读取还是写入此类报头的字段，直接访问它都能节省内存。

net_pkt 为此提供了专用 API，它构建在前面介绍的 API 之上，能够透明地处理连续和非连续访问。

有两个宏用于定义数据访问描述符：当无法确定数据是否位于连续区域时，使用 :c:macro:`NET_PKT_DATA_ACCESS_DEFINE` ；当可以保证数据位于连续区域时，使用 :c:macro:`NET_PKT_DATA_ACCESS_CONTIGUOUS_DEFINE` 。

以 IP 和 UDP（User Datagram Protocol）为例。IPv4 和 IPv6 报头始终位于数据包开头，且足够小，可以放入 128 字节的 net_buf 中（例如，也可以选择 64 字节）。

.. code-block:: c

    NET_PKT_DATA_ACCESS_CONTIGUOUS_DEFINE(ipv4_access, struct net_ipv4_hdr);
    struct net_ipv4_hdr *ipv4_hdr;

    ipv4_hdr = (struct net_ipv4_hdr *)net_pkt_get_data(pkt, &ipv4_access);

对于 struct net_ipv4_hdr 也是如此。而对于 UDP 报头，例如在 IPv6 中，它很可能不在连续区域内，因此：

.. code-block:: c

    NET_PKT_DATA_ACCESS_DEFINE(udp_access, struct net_udp_hdr);
    struct net_udp_hdr *udp_hdr;

    udp_hdr = (struct net_udp_hdr *)net_pkt_get_data(pkt, &udp_access);

此时，net_pkt 的游标指向所请求数据的开头。在 RX 路径中，这些报头会被读取但不会被修改，因此要继续处理，游标需要越过这些数据。为此提供了专门的函数：

.. code-block:: c

    net_pkt_acknowledge_data(pkt, &ipv4_access);

然而，在 TX 路径中，报头字段已被修改。在这种情况下：

.. code-block:: c

    net_pkt_set_data(pkt, &ipv4_access);

如果数据位于连续区域，它会相应地推进游标。如果不是，则会写入数据并更新游标。请注意，:c:func:`net_pkt_set_data` 也可以用在 RX 路径中，但使用 :c:func:`net_pkt_acknowledge_data` 稍快一些，因为后者完全不关心连续性，它直接通过 :c:func:`net_pkt_skip` 推进游标。


API 参考
********

.. doxygengroup:: net_pkt
