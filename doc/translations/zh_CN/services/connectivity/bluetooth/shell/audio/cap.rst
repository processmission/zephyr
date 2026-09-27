.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：Common Audio Profile Shell
################################

本文档介绍如何运行 Common Audio Profile 功能。

CAP 接受者
**********

接受者通常是资源受限设备，例如头戴式耳机、耳塞或助听器。如果接受者与一个或多个其他 CAP 接受者配对，则可以初始化协调集标识服务（CSIS）实例。

使用 CAP 接受者
===============

蓝牙协议栈初始化（ :code:`bt init` ）后，可以调用 :code:`cap_acceptor init` 注册接受者；该命令会注册 CAS 和 CSIS 服务，并注册回调。

.. code-block:: console


   cap_acceptor --help
   cap_acceptor - Bluetooth CAP acceptor shell commands
   Subcommands:
     init          :Initialize the service and register callbacks [size <int>]
                    [rank <int>] [not-lockable] [sirk <data>]
     lock          :Lock the set
     release       :Release the set [force]
     sirk          :Set the currently used SIRK <sirk>
     get_info      :Get CSIS info
     sirk_rsp      :Set the response used in SIRK requests <accept, accept_enc,
                    reject, oob>

除了初始化 CAS 和 CSIS 之外，还有一些命令可用于锁定和释放 CSIS 实例，以及打印和修改 CSIS 的 SIRK 访问权限。

设置新的 SIRK
-------------

此命令可以修改当前使用的 SIRK。要让新的 RSI 在空口广播，必须再次调用 :code:`bt adv-data` 或 :code:`bt advertise` 来设置新的广播数据。如果启用了 :code:`CONFIG_BT_CSIP_SET_MEMBER_SIRK_NOTIFIABLE`，这还会通知已连接的客户端。

.. code-block:: console

   uart:~$ cap_acceptor sirk 00112233445566778899aabbccddeeff
   SIRK updated

获取当前 SIRK
-------------

此命令可以获取当前使用的 SIRK。

.. code-block:: console

   uart:~$ cap_acceptor get_info
   Info for 0x2003b0c8
           SIRK
   00000000: 20 37 0a 00 95 c4 04 20  00 00 00 00 f1 79 09 00 | 7.....  .....y..|
           Set size: 2
           Rank: 1
           Lockable: true
           Locked: false

CAP 发起者
**********

发起者通常是资源丰富的设备，例如手机或 PC。发起者可以发现 CAP 接受者的 CAS 以及可选的 CSIS 服务。可以读取 CSIS 服务，以获取同一协调集中其他 CAP 接受者的信息。发起者可以对设备集执行流控制过程，无论是临时设备集还是协调设备集，从而提供了一种同时为多个设备设置多个流的简便方法。

使用 CAP 发起者
===============

蓝牙协议栈初始化（ :code:`bt init` ）后，发起者可以通过调用（ :code:`cap_initiator discover` ）发现 CAS 以及可选包含的 CSIS 实例。CAP 发起者还支持作为源端的广播音频。

.. code-block:: console

   uart:~$ cap_initiator --help
   cap_initiator - Bluetooth CAP initiator shell commands
   Subcommands:
     discover          : Discover CAS
     unicast_start     : Unicast Start [csip] [sinks <cnt> (default 1)] [sources
                        <cnt> (default 1)] [conns (<cnt> | all) (default 1)]
     unicast_list      : Unicast list streams
     unicast_update    : Unicast Update <all | stream [stream [stream...]]>
     unicast_stop      : Unicast stop streams [stream [stream [stream...]]] (all by default)
     unicast_cancel    : Unicast cancel current procedure
     ac_1              : Unicast audio configuration 1
     ac_2              : Unicast audio configuration 2
     ac_3              : Unicast audio configuration 3
     ac_4              : Unicast audio configuration 4
     ac_5              : Unicast audio configuration 5
     ac_6_i            : Unicast audio configuration 6(i)
     ac_6_ii           : Unicast audio configuration 6(ii)
     ac_7_i            : Unicast audio configuration 7(i)
     ac_7_ii           : Unicast audio configuration 7(ii)
     ac_8_i            : Unicast audio configuration 8(i)
     ac_8_ii           : Unicast audio configuration 8(ii)
     ac_9_i            : Unicast audio configuration 9(i)
     ac_9_ii           : Unicast audio configuration 9(ii)
     ac_10             : Unicast audio configuration 10
     ac_11_i           : Unicast audio configuration 11(i)
     ac_11_ii          : Unicast audio configuration 11(ii)
     broadcast_start   :
     broadcast_update  : <meta>
     broadcast_stop    :
     broadcast_delete  :
     ac_12             : Broadcast audio configuration 12
     ac_13             : Broadcast audio configuration 13
     ac_14             : Broadcast audio configuration 14

在执行任何流操作之前，设备还必须执行 :code:`bap discover` 操作以发现 ASE 和 PAC 记录。还需要调用 :code:`bap init` 命令。

连接后
------

发现设备上的 CAS 和 CSIS：

.. code-block:: console

   uart:~$ cap_initiator discover
   discovery completed with CSIS


发现设备上的 ASE 和 PAC 记录：

.. code-block:: console

   uart:~$ bap discover
   conn 0x81cc260: #0: codec 0x81d5b28 dir 0x01
   codec 0x06 cid 0x0000 vid 0x0000 count 5
   data #0: type 0x01 len 2
   00000000: f5                                               |.                |
   data #1: type 0x02 len 1
   data #2: type 0x03 len 1
   data #3: type 0x04 len 4
   00000000: 1e 00 f0                                         |...              |
   data #4: type 0x05 len 1
   meta #0: type 0x01 len 2
   00000000: 06                                               |.                |
   dir 1 loc 1
   snk ctx 6 src ctx 6
   Conn: 0x81cc260, Sink #0: ep 0x81e4248
   Conn: 0x81cc260, Sink #1: ep 0x81e46a8
   conn 0x81cc260: #0: codec 0x81d5f00 dir 0x02
   codec 0x06 cid 0x0000 vid 0x0000 count 5
   data #0: type 0x01 len 2
   00000000: f5                                               |.                |
   data #1: type 0x02 len 1
   data #2: type 0x03 len 1
   data #3: type 0x04 len 4
   00000000: 1e 00 f0                                         |...              |
   data #4: type 0x05 len 1
   meta #0: type 0x01 len 2
   00000000: 06                                               |.                |
   dir 2 loc 1
   snk ctx 6 src ctx 6
   Conn: 0x81cc260, Source #0: ep 0x81e5c88
   Conn: 0x81cc260, Source #1: ep 0x81e60e8
   Discover complete: err 0

上述两个命令应对要加入该集合的每个设备执行。要使用多个设备，只需连接更多设备，然后使用 :code:`bt select` 选择要对其执行命令的设备。

所有设备都已连接并执行了各自的发现命令后，可以使用 :code:`cap_initiator unicast_start` 命令使一个或多个流进入流传输状态。

.. code-block:: console

   uart:~$ cap_initiator unicast_start sinks 1 sources 0 conns all
   Setting up 1 sinks and 0 sources on each (2) conn
   Starting 1 streams
   Unicast start completed

要停止所有已启动的流，可以使用 :code:`cap_initiator unicast_stop` 命令。


.. code-block:: console

   uart:~$ cap_initiator unicast_stop all
   Unicast stop completed

进行广播时
----------

要作为 CAP 发起者启动广播，需要完成以下几个步骤：

1. 创建并配置带周期性广播的扩展广播集
2. 创建并配置广播源端
3. 设置扩展广播数据和周期性广播数据

以下命令将使用 16_2_1 预设（由 BAP 定义）设置一个 CAP 广播源端：


.. code-block:: console

   bt init
   bap init
   bt adv-create nconn-nscan ext-adv
   bt per-adv-param
   bap preset broadcast 16_2_1
   cap_initiator ac_12
   bt adv-data dev-name discov
   bt per-adv-data
   cap_initiator broadcast_start
   bt adv-start
   bt per-adv on


广播源端由 :code:`cap_initiator ac_12`、:code:`cap_initiator ac_13` 和 :code:`cap_initiator ac_14` 命令创建，并根据 BAP 定义的音频配置来配置广播源端。然后可以使用 :code:`cap_initiator broadcast_stop` 停止广播源端，或使用 :code:`cap_initiator broadcast_delete` 删除广播源端。

广播源端的元数据可以随时更新，包括在已处于流传输状态时。要更新元数据，可以使用 :code:`cap_initiator broadcast_update` 命令。该命令接受一个数据数组，唯一的要求（除了数据有效之外）是必须设置流传输上下文。例如，要将流传输上下文设置为媒体，可以按如下方式使用该命令：

.. code-block:: console

   cap_initiator broadcast_update 03020400
   CAP Broadcast source updated with new metadata. Update the advertised base via `bt per-adv-data`
   bt per-adv-data

之后应使用 :code:`bt per-adv-data` 命令更新所广播 BASE 中的数据。数据必须采用小端序，因此在上面的示例中，元数据 :code:`03020400` 将元数据项设置为：长度 :code:`03`、类型 :code:`02` （流传输上下文）、值 :code:`0400` （即 :code:`BT_AUDIO_CONTEXT_TYPE_MEDIA`，其数值为 0x）。

CAP 指挥者
**********

指挥者通常与 CAP 发起者位于同一设备，或者位于单独的资源丰富移动设备上，例如手机或智能手表。指挥者可以发现 CAP 接受者的 CAS 以及可选的 CSIS 服务。可以读取 CSIS 服务，以获取同一协调集中其他 CAP 接受者的信息。指挥者可以向 CAP 接受者提供广播源端信息，或协调采集和渲染信息，例如静音或音量状态。

使用 CAP 指挥者
===============

蓝牙协议栈初始化（ :code:`bt init` ）后，指挥者可以通过调用（ :code:`cap_commander discover` ）发现 CAS 以及可选包含的 CSIS 实例。

.. code-block:: console

   cap_commander --help
   cap_commander - Bluetooth CAP commander shell commands
   Subcommands:
     discover                  :Discover CAS
     cancel                    :CAP commander cancel current procedure
     change_volume             :Change volume on all connections <volume>
     change_volume_mute        :Change volume mute state on all connections <mute>
     change_volume_offset      :Change volume offset per connection <volume_offset
                                [volume_offset [...]]>
     change_microphone_mute    :Change microphone mute state on all connections <mute>
     change_microphone_gain    :Change microphone gain per connection <gain
                                [gain [...]]>
     broadcast_reception_start : Start broadcast reception with source
                                 <address: P:XX:XX:XX:XX:XX:XX or R:XX:XX:XX:XX:XX:XX>
                                 <adv_sid> <broadcast_id>
                                 [<pa_interval>] [<sync_bis>] [<metadata>]
     broadcast_reception_stop  : Stop broadcast reception <src_id [...]>
     distribute_broadcast_code : Distribute broadcast code <src_id [...]> <broadcast_code>


在执行任何流操作之前，设备还必须执行 :code:`bap discover` 操作以发现 ASE 和 PAC 记录。还需要调用 :code:`bap init` 命令。

When connected
--------------

发现设备上的 CAS 和 CSIS
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   uart:~$ cap_commander discover
   discovery completed with CSIS


设置所有已连接设备的音量
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   uart:~$ vcp_vol_ctlr discover
   VCP discover done with 1 VOCS and 1 AICS
   uart:~$ cap_commander change_volume 15
   uart:~$ cap_commander change_volume 15
   Setting volume to 15 on 2 connections
   VCP volume 15, mute 0
   VCP vol_set done
   VCP volume 15, mute 0
   VCP flags 0x01
   VCP vol_set done
   Volume change completed

设置一个或多个设备的音量偏移
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
偏移量按连接索引设置，因此连接索引 0 对应第一个偏移量，索引 1 对应第二个偏移量，依此类推：

.. code-block:: console

   uart:~$ bt connect <device A>
   Connected: <device A>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ vcp_vol_ctlr discover
   VCP discover done with 1 VOCS and 1 AICS
   uart:~$
   uart:~$ bt connect <device B>
   Connected: <device B>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ vcp_vol_ctlr discover
   VCP discover done with 1 VOCS and 1 AICS
   uart:~$
   uart:~$ cap_commander change_volume_offset 10
   Setting volume offset on 1 connections
   VOCS inst 0x200140a4 offset 10
   Offset set for inst 0x200140a4
   Volume offset change completed
   uart:~$
   uart:~$ cap_commander change_volume_offset 10 15
   Setting volume offset on 2 connections
   Offset set for inst 0x200140a4
   VOCS inst 0x20014188 offset 15
   Offset set for inst 0x20014188
   Volume offset change completed

将所有已连接设备设置为音量静音
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   uart:~$ bt connect <device A>
   Connected: <device A>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ vcp_vol_ctlr discover
   VCP discover done with 1 VOCS and 1 AICS
   uart:~$
   uart:~$ bt connect <device B>
   Connected: <device B>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ vcp_vol_ctlr discover
   VCP discover done with 1 VOCS and 1 AICS
   uart:~$
   uart:~$ cap_commander change_volume_mute 1
   Setting volume mute to 1 on 2 connections
   VCP volume 100, mute 1
   VCP mute done
   VCP volume 100, mute 1
   VCP mute done
   Volume mute change completed
   uart:~$ cap_commander change_volume_mute 0
   Setting volume mute to 0 on 2 connections
   VCP volume 100, mute 0
   VCP unmute done
   VCP volume 100, mute 0
   VCP unmute done
   Volume mute change completed

将所有已连接设备设置为麦克风静音
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   uart:~$ bt connect <device A>
   Connected: <device A>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ micp_mic_ctlr discover
   MICP discover done with 1 VOCS and 1 AICS
   uart:~$
   uart:~$ bt connect <device B>
   Connected: <device B>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ micp_mic_ctlr discover
   MICP discover done with 1 VOCS and 1 AICS
   uart:~$
   uart:~$ cap_commander change_microphone_mute 1
   Setting microphone mute to 1 on 2 connections
   MICP microphone 100, mute 1
   MICP mute done
   MICP microphone 100, mute 1
   MICP mute done
   Microphone mute change completed
   uart:~$ cap_commander change_microphone_mute 0
   Setting microphone mute to 0 on 2 connections
   MICP microphone 100, mute 0
   MICP unmute done
   MICP microphone 100, mute 0
   MICP unmute done
   Microphone mute change completed

设置一个或多个设备的麦克风增益
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
增益按连接索引设置，因此连接索引 0 对应第一个偏移量，索引 1 对应第二个偏移量，依此类推：

.. code-block:: console

   uart:~$ bt connect <device A>
   Connected: <device A>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ micp_mic_ctlr discover
   MICP discover done with 1 AICS
   uart:~$
   uart:~$ bt connect <device B>
   Connected: <device B>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ micp_mic_ctlr discover
   MICP discover done with 1 AICS
   uart:~$
   uart:~$ cap_commander change_microphone_gain 10
   Setting microphone gain on 1 connections
   AICS inst 0x200140a4 state gain 10, mute 0, mode 0
   Gain set for inst 0x200140a4
   Microphone gain change completed
   uart:~$
   uart:~$ cap_commander change_microphone_gain 10 15
   Setting microphone gain on 2 connections
   Gain set for inst 0x200140a4
   AICS inst 0x20014188 state gain 15, mute 0, mode 0
   Gain set for inst 0x20014188
   Microphone gain change completed

启动和停止广播接收
^^^^^^^^^^^^^^^^^^

.. code-block:: console

   uart:~$ bt connect <device A>
   Connected: <device A>
   uart:~$ bap_init
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ bap_broadcast_assistant discover
   BASS discover done with 1 recv states
   uart:~$ cap_commander broadcast_reception_start <device B> 0 4
   Starting broadcast reception on 1 connection(s)
   Broadcast reception start completed
   uart:~$ cap_commander broadcast_reception_stop 0
   Stopping broadcast reception on 1 connection(s)
   Broadcast reception stop completed

分发广播代码
^^^^^^^^^^^^

.. code-block:: console

   uart:~$ bt connect <device A>
   Connected: <device A>
   uart:~$ bap_init
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ bap_broadcast_assistant discover
   BASS discover done with 1 recv states
   uart:~$ cap_commander broadcast_reception_start <device B> 0 4
   Starting broadcast reception on 1 connection(s)
   Broadcast reception start completed
   uart:~$ cap_commander distribute_broadcast_code 0 "BroadcastCode"
   Distribute broadcast code completed

CAP 切换
********

切换过程允许用户在单播流和广播流之间切换。由于广播流始终是单向的，这些过程仅适用于音频方向从发起者到接受者的流（接收端流）。

使用 CAP 切换过程
=================

蓝牙协议栈初始化（ :code:`bt init` ）后，连接一个或多个远端 CAP 接受者设备并设置好音频流后，可以使用切换过程在单播和广播之间切换。在使用任何切换过程之前，必须已发出并完成 :code:`bap discover`、:code:`cap_initiator discover` 和 :code:`bap_broadcast_assistant discover` 命令。

.. code-block:: console

   cap_handover --help
   cap_handover - Bluetooth CAP handover shell commands
   Subcommands:
     unicast_to_broadcast  : Handover current unicast group to broadcast (unicast
                           group will be deleted) [enc <broadcast_code>] [preset <preset_name>]
     broadcast_to_unicast  : Handover current broadcast source to unicast
                           (broadcast source will be deleted)
                           [conns <count>|all] [preset <preset_name>]



将单播切换为广播
----------------

此命令将一个或多个单播流从单播切换为广播。

.. code-block:: console

   uart:~$ bt init
   uart:~$ bap init
   uart:~$ bt connect <addr>

   # Discover necessary services
   uart:~$ bap discover
   uart:~$ cap_initiator discover
   uart:~$ bap_broadcast_assistant discover

   # Setup unicast audio e.g. using the ac_1
   uart:~$ cap_initiator ac_1

   # Create a non-connectable and non-scannable extended advertising set for broadcast
   uart:~$ bt adv-create nconn-nscan ext-adv
   uart:~$ bt per-adv-param

   # Perform the handover and update the advertising data to contain the broadcast ID
   uart:~$ cap_handover unicast_to_broadcast
   uart:~$ bt adv-data dev-name discov
   uart:~$ bt per-adv-data

   # Enable periodic advertising (extended advertising is enabled as part of handover)
   uart:~$ bt per-adv on

将广播切换为单播
----------------

此命令将一个或多个单播流从广播切换为单播。

.. code-block:: console

   uart:~$ bt init
   uart:~$ bap init
   uart:~$ bt connect <addr>

   # Discover necessary services
   uart:~$ bap discover
   uart:~$ cap_initiator discover
   uart:~$ bap_broadcast_assistant discover

   # Create a non-connectable and non-scannable extended advertising set for broadcast
   uart:~$ bt adv-create nconn-nscan ext-adv
   uart:~$ bt per-adv-param

   # Setup broadcast audio e.g. using the ac_12
   uart:~$ cap_initiator ac_12
   uart:~$ cap_initiator broadcast_start

   # Set advertising data and enable advertising
   uart:~$ bt adv-data dev-name discov
   uart:~$ bt per-adv-data
   uart:~$ bt per-adv on
   uart:~$ bt adv-start

   # Wait for broadcast sink to self-scan, or use broadcast reception to instruct sink to sync

   # Perform the handover
   uart:~$ cap_handover broadcast_to_unicast

   # Terminate the advertiser (optional)
   uart:~$ bt adv-stop
   uart:~$ bt per-adv off
   uart:~$ bt adv-delete
