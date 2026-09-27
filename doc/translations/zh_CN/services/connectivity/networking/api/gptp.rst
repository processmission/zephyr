.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _gptp_interface:

通用精确时间协议（generic Precision Time Protocol，gPTP）
#########################################################

.. contents::
    :local:
    :depth: 2

概述
****

该 gPTP 协议栈支持 `IEEE 802.1AS-2011 standard`_ 中定义的协议和过程（桥接局域网中时间敏感应用的定时与同步）。

支持的功能
**********

该协议栈处理 `IEEE 802.1AS-2011 standard`_ 中定义的通信和状态机。支持标准附录 A 中规定的全双工点对点链路端点强制要求。

该协议栈原则上能够处理多个网络接口（标准中也称为“端口”）上的通信，从而充当 802.1AS 网桥。然而，这种工作模式尚未在 Zephyr OS 上验证。

该协议栈还可以在遵循 IEEE 802.1AS 汽车配置文件、不交换 Announce 消息的网络上作为静态配置的时间接收端运行。请参阅下文的 `静态时间接收端操作`_。

支持的硬件
**********

尽管协议栈本身与硬件无关，但必须在以太网驱动中启用以太网帧时间戳支持。

支持的开发板：

- :zephyr:board:`frdm_k64f`
- :zephyr:board:`nucleo_h743zi`
- :zephyr:board:`nucleo_h745zi_q`
- :zephyr:board:`nucleo_f767zi`
- :zephyr:board:`sam_e70_xplained`
- :zephyr:board:`native_sim` （仅可用于简单测试，由于缺少硬件时钟，功能受限）
- :zephyr:board:`qemu_x86` （模拟环境，由于缺少硬件时钟，功能受限）

启用协议栈
**********

必须在 :file:`prj.conf` 文件中启用以下配置选项。

- :kconfig:option:`CONFIG_NET_GPTP`

静态时间接收端操作
******************

按照 IEEE 802.1AS 汽车配置文件（AVnu“Automotive Ethernet AVB Functional and Interoperability Specification”）构建的网络使用静态端口角色，而不是最佳主时钟算法（BMCA）。此类网络上的网桥会发送 Sync 和 Follow_Up 消息，但不发送 Announce 消息，也不需要在其时间发送端（timeTransmitter）端口上应答 Pdelay 请求。默认协议栈无法与这样的网桥同步：如果没有收到 Announce，端口永远不会进入时间接收端（“从节点”）角色。

启用 :kconfig:option:`CONFIG_NET_GPTP_STATIC_TIME_RECEIVER` 会将节点配置为静态配置的时间接收端：绕过 BMCA 和所有 Announce 处理，所有端口都固定为时间接收端角色，强制设置 asCapable，因此同步不依赖于 Pdelay 测量，本地时钟仅根据接收到的 Sync 和 Follow_Up 消息进行校准。即使设置了 :kconfig:option:`CONFIG_NET_GPTP_GM_CAPABLE` 选项，该节点也永远不会成为 grandmaster（主时钟），并且绝不会发送 Sync 或 Announce 消息。这与 linuxptp ptp4l 的汽车时间接收端配置一致（BMCA “noop”、clientOnly、inhibit_announce、asCapable “true”、ignore_source_id）。以这种方式禁用 BMCA 在标准中的对应做法是 IEEE 802.1AS-2020 的外部端口配置（第 10.3.14 条，源自 IEEE 1588-2019 第 17.6.2 条）。

应用接口
********

以下标准第 9 节中定义的应用接口可用：

- ``ClockSourceTime`` 接口（:c:func:`gptp_clk_src_time_invoke`）
- ``ClockTargetPhaseDiscontinuity`` 接口（:c:func:`gptp_register_phase_dis_cb`）
- ``ClockTargetEventCapture`` 接口（:c:func:`gptp_event_capture`）

测试
****

该协议栈已使用 `OpenAVnu gPTP <https://github.com/AVnu/gptp>`_ 和 `Linux ptp4l <https://linuxptp.sourceforge.net/>`_ 守护进程进行了非正式测试。可以使用 Zephyr 源码发行版中的 :zephyr:code-sample:`gPTP 示例应用 <gptp>` 进行测试。

.. _IEEE 802.1AS-2011 standard:
   https://standards.ieee.org/findstds/standard/802.1AS-2011.html

API 参考
********

.. doxygengroup:: gptp
