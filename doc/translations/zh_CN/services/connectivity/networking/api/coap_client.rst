.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _coap_client_interface:

CoAP 客户端
###########

.. contents::
    :local:
    :depth: 2

概述
****

CoAP 客户端库允许应用发送 CoAP 请求并解析 CoAP 响应。该库可通过 :kconfig:option:`CONFIG_COAP_CLIENT` Kconfig 选项启用。应用通过请求中提供给 API 的回调获知响应。CoAP 客户端通过 socket 处理通信。由于 CoAP 客户端不会创建其使用的 socket，应用需要负责创建 socket。支持普通 UDP 或 DTLS socket。

基于 TCP 的 CoAP
================

还支持 :rfc:`8323` 中规定的基于可靠传输（TCP/TLS）的 CoAP。可通过 :kconfig:option:`CONFIG_COAP_CLIENT_TCP` 启用。TCP 客户端内部管理连接建立、CSM（Capabilities and Settings Message）交换以及信令（Ping/Pong、Release、Abort）。与 UDP 客户端不同，应用不创建 socket，而是使用服务器地址调用 :c:func:`coap_client_tcp_connect`。用法示例见 :zephyr:code-sample:`coap-client-tcp`。

用法示例
********

以下示例展示了如何初始化 CoAP 客户端并发送请求：

.. code-block:: c

    static struct coap_client client;
    struct coap_client_request req = { 0 };

    coap_client_init(&client, NULL);

    req.method = COAP_METHOD_GET;
    req.confirmable = true;
    strcpy(req.path, "test");
    req.fmt = COAP_CONTENT_FORMAT_TEXT_PLAIN;
    req.cb = response_cb;
    req.payload = NULL;
    req.len = 0;

    /* Sock is a file descriptor referencing a socket, address is the net_sockaddr struct for the
     * destination address of the request or NULL if the socket is already connected.
     */
    ret = coap_client_req(&client, sock, &address, &req, -1);

发送任何请求之前，需要先初始化 CoAP 客户端。初始化后，应用可以发送 CoAP 请求并等待响应。目前，单个 CoAP 客户端一次只能发送一个请求。系统中可以有多个 CoAP 客户端。

所提供的回调将在以下情况下被调用：

- 请求有响应
- 请求因某种原因失败

回调包含一个标志 ``last_block``，用于指示响应中是否还有更多数据，并表示当前响应属于块传输的一部分。当 ``last_block`` 设为 true 时，响应已经完成，客户端从回调返回后即可处理下一个请求。

如果服务器对请求作出响应，库会通过请求结构中注册的响应回调将响应提供给应用。由于响应可能采用块传输，且客户端会针对每个块调用一次回调，因此应用应能够处理所有块，以便处理完整的响应。

在块传输期间，客户端会按照 :rfc:`7959` 的要求比较已接收块的 ETag 选项。如果在传输过程中资源表示发生变化，传输将被中止，并以 ``result_code`` 设置为 ``-EBADMSG`` 调用回调。这比 RFC 的最低要求更严格：RFC 仅要求比较服务器提供的 ETag，而此实现还会在块之间 ETag 选项出现或消失时中止传输，因为无法验证这种带标签和未带标签块的混合情况。应用应丢弃已接收的部分数据，并可以重试请求。

以下是一个非常简单的响应处理函数示例：

.. code-block:: c

    void response_cb(const struct coap_client_response_data *data, void *user_data)
    {
        if (data->result_code >= 0) {
                LOG_INF("CoAP response from server %d", data->result_code);
                if (data->last_block) {
                        LOG_INF("Last packet received");
                }
        } else {
                LOG_ERR("Error in sending request %d", data->result_code);
        }
    }

应用也可以向请求中添加 CoAP 选项。以下示例展示了应用向初始请求添加 Block2 选项，以便针对预期大到需要块传输的资源，向服务器建议最大块大小（参见 :rfc:`7959` 图 3：带早期协商的块式 GET）。

.. code-block:: c

    static struct coap_client client;
    struct coap_client_request req = { 0 };

    coap_client_init(&client, NULL);

    req.method = COAP_METHOD_GET;
    req.confirmable = true;
    strcpy(req.path, "test");
    req.fmt = COAP_CONTENT_FORMAT_TEXT_PLAIN;
    req.cb = response_cb;
    req.options[0] = coap_client_option_initial_block2();
    req.num_options = 1;
    req.payload = NULL;
    req.len = 0;

    ret = coap_client_req(&client, sock, &address, &req, -1);

应用还可以选择为 CoAP 上传注册载荷回调，而不是提供载荷指针。在这种情况下，CoAP 客户端库会在准备 PUT/POST 请求时调用该回调，以便应用可以分块提供载荷，而无需提供包含完整载荷的单个连续缓冲区。提供 Lorem Ipsum 字符串内容的示例回调如下所示：

.. code-block:: c

    static int lorem_ipsum_cb(size_t offset, const uint8_t **payload, size_t *len,
                              bool *last_block, void *user_data)
    {
        size_t data_left;

        if (offset > LOREM_IPSUM_STRLEN) {
            return -EINVAL;
        }

        *payload = LOREM_IPSUM + offset;

        data_left = LOREM_IPSUM_STRLEN - offset;
        if (data_left <= *len) {
            *len = data_left;
            *last_block = true;
        } else {
            *last_block = false;
        }

        return 0;
    }

然后可以为 PUT/POST 请求注册该回调，而不是提供载荷指针：

.. code-block:: c

    struct coap_client_request req = { 0 };

    req.method = COAP_METHOD_PUT;
    req.confirmable = true;
    strcpy(req.path, "lorem-ipsum");
    req.fmt = COAP_CONTENT_FORMAT_TEXT_PLAIN;
    req.cb = response_cb;
    req.payload_cb = lorem_ipsum_cb,

    ret = coap_client_req(&client, sock, &address, &req, -1);


API 参考
********

.. doxygengroup:: coap_client

.. doxygengroup:: coap_client_tcp
