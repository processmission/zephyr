.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_connection_mgmt:

连接管理
########

Zephyr 蓝牙协议栈使用名为 :c:struct:`bt_conn` 的抽象来表示与其他设备的连接。该结构体的内部实现不向应用公开，但可以使用 :c:func:`bt_conn_get_info` API 获取有限的信息（例如远端地址）。连接对象采用引用计数，当应用需要长时间保存连接指针时，应使用 :c:func:`bt_conn_ref` API，以确保该对象保持有效（即使连接断开）。类似地，释放连接引用时应使用 :c:func:`bt_conn_unref` API。

一个常见错误是忘记释放由 :c:func:`bt_conn_le_create` 和 :c:func:`bt_conn_le_create_synced` 函数创建的连接对象的引用。为防止这种情况，可使用 :kconfig:option:`CONFIG_BT_CONN_CHECK_NULL_BEFORE_CREATE` Kconfig 选项，该选项会强制这些函数在传入的连接指针不为 NULL 时返回错误。这有助于发现此类问题，并避免因未释放连接对象而导致的偶发缺陷。

应用可以通过使用 :c:func:`bt_conn_cb_register` 或 :c:macro:`BT_CONN_CB_DEFINE` API 注册 :c:struct:`bt_conn_cb` 结构体来跟踪连接。该结构体允许应用为连接和断开事件，以及与连接相关的其他事件（例如安全级别或连接参数的变化）定义回调。当应用充当中心设备（central）时，还可以通过 :c:func:`bt_conn_le_create` API 的返回值获取连接对象。

API 参考
********

.. doxygengroup:: bt_conn
