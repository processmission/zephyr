.. SPDX-FileCopyrightText: Copyright The Process Mission
.. SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
.. SPDX-License-Identifier: Apache-2.0

.. zephyr:code-sample:: hello_world
   :name: Hello World

   向控制台输出 "Hello World"。

概述
****

这是一个简单的示例，可在任意 :ref:`受支持的开发板 <boards>` 上运行，
并向控制台输出 "Hello World"。

构建与运行
**********

使用以下命令在 QEMU 中构建并运行此应用：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :host-os: unix
   :board: qemu_x86
   :goals: run
   :compact:

要为其他开发板构建，将上面的 "qemu_x86" 替换为目标开发板名称。

示例输出
========

.. code-block:: console

    Hello World! x86

依次按 :kbd:`CTRL+A` 和 :kbd:`x` 退出 QEMU。
