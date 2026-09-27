.. SPDX-FileCopyrightText: Copyright The Process Mission
.. SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
.. SPDX-License-Identifier: Apache-2.0

.. _devicetree:

Devicetree
##########

*设备树（devicetree）* 是一种层次化的数据结构，主要用于描述硬件。
Zephyr 主要将设备树用于以下两个方面：

- 向 :ref:`device_model_api` 描述硬件。
- 提供硬件的初始配置。

本页提供设备树使用指南和参考资料的入口。

.. _dt-guide:

设备树指南
**********

本节介绍在 Zephyr 开发中使用设备树的方法。

.. toctree::
   :maxdepth: 2

   intro.rst
   design.rst
   bindings.rst
   api-usage.rst
   phandles.rst
   zephyr-user-node.rst
   howtos.rst
   troubleshooting.rst
   dt-vs-kconfig.rst

.. _dt-reference:

设备树参考
**********

本节提供 Zephyr 设备树 API 和内置绑定的参考资料。

与平台无关的详细说明，请参阅 `设备树规范 <Devicetree specification_>`_。

.. _Devicetree specification: https://www.devicetree.org/

.. toctree::
   :maxdepth: 3
   :glob:

   api/*
