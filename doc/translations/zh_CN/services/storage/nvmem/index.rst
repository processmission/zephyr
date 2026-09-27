.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _nvmem:

非易失性存储器（NVMEM）
#######################

NVMEM 子系统为访问非易失性存储设备提供通用接口。它抽象底层硬件，并提供用于读写数据的统一 API。

关键概念
********

NVMEM 提供者
============

NVMEM 提供者是公开 NVMEM 单元的驱动。例如，EEPROM 驱动可以是 NVMEM 提供者。NVMEM 提供者负责向底层硬件读写数据。

NVMEM 单元
==========

NVMEM 单元是非易失性存储器的区域。它在 devicetree 中定义，并具有偏移量、大小和只读状态等属性。

NVMEM 使用者
============

NVMEM 使用者是使用 NVMEM 单元存储或检索数据的驱动或应用。

配置
****

* :kconfig:option:`CONFIG_NVMEM`：启用 NVMEM 子系统。
* :kconfig:option:`CONFIG_NVMEM_BBRAM`：启用对电池后备 RAM 的 NVMEM 支持。
* :kconfig:option:`CONFIG_NVMEM_EEPROM`：启用对 EEPROM 设备的 NVMEM 支持。
* :kconfig:option-regex:`CONFIG_NVMEM_FLASH.*`：配置对 flash 设备的 NVMEM 支持。
* :kconfig:option-regex:`CONFIG_NVMEM_OTP.*`：配置对 OTP 设备的 NVMEM 支持。

Devicetree 绑定
***************

NVMEM 子系统依赖 devicetree 绑定来定义 NVMEM 单元。以下是在 devicetree 中定义 NVMEM 提供者和单元的示例：

.. literalinclude:: devicetree_bindings.txt
   :language: dts

reg 属性是一个数组，包含：

* 在其中创建单元的内存偏移量，
* 单元的大小（以字节为单位）。

``#nvmem-cell-cells`` 描述 phandle 中属性项的数量，参见 :ref:`dt-bindings-cells`，通常设置为零。

然后，使用者可以像这样引用 NVMEM 单元：

.. literalinclude:: my_consumer.txt
   :language: dts


用法示例
********

以下示例展示如何使用 NVMEM API 从 NVMEM 单元读取数据：

.. literalinclude:: usage_example.txt
   :language: c


API 参考
********

.. doxygengroup:: nvmem_interface
