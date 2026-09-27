.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _peci_api:

平台环境控制接口（PECI）
########################

概述
****
平台环境控制接口（简称 PECI）是一项热管理标准，于 2006 年随 Intel Core 2 Duo 微处理器一同推出。PECI 接口允许外部设备读取处理器温度、执行处理器管理功能，以及管理处理器接口调优和诊断。PECI 总线驱动 API 支持嵌入式微控制器与 CPU 之间的交互。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_PECI`

API 参考
********

.. doxygengroup:: peci_interface
