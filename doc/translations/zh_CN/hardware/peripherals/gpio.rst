.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _gpio_api:

通用输入/输出（GPIO）
#####################

概述
****

通用输入/输出（GPIO）是一种没有固定功能的数字信号引脚，可通过软件控制其作为输入或输出。

GPIO API 提供了与通用输入/输出（GPIO）引脚交互的通用方法。应用可以通过该 API 将引脚配置为输入或输出、读写引脚状态以及管理中断。主要功能包括：

**引脚配置**
  将引脚配置为输入、输出或断开连接状态。支持内部上拉/下拉电阻和驱动强度配置。

**数据访问**
  读取输入值和写入输出值。

**中断**
  配置由引脚状态变化（上升沿、下降沿、低电平、高电平）触发的中断，并注册回调函数来处理这些中断。

**Devicetree 集成**
  GPIO 通常在 Devicetree 中定义，驱动和应用可以使用 :c:struct:`gpio_dt_spec` 以与硬件无关的方式引用它们。

Devicetree 配置
***************

GPIO 控制器在 Devicetree 中定义为具有 ``gpio-controller`` 属性的节点。``#gpio-cells`` 属性通常指定使用 2 个单元来描述一个 GPIO：引脚编号和标志。

GPIO 控制器定义示例：

.. code-block:: devicetree

   gpio0: gpio@40022000 {
       compatible = "ti,cc13xx-cc26xx-gpio";
       reg = <0x40022000 0x400>;
       interrupts = <0 0>;
       gpio-controller;
       #gpio-cells = <2>;
   };

引用 GPIO 的示例：

.. code-block:: devicetree

   leds {
       compatible = "gpio-leds";
       led0: led_0 {
           gpios = <&gpio0 25 GPIO_ACTIVE_HIGH>;
           label = "Green LED";
       };
   };

基本操作
********

GPIO 操作通常通过 :c:struct:`gpio_dt_spec` 结构体执行，该结构体用于保存 Devicetree 中指定的 GPIO 引脚信息。

该结构体通常使用 :c:macro:`GPIO_DT_SPEC_GET` 宏（或其任一变体）填充。

.. code-block:: c
   :caption: 为别名为 ``led0`` 的 GPIO 引脚填充 gpio_dt_spec 结构体

   #define LED0_NODE DT_ALIAS(led0)
   static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);

随后即可使用 :c:struct:`gpio_dt_spec` 结构体执行 GPIO 操作。

.. code-block:: c
   :caption: 将 GPIO 引脚（上一段代码中的 ``led`` ）配置为输出，初始状态为非有效状态，然后将其设置为有效电平。

   int ret;

   ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_INACTIVE);
   if (ret < 0) {
       return ret;
   }

   ret = gpio_pin_set_dt(&led, 1);
   if (ret < 0) {
       return ret;
   }

有关使用 :c:struct:`gpio_dt_spec` 结构体对 GPIO 执行基本操作的完整示例，请参阅 :zephyr:code-sample:`blinky` 。

也可以直接对 GPIO 控制器设备执行 GPIO 操作，此时需要使用以设备指针作为参数的 GPIO API 函数。例如，使用 :c:func:`gpio_pin_configure` 代替 :c:func:`gpio_pin_configure_dt` 。

GPIO Hogs
*********

GPIO hog 机制可在系统初始化期间自动配置 GPIO 引脚。对于需要设置为特定状态（例如复位线、电源使能引脚）且不需要应用在运行时控制的引脚，此机制很有用。

Hog 在 Devicetree 中定义为 GPIO 控制器节点的子节点。

- ``gpio-hog`` 属性将节点标记为 hog。
- ``gpios`` 属性指定引脚及其有效状态。
- 使用 ``input`` 、``output-low`` 或 ``output-high`` 属性之一指定配置。

Devicetree 覆盖文件示例：

.. code-block:: devicetree

   &gpio0 {
       hog1 {
           gpio-hog;
           gpios = <1 GPIO_ACTIVE_LOW>;
           output-high;
       };

       hog2 {
           gpio-hog;
           gpios = <2 GPIO_ACTIVE_HIGH>;
           output-low;
       };
   };

如果某个引脚被配置为 hog，而你除了需要在系统初始化期间自动设置其初始状态之外，还需要在运行时控制该引脚，可以考虑改用 :ref:`regulator_api`，并配合使用 :dtcompatible:`regulator-fixed` Devicetree 节点。

配置选项
********

主要配置选项：

* :kconfig:option:`CONFIG_GPIO`
* :kconfig:option:`CONFIG_GPIO_SHELL`
* :kconfig:option:`CONFIG_GPIO_GET_DIRECTION`
* :kconfig:option:`CONFIG_GPIO_GET_CONFIG`
* :kconfig:option:`CONFIG_GPIO_HOGS`
* :kconfig:option:`CONFIG_GPIO_ENABLE_DISABLE_INTERRUPT`

API 参考
********

.. doxygengroup:: gpio_interface
