.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _reset_api:

复位控制器
##########

概述
****

复位控制器是控制多个外设复位信号的单元。复位控制器 API 允许外设驱动程序请求控制其复位输入信号，包括置位、解除和切换这些信号。此外，还可以检查复位输入信号的复位状态。

line_assert 和 line_deassert API 函数是可选的，主要是因为在大多数情况下，我们只需要切换复位信号。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_RESET`

API 参考
********

.. doxygengroup:: reset_controller_interface
