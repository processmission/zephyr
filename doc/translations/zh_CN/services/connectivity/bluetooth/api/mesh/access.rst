.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_access:

访问层
######

访问层是应用与 Bluetooth Mesh 网络之间的接口。访问层提供了将节点行为划分为元素和模型的机制，这些元素和模型由应用实现。

Mesh 模型
*********

Mesh 节点的功能由模型表示。模型实现节点支持的单一行为，例如灯、传感器或恒温器。Mesh 模型被分组到 *元素* 中。每个元素分配有自己的单播地址，并且每种类型的模型最多只能包含一个。按照惯例，每个元素表示 Mesh 节点行为的一个方面。例如，一个包含传感器、两盏灯和一个电源插座的节点会将此功能分布在四个元素上，每个元素实例化支持行为中单个方面所需的所有模型。

节点的元素和模型结构在节点 Composition Data 中指定，并在初始化期间传递给 :c:func:`bt_mesh_init`。Bluetooth SIG 定义了一组基础模型（参见 :ref:`bluetooth_mesh_models`）以及一组用于实现常见行为的模型，详见 `Bluetooth Mesh Model Specification <https://www.bluetooth.com/specifications/mesh-specifications/>`_。Bluetooth SIG 未指定的所有模型都是厂商模型，必须绑定到一个 Company ID。

Mesh 模型有几个参数，可以通过初始化 Mesh 协议栈或使用 :ref:`bluetooth_mesh_models_cfg_srv` 进行配置：

Opcode 列表
===========

Opcode 列表包含模型可以接收的所有消息 Opcode，以及可接受的最小有效载荷长度和用于传递消息的回调。模型可以支持任意数量的 Opcode，但每个 Opcode 在每个元素中只能由一个模型列出。

完整的 Opcode 列表必须在 Composition Data 中传递给模型结构，并且不能在运行时更改。Opcode 列表的结尾由特殊的 :c:macro:`BT_MESH_MODEL_OP_END` 条目确定。除非列表为空，否则该条目必须始终存在于 Opcode 列表中。如果列表为空，则应使用 :c:macro:`BT_MESH_MODEL_NO_OPS` 代替正式的 Opcode 列表定义。

AppKey 列表
===========

AppKey 列表包含模型可以接收消息的所有应用密钥。只有使用 AppKey 列表中的应用密钥加密的消息才会传递给模型。

每个模型可持有的最大支持应用密钥数通过 :kconfig:option:`CONFIG_BT_MESH_MODEL_KEY_COUNT` 配置选项进行配置。AppKey 列表的内容由 :ref:`bluetooth_mesh_models_cfg_srv` 管理。

订阅列表
========

模型会处理发往其元素单播地址的所有消息（前提是所使用的应用密钥存在于 AppKey 列表中）。此外，模型还会处理发往其订阅列表中任何组地址或虚拟地址的数据包。这使节点能够通过单条消息寻址整个 Mesh 网络中的多个节点。

每个模型可在订阅列表中持有的最大支持地址数通过 :kconfig:option:`CONFIG_BT_MESH_MODEL_GROUP_COUNT` 配置选项进行配置。订阅列表的内容由 :ref:`bluetooth_mesh_models_cfg_srv` 管理。

模型发布
========

模型可以通过两种方式发送消息：

* 在 :c:struct:`bt_mesh_msg_ctx` 中指定一组消息参数，并调用 :c:func:`bt_mesh_model_send`。
* 设置 :c:struct:`bt_mesh_model_pub` 结构并调用 :c:func:`bt_mesh_model_publish`。

使用 :c:func:`bt_mesh_model_publish` 发布消息时，模型将使用由 :ref:`bluetooth_mesh_models_cfg_srv` 配置的发布参数。这是发送非提示性模型消息的推荐方式，因为它将选择消息参数的责任交给网络管理员，而网络管理员对 Mesh 网络的了解通常比各个节点更多。

为了支持使用发布参数进行发布，模型必须为发布分配一个数据包缓冲区，并将其传递给 :c:member:`bt_mesh_model_pub.msg`。配置服务器还可以为发布消息设置周期发布。为支持这一点，模型必须填充 :c:member:`bt_mesh_model_pub.update` 回调。:c:member:`bt_mesh_model_pub.update` 回调将在消息发布之前立即调用，使模型能够更改有效载荷以反映其当前状态。

通过将 :c:member:`bt_mesh_model_pub.retr_update` 设置为 1，模型可以配置 :c:member:`bt_mesh_model_pub.update` 回调在每次重传时触发。例如，这可被使用 Delay 参数的模型使用，该参数可以在每次重传时调整。可以使用 :c:func:`bt_mesh_model_pub_is_retransmission` 函数区分首次发布和重传。可以使用 :c:macro:`BT_MESH_PUB_MSG_TOTAL` 和 :c:macro:`BT_MESH_PUB_MSG_NUM` 宏返回一个发布间隔内的总传输次数和重传编号。

扩展模型
========

Bluetooth Mesh 规范允许 Mesh 模型相互扩展。当一个模型扩展另一个模型时，它会继承该模型的功能，扩展可用于由简单模型构建复杂模型，利用现有模型功能来避免定义新的 Opcode。模型可以扩展任意数量的模型，且可以来自任意元素。当一个模型扩展同一元素中的另一个模型时，这两个模型将共享订阅列表。Mesh 协议栈通过将两个模型的订阅列表合并为一个来实现这一点，合并后模型总共可拥有的订阅数相加。模型可以扩展那些扩展了其他模型的模型，从而形成“扩展树”。扩展树中的所有模型在其跨越的每个元素中共享一个订阅列表。

模型扩展在初始化期间通过调用 :c:func:`bt_mesh_model_extend` 完成。一个模型只能被另一个模型扩展，并且扩展不能形成循环。请注意，节点状态的绑定以及模型之间的其他关系必须由模型实现定义。

模型扩展概念会在访问层数据包处理中增加一些开销，必须显式启用 :kconfig:option:`CONFIG_BT_MESH_MODEL_EXTENSIONS` 才能生效。

模型数据存储
============

Mesh 模型可能具有需要持久存储的、与每个模型实例关联的数据。访问 API 提供了一种利用内部模型实例编码方案来存储这些数据的机制。模型可以通过调用 :c:func:`bt_mesh_model_data_store` 为每个实例存储一个用户定义的数据条目。为了在设备下次重启时能够读取数据，必须填充模型的 :c:member:`bt_mesh_model_cb.settings_set` 回调。当在持久存储中找到模型特定数据时，将调用此回调。模型可以通过调用作为参数传递给该回调的 ``read_cb`` 来获取数据。详情请参阅 :ref:`settings_api` 模块文档。

当模型数据频繁变化时，每次变化都存储可能会导致闪存磨损增加。为减少磨损，模型可以通过调用 :c:func:`bt_mesh_model_data_store_schedule` 推迟数据存储。协议栈将调度一个工作项，其延迟由 :kconfig:option:`CONFIG_BT_MESH_STORE_TIMEOUT` 选项定义。工作项运行时，协议栈将为每个请求存储数据的模型调用 :c:member:`bt_mesh_model_cb.pending_store` 回调。然后模型可以调用 :c:func:`bt_mesh_model_data_store` 来存储数据。

如果启用了 :kconfig:option:`CONFIG_BT_MESH_SETTINGS_WORKQ`，则会从专用线程调用 :c:member:`bt_mesh_model_cb.pending_store` 回调。这使协议栈能够在存储模型数据的同时处理其他传入和传出消息。当需要存储大量数据时，建议使用此选项和 :c:func:`bt_mesh_model_data_store_schedule` 函数。

Composition Data
================

Composition Data 提供有关 Mesh 设备的信息。设备的 Composition Data 保存有关设备上的元素、支持的模型以及其他功能的信息。Composition Data 分为不同的页，每页包含设备的特定功能信息。为访问此信息，用户可以使用 :ref:`bluetooth_mesh_models_cfg_srv` 模型，或者如果支持，也可以使用 :ref:`bluetooth_mesh_lcd_srv` 模型。

Composition Data Page 0
-----------------------

Composition Data Page 0 提供有关设备的基本信息，并且对所有 Mesh 设备都是必需的。它包含元素和模型组成、支持的功能以及制造商信息。

Composition Data Page 1
-----------------------

Composition Data Page 1 提供有关模型之间关系的信息，并且对所有 Mesh 设备都是必需的。一个模型可以扩展和/或对应一个或多个模型。模型可以通过调用 :c:func:`bt_mesh_model_extend` 扩展另一个模型，或通过调用 :c:func:`bt_mesh_model_correspond` 对应另一个模型。:kconfig:option:`CONFIG_BT_MESH_MODEL_EXTENSION_LIST_SIZE` 指定设备上的 Composition Data 中可以存储多少个模型关系，该数量应反映 :c:func:`bt_mesh_model_extend` 和 :c:func:`bt_mesh_model_correspond` 调用的次数。

Composition Data Page 2
-----------------------

Composition Data Page 2 提供受支持 Mesh 配置文件的信息。Mesh 配置文件规范定义了希望支持特定 Bluetooth SIG 定义配置文件的产品的需求。当前支持的配置文件可在 `Bluetooth SIG Assigned Numbers <https://www.bluetooth.com/specifications/assigned-numbers/uri-scheme-name-string-mapping/>`_ 的第 3.12 节中找到。Composition Data Page 2 仅对声明支持一个或多个 Mesh 配置文件的设备是必需的。

Composition Data Pages 128、129 和 130
--------------------------------------

Composition Data Pages 128、129 和 130 分别镜像 Composition Data Pages 0、1 和 2。当固件更新后 Composition Data 发生变化时，它们用于表示被镜像页的新内容。详情请参阅 :ref:`bluetooth_mesh_dfu_srv_comp_data_and_models_metadata`。

可延迟消息
==========

可延迟消息功能通过 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_ACCESS_DELAYABLE_MSG` 启用。这是一个可选功能，实现规范中针对模型为响应收到消息而发送的消息（也称为响应消息）的建议。

响应消息应使用以下随机延迟发送：

* 如果收到的消息是发送到单播地址，则为 20 到 50 毫秒之间
* 如果收到的消息是发送到组地址或虚拟地址，则为 20 到 500 毫秒之间

如果设置了 :c:member:`bt_mesh_msg_ctx.rnd_delay` 标志，则会触发可延迟消息功能。可延迟消息功能会将这些消息存储在本地内存中，直到随机延迟到期。

如果传输层在随机延迟到期时没有足够内存发送消息，则该消息会再推迟 10 毫秒。如果传输层因任何其他原因无法发送消息，则可延迟消息功能会使用传输层错误码触发 :c:member:`bt_mesh_send_cb.start` 回调。

如果可延迟消息功能找不到足够的空闲内存来存储传入消息，它会发送延迟接近到期的消息以释放内存。

当 Mesh 协议栈挂起或重置时，尚未发送的消息会被移除，并使用错误码触发 :c:member:`bt_mesh_send_cb.start` 回调。

.. note::
   当一个模型连续发送多条消息时，可能会出现消息未按传递给访问层的顺序发送的情况。这是因为某些消息的延迟可能比其他消息更长。

   当同一模型产生的一组消息需要按特定顺序发送时，将 :c:member:`bt_mesh_msg_ctx.rnd_delay` 设置为 ``false`` 以禁用随机化。

可延迟发布
==========

可延迟发布功能在以下情况下实现规范中关于消息发布延迟的建议：

* 当 Bluetooth Mesh 协议栈启动或通过 :c:func:`bt_mesh_model_publish` 函数触发发布时，为 20 到 500 毫秒之间
* 对于周期性发布的消息，为 20 到 50 毫秒之间

此功能是可选的，通过 :kconfig:option:`CONFIG_BT_MESH_DELAYABLE_PUBLICATION` Kconfig 选项启用。启用后，每个模型可以通过将 :c:member:`bt_mesh_model_pub.delayable` 位字段相应地设置为 ``1`` 或 ``0`` 来启用或禁用可延迟发布。该位字段可以随时更改。

API 参考
********

.. doxygengroup:: bt_mesh_access
