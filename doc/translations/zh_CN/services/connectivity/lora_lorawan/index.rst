.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _lora_api:
.. _lorawan_api:

LoRa 与 LoRaWAN
###############

概述
****

LoRa（Long Range 的缩写）是由 `Semtech Corporation`_ 开发的专有低功耗无线通信协议。

LoRa 基于线性调频扩频（CSS，chirp spread spectrum）调制技术，充当物理层（PHY）。

LoRaWAN（Long Range Wide Area Network）在 LoRa PHY 之上定义了网络层。

Zephyr 提供 LoRa API，可直接通过无线接口发送原始数据包；也提供 LoRaWAN API，可通过网关将终端设备连接到互联网。

Zephyr 提供两种 LoRaWAN 后端实现：

* **LoRaMac-node** （默认）：基于 Semtech 的 `LoRaMac-node library`_，作为 Zephyr 模块包含在内。支持 LoRaWAN 规范定义的所有区域。通过 :kconfig:option:`CONFIG_LORA_MODULE_BACKEND_LORAMAC_NODE` 选择。

* **Native**：与 Zephyr 风格一致的 LoRaWAN 1.0.x Class A 实现，直接与 LoRa 无线电驱动通信，不依赖外部组件。目前支持 EU868 区域。通过 :kconfig:option:`CONFIG_LORA_MODULE_BACKEND_NATIVE` 选择。

.. note::

        ``LoRaMac-node`` 已被 Semtech 弃用，改用 `LoRa Basics Modem`_。将 Zephyr API 移植为以 ``LoRa Basics Modem`` 为后端的工作正在进行中。

        目前，通过 :kconfig:option:`CONFIG_LORA_MODULE_BACKEND_LORA_BASICS_MODEM`，仅 SX1261、SX1262、SX1272 和 SX1276 芯片组支持基础 LoRa API。


LoRaWAN 规范由 `LoRa Alliance`_ 发布。

.. _`Semtech Corporation`: https://www.semtech.com/

.. _`LoRaMac-node library`: https://github.com/Lora-net/LoRaMac-node

.. _`LoRa Basics Modem`: https://github.com/Lora-net/SWL2001

.. _`LoRa Alliance`: https://lora-alliance.org/

配置选项
********

LoRa PHY
========

相关配置选项见 :zephyr_file:`drivers/lora/Kconfig`。

* :kconfig:option:`CONFIG_LORA`

* :kconfig:option:`CONFIG_LORA_SHELL`

* :kconfig:option:`CONFIG_LORA_INIT_PRIORITY`

LoRaWAN
=======

相关配置选项见 :zephyr_file:`subsys/lorawan/Kconfig`。

* :kconfig:option:`CONFIG_LORAWAN`

* :kconfig:option:`CONFIG_LORAWAN_SYSTEM_MAX_RX_ERROR`

* :kconfig:option:`CONFIG_LORAWAN_REGION_AS923`

* :kconfig:option:`CONFIG_LORAWAN_REGION_AU915`

* :kconfig:option:`CONFIG_LORAWAN_REGION_CN470`

* :kconfig:option:`CONFIG_LORAWAN_REGION_CN779`

* :kconfig:option:`CONFIG_LORAWAN_REGION_EU433`

* :kconfig:option:`CONFIG_LORAWAN_REGION_EU868`

* :kconfig:option:`CONFIG_LORAWAN_REGION_KR920`

* :kconfig:option:`CONFIG_LORAWAN_REGION_IN865`

* :kconfig:option:`CONFIG_LORAWAN_REGION_US915`

* :kconfig:option:`CONFIG_LORAWAN_REGION_RU864`

原生后端
--------

原生后端通过 :kconfig:option:`CONFIG_LORA_MODULE_BACKEND_NATIVE` 选择，其附加选项位于 :zephyr_file:`subsys/lorawan/native/Kconfig`：

* :kconfig:option:`CONFIG_LORAWAN_NATIVE_ENGINE_STACK_SIZE`

* :kconfig:option:`CONFIG_LORAWAN_NATIVE_ENGINE_PRIORITY`

* :kconfig:option:`CONFIG_LORAWAN_NATIVE_PUBLIC_NETWORK`

* :kconfig:option:`CONFIG_LORAWAN_NATIVE_DUTY_CYCLE`

API 参考
********

LoRa PHY
========

.. doxygengroup:: lora_interface

LoRaWAN
=======

.. doxygengroup:: lorawan_api
