.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _pulse_io_api:

脉冲 IO
#######

概述
****

脉冲 IO 子系统为在单条 GPIO 线上生成和捕获具有精确定时的数字信号边沿的硬件提供了与厂商无关的 API。多个 MCU 系列为此配备了专用外设，但名称各不相同。脉冲 IO 对这类硬件进行了抽象，使可寻址 LED 灯带、红外收发、步进电机脉冲生成、频率和占空比测量以及单线类协议等客户端驱动只需对接一次，就能在任何提供相应后端的 SoC 上运行。

相关配置选项：

* :kconfig:option:`CONFIG_PULSE_IO`

提交模式
********

通道在配置时固定为一种提交模式，该模式从后端通过其能力信息声明支持的模式中选择。

``PULSE_IO_MODE_SYMBOL``
   应用提交一个 :c:struct:`pulse_symbol` 数组，每个符号都包含明确的电平和持续时间，持续时间以所配置分辨率对应的时钟节拍为单位。连续符号的持续时间可以任意指定，彼此无关。此模式适用于同一数据流中边沿间隔变化的协议或场景，例如红外遥控、单线协议和步进电机加速过程。

``PULSE_IO_MODE_CELL``
   应用提交一个 :c:struct:`pulse_cell` 数组。每个单元的周期相同，在通道配置中一次性设置，每个单元包含该周期内的电平或占空比值。此模式适用于本身具有周期性、仅每个周期的电平或占空比发生变化的数据流，例如可寻址 LED 的位波形整形或可变占空比 PWM。在这些场景中，单元比符号更节省内存。

后端在 :c:struct:`pulse_io_caps` 中声明支持的模式。请求不支持的模式会导致 :c:func:`pulse_io_channel_configure` 返回 ``-ENOTSUP`` 。

配置
****

客户端在探测时调用 :c:func:`pulse_io_get_capabilities` 查询能力，以决定使用哪种模式和功能集，通过 :c:func:`pulse_io_channel_get` 预留通道，并在进行任何传输之前使用 :c:func:`pulse_io_channel_configure` 配置通道。阻塞式传输使用 :c:func:`pulse_io_transmit_sync` 和 :c:func:`pulse_io_receive_sync` ；异步传输和流式传输使用 RTIO 路径。

字节转符号辅助函数 :c:func:`pulse_io_encode_bytes` 及其逆向函数 :c:func:`pulse_io_decode_bytes` 使用逐位模板，在协议字节流和脉冲符号之间进行转换。

RTIO
****

后端可以选择与 :ref:`rtio` 集成，提供 iodev 提交路径，以及通过 :c:func:`pulse_io_get_encoder` 和 :c:func:`pulse_io_get_decoder` 获取的编码器和解码器虚函数表。使用 RTIO 时，客户端将有效载荷编码到符号缓冲区中，通过 RTIO 队列提交，并解码捕获到的任何响应，从而获得排队传输、链式传输、流式接收以及 RTIO 框架提供的用户空间路径。RTIO 操作是可选的；未实现这些操作的后端会将相应的驱动 API 成员保留为 ``NULL`` ，相应的访问函数则返回 ``-ENOSYS`` 。

API 参考
********

.. doxygengroup:: pulse_io_interface
