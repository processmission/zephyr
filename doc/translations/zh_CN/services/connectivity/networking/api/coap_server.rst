.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _coap_server_interface:

CoAP 服务器
###########

.. contents::
    :local:
    :depth: 2

概述
****

Zephyr 自带一个开箱即用的 CoAP 服务器，它使用服务来监听 CoAP 请求。CoAP 服务通过 socket 处理通信，并将请求传递给已注册的 CoAP 资源。

设置
****

需要一些配置，以确保可以使用 CoAP 服务器启动服务。应在项目中启用 :kconfig:option:`CONFIG_COAP_SERVER` 选项：

.. code-block:: cfg
    :caption: ``prj.conf``

    CONFIG_COAP_SERVER=y

所有服务都会添加到预定义的链接器节中，每个服务的所有资源也会获得各自的链接器节。如果有一个名为 ``my_service`` 的服务，其名称必须添加 ``coap_resource_`` 前缀，并添加到链接器文件中：

.. code-block:: c
    :caption: ``sections-ram.ld``

    #include <zephyr/linker/iterable_sections.h>

    ITERABLE_SECTION_RAM(coap_resource_my_service, Z_LINK_ITERABLE_SUBALIGN)

使用 CMake 将此链接器文件添加到应用中：

.. code-block:: cmake
    :caption: ``CMakeLists.txt``

    # Support LD linker template
    zephyr_linker_sources(DATA_SECTIONS sections-ram.ld)

    # Support CMake linker generator
    zephyr_iterable_section(NAME coap_resource_my_service
                            GROUP DATA_REGION ${XIP_ALIGN_WITH_INPUT})

现在，可以将服务定义为应用的一部分：

.. code-block:: c

    #include <zephyr/net/coap_service.h>

    static const uint16_t my_service_port = 5683;

    COAP_SERVICE_DEFINE(my_service, "0.0.0.0", &my_service_port, COAP_SERVICE_AUTOSTART);

.. note::

    使用 ``COAP_SERVICE_AUTOSTART`` 标志定义的服务将随 CoAP 服务器线程一起启动。可以分别使用 ``coap_service_start`` 和 ``coap_service_stop`` 手动启动和停止服务。

用法示例
********

以下示例展示了向我们的服务注册 CoAP 资源的方式：

.. code-block:: c

    #include <zephyr/net/coap_service.h>

    static int my_get(struct coap_resource *resource, struct coap_packet *request,
                      struct net_sockaddr *addr, socklen_t addr_len)
    {
        static const char *msg = "Hello, world!";
        uint8_t data[CONFIG_COAP_SERVER_MESSAGE_SIZE];
        struct coap_packet response;
        uint16_t id;
        uint8_t token[COAP_TOKEN_MAX_LEN];
        uint8_t tkl, type;

        type = coap_header_get_type(request);
        id = coap_header_get_id(request);
        tkl = coap_header_get_token(request, token);

        /* Determine response type */
        type = (type == COAP_TYPE_CON) ? COAP_TYPE_ACK : COAP_TYPE_NON_CON;

        coap_packet_init(&response, data, sizeof(data), COAP_VERSION_1, type, tkl, token,
                         COAP_RESPONSE_CODE_CONTENT, id);

        /* Set content format */
        coap_append_option_int(&response, COAP_OPTION_CONTENT_FORMAT,
                               COAP_CONTENT_FORMAT_TEXT_PLAIN);

        /* Append payload */
        coap_packet_append_payload_marker(&response);
        coap_packet_append_payload(&response, (uint8_t *)msg, strlen(msg));

        /* Send to response back to the client */
        return coap_resource_send(resource, &response, addr, addr_len, NULL);
    }

    static int my_put(struct coap_resource *resource, struct coap_packet *request,
                      struct net_sockaddr *addr, socklen_t addr_len)
    {
        /* ... Handle the incoming request ... */

        /* Return a CoAP response code as a shortcut for an empty ACK message */
        return COAP_RESPONSE_CODE_CHANGED;
    }

    static const char * const my_resource_path[] = { "test", NULL };
    COAP_RESOURCE_DEFINE(my_resource, my_service, {
        .path = my_resource_path,
        .get = my_get,
        .put = my_put,
    });

.. note::

    如上面的示例所示，CoAP 资源处理函数可以返回响应代码，让服务器以空 ACK 响应进行响应。

可观察资源
**********

CoAP 服务器提供了解析观察请求的逻辑，并使用 CoAP 服务的运行时数据存储这些请求。使用温度传感器的示例可能如下所示：

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zephyr/drivers/sensor.h>
    #include <zephyr/net/coap_service.h>

    static void notify_observers(struct k_work *work);
    K_WORK_DELAYABLE_DEFINE(temp_work, notify_observers);

    static int send_temperature(struct coap_resource *resource,
                                const struct net_sockaddr *addr, socklen_t addr_len,
                                uint16_t age, uint16_t id, const uint8_t *token, uint8_t tkl,
                                bool is_response)
    {
        const struct device *dev = DEVICE_DT_GET(DT_ALIAS(ambient_temp0));
        uint8_t data[CONFIG_COAP_SERVER_MESSAGE_SIZE];
        struct coap_packet response;
        char payload[14];
        struct sensor_value value;
        double temp;
        uint8_t type;

        /* Determine response type */
        type = is_response ? COAP_TYPE_ACK : COAP_TYPE_CON;

        if (!is_response) {
            id = coap_next_id();
        }

        coap_packet_init(&response, data, sizeof(data), COAP_VERSION_1, type, tkl, token,
                         COAP_RESPONSE_CODE_CONTENT, id);

        if (age >= 2U) {
            coap_append_option_int(&response, COAP_OPTION_OBSERVE, age);
        }

        /* Set content format */
        coap_append_option_int(&response, COAP_OPTION_CONTENT_FORMAT,
                               COAP_CONTENT_FORMAT_TEXT_PLAIN);

        /* Get the sensor data */
        sensor_sample_fetch_chan(dev, SENSOR_CHAN_AMBIENT_TEMP);
        sensor_channel_get(dev, SENSOR_CHAN_AMBIENT_TEMP, &value);
        temp = sensor_value_to_double(&value);

        snprintk(payload, sizeof(payload), "%0.2f°C", temp);

        /* Append payload */
        coap_packet_append_payload_marker(&response);
        coap_packet_append_payload(&response, (uint8_t *)payload, strlen(payload));

        return coap_resource_send(resource, &response, addr, addr_len, NULL);
    }

    static int temp_get(struct coap_resource *resource, struct coap_packet *request,
                        struct net_sockaddr *addr, socklen_t addr_len)
    {
        uint8_t token[COAP_TOKEN_MAX_LEN];
        uint16_t id;
        uint8_t tkl;
        int r;

        /* Let the CoAP server parse the request and add/remove observers if needed */
        r = coap_resource_parse_observe(resource, request, addr);

        id = coap_header_get_id(request);
        tkl = coap_header_get_token(request, token);

        return send_temperature(resource, addr, addr_len, r == 0 ? resource->age : 0,
                                id, token, tkl, true);
    }

    static void temp_notify(struct coap_resource *resource, struct coap_observer *observer)
    {
        send_temperature(resource, net_sad(&observer->addr), sizeof(observer->addr), resource->age,
                         0, observer->token, observer->tkl, false);
    }

    static const char * const temp_resource_path[] = { "sensors", "temp1", NULL };
    COAP_RESOURCE_DEFINE(temp_resource, my_service, {
        .path = temp_resource_path,
        .get = temp_get,
        .notify = temp_notify,
    });

    static void notify_observers(struct k_work *work)
    {
        if (sys_slist_is_empty(&temp_resource.observers)) {
            return;
        }

        coap_resource_notify(&temp_resource);
        k_work_reschedule(&temp_work, K_SECONDS(1));
    }

CoAP 事件
*********

通过启用 :kconfig:option:`CONFIG_NET_MGMT_EVENT`，用户可以注册 CoAP 事件。以下示例仅会在事件发生时打印信息。

.. code-block:: c

    #include <zephyr/sys/printk.h>
    #include <zephyr/net/coap_mgmt.h>
    #include <zephyr/net/coap_service.h>

    #define COAP_EVENTS_SET (NET_EVENT_COAP_OBSERVER_ADDED | NET_EVENT_COAP_OBSERVER_REMOVED | \
                             NET_EVENT_COAP_SERVICE_STARTED | NET_EVENT_COAP_SERVICE_STOPPED)

    void coap_event_handler(uint64_t mgmt_event, struct net_if *iface,
                            void *info, size_t info_length, void *user_data)
    {
        switch (mgmt_event) {
        case NET_EVENT_COAP_OBSERVER_ADDED:
            printk("CoAP observer added");
            break;
        case NET_EVENT_COAP_OBSERVER_REMOVED:
            printk("CoAP observer removed");
            break;
        case NET_EVENT_COAP_SERVICE_STARTED:
            if (info != NULL && info_length == sizeof(struct net_event_coap_service)) {
                struct net_event_coap_service *net_event = info;

                printk("CoAP service %s started", net_event->service->name);
            } else {
                printk("CoAP service started");
            }
            break;
        case NET_EVENT_COAP_SERVICE_STOPPED:
            if (info != NULL && info_length == sizeof(struct net_event_coap_service)) {
                struct net_event_coap_service *net_event = info;

                printk("CoAP service %s stopped", net_event->service->name);
            } else {
                printk("CoAP service stopped");
            }
            break;
        }
    }

    NET_MGMT_REGISTER_EVENT_HANDLER(coap_events, COAP_EVENTS_SET, coap_event_handler, NULL);

CoRE 链接格式
*************

:kconfig:option:`CONFIG_COAP_SERVER_WELL_KNOWN_CORE` 选项允许服务器处理 ``.well-known/core`` GET 请求。这样，客户端可以获取指向该服务器中托管的其他资源的超媒体链接列表。

API 参考
********

.. doxygengroup:: coap_service
.. doxygengroup:: coap_mgmt
