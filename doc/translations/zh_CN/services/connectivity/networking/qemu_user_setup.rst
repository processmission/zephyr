.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _networking_with_user_qemu:

使用 QEMU 用户模式进行网络连接
##############################

.. contents::
    :local:
    :depth: 2

本页面旨在为有兴趣在 Zephyr 中使用 QEMU SLIRP 的用户提供一个起点。

简介
****

SLIRP 是一种网络后端，它在 QEMU 内部提供完整的 TCP/IP 协议栈，并利用该协议栈实现虚拟 NAT 网络。由于不依赖于主机，SLIRP 的搭建非常简单。

默认情况下，QEMU 使用 ``10.0.2.X/24`` 网络，并在 ``10.0.2.2`` 上运行网关。所有发往主机网络的流量都必须经过此网关，网关会根据 QEMU 命令行参数过滤数据包。该网关还充当所有 GOS 的 DHCP 服务器，使它们可以从 ``10.0.2.15`` 开始自动分配 IP 地址。

有关用户模式网络的更多详细信息，请参见：https://wiki.qemu.org/Documentation/Networking#User_Networking_.28SLIRP.29

在 Zephyr 中使用 SLIRP
**********************

要在 Zephyr 中使用 SLIRP，用户必须设置 Kconfig 选项以启用用户模式网络。

.. code-block:: cfg

   CONFIG_NET_QEMU_USER=y

启用此配置选项后，所有 QEMU 启动都将使用 SLIRP。在默认配置中，Zephyr 仅启用用户模式网络，不向其传递任何参数。这意味着客户机只能与 QEMU 网关通信，任何发往主机的数据都将被 QEMU 丢弃。

一般来说，QEMU 用户模式网络可以接受很多参数，包括：

* 主机/客户机端口转发信息。必须提供该信息才能在客户机与主机之间建立通信通道。
* 要使用的网络信息。如果用户不想使用默认的 ``10.0.2.X`` 网络，该信息会很有用。
* 指示 QEMU 在用户定义的 IP 地址上启动 DHCP 服务器。
* ID 及其他信息。

由于这些信息因用例而异，很难给出适用于所有情况的良好默认值。因此，Zephyr 实现将此交给用户处理，并期望用户根据需求提供参数。为此，有一个可由用户填充的 Kconfig 字符串选项。

.. code-block:: cfg

   CONFIG_NET_QEMU_USER_EXTRA_ARGS="net=192.168.0.0/24,hostfwd=tcp::8080-:8080"

此选项会原样追加到 QEMU 命令行中。因此，与此命令行相关的任何问题都只会由 QEMU 报告。以下为此具体示例的作用：

* 让 QEMU 使用 ``192.168.0.0/24`` 网络，而不是默认网络。
* 启用转发：将从主机 8080 端口接收到的任何 TCP 数据转发到客户机的 8080 端口，反之亦然。

限制
****

如果用户除了能从客户机访问网页之外没有其他特定的网络需求，那么用户模式网络（slirp）是一个不错的选择。但它有一些限制：

* 开销很大，因此性能较差。
* 无法从主机或外部网络直接访问客户机。
* 一般来说，ICMP 流量无法正常工作（因此不能在客户机内使用 ping）。
* 由于端口映射需要在启动 qemu 之前定义，使用动态生成端口的客户端无法与外部网络通信。
* SLIRP 实现中存在一个缺陷，会过滤掉来自客户机的所有 IPv6 数据包。详情见 https://bugs.launchpad.net/qemu/+bug/1724590。因此，IPv6 无法与用户模式网络一起使用。
