.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_ludlc:

LuDLC
#####

简介
****

LuDLC（轻量级微型设备链路控制）是一种面向资源受限系统、独立于传输方式的数据链路协议。

LuDLC 无需完整网络协议栈，即可通过 UART、SPI 或 CAN 总线等简单传输方式提供可靠、有序的通信。它支持流量控制、重传、连接管理及通道复用，适用于 TCP/IP 过于庞大或不可用的场景。

LuDLC 采用双重许可证：Apache-2.0 OR GPL-2.0-or-later。

在 Zephyr 中使用
****************

要将 LuDLC 作为 Zephyr 模块（ludlc）引入，可以在 :file:`west.yaml` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/ludlc.yaml``，然后运行 :command:`west update`：

.. code-block:: yaml

   manifest:
     projects:
       - name: ludlc
         url: https://github.com/avolkov-1221/ludlc.git
         revision: main
         path: modules/ludlc # adjust the path as needed

参考资料
********

.. target-notes::

.. _ludlc: https://github.com/avolkov-1221/ludlc

.. _ludlc documentation:
   https://github.com/avolkov-1221/ludlc/tree/main/doc

.. _ludlc examples:
   https://github.com/avolkov-1221/ludlc/tree/main/src/samples
