.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bsd_sockets_interface:

BSD Sockets
###########

.. contents::
    :local:
    :depth: 2

概述
****

Zephyr 提供了 BSD Sockets API（POSIX 标准的一部分）的一个子集实现。该 API 允许复用现有的编程经验，并将现有简单的网络应用移植到 Zephyr。

以下是指导 Zephyr 的 BSD Sockets 兼容 API 实现的关键要求和概念：

* 开销最小，与其他 Zephyr 子系统的要求类似。
* 默认采用命名空间，以避免与 libc 或其他 POSIX 兼容库中可能存在的 ``close()`` 等知名名称冲突。如果通过 :kconfig:option:`CONFIG_POSIX_API` 启用，它还会暴露 POSIX 兼容 API。

BSD Sockets 兼容 API 通过 :kconfig:option:`CONFIG_NET_SOCKETS` 配置选项启用，并实现以下操作： ``socket()``、``close()``、``recv()``、``recvfrom()``、``send()``、``sendto()``、``connect()``、``bind()``、``listen()``、``accept()``、``fcntl()`` （用于设置非阻塞模式）、``getsockopt()``、``setsockopt()``、``poll()``、``select()``、``getaddrinfo()``、``getnameinfo()``。

基于上述命名空间要求，这些操作默认以带 ``zsock_`` 前缀的函数形式暴露，例如 :c:func:`zsock_socket` 和 :c:func:`zsock_close`。如果定义了配置选项 :kconfig:option:`CONFIG_POSIX_API`，所有函数还会以不带前缀的别名形式暴露。这包括 ``close()`` 和 ``fcntl()`` 之类的函数（它们可能与 libc 或其他库中的函数冲突，例如与文件系统库冲突）。

上述设计要求的另一个推论是，Zephyr API 会尽可能积极地利用 POSIX API 的短读/短写特性（以降低复杂度和开销）。POSIX 允许 ``recv()`` 和 ``send()`` 之类的调用实际处理（接收或发送）的数据少于用户请求的数据量（在 ``SOCK_STREAM`` 类型的 socket 上）。例如，调用 ``recv(sock, 1000, 0)`` 可能返回 100，表示只读取了 100 字节（短读），应用需要重试调用以接收剩余的 900 字节。

BSD Sockets API 使用文件描述符表示 socket。文件描述符是小整数，从零开始连续分配，在 socket、文件、特殊设备（如 stdin/stdout）等之间共享。在内部，有一个将文件描述符映射到内部对象指针的表。即使 POSIX 子系统的其余部分（文件系统、stdin/stdout）未启用，BSD Sockets API 也会使用该文件描述符表。

Zephyr 支持多种类型的 BSD socket，下表总结了可用的 socket 类型：

+-----------------------+---------------+-------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 地址族                | 类型          | 协议                    | 描述                                                                                                                                                                                         |
+=======================+===============+=========================+==============================================================================================================================================================================================+
| AF_INET |br| AF_INET6 | SOCK_DGRAM    | IPPROTO_UDP             | 如果设置了 :kconfig:option:`CONFIG_NET_UDP`，则启用。 |br| 允许发送和接收 UDP 数据报。                                                                                                       |
|                       |               +-------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                       |               | IPPROTO_DTLS_1_x        | 如果设置了 :kconfig:option:`CONFIG_NET_SOCKETS_ENABLE_DTLS`，则启用。 |br| 允许发送和接收 DTLS 数据报。                                                                                      |
|                       +---------------+-------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                       | SOCK_STREAM   | IPPROTO_TCP             | 如果设置了 :kconfig:option:`CONFIG_NET_TCP`，则启用。 |br| 允许发送和接收 TCP 数据流。                                                                                                       |
|                       |               +-------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                       |               | IPPROTO_TLS_1_x         | 如果设置了 :kconfig:option:`CONFIG_NET_SOCKETS_SOCKOPT_TLS`，则启用。 |br| 允许发送和接收 TLS 数据流。                                                                                       |
|                       +---------------+-------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                       | SOCK_RAW      | IPPROTO_IP |br| <proto> | 如果设置了 :kconfig:option:`CONFIG_NET_SOCKETS_INET_RAW`，则启用。 |br| 允许发送和接收 IPv4/IPv6 数据报。 |br| 数据包按指定的 L4 协议过滤。IPPROTO_IP 是用于接收所有 IP 数据报的通配协议。   |
+-----------------------+---------------+-------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| AF_PACKET             | SOCK_DGRAM    | ETH_P_ALL |br| <proto>  | 如果设置了 :kconfig:option:`CONFIG_NET_SOCKETS_PACKET_DGRAM`，则启用。 |br| 允许发送和接收不带 L2 报头的数据包。 |br| 数据包按指定的 L3 协议过滤。ETH_P_ALL 是用于接收所有数据包的通配协议。 |
|                       +---------------+-------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                       | SOCK_RAW      | ETH_P_ALL               | 如果设置了 :kconfig:option:`CONFIG_NET_SOCKETS_PACKET`，则启用。 |br| 允许发送和接收包含 L2 报头的数据包。                                                                                   |
+-----------------------+---------------+-------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| AF_CAN                | SOCK_RAW      | CAN_RAW                 | 如果设置了 :kconfig:option:`CONFIG_NET_SOCKETS_CAN`，则启用。 |br| 允许发送和接收 CAN 数据包。                                                                                               |
+-----------------------+---------------+-------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

请参阅 :zephyr:code-sample:`sockets-echo-server` 和 :zephyr:code-sample:`sockets-echo-client` 示例应用，了解如何创建基于 BSD socket 的简单服务器或客户端应用。

.. _ip_socket_options:

IPv4 和 IPv6 socket 选项
************************

Zephyr 通过 :c:func:`zsock_setsockopt` 和 :c:func:`zsock_getsockopt`，在 ``NET_IPPROTO_IP`` 协议级别（IPv4）和 ``NET_IPPROTO_IPV6`` 协议级别（IPv6）支持 IP 级 socket 选项。选项的可用性可能取决于 Kconfig 设置和 socket 地址族。

IPv4 选项
=========

.. doxygengroup:: ipv4_socket_options

IPv6 选项
=========

.. doxygengroup:: ipv6_socket_options

QUIC 协议栈在 DPLPMTUD 探测期间会在内部使用 :c:macro:`ZSOCK_IP_DONTFRAG` 和 :c:macro:`ZSOCK_IPV6_DONTFRAG` 选项（参见 :ref:`quic_dplpmtud`）。

.. _secure_sockets_interface:

安全 socket
***********

Zephyr 提供了标准 POSIX socket API 的扩展，允许创建和配置使用 TLS 协议类型的 socket，从而实现安全通信。实现所需的安全函数由 Mbed TLS 库提供。安全 socket 实现允许通过标准 socket 调用使用 TLS 和 DTLS 两种协议。有关支持的安全协议版本，请参见 :c:enum:`net_ip_protocol_secure` 类型。

要启用安全 socket，请设置 :kconfig:option:`CONFIG_NET_SOCKETS_SOCKOPT_TLS` 选项。要启用 DTLS 支持，请使用 :kconfig:option:`CONFIG_NET_SOCKETS_ENABLE_DTLS` 选项。

.. _sockets_tls_credentials_subsys:

TLS 凭据子系统
==============

TLS 凭据必须先注册到系统中，然后才能用于安全 socket。更多信息请参见 :c:func:`tls_credential_add`。

当特定 TLS 凭据注册到系统时，会为其分配一个 :c:type:`sec_tag_t` 类型的数值，称为标签。之后在通过 socket 选项配置安全 socket 时，可以使用该值来引用此凭据。

可以在系统中注册以下 TLS 凭据类型：

- ``TLS_CREDENTIAL_CA_CERTIFICATE``
- ``TLS_CREDENTIAL_PUBLIC_CERTIFICATE``
- ``TLS_CREDENTIAL_PRIVATE_KEY``
- ``TLS_CREDENTIAL_PSK``
- ``TLS_CREDENTIAL_PSK_ID``

CA 证书的注册示例（在 ``ca_certificate`` 数组中提供）如下所示：

.. code-block:: c

   ret = tls_credential_add(CA_CERTIFICATE_TAG, TLS_CREDENTIAL_CA_CERTIFICATE,
                            ca_certificate, sizeof(ca_certificate));

默认支持 DER 格式的证书。可以在 Mbed TLS 设置中启用 PEM 支持。

安全 socket 的创建
==================

可以通过指定安全协议类型来创建安全 socket，例如：

.. code-block:: c

   sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TLS_1_2);

创建安全 socket 时指定的协议版本表示该 TLS 会话使用的最低 TLS 版本。

创建后，可以使用 socket 选项对其进行配置。例如，可以设置 CA 证书和主机名：

.. code-block:: c

   sec_tag_t sec_tag_opt[] = {
           CA_CERTIFICATE_TAG,
   };

   ret = setsockopt(sock, SOL_TLS, TLS_SEC_TAG_LIST,
                    sec_tag_opt, sizeof(sec_tag_opt));

.. code-block:: c

   char host[] = "google.com";

   ret = setsockopt(sock, SOL_TLS, TLS_HOSTNAME, host, sizeof(host));

配置完成后，该 socket 就可以像普通 TCP socket 一样使用。

.. note::

   由于 mbed TLS 内部数据缓冲以及 ``mbedtls_ssl_write()`` 函数的要求，当非阻塞的 :c:func:`zsock_send` 返回 ``EAGAIN`` 时，后续对 :c:func:`zsock_send` 的调用应包含与原始调用相同的数据。

Zephyr 中有多个示例使用安全 socket 进行通信。示例用法请参见 :zephyr:code-sample:`echo-server 示例应用 <sockets-echo-server>` 或 :zephyr:code-sample:`HTTP GET 示例应用 <sockets-http-get>`。

安全 socket 选项
================

安全 socket 提供以下用于 socket 管理的选项：

.. doxygengroup:: secure_sockets_options

socket 卸载
***********

Zephyr 允许注册自定义 socket 实现（称为卸载 socket）。这样可以将提供外部 IP 协议栈并暴露类 socket API 的设备无缝集成进来。

socket 卸载可以通过 :kconfig:option:`CONFIG_NET_SOCKETS_OFFLOAD` 选项启用。想要注册新 socket 实现的网络驱动应使用 :c:macro:`NET_SOCKET_OFFLOAD_REGISTER` 宏。该宏接受以下参数：

 * ``socket_name``
     socket 实现的任意名称。

 * ``prio``
     socket 实现的优先级。优先级越高，创建新 socket 时该实现被处理的顺序越靠前。数值越小表示优先级越高。

 * ``_family``
     卸载 socket 所实现的 socket 地址族。``AF_UNSPEC`` 表示任意地址族。

 * ``_is_supported``
     过滤函数，用于验证卸载 socket 实现是否支持特定的 socket 地址族、类型和协议。

 * ``_handler``
     与 :c:func:`socket` API 兼容的函数，用于创建卸载 socket。

每个卸载 socket 实现还应实现一组 socket API，这些 API 在 :c:struct:`socket_op_vtable` 结构体中指定。

为创建 socket 而注册的函数应使用 :c:func:`zvfs_reserve_fd` 函数分配新的文件描述符。特定于某个卸载 socket 实现创建过程的任何附加操作，都应在分配文件描述符之后执行。最后，如果卸载 socket 创建成功，应使用 :c:func:`zvfs_finalize_typed_fd` 或 :c:func:`zvfs_finalize_fd` 函数完成文件描述符的最终化处理。finalize 函数允许为卸载 socket 注册一个实现 socket API 的 :c:struct:`socket_op_vtable` 结构体，并可附加一个可选的 socket 上下文数据指针。

最后，当卸载网络接口初始化时，应使用 :c:func:`net_if_socket_offload_set` 函数指明该接口已卸载。该函数会在网络接口上注册用于创建卸载 socket 的函数（与 :c:macro:`NET_SOCKET_OFFLOAD_REGISTER` 中提供的函数相同）。

卸载 socket 的创建
==================

当应用使用 :c:func:`socket` 函数创建新 socket 时，网络协议栈会遍历所有已注册的 socket 实现（原生和卸载）。优先级较高的 socket 实现会先被处理。对于每个已注册的 socket 实现，会验证地址族，如果匹配（或者该 socket 注册为 ``AF_UNSPEC``），则调用相应的 ``_is_supported`` 函数来验证其余 socket 参数。第一个满足 socket 要求的实现（即 ``_is_supported`` 返回 true）将使用其 ``_handler`` 函数创建新 socket。

以上说明了 socket 优先级的重要性。如果多个 socket 实现支持相同的 socket 地址族/类型/协议组合，系统处理的第一个实现将创建 socket。因此，为应作为系统默认的实现赋予最高优先级非常重要。

原生 socket 实现的 socket 优先级通过 Kconfig 配置。使用 :kconfig:option:`CONFIG_NET_SOCKETS_TLS_PRIORITY` 设置原生 TLS socket 的优先级。使用 :kconfig:option:`CONFIG_NET_SOCKETS_PRIORITY_DEFAULT` 设置其余原生 socket 的优先级。

处理多个卸载接口
================

由于 :c:func:`socket` 函数不允许指定 socket 应使用哪个网络接口，因此当存在多个支持相同 socket 类型的卸载 socket 实现时，无法选择特定的实现。当系统中同时存在原生和卸载 socket 时，也会出现同样的问题。

为了解决此问题，引入了一种特殊的 socket 实现（称为 socket 调度器）。该模块的唯一目的是将 socket 的创建推迟到对 socket 执行第一个操作时。这样就留出了使用 ``SO_BINDTODEVICE`` socket 选项将 socket 绑定到特定网络接口（从而绑定到卸载 socket 实现）的机会。可以通过 :kconfig:option:`CONFIG_NET_SOCKETS_OFFLOAD_DISPATCHER` Kconfig 选项启用 socket 调度器。

启用后，应用可以使用 :c:func:`setsockopt` 函数指定要使用的网络接口：

.. code-block:: c

   /* A "dispatcher" socket is created */
   sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

   struct ifreq ifreq = {
      .ifr_name = "SimpleLink"
   };

   /* The socket is "dispatched" to a particular network interface
    * (offloaded or not).
    */
   setsockopt(sock, SOL_SOCKET, SO_BINDTODEVICE, &ifreq, sizeof(ifreq));

类似地，如果原生和卸载 socket 都支持 TLS，可以使用 ``TLS_NATIVE`` socket 选项来指示应创建原生 TLS socket。随后，可以将底层 socket 绑定到特定的网络接口：

.. code-block:: c

   /* A "dispatcher" socket is created */
   sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TLS_1_2);

   int tls_native = 1;

   /* The socket is "dispatched" to a native TLS socket implmeentation.
    * The underlying socket is a "dispatcher" socket now.
    */
   setsockopt(sock, SOL_TLS, TLS_NATIVE, &tls_native, sizeof(tls_native));

   struct ifreq ifreq = {
      .ifr_name = "SimpleLink"
   };

   /* The underlying socket is "dispatched" to a particular network interface
    * (offloaded or not).
    */
   setsockopt(sock, SOL_SOCKET, SO_BINDTODEVICE, &ifreq, sizeof(ifreq));

如果未对 socket 使用 ``SO_BINDTODEVICE`` socket 选项，则在首次调用 socket API 时，将根据默认优先级和过滤规则分派该 socket。

API 参考
********

BSD Sockets
===========

.. doxygengroup:: bsd_sockets

TLS 凭据
========

.. doxygengroup:: tls_credentials
