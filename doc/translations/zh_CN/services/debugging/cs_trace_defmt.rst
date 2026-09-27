.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _cs_trace_defmt:

ARM Coresight 跟踪反格式化器
############################

格式化器是一种将多个跟踪流（由 7 位 ID 指定）封装为单个输出流的方法。格式化器使用 16 字节帧，最多封装 15 字节的数据。例如，ETR（Embedded Trace Router）会使用它，ETR 是一个循环 RAM 缓冲区，可以保存来自各种跟踪流的数据。跟踪数据通常由主机离线解码，但也可以在应用运行时使用反格式化器在片上解码数据。

用法
****

反格式化器通过用户回调进行初始化。数据使用 :c:func:`cs_trace_defmt_process` 按 16 字节块进行解码。每当流发生变化或到达块末尾时都会调用回调。回调包含流 ID 和数据。

API 文档
********

.. doxygengroup:: cs_trace_defmt
