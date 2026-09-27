.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_greybus:

Greybus
#######

简介
****

Greybus 是轻量级的消息协议框架，为主机访问远端模块提供的硬件功能提供标准化方式。它最初面向模块化系统开发，为 GPIO、I²C、SPI、PWM 和固件更新等常见外设类别定义了明确的操作协议。

Zephyr 的 Greybus 模块实现相关协议层，将 Greybus 操作映射到 Zephyr 子系统。启用后，Zephyr 设备可通过 Greybus 协议向主机暴露硬件能力。主机通过 Greybus 清单数据发现可用功能，再发出特定类别的请求，由 Zephyr 模块处理并响应。

Greybus 最初设计用于 `Unipro`_，但协议本身基本独立于底层传输。目前该模块支持通过 TCP 套接字传输，也应可适配 UART、I2C 等其他传输方式。当前支持的后端见 `this directory <Greybus Transport Directory_>`_，欢迎提交新的传输后端 PR。

Greybus 同时使用 Apache-2.0 和 BSD-3-Clause 许可证。

在 Zephyr 中使用
****************

要将 Greybus for Zephyr 作为模块引入，可以在 west.yaml 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/greybus.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: Greybus-Zephyr
         path: modules/lib/greybus
         revision: main
         url: https://github.com/beagleboard/greybus-zephyr

Greybus 子系统的使用说明见 `Greybus module repository`_ 和 `Greybus samples`_。

目前所有开发和实际测试均使用 `BeaglePlay`_ 和 `BeagleConnect Freedom`_。

参考资料
********

#. `Greybus Specification`_

#. Christopher Friedt，LPC 2020

   - `Slides <LPC 2020 Slides_>`_
   - `Video <LPC 2020 Video_>`_

.. target-notes::

.. _Greybus Specification: https://github.com/projectara/greybus-spec
.. _LPC 2020 Slides: https://linuxplumbersconf.org/event/7/contributions/814/
.. _LPC 2020 Video: https://youtu.be/n4yiCF2wYeo?t=11683
.. _Greybus module repository: https://github.com/beagleboard/greybus-zephyr
.. _Greybus samples: https://github.com/beagleboard/greybus-zephyr/tree/main/samples/basic
.. _BeaglePlay: https://www.beagleboard.org/boards/beagleplay
.. _BeagleConnect Freedom: https://www.beagleboard.org/boards/beagleconnect-freedom
.. _UniPro: https://en.wikipedia.org/wiki/UniPro
.. _Greybus Transport Directory: https://github.com/beagleboard/greybus-zephyr/tree/main/subsys/greybus/transport
