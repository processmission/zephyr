.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _sdhc_api:

安全数字（SD 卡）接口
#####################

Zephyr 可以通过系统的原生 SD 卡接口或 SPI（串行外设接口）与连接的 SD 卡通信。某些设备还可以与 MMC（多媒体卡）设备通信。

应用可以使用 Zephyr 的 :ref:`磁盘访问 API <disk_access_api>` 将 SD 卡用作存储设备，也可以使用 Zephyr 的 SD 卡子系统直接读写 SD 卡。

SD 主机控制器（SDHC）
*********************

SD 主机控制器（SDHC）是一种能够向 SD 卡发送命令的设备。这些命令可以通过系统的原生 SD 卡接口或 SPI 发送。

应用通常应使用 Zephyr 的 SD 卡子系统，而不应直接使用 SD 主机控制器 API。

请求
====

SD 主机控制器（SDHC）API 的核心是 :c:func:`sdhc_request` API。请求包含一个 :c:struct:`sdhc_command` 命令结构体，以及一个可选的 :c:struct:`sdhc_data` 数据结构体。调用者可以检查返回码或 SD 命令结构体的 ``response`` 字段，以确定 SDHC 请求是否成功。数据结构体允许调用者指定要传输的块数，以及用于读取或写入这些块的缓冲区位置。所提供的缓冲区用于发送还是读取数据，取决于所提供的命令操作码。

主机控制器 I/O
==============

:c:func:`sdhc_set_io` API 允许用户更改 SD 主机控制器的 I/O 设置，例如时钟频率、I/O 电压和卡供电状态。并非所有控制器都支持应用全部 I/O 设置。例如，SPI 模式控制器通常无法接通或切断 SD 卡的电源。

相关配置选项：

* :kconfig:option:`CONFIG_SDHC`

API 参考
********

.. doxygengroup:: sdhc_interface
