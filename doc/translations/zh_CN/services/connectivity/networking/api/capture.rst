.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_capture_interface:

网络抓包
########

.. contents::
    :local:
    :depth: 2

概述
****

``net_capture`` API 允许用户监控 Zephyr 某个网络接口中的网络流量，并将该流量发送到外部系统进行分析。监控既可以手动使用 ``net-shell`` 设置，也可以通过 ``net_capture`` API 自动设置。

Cooked 模式抓包
***************

如果已启用并配置抓包，系统将自动抓取指定网络接口的网络流量。如果要在不涉及网络接口的情况下抓取网络数据，则需要使用 Cooked 模式抓包 API。

在 Cooked 模式抓包中，可以抓取任意网络数据包，且无需涉及网络接口。例如，可以抓取 PPP 中的低层 HDLC 数据包，因为使用基于常规网络接口的抓包方式时，HDLC L2 层数据会被剥离。也可以抓取 CANBUS 或蓝牙网络数据，尽管目前网络协议栈尚不支持抓取这些数据。

Cooked 模式抓包的工作方式如下：

* 创建一个 ``any`` 网络接口。它充当汇聚接口，Cooked 模式抓包 API 会将抓取的数据包写入其中。
* 在此 ``any`` 接口之上附加一个 ``cooked`` 虚拟网络接口。
* ``cooked`` 接口必须使用网络接口配置 API 配置为抓取特定的 L2 数据包类型。
* 使用 Cooked 模式抓包 API 时，调用者必须指定所抓取数据的 L2（第 2 层）协议类型。这样，Cooked 模式抓包 API 在收到此类 L2 数据包时就能确定要抓取什么。
* 随后设置网络数据包抓包基础设施，将 ``cooked`` 接口标记为抓包网络接口。``cooked`` 接口通过 ``any`` 接口接收的数据包随后会自动放入抓包 IP 隧道，并发送到远程主机进行分析。

例如，在抓包示例应用中，创建了以下网络接口：

.. code-block:: c

        Interface any (0x808ab3c) (Dummy) [1]
        ================================
        Virtual interfaces attached to this : 2
        Device    : NET_ANY (0x80849a4)

        Interface cooked (0x808ac94) (Virtual) [2]
        ==================================
        Virtual name : Cooked mode capture
        Attached  : 1 (Dummy / 0x808ab3c)
        Device    : NET_COOKED (0x808497c)

        Interface eth0 (0x808adec) (Ethernet) [3]
        ===================================
        Virtual interfaces attached to this : 4
        Device    : zeth0 (0x80849b8)
        IPv6 unicast addresses (max 4):
             fe80::5eff:fe00:53e6 autoconf preferred infinite
             2001:db8::1 manual preferred infinite
        IPv4 unicast addresses (max 2):
             192.0.2.1/255.255.255.0 overridable preferred infinite

        Interface net0 (0x808af44) (Virtual) [4]
        ==================================
        Virtual name : Capture tunnel
        Attached  : 3 (Ethernet / 0x808adec)
        Device    : IP_TUNNEL0 (0x8084990)
        IPv6 unicast addresses (max 4):
             2001:db8:200::1 manual preferred infinite
             fe80::efed:6dff:fef2:b1df autoconf preferred infinite
             fe80::56da:1eff:fe5e:bc02 autoconf preferred infinite

在本示例中，``192.0.2.2`` 是终止隧道的主机外侧端点地址。Zephyr 使用该地址选择用于隧道的内部接口。在本示例中，该接口是接口 3。

接口 2 是运行在接口 1 之上的虚拟接口。Cooked 抓包数据包由抓包 API 写入汇聚接口 1。这些数据包会传播到接口 2，因为它与第一个接口相连。``net capture enable 2`` net-shell 命令会使发送到接口 2 的数据包写入抓包接口 4，接口 4 随后会封装这些数据包，并通过以太网接口 3 将它们隧道传输到对端。

如果更改示例文件 :zephyr_file:`samples/net/capture/overlay-tunnel.conf` 中的地址，上述 IP 地址可能会发生变化。

用法示例
********

详情请参见 :zephyr:code-sample:`net-capture` 示例应用和 :ref:`network_monitoring`。


API 参考
********

.. doxygengroup:: net_capture
