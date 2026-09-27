.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _dhcpv6_interface:

DHCPv6
######

.. contents::
    :local:
    :depth: 2

概述
****

用于 IPv6 的动态主机配置协议（DHCP，Dynamic Host Configuration Protocol）是 IPv6 网络中使用的网络管理协议。DHCPv6 服务器为网络中的每台设备动态分配 IPv6 地址和其他网络配置参数，使它们能够与其他 IP 网络通信。DHCPv6 工作原理的详细概述见 `DHCPv6 Wikipedia article <https://en.wikipedia.org/wiki/DHCPv6>`_。

Zephyr 同时支持 DHCPv6 客户端和服务器功能，包括 `RFC 8415 <https://www.rfc-editor.org/rfc/rfc8415>`_ 中规定的 IPv6 前缀委派（IA_PD）。

前缀委派
********

DHCPv6 客户端可以充当 *请求路由器*：除了请求非临时地址（IA_NA）外，它还可以通过设置 :c:member:`net_dhcpv6_params.request_prefix` 来请求委派前缀（IA_PD）。委派得到的前缀会安装到请求接口上。

若要让该节点成为完整的前缀请求路由器，并向下游链路再委派前缀，请在 :c:member:`net_dhcpv6_params.downstream_ifaces` 中列出下游（LAN）接口索引，并将 :c:member:`net_dhcpv6_params.downstream_count` 设置为条目数量。每个下游接口都会从委派前缀中划分出一个不同的 ``/64`` （第 N 个接口获得第 N 个 ``/64``），随后通过路由器通告在该接口上通告，使下游主机能够使用 SLAAC 自动配置地址。该数组最多容纳 :kconfig:option:`CONFIG_NET_DHCPV6_MAX_DOWNSTREAM` 个条目；:c:member:`net_dhcpv6_params.downstream_count` 为 0 表示委派前缀仅安装在请求接口上。这需要启用 :kconfig:option:`CONFIG_NET_IPV6_ND_RA_TX` （路由器通告发送／路由器角色）；此外，若要在上游和下游接口之间转发流量，还需要启用 :kconfig:option:`CONFIG_NET_IPV6_FORWARDING`。

委派前缀必须足够短，以便为每个下游接口包含一个不同的 ``/64``，也就是说，长度为 ``L`` 的委派前缀最多可服务 ``2^(64 - L)`` 条下游链路。因此，恰好为 ``/64`` 的委派前缀只能服务一条链路，而比 ``/64`` 更长的前缀完全无法再委派。无法分配不同 ``/64`` 的下游接口会被跳过并给出警告。

DHCPv6 服务器（:kconfig:option:`CONFIG_NET_DHCPV6_SERVER`）实现 *委派路由器* 角色，从配置的地址池中分配地址和委派前缀。两种角色的完整示例见 :zephyr:code-sample:`dhcpv6-pd`。

限制
****

该实现有意省略了 RFC 8415 和 RFC 4861 允许简化处理的几项内容：

* 客户端停止时发送的 Release（:kconfig:option:`CONFIG_NET_DHCPV6_SEND_RELEASE_ON_STOP`）是尽力而为的：它只发送一次，不会像 :rfc:`8415#section-18.2.7` 中描述的那样重传 ``REL_MAX_RC`` 次。未释放的租约在到期后由服务器回收。

* 非请求路由器通告按 :kconfig:option:`CONFIG_NET_IPV6_ND_RA_TX_INTERVAL` 配置的固定间隔发送，而不是在 ``MinRtrAdvInterval`` 和 ``MaxRtrAdvInterval`` 之间的随机间隔发送；并且当接口承担路由器角色时，不会发送 ``MAX_INITIAL_RTR_ADVERTISEMENTS`` 次初始突发通告。请求通告按 :rfc:`4861#section-6.2.6` 的要求进行速率限制并随机延迟。

* 服务器通过改变所配置地址池基址的单个字节来分配地址和前缀，因此地址池条目数受限于 :kconfig:option:`CONFIG_NET_DHCPV6_SERVER_MAX_LEASES`，且 IA_PD 地址池的前缀长度必须按字节对齐。

API 参考
********

.. doxygengroup:: dhcpv6

.. doxygengroup:: dhcpv6_server
