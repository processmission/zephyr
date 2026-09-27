.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ota:

空中下载更新
############

概述
****

空中下载（OTA）更新是一种使用网络连接向远程设备交付固件更新的方法。尽管该名称暗示无线连接，但通过有线连接（例如以太网）接收的更新通常仍被称为 OTA 更新。这种方法需要服务器基础设施来托管固件二进制文件，并实现一种在更新可用时发出信号的方法。安全性是 OTA 更新关注的问题；固件二进制文件在升级前应经过加密签名和验证。

:ref:`dfu` 一节讨论了使用 MCUboot 升级 Zephyr 固件。相同的方法可以作为 OTA 的一部分使用。二进制文件首先下载到未占用的代码分区，通常名为 ``slot1_partition``，然后使用 :ref:`mcuboot` 流程进行升级。

OTA 示例
********

Golioth
=======

`Golioth`_ 是一个包含 OTA 更新的 IoT 管理平台。设备被配置为在 Golioth Cloud 上观察可用的固件修订版本。当有新版本可用时，设备会下载并烧录二进制文件。在此实现中，云与设备之间的连接使用 TLS/DTLS 保护，签名的固件二进制文件在升级发生前由 MCUboot 确认。

1. 可在 `Golioth Firmware SDK repository`_ 上找到可用的示例
2. `Golioth OTA documentation`_ 包含有关版本管理过程的完整信息

Eclipse hawkBit™
================

`Eclipse hawkBit™`_ 是一个更新服务器框架，通过对 REST API 进行轮询来检测固件更新。检测到新更新后，会下载并安装二进制文件。可以使用 MCUboot 在升级固件前验证签名。

Zephyr 的 :zephyr:code-sample-category:`mgmt` 部分中包含一个 :zephyr:code-sample:`hawkbit-api` 示例。

UpdateHub
=========

`UpdateHub`_ 是一个用于远程更新嵌入式设备的平台。更新可以手动触发，也可以通过轮询进行监控。检测到新更新后，会下载并安装二进制文件。可以使用 MCUboot 在升级固件前验证签名。

Zephyr 的 :zephyr:code-sample-category:`mgmt` 部分中包含一个 :zephyr:code-sample:`updatehub-fota` 示例。

SMP 服务器
==========

简单管理协议（SMP）服务器可用于通过 Bluetooth Low Energy（LE）或 UDP 更新固件。:ref:`mcu_mgr` 用于将签名的固件二进制文件发送到远程设备，在此设备上由 MCUboot 在升级发生前对其进行验证。

Zephyr 的 :zephyr:code-sample-category:`mgmt` 部分中包含一个 :zephyr:code-sample:`smp-svr` 示例。

轻量级 M2M（LwM2M）
===================

:ref:`lwm2m_interface` 协议包含通过 :kconfig:option:`CONFIG_LWM2M_FIRMWARE_UPDATE_OBJ_SUPPORT` 进行固件更新的支持。设备使用 DTLS 安全地连接到 LwM2M 服务器。有一个 :zephyr:code-sample:`lwm2m-client` 示例可用，但它不演示固件更新功能。

mender-mcu
==========

`mender-mcu`_ 通过与 Zephyr 集成，在资源受限的设备上实现稳健的固件更新。它实现了 Update Module 接口，并提供一个默认的 Update Module，该模块与 MCUboot 集成以提供 A/B 更新。这使得微控制器单元（MCU）能够执行原子、故障安全的 OTA 更新，并在失败时自动回滚。

有关集成细节和示例，请参阅 :ref:`external_module_mender_mcu`。

Memfault 和由 Memfault 提供支持的 nRF Cloud
===========================================

`Memfault`_ 是一个包含 OTA 管理的 IoT 可观测性平台。设备定期与 Memfault 的服务签到以检查 OTA 更新，当有更新可用时，会下载并安装二进制文件。

有关整体集成细节和示例，请参阅 :ref:`external_module_memfault_firmware_sdk`。

.. _MCUboot bootloader: https://mcuboot.com/
.. _Golioth: https://golioth.io/
.. _Golioth Firmware SDK repository: https://github.com/golioth/golioth-firmware-sdk/tree/main/examples/zephyr/fw_update
.. _Golioth OTA documentation: https://docs.golioth.io/device-management/ota
.. _Eclipse hawkBit™: https://www.eclipse.org/hawkbit/
.. _UpdateHub: https://updatehub.io/
.. _mender-mcu: https://github.com/mendersoftware/mender-mcu
.. _Memfault: https://memfault.com/
