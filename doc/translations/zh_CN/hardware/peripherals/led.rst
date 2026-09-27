.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _led_api:

发光二极管（LED）
#################

概述
****

LED API 提供对单个发光二极管和 LED 灯带的访问。它通过一组精简的通用操作，抽象了简单的 GPIO 驱动 LED、支持 PWM 调光的 LED、专用 LED 控制器 IC 和可寻址 LED 灯带之间的差异。

提供两个相关的子系统：

* **LED** — 用于控制独立 LED 或由控制器驱动的 LED 的通用 API（开关、亮度、颜色、闪烁）
* **LED 灯带** — 专为 WS2812 和 APA102 等可寻址 LED 灯串设计的 API，其中每个像素都有自己的颜色值

LED 操作
********

驱动实现下列操作的一个子集。如果底层驱动未提供某个可选操作，调用该操作将返回 ``-ENOSYS`` 。

必需操作（至少实现以下一项）：

* :c:func:`led_on` / :c:func:`led_off` — 将 LED 完全点亮或关闭
* :c:func:`led_set_brightness` — 在 0 到 :c:macro:`LED_BRIGHTNESS_MAX` （100）的范围内设置亮度；实现此操作后，:c:func:`led_on` 和 :c:func:`led_off` 也会自动使用它

可选操作：

* :c:func:`led_blink` — 按给定的点亮和关闭时长启动 LED 闪烁
* :c:func:`led_set_color` — 设置多色 LED 各通道的颜色值
* :c:func:`led_get_info` — 获取描述特定 LED 的 :c:struct:`led_info` （标签、索引、颜色映射）
* :c:func:`led_write_channels` — 写入一段连续通道的原始值，供将 LED 表示为通道数组的驱动使用

LED 索引
********

驱动控制的每个 LED 都通过从零开始的 ``led`` 索引寻址。多色 LED 占用一个索引；其各颜色通道的值一并提交给 :c:func:`led_set_color` 。

多色 LED 的颜色通道顺序由 :c:struct:`led_info` 的 ``color_mapping`` 字段描述。每个条目均为 :file:`include/zephyr/dt-bindings/led/led.h` 中定义的 ``LED_COLOR_ID_*`` 值之一：

* ``LED_COLOR_ID_WHITE``
* ``LED_COLOR_ID_RED``
* ``LED_COLOR_ID_GREEN``
* ``LED_COLOR_ID_BLUE``
* ``LED_COLOR_ID_AMBER``
* ``LED_COLOR_ID_VIOLET``
* ``LED_COLOR_ID_YELLOW``
* ``LED_COLOR_ID_IR``

Devicetree 配置
***************

简单的 LED 通常描述为 LED 控制器的子节点，并通过 Devicetree 别名引用：

.. code-block:: dts

   / {
       aliases {
           led0 = &status_led;
       };

       leds {
           compatible = "gpio-leds";
           status_led: led_0 {
               gpios = <&gpio0 13 GPIO_ACTIVE_HIGH>;
               label = "Status LED";
           };
       };
   };

对于多色 LED，颜色信息通过 ``color-mapping`` 属性编码，其值使用 :file:`include/zephyr/dt-bindings/led/led.h` 中的 ``LED_COLOR_ID_*`` 值。

用法示例
********

使用 Devicetree 别名进行基本的开关控制：

.. code-block:: c

   #include <zephyr/drivers/led.h>
   #include <zephyr/devicetree.h>

   #define LED_NODE DT_ALIAS(led0)
   static const struct device *led_dev = DEVICE_DT_GET(DT_PARENT(LED_NODE));
   static const uint32_t led_idx = DT_NODE_CHILD_IDX(LED_NODE);

   int turn_on_status_led(void)
   {
       if (!device_is_ready(led_dev)) {
           return -ENODEV;
       }
       return led_on(led_dev, led_idx);
   }

设置亮度（0 到 100）：

.. code-block:: c

   /* Dim the LED to 25% brightness */
   led_set_brightness(led_dev, led_idx, 25);

以点亮 500 ms、熄灭 500 ms 的模式闪烁：

.. code-block:: c

   int err = led_blink(led_dev, led_idx, 500, 500);

   if (err == -ENOSYS) {
       /* Driver does not implement blink natively */
   }

设置多色（RGB）LED 的颜色：

.. code-block:: c

   /* Order of the values must match the color_mapping reported by
    * led_get_info(); for a standard RGB mapping the order is R, G, B.
    */
   const uint8_t purple[] = { 0x80, 0x00, 0x80 };

   led_set_color(led_dev, led_idx, ARRAY_SIZE(purple), purple);

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_LED`
* :kconfig:option:`CONFIG_LED_STRIP`
* :kconfig:option:`CONFIG_LED_SHELL`
* :kconfig:option:`CONFIG_LED_INIT_PRIORITY`

API 参考
********

LED
===

.. doxygengroup:: led_interface

LED 灯带
========

.. doxygengroup:: led_strip_interface

模拟 LED 控制器
===============

.. doxygengroup:: led_fake
