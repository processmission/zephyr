.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_brg_cfg:

子网桥接
########

Bluetooth Mesh Protocol Specification 1.1 版引入了 Bluetooth Mesh 子网桥接功能。该功能允许 Mesh 网络使用子网进行区域隔离，同时还允许不同相邻子网中的特定设备之间进行通信，而不会损害安全性。

Bluetooth Mesh 子网桥接功能使网络中的选定节点能够充当子网桥，通过中继相邻子网中节点之间的消息来实现受控通信。

子网桥接功能包括两个模型：

- :ref:`bluetooth_mesh_models_brg_cfg_srv`
- :ref:`bluetooth_mesh_models_brg_cfg_cli`

桥接配置服务器模型是支持子网桥接功能所必需的。桥接配置客户端模型是可选的，允许节点在其他节点上配置子网桥接。这些模型定义了配置和管理子网桥接功能所需的状态、消息和行为。

子网桥接功能的配置和管理由桥接配置服务器和客户端模型处理。实现桥接配置客户端模型的节点可以充当子网桥接功能的 *配置管理器*。

概念
****

为了更好地理解子网桥接功能及其能力，需要概述几个概念。

子网
====

子网是 Mesh 网络内共享同一网络密钥的一组节点，使它们能够在网络层安全地通信。每个子网独立运行，节点仅在该组内交换消息。一个节点可以同时属于多个子网。

子网桥接节点
============

子网桥接节点是 Bluetooth Mesh 网络中属于多个子网并启用了子网桥接功能的节点。只有此类节点才能执行子网桥接。子网桥接节点连接各子网，并通过跨子网组中继消息来允许它们之间通信。

子网桥接节点有一个基于主 NetKey 的主子网，它负责处理 IV Update 过程并将更新传播到其他子网。消息中继到的其他子网称为 *桥接子网*。

桥接表
======

桥接表包含节点所桥接的子网条目，由桥接配置服务器模型管理。

桥接表中的最大条目数由 :kconfig:option:`CONFIG_BT_MESH_BRG_TABLE_ITEMS_MAX` 选项定义，其默认值为最小值 16，最大可能大小为 255。

启用或禁用子网桥接功能
**********************

桥接配置客户端（或配置管理器）可以通过使用 :c:func:`bt_mesh_brg_cfg_cli_set` 函数向目标节点上的桥接配置服务器模型发送 **Subnet Bridge Set** 消息，以启用或禁用节点上的子网桥接功能。

添加或移除子网
**************

桥接配置客户端可以通过调用 :c:func:`bt_mesh_brg_cfg_cli_table_add` 或 :c:func:`bt_mesh_brg_cfg_cli_table_remove` 函数，向目标节点上的桥接配置服务器模型发送 **Bridging Table Add** 或 **Bridging Table Remove** 消息，以在桥接表中添加或移除条目。

.. _bluetooth_mesh_brg_cfg_states:

子网桥接状态
************

子网桥接具有以下状态：

- *子网桥接*：此状态指示节点上的子网桥接功能是启用还是禁用。桥接配置客户端可以使用 :c:func:`bt_mesh_brg_cfg_cli_get` 函数向桥接配置服务器发送 **Subnet Bridge Get** 消息来获取此信息。

- *桥接表*：此状态保存桥接表。客户端可以使用 :c:func:`bt_mesh_brg_cfg_cli_table_get` 函数向目标节点发送 **Bridging Table Get** 消息，以请求桥接表中的条目列表。

  客户端可以通过调用 :c:func:`bt_mesh_brg_cfg_cli_subnets_get` 函数，向目标服务器发送 **Bridged Subnets Get** 消息，以获取当前由子网桥桥接的子网列表。

- *桥接表大小*：此状态报告桥接表可存储的最大条目数。客户端可以使用 :c:func:`bt_mesh_brg_cfg_cli_table_size_get` 函数发送 **Bridging Table Size Get** 消息来获取此信息。这是一个只读状态。

子网桥接与重放保护
******************

子网桥接功能支持子网之间的消息中继，需要有效的重放保护来确保网络安全。以下描述了需要考虑的关键事项。

中继缓冲区注意事项
==================

当消息由子网桥在子网之间中继时，会从中继缓冲区池中分配。中继缓冲区的数量可以使用 :kconfig:option:`CONFIG_BT_MESH_RELAY_BUF_COUNT` Kconfig 选项进行配置。

启用 :kconfig:option:`CONFIG_BT_MESH_ADV_EXT` 时，消息将使用中继广播集进行传输。广播集的数量可以使用 :kconfig:option:`CONFIG_BT_MESH_RELAY_ADV_SETS` Kconfig 选项进行配置。

即使中继功能 :kconfig:option:`CONFIG_BT_MESH_RELAY` 被禁用，中继缓冲区池和广播集也可以使用。

重放保护与桥接表
================

子网桥接节点必须为发送到桥接子网的所有 Access 和 Transport Control 消息实现重放保护。

重放保护列表（Replay Protection List，RPL）与桥接表配合工作，以确保安全性：

- 子网桥为每个获准向桥接子网发送消息的源地址存储最新的 IVISeq。

- IVISeq 小于或等于存储值的消息将被丢弃，而有效消息会在被中继之前更新存储的 IVISeq。

为确保正常运行，RPL 与桥接表保持同步非常重要，因为每条桥接消息在被中继之前都必须经过重放保护机制。

.. note::

   RPL 的大小应随桥接表扩展。随着桥接子网数量的增加，必须跟踪更多的源地址和 IVISeq 值，因此需要更大的 RPL 来维持有效的重放保护。

子网桥接与定向转发
******************

Bluetooth Mesh 定向转发（Directed Forwarding，MDF）通过优化中继路径，实现跨子网节点之间的高效路由。虽然 MDF 可以通过处理路径发现和转发来增强子网桥接，但当前实现不支持该功能。

API 参考
********

本节包含桥接配置模型通用的类型和定义。

.. doxygengroup:: bt_mesh_brg_cfg
