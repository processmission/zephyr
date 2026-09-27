.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_thrift:

Thrift
######

简介
****

`Apache Thrift`_ 同时提供 `IDL`_ 规范、`RPC`_ 框架和 `code generator`_。它适用于所有主要操作系统，支持超过 27 种编程语言、7 种协议和 6 种底层传输。Thrift 最初于 `Facebook in 2006`_ 开发，随后贡献给 `Apache Software Foundation`_。它支持丰富的类型与数据结构，并封装传输和协议细节，让开发者专注于应用逻辑。

在 Zephyr 中使用
****************

要将 Thrift 作为 Zephyr 模块引入，可以在 ``west.yaml`` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/thrift.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: Thrift
         path: modules/lib/thrift
         revision: zephyr
         url: https://github.com/zephyrproject-rtos/thrift

该模块在 ``zephyr/`` 目录下提供示例应用和测试。

.. target-notes::

.. _Apache Thrift: https://github.com/apache/thrift
.. _IDL: https://en.wikipedia.org/wiki/Interface_description_language
.. _RPC: https://en.wikipedia.org/wiki/Remote_procedure_call
.. _code generator: https://en.wikipedia.org/wiki/Automatic_programming
.. _Facebook in 2006: https://thrift.apache.org/static/files/thrift-20070401.pdf
.. _Apache Software Foundation: https://www.apache.org
