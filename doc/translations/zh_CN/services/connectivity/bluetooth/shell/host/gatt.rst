.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：GATT Shell
################

以下示例假设您已连接两台设备。

要在客户端侧执行服务发现，请使用 :code:`gatt discover` 命令。该命令应打印 GATT 服务器上所有可用的服务。

在服务器侧，可以使用 :code:`gatt register` 命令注册预定义的测试服务。完成后，在客户端侧运行发现命令时，应能看到新添加的服务。

现在可以在客户端侧订阅这些新服务。以下示例演示如何订阅测试服务：

.. code-block:: console

        uart:~$ gatt subscribe 26 25
        Subscribed

服务器现在可以使用 :code:`gatt notify` 命令通知客户端。

GATT 命令还提供另一个选项：发起 MTU 交换。为此，请使用 :code:`gatt exchange-mtu` 命令。要更新 shell 的最大 MTU，需要更新 shell 配置文件中的 Kconfig 符号。更多详细信息，请参阅 :zephyr:code-sample:`bluetooth_mtu_update`。
