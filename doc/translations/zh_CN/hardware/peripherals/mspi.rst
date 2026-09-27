.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mspi_api:

多位 SPI 总线
#############

MSPI（多位 SPI）以通用 API 的形式提供，用于支持高级 SPI 外设和设备。这些外设和设备通常需要命令、地址和数据阶段，并在这些阶段使用多条信号线。该 API 支持 :term:`XIP` 和加扰等高级功能，同时也兼容通用 SPI。

.. contents::
    :local:
    :depth: 2

.. _mspi-controller-api:

MSPI 控制器 API
***************

当系统中存在多位 SPI 控制器时，可以使用 Zephyr 的 MSPI 控制器 API，例如 Ambiq MSPI、QSPI、OSPI、Flexspi 等。该 API 支持单线至十六线 SDR/DDR IO、可变延迟，以及 :term:`XIP` 和加扰等高级功能。适用设备包括但不限于高速、高密度闪存/PSRAM 存储设备、显示器和传感器。

MSPI 接口包含针对特定 SoC 平台并实现 MSPI API 的控制器驱动，以及调用这些 API 的设备驱动。控制器驱动与设备驱动之间是多对多关系，便于在不同平台之间切换。

以下是在设备驱动初始化函数中初始化 MSPI 控制器和 MSPI 总线的通用步骤：

#. 初始化 MSPI 控制器驱动实例的数据结构。可以使用 :c:macro:`DEVICE_DT_INST_DEFINE` 等常用的设备定义宏，并将初始化函数、配置和数据作为参数传递给该宏。

#. 初始化硬件，包括但不限于：

   * 根据硬件自身的能力检查 :c:struct:`mspi_cfg` ，防止错误使用。

   * 设置默认引脚复用。

   * 设置控制器时钟。

   * 为硬件上电。

   * 使用 :c:struct:`mspi_cfg` 以及可能需要的其他平台特定设置来配置硬件。

   * 通常， :c:struct:`mspi_cfg` 根据 Devicetree 填充，包含启动时使用的静态参数。不过，如果需要，可以在运行时使用 :c:func:`mspi_config` 以新参数重新初始化硬件。

   * 如有持有的锁，释放这些锁。

#. 执行设备驱动初始化。与通常的做法一样，可以使用 :c:macro:`DEVICE_DT_INST_DEFINE` 。在设备驱动初始化函数中，执行以下必要步骤。

   #. 使用从设备数据手册中获取的设备特定硬件设置调用 :c:func:`mspi_dev_config` 。

      * :c:struct:`mspi_dev_cfg` 应根据 Devicetree 填充，可以使用辅助宏 :c:macro:`MSPI_DEVICE_CONFIG_DT` 。

      * 随后，控制器驱动应验证 :c:struct:`mspi_dev_cfg` 的成员，防止错误使用。

      * 控制器驱动应实现互斥锁，防止意外访问。

      * 控制器驱动还可以根据 :c:struct:`mspi_dev_id` 在不同设备之间切换。

   #. 如果硬件支持，调用 API 进行额外设置

      * :c:func:`mspi_memmap_config` 用于内存映射访问（例如 :term:`XIP` ）

      * :c:func:`mspi_scramble_config` 用于加扰功能

      * :c:func:`mspi_timing_config` 用于平台特定的时序设置。

   #. 如有需要，使用 :c:func:`mspi_register_callback` 注册回调。

   #. 释放控制器互斥锁。

收发
====
收发请求的类型为 :c:struct:`mspi_xfer` 。通过 :c:func:`mspi_dev_config` 确定并配置工作模式后，可以使用该类型动态更改传输相关设置。

该 API 还支持通过 :c:struct:`mspi_xfer_packet` 进行起始地址和大小各不相同的批量传输。不过，是否支持分散 IO 和回调管理取决于控制器的实现。如果已使用 :c:func:`mspi_register_callback` 注册回调，控制器可以在每次异步或同步传输完成后，根据 :c:enum:`mspi_bus_event_cb_mask` 确定要触发的用户回调。也可以使用 :c:enum:`MSPI_BUS_NO_CB` ，即使已注册回调，也不触发任何回调。如果驱动实现支持，该 API 可以通过 :c:enum:`MSPI_BUS_XFER_COMPLETE_CB` 通知传输完成，并通过 :c:enum:`MSPI_BUS_TIMEOUT_CB` 通知传输或请求超时。如果控制器支持硬件命令队列，且驱动实现支持分散 IO 和回调管理，用户就可以充分发挥硬件性能。

设备树
======

下面是在 Devicetree 中定义 MSPI 控制器的示例：MSPI 控制器的绑定应引用 mspi-controller.yaml 作为基础绑定之一。

.. code-block:: devicetree

   mspi0: mspi@400 {
            status = "okay";
            compatible = "zephyr,mspi-emul-controller";

            reg = <0x400 0x4>;
            #address-cells = <0x1>;
            #size-cells = <0x0>;

            clock-frequency = <0x17d7840>;
            op-mode = "MSPI_CONTROLLER";
            duplex = "MSPI_HALF_DUPLEX";
            ce-gpios = <&gpio0 0x5 0x1>, <&gpio0 0x12 0x1>;
            dqs-support;

            pinctrl-0 = <&pinmux-mspi0>;
            pinctrl-names = "default";
   };

下面是在 Devicetree 中定义 MSPI 设备的示例：MSPI 设备的绑定应引用 mspi-device.yaml 作为基础绑定之一。

.. code-block:: devicetree

   &mspi0 {

            mspi_dev0: mspi_dev0@0 {
                     status = "okay";
                     compatible = "zephyr,mspi-emul-device";

                     reg = <0x0>;
                     size = <0x10000>;

                     mspi-max-frequency = <0x2dc6c00>;
                     mspi-io-mode = "MSPI_IO_MODE_QUAD";
                     mspi-data-rate = "MSPI_DATA_RATE_SINGLE";
                     mspi-hardware-ce-num = <0x0>;
                     read-instruction = <0xb>;
                     write-instruction = <0x2>;
                     instruction-length = "INSTR_1_BYTE";
                     address-length = "ADDR_4_BYTE";
                     rx-dummy = <0x8>;
                     tx-dummy = <0x0>;
                     memmap-config = <0x0 0x0 0x0 0x0>;
                     ce-break-config = <0x0 0x0>;
            };

   };

用户应在 DTS 中指定目标运行参数，例如 ``mspi-max-frequency`` 、 ``mspi-io-mode`` 和 ``mspi-data-rate`` ，即使这些参数可能在运行时发生变化。这些参数应反映设备正常运行时的典型配置。

多外设
======
:c:struct:`mspi_dev_id` 定义为 Devicetree 中的设备索引与 CE GPIO 的组合，因此该 API 支持在同一个控制器实例上连接多个设备。控制器驱动的实现可能支持设备切换，也可能不支持；设备切换可以由软件或硬件执行。如果由软件处理切换，则应在调用 :c:func:`mspi_dev_config` 时执行。

设备驱动应通过保存和更新 :c:struct:`mspi_dev_cfg` 以及其他相关的 mspi 结构体或私有数据结构，记录设备当前的运行条件，以支持由软件控制的设备切换。特别是，每次 API 调用都需要使用包含设备标识的 :c:struct:`mspi_dev_id` 。


配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_MSPI`
* :kconfig:option:`CONFIG_MSPI_ASYNC`
* :kconfig:option:`CONFIG_MSPI_PERIPHERAL`
* :kconfig:option:`CONFIG_MSPI_MEMMAP`
* :kconfig:option:`CONFIG_MSPI_SCRAMBLE`
* :kconfig:option:`CONFIG_MSPI_TIMING`
* :kconfig:option:`CONFIG_MSPI_INIT_PRIORITY`
* :kconfig:option:`CONFIG_MSPI_COMPLETION_TIMEOUT_TOLERANCE`
* :kconfig:option:`CONFIG_MSPI_DMA`

API 参考
********

.. doxygengroup:: mspi_interface
