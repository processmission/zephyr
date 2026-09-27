.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ppp:

点对点协议（PPP）支持
#####################

.. contents::
    :local:
    :depth: 2

概述
****

`Point-to-Point Protocol <https://en.wikipedia.org/wiki/Point-to-Point_Protocol>`_ （PPP）是一种数据链路层（第 2 层）通信协议，用于在两个节点之间建立直接连接。由于 IP 数据包无法在没有某种数据链路协议的情况下通过调制解调器线路传输，PPP 被用于多种串行链路。

在 Zephyr 中，每条 PPP 链路都建模为一个网络接口。这与 Linux 实现 PPP 的方式类似。

必须通过设置 :kconfig:option:`CONFIG_NET_L2_PPP` 选项在编译时启用 PPP 支持。PPP 实现仅支持以下协议：

* LCP（链路控制协议，:rfc:`1661`）
* HDLC（高级数据链路控制，:rfc:`1662`）
* IPCP（IP 控制协议，:rfc:`1332`）
* IPV6CP（IPv6 控制协议，:rfc:`5072`）

关于将 PPP 与蜂窝调制解调器配合使用，更多信息见 :zephyr:code-sample:`cellular-modem` 示例。

测试
****

有关如何针对 Linux 中运行的 pppd 测试 Zephyr PPP 的更多细节，请参见 `net-tools README`_ 文件。

.. _net-tools README:
   https://github.com/zephyrproject-rtos/net-tools/blob/master/README.md#ppp-connectivity
