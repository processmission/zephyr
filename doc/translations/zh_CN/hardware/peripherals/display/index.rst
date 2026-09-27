.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _display_api:

显示
####

Zephyr 的显示子系统提供了与各种显示设备交互的统一方式。显示 API 与传输方式无关：它描述你希望显示设备执行的操作，而不暴露数据如何通过线路传输。

MIPI 显示总线接口（DBI）
************************

**MIPI DBI** 规范定义了多种用于连接主机与显示控制器的并行和串行总线。在 Zephyr 中，DBI 支持提供了命令写入、读取、像素传输、复位及相关操作的总线级原语，驱动程序在内部使用这些原语实现通用 API。

应用不直接使用 DBI 函数，而是调用通用显示 API（例如写入像素），由显示驱动程序在底层处理 DBI 协议。

MIPI-DBI 定义了 3 种接口类型：

* A 型：Motorola 6800 并行总线
* B 型：Intel 8080 并行总线
* C 型：SPI 类型的串行位总线，有 3 种选项：

  #. 每字节需要 9 个写时钟周期，最后一位为命令/数据选择位
  #. 与上述相同，但每字节需要 16 个写时钟周期
  #. 每字节需要 8 个写时钟周期。通过 GPIO 引脚选择命令/数据

目前，API 不支持采用 16 个写时钟周期的 C 型控制器（选项 2）。

MIPI 显示串行接口（DSI）
************************

**MIPI DSI** 标准定义了一种面向现代彩色 TFT 面板的高速差分串行总线。Zephyr 的 DSI 支持提供了驱动程序在 DSI 链路上实现通用显示 API 所需的原语。

与 DBI 一样，应用不直接调用 DSI 函数。应用通过使用通用显示 API 保持可移植性，而驱动程序在内部处理 DSI 事务。

API 参考
********

通用显示接口
============

.. doxygengroup:: display_interface

.. _mipi_dbi_api:

MIPI Display Bus Interface (DBI)
================================

.. doxygengroup:: mipi_dbi_interface

.. _mipi_dsi_api:

MIPI Display Serial Interface (DSI)
===================================

.. doxygengroup:: mipi_dsi_interface

Grove LCD 显示屏
================

.. doxygengroup:: grove_display

BBC micro:bit 显示屏
====================

.. doxygengroup:: mb_display

单色字符帧缓冲区
================

.. doxygengroup:: monochrome_character_framebuffer
