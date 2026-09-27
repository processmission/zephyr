.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _pwm_api:

脉冲宽度调制（PWM）
###################

概述
****

脉冲宽度调制（PWM）是一种通过改变数字信号的占空比来编码信息或控制功率输出的技术。PWM 信号以固定频率在高、低电平之间切换；每个周期内高电平所占的时间比例称为 *占空比* 。

PWM 在嵌入式系统中的常见用途：

* **LED 亮度控制** — 占空比直接对应感知亮度
* **直流电机转速控制** — 平均电压与占空比成正比
* **伺服电机定位** — 脉冲宽度用于编码目标角度
* **音调生成** — 通过改变频率产生可听见的音调
* **功率转换** — 降压/升压转换器和 D 类放大器

PWM 信号参数
************

PWM 信号由三个数值描述：

* **周期** — 一次完整通断循环的总时长，单位为纳秒
* **脉冲宽度** — 高电平（有效）部分的持续时间，单位为纳秒
* **占空比** — 脉冲宽度与周期的比值（以百分比表示）；50% 的占空比表示信号在半个周期内处于高电平

.. code-block:: none

   |<-- pulse -->|
   +--------------+            +-
   |              |            |
   +              +------------+
   |<----------- period -------->|

Zephyr PWM 驱动模型
*******************

每个 PWM 控制器提供一个或多个独立的 *通道* 。通道由从零开始的索引标识，并驱动单个输出引脚。

所有 PWM 驱动都实现了 :file:`include/zephyr/drivers/pwm.h` 中定义的同一套 API。核心函数是 :c:func:`pwm_set` ，用于设置通道的周期和脉冲宽度。辅助宏可将常用时间单位转换为纳秒：

* :c:macro:`PWM_HZ` — 以 Hz 为单位的频率（例如， ``PWM_HZ(1000)`` → 1 ms 周期）
* :c:macro:`PWM_KHZ` — 以 kHz 为单位的频率
* :c:macro:`PWM_USEC` — 以微秒为单位的周期或脉冲宽度
* :c:macro:`PWM_MSEC` — 以毫秒为单位的周期或脉冲宽度

Devicetree 配置
***************

PWM 引脚通过 Devicetree 中的 ``pwms`` 属性描述。每个条目指定控制器的 phandle、通道编号、以纳秒为单位的周期，以及可选的极性标志：

.. code-block:: dts

   / {
       my_node {
           pwms = <&pwm0 0 PWM_MSEC(20) PWM_POLARITY_NORMAL>;
           pwm-names = "servo";
       };
   };

在 C 代码中，使用 :c:macro:`PWM_DT_SPEC_GET` 系列宏获取配置信息：

.. code-block:: c

   static const struct pwm_dt_spec servo =
       PWM_DT_SPEC_GET(DT_NODELABEL(my_node));

用法示例
********

使用 ``pwm_dt_spec`` 设置占空比：

.. code-block:: c

   #include <zephyr/drivers/pwm.h>

   static const struct pwm_dt_spec led_pwm =
       PWM_DT_SPEC_GET(DT_ALIAS(pwm_led0));

   int set_led_brightness(uint8_t percent)
   {
       if (!device_is_ready(led_pwm.dev)) {
           return -ENODEV;
       }

       /* pulse = period * duty_cycle / 100 */
       uint32_t pulse = led_pwm.period / 100 * percent;

       return pwm_set_dt(&led_pwm, led_pwm.period, pulse);
   }

设置伺服电机位置（在 20 ms 周期内产生 1–2 ms 的脉冲）：

.. code-block:: c

   #include <zephyr/drivers/pwm.h>

   #define SERVO_PERIOD_NS   PWM_MSEC(20)
   #define SERVO_MIN_PULSE   PWM_USEC(1000)
   #define SERVO_MAX_PULSE   PWM_USEC(2000)

   int set_servo_angle(const struct device *pwm_dev, uint32_t channel,
                       uint8_t angle_deg)
   {
       uint32_t pulse = SERVO_MIN_PULSE +
           (SERVO_MAX_PULSE - SERVO_MIN_PULSE) * angle_deg / 180;

       return pwm_set(pwm_dev, channel, SERVO_PERIOD_NS, pulse,
                      PWM_POLARITY_NORMAL);
   }

PWM 捕获
********

某些 PWM 控制器支持 *输入捕获* ，用于测量输入信号的周期和/或脉冲宽度。这有助于解码来自遥控接收机或传感器输出等外部来源的 PWM 信号。

使用 :c:func:`pwm_configure_capture` 和 :c:func:`pwm_enable_capture` 启用捕获：

.. code-block:: c

   void pwm_capture_cb(const struct device *dev, uint32_t channel,
                       uint32_t period_cycles, uint32_t pulse_cycles,
                       int status, void *user_data)
   {
       if (status != 0) {
           return;
       }
       /* convert cycles to nanoseconds using pwm_get_cycles_per_sec() */
   }

   /* configure for single-shot capture of both period and pulse */
   pwm_configure_capture(dev, channel,
                         PWM_CAPTURE_TYPE_BOTH | PWM_CAPTURE_MODE_SINGLE,
                         pwm_capture_cb, NULL);
   pwm_enable_capture(dev, channel);

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_PWM`
* :kconfig:option:`CONFIG_PWM_SHELL`
* :kconfig:option:`CONFIG_PWM_CAPTURE`
* :kconfig:option:`CONFIG_PWM_EVENT`

API 参考
********

.. doxygengroup:: pwm_interface

.. doxygengroup:: pwm_fake
