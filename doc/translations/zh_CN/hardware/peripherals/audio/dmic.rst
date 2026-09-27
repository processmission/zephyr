.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _audio_dmic_api:

数字麦克风（DMIC）
##################

概述
****

音频 DMIC 接口提供对数字麦克风的访问。

数字麦克风通常输出 PDM（脉冲密度调制）比特流，而非模拟音频。PDM 使用高速率的 1 位信号，通过一段时间内 1 和 0 的密度来表示音频幅度。

由于应用通常使用 PCM（脉冲编码调制）采样数据，而非原始 PDM 数据，因此 DMIC 控制器会将麦克风数据流转换为 PCM 音频。此转换过程包括滤波和抽取：滤波用于去除通过噪声整形转移到 PDM 数据流高频部分的噪声，抽取则将比特流速率降低到所需的 PCM 采样率。

从 Zephyr 的角度来看，DMIC 设备是一种音频采集外设。应用配置麦克风和控制器，启动采集，并从驱动程序读取 PCM 缓冲区。

关键概念
********

DMIC API 将配置分为三个部分，分别对应采集路径中的以下环节：

#. 如何在 PDM 侧驱动麦克风，
#. 如何排列输入的 PDM 通道，以及
#. 如何将转换后的 PCM 采样数据传递给应用。

这些部分组合在 :c:struct:`dmic_cfg` 中，并传递给 :c:func:`dmic_configure` 。

**PDM I/O 配置** （:c:member:`dmic_cfg.io` ）
  此部分描述麦克风接口的电气和时序要求，例如支持的 PDM 时钟频率范围、占空比，以及控制器特有的信号极性设置。

**通道配置** （:c:member:`dmic_cfg.channel` ）
  此部分告知驱动程序，应将哪个物理 PDM 控制器的左路或右路麦克风映射为 PCM 输出中的各个逻辑音频通道。它还声明应用希望使用的通道数和数据流数。

**PCM 数据流配置** （:c:member:`dmic_cfg.streams` ）
  此部分定义驱动程序传递的 PCM 数据，包括采样率、采样位宽、块大小，以及用于为每个已启用的数据流分配接收缓冲区的 :c:struct:`k_mem_slab` 。

典型应用流程
============

DMIC API 的典型使用流程如下：

#. 获取 DMIC 设备，通常通过 Devicetree 获取。
#. 将 I/O、通道和数据流设置填入 :c:struct:`dmic_cfg` 结构体。有关如何定义 DMIC 用于存储所接收 PCM 数据的内存缓冲区，详见下文的 :ref:`dmic_buffering` 一节。
#. 调用 :c:func:`dmic_configure` ，传入配置结构体。
#. 调用 :c:func:`dmic_trigger` 并使用 :c:enumerator:`DMIC_TRIGGER_START` 启动采集。
#. 通过 :c:func:`dmic_read` 获取 PCM 数据。
#. 根据需要，使用其他触发命令停止、暂停或重置采集。

.. _dmic_buffering:

缓冲
====

接收到的 PCM 数据通过驱动程序拥有的缓冲区返回。应用通过各个已配置的 PCM 数据流所引用的 :c:struct:`k_mem_slab` 提供底层内存。

一种常见做法是静态声明此内存块池：

.. code-block:: c
  :caption: 为 PCM 接收缓冲区静态声明内存块池

   K_MEM_SLAB_DEFINE_STATIC(mem_slab,
                            SAMPLES_PER_BUFFER * sizeof(int16_t),
                            BUFFER_COUNT,
                            sizeof(void *));

在此示例中，内存块池中的每个块存储一个 PCM 缓冲区，``BUFFER_COUNT`` 设置应用通过 :c:func:`dmic_read` 读取缓冲区之前，内部可排队保存的缓冲区数量。

Shell 命令
**********

启用 :kconfig:option:`CONFIG_AUDIO_DMIC_SHELL` 后，即可使用一组 ``dmic`` 命令。这些命令支持以交互方式从 DMIC 设备采集音频，无需编写专用应用。

每个子命令的第一个参数均为 DMIC 设备名称，其后可选填音频采集参数（采样率、通道数和 PCM 采样位宽）。

可用的子命令如下：

``dmic read <device> [<count> [<rate_hz> [<channels> [<pcm_width>]]]]``
  采集 ``count`` 个音频块，并打印每个通道的峰值电平。``count`` 的默认值为 5；每个音频块包含 50 ms 的音频。

``dmic vu <device> [<rate_hz> [<channels> [<pcm_width>]]]``
  显示以颜色区分电平的实时电平表，带有峰值保持和削波指示，每个通道对应一个条形指示器。持续运行，直到按下任意键。

``dmic dump <device> [<seconds> [<rate_hz> [<channels> [<pcm_width>]]]]``
  采集 ``seconds`` 秒的音频，并将其以 base64 编码的原始 PCM 格式打印，同时输出用于解码和回放的主机命令。默认时长为 2 秒。

内置帮助（例如 ``dmic read --help`` ）列出了各参数及其默认值。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_AUDIO_DMIC`
* :kconfig:option:`CONFIG_AUDIO_DMIC_SHELL`

API 参考
********

.. doxygengroup:: audio_dmic_interface
