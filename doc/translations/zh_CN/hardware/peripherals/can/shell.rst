.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _can_shell:

CAN Shell
#########

.. contents::
    :local:
    :depth: 1

概述
****

CAN shell 为 :ref:`shell <shell_api>` 模块提供了一个包含一组子命令的 ``can`` 命令。它允许通过交互式界面测试和探索 :ref:`can_api` 驱动 API，无需编写专用应用。也可以在现有应用中启用 CAN shell，以辅助交互式调试 CAN 问题。

CAN shell 可访问 CAN 控制器的大多数功能，包括查看信息、配置、发送和接收 CAN 帧以及总线恢复。

要启用 CAN shell，必须启用以下 :ref:`Kconfig <kconfig>` 选项：

* :kconfig:option:`CONFIG_SHELL`
* :kconfig:option:`CONFIG_CAN`
* :kconfig:option:`CONFIG_CAN_SHELL`

以下 :ref:`Kconfig <kconfig>` 选项可启用 ``can`` 命令的其他子命令和功能：

* :kconfig:option:`CONFIG_CAN_FD_MODE` 启用 CAN FD 专用子命令（例如用于设置 CAN FD 数据阶段时序的子命令）。
* :kconfig:option:`CONFIG_CAN_RX_TIMESTAMP` 启用接收到的 CAN 帧的时间戳输出。
* :kconfig:option:`CONFIG_CAN_STATS` 启用 ``can show`` 子命令中 CAN 控制器的各项统计信息输出。这还依赖于启用 :kconfig:option:`CONFIG_STATS` 选项。
* :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE` 启用 ``can recover`` 子命令。

例如，为 :zephyr:board:`frdm_k64f` 开发板构建 :zephyr:code-sample:`hello_world` 示例，并启用 CAN shell 和 CAN 统计功能：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: frdm_k64f
   :gen-args: -DCONFIG_SHELL=y -DCONFIG_CAN=y -DCONFIG_CAN_SHELL=y -DCONFIG_STATS=y -DCONFIG_CAN_STATS=y
   :goals: build

有关如何连接 shell 并与之交互的一般说明，请参阅 :ref:`shell <shell_api>` 文档。CAN shell 提供内置帮助（除非禁用了 :kconfig:option:`CONFIG_SHELL_HELP` ）。向 ``can`` 命令或其任意子命令传入 ``-h`` 或 ``--help`` 即可输出内置帮助信息。所有子命令的参数也都支持 Tab 补全。

.. tip::
   所有 CAN shell 子命令都以 CAN 控制器名称作为第一个参数，该参数也支持 Tab 补全。启用 :kconfig:option:`CONFIG_DEVICE_SHELL` 后，可以使用 ``device list`` shell 命令获取所有可用设备的列表。以下示例均使用设备名称 ``can@0`` 。

查看信息
********

可以使用 ``can show`` 子命令查看指定 CAN 控制器的属性，如下所示。这些属性包括 CAN 核心时钟频率、支持的最高比特率、支持的接收过滤器数量、功能特性、当前模式、当前状态、错误计数器、时序限制等：

.. code-block:: console

   uart:~$ can show can@0
   core clock:      144000000 Hz
   max bitrate:     5000000 bps
   max std filters: 15
   max ext filters: 15
   capabilities:    normal loopback listen-only fd
   mode:            normal
   state:           stopped
   rx errors:       0
   tx errors:       0
   timing:          sjw 1..128, prop_seg 0..0, phase_seg1 2..256, phase_seg2 2..128, prescaler 1..512
   timing data:     sjw 1..16, prop_seg 0..0, phase_seg1 1..32, phase_seg2 1..16, prescaler 1..32
   transceiver:     passive/none
   statistics:
     bit errors:    0
       bit0 errors: 0
       bit1 errors: 0
     stuff errors:  0
     crc errors:    0
     form errors:   0
     ack errors:    0
     rx overruns:   0

.. note::
   仅在启用 :kconfig:option:`CONFIG_CAN_STATS` 时才会输出统计信息。

配置
****

CAN shell 支持配置 CAN 控制器的模式和时序，以及启动和停止 CAN 帧处理。

.. note::
   只有在 CAN 控制器停止时才能更改其模式和时序，而停止状态也是系统启动后控制器的初始状态。CAN 控制器的初始模式设为 ``normal`` ，初始时序则根据 :ref:`devicetree` 的 ``bitrate`` 、 ``sample-point`` 、 ``bitrate-data`` 和 ``sample-point-data`` 属性设置。

时序
====

可以使用 ``can bitrate`` 子命令配置经典 CAN 的比特率或 CAN FD 仲裁阶段的比特率，如下所示。比特率以比特每秒为单位指定。

.. code-block:: console

   uart:~$ can bitrate can@0 125000
   setting bitrate to 125000 bps

如果启用了 :kconfig:option:`CONFIG_CAN_FD_MODE` ，则可以使用 ``can dbitrate`` 子命令配置数据阶段的比特率，如下所示。比特率以比特每秒为单位指定。

.. code-block:: console

   uart:~$ can dbitrate can@0 1000000
   setting data bitrate to 1000000 bps

这两个子命令都允许通过位置参数指定可选的采样点和（重）同步跳转宽度（SJW），前者以千分比表示，后者以时间量子为单位。有关更多详细信息，请参阅这些子命令的交互式帮助。

也可以使用 ``can timing`` 和 ``can dtiming`` 子命令配置原始位时序参数。有关所需参数的详细信息，请参阅这些子命令的交互式帮助输出。

模式
====

CAN shell 支持使用 ``can mode`` 子命令设置 CAN 控制器的模式。以下是启用回环模式的示例。

.. code-block:: console

   uart:~$ can mode can@0 loopback
   setting mode 0x00000001

该子命令支持在同一命令行中指定多个模式（例如，使用 ``can mode can@0 fd loopback`` 设置 CAN FD 和回环模式）。厂商特定模式可以用十六进制指定。

启动和停止
==========

按需配置时序和模式后，可以使用 ``can start`` 子命令启动 CAN 控制器，如下所示。这将启用 CAN 帧的接收和发送。

.. code-block:: console

   uart:~$ can start can@0
   starting can@0

重新配置时序或模式之前，需要使用 ``can stop`` 子命令停止 CAN 控制器，如下所示：

.. code-block:: console

   uart:~$ can stop can@0
   stopping can@0

接收
****

要接收 CAN 帧，需要配置一个或多个 CAN 接收过滤器。使用 ``can filter add`` 子命令添加 CAN 接收过滤器，如下所示。该子命令接受一个十六进制格式的 CAN ID，以及一个可选的、同样采用十六进制格式的 CAN ID 掩码，用于设置需要匹配 CAN ID 中的哪些位。有关支持的参数的更多详细信息，请参阅该子命令的交互式帮助输出。

.. code-block:: console

   uart:~$ can filter add can@0 010
   adding filter with standard (11-bit) CAN ID 0x010, CAN ID mask 0x7ff, data frames 1, RTR frames 0, CAN FD frames 0
   filter ID: 0

移除 CAN 接收过滤器时，需要使用返回的过滤器 ID（上例中为 0）。

接收到的、与已添加过滤器匹配的 CAN 帧会打印到 shell 中。以下是几个示例：

.. code-block:: console

   # Dev Flags    ID   Size  Data bytes
   can0  --       010   [8]  01 02 03 04 05 06 07 08
   can0  B-       010  [08]  01 02 03 04 05 06 07 08
   can0  BP       010  [03]  01 aa bb
   can0  --  00000010   [0]
   can0  --       010   [1]  20
   can0  --       010   [8]  remote transmission request

各列的含义如下：

* 设备

  * 接收该帧的设备名称。

* 标志

  * ``B`` ：该帧设置了 CAN FD 波特率切换（BRS）标志。
  * ``P`` ：该帧设置了 CAN FD 错误状态指示（ESI）标志。发送节点处于错误被动状态。
  * ``-`` ：未设置的标志。

* ID

  * ``010`` ：该帧的标准（11 位）CAN ID，以十六进制格式表示，此处为 10h。
  * ``00000010`` ：该帧的扩展（29 位）CAN ID，以十六进制格式表示，此处为 10h。

* 大小

  * ``[8]`` ：帧的数据字节数，以十进制格式表示，此处为包含 8 个数据字节的经典 CAN 帧。
  * ``[08]`` ：帧的数据字节数，以十进制格式表示，此处为包含 8 个数据字节的 CAN FD 帧。

* 数据字节

  * ``01 02 03 04 05 06 07 08`` ：帧的数据字节，以十六进制格式表示，此处为数字 1 到 8。
  * ``remote transmission request`` ：该帧是远程传输请求（RTR）帧，因此不携带数据字节。

.. tip::
   如果启用了 :kconfig:option:`CONFIG_CAN_RX_TIMESTAMP` ，则每行的开头都会添加一个时间戳，该时间戳来自 CAN 控制器中的自由运行时间戳计数器。

可以使用 ``can filter remove`` 子命令移除已配置的 CAN 接收过滤器，如下所示。过滤器 ID 是 ``can filter add`` 子命令返回的 ID（下例中为 0）。

.. code-block:: console

   uart:~$ can filter remove can@0 0
   removing filter with ID 0

另一种方式是使用 ``can dump`` 子命令，该命令会添加可匹配任意接收帧的标准（11 位）和扩展（29 位）CAN 过滤器，启动 CAN 控制器，并将所有接收到的 CAN 帧打印到 shell 中：

.. code-block:: console

   uart:~$ can dump can@0
   dumping CAN RX frames on device can@0, press Ctrl+C to exit

按 Ctrl+C 退出 ``can dump`` 子命令后，添加的过滤器会自动移除，CAN 控制器也会再次停止。

发送
****

可以使用 ``can send`` 子命令将 CAN 帧加入发送队列，如下所示。该子命令接受一个十六进制格式的 CAN ID，还可接受若干个同样以十六进制格式指定的数据字节。有关支持的参数的更多详细信息，请参阅该子命令的交互式帮助输出。

.. code-block:: console

   uart:~$ can send can@0 010 1 2 3 4 5 6 7 8
   enqueuing CAN frame #2 with standard (11-bit) CAN ID 0x010, RTR 0, CAN FD 0, BRS 0, DLC 8
   CAN frame #2 successfully sent

总线恢复
********

可以使用 ``can recover`` 子命令发起手动恢复，以从 CAN 总线关闭状态恢复，如下所示：

.. code-block:: console

   uart:~$ can recover can@0
   recovering, no timeout

该子命令接受一个可选的总线恢复超时时间，单位为毫秒。如果未指定超时时间，该命令将无限期等待，直到总线恢复成功。

.. note::
   仅当启用 :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE` 时，``recover`` 子命令才可用。
