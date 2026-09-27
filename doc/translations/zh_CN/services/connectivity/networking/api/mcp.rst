.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mcp_server_interface:

MCP 服务器
##########

.. contents::
    :local:
    :depth: 2

概述
****

`Model Context Protocol`_ （MCP）是一种开放标准，用于将 AI 应用连接到外部数据源和工具。它定义了 MCP 客户端（AI 代理）与 MCP 服务器（能力提供方）之间基于 JSON-RPC 的通信协议。

Zephyr MCP 服务器库实现 MCP 规范（版本 2025-11-25）中的服务器角色。它使联网的 Zephyr 设备能够公开工具，供 AI 代理通过 HTTP 发现和调用。该库基于现有的 Zephyr 子系统构建：用于传输的 HTTP 服务器库和用于序列化的 JSON 库。

.. note::

   该库被标记为 :ref:`实验性 <api_lifecycle_experimental>`。目前仅实现带文本响应的工具服务。更多内容类型、会话管理、SSE 流式传输、授权以及其他服务等附加功能计划在后续版本中提供。

.. _Model Context Protocol: https://modelcontextprotocol.io/specification/2025-11-25

架构
****

.. graphviz::
   :caption: MCP 服务器分层架构
   :alt: MCP Server layered architecture diagram

   digraph mcp_arch {
       rankdir=TB;
       node [shape=box, style=filled, fillcolor="#e8e8e8", fontname="sans-serif"];
       edge [arrowsize=0.8];

       app [label="Application\n(tool callbacks)", fillcolor="#cce5ff"];
       core [label="MCP Server Core\n(protocol, registries, workers)"];
       json [label="JSON Processing\n(Zephyr JSON library)"];
       transport [label="Transport Layer\n(HTTP / mock)"];

       app -> core [label="register/respond"];
       core -> json [label="serialize/parse"];
       core -> transport [label="send/receive"];
   }

应用
   注册工具并实现其回调。工具执行结果通过 :c:func:`mcp_server_submit_tool_message` 提交回核心。

MCP 服务器核心
   实现 MCP 协议状态机。管理客户端连接、工具注册表、执行跟踪以及可配置的工作线程池。健康监视线程负责执行超时并触发取消操作。

JSON 处理
   使用 Zephyr JSON 库序列化传出的响应，并反序列化传入的 JSON-RPC 请求。

传输层
   对网络协议进行抽象。随附的 HTTP 传输使用 Zephyr HTTP 服务器库。另提供用于单元测试的模拟传输。

HTTP 传输与异步响应
===================

Zephyr 的 HTTP 服务器在单线程中运行，并且一次只能处理所有连接中的一个请求。资源回调必须返回后，服务器才能处理来自任何客户端的下一个请求。由于工具执行耗时可能超过阻塞整个服务器所能接受的程度，MCP HTTP 传输实现了轮询到 SSE 的回退机制：

1. 对于 POST 请求，传输层会在内部轮询工具响应，最长持续 :kconfig:option:`CONFIG_MCP_HTTP_TIMEOUT_MS` （每隔 :kconfig:option:`CONFIG_MCP_HTTP_POLL_INTERVAL_MS` 检查一次）。
2. 如果响应在此时间窗口内就绪，则直接以 ``application/json`` 返回。
3. 如果超时到期，传输层会切换到 SSE 模式：返回一个仅包含事件 ID（不含数据）的 ``text/event-stream`` 响应。这会通知客户端响应仍在等待中，客户端应开始通过周期性 GET 请求进行轮询（间隔由 :kconfig:option:`CONFIG_MCP_HTTP_SSE_RETRY_MS` 控制）。
4. 客户端随后使用 ``Last-Event-Id`` 标头发起周期性 GET 请求。如果结果已就绪，服务器会发送响应并结束 SSE 流。如果结果尚未就绪，服务器会再次发送重试响应。

.. note::

   这并不是完整的 SSE 流式传输。该机制仅为无法在初始 HTTP 超时内完成的请求提供延迟响应。本阶段不支持服务器发起的通知和流式工具输出。

配置
****

使用 :kconfig:option:`CONFIG_MCP_SERVER` 启用该库。传输方式通过 :kconfig:option:`CONFIG_MCP_TRANSPORT_HTTP` （默认）或 :kconfig:option:`CONFIG_MCP_TRANSPORT_MOCK` （仅用于测试）选择。

最小 ``prj.conf``：

.. code-block:: kconfig

   CONFIG_NETWORKING=y
   CONFIG_NET_TCP=y
   CONFIG_HTTP_SERVER=y
   CONFIG_MCP_SERVER=y
   CONFIG_MCP_TRANSPORT_HTTP=y

关键配置组：

可扩展性
   :kconfig:option:`CONFIG_MCP_MAX_CLIENTS`,
   :kconfig:option:`CONFIG_MCP_MAX_CLIENT_REQUESTS`,
   :kconfig:option:`CONFIG_MCP_MAX_TOOLS`,
   :kconfig:option:`CONFIG_MCP_REQUEST_WORKERS`

超时
   :kconfig:option:`CONFIG_MCP_TOOL_EXEC_TIMEOUT_MS`,
   :kconfig:option:`CONFIG_MCP_TOOL_IDLE_TIMEOUT_MS`,
   :kconfig:option:`CONFIG_MCP_TOOL_CANCEL_TIMEOUT_MS`,
   :kconfig:option:`CONFIG_MCP_CLIENT_TIMEOUT_MS`
   :kconfig:option:`CONFIG_MCP_HTTP_TIMEOUT_MS`

内存分配
   :kconfig:option:`CONFIG_MCP_ALLOC_SLAB` （默认）使用预分配的 slab 提供确定且无碎片的分配。:kconfig:option:`CONFIG_MCP_ALLOC_HEAP` 使用 ``k_malloc``/``k_free`` 进行按需分配，但可能产生碎片。

用法
****

服务器设置
==========

.. code-block:: c

   #include <zephyr/net/mcp/mcp_server.h>
   #include <zephyr/net/mcp/mcp_server_http.h>

   static mcp_server_ctx_t server;

   int main(void)
   {
       server = mcp_server_init();
       mcp_server_http_init(server);

       /* Register tools here */

       mcp_server_start(server);
       mcp_server_http_start(server);
       return 0;
   }

工具注册
========

.. code-block:: c

   static int my_tool_cb(enum mcp_tool_event_type event,
                         const char *arguments,
                         const char *execution_token)
   {
       if (event == MCP_TOOL_CANCEL_REQUEST) {
           struct mcp_tool_message ack = {
               .type = MCP_USR_TOOL_CANCEL_ACK,
           };

           mcp_server_submit_tool_message(server, &ack, execution_token);

           /* Handle cancellation here */
       }

       struct mcp_tool_message resp = {
           .type = MCP_USR_TOOL_RESPONSE,
           .data = "Tool execution result",
           .length = strlen("Tool execution result"),
           .is_error = false,
       };
       return mcp_server_submit_tool_message(server, &resp, execution_token);
   }

   static const struct mcp_tool_record my_tool = {
       .metadata = {
           .name = "my_tool",
           .input_schema = "{\"type\":\"object\",\"properties\":{}}",
       },
       .callback = my_tool_cb,
   };

   mcp_server_add_tool(server, &my_tool);

``.data`` 字段接受纯文本字符串。服务器会自动将其包装为符合 MCP 的 ``"text"`` 内容项。最大长度为 :kconfig:option:`CONFIG_MCP_TOOL_RESULT_MAX_LEN`。

工具回调模式
============

阻塞
   短时运行的工具直接在工作线程中执行，并在返回前调用 :c:func:`mcp_server_submit_tool_message`。工作线程栈大小为 :kconfig:option:`CONFIG_MCP_REQUEST_WORKER_STACK_SIZE`。

异步
   长时间运行的工具应派生专用线程，从回调中立即返回，并在稍后使用提供的执行令牌提交响应。周期性 ping（``MCP_USR_TOOL_PING``）可防止健康监视器取消空闲执行。

取消
   当健康监视器或客户端请求取消时，会使用 ``MCP_TOOL_CANCEL_REQUEST`` 调用回调。工具应停止工作并提交 ``MCP_USR_TOOL_CANCEL_ACK``。

工具移除
========

可以在运行时使用 :c:func:`mcp_server_remove_tool` 移除工具。如果工具当前正在执行，该调用会返回 ``-EBUSY``；请稍后重试。

限制
****

以下 MCP 功能尚未实现：

- 资源、提示、采样、根和会话管理
- 服务器发起的通知和流式工具输出
- 图像和嵌入式资源内容类型（仅支持 ``"text"``）
- 完整 SSE 传输（仅支持延迟响应交付）

测试
****

单元测试位于 :zephyr_file:`tests/net/lib/mcp/`。它们使用模拟传输（:kconfig:option:`CONFIG_MCP_TRANSPORT_MOCK`）在没有网络协议栈的情况下测试协议逻辑。

示例
****

有关注册多个工具（包括基于 GPIO 的 LED 控制）的可运行示例，请参见 :zephyr:code-sample:`mcp-server-hello-world`。

API 参考
********

.. doxygengroup:: mcp_server
