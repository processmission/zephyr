.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_hostname_interface:

主机名配置
##########

.. contents::
    :local:
    :depth: 2

概述
****

联网设备可能需要一个主机名，例如当设备被配置为 mDNS 响应者（详情见 :ref:`dns_resolve_interface`）并且需要响应 ``<hostname>.local`` DNS 查询时。

必须设置 :kconfig:option:`CONFIG_NET_HOSTNAME_ENABLE` 才能存储主机名并启用相关 API。如果启用了该选项，则默认主机名由 :kconfig:option:`CONFIG_NET_HOSTNAME` 选项设置为 ``zephyr``。

如果用同一固件映像烧录多块开发板，那么在所有开发板上使用相同的主机名并不实际。此时可以启用 :kconfig:option:`CONFIG_NET_HOSTNAME_UNIQUE`，它会在主机名后添加一个唯一后缀。默认情况下，使用第一个网络接口的链路本地地址作为后缀。在以太网中，链路本地地址指的是 MAC 地址。例如，如果链路本地地址是 ``01:02:03:04:05:06``，那么唯一主机名可以是 ``zephyr010203040506``。如果希望自行设置前缀，请在创建网络接口之前调用 ``net_hostname_set_postfix_str()``；如果希望前缀采用十六进制转换，则调用 ``net_hostname_set_postfix()``。例如对于以太网，初始化优先级由 :kconfig:option:`CONFIG_ETH_INIT_PRIORITY` 设置，因此需要在该优先级之前设置后缀。后缀只能设置一次。

API 参考
********

.. doxygengroup:: net_hostname
