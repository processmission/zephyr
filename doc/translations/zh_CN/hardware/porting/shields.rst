.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _shields:

扩展板
######

扩展板也称为“附加板”或“子板”，连接到开发板上以扩展其功能和服务，让原型开发更简单、更模块化。在 Zephyr 中，扩展板功能提供符合 Zephyr 格式的扩展板描述，使扩展板更容易与应用兼容。

启用扩展板
**********

在 west 命令中添加相应的 ``--shield`` 参数，即可启用对一个或多个扩展板的支持：

  .. zephyr-app-commands::
     :app: your_app
     :board: your_board
     :shield: x_nucleo_idb05a1,x_nucleo_iks01a1
     :goals: build


也可以在项目的 CMakeLists.txt 中将其设为默认值：

.. code-block:: cmake

        set(SHIELD x_nucleo_iks01a1)

.. _shield-interfaces:

扩展板接口
**********

扩展板由两个关键特征定义：

#. **物理连接器** - 机械接口
#. **电气信号** - 每个引脚的实际功能

扩展板与开发板之间的连接通过 Devicetree 文件描述：

- 开发板侧：开发板的 Devicetree 文件使用 :ref:`GPIO 连接节点 <gpio-nexus-node>` 将连接器引脚映射到微控制器的实际 GPIO 引脚。该文件还为通过连接器引出的总线定义标签（例如 ``arduino_i2c`` 、 ``arduino_spi`` 、 ``arduino_uart`` ）。

- 扩展板侧：扩展板的 .overlay 文件引用这些相同的标签，以描述其组件如何连接到开发板。

构建时，开发板的 Devicetree 与扩展板的 overlay 合并，形成完整的硬件配置描述。

例如，假设你有一块带有 Arduino 连接器但没有内置加速度计的开发板。你可以通过 Arduino 扩展板添加加速度计：

#. 开发板的 Devicetree 定义了一个 ``arduino_i2c`` 标签：它表示 Arduino 连接器上引出的 I2C 总线

#. 加速度计扩展板的 overlay 文件也引用 ``arduino_i2c`` ，以表明它使用同一条 I2C 总线。如果需要使用连接器上的 GPIO 引脚，它会引用开发板 Devicetree 中定义的 GPIO 连接节点（例如 ``arduino_header`` ）。

随后，当你为这块开发板及其扩展板进行构建时，Zephyr 会自动将它们“连接”起来。

.. note::

   某些开发板和扩展板可能仅支持扩展板硬件接口的部分功能。有关更多详细信息，请参阅各自的文档。


Arduino MKR
-----------

这是 Arduino MKR 开发板的外形规格。

.. figure:: ../../../boards/arduino/mkrzero/doc/img/arduino_mkrzero.jpg
   :align: center
   :width: 200px
   :alt: Arduino MKR Zero

   Arduino MKR Zero，一款具有 Arduino MKR 扩展板接口的开发板

相关的 Devicetree 节点标签：

- ``arduino_mkr_header`` 有关 GPIO 引脚定义以及在 Devicetree 文件中使用时需要包含的文件的详细信息，请参阅 :dtcompatible:`arduino-mkr-header` 。
- ``arduino_mkr_i2c``
- ``arduino_mkr_spi``
- ``arduino_mkr_serial``


Arduino Nano
------------

这是 Arduino Nano 开发板的外形规格。

.. figure:: ../../../boards/arduino/nano_33_iot/doc/img/nano_33_iot.jpg
   :align: center
   :width: 300px
   :alt: Arduino Nano 33 IOT

   Arduino Nano 33 IOT，一款具有 Arduino Nano 扩展板接口的开发板示例

相关的 Devicetree 节点标签：

- ``arduino_nano_header`` 有关 GPIO 引脚定义以及在 Devicetree 文件中使用的包含文件的详细信息，请参阅 :dtcompatible:`arduino-nano-header` 。
- ``arduino_nano_i2c``
- ``arduino_nano_spi``
- ``arduino_nano_serial``


Arduino Uno R3
--------------

这是 Arduino Uno R3 开发板的外形规格。

.. figure:: ../../../boards/shields/mcp2515/doc/keyestudio_can_bus_ks0411.jpg
   :align: center
   :width: 300px
   :alt: Keyestudio CAN-BUS 扩展板（KS0411）

   Keyestudio CAN-BUS，一款 Arduino 扩展板示例（图片来源：Keyestudio）

相关的 Devicetree 节点标签：

- ``arduino_header`` 有关 GPIO 引脚定义以及在 Devicetree 文件中使用的包含文件的详细信息，请参阅 :dtcompatible:`arduino-header-r3` 。
- ``arduino_adc`` 请参阅 :dtcompatible:`arduino,uno-adc`
- ``arduino_pwm`` 请参阅 :dtcompatible:`arduino-header-pwm`
- ``arduino_serial``
- ``arduino_i2c``
- ``arduino_spi``

有关技术细节，请参阅 `Arduino Uno R3 pinout`_ 。


摄像头和显示器连接器
--------------------

这些连接器描述了摄像头和显示器的连接方式（严格来说，它们并非扩展板）。

- :dtcompatible:`arducam,dvp-20pin-connector`
- :dtcompatible:`nxp,cam-44pins-connector`
- :dtcompatible:`nxp,parallel-lcd-connector`
- :dtcompatible:`raspberrypi,csi-connector`
- :dtcompatible:`st,dsi-lcd-qsh-030-connector`
- :dtcompatible:`st,dvp-cam-zif-30-connector`
- :dtcompatible:`weact,dcmi-camera-connector`


ESP-01
------

这是用于 ESP-01 Wi-Fi 模块的 8 引脚排针接口。

相关的 Devicetree 节点标签：

- ``esp_01_header`` 有关 GPIO 引脚定义以及在 Devicetree 文件中使用的包含文件的详细信息，请参阅 :dtcompatible:`esp-01-header` 。
- ``esp_01_serial``


Feather
-------

这是 Adafruit Feather 系列开发板的外形规格。用于 Feather 开发板的扩展板称为 Featherwing。

.. figure:: ../../../boards/shields/adafruit_adalogger_featherwing/doc/adafruit_adalogger_featherwing.webp
   :align: center
   :width: 300px
   :alt: Adafruit Adalogger Featherwing 扩展板

   Adafruit Adalogger，一款 Featherwing 扩展板（图片来源：Adafruit）

相关的 Devicetree 节点标签：

- ``feather_header`` GPIO 引脚定义请参见 :dtcompatible:`adafruit-feather-header` 。
- ``feather_adc``
- ``feather_i2c``
- ``feather_serial``
- ``feather_spi``


Microbit
--------

此接口用于 Microbit 开发板的板边连接器。

.. figure::  ../../../boards/bbc/microbit_v2/doc/img/bbc_microbit2.jpg
   :align: center
   :width: 500px
   :alt: Microbit V2 开发板

   Microbit V2 开发板使用 Microbit 扩展板接口

GPIO 引脚定义和技术要求链接请参见 :dtcompatible:`microbit,edge-connector` 。


mikroBUS™
---------

这是由 Mikroe 开发的附加板接口标准。

.. figure:: ../../../boards/shields/mikroe_3d_hall_3_click/doc/images/mikroe_3d_hall_3_click.webp
   :align: center
   :alt: 3D Hall 3 Click
   :height: 300px

   3D Hall 3 Click，一款 mikroBUS™ 扩展板

相关的 Devicetree 节点标签：

- ``mikrobus_header`` GPIO 引脚定义和技术规范链接请参见 :dtcompatible:`mikro-bus` 。
- ``mikrobus_adc``
- ``mikrobus_i2c``
- ``mikrobus_pwm``
- ``mikrobus_spi``
- ``mikrobus_serial``

请注意，具有多个 mikroBUS™ 连接器的开发板可能会定义诸如 ``mikrobus_2_spi`` 这样的标签。


Pico
----

这是 Raspberry Pi Pico 开发板的外形规格。

.. figure::  ../../../boards/shields/waveshare_ups/doc/waveshare_pico_ups_b.jpg
   :align: center
   :width: 300px
   :alt: Waveshare Pico UPS-B 扩展板

   Waveshare Pico UPS-B，一款 Pico 扩展板

相关的 Devicetree 节点标签：

- ``pico_header`` GPIO 引脚定义请参见 :dtcompatible:`raspberrypi,pico-header` 。
- ``pico_i2c`` 一个节点标签，与节点标签 ``pico_i2c0`` 或 ``pico_i2c1`` 指向同一节点。它引用应优先使用或默认使用的节点。
- ``pico_i2c0``
- ``pico_i2c1``
- ``pico_serial``
- ``pico_spi``


ST Morpho
---------

意法半导体的开发板通常使用 ST Morpho 扩展板接口。

.. figure:: ../../../boards/shields/x_nucleo_gfx01m2/doc/x_nucleo_gfx01m2.webp
   :align: center
   :width: 300px
   :alt: X-NUCLEO-GFX01M2

   X-NUCLEO-GFX01M2，一款 ST Morpho 扩展板

相关的 Devicetree 节点标签：

- ``st_morpho_header`` 有关 GPIO 引脚定义以及可在 Devicetree 文件中使用的包含文件的详细信息，请参阅 :dtcompatible:`st-morpho-header` 。
- ``st_morpho_lcd_spi``
- ``st_morpho_flash_spi``


ST Zio
------

意法半导体的 STM32 Nucleo-144 开发板提供 ST Zio 连接器，它是 Arduino Uno V3 连接器的扩展，通过四个排针（CN7、CN8、CN9 和 CN10）引出更多 STM32 I/O。

相关的 Devicetree 节点标签：

- ``st_zio_header`` 有关 GPIO 引脚定义以及可在 Devicetree 文件中使用的包含文件的详细信息，请参阅 :dtcompatible:`st-zio-header` 。


STMod+
------

这是部分意法半导体 Discovery 开发板和评估开发板上配备的 20 引脚扩展连接器。

相关的 Devicetree 节点标签：

- ``stmod_plus_connector`` 有关 GPIO 引脚定义以及可在 Devicetree 文件中使用的包含文件的详细信息，请参阅 :dtcompatible:`st,stmod-plus-connector` 。
- ``stmod_adc``
- ``stmod_i2c``
- ``stmod_pwm``
- ``stmod_serial``
- ``stmod_spi``

当外设连接到 STMod+ 连接器并在开发板的 Devicetree 中启用时，开发板可能会提供额外的接口标签。


Xiao
----

这是 Seeeduino XIAO 开发板的外形规格。

.. figure:: ../../../boards/shields/seeed_xiao_expansion_board/doc/img/seeed_xiao_expansion_board.webp
     :align: center
     :width: 300px
     :alt: Seeed Studio XIAO 扩展板

     Seeed Studio XIAO 扩展板，一款 Xiao 扩展板（图片来源：Seeed Studio）

相关的 Devicetree 节点标签：

- ``xiao_d`` 有关 GPIO 引脚定义，请参阅 :dtcompatible:`seeed,xiao-gpio` 。
- ``xiao_spi``
- ``xiao_i2c``
- ``xiao_serial``
- ``xiao_adc``
- ``xiao_dac``


zephyr_i2c / Stemma QT / Quiic
------------------------------

这些是四引脚 I2C 连接器。SparkFun 将这些连接器称为“Qwiic”，Adafruit 则将其称为“Stemma QT”。I2C 连接器有四个引脚：GND、+3.3 伏、I2C 数据和 I2C 时钟。最常见的物理连接器是引脚间距为 1.0 mm 的 JST-SH。

由于品牌名称不同，该接口统一标记为“zephyr_i2c”。

.. figure::  ../../../boards/shields/adafruit_vcnl4040/doc/adafruit_vcnl4040.webp
   :align: center
   :width: 200px
   :alt: Adafruit VCNL4040 扩展板

   Adafruit VCNL4040，一款 zephyr_i2c 扩展板（图片来源：Adafruit）

有关说明和更多详细信息的链接，请参阅 :dtcompatible:`stemma-qt-connector` 和 :dtcompatible:`grove-header` 。

相关的 Devicetree 节点标签：

- ``zephyr_i2c``

ST M.2 串行存储器连接器
-----------------------

部分 STMicroelectronics Nucleo-144 开发板提供 ST 专用的 M.2 串行存储器连接器，用于通过 XSPI 连接外部串行存储器，同时提供 I2C 和连接器 GPIO 等辅助信号。

.. figure:: ../../../boards/shields/st_b_m2mem_pack1/doc/b_m2mem_pack1.webp
   :align: center
   :width: 300px
   :alt: B-M2MEM-PACK1

   B-M2MEM-PACK1，一款 ST M.2 存储器扩展板。

相关的 Devicetree 节点标签：

- ``m2mem_connector``  有关 GPIO 引脚定义以及在 Devicetree 文件中使用的包含文件的详细信息，请参阅 :dtcompatible:`st,m2-memory-connector` 。
- ``m2mem_i2c``
- ``m2mem_xspi``

.. _shield_porting_guide:

扩展板移植与配置
****************

扩展板配置文件位于 :zephyr_file:`boards/shields` 下的开发板目录中：

.. code-block:: none

   boards/shields/<shield>
   ├── shield.yml
   ├── <shield>.overlay
   ├── Kconfig.shield
   ├── Kconfig.defconfig
   └── pre_dt_shield.cmake

这些文件提供的扩展板配置如下：

* **shield.yml** ：此文件以 YAML 格式提供扩展板的元数据。它必须包含以下字段：

  * ``name`` ：在 Kconfig 和构建系统中使用的扩展板名称（必填）
  * ``full_name`` ：扩展板的完整商业名称（必填）
  * ``vendor`` ：扩展板的制造商或供应商（必填）
  * ``supported_features`` ：扩展板支持的硬件功能列表（可选）。为了帮助用户了解扩展板支持的功能，而无需深入查看其 overlay 文件，可以使用 ``supported_features`` 字段列出扩展板支持的功能类型。这些值应与 :zephyr_file:`dts/bindings/binding-types.txt` 文件中定义的值一致。

  示例：

  .. code-block:: yaml

     name: foo_shield
     full_name: Foo Shield for Arduino
     vendor: acme
     supported_features:
       - display
       - input

* **<shield>.overlay** ：此文件以 Devicetree 格式提供扩展板描述，并在编译前与开发板的 :ref:`Devicetree <dt-guide>` 合并。

* **Kconfig.shield** ：此文件定义用于扩展板默认配置的扩展板 Kconfig 符号。为便于应用使用，此处的扩展板默认配置应与 :ref:`default_board_configuration` 中的配置保持一致。

* **Kconfig.defconfig** ：此文件定义扩展板的默认配置，并与 :ref:`default_board_configuration` 保持一致。因此，配置扩展板时应牢记，启用功能是应用的职责。

* **pre_dt_shield.cmake** ：此可选文件可用于向 Devicetree 编译器 ``dtc`` 传递额外参数。

此外，为避免与可能在开发板层面定义的设备发生名称冲突，建议在扩展板的 Devicetree 描述中采用 <device>_<shield> 形式的设备节点标签，例如：

.. code-block:: devicetree

        sdhc_myshield: sdhc@1 {
                reg = <1>;
                ...
        };

添加源代码
**********

可以向扩展板添加源代码，以满足扩展板特有的配置要求（例如初始化例程、时序约束等），使其能够与不同的 Zephyr 组件正常协同工作。

.. note::

   扩展板中的源代码不得用于上述用途之外的其他目的。可在多个扩展板（和/或目标）之间复用的通用功能不应放在这里。

要将源代码实际纳入构建，请添加一个 :file:`CMakeLists.txt` 文件以及相应的源文件（在 CMake 中引用这些源文件的方式与 Zephyr 的其他部分相同，例如开发板）。

开发板兼容性
************

扩展板与开发板之间的硬件兼容性取决于是否采用常见开发板（如 Arduino 和 96boards）所使用的通用连接器。为实现软件兼容性，开发板还必须提供与其支持的连接器相匹配的配置。

这需要在两个不同的层面完成：

* 引脚复用：应正确配置连接器引脚，使其与扩展板引脚匹配

* Devicetree：开发板的 :ref:`Devicetree <dt-guide>` 文件 :file:`BOARD.dts` 应为每个连接器接口定义一个备用节点标签。例如，对于 Arduino I2C：

.. code-block:: devicetree

        arduino_i2c: &i2c1 {};

开发板专用的扩展板配置
----------------------

如果需要进行修改以使扩展板适配特定开发板或开发板修订版，可以向扩展板添加针对该开发板或开发板修订版的覆盖文件，以覆盖特定开发板所使用的扩展板描述，如下所示：

.. code-block:: none

   boards/shields/<shield>
   └── boards
       ├── <board>_<revision>.overlay
       ├── <board>.overlay
       ├── <board>.defconfig
       ├── <board>_<revision>.conf
       └── <board>.conf


扩展板变体
**********

某些扩展板可能支持多个变体或修订版。在这种情况下，可以提供多个版本的扩展板描述：

.. code-block:: none

   boards/shields/<shield>
   ├── <shield_v1>.overlay
   ├── <shield_v1>.defconfig
   ├── <shield_v2>.overlay
   └── <shield_v2>.defconfig

在这种情况下，可以使用扩展板特定的修订版名称：

  .. zephyr-app-commands::
     :app: your_app
     :shield: shield_v2
     :goals: build

还可以为特定的扩展板修订版提供开发板专用的配置：

.. code-block:: none

   boards/shields/<shield>
   ├── <shield_v1>.overlay
   ├── <shield_v1>.defconfig
   ├── <shield_v2>.overlay
   ├── <shield_v2>.defconfig
   └── boards
       └── <shield_v2>
           ├── <board>.overlay
           └── <board>.defconfig

.. _gpio-nexus-node:

GPIO nexus 节点
***************

扩展板外设访问的 GPIO 必须使用扩展板的 GPIO 抽象来标识，例如由 ``arduino-header-r3`` 兼容标识提供的抽象。提供该排针接口的开发板必须将排针引脚映射到 SoC 特定的引脚。为此，需要在开发板的 Devicetree 文件中加入一个如下所示的 `nexus node`_ ：

.. _nexus node:
    https://github.com/devicetree-org/devicetree-specification/blob/4b1dac80eaca45b4babf5299452a951008a5d864/source/devicetree-basics.rst#nexus-nodes-and-specifier-mapping

.. code-block:: devicetree

    arduino_header: connector {
            compatible = "arduino-header-r3";
            #gpio-cells = <2>;
            gpio-map-mask = <0xffffffff 0xffffffc0>;
            gpio-map-pass-thru = <0 0x3f>;
            gpio-map = <0 0 &gpioa 0 0>,    /* A0 */
                       <1 0 &gpioa 1 0>,    /* A1 */
                       <2 0 &gpioa 4 0>,    /* A2 */
                       <3 0 &gpiob 0 0>,    /* A3 */
                       <4 0 &gpioc 1 0>,    /* A4 */
                       <5 0 &gpioc 0 0>,    /* A5 */
                       <6 0 &gpioa 3 0>,    /* D0 */
                       <7 0 &gpioa 2 0>,    /* D1 */
                       <8 0 &gpioa 10 0>,   /* D2 */
                       <9 0 &gpiob 3 0>,    /* D3 */
                       <10 0 &gpiob 5 0>,   /* D4 */
                       <11 0 &gpiob 4 0>,   /* D5 */
                       <12 0 &gpiob 10 0>,  /* D6 */
                       <13 0 &gpioa 8 0>,   /* D7 */
                       <14 0 &gpioa 9 0>,   /* D8 */
                       <15 0 &gpioc 7 0>,   /* D9 */
                       <16 0 &gpiob 6 0>,   /* D10 */
                       <17 0 &gpioa 7 0>,   /* D11 */
                       <18 0 &gpioa 6 0>,   /* D12 */
                       <19 0 &gpioa 5 0>,   /* D13 */
                       <20 0 &gpiob 9 0>,   /* D14 */
                       <21 0 &gpiob 8 0>;   /* D15 */
    };

这指定了如何将 ``<&arduino_header 11 0>`` 这样的 Arduino 引脚引用转换为 ``<&gpiob 4 0>`` 这样的 SoC GPIO 引脚引用。

在 Zephyr 中，GPIO 指定符通常有两个参数（由 ``#gpio-cells = <2>`` 表示）：引脚编号和一组标志。标志的低 6 位对应可在 Devicetree 中配置的特性。在某些情况下，需要使用非零标志值来告知驱动程序特定引脚的行为，例如：

.. code-block:: devicetree

    drdy-gpios = <&arduino_header 11 GPIO_ACTIVE_LOW>;

预处理后，这会变成 ``<&arduino_header 11 1>`` 。通常，这种标志的存在会导致映射查找失败，因为没有标志值为非零的映射条目。 ``gpio-map-mask`` 属性指定，在查找时，使用引脚编号的所有位以及标志中除低 6 位以外的所有位来识别指定符。然后， ``gpio-map-pass-thru`` 指定将标志的低 6 位复制过去，因此 SoC GPIO 引用会按预期变为 ``<&gpiob 4 1>`` 。

有关此功能的更多信息，请参阅 `nexus node`_ 。


.. _Arduino Uno R3 pinout:
  https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf
