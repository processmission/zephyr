.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ocpp_interface:

开放充电点协议（OCPP）
######################

.. contents::
    :local:
    :depth: 2

概述
****

开放充电点协议（OCPP，Open Charge Point Protocol）是一种应用协议，用于充电点（电动汽车充电站）与中央管理系统（也称为充电站网络）之间的通信。OCPP 是由 The Open Charge Alliance 定义的 `standard <https://openchargealliance.org/protocols/open-charge-point-protocol/>`_，其目标是为充电点与中央系统之间的通信方式提供统一方案。借助该协议，任何中央系统都可以与任何充电点相连，而与厂商无关。

Zephyr 提供基于 websocket API 构建的 OCPP 充电点（CP）库，其载荷采用 json 格式。可通过 :kconfig:option:`CONFIG_OCPP` Kconfig 选项启用该库。目前支持带基本核心配置文件的 OCPP 1.6。

OCPP 充电点（CP）需要连接中央系统（CS）服务器，出于开发目的可在本地搭建开源的 SteVe 服务器，搭建详情见 `SteVe server <https://github.com/steve-community/steve/blob/master/README.md>`_。

Zephyr OCPP CP 库实现了以下内容：

* 处理 socket 连接和事件的引擎
* 用于封装／解析载荷的 OCPP 核心功能，以及 OCPP 事件的用户通知和心跳通知

用法示例
********

使用充电点和中央系统的整体信息初始化 ocpp 库。在初始化 OCPP 库之前，应先准备好以太网、wifi 或 modem 网络接口。需要在 ocpp_init 中传入填充好的 CP、CS 结构和用户回调。

.. code-block:: c

   static int user_notify_cb(ocpp_notify_reason_t reason,
                             ocpp_io_value_t *io,
                             void *user_data)
   {

        switch (reason) {
        case OCPP_USR_GET_METER_VALUE:
                ...
                break;

        case OCPP_USR_START_CHARGING:
                ...
                break;

                ...
                ...
   }

   /* OCPP configuration */
   ocpp_cp_info_t cpi = { "basic", "zephyr", .num_of_con = 1};
   ocpp_cs_info_t csi =  {"192.168.1.3",   /* ip address */
                          "/steve/websocket/CentralSystemService/zephyr",
                          8180,
                          AF_INET};

   ret = ocpp_init(&cpi, &csi, user_notify_cb, NULL);

在进行任何 ocpp 事务 API 调用之前，必须为每个物理连接器打开一个唯一的会话。

.. code-block:: c

   ocpp_session_handle_t sh = NULL;
   ret = ocpp_session_open(&sh);

idtag 是电动汽车用户的身份认证令牌，应与中央系统上的列表匹配。必须调用授权请求，以确保在开始向电动汽车传输能量之前 idtag 有效（如果充电请求源自本地充电点）。

.. code-block:: c

    ocpp_auth_status_t status;
    ret = ocpp_authorize(sh, idtag, &status, 500);

成功时，授权状态可在 status 中获取。

除了本地充电点外，充电请求也可能来自中央系统，此时会通过回调以 OCPP_USR_START_CHARGING 通知用户，这种情况下授权请求调用是可选的。当中央系统准备好向电动汽车供电时，使用 ocpp_start_transaction 将包含电表读数和连接器 id 的启动事务通知给中央系统。

.. code-block:: c

   const int idcon = 1;
   const int mval = 25; //meter reading in wh
   ret = ocpp_start_transaction(sh, mval, idcon, 200);

启动事务成功后，会调用用户回调以从库中获取电表读数。回调不应长时间占用。

API 参考
********

.. doxygengroup:: ocpp_api
