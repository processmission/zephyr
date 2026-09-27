.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_blob:

BLOB 传输模型
#############

Binary Large Object (BLOB) 传输模型实现了 Bluetooth Mesh 二进制大对象传输模型规范 1.0 版，提供通过 Bluetooth Mesh 网络将大型二进制对象从单个源发送到多个目标节点的功能。它是 :ref:`bluetooth_mesh_dfu` 的底层传输方式，但也可用于其他对象传输目的。该实现处于实验性状态。

BLOB 传输模型支持最大 4 GB（2 \ :sup:`32` 字节）的连续二进制对象传输。BLOB 传输协议内置丢包恢复流程，并设置检查点以确保所有目标在继续之前都已收到全部数据。数据传输顺序不做保证。

BLOB 传输受底层 Mesh 网络的传输速度和可靠性限制。在理想条件下，BLOB 的传输速率最高可达 1 kbps，100 kB 的 BLOB 可在 10-15 分钟内传输完毕。然而，网络状况、传输能力和其他限制因素很容易使数据速率下降几个数量级。根据应用和网络配置调整传输参数，并将其安排在网络流量较低的时段，可以显著提升协议的速度和可靠性。不过，在实际部署中很难达到接近理想速率的传输速率。

BLOB 传输模型有两种：

.. toctree::
   :maxdepth: 1

   blob_srv
   blob_cli

BLOB 传输客户端实例化在发送方节点上，BLOB 传输服务器实例化在接收方节点上。

概念
****

BLOB 传输协议引入了若干新概念来实现 BLOB 传输。


BLOB
====

BLOB 是最大 4 GB 的二进制对象，可以包含应用希望通过 Mesh 网络传输的任何数据。BLOB 是连续的数据对象，被划分为块（block）和分块（chunk），以确保传输可靠且易于处理。BLOB 的内容或结构没有任何限制，应用可以自由地为其数据定义任何编码或压缩方式。

BLOB 传输协议不提供任何内置的 BLOB 数据完整性检查、加密或认证。不过，Bluetooth Mesh 协议的底层加密通过网络安全和应用层加密提供数据完整性检查，并保护 BLOB 内容不被第三方获取。

块
---

二进制对象被划分为块，块大小通常从几百字节到几千字节不等。每个块单独传输，BLOB 传输客户端确保所有 BLOB 传输服务器都已收到完整的块后，才继续下一个块。块大小由传输的 ``block_size_log`` 参数确定，除最后一个块可能较小外，传输中所有块的大小都相同。对于存储在闪存中的 BLOB，块大小通常是目标设备闪存页大小的倍数。

分块
----

每个块被划分为分块。分块是 BLOB 传输中最小的数据单元，必须能够放入单个 Bluetooth Mesh 访问消息中（不包括 Opcode，379 字节或更小）。分块的传输机制取决于传输模式。

在 Push BLOB 传输模式下，分块以未确认数据包的形式从 BLOB 传输客户端发送到所有目标 BLOB 传输服务器。一个块中的所有分块发送完毕后，BLOB 传输客户端会询问每个 BLOB 传输服务器是否缺少分块，并重发缺少的分块。重复此过程，直到所有 BLOB 传输服务器都收到全部分块，或者 BLOB 传输客户端放弃。

在 Pull BLOB 传输模式下，BLOB 传输服务器每次向 BLOB 传输客户端请求少量分块，并等待 BLOB 传输客户端发送这些分块后再请求更多分块。重复此过程，直到所有分块传输完毕，或者 BLOB 传输服务器放弃。

有关传输模式的更多信息，请参见 :ref:`bluetooth_mesh_blob_transfer_modes` 一节。

.. _bluetooth_mesh_blob_stream:

BLOB 流
=======

在 BLOB 传输模型的 API 中，BLOB 数据处理与高层传输处理相互分离。这种分离使得不同应用可以复用不同的 BLOB 存储和传输策略。高层传输由应用直接控制，而 BLOB 数据本身则通过 *BLOB 流* 访问。

BLOB 流类似于标准库的文件流。通过打开、关闭、读取和写入，BLOB 传输模型可以完全访问 BLOB 数据，无论数据存储在闪存、RAM 还是外设中。BLOB 流在使用前需要以访问模式（读或写）打开，BLOB 传输模型将以块和分块为单位在 BLOB 数据中移动，并将 BLOB 流作为接口。

交互
----

在读取或写入 BLOB 之前，通过调用其 :c:member:`open <bt_mesh_blob_io.open>` 回调来打开流。与 BLOB 传输服务器一起使用时，BLOB 流始终以写模式打开；与 BLOB 传输客户端一起使用时，BLOB 流始终以读模式打开。

对于 BLOB 中的每个块，BLOB 传输模型首先调用 :c:member:`block_start <bt_mesh_blob_io.block_start>` 回调。然后根据访问模式，重复调用 BLOB 流的 :c:member:`wr <bt_mesh_blob_io.wr>` 或 :c:member:`rd <bt_mesh_blob_io.rd>` 回调，以将数据移入或移出 BLOB。模型处理完该块后，调用 :c:member:`block_end <bt_mesh_blob_io.block_end>` 回调。传输完成后，通过调用 :c:member:`close <bt_mesh_blob_io.close>` 回调关闭 BLOB 流。

实现
----

应用可以实现自己的 BLOB 流，也可以使用 Zephyr 提供的实现：

.. toctree::
   :maxdepth: 2

   blob_flash


传输能力
========

每个 BLOB 传输服务器可能具有不同的传输能力。每个设备的传输能力通过以下配置选项控制：

* :kconfig:option:`CONFIG_BT_MESH_BLOB_SIZE_MAX`
* :kconfig:option:`CONFIG_BT_MESH_BLOB_BLOCK_SIZE_MIN`
* :kconfig:option:`CONFIG_BT_MESH_BLOB_BLOCK_SIZE_MAX`
* :kconfig:option:`CONFIG_BT_MESH_BLOB_CHUNK_COUNT_MAX`

:kconfig:option:`CONFIG_BT_MESH_BLOB_CHUNK_COUNT_MAX` 选项也由 BLOB 传输客户端使用，并影响 BLOB 传输客户端模型结构的内存占用。

为确保尽可能多的服务器能够接收传输，BLOB 传输客户端可以在开始传输前获取每个 BLOB 传输服务器的能力。客户端将以尽可能大的块和分块大小传输 BLOB。

.. _bluetooth_mesh_blob_transfer_modes:

传输模式
========

BLOB 可以使用两种传输模式传输：Push BLOB 传输模式和 Pull BLOB 传输模式。在大多数情况下，应使用 Push BLOB 传输模式进行传输。

在 Push BLOB 传输模式下，发送速率由 BLOB 传输客户端控制，客户端会在没有任何高层流控的情况下推送每个块的所有分块。Push BLOB 传输模式支持任意数量的目标节点，应作为默认传输模式。

在 Pull BLOB 传输模式下，BLOB 传输服务器会按自己的速率从 BLOB 传输客户端“拉取”分块。Pull BLOB 传输模式可与多个目标节点一起使用，适用于向作为 :ref:`bluetooth_mesh_lpn` 的目标节点传输 BLOB。在 Pull BLOB 传输模式下运行时，BLOB 传输服务器会小批量地向 BLOB 传输客户端请求分块，并等待这些分块全部到达后再请求更多分块。重复此过程，直到 BLOB 传输服务器收到一个块中的所有分块。随后，BLOB 传输客户端开始下一个块，BLOB 传输服务器请求该块的所有分块。


.. _bluetooth_mesh_blob_timeout:

传输超时
========

BLOB 传输的超时基于 Timeout Base 值。客户端和服务器使用相同的 Timeout Base 值，但计算超时的方式不同。

BLOB 传输服务器使用以下公式计算 BLOB 传输超时::

  10 * (Timeout Base + 1) seconds


对于 BLOB 传输客户端，使用以下公式::

  (10000 * (Timeout Base + 2)) + (100 * TTL) milliseconds

其中 TTL 是传输中设置的 time to live（生存时间）值。

API 参考
********

本节包含 BLOB 传输模型通用的类型和定义。

.. doxygengroup:: bt_mesh_blob
