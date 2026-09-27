.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth-arch:

协议栈架构
##########

概述
****

本页介绍 Zephyr 蓝牙协议栈的软件架构。

.. note::
   Zephyr 主要支持低功耗蓝牙（Bluetooth Low Energy，LE），即蓝牙规范中的低功耗版本。Zephyr 也对 BR/EDR 主机的部分功能提供有限支持。

.. _bluetooth-layers:

蓝牙 LE 层
==========

共有 3 个主要层，它们共同构成完整的低功耗蓝牙协议栈：

* **主机**：该层位于应用的正下方，由多个（非实时）网络与传输协议组成，使应用能够以标准且可互操作的方式与对端设备通信。
* **控制器**：控制器实现链路层（Link Layer，LE LL），这是一种底层实时协议，与射频硬件共同提供标准且可互操作的空口通信。链路层负责调度数据包的接收与发送，保证数据交付，并处理所有链路层控制过程。
* **射频硬件**：硬件实现所需的模拟与数字基带功能块，使链路层固件能够在 2.4GHz 频段内收发数据。

.. _bluetooth-hci:

主机控制器接口
==============

`Bluetooth Specification`_ 描述了主机与控制器之间必须采用的通信格式。这种格式称为主机控制器接口（Host Controller Interface，HCI）协议。HCI 可以基于多种不同的物理传输方式实现，例如 UART、SPI 或 USB。该协议定义了主机可以发送给控制器的命令、主机可以预期收到的事件，以及需要通过空口传输的用户数据与协议数据的格式。HCI 确保不同的主机与控制器实现能够以标准方式通信，从而可以将来自不同厂商的主机与控制器组合在一起。

.. _bluetooth-configs:

配置
====

协议的三个独立层以及标准化接口使得主机与控制器可以在不同平台上实现。常用的配置有以下两种：

* **单芯片配置（Single-chip configuration）**：在这种配置中，单个微控制器实现全部三层以及应用本身。这也可以称为片上系统（System-on-Chip，SoC）实现。此时，蓝牙主机与蓝牙控制器通过函数调用和 RAM 中的队列直接通信。蓝牙规范并未规定单芯片配置中 HCI 的实现方式，因此两者之间 HCI 命令、事件和数据流的传递方式可以因实现而异。这种配置非常适合需要较小占用空间和尽可能低功耗的应用与设计，因为一切都在单个 IC 上运行。
* **双芯片配置（Dual-chip configuration）**：这种配置使用两个独立的 IC，其中一个运行应用和主机，另一个包含控制器和射频硬件。这种配置有时也称为连接芯片配置。使用 Zephyr OS 作为控制器时，这种配置允许更广泛地组合各种主机。由于 HCI 可确保主机与控制器实现之间的互操作性（当然也包括 Zephyr 自己的蓝牙主机与控制器），Zephyr 控制器用户可以选用他们喜欢的、运行在任何平台上的任意主机。例如，主机可以是运行在任意支持 Linux 的处理器上的 Linux 蓝牙主机协议栈（BlueZ）。主机处理器当然也可以运行 Zephyr 以及 Zephyr OS 蓝牙主机。反之，将运行 Zephyr 主机的 IC 与不运行 Zephyr 的外部控制器组合使用也同样受支持。

.. _bluetooth-build-types:

构建类型
========

作为 RTOS，Zephyr 软件栈具有高度可配置性，尤其是蓝牙子系统，可以在构建过程中通过多种方式进行配置，以便只包含必需的功能和层，从而降低 RAM 和 ROM 占用以及功耗。以下简要列出了可以从 Zephyr 项目代码库生成的启用蓝牙的各种构建：

* **仅控制器构建（Controller-only build）**：当作为蓝牙控制器构建时，Zephyr 包含链路层和一个特殊应用。该应用因 HCI 所选用的物理传输方式而异：

  * :zephyr:code-sample:`bluetooth_hci_uart`
  * :zephyr:code-sample:`bluetooth_hci_usb`
  * :zephyr:code-sample:`bluetooth_hci_spi`

  该应用充当 UART、SPI 或 USB 外设与控制器子系统之间的桥梁，负责监听 HCI 命令、发送应用数据，并通过事件和接收到的数据进行响应。此类构建会设置以下 Kconfig 选项值：

  * :kconfig:option:`CONFIG_BT` ``=y``
  * :kconfig:option:`CONFIG_BT_HCI` ``=y``
  * :kconfig:option:`CONFIG_BT_HCI_RAW` ``=y``

  控制器本身也需要启用，通常要确保相应的设备树节点已启用。

* **仅主机构建（Host-only build）**：Zephyr OS 主机构建将包含应用和蓝牙主机，以及用于连接外部控制器芯片的 HCI 驱动（UART 或 SPI）。此类构建会设置以下 Kconfig 选项值：

  * :kconfig:option:`CONFIG_BT` ``=y``
  * :kconfig:option:`CONFIG_BT_HCI` ``=y``

  此外，如果平台还支持本地控制器，则需要将其禁用，通常通过禁用相应的设备树节点来实现。同时，还要启用其他某个 HCI 驱动对应的设备树节点，并确保 ``zephyr,bt-hci`` 设备树 chosen 属性指向它。

  除用于仅控制器构建的示例外，``samples/bluetooth`` 中的所有示例都可以按仅主机方式构建

* **组合构建（Combined build）**：包含应用、主机和控制器，专用于单芯片（SoC）配置。此类构建会设置以下 Kconfig 选项值：

  * :kconfig:option:`CONFIG_BT` ``=y``
  * :kconfig:option:`CONFIG_BT_HCI` ``=y``

  控制器本身也需要启用，通常要确保相应的设备树节点已启用。

  除用于仅控制器构建的示例外，``samples/bluetooth`` 中的所有示例都可以按组合方式构建

下图展示了使用 Zephyr 组合构建（即在烧录到芯片上的同一固件映像中同时包含蓝牙主机和控制器的构建）时的 SoC 或单芯片配置：

.. figure:: img/ble_cfg_single.png
   :align: center
   :alt: 单芯片上的蓝牙组合构建

   单芯片配置上的组合构建

使用连接芯片或双芯片配置时，可以有多种主机与控制器组合，下面展示了其中一些：

.. figure:: img/ble_cfg_dual.png
   :align: center
   :alt: 蓝牙双芯片配置构建

   双芯片配置上的仅主机和仅控制器构建

使用 Zephyr 主机时（图中左侧），必须使用不同的配置构建两个 Zephyr OS 实例，生成两个独立的映像，并分别烧录到各自的芯片中。主机构建映像包含应用、蓝牙主机以及所选的 HCI 驱动（UART 或 SPI）；控制器构建则运行 :zephyr:code-sample:`bluetooth_hci_uart` 或 :zephyr:code-sample:`bluetooth_hci_spi` 应用，以提供与蓝牙控制器之间的接口。

如图中右侧所示，这种配置并不限于使用 Zephyr OS 主机。实际上，可以使用众多现有 GNU/Linux 发行版之一（其中大多数都包含 Linux 自带的蓝牙主机 BlueZ），通过 UART 或 USB 将其连接到一个或多个 Zephyr OS 控制器构建实例。当应用需要多个蓝牙射频同时工作但共享同一主机协议栈时，作为主机的 BlueZ 可同时支持多个控制器。

源码树布局
**********

协议栈在源码树中的划分如下：

:zephyr_file:`subsys/bluetooth/host`
  :ref:`主机协议栈 <bluetooth_le_host>`。这是处理 HCI 命令和事件以及跟踪连接的地方。L2CAP、ATT 和 SMP 等核心协议的实现也位于此处。

:zephyr_file:`subsys/bluetooth/controller`
  :ref:`低功耗蓝牙控制器 <bluetooth-ctlr-arch>` 实现。实现了 HCI 的控制器侧、链路层以及对射频收发器的访问。

:zephyr_file:`include/zephyr/bluetooth/`
  :ref:`公共 API <bluetooth_api>` 头文件。这些是应用为了使用蓝牙功能而需要包含的头文件。

:zephyr_file:`drivers/bluetooth/`
  HCI 传输驱动。每种 HCI 传输都需要自己的驱动。例如，两种常见的 UART 传输协议（3-Wire 和 5-Wire）各有自己的驱动。

:zephyr_file:`samples/bluetooth/`
  :zephyr:code-sample-category:`蓝牙示例代码 <bluetooth>`。这是开始蓝牙应用开发的良好参考。

:zephyr_file:`tests/bluetooth/`
  测试应用。这些应用用于验证蓝牙协议栈的功能，但不一定是示例代码的最佳来源（请参见 :zephyr_file:`samples/bluetooth`）。

:zephyr_file:`doc/services/connectivity/bluetooth/`
  其他文档，例如 PICS 文档。

.. _Bluetooth Specification: https://www.bluetooth.com/specifications/bluetooth-core-specification
