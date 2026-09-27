.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _regulator_api:

稳压器
######

此子系统用于控制稳压器和稳流器。一个常见的例子是通过 GPIO 控制晶体管，为并非始终需要运行的设备供电。另一个例子是电源管理集成电路（PMIC），这类设备通常要复杂得多。

``*-supply`` Devicetree 属性用于标识 Devicetree 节点直接依赖的稳压器。在该节点的驱动程序中，当设备需要工作时，使用稳压器 API 请求供电；当设备关闭时，释放供电请求。

需要稳压器的最简单情况是只有一个使用者。在这种情况下，使用稳压器设备基础设施的开销并不划算，应使用 ``*-gpios`` Devicetree 属性。这些稳压器不提供设备接口，因为它们完全由相应节点（例如传感器）的驱动程序控制。

.. _regulator_api_reference:

API 参考
********

.. doxygengroup:: regulator_interface

.. doxygengroup:: regulator_fake
