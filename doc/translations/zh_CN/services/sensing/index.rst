.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _sensing:

感知子系统
##########

.. contents::
    :local:
    :depth: 2

概述
****

感知子系统是 OS 用户空间服务层中的一个高层传感器框架。该框架专注于传感器融合、客户端仲裁、采样、定时、调度以及基于传感器的电源管理。

感知子系统中的关键概念包括物理传感器和虚拟传感器对象，以及建立在传感器对象关系之上的调度框架。物理传感器不依赖任何其他传感器对象作为输入，而是直接与现有的 Zephyr 传感器设备驱动交互。虚拟传感器则依赖其他传感器对象（物理或虚拟）作为上报输入。

感知子系统依赖 Zephyr 传感器设备 API（现有版本或将来更新的版本），以复用 Zephyr 庞大的传感器设备驱动库（100 多个）。

使用感知子系统是可选的。只需要访问简单传感器设备的应用可以直接使用 Zephyr :ref:`sensor` API。

由于感知子系统与设备驱动层或内核空间分离，并且可以通过虚拟传感器概念在用户空间支持各种定制和传感器算法，现有的传感器设备驱动可以专注于底层设备侧的工作，尽可能保持简单，只提供设备硬件抽象和操作等。这非常有利于系统稳定性。

感知子系统与任何传感器公开或传输协议解耦，目标是支持采用不同传感器公开或传输协议的各种上层框架和应用，例如 `CHRE <https://github.com/zephyrproject-rtos/chre>`_、HID 传感器应用、MQTT 传感器应用，以满足不同产品的需求。凭借其多客户端支持设计，它甚至可以同时支持采用不同上层传感器协议的多个应用。

感知子系统可以帮助构建统一的 Zephyr 感知架构，以支持跨主机操作系统，并适用于 IoT 传感器解决方案。

下图说明感知子系统如何与上层框架集成。

.. image:: images/sensing_solution.png
   :align: center
   :alt: 统一的 Zephyr 感知架构。

可配置性
********

* 可复用、可配置的独立子系统。
* 基于 Zephyr 现有底层传感器 API（复用 100 多个现有传感器设备驱动）
* 为应用提供 Zephyr 高层感知子系统 API。
* 独立的可选 CHRE Sensor PAL 实现模块，用于支持 CHRE。
* 与任何主机链路协议解耦，由 Zephyr 应用负责处理不同协议（MQTT、HID 或私有协议，均可配置）

主要特性
********

范围
  专注于传感器融合、多客户端、仲裁、数据采样、定时管理和调度的框架。

传感器抽象
  * **物理传感器**：与 Zephyr 传感器设备驱动交互，专注于数据采集。
  * **虚拟传感器**：依赖其他传感器（**物理** 或 **虚拟**），专注于数据融合。

数据驱动模型
  * **轮询模式**：周期性采样率
  * **中断模式**：数据就绪、阈值中断等。

调度
  为所有传感器对象的采样和处理使用单线程主循环。

用于批量处理的缓冲模式
  ..

可通过 Devicetree 配置
  ..


下图展示了 API 的位置和范围：

.. image:: images/sensing_api_org.png
   :align: center
   :alt: 感知子系统 API 组织。

``Sensing Subsystem API`` 面向应用。``Sensing Sensor API`` 面向 ``sensors`` 开发。


主要流程
********

* 传感器配置流程

.. image:: images/sensor_config_flow.png
   :align: center
   :alt: 传感器配置流程（应用为铰链角度传感器设置上报周期的示例）。

* 传感器数据流程

.. image:: images/sensor_data_flow.png
   :align: center
   :alt: 传感器数据流程（应用通过数据事件回调接收铰链角度数据的示例）。

传感器类型与实例
****************

``Sensing Subsystem`` 支持同一传感器类型的多个实例，应用可以通过两种方法识别并打开唯一的传感器实例：

* 枚举所有传感器实例

  :c:func:`sensing_get_sensors` 以 :c:struct:`sensing_sensor_info` 指针数组的形式返回当前开发板配置所支持的所有传感器实例的信息。

  随后应用可以使用 :c:func:`sensing_open_sensor` 打开特定的传感器实例，以便后续访问、配置和接收传感器数据等。

  这种方法适合支持 ``CHRE``、``HID`` 等需要动态枚举底层平台传感器实例的上层框架。

* 直接通过 devicetree 节点打开传感器实例

  应用可以使用 :c:func:`sensing_open_sensor_by_dt`，直接通过传感器 devicetree 节点标识符打开传感器实例。

  例如：

.. code-block:: c

   sensing_open_sensor_by_dt(DEVICE_DT_GET(DT_NODELABEL(base_accel)), cb_list, handle);
   sensing_open_sensor_by_dt(DEVICE_DT_GET(DT_CHOSEN(zephyr_sensing_base_accel)), cb_list, handle);

对于只想访问特定传感器的简单应用，这种方法简单易用。


``Sensor type`` 遵循 `HID standard sensor types definition <https://usb.org/sites/default/files/hutrr39b_0.pdf>`_。

:zephyr_file:`include/zephyr/sensing/sensing_sensor_types.h`

传感器实例句柄
**************

客户端使用 :c:type:`sensing_sensor_handle_t` 类型的句柄来处理已打开的传感器实例，此后对该传感器实例的所有操作都需要使用该句柄，例如设置配置、读取传感器采样数据等。

一个传感器实例可以有两种客户端：``Application clients`` 和 ``Sensor clients``。

``Application clients`` 可以使用 :c:func:`sensing_open_sensor` 打开传感器实例并获取其句柄。

对于 ``Sensor clients``，没有用于打开上报者的 open API，因为客户端与上报者的关系在传感器注册阶段就通过 devicetree 建立了。

``Sensing Subsystem`` 会自动为客户端传感器打开其上报者传感器并创建 ``handlers``。``Sensor clients`` 可以通过 :c:func:`sensing_sensor_get_reporters` 获取其上报者的句柄。

.. image:: images/sensor_top.png
   :align: center
   :alt: 传感器上报拓扑。

.. note::
   对于感知子系统内部的传感器，它们之间的上报关系全部由感知子系统根据 devicetree 定义自动生成，客户端传感器与上报者传感器之间的句柄会自动创建。应用需要调用 :c:func:`sensing_open_sensor` 显式打开传感器实例。

传感器采样值
************

* 数据结构

  每个传感器采样值都定义为通用的 ``header`` + ``readings[]`` 数据结构，例如 :c:struct:`sensing_sensor_value_3d_q31`、:c:struct:`sensing_sensor_value_q31` 和 :c:struct:`sensing_sensor_value_uint32`。

  ``header`` 的定义见 :c:func:`sensing_sensor_value_header`。


* 时间戳

  感知子系统中的时间戳单位是 ``micro seconds``。

  ``header`` 中定义了 **base_timestamp**，而 **readings[]** 数组中的每个元素都定义了 **timestamp_delta**。

  **timestamp_delta** 相对于前一个 **readings** （或 **base_timestamp**）

  例如：

  * ``readings[0]`` 的时间戳为 ``header.base_timestamp`` + ``readings[0].timestamp_delta``。

  * ``readings[1]`` 的时间戳为 ``timestamp of readings[0]`` + ``readings[1].timestamp_delta``。

  由于时间戳单位是微秒，**timestamp_delta** （``uint32_t``）的最大值为 ``4295`` 秒。

  如果传感器的批量数据中相邻两次读数相差超过 ``4295`` 秒，感知子系统运行时会把它们拆分到多个 readings 结构实例中，并发送多个事件。

  此概念参考自 `CHRE Sensor API <https://github.com/zephyrproject-rtos/ chre/blob/zephyr/chre_api/include/chre_api/chre/sensor_types.h>`_。

* 数据格式

  ``Sensing Subsystem`` 使用按传感器类型定义的数据格式结构，并支持 :zephyr_file:`include/zephyr/dsp/types.h` 中为 ``zdsp`` 库支持而定义的 ``Q Format``。

  例如，:c:struct:`sensing_sensor_value_3d_q31` 可供 :c:macro:`SENSING_SENSOR_TYPE_MOTION_ACCELEROMETER_3D`、:c:macro:`SENSING_SENSOR_TYPE_MOTION_UNCALIB_ACCELEROMETER_3D` 和 :c:macro:`SENSING_SENSOR_TYPE_MOTION_GYROMETER_3D` 等 3D IMU 传感器使用。

  :c:struct:`sensing_sensor_value_uint32` 可供 :c:macro:`SENSING_SENSOR_TYPE_LIGHT_AMBIENTLIGHT` 传感器使用，

  而 :c:struct:`sensing_sensor_value_q31` 可供 :c:macro:`SENSING_SENSOR_TYPE_MOTION_HINGE_ANGLE` 传感器使用

  :zephyr_file:`include/zephyr/sensing/sensing_datatypes.h`


Devicetree 配置
***************

感知子系统使用 devicetree 配置所有传感器实例及其属性、上报关系。

示例见 :zephyr_file:`samples/subsys/sensing/simple/boards/native_sim.overlay`

API 参考
********

.. doxygengroup:: sensing_api
