.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

.. _cmake-style:

CMake 风格指南
##############

这些指南中的一部分由 CI 中的 ``CMakeStyle`` 合规检查强制执行。你可以在本地使用 ``scripts/cmake/cmake_style.py`` 运行相同的检查（该脚本会递归搜索目录中的 ``CMakeLists.txt`` 和 ``*.cmake`` 文件）：

.. code-block:: console

   pip install tree-sitter tree-sitter-cmake
   ./scripts/cmake/cmake_style.py path/to/CMakeLists.txt
   ./scripts/cmake/cmake_style.py drivers/

通用格式
********

- **缩进**：使用 **2 个空格** 进行缩进。避免使用制表符，以确保不同环境之间的一致性。
- **行长**：尽可能将行长限制在 **100 列** 以内。
- **空行**：使用空行分隔 CMake 文件中逻辑上不同的部分。
- **左括号前不留空格**：不要在命令与左括号之间添加空格。使用 ``if(...)`` 而不是 ``if (...)``。

  .. code-block:: cmake

     # Good:
     if(ENABLE_TESTS)
       add_subdirectory(tests)
     endif()

     # Bad:
     if (ENABLE_TESTS)
       add_subdirectory(tests)
     endif()

命令与语法
**********

- **命令使用小写**：CMake 命令始终使用 **小写** （例如 ``add_executable``、``find_package``）。这样可以提高可读性和一致性。

  .. code-block:: cmake

     # Good:
     add_library(my_lib STATIC src/my_lib.cpp)

     # Bad:
     ADD_LIBRARY(my_lib STATIC src/my_lib.cpp)

  由 CMake 模块定义的命令，以及扩展了已有混合大小写命令的 Zephyr 或 sysbuild 扩展命令属于例外：它们遵循混合大小写的 ``Module_Action`` 命名约定，必须按其规范大小写拼写（例如 CMake 的 ``ExternalProject_Add``，被 Zephyr 的 ``ExternalZephyrProject_Add`` 扩展）。``CMakeStyle`` 检查会将它们排除在小写规则之外。小写命令的扩展保持小写（例如 ``add_dependencies``，被 sysbuild 的 ``sysbuild_add_dependencies`` 扩展）。

- **每行一个文件参数**：将文件参数拆分到多行，以便更轻松地浏览和识别每个源文件或条目。

  .. code-block:: cmake

     # Good:
     target_sources(my_target PRIVATE
       src/file1.cpp
       src/file2.cpp
     )

      # Bad:
     target_sources(my_target PRIVATE src/file1.cpp src/file2.cpp)

变量命名
********

- **缓存变量或在多个 CMake 文件间共享的变量使用大写**：使用 ``option`` 或 ``set(... CACHE ...)`` 定义缓存变量时，请使用 **大写名称**。

  .. code-block:: cmake

     option(ENABLE_TESTS "Enable test suite" ON)
     set(CMAKE_CXX_STANDARD 17 CACHE STRING "C++ standard version")

- **局部变量使用小写**：对于 CMake 文件中的局部变量，请使用 **小写** 或 **snake_case**。

  .. code-block:: cmake

     set(output_dir "${CMAKE_BINARY_DIR}/output")

- **前缀保持一致**：为变量使用一致的前缀，以避免名称冲突，尤其是在大型项目中。

  .. code-block:: cmake

     set(MYPROJECT_SRC_DIR "${CMAKE_SOURCE_DIR}/src")

引号
****

- **为字符串和变量加引号**：始终为字符串字面量和变量加引号，以防止出现意外行为，尤其是在处理可能包含空格的路径或参数时。

  .. code-block:: cmake

     # Good:
     set(my_path "${CMAKE_SOURCE_DIR}/include")

     # Bad:
     set(my_path ${CMAKE_SOURCE_DIR}/include)

- **不要为布尔值加引号**：对于布尔值（ ``ON``、``OFF``、``TRUE``、``FALSE`` ），请避免为它们加引号。

  .. code-block:: cmake

     option(BUILD_SHARED_LIBS "Build shared libraries" OFF)

避免硬编码路径
**************

- 使用 CMake 变量（ ``CMAKE_SOURCE_DIR``、``CMAKE_BINARY_DIR``、``CMAKE_CURRENT_SOURCE_DIR`` ）而不是硬编码路径。

  .. code-block:: cmake

     set(output_dir "${CMAKE_BINARY_DIR}/bin")

条件逻辑
********

- 使用 ``if``、``elseif`` 和 ``else`` 时保持正确的缩进，并以 ``endif()`` 结束。

  .. code-block:: cmake

     if(ENABLE_TESTS)
       add_subdirectory(tests)
     endif()

文档
****

- 使用注释记录 CMake 文件中的复杂逻辑。

  .. code-block:: cmake

     # Find LlvmLld components required for building with llvm
     find_package(LlvmLld 14.0.0 REQUIRED)
