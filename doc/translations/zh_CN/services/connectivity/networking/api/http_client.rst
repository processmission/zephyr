.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _http_client_interface:

HTTP 客户端
###########

.. contents::
    :local:
    :depth: 2

概述
****

HTTP 客户端库允许发送 HTTP 请求并解析 HTTP 响应。该库通过 sockets API 进行通信，但不会自行创建 socket。可通过 :kconfig:option:`CONFIG_HTTP_CLIENT` Kconfig 选项启用。

应用必须负责创建 socket 并将其传递给该库。因此，根据应用的需求，该库可以通过普通 TCP socket（HTTP）或 TLS socket（HTTPS）进行通信。

使用示例
********

HTTP 客户端库的 API 只有一个函数。

下面是一个正确创建的请求结构示例：

.. code-block:: c

    struct http_request req = { 0 };
    static uint8_t recv_buf[512];

    req.method = HTTP_GET;
    req.url = "/";
    req.host = "localhost";
    req.protocol = "HTTP/1.1";
    req.response = response_cb;
    req.recv_buf = recv_buf;
    req.recv_buf_len = sizeof(recv_buf);

    /* sock is a file descriptor referencing a socket that has been connected
     * to the HTTP server.
     */
    ret = http_client_req(sock, &req, 5000, NULL);

如果服务器响应该请求，库会通过请求结构中注册的响应回调向应用提供响应。由于库可能分块提供响应，应用必须能够处理这些数据块。

除了包含响应数据的结构之外，回调函数还会一并提供库是否期望接收更多数据的信息。

下面是一个非常简单的响应处理函数示例：

.. code-block:: c

    static int response_cb(struct http_response *rsp,
                           enum http_final_call final_data,
                           void *user_data)
    {
        if (final_data == HTTP_DATA_MORE) {
            LOG_INF("Partial data received (%zd bytes)", rsp->data_len);
        } else if (final_data == HTTP_DATA_FINAL) {
            LOG_INF("All the data received (%zd bytes)", rsp->data_len);
        }

        LOG_INF("Response status %s", rsp->http_status);

        return 0;
    }

有关该库用法的更多信息，请参见 :zephyr:code-sample:`HTTP 客户端示例应用 <sockets-http-client>`。

API 参考
********

.. doxygengroup:: http_client
