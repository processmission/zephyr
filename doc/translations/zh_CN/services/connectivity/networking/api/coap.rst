.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _coap_sock_interface:

CoAP
####

.. contents::
    :local:
    :depth: 2

概述
****

受限应用协议（Constrained Application Protocol，CoAP）是一种专用 Web 传输协议，适用于受限节点和受限网络（例如低功耗、有损网络）。它为支持 CoAP 特性的 RESTful Web 服务提供了便捷的 API。有关该协议本身的更多信息，请参见 :rfc:`7252`。

Zephyr 提供了一个支持客户端和服务器角色的 CoAP 库。该库可通过 :kconfig:option:`CONFIG_COAP` Kconfig 选项启用，并可根据用户需求进行配置。Zephyr CoAP 库使用普通缓冲区实现。API 用户创建用于通信的 socket，并将缓冲区传给该库以进行解析等操作。该库本身不为用户创建任何 socket。

在 CoAP 之上，Zephyr 还支持 LwM2M（Lightweight Machine 2 Machine）协议，这是一种简单、低成本的远程管理和服务启用机制。更多信息请参见 :ref:`lwm2m_interface`。

支持的 RFC：

- :rfc:`7252` - 受限应用协议（CoAP）
- :rfc:`6690` - 受限 RESTful 环境（CoRE）链接格式
- :rfc:`7959` - 受限应用协议（CoAP）中的块传输
- :rfc:`7641` - 受限应用协议（CoAP）中的资源观察
- :rfc:`8613` - 受限 RESTful 环境中的对象安全（OSCORE）

.. note:: 这些 RFC 的内容并未全部得到支持。具体支持的功能取决于 Zephyr 的需求。

Zephyr CoAP 库还支持 :rfc:`8613` 中规定的受限 RESTful 环境对象安全（OSCORE）。更多信息请参见 :ref:`coap_oscore_interface`。

用法示例
********

CoAP 服务器
===========

.. note::

   系统提供了 :ref:`coap_server_interface` 子系统；下文介绍如何创建自定义服务器实现。

要创建 CoAP 服务器，需要为服务器定义资源。应先添加 ``.well-known/core`` 资源，然后再添加其他需要包含在 ``.well-known/core`` 资源响应中的所有资源。

.. code-block:: c

    static struct coap_resource resources[] = {
        { .get = well_known_core_get,
          .path = COAP_WELL_KNOWN_CORE_PATH,
        },
        { .get  = sample_get,
          .post = sample_post,
          .del  = sample_del,
          .put  = sample_put,
          .path = sample_path
        },
        { },
    };

应用从 socket 读取数据，并将缓冲区传给 CoAP 库以解析消息。如果 CoAP 消息格式正确，该库会使用缓冲区以及上面定义的资源，调用正确的回调函数来处理来自客户端的 CoAP 请求。回调函数负责根据 CoAP 请求进行回复或执行相应操作。

.. code-block:: c

    coap_packet_parse(&request, data, data_len, options, opt_num);
    ...
    coap_handle_request(&request, resources, options, opt_num,
                        client_addr, client_addr_len);

如果启用了 :kconfig:option:`CONFIG_COAP_URI_WILDCARD`，服务器可以使用类似 MQTT 的通配符风格接受多个资源：

- 加号（+）表示路径中的单级通配符；
- 井号（#）表示路径中的多级通配符。

.. code-block:: c

    static const char * const led_set[] = { "led","+","set", NULL };
    static const char * const btn_get[] = { "button","#", NULL };
    static const char * const no_wc[] = { "test","+1", NULL };

它接受 /led/0/set、led/1234/set、led/any/set、/button/door/1、/test/+1，但对于 /led/1、/test/21、/test/1 返回 -ENOENT。

此选项默认启用；对于类似 '/some_resource/+/#' 的资源路径，请禁用它以避免意外行为。

CoAP 客户端
===========

.. note::

   系统提供了 :ref:`coap_client_interface` 子系统；下文介绍如何创建自定义客户端实现。

如果 CoAP 客户端知道 CoAP 服务器中的资源，客户端可以开始准备 CoAP 请求并等待响应。如果客户端不知道 CoAP 服务器中的资源，可以通过 ``.well-known/core`` CoAP 消息请求资源。

.. code-block:: c

    /* Initialize the CoAP message */
    char *path = "test";
    struct coap_packet request;
    uint8_t data[100];
    uint8_t payload[20];

    coap_packet_init(&request, data, sizeof(data),
                     1, COAP_TYPE_CON, 8, coap_next_token(),
                     COAP_METHOD_GET, coap_next_id());

    /* Append options */
    coap_packet_append_option(&request, COAP_OPTION_URI_PATH,
                              path, strlen(path));

    /* Append Payload marker if you are going to add payload */
    coap_packet_append_payload_marker(&request);

    /* Append payload */
    coap_packet_append_payload(&request, (uint8_t *)payload,
                               sizeof(payload) - 1);

    /* send over sockets */

测试
****

测试 Zephyr CoAP 库有多种方法。

libcoap
=======
libcoap 为计算能力、射频范围、内存、带宽或网络数据包大小等方面受限的设备实现了一种轻量级应用协议。源代码见 `libcoap <https://github.com/obgm/libcoap>`_。libcoap 提供了一个脚本（``examples/etsi_coaptest.sh``），用于测试 Zephyr 中的 coap-server 功能。

更多详情请参见 `net-tools <https://github.com/zephyrproject-rtos/net-tools>`_ 项目

按照 :ref:`networking_with_qemu` 中所述，可以在 QEMU 上构建并运行 :zephyr:code-sample:`coap-server` 示例。

在主机上使用以下命令，运行 ETSI 测试用例的 libcoap 实现：

.. code-block:: console

   sudo ./libcoap/examples/etsi_coaptest.sh -i tap0 2001:db8::1

TTCN3
=====
Eclipse 提供了基于 TTCN3 的测试，可用于测试 CoAP 实现。

安装 eclipse-titan，并为 titan 工具设置符号链接

.. code-block:: console

    sudo apt-get install eclipse-titan

    cd /usr/share/titan

    sudo ln -s /usr/bin bin
    sudo ln /usr/bin/titanver bin
    sudo ln -s /usr/bin/mctr_cli bin
    sudo ln -s /usr/include/titan include
    sudo ln -s /usr/lib/titan lib

    export TTCN3_DIR=/usr/share/titan

    git clone https://gitlab.eclipse.org/eclipse/titan/titan.misc.git

    cd titan.misc

按照以下说明设置 CoAP 测试套件：

- https://gitlab.eclipse.org/eclipse/titan/titan.misc
- https://gitlab.eclipse.org/eclipse/titan/titan.misc/-/tree/master/CoAP_Conf

构建完成后，可按照 :ref:`networking_with_qemu` 中所述，在 QEMU 上构建并运行 :zephyr:code-sample:`coap-server` 示例。

根据实际设置，修改 coap.cfg 文件中客户端（测试套件）和服务器（Zephyr coap-server 示例）的地址。

使用以下命令执行测试用例。

.. code-block:: console

   ttcn3_start coaptests coap.cfg

TTCN3 测试的示例输出如下所示。

.. code-block:: console

   Verdict statistics: 0 none (0.00 %), 10 pass (100.00 %), 0 inconc (0.00 %), 0 fail (0.00 %), 0 error (0.00 %).
   Test execution summary: 10 test cases were executed. Overall verdict: pass

API 参考
********

.. doxygengroup:: coap
