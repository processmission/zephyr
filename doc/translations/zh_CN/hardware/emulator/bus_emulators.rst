.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bus_emul:

外部总线及总线连接外设的仿真器
##############################

概述
====

Zephyr 支持一个简单的仿真器框架，可在无需真实硬件的情况下测试外部外设驱动。

仿真器用于仿真外部硬件设备，以支持对各种子系统的测试。例如，可以为 I2C 罗盘编写仿真器，使其出现在 I2C 总线上，并像真实硬件设备一样使用。

仿真器通常会实现用于测试的特殊功能。例如，罗盘可以在 I2C 总线速度过高时返回错误数据，或在校准尚未完成时返回无效测量值。这样就能测试高层代码是否能够正确处理这些情况。因此，如果仿真了所有故障条件，测试覆盖率就可以接近 100%。

概念
====

下图顶部展示了应用代码和高层测试。这就是我们最终想要运行的应用。

.. figure:: img/arch.svg
   :align: center
   :alt: 展示测试、仿真器和驱动的仿真器架构

其下方是外设驱动，例如 AT24 EEPROM 驱动。我们可以使用通过总线控制器仿真器连接的外设仿真器来测试外设驱动。例如，总线控制器仿真器会将 I2C 通信从 AT24 驱动（外设驱动）传递到 AT24 仿真器（外设仿真器）。

另外，我们可以使用 API 测试，在真实硬件上测试 STM32 和 NXP 的 I2C 驱动。这些测试需要在总线上连接某种外设设备，有了这些设备，我们就可以验证驱动的大部分功能。

将这两种方式结合起来，我们就可以完全在 native_sim 上测试应用和外设代码。既然已经确认真实硬件上的 I2C 驱动能够正常工作，就可以预期应用和外设驱动也能在真实硬件上正常工作。

使用上述框架，为所有片外设备驱动配备仿真器后，我们就可以在 native_sim 上测试整个应用（例如嵌入式控制器）。

采用这种方法，我们可以：

* 为每个驱动（绿色部分）编写独立的测试，覆盖所有故障模式、错误条件等。

* 确保驱动（绿色部分）的测试覆盖率达到 100%

* 为驱动组合编写测试，例如通过 I2C 总线通信的 I2C GPIO 扩展器驱动所提供的 GPIO，这些 GPIO 又用于控制充电器。所有这些都可以在仿真环境或真实硬件上运行。

* 编写一个将所有这些部分整合起来并在 native_sim 上运行的复杂应用。我们可以在主机上开发，进行源码级调试等。

* 通过添加 Kconfig 和 Devicetree 片段，将应用移植到任何具备所需功能（例如 I2C、足够数量的 GPIO）的开发板上。

创建设备驱动仿真器
==================

仿真器子系统以 :ref:`device_model_api` 为模型。可以使用 :c:func:`EMUL_DT_DEFINE()` 或 :c:func:`EMUL_DT_INST_DEFINE()` API 创建仿真器实例。

外设设备的仿真器与真实设备驱动复用同一个 Devicetree 节点。这意味着仿真器在定义 ``DT_DRV_COMPAT`` 时，使用的 ``compat`` 值与真实驱动相同。

.. code-block:: C

  /* From drivers/sensor/bm160/bm160.c */
  #define DT_DRV_COMPAT bosch_bmi160

  /* From drivers/sensor/bmi160/emul_bmi160.c */
  #define DT_DRV_COMPAT bosch_bmi160

``EMUL_DT_DEFINE()`` 函数接受两种 API 类型：

  #. ``bus_api`` - 指向仿真器所连接的上游总线的 API。 ``bus_api`` 参数为必填项。支持的仿真总线类型包括 I2C、SPI、eSPI 和 MSPI。
  #. ``_backend_api`` - 指向仿真器所属设备类别专用的后端 API。 ``_backend_api`` 参数为可选项。

下图以 BC1.2 充电检测器驱动作为设备类别示例，展示了 ``bus_api`` 和 ``_backend_api`` 的逻辑组织方式。

.. figure:: img/device_class_emulator.svg
   :align: center
   :alt: 以 BC1.2 充电检测器演示的设备类别示例。

真实代码以绿色显示，仿真器代码以黄色显示。

``bus_api`` 将 BC1.2 仿真器连接到 ``native_sim`` I2C 控制器。真实的 BC1.2 驱动无需更改，其运行方式与系统中存在物理 I2C 控制器时完全相同。 ``native_sim`` I2C 控制器使用 ``bus_api`` 向仿真器发起寄存器读写操作。

``_backend_api`` 提供了一种机制，让测试能够通过带外方式操纵仿真器。每个设备类别都定义了自己的 API 函数。后端 API 函数专注于高层行为，不提供针对特定仿真器的钩子。

对于 BC1.2 充电检测器，后端 API 提供了用于模拟充电器连接到仿真 BC1.2 设备以及从该设备断开的函数。每个仿真器负责更新相应的厂商专用寄存器，并可能触发中断。

测试流程示例：

  #. 测试使用 Zephyr BC1.2 驱动 API 注册 BC1.2 检测回调。
  #. 测试使用 BC1.2 仿真器后端连接充电器。
  #. 测试验证 B1.2 检测回调被调用时传入的充电器类型是否正确。
  #. 测试使用 BC1.2 仿真器后端断开充电器连接。

采用这种架构，同一测试可用于同一驱动类别中所有受支持的驱动。

可用的仿真器
============

Zephyr 包含以下仿真器：

* I2C 仿真器驱动，允许将驱动连接到仿真器，以便在无法访问真实硬件的情况下执行测试

* SPI 仿真器驱动，为 SPI 提供相同的功能

* eSPI 仿真器驱动，为 eSPI 提供相同的功能。该仿真器正在开发中，以支持更多功能。

* MSPI 仿真器驱动，允许将驱动连接到仿真器，以便在无法访问真实硬件的情况下执行测试。

I2C 仿真功能
------------

I2C 仿真总线的绑定中有一个用于基于地址转发的自定义属性。以下面的 Devicetree 节点为例：

.. code-block:: devicetree

   i2c0: i2c@100 {
     status = "okay";
     compatible = "zephyr,i2c-emul-controller";
     clock-frequency = <I2C_BITRATE_STANDARD>;
     #address-cells = <1>;
     #size-cells = <0>;
     #forward-cells = <1>;
     reg = <0x100 4>;
     forwards = <&i2c1 0x20>;
   };

最后一个属性 ``forwards`` 表示，发送到地址 ``0x20`` 的所有读写请求都应转发到 ``i2c1`` 的相同地址。这使我们能够在同一映像中测试通信的控制器端和目标端。

.. note::
   ``#forward-cells`` 属性应始终为 1。``forwards`` 属性中的每个条目都由 phandle 及其后面的地址组成。在上面的示例中，``<&i2c1 0x20>`` 会将对 ``i2c0`` 的 ``0x20`` 端口执行的所有读写操作转发到 ``i2c1`` 的相同端口。由于仿真控制器不使用额外的单元，单元数量应保持为 1。

示例
====

以下是 Zephyr 中的一些示例：

#. Bosch BMI160 传感器驱动通过 I2C 和 SPI 两种方式连接到仿真器：

   .. zephyr-app-commands::
      :zephyr-app: tests/drivers/sensor/bmi160
      :board: native_sim
      :goals: build

#. 同一测试也可以使用第二种 EEPROM 来构建，即通过 I2C 连接到仿真器的 Atmel AT24 EEPROM 驱动：

   .. zephyr-app-commands::
      :zephyr-app: tests/drivers/eeprom/api
      :board: native_sim
      :goals: build
      :gen-args: -DDTC_OVERLAY_FILE=at2x_emul.overlay -DEXTRA_CONF_FILE=at2x_emul.conf

API 参考
========

.. doxygengroup:: io_emulators
