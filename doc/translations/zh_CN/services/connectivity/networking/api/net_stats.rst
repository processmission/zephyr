.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_stats_interface:

网络统计
########

.. contents::
    :local:
    :depth: 2

概述
****

如果设置了 :kconfig:option:`CONFIG_NET_STATISTICS`，则会收集网络统计信息。如果不需要 IPv4 或 IPv6 的各组件统计信息，可以将其关闭。详情见 :zephyr_file:`subsys/net/ip/Kconfig.stats` 文件中的各个选项。

默认情况下，系统按网络接口收集网络统计信息。这可以通过 :kconfig:option:`CONFIG_NET_STATISTICS_PER_INTERFACE` 选项控制。

如果应用希望收集统计信息以便进一步处理，可以设置 :kconfig:option:`CONFIG_NET_STATISTICS_USER_API` 选项，这需要使用网络管理接口 API。详情见 :ref:`net_mgmt_interface`。

可以设置 :kconfig:option:`CONFIG_NET_STATISTICS_ETHERNET` 选项来收集通用以太网统计信息。如果设置了 :kconfig:option:`CONFIG_NET_STATISTICS_ETHERNET_VENDOR` 选项，则以太网设备驱动可以收集以太网设备特定的统计信息，并将其传给应用进行处理。

如果设置了 :kconfig:option:`CONFIG_NET_SHELL` 选项，则网络 shell 可以通过 ``net stats`` 命令显示统计信息。

API 参考
********

.. doxygengroup:: net_stats
