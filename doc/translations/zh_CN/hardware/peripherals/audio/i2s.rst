.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _i2s_api:

芯片间音频（I2S）总线
#####################

概述
****

I2S（芯片间音频）API 支持标准 I2S 接口以及常见的非标准扩展，例如 PCM 短帧/长帧同步和左对齐/右对齐数据格式。

Shell
*****

启用 :kconfig:option:`CONFIG_I2S_SHELL` 后，即可使用 ``i2s`` shell 命令，通过任意 I2S 控制器流式传输生成的正弦波测试音，无需编写应用代码。该命令仅负责传输；需配合 ``codec`` shell 将音频路由到编解码器。

测试音命令归于 ``i2s tone`` 下：

* ``i2s tone start <device> [frequency_hz] [sample_rate] [bits]`` 在指定的 I2S 设备上启动立体声测试音。``frequency_hz`` 默认为 440 Hz，``sample_rate`` 默认为 48000 Hz，``bits`` 默认为 16（有效值为 16、24 和 32）。
* ``i2s tone stop`` 停止正在播放的测试音。
* ``i2s tone info`` 显示当前测试音流的状态。

例如，流式传输频率为 1 kHz、采样率为 48 kHz、位深为 16 位的测试音：

.. code-block:: console

   uart:~$ i2s tone start i2s@0 1000 48000 16
   Streaming 1000 Hz tone on i2s@0 @ 48000 Hz, 16-bit stereo
   uart:~$ i2s tone info
   state    : streaming
   i2s dev  : i2s@0
   tone     : 1000 Hz
   rate     : 48000 Hz
   format   : 16-bit stereo, 64-frame blocks x 8
   uart:~$ i2s tone stop
   Stopped

shell 使用的发送（TX）缓冲由 :kconfig:option:`CONFIG_I2S_SHELL_BLOCK_FRAMES` 和 :kconfig:option:`CONFIG_I2S_SHELL_BLOCK_COUNT` 控制。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_I2S`
* :kconfig:option:`CONFIG_I2S_SHELL`

API 参考
********

.. doxygengroup:: i2s_interface
