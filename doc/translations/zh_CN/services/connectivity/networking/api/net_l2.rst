.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_l2_interface:

L2 层管理
#########

.. contents::
    :local:
    :depth: 2

概述
****

L2 协议栈的设计目的是对上层的网络协议栈隐藏整个网络链路层部分及相关设备驱动。这是通过 :zephyr_file:`include/zephyr/net/net_if.h` 中声明的 :c:struct:`net_if` 实现的。

除了 net_if 对象以及 L2 层在 :zephyr_file:`include/zephyr/net/net_l2.h` 中以 :c:struct:`net_l2` 形式提供的通用 API 之外，上层并不了解实现细节。

只有 L2 层才能与关联到 net_if 对象的设备驱动通信。L2 层规定了设备驱动所要提供的 API，这些 API 针对该设备而特定、并为协同工作进行了优化。

目前已有针对 :ref:`以太网 <ethernet_interface>`、:ref:`IEEE 802.15.4 Soft-MAC <ieee802154_interface>`、:ref:`CANBUS <can_api>`、:ref:`OpenThread <thread_protocol_interface>`、Wi-Fi 的 L2 层，以及一个可作为编写新 L2 层模板的 dummy 层示例。

L2 层 API
*********

要创建 L2 层或针对特定 L2 层的驱动，需要理解 L3 层如何与其交互以及 L2 层应如何工作。更多细节另见 :ref:`网络协议栈架构 <network_stack_architecture>`。通用 L2 API 包含以下函数：

- ``recv()``：所有设备驱动在收到数据包并将其放入 :c:struct:`net_pkt` 后，都会通过 :c:func:`net_recv_data` 将该缓冲区推送到网络协议栈。此时网络协议栈不知道该数据包如何处理，而是将缓冲区传给 L2 协议栈的 ``recv()`` 函数处理。L2 协议栈对数据包执行所需的操作，例如解析链路层报头，或处理仅链路层的收据包。如果数据包有误，``recv()`` 函数返回 ``NET_DROP``；如果数据包已被 L2 完全消费，则返回 ``NET_OK``；如果应由网络协议栈继续处理，则返回 ``NET_CONTINUE``。

- ``send()``：与接收函数类似，网络协议栈会调用该函数来实际发送网络数据包。所有相关的链路层内容都由该函数生成并添加。``send()`` 函数返回已发送的字节数，如果发送网络数据包失败，则返回负的错误码。

- ``enable()``：该函数用于启用/禁用网络接口上的流量。函数返回 ``<0`` 表示出错，``>=0`` 表示无错误。

- ``get_flags()``：该函数返回 L2 驱动的能力，例如该 L2 是否支持多播或混杂模式。

网络设备驱动
************

网络设备驱动完全以 Zephyr 设备驱动模型为基础。请参见 :ref:`device_model_api`。

不过有两点不同：

- driver_api 指针必须指向有效的 :c:struct:`net_if_api` 指针。

- 网络设备驱动必须对以太网设备使用 :c:macro:`NET_DEVICE_INIT_INSTANCE()` 或 :c:macro:`ETH_NET_DEVICE_INIT()`。这些宏会调用 :c:macro:`DEVICE_DEFINE()` 宏，并为所创建的设备驱动实例实例化一个唯一的 :c:struct:`net_if`。

实现网络设备驱动取决于其所属的 L2 协议栈：:ref:`以太网 <ethernet_interface>`、:ref:`IEEE 802.15.4 <ieee802154_interface>` 等。下一节将描述设备驱动在接收或发送网络数据包时应如何工作，其余部分与硬件相关，此处不再详细说明。

以太网设备驱动
==============

接收时，设备驱动需要按需用尽可能多的数据缓冲区填充网络数据包。网络数据包本身就是 :c:struct:`net_pkt`，应通过 :c:func:`net_pkt_rx_alloc_with_buffer` 分配。之后所有数据缓冲区都会由 :c:func:`net_pkt_write` 自动分配并填充。

接收完所有网络数据后，设备驱动需要调用 :c:func:`net_recv_data`。如果该调用失败，则由设备驱动负责通过 :c:func:`net_pkt_unref` 解除对该缓冲区的引用。

发送时，设备驱动的发送函数会被调用，由设备驱动负责一次性带所有缓冲区发送该网络数据包。

最终，每个以太网设备驱动都需要像这样调用 ``ETH_NET_DEVICE_INIT()``：

.. code-block:: c

   ETH_NET_DEVICE_INIT(..., CONFIG_ETH_INIT_PRIORITY,
                       &the_valid_net_if_api_instance, 1500);

IEEE 802.15.4 设备驱动
======================

IEEE 802.15.4 L2 的设备驱动工作方式与以太网基本相同。上面描述的内容，尤其是 ``recv()``，同样适用。不过有两点具体差异：

- 它需要专用的设备驱动 API：:c:struct:`ieee802154_radio_api`，该 API 重载了 :c:struct:`net_if_api`。这是因为 802.15.4 L2 对设备驱动的要求不只是 ``send()`` 和 ``recv()`` 函数。这个专用 API 声明在 :zephyr_file:`include/zephyr/net/ieee802154_radio.h` 中。每个 IEEE 802.15.4 设备驱动都必须为这样填充好的 API 结构体提供有效的指针。

- 发送数据包与以太网略有不同。大多数 IEEE 802.15.4 PHY 只支持相对较小的帧，总计 127 字节：帧头、载荷和帧校验和。需要通过无线电发送的缓冲区往往不适合这一帧长度限制，例如包含 IPv6 数据包的缓冲区通常必须拆分成若干分片，并且 IPv6 数据包报头和分片需要先使用 6LoWPAN 之类的协议压缩后再交给无线电驱动。此外，IEEE 802.15.4 标准还定义了介质访问（例如 CSMA/CA）、帧重传、加密和其他预处理过程（例如添加信息元素），这些都不应由各个无线电驱动关心。因此 :c:struct:`ieee802154_radio_api` 要求的 tx 函数指针不同于 :c:struct:`net_if_api` 的发送函数指针。Zephyr 原生的 IEEE 802.15.4 L2 实现改为提供通用的 :c:func:`ieee802154_send`，用作 :c:type:`net_if` 的发送函数。:c:func:`ieee802154_send` 的实现负责 IEEE 802.15.4 标准的数据包准备过程：将数据包拆分为可能经过压缩、加密和其他预处理的分片缓冲区，依次通过 :c:struct:`ieee802154_radio_api` 的 tx 函数发送一个缓冲区，并且只有在整个传输成功或失败后才解除对网络数据包的引用。

IEEE 802.15.4 无线电设备驱动与 L2 之间的交互是双向的：

- L2 -> L1：诸如 :c:func:`ieee802154_send` 之类的方法以及若干 IEEE 802.15.4 网络管理调用会调用驱动，例如通过无线电链路发送数据包或在运行时重新配置驱动。这些调入调用全部由 :c:struct:`ieee802154_radio_api` 中的方法处理。

- L1 -> L2：在若干情况下驱动需要发起对 L2/MAC 层的调用。Zephyr 的 IEEE 802.15.4 L1 -> L2 适配 API 在这种情况下采用“控制反转”模式，从而避免在相互独立的驱动实现中重复复杂的逻辑，并在需要反向传递信息或硬件与 L2 紧密协作时，确保与实现无关的松耦合以及 MAC（L2）与 PHY（L1）之间清晰的职责分离。例如在驱动初始化期间，驱动会调用 :c:func:`ieee802154_init`，将接口的 MAC 地址以及其他与硬件相关的配置传给 L2。类似地，驱动可以向 L2 指示需要与硬件紧密集成的性能或时序关键无线电事件（例如 :c:func:`ieee802154_handle_ack`）。从 L1 到 L2 的调用并非以 :c:struct:`ieee802154_radio_api` 中方法的形式实现，而是在 :zephyr_file:`include/zephyr/net/ieee802154_radio.h` 中声明并如此记录的独立函数。API 文档会明确说明哪些函数必须由所有 L2 协议栈作为 L1 -> L2“控制反转”适配 API 的一部分来实现。

注意：:zephyr_file:`include/zephyr/net/ieee802154_radio.h` 中未被明确记录为回调的独立函数，视为 PHY（L1）层内部独立于任何特定 L2 协议栈实现的辅助函数，例如 :c:func:`ieee802154_is_ar_flag_set`。

与所有网络接口一样，IEEE 802.15.4 设备驱动实现最终也必须调用 ``NET_DEVICE_INIT_INSTANCE()``：

.. code-block:: c

   NET_DEVICE_INIT_INSTANCE(...,
                            the_device_init_prio,
                            &the_valid_ieee802154_radio_api_instance,
                            IEEE802154_L2,
                            NET_L2_GET_CTX_TYPE(IEEE802154_L2), 125);

API 参考
********

.. doxygengroup:: net_l2
