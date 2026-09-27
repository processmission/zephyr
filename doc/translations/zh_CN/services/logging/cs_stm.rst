.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _logging_cs_stm:

使用 ARM Coresight STM 的多域日志
#################################

Arm CoreSight SoC-400 是一套完整的组件库，用于在系统中构建调试和跟踪功能。STM（System Trace Macrocell，系统跟踪宏单元）是集成到 CoreSight 系统中的跟踪源，主要设计用于对嵌入软件中的插桩进行高带宽跟踪。这些插桩由对 STMESP（STM Extended Stimulus Port，STM 扩展激励端口）外设寄存器的内存映射写操作组成。多个内核可以共享并直接访问 STM，而彼此无需感知。每个内核都有 65536 个激励端口（寄存器组完全相同），可以独立访问，因此各种上下文在记录数据时无需加锁。

STM 扩展激励端口（STMESP）
**************************

本地域（每个内核）可以访问自己的一组 STMESP 外设。每组外设都有用于写入数据（可带或不带时间戳，也可带或不带标记）以及写入标志的寄存器。每次写 STMESP 寄存器都会把用户数据编码为 MIPI System Trace Protocol v2（STPv2）。硬件负责在不同 STMESP 寄存器组以及不同内核的数据之间进行复用，在需要时向数据流中插入 Major 和 Channel 操作码。时间戳（来自所有内核共用的时钟源）和同步操作码由 STM 自动添加。

STM 产生的数据流可以进入各种接收端。例如，它可以直接发送到 TPIU（Trace Port Interface Unit，跟踪端口接口单元），或保存到称为 ETR（Embedded Trace Router，嵌入式跟踪路由器）的 RAM 环形缓冲区中。TPIU 是 5 引脚接口（4 个数据引脚加时钟），需要外部工具（例如 J-Trace PRO）来捕获数据。使用 ETR 时，系统中有一个内核负责处理这些数据，例如通过 UART 把它们转存到主机。

ARM Coresight 嵌入式跟踪路由器（ETR）
*************************************

ETR 是一个环形 RAM 缓冲区，跟踪数据被保存到其中。由于它可能包含来自不同来源的数据，因此使用额外的封装协议来复用它们，为此使用 ``Coresight Trace Formatter``。数据被编码为 16 字节的帧，每帧最多携带 15 字节数据。环形 RAM 缓冲区的大小被限制为 4k，因此存在数据溢出的风险。如果发生溢出，数据会丢失，但由于 STPv2 数据流中存在同步操作码，同步可以重新建立。

来自 ETR 的数据在设备上处理。它可以原样转发到主机（例如使用 UART），由主机工具解码；也可以在片上解码，以人类可读的格式输出数据。

Nordic Semiconductor NRF54H20 的实现没有使用 ETR 外设来判断缓冲区是否繁忙，而是使用自己的封装：Trace Buffer Monitor（TBM）。

STMESP 日志前端
***************

实现了 :ref:`log_frontend` API。自定义前端假定所有必需的操作都在日志宏调用的上下文中执行，也假定前端提供时间戳。该前端利用存在多个 STMESP 寄存器组这一事实，使用多组寄存器来避免上下文加锁。它使用原子递增的通道计数器来选择唯一的 STMESP 组，并把整条消息写入该 STMESP。它只使用有限的寄存器组池，把大多数通道留给其他用途。

早期日志
========

在 STM 或 ETR/TPIU 完成设置之前无法使用 STMESP。为了支持在基础设施就绪之前进行早期日志记录，系统使用一个专用的 RAM 缓冲区来写入数据。当收到 STM 基础设施就绪通知（:c:func:`log_frontend_stmesp_etr_ready`）时，RAM 缓冲区的内容会被写入 STMESP。早期日志仅适用于拥有并配置 Coresight 基础设施的那个内核（例如 NRF54H20 上是安全核）。

跟踪点
======

有些情况下日志仍然太慢（即使它已经非常快）。针对这类情况，系统新增了专用的 ``trace point`` API。它极快，因为只是对某个 STMESP 寄存器的一次写操作。该 API 中有 2 个函数：

* :c:func:`log_frontend_stmesp_tp` - 它只接受一个参数：index。index 的取值范围是 0 到 65280。
* :c:func:`log_frontend_stmesp_tp_d32` - 它接受两个参数：index 和用户数据。index 的取值范围是 0 到 65280。用户数据是一个 32 位字。

在 NRF54H20 上记录一个跟踪点耗时不到 100 ns，比最快的日志消息大约快 7 倍。

使用 STM 记录日志
*****************

STM 日志有两种运行模式：

* 基于字典 - 辅助模式，使用基于字典的日志。在这种模式下，日志字符串可以从二进制文件中移除，因为它们只用于解码，而解码由主机工具完成。这种模式占用内存更少、速度更快（快 2-3 倍）。写入的数据更少，因此 ETR 缓冲区发生数据溢出的可能性更低。
* 独立模式 - 数据在片上解码并打印人类可读的字符串。这种模式需要更多的设备资源和处理能力。

下图展示了使用 ARM Coresight STM 的多域日志。

.. figure:: images/coresight_architecture.png

每个内核（本地域）都使用日志前端，把日志数据写入 STMESP 寄存器。

如果使用 TPIU 作为输出，则不再需要其他软件组件。STPv2 数据流由 STM 组装，并通过 TPIU 发送。

如果使用 ETR RAM 缓冲区，则由缓冲区的所有者内核（``proxy``）负责处理这些数据。如果使用基于字典的日志，proxy 只需把数据原样通过 UART 发送。如果使用独立日志，proxy 会使用 :ref:`cs_trace_defmt` 和 :ref:`mipi_stp_decoder` 来解码数据并解复用消息。消息会使用日志 :ref:`log_output` 格式化为人类可读的字符串。

基于字典的日志
==============

辅助式多核日志使用基于字典的日志，把不含冗余字符串的消息发送到 STM，它基于 Zephyr 日志 API 提供的 :ref:`logging_guide_dictionary` 特性。它不在日志消息中包含格式字符串，而是记录字符串存放的地址（消息 ID），从而减小日志子系统的体积。如果数据进入 ETR 缓冲区，proxy 内核的职责就是把该数据转存出来。配备解码工具的主机 PC 使用构建过程中生成的 JSON 数据库，把这些地址还原为人类可读的文本。

使用日志时，这种方法有以下优点：

* 它减小了二进制文件的体积，因为日志消息中使用的字符串不存放在二进制文件本身中。日志基础设施也非常精简，在本地域上只有前端，甚至不需要字符串格式化函数。
* 它减少了需要发送到应用核并由应用核处理的数据量，因为字符串格式化被卸载到主机侧。
* 日志速度很快。在 NRF54H20 上记录一条简单消息（最多 2 个参数）耗时不到 1 us。

Proxy 内核使用 Nordic 专有的外设（TBM）来获取 ETR 缓冲区的繁忙状态并通过 UART 发送数据。ETR 缓冲区的 Nordic 专有驱动位于 :zephyr_file:`drivers/debug/debug_nrf_etr.c`。

配置
----

对于 Nordic SoC，应使用专用的 snippet（:ref:`nordic-log-stm-dict`）来启用日志。每个内核都必须使用该 snippet 构建。如果有任何内核想使用它，应用核也必须启用它，因为应用核充当 proxy（处理 ETR 缓冲区）。所有内核必须使用相同的日志配置。

读取日志
--------

要读取基于字典的 STM 日志输出，请执行以下操作：

1. 设置日志捕获。

   使用 ``nrfutil trace stm`` 命令开始从设备捕获日志，并为每个域 ID 指定数据库配置，同时指定串口、波特率和输出文件名::

      nrfutil trace stm --database-config 34:build/zephyr/log_dictionary.json,35:build_rad/zephyr/log_dictionary.json --input-serialport /dev/ttyACM1 --baudrate 115200 --output-ascii out.txt

#. 捕获并解码日志。

   nrfutil 会从指定的 UART 端口捕获日志数据，并使用提供的字典数据库把日志解码为人类可读的格式。解码后的日志会保存到指定的输出文件中（上面示例中的 :file:`out.txt` 文件）。

#. 打开输出文件查看解码后的日志消息。

   该文件中包含时间戳和人类可读格式的日志消息。

如果日志捕获找不到同步，请重新运行捕获过程。

.. note::
   重新运行该过程时可能出现解码异常或时间戳不正确的情况。

每行日志在日志级别和模块名之间都包含与域或内核相关的前缀，用于表明产生该日志条目的内核。下面列出了用于表示各个内核的前缀：

.. csv-table:: nRF54H20 日志前缀
   :header: "内核", "前缀", "ID"

   安全域, ``sec``, 0x21
   应用核, ``app``, 0x22
   无线核, ``rad``, 0x23
   系统控制器（SysCtrl）, ``sys``, 0x2c
   快速轻量级处理器（FLPR）, ``flpr``, 0x2d
   外设处理器（PPR）, ``ppr``, 0x2e
    , ``mod``, 0x24

独立日志
========

前端写入 STMESP 寄存器。消息格式与片上解码器 :zephyr_file:`subsys/logging/frontends/log_frontend_stmesp_demux.c` 保持一致。

``Proxy`` 使用 Nordic 专有的外设（TBM）获取 ETR 缓冲区的繁忙状态，读取并解码数据，然后通过 UART 发送人类可读的数据。ETR 缓冲区的 Nordic 专有驱动位于 :zephyr_file:`drivers/debug/debug_nrf_etr.c`。它使用 :ref:`cs_trace_defmt`、:ref:`mipi_stp_decoder` 以及上述解复用器来解码消息。

日志消息包含日志宏中使用的只读格式字符串，因此它们无法从二进制文件中移除。这种模式占用更多只读内存，吞吐量也更低，因为消息更长，处理也更耗时。与基于字典的模式相比，日志速度慢 2-3 倍。

Configuration
-------------

对于 Nordic SoC，应使用专用的 snippet（:ref:`nordic-log-stm`）来启用日志。每个内核都必须使用该 snippet 构建。如果有任何内核想使用它，应用核也必须启用它，因为应用核充当 proxy（处理 ETR 缓冲区）。所有内核必须使用相同的日志配置。

Reading the logs
----------------

日志通过控制台 UART 打印。

.. note::
   要在应用中使用 UART，必须在 devicetree 中描述 UART 节点。更多细节请参见 :ref:`devicetree-intro`。

下面是一个日志输出示例::

   [00:00:00.154,790] <inf> app/spsc_pbuf: alloc in 0x2f0df800
   [00:00:00.163,319] <inf> app/spsc_pbuf: alloc 0x2f0df800 wr_idx:20
   [00:00:00.181,112] <inf> app/spsc_pbuf: commit in 0x2f0df800
   [00:00:00.189,090] <inf> app/spsc_pbuf: commit 0x2f0df800, len:20 wr_idx: 44
   [00:00:00.202,577] <inf> rad/icmsg: mbox_callback
   [00:00:00.214,750] <inf> rad/spsc_pbuf: claim 0x2f0df800 rd_idx:20
   [00:00:00.235,823] <inf> rad/spsc_pbuf: free 0x2f0df800 len:20 rd_idx: 44
   [00:00:00.244,507] <inf> rad/spsc_pbuf: read done 0x2f0df800 len:20
   [00:00:00.272,444] <inf> rad/host: ep recv 0x330021f0, len:20
   [00:00:00.283,939] <inf> rad/host: rx:00 exp:00
   [00:00:00.292,200] <inf> rad/icmsg: read 0
   [00:00:05.077,026] <inf> rad/spsc_pbuf: alloc in 0x2f0df000
   [00:00:05.077,068] <inf> rad/spsc_pbuf: alloc 0x2f0df000 wr_idx:44
   [00:00:05.077,098] <inf> rad/spsc_pbuf: commit in 0x2f0df000
   [00:00:05.077,134] <inf> rad/spsc_pbuf: commit 0x2f0df000, len:20 wr_idx

每行日志在日志级别和模块名之间都包含与域或内核相关的前缀，用于表明产生该日志条目的内核。下面列出了用于表示各个内核的前缀：

.. csv-table:: nRF54H20 日志前缀
   :header: "Core", "Prefix"

   Secure Domain, ``sec``
   Application core, ``app``
   Radio core, ``rad``
   System Controller (SysCtrl), ``sys``
   Fast Lightweight Processor (FLPR), ``flpr``
   Peripheral Processor (PPR), ``ppr``

其他注意事项
============

使用 STM 日志时，请考虑以下几点：

* 使用优化后的日志宏（最多带 2 个字长的数值参数，例如 ``LOG_INF("%d %c", (int)x, (char)y)``）来改善日志的体积和速度。
* 对于内存受限的应用（例如在 PPR 内核上运行时），请在项目配置中把 :kconfig:option:`CONFIG_PRINTK` 和 :kconfig:option:`CONFIG_BOOT_BANNER` 两个 Kconfig 选项都设置为 ``n``，以禁用 ``printk()`` 函数。
* 在处理多个域（例如无线核和应用核）时，请确保每个数据库都以正确的域 ID 为前缀。
* 由于存放 STM 日志的 RAM 缓冲区大小有限，某些日志消息可能会被丢弃。
