.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _stm32cube_ide:

STM32CubeIDE
############

STM32CubeIDE_ 是 STMicroelectronics 基于 Eclipse 的集成开发环境，面向 STM32 系列 MCU 和 MPU。

本指南介绍如何使用该 IDE 设置、构建和调试 Zephyr 应用。

必须先通过 Zephyr 和 west 创建项目。

这些说明已在 Linux 上使用 IDE 1.16.0 版本验证。

项目设置
********

#. 开始之前，请按照 :ref:`getting_started` 确保 Zephyr 开发环境正常工作。

#. 从 Zephyr 环境启动 STM32CubeIDE，例如：

   .. code-block::

      $ /opt/st/stm32cubeide_1.16.0/stm32cubeide

#. 通过 :menuselection:`File --> New --> STM32 CMake Project` 打开已有项目：

   .. figure:: img/stm32cube_new_cmake.webp
      :align: center
      :alt: 创建新的 CMake 项目

#. 选择 :guilabel:`Project with existing CMake sources`，点击 :guilabel:`Next`。

#. 选择 :menuselection:`Next`，浏览到源码位置。打开的目录应包含 ``CMakeLists.txt`` 和 ``prj.conf``。

#. 选择 :menuselection:`Next`，选择合适的 MCU，点击 :guilabel:`Finish`。项目现在应已可见，但还需进一步配置。

#. 右键点击工作区中新建的项目，选择 :guilabel:`Properties`。

#. 进入 :guilabel:`C/C++ Build` 页面，将 Generator 设为 ``Ninja``。在 :guilabel:`Other Options` 中以 CMake 参数格式指定目标 ``BOARD``。如果目标开发板位于源码树外，还必须设置 ``BOARD_ROOT``。设置页面应类似如下：

   .. figure:: img/stm32cube_project_properties.webp
      :align: center
      :alt: 项目属性对话框

   是否需要这些选项，取决于项目是否位于源码树外。

#. 进入 :menuselection:`C/C++ General --> Preprocessor Include` 页面，选择 :guilabel:`GNU C` 语言，再点击 :menuselection:`CDT User Settings Entries`。

   .. figure:: img/stm32cube_preprocessor_include.webp
      :align: center
      :alt: 预处理器选项属性对话框

   点击 :guilabel:`Add` 添加 :guilabel:`Include File`，指向 Zephyr 的 ``autoconf.h``，其位置为 ``<build dir>/zephyr/include/generated/autoconf.h``。这可确保 STM32CubeIDE 识别 Zephyr 配置选项。出现以下对话框后，按图填写：

   .. figure:: img/stm32cube_add_include.webp
      :align: center
      :alt: 添加包含文件对话框

   添加包含文件后，属性页面应类似如下：

   .. figure:: img/stm32cube_autoconf_h.webp
      :align: center
      :alt: 添加 autoconf.h 后的属性页面

#. 点击 :guilabel:`Apply and Close`。

#. 现在可以使用工具栏 :guilabel:`Build` 按钮构建项目，通过 :guilabel:`Run` 运行，或通过 :guilabel:`Debug` 调试。

仅用于调试
**********

如果只想使用 STM32CubeIDE 调试项目，可执行以下步骤：

#. 先编译项目，确保已有 ``zephyr.elf``。

#. 启动 STM32CubeIDE，通过 :menuselection:`File --> Import...` 导入项目：

   .. figure:: img/stm32cube_menu_import.webp
      :align: center
      :alt: 导入项目

#. 选择 :menuselection:`C/C++ --> STM32 Cortex-M Executable`，点击 :guilabel:`Next`：

   .. figure:: img/stm32cube_import_project.webp
      :align: center
      :alt: 导入项目选择

#. 点击 :guilabel:`Browse` 浏览构建目录，选择 ``zephyr.elf``。

#. 点击 :guilabel:`Select` 选择 MCU。如果适用，也选择 CPU 和／或内核。

#. 点击 :guilabel:`Finish`。

#. 现在可以通过 :guilabel:`Debug` 按钮调试项目。

.. _STM32CubeIDE: https://www.st.com/en/development-tools/stm32cubeide.html
