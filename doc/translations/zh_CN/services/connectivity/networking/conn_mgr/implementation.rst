.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _conn_mgr_impl:

连接性实现
##########

.. _conn_mgr_impl_overview:

概述
====

连接性实现是特定于技术的模块，使特定的 Zephyr 接口能够支持 :ref:`连接控制 <conn_mgr_control>`。它们负责将通用的 :ref:`连接控制 API <conn_mgr_control_api>` 调用转换为硬件特定操作，还负责实现标准化的 :ref:`持久性与超时 <conn_mgr_control_persistence_timeouts>` 行为。

有关编写符合规范的连接性实现的详细信息，请参阅 :ref:`实现指南 <conn_mgr_impl_guidelines>`。

.. _conn_mgr_impl_architecture:

架构
====

:ref:`实现 API <conn_mgr_impl_api>` 允许在构建时使用 :c:macro:`CONN_MGR_CONN_DEFINE` :ref:`定义 <conn_mgr_impl_defining>` 连接性实现。

这会创建 :c:struct:`conn_mgr_conn_impl` 结构体的静态实例，该实例随后保存对传入的 :c:struct:`conn_mgr_conn_api` 结构体的引用（应使用实现回调填充该结构体）。

定义后，可以按名称引用实现，并使用 :c:macro:`CONN_MGR_BIND_CONN` 将它们绑定到任何未绑定的接口。请确保不要意外地将两个连接性实现绑定到同一个接口。

接口绑定后，可以在该接口上调用 :ref:`连接控制 API <conn_mgr_control_api>` 函数，这些函数会转换为 :c:struct:`conn_mgr_conn_api` 中对应的实现函数。

绑定接口不会直接修改其 :c:struct:`接口结构体 <net_if>`。

而是会创建一个 :c:struct:`conn_mgr_conn_binding` 实例，并将其追加到内部 :ref:`可迭代段 <iterable_sections_api>`。

该绑定结构体将包含对已绑定接口的引用、该接口所绑定的连接性实现，以及指向每个接口的 :ref:`上下文指针 <conn_mgr_impl_ctx>` 的指针。

随后可以遍历此可迭代段，以查明给定接口绑定了哪个连接性实现（如果有）。:ref:`连接控制 API <conn_mgr_control_api>` 中的大多数函数都使用此搜索过程。因此，由于搜索成本相对较高，应尽量少调用这些函数。

单个连接性实现可以绑定到多个接口。有关更多详细信息，请参阅 :ref:`conn_mgr_impl_guidelines_no_instancing`。

.. _conn_mgr_integration_diagram_detailed:

.. figure:: figures/integration_diagram_detailed.svg
    :alt: A detailed view of how Connection Manager integrates with Zephyr and the application.
    :figclass: align-center

    连接管理器 如何与 Zephyr 和应用集成的详细视图。

    有关简化版本，请参阅 :ref:`此处 <conn_mgr_integration_diagram_simple>`。

.. _conn_mgr_impl_ctx:

上下文指针
==========

由于单个连接性实现可能由多个 Zephyr 接口共享，每个绑定都会实例化一个专属于该绑定的上下文容器（其类型为 :ref:`可配置类型 <conn_mgr_impl_declaring>`）。然后，每个绑定都会使用对该容器的引用进行实例化，实现随后可以使用该引用来访问各接口的状态信息。

另请参阅 :ref:`conn_mgr_impl_guidelines_binding_access` 和 :ref:`conn_mgr_impl_guidelines_no_instancing`。

.. _conn_mgr_impl_defining:

定义实现
========

连接性实现可以按如下方式定义：

.. code-block:: c

   /* Create the API implementation functions */
   int my_connect_impl(struct conn_mgr_conn_binding *const binding) {
           /* Cause your underlying technology to associate */
   }
   int my_disconnect_impl(struct conn_mgr_conn_binding *const binding) {
           /* Cause your underlying technology to disassociate */
   }
   void my_init_impl(struct conn_mgr_conn_binding *const binding) {
           /* Perform any required initialization for your underlying technology */
   }

   /* Declare the API struct */
   static struct conn_mgr_conn_api my_impl_api = {
           .connect = my_connect_impl,
           .disconnect = my_disconnect_impl,
           .init = my_init_impl,
           /* ... so on */
   };

   /* Define the implementation (named MY_CONNECTIVITY_IMPL) */
   CONN_MGR_CONN_DEFINE(MY_CONNECTIVITY_IMPL, &my_impl_api);

.. note::
   除非你还 :ref:`声明上下文指针类型 <conn_mgr_impl_declaring_ctx>`，否则这不会生效。

.. _conn_mgr_impl_declaring:

公开声明实现
============

定义后，可以通过在头文件中声明连接性实现，使其可供其他编译单元使用，如下所示：

.. code-block:: c
   :caption: ``my_connectivity_header.h``

   CONN_MGR_CONN_DECLARE_PUBLIC(MY_CONNECTIVITY_IMPL);

包含此声明的头文件必须包含在任何需要引用该实现的编译单元中。

.. _conn_mgr_impl_declaring_ctx:

声明上下文类型
==============

为使 :c:macro:`CONN_MGR_CONN_DEFINE` 生效，你必须声明相应的上下文指针类型。这是因为所有连接性绑定都包含其关联上下文指针类型的 :ref:`conn_mgr_impl_ctx`。

如果你使用 :c:macro:`CONN_MGR_CONN_DECLARE_PUBLIC`，请在声明的同时声明此类型：

.. code-block:: c
   :caption: ``my_connectivity_impl.h``

   #define MY_CONNECTIVITY_IMPL_CTX_TYPE struct my_context_type *
   CONN_MGR_CONN_DECLARE_PUBLIC(MY_CONNECTIVITY_IMPL);

然后，确保在调用 :c:macro:`CONN_MGR_CONN_DEFINE` 之前包含该头文件：

.. code-block:: c
   :caption: ``my_connectivity_impl.c``

   #include "my_connectivity_impl.h"

   CONN_MGR_CONN_DEFINE(MY_CONNECTIVITY_IMPL, &my_impl_api);

否则，只需在调用 :c:macro:`CONN_MGR_CONN_DEFINE` 之前直接声明该上下文指针类型即可：

.. code-block:: c

   #define MY_CONNECTIVITY_IMPL_CTX_TYPE struct my_context_type *
   CONN_MGR_CONN_DEFINE(MY_CONNECTIVITY_IMPL, &my_impl_api);

.. note::

   命名很重要。上下文指针类型声明必须使用与实现声明相同的名称，但需附加 ``_CTX_TYPE``。

   在上一个示例中，上下文类型命名为 ``MY_CONNECTIVITY_IMPL_CTX_TYPE``，因为 ``MY_CONNECTIVITY_IMPL`` 被用作连接性实现名称。

如果连接性实现不需要上下文指针，只需将该类型声明为 void：

.. code-block:: c

   #define MY_CONNECTIVITY_IMPL_CTX_TYPE void *

.. _conn_mgr_impl_binding:

将接口绑定到实现
================

已定义的连接性实现可以在接口的设备定义之后的任何位置通过调用 :c:macro:`CONN_MGR_BIND_CONN` 绑定到该接口：

.. code-block:: c

        /* Define an iface */
        NET_DEVICE_INIT(my_iface,
                /* ... the specifics here don't matter ... */
        );

        /* Now bind MY_CONNECTIVITY_IMPL to that iface --
         * the name used should match with the above
         */
        CONN_MGR_BIND_CONN(my_iface, MY_CONNECTIVITY_IMPL);

.. _conn_mgr_impl_guidelines:

连接性实现指南
==============

与其集中实现所有功能，连接管理器 依赖于每个连接性实现单独实现许多行为和功能。

这种方法使 连接管理器 保持精简，并允许每个连接性实现为自身选择最适合这些行为的方案。但是，它依赖于信任，即所有连接性实现都会忠实实现委托给它们的功能。

为了保持所有连接性实现之间的一致性，在编写自己的实现时请遵循以下指南：

.. _conn_mgr_impl_guidelines_timeout_persistence:

*完全实现超时和持久性*
----------------------

所有连接性实现都必须为 :ref:`超时和持久性 <conn_mgr_control_persistence_timeouts>` 提供完整支持，使用户能够禁用或启用这些功能，而无论底层技术固有的行为如何。换言之，无论底层技术如何行为，你的实现都必须使最终用户看到的行为完全符合 :ref:`conn_mgr_control_persistence_timeouts` 一节中的规定。

有关实现超时和持久性的详细技术讨论，请参阅 :ref:`conn_mgr_impl_timeout_persistence`。

.. _conn_mgr_impl_guidelines_conformity:

*符合 API 规范*
---------------

你实现的每个 :c:struct:`实现 API 函数 <conn_mgr_conn_api>` 都应具有对应连接控制 API 函数所描述的行为。

例如，你对 :c:member:`conn_mgr_conn_api.connect` 的实现应符合 :c:func:`conn_mgr_if_connect` 所描述的行为。

.. _conn_mgr_impl_guidelines_preconfig:

*允许连接预先配置*
------------------

连接性实现应提供一种方式，使应用能够在调用 :c:func:`conn_mgr_if_connect` 之前预先配置所有必要的连接参数（例如网络 SSID 或 PSK，如适用）。这些信息不必作为 :c:func:`conn_mgr_if_connect` 调用的一部分提供，也不必在该调用之后提供，但实现 :ref:`在未提供这些信息时应等待 <conn_mgr_impl_guidelines_await_config>`。

.. _conn_mgr_impl_guidelines_await_config:

*等待有效的连接配置*
--------------------

如果由于应用预配置了无效的连接参数，或根本没有配置连接参数而导致网络关联失败，则应将此视为网络故障。

换言之，即使尚未配置有效的连接参数，连接性实现也不应放弃连接尝试。

相反，连接性实现应异步等待有效的连接参数被配置，可以无限期等待，也可以等到配置的 :ref:`连接超时 <conn_mgr_control_timeouts>` 结束。

例外情况是：网络接口已配置为非持久性，并且连接性实现为 :c:member:`conn_mgr_conn_api.has_connection_config` 定义了实现。

在这种情况下，为了降低功耗并避免不必要的状态转换，如果 :c:member:`conn_mgr_conn_api.has_connection_config` 返回 ``false``，则 :c:func:`conn_mgr_if_connect` 将提前退出，而不会使接口启动。同时会发出 :c:enum:`NET_EVENT_CONN_IF_NO_CONFIGURATION` 事件，以通知订阅者配置错误。

.. _conn_mgr_impl_guidelines_iface_state_reporting:

*实现接口状态报告*
------------------

所有连接性实现都必须使绑定的接口状态保持最新。

具体而言：

* 在 :c:member:`绑定初始化 <conn_mgr_conn_api.init>` 期间，将接口设置为休眠状态、载波关闭状态，或同时设置为两者。

  *  有关接口载波和休眠状态的详细信息，请参阅 :ref:`net_if_interface_state_management`。

* 更新休眠和载波状态，使接口在关联完成且连接性就绪时（且仅在此时）处于非休眠和载波开启状态。
* 一旦检测到服务中断，就将接口设置为休眠或载波关闭状态。

  * 对于服务通常间歇性的网络技术，可以将此操作置于一个较小的超时（与连接超时分开）之后，这是可以接受的。

* 如果该技术还处理 IP 分配，请确保这些 IP 地址 :ref:`已分配给接口 <net_if_interface_ip_management>`。

.. note::

   接口状态更新不一定需要由连接性实现直接执行。

   例如：

   * 如果为接口使用 :ref:`DHCP <dhcpv4_interface>`，则不需要进行 IP 分配。
   * 如果底层 :ref:`L2 实现 <net_l2_interface>` 已经更新了接口休眠状态，则连接性实现无需再更新。

.. _conn_mgr_impl_guidelines_iface_state_writeonly:

*不要将接口状态用作实现状态*
----------------------------

Zephyr 接口可能会被其他线程访问，而不遵守绑定互斥锁。因此，在连接性实现回调期间，Zephyr 接口状态可能会不可预测地变化。

因此，不要基于接口状态来确定实现行为。

保持接口状态更新以反映网络可用性，但不要出于任何目的读取接口状态。

如果需要跟踪休眠或 IP 分配，请使用存储在 :ref:`上下文指针 <conn_mgr_impl_ctx>` 中的单独状态变量。

.. _conn_mgr_impl_guidelines_non_interference:

*保持无干扰*
------------

连接性实现不应阻止应用直接与相关的特定技术 API 交互。

换言之，应用应能直接使用底层技术，而不会破坏连接性实现。

如果确实需要例外情况，应将其限制在特定 API 调用中，并应记录在文档中。

.. note::

   虽然连接性实现不能中断，但如果应用试图直接控制关联状态，实现出现潜在意外行为是可以接受的。

   例如，如果应用直接指示底层技术断开关联，连接性实现将此解释为意外连接丢失并立即尝试重新关联，是可以接受的。

.. _conn_mgr_impl_guidelines_non_blocking:

*保持非阻塞*
------------

所有连接性实现回调都应为非阻塞。

例如，对 :c:member:`conn_mgr_conn_api.connect` 的调用应启动连接过程并立即返回。

一个例外是 :c:member:`conn_mgr_conn_api.init`，其实现允许阻塞。

但是，请记住，在此回调期间阻塞会延迟系统初始化，因此仍应考虑将耗时任务卸载到后台线程。

.. _conn_mgr_impl_guidelines_immediate_api_readiness:

*使 API 立即可用*
-----------------

连接性实现必须能够在 :c:member:`conn_mgr_conn_api.init` 之后立即接收 API 调用。

例如，即使是在 :c:member:`conn_mgr_conn_api.init` 之后立即调用，对 :c:member:`conn_mgr_conn_api.connect` 的调用最终也必须导致一次关联尝试。

如果在调用 :c:member:`conn_mgr_conn_api.init` 时，底层技术无法立即准备好接受连接命令，则必须以非阻塞方式排队对 :c:member:`conn_mgr_conn_api.connect` 的调用，并在准备就绪后执行。

.. _conn_mgr_impl_guidelines_context_pointer:

*不要将状态信息存储在上下文指针之外*
------------------------------------

连接管理器 会为每个绑定提供一个上下文指针。

连接性实现应将所有状态信息存储在此上下文指针中。

唯一的例外是只打算绑定到单个接口的连接性实现。此类实现可以使用静态声明的状态。

另请参阅 :ref:`conn_mgr_impl_guidelines_no_instancing`。

.. _conn_mgr_impl_guidelines_iface_access:

*仅通过绑定结构体访问接口*
--------------------------

不要使用静态声明的接口，也不要从外部获取接口引用。

例如，不要假设绑定的接口将是默认接口而使用 :c:func:`net_if_get_default`。

相反，请始终使用相关 :c:struct:`绑定结构体 <conn_mgr_conn_binding>` 提供的 :c:member:`接口指针 <conn_mgr_conn_binding.iface>`。另请参阅 :ref:`conn_mgr_impl_guidelines_binding_access`。

.. _conn_mgr_impl_guidelines_bindings_optional:

*在编译时使实现可选*
--------------------

连接性实现应提供 Kconfig 选项，以便在不影响绑定接口可用性的情况下启用或禁用该实现。

换言之，应该可以配置这样的构建：包含 连接管理器 以及本应绑定到该实现的接口，但不包含实现本身，也不包含其绑定。

.. _conn_mgr_impl_guidelines_no_instancing:

*不要实例化实现*
----------------

不要为每个要绑定的接口声明单独的连接性实现。

相反，应将一个全局连接性实现绑定到所有接口，并使用上下文指针存储与各个接口相关的状态。

另请参阅 :ref:`conn_mgr_impl_guidelines_binding_access` 和 :ref:`conn_mgr_impl_guidelines_iface_access`。

.. _conn_mgr_impl_guidelines_binding_access:

*不要在未锁定的情况下访问绑定*
------------------------------

绑定可能会被多个线程随机访问和修改，因此，如果未先 :c:func:`锁定绑定 <conn_mgr_binding_lock>` 就修改或读取绑定，可能会导致不可预测的行为。

这适用于绑定的所有后代，包括 :ref:`上下文容器 <conn_mgr_impl_ctx>` 中的任何内容。

访问完绑定后，请确保 :c:func:`解锁 <conn_mgr_binding_unlock>` 该绑定。

.. note::

   这条规则的一个可能例外是，所涉及的资源本身是线程安全的。

   但是，利用此例外时要小心。仍然可能产生竞态条件，例如同时访问多个线程安全的资源时。

   因此，建议始终锁定绑定，无论所访问的资源本身是否线程安全。

.. _conn_mgr_impl_guidelines_support_builtins:

*不要禁用内置功能*
------------------

不要试图阻止使用内置功能（例如 :ref:`conn_mgr_control_persistence_timeouts` 或 :ref:`conn_mgr_control_automations`）。

所有连接性实现都必须完全支持这些功能。实现不得试图强制某些功能始终启用或始终禁用。

.. _conn_mgr_impl_guidelines_trigger_events:

*触发连接控制事件*
------------------

连接管理器 不会自动触发连接控制 :ref:`网络管理 <net_mgmt_interface>` 事件。

连接性实现必须自行触发这些事件。

发生连接 :ref:`超时 <conn_mgr_control_timeouts>` 时，触发 :c:macro:`NET_EVENT_CONN_CMD_IF_TIMEOUT`。有关详细信息，请参阅 :ref:`conn_mgr_control_events_timeout`。

发生致命（不可恢复）连接错误时，触发 :c:macro:`NET_EVENT_CONN_IF_FATAL_ERROR`。有关详细信息，请参阅 :ref:`conn_mgr_control_events_fatal_error`。

有关触发网络管理事件的详细信息，请参阅 :ref:`net_mgmt_interface`。

.. _conn_mgr_impl_timeout_persistence:

实现超时和持久性
================

首先，请参阅 :ref:`conn_mgr_control_persistence_timeouts`，了解超时和持久性预期行为的高层描述。

连接性实现必须完全符合该描述，无论底层连接技术的行为如何。

有时这意味着需要在连接性实现中编写额外逻辑来模拟某些行为。以下各节讨论各种常见边缘情况和细微差别，以及如何处理它们。

.. _conn_mgr_impl_tp_inherent_persistence:

*本身具有持久性的技术*
----------------------

如果底层技术在连接丢失或失败后自动尝试重新连接或重试连接，则当这些尝试与超时或持久性设置冲突时，连接性实现必须手动取消此类尝试。

例如：

  * 如果底层技术在失去连接后自动尝试重新连接，而该接口的持久性已禁用，则连接性实现应立即取消此重新连接尝试。
  * 如果连接尝试在底层技术没有内置超时的接口上超时，则连接性实现必须通过手动取消连接尝试来模拟超时。

.. _conn_mgr_impl_tp_inherent_nonpersistence:

*放弃连接尝试的技术*
--------------------

如果底层技术没有重试连接尝试的机制，或者在用户配置的超时之前就放弃重试，或者在连接丢失后不会重新连接，则连接性实现必须手动重新请求连接，以抵消这些偏差。

* 如果底层技术不是持久性的，则在启用持久性时必须手动触发重新连接尝试。
* 如果底层技术不支持超时，则在启用超时时必须手动取消连接尝试。
* 如果底层技术强制设置超时，且该超时短于 连接管理器 超时，则必须手动触发新的连接尝试。

.. _conn_mgr_impl_tp_assoc_retry:

*具有关联重试机制的技术*
------------------------

许多底层技术通常不会在一次尝试中就完成关联。

相反，这些底层技术可能需要进行多次连续关联尝试，通常带有短暂延迟。

在这些情况下，连接性实现应将这一系列连续的关联子尝试视为一次统一的连接尝试。

例如，在子尝试失败后，禁用持久性不应阻止进一步子尝试，因为它们都算作一次整体连接尝试。另请参阅 :ref:`conn_mgr_impl_tp_persistence_during_connect`。

一系列失败的子尝试在何种情况下应被视为整个连接尝试的失败，由每个实现自行决定。

如果连接尝试超过此阈值，但配置的超时尚未结束，或者没有超时，则应继续子尝试。

.. _conn_mgr_impl_tp_persistence_during_connect:

*连接尝试期间的持久性*
----------------------

持久性不应影响连接尝试期间实现行为的任何方面。持久性只应影响连接丢失后是否自动触发连接尝试。

配置的超时应完全决定是否应执行连接重试。

.. _conn_mgr_impl_api:

实现 API
========

包含头文件 :file:`include/zephyr/net/conn_mgr_connectivity_impl.h` 以访问这些内容。

仅供连接性实现使用。

.. doxygengroup:: conn_mgr_connectivity_impl
