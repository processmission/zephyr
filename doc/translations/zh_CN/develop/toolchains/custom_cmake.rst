.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _custom_cmake_toolchains:

自定义 CMake 工具链
###################

要使用外部 CMake 文件定义的自定义工具链，请 :ref:`设置以下环境变量 <env_vars>`：

- 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设为工具链名称。
- 将 ``TOOLCHAIN_ROOT`` 设为包含工具链 CMake 配置文件的目录路径。

随后，Zephyr 会包含 :file:`TOOLCHAIN_ROOT` 目录中的工具链 CMake 文件：

- :file:`cmake/toolchain/<toolchain name>/generic.cmake`：配置工具链的“通用”用途，主要是在生成的 :ref:`devicetree` 文件上运行 C 预处理器。
- :file:`cmake/toolchain/<toolchain name>/target.cmake`：配置工具链的“目标”用途，即构建 Zephyr 和应用源代码。

这里的 <toolchain name> 与 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 中的名称相同。:file:`generic.cmake` 和 :file:`target.cmake` 应包含哪些内容，详见 Zephyr 文件 :zephyr_file:`cmake/modules/FindHostTools.cmake` 和 :zephyr_file:`cmake/modules/FindTargetTools.cmake`。

为 Zephyr 应用生成构建系统时，也可以将 ``ZEPHYR_TOOLCHAIN_VARIANT`` 和 ``TOOLCHAIN_ROOT`` 设为 CMake 变量，如下所示：

.. code-block:: console

   west build ... -- -DZEPHYR_TOOLCHAIN_VARIANT=... -DTOOLCHAIN_ROOT=...

.. code-block:: console

   cmake -DZEPHYR_TOOLCHAIN_VARIANT=... -DTOOLCHAIN_ROOT=...

采用这种方式时，``-C <initial-cache>`` 这一 `cmake option`_ 可能很有用。将 :makevar:`ZEPHYR_TOOLCHAIN_VARIANT`、:makevar:`TOOLCHAIN_ROOT` 等设置保存在 :file:`my-toolchain.cmake` 中后，即可通过 ``cmake -C my-toolchain.cmake ...`` 调用 CMake，减少重复输入。

Zephyr 包含 :file:`include/zephyr/toolchain.h`，后者根据 ``__llvm__`` 或 ``__GNUC__`` 等编译器标识符包含工具链专用头文件。某些自定义编译器会将自身标识为所基于的编译器，例如 ``llvm``，因而包含 :file:`toolchain/llvm.h`，但该文件可能不适合自定义工具链。要改为包含 :file:`include/other.h`，请在 :file:`<TOOLCHAIN_ROOT>/cmake/toolchain/<toolchain name>/` 下的 generic.cmake 和／或 target.cmake 中添加 set(TOOLCHAIN_USE_CUSTOM 1)。

设置 :makevar:`TOOLCHAIN_USE_CUSTOM` 后，必须在源码树外提供 :file:`other.h`，并由其包含自定义工具链所需的正确头文件。放置 :file:`other.h` 的合适位置是 ``TOOLCHAIN_ROOT`` 指定目录下的 :file:`include/zephyr/toolchain`。为使 Zephyr 构建包含该工具链头文件，可将 :makevar:`USERINCLUDE` 指向包含目录，如下所示：

.. code-block:: console

   west build -- -DZEPHYR_TOOLCHAIN_VARIANT=... -DTOOLCHAIN_ROOT=... -DUSERINCLUDE=...

.. _cmake option:
   https://cmake.org/cmake/help/latest/manual/cmake.1.html#options
