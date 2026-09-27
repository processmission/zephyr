.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_if_interface:

网络接口
########

.. contents::
    :local:
    :depth: 2

概述
****

网络接口是连接网络设备驱动与网络协议栈上层的枢纽。所有发送和接收的数据都通过网络接口传输。网络接口不能在运行时创建。一个特殊的链接器段将包含这些接口的信息，该段在链接时填充。

网络接口由 ``NET_DEVICE_INIT()`` 宏创建。对于以太网网络，应改用 ``ETH_NET_DEVICE_INIT()`` 宏，因为启用 :kconfig:option:`CONFIG_NET_VLAN` 时，该宏会自动创建 VLAN 接口。这些宏通常用于网络设备驱动源代码中。

可以通过调用 ``net_if_up()`` 打开网络接口，通过调用 ``net_if_down()`` 关闭网络接口。设备上电时，网络接口默认也会打开。

网络接口可以通过 ``struct net_if *`` 指针或网络接口索引来引用。可以通过调用 ``net_if_get_by_index()`` 根据索引解析网络接口，也可以通过调用 ``net_if_get_by_iface()`` 根据接口指针解析网络接口。

.. _net_if_interface_ip_management:

必须为网络设备设置 IP 地址，设备才能连接。在典型的动态网络环境中，IP 地址例如由 DHCPv4 自动设置。不过，如有需要，应用可以手动设置设备的 IP 地址。有关实现该功能的函数（如 ``net_if_ipv4_addr_add()``），请参见下文 API 文档。

``net_if_get_default()`` 返回一个 *默认* 网络接口。这个默认接口的含义可以通过 :kconfig:option:`CONFIG_NET_DEFAULT_IF_FIRST` 和 :kconfig:option:`CONFIG_NET_DEFAULT_IF_ETHERNET` 等选项进行配置。关于可用于选择默认网络接口的选项，请参见 Kconfig 文件 :zephyr_file:`subsys/net/ip/Kconfig`。

发送和接收的网络数据包可以通过网络数据包优先级进行分类。这通常在使用虚拟 LAN（VLAN）的以太网网络中进行。高优先级数据包可以比低优先级数据包更早发送或接收。流量类别设置可通过 :kconfig:option:`CONFIG_NET_TC_TX_COUNT` 和 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` 选项配置。

如果启用了 :kconfig:option:`CONFIG_NET_PROMISCUOUS_MODE`，并且底层网络技术支持混杂模式，则可以接收网络设备驱动能够接收的所有网络数据包。更多详情见 :ref:`promiscuous_interface` API。

.. _net_if_interface_state_management:

网络接口状态管理
****************

Zephyr 区分两种接口状态：管理状态（administrative state）和运行状态（operational state），如 RFC 2863 所述。管理状态表示接口是打开还是关闭。该状态由 :c:enumerator:`NET_IF_UP` 标志表示，并由应用控制。可以通过调用 :c:func:`net_if_up` 或 :c:func:`net_if_down` 函数来更改。网络驱动或 L2 实现不应自行更改管理状态。

然而，打开接口并不总是意味着接口已准备好发送数据包。因此，引入了表示接口内部状态的运行状态。当发生以下任一情况时，会更新运行状态：

  * 应用打开/关闭接口（管理状态发生变化）。
  * 接口收到驱动/L2 关于 PHY 状态已更改的通知。
  * 接口收到驱动/L2 关于其已加入/离开网络的通知。

PHY 状态由 :c:enumerator:`NET_IF_LOWER_UP` 标志表示，并可通过 :c:func:`net_if_carrier_on` 和 :c:func:`net_if_carrier_off` 更改。默认情况下，新初始化的接口会设置该标志。改变载波（carrier）状态的事件示例是插入或拔出以太网网线。

网络关联状态由 :c:enumerator:`NET_IF_DORMANT` 标志表示，并可通过 :c:func:`net_if_dormant_on` 和 :c:func:`net_if_dormant_off` 更改。默认情况下，新初始化的接口会清除该标志。改变休眠（dormant）状态的事件示例是 Wi-Fi 驱动成功连接到接入点。在此场景中，驱动应在初始化期间将休眠状态设为 ON，一旦检测到已连接到 Wi-Fi 网络，就应将休眠状态设为 OFF。

接口的运行状态按如下方式更新：

  * ``!net_if_is_admin_up()``

    接口处于 :c:enumerator:`NET_IF_OPER_DOWN`。

  * ``net_if_is_admin_up() && !net_if_is_carrier_ok()``

    如果接口是堆叠（虚拟）接口，则接口处于 :c:enumerator:`NET_IF_OPER_DOWN` 或 :c:enumerator:`NET_IF_OPER_LOWERLAYERDOWN`。

  * ``net_if_is_admin_up() && net_if_is_carrier_ok() && net_if_is_dormant()``

    接口处于 :c:enumerator:`NET_IF_OPER_DORMANT`。

  * ``net_if_is_admin_up() && net_if_is_carrier_ok() && !net_if_is_dormant()``

    接口处于 :c:enumerator:`NET_IF_OPER_UP`。

只有当接口进入 :c:enumerator:`NET_IF_OPER_UP` 状态后，才会在接口上设置 :c:enumerator:`NET_IF_RUNNING` 标志，表示该接口已可供应用使用。

API 参考
********

.. doxygengroup:: net_if
