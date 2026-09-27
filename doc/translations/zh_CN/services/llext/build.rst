.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

构建扩展
########

LLEXT 子系统允许创建可以加载到正在运行的 Zephyr 应用程序中的扩展。构建这些扩展时，通常需要能够访问主 Zephyr 应用程序使用的头文件和编译器标志。

实现这一点最简单的方法是使用 `Zephyr 原生 CMake 功能 <llext_build_native_>`_ 将扩展作为 Zephyr 应用程序的一部分来构建。这样一次构建即可同时生成主 Zephyr 应用程序和扩展，它们都会自动使用相同的参数构建。

在某些情况下，引入完整的 Zephyr 构建系统可能不可行或不方便；扩展可能是使用不同的编译器套件构建的，或者完全属于另一个项目的一部分。在这种情况下，扩展开发者需要导出主 Zephyr 应用程序使用的头文件和编译器标志。这可以使用 `LLEXT 扩展开发工具包 <llext_build_edk_>`_ 来完成。

.. _llext_build_native:

使用 Zephyr CMake 功能
**********************

Zephyr 构建系统提供了一组功能，可用于将扩展作为 Zephyr 应用程序的一部分进行构建。这是构建扩展最简单的方法，因为只需对应用程序构建系统做最少的添加。

构建扩展
--------

可以通过调用 :cmake:command:`add_llext_target` 函数在应用程序的 ``CMakeLists.txt`` 中定义扩展，并提供目标名称、输出和源文件。用法与标准的 :cmake:command:`add_custom_target <command:add_custom_target>` CMake 函数类似：

.. code-block:: cmake

   add_llext_target(
       <target_name>
       OUTPUT <ext_file.llext>
       SOURCES <src1> [<src2>...]
   )

其中：

- ``<target_name>`` 是最终 CMake 目标的名称，该目标将生成 LLEXT 二进制文件；
- ``<ext_file.llext>`` 是输出文件的名称，其中包含打包后的扩展；
- ``<src1> [<src2>...]`` 是用于编译以创建扩展的源文件列表。

扩展构建过程的具体步骤取决于当前选择的 :ref:`ELF 目标文件格式 <llext_kconfig_type>` 。

定义并可使用 ``get_target_property()`` CMake 函数检索 ``<target_name>`` 的以下自定义属性：

``lib_target``

    用于源代码编译和/或链接步骤的目标名称。

``lib_output``

    编译和/或链接步骤产生的二进制文件。

``pkg_input``

     用作打包步骤输入的文件。

``pkg_output``

    最终扩展文件的名称。

调整构建过程
------------

以下 CMake 函数可用于在扩展构建过程中对构建系统行为进行精细调整。以下每个函数都将 LLEXT 目标名称作为第一个参数；除此之外，它在功能上等同于常见的 Zephyr ``target_*`` 版本。

* :cmake:command:`llext_compile_definitions`
* :cmake:command:`llext_compile_features`
* :cmake:command:`llext_compile_options`
* :cmake:command:`llext_include_directories`
* :cmake:command:`llext_link_options`

自定义构建步骤
--------------

可以使用 ``add_llext_command`` CMake 函数添加将在扩展构建过程中执行的自定义构建步骤。命令将在指定的构建步骤运行，并可以引用目标的属性以获取特定于构建的详细信息。

函数签名如下：

.. code-block:: cmake

   add_llext_command(
       TARGET <target_name>
       [PRE_BUILD | POST_BUILD | POST_PKG]
       COMMAND <command> [args...]
   )

不同的构建步骤如下：

``PRE_BUILD``

    在链接扩展代码之前执行（如果该架构使用动态库）。此步骤可以访问 ``lib_target`` 及其自身的属性。

``POST_BUILD``

    在扩展代码构建完成之后、打包到 ``.llext`` 文件之前执行。此步骤应通过读取 :file:`lib_output` 的内容来创建 :file:`pkg_input` 文件。

``POST_PKG``

    在扩展输出文件创建完成之后执行。命令可以对最终的 llext 文件 :file:`pkg_output` 进行操作。

``COMMAND`` 之后的其他内容将按原样传递给 ``add_custom_command()`` （包括多个命令和其他选项）。

.. _llext_build_edk:

LLEXT 扩展开发工具包（EDK）
***************************

当在主 Zephyr 构建系统之外将扩展作为独立项目构建时，能够访问主 Zephyr 应用程序使用的同一组生成头文件和编译器标志非常重要，因为它们直接影响 Zephyr 头文件的解释方式以及扩展的总体编译方式。

为此，可以让 Zephyr 从主 Zephyr 应用程序的构建产物生成扩展开发工具包（EDK），具体方法是运行以下使用 ``llext-edk`` 目标的命令：

.. code-block:: shell

    west build -t llext-edk

生成的 EDK 位于构建目录下的 ``zephyr`` 目录中。它是一个 tar 包，包含构建扩展所需的头文件和编译标志。随后，扩展开发者可以在其构建系统中包含这些头文件并使用这些编译标志来构建扩展。

EDK 定义文件
------------

EDK 包含若干便利文件，这些文件在启用时定义一组变量，其中包含项目所需的编译标志以及其他与构建相关的信息。目前，这些信息以以下格式导出：

- ``Makefile.cflags`` ，用于基于 Makefile 的项目；
- ``cmake.cflags`` ，用于基于 CMake 的项目。

头文件和标志的路径以 EDK 根目录为前缀。对于 CMake 项目，该目录自动从 ``CMAKE_CURRENT_LIST_DIR`` 获取；其他格式则引用 ``LLEXT_EDK_INSTALL_DIR`` 变量，用户必须在包含生成文件之前将其设置为 EDK 的安装路径。

.. note::
   变量名称中的 ``LLEXT_EDK`` 前缀可以通过 :kconfig:option:`CONFIG_LLEXT_EDK_NAME` 选项更改。

编译标志
--------

构建扩展所需的完整标志列表由 ``LLEXT_CFLAGS`` 提供。还提供了一组更细粒度的标志，可用于支持不同的用例，例如为单元测试构建 mock 时：

``LLEXT_INCLUDE_CFLAGS``

        用于将包含非自动生成头文件的目录添加到编译器包含搜索路径的编译标志。

``LLEXT_GENERATED_INCLUDE_CFLAGS``

        用于将包含自动生成头文件的目录添加到编译器包含搜索路径的编译标志。

``LLEXT_ALL_INCLUDE_CFLAGS``

        用于将构建中使用的所有包含头文件的目录添加到编译器包含搜索路径的编译标志。它是 ``LLEXT_INCLUDE_CFLAGS`` 和 ``LLEXT_GENERATED_INCLUDE_CFLAGS`` 的组合。

``LLEXT_GENERATED_IMACROS_CFLAGS``

        用于自动生成头文件的编译标志，这些头文件必须通过 ``-imacros`` 包含在构建中。

``LLEXT_BASE_CFLAGS``

        其他用于控制目标 CPU 代码生成的编译标志。以上列表中不包含这些标志。

``LLEXT_CFLAGS``

        构建扩展所需的全部标志。它是 ``LLEXT_ALL_INCLUDE_CFLAGS`` 、 ``LLEXT_GENERATED_IMACROS_CFLAGS`` 和 ``LLEXT_BASE_CFLAGS`` 的组合。

目标信息
--------

EDK 包含用于标识当前 Zephyr 构建目标的信息。目前定义了以下变量，它们反映了 Zephyr 构建系统中可用的信息：

``LLEXT_EDK_BOARD_NAME``
    Zephyr 构建中使用的开发板名称。

``LLEXT_EDK_BOARD_QUALIFIERS``
    Zephyr 构建中使用的开发板限定符（如果提供）。

``LLEXT_EDK_BOARD_REVISION``
    Zephyr 构建中使用的开发板版本（如果提供）。

``LLEXT_EDK_BOARD_TARGET``
    Zephyr 构建中使用的完全限定开发板目标。

.. note::
   变量名称中的 ``LLEXT_EDK`` 前缀可以通过 :kconfig:option:`CONFIG_LLEXT_EDK_NAME` 选项更改。

.. _llext_kconfig_edk:

LLEXT EDK Kconfig 选项
----------------------

可以使用以下 Kconfig 选项配置 LLEXT EDK：

:kconfig:option:`CONFIG_LLEXT_EDK_NAME`
    生成的 EDK tar 包的名称。它还用作 EDK 文件中定义的若干变量的前缀。

:kconfig:option:`CONFIG_LLEXT_EDK_USERSPACE_ONLY`
    如果设置该选项，EDK 将包含不含有用于将系统调用路由到内核的代码的头文件。这在构建仅在用户模式下运行的扩展时非常有用。

EDK 示例
--------

有关如何使用 LLEXT EDK 的示例，请参阅 :zephyr:code-sample:`llext-edk` 。
