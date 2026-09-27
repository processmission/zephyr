.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mqtt_socket_interface:

MQTT
####

.. contents::
    :local:
    :depth: 2

概述
****

MQTT（Message Queuing Telemetry Transport）是运行在 TCP/IP 协议栈之上的应用层协议。它是一种用于机器对机器通信的轻量级发布/订阅消息传输协议。有关该协议本身的更多信息，请参见 https://mqtt.org/。

Zephyr 提供了基于 BSD sockets API 构建的 MQTT 客户端库。可以通过 :kconfig:option:`CONFIG_MQTT_LIB` Kconfig 选项启用该库，并且可以按客户端进行配置，支持 MQTT 3.1.0、3.1.1 和 5.0 版本。Zephyr MQTT 实现既可以与通过 TCP 通信的普通 socket 一起使用，也可以与通过 TLS 通信的安全 socket 一起使用。有关 Zephyr socket 的更多信息，请参见 :ref:`bsd_sockets_interface`。

MQTT 客户端需要连接到 MQTT 服务器。这种服务器称为 MQTT Broker，负责管理客户端订阅并分发客户端发布的消息。MQTT Broker 有很多实现，其中之一是 Eclipse Mosquitto。有关 Eclipse Mosquitto 项目的更多信息，请参见 https://mosquitto.org/。

使用示例
********

要创建 MQTT 客户端，需要定义客户端上下文结构和缓冲区：

.. code-block:: c

   /* Buffers for MQTT client. */
   static uint8_t rx_buffer[256];
   static uint8_t tx_buffer[256];

   /* MQTT client context */
   static struct mqtt_client client_ctx;

应用中可以有多个 MQTT 客户端实例，并分别独立管理。此外，还需要一个用于存放 MQTT Broker 地址信息的结构。该结构必须在 MQTT 客户端的整个生命周期内可访问，并且可以在多个 MQTT 客户端之间共享：

.. code-block:: c

   /* MQTT Broker address information. */
   static struct net_sockaddr_storage broker;

MQTT 客户端库会通过为处理相应事件而创建的回调函数向应用通知 MQTT 事件：

.. code-block:: c

   void mqtt_evt_handler(struct mqtt_client *client,
                         const struct mqtt_evt *evt)
   {
      switch (evt->type) {
         /* Handle events here. */
      }
   }

有关可能事件的列表，请参见 :ref:`mqtt_api_reference`。

客户端上下文结构在使用前需要初始化并设置完成。下面是 TCP 传输的示例配置：

.. code-block:: c

   mqtt_client_init(&client_ctx);

   /* MQTT client configuration */
   client_ctx.broker = &broker;
   client_ctx.evt_cb = mqtt_evt_handler;
   client_ctx.client_id.utf8 = (uint8_t *)"zephyr_mqtt_client";
   client_ctx.client_id.size = sizeof("zephyr_mqtt_client") - 1;
   client_ctx.password = NULL;
   client_ctx.user_name = NULL;
   client_ctx.protocol_version = MQTT_VERSION_3_1_1;
   client_ctx.transport.type = MQTT_TRANSPORT_NON_SECURE;

   /* MQTT buffers configuration */
   client_ctx.rx_buf = rx_buffer;
   client_ctx.rx_buf_size = sizeof(rx_buffer);
   client_ctx.tx_buf = tx_buffer;
   client_ctx.tx_buf_size = sizeof(tx_buffer);

配置设置完成后，MQTT 客户端可以连接到 MQTT Broker。调用 ``mqtt_connect`` 函数，该函数将创建适当的 socket、建立 TCP/TLS 连接并发送 ``MQTT CONNECT`` 消息。收到通知后，应用应调用 ``mqtt_input`` 函数处理收到的响应。请注意，``mqtt_input`` 是非阻塞函数，因此应用应使用 socket ``poll`` 等待响应。如果连接成功，将通过回调函数向应用通知 ``MQTT_EVT_CONNACK``。

.. code-block:: c

   rc = mqtt_connect(&client_ctx);
   if (rc != 0) {
      return rc;
   }

   fds[0].fd = client_ctx.transport.tcp.sock;
   fds[0].events = ZSOCK_POLLIN;
   poll(fds, 1, 5000);

   mqtt_input(&client_ctx);

   if (!connected) {
      mqtt_abort(&client_ctx);
   }

在上面的代码片段中，MQTT 回调函数应在连接成功时设置 ``connected`` 标志。如果 MQTT 层连接失败或发生超时，连接将被中止，底层 socket 也会关闭。

连接建立后，应用需要定期调用 ``mqtt_input`` 和 ``mqtt_live`` 函数来处理传入数据并维持连接。如果收到 MQTT 消息，将调用 MQTT 回调函数并通知相应事件。

可以调用 ``mqtt_disconnect`` 函数来关闭连接。

Zephyr 提供了使用 MQTT 客户端 API 的示例代码。更多信息请参见 :zephyr:code-sample:`mqtt-publisher`。

将 MQTT 与 TLS 配合使用
***********************

通过选择安全传输类型（``MQTT_TRANSPORT_SECURE``）并提供一些额外的配置信息，可以将 Zephyr MQTT 库与 TLS 传输配合使用，以实现安全通信：

.. code-block:: c

   client_ctx.transport.type = MQTT_TRANSPORT_SECURE;

   struct mqtt_sec_config *tls_config = &client_ctx.transport.tls.config;

   tls_config->peer_verify = TLS_PEER_VERIFY_REQUIRED;
   tls_config->cipher_list = NULL;
   tls_config->sec_tag_list = m_sec_tags;
   tls_config->sec_tag_count = ARRAY_SIZE(m_sec_tags);
   tls_config->hostname = MQTT_BROKER_HOSTNAME;
   tls_config->set_native_tls = true;

在此示例代码中，``m_sec_tags`` 数组保存一组标签，这些标签引用 MQTT 库应用于身份验证的 TLS 凭据。我们没有指定 ``cipher_list``，以便使用系统中所有可用的密码套件。我们将 ``hostname`` 字段设置为 Broker 主机名，这是服务器身份验证所必需的。最后，我们通过设置 ``peer_verify`` 字段强制进行对端证书验证。

请注意，``m_sec_tags`` 数组引用的 TLS 凭据必须先在系统中注册。有关如何注册的更多信息，请参见 :ref:`安全 socket 文档 <secure_sockets_interface>`。

最后，可以选择设置 ``set_native_tls`` 以启用原生 TLS 支持，而不是将 TLS 操作卸载到卸载 socket。

关于如何将 TLS 与 MQTT 配合使用的示例也包含在 :zephyr:code-sample:`mqtt-publisher` 示例应用中。

.. _mqtt_api_reference:

API 参考
********

.. doxygengroup:: mqtt_socket
