.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _network_tracing:

网络跟踪
########

.. contents::
    :local:
    :depth: 2

用户可以启用网络核心协议栈和 socket API 调用跟踪。

:kconfig:option:`CONFIG_TRACING_NET_CORE` 选项控制核心网络协议栈跟踪。如果启用了跟踪和网络功能，默认会启用此选项。系统将开始收集接收和发送调用的判定结果，即网络数据包是成功发送还是成功接收。它还会收集数据包发送或接收的耗时，即交付网络数据包所花费的时间，以及所使用的网络接口、优先级和流量类别。

:kconfig:option:`CONFIG_TRACING_NET_SOCKETS` 选项可用于跟踪系统中 BSD socket 调用的使用情况。如果启用了跟踪和 BSD socket API 支持，则会启用此选项。系统将开始收集进行了哪些 BSD socket API 调用，以及这些 API 调用使用了哪些参数、返回了哪些内容。

关于如何使用跟踪服务，请参阅 :ref:`跟踪文档 <tracing>`。
