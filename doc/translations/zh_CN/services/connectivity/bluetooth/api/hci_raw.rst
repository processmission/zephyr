.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bt_hci_raw:


HCI RAW 通道
############

概述
****

HCI RAW 通道 API 旨在向远程实体公开 HCI 接口。本地蓝牙控制器将归远程实体所有，不使用主机蓝牙协议栈。RAW API 提供对蓝牙 HCI 驱动发送和接收的数据包的直接访问。

API 参考
********

.. doxygengroup:: hci_raw
