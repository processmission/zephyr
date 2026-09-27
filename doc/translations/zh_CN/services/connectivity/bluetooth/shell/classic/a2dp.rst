.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：A2DP Shell
################

:code:`a2dp` 命令公开部分 A2DP API。

以下示例假设您已连接两台设备。

.. _a2dp_conn_disconn:

A2DP 连接
*********

演示创建 A2DP 连接的流程：

* 双方使用 :code:`a2dp register_cb` 注册 A2DP 回调。
* 任一方都可以使用 :code:`a2dp connect` 建立 A2DP 连接，这将创建 AVDTP 信令通道。
* 任一方都可以使用 :code:`a2dp get_conn` 获取 ACL 连接。
* 任一方都可以使用 :code:`a2dp disconnect` 断开 A2DP 连接。

.. tabs::

        .. group-tab:: 设备 A（发起者）

                .. code-block:: console

                        uart:~$ a2dp register_cb
                        success
                        uart:~$ a2dp connect
                        Bonded with XX:XX:XX:XX:XX:XX
                        Security changed: XX:XX:XX:XX:XX:XX level 2
                        a2dp connected
                        uart:~$ a2dp get_conn
                        a2dp conn is: 0xXXXXXXXX
                        uart:~$ a2dp disconnect
                        a2dp disconnected

        .. group-tab:: 设备 B（接受者）

                .. code-block:: console

                        uart:~$ a2dp register_cb
                        success
                        <input `a2dp connect` in initiator side>
                        Connected: XX:XX:XX:XX:XX:XX
                        Bonded with XX:XX:XX:XX:XX:XX
                        Security changed: XX:XX:XX:XX:XX:XX level 2
                        a2dp connected
                        <input `a2dp disconnect` in initiator side>
                        a2dp disconnected

.. _a2dp_basic_operations:

基本 A2DP 操作
**************

演示基本 A2DP 操作的流程：

* 源端和接收端分别使用 :code:`a2dp register_ep source sbc` 和 :code:`a2dp register_ep sink sbc` 注册流端点。
* 基于 :ref:`a2dp 连接 <a2dp_conn_disconn>` 创建 A2DP 连接。
* 发起者使用 :code:`a2dp discover_peer_eps 0x0104` 发现远端设备的流端点。
* 发起者在发现远端端点后使用 :code:`a2dp configure` 配置流以创建流。
* 发起者使用 :code:`a2dp establish` 建立流。
* 接收端使用 :code:`a2dp send_delay_report` 发送延迟报告。
* 发起者使用 :code:`a2dp start` 启动媒体。
* 源端使用 :code:`a2dp send_media` 测试媒体发送，发送一个测试数据包数据。
* 发起者使用 :code:`a2dp suspend` 暂停媒体。
* 发起者使用 :code:`a2dp release` 释放媒体。

.. note::
   在以下日志中，发起者对应 A2DP 源端角色，接受者对应 A2DP 接收端角色。延迟报告只能由接收端角色发送，媒体数据只能由源端角色发送。

.. tabs::

        .. group-tab:: 设备 A（发起者）

                .. code-block:: console

                        uart:~$ a2dp register_ep source sbc
                        SBC source endpoint is registered
                        uart:~$ a2dp discover_peer_eps 0x0104
                        endpoint id: 1, (sink), (idle):
                          codec type: SBC
                          sample frequency:
                                  44100
                                  48000
                          channel mode:
                                  Mono
                                  Stereo
                                  Joint-Stereo
                          Block Length:
                                  16
                          Subbands:
                                  8
                          Allocation Method:
                                  Loudness
                          Bitpool Range: 18 - 35
                        uart:~$ a2dp configure
                        success to configure
                        stream configured
                        uart:~$ a2dp establish
                        success to establish
                        stream established
                        <input `a2dp send_delay_report` in sink side>
                        receive delay report and accept
                        received delay report: 1 1/10ms
                        uart:~$ a2dp start
                        success to start
                        stream started
                        uart:~$ a2dp send_media
                        frames num: 1, data length: 160
                        data: 1, 2, 3, 4, 5, 6 ......
                        uart:~$ a2dp suspend
                        success to suspend
                        stream suspended
                        uart:~$ a2dp release
                        success to release
                        stream released

        .. group-tab:: 设备 B（接受者）

                .. code-block:: console

                        uart:~$ a2dp register_ep sink sbc
                        SBC sink endpoint is registered
                        <input `a2dp configure` in initiator side>
                        receive requesting config and accept
                        sample rate 44100Hz
                        stream configured
                        <input `a2dp establish` in initiator side>
                        receive requesting establishment and accept
                        stream established
                        uart:~$ a2dp send_delay_report
                        success to send report delay
                        <input `a2dp start` in initiator side>
                        receive requesting start and accept
                        stream started
                        <input `a2dp send_media` in source side>
                        received, num of frames: 1, data length: 160
                        data: 1, 2, 3, 4, 5, 6 ......
                        <input `a2dp suspend` in initiator side>
                        receive requesting suspend and accept
                        stream suspended
                        <input `a2dp release` in initiator side>
                        receive requesting release and accept
                        stream released

中止操作
********

演示中止操作：

* 基于 :ref:`基本 A2DP 操作 <a2dp_basic_operations>` 建立 A2DP 流。
* 发起者使用 :code:`a2dp abort` 中止流。

.. tabs::

        .. group-tab:: 设备 A（发起者）

                .. code-block:: console

                        uart:~$ a2dp abort
                        success to abort
                        stream released

        .. group-tab:: 设备 B（接受者）

                .. code-block:: console

                        <input `a2dp abort` in initiator side>
                        receive requesting abort and accept
                        stream released

获取配置和重新配置操作
**********************

演示获取配置和重新配置操作：

* 基于 :ref:`基本 A2DP 操作 <a2dp_basic_operations>` 建立 A2DP 流。
* 发起者使用 :code:`a2dp get_config` 获取配置。
* 发起者使用 :code:`a2dp reconfigure` 重新配置流。

.. tabs::

        .. group-tab:: 设备 A（发起者）

                .. code-block:: console

                        uart:~$ a2dp get_config
                        get config result: 0
                        sample rate 44100Hz
                        uart:~$ a2dp reconfigure
                        success to configure
                        stream configured

        .. group-tab:: 设备 B（接受者）

                .. code-block:: console

                        <input `a2dp get_config` in initiator side>
                        receive get config request and accept
                        <input `a2dp reconfigure` in initiator side>
                        receive requesting reconfig and accept
                        sample rate 44100Hz
                        stream configured
