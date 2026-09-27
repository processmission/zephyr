.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _nanopb_reference:

Nanopb
######

`Nanopb <https://jpa.kapsi.fi/nanopb/>`_ 是 Google `Protocol Buffers <https://protobuf.dev/>`_ 的 C 实现。

要求
****

Nanopb 使用 protocol buffer 编译器生成源文件和头文件，请确保 ``protoc`` 可执行文件已安装并可用。

.. tabs::

   .. group-tab:: Ubuntu

      使用 ``apt`` 安装依赖项：

         .. code-block:: shell

            sudo apt install protobuf-compiler

   .. group-tab:: macOS

      使用 ``brew`` 安装依赖项：

         .. code-block:: shell

            brew install protobuf

   .. group-tab:: Windows

      使用 ``choco`` 安装依赖项：

         .. code-block:: shell

            choco install protoc


配置
****

请确保在 ``CMakeLists.txt`` 文件中按如下方式包含 ``nanopb``：

.. code-block:: cmake

   list(APPEND CMAKE_MODULE_PATH ${ZEPHYR_BASE}/modules/nanopb)
   include(nanopb)

可以使用 ``zephyr_nanopb_sources()`` CMake 函数来添加 ``proto`` 文件，该函数确保在构建指定目标之前生成头文件和源文件。

Nanopb 提供了 `generator options <https://jpa.kapsi.fi/nanopb/docs/reference.html#generator-options>`_，可用于配置消息或字段。这样可以设置固定大小，或者完全跳过某些字段。

内部 CMake 生成器提供了一个扩展，可以使用 CMake 变量自动配置 ``*.options.in`` 文件。

有关用法示例，请参阅 :zephyr_file:`samples/modules/nanopb/src/simple.options.in` 和 :zephyr_file:`samples/modules/nanopb/CMakeLists.txt`。
