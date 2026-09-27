.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _socket_service_interface:

socket 服务
###########

.. contents::
    :local:
    :depth: 2

概述
****

socket 服务 API 可用于安装一个处理函数，当 socket 上收到数据时会调用该函数。该 API 有助于避免为应用提供的每个 TCP 或 UDP 服务创建专用线程。相反，系统会创建一个线程，为多个监听 socket 提供数据服务；这样可节省内存，因为在这种情况下系统中只需创建一个线程。

请参阅 :zephyr:code-sample:`sockets-service-echo` 示例应用，了解如何使用 socket 服务 API 创建基于 BSD socket 的简单服务器应用。该示例应用的源代码位于 :zephyr_file:`samples/net/sockets/echo_service`。

API 说明
********

socket 服务 API 通过 :kconfig:option:`CONFIG_NET_SOCKETS_SERVICE` 配置选项启用，并实现以下操作：

* :c:macro:`NET_SOCKET_SERVICE_SYNC_DEFINE`

  定义一个网络 socket 服务。该 socket 服务以 extern 作用域创建，因此可以在多个 C 源文件中使用。

* :c:macro:`NET_SOCKET_SERVICE_SYNC_DEFINE_STATIC`

  定义一个具有 static 作用域的网络 socket 服务。该 socket 服务只能在一个 C 源文件中使用。

* :c:func:`net_socket_service_register`

  为此服务注册可轮询的 socket。用户必须在此调用之前创建这些 socket。

* :c:func:`net_socket_service_unregister`

  移除此服务的可轮询 socket。用户可以在该调用之后关闭这些 socket。

* :c:type:`net_socket_service_handler_t`

  用户指定的回调函数，当监听 socket 上收到数据时会调用该回调。

应用概述
********

如果启用了 socket 服务 API，应用必须按如下方式创建服务：

.. code-block:: c

   #define MAX_BUF_LEN 1500
   #define MAX_SERVICES 1

   static void udp_service_handler(struct net_socket_service_event *pev)
   {
        struct pollfd *pfd = &pev->event;
        int client = pfd->fd;
        struct sockaddr_in6 addr;
        socklen_t addrlen = sizeof(addr);

        /* In this example we use one static buffer in order to avoid
         * having a large stack.
         */
        static char buf[MAX_BUF_LEN];

        len = recvfrom(client, buf, sizeof(buf), 0,
                       (struct sockaddr *)&addr, &addrlen);
        if (len <= 0) {
                /* Error */
                ...
                return;
        }

        /* Do something with the received data. The pev variable contains
         * user data that was stored in the socket service when it was
         * registered.
         */
   }

   NET_SOCKET_SERVICE_SYNC_DEFINE_STATIC(service_udp, udp_service_handler, MAX_SERVICES);

应用需要先创建 socket，然后将它们注册到 socket 服务；此后 socket 服务线程将开始为任何传入数据调用回调函数。

.. code-block:: c

   /* Create one or multiple sockets */

   struct pollfd sockfd_udp[1] = { 0 };
   int sock, ret;

   sock = socket(AF_INET6, SOCK_DGRAM, IPPROTO_UDP);
   if (sock < 0) {
        LOG_ERR("socket: %d", -errno);
        return -errno;
   }

   /* Set possible socket options after creation */
   ...

   /* Then bind the socket to local address */
   if (bind(sock, (struct sockaddr *)addr, sizeof(*addr)) < 0) {
        LOG_ERR("bind: %d", -errno);
        return -errno;
   }

   /* Set the polled sockets */
   sockfd_udp[0].fd = sock;
   sockfd_udp[0].events = POLLIN;

   /* Register UDP socket to service handler */
   ret = net_socket_service_register(&service_udp, sockfd_udp,
                                     ARRAY_SIZE(sockfd_udp), NULL);
   if (ret < 0) {
        LOG_ERR("Cannot register socket service handler (%d)", ret);
        return ret;
   }

   /* Application logic happens here. When application is ready to
    * quit, one should unregister the socket service and close the
    * socket.
    */

   (void)net_socket_service_unregister(&service_udp);
   close(sock);

TCP socket 需要略微不同的逻辑，因为需要通过为已接受的 socket 调用 :c:func:`net_socket_service_register`，将任何已接受的 socket 添加到监听 socket 中。

.. code-block:: c

   struct sockaddr_in6 client_addr;
   socklen_t client_addr_len = sizeof(client_addr);
   struct pollfd sockfd_tcp[1] = { 0 };
   int client;

   /* TCP socket service is created similar way as the UDP one */
   sock = socket(AF_INET6, SOCK_STREAM, IPPROTO_TCP);
   if (sock < 0) {
        LOG_ERR("socket: %d", -errno);
        return -errno;
   }

   if (bind(sock, (struct sockaddr *)addr, sizeof(*addr)) < 0) {
        LOG_ERR("bind: %d", -errno);
        return -errno;
   }

   if (listen(sock, 5) < 0) {
        LOG_ERR("listen: %d", -errno);
        return -errno;
   }

   while (1) {
        client = accept(tcp_sock, (struct sockaddr *)&client_addr,
                        &client_addr_len);
        if (client < 0) {
                LOG_ERR("accept: %d", -errno);
                continue;
        }

        inet_ntop(client_addr.sin6_family, &client_addr.sin6_addr,
                  addr_str, sizeof(addr_str));
        LOG_INF("Connection from %s (%d)", addr_str, client);

        sockfd_tcp[0].fd = client;
        sockfd_tcp[0].events = POLLIN;

        /* Register all the sockets to service handler */
        ret = net_socket_service_register(&service_tcp, sockfd_tcp,
                                          ARRAY_SIZE(sockfd_tcp), NULL);
        if (ret < 0) {
                LOG_ERR("Cannot register socket service handler (%d)", ret);
                break;
        }
   }

对于任何已关闭的 TCP 客户端连接，我们需要从轮询 socket 列表中移除已关闭的 socket。

.. code-block:: c

   /* If the TCP socket is closed while reading the data in the handler,
    * mark it as non pollable.
    */
   if (sockfd_tcp[0].fd == client) {
        sockfd_tcp[0].fd = -1;

        /* Update the handler so that client connection is
         * not monitored any more.
         */
         (void)net_socket_service_register(&service_tcp, sockfd_tcp,
                                           ARRAY_SIZE(sockfd_tcp), NULL);
         close(client);

         LOG_INF("Connection from %s closed", addr_str);
   }

更完整的示例请参见 ``echo_service`` 示例源代码 :zephyr_file:`samples/net/sockets/echo_service/src/main.c`。

API 参考
********

.. doxygengroup:: bsd_socket_service
