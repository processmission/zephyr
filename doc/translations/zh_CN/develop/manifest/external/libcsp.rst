.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_libcsp:

libcsp（立方星空间协议）
########################

简介
****

libcsp 是立方星空间协议（CSP）的实现，是使用 C 编写的小型协议栈。CSP 旨在简化立方星等小型网络中分布式嵌入式系统之间的通信。其设计遵循 TCP/IP 模型，包含传输协议、路由协议及多个 MAC 层接口。libcsp 核心包含路由器、面向连接的套接字 API，以及消息池和连接池。

某些立方星使用 Zephyr，并通过 libcsp 与星上其他组件通信。

libcsp 采用 MIT 许可证。


在 Zephyr 中使用
****************

要在 Zephyr 中使用 libcsp，首先将以下片段加入 ``west.yaml``：

.. code-block:: yaml

   manifest:
     projects:
       - name: libcsp
         url: https://github.com/libcsp/libcsp
         revision: develop
         path: modules/lib/libcsp


再将以下内容加入 ``prj.conf``：

.. code-block:: cfg

     CONFIG_LIBCSP=y

将 libcsp 加入项目后，运行 ``west update``。

详细说明和 API 文档见 `libcsp documentation`_。


参考资料
********

.. target-notes::

.. _libcsp:
   https://github.com/libcsp/libcsp

.. _libcsp documentation:
   https://libcsp.github.io/libcsp/
