.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _usbc_api:

USB-C 设备协议栈
################

USB-C 设备协议栈是 Type-C 端口控制器（TCPC）与客户应用之间的硬件无关接口。它移植自 Google ChromeOS 的 Type-C 端口管理器（TCPM）协议栈。它提供以下功能：

* 使用 Type-C 端口控制器驱动提供的 API 与 Type-C 端口控制器交互。
* 提供供客户应用使用的编程接口。API 说明见 :zephyr_file:`include/zephyr/usb_c/usbc.h`。

配置选项
********

USB-C 设备协议栈支持仅受电端（Sink）、仅供电端（Source）以及双角色电源（DRP）设备的实现。

- :kconfig:option:`CONFIG_USBC_CSM_SINK_ONLY`：受电端 USB-C 连接状态机
- :kconfig:option:`CONFIG_USBC_CSM_SOURCE_ONLY`：供电端 USBC 连接状态机
- :kconfig:option:`CONFIG_USBC_CSM_DRP`：双角色电源（DRP）USB-C 连接状态机

:zephyr:code-sample-category:`列表<usbc>` 中提供了用于不同目的的示例。

实现受电端 Type-C 与 Power Delivery USB-C 设备
**********************************************

USB-C 设备的配置在协议栈层和设备树中完成。

需要定义以下设备树内容、结构和回调：

* 引用 TCPC 的设备树 usb-c-connector 节点
* 引用 VBUS 测量设备的设备树 vbus 节点
* 封装应用特定数据的用户定义结构
* 策略回调

例如，对于 USB-C 受电端示例应用：

每个物理 Type-C 端口在设备树中由 usb-c-connector 兼容节点表示：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/boards/b_g474e_dpow1.overlay
   :language: dts
   :start-after: usbc.rst usbc-port start
   :end-before: usbc.rst usbc-port end
   :linenos:

VBUS 由设备树中通过 usb-c-vbus-adc 兼容节点引用的设备测量：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/boards/b_g474e_dpow1.overlay
   :language: dts
   :start-after: usbc.rst vbus-voltage-divider-adc start
   :end-before: usbc.rst vbus-voltage-divider-adc end
   :linenos:


定义用户定义的结构，稍后向子系统注册，并可通过 API 从回调中访问：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst port data object start
   :end-before: usbc.rst port data object end
   :linenos:

子系统使用这些回调来设置或获取应用特定数据：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst callbacks start
   :end-before: usbc.rst callbacks end
   :linenos:

子系统使用此回调查询是否可以执行某项操作：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst check start
   :end-before: usbc.rst check end
   :linenos:

子系统使用此回调向应用通知事件：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst notify start
   :end-before: usbc.rst notify end
   :linenos:

注册回调：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst register start
   :end-before: usbc.rst register end
   :linenos:

注册用户定义的结构：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst user data start
   :end-before: usbc.rst user data end
   :linenos:

启动 USB-C 子系统：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst usbc start
   :end-before: usbc.rst usbc end
   :linenos:

实现供电端 Type-C 与 Power Delivery USB-C 设备
**********************************************

USB-C 设备的配置在协议栈层和设备树中完成。

定义以下设备树内容、结构和回调：

* 引用 TCPC 的设备树 ``usb-c-connector`` 节点
* 引用 VBUS 测量设备的设备树 ``vbus`` 节点
* 用于 VBUS 和 VCONN 电源控制的设备树 ``pwrctrl`` 节点
* 封装应用特定数据的用户定义结构
* 策略回调

例如，对于 USB-C 供电端示例应用：

每个物理 Type-C 端口在设备树中由 ``usb-c-connector`` 兼容节点表示：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/boards/stm32g081b_eval.overlay
   :language: dts
   :start-after: usbc.rst usbc-port start
   :end-before: usbc.rst usbc-port end
   :linenos:

VBUS 由设备树中通过 ``usb-c-vbus-adc`` 兼容节点引用的设备测量：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/boards/stm32g081b_eval.overlay
   :language: dts
   :start-after: usbc.rst vbus-voltage-divider-adc start
   :end-before: usbc.rst vbus-voltage-divider-adc end
   :linenos:

VBUS 和 VCONN 的电源控制可以由设备树中通过 ``zephyr,usb-c-pwrctrl`` 兼容节点引用的设备管理：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/boards/stm32g081b_eval.overlay
   :language: dts
   :start-after: usbc.rst pwrctrl start
   :end-before: usbc.rst pwrctrl end
   :linenos:

定义用户定义的结构，稍后向子系统注册，并可通过 API 从回调中访问：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst port data object start
   :end-before: usbc.rst port data object end
   :linenos:

子系统使用这些回调来设置或获取应用特定数据：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst callbacks start
   :end-before: usbc.rst callbacks end
   :linenos:

子系统使用此回调查询是否可以执行某项操作：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst check start
   :end-before: usbc.rst check end
   :linenos:

子系统使用此回调向应用通知事件：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst notify start
   :end-before: usbc.rst notify end
   :linenos:

注册回调：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst register start
   :end-before: usbc.rst register end
   :linenos:

注册用户定义的结构：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst user data start
   :end-before: usbc.rst user data end
   :linenos:

启动 USB-C 子系统：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst usbc start
   :end-before: usbc.rst usbc end
   :linenos:

实现双角色电源（DRP）USB-C 设备
*******************************

DRP 设备既可以作为供电端，也可以作为受电端运行，并自动与端口对端协商合适的角色。未连接时，设备会在供电端（Rp）和受电端（Rd）的 CC 线通告之间切换，以检测并连接任何类型的对端。检测到连接后，设备会进入相应的已连接状态（Attached.SRC 或 Attached.SNK），并启动对应的策略引擎状态机（PE_SRC 或 PE_SNK）来协商电源传输。

配置与供电端和受电端设备类似，但有以下关键区别：

* 在设备树 ``usb-c-connector`` 节点中设置 ``power-role = "dual"``
* 为供电端和受电端操作实现回调

可以通过 Kconfig 配置 DRP 切换行为：

- :kconfig:option:`CONFIG_USBC_DRP_PERIOD_MS`：切换周期（50-100 毫秒，默认 75 毫秒）
- :kconfig:option:`CONFIG_USBC_DRP_DUTY_CYCLE`：作为供电端的时间百分比（30-70%，默认 50%）

完整示例请参见 :zephyr:code-sample:`usb-c-drp`。

API 参考
********

.. doxygengroup:: _usbc_device_api

受电端（SINK）回调参考
**********************

.. doxygengroup:: sink_callbacks

供电端（SOURCE）回调参考
************************

.. doxygengroup:: source_callbacks
