.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _conn_mgr_overview:

概述
####

连接管理器 是一组可选的 Zephyr 功能，旨在让应用能够以尽可能少关注底层网络技术细节的方式，监控和控制连接性（对支持 IP 的网络的访问）。

借助 连接管理器，应用可以使用单一的抽象 API 控制网络关联并监控互联网访问，避免过度使用特定于技术的样板代码。

这使应用有可能用单一代码库支持多种差异很大的连接性技术（例如 Wi-Fi 和 LTE）。

应用还可以使用 连接管理器 以通用方式同时管理和使用多种连接性技术。

结构
====

连接管理器 分为以下两个子系统：

* :ref:`连接性监控 <conn_mgr_monitoring>` （头文件 :file:`include/zephyr/net/conn_mgr_monitoring.h`）监控所有可用的 :ref:`Zephyr 网络接口（接口） <net_if_interface>`，并触发 :ref:`网络管理 <net_mgmt_interface>` 事件，以指示何时获得或丢失 IP 连接。

* :ref:`连接控制 <conn_mgr_control>` （头文件 :file:`include/zephyr/net/conn_mgr_connectivity.h`）提供用于控制接口网络关联的抽象 API。

.. _conn_mgr_integration_diagram_simple:

.. figure:: figures/integration_diagram_simplified.svg
    :alt: A simplified view of how Connection Manager integrates with Zephyr and the application.
    :figclass: align-center

    连接管理器 如何与 Zephyr 和应用集成的简化视图。

    有关更详细的版本，请参阅 :ref:`此处 <conn_mgr_integration_diagram_detailed>`。

.. _conn_mgr_monitoring:

连接性监控
##########

连接性监控会跟踪所有可用接口（无论它们是否支持 :ref:`连接控制 <conn_mgr_control>`）在各种 :ref:`运行状态 <net_if_interface_state_management>` 之间转换以及获取或丢失分配的 IP 地址的过程。

如果某个可用接口满足以下条件，则认为该接口已就绪：

* 接口处于 admin-up 状态

  * 这意味着已指示该接口进入 operational-up（可供使用）状态。这是通过调用 :c:func:`net_if_up` 完成的。

* 接口处于 oper-up 状态

  * 这意味着接口已完全可供使用；它已在线，并且在适用的情况下已与网络关联。
  * 有关详细信息，请参阅 :ref:`net_if_interface_state_management`。

* 接口至少分配了一个 IP 地址

  * IPv4 和 IPv6 地址均可接受。只要分配了其中之一或两者，就满足此条件。
  * 有关接口 IP 分配的详细信息，请参阅 :ref:`net_if_interface`。

* 接口未被忽略

  * 被忽略的接口始终被视为未就绪。
  * 有关更多详细信息，请参阅 :ref:`conn_mgr_monitoring_ignoring_ifaces`。

.. note::

   通常，接口状态和 IP 分配由接口的 :ref:`L2 实现 <net_l2_interface>` 或绑定的 :ref:`连接性实现 <conn_mgr_impl>` 更新。

   有关详细信息，请参阅 :ref:`conn_mgr_impl_guidelines_iface_state_reporting`。

已就绪的接口一旦丢失上述任一条件，就不再处于就绪状态。

当至少有一个接口就绪时，会触发 :c:macro:`NET_EVENT_L4_CONNECTED` :ref:`网络管理 <net_mgmt_interface>` 事件，此时称 IP 连接性已就绪。

此后，只要始终至少有一个就绪接口，接口就可以在不触发额外事件的情况下变为就绪或未就绪。

当不再有任何就绪接口时，会触发 :c:macro:`NET_EVENT_L4_DISCONNECTED` :ref:`网络管理 <net_mgmt_interface>` 事件，此时称 IP 连接性未就绪。

.. note::

   连接管理器 还会触发以下更具体的 ``CONNECTED`` / ``DISCONNECTED`` 事件：

   - :c:macro:`NET_EVENT_L4_IPV4_CONNECTED`
   - :c:macro:`NET_EVENT_L4_IPV4_DISCONNECTED`
   - :c:macro:`NET_EVENT_L4_IPV6_CONNECTED`
   - :c:macro:`NET_EVENT_L4_IPV6_DISCONNECTED`

   这些事件与 :c:macro:`NET_EVENT_L4_CONNECTED` 和 :c:macro:`NET_EVENT_L4_DISCONNECTED` 类似，但专门跟踪支持 IPv4 和 IPv6 的接口是否就绪。

.. _conn_mgr_monitoring_usage:

用法
====

如果启用了 :kconfig:option:`CONFIG_NET_CONNECTION_MANAGER` Kconfig 选项，则启用连接性监控。

要接收连接性更新，请为 :c:macro:`NET_EVENT_L4_CONNECTED` 和 :c:macro:`NET_EVENT_L4_DISCONNECTED` :ref:`网络管理 <net_mgmt_interface>` 事件创建并注册监听器：

.. code-block:: c

   /* Callback struct where the callback will be stored */
   struct net_mgmt_event_callback l4_callback;

   /* Callback handler */
   static void l4_event_handler(struct net_mgmt_event_callback *cb,
                                uint32_t event, struct net_if *iface)
   {
           if (event == NET_EVENT_L4_CONNECTED) {
                   LOG_INF("Network connectivity gained!");
           } else if (event == NET_EVENT_L4_DISCONNECTED) {
                   LOG_INF("Network connectivity lost!");
           }

           /* Otherwise, it's some other event type we didn't register for. */
   }

   /* Call this before Connection Manager monitoring initializes */
   static void my_application_setup(void)
   {
           /* Configure the callback struct to respond to (at least) the L4_CONNECTED
            * and L4_DISCONNECTED events.
            *
            *
            * Note that the callback may also be triggered for events other than those specified here!
            * (See the net_mgmt documentation)
            */
           net_mgmt_init_event_callback(
                   &l4_callback, l4_event_handler,
                   NET_EVENT_L4_CONNECTED | NET_EVENT_L4_DISCONNECTED
           );

           /* Register the callback */
           net_mgmt_add_event_callback(&l4_callback);
   }

还可以使用 :c:macro:`NET_MGMT_REGISTER_EVENT_HANDLER` 在编译时而不是运行时注册回调处理程序。这样可以确保回调在 连接管理器 监控初始化之前完成注册。

.. code-block:: c

   static void l4_event_handler(uint64_t event, struct net_if *iface, void *info,
                                size_t info_length, void *user_data)
   {
           if (event == NET_EVENT_L4_CONNECTED) {
                   LOG_INF("Network connectivity gained!");
           } else if (event == NET_EVENT_L4_DISCONNECTED) {
                   LOG_INF("Network connectivity lost!");
           }

           /* Otherwise, it's some other event type we didn't register for. */
   }

   NET_MGMT_REGISTER_EVENT_HANDLER(l4_callback, l4_event_handler,
                                   NET_EVENT_L4_CONNECTED | NET_EVENT_L4_DISCONNECTED, NULL);

有关监听 net_mgmt 事件的更多详细信息，请参阅 :ref:`net_mgmt_listening`。

.. note::
   为避免错过初始连接性事件，应在 连接管理器 监控初始化之前注册监听器。有关确保这一点的策略，请参阅 :ref:`conn_mgr_monitoring_missing_notifications`。

.. _conn_mgr_monitoring_missing_notifications:

避免错过通知
============

连接性监控在初始化时可能会立即触发事件。

如果应用在连接性监控初始化之后才注册事件监听器，则可能会错过这第一波事件，从而在首次获得网络连接时无法收到通知。

如果存在此问题，应用应在连接性监控初始化之前 :ref:`注册事件监听器 <conn_mgr_monitoring_usage>`。

连接性监控使用由 :kconfig:option:`CONFIG_NET_CONNECTION_MANAGER_MONITOR_PRIORITY` Kconfig 选项指定的 :c:macro:`SYS_INIT` ``APPLICATION`` 初始化优先级进行初始化。

你可以使用具有比该值更早初始化优先级的 :c:macro:`SYS_INIT` 在此初始化之前注册回调，例如优先级 0：

.. code-block:: C

   static int my_application_setup(void)
   {
           /* Register callbacks here */
           return 0;
   }

   SYS_INIT(my_application_setup, APPLICATION, 0);

如果这不可行，也可以随时调用 :c:func:`conn_mgr_mon_resend_status`，请求连接性监控重新发送最新的连接性事件：

.. code-block:: C

   static void my_late_application_setup(void)
   {
     /* Register callbacks here */

     /* Once done, request that events be re-triggered */
     conn_mgr_mon_resend_status();
   }

.. _conn_mgr_monitoring_ignoring_ifaces:

忽略接口
========

应用可以调用 :c:func:`conn_mgr_ignore_iface` 并传入要忽略的接口，请求 连接管理器 忽略这些接口。

或者，可以调用 :c:func:`conn_mgr_ignore_l2` 来忽略整个 :ref:`L2 实现 <net_l2_interface>`。

这样做的效果是单独忽略使用该 :ref:`L2 实现 <net_l2_interface>` 的所有接口。

被忽略时，无论接口的实际状态如何，连接管理器 都会将其视为未准备好处理网络流量。

例如，如果应用配置了一个或多个无法（或由于任何原因不应）用于联系更广泛互联网的接口，这可能很有用。

:ref:`批量便捷函数 <conn_mgr_control_api_bulk>` 可以选择跳过被忽略的接口。

有关更多详细信息，请参阅 :c:func:`conn_mgr_ignore_iface` 和 :c:func:`conn_mgr_watch_iface`。

.. _conn_mgr_monitoring_api:

连接性监控 API
==============

包含头文件 :file:`include/zephyr/net/conn_mgr_monitoring.h` 以访问这些内容。

.. doxygengroup:: conn_mgr

.. _conn_mgr_control:

连接控制
########

许多网络接口需要先完成网络关联过程，然后才能使用。

对于此类接口，连接控制可以提供一个通用 API 来请求网络关联（:c:func:`conn_mgr_if_connect`）和取消关联（:c:func:`conn_mgr_if_disconnect`）。网络接口通过 :ref:`将自身绑定到连接性实现 <conn_mgr_impl_binding>` 来实现对此 API 的支持。

使用此 API，应用可以以最少的特定于技术的样板代码与网络关联。

连接控制还提供以下附加功能：

* 在关联期间提供标准化的 :ref:`持久性和超时 <conn_mgr_control_persistence_timeouts>` 行为。
* :ref:`批量函数 <conn_mgr_control_api_bulk>`，用于同时控制所有可用接口的管理状态和网络关联。
* 用于常见连接性操作的可选 :ref:`便捷自动化 <conn_mgr_control_automations>`。

.. _conn_mgr_control_operation:

基本操作
========

以下各节概述 连接管理器 连接控制的基本操作。

.. _conn_mgr_control_operation_binding:

绑定
----

在可以使用 连接管理器 命令接口进行关联或取消关联之前，必须先将其绑定到 :ref:`连接性实现 <conn_mgr_impl>`。绑定由接口的提供者执行，而不是由应用执行（请参阅 :ref:`conn_mgr_impl_binding`），可以将其视为接口声明的扩展。

接口绑定后，传递给它的所有连接性命令（例如 :c:func:`conn_mgr_if_connect` 或 :c:func:`conn_mgr_if_disconnect`）都将路由到连接性实现中对应的实现函数。

.. note::

  为避免行为不一致，所有连接性实现都必须遵守 :ref:`实现指南 <conn_mgr_impl_guidelines>`。

.. _conn_mgr_control_operation_connecting:

连接
----

绑定的接口处于 admin-up（请参阅 :ref:`net_if_interface_state_management`）后，可以调用 :c:func:`conn_mgr_if_connect` 使其与网络关联。

如果关联成功，连接性实现会将接口标记为 operational-up（请参阅 :ref:`net_if_interface_state_management`）。

如果关联失败且无法恢复，将触发 :ref:`致命错误事件 <conn_mgr_control_events_fatal_error>`。

你可以为此过程配置可选的 :ref:`超时 <conn_mgr_control_timeouts>`。

.. note::
   :c:func:`conn_mgr_if_connect` 函数有意保持极简，不接受任何形式的配置。每个连接性实现应提供一种方法来预配置或自动配置任何所需的关联设置或凭据。有关详细信息，请参阅 :ref:`conn_mgr_impl_guidelines_preconfig`。

.. _conn_mgr_control_operation_loss:

连接丢失
--------

如果连接性因外部因素丢失，连接性实现会将接口标记为 operational-down。

根据是否设置了 :ref:`持久性 <conn_mgr_control_persistence>`，接口随后可能会尝试重新连接。

.. _conn_mgr_control_operation_disconnection:

手动断开连接
------------

应用还可以通过调用 :c:func:`conn_mgr_if_disconnect` 请求有意放弃连接性。

在这种情况下，连接性实现将使接口与其网络取消关联，并将接口标记为 operational-down（请参阅 :ref:`net_if_interface_state_management`）。无论是否启用持久性，都不会发起新的连接尝试。

.. _conn_mgr_control_persistence_timeouts:

超时和持久性
============

连接管理器 要求所有连接性实现支持以下标准关键功能：

* :ref:`连接超时 <conn_mgr_control_timeouts>`
* :ref:`连接持久性 <conn_mgr_control_persistence>`

这些功能描述了接口在连接和断开连接事件期间应如何表现。你可以为每个接口单独设置它们。

.. note::
   连接性实现需负责按以下所述成功且准确地实现这两项功能。有关从连接性实现角度的更多详细信息，请参阅 :ref:`conn_mgr_impl_timeout_persistence`。

连接管理器 还实现了以下可选功能：

* :ref:`接口空闲超时 <conn_mgr_control_idle_timeout>`

.. note::
   连接性实现实现空闲超时的唯一要求是，在每次使用接口时调用 :c:func:`conn_mgr_if_used`。

.. _conn_mgr_control_timeouts:

连接超时
--------

当对接口调用 :c:func:`conn_mgr_if_connect` 时，会开始一次连接尝试。

连接尝试会无限期持续，直到成功为止，除非为该接口指定了超时（使用 :c:func:`conn_mgr_if_set_timeout`）。

在这种情况下，如果超时在成功之前结束，则将放弃该连接尝试。如果发生这种情况，会引发 :ref:`超时事件 <conn_mgr_control_events_timeout>`。

.. _conn_mgr_control_idle_timeout:

接口空闲超时
------------

连接管理器允许用户在接口上设置不活动超时（:c:func:`conn_mgr_if_set_idle_timeout`）。一旦连接，如果接口在配置的秒数内没有任何活动，接口会自动断开连接。如果发生这种情况，会引发 :ref:`空闲超时事件 <conn_mgr_control_events_idle_timeout>`。就 :ref:`连接持久性 <conn_mgr_control_persistence>` 而言，空闲超时被视为非故意的连接丢失。

.. _conn_mgr_control_persistence:

连接持久性
----------

每个接口还有一个连接持久性设置，你可以通过使用 :c:func:`conn_mgr_binding_set_flag` 设置 :c:enumerator:`CONN_MGR_IF_PERSISTENT` 标志来启用或禁用该设置。

此设置指定接口应如何处理非故意的连接丢失。

如果启用了持久性，任何非故意的连接丢失都将发起新的连接尝试，并在适用时使用新的超时。

否则，接口将不会尝试重新连接。

.. note::
   持久性不会影响连接尝试行为，只有超时设置会影响此行为。

   例如，如果接口上的连接尝试超时，即使该接口是持久性的，它也不会尝试重新连接。

   相反，如果没有指定超时，即使接口不是持久性的，它也会一直尝试连接，直到成功。

   有关等效的实现指南，请参阅 :ref:`conn_mgr_impl_tp_persistence_during_connect`。

.. _conn_mgr_control_events:

控制事件
========

连接控制会触发 :ref:`网络管理 <net_mgmt_interface>` 事件，以将重要状态变化告知应用。

有关对应的连接性实现指南，请参阅 :ref:`conn_mgr_impl_guidelines_trigger_events`。

.. _conn_mgr_control_events_fatal_error:

致命错误
--------

当接口遇到无法恢复的错误（意味着后续任何关联尝试都必定失败，并且应放弃所有此类尝试）时，会引发 :c:macro:`NET_EVENT_CONN_IF_FATAL_ERROR` 事件。

此事件的处理程序将收到一个指向发生致命错误的接口的指针。各个连接性实现还可以传递应用特定的数据指针。

.. _conn_mgr_control_events_timeout:

超时
----

当 :ref:`接口关联 <conn_mgr_control_operation_connecting>` 尝试 :ref:`超时 <conn_mgr_control_timeouts>` 时，会引发 :c:macro:`NET_EVENT_CONN_IF_TIMEOUT` 事件。

此事件的处理程序将收到一个指向关联尝试超时的接口的指针。

.. _conn_mgr_control_events_idle_timeout:

空闲超时
--------

当接口被视为 :ref:`不活动 <conn_mgr_control_idle_timeout>` 时，会引发 :c:macro:`NET_EVENT_CONN_IF_IDLE_TIMEOUT` 事件。

此事件的处理程序将收到一个指向关联尝试超时的接口的指针。

.. _conn_mgr_control_events_listening:

监听控制事件
------------

你可以按如下方式监听控制事件：

.. code-block:: c

   /* Declare a net_mgmt callback struct to store the callback */
   struct net_mgmt_event_callback my_conn_evt_callback;

   /* Declare a handler to receive control events */
   static void my_conn_evt_handler(struct net_mgmt_event_callback *cb,
                                   uint32_t event, struct net_if *iface)
   {
           if (event == NET_EVENT_CONN_IF_TIMEOUT) {
                   /* Timeout occurred, handle it */
           } else if (event == NET_EVENT_CONN_IF_FATAL_ERROR) {
                   /* Fatal error occurred, handle it */
           }

           /* Otherwise, it's some other event type we didn't register for. */
   }

   int main()
   {
           /* Configure the callback struct to respond to (at least) the CONN_IF_TIMEOUT
            * and CONN_IF_FATAL_ERROR events.
            *
            * Note that the callback may also be triggered for events other than those specified here!
            * (See the net_mgmt documentation)
            */

           net_mgmt_init_event_callback(
                   &conn_mgr_conn_callback, conn_mgr_conn_handler,
                       NET_EVENT_CONN_IF_TIMEOUT | NET_EVENT_CONN_IF_FATAL_ERROR
           );

           /* Register the callback */
           net_mgmt_add_event_callback(&conn_mgr_conn_callback);
           return 0;
   }

有关监听 net_mgmt 事件的更多详细信息，请参阅 :ref:`net_mgmt_listening`。

.. _conn_mgr_control_automations:

自动化行为
==========

有一些与连接性相关的操作（至少默认情况下）会自动为用户执行。

.. _conn_mgr_control_automations_auto_up:

.. topic:: 自动 admin-up

   在 Zephyr 中，接口在初始化期间会自动进入 admin-up 状态（有关接口状态的详细信息，请参阅 :ref:`net_if_interface_state_management`）。

   应用可以通过使用 :c:func:`net_if_flag_set` 设置 :c:enumerator:`NET_IF_NO_AUTO_START` 接口标志来禁用此行为。

.. _conn_mgr_control_automations_auto_connect:

.. topic:: 自动连接

   默认情况下，连接管理器 会自动连接任何变为 admin-up 的 :ref:`已绑定 <conn_mgr_impl_binding>` 接口。

   应用可以通过使用 :c:func:`conn_mgr_if_set_flag` 设置 :c:enumerator:`CONN_MGR_IF_NO_AUTO_CONNECT` 连接性标志来禁用此行为。

.. _conn_mgr_control_automations_auto_down:

.. topic:: 自动 admin-down

   默认情况下，如果任何已绑定的接口放弃关联，连接管理器 会自动将其置于 admin-down 状态。

   应用可以通过禁用 :kconfig:option:`CONFIG_NET_CONNECTION_MANAGER_AUTO_IF_DOWN` Kconfig 选项来为所有接口禁用此行为，也可以通过使用 :c:func:`conn_mgr_if_set_flag` 设置 :c:enumerator:`CONN_MGR_IF_NO_AUTO_DOWN` 连接性标志来为单个接口禁用此行为。

.. _conn_mgr_control_api:

连接控制 API
============

包含头文件 :file:`include/zephyr/net/conn_mgr_connectivity.h` 以访问这些内容。

.. doxygengroup:: conn_mgr_connectivity

.. _conn_mgr_control_api_bulk:

批量 API
--------

连接控制提供了多个批量函数，可以一次性控制所有接口。

如果需要，你可以将这些函数限制为仅对非 :ref:`被忽略 <conn_mgr_monitoring_ignoring_ifaces>` 的接口进行操作。

包含头文件 :file:`include/zephyr/net/conn_mgr_connectivity.h` 以访问这些内容。

.. doxygengroup:: conn_mgr_connectivity_bulk
