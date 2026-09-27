.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _eeprom_shell:

EEPROM Shell
############

.. contents::
    :local:
    :depth: 1

概述
****

EEPROM shell 为 :ref:`shell <shell_api>` 模块提供了一个带有一组子命令的 ``eeprom`` 命令。它允许通过交互式界面测试和探索 :ref:`EEPROM <eeprom_api>` 驱动 API，而无需编写专用应用。也可以在现有应用中启用 EEPROM shell，以辅助交互式调试 EEPROM 问题。

要启用 EEPROM shell，必须启用以下 :ref:`Kconfig <kconfig>` 选项：

* :kconfig:option:`CONFIG_SHELL`
* :kconfig:option:`CONFIG_EEPROM`
* :kconfig:option:`CONFIG_EEPROM_SHELL`

例如，为 :zephyr:board:`native_sim` 开发板构建启用了 EEPROM shell 的 :zephyr:code-sample:`hello_world` 示例：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: native_sim
   :gen-args: -DCONFIG_SHELL=y -DCONFIG_EEPROM=y -DCONFIG_EEPROM_SHELL=y
   :goals: build

有关如何连接 shell 并与之交互的一般说明，请参阅 :ref:`shell <shell_api>` 文档。EEPROM shell 提供内置帮助（除非禁用了 :kconfig:option:`CONFIG_SHELL_HELP` ）。向 ``eeprom`` 命令或其任意子命令传入 ``-h`` 或 ``--help`` 即可打印内置帮助信息。所有子命令的参数也都支持 Tab 补全。

.. tip::
   所有 EEPROM shell 子命令都将 EEPROM 外设名称作为第一个参数，该参数也支持 Tab 补全。启用 :kconfig:option:`CONFIG_DEVICE_SHELL` 后，可以使用 ``device list`` shell 命令获取所有可用设备的列表。以下示例均使用设备名称 ``eeprom@0`` 。

EEPROM 容量
***********

可以使用 ``eeprom size`` 子命令查看 EEPROM 的容量，如下所示：

.. code-block:: console

   uart:~$ eeprom size eeprom@0
   32768 bytes

写入数据
********

可以使用 ``eeprom write`` 子命令向 EEPROM 写入数据。此子命令至少接受三个参数：EEPROM 设备名称、开始写入的偏移量，以及至少一个数据字节。在以下示例中，将十六进制字节序列 ``0x0d 0x0e 0x0a 0x0d 0x0b 0x0e 0x0e 0x0f`` 写入偏移量 ``0x0`` 处：

.. code-block:: console

   uart:~$ eeprom write eeprom@0 0x0 0x0d 0x0e 0x0a 0x0d 0x0b 0x0e 0x0e 0x0f
   Writing 8 bytes to EEPROM...
   Verifying...
   Verify OK

也可以使用 ``eeprom fill`` 子命令，以相同的数据模式填充 EEPROM 的部分区域。在以下示例中，从偏移量 ``0x8`` 开始的 16 个字节均被填充为 ``0xaa`` ：

.. code-block:: console

   uart:~$ eeprom fill eeprom@0 0x8 16 0xaa
   Writing 16 bytes of 0xaa to EEPROM...
   Verifying...
   Verify OK

读取数据
********

可以使用 ``eeprom read`` 子命令从 EEPROM 读取数据。此子命令接受三个参数：EEPROM 设备名称、开始读取的偏移量，以及要读取的字节数：

.. code-block:: console

   uart:~$ eeprom read eeprom@0 0x0 8
   Reading 8 bytes from EEPROM, offset 0...
   00000000: 0d 0e 0a 0d 0b 0e 0e 0f                          |........         |
