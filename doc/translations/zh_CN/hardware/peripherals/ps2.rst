.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ps2_api:


PS/2
####

概述
****
PS/2 连接器于 1987 年首次随 IBM 同名台式 PC 产品线上市，随后成为鼠标和键盘连接的行业标准。大约从 2007 年开始，USB 取代了 PS/2，成为现代外设连接标准。为在配备 PS/2 连接器的开发板上支持旧式设备，Zephyr 提供了这些 PS/2 驱动 API。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_PS2`

API 参考
********

.. doxygengroup:: ps2_interface
