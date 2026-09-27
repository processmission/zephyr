.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_config_interface:

网络配置库
##########

.. contents::
    :local:
    :depth: 2

概述
****

网络配置库在系统启动期间根据用户提供的 Kconfig 选项，以半自动方式设置网络设备。

以下 Kconfig 选项会影响配置库如何设置系统：

.. csv-table:: 网络配置库的 Kconfig 选项
   :header: "选项名称", "描述"
   :widths: 45 55

   ":kconfig:option:`CONFIG_NET_CONFIG_SETTINGS`", "该选项控制是否对网络系统进行配置或初始化。如果未设置，则不会使用配置库进行初始化，应用需要自行完成所有与网络相关的配置。如果设置了该选项，用户可以选择为系统中的第一个网络接口配置静态 IP 地址。通常设置静态 IP 地址只适用于测试，不应在量产代码中使用。设置静态 IP 地址的具体选项见配置库的 Kconfig 文件 :zephyr_file:`subsys/net/lib/config/Kconfig`。"
   ":kconfig:option:`CONFIG_NET_CONFIG_AUTO_INIT`", "设备启动时会自动配置网络系统。"
   ":kconfig:option:`CONFIG_NET_CONFIG_INIT_TIMEOUT`", "该选项指定等待网络就绪可用的时长。例如，如果在该时限内未收到来自 DHCPv4 的 IPv4 地址，那么设备启动期间调用 ``net_config_init()`` 将返回错误。"
   ":kconfig:option:`CONFIG_NET_CONFIG_NEED_IPV4`", "该网络应用需要 IPv4 支持才能正常工作。该选项确保网络应用为使用 IPv4 而正确初始化。如果未启用 :kconfig:option:`CONFIG_NET_IPV4`，则设置该选项会自动启用 IPv4。"
   ":kconfig:option:`CONFIG_NET_CONFIG_NEED_IPV6`", "该网络应用需要 IPv6 支持才能正常工作。该选项确保网络应用为使用 IPv6 而正确初始化。如果未启用 :kconfig:option:`CONFIG_NET_IPV6`，则设置该选项会自动启用 IPv6。"
   ":kconfig:option:`CONFIG_NET_CONFIG_NEED_IPV6_ROUTER`", "如果启用了 IPv6，该选项表示网络应用需要存在 IPv6 路由器才能继续。实际上这意味着应用希望等到收到 IPv6 路由器通告消息后再继续。"
   ":kconfig:option:`CONFIG_NET_CONFIG_MY_IPV6_ADDR`","分配给默认网络接口的本地静态 IPv6 地址。"
   ":kconfig:option:`CONFIG_NET_CONFIG_PEER_IPV6_ADDR`","对端静态 IPv6 地址。这主要用于测试环境，此时应用可以连接到预先定义的主机。"
   ":kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_ADDR`","分配给默认网络接口的本地静态 IPv4 地址。"
   ":kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_NETMASK`","分配给该 IPv4 地址的静态 IPv4 子网掩码。"
   ":kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_GW`","分配给默认网络接口的静态 IPv4 网关地址。"
   ":kconfig:option:`CONFIG_NET_CONFIG_PEER_IPV4_ADDR`","对端静态 IPv4 地址。这主要用于测试环境，此时应用可以连接到预先定义的主机。"

用法示例
********

如果设置了 :kconfig:option:`CONFIG_NET_CONFIG_AUTO_INIT`，则配置库会在设备启动期间自动启用并运行。此时该库会自动调用 ``net_config_init()``，应用无需进行任何网络配置。

如果想使用网络配置库但不希望自动初始化，可以手动调用 ``net_config_init()``。``flags`` 参数可用于向该库提示应用在实际启动之前希望具备哪类功能。

API 参考
********

.. doxygengroup:: net_config
