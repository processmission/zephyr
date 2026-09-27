.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _networking_api:

网络 API
########

Zephyr 为应用提供了标准 BSD socket API（定义于 :zephyr_file:`include/zephyr/net/socket.h`）支持。更多详情见 :ref:`BSD socket API <bsd_sockets_interface>`。

除标准 API 外，Zephyr 还提供了一组供应用使用的自定义网络 API 和库。详情见下面的列表。

.. note::
   应用不应使用 :zephyr_file:`include/zephyr/net/net_context.h` 中的旧版连接 API。

.. toctree::
   :maxdepth: 2

   apis.rst
   buf_mgmt.rst
   net_tech.rst
   protocols.rst
   quic.rst
   system_mgmt.rst
   tsn.rst
   zperf.rst
