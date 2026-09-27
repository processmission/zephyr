.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_mgmt_interface:

网络管理
########

.. contents::
    :local:
    :depth: 2

概述
****

网络管理 API 允许应用以及网络层代码本身在 IP 协议栈的任意层调用已定义的网络例程，或者接收相关网络事件的通知。例如，应用代码可以使用这些 API 请求在基于 Wi-Fi 或 Bluetooth 的网络接口上执行扫描，或者在网络接口 IP 地址发生变化时请求通知。

网络管理 API 的实现旨在通过在构建时剔除未使用的管理例程代码来节省内存。它不使用各自独立、静态定义的网络管理过程 API，而是通过 :c:macro:`NET_MGMT_REGISTER_REQUEST_HANDLER` 宏注册已定义的过程处理程序。过程请求通过单个 :c:func:`net_mgmt` API 发起，该 API 会调用与相应请求关联的已注册处理程序。

当前实现是实验性的，在未来的版本中可能会发生变化和改进。

请求已定义的过程
****************

所有网络管理请求的形式都是 ``net_mgmt(mgmt_request, ...)``。``mgmt_request`` 参数是一个位掩码，用于指明所针对的协议栈层、是否隐含 ``net_if`` 对象，以及所请求的具体管理过程。可用的过程请求取决于协议栈中已实现的内容。

为避免额外开销，所有 :c:func:`net_mgmt` 调用都是直接的。尽管这一点在未来的版本中可能改变，但不会影响该函数的使用者。

.. _net_mgmt_listening:

监听网络事件
************

通过注册回调函数并指定一组用于过滤回调触发时机的网络事件，即可接收网络事件通知。对于每一对层和代码，回调必须是唯一的；而在命令部分，它是一组事件的掩码。

运行时有两个可用函数：:c:func:`net_mgmt_add_event_callback` 用于注册回调函数，:c:func:`net_mgmt_del_event_callback` 用于注销回调。辅助函数 :c:func:`net_mgmt_init_event_callback` 可用于简化回调结构体的初始化。

此外，可以使用 :c:macro:`NET_MGMT_REGISTER_EVENT_HANDLER` 在编译时注册回调处理程序。

当发生与某个回调的事件集合匹配的事件时，会以实际的事件代码调用关联的回调函数。因此，如有需要，同一个回调函数可以处理不同的事件。

.. warning::

   事件集合过滤对于层和层代码相同的事件会产生误报。回调处理函数 **必须** 将传入的事件代码（作为参数）与它要处理的特定网络事件进行比对，**无论** 传给 :c:func:`net_mgmt_init_event_callback` 的集合中有多少个事件。

   请注意，要接收来自多个层的事件，必须注册多个监听器，每个被监听的层各一个。回调处理函数可以在不同层的事件之间共享。

   （对于层和层代码相同的事件会出现误报。）

示例如下。

.. code-block:: c

        /*
         * Set of events to handle.
         * See e.g. include/zephyr/net/net_event.h for some NET_EVENT_xxx values.
         */
        #define EVENT_IFACE_SET (NET_EVENT_IF_xxx | NET_EVENT_IF_yyy)
        #define EVENT_IPV4_SET (NET_EVENT_IPV4_xxx | NET_EVENT_IPV4_yyy)

        struct net_mgmt_event_callback iface_callback;
        struct net_mgmt_event_callback ipv4_callback;

        void callback_handler(struct net_mgmt_event_callback *cb,
                              uint64_t mgmt_event,
                              struct net_if *iface)
        {
                if (mgmt_event == NET_EVENT_IF_xxx) {
                        /* Handle NET_EVENT_IF_xxx */
                } else if (mgmt_event == NET_EVENT_IF_yyy) {
                        /* Handle NET_EVENT_IF_yyy */
                } else if (mgmt_event == NET_EVENT_IPV4_xxx) {
                        /* Handle NET_EVENT_IPV4_xxx */
                } else if (mgmt_event == NET_EVENT_IPV4_yyy) {
                        /* Handle NET_EVENT_IPV4_yyy */
                } else {
                        /* Spurious (false positive) invocation. */
                }
        }

        void register_cb(void)
        {
                net_mgmt_init_event_callback(&iface_callback, callback_handler,
                                             EVENT_IFACE_SET);
                net_mgmt_init_event_callback(&ipv4_callback, callback_handler,
                                             EVENT_IPV4_SET);
                net_mgmt_add_event_callback(&iface_callback);
                net_mgmt_add_event_callback(&ipv4_callback);
        }

或者类似地使用 :c:macro:`NET_MGMT_REGISTER_EVENT_HANDLER`。

.. note::

   ``info`` 和 ``info_length`` 参数只有在启用 :kconfig:option:`CONFIG_NET_MGMT_EVENT_INFO` 时才能使用，否则它们为 ``NULL`` 和零。

.. code-block:: c

        /*
         * Set of events to handle.
         */
        #define EVENT_IFACE_SET (NET_EVENT_IF_xxx | NET_EVENT_IF_yyy)
        #define EVENT_IPV4_SET (NET_EVENT_IPV4_xxx | NET_EVENT_IPV4_yyy)

        static void event_handler(uint64_t mgmt_event, struct net_if *iface,
                                  void *info, size_t info_length,
                                  void *user_data)
        {
                if (mgmt_event == NET_EVENT_IF_xxx) {
                        /* Handle NET_EVENT_IF_xxx */
                } else if (mgmt_event == NET_EVENT_IF_yyy) {
                        /* Handle NET_EVENT_IF_yyy */
                } else if (mgmt_event == NET_EVENT_IPV4_xxx) {
                        /* Handle NET_EVENT_IPV4_xxx */
                } else if (mgmt_event == NET_EVENT_IPV4_yyy) {
                        /* Handle NET_EVENT_IPV4_yyy */
                } else {
                        /* Spurious (false positive) invocation. */
                }
        }

        NET_MGMT_REGISTER_EVENT_HANDLER(iface_event_handler, EVENT_IFACE_SET,
                                        event_handler, NULL);
        NET_MGMT_REGISTER_EVENT_HANDLER(ipv4_event_handler, EVENT_IPV4_SET,
                                        event_handler, NULL);

可监听的通用核心事件见 :zephyr_file:`include/zephyr/net/net_event.h`。


定义网络管理过程
****************

可以为自己的协议栈实现提供额外的管理过程：定义一个处理程序，并将其与关联的 mgmt_request 代码一起注册。

管理请求代码定义在相关位置，具体取决于所针对的层；如果目标是 L2 层，则还取决于具体技术。例如，所有 IP 层管理请求代码都可以在 :zephyr_file:`include/zephyr/net/net_event.h` 头文件中找到；而对于 L2 技术（比如以太网），这些代码则位于 :zephyr_file:`include/zephyr/net/ethernet.h`。

定义采用该签名的处理程序：

.. code-block:: c

   static int your_handler(uint64_t mgmt_event, struct net_if *iface,
                           void *data, size_t len);

然后将其与关联的 mgmt_request 代码一起注册：

.. code-block:: c

   NET_MGMT_REGISTER_REQUEST_HANDLER(<mgmt_request code>, your_handler);

此后可以使用以下方式调用这个新的管理过程：

.. code-block:: c

   net_mgmt(<mgmt_request code>, ...);


发出网络事件信号
****************

可以使用 :c:func:`net_mgmt_event_notify` 函数并提供网络事件代码来发出特定网络事件的信号，详情见 :zephyr_file:`include/zephyr/net/net_mgmt.h`。与管理请求代码类似，事件代码也可以在特定 L2 技术的管理头文件中找到；例如，如果要监听 802.15.4 L2 的事件，:zephyr_file:`include/zephyr/net/ieee802154_mgmt.h` 就是合适的位置。

API 参考
********

.. doxygengroup:: net_mgmt
