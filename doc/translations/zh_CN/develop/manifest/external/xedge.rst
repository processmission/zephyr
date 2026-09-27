.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_xedge:

Xedge
#####

简介
****

`Xedge`_ 是面向资源受限设备和 RTOS 环境的安全嵌入式 Web 与物联网边缘框架。它基于 Barracuda App Server 技术，提供基于 Lua 的高层应用环境，用于开发安全联网设备。

Xedge 采用 GPLv2 许可证，也提供商业许可选项。

在 Zephyr 中使用
****************

Xedge 框架是一个 Zephyr :ref:`模块 <modules>`，使开发者能够直接在嵌入式硬件上实现基于 Web 的管理界面、REST API 和安全物联网服务。

要将 Xedge 作为 Zephyr 模块引入，添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/xedge.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: xedge
         url: https://github.com/RealTimeLogic/Xedge4Zephyr.git
         revision: main
         path: modules/Xedge4Zephyr

详细构建说明、受支持功能和示例见 `Xedge for Zephyr GitHub Repository`_。

参考资料
********

.. target-notes::

.. _Xedge:
.. _Xedge Introduction:
   https://realtimelogic.com/products/xedge/

.. _Xedge for Zephyr GitHub Repository:
   https://github.com/RealTimeLogic/Xedge4Zephyr

.. _Barracuda App Server:
   https://realtimelogic.com/products/barracuda-application-server/
