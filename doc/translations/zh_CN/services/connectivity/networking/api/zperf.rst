.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _zperf:

zperf：网络流量生成器
#####################

.. contents::
    :local:
    :depth: 2

概述
****

zperf 是一个 shell 实用工具，可以在 Zephyr 中生成网络流量，可用于评估网络带宽。

zperf 与 iPerf 2.0.10 及更新版本兼容。要兼容更早的版本，请启用 :kconfig:option:`CONFIG_NET_ZPERF_LEGACY_HEADER_COMPAT`。

zperf 可以在任何应用中启用，Zephyr 中还提供了专门的示例。详情见 :zephyr:code-sample:`zperf 示例应用 <zperf>`。

用法示例
********

如果 Zephyr 充当客户端，则 iPerf 必须以服务器模式运行。例如，进行 UDP 测试时必须使用以下命令行：

.. code-block:: console

   $ iperf -s -l 1K -u -V -B 2001:db8::2

进行 TCP 测试时，命令行如下所示：

.. code-block:: console

   $ iperf -s -l 1K -V -B 2001:db8::2


在 Zephyr 控制台中，可以按如下方式执行 zperf：

.. code-block:: console

   zperf udp upload 2001:db8::2 5001 10 1K 1M


对于 TCP，zperf 命令如下所示：

.. code-block:: console

   zperf tcp upload 2001:db8::2 5001 10 1K 1M


如果在配置文件中指定了 Zephyr 和主机的 IP 地址，则可以按如下方式启动 zperf：

.. code-block:: console

   zperf udp upload2 v6 10 1K 1M


如果要测试 TCP，则如下所示：

.. code-block:: console

   zperf tcp upload2 v6 10 1K 1M


如果 Zephyr 充当服务器，则对 UDP 按如下方式设置下载模式：

.. code-block:: console

   zperf udp download 5001


对 TCP 则如下所示：

.. code-block:: console

   zperf tcp download 5001


在主机侧，如果要测试 UDP，则必须使用以下命令行运行 iPerf：

.. code-block:: console

   $ iperf -l 1K -u -V -c 2001:db8::1 -p 5001


如果要测试 TCP，则使用以下命令行：

.. code-block:: console

   $ iperf -l 1K -V -c 2001:db8::1 -p 5001


如果 Zephyr 无法有序地接收所有数据包，可以使用 -b 选项来限制 iPerf 的输出。

会话管理
********

如果设置了 :kconfig:option:`CONFIG_ZPERF_SESSION_PER_THREAD` 选项，那么当用户在启动上载时提供 ``-a`` 选项，就可以同时进行多个上载会话。每个会话都有自己的工作队列来运行测试。测试结束后仍可查看会话测试结果。可以使用 ``-w`` 选项启动会话，这样工作线程会等待启动信号，从而让所有线程同时启动。这可以避免因 zperf shell 的优先级低于已启动的会话线程而无法运行的情况。如果只有一个上载会话，则并不真正需要 ``-w``。

以下 zperf shell 命令可用于会话管理：

.. csv-table::
   :header: "zperf shell 命令", "描述"
   :widths: auto

   "``jobs``", "显示当前活动或已完成的会话"
   "``jobs all``", "显示已完成会话的统计信息"
   "``jobs clear``", "清除已完成会话的统计信息"
   "``jobs start``", "启动所有等待中的会话"

示例：

.. code-block:: console

   uart:~$ zperf udp upload -a -t 5 192.0.2.2 5001 10 1K 1M
   Remote port is 5001
   Connecting to 192.0.2.2
   Duration:       10.00 s
   Packet size:    1000 bytes
   Rate:           1000 kbps
   Starting...
   Rate:           1.00 Mbps
   Packet duration 7 ms

   uart:~$ zperf jobs all
   No sessions sessions found
   uart:~$ zperf jobs
              Thread    Remaining
   Id  Proto  Priority  time (sec)
   [1] UDP    5            4

   Active sessions have not yet finished
   -
   Upload completed!
   Statistics:             server  (client)
   Duration:               30.01 s (30.01 s)
   Num packets:            3799    (3799)
   Num packets out order:  0
   Num packets lost:       0
   Jitter:                 63 us
   Rate:                   1.01 Mbps       (1.01 Mbps)
   Thread priority:        5
   Protocol:               UDP
   Session id:             1

   uart:~$ zperf jobs all
   -
   Upload completed!
   Statistics:             server  (client)
   Duration:               30.01 s (30.01 s)
   Num packets:            3799    (3799)
   Num packets out order:  0
   Num packets lost:       0
   Jitter:                 63 us
   Rate:                   1.01 Mbps       (1.01 Mbps)
   Thread priority:        5
   Protocol:               UDP
   Session id:             1
   Total 1 sessions done

   uart:~$ zperf jobs clear
   Cleared data from 1 sessions

   uart:~$ zperf jobs
   No active upload sessions
   No finished sessions found

可以像这样使用 ``-w`` 选项来延迟作业的启动。

.. code-block:: console

   uart:~$ zperf tcp upload -a -t 6 -w 192.0.2.2 5001 10 1K
   Remote port is 5001
   Connecting to 192.0.2.2
   Duration:       10.00 s
   Packet size:    1000 bytes
   Rate:           10 kbps
   Waiting "zperf jobs start" command.
   [01:06:51.392,288] <inf> net_zperf: [0] TCP waiting for start

   uart:~$ zperf udp upload -a -t 6 -w 192.0.2.2 5001 10 1K 10M
   Remote port is 5001
   Connecting to 192.0.2.2
   Duration:       10.00 s
   Packet size:    1000 bytes
   Rate:           10000 kbps
   Waiting "zperf jobs start" command.
   Rate:           10.00 Mbps
   Packet duration 781 us
   [01:06:58.064,552] <inf> net_zperf: [0] UDP waiting for start

   uart:~$ zperf jobs start
   -
   Upload completed!
   -
   Upload completed!

   # Note that the output may be garbled as two threads printed
   # output at the same time. Just print out the fresh listing
   # like this.

   uart:~$ zperf jobs all
   -
   Upload completed!
   Statistics:             server  (client)
   Duration:               9.99 s  (10.00 s)
   Num packets:            11429   (11429)
   Num packets out order:  0
   Num packets lost:       0
   Jitter:                 164 us
   Rate:                   9.14 Mbps       (9.14 Mbps)
   Thread priority:        6
   Protocol:               UDP
   Session id:             0
   -
   Upload completed!
   Duration:               10.00 s
   Num packets:            15487
   Num errors:             0 (retry or fail)
   Rate:                   12.38 Mbps
   Thread priority:        6
   Protocol:               TCP
   Session id:             0
   Total 2 sessions done

自定义数据上载
**************

zperf 支持更高级的数据上载剖析：通过 :c:member:`zperf_upload_params.data_loader` 设置自定义数据源。这样就可以生成自定义的数据包内容，而不是发送仅由 ``z`` 字符组成的固定数据包。一个示例用例是测定从外部闪存芯片上载数据的最大吞吐量。

原始 TX 模式
************

zperf 支持原始数据包发送模式，用于测试自定义 L2 帧或厂商专用协议。该模式绕过 UDP/TCP，直接使用数据包 socket 发送原始数据包。

要启用原始 TX 模式，请设置以下 Kconfig 选项：

.. code-block:: kconfig

   CONFIG_NET_SOCKETS_PACKET=y
   CONFIG_NET_ZPERF_RAW_TX=y

最大报头长度可通过 :kconfig:option:`CONFIG_NET_ZPERF_RAW_TX_MAX_HDR_SIZE` 配置（默认值：64 字节）。

在使用原始 TX 模式之前，必须在网络接口上启用 TX 注入模式：

.. code-block:: console

   uart:~$ net iface txinjection 1 on

原始 TX 上载命令的语法为：

.. code-block:: console

   zperf raw upload [-a] <if_index> <header_hex> [<duration_sec>] [<packet_size>] [<rate_kbps>]

位置：

- ``-a``：可选的异步模式标志
- ``if_index``：网络接口索引（例如 1）
- ``header_hex``：用户提供的十六进制字符串报头（厂商元数据 + 帧报头）
- ``duration_sec``：测试持续时间，单位为秒（默认值：1）
- ``packet_size``：包含报头的数据包总长度（默认值：256）
- ``rate_kbps``：目标速率，单位为 Kbps，支持 K/M 后缀（默认值：10）

发送带厂商元数据的原始 802.11 帧的示例：

.. code-block:: console

   uart:~$ zperf raw upload 1 12345678000400030000000088000000ffffffffffa06960e35215a06960e3521500000000aaaa030000000800 10 1024 50M

报头十六进制字符串包含：

- 厂商元数据（本示例中为前 12 个字节）
- 带 LLC/SNAP 的 802.11 QoS 数据报头

载荷（用 ``z`` 字符填充）会自动追加，以达到指定的数据包长度。
