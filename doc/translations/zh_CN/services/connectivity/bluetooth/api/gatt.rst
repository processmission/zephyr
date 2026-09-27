.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bt_gatt:


通用属性配置文件（GATT）
########################

GATT 层管理服务数据库，提供服务注册和属性声明所需的 API。

GATT 客户端向 GATT 服务器发起命令和请求，并可以接收服务器发送的响应、指示（indication）和通知（notification）。它通过配置选项 :kconfig:option:`CONFIG_BT_GATT_CLIENT` 启用。

GATT 服务器接受来自 GATT 客户端的命令和请求，并向客户端发送响应、指示和通知。

可使用 :c:func:`bt_gatt_service_register` API 注册服务，该 API 接受 :c:struct:`bt_gatt_service` 结构体，其中提供服务包含的属性列表。辅助宏 :c:macro:`BT_GATT_SERVICE()` 可用于声明服务。

可以使用 :c:struct:`bt_gatt_attr` 结构体或以下辅助宏之一来声明属性：

    :c:macro:`BT_GATT_PRIMARY_SERVICE`
        声明主要服务。

    :c:macro:`BT_GATT_SECONDARY_SERVICE`
        声明次要服务。

    :c:macro:`BT_GATT_INCLUDE_SERVICE`
        声明包含服务。

    :c:macro:`BT_GATT_CHARACTERISTIC`
        声明特征。

    :c:macro:`BT_GATT_DESCRIPTOR`
        声明描述符。

    :c:macro:`BT_GATT_ATTRIBUTE`
        声明属性。

    :c:macro:`BT_GATT_CCC`
        声明客户端特征配置（CCC）。

    :c:macro:`BT_GATT_CEP`
        声明特征扩展属性（CEP）。

    :c:macro:`BT_GATT_CUD`
        声明特征用户格式（CUD）。

每个属性都包含一个描述其类型的 ``uuid``、一个 ``read`` 回调、一个 ``write`` 回调以及一组权限。如果属性权限不允许相应操作，则 read 和 write 回调都可以设置为 NULL。

.. note::
   GATT 不支持 32 位 UUID。当 UUID 包含在 ATT PDU 中时，所有 32 位 UUID 都应转换为 128 位 UUID。

.. note::
  属性 ``read`` 和 ``write`` 回调直接从 RX 线程调用，因此不建议在其中长时间阻塞。

可以使用 :c:func:`bt_gatt_notify` API 通知属性值变化；另一种选择是 :c:func:`bt_gatt_notify_cb`，通过它可以传入一个回调，以便在需要知道数据通过空口发送的确切时刻时调用。指示（indication）由 :c:func:`bt_gatt_indicate` API 支持。

可以使用 :c:func:`bt_gatt_discover` API 发起发现流程，该 API 接受描述发现类型的 :c:struct:`bt_gatt_discover_params` 结构体。这些参数还可用作过滤器：设置 ``uuid`` 字段后只会发现与之匹配的属性，而将其设置为 NULL 则允许发现所有属性。

.. note::
  不支持缓存已发现的属性。

读流程由 :c:func:`bt_gatt_read` API 支持，该 API 接受 :c:struct:`bt_gatt_read_params` 结构体作为参数。在参数中可以设置一个或多个属性，不过设置多个句柄需要启用选项 :kconfig:option:`CONFIG_BT_GATT_READ_MULTIPLE`

写流程由 :c:func:`bt_gatt_write` API 支持，它接受 :c:struct:`bt_gatt_write_params` 结构体作为参数。如果写操作不需要响应，可以使用 :c:func:`bt_gatt_write_without_response` 或 :c:func:`bt_gatt_write_without_response_cb` API，其中后者与 :c:func:`bt_gatt_notify_cb` 的工作方式类似。

可以使用 :c:func:`bt_gatt_subscribe` API 发起对通知和指示的订阅，该 API 接受 :c:struct:`bt_gatt_subscribe_params` 作为参数。支持对同一属性进行多次订阅，因此同一属性可能会触发多个 ``notify`` 回调。可以使用 :c:func:`bt_gatt_unsubscribe` API 移除订阅。

.. note::
  移除订阅时，会调用 ``notify`` 回调并将数据设置为 NULL。

API 参考
********

.. doxygengroup:: bt_gatt

GATT 服务器
===========

.. doxygengroup:: bt_gatt_server

GATT 客户端
===========

.. doxygengroup:: bt_gatt_client
