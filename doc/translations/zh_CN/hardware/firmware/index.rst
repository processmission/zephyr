.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

固件
####

概述
****

此类驱动程序支持与提供各种服务（例如时钟管理、电源管理、pinctrl 等）的固件交互。Zephyr 目前支持的固件列表汇总如下：

.. list-table::
   :align: center

   * - 名称
     - 供应商
     - 描述
     - 文档

   * - SCMI
     - ARM
     - 系统控制与管理接口
     - `Link <https://developer.arm.com/documentation/den0056/latest/>`__

   * - TISCI
     - TI
     - TI 系统控制器接口
     - `Link <https://software-dl.ti.com/tisci/esd/latest/index.html>`__

   * - QEMU FWCFG
     - QEMU
     - QEMU 固件配置
     - `Link <https://www.qemu.org/docs/master/specs/fw_cfg.html>`__

   * - RPI FIRMWARE
     - Raspberry Pi
     - Raspberry Pi VideoCore 固件接口
     - `Link <https://github.com/raspberrypi/firmware/wiki>`__

API 参考
********

固件驱动程序通常用于为其他类别的驱动程序提供功能。此外，不同固件的用途和功能可能有所不同。因此，此类驱动程序未实现供最终用户使用的标准 API。

示例
****

请参阅 :zephyr:code-sample-category:`firmware` 。

资源
****

.. toctree::
   :maxdepth: 1

   arm-scmi
