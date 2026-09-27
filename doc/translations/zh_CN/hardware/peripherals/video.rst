.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _video_api:

视频
####

视频驱动 API 为视频设备提供通用接口。

基本操作
********

视频设备
========

视频设备是对硬件或软件视频功能的抽象，可以生成、处理、消耗或转换视频数据。视频 API 旨在提供灵活的方式来创建、操作和组合各种视频设备。

端点
====

每个视频设备可以具有一个或多个端点。输出端点用于配置视频输出功能并生成数据。输入端点用于配置视频输入功能并消耗数据。

视频缓冲区
==========

视频缓冲区为数据提供传输机制，对内容本身没有特定要求。内容要求由端点格式定义。视频缓冲区可以加入设备端点的队列，以执行填充（输入端点）或消耗（输出端点）操作。操作完成后，可以将缓冲区移出队列，以便进行后续处理、释放或重用。

控制项
======

视频控制项通过 CID（控制标识符）进行访问和标识，表示一个视频控制属性。不同设备提供的控制项各不相同，可以是通用控制项、与设备类别相关的控制项或厂商专用控制项。设置和获取控制项的函数提供通用且可扩展的接口，用于操作和创建控制项。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_VIDEO`

API 参考
********

.. doxygengroup:: video_api

.. doxygengroup:: video_interface

.. doxygengroup:: video_control_ids
