.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_core:

核心
####

核心提供用于管理 Bluetooth Mesh 整体状态的功能。

.. _bluetooth_mesh_lpn:

低功耗节点
**********

低功耗节点（LPN，Low Power Node）角色允许电池供电的设备作为叶子节点加入网状网络。LPN 通过 Friend 节点与网状网络交互，Friend 节点负责转发所有发往该 LPN 的消息。LPN 通过保持无线电关闭来省电，只在发送消息或向 Friend 节点轮询传入消息时才唤醒。

无线电控制和轮询由 mesh 协议栈自动管理，但 LPN API 允许应用随时通过 :c:func:`bt_mesh_lpn_poll` 触发轮询。LPN 的运行参数（包括轮询间隔、轮询事件时序和 Friend 要求）通过 :kconfig:option:`CONFIG_BT_MESH_LOW_POWER` 选项及相关配置选项控制。

将 LPN 功能与日志功能一起使用时，强烈建议只使用 :kconfig:option:`CONFIG_LOG_MODE_DEFERRED` 选项。非延迟的日志模式可能会在处理日志消息时造成意外延迟，进而影响接收延迟和接收窗口的调度。相同的限制也适用于 :kconfig:option:`CONFIG_BT_MESH_FRIEND` 选项。

重放保护列表
************

重放保护列表（RPL，Replay Protection List）用于保存最近从网状网络中各元素接收到的序列号，以防止重放攻击。

为了让节点在重启后仍能防御重放攻击，节点需要在断电前将整个 RPL 存入持久化存储。根据网状网络中的流量大小，存储最近收到的序列号可能会或早或晚地造成闪存磨损。为缓解这一问题，可以使用 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT`。该选项会推迟将 RPL 条目写入持久化存储。

不过，该选项并不能完全解决问题，因为节点可能在存储 RPL 的定时器触发之前就断电了。为确保消息无法被重放，节点可以随时（或在断电之前足够早的时候）调用 :c:func:`bt_mesh_rpl_pending_store`，触发存储待处理的 RPL 条目。此时存储哪些 RPL 条目由节点自行决定。

将 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` 设置为 -1 可以完全关闭该定时器，这有助于显著减少闪存磨损。这样，存储 RPL 的责任就转移到用户应用，并且要求从调用该 API 之时起直到所有 RPL 条目写入闪存为止都有足够的备用电源。

在 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` 与调用 :c:func:`bt_mesh_rpl_pending_store` 之间找到合适的平衡，可以降低安全漏洞和闪存磨损的风险。

.. warning:

   Failing to enable :kconfig:option:`CONFIG_BT_SETTINGS`, or setting
   :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` to -1 and not storing
   the RPL between reboots, will make the device vulnerable to replay attacks
   and not perform the replay protection required by the spec.

.. _bluetooth_mesh_persistent_storage:

持久化存储
**********

mesh 协议栈使用 :ref:`Settings 子系统 <settings_api>` 持久存储设备配置。当协议栈配置发生变化且需要持久存储该变化时，协议栈会安排一个工作项。从安排工作项到将其提交给工作队列之间的延迟由 :kconfig:option:`CONFIG_BT_MESH_STORE_TIMEOUT` 选项定义。一旦安排了数据存储，在该工作项被处理之前无法重新安排。某些情况下会有例外，如下所述。

当需要存储 IV index、序列号或 CDB 配置时，工作项会被立即提交给工作队列，不设延迟。如果该工作项此前已被安排，则会无延迟地重新安排。

重放保护列表使用同一个工作项来存储 RPL 条目。如果请求存储 RPL 条目且没有其他待存储的配置，则延迟设置为 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT`。如果还有其他协议栈配置需要存储，:kconfig:option:`CONFIG_BT_MESH_STORE_TIMEOUT` 选项定义的延迟小于 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT`，并且该工作项是由重放保护列表安排的，则该工作项会被重新安排。

工作项运行时，协议栈会存储所有待处理的配置，包括 RPL 条目。

工作项执行上下文
================

:kconfig:option:`CONFIG_BT_MESH_SETTINGS_WORKQ` 选项配置执行该工作项的上下文。该选项默认启用，协议栈会使用一个专用的协作式线程来处理该工作项。这样，在存储协议栈配置期间，协议栈仍能处理其他传入和传出的消息，以及提交到系统工作队列的其他工作项。

禁用该选项时，工作项会被提交到系统工作队列。这意味着在存储协议栈配置所需的时间内，系统工作队列会被阻塞。不建议禁用该选项，因为这样会使设备在相当长的一段时间内无响应。

.. _bluetooth_mesh_adv_identity:

广播身份
********

所有 mesh 协议栈承载都使用 :c:macro:`BT_ID_DEFAULT` 本地身份广播数据。该值在 mesh 协议栈实现中预设。当 Bluetooth® Low Energy（LE）与 Bluetooth Mesh 在同一设备上共存时，应用应在开始通信之前为 Bluetooth LE 分配并配置另一个本地身份。

API 参考
********

.. doxygengroup:: bt_mesh
