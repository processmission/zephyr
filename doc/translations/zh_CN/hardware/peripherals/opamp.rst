.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _opamp_api:

运算放大器（OPAMP）
###################

概述
****

运算放大器是一种模拟器件，可放大差分输入信号（反相输入与同相输入之间的差值），产生相应的输出电压。


配置
****

启用 OPAMP 时，必须通过 Devicetree 提供初始配置。OPAMP 的增益可在运行时调整。

相关配置选项：

* :kconfig:option:`CONFIG_OPAMP`

API 参考
********

.. doxygengroup:: opamp_interface
