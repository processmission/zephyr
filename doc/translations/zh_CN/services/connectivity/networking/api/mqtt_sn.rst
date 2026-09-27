.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mqtt_sn_socket_interface:

MQTT-SN
#######

.. contents::
    :local:
    :depth: 2

概述
****

MQTT-SN 是众所周知的 MQTT 协议的一种变体，请参见 :ref:`mqtt_socket_interface`。

与 MQTT 不同，MQTT-SN 不要求使用 TCP 传输，而是设计为可在任何基于消息的传输方式上使用。它最初主要针对 ZigBee 设计，但也可以同样使用蓝牙、UDP 甚至 UART 等其它传输方式。

Zephyr 提供了基于 BSD sockets API 构建的 MQTT-SN 客户端库。可以通过 :kconfig:option:`CONFIG_MQTT_SN_LIB` Kconfig 选项启用该库，并可针对每个客户端进行配置，支持 MQTT-SN 1.2 版本。Zephyr MQTT-SN 实现可用于任何基于消息的传输，但已内置对 UDP 的支持。

MQTT-SN 客户端需要连接到 MQTT-SN 网关。这些网关在 MQTT-SN 和 MQTT 之间进行转换。Eclipse Paho 项目提供了 MQTT-SN 网关的一种实现，也有其它实现可用。https://www.eclipse.org/paho/index.php?page=components/mqtt-sn-transparent-gateway/index.php

MQTT-SN v1.2 规范可在此处找到：https://www.oasis-open.org/committees/download.php/66091/MQTT-SN_spec_v1.2.pdf

使用示例
********

要创建 MQTT-SN 客户端，需要定义客户端上下文结构和缓冲区：

.. code-block:: c

   /* Buffers for MQTT client. */
   static uint8_t rx_buffer[256];
   static uint8_t tx_buffer[256];

   /* MQTT-SN client context */
   static struct mqtt_sn_client client;

应用中可以有多个 MQTT-SN 客户端实例，并分别独立管理。此外，还需要一个用于传输的结构。该库已经附带了一个 UDP 的示例实现。

.. code-block:: c

   /* MQTT Broker address information. */
   static struct mqtt_sn_transport tp;

MQTT-SN 库将使用回调向客户端通知某些事件。

.. code-block:: c

   static void evt_cb(struct mqtt_sn_client *client,
                      const struct mqtt_sn_evt *evt)
   {
      switch(evt->type) {
      {
         /* Handle events here. */
      }
   }

有关可能事件的列表，请参见 :ref:`mqtt_sn_api_reference`。

客户端上下文结构在使用前需要初始化并设置完成。下面是 UDP 传输的示例配置：

.. code-block:: c

   struct mqtt_sn_data client_id = MQTT_SN_DATA_STRING_LITERAL("ZEPHYR");
   struct net_sockaddr_in gateway = {0};

   uint8_t tx_buf[256];
   uint8_t rx_buf[256];

   mqtt_sn_transport_udp_init(&tp, (struct net_sockaddr*)&gateway, sizeof((gateway)));

   mqtt_sn_client_init(&client, &client_id, &tp.tp, evt_cb, tx_buf, sizeof(tx_buf), rx_buf, sizeof(rx_buf));

配置设置完成后，必须定义要连接的网关的网络地址。MQTT-SN 协议提供了通过通告或搜索机制发现网关的功能。用户至少应执行以下步骤之一来为该库定义网关：

* 调用 :c:func:`mqtt_sn_add_gw` 函数手动定义网关地址。
* 等待 :c:enumerator:`MQTT_SN_EVT_ADVERTISE`。
* 调用 :c:func:`mqtt_sn_search` 函数并等待 :c:enumerator:`MQTT_SN_EVT_GWINFO` 回调。请确保定期调用 :c:func:`mqtt_sn_input` 函数以处理传入消息。

示例 :c:func:`mqtt_sn_search` 函数调用：

.. code-block:: c

        err = mqtt_sn_search(&mqtt_client, 1);
        k_sleep(K_SECONDS(10));
        err = mqtt_sn_input(&mqtt_client);
        __ASSERT(err == 0, "mqtt_sn_search() failed %d", err);

定义或找到网关地址后，MQTT-SN 客户端可以连接到该网关。调用 :c:func:`mqtt_sn_connect` 函数，它将发送 ``CONNECT`` MQTT-SN 消息。应用应定期调用 :c:func:`mqtt_sn_input` 函数以处理收到的响应。如果应用知道没有收到数据（例如使用蓝牙时），则不必调用 :c:func:`mqtt_sn_input`。请注意，如果传输结构包含与 :c:func:`poll` 兼容的函数指针，则 :c:func:`mqtt_sn_input` 是非阻塞函数。如果连接成功，将通过回调函数向应用通知 :c:enumerator:`MQTT_SN_EVT_CONNECTED`。

.. code-block:: c

        err = mqtt_sn_connect(&client, false, true);
        __ASSERT(err == 0, "mqtt_sn_connect() failed %d", err);

        while (1) {
                mqtt_sn_input(&client);
                if (connected) {
                        mqtt_sn_publish(&client, MQTT_SN_QOS_0, &topic_p, false, &pubdata);
                }
                k_sleep(K_MSEC(500));
        }

在上面的代码片段中，应先连接网关，然后再发布消息。如果 MQTT 层连接失败或发生超时，连接将被中止并返回错误。

连接建立后，应用需要定期调用 :c:func:`mqtt_input` 函数以处理传入数据。另一方面，连接维护通过 k_work 工作项自动完成。如果收到 MQTT 消息，将调用 MQTT 回调函数并通知相应事件。

可以调用 :c:func:`mqtt_sn_disconnect` 函数关闭连接。但这不会影响传输。如果要关闭传输（例如 socket），请调用 :c:func:`mqtt_sn_client_deinit`，它也会反初始化传输。

Zephyr 提供了使用 MQTT-SN 客户端 API 的示例代码。更多信息请参见 :zephyr:code-sample:`mqtt-sn-publisher`。

与标准的差异
************

该库尚未支持协议中的某些部分。

* 转发器封装

.. _mqtt_sn_api_reference:

API 参考
********

.. doxygengroup:: mqtt_sn_socket
