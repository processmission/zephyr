.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _gnss_api:

GNSS（全球导航卫星系统）
########################

概述
****

GNSS 是用于导航的卫星系统的统称，例如 GPS（全球定位系统）。GNSS 服务通常通过 GNSS 调制解调器访问，这些调制解调器接收并处理 GNSS 信号，以确定自身的位置，更确切地说，是其天线的位置。它们通常还提供精确的时间同步机制，一般称为 PPS（秒脉冲）。

子系统支持
**********

GNSS 子系统基于 :ref:`modem` 。GNSS 子系统涵盖了向调制解调器发送命令、从调制解调器接收命令，以及解析、创建和处理 NMEA0183 消息等全部功能。

要添加对其他基于 NMEA0183 的 GNSS 调制解调器的支持，基本上只需为特定的 GNSS 调制解调器实现电源管理和配置功能。

也可以添加对使用其他协议和/或总线的 GNSS 调制解调器的支持，而不局限于常见的通过 UART 传输 NMEA0183 的方式，但这需要驱动开发者投入更多工作。

电源管理
********

除非另有配置，GNSS 接收机通常在上电后立即开始捕获和跟踪 GNSS 信号。为了节省电力，应用可以切断 GNSS 接收机的电源，也可以停止内部 GNSS 引擎主动捕获和跟踪信号。后一种方式会停止位置计算，同时保持接收机供电并降低功耗，接收机与主机应用之间的通信链路也仍然可用，以便执行其他操作或恢复 GNSS 引擎运行。

在 GNSS 子系统中，可以通过调用 :c:func:`gnss_stop` API 实现这一点。这与 Zephyr 的设备电源管理（挂起/恢复）不同：接收机仍然保持供电，并且能够与主机应用通信，但 GNSS 跟踪已停止。

可以使用 :c:func:`gnss_start` 恢复 GNSS 跟踪。应用可以指定 :c:enum:`gnss_start_mode` ，该模式会影响首次定位时间。热启动保留导航数据，使接收机能够快速重新捕获信号；温启动和冷启动则分别丢弃部分或全部导航数据，因此需要更长的捕获时间。

GNSS 设备驱动必须确保 GNSS 调制解调器从挂起或断电状态恢复时开始跟踪，而无需应用显式调用 :c:func:`gnss_start` 。在这种情况下，大多数接收机最终会执行冷启动，因为它们在断电期间丢失了跟踪数据；但如果调制解调器保留了足够的状态信息，驱动也可以尝试温启动或热启动，以更快地恢复跟踪。这里的要求是上电后自动恢复跟踪；清除导航数据只是调制解调器断电带来的副作用，并不是从挂起状态恢复时有意执行的操作。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_GNSS`
* :kconfig:option:`CONFIG_GNSS_SATELLITES`
* :kconfig:option:`CONFIG_GNSS_DUMP_TO_LOG`

导航参考
********

.. doxygengroup:: navigation

GNSS API 参考
*************

.. doxygengroup:: gnss_interface
