.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_dplpmtud:

数据报 PLPMTUD API
##################

.. contents::
    :local:
    :depth: 2

概述
****

Zephyr 基于 :rfc:`8899` 提供通用的 **数据报分组层路径 MTU 发现** （DPLPMTUD）实现。它面向基于 UDP 的传输协议（QUIC、基于 UDP 的 CoAP、自定义协议），这些协议必须在不依赖本地 IP 分片的情况下发现数据报载荷可以达到多大。

该子系统按如下方式划分职责：

**通用协议栈** （``subsys/net/ip/dplpmtud.c``）

* 每个目标的搜索状态：已验证的 PLPMTU、探测大小、重试次数、上下界
* 在基础 PLPMTU（1200 字节）与路径上限之间进行二分查找
* 与现有的 PMTU 目标缓存集成（输入 ICMP PTB，输出已验证的大小）
* 当 PMTU 缓存报告的 MTU 低于基础 PLPMTU 时进行黑洞处理

**传输层使用方**

* 按照 :c:func:`net_dplpmtud_get_path_probe_size()` 返回的大小构造探测数据报
* 在启用“不分片”的情况下发送探测包（见 :ref:`ip_socket_options` 以及 :c:macro:`ZSOCK_IP_DONTFRAG` / :c:macro:`ZSOCK_IPV6_DONTFRAG`）
* 将传输层的 ACK/丢失映射到 :c:func:`net_dplpmtud_on_path_probe_acked()` 和 :c:func:`net_dplpmtud_on_path_probe_lost()`

:ref:`QUIC <quic_dplpmtud>` 是树内的首个使用方。其他传输协议可以使用同一套 API，而无需重复实现 RFC 8899 状态机。

配置
****

按地址族启用 DPLPMTUD：

* IPv4 使用 :kconfig:option:`CONFIG_NET_IPV4_PMTU` 和 :kconfig:option:`CONFIG_NET_IPV4_PMTU_DPLPMTUD`
* IPv6 使用 :kconfig:option:`CONFIG_NET_IPV6_PMTU` 和 :kconfig:option:`CONFIG_NET_IPV6_PMTU_DPLPMTUD`

两个地址族都还需要 :kconfig:option:`CONFIG_NET_UDP`。启用任一地址族选项时，都会选中总括选项 :kconfig:option:`CONFIG_NET_PMTU_DPLPMTUD`。

基于 ICMP 的 PMTU 缩减（数据包过大）仍可通过 :kconfig:option:`CONFIG_NET_IPV4_PMTU_PTB` 和 :kconfig:option:`CONFIG_NET_IPV6_PMTU_PTB` 使用。DPLPMTUD 是 PTB 的补充：当路径允许时，它会主动探测更大的长度。

同时跟踪的路径数量分别取决于 :kconfig:option:`CONFIG_NET_IPV4_PMTU_DESTINATION_CACHE_ENTRIES` 和 :kconfig:option:`CONFIG_NET_IPV6_PMTU_DESTINATION_CACHE_ENTRIES`。

使用模型
********

为每个远端目标初始化一个 :c:struct:`net_dplpmtud_path` （或者在连接的整个生命周期内复用该句柄）：

.. code-block:: c

   struct net_dplpmtud_path path;
   uint16_t max_plpmtu = 1452U; /* transport / peer limit, or 0 if uncapped */
   int mtu;
   int probe;
   int ret;

   ret = net_dplpmtud_init_path(&path, &remote_addr, max_plpmtu);
   if (ret < 0) {
       /* handle error */
   }

   mtu = net_dplpmtud_get_path_mtu(&path);
   if (mtu < 0) {
       mtu = NET_DPLPMTUD_BASE_PLPMTU;
   }

   /* Application data must fit in @a mtu bytes (transport framing excluded). */

探测生命周期：

1. 调用 :c:func:`net_dplpmtud_get_path_probe_size()`。返回值为 ``0`` 表示无需探测。该路径必须已经初始化；getter 不会创建缓存条目。
2. 如果 :c:func:`net_dplpmtud_path_probe_in_flight()` 为假，则以该大小构造并发送一个启用了“不分片”的探测数据报（使用 socket 选项，或在 :c:func:`zsock_sendmsg()` 中按数据报传递控制消息）。
3. 调用 :c:func:`net_dplpmtud_on_path_probe_sent()` 在通用状态机中登记该探测包，然后发送该探测数据报。
4. 如果发送失败，请调用 :c:func:`net_dplpmtud_on_path_probe_lost()`，使核心与传输层的状态保持一致。
5. 在传输层确认时，调用 :c:func:`net_dplpmtud_on_path_probe_acked()` 或 :c:func:`net_dplpmtud_on_path_probe_lost()`。

当传输层得知新的上限时（例如 QUIC 的 ``max_udp_payload_size`` 传输参数），调用 :c:func:`net_dplpmtud_set_path_max_plpmtu()` 更新该值。

如果传输层检测到与 ICMP 无关的黑洞，请调用 :c:func:`net_dplpmtud_note_path_blackhole()`。低于基础 PLPMTU 的 PTB 更新会通过 PMTU 缓存自动应用。

API 参考
********

.. doxygengroup:: net_dplpmtud
