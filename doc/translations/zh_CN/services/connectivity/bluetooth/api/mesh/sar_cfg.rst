.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_sar_cfg:

分段与重组（SAR）
#################

分段与重组（SAR）提供了一种在 Mesh 网络中处理较大上层传输层消息的方式，目的是提升 Bluetooth Mesh 吞吐量。分段与重组机制由下层传输层使用。

下层传输层定义了如何将上层传输层 PDU 分段并重组为多个下层传输 PDU，并将它们发送到对端设备的下层传输层。如果上层传输 PDU 能够容纳，则会通过单个下层传输 PDU 发送。对于无法容纳在单个下层传输 PDU 中的较长数据包，下层传输层会执行分段，将上层传输 PDU 拆分为多个段。

接收设备上的下层传输层在将消息向上层协议栈传递之前，会将这些段重组为单个上层传输 PDU。分段消息的送达由接收节点的下层传输层进行确认，而非分段消息的送达则不确认。不过，当需要下层传输层确认时，能够容纳在单个下层传输 PDU 中的上层传输 PDU 也可以作为单段分段消息发送。设置 ``send rel`` 标志（参见 :c:struct:`bt_mesh_msg_ctx`）以使用可靠消息传输并确认单段分段消息。

传输层能够通过其 SAR 机制传输最多 32 个段，最大消息（PDU）大小为 384 个八位字节。要为 Bluetooth Mesh 协议栈配置消息大小，请使用以下 Kconfig 选项：

* :kconfig:option:`CONFIG_BT_MESH_RX_SEG_MAX` 用于设置传入消息中的最大段数。
* :kconfig:option:`CONFIG_BT_MESH_TX_SEG_MAX` 用于设置传出消息中的最大段数。

Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_TX_SEG_MSG_COUNT` 和 :kconfig:option:`CONFIG_BT_MESH_RX_SEG_MSG_COUNT` 定义可以同时处理多少条传出和传入分段消息。当向同一目的地发送多条分段消息时，这些消息会排队并一次发送一条。

传入和传出分段消息共享同一个段分配池。该池大小通过 :kconfig:option:`CONFIG_BT_MESH_SEG_BUFS` Kconfig 选项配置。传入和传出消息在事务开始时分配段。传出分段消息在接收方确认后逐个释放其段，而传入消息则在消息完全接收后才释放段。定义缓冲区大小时请记住这一点。

SAR 不会给每个段的访问层有效载荷带来额外开销。

分段与重组（SAR）配置模型
*************************

借助 Bluetooth Mesh Protocol Specification 1.1 版，可以使用 SAR 配置模型通过 Mesh 网络配置 SAR 行为，例如间隔、定时器和重传计数器：

* :ref:`bluetooth_mesh_sar_cfg_cli`
* :ref:`bluetooth_mesh_sar_cfg_srv`

无论节点上是否存在 SAR 配置服务器，以下 SAR 行为都适用。

段的传输由段传输间隔分隔（参见 `SAR Segment Interval Step`_ 状态）。可用于分段和重组的其他可配置时间间隔和延迟包括：

* 单播重传之间的间隔（参见 `SAR Unicast Retransmissions Interval Step`_ 和 `SAR Unicast Retransmissions Interval Increment`_ 状态）。
* 组播重传之间的间隔（参见 `SAR Multicast Retransmissions Interval Step`_ 状态）。
* 段接收间隔（参见 `SAR Receiver Segment Interval Step`_ 状态）。
* 确认延迟增量（参见 `SAR Acknowledgment Delay Increment`_ 状态）。

当标记为未确认的最后一个段被传输后，下层传输层会启动重传定时器。SAR 单播重传定时器的初始值取决于消息 TTL 字段的值。如果 TTL 字段值大于 ``0``，则定时器初始值按以下公式设置：

.. math::

   unicast~retransmissions~interval~step + unicast~retransmissions~interval~increment \times (TTL - 1)


如果 TTL 字段值为 ``0``，则定时器初始值设置为单播重传间隔步长。

SAR 组播重传定时器的初始值设置为组播重传间隔。

当下层传输层接收到消息段时，会启动 SAR 丢弃定时器。丢弃定时器指示下层传输层在丢弃该段所属的分段消息之前等待多长时间。SAR 丢弃定时器的初始值为 `SAR Discard Timeout`_ 状态所指示的丢弃超时值。

SAR 确认定时器保存收到段后发送 Segment Acknowledgment 消息之前的等待时间。SAR 确认定时器的初始值使用以下公式计算：

.. math::

   min(SegN + 0.5 , acknowledgment~delay~increment) \times segment~reception~interval


``SegN`` 字段值标识上层传输 PDU 被分成的总段数。

有四个计数器与 SAR 行为相关：

* 两个单播重传计数（参见 `SAR Unicast Retransmissions Count`_ 状态和 `SAR Unicast Retransmissions Without Progress Count`_ 状态）
* 组播重传计数（参见 `SAR Multicast Retransmissions Count`_ 状态）
* 确认重传计数（参见 `SAR Acknowledgment Retransmissions Count`_ 状态）

如果传输中的段数高于 `SAR Segments Threshold`_ 状态的值，则使用 `SAR Acknowledgment Retransmissions Count`_ 状态的值重传 Segment Acknowledgment 消息。

.. _bt_mesh_sar_cfg_states:

SAR 状态
********

有两个与分段和重组相关的状态：

* SAR 发送器状态
* SAR 接收器状态

SAR 发送器状态是一个复合状态，控制分段消息的传输次数和时机。它包括以下状态：

* SAR Segment Interval Step
* SAR Unicast Retransmissions Count
* SAR Unicast Retransmissions Without Progress Count
* SAR Unicast Retransmissions Interval Step
* SAR Unicast Retransmissions Interval Increment
* SAR Multicast Retransmissions Count
* SAR Multicast Retransmissions Interval Step

SAR 接收器状态是一个复合状态，控制 Segment Acknowledgment 传输的次数和时机，以及分段消息重组的丢弃。它包括以下状态：

* SAR Segments Threshold
* SAR Discard Timeout
* SAR Acknowledgment Delay Increment
* SAR Acknowledgment Retransmissions Count
* SAR Receiver Segment Interval Step

SAR Segment Interval Step
=========================

SAR Segment Interval Step 状态保存一个值，用于控制分段消息各段传输之间的间隔。该间隔以毫秒为单位。

使用 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_SEG_INT_STEP` Kconfig 选项设置默认值。然后使用以下公式计算段传输间隔：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_SEG\_INT\_STEP} + 1) \times 10~\text{ms}


SAR Unicast Retransmissions Count
=================================

SAR Unicast Retransmissions Count 保存一个值，定义分段消息向单播目的地重传的最大次数。使用 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_COUNT` Kconfig 选项设置该状态的默认值。

SAR Unicast Retransmissions Without Progress Count
==================================================

该状态保存一个值，定义分段消息向单播地址重传的最大次数；如果在超时期间未收到确认，或收到包含已确认段的确认，则会发送这些重传。使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_WITHOUT_PROG_COUNT` 设置最大重传次数。

SAR Unicast Retransmissions Interval Step
=========================================

该状态的值控制用于延迟向单播地址重传分段消息中未确认段的间隔步长。该间隔步长以毫秒为单位。

使用 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_INT_STEP` Kconfig 选项设置默认值。然后使用以下公式计算间隔步长：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_UNICAST\_RETRANS\_INT\_STEP} + 1) \times 25~\text{ms}


SAR Unicast Retransmissions Interval Increment
==============================================

SAR Unicast Retransmissions Interval Increment 保存一个值，用于控制延迟向单播地址重传分段消息中未确认段时使用的间隔增量。该增量以毫秒为单位。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_INT_INC` 设置默认值。Kconfig 选项值用于按以下公式计算增量：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_UNICAST\_RETRANS\_INT\_INC} + 1) \times 25~\text{ms}


SAR Multicast Retransmissions Count
===================================

该状态保存一个值，控制分段消息向组播地址重传的总次数。使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_MULTICAST_RETRANS_COUNT` 设置总重传次数。

SAR Multicast Retransmissions Interval Step
===========================================

该状态保存一个值，控制分段消息中所有段向组播地址重传之间的间隔。该间隔以毫秒为单位。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_MULTICAST_RETRANS_INT` 设置默认值，该值用于按以下公式计算间隔：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_MULTICAST\_RETRANS\_INT} + 1) \times 25~\text{ms}


SAR Discard Timeout
===================

该状态的值定义下层传输层在接收到分段消息的段之后，等待多少秒才丢弃该分段消息。使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_DISCARD_TIMEOUT` 设置默认值。丢弃超时将使用以下公式计算：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_RX\_DISCARD\_TIMEOUT} + 1) \times 5~\text{seconds}


SAR Acknowledgment Delay Increment
==================================

该状态保存一个值，控制收到新段后延迟发送确认消息所用间隔的延迟增量。该增量以段数为单位。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_DELAY_INC` 设置默认值。增量值计算为 :math:`\verb|CONFIG_BT_MESH_SAR_RX_ACK_DELAY_INC| + 1.5`。

SAR Segments Threshold
======================

SAR Segments Threshold 状态保存一个值，定义用于确认重传的分段消息段数阈值。使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_THRESHOLD` 设置阈值。

当分段消息的段数高于此阈值时，协议栈会额外将每条确认消息重传 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT` 值所指定的次数。

SAR Acknowledgment Retransmissions Count
========================================

SAR Acknowledgment Retransmissions Count 状态控制下层传输层发送的 Segment Acknowledgment 消息的重传次数。它给出当分段消息中的段数高于 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_THRESHOLD` 值时，协议栈将额外发送的确认消息重传总次数。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT` 设置该状态的默认值。Segment Acknowledgment 消息的最大传输次数为 :math:`\verb|CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT| + 1`。

SAR Receiver Segment Interval Step
==================================

SAR Receiver Segment Interval Step 定义用于收到新段后延迟发送确认消息的段接收间隔步长。该间隔以毫秒为单位。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_INT_STEP` 设置默认值，并使用以下公式计算间隔：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_RX\_SEG\_INT\_STEP} + 1) \times 10~\text{ms}
