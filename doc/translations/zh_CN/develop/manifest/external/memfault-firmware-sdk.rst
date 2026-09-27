.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_memfault_firmware_sdk:

memfault-firmware-sdk
#####################

简介
****

`memfault-firmware-sdk`_ 为嵌入式开发者提供 MCU 设备的内置远程调试、性能监测和 OTA 更新能力。它自动收集现场设备的崩溃报告、日志和栈回溯，使开发者无需直接接触设备即可诊断问题。SDK 还收集内存使用、电池续航、连接状况及固件稳定性等轻量级性能指标，以持续跟踪设备群的可靠性。

SDK 与 `Memfault`_ 平台通信，由平台汇总数据，帮助团队更快确定问题优先级并解决问题。此外，SDK 支持无线固件更新，可受控分批发布并远程部署新版本。

该 SDK 采用带有特定服务使用限制的自定义 BSD 风格许可证。详情见 `Memfault Firmware SDK License`_。

在 Zephyr 中使用
****************

要将 ``memfault-firmware-sdk`` 作为 Zephyr :ref:`模块 <modules>` 引入，在 :file:`west.yaml` 中添加以下 West 项目条目，然后运行 :command:`west update`：

.. code-block:: yaml

   manifest:
     remotes:
       # Add the Memfault GitHub repo
       - name: memfault
         url-base: https://github.com/memfault
     projects:
       # Add the Memfault SDK
       - name: memfault-firmware-sdk
         path: modules/lib/memfault-firmware-sdk
         revision: 1.33.0
         remote: memfault

.. note::

   上述 revision 仅为示例。请在 `memfault-firmware-sdk`_ 发布页面查看最新发布标签，确保选择所需版本。

详细说明和 API 文档见 `memfault-firmware-sdk documentation`_ 及随附的 `memfault-firmware-sdk examples`_。

参考资料
********

.. _memfault-firmware-sdk:
   https://github.com/memfault/memfault-firmware-sdk

.. _Memfault Firmware SDK License:
   https://github.com/memfault/memfault-firmware-sdk/blob/master/LICENSE

.. _memfault-firmware-sdk documentation:
    https://docs.memfault.com/docs/mcu/introduction

.. _memfault-firmware-sdk Zephyr guide:
   https://docs.memfault.com/docs/mcu/zephyr-guide

.. _memfault-firmware-sdk examples:
   https://github.com/memfault/memfault-firmware-sdk/tree/master/examples

.. _Memfault:
   https://memfault.com/
