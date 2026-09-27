.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_zenoh_pico:

zenoh-pico
##########

简介
****

`zenoh-pico`_ 是面向资源受限设备的 `Eclipse Zenoh`_ 实现，提供原生 C API，为嵌入式系统和微控制器提供零开销的发布／订阅、存储／查询及计算能力。

zenoh-pico 将传输中的数据、静态存储数据和计算统一起来，同时保持远超主流协议栈的时间与空间效率。它与主要的 Rust Zenoh 实现完全兼容，以轻量方式实现了大部分功能。

zenoh-pico 采用 Eclipse Public License 2.0 和 Apache License 2.0。

在 Zephyr 中使用
****************

zenoh-pico 仓库是一个 Zephyr :ref:`模块 <modules>`，为 Zephyr 应用提供分布式通信能力。它支持在 IPv4、IPv6 和 6LoWPAN 网络上使用 UDP（单播和组播）及 TCP 传输层，支持 WiFi、以太网、Thread 和串行数据链路层。

要将 zenoh-pico 作为 Zephyr 模块引入，可以在 ``west.yaml`` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/zenoh-pico.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: zenoh-pico
         url: https://github.com/eclipse-zenoh/zenoh-pico.git
         revision: main
         path: modules/lib/zenoh-pico # adjust the path as needed

详细说明和 API 文档见 `zenoh-pico documentation`_ 及随附的 `Zephyr examples`_。

参考资料
********

.. target-notes::

.. _zenoh-pico:
   https://github.com/eclipse-zenoh/zenoh-pico

.. _Eclipse Zenoh:
   https://zenoh.io

.. _zenoh-pico documentation:
   https://zenoh-pico.readthedocs.io/en/latest/

.. _Zephyr examples:
   https://github.com/eclipse-zenoh/zenoh-pico/tree/main/examples/zephyr
