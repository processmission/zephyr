.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ptp_interface:

精确时间协议（PTP）
###################

.. contents::
    :local:
    :depth: 2

概述
****

PTP 是一种在应用层实现的网络协议，用于同步计算机网络中的时钟，精度可达亚微秒级。该协议栈支持 `IEEE 1588-2019 standard`_ 中定义的协议和过程（IEEE Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems）。它具有多种配置文件，可基于 L2（以太网）或 L3（UDP/IPv4 或 UDP/IPv6）实现。其精度通过使用协议数据包的硬件时间戳来实现。

Zephyr 的 PTP 协议栈实现包含以下内容：

* 处理传入消息和事件的 PTP 协议栈线程
* 与 ptp_clock 驱动集成
* 在系统初始化期间执行的 PTP 协议栈初始化

该实现会自动创建 PTP 端口（每个 PTP 端口对应一个唯一接口）。

支持情况 features
*****************

协议栈实现并不支持标准中规定的所有功能。下表列出了所有支持的功能。

.. csv-table:: 支持的功能
   :header: 功能, Supported
   :widths: 50,10

    普通时钟, yes
    边界时钟, yes
    透明时钟,
    管理节点,
    端到端延时机制, yes
    对等延时机制, 是（两步）
    组播操作模式, yes
    混合操作模式, yes
    单播操作模式,
    非易失性存储,
    UDP IPv4 传输协议, yes
    UDP IPv6 传输协议, yes
    IEEE 802.3（以太网）传输协议, yes
    硬件时间戳, yes
    软件时间戳,
    TIME_RECEIVER_ONLY PTP 实例, yes
    TIME_TRANSMITTER_ONLY PTP 实例,

网络传输模式
************

网络传输模式通过 ``PTP_NETWORK_MODE`` Kconfig 选择项进行选择：

* 组播模式（:kconfig:option:`CONFIG_PTP_NETWORK_MODE_MULTICAST`，默认）是标准的 PTP 模式，其中所有 PTP 消息都发送到默认组播地址。这意味着每个节点都会接收所有其他节点的 ``Delay_Req`` 和 ``Delay_Resp`` 消息对，从而增加网络流量。在仅使用少量时间接收端（timeReceiver）的较小网络中，这通常不是问题。

* 混合模式（:kconfig:option:`CONFIG_PTP_NETWORK_MODE_HYBRID`）仍然将 ``Announce``、``Sync`` 和 ``Follow_Up`` 消息发送到默认组播地址，但时间接收端（timeReceiver）会将其 ``Delay_Req`` 消息以单播方式直接发送到当前时间发送端（timeTransmitter）的协议地址（对于 IEEE 802.3 传输，为 IP 地址或 MAC 地址），后者随后向发起请求的时间接收端单播回应 ``Delay_Resp``。这减少了网络上的 PTP 流量，在扩展到使用大量时间接收端的较大网络时可能是一个重要因素。混合模式仅要求网络支持从时间发送端到时间接收端的组播传输。该模式与 linuxptp 的 ``hybrid_e2e`` 选项以及 sfptpd 的 ``hybrid`` 网络模式兼容；不支持单播协商。

  如果时间发送端（timeTransmitter）连续 :kconfig:option:`CONFIG_PTP_HYBRID_FALLBACK_ATTEMPTS` 次未能应答单播 ``Delay_Req`` 消息，PTP 端口会记录错误，回退到组播延时测量，并保持在组播模式，直到选出新的时间发送端。可以使用 :kconfig:option:`CONFIG_PTP_NETWORK_MODE_HYBRID_NO_FALLBACK` 禁用回退；在这种情况下，端口将始终继续发送单播 ``Delay_Req`` 消息。

  混合模式要求使用端到端延时机制（:kconfig:option:`CONFIG_PTP_DELAY_MECHANISM_E2E`），并且在所有传输协议（UDP IPv4、UDP IPv6 和 IEEE 802.3）上均受支持。

支持的管理消息
**************

根据 IEEE 1588-2019 第 15.5.2.3 节中的表 59，支持以下管理 TLV：

.. csv-table:: 支持的管理消息 ID
   :header: Management_ID, Management_ID 名称, 允许的操作
   :widths: 10,40,25

    0x0000, NULL_PTP_MANAGEMENT, GET SET COMMAND
    0x0001, CLOCK_DESCRIPTION, GET
    0x0002, USER_DESCRIPTION, GET
    0x0003, SAVE_IN_NON_VOLATILE_STORAGE, -
    0x0004, RESET_NON_VOLATILE_STORAGE, -
    0x0005, INITIALIZE, -
    0x0006, FAULT_LOG, -
    0x0007, FAULT_LOG_RESET, -
    0x2000, DEFAULT_DATA_SET, GET
    0x2001, CURRENT_DATA_SET, GET
    0x2002, PARENT_DATA_SET, GET
    0x2003, TIME_PROPERTIES_DATA_SET, GET
    0x2004, PORT_DATA_SET, GET
    0x2005, PRIORITY1, GET SET
    0x2006, PRIORITY2, GET SET
    0x2007, DOMAIN, GET SET
    0x2008, TIME_RECEIVER_ONLY, GET SET
    0x2009, LOG_ANNOUNCE_INTERVAL, GET SET
    0x200A, ANNOUNCE_RECEIPT_TIMEOUT, GET SET
    0x200B, LOG_SYNC_INTERVAL, GET SET
    0x200C, VERSION_NUMBER, GET SET
    0x200D, ENABLE_PORT, COMMAND
    0x200E, DISABLE_PORT, COMMAND
    0x200F, TIME, GET SET
    0x2010, CLOCK_ACCURACY, GET SET
    0x2011, UTC_PROPERTIES, GET SET
    0x2012, TRACEBILITY_PROPERTIES, GET SET
    0x2013, TIMESCALE_PROPERTIES, GET SET
    0x2014, UNICAST_NEGOTIATION_ENABLE, -
    0x2015, PATH_TRACE_LIST, -
    0x2016, PATH_TRACE_ENABLE, -
    0x2017, GRANDMASTER_CLUSTER_TABLE, -
    0x2018, UNICAST_TIME_TRANSMITTER_TABLE, -
    0x2019, UNICAST_TIME_TRANSMITTER_MAX_TABLE_SIZE, -
    0x201A, ACCEPTABLE_TIME_TRANSMITTER_TABLE, -
    0x201B, ACCEPTABLE_TIME_TRANSMITTER_TABLE_ENABLED, -
    0x201C, ACCEPTABLE_TIME_TRANSMITTER_MAX_TABLE_SIZE, -
    0x201D, ALTERNATE_TIME_TRANSMITTER, -
    0x201E, ALTERNATE_TIME_OFFSET_ENABLE, -
    0x201F, ALTERNATE_TIME_OFFSET_NAME, -
    0x2020, ALTERNATE_TIME_OFFSET_MAX_KEY, -
    0x2021, ALTERNATE_TIME_OFFSET_PROPERTIES, -
    0x3000, EXTERNAL_PORT_CONFIGURATION_ENABLED,
    0x3001, TIME_TRANSMITTER_ONLY, -
    0x3002, HOLDOVER_UPGRADE_ENABLE, -
    0x3003, EXT_PORT_CONFIG_PORT_DATA_SET, -
    0x4000, TRANSPARENT_CLOCK_DEFAULT_DATA_SET, -
    0x4001, TRANSPARENT_CLOCK_PORT_DATA_SET, -
    0x4002, PRIMARY_DOMAIN, -
    0x6000, DELAY_MECHANISM, GET
    0x6001, LOG_MIN_PDELAY_REQ_INTERVAL, GET SET

时间戳说明
**********

当接收（RX）硬件时间戳不可用或无效时，同步会回退到在接收处理期间读取 PHC 时间。这可能会因帧到达与 PHC 读取之间软件处理时延（数据包路径和调度）而引入额外的抖动。

对于没有驱动提供的真实接收（RX）硬件时间戳的 L2 AF_PACKET 路径，这种行为是预期现象。

对于 IEEE 802.3 传输，Sync 以两步模式发送，Follow_Up 根据 TX 时间戳回调生成。如果 TX 时间戳缺失或延迟，协议栈会记录警告并跳过该 Sync 序列的 Follow_Up，然后在后续间隔中继续正常发送 Sync（尽力而为行为）。

可以使用 :kconfig:option:`CONFIG_PTP_DELAY_MECHANISM_P2P` 选择对等延时测量。第一种支持的 P2P 模式是两步式 ``Pdelay_Req`` / ``Pdelay_Resp`` / ``Pdelay_Resp_Follow_Up``。单步式 ``Pdelay_Resp`` 采样会被拒绝并记录日志，以供后续实现。

支持的硬件
**********

尽管协议栈本身与硬件无关，但必须在以太网驱动中启用以太网帧时间戳支持。

支持的开发板：

- :zephyr:board:`nucleo_h563zi`
- :zephyr:board:`nucleo_h743zi`
- :zephyr:board:`nucleo_h745zi_q`
- :zephyr:board:`nucleo_f767zi`
- :zephyr:board:`frdm_mcxn947`
- :zephyr:board:`native_sim` （仅可用于简单测试，由于缺少硬件时钟，功能受限）

启用协议栈
**********

必须在 :file:`prj.conf` 文件中启用以下配置选项。

- :kconfig:option:`CONFIG_PTP`

测试
****

已使用 `Linux ptp4l <https://linuxptp.sourceforge.net/>`_ 守护进程对该协议栈进行了非正式测试。还使用 :zephyr:board:`nucleo_h563zi` 和 :zephyr:board:`frdm_mcxn947` 开发板针对 GPS 时钟进行了测试，既采用直接以太网连接，也在中间使用支持 PTP 的交换机。所有测试均使用 :zephyr:code-sample:`PTP 示例应用 <ptp>` 进行，涵盖 UDP IPv4、UDP IPv6 和 IEEE 802.3 传输。

下表总结了非正式测试矩阵：

+----------------------------------+---------------+------------+------------+
|                                  | IEEE 802.3    | UDP IPv4   | UDP IPv6   |
+==================================+===============+============+============+
| ptp4l 守护进程                   | 是            | 是         | 是         |
+----------------------------------+---------------+------------+------------+
| GPS 时钟（直接连接）             | 是            | 是         | 是         |
+----------------------------------+---------------+------------+------------+
| 支持 PTP 的交换机                | 是            | 是         | 是         |
+----------------------------------+---------------+------------+------------+
| GPS 时钟 + 支持 PTP 的交换机     | 是            | 是         | 是         |
+----------------------------------+---------------+------------+------------+

对等延时测量已针对普通时钟用途实现并验证。边界时钟操作预期会共享相同的端口级 Pdelay 机制，但尚未在多端口硬件上验证。

可以使用 Zephyr 源码发行版中的 :zephyr:code-sample:`PTP 示例应用 <ptp>` 进行测试。

.. _IEEE 1588-2019 standard:
   https://standards.ieee.org/ieee/1588/6825/

API 参考
********

.. doxygengroup:: ptp
