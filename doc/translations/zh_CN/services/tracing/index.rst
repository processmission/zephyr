.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _tracing:

跟踪
####

概述
****

跟踪功能提供了一些钩子，让你可以从应用程序中收集数据，并允许在主机上运行的 :ref:`工具 <tools>` 可视化内核和各种子系统的内部工作原理。

每个系统都有特定于应用程序的事件需要跟踪。从历史上看，这意味着：

1. 确定特定于应用程序的负载，
2. 选择合适的序列化格式，
3. 编写目标端的序列化代码，
4. 确定并编写 I/O 传输机制，
5. 编写 PC 端的反序列化器/解析器，
6. 编写用于过滤和呈现的自定义专用工具。

应用程序可以使用现有格式之一，也可以通过覆盖 :zephyr_file:`include/zephyr/tracing/tracing.h` 中声明的宏来定义自定义格式。

Zephyr 中提供并支持不同的格式、传输方式和主机端工具。

事实上，I/O 因系统不同而差异很大。因此，当我们必须确保负载/格式（顶层）与传输机制（底层）之间的接口足够通用且高效，足以对这些 I/O 类型建模时，为 I/O 类型建立分类体系会很有帮助。请参阅下文的 *I/O taxonomy* 一节。

命名跟踪事件
************

尽管用户可以通过扩展任何受支持的序列化格式来启用额外的跟踪功能（或者提供自己的后端），Zephyr 还提供了一个通用的命名跟踪函数以方便使用，同时也用于演示如何扩展跟踪框架。

用户可以通过调用 :c:func:`sys_trace_named_event` 生成自定义跟踪事件，该函数接受事件名称以及两个任意的 4 字节参数。如果提供的事件名称对于跟踪后端所支持的序列化格式而言过长，跟踪后端可能会将其截断。

序列化格式
**********

.. _ctf:

Common Trace Format（CTF）支持
==============================

Common Trace Format（CTF）是一种用于描述跟踪格式的开放格式和语言。它支持工具复用，目前已存在行文本形式（babeltrace）和图形形式（TraceCompass）的变体。

CTF 对 C 程序员来说应该很熟悉，但它增加了更强的类型。参见 `CTF - A Flexible, High-performance Binary Trace Format <https://diamon.org/ctf/>`_。


CTF 让我们能够正式地描述应用程序特定的负载和序列化格式，从而为主机端工具、解析器以及用于过滤和呈现的工具提供通用基础设施。


通用接口
--------

在 CTF 中，事件会被序列化为一个包含一个或多个字段的数据包。如下文 *I/O taxonomy* 一节所述，底层可以：

- 在事务开始时执行操作（例如互斥锁加锁），
- 以某种方式处理每个字段（例如同步推送发送、拼接、入队到线程绑定的 FIFO），
- 在事务结束时执行操作（例如互斥锁释放、发送拼接缓冲区）。

CTF 顶层示例
------------

CTF_EVENT 宏会将每个参数序列化为一个字段::

  /* Example for illustration */
  static inline void ctf_top_foo(uint32_t thread_id, ctf_bounded_string_t name)
  {
    CTF_EVENT(
      CTF_LITERAL(uint8_t, 42),
      thread_id,
      name,
      "hello, I was emitted from function: ",
      __func__  /* __func__ is standard since C99 */
    );
  }

如何序列化和发送字段以及如何处理对齐，都可以在底层内部于编译时静态完成。


CTF 顶层通过配置选项 :kconfig:option:`CONFIG_TRACING_CTF` 启用，并且可以在同步和异步模式下与不同的传输后端一起使用。

.. _tools:

跟踪工具
********

Zephyr 支持多种流行的跟踪工具，下面按字母顺序介绍。

Percepio Tracealyzer 支持
=========================

Zephyr 支持 `Percepio Tracealyzer`_，它提供跟踪可视化，可简化分析、生成报告以及实现其他分析功能。Tracealyzer 支持通过各种接口进行跟踪流式传输，也支持快照跟踪，其中事件保存在 RAM 缓冲区中。

.. _Percepio Tracealyzer: https://percepio.com/tracealyzer

.. figure:: percepio_tracealyzer.png
    :align: center
    :alt: Percepio Tracealyzer
    :figclass: align-center
    :width: 80%

启用 Tracealyzer 跟踪后，Zephyr 内核事件会被自动捕获。Tracealyzer 还为应用程序日志记录提供广泛支持，你可以从应用程序代码中调用跟踪库。这样就能将内核事件和应用程序事件一起可视化，例如以数据图或记录变量的状态图形式呈现。要了解更多信息，请参阅随应用程序提供的 Tracealyzer 用户手册。

Percepio TraceRecorder 与流端口
-------------------------------
Tracealyzer 的跟踪库（TraceRecorder）包含在 Zephyr manifest 中，并按照相同的许可证（Apache 2.0）提供。在 prj.conf 中添加以下配置选项即可启用：

.. code-block:: cfg

    CONFIG_TRACING=y
    CONFIG_PERCEPIO_TRACERECORDER=y

或者使用 menuconfig：

* 启用 :menuselection:`Subsystems and OS Services --> Tracing Support`
* 在 :menuselection:`Subsystems and OS Services --> Tracing Support --> Tracing Format` 下，选择 :guilabel:`Percepio Tracealyzer`

配置 TraceRecorder 还需要一些额外的设置。最重要的配置是选择正确的“流端口”。它指定了如何输出跟踪数据。截至 2024 年 7 月，Zephyr 配置系统中提供以下流端口：

* **Ring Buffer：** 跟踪数据保存在循环 RAM 缓冲区中。
* **RTT：** 通过 J-Link 调试探针上的 SEGGER RTT 进行跟踪流式传输。
* **ITM：** 在 Arm Cortex-M 设备上通过 ITM 功能进行跟踪流式传输。
* **Semihost：** 用于在 QEMU 上进行跟踪。将跟踪数据流式传输到主机文件。

在 menuconfig 中的 :menuselection:`Modules --> percepio --> TraceRecorder --> Stream Port` 下选择流端口。

或者只需在 prj.conf 中添加以下选项之一：

.. code-block:: cfg

    CONFIG_PERCEPIO_TRC_CFG_STREAM_PORT_RINGBUFFER=y
    CONFIG_PERCEPIO_TRC_CFG_STREAM_PORT_RTT=y
    CONFIG_PERCEPIO_TRC_CFG_STREAM_PORT_ITM=y
    CONFIG_PERCEPIO_TRC_CFG_STREAM_PORT_ZEPHYR_SEMIHOST=y

请确保只包含这些配置选项中的一个。

流端口模块有各自的配置选项。在 menuconfig 中，可以在 :menuselection:`Modules --> percepio --> TraceRecorder --> (Stream Port) Config` 下找到这些选项。下文介绍每个流端口最重要的选项。

Tracealyzer 快照跟踪（Ring Buffer）
-----------------------------------

“Ring Buffer”流端口将跟踪数据保存在设备上的 RAM 缓冲区中。默认情况下，这是一个循环缓冲区，也就是说它始终包含最新的数据。它用于转储跟踪数据的“快照”，例如通过使用调试器来完成。除非你有数 MB 的 RAM 可供使用，否则这通常只允许记录较短的跟踪，因此它不适合用于性能分析。不过，它结合断点进行调试时可能相当有用。例如，如果在错误处理程序中设置断点，快照跟踪可以显示导致该错误的事件序列。快照跟踪也很容易上手，因为它不依赖任何特定的调试探针或其他开发工具。

要使用 Ring Buffer 选项，请确保在 prj.cnf 中包含以下配置选项：

.. code-block:: cfg

    CONFIG_TRACING=y
    CONFIG_PERCEPIO_TRACERECORDER=y
    CONFIG_PERCEPIO_TRC_START_MODE_START=y
    CONFIG_PERCEPIO_TRC_CFG_STREAM_PORT_RINGBUFFER=y
    CONFIG_PERCEPIO_TRC_CFG_STREAM_PORT_RINGBUFFER_SIZE=<size in bytes>

或者如果使用 menuconfig：

* 启用 :menuselection:`Subsystems and OS Services --> Tracing Support`
* 在 :menuselection:`Subsystems and OS Services --> Tracing Support --> Tracing Format` 下，选择 :guilabel:`Percepio Tracealyzer`
* 在 :menuselection:`Modules --> percepio --> TraceRecorder --> Recorder Start Mode` 下，选择 :guilabel:`Start`
* 在 :menuselection:`Modules --> percepio --> TraceRecorder --> Stream Port` 下，选择 :guilabel:`Ring Buffer`
* 在 :menuselection:`Modules --> percepio --> TraceRecorder --> Ring Buffer Config --> Buffer Size` 下，以字节为单位设置缓冲区大小。

如果 RAM 紧张，可以减小默认缓冲区大小；如果 RAM 有富余并且希望获得更长的跟踪，则可以增大默认缓冲区大小。你也可以通过过滤掉不太重要的事件来优化跟踪配置设置，从而获得更长的跟踪。在 menuconfig 中，请参阅 :menuselection:`Subsystems and OS Services --> Tracing Support --> Tracing Configuration`。

要查看跟踪数据，最简单的方法是启动调试器（west debug）并运行以下 GDB 命令::

    dump binary value trace.bin *RecorderDataPtr

生成的文件通常位于构建文件夹的根目录中，除非指定了其他路径。在 Tracealyzer 中，通过选择 :menuselection:`File --> Open --> Open File` 打开此文件。

使用 SEGGER RTT 进行 Tracealyzer 流式传输
-----------------------------------------

Tracealyzer 内置对 SEGGER RTT 的支持，可以使用 J-Link 探针接收跟踪数据。这样可以记录非常长的跟踪。要将 Zephyr 配置为通过 RTT 向 Tracealyzer 流式传输，请在 prj.cnf 中添加以下配置选项：

.. code-block:: cfg

    CONFIG_TRACING=y
    CONFIG_PERCEPIO_TRACERECORDER=y
    CONFIG_PERCEPIO_TRC_START_MODE_START_FROM_HOST=y
    CONFIG_PERCEPIO_TRC_CFG_STREAM_PORT_RTT=y
    CONFIG_PERCEPIO_TRC_CFG_STREAM_PORT_RTT_UP_BUFFER_SIZE=<size in bytes>

或者如果使用 menuconfig：

* 启用 :menuselection:`Subsystems and OS Services --> Tracing Support`
* 在 :menuselection:`Subsystems and OS Services --> Tracing Support --> Tracing Format` 下，选择 :guilabel:`Percepio Tracealyzer`
* 在 :menuselection:`Modules --> percepio --> TraceRecorder --> Recorder Start Mode` 下，选择 :guilabel:`Start From Host`
* 在 :menuselection:`Modules --> percepio --> TraceRecorder --> Stream Port` 下，选择 :guilabel:`RTT`
* 在 :menuselection:`Modules --> percepio --> TraceRecorder --> RTT Config` 下，以字节为单位设置 RTT “up” 缓冲区的大小。

设置项 :guilabel:`RTT buffer size up` 用于设置 RTT 传输缓冲区的大小。这对吞吐量很重要。默认情况下，该缓冲区相当大，为 5000 字节，以便在板载 J-Link 调试器（它们不如独立探针快）上也能提供不错的性能。如果 RAM 紧张，可以考虑减小此设置。如果使用普通的 J-Link 探针，通常使用小得多的缓冲区就足够了，例如 1 KB 或更小。

在 Tracealyzer 用户手册中了解有关 RTT 流式传输的更多信息。请参阅 Creating and Loading Traces -> Percepio TraceRecorder -> Using TraceRecorder v4.6 or later -> Stream ports（或搜索 RTT）。

使用 Arm ITM 进行 Tracealyzer 流式传输
--------------------------------------

此流端口适用于带有 ITM 单元的 Arm Cortex-M 设备。建议使用支持 10 MHz 或更高 SWO 速度的快速调试探针。要使用此流端口，请应用以下配置选项：

.. code-block:: cfg

    CONFIG_TRACING=y
    CONFIG_PERCEPIO_TRACERECORDER=y
    CONFIG_PERCEPIO_TRC_START_MODE_START=y
    CONFIG_PERCEPIO_TRC_CFG_STREAM_PORT_ITM=y
    CONFIG_PERCEPIO_TRC_CFG_STREAM_PORT_ITM_PORT=1

或者如果使用 menuconfig：

* 启用 :menuselection:`Subsystems and OS Services --> Tracing Support`
* 在 :menuselection:`Subsystems and OS Services --> Tracing Support --> Tracing Format` 下，选择 :guilabel:`Percepio Tracealyzer`
* 在 :menuselection:`Modules --> percepio --> TraceRecorder --> Recorder Start Mode` 下，选择 :guilabel:`Start`
* 在 :menuselection:`Modules --> percepio --> TraceRecorder --> Stream Port` 下，选择 :guilabel:`ITM`
* 在 :menuselection:`Modules --> percepio --> TraceRecorder --> ITM Config` 下，将 ITM 端口设置为 1。

ITM 流端口的主要设置是 ITM 端口（0-31）。Tracealyzer 需要专用通道。端口 0 通常保留给 printf 日志记录，因此默认使用通道 1。

选项 :guilabel:`Use internal buffer` 通常应保持禁用。它会在传输前将数据缓冲到 RAM 中，并把数据传输推迟到周期性的 TzCtrl 线程执行。

主机侧设置取决于所使用的调试探针。更多信息请参阅 Tracealyzer 用户手册。参见 :menuselection:`Creating and Loading Traces --> Percepio TraceRecorder --> Using TraceRecorder v4.6 or later --> Stream ports (or search for ITM)`。

从 QEMU 进行 Tracealyzer 流式跟踪（Semihost）
---------------------------------------------

该流端口专为在 QEMU 中进行 Zephyr 跟踪而设计。这是开始使用跟踪并尝试流式跟踪的一种简便方式，无需快速的调试探针。数据通过半主机机制流式传输到主机文件中。要使用该选项，请应用以下配置选项：

.. code-block:: cfg

    CONFIG_SEMIHOST=y
    CONFIG_TRACING=y
    CONFIG_PERCEPIO_TRACERECORDER=y
    CONFIG_PERCEPIO_TRC_START_MODE_START=y
    CONFIG_PERCEPIO_TRC_CFG_STREAM_PORT_ZEPHYR_SEMIHOST=y

使用 menuconfig

* 启用 :menuselection:`General Architecture Options --> Semihosting support for Arm and RISC-V targets`
* 启用 :menuselection:`Subsystems and OS Services --> Tracing Support`
* 在 :menuselection:`Subsystems and OS Services --> Tracing Support --> Tracing Format` 下，选择 :guilabel:`Percepio Tracealyzer`
* 在 :menuselection:`Modules --> percepio --> TraceRecorder --> Recorder Start Mode` 下，选择 :guilabel:`Start`
* 在 :menuselection:`Modules --> percepio --> TraceRecorder --> Stream Port` 下，选择 :guilabel:`Semihost`

默认情况下，生成的跟踪文件位于构建文件夹根目录下的 :file:`./trace.psf`，除非指定了其他路径。可在 `Percepio Tracealyzer`_ 中选择 :menuselection:`File --> Open --> Open File` 打开该文件。

记录器启动模式
--------------

您可能已经注意到上面 Tracealyzer 示例中的 :guilabel:`Recorder Start Mode` 选项。它决定跟踪何时开始。使用 :guilabel:`Start` 选项时，一旦 TraceRecorder 库完成初始化，跟踪便会直接在启动时开始。在使用 Ring Buffer 和 Semihost 流端口时，建议使用这种方式。

通过 RTT 或 ITM 进行流式传输时，也可以使用 :guilabel:`Start From Host` 或 :guilabel:`Start Await Host`。两者都会监听来自 Tracealyzer 应用程序的启动命令。后一个选项 :guilabel:`Start Await Host` 会使 TraceRecorder 初始化阻塞，直到从 Tracealyzer 应用程序收到启动命令。

为 Tracealyzer 自定义流端口
---------------------------

流端口是 TraceRecorder 内的小型模块，用于定义输出跟踪数据时要调用哪些函数，以及（可选地）如何从 Tracealyzer 读取启动/停止命令。自定义流端口相当容易，可实现您自己的数据传输，而 Tracealyzer 可以通过多种接口接收跟踪流，包括文件、套接字、COM 端口、命名管道等。请注意，TraceRecorder 仓库中还提供额外的流端口模块（例如 lwIP），但它们可能需要修改才能与 Zephyr 配合使用。

了解更多
--------

有关如何入门的更多信息，请参阅 `Tracealyzer Getting Started Guides`_。

.. _Tracealyzer Getting Started Guides: https://percepio.com/tracealyzer/gettingstarted/


用于 Zephyr 的 Percepio View
============================
Percepio View 是一款基于 `Percepio Tracealyzer`_ 的免费跟踪工具，用于调试和验证 Zephyr 应用程序。

.. figure:: percepio_view.webp
    :align: center
    :alt: Percepio View
    :figclass: align-center
    :width: 80%

Percepio View 可以与传统的调试器并排使用，并通过可视化线程、ISR、系统调用以及您自己的“User Events”的实时执行来补充您的调试器。

.. figure:: percepio_view_user_event.webp
    :align: center
    :alt: Percepio View 用户事件
    :figclass: align-center
    :width: 80%


要详细了解 Percepio View、如何入门以及升级选项，请查看 `Percepio 的产品页面 <https://traceviewer.io/get-view/?target=zephyr>`_。

Percepio View 提供快照跟踪，即数据存储在目标 RAM 的环形缓冲区中，并通过常规调试器连接保存到主机。为支持跟踪流式传输，Percepio 提供（付费）升级到 Percepio Profile 或 Percepio Tracealyzer 的选项。无需修改 Zephyr 源代码，只需在 Kconfig 中启用 TraceRecorder 库。Percepio View 可在 Windows 和 Linux 主机上运行。


SEGGER SystemView 支持
======================

Zephyr 为 `SEGGER SystemView`_ 提供内置支持，可在具有所需硬件支持的平台上为任何应用程序启用。

SystemView 使用的负载和格式由应用程序自定义，并依赖 RTT 作为传输方式。较新版本的 SystemView 支持其他传输方式，例如 UART 或使用快照模式（Zephyr 目前仍不支持这两种方式）。

要使用 `SEGGER SystemView`_ 启用跟踪支持，请在构建命令中添加 :ref:`snippet-rtt-tracing`：

    .. zephyr-app-commands::
        :zephyr-app: samples/synchronization
        :board: <board>
        :snippets: rtt-tracing
        :goals: build
        :compact:

SystemView 还可用于事后跟踪，可通过 :kconfig:option:`CONFIG_SEGGER_SYSVIEW_POST_MORTEM_MODE` 启用。在该模式下，系统崩溃后可以使用 ``west attach`` 附加调试器，随后即可将内部 RAM 缓冲区中的最新数据加载到 SystemView 中。

.. figure:: segger_systemview.png
    :align: center
    :alt: SEGGER SystemView
    :figclass: align-center
    :width: 80%

.. _SEGGER SystemView: https://www.segger.com/products/development-tools/systemview/


较新版本的 `SEGGER SystemView`_ 附带了针对 Zephyr 的 API 转换表，但该表并不完整，且与 Zephyr 中当前提供的支持水平不符。要使用最新的 Zephyr API 描述表，请将代码树中提供的文件复制到本地配置目录，以覆盖内置表::

        # On Linux and MacOS
        cp $ZEPHYR_BASE/subsys/tracing/sysview/SYSVIEW_Zephyr.txt ~/.config/SEGGER/

TraceCompass
============

TraceCompass 是一款开源工具，可可视化线程调度和中断等 CTF 事件，有助于在复杂系统中发现意外的交互和资源冲突。

另请参阅 Ericsson 的演示 `Advanced Trouble-shooting Of Real-time Systems <https://wiki.eclipse.org/images/0/0e/TechTalkOnlineDemoFeb2017_v1.pdf>`_。


Perfetto
========

`Perfetto`_ 是 Chrome `Trace Event Format`_ 的 Web 跟踪查看器。无需安装任何工具，它就能显示与 TraceCompass 相同的调度和中断活动：:zephyr_file:`scripts/tracing/ctf2perfetto.py` 仅用 Python 3 即可将 CTF 跟踪转换为该格式::

    $ZEPHYR_BASE/scripts/tracing/ctf2perfetto.py <trace file> -o trace.json

在 https://ui.perfetto.dev 中加载 ``trace.json``，会得到一条时间线，其中每个线程一条泳道，另外还有 ISR 的泳道以及信号量、互斥量和定时器等内核对象的泳道。

同一格式也会由 :ref:`instrumentation` 子系统根据函数调用跟踪写入，因此同一个构建结果可以在同一查看器中以任一方式查看。

TSDL ``metadata`` 默认从跟踪文件旁边读取，这与 babeltrace2 的预期一致，除非 ``--metadata`` 指向其他位置。请使用生成该跟踪的构建所生成的元数据：CTF 记录不携带长度信息，因此元数据未描述的记录无法跳过，转换器会停止并指出其事件 ID，而不是写入不完整的跟踪。

.. _Perfetto: https://perfetto.dev/
.. _Trace Event Format: https://docs.google.com/document/d/1CvAClvFfyA5R-PhYUmn5OOQtYMH4h6I0nSsKchNAySU


用户自定义跟踪
==============

该跟踪格式允许应用程序定义在每个钩子上运行的普通 C 函数，无需编写或派生跟踪头文件。每个 ``sys_port_trace_*`` 钩子都会路由到名为 ``sys_trace_<event>_user()`` 的 ``__weak`` 回调；应用程序只重写自己关心的回调，任何未定义的回调都是空操作。

示例包括：

- 简单的 GPIO 翻转，用于配合外部示波器进行跟踪，同时尽量减少额外的 CPU 负载
- 以其他跟踪系统无法支持的非标准或专有格式生成/输出跟踪数据

回调涵盖线程/调度器、ISR、空闲、系统初始化和睡眠事件，以及 GPIO、定时器、RTIO 和内核对象（信号量、互斥量、条件变量、消息队列、邮箱、事件、轮询、内存 slab 和工作队列）。权威列表（含准确签名）是 :zephyr_file:`subsys/tracing/user/tracing_user.h` 中的 ``sys_trace_*_user`` 声明集合。以下是具有代表性的子集：

.. code-block:: c

   void sys_trace_thread_create_user(struct k_thread *thread);
   void sys_trace_thread_switched_in_user(void);
   void sys_trace_thread_switched_out_user(void);
   void sys_trace_isr_enter_user(void);
   void sys_trace_isr_exit_user(void);
   void sys_trace_idle_user(void);
   void sys_trace_k_sem_give_enter_user(struct k_sem *sem);
   void sys_trace_k_mutex_lock_enter_user(struct k_mutex *mutex, k_timeout_t timeout);

使用 :kconfig:option:`CONFIG_TRACING_USER` 选项启用该格式。:zephyr_file:`tests/subsys/tracing/tracing_user_callbacks` 展示了一个重写对象回调的应用程序。

树外跟踪格式
============

下游模块无需修改 Zephyr 代码树即可提供自己的跟踪格式。将 :kconfig:option:`CONFIG_TRACING_FORMAT_HEADER` （一个无提示的 Kconfig 字符串，由模块的 ``Kconfig`` 通过 ``default`` 赋值）设置为包含路径上某个头文件的名称；当未选择树内格式时，:zephyr_file:`include/zephyr/tracing/tracing.h` 会通过计算得到的 ``#include`` 将其引入。

格式头文件定义它要记录的 ``sys_port_trace_*`` 钩子，并以如下内容结束：

.. code-block:: c

   /* default no-ops for the scheduler/idle/init/named function layer */
   #include <zephyr/tracing/tracing_default_hooks.h>
   /* no-op for every sys_port_trace_* hook this header does not define */
   #include <zephyr/tracing/tracing_hooks.h>

因此，格式只需实现自己关心的钩子。跟踪传输通过 ``TRACING_BACKEND_DEFINE()`` 独立添加（参见 :zephyr_file:`subsys/tracing/include/tracing_backend.h`），因此无论是自定义格式还是自定义后端都无需修改核心代码树。:zephyr_file:`tests/subsys/tracing/tracing_format_module` 是一个完整的示例。

传输后端
********

目前支持以下后端：

* UART
* USB
* 文件（在基于 POSIX 架构的目标上使用原生端口）
* RTT（配合 SystemView）
* RAM（可由调试器读取的缓冲区）

使用跟踪
********

示例 :zephyr_file:`samples/subsys/tracing` 演示了使用不同格式和后端的跟踪。

要开始使用，最简单的方式是结合 :zephyr:board:`native_sim <native_sim>` 端口使用 CTF 格式，并按如下方式构建示例：

.. zephyr-app-commands::
   :tool: all
   :zephyr-app: samples/subsys/tracing
   :board: native_sim
   :gen-args: -DCONF_FILE=prj_native_ctf.conf
   :goals: build

然后可以使用 ``-trace-file`` 选项运行生成的二进制文件，以生成跟踪数据::

    mkdir data
    cp $ZEPHYR_BASE/subsys/tracing/ctf/tsdl/metadata data/
    ./build/zephyr/zephyr.exe -trace-file=data/channel0_0

生成的 CTF 输出可以使用 babeltrace 或 TraceCompass 可视化，只需将工具指向包含元数据和跟踪文件的 ``data`` 目录。

使用 RAM 后端
=============

对于没有可用于跟踪的 I/O（例如 USB 或 UART）但拥有足够 RAM 收集跟踪数据的设备，可以通过配置 :kconfig:option:`CONFIG_TRACING_BACKEND_RAM` 启用 RAM 后端。请调整 :kconfig:option:`CONFIG_RAM_TRACING_BUFFER_SIZE`，以便能够记录满足需求数量的跟踪数据。然后，借助 gdb 等运行时调试器，可以从目标机将该缓冲区取到主机上::

    (gdb) dump binary memory data/channel0_0 <ram_tracing_start> <ram_tracing_end>

生成的 channel0_0 文件必须与其他后端一样，放置在包含 ``metadata`` 文件的目录中。

未来对 LTTng 的借鉴
*******************

目前，这里提供的顶层实现相当简单且功能简陋，并且是从 Zephyr 的 Segger SystemView 调试模块中不必要地复制而来的。

对于像 Zephyr 这样的操作系统，从 Linux 的 LTTng 中汲取灵感，并将顶层实现改为序列化为相同格式是合理的。这样做可以直接复用 TraceCompass 为 Linux 提供的现成分析。另一种方案是针对 Zephyr 定制 TraceCompass 中的 LTTng-analyses。目前正在开展相关工作，以目标无关且开源的方式实现 TraceCompass 对 Zephyr 的可视化。


I/O 分类
========

- 原子推送/产生/写入/入队：

  - 同步：
                  表示在调用返回时数据传输已经完成。

  - 异步：
                  表示在调用返回时数据传输处于挂起或进行中状态。通常使用中断/回调/信号或轮询来确定是否完成。

  - 带缓冲：
                  表示数据传输会被复制并合并成更大的传输。通常用于分摊开销（突发式出队）或缓解抖动（稳态出队）。

  示例：
    - 同步无缓冲
        例如，通过 GPIO 使用 PIO，数据流稳定，不需要额外的 FIFO 内存。抖动低，但效率可能较低（无法分摊写入开销）。

    - 同步带缓冲
        例如 ``fwrite()`` 或入队到 FIFO。当其缓冲区水位超过阈值时，以阻塞方式突发写入 FIFO。突发导致的抖动可能导致错过截止期限。

    - 异步无缓冲
        例如 DMA，或共享内存中的零拷贝。请注意数据冒险、竞态条件等！

    - 异步带缓冲
        例如入队到 FIFO。



- 原子拉取/消费/读取/出队：

  - 同步：
                  表示在调用返回时数据接收已经完成。

  - 异步：
                  表示在调用返回时数据接收处于挂起或进行中状态。通常使用中断/回调/信号或轮询来确定是否完成。

  - 带缓冲：
                  表示数据以大于请求大小的块被复制进来。通常用于分摊等待时间。

  示例：
    - 同步无缓冲
        例如阻塞式读取调用、 ``fread()`` 或 SPI 读取，以及共享内存中的零拷贝。

    - 同步带缓冲
        例如应用了缓存的阻塞式读取调用。如果读取模式表现出空间局部性，这种方式就有意义。

    - 异步无缓冲
        例如共享内存中的零拷贝。请注意数据冒险、竞态条件等！

    - 异步带缓冲
        例如 ``aio_read()`` 或 DMA。



遗憾的是，I/O 可能不是原子的，因此可能需要加锁。如果有多个独立通道可用，则可能不需要加锁。

  - 系统具有非原子写入和一个共享通道
        例如 UART。需要加锁。

        ``lock(); emit(a); emit(b); emit(c); release();``

  - 系统具有非原子写入但有多个通道
        例如多路 UART。如果底层将每个 Zephyr 线程和 ISR 映射到各自的通道，就可以实现无锁，因为每个线程与自身是顺序一致的，从而减少了竞态。

        ``emit(a,thread_id); emit(b,thread_id); emit(c,thread_id);``

  - 系统具有原子写入但只有一个共享通道
        例如 ``native_sim`` 或带有 DMA 的板子。可能需要加锁，也可能不需要。

        ``emit(a ## b ## c); /* Concat to buffer */``

        ``lock(); emit(a); emit(b); emit(c); release(); /* No extra mem */``

  - 系统具有原子写入和多个通道
        例如 native_sim 或带有多通道 DMA 的板子。无锁。

        ``emit(a ## b ## c, thread_id);``


对象跟踪
********

内核还可以维护对象列表，用于跟踪它们的使用情况。目前可以启用以下列表::

  struct k_timer *_track_list_k_timer;
  struct k_mem_slab *_track_list_k_mem_slab;
  struct k_sem *_track_list_k_sem;
  struct k_mutex *_track_list_k_mutex;
  struct k_stack *_track_list_k_stack;
  struct k_msgq *_track_list_k_msgq;
  struct k_mbox *_track_list_k_mbox;
  struct k_pipe *_track_list_k_pipe;
  struct k_queue *_track_list_k_queue;
  struct k_event *_track_list_k_event;

这些全局变量是各列表的头节点，可以借助宏 ``SYS_PORT_TRACK_NEXT`` 遍历它们。例如，要遍历所有已初始化的互斥量，可以这样编写::

  struct k_mutex *cur = _track_list_k_mutex;
  while (cur != NULL) {
    /* Do something */

    cur = SYS_PORT_TRACK_NEXT(cur);
  }

要启用对象跟踪，请启用 :kconfig:option:`CONFIG_TRACING_OBJECT_TRACKING`。请注意，每个列表都可以通过其跟踪配置来启用或禁用。例如，要禁用信号量跟踪，可以禁用 :kconfig:option:`CONFIG_TRACING_SEMAPHORE`。

对象跟踪依赖跟踪配置，因为它目前利用跟踪基础设施来执行跟踪。

API
***


通用
====

.. doxygengroup:: subsys_tracing_apis

线程
====

.. doxygengroup:: subsys_tracing_apis_thread

工作队列
========

.. doxygengroup:: subsys_tracing_apis_work

轮询
====

.. doxygengroup:: subsys_tracing_apis_poll

信号量
======

.. doxygengroup:: subsys_tracing_apis_sem

互斥量
======

.. doxygengroup:: subsys_tracing_apis_mutex

条件变量
========

.. doxygengroup:: subsys_tracing_apis_condvar

队列
====

.. doxygengroup:: subsys_tracing_apis_queue

FIFO
====

.. doxygengroup:: subsys_tracing_apis_fifo

LIFO
====
.. doxygengroup:: subsys_tracing_apis_lifo

栈
===

.. doxygengroup:: subsys_tracing_apis_stack

消息队列
========

.. doxygengroup:: subsys_tracing_apis_msgq

邮箱
====

.. doxygengroup:: subsys_tracing_apis_mbox

管道
====

.. doxygengroup:: subsys_tracing_apis_pipe

堆
===

.. doxygengroup:: subsys_tracing_apis_heap

内存 slab
=========

.. doxygengroup:: subsys_tracing_apis_mslab

定时器
======

.. doxygengroup:: subsys_tracing_apis_timer

Object tracking
===============

.. doxygengroup:: subsys_tracing_object_tracking

系统调用
========

.. doxygengroup:: subsys_tracing_apis_syscall

网络跟踪
========

.. doxygengroup:: subsys_tracing_apis_net

网络套接字跟踪
==============

.. doxygengroup:: subsys_tracing_apis_socket
