.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _dsa:

分布式交换机架构（DSA）
#######################

.. contents::
    :local:
    :depth: 2

分布式交换机架构（DSA）并不是什么新事物。多年来，它一直是 Linux 中成熟的子系统。本文档略去了背景、术语及任何相关知识描述，用户可以在 `Linux DSA documentation`_ 中找到所有这些内容。


DSA 交换机 TX/RX 处理过程
*************************

DSA 交换机 TX/RX 处理过程如下。

.. image:: dsa_txrx_process.svg

主机接口
********

主机接口网络设备使用常规、未经修改的以太网驱动程序，作为 DSA 通道端口（conduit port）工作，并通过处理器管理交换机。

交换机接口
**********

交换机接口在 Zephyr 中也作为标准以太网接口呈现。连接到通道端口的接口充当 CPU 端口，其他供用户使用的接口则充当用户端口。

交换机标记协议
**************

通常，交换机标记协议因厂商而异。它们都包含以下内容：

- 标识以太网帧来自哪个端口/应发送到哪个端口
- 提供该帧被转发到管理接口的原因

并在数据包上打标记，为其添加交换机帧报头。但也存在无标记的情况，这取决于厂商。

网络协议栈处理过程
******************

为了让 DSA 子系统通过通道端口处理以太网交换机特定的标记协议。

对于 RX 路径，将 ``dsa_recv()`` 放在 ``subsys/net/ip/net_core.c`` 中 ``net_recv_data()`` 的开头，以便首先进行去标记和接口重定向处理。

对于 TX 路径，交换机接口注册为标准以太网设备，并将 ``dsa_xmit()`` 作为 ``ethernet_api->send``。``dsa_xmit()`` 负责处理标记以及到通道端口的重定向工作。

DSA 设备驱动程序支持
********************

由于 DSA 核心驱动程序与 MDIO、PHY 和 Devicetree 等子系统/驱动程序交互，以支持通用的 DSA 搭建和工作流程，因此设备驱动程序支持要容易得多。

对于 Devicetree，交换机描述应遵循 ``dts/bindings/dsa/dsa.yaml``。

对于设备驱动程序，需要准备的是 :c:struct:`dsa_api`、私有数据（如果有）和 :c:struct:`dsa_port_config`。可以利用宏函数。下面是 i.MX NETC 的示例。

- :c:macro:`DSA_SWITCH_INST_INIT`
- :c:macro:`DSA_PORT_INST_INIT`

.. code-block:: c

   #define DSA_NETC_PORT_INST_INIT(port, n)                                                    \
           COND_CODE_1(DT_NUM_PINCTRL_STATES(port),                                            \
                           (PINCTRL_DT_DEFINE(port);), (EMPTY))                                \
           struct dsa_netc_port_config dsa_netc_##n##_##port##_config = {                      \
                   .pincfg = COND_CODE_1(DT_NUM_PINCTRL_STATES(port),                          \
                                   (PINCTRL_DT_DEV_CONFIG_GET(port)), NULL),                   \
                   .phy_mode = NETC_PHY_MODE(port),                                            \
           };                                                                                  \
           struct dsa_port_config dsa_##n##_##port##_config = {                                \
                   .mcfg = NET_ETH_MAC_DT_CONFIG_INIT(port),                                   \
                   .port_idx = DT_REG_ADDR(port),                                              \
                   .phy_dev = DEVICE_DT_GET_OR_NULL(DT_PHANDLE(port, phy_handle)),             \
                   .phy_mode = DT_PROP_OR(port, phy_connection_type, ""),                      \
                   .ethernet_connection = DEVICE_DT_GET_OR_NULL(DT_PHANDLE(port, ethernet)),   \
                   .prv_config = &dsa_netc_##n##_##port##_config,                              \
           };                                                                                  \
           DSA_PORT_INST_INIT(port, n, &dsa_##n##_##port##_config)

   #define DSA_NETC_DEVICE(n)                                                                  \
           AT_NONCACHEABLE_SECTION_ALIGN(static netc_cmd_bd_t dsa_netc_##n##_cmd_bd[8],        \
                                         NETC_BD_ALIGN);                                       \
           static struct dsa_netc_data dsa_netc_data_##n = {                                   \
                   .cmd_bd = dsa_netc_##n##_cmd_bd,                                            \
           };                                                                                  \
           DSA_SWITCH_INST_INIT(n, &dsa_netc_api, &dsa_netc_data_##n, DSA_NETC_PORT_INST_INIT);

使用 DSA 搭建时的常见陷阱
*************************

以下内容摘自 Linux DSA 文档，同样适用于 Zephyr。尽管通道端口和 CPU 端口在 Zephyr 中作为以太网设备呈现，但它们无法使用。

.. note::

  一旦通道网络设备被配置为使用 DSA（dev->dsa_ptr 变为非 NULL），并且其后面的交换机要求使用标记协议，该网络接口就只能专门用作通道接口。直接通过此接口发送数据包（例如：使用此接口打开 socket）不会经过交换机标记协议的发送函数，因此另一端期望收到标记的以太网交换机通常会丢弃该帧。

待完成的工作
************

与 Linux 相比，Zephyr DSA 中需要支持的功能太多。但基本上应支持桥接层。这样 DSA 就可以为用户提供两种使用交换机端口的方式。

- 独立模式：所有用户端口都作为常规以太网设备工作，不进行交换。
- 桥接模式：将用户端口加入虚拟桥接设备，从而启用交换模式。可以为该桥接分配 IP 地址。

.. _Linux DSA documentation:
   https://www.kernel.org/doc/html/latest/networking/dsa/dsa.html
