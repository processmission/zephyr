.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth-qual:

认证
####

有关 Bluetooth SIG 认证流程的详细信息，请访问：https://www.bluetooth.com/develop-with-bluetooth/qualify

认证环境搭建
************

.. _AutoPTS automation software:
   https://github.com/auto-pts/auto-pts

Zephyr 蓝牙主机可以使用 Bluetooth 的 PTS（Profile Tuning Suite）软件进行认证。该过程原本是手动进行的，但通过使用 `AutoPTS automation software`_ 实现了自动化。

下文链接的页面更详细地介绍了该环境搭建过程。

.. toctree::
   :maxdepth: 1

   autopts/autopts-win10.rst
   autopts/autopts-linux.rst

ICS 功能
********

.. _Bluetooth Qualification website:
   https://qualification.bluetooth.com/

用于 Host 功能的 Zephyr ICS 文件可在此处下载 :download:`ICS_Zephyr_Bluetooth_Host.pts </tests/bluetooth/qualification/ICS_Zephyr_Bluetooth_Host.pts>`。

使用 `Bluetooth Qualification website`_ 查看和编辑 ICS。

已认证版本
**********

.. _Bluetooth qualification listing 332380:
   https://qualification.bluetooth.com/ListingDetails/332380

Zephyr 项目提供预先认证的蓝牙主机协议栈，方便用户构建经过认证的蓝牙产品。该协议栈可以纳入产品认证设计，提供功能覆盖并减少认证工作量。认证范围可能因版本而异，详细信息可在下文查看。

.. list-table::
  :header-rows: 1

  * - 版本
    - 设计编号
    - 详情
  * - v4.4
    - Q385945
    - `Bluetooth qualification listing 332380`_
