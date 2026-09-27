.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth-features:

支持的功能
##########

.. contents::
    :local:
    :depth: 2

自诞生以来，Zephyr 一直高度重视蓝牙（Bluetooth），尤其是低功耗蓝牙（Bluetooth Low Energy，LE）。在多家公司和个人的贡献下，他们参与了现有蓝牙规范开源实现（Linux 的 BlueZ）以及蓝牙 LE 射频硬件的设计与开发，Zephyr 中的协议栈已成长为成熟且功能丰富的实现，详见下文。

* 符合 Bluetooth v5.3 规范

  * 高度可配置

      * 功能、缓冲区大小/数量、协议栈大小等均可配置。

  * 可移植到 Zephyr 支持的所有架构（包括大端和小端、不同对齐方式等）

  * 支持 Host 与 Controller 构建的 :ref:`所有组合 <bluetooth-hw-setup>`：

    * 仅控制器（Controller-only，HCI），通过 UART、SPI、USB 和 IPC 物理传输
    * 仅主机（Host-only），通过 UART、SPI 和 IPC（共享内存）
    * 组合模式（Host + Controller）

* :ref:`可通过 Bluetooth-SIG 认证 <bluetooth-qual>`

  * 在 Nordic Semiconductor 硬件上定期对所有层（控制器和主机，BT Classic 除外）运行一致性测试。

* :ref:`低功耗蓝牙控制器 <bluetooth-ctlr-arch>` （LE 链路层）

  * 角色和连接数量不受限制，支持所有角色
  * 支持 v5.3 规范的所有功能（少数次要项除外）
  * 支持并发多协议
  * 智能调度角色以尽量减少重叠
  * 可移植到任何开放式蓝牙 LE 射频设计，目前支持 Nordic Semiconductor nRF52x 和 nRF53x SoC 系列以及专有射频
  * 支持小端和大端架构，并抽象出硬实时相关细节，使其可封装在硬件特定的模块中
  * 支持基于不同物理传输的控制器（HCI）构建
  * 等时通道（Isochronous Channels）

* :ref:`蓝牙主机 <bluetooth_le_host>`

  * 支持通用访问配置文件（GAP）的所有 LE 角色

    * 外围设备（Peripheral）与中心设备（Central）
    * 观察者（Observer）与广播者（Broadcaster）
    * 支持多种 PHY（2 Mbit/s、Coded）
    * 扩展广播
    * 周期性广播（包括同步传输）

  * GATT（Generic Attribute Profile）

    * 服务器（用作传感器）
    * 客户端（用于连接传感器）
    * 增强型 ATT（EATT）
    * GATT 数据库哈希
    * GATT 多重通知

  * 支持配对，包括 Bluetooth 4.2 引入的 Secure Connections 功能

  * 支持非易失性存储，用于永久保存蓝牙相关设置和数据

  * 支持蓝牙 Mesh

    * 支持 Relay、Friend Node、Low-Power Node（LPN）和 GATT Proxy 功能
    * 支持两种 Provisioning 角色和承载方式（PB-ADV 和 PB-GATT）
    * 包含基础模型（Foundation Models）
    * 高度可配置，适用于 RAM 小至 16 KB 的设备

  * 支持基本蓝牙 BR/EDR（经典蓝牙）

    * 通用访问配置文件（GAP）
    * 逻辑链路控制与适配协议（L2CAP）
    * 串行端口仿真（RFCOMM 协议）
    * 服务发现协议（SDP）

  * 简洁的 HCI 驱动抽象层

    * 3 线（H:5）和 5 线（H:4）UART
    * SPI
    * 通过虚拟 HCI 驱动支持本地控制器

  * 已在多种常见控制器上验证
  * 等时通道（Isochronous Channels）
  * :ref:`LE Audio <bluetooth_le_audio_arch>`
