.. SPDX-FileCopyrightText: Copyright The Process Mission
.. SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
.. SPDX-License-Identifier: Apache-2.0

.. zephyr:code-sample:: external_library
   :name: 外部静态库

   将外部静态库接入 Zephyr 构建系统。

概述
****

此示例演示如何将外部静态库接入 Zephyr 构建系统，
包括使用其他构建系统编译外部库，以及链接生成的静态库。

Windows 使用说明
****************

在 Windows 主机上使用此示例时，必须将 GNU Make 加入 PATH。
可以通过 Chocolatey 或手动安装完成配置。

使用 Chocolatey 安装
====================

运行以下命令安装 make：

.. code-block:: bash

   choco install make

安装完成后，按通常的方式构建应用。

手动安装
========

从 https://gnuwin32.sourceforge.net/packages/make.htm 下载预编译的 make。
可以分别下载 ``Binaries`` 和 ``Dependencies`` 并解压到同一目录，
也可以使用 ``Complete package`` 安装程序。安装完成并加入 PATH 后，按通常的方式构建应用。
