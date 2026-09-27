.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mipi_stp_decoder:

MIPI STP 解码器
###############

MIPI 系统跟踪协议（MIPI STP）是作为一种通用基础协议开发的，可由多个特定于应用的跟踪协议共享。它充当包装协议，将通常包含来自不同跟踪源的不同跟踪协议的各类流合并在一起。流由操作码（最短为 4 位）以及可选数据和可选时间戳组成。操作码可用于数据（8、16、32、64 位数据，带标记/不带标记，带或不带时间戳）、流识别（主设备和通道）、同步（ASYNC 操作码）等。

使用该协议的一个示例是 ARM Coresight STM（System Trace Macrocell），写入 Stimulus Port 寄存器的数据会直接映射到 STP 流。

该模块可用于在片上对数据流进行解码。这里使用 STP v2。

用法
****

解码器通过回调进行初始化。每解码出一个操作码都会调用一次回调。由于操作码之间存在依赖关系（例如时间戳可以是相对的），解码器具有内部状态。解码器可以处于同步状态，也可以未同步。初始状态是可配置的。如果解码器未与流同步，则它会逐个解码半字节，以搜索 ASYNC 操作码。可以通过调用 :c:func:`mipi_stp_decoder_sync_loss` 向解码器指示同步丢失。使用 :c:func:`mipi_stp_decoder_decode` 解码数据。

限制
****

存在以下限制：

* 解码器仅支持小端架构。
* 在解码半字节时，如果内核支持非对齐内存访问，效率会更高。实现同时提供使用非对齐内存访问的优化版本和通用版本。优化版本用于 ARM Cortex-M（M0 除外）。
* 仅实现了最常用操作码的有限集合。

API 文档
********

.. doxygengroup:: mipi_stp_decoder_apis
