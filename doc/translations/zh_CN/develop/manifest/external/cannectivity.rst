.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_cannectivity:

CANnectivity USB 转 CAN 适配器固件
##################################

简介
****

`CANnectivity`_ 是用于通用串行总线（USB）转控制器局域网（CAN）适配器的开源固件。

该固件实现 Geschwister Schneider USB/CAN 设备协议，通常称为“gs_usb”。Linux 内核的 SocketCAN `gs_usb driver`_、`python-can`_ 以及许多其他软件包均支持该协议。

该固件基于 Zephyr RTOS，可将你喜欢的微控制器开发板变成完整的 USB 转 CAN 适配器。

CANnectivity 采用 Apache-2.0 许可证。

在 Zephyr 中使用
****************

CANnectivity 固件仓库是一个 Zephyr :ref:`模块 <modules>`，使其组件，即“gs_usb”协议实现，可以在 CANnectivity 固件应用之外复用。

要将 CANnectivity 作为 Zephyr 模块引入，可以在 ``west.yaml`` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/cannectivity.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: cannectivity
         url: https://github.com/CANnectivity/cannectivity.git
         revision: main
         path: custom/cannectivity # adjust the path as needed

加入该模块后，在 CANnectivity 固件应用之外包含以下头文件，即可复用“gs_usb”实现：

.. code-block:: c

   #include <cannectivity/usb/class/gs_usb.h>

API 细节见该头文件。

.. _CANnectivity:
   https://github.com/CANnectivity/cannectivity

.. _gs_usb driver:
   https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/can/usb/gs_usb.c

.. _python-can:
   https://python-can.readthedocs.io/en/stable/interfaces/gs_usb.html
