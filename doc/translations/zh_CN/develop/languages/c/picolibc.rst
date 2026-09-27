.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _c_library_picolibc:

Picolibc
########

`Picolibc`_ 是面向嵌入式系统的完整 C 库实现，以 `C17 (ISO/IEC 9899:2018)`_ 和 `POSIX 2018 (IEEE Std 1003.1-2017)`_ 标准为目标。它是外部开源项目，以 Zephyr 模块形式提供；:ref:`toolchain_zephyr_sdk` 也为每种受支持架构附带预编译版本（:file:`libc.a`）。

.. note::
   Picolibc 也可用于 :ref:`toolchain_gnuarmemb` 等第三方工具链。

Zephyr 实现了由 Picolibc 标准 C 库函数调用的“API 钩子”函数。这些函数位于 :zephyr_file:`lib/libc/picolibc/`，将库内部系统调用转换为等效的 Zephyr API 调用。

.. _`Picolibc`: https://github.com/picolibc/picolibc
.. _`C17 (ISO/IEC 9899:2018)`: https://www.iso.org/standard/74528.html
.. _`POSIX 2018 (IEEE Std 1003.1-2017)`: https://pubs.opengroup.org/onlinepubs/9699919799/functions/printf.html

.. _c_library_picolibc_module:

Picolibc 模块
=============

以 Zephyr 模块形式构建时，可以通过多个配置项调整库的功能集，在支持的功能与生成函数的代码体积之间权衡。由于标准 C++ 库必须针对目标 C 库编译，因此使用标准 C++ 库的应用不能使用 Picolibc 模块。构建该模块会增加应用的编译时间。

在应用配置文件中选择 :kconfig:option:`CONFIG_PICOLIBC_USE_MODULE`，即可启用 Picolibc 模块。

将 Picolibc 模块更新到新版本时，也必须将 :ref:`Zephyr SDK 工具链附带的 Picolibc <c_library_picolibc_toolchain>` 更新到同一版本。

.. _c_library_picolibc_toolchain:

工具链中的 Picolibc
===================

从 0.16 版本开始，Zephyr SDK 为每种目标架构提供预编译的 Picolibc 和 libstdc++。

在应用配置文件中取消选择 :kconfig:option:`CONFIG_PICOLIBC_USE_MODULE`，即可使用工具链版本的 Picolibc。

对于每个 Zephyr 版本，只要使用 :ref:`推荐的 Zephyr SDK 版本 <toolchain_zephyr_sdk_compatibility>`，工具链附带的 Picolibc 就保证与 :ref:`Picolibc 模块 <c_library_picolibc_module>` 保持同步。

工具链未附带 Picolibc 时的构建
------------------------------

即使工具链未附带 Picolibc，仍可通过从源码构建来使用它。注意，:ref:`c_library_picolibc_module` 中的限制仍然适用。

工具链未附带 Picolibc 时，必须启用 :kconfig:option:`CONFIG_PICOLIBC_SUPPORTED` 才能构建。例如，需要在工具链 Kconfig 文件中添加：

.. code-block:: kconfig

   config TOOLCHAIN_<name>_PICOLIBC_SUPPORTED
      def_bool y
      select PICOLIBC_SUPPORTED

启用 :kconfig:option:`CONFIG_PICOLIBC_SUPPORTED` 后，如果工具链未附带 Picolibc，构建系统会自动通过模块从源码构建它。

格式化输出
**********

Picolibc 支持所有标准 C 格式化输入输出函数，包括 :c:func:`printf`、:c:func:`fprintf`、:c:func:`sprintf` 和 :c:func:`sscanf`。

Picolibc 的格式化输入输出实现支持 C17 和 POSIX 2018 定义的所有格式说明符，但有以下例外：

* 浮点格式说明符（例如 ``%f``）要求启用 :kconfig:option:`CONFIG_PICOLIBC_IO_FLOAT`。

* long long 格式说明符（例如 ``%lld``）要求启用 :kconfig:option:`CONFIG_PICOLIBC_IO_LONG_LONG`。启用 :kconfig:option:`CONFIG_PICOLIBC_IO_FLOAT` 时，会自动启用此选项。

Printk、cbprintf 及相关函数
***************************

使用 Picolibc 时，Zephyr 格式化输出函数通过 stdio 调用实现，包括：

 * printk、snprintk 和 vsnprintk
 * cbprintf 和 cbvprintf
 * fprintfcb、vfprintfcb、printfcb、vprintfcb、snprintfcb 和 vsnprintfcb

使用带标记参数（:kconfig:option:`CONFIG_CBPRINTF_PACKAGE_SUPPORT_TAGGED_ARGUMENTS` 和 :c:macro:`CBPRINTF_PACKAGE_ARGS_ARE_TAGGED`）时，cbpprintf 调用不会使用 Picolibc。由于 cbprintf 函数并不完全符合 C/POSIX，这些代码的输出格式可能与 Picolibc 不同。

数学函数
********

Picolibc 为 float、double 和 long double 数学运算提供完整的 C17／`IEEE STD 754-2019`_ 支持，但 long double 版本的贝塞尔函数除外。

.. _`IEEE STD 754-2019`: https://ieeexplore.ieee.org/document/8766229

线程局部存储
************

在受支持的平台上，Picolibc 使用线程局部存储（TLS）保存应由各线程独有的数据，例如 :c:macro:`errno`。因此，使用 Picolibc 时会启用 TLS 支持。所有 TLS 变量均从线程栈区域分配，可能使所需栈大小增加几个字节。

C 库局部变量
************

Picolibc 使用少量内部变量进行堆管理等工作，统一放入名为 :c:var:`z_libc_partition` 的专用内存分区。使用 :kconfig:option:`CONFIG_USERSPACE` 和内存域的应用，必须确保调用 Picolibc 时活动的任何内存域都包含该分区。

动态内存管理
************

Picolibc 使用 :ref:`公共 C 库 <c_library_common>` 提供的 malloc 系列 API 实现，后者基于 :ref:`内核内存堆 API <heap_v2>`。
