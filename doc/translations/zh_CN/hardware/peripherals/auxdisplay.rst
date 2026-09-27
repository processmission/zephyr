.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _auxdisplay_api:

辅助显示屏（auxdisplay）
########################

概述
****

辅助显示屏是一种基于文本的显示屏，提供简单的接口，用于显示文本、数字或字母数字数据。与 :ref:`display_api` 不同，辅助显示屏不支持自定义图形输出，且通常为单色显示屏，其支持的最复杂的自定义功能是生成自定义字符。这类显示屏价格低廉，有多种配置和尺寸，常见的显示尺寸为 2 行，每行 16 个字符。

此 API 尚不稳定，可能会发生变化。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_AUXDISPLAY`
* :kconfig:option:`CONFIG_AUXDISPLAY_INIT_PRIORITY`

API 参考
********

.. doxygengroup:: auxdisplay_interface
