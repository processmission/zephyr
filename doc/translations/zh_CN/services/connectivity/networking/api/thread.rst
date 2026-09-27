.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _thread_protocol_interface:

Thread 协议
###########

.. contents::
    :local:
    :depth: 2

概述
****
Thread 是一种低功耗网状网络技术，专为家庭自动化应用而设计。它是一种基于 IPv6 的标准，在 IEEE 802.15.4 协议之上使用 6LoWPAN 技术。借助 IP 连接性，可以通过 Thread 边界路由器轻松地将 Thread 网状网络连接到互联网。

Thread 规范提供了高水平的网络安全性。使用 Thread 构建的网状网络是安全的：只有经过身份验证的设备才能加入网络，网状网络内的所有通信都经过加密。有关 Thread 协议的更多信息见 `Thread Group website <https://www.threadgroup.org>`_。

Zephyr 集成了名为 OpenThread 的开源 Thread 协议实现，其文档见 `OpenThread website <https://openthread.io/>`_。

互联网连接
**********

要将网状网络连接到互联网，需要 Thread 边界路由器。OpenThread 社区提供了 Thread 边界路由器的开源实现。搭建边界路由器的说明见 `OpenThread Border Router guide <https://openthread.io/guides/border-router>`_。

用法示例
********

可以使用 Zephyr 的 Echo server 和 Echo client 示例来试用 OpenThread，这些示例为 OpenThread 提供了开箱即用的配置。要在这两个示例中启用 OpenThread 支持，请使用 ``overlay-ot.conf`` 覆盖配置文件构建它们。详情见 :zephyr:code-sample:`sockets-echo-server` 和 :zephyr:code-sample:`sockets-echo-client` 示例。

Zephyr 还提供了 :zephyr:code-sample:`openthread-shell`，它可用于测试和调试 Thread 及其底层的 IEEE 802.15.4 驱动。

Thread 相关 API
***************

OpenThread 驱动 API
===================

OpenThread L2 内部使用 Zephyr 与协议无关的 IEEE 802.15.4 驱动 API。希望支持 OpenThread 的 **驱动开发者** 会关注该 API。

该驱动 API 是 :ref:`ieee802154_driver_api` 子系统的一部分，并在该处有文档说明。

OpenThread L2 适配层 API
========================

Zephyr 的 OpenThread L2 平台适配层将外部 OpenThread 协议栈与 Zephyr 与协议无关的 IEEE 802.15.4 驱动 API 粘合在一起。只有 OpenThread L2 的 **子系统贡献者** 会关注该 API。

OpenThread 平台 API
===================

OpenThread 平台 API 由 OpenThread 协议栈定义，并在 Zephyr 中作为 OpenThread 模块实现。应用可以直接使用该实现，也可以通过 OpenThread L2 适配层访问它。

使用 OpenThread L2 适配层 API
-----------------------------

要通过 OpenThread L2 适配层使用 OpenThread 平台 API，请将 :kconfig:option:`CONFIG_NET_L2_OPENTHREAD` 和 :kconfig:option:`CONFIG_NETWORKING` 这两个 Kconfig 选项都设置为 ``y``。适配层将使用 :file:`modules/openthread/platform/radio.c` 中的 OpenThread 无线电 API 实现。在这种配置下，OpenThread 协议栈由适配层初始化和管理。

直接使用 OpenThread 平台 API
----------------------------

也可以绕过 OpenThread L2 适配层，直接使用 OpenThread 平台 API。但这种方式需要自行提供与特定无线电驱动兼容的 OpenThread 无线电 API 实现。

要直接使用 OpenThread 平台 API，请将 :kconfig:option:`CONFIG_OPENTHREAD` Kconfig 选项设置为 ``y``，并且 **不要** 设置 :kconfig:option:`CONFIG_NET_L2_OPENTHREAD`。此时必须使用自己的无线电驱动实现 `OpenThread radio API <https://openthread.io/reference/group/radio-config>`_ 中的以下函数：

* ``otPlatRadioGetPromiscuous``
* ``otPlatRadioGetCcaEnergyDetectThreshold``
* ``otPlatRadioGetTransmitPower``
* ``otPlatRadioGetIeeeEui64``
* ``otPlatRadioSetPromiscuous``
* ``otPlatRadioGetCaps``
* ``otPlatRadioGetTransmitBuffer``
* ``otPlatRadioSetPanId``
* ``otPlatRadioEnable``
* ``otPlatRadioDisable``
* ``otPlatRadioReceive``
* ``otPlatRadioGetRssi``
* ``otPlatRadioGetReceiveSensitivity``
* ``otPlatRadioEnergyScan``
* ``otPlatRadioSetExtendedAddress``
* ``otPlatRadioSetShortAddress``
* ``otPlatRadioAddSrcMatchExtEntry``
* ``otPlatRadioTransmit``
* ``otPlatRadioClearSrcMatchShortEntries``
* ``otPlatRadioClearSrcMatchExtEntries``
* ``otPlatRadioEnableSrcMatch``
* ``otPlatRadioAddSrcMatchShortEntry``
* ``otPlatRadioClearSrcMatchShortEntry``
* ``otPlatRadioClearSrcMatchExtEntry``

此外，还必须实现 OpenThread 无线电 API 中的以下函数（见 :zephyr_file:`include/zephyr/net/openthread.h`），以处理无线电初始化和事件处理：

* :c:func:`platformRadioInit`
* :c:func:`platformRadioProcess`

要在此方式下初始化 OpenThread 协议栈，可以在应用中调用 :c:func:`ot_platform_init` 函数，也可以启用 :kconfig:option:`CONFIG_OPENTHREAD_SYS_INIT` Kconfig 选项，在系统启动期间自动初始化 OpenThread。可以使用 :kconfig:option:`CONFIG_OPENTHREAD_SYS_INIT_PRIORITY` Kconfig 选项设置初始化优先级。

.. doxygengroup:: openthread
