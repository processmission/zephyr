.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bt_mesh_proxy:

代理
####

代理（Proxy）功能允许手机等传统设备通过 GATT 访问 Bluetooth Mesh 网络。只有在设置了 :kconfig:option:`CONFIG_BT_MESH_GATT_PROXY` 选项时，才会编译代理功能。代理功能状态由 :ref:`bluetooth_mesh_models_cfg_srv` 控制，初始值可以通过 :c:member:`bt_mesh_cfg_srv.gatt_proxy` 设置。

启用代理功能的节点可以使用 Network Identity 和 Node Identity 进行广播，这由 :ref:`bluetooth_mesh_models_cfg_cli` 控制。

GATT Proxy 状态指示是否支持代理功能。

私有代理
********

支持代理功能和 :ref:`bluetooth_mesh_models_priv_beacon_srv` 模型的节点可以使用 Private Network Identity 和 Private Node Identity 类型进行广播，这由 :ref:`bluetooth_mesh_models_priv_beacon_cli` 控制。通过使用这组标识类型进行广播，节点允许传统设备通过 GATT 连接到网络，同时保持网络的隐私性。

Private GATT Proxy 状态指示是否支持私有代理功能。

代理请求
********

如果节点上的 GATT Proxy 和 Private GATT Proxy 状态均被禁用，则传统设备无法连接到该节点。不过，支持 :ref:`bluetooth_mesh_od_srv` 的节点可以在不启用 Private GATT Proxy 状态的情况下，被请求发送可连接广播事件。要请求该节点，传统设备可以调用 :func:`bt_mesh_proxy_solicit` 函数发送 Solicitation PDU。要启用此功能，设备必须设置 :kconfig:option:`CONFIG_BT_MESH_PROXY_SOLICITATION` 选项进行编译。

Solicitation PDU 是非 Mesh、不可连接、无方向的广播消息，包含 Proxy Solicitation UUID，并使用传统设备想要连接到的子网的网络密钥加密。该 PDU 包含传统设备的源地址和一个序列号。序列号由传统设备维护，并在每发送一个新的 Solicitation PDU 时递增。

每个支持接收 Solicitation PDU 的节点都维护自己的 Solicitation Replay Protection List（SRPL）。SRPL 通过存储节点处理的有效 Solicitation PDU 的请求序列号（SSEQ）和请求源（SSRC）对，保护请求机制免受重放攻击。更新 SRPL 与将更改存储到持久存储之间的延迟由 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` 定义。

Solicitation PDU RPL 配置模型 :ref:`bluetooth_mesh_srpl_cli` 和 :ref:`bluetooth_mesh_srpl_srv` 提供保存和清除 SRPL 条目的功能。支持 Solicitation PDU RPL Configuration Client 模型的节点可以通过调用 :func:`bt_mesh_sol_pdu_rpl_clear` 函数来清除目标上的一段 SRPL。Solicitation PDU RPL Configuration Client 与 Server 之间的通信使用应用密钥加密，因此，Solicitation PDU RPL Configuration Client 可以实例化在网络中的任何设备上。

当节点收到 Solicitation PDU 并成功通过认证时，它将开始使用 Private Network Identity 类型广播可连接广播。广播的持续时间可以由 On-Demand Private Proxy Client 模型配置。

API 参考
********

.. doxygengroup:: bt_mesh_proxy
