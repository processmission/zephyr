.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _rtc_api:

实时时钟（RTC）
###############

概述
****

.. list-table:: **术语表**
    :widths: 30 80
    :header-rows: 1

    * - 术语
      - 定义
    * - 实时时钟
      - 使用分解时间（年、月、日、时、分、秒等字段）跟踪时间的低功耗设备
    * - 实时计数器
      - 可用于跟踪时间的低功耗计数器
    * - RTC
      - 实时时钟的英文缩写

RTC 是一种使用分解时间（年、月、日、时、分、秒等字段）跟踪时间的低功耗设备。不应将其与低功耗计数器混淆，后者有时具有相同的名称、缩写或两者兼有。

RTC 通常针对低能耗进行优化，即使系统处于低功耗状态，也通常保持运行。

RTC 通常包含一个或多个闹钟，可配置为在指定时间触发。这些闹钟通常用于将系统从低功耗状态唤醒。

Devicetree 绑定
***************

RTC 绑定必须包含 ``rtc-device.yaml`` 绑定，该绑定包含 ``base.yaml`` 绑定和必需的 ``alarms-count`` 属性。

.. code-block:: yaml

   include: rtc-device.yaml

设备驱动设计
************

驱动初始化
==========

系统从不关闭 RTC 的电源。初始化时，驱动应预期 RTC 处于以下任一状态：

* 已供电、已配置且正在运行。
* 已供电、未配置且已停止。

初始化时，驱动必须确保 RTC 配置正确，同时保留时间、闹钟和运行状态。

通过调用 :c:func:`rtc_set_time` 设置时间，RTC 将在此时开始运行。闹钟的待处理状态由 :c:func:`rtc_alarm_is_pending` 清除，或由通过 :c:func:`rtc_alarm_set_callback` 设置的闹钟回调清除。

通过 GPIO 路由的中断
====================

对于已连接中断输出引脚的 RTC，必须在初始化时配置并启用这些引脚。主机可以启用和禁用其 GPIO 的中断，但 RTC 中断输出引脚必须保持启用。

这可确保内部连接和外部连接的 RTC 行为一致，并允许任何已启用的 RTC 事件（如闹钟或更新）通过 GPIO 唤醒系统。

.. note::

   对于未连接中断输出引脚的 RTC，不允许通过定期轮询 RTC 来模拟引脚已连接的行为。在这种情况下，:c:func:`rtc_alarm_set_callback` 和 :c:func:`rtc_update_set_callback` 必须返回 ``-ENOTSUP`` 。

时钟输出
========

如果支持时钟输出，其配置在 Devicetree 中定义。驱动在初始化时配置该输出。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_RTC`
* :kconfig:option:`CONFIG_RTC_ALARM`
* :kconfig:option:`CONFIG_RTC_UPDATE`
* :kconfig:option:`CONFIG_RTC_CALIBRATION`

API 参考
********

.. doxygengroup:: rtc_interface

.. doxygengroup:: rtc_fake

RTC 设备驱动程序测试套件
************************

此测试套件验证 RTC 设备驱动程序的行为，其设计支持在不同开发板之间移植。它使用 Devicetree 别名 ``rtc`` 指定要测试的 RTC 设备。

此测试套件测试以下内容：

* 设置和获取时间。
* RTC 时间是否正确递增。
* 在硬件支持的情况下，测试启用和禁用回调时的闹钟功能。
* 在硬件支持的情况下，测试校准功能。

校准测试会测试一系列数值，并将其打印到控制台以供手动比较。用户必须检查设置的值和获取的值，确保它们有效。

默认情况下，仅启用对必需的时间设置和获取功能的测试。要测试可选的闹钟、更新事件回调和时钟校准功能，必须通过选择 :kconfig:option:`CONFIG_RTC_ALARM` 、 :kconfig:option:`CONFIG_RTC_UPDATE` 和 :kconfig:option:`CONFIG_RTC_CALIBRATION` 来启用这些功能。

以下示例为 ``native_sim`` 开发板构建测试套件。要为其他开发板构建测试套件，请将 ``native_sim`` 开发板替换为你的开发板。

要使用默认配置构建测试应用，仅测试必需功能，可参考以下命令：

.. zephyr-app-commands::
   :tool: west
   :host-os: unix
   :board: native_sim
   :zephyr-app: tests/drivers/rtc/rtc_api
   :goals: build

要构建启用其他 RTC 功能的测试，请使用 menuconfig 更新配置以启用这些功能。可参考以下命令：

.. zephyr-app-commands::
   :tool: west
   :host-os: unix
   :board: native_sim
   :zephyr-app: tests/drivers/rtc/rtc_api
   :goals: menuconfig

然后使用以下命令构建测试应用：

.. zephyr-app-commands::
   :tool: west
   :host-os: unix
   :board: native_sim
   :zephyr-app: tests/drivers/rtc/rtc_api
   :maybe-skip-config:
   :goals: build

要运行测试套件，请将应用烧录到开发板并运行，输出将打印到控制台。

.. note::

    测试真实硬件时，每项测试最多需要 30 秒。

.. _rtc_api_emul_dev:

RTC 仿真设备
************

RTC 仿真设备完整实现了 RTC API，其行为与真实 RTC 设备相同，但有以下限制：

* RTC 时间无法跨应用初始化保留。
* RTC 闹钟无法跨应用初始化保留。
* RTC 时间会随时间推移发生漂移。

每次应用初始化时，RTC 的时间和闹钟都会重置。在使用 :c:func:`rtc_set_time` 设置时间之前，使用 :c:func:`rtc_get_time` 读取时间将返回 ``-ENODATA`` 。设置时间后，RTC 的行为将与真实 RTC 相同，直到应用被重置。

RTC 仿真设备驱动程序针对 compatible 为 :dtcompatible:`zephyr,rtc-emul` 的设备构建，选择 :kconfig:option:`CONFIG_RTC` 后便会将其包含在构建中。

Zephyr 中 RTC 的历史
********************

在此 API 创建之前，Zephyr 已通过 :ref:`counter_api` API 支持 RTC。RTC 驱动程序内部使用分解时间表示形式，并通过 Unix 时间戳在分解时间与 Unix 时间戳之间进行转换。

这种方法的缺点是：硬件计数器无法设置为特定计数值，因此所有 RTC 都需要使用设备专用 API 来设置时间；需要将 Unix 时间转换为分解时间，而这种转换在某些情况下并无必要；还缺少一些常用功能，例如输入时钟校准和更新回调。
