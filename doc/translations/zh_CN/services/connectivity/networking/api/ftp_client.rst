.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ftp_client_interface:

FTP 客户端
##########

.. contents::
   :local:
   :depth: 2

概述
****

FTP 客户端库可用于从 FTP 服务器下载文件或向其上载文件。

FTP 客户端库通过 :c:member:`ftp_client.ctrl_callback` 和 :c:member:`ftp_client.data_callback` 这两个独立的回调函数上报 FTP 控制消息和下载数据。如果 :kconfig:option:`CONFIG_FTP_CLIENT_KEEPALIVE_TIME` 不为零，则可以将该库配置为通过定时器自动向服务器发送 KEEPALIVE 消息。KEEPALIVE 消息会按照 :kconfig:option:`CONFIG_FTP_CLIENT_KEEPALIVE_TIME` 所指示的时间间隔周期性地在间隔结束时发送。

协议
****

该库按照 :rfc:`959` 规范实现。

限制
****

该库目前只实现了一小部分命令，但添加新的命令支持很容易。

由于各 FTP 服务器实现存在差异，该库可能需要定制才能与特定服务器配合工作。

API 参考
********

.. doxygengroup:: ftp_client
