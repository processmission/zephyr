.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _dtdoctor:

设备树诊断（``dtdoctor``）
##########################

``dtdoctor`` 是用于诊断设备树相关构建错误的静态分析工具。

它拦截编译器和链接器错误消息，当消息涉及未解析的设备树设备符号（例如 ``__device_dts_ord_*``）时，提供详细的可能原因和修复方法。

使用 dtdoctor
*************

构建时传入 ``-DZEPHYR_SCA_VARIANT=dtdoctor``，即可启用 ``dtdoctor``。

例如：

.. code-block:: shell

   west build -b reel_board samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=dtdoctor
