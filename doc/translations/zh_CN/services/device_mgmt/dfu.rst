.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _dfu:

设备固件升级
############

概述
****

设备固件升级子系统提供必要的框架，用于在运行时升级基于 Zephyr 的应用程序映像。它目前由两个不同的模块组成：

* :zephyr_file:`subsys/dfu/boot/`：引导加载程序接口代码
* :zephyr_file:`subsys/dfu/img_util/`：映像管理代码

DFU 子系统负责映像管理，但不涉及将映像发送到目标设备所需的传输或管理协议本身。有关这些协议和框架的信息，请参阅 :ref:`device_mgmt` 一节。

.. _flash_img_api:

Flash 映像
==========

作为设备固件升级（DFU）子系统一部分的 Flash 映像 API 在 Flash Stream 之上提供了一层抽象，以简化将固件映像块写入 Flash 的操作。

API 参考
--------

.. doxygengroup:: flash_img_api

.. _mcuboot_api:

MCUBoot API
===========

提供 MCUboot API 用于获取应用程序映像的版本信息和启动状态。它允许为下一次启动选择应用程序映像和启动类型。

API Reference
-------------

.. doxygengroup:: mcuboot_api

引导加载程序
************

.. _mcuboot:

MCUboot
=======

Zephyr 直接兼容开源、跨 RTOS 的 `MCUboot boot loader`_。它与 MCUboot 对接，并了解其所需的映像格式，因此当 Zephyr 使用 MCUboot 作为引导加载程序时，即可使用设备固件升级。源代码本身托管在 `MCUboot GitHub Project`_ 页面上。

要将 MCUboot 与 Zephyr 一起使用，需要考虑以下事项：

1. 需要定义 MCUboot 所需的 Flash 分区；有关详细信息，请参阅 :ref:`flash_map_api`。
2. 必须将 Flash 分区指定为选定的代码分区

.. code-block:: devicetree

   / {
      chosen {
         zephyr,code-partition = &slot0_partition;
      };
   };

3. 应用程序的 :file:`.conf` 文件需要启用 :kconfig:option:`CONFIG_BOOTLOADER_MCUBOOT` Kconfig 选项，以便以兼容 MCUboot 的方式构建 Zephyr
4. 需要在设备上构建并烧录 MCUboot 本身
5. 可能需要采取预防措施，避免整片擦除 Flash，并将 Zephyr 应用程序映像烧录到正确偏移处（紧跟在引导加载程序之后）

有关将 MCUboot 与 Zephyr 一起使用的更详细信息，请参阅 MCUboot 网站上的 `MCUboot with Zephyr`_ 文档页面。

.. _MCUboot boot loader: https://mcuboot.com/
.. _MCUboot with Zephyr: https://docs.mcuboot.com/readme-zephyr
.. _MCUboot GitHub Project: https://github.com/runtimeco/mcuboot
