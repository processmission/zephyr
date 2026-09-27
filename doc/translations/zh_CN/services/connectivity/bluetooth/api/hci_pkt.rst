.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bt_hci_pkt:

HCI 数据包辅助程序
##################

用于在 :c:struct:`net_buf_simple` 缓冲区和数据包字节中封装 HCI 命令数据包并解析命令响应的辅助程序，它独立于蓝牙主机和 HCI 驱动接口；此外还提供一个锁步（lockstep）辅助程序，供通过自有传输通道与控制器交换 HCI 命令的 HCI 驱动使用，例如用于厂商特定的控制器初始化。

启用 :kconfig:option:`CONFIG_BT` 时，这两个辅助程序都会包含在每次构建中。锁步辅助程序的头文件与 HCI 驱动 API 放在一起，位于 :file:`include/zephyr/drivers/bluetooth/` 下。

这些并非通用的应用 API：目标用户是 HCI 驱动和蓝牙协议栈内部。需要在运行中的主机之外发送 HCI 命令的应用，应改用更高层的 :c:func:`bt_hci_cmd_alloc`、:c:func:`bt_hci_cmd_send` 和 :c:func:`bt_hci_cmd_send_sync` API，它们会与主机的命令流控机制协同工作。

API 参考
********

.. doxygengroup:: bt_hci_pkt

.. doxygengroup:: bt_hci_lockstep
