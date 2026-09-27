.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_shell_audio:

蓝牙：Basic Audio Profile Shell
###############################

本文档介绍如何运行 Basic Audio Profile 功能，包括：

  - 能力与端点发现
  - 音频流端点过程

命令
****

.. code-block:: console

   bap --help
   Subcommands:
      init                   : [ase_sink_count, ase_source_count]
      select_broadcast       : <stream>
      create_broadcast       : [preset <preset_name>] [enc <broadcast_code>]
      start_broadcast        :
      stop_broadcast         :
      delete_broadcast       :
      create_broadcast_sink  : 0x<broadcast_id>
      create_sink_by_name    : <broadcast_name>
      sync_broadcast         : 0x<bis_index> [[[0x<bis_index>] 0x<bis_index>] ...]
                              [bcode <broadcast code> || bcode_str <broadcast code
                              as string>]
      stop_broadcast_sink    : Stops broadcast sink
      term_broadcast_sink    :
      discover               : [dir: sink, source]
      config                 : <direction: sink, source> <index> [loc <loc_bits>]
                              [preset <preset_name>]
      stream_qos             : interval [framing] [latency] [pd] [sdu] [phy] [rtn]
      qos                    : Send QoS configure for Unicast Group
      enable                 : [context]
      connect                : Connect the CIS of the stream
      stop
      list
      print_ase_info         : Print ASE info for default connection
      metadata               : [context]
      start
      disable
      release
      select_unicast         : <stream>
      preset                 : <sink, source, broadcast> [preset]
                              [config
                                    [freq <frequency>]
                                    [dur <duration>]
                                    [chan_alloc <location>]
                                    [frame_len <frame length>]
                                    [frame_blks <frame blocks>]]
                              [meta
                                    [pref_ctx <context>]
                                    [stream_ctx <context>]
                                    [program_info <program info>]
                                    [lang <ISO 639-3 lang>]
                                    [ccid_list <ccids>]
                                    [parental_rating <rating>]
                                    [program_info_uri <URI>]
                                    [audio_active_state <state>]
                                    [bcast_flag]
                                    [extended <meta>]
                                    [vendor <meta>]]
      send                   : Send to Audio Stream [data]
      stats                  : Sets or gets the statistics reporting interval in # of
                              packets (set 0 to disable)
      set_location           : <direction: sink, source> <location bitmask>
      set_context            : <direction: sink, source><context bitmask> <type:
                              supported, available>


.. csv-table:: 状态机转换
   :header: "命令", "依赖", "允许状态", "下一状态"
   :widths: auto

   "init","none","any","none"
   "discover","init","any","any"
   "config","discover","idle/codec-configured/qos-configured","codec-configured"
   "qos","config","codec-configured/qos-configured","qos-configured"
   "enable","qos","qos-configured","enabling"
   "connect","qos/enable","qos-configured/enabling","qos-configured/enabling"
   "[start]","enable/connect","enabling","streaming"
   "disable","enable", "enabling/streaming","disabling"
   "[stop]","disable","disabling","qos-configure/idle"
   "release","config","any","releasing/codec-configure/idle"
   "list","none","any","none"
   "select_unicast","none","any","none"
   "send","enable","streaming","none"

中心设备示例
************

连接并建立接收端流：

.. code-block:: console

   uart:~$ bt init
   uart:~$ bap init
   uart:~$ bt connect <address>
   uart:~$ gatt exchange-mtu
   uart:~$ bap discover sink
   uart:~$ bap config sink 0
   uart:~$ bap qos
   uart:~$ bap enable
   uart:~$ bap connect

连接并建立源端流：

.. code-block:: console

   uart:~$ bt init
   uart:~$ bap init
   uart:~$ bt connect <address>
   uart:~$ gatt exchange-mtu
   uart:~$ bap discover source
   uart:~$ bap config source 0
   uart:~$ bap qos
   uart:~$ bap enable
   uart:~$ bap connect
   uart:~$ bap start

断开连接并释放：

.. code-block:: console

   uart:~$ bap disable
   uart:~$ bap release

外围设备示例
************

监听：

.. code-block:: console

   uart:~$ bt init
   uart:~$ bap init
   uart:~$ bt advertise on

服务器发起的禁用和释放：

.. code-block:: console

   uart:~$ bap disable
   uart:~$ bap release

广播源端示例
************

创建并建立广播源端流：

.. code-block:: console

   uart:~$ bap init
   uart:~$ bap create_broadcast
   uart:~$ bap start_broadcast

停止并释放广播源端流：

.. code-block:: console

   uart:~$ bap stop_broadcast
   uart:~$ bap delete_broadcast


广播接收端示例
**************

扫描并建立广播接收端流。 :code:`bap create_broadcast_sink` 命令将使用现有的周期性广播同步（如果存在），或者开始扫描，并在同步到 BIG 之前，根据提供的广播 ID 同步到周期性广播。

.. code-block:: console

   uart:~$ bap init
   uart:~$ bap create_broadcast_sink 0xEF6716
   No PA sync available, starting scanning for broadcast_id
   Found broadcaster with ID 0xEF6716 and addr R:03:47:95:75:C0:08 and sid 0x00
   Attempting to PA sync to the broadcaster
   PA synced to broadcast with broadcast ID 0xEF6716
   Attempting to sync to the BIG
   Received BASE from sink 0x20019080:
   Presentation delay: 40000
   Subgroup count: 1
   Subgroup 0x20024182:
      Codec Format: 0x06
      Company ID  : 0x0000
      Vendor ID   : 0x0000
      codec cfg id 0x06 cid 0x0000 vid 0x0000 count 16
         Codec specific configuration:
         Sampling frequency: 16000 Hz (3)
         Frame duration: 10000 us (1)
         Channel allocation:
                  Front left (0x00000001)
                  Front right (0x00000002)
         Octets per codec frame: 40
         Codec specific metadata:
         Streaming audio contexts:
            Unspecified (0x0001)
         BIS index: 0x01
            codec cfg id 0x06 cid 0x0000 vid 0x0000 count 6
            Codec specific configuration:
               Channel allocation:
                  Front left (0x00000001)
            Codec specific metadata:
               None
         BIS index: 0x02
            codec cfg id 0x06 cid 0x0000 vid 0x0000 count 6
            Codec specific configuration:
               Channel allocation:
                  Front right (0x00000002)
            Codec specific metadata:
               None
   Possible indexes: 0x01 0x02
   Sink 0x20019110 is ready to sync without encryption
   uart:~$ bap sync_broadcast 0x01


按广播名称扫描并建立广播接收端流
--------------------------------

:code:`bap create_sink_by_name` 命令将开始扫描，并在同步到 BIG 之前，根据提供的广播名称同步到周期性广播。

.. code-block:: console

   uart:~$ bap init
   uart:~$ bap create_sink_by_name "Test Broadcast"
   Starting scanning for broadcast_name
   Found matched broadcast name 'Test Broadcast' with address R:03:47:95:75:C0:08
   Found broadcaster with ID 0xEF6716 and addr R:03:47:95:75:C0:08 and sid 0x00
   Attempting to PA sync to the broadcaster
   PA synced to broadcast with broadcast ID 0xEF6716
   Attempting to create the sink
   Received BASE from sink 0x20019080:
   Presentation delay: 40000
   Subgroup count: 1
   Subgroup 0x20024182:
      Codec Format: 0x06
      Company ID  : 0x0000
      Vendor ID   : 0x0000
      codec cfg id 0x06 cid 0x0000 vid 0x0000 count 16
         Codec specific configuration:
         Sampling frequency: 16000 Hz (3)
         Frame duration: 10000 us (1)
         Channel allocation:
                  Front left (0x00000001)
                  Front right (0x00000002)
         Octets per codec frame: 40
         Codec specific metadata:
         Streaming audio contexts:
            Unspecified (0x0001)
         BIS index: 0x01
            codec cfg id 0x06 cid 0x0000 vid 0x0000 count 6
            Codec specific configuration:
               Channel allocation:
                  Front left (0x00000001)
            Codec specific metadata:
               None
         BIS index: 0x02
            codec cfg id 0x06 cid 0x0000 vid 0x0000 count 6
            Codec specific configuration:
               Channel allocation:
                  Front right (0x00000002)
            Codec specific metadata:
               None
   Possible indexes: 0x01 0x02
   Sink 0x20019110 is ready to sync without encryption
   uart:~$ bap sync_broadcast 0x01

同步到加密广播
--------------

如果广播已加密，可以使用 :code:`bap sync_broadcast` 命令输入广播代码，如下所示：

.. code-block:: console

   Sink 0x20019110 is ready to sync with encryption
   uart:~$ bap sync_broadcast 0x01 bcode 0102030405060708090a0b0c0d0e0f

广播代码可以是 1-16 个值，既可以是字符串，也可以是十六进制值。

.. code-block:: console

   Sink 0x20019110 is ready to sync with encryption
   uart:~$ bap sync_broadcast 0x01 bcode_str thisismycode

停止并释放广播接收端流：

.. code-block:: console

   uart:~$ bap stop_broadcast_sink
   uart:~$ bap term_broadcast_sink

初始化
******

:code:`init` 命令会注册本地 PAC 记录，这是配置流并正确管理所使用能力所必需的。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "none","any","none"

.. code-block:: console

   uart:~$ bap init

发现 PAC 和 ASE
***************

连接后，:code:`discover` 命令会发现 PAC 记录和表示远端端点的 ASE 特征。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "init","any","any"

.. note::

   使用 :code:`gatt exchange-mtu` 命令确保 MTU 配置正确。

.. code-block:: console

   uart:~$ gatt exchange-mtu
   Exchange pending
   Exchange successful
   uart:~$ bap discover [type: sink, source]
   uart:~$ bap discover sink
   conn 0x8256f80: dir Sink (0x01)
   codec cap id 0x06 cid 0x0000 vid 0x0000
     Codec specific capabilities:
       Supported sampling frequencies:
         8000 Hz (0x0001)
         11025 Hz (0x0002)
         16000 Hz (0x0004)
         22050 Hz (0x0008)
         24000 Hz (0x0010)
         32000 Hz (0x0020)
         44100 Hz (0x0040)
         48000 Hz (0x0080)
         88200 Hz (0x0100)
         96000 Hz (0x0200)
         176400 Hz (0x0400)
         192000 Hz (0x0800)
         384000 Hz (0x1000)
       Supported frame durations:
         7.5 ms (0x01)
         10 ms (0x02)
       Supported channel counts:
         1 channel (0x01)
         2 channels (0x02)
       Supported octets per codec frame counts:
         Min: 30
         Max: 155
       Supported max codec frames per SDU: 4
     Codec capabilities metadata:
       Preferred audio contexts:
         Unspecified        (0x0001)
         Conversational     (0x0002)
         Media              (0x0004)
   conn 0x8256f80: dir Sink (0x01)
   codec cap id 0x06 cid 0x0000 vid 0x0000
     Codec specific capabilities:
       Supported sampling frequencies:
         16000 Hz (0x0004)
         32000 Hz (0x0020)
         48000 Hz (0x0080)
       Supported frame durations:
         7.5 ms (0x01)
         10 ms (0x02)
       Supported channel counts:
         1 channel (0x01)
         2 channels (0x02)
       Supported octets per codec frame counts:
         Min: 30
         Max: 120
       Supported max codec frames per SDU: 4
     Codec capabilities metadata:
       Preferred audio contexts:
         Game               (0x0008)
   Supported audio contexts:
     Sink:
       Unspecified        (0x0001)
       Conversational     (0x0002)
       Media              (0x0004)
       Game               (0x0008)
       Instructional      (0x0010)
       Voice assistant    (0x0020)
       Live               (0x0040)
       Sound effects      (0x0080)
     Source:
       Unspecified        (0x0001)
       Conversational     (0x0002)
       Media              (0x0004)
       Game               (0x0008)
       Instructional      (0x0010)
       Voice assistant    (0x0020)
       Live               (0x0040)
       Sound effects      (0x0080)
   Sink location:
     Front left               (0x00000001)
     Front right              (0x00000002)
   Available audio contexts:
     Sink:
       Unspecified        (0x0001)
       Conversational     (0x0002)
       Media              (0x0004)
       Game               (0x0008)
       Instructional      (0x0010)
       Voice assistant    (0x0020)
       Live               (0x0040)
       Sound effects      (0x0080)
     Source:
       Unspecified        (0x0001)
       Conversational     (0x0002)
       Media              (0x0004)
       Game               (0x0008)
       Instructional      (0x0010)
       Voice assistant    (0x0020)
       Live               (0x0040)
       Sound effects      (0x0080)
   Conn: 0x8256f80, Sink #0: ep 0x8288e1c
   Conn: 0x8256f80, Sink #1: ep 0x8289000
   Discover complete: err 0


选择预设
********

:code:`preset` 命令可用于打印默认预设配置或设置其他预设。需要注意的是，它不会更改之前已配置的任何流。

.. code-block:: console

   uart:~$ bap preset
   preset - <sink, source, broadcast> [preset]
            [config
                  [freq <frequency>]
                  [dur <duration>]
                  [chan_alloc <location>]
                  [frame_len <frame length>]
                  [frame_blks <frame blocks>]]
            [meta
                  [pref_ctx <context>]
                  [stream_ctx <context>]
                  [program_info <program info>]
                  [lang <ISO 639-3 lang>]
                  [ccid_list <ccids>]
                  [parental_rating <rating>]
                  [program_info_uri <URI>]
                  [audio_active_state <state>]
                  [bcast_flag]
                  [extended <meta>]
                  [vendor <meta>]]
   uart:~$ bap preset sink
   16_2_1
   codec cfg id 0x06 cid 0x0000 vid 0x0000 count 16
      Codec specific configuration:
         Sampling frequency: 16000 Hz (3)
         Frame duration: 10000 us (1)
         Channel allocation:
                     Front left (0x00000001)
                     Front right (0x00000002)
         Octets per codec frame: 40
      Codec specific metadata:
         Streaming audio contexts:
            Game (0x0008)
   QoS: interval 10000 framing 0x00 phy 0x02 sdu 40 rtn 2 latency 10 pd 40000

   uart:~$ bap preset sink 32_2_1
   32_2_1
   codec cfg id 0x06 cid 0x0000 vid 0x0000 count 16
      Codec specific configuration:
         Sampling frequency: 32000 Hz (6)
         Frame duration: 10000 us (1)
         Channel allocation:
                     Front left (0x00000001)
                     Front right (0x00000002)
         Octets per codec frame: 80
      Codec specific metadata:
         Streaming audio contexts:
            Game (0x0008)
      QoS: interval 10000 framing 0x00 phy 0x02 sdu 80 rtn 2 latency 10 pd 40000


配置预设
********

:code:`bap preset` 命令还可用于配置后续命令使用的预设。可以添加或设置（或重置）任意值。要重置预设，只需在不带 :code:`config` 或 :code:`meta` 参数的情况下运行该命令。这些参数使用分配编号（Assigned Numbers）的值。

.. code-block:: console

   uart:~$ bap preset sink 32_2_1
   32_2_1
   codec cfg id 0x06 cid 0x0000 vid 0x0000 count 16
   data #0: type 0x01 value_len 1
   00000000: 06                                               |.                |
   data #1: type 0x02 value_len 1
   00000000: 01                                               |.                |
   data #2: type 0x03 value_len 4
   00000000: 03 00 00 00                                      |....             |
   data #3: type 0x04 value_len 2
   00000000: 50 00                                            |P.               |
   meta #0: type 0x02 value_len 2
   00000000: 08 00                                            |..               |
   QoS: interval 10000 framing 0x00 phy 0x02 sdu 80 rtn 2 latency 10 pd 40000

   uart:~$ bap preset sink 32_2_1 config freq 10
   32_2_1
   codec cfg id 0x06 cid 0x0000 vid 0x0000 count 16
   data #0: type 0x01 value_len 1
   00000000: 0a                                               |.                |
   data #1: type 0x02 value_len 1
   00000000: 01                                               |.                |
   data #2: type 0x03 value_len 4
   00000000: 03 00 00 00                                      |....             |
   data #3: type 0x04 value_len 2
   00000000: 50 00                                            |P.               |
   meta #0: type 0x02 value_len 2
   00000000: 08 00                                            |..               |
   QoS: interval 10000 framing 0x00 phy 0x02 sdu 80 rtn 2 latency 10 pd 40000

   uart:~$ bap preset sink 32_2_1 config freq 10 meta lang "eng" stream_ctx 4
   32_2_1
   codec cfg id 0x06 cid 0x0000 vid 0x0000 count 16
   data #0: type 0x01 value_len 1
   00000000: 0a                                               |.                |
   data #1: type 0x02 value_len 1
   00000000: 01                                               |.                |
   data #2: type 0x03 value_len 4
   00000000: 03 00 00 00                                      |....             |
   data #3: type 0x04 value_len 2
   00000000: 50 00                                            |P.               |
   meta #0: type 0x02 value_len 2
   00000000: 04 00                                            |..               |
   meta #1: type 0x04 value_len 3
   00000000: 65 6e 67                                         |eng              |
   QoS: interval 10000 framing 0x00 phy 0x02 sdu 80 rtn 2 latency 10 pd 40000

配置编解码器
************

:code:`config` 命令尝试使用预设的编解码器配置为指定方向配置流；该配置可以直接传入，如果省略，则使用默认预设。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "discover","idle/codec-configured/qos-configured","codec-configured"

.. code-block:: console

   uart:~$ bap config <direction: sink, source> <index> [loc <loc_bits>] [preset <preset_name>]
   uart:~$ bap config sink 0
   Setting location to 0x00000000
   ASE config: preset 16_2_1
   stream 0x2000df70 config operation rsp_code 0 reason 0

配置流 QoS
**********

:code:`stream_qos` 设置新的流 QoS。

.. code-block:: console

   uart:~$ bap stream_qos <interval> [framing] [latency] [pd] [sdu] [phy] [rtn]
   uart:~$ bap stream_qos 10

配置 QoS
********

:code:`qos` 命令尝试使用预设配置来配置流 QoS，每个单独的 QoS 参数都可以通过可选参数设置。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "config","qos-configured/codec-configured","qos-configured"

.. code-block:: console

   uart:~$ bap qos

启用
****

:code:`enable` 命令尝试启用之前配置的流。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "qos","qos-configured","enabling"

.. code-block:: console

   uart:~$ bap enable [context]
   uart:~$ bap enable Media

连接
****

:code:`connect` 命令尝试连接之前配置的流。接收端流必须由单播服务器启动，源端流必须由单播客户端启动。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "qos/enable","qos-configured/enabling","qos-configured/enabling"

.. code-block:: console

   uart:~$ bap connect

启动
****

:code:`start` 命令仅在启动源端流时需要。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "enable/connect","enabling","streaming"

.. code-block:: console

   uart:~$ bap start

禁用
****

:code:`disable` 命令尝试禁用之前启用的流；如果远端对端接受，则还会启动 ISO 断开过程。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "enable","enabling/streaming","disabling"

.. code-block:: console

   uart:~$ bap disable

停止
****

:code:`stop` 命令仅在作为接收端时需要使用，因为它会向源端表明协议栈已准备好停止接收数据。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "disable","disabling","qos-configure/idle"

.. code-block:: console

   uart:~$ bap stop

释放
****

:code:`release` 命令释放当前流及其配置。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "config","any","releasing/codec-configure/idle"

.. code-block:: console

   uart:~$ bap release

列出
****

:code:`list` 命令列出可用的流。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "none","any","none"

.. code-block:: console

   uart:~$ bap list
   *0: ase 0x01 dir 0x01 state 0x01

选择单播
********

:code:`select_unicast` 命令将单播流设置为默认流。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "none","any","none"

.. code-block:: console

   uart:~$ bap select <ase>
   uart:~$ bap select 0x01
   Default stream: 1

要选择广播流：

.. code-block:: console

   uart:~$ bap select 0x01 broadcast
   Default stream: 1 (broadcast)

发送
****

:code:`send` 命令通过 BAP 流发送数据。

.. csv-table:: 状态机转换
   :header: "Depends", "Allowed States", "Next States"
   :widths: auto

   "enable","streaming","none"

.. code-block:: console

   uart:~$ bap send [count]
   uart:~$ bap send
   Audio sending...
