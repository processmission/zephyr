.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _dns_resolve_interface:

DNS 解析
########

.. contents::
    :local:
    :depth: 2

概述
****

DNS 解析器根据 :rfc:`1035` 实现了一个基本的 DNS 解析器。支持的 DNS 应答类型为 IPv4/IPv6 地址和 CNAME。

如果收到 CNAME，DNS 解析器会再发起一次 DNS 查询。附加查询的次数由 :kconfig:option:`CONFIG_DNS_RESOLVER_ADDITIONAL_QUERIES` Kconfig 变量控制。

通过设置 :kconfig:option:`CONFIG_MDNS_RESOLVER` Kconfig 选项，可以启用多播 DNS（mDNS）客户端解析器支持。有关 mDNS 的更多细节见 :rfc:`6762`。

通过设置 :kconfig:option:`CONFIG_LLMNR_RESOLVER` Kconfig 变量，可以启用链路本地多播名称解析（LLMNR）客户端解析器支持。有关 LLMNR 的更多细节见 :rfc:`4795`。

有关 DNS 配置变量的更多信息，请参见 :zephyr_file:`subsys/net/lib/dns/Kconfig`。DNS 解析器 API 位于 :zephyr_file:`include/zephyr/net/dns_resolve.h`。

:rfc:`6763` 中描述的基于 DNS 的服务发现查询可通过 :c:func:`dns_resolve_service` API 完成。返回的服务描述会传给用户提供的回调，该 API 会将地址族设置为 :c:macro:`AF_LOCAL`，以表明该值不是 IPv4 或 IPv6 地址，而是服务描述。

示例：

.. code-block:: c

   #include <zephyr/net/dns_resolve.h>

   #define MAX_STR_LEN CONFIG_DNS_RESOLVER_MAX_NAME_LEN

   static void dns_result_cb(enum dns_resolve_status status,
                             struct dns_addrinfo *info,
                             void *user_data)
   {
        if (status == DNS_EAI_CANCELED) {
                /* dns: Timeout while resolving name */
                return;
        }

        if (status == DNS_EAI_INPROGRESS && info) {
                char str[MAX_STR_LEN + 1];

                if (info->ai_family == NET_AF_INET) {
                        net_addr_ntop(NET_AF_INET,
                                      &net_sin(&info->ai_addr)->sin_addr,
                                      str, NET_IPV4_ADDR_LEN);
                } else if (info->ai_family == NET_AF_INET6) {
                        net_addr_ntop(NET_AF_INET6,
                                      &net_sin6(&info->ai_addr)->sin6_addr,
                                      str, NET_IPV6_ADDR_LEN);
                } else if (info->ai_family == AF_LOCAL) {
                        /* service discovery */
                        memset(str, 0, MAX_STR_LEN);
                        memcpy(str, info->ai_canonname,
                               MIN(info->ai_addrlen, MAX_STR_LEN));
                } else {
                        strncpy(str, "Invalid proto family", MAX_STR_LEN + 1);
                }

                str[MAX_STR_LEN] = '\0';

                printk("dns: %s\n", str);
                return;
        }

        if (status == DNS_EAI_ALLDONE) {
                printk("dns: All results received\n");
                return;
        }

        if (status == DNS_EAI_FAIL) {
                printk("dns: No such name found.\n");
                return;
        }

        printk("dns: Unhandled status %d received (errno %d)\n", status, errno);
   }

   #define DNS_TIMEOUT (MSEC_PER_SEC * 5) /* in ms */

   static void discover_service(void)
   {
        int ret = dns_resolve_service(dns_resolve_get_default(),
                                      "_http._tcp.dns-sd.org",
                                      NULL, dns_result_cb,
                                      NULL, DNS_TIMEOUT);
        ...
   }

上述查询会返回类似如下的输出：

.. code-block: console

    Query for '_http._tcp.dns-sd.org' sent.
    dns: . * cnn, world news._http._tcp.dns-sd.org
    dns: .source de télévision, département de langues._http._tcp.dns-sd.org
    dns: . * multicast dns._http._tcp.dns-sd.org
    dns: . * amazon.com, on-line shopping._http._tcp.dns-sd.org
    dns: . * google, searching the web._http._tcp.dns-sd.org
    dns: . * ebay, online auctions._http._tcp.dns-sd.org
    dns: . * apple, makers of the ipod._http._tcp.dns-sd.org
    dns: . * yahoo, maps, weather, and stock quotes._http._tcp.dns-sd.org
    dns: .about bonjour in web browsers._http._tcp.dns-sd.org
    dns: .π._http._tcp.•bullets•.dns-sd.org
    dns: . * dns service discovery._http._tcp.dns-sd.org
    dns: . * wired, technology, culture, business, politics._http._tcp.dns-sd.org
    dns: . * slashdot, news for nerds, stuff that matters._http._tcp.dns-sd.org
    dns: . * bbc, world news._http._tcp.dns-sd.org
    dns: .stuart’s printer._http._tcp.dns-sd.org
    dns: . * zeroconf._http._tcp.dns-sd.org
    dns: All results received

由于服务发现查询可能返回长字符串，且数据包可能很大，可能需要调整以下 Kconfig 选项：

- :kconfig:option:`CONFIG_DNS_RESOLVER_MAX_ANSWER_SIZE`：该选项指定应答的最大长度，典型取值可以是 1024，默认值为 512 字节。

- :kconfig:option:`CONFIG_DNS_RESOLVER_MAX_NAME_LEN`：该选项指定返回名称的最大长度。具体取值取决于预期的数据大小，典型取值可能是 128 字节。

网络管理事件
************

DNS 解析器会引发以下 :c:macro:`NET_MGMT_EVENT` 事件：

- :c:macro:`NET_EVENT_DNS_SERVER_ADD`：向解析器添加了一个 DNS 服务器槽位。每个槽位引发一次，事件载荷为发起该操作的接口。
- :c:macro:`NET_EVENT_DNS_SERVER_DEL`：删除了一个 DNS 服务器槽位，事件载荷为发起该操作的接口。
- :c:macro:`NET_EVENT_DNS_SERVERS_RECONFIGURED`：通过 :c:func:`dns_resolve_reconfigure` 或 :c:func:`dns_resolve_reconfigure_with_interfaces` 刷新了 DNS 服务器配置。每次成功调用都会引发，无论各个服务器槽位是否真的发生了变化，iface 为 ``NULL`` （系统级事件）。

``ADD`` 和 ``DEL`` 是 *增量* 事件：当使用与现有服务器集合相同的集合调用 :c:func:`dns_resolve_reconfigure` 时，``ADD`` 和 ``DEL`` 都不会触发——解析器有意抑制它们，以避免在 DHCP offer 重传和 IPv6 RA 时取消正在进行的查询。如果使用方在网络事件之后需要一个“DNS 配置已再次就绪”的门控（例如在 PPP 接口重新建立并在每次 PM 恢复周期通过 IPCP 推送相同 DNS 服务器之后），应监听 ``NET_EVENT_DNS_SERVERS_RECONFIGURED`` 而不是 ``NET_EVENT_DNS_SERVER_ADD``。

用法示例
********

详见 :zephyr:code-sample:`dns-resolve` 示例应用。

API 参考
********

.. doxygengroup:: dns_resolve
