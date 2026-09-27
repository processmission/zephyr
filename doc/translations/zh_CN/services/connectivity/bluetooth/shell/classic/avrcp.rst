.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：经典：AVRCP Shell
#######################

本文档介绍如何通过 shell 命令使用蓝牙经典 AVRCP（音频/视频远程控制配置文件）功能。 :code:`avrcp` 命令同时提供控制器（CT）和目标端（TG）角色，用于执行 AVRCP 控制和浏览功能。

有两个子命令： :code:`avrcp ct` 和 :code:`avrcp tg`。 :code:`avrcp ct` 子命令提供 **控制器（CT）** 功能， :code:`avrcp tg` 子命令提供 **目标端（TG）** 功能。

前置条件
--------

在运行 :code:`avrcp` shell 之前，请确保构建中启用了蓝牙经典和 shell。必须先与对端设备建立 ACL BR/EDR 连接（通常通过通用 :code:`bt` shell 命令），然后才能创建 AVRCP 控制连接或浏览连接。

命令
****

除 :code:`avrcp ct register_cb` 和 :code:`avrcp tg register_cb` 之外，所有命令都只能在建立 ACL 连接后使用。

:code:`avrcp` 命令：

.. code-block:: console

   uart:~$ avrcp
   avrcp - Bluetooth AVRCP shell commands
   Subcommands:
     connect                : connect AVRCP
     disconnect             : disconnect AVRCP
     browsing_connect       : connect browsing AVRCP
     browsing_disconnect    : disconnect browsing AVRCP
     ct                     : AVRCP CT shell commands
     tg                     : AVRCP TG shell commands

:code:`avrcp ct` 命令：

.. code-block:: console

   uart:~$ avrcp ct
   ct - AVRCP CT shell commands
   Subcommands:
     register_cb                 : register avrcp ct callbacks
     get_unit                    : get unit info
     get_subunit                 : get subunit info
     get_caps                    : get capabilities <cap_id: company or events>
     play                        : request a play at the remote player
     pause                       : request a pause at the remote player
     register_notification       : register notify <event_id> [playback_interval]
     set_browsed_player          : set browsed player <player_id>
     get_folder_items            : [none]
     change_path                 : [none]
     get_item_attrs              : get item attrs [scope]
     get_total_number_of_items   : get total number of items [scope]
     search                      : search [search_string]
     list_app_attrs              : [none]
     list_app_vals               : List App vals <attr_id>
     get_app_curr                : Get curr player app setting val [attr1] [attr2] ...
     set_app_val                 : Set app setting Val <attr1> <val1> [<attr2> <val2>] ...
     get_app_attr_text           : Get app setting attrs text <attr1> [attr2] ...
     get_app_val_text            : Get setting vals Text <attr_id> <val1> [val2] ...
     inform_displayable_char     : Inform Displayable Character Set <charset_id1> [charset_id2] ...
     inform_batt                 : Inform Battery Status Of CT <Battery status>
     set_absolute_volume         : set absolute volume <volume>
     get_element_attrs           : get element attrs [identifier] [attr1] [attr2] ...
     get_play_status             : [none]
     set_addressed_player        : set addressed player <player_id>
     play_item                   : PlayItem <scope> <uid_hex> <uid_counter>
     add_to_now_playing          : AddToNowPlaying <scope> <uid_hex> <uid_counter>

:code:`avrcp tg` 命令：

.. code-block:: console

   uart:~$ avrcp tg
   tg - AVRCP TG shell commands
   Subcommands:
     register_cb                                : register avrcp tg callbacks
     send_unit_rsp                              : send unit info response
     send_subunit_rsp                           : [none]
     send_get_caps_rsp                          : send get capabilities response [status]
     send_notification_rsp                      : send notify rsp <event_id> <type> [value...]
     send_browsed_player_rsp                    : Send SetBrowsedPlayer response
     send_get_folder_items_rsp                  : send get folder items [status]
     send_change_path_rsp                       : send change path [status]
     send_get_item_attrs_rsp                    : send get item attrs [status]
     send_get_total_number_of_items_rsp         : send get total number of items [status]
     send_search_rsp                            : search [status]
     send_browsing_general_reject               : send browsing general reject [reason]
     send_passthrough_rsp                       : send_passthrough_rsp <op/opvu> <opid> <state>
     send_list_player_app_setting_attrs_rsp     : send attrs rsp <num> [attr_id...]
     send_list_player_app_setting_vals_rsp      : send vals rsp <num> [val_id...]
     send_get_curr_player_app_setting_val_rsp   : send current vals rsp <num_pairs> [attr val]...
     send_set_player_app_setting_val_rsp        : set app setting val rsp [status]
     send_get_player_app_setting_attr_text_rsp  : send get player app setting attr text rsp [status]
     send_get_player_app_setting_val_text_rsp   : send get player app setting val text rsp [status]
     send_inform_displayable_char_rsp           : send displayable char rsp [status]
     send_inform_batt_status_of_ct_rsp          : send inform batt rsp [status]
     send_get_element_attrs_rsp                 : send get element attrs response<large: 1>
     send_absolute_volume_rsp                   : send absolute volume rsp <volume>
     send_get_play_status_rsp                   : send get play status [status]
     send_set_addressed_player_rsp              : send set addressed player rsp [status]
     send_play_item_rsp                         : send play item rsp [status]
     send_add_to_now_playing_rsp                : send add to now playing rsp [status]

.. _avrcp_basic_operations:

基本 AVRCP 操作
***************

演示基本 AVRCP 操作的流程：
 * 双方分别使用 :code:`avrcp ct register_cb` 和 :code:`avrcp tg register_cb` 注册 AVRCP 回调。
 * 使用 :code:`avrcp connect` 创建 AVRCP 连接。
 * CT 使用 :code:`avrcp ct get_caps events` 从 TG 获取能力。
 * CT 使用 :code:`avrcp ct register_notification 0x01` 注册通知。
 * CT 使用 :code:`avrcp ct play` 请求播放控制。
 * CT 使用 :code:`avrcp ct get_play_status` 获取当前播放状态。
 * CT 使用 :code:`avrcp ct get_element_attrs` 获取元素属性（元数据）。
 * CT 使用 :code:`avrcp ct set_absolute_volume 50` 设置音量。
 * CT 使用 :code:`avrcp ct pause` 暂停播放。

.. note::
   CT（控制器）发送命令，TG（目标端）进行响应。对于支持通知的事件，TG 通常会在注册后立即发送 **INTERIM** 响应以指示当前值，并在值实际发生变化后发送 **CHANGED** 响应。

.. tabs::

        .. group-tab:: 设备 A（CT - 控制器）

                .. code-block:: console

                        uart:~$ avrcp ct register_cb
                        AVRCP CT callbacks registered
                        uart:~$ avrcp connect
                        AVRCP CT connected
                        uart:~$ avrcp ct get_caps events
                        GetCapabilities : status=0x04
                        Remote supported EventID = 0x01
                        Remote supported EventID = 0x02
                        Remote supported EventID = 0x0d
                        uart:~$ avrcp ct register_notification 0x01
                        Get capabilities command sent successfully: cap_id=events
                        Sent register notification event_id=0x01
                        AVRCP notification rsp: tid=0x01, status=0x04, event_id=0x01
                         Notification type: INTERIM
                         PLAYBACK_STATUS_CHANGED: status=0x00
                        uart:~$ avrcp ct play
                        Passthrough PRESSED command sent successfully: opid=0x44
                        Passthrough RELEASED command sent successfully: opid=0x44
                        <input `avrcp tg send_passthrough_rsp op play pressed` in TG side>
                        AVRCP passthrough command accepted, operation id = 0x44, state = 0
                        <input `avrcp tg send_passthrough_rsp op play released` in TG side>
                        AVRCP passthrough command accepted, operation id = 0x44, state = 1
                        <input `avrcp tg send_notification_rsp 0x01 changed 1` in TG side>
                        AVRCP notification rsp: tid=0x01, status=0x04, event_id=0x01
                         Notification type: CHANGED
                         PLAYBACK_STATUS_CHANGED: status=0x01
                        uart:~$ avrcp ct get_play_status
                        AVRCP GetPlayStatus
                        getplaystatus : status=0x04
                        GetPlayStatus: len=180000 ms, pos=30000 ms, status=0x01
                         status: PLAYING
                        uart:~$ avrcp ct get_element_attrs
                        Requesting element attributes: identifier=0x0000000000000000, num_attrs=0
                        AVRCP CT get element attrs command sent
                        GetElementAttributes : status=0x04
                        AVRCP GetElementAttributes response received, tid=0x05, num_attrs=7
                         Attr[0]: ID=0x00000001 (TITLE), charset=0x006a, len=11
                           Value: "Test Title"
                         Attr[1]: ID=0x00000002 (ARTIST), charset=0x006a, len=11
                           Value: "Test Artist"
                        uart:~$ avrcp ct set_absolute_volume 50
                        set absolute volume absolute_volume=0x32
                        AVRCP set absolute volume rsp: tid=0x02, status=0x04, volume=0x32
                        uart:~$ avrcp ct pause
                        Passthrough PRESSED command sent successfully: opid=0x46
                        Passthrough RELEASED command sent successfully: opid=0x46
                        <input `avrcp tg send_passthrough_rsp op pause pressed` in TG side>
                        AVRCP passthrough command accepted, operation id = 0x46, state = 0
                        <input `avrcp tg send_passthrough_rsp op pause released` in TG side>
                        AVRCP passthrough command accepted, operation id = 0x46, state = 1

        .. group-tab:: 设备 B（TG - 目标端）

                .. code-block:: console

                        uart:~$ avrcp tg register_cb
                        AVRCP TG callbacks registered
                        <input `avrcp connect` in CT side>
                        AVRCP TG connected
                        <input `avrcp ct get_caps events` in CT side>
                        AVRCP get capabilities command received: cap_id 0x03 (EVENTS_SUPPORTED)
                        uart:~$ avrcp tg send_get_caps_rsp
                        Get capabilities response sent successfully
                        <input `avrcp ct register_notification 0x01` in CT side>
                        receive register notification request event_id=0x01
                        uart:~$ avrcp tg send_notification_rsp 0x01 interim 0
                        Sent notification rsp event_id=0x01 type=interim
                        <input `avrcp ct play` in CT side>
                        receive passthrough command: op_id=0x44 (PLAY)
                        uart:~$ avrcp tg send_passthrough_rsp op play pressed
                        Passthrough opid=0x44 (STANDARD), state=pressed sent successfully
                        uart:~$ avrcp tg send_passthrough_rsp op play released
                        Passthrough opid=0x44 (STANDARD), state=released sent successfully
                        uart:~$ avrcp tg send_notification_rsp 0x01 changed 1
                        Sent notification rsp event_id=0x01 type=changed
                        <input `avrcp ct get_play_status` in CT side>
                        receive get play status request
                        uart:~$ avrcp tg send_get_play_status_rsp
                        GetPlayStatus rsp sent
                        <input `avrcp ct get_element_attrs` in CT side>
                        AVRCP GetElementAttributes command received
                        uart:~$ avrcp tg send_get_element_attrs_rsp 0
                        Sending standard GetElementAttributes response (7 attrs)
                        GetElementAttributes response sent successfully
                        <input `avrcp ct set_absolute_volume 50` in CT side>
                        AVRCP set_absolute_volume_req: tid=0x06, absolute_volume=0x32
                        uart:~$ avrcp tg send_absolute_volume_rsp 50
                        Set absolute volume response sent successfully
                        <input `avrcp ct pause` in CT side>
                        AVRCP passthrough command received: opid = 0x46
                        uart:~$ avrcp tg send_passthrough_rsp op pause pressed
                        send passthrough response
                        uart:~$ avrcp tg send_passthrough_rsp op pause released
                        send passthrough response

AVRCP 连接
**********

AVRCP 配置文件同时支持控制连接和浏览连接。控制连接用于基本远程控制功能，浏览连接则允许浏览媒体内容。

控制连接
========

建立 AVRCP 控制连接：

1. 注册回调（CT 侧）：

.. code-block:: console

   uart:~$ avrcp ct register_cb
   AVRCP CT callbacks registered

2. 注册回调（TG 侧）：

.. code-block:: console

   uart:~$ avrcp tg register_cb
   AVRCP TG callbacks registered

3. 连接 AVRCP：

.. code-block:: console

   uart:~$ avrcp connect
   AVRCP CT connected
   AVRCP TG connected

4. 断开 AVRCP：

.. code-block:: console

   uart:~$ avrcp disconnect
   AVRCP CT disconnected
   AVRCP TG disconnected

浏览连接
========

建立控制连接后，可以发起浏览连接：

1. 连接浏览：

.. code-block:: console

   uart:~$ avrcp browsing_connect
   AVRCP browsing connect request sent
   AVRCP CT browsing connected
   AVRCP TG browsing connected

2. 断开浏览：

.. code-block:: console

   uart:~$ avrcp browsing_disconnect
   AVRCP browsing disconnect request sent
   AVRCP CT browsing disconnected
   AVRCP TG browsing disconnected

基本播放控制
************

从 CT 侧控制播放：

.. tabs::

   .. group-tab:: 播放命令

      .. code-block:: console

         uart:~$ avrcp ct play
         Passthrough PRESSED command sent successfully: opid=0x44
         Passthrough RELEASED command sent successfully: opid=0x44

   .. group-tab:: 暂停命令

      .. code-block:: console

         uart:~$ avrcp ct pause
         Passthrough PRESSED command sent successfully: opid=0x46
         Passthrough RELEASED command sent successfully: opid=0x46

获取能力
********

查询支持的能力：

.. tabs::

   .. group-tab:: 公司 ID

      .. code-block:: console

         uart:~$ avrcp ct get_caps company
         Get capabilities command sent successfully: cap_id=company
         GetCapabilities : status=0x04
         Remote CompanyID = 0x001958

   .. group-tab:: 支持的事件

      .. code-block:: console

         uart:~$ avrcp ct get_caps events
         Get capabilities command sent successfully: cap_id=events
         GetCapabilities : status=0x04
         Remote supported EventID = 0x01
         Remote supported EventID = 0x02
         Remote supported EventID = 0x03
         Remote supported EventID = 0x04
         Remote supported EventID = 0x0d

   .. group-tab:: TG 响应

      .. code-block:: console

         uart:~$ avrcp tg send_get_caps_rsp
         Sending company ID capability rsp: 0x001958

媒体元数据操作
**************

获取元素属性
============

获取当前播放媒体的元数据：

.. tabs::

   .. group-tab:: CT 请求

      .. code-block:: console

         uart:~$ avrcp ct get_element_attrs
         Requesting element attributes: identifier=0x0000000000000000, num_attrs=0
         AVRCP CT get element attrs command sent
         GetElementAttributes : status=0x04
         AVRCP GetElementAttributes response received, tid=0x00, num_attrs=7
          Attr[0]: ID=0x00000001 (TITLE), charset=0x006a, len=11
            Value: "Test Title"
          Attr[1]: ID=0x00000002 (ARTIST), charset=0x006a, len=11
            Value: "Test Artist"
          Attr[2]: ID=0x00000003 (ALBUM), charset=0x006a, len=10
            Value: "Test Album"
          Attr[3]: ID=0x00000004 (TRACK_NUMBER), charset=0x006a, len=1
            Value: "1"
          Attr[4]: ID=0x00000005 (TOTAL_TRACKS), charset=0x006a, len=2
            Value: "10"
          Attr[5]: ID=0x00000006 (GENRE), charset=0x006a, len=4
            Value: "Rock"
          Attr[6]: ID=0x00000007 (PLAYING_TIME), charset=0x006a, len=6
            Value: "240000"

   .. group-tab:: TG 响应

      .. code-block:: console

         uart:~$ avrcp tg send_get_element_attrs_rsp 0
         Sending standard GetElementAttributes response (7 attrs)
         GetElementAttributes response sent successfully

播放状态
========

获取当前播放状态：

.. tabs::

   .. group-tab:: CT 请求

      .. code-block:: console

         uart:~$ avrcp ct get_play_status
         AVRCP GetPlayStatus
         getplaystatus : status=0x04
         GetPlayStatus: len=180000 ms, pos=30000 ms, status=0x01
          status: PLAYING

   .. group-tab:: TG 响应

      .. code-block:: console

         uart:~$ avrcp tg send_get_play_status_rsp
         GetPlayStatus rsp sent

音量控制
********

设置绝对音量：

.. tabs::

   .. group-tab:: CT 设置音量

      .. code-block:: console

         uart:~$ avrcp ct set_absolute_volume 50
         set absolute volume absolute_volume=0x32
         AVRCP set absolute volume rsp: tid=0x01, status=0x04, volume=0x32

   .. group-tab:: TG 响应

      .. code-block:: console

         uart:~$ avrcp tg send_absolute_volume_rsp 50
         Set absolute volume response sent successfully

事件通知
********

注册通知并处理事件：

注册音量变化通知
================

.. tabs::

   .. group-tab:: CT 注册

      .. code-block:: console

         uart:~$ avrcp ct register_notification 0x0d
         Sent register notification event_id=0x0d
         AVRCP notification rsp: tid=0x02, status=0x04, event_id=0x0d
          Notification type: INTERIM
          VOLUME_CHANGED: absolute_volume=0x0a
         AVRCP notify_changed_cb received: event_id=0x0d
          Notification type: CHANGED
          VOLUME_CHANGED: absolute_volume=0x14

   .. group-tab:: TG 发送通知

      .. code-block:: console

         uart:~$ avrcp tg send_notification_rsp 0x0d interim 10
         Sent notification rsp event_id=0x0d type=interim

         uart:~$ avrcp tg send_notification_rsp 0x0d changed 20
         Sent notification rsp event_id=0x0d type=changed

浏览操作
********

设置浏览播放器
==============

.. tabs::

   .. group-tab:: CT 请求

      .. code-block:: console

         uart:~$ avrcp ct set_browsed_player 1
         AVRCP send set browsed player req
         AVRCP set browsed player success, tid = 0
           UID Counter: 1
           Number of Items: 100
           Charset ID: 0x006A
           Folder Depth: 1
           charset_id  : 0x006A
           Get folder Name (hex)  :
         00000000: 4d 75 73 69 63                                   |Music            |

   .. group-tab:: TG 响应

      .. code-block:: console

         uart:~$ avrcp tg send_browsed_player_rsp
         Send set browsed player response, status = 0x04

获取文件夹项
============

.. tabs::

   .. group-tab:: CT 请求

      .. code-block:: console

         uart:~$ avrcp ct get_folder_items
         Sent GetFolderItems command
         AVRCP get folder items success, tid = 1
           UID Counter: 1
           Number of Items: 1
         Media Player Item:
           item_len   : 28
           player_id   : 1
           major_type  : 0x01
           sub_type    : 0x00000000
           play_status : 0x00
           charset_id  : 0x006A
           name_len    : 4
           charset_id  : 0x006A
           Name (hex)  :
         00000000: 44:65:6d:6f                                      |Demo

   .. group-tab:: TG 响应

      .. code-block:: console

         uart:~$ avrcp tg send_get_folder_items_rsp
         TG: Sent GetFolderItems response

播放器应用设置
**************

列出并获取播放器应用设置：

列出可用设置
============

.. tabs::

   .. group-tab:: CT 请求

      .. code-block:: console

         uart:~$ avrcp ct list_app_attrs
         Sent list player app setting attrs
         list player app setting attrs : status=0x04
         attr =0x01 (EQUALIZER)
         attr =0x02 (REPEAT_MODE)

   .. group-tab:: TG 响应

      .. code-block:: console

         uart:~$ avrcp tg send_list_player_app_setting_attrs_rsp 2 0x01 0x02
         TG: Sent list player app setting attrs response

获取当前设置
============

.. tabs::

   .. group-tab:: CT 请求

      .. code-block:: console

         uart:~$ avrcp ct get_app_curr 1 2
         Sent get_curr_player_app_setting_val num=2
         get curr player app setting val : status=0x04
         attr_id :1 val 1
         attr_id :2 val 1

   .. group-tab:: TG 响应

      .. code-block:: console

         uart:~$ avrcp tg send_get_curr_player_app_setting_val_rsp 2 0x01 0x01 0x02 0x02
         TG: Send get curr player app setting val rsp (num=2)
