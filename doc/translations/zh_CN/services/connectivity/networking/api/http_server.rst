.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _http_server_interface:

HTTP 服务器
###########

.. contents::
    :local:
    :depth: 2

概述
****

Zephyr 提供了一个 HTTP 服务器库，可用于注册 HTTP 服务以及与这些服务关联的 HTTP 资源。服务器会为每个注册的服务创建一个监听 socket，并处理传入的客户端连接。可以通过普通 TCP socket（HTTP）或 TLS socket（HTTPS）进行通信。支持 HTTP/1.1 （:rfc:`2616`）、HTTP/2 （:rfc:`9113`）和 HTTP/3 （:rfc:`9114`）协议版本。

服务器通常在后台线程中运行，对应用是透明的。应用可以通过相应的 API 函数控制服务器的活动。

某些资源类型（例如动态资源）会提供特定于资源的应用回调，使服务器能够与应用交互（例如提供资源内容或处理请求载荷）。

目前支持以下资源类型：

* 静态资源：内容在编译时定义，运行时不可修改（:c:enumerator:`HTTP_RESOURCE_TYPE_STATIC`）。

* 静态文件系统资源：文件系统的挂载路径以及文件系统对外提供的 URL 在构建时固定，但文件系统中的内容可以动态更改。这意味着文件可以由 HTTP 服务器之外的其它代码创建、修改或删除（:c:enumerator:`HTTP_RESOURCE_TYPE_STATIC_FS`）。

* 动态资源：内容由相应的应用回调在运行时提供（:c:enumerator:`HTTP_RESOURCE_TYPE_DYNAMIC`）。

* WebSocket 资源：允许与服务器建立 WebSocket 连接（:c:enumerator:`HTTP_RESOURCE_TYPE_WEBSOCKET`）。

Zephyr 提供了一个示例，演示 HTTP(s) 服务器运行和各种资源类型的使用。更多信息请参见 :zephyr:code-sample:`sockets-http-server`。

服务器设置
**********

在应用中启用 HTTP 服务器功能需要满足一些前提条件。

首先，必须在应用的配置文件中通过 :kconfig:option:`CONFIG_HTTP_SERVER` Kconfig 选项启用 HTTP 服务器：

.. code-block:: cfg
    :caption: ``prj.conf``

    CONFIG_HTTP_SERVER=y

所有 HTTP 服务和 HTTP 资源都放在专用的链接器段中。服务的链接器段在本地预定义，但应用需要为与各服务关联的资源定义各自的链接器段。资源的链接器段名称应以 ``http_resource_desc_`` 为前缀，并追加服务名称。

资源的链接器段应在链接器文件中定义。例如，对于名为 ``my_service`` 的服务，链接器段应定义如下：

.. code-block:: c
    :caption: ``sections-rom.ld``

    #include <zephyr/linker/iterable_sections.h>

    ITERABLE_SECTION_ROM(http_resource_desc_my_service, Z_LINK_ITERABLE_SUBALIGN)

最后，必须使用 CMake 将链接器文件和链接器段添加到应用中：

.. code-block:: cmake
    :caption: ``CMakeLists.txt``

    zephyr_linker_sources(SECTIONS sections-rom.ld)
    zephyr_linker_section(NAME http_resource_desc_my_service
                          KVMA RAM_REGION GROUP RODATA_REGION)

.. note::

    需要为系统中注册的每个 HTTP 服务定义一个单独的链接器段。

使用示例
********

服务
====

应用需要定义一个 HTTP 服务（或多个服务），其名称应与使用 :c:macro:`HTTP_SERVICE_DEFINE` 宏定义链接器段时使用的名称相同：

.. code-block:: c

    #include <zephyr/net/http/service.h>

    static uint16_t http_service_port = 80;

    HTTP_SERVICE_DEFINE(my_service, "0.0.0.0", &http_service_port, 1, 10, NULL, NULL, NULL);

或者，可以使用 :c:macro:`HTTPS_SERVICE_DEFINE` 定义 HTTPS 服务：

.. code-block:: c

    #include <zephyr/net/http/service.h>
    #include <zephyr/net/tls_credentials.h>

    #define HTTP_SERVER_CERTIFICATE_TAG 1

    static uint16_t https_service_port = 443;
    static const sec_tag_t sec_tag_list[] = {
        HTTP_SERVER_CERTIFICATE_TAG,
    };

    HTTPS_SERVICE_DEFINE(my_service, "0.0.0.0", &https_service_port, 1, 10,
                         NULL, NULL, NULL, sec_tag_list, sizeof(sec_tag_list));

按服务配置
==========

HTTP 服务支持单独配置，目前仅包括通过 ``http_service_config`` 结构进行 socket 创建。这允许应用自定义 socket 创建行为，例如设置特定的 socket 选项或使用自定义 socket 类型。

要使用自定义 socket 创建功能：

.. code-block:: c

    static int my_socket_create(const struct http_service_desc *svc, int af, int proto)
    {
        int fd;

        /* Create socket with custom parameters */
        fd = zsock_socket(af, SOCK_STREAM, proto);
        if (fd < 0) {
            return fd;
        }

        /* Set custom socket options */
        /* Add any other custom socket configuration */

        return fd;
    }

    static const struct http_service_config my_service_config = {
        .socket_create = my_socket_create,
    };

    static uint16_t http_service_port = 80;

    HTTP_SERVICE_DEFINE(my_service, "0.0.0.0", &http_service_port, 1, 10,
                        NULL, NULL, &my_service_config);

自定义 socket 创建函数接收以下参数： - ``svc``：指向服务描述符的指针 - ``af``：地址族（NET_AF_INET 或 NET_AF_INET6） - ``proto``：协议（对于 HTTPS，为 NET_IPPROTO_TCP 或 NET_IPPROTO_TLS_1_2）

该函数应在成功时返回 socket 文件描述符，在失败时返回负的错误码。

如果不需要自定义配置，只需为 config 参数传入 ``NULL``：

.. code-block:: c

    HTTP_SERVICE_DEFINE(my_service, "0.0.0.0", &http_service_port, 1, 10,
                        NULL, NULL, NULL);

回退资源
========

定义 HTTP/HTTPS 服务时，可以使用 ``_res_fallback`` 参数指定回退资源；当没有其它资源与 URL 匹配时，将使用该资源。例如，可以用它为所有未知路径提供索引页（适用于在前端处理路由的单页应用），或提供自定义的 404 响应。

.. code-block:: c

    static int default_handler(struct http_client_ctx *client, enum http_transaction_status status,
                       const struct http_request_ctx *request_ctx,
                       struct http_response_ctx *response_ctx, void *user_data)
    {
        static const char response_404[] = "Oops, page not found!";

        if (status == HTTP_SERVER_REQUEST_DATA_FINAL) {
            response_ctx->status = 404;
            response_ctx->body = response_404;
            response_ctx->body_len = sizeof(response_404) - 1;
            response_ctx->final_chunk = true;
        }

        return 0;
    }

    static struct http_resource_detail_dynamic default_detail = {
        .common = {
            .type = HTTP_RESOURCE_TYPE_DYNAMIC,
            .bitmask_of_supported_http_methods = BIT(HTTP_GET),
        },
        .cb = default_handler,
        .user_data = NULL,
    };

    /* Register a fallback resource to handle any unknown path */
    HTTP_SERVICE_DEFINE(my_service, "0.0.0.0", &http_service_port, 1, 10, NULL, &default_detail, NULL);

.. note::

    HTTPS 服务依赖于系统中注册的 TLS 凭据。有关如何在系统中配置 TLS 凭据的信息，请参见 :ref:`sockets_tls_credentials_subsys`。

定义 HTTP(s) 服务后，可以使用 :c:macro:`HTTP_RESOURCE_DEFINE` 宏为其注册资源。

应用可以通过启用 :kconfig:option:`CONFIG_HTTP_SERVER_RESOURCE_WILDCARD` 选项来启用资源通配符支持。设置该选项后，只需一个资源处理程序即可匹配多个传入的 HTTP 请求。系统使用 `fnmatch() <https://pubs.opengroup.org/onlinepubs/9699919799/functions/fnmatch.html>`__ POSIX API 函数来匹配 URL 路径中的模式。

示例：

.. code-block:: c

    HTTP_RESOURCE_DEFINE(my_resource, my_service, "/foo*", &resource_detail);

这将匹配所有以字符串 ``foo`` 开头的 URL。有关模式匹配语法的说明，请参见 `POSIX.2 第 2.13 章 <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_13>`__。

静态资源
========

静态资源内容在构建时定义且不可变。以下示例展示了如何在应用中将 gzip 压缩的网页定义为静态资源：

.. code-block:: c

    static const uint8_t index_html_gz[] = {
        #include "index.html.gz.inc"
    };

    struct http_resource_detail_static index_html_gz_resource_detail = {
        .common = {
            .type = HTTP_RESOURCE_TYPE_STATIC,
            .bitmask_of_supported_http_methods = BIT(HTTP_GET),
            .content_encoding = "gzip",
        },
        .static_data = index_html_gz,
        .static_data_len = sizeof(index_html_gz),
    };

    HTTP_RESOURCE_DEFINE(index_html_gz_resource, my_service, "/",
                         &index_html_gz_resource_detail);

资源内容和内容编码由应用决定。对于上面的示例，可以在构建期间向应用的 ``CMakeLists.txt`` 文件中添加以下代码来生成 gzip 压缩的网页：

.. code-block:: cmake
    :caption: ``CMakeLists.txt``

    set(gen_dir ${ZEPHYR_BINARY_DIR}/include/generated/)
    set(source_file_index src/index.html)
    generate_inc_file_for_target(app ${source_file_index} ${gen_dir}/index.html.gz.inc --gzip)

其中 ``src/index.html`` 是要压缩的网页的位置。

静态文件系统资源
================

静态文件系统资源内容在构建时定义且不可变。请注意，仅支持 ``GET`` 操作，用户无法将文件上传到文件系统。以下示例展示了如何在应用中将路径定义为静态资源：

.. code-block:: c

    struct http_resource_detail_static_fs static_fs_resource_detail = {
        .common = {
            .type                              = HTTP_RESOURCE_TYPE_STATIC_FS,
            .bitmask_of_supported_http_methods = BIT(HTTP_GET),
        },
        .fs_path = "/lfs1/www",
    };

    HTTP_RESOURCE_DEFINE(static_fs_resource, my_service, "*", &static_fs_resource_detail);

所有位于 /lfs1/www 的文件都会提供给客户端。如果文件经过 gzip 压缩，则必须在文件名后追加 .gz（例如 index.html.gz）；当客户端请求 index.html 时，服务器会提供 index.html.gz，并向 HTTP 报头添加 gzip content-encoding。

内容类型根据文件扩展名确定。服务器支持 .html、.js、.css、.jpg、.png 和 .svg。可以通过 :c:macro:`HTTP_SERVER_CONTENT_TYPE` 宏提供更多内容类型。所有其它文件都以 text/html 内容类型提供。

.. code-block:: c

    HTTP_SERVER_CONTENT_TYPE(json, "application/json")

从静态文件系统提供文件时，可以使用 :kconfig:option:`CONFIG_HTTP_SERVER_STATIC_FS_RESPONSE_SIZE` Kconfig 选项配置响应块大小。该选项决定向客户端传输文件内容时各个块的大小。

动态资源
========

对于动态资源，需要注册资源回调，以便在服务器与应用之间交换数据。

以下示例代码展示了如何注册带有简单资源处理程序的动态资源，该处理程序将接收到的数据回显给客户端：

.. code-block:: c

    static int dyn_handler(struct http_client_ctx *client, enum http_transaction_status status,
                           const struct http_request_ctx *request_ctx,
                           struct http_response_ctx *response_ctx, void *user_data)
    {
    #define MAX_TEMP_PRINT_LEN 32
        static char print_str[MAX_TEMP_PRINT_LEN];
        enum http_method method = client->method;
        static size_t processed;

        __ASSERT_NO_MSG(request_ctx->data != NULL);

        if (status == HTTP_SERVER_TRANSACTION_ABORTED ||
            status == HTTP_SERVER_TRANSACTION_COMPLETE) {
            if (status == HTTP_SERVER_TRANSACTION_ABORTED) {
                LOG_DBG("Transaction aborted after %zd bytes.", processed);
            }
            processed = 0;
            return 0;
        }

        processed += request_ctx->data_len;

        snprintf(print_str, sizeof(print_str), "%s received (%zd bytes)",
                 http_method_str(method), request_ctx->data_len);
        LOG_HEXDUMP_DBG(request_ctx->data, request_ctx->data_len, print_str);

        if (status == HTTP_SERVER_REQUEST_DATA_FINAL) {
            LOG_DBG("All data received (%zd bytes).", processed);
            processed = 0;
        }

        /* Echo data back to client */
        response_ctx->body = request_ctx->data;
        response_ctx->body_len = request_ctx->data_len;
        response_ctx->final_chunk = (status == HTTP_SERVER_REQUEST_DATA_FINAL);

        return 0;
    }

    struct http_resource_detail_dynamic dyn_resource_detail = {
        .common = {
            .type = HTTP_RESOURCE_TYPE_DYNAMIC,
            .bitmask_of_supported_http_methods =
                BIT(HTTP_GET) | BIT(HTTP_POST),
        },
        .cb = dyn_handler,
        .user_data = NULL,
    };

    HTTP_RESOURCE_DEFINE(dyn_resource, my_service, "/dynamic",
                         &dyn_resource_detail);


对于单个请求，资源回调可能会被多次调用，因此应用应能够跟踪已接收数据的进度。

``status`` 字段向应用告知请求载荷从服务器传递到应用的进度。只要状态为 :c:enumerator:`HTTP_SERVER_REQUEST_DATA_MORE`，应用就应预期在后续回调调用中提供更多数据。当所有请求载荷都传递给应用后，服务器会报告 :c:enumerator:`HTTP_SERVER_REQUEST_DATA_FINAL` 状态。如果请求处理期间发生通信错误（例如客户端在收到完整载荷之前关闭了连接），服务器会报告 :c:enumerator:`HTTP_SERVER_TRANSACTION_ABORTED`。当响应已完整发送给客户端后，服务器会报告 :c:enumerator:`HTTP_SERVER_TRANSACTION_COMPLETE` 状态。这两个事件中任一事件都表示请求处理已完成，应用应重置为该资源记录的任何进度，并等待新请求到来。服务器保证同一时间只能有一个客户端访问该资源。

``request_ctx`` 参数用于向应用传递请求数据：

* ``data`` 和 ``data_len`` 字段向应用传递请求数据。

* 如果启用了 :kconfig:option:`CONFIG_HTTP_SERVER_CAPTURE_HEADERS`，则 ``headers``、``header_count`` 和 ``headers_status`` 字段会向应用传递请求报头。这些字段仅在请求的首次回调中填充；详情请参见 :ref:`http_server_interface_accessing_request_headers`。

``response_ctx`` 字段由应用用于向 HTTP 服务器传递响应数据：

* ``status`` 字段允许应用发送 HTTP 响应码。如果未填充，响应码默认为 200。

* ``headers`` 和 ``header_count`` 字段可用于让应用发送任意 HTTP 报头。如果未填充，默认仅发送 Transfer-Encoding 和 Content-Type。回调可以根据需要覆盖 Content-Type。

* ``body`` 和 ``body_len`` 字段用于发送主体数据。

* ``final_chunk`` 字段用于指示应用没有更多要发送的响应数据。

报头和/或响应码只能在第一个填充的 ``response_ctx`` 中发送，此后在后续回调中只允许发送更多主体数据。

服务器会持续调用资源回调，直到它向应用提供了所有请求数据，并且应用报告回复中没有更多要包含的数据。

WebSocket 资源
==============

WebSocket 资源会注册一个应用回调，当发生 WebSocket 连接升级时会调用该回调。该回调会收到一个与底层 TCP/TLS 连接对应的 socket 描述符。一旦调用，应用将完全接管该 socket，即负责在完成后释放它。

.. code-block:: c

    static int ws_socket;
    static uint8_t ws_recv_buffer[1024];

    int ws_setup(int sock, struct http_request_ctx *request_ctx, void *user_data)
    {
        ws_socket = sock;
        return 0;
    }

    struct http_resource_detail_websocket ws_resource_detail = {
        .common = {
            .type = HTTP_RESOURCE_TYPE_WEBSOCKET,
            /* We need HTTP/1.1 Get method for upgrading */
            .bitmask_of_supported_http_methods = BIT(HTTP_GET),
        },
        .cb = ws_setup,
        .data_buffer = ws_recv_buffer,
        .data_buffer_len = sizeof(ws_recv_buffer),
        .user_data = NULL, /* Fill this for any user specific data */
    };

    HTTP_RESOURCE_DEFINE(ws_resource, my_service, "/", &ws_resource_detail);

以上最小示例展示了如何注册带有简单回调的 WebSocket 资源，该回调仅用于存储收到的 socket 描述符。WebSocket 连接的后续处理取决于应用，不在本指南的讨论范围内。有关基于 WebSocket 的回显服务实现示例，请参见 :zephyr:code-sample:`sockets-http-server`。

.. _http_server_interface_accessing_request_headers:

访问请求报头
============

应用可以注册对任何特定 HTTP 请求报头的关注。随后，这些报头会为每个传入请求存储，并可从动态资源回调中访问。

.. important::

   对于给定请求，捕获的请求报头 **仅在首次回调中** 传递给应用。在同一请求的任何后续回调中，``request_ctx`` 的 ``headers``、``header_count`` 和 ``headers_status`` 字段都会被清除（``headers_status`` 变为 :c:enumerator:`HTTP_HEADER_STATUS_NONE`）。应用必须在首次回调期间复制出所需的任何报头值，而不是稍后再读取。

   请注意，首次回调可能同时携带请求主体数据，也可能不携带（这取决于 HTTP 方法和传输分帧方式）。不要根据是否存在主体数据来决定是否处理报头：始终检查 ``headers_status``，并在其不是 :c:enumerator:`HTTP_HEADER_STATUS_NONE` 时保存报头。

必须首先通过 :kconfig:option:`CONFIG_HTTP_SERVER_CAPTURE_HEADERS` Kconfig 选项启用此功能。

随后，应用可以注册要捕获的报头，并在动态资源回调中读取这些值。推荐的做法是在首次回调中复制出关注的报头，然后在收到完整请求主体后对其进行处理：

.. code-block:: c

    HTTP_SERVER_REGISTER_HEADER_CAPTURE(capture_user_agent, "User-Agent");

    static char user_agent[64];

    static int dyn_handler(struct http_client_ctx *client, enum http_transaction_status status,
                           const struct http_request_ctx *request_ctx,
                           struct http_response_ctx *response_ctx, void *user_data)
    {
        /* Request headers are only present in the first callback, so copy out
         * any values needed later before they are gone.
         */
        if (request_ctx->headers_status != HTTP_HEADER_STATUS_NONE) {
            for (size_t i = 0; i < request_ctx->header_count; i++) {
                const struct http_header *hdr = &request_ctx->headers[i];

                LOG_INF("Captured header: '%s: %s'", hdr->name, hdr->value);

                if (strcasecmp(hdr->name, "User-Agent") == 0) {
                    strncpy(user_agent, hdr->value, sizeof(user_agent) - 1);
                }
            }
        }

        /* Process request body data (may be empty in the first callback). */

        if (status == HTTP_SERVER_REQUEST_DATA_FINAL) {
            /* Full request received: act on the body together with the header
             * values stashed above (e.g. user_agent).
             */
        }

        return 0;
    }

API 参考
********

.. doxygengroup:: http_service
.. doxygengroup:: http_server
