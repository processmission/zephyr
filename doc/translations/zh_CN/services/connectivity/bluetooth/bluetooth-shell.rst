.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_shell:

Shell
#####

蓝牙 Shell 是一种基于 :ref:`shell_api` 模块的应用。它提供了一组命令，可方便地与蓝牙协议栈交互。

有关特定蓝牙功能，另请参阅以下 Shell 文档：

.. toctree::
   :maxdepth: 1

   shell/audio/bap.rst
   shell/audio/bap_broadcast_assistant.rst
   shell/audio/bap_scan_delegator.rst
   shell/audio/cap.rst
   shell/audio/ccp.rst
   shell/audio/csip.rst
   shell/audio/gmap.rst
   shell/audio/mcp.rst
   shell/audio/tbs.rst
   shell/audio/tmap.rst
   shell/audio/pbp.rst
   shell/classic/a2dp.rst
   shell/classic/avrcp.rst
   shell/classic/goep.rst
   shell/classic/hfp.rst
   shell/classic/l2cap.rst
   shell/classic/map.rst
   shell/classic/pbap.rst
   shell/classic/spp.rst
   shell/host/gap.rst
   shell/host/gatt.rst
   shell/host/iso.rst
   shell/host/l2cap.rst

蓝牙 Shell 环境搭建与使用
*************************

首先，需要使用蓝牙 Shell 构建并烧写开发板。具体方法请参阅 :ref:`getting_started`。蓝牙 Shell 本身位于 :zephyr_file:`tests/bluetooth/shell/`。

完成后，使用您常用的串行终端应用连接到 CLI。您应看到以下提示符：

.. code-block:: console

        uart:~$

有关 Shell 常规用法的更多详细信息，请参阅 :ref:`shell_api`。

第一步是启用蓝牙。为此，请使用 :code:`bt init` 命令。系统会打印以下消息，以确认蓝牙已完成初始化。

.. code-block:: console

        uart:~$ bt init
        Bluetooth initialized
        Settings Loaded
        [00:02:26.771,148] <inf> fs_nvs: nvs_mount: 8 Sectors of 4096 bytes
        [00:02:26.771,148] <inf> fs_nvs: nvs_mount: alloc wra: 0, fe8
        [00:02:26.771,179] <inf> fs_nvs: nvs_mount: data wra: 0, 0
        [00:02:26.777,984] <inf> bt_hci_core: hci_vs_init: HW Platform: Nordic Semiconductor (0x0002)
        [00:02:26.778,015] <inf> bt_hci_core: hci_vs_init: HW Variant: nRF52x (0x0002)
        [00:02:26.778,045] <inf> bt_hci_core: hci_vs_init: Controller: Zephyr Bluetooth Controller (0x00) manufacturer 0x05f1 Version 3.2 Build 99
        [00:02:26.778,656] <inf> bt_hci_core: bt_init: No ID address. App must call settings_load()
        [00:02:26.794,738] <inf> bt_hci_core: bt_dev_show_info: Identity: R:EB:BF:36:26:42:09
        [00:02:26.794,769] <inf> bt_hci_core: bt_dev_show_info: HCI: version 5.3 (0x0c) revision 0x0000, manufacturer 0x05f1
        [00:02:26.794,799] <inf> bt_hci_core: bt_dev_show_info: LMP: version 5.3 (0x0c) subver 0xffff


日志记录
********

您可以在运行时按模块配置日志级别。这取决于编译时设置的最大日志级别。要配置日志级别，请使用 :code:`log` 命令。以下是一些示例：

* 列出可用模块及其当前日志级别

.. code-block:: console

        uart:~$ log status

* 禁用 *bt_hci_core* 的日志记录

.. code-block:: console

        uart:~$ log disable bt_hci_core

* 为 *bt_att* 和 *bt_smp* 启用错误日志

.. code-block:: console

        uart:~$ log enable err bt_att bt_smp

* 禁用所有模块的日志记录

.. code-block:: console

        uart:~$ log disable

* 为所有模块启用警告日志

.. code-block:: console

        uart:~$ log enable wrn
