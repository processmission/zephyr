.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_pkt_filter_interface:

网络数据包过滤
##############

.. contents::
    :local:
    :depth: 2

概述
****

网络数据包过滤设施提供了构建自定义规则的基础设施，用于接受和/或拒绝数据包的发送与接收。它还允许修改传入网络数据包的优先级。这可用于创建基本防火墙、控制网络流量等。

必须设置 :kconfig:option:`CONFIG_NET_PKT_FILTER` 才能启用相关 API。

发送路径和接收路径都可以有一个过滤器规则列表。每条规则由一组条件和数据包处理结果组成。每个数据包都要接受规则所附条件的检查。当某条规则的所有条件都为真时，数据包的处理结果会立即按当前规则确定，不再考虑后续规则。如果有一个条件为假，则考虑列表中的下一条规则。

数据包处理结果可以是 ``NET_OK`` （接受数据包）、 ``NET_DROP`` （丢弃数据包）或 ``NET_CONTINUE`` （动态修改其优先级）。

当结果为 ``NET_CONTINUE`` 时，优先级会被更新，但最终结果尚未确定，处理会继续进行。如果多条规则的所有条件都为真，则数据包会获得最后考虑的那条规则的优先级。

规则由 :c:struct:`npf_rule` 对象表示。可以使用 :c:func:`npf_insert_rule()` 、 :c:func:`npf_append_rule()` 和 :c:func:`npf_remove_rule()` 将其插入、追加到或从 :c:struct:`npf_rule_list` 对象所包含的规则列表中移除。

网络协议栈的不同层有各自的规则集。有些规则适用于 L2 层（如以太网），有些适用于处理 IPv4 或 IPv6 协议的 L3 层。``local_in`` 规则用于匹配传入的协议类型，例如基于 IPv4 或 IPv6 运行的 UDP 或 TCP 数据包。不同层的规则支持情况可由下文提到的相关 Kconfig 选项控制。

* ``npf_send_rules`` 是应用于 L2 层传出数据包的规则列表
* ``npf_recv_rules`` 是应用于 L2 层传入数据包的规则列表
* ``npf_ipv4_recv_rules`` 是应用于传入 IPv4 数据包的规则列表。可通过 :kconfig:option:`CONFIG_NET_PKT_FILTER_IPV4_HOOK` 选项启用或禁用。
* ``npf_ipv6_recv_rules`` 是应用于传入 IPv6 数据包的规则列表。可通过 :kconfig:option:`CONFIG_NET_PKT_FILTER_IPV6_HOOK` 选项启用或禁用。
* ``npf_local_in_recv_rules`` 是应用于传入 UDP 或 TCP 数据包的规则列表。可通过 :kconfig:option:`CONFIG_NET_PKT_FILTER_LOCAL_IN_HOOK` 选项启用或禁用。

如果过滤器规则列表为空，则假定为 ``NET_OK`` 。如果非空规则列表执行到末尾，则假定为 ``NET_DROP`` 。不过，建议始终使用显式默认终止规则（ ``npf_default_ok`` 或 ``npf_default_drop`` ）终止非空规则列表。

规则条件由 :c:struct:`npf_test` 表示。当特定条件需要额外测试数据时，可将该结构体嵌入更大的结构体中。此类条件的测试函数需要从提供的 ``npf_test`` 结构体指针中获取外层结构体。

在 :zephyr_file:`include/zephyr/net/net_pkt_filter.h` 中提供了便捷宏，用于为各种条件静态定义条件实例，还提供了 :c:macro:`NPF_RULE()` 和 :c:macro:`NPF_PRIORITY()` 来创建具有即时处理结果或优先级变更的规则实例。

另请参见 :zephyr:code-sample:`net-pkt-filter` 示例，了解如何创建和管理数据包过滤器。net shell 提供了 ``net filter`` 命令，可用于在运行时查看已安装的规则。

示例
****

以下是一个用法示例：

.. code-block:: c

    static NPF_SIZE_MAX(maxsize_200, 200);
    static NPF_ETH_TYPE_MATCH(ip_packet, NET_ETH_PTYPE_IP);

    static NPF_RULE(small_ip_pkt, NET_OK, ip_packet, maxsize_200);

    void install_my_filter(void)
    {
        npf_insert_recv_rule(&npf_default_drop);
        npf_insert_recv_rule(&small_ip_pkt);
    }

上述配置会接受 200 字节或更小的 IP 数据包，并丢弃所有其他数据包。

另一种（效率较低）实现相同结果的方式是：

.. code-block:: c

    static NPF_SIZE_MIN(minsize_201, 201);
    static NPF_ETH_TYPE_UNMATCH(not_ip_packet, NET_ETH_PTYPE_IP);

    static NPF_RULE(reject_big_pkts, NET_DROP, minsize_201);
    static NPF_RULE(reject_non_ip, NET_DROP, not_ip_packet);

    void install_my_filter(void) {
        npf_append_recv_rule(&reject_big_pkts);
        npf_append_recv_rule(&reject_non_ip);
        npf_append_recv_rule(&npf_default_ok);
    }

此示例为不同的网络流量分配优先级。它为 ``ptp`` 数据包分配网络控制优先级（ ``NET_PRIORITY_NC`` ），为第 6 版互联网流量分配关键应用优先级（ ``NET_PRIORITY_CA`` ），为第 4 版互联网协议流量分配优良尽力优先级（ ``NET_PRIORITY_EE`` ），并为 ``lldp`` 和 ``arp`` 分配最低的后台优先级（ ``NET_PRIORITY_BK`` ）。

只有在项目配置中通过 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` 启用多个流量类别队列时，优先级规则才真正有用。数据包优先级到流量类别队列的映射依据 802.1Q 标准，并取决于 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` 。

.. code-block:: c

    static NPF_ETH_TYPE_MATCH(is_arp, NET_ETH_PTYPE_ARP);
    static NPF_ETH_TYPE_MATCH(is_lldp, NET_ETH_PTYPE_LLDP);
    static NPF_ETH_TYPE_MATCH(is_ptp, NET_ETH_PTYPE_PTP);
    static NPF_ETH_TYPE_MATCH(is_ipv4, NET_ETH_PTYPE_IP);
    static NPF_ETH_TYPE_MATCH(is_ipv6, NET_ETH_PTYPE_IPV6);

    static NPF_PRIORITY(priority_bk, NET_PRIORITY_BK, is_arp, is_lldp);
    static NPF_PRIORITY(priority_ee, NET_PRIORITY_EE, is_ipv4);
    static NPF_PRIORITY(priority_ca, NET_PRIORITY_CA, is_ipv6);
    static NPF_PRIORITY(priority_nc, NET_PRIORITY_NC, is_ptp);

    void install_my_filter(void) {
        npf_append_recv_rule(&priority_bk);
        npf_append_recv_rule(&priority_ee);
        npf_append_recv_rule(&priority_ca);
        npf_append_recv_rule(&priority_nc);
        npf_append_recv_rule(&npf_default_ok);
    }

API 参考
********

.. doxygengroup:: net_pkt_filter

.. doxygengroup:: npf_basic_cond

.. doxygengroup:: npf_eth_cond
