.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _websocket_interface:

WebSocket 客户端 API
####################

.. contents::
    :local:
    :depth: 2

概述
****

WebSocket 客户端库允许 Zephyr 连接到 WebSocket 服务器。应用可以直接使用 WebSocket 客户端 API 与服务器建立 WebSocket 连接，也可以将其用作 MQTT 等其它网络协议的传输层。

有关 WebSocket 工作原理的详细介绍，请参见这篇 `WebSocket 维基百科文章 <https://en.wikipedia.org/wiki/WebSocket>`_。

有关该协议本身的更多信息，请参见 :rfc:`6455`。

WebSocket 传输
**************

WebSocket API 可充当 MQTT 等其它高层协议的传输层。通过启用 :kconfig:option:`CONFIG_MQTT_LIB_WEBSOCKET` 和 :kconfig:option:`CONFIG_WEBSOCKET_CLIENT` Kconfig 选项，可以将 Zephyr MQTT 客户端库配置为使用 WebSocket 传输。

首先需要创建一个 socket 并连接到 WebSocket 服务器：

.. code-block:: c

    sock = socket(family, SOCK_STREAM, IPPROTO_TCP);
    ...
    ret = connect(sock, addr, addr_len);
    ...

然后按如下方式创建 WebSocket 传输 socket：

.. code-block:: c

    ws_sock = websocket_connect(sock, &config, timeout, user_data);

随后可以使用该 WebSocket socket 发送或接收数据，WebSocket 客户端 API 会将发送或接收的数据封装到 WebSocket 数据包载荷中或从中解封装。可以使用 :c:func:`websocket_xxx()` API 或普通 BSD socket API 函数来发送和接收应用数据。

.. code-block:: c

    ret = websocket_send_msg(ws_sock, buf_to_send, buf_len,
                             WEBSOCKET_OPCODE_DATA_BINARY, true, true,
                             K_FOREVER);
    ...
    ret = send(ws_sock, buf_to_send, buf_len, 0);

如果使用普通 BSD socket 函数，则目前仅支持 TEXT 数据。要发送 BINARY 数据，必须使用 :c:func:`websocket_send_msg()`。

完成后，必须关闭 WebSocket 传输 socket。用户应在调用 websocket_disconnect 之后处理 TCP socket 的生命周期（关闭/复用）。

.. code-block:: c

    ret = close(ws_sock);
    or
    ret = websocket_disconnect(ws_sock);


API 参考
********

.. doxygengroup:: websocket
