.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _comparator_api:

比较器
######

概述
****

模拟比较器用于比较接入其反相输入端和同相输入端的两个模拟信号的电压。如果同相输入端的电压高于反相输入端的电压，比较器将输出高电平，否则输出低电平。

比较器通常可以设置在输出变化时触发的触发器。该触发器可以调用回调函数，也可以通过轮询查询其状态。

相关配置选项：

* :kconfig:option:`CONFIG_COMPARATOR`

配置
****

嵌入式比较器通常可以在运行时进行配置。启用比较器时，必须通过 Devicetree 提供初始配置。在运行时，可以使用设备驱动程序专用的 API 更新比较器的配置。配置将在比较器恢复运行时应用。

电源管理
********

比较器通过电源管理启用。恢复运行后，比较器会持续比较输入信号、产生输出并检测边沿。挂起时，比较器停止工作。

比较器 shell
************

比较器 shell 为 :ref:`shell <shell_api>` 模块提供了 ``comp`` 命令及一组子命令。

``comp`` shell 命令提供以下子命令：

* ``get_output`` 参见 :c:func:`comparator_get_output`
* ``set_trigger`` 参见 :c:func:`comparator_set_trigger`
* ``await_trigger`` 按以下流程等待触发：

  * 使用 :c:func:`comparator_set_trigger_callback` 设置触发回调函数
  * 等待回调，或在默认或可选指定的超时时间到期后超时退出
  * 使用 :c:func:`comparator_set_trigger_callback` 清除触发回调函数
* ``trigger_is_pending`` 参见 :c:func:`comparator_trigger_is_pending`

相关配置选项：

* :kconfig:option:`CONFIG_SHELL`
* :kconfig:option:`CONFIG_COMPARATOR_SHELL`
* :kconfig:option:`CONFIG_COMPARATOR_SHELL_AWAIT_TRIGGER_DEFAULT_TIMEOUT`
* :kconfig:option:`CONFIG_COMPARATOR_SHELL_AWAIT_TRIGGER_MAX_TIMEOUT`

.. note::
   启用比较器 shell 时，也可以选择同时启用电源管理 shell。

   相关配置选项：

   * :kconfig:option:`CONFIG_PM_DEVICE`
   * :kconfig:option:`CONFIG_PM_DEVICE_SHELL`

API 参考
********

.. doxygengroup:: comparator_interface

.. doxygengroup:: comparator_fake
