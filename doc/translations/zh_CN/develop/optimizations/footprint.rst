.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _footprint:

优化内存占用
############

栈大小
******

各系统线程的栈大小留有较大余量，以适应尽可能多的受支持平台上的不同场景。优化时应先检查所有栈大小，并根据应用进行调整：

:kconfig:option:`CONFIG_ISR_STACK_SIZE`
  默认设为 2048

:kconfig:option:`CONFIG_MAIN_STACK_SIZE`
  默认设为 1024

:kconfig:option:`CONFIG_IDLE_STACK_SIZE`
  默认设为 320

:kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`
  默认设为 1024

:kconfig:option:`CONFIG_PRIVILEGED_STACK_SIZE`
  默认设为 1024，取决于用户空间功能。


未使用的外设
************

某些外设默认启用。可以在项目配置中禁用未使用的外设，例如::


        CONFIG_GPIO=n
        CONFIG_SPI=n

各类调试和信息选项
******************

以下选项输出运行中应用的更多信息，并提供调试和错误处理手段：

:kconfig:option:`CONFIG_BOOT_BANNER`
  可以禁用此选项以节省一些字节。

:kconfig:option:`CONFIG_DEBUG`
  调试构建可以启用此选项。

注意，启动横幅默认启用。


MPU/MMU 支持
************

根据应用和平台需求，可以禁用 MPU/MMU 支持以节省内存并提高性能。但应考虑此配置选择的后果，因为这样会失去高级栈检查及相关支持。
