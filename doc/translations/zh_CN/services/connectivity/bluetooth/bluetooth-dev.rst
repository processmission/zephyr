.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth-dev:

应用开发
########

蓝牙应用的开发使用文档中 :ref:`application` 一节介绍的通用基础设施和方法。

本页提供仅与蓝牙应用相关的其他信息。

.. contents::
    :local:
    :depth: 2

线程安全
********

调用蓝牙 API 应当是线程安全的，除非 API 函数的文档中另有说明。确保所有 API 调用都满足这一要求的工作仍在持续进行，但总体目标已在本段中正式说明。欢迎提交朝着该目标推进子系统的 Bug 报告和 Pull Request。

.. _bluetooth-hw-setup:

硬件设置
********

本节介绍使用 Zephyr 构建和调试蓝牙应用时可用的各种选项。您可以根据手头的硬件、自身需求以及偏好的开发方式，选择适合自己的设置。

有以下 3 种可能的设置：

#. :ref:`嵌入式 <bluetooth-hw-setup-embedded>`
#. :ref:`外部控制器 <bluetooth-hw-setup-external-ll>`

   - :ref:`QEMU 主机 <bluetooth-hw-setup-qemu-host>`
   - :ref:`native_sim 主机 <bluetooth-hw-setup-native-sim-host>`

#. :ref:`使用 BabbleSim 仿真的 nRF5x <bluetooth-hw-setup-bsim>`

.. _bluetooth-hw-setup-embedded:

嵌入式
======

这种设置要求所有软件都直接运行在应用所面向的嵌入式平台上。支持 :ref:`bluetooth-configs` 和 :ref:`bluetooth-build-types` 中描述的所有配置与构建类型，但如果使用双芯片配置，或者 SoC 中有多个核心且各核心运行不同的构建类型（例如一个运行主机，另一个运行控制器），则可能需要多次构建 Zephyr。

要使用此设置开始开发，请按照 :ref:`入门指南 <getting_started>` 操作，选择一块支持蓝牙的开发板（如果使用双芯片方案，则可选择多块），然后 :ref:`运行应用 <application_run_board>`）。

即使没有物理传输，也有办法访问主机与控制器之间的 :ref:`HCI <bluetooth-hci>` 流量。有关操作方法，请参见 :ref:`嵌入式 HCI 跟踪 <bluetooth-embedded-hci-tracing>`。

.. _bluetooth-hw-setup-external-ll:

Linux 上带外部控制器的主机
==========================

.. note::
   目前仅在 GNU/Linux 上可用

这种设置依赖于“双芯片” :ref:`配置 <bluetooth-configs>`，它由以下设备组成：

#. 一个在 :ref:`QEMU <application_run_qemu>` 模拟器或 Zephyr 的 :zephyr:board:`native_sim <native_sim>` 本机移植上运行的 :ref:`仅主机 <bluetooth-build-types>` 应用
#. 一个控制器，可以是以下类型之一：

   * 市售控制器
   * Zephyr 的 :ref:`仅控制器 <bluetooth-build-types>` 构建
   * :ref:`虚拟控制器 <bluetooth_virtual_posix>`

.. warning::
   某些外部控制器要么无法接受 Zephyr 默认设置的主机到控制器流控参数（Qualcomm），要么不会从控制器向主机传输任何数据（Realtek）。如果看到类似以下内容的消息::

     <wrn> bt_hci_core: opcode 0x0c33 status 0x12

   在启动所选示例时（请确保在运行示例前已在 :file:`prj.conf` 中启用 :kconfig:option:`CONFIG_LOG`），或者如果从控制器到主机没有数据流动，则需要禁用主机到控制器的流控。为此，请在 :file:`prj.conf` 中设置 ``CONFIG_BT_HCI_ACL_FLOW_CONTROL=n``。

.. _bluetooth-hw-setup-qemu-host:

QEMU
----

您可以在 :ref:`QEMU 模拟器<application_run_qemu>` 上运行 Zephyr 主机，并让它与物理外部蓝牙控制器交互。

有关在此设置中构建和运行应用的完整说明，请参见 :ref:`bluetooth_qemu_native`。

.. _bluetooth-hw-setup-native-sim-host:

native_sim
----------

.. note::
   目前仅在 GNU/Linux 上可用

:zephyr:board:`native_sim <native_sim>` 目标会将您的 Zephyr 应用连同 Zephyr 内核以及一些最小限度的硬件仿真一起构建为原生 Linux 可执行文件。

该可执行文件是一个普通的 Linux 程序，可以像其他程序一样进行调试和插桩，并与物理或虚拟外部控制器通信。请参见：

- 物理控制器请参见 :ref:`bluetooth_qemu_native`
- 虚拟控制器请参见 :ref:`bluetooth_virtual_posix`

.. _bluetooth-hw-setup-bsim:

使用 BabbleSim 仿真的 nRF5x
===========================

.. note::
   目前仅在 GNU/Linux 上可用

:ref:`nrf52_bsim <nrf52_bsim>` 和 :ref:`nrf5340bsim <nrf5340bsim>` 开发板是仿真目标开发板，它们仿真 nRF52/53 SoC 的必要外设，以便开发和测试低功耗蓝牙应用。这些开发板使用：

   * `BabbleSim`_ 用于仿真 nRF5x 调制解调器和射频环境。
   * POSIX 架构和原生模拟器，用于仿真处理器并在主机上原生运行。
   * `nrf5x 硬件模型 <https://github.com/BabbleSim/ext_NRF_hw_models/>`_

与 :zephyr:board:`native_sim <native_sim>` 目标一样，构建结果是普通的 Linux 可执行文件。有关如何使用一个或多个设备运行仿真的更多信息，请参见 :ref:`这些开发板的文档 <nrf52bsim_build_and_run>`。

使用 :ref:`nrf52_bsim <nrf52_bsim>` 时，通常会进行 :ref:`组合构建 <bluetooth-build-types>`，但也可以在一个仿真设备中使用 :zephyr:code-sample:`bluetooth_hci_uart` 示例之一构建控制器，并在另一个仿真设备中使用 H4 驱动而不是集成控制器来构建主机。

使用 :ref:`nrf5340bsim <nrf5340bsim>` 时，可以采用两种构建方式：控制器和主机都运行在其网络核心上；或者网络核心只运行控制器，应用核心运行主机和您的应用，并通过 IPC 传输 HCI。

初始化
******

蓝牙子系统使用 :c:func:`bt_enable` 函数初始化。调用者应检查返回码中是否有错误，以确保该函数成功执行。如果将函数指针传递给 :c:func:`bt_enable`，则初始化会异步进行，并通过所给的函数通知完成。

蓝牙应用示例
************

下面展示了一个简单的蓝牙信标应用。该应用初始化蓝牙子系统并启用不可连接广播，实际上充当低功耗蓝牙广播者。

.. literalinclude:: ../../../../samples/bluetooth/beacon/src/main.c
   :language: c
   :lines: 19-
   :linenos:

信标示例所用的关键 API 是 :c:func:`bt_enable`，用于初始化蓝牙，以及 :c:func:`bt_le_adv_start`，用于开始广播特定的广播数据与扫描响应数据组合。

更多示例
********

更多 :zephyr:code-sample-category:`蓝牙应用示例 <bluetooth>` 可在 ``samples/bluetooth/`` 中找到。

.. _BabbleSim: https://babblesim.github.io/
