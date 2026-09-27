.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _application:

应用开发
########

.. note::

   本文档中，我们假设：

   - 您的 **应用目录** 为 :file:`<app>` 目录，类似于 :file:`<home>/zephyrproject/app`
   - 其 **构建目录** 是 :file:`<app>/build`

   这些术语的定义见下文。在 Linux/macOS 上，<home> 等同于 ``~`` 目录。在 Windows 上，它等同于 ``%userprofile%`` 目录。

   将应用保留在工作区 :file:`<home>/zephyrproject` 内，可以更轻松地对其使用 ``west build`` 和其他命令。（不过，只要正确设置 :ref:`ZEPHYR_BASE <important-build-vars>` 变量，您可以将应用放在任何位置。）

概述
****

Zephyr 的构建系统基于 `CMake`_ 构建。

该构建系统以应用为中心，要求基于 Zephyr 的应用发起对 Zephyr 源代码的构建。应用构建控制应用本身和 Zephyr 的配置与构建过程，并将它们编译为单个二进制文件。

zephyr 主仓库包含 Zephyr 的源代码、配置文件和构建系统。您很可能还随 zephyr 仓库一起安装了各种 :ref:`modules` ，它们提供第三方源代码集成。

**应用目录** 中的文件将 Zephyr 和任何模块与应用关联起来。该目录包含所有应用专用文件，例如应用专用配置文件和源代码。

以下是一个简单 Zephyr 应用中的文件：

.. code-block:: none

   <app>
   ├── CMakeLists.txt
   ├── app.overlay
   ├── prj.conf
   ├── VERSION
   └── src
       └── main.c

这些内容分别是：

* **CMakeLists.txt** 文件：此文件告知构建系统在哪里找到其他应用文件，并将应用目录与 Zephyr 的 CMake 构建系统关联起来。这种关联提供了 Zephyr 构建系统支持的功能，例如开发板专用配置文件、在真实或仿真硬件上运行和调试已编译的二进制文件的能力，等等。

* **app.overlay** 文件：这是一个 Devicetree overlay 文件，用于指定应用专用更改；对于您构建的任何开发板，这些更改都应应用到基础 Devicetree 上。Devicetree overlay 的用途通常是配置应用所用硬件的某些方面。

  构建系统默认会查找 :file:`app.overlay` 文件，但您可以添加更多 Devicetree overlay，系统还会搜索其他默认文件。

  有关 Devicetree 的更多信息，请参见 :ref:`devicetree` 章节。

* **prj.conf** 文件：这是一个 Kconfig 片段，为一个或多个 Kconfig 选项指定应用专用值。这些应用设置会与其他设置合并，以生成最终配置。Kconfig 片段的用途通常是配置应用使用的软件功能。

  构建系统默认会查找 :file:`prj.conf` 文件，但您可以添加更多 Kconfig 片段，系统还会搜索其他默认文件。

  更多信息请参见下文 :ref:`application-kconfig` 章节。

* **VERSION** 文件：该文本文件包含多个版本信息字段。这些字段让您可以管理应用的生命周期，并在签署应用镜像时自动提供应用版本。

  有关此文件及其用法的更多信息，请参见 :ref:`app-version-details` 章节。

* **main.c** 文件：一个源代码文件。应用通常包含用 C、C++ 或汇编语言编写的源文件。Zephyr 的约定是将它们放在 :file:`<app>` 下名为 :file:`src` 的子目录中。

定义应用后，您将使用 CMake 生成一个 **构建目录** 用于存放构建应用和 Zephyr 所需的文件，然后将它们链接为可在开发板上运行的最终二进制文件。最简单的方法是使用 :ref:`west build <west-building>` 命令，但您也可以直接使用 CMake。应用构建产物始终在单独的构建目录中生成：Zephyr 不支持“树内”构建。

以下章节介绍如何创建、构建和运行 Zephyr 应用，随后提供更详细的参考资料。

.. _zephyr-app-types:

应用类型
********

我们根据 :file:`<app>` 所在的位置区分三种基本的 Zephyr 应用类型：

.. table::

   +---------------------------------------+----------------------------------+
   | 应用类型                              | :file:`<app>` 位置               |
   +---------------------------------------+----------------------------------+
   | :ref:`仓库 <zephyr-repo-app>`         | zephyr 仓库                      |
   +---------------------------------------+----------------------------------+
   | :ref:`工作区 <zephyr-workspace-app>`  | 安装 Zephyr 的 west 工作区       |
   +---------------------------------------+----------------------------------+
   | :ref:`独立 <zephyr-freestanding-app>` | 其他位置                         |
   +---------------------------------------+----------------------------------+

我们将在下文进一步讨论这些内容。要了解构建系统如何支持每种类型，请参见 :ref:`cmake_pkg` 章节。

.. _zephyr-repo-app:

Zephyr 仓库应用
===============

位于 Zephyr :ref:`west 工作区 <west-workspaces>` 内 ``zephyr`` 源代码仓库中的应用称为 Zephyr 仓库应用。在以下示例中，:zephyr:code-sample:`hello_world 示例 <hello_world>` 就是一个 Zephyr 仓库应用：

.. code-block:: none

   zephyrproject/
   ├─── .west/
   │    └─── config
   └─── zephyr/
        ├── arch/
        ├── boards/
        ├── cmake/
        ├── samples/
        │    ├── hello_world/
        │    └── ...
        ├── tests/
        └── ...

.. _zephyr-workspace-app:

Zephyr 工作区应用
=================

位于 :ref:`工作区 <west-workspaces>` 内但在 zephyr 仓库之外的应用称为 Zephyr 工作区应用。在以下示例中， ``app`` 就是一个 Zephyr 工作区应用：

.. code-block:: none

   zephyrproject/
   ├─── .west/
   │    └─── config
   ├─── zephyr/
   ├─── bootloader/
   ├─── modules/
   ├─── tools/
   ├─── <vendor/private-repositories>/
   └─── applications/
        └── app/

.. _zephyr-freestanding-app:

Zephyr 独立应用
===============

位于 Zephyr :ref:`工作区 <west-workspaces>` 之外的 Zephyr 应用称为 Zephyr 独立应用。在以下示例中， ``app`` 就是一个 Zephyr 独立应用：

.. code-block:: none

   <home>/
   ├─── zephyrproject/
   │     ├─── .west/
   │     │    └─── config
   │     ├── zephyr/
   │     ├── bootloader/
   │     ├── modules/
   │     └── ...
   │
   └─── app/
        ├── CMakeLists.txt
        ├── prj.conf
        └── src/
            └── main.c

.. _zephyr-creating-app:

创建应用
********

在 Zephyr 中，您既可以使用参考工作区应用，也可以手动创建自己的应用。

.. _zephyr-creating-app-from-example:

使用参考工作区应用
==================

`example-application`_ Git 仓库包含一个可供参考的 :ref:`工作区应用 <zephyr-workspace-app>` 实例。建议在按下文所述创建自己的应用时，将其用作参考。

example-application 仓库演示了如何使用若干常用功能，例如：

- 自定义 :ref:`开发板移植 <board_porting_guide>`
- 自定义 :ref:`Devicetree 绑定 <dt-bindings>`
- 自定义 :ref:`设备驱动程序 <device_model_api>`
- 持续集成（CI）设置，包括使用 :ref:`twister <twister_script>`
- 自定义 west :ref:`扩展命令 <west-extensions>`

example-application 基本用法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在现有 Zephyr 工作区中开始使用 example-application 仓库，最简单的方法是按照以下步骤操作：

.. code-block:: console

   cd <home>/zephyrproject
   git clone https://github.com/zephyrproject-rtos/example-application my-app

上面的目录名 :file:`my-app` 是任意的：可根据需要更改。现在您可以进入此目录，并根据需要调整其内容。由于使用的是现有 Zephyr 工作区，您可以使用 ``west build`` 或任何其他 west 命令来构建、烧录和调试。

example-application 高级用法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

您还可以将 example-application 仓库作为构建自己定制的、基于 Zephyr 的软件发行版的起点。这样您可以执行以下操作：

- 移除不需要的 Zephyr 模块
- 添加自己的其他自定义仓库
- 用您自己的版本覆盖 Zephyr 提供的仓库
- 与他人共享成果并进一步协作

example-application 仓库包含 :file:`west.yml` 文件，因此它也可以作为 west :ref:`manifest 仓库 <west-workspace>` 使用。按照以下步骤操作，即可用它创建一个新的自定义工作区：

.. code-block:: console

   cd <home>
   mkdir my-workspace
   cd my-workspace
   git clone https://github.com/zephyrproject-rtos/example-application my-manifest-repo
   west init -l my-manifest-repo

这将创建一个采用 :ref:`T2 拓扑 <west-t2>` 的新工作区，并将 :file:`my-manifest-repo` 作为 manifest 仓库。:file:`my-workspace` 和 :file:`my-manifest-repo` 名称是任意的：可根据需要更改。

接下来，定制 manifest 仓库。克隆该仓库时，其初始内容将与 example-application 的内容相同。然后，您可以按自己的喜好编辑 :file:`my-manifest-repo/west.yml` 文件，随意更改其中的仓库集合。有关如何根据需要从工作区添加或移除不同仓库，请参见 :ref:`west-manifest-import` 中的许多示例。最后，对其他文件进行所需的任何其他更改。

满意后，可以运行：

.. code-block::

   west update

然后您的工作区就可以使用了。

如果将生成的 :file:`my-manifest-repo` 仓库推送到其他地方，您就可以与他人共享您的工作。例如，假设您将仓库推送到 ``https://git.example.com/my-manifest-repo`` 这个地址。其他人就可以通过运行以下命令来设置一个匹配的工作区：

.. code-block::

   west init -m https://git.example.com/my-manifest-repo my-workspace
   cd my-workspace
   west update

从现在起，您可以通过将更改推送到所使用的仓库，并按需更新 :file:`my-manifest-repo/west.yml` 以添加或移除仓库或更改其内容，从而在共享软件上开展协作。

.. _zephyr-creating-app-by-hand:

手动创建应用
============

您可以按照以下步骤从头创建基本应用目录。不过，使用 `example-application`_ 仓库或 Zephyr 的某个 :zephyr:code-sample-category:`samples` 作为起点可能更简单。

#. 创建应用目录。

   例如，在 Unix shell 或 Windows ``cmd.exe`` 提示符中：

   .. code-block:: console

      mkdir app

   .. warning::

      不支持在路径中任何位置包含空格的情况下构建 Zephyr 或创建应用。因此，Windows 路径 :file:`C:\\Users\\YourName\\app` 可以正常工作，但 :file:`C:\\Users\\Your Name\\app` 不行。

#. 创建源代码文件。

   建议将所有应用源代码放在名为 :file:`src` 的子目录中。这样更容易区分项目文件和源代码。

   继续前面的示例，输入：

   .. code-block:: console

      cd app
      mkdir src

#. 将应用源代码放在 :file:`src` 子目录中。在本示例中，假设您已创建名为 :file:`src/main.c` 的文件。

#. 在 ``app`` 目录中创建名为 :file:`CMakeLists.txt` 的文件，内容如下：

   .. code-block:: cmake

      cmake_minimum_required(VERSION 3.28.0)

      find_package(Zephyr)
      project(my_zephyr_app)

      target_sources(app PRIVATE src/main.c)

   备注：

   - ``cmake_minimum_required()`` 调用是 CMake 所要求的。下一行的 Zephyr 软件包也会调用它。如果 CMake 的版本低于 :file:`CMakeLists.txt` 中的版本或 Zephyr 软件包中的版本号，CMake 将报错。

   - ``find_package(Zephyr)`` 会引入 Zephyr 构建系统，该系统会创建一个名为 ``app`` 的 CMake 目标（参见 :ref:`cmake_pkg`）。向此目标添加源文件即可将其纳入构建。Zephyr 软件包会将 ``Zephyr-Kernel`` 定义为一个 CMake 项目，并启用对 ``C``、``CXX``、``ASM`` 语言的支持。

   - ``project(my_zephyr_app)`` 定义应用的 CMake 项目。必须在 ``find_package(Zephyr)`` 之后调用，以避免干扰 Zephyr 的 ``project(Zephyr-Kernel)``。

   - ``target_sources(app PRIVATE src/main.c)`` 用于将源文件添加到 ``app`` 目标。此语句必须位于定义该目标的 ``find_package(Zephyr)`` 之后。可以使用 ``target_sources()`` 添加任意数量的文件。

#. 为应用创建至少一个 Kconfig 片段（通常命名为 :file:`prj.conf`），并在其中设置应用所需的 Kconfig 选项值。参见 :ref:`application-kconfig`。如果不需要设置任何 Kconfig 选项，请创建一个空文件。

#. 配置应用所需的任何 Devicetree overlay，通常放在名为 :file:`app.overlay` 的文件中。参见 :ref:`set-devicetree-overlays`。

#. 设置可能需要的任何其他文件，例如 :ref:`twister <twister_script>` 配置文件、持续集成文件、文档等。

.. _important-build-vars:

重要的构建系统变量
******************

可以使用许多变量来控制 Zephyr 构建系统。本节介绍每位 Zephyr 开发人员都应了解的最重要的变量。

.. note::

   变量 :makevar:`BOARD`、:makevar:`CONF_FILE` 和 :makevar:`DTC_OVERLAY_FILE` 可以通过 3 种方式提供给构建系统（按优先级顺序）：

   * 作为 ``west build`` 或 ``cmake`` 调用的参数，通过 ``-D`` 命令行开关传入。如果存在多个 overlay 文件，应使用引号，例如 ``"file1.overlay;file2.overlay"``
   * 作为 :ref:`env_vars`。
   * 在 :file:`CMakeLists.txt` 中作为 ``set(<VARIABLE> <VALUE>)`` 语句

* :makevar:`ZEPHYR_BASE`：构建系统使用的 Zephyr base 变量。``find_package(Zephyr)`` 会自动将其设置为缓存的 CMake 变量。但 ``ZEPHYR_BASE`` 也可以设置为环境变量，以强制 CMake 使用特定的 Zephyr 安装。

* :makevar:`BOARD`：选择应用构建用于默认配置的开发板。有关内置开发板，请参见 :ref:`boards`；有关添加开发板支持的信息，请参见 :ref:`board_porting_guide`。

* :makevar:`CONF_FILE`：指定一个或多个 Kconfig 配置片段文件的名称。多个文件名可以用空格或分号分隔。每个文件包含覆盖默认配置值的 Kconfig 配置值。

  更多信息请参见 :ref:`initial-conf`。

* :makevar:`EXTRA_CONF_FILE`：额外的 Kconfig 配置片段文件。多个文件名可以用空格或分号分隔。当需要让 :makevar:`CONF_FILE` 保持默认值，同时“混入”一些额外的配置选项时，这会很有用。

* :makevar:`DTC_OVERLAY_FILE`：要使用的一个或多个 Devicetree overlay 文件。多个文件可以用分号分隔。示例请参见 :ref:`set-devicetree-overlays`，有关 Devicetree 和 Zephyr 的信息请参见 :ref:`devicetree-intro`。

* :makevar:`EXTRA_DTC_OVERLAY_FILE`：要使用的额外 Devicetree overlay 文件。多个文件可以用分号分隔。当需要让 :makevar:`DTC_OVERLAY_FILE` 保持默认值，同时“混入”一些额外的 overlay 文件时，这会很有用。

* :makevar:`SHIELD`：参见 :ref:`shields`

* :makevar:`ZEPHYR_MODULES`：一个 `CMake list`_，其中包含应在此应用构建中使用的其他目录（内含源代码、Kconfig 等）的绝对路径。详情请参见 :ref:`modules`。如果设置此变量，它必须是所有要使用的模块的完整列表，因为构建系统不会自动从 west 获取任何模块。

* :makevar:`EXTRA_ZEPHYR_MODULES`：类似于 :makevar:`ZEPHYR_MODULES`，区别在于这些模块会追加到通过 west 找到的模块列表中，而不是替换该列表。

* :makevar:`FILE_SUFFIX`：可选的文件名后缀，会添加到 Kconfig 片段和 Devicetree overlay 的文件名中（如果这些文件存在，否则将回退为不带该前缀的名称）。详情请参见 :ref:`application-file-suffixes`。

* :makevar:`KCONFIG_WARNING_AS_ERROR`：将每条 Kconfig 警告都视为错误，包括默认情况下仅打印的警告。详情请参见 :ref:`kconfig_warning_as_error`。

.. note::

   可以使用 :ref:`cmake_build_config_package` 来共享这些变量的通用设置。

.. _zephyr-app-cmakelists:

应用 CMakeLists.txt
*******************

每个应用都必须有一个 :file:`CMakeLists.txt` 文件。该文件是构建系统的入口点，即顶层。最终的 :file:`zephyr.elf` 镜像同时包含应用和内核库。

本节介绍您可以在自己的 :file:`CMakeLists.txt` 中完成的部分操作。请务必按顺序执行这些步骤。

#. 如果只想为一个开发板构建，请在新增的一行中添加应用的开发板配置名称。例如：

   .. code-block:: cmake

      set(BOARD qemu_x86)

   有关可用开发板的更多信息，请参见 :ref:`boards`。

   Zephyr 构建系统按顺序检查以下内容来确定 :makevar:`BOARD` 的值（当找到 BOARD 值时，CMake 会停止继续检查列表后面的项）：

   - 由 CMake 缓存确定的任何先前使用过的值优先级最高。这可确保不会尝试使用与构建配置步骤中所设置的不同 :makevar:`BOARD` 值来运行构建。

   - 接下来将检查并使用在 CMake 命令行上（直接或通过 ``west build`` 间接）使用 ``-DBOARD=YOUR_BOARD`` 给出的任何值。

   - 如果设置了 :ref:`环境变量 <env_vars>` ``BOARD``，则会使用其值。

   - 最后，如果按本步骤所述在应用的 :file:`CMakeLists.txt` 中设置了 ``BOARD``，则将使用该值。

#. 如果应用使用的配置文件不是通常的 :file:`prj.conf`，请添加相应的行，将 :makevar:`CONF_FILE` 变量适当地设置为这些文件。如果给出多个文件名，请用单个空格或分号分隔。当希望避免在单一位置设置 :makevar:`CONF_FILE` 时，可以使用 CMake 列表以模块化方式逐步构建配置片段文件。例如：

   .. code-block:: cmake

     set(CONF_FILE "fragment_file1.conf")
     list(APPEND CONF_FILE "fragment_file2.conf")

   更多信息请参见 :ref:`initial-conf`。

#. 如果应用使用了 Devicetree overlay，可能需要设置 :ref:`DTC_OVERLAY_FILE <important-build-vars>`。参见 :ref:`set-devicetree-overlays`。

#. 如果应用有自己的内核配置选项，请在与应用的 :file:`CMakeLists.txt` 相同的目录中创建 :file:`Kconfig` 文件。

   详细的 Kconfig 文档请参见 :ref:`手册中的 Kconfig 章节 <kconfig>`。

   一种（不太常见的）高级用例是：应用具有自己独特的配置 **选项**，并且这些选项需要根据构建配置设置不同的值。

   如果只是想为现有 Zephyr 配置选项设置应用特定的 **值**，请参见上面的 :makevar:`CONF_FILE` 说明。

   按如下方式组织 :file:`Kconfig` 文件：

   .. literalinclude:: application-kconfig.include
      :language: kconfig

   .. note::

      ``source`` 语句中的环境变量会直接展开，因此不需要定义 ``option env="ZEPHYR_BASE"`` 这样的 Kconfig “bounce” 符号。如果使用此类符号，其名称必须与环境变量相同。

      更多信息请参见 :ref:`kconfig_extensions`。

   将 :file:`Kconfig` 文件放在应用目录中时会自动检测到它；但如果使用绝对路径设置 CMake 变量 :makevar:`KCONFIG_ROOT`，也可以在其他位置找到它。

#. 另起一行指定应用需要 Zephyr，**且必须放在上述步骤添加的所有行之后**：

   .. code-block:: cmake

      find_package(Zephyr)
      project(my_zephyr_app)

   .. note:: 如果需要支持通过显式设置 ``ZEPHYR_BASE`` 环境变量来强制使用特定的 Zephyr 安装，则可以使用 ``find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})``。Zephyr 中的所有示例都支持 ``ZEPHYR_BASE`` 环境变量。

#. 现在将任何应用源文件添加到 'app' 目标库中，每个文件单独一行，如下所示：

   .. code-block:: cmake

      target_sources(app PRIVATE src/main.c)

下面是一个简单的示例 :file:`CMakeList.txt`：

.. code-block:: cmake

   set(BOARD qemu_x86)

   find_package(Zephyr)
   project(my_zephyr_app)

   target_sources(app PRIVATE src/main.c)

CMake 属性 ``HEX_FILES_TO_MERGE`` 利用 Kconfig 和 CMake 提供的应用配置，使您可以将外部构建的 hex 文件与构建 Zephyr 应用时生成的 hex 文件合并。例如：

.. code-block:: cmake

  set_property(GLOBAL APPEND PROPERTY HEX_FILES_TO_MERGE
      ${app_bootloader_hex}
      ${PROJECT_BINARY_DIR}/${KERNEL_HEX_NAME}
      ${app_provision_hex})

.. _zephyr-app-cmakecache:

CMakeCache.txt
**************

CMake 使用 CMakeCache.txt 文件作为持久化的键/值字符串存储，用于在多次运行之间缓存值，包括编译和构建选项以及库依赖项的路径。当 CMake 在空的构建目录中运行时，会创建此缓存文件。

有关 CMakeCache.txt 文件的更多详细信息，请参阅官方的 `CMake Cache`_ 文档。

.. _CMake Cache: https://cmake.org/cmake/help/book/mastering-cmake/chapter/CMake%20Cache.html


应用配置
********

.. _application-configuration-directory:

应用配置目录
============

Zephyr 将使用应用配置目录中的配置文件，但前面所述参数（例如 ``CONF_FILE``、``EXTRA_CONF_FILE``、``DTC_OVERLAY_FILE`` 和 ``EXTRA_DTC_OVERLAY_FILE``）提供了绝对路径的文件除外。

应用配置目录由 ``APPLICATION_CONFIG_DIR`` 变量定义。

``APPLICATION_CONFIG_DIR`` 将由以下来源之一设置，优先级最高的列在最前面。

1. 如果用户通过 ``-DAPPLICATION_CONFIG_DIR=<path>`` 指定 ``APPLICATION_CONFIG_DIR``，或在 CMake 文件中于 ``find_package(Zephyr)`` 之前指定，则该文件夹将用作应用的配置目录。

2. 应用的源码目录。

.. _application-kconfig:

Kconfig 配置
============

应用配置选项通常设置在应用目录的 :file:`prj.conf` 中。例如，可以使用以下赋值启用 C++ 支持：

.. code-block:: cfg

   CONFIG_CPP=y

查看 :zephyr:code-sample-category:`现有示例 <samples>` 是入门的好方法。

有关设置 Kconfig 配置值的详细文档，请参阅 :ref:`setting_configuration_values`。同一页面里的 :ref:`initial-conf` 小节说明了初始配置是如何推导出来的。有关配置选项的完整列表，请参阅 :ref:`kconfig-search`。有关与 Kconfig 选项相关的安全信息，请参阅 :ref:`hardening`。

手册里 :ref:`Kconfig 章节 <kconfig>` 中的其他页面也值得一读，尤其是在你打算添加新的配置选项时。

实验性功能
~~~~~~~~~~

Zephyr 是一个持续开发的项目，因此有些功能仍处于其开发周期的早期阶段。此类功能会在其 Kconfig 标题中标记为 ``[EXPERIMENTAL]``。

如果启用了任何实验性功能，可以使用 :kconfig:option:`CONFIG_WARN_EXPERIMENTAL` 设置在 CMake 配置阶段启用警告。

.. code-block:: cfg

   CONFIG_WARN_EXPERIMENTAL=y

例如，如果选项 ``CONFIG_FOO`` 是实验性的，那么启用它以及 :kconfig:option:`CONFIG_WARN_EXPERIMENTAL` 后，在构建应用时会在 CMake 配置阶段打印以下警告：

.. code-block:: none

   warning: Experimental symbol FOO is enabled.

Devicetree 叠加层
=================

请参阅 :ref:`set-devicetree-overlays`。

.. _application-file-suffixes:

文件后缀
========

Zephyr 应用可能希望用同一代码库为不同的构建/产品变体提供多种配置，这需要使用不同的 Kconfig 选项和 Devicetree 配置。为了更好地进行这种配置，Zephyr 在配置应用时提供了 :makevar:`FILE_SUFFIX` 选项，它可以自动附加到文件名中。该选项适用于 Kconfig 片段和开发板叠加层，但带有回退机制：如果这类文件不存在，则会改用不带这些后缀的文件。

假设示例项目结构如下：

.. code-block:: none

   <app>
   ├── CMakeLists.txt
   ├── prj.conf
   ├── prj_mouse.conf
   ├── boards
   │   ├── native_sim.overlay
   │   └── qemu_cortex_m3_mouse.overlay
   └── src
       └── main.c

* 如果在未为 ``native_sim`` 定义 ``FILE_SUFFIX`` 的情况下按常规构建，则会使用 ``prj.conf`` 和 ``boards/native_sim.overlay``。

* 如果在未为 ``qemu_cortex_m3`` 定义 ``FILE_SUFFIX`` 的情况下按常规构建，则会使用 ``prj.conf``，不会使用应用 Devicetree 叠加层。

* 如果在为 ``native_sim`` 构建时将 ``FILE_SUFFIX`` 设置为 ``mouse``，则会使用 ``prj_mouse.conf`` 和 ``boards/native_sim.overlay``；由于不存在 ``native_sim_mouse.overlay`` 文件，因此会回退到 ``native_sim.overlay``。

* 如果在为 ``qemu_cortex_m3`` 构建时将 ``FILE_SUFFIX`` 设置为 ``mouse``，则会使用 ``prj_mouse.conf``，并使用 ``boards/qemu_cortex_m3_mouse.overlay``。

应用专用代码
************

应用专用源代码文件通常添加到应用的 :file:`src` 目录中。如果应用添加了大量文件，开发者可以将它们分组到 :file:`src` 下的子目录中，深度不限。

应用专用源代码不应使用内核为其自身保留的符号名前缀。有关更多信息，请参阅 `命名约定 <https://github.com/zephyrproject-rtos/zephyr/wiki/Naming-Conventions>`_。

第三方库代码
============

可以在应用的 :file:`src` 目录之外构建库代码，但应用代码和库代码必须面向相同的应用二进制接口（ABI）。在大多数架构上，都有用于控制所面向 ABI 的编译器标志，因此库和应用必须共用某些编译器标志。让胶合代码能够访问 Zephyr 内核头文件也可能很有用。

为了更轻松地集成第三方组件，Zephyr 构建系统定义了一些 CMake 函数，让应用构建脚本能够访问 Zephyr 编译器选项。这些函数记录并定义在 :zephyr_file:`cmake/modules/extensions.cmake` 中，并遵循 ``zephyr_get_<type>_<format>`` 命名约定。

通常需要将以下变量导出到第三方构建系统。

* ``CMAKE_C_COMPILER``、``CMAKE_AR``。

* ``ARCH`` 和 ``BOARD``，以及若干用于标识 Zephyr 内核版本的变量。

:zephyr_file:`samples/application_development/external_lib` 是一个示例项目，演示了其中一些功能。


.. _build_an_application:

构建应用
********

Zephyr 构建系统会将应用的所有组件编译并链接为单个应用映像，该映像可以在仿真硬件或真实硬件上运行。

与任何其他基于 CMake 的系统一样，构建过程 :ref:`分为两个阶段 <cmake-details>`。首先，使用 ``cmake`` 命令行工具并指定生成器来生成构建文件（也称为构建系统）。该生成器决定了构建系统在第二阶段所用的原生构建工具。第二阶段运行原生构建工具，实际构建源文件并生成映像。要了解有关这些概念的更多信息，请参阅官方 CMake 文档中的 `CMake introduction`_。

尽管 Zephyr 中默认的构建工具是 :std:ref:`west <west>`，即 Zephyr 的元工具，它在后台调用 ``cmake`` 以及底层构建工具（``ninja`` 或 ``make``），但你也可以选择直接调用 ``cmake``。在 Linux 和 macOS 上，你可以在 ``make`` 和 ``ninja`` 生成器（即构建工具）之间进行选择，而在 Windows 上需要使用 ``ninja``，因为该平台不支持 ``make``。为简单起见，本指南将始终使用 ``ninja``；如果你选择使用 ``west build`` 构建应用，请注意它在底层默认使用 ``ninja``。

作为示例，我们来为 ``reel_board`` 构建 Hello World 示例：

.. zephyr-app-commands::
   :tool: all
   :zephyr-app: samples/hello_world
   :board: reel_board
   :goals: build

在 Linux 和 macOS 上，你也可以使用 ``make`` 代替 ``ninja`` 进行构建：

使用 west：

- 要仅使用一次 ``make``，请在 west build 命令行中添加 ``-- -G"Unix Makefiles"``；有关示例，请参阅 :ref:`west build <west-building-generator>` 文档。
- 要此后默认使用 ``make``，请运行 ``west config build.generator "Unix Makefiles"``。

直接使用 CMake：

.. zephyr-app-commands::
   :tool: cmake
   :zephyr-app: samples/hello_world
   :generator: make
   :host-os: unix
   :board: reel_board
   :goals: build


基本用法
========

#. 导航到应用目录 :file:`<app>`。
#. 输入以下命令，为命令行参数中指定的开发板构建应用的 :file:`zephyr.elf` 映像：

   .. zephyr-app-commands::
      :tool: all
      :cd-into:
      :board: <board>
      :goals: build

   如果需要，你可以使用 :code:`CONF_FILE` 参数，依据备用的 :file:`.conf` 文件中所指定的配置设置来构建应用。这些设置将覆盖应用的 :file:`.config` 文件或其默认 :file:`.conf` 文件中的设置。例如：

   .. zephyr-app-commands::
      :tool: all
      :cd-into:
      :board: <board>
      :gen-args: -DCONF_FILE=prj.alternate.conf
      :goals: build
      :compact:

   如上一节所述，你也可以选择永久设置开发板和配置：既可以导出 :makevar:`BOARD` 和 :makevar:`CONF_FILE` 环境变量，也可以在 :file:`CMakeLists.txt` 中使用 ``set()`` 语句设置它们的值。此外，``west`` 允许你 :ref:`设置默认开发板 <west-building-config>`。

.. _build-directory-contents:

构建目录内容
============

使用 Ninja 生成器时，构建目录如下所示：

.. code-block:: none

   <app>/build
   ├── build.ninja
   ├── CMakeCache.txt
   ├── CMakeFiles
   ├── cmake_install.cmake
   ├── rules.ninja
   └── zephyr

构建目录中最值得注意的文件有：

* :file:`build.ninja`，可用于构建应用。

* :file:`zephyr` 目录，它是所生成构建系统的工作目录，也是大多数生成文件的创建和存储位置。

运行 ``ninja`` 后，以下构建输出文件将写入构建目录的 :file:`zephyr` 子目录。（它 **不是 Zephyr 基础目录**，后者包含 Zephyr 源代码等，详见上文。）

* :file:`.config`，其中包含用于构建应用的配置设置。

  .. note::

     每当配置更新时，:file:`.config` 的先前版本都会保存到 :file:`.config.old`。这样做是为了方便，因为对比新旧版本很有用。

* 各种目标文件（:file:`.o` 文件和 :file:`.a` 文件），其中包含已编译的内核和应用代码。

* :file:`zephyr.elf`，其中包含最终合并的应用和内核二进制文件。也支持其他二进制输出格式，例如 :file:`.hex` 和 :file:`.bin`。

.. _application_rebuild:

重新构建应用
============

在持续测试更改时，应用开发的效率通常最高。随着应用变得越来越复杂，频繁重新构建应用可以减轻调试的痛苦。在对应用的源文件、CMakeLists.txt 文件或配置设置进行任何重大更改后，通常最好重新构建并测试。

.. important::

    Zephyr 构建系统只重新构建应用映像中可能受更改影响的部分。因此，重新构建应用通常比首次构建快得多。

有时构建系统无法正确重新构建应用，因为它未能重新编译一个或多个必需的文件。你可以通过以下步骤强制构建系统从头重新构建整个应用：

#. 在主机上打开终端控制台，然后导航到构建目录 :file:`<app>/build`。

#. 根据你是想直接使用 ``west`` 还是 ``cmake`` 来删除应用生成的文件（但保留包含应用当前配置信息的 :file:`.config` 文件），输入以下命令之一。

   .. code-block:: console

       west build -t clean

   或

   .. code-block:: console

       ninja clean

   或者，输入以下命令之一来删除 *所有* 生成的文件，包括包含这些开发板类型的应用当前配置信息的 :file:`.config` 文件。

   .. code-block:: console

       west build -t pristine

   或

   .. code-block:: console

       ninja pristine

   如果使用 west，你可以利用它在需要时自动 :ref:`将构建文件夹恢复为纯净状态 <west-building-config>` 的能力。

#. 按照上文 :ref:`build_an_application` 中指定的步骤正常重新构建应用。

.. _application_board_version:

为开发板修订版构建
==================

Zephyr 构建系统支持为单个开发板指定多个仅有微小差异的硬件修订版。使用修订版可以让开发板支持文件对开发板配置进行小幅调整，而无需为每个修订版复制 :ref:`create-your-board-directory` 中描述的所有文件。

要为特定修订版构建，请使用 ``<board>@<revision>`` 或 ``<board>@<revision>/<qualifiers>``，而不是普通的 ``<board>`` 或 ``<board>/<qualifiers>``。例如：

.. zephyr-app-commands::
   :tool: all
   :cd-into:
   :board: nrf9160dk@0.14.0/nrf9160/ns
   :goals: build
   :compact:

请查看开发板文档，了解它是否有多个修订版，以及支持哪些修订版。

针对开发板修订版进行构建时，CMake 配置阶段会打印当前启用的修订版，如下所示：

.. code-block:: console

   -- Board: plank, Revision: 1.5.0

.. _application_run:

运行应用
********

应用映像可以在真实开发板或仿真硬件上运行。

.. _application_run_board:

在开发板上运行
==============

Zephyr 支持的大多数开发板都可以使用 ``west flash`` 烧录编译后的二进制文件，将其复制到开发板并运行。请按照以下说明在真实硬件上烧录并运行应用：

#. 构建应用，如 :ref:`build_an_application` 中所述。

#. 确保开发板已连接到主机。通常通过 USB 完成连接。

#. 在构建目录 :file:`<app>/build` 中运行以下控制台命令，以将编译好的 Zephyr 映像烧录到开发板并运行：

   .. code-block:: console

      west flash

Zephyr 构建系统会与开发板支持文件集成，以使用特定于硬件的工具将 Zephyr 二进制文件烧录到你的硬件上，然后运行它。

每次运行烧录命令时，你的应用都会被重新构建并再次烧录。

如果开发板支持不完整，可能不支持通过 Zephyr 构建系统进行烧录。如果你收到有关烧录支持不可用的错误消息，请查阅 :ref:`你的开发板文档 <boards>` 以获取有关如何烧录开发板的更多信息。

.. note:: 在 Linux 上开发时，通常需要安装特定于开发板的 udev 规则，以便能够以非 root 用户身份通过 USB 访问开发板。如果烧录失败，请查阅开发板文档，确认是否需要这样做。

.. _application_run_qemu:

在模拟器中运行
==============

Zephyr 内置了对 QEMU 的模拟器支持。它允许你在实际目标硬件上加载和运行应用之前（或代替加载运行），以虚拟方式运行和测试应用。

有关 Windows 上所需的额外步骤，请参阅 :ref:`beyond-GSG`。

按照以下说明通过 QEMU 运行应用：

#. 如 :ref:`build_an_application` 中所述，为其中一个 QEMU 开发板构建你的应用。

   例如，你可以将 ``BOARD`` 设置为：

   - ``qemu_x86`` 用于仿真在基于 x86 的开发板上运行
   - ``qemu_cortex_m3`` 用于仿真在基于 ARM Cortex M3 的开发板上运行

#. 在构建目录 :file:`<app>/build` 中运行以下控制台命令之一，以在 QEMU 中运行 Zephyr 二进制文件：

   .. code-block:: console

      west build -t run

   或

   .. code-block:: console

      ninja run

#. 按下 :kbd:`Ctrl A, X` 可停止在 QEMU 中运行的应用。

   应用停止运行，终端控制台提示符会重新显示。

每次执行运行命令时，你的应用都会被重新构建并再次运行。


.. note::

   如果已安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>`，则 ``run`` 目标默认会使用该 SDK 的 QEMU 二进制文件。若要改用其他版本的 QEMU，请 :ref:`设置环境变量 <env_vars>` ``QEMU_BIN_PATH``，使其指向你想使用的 QEMU 二进制文件路径。

.. note::

   你可以通过在目标名称后追加 ``_<emulator>`` 来选择特定的模拟器，例如对于 QEMU 可使用 ``west build -t run_qemu`` 或 ``ninja run_qemu``。

.. _custom_board_definition:

自定义开发板、Devicetree 和 SOC 定义
************************************

如果你正在开发的开发板或平台尚未得到 Zephyr 支持，你可以将开发板、Devicetree 和 SOC 定义添加到应用中，而不必将它们添加到 Zephyr 代码树中。

支持树外开发板和 SOC 开发所需的结构与 Zephyr 代码树中维护开发板和 SOC 的方式类似。采用这种结构后，在初期开发完成后，将平台相关工作贡献到 Zephyr 代码树上游会容易得多。

使用以下结构将自定义开发板添加到你的应用或专用仓库中：

.. code-block:: console

   boards/
   soc/
   CMakeLists.txt
   prj.conf
   README.rst
   src/

其中 ``boards`` 目录用于存放你要为之构建的开发板：

.. code-block:: console

   .
   ├── boards
   │   └── vendor
   │       └── my_custom_board
   │           ├── doc
   │           │   └── img
   │           └── support
   └── src

``soc`` 目录则存放任何 SOC 代码。你也可以让开发板由 Zephyr 代码树中已有的 SOC 来支持。

开发板
======

对于 ``my_custom_board``，请在 ``boards`` 下使用厂商名称作为文件夹名（若要向上游 Zephyr 提交，该名称必须与 :zephyr_file:`dts/bindings/vendor-prefixes.txt` 中的厂商前缀一致；如果不是厂商开发板，则应为 ``others``）。

文档（位于 ``doc/`` 下）和支持文件（位于 ``support/`` 下）是可选的，但在向 Zephyr 提交时是必需的。

``my_custom_board`` 的内容应遵循适用于任何 Zephyr 开发板的相同准则，并提供以下文件::

    board.yml
    my_custom_board_defconfig
    my_custom_board.dts
    my_custom_board.yaml
    board.cmake
    board.h
    CMakeLists.txt
    doc/
    Kconfig.my_custom_board
    Kconfig.defconfig
    support/


开发板结构就绪后，你可以通过向 CMake 构建系统传入 ``-DBOARD_ROOT`` 参数来指定自定义开发板信息的位置，从而构建面向该开发板的应用：

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DBOARD_ROOT=<path to boards>
   :goals: build
   :compact:

这将使用你的自定义开发板配置，并将 Zephyr 二进制文件生成到你的应用目录中。

你也可以在应用的 :file:`CMakeLists.txt` 文件中定义 ``BOARD_ROOT`` 变量。请务必在使用 ``find_package(Zephyr ...)`` 引入 Zephyr 样板代码 **之前** 完成此操作。

.. note::

   在 CMakeLists.txt 中指定 ``BOARD_ROOT`` 时，必须提供绝对路径，例如 ``list(APPEND BOARD_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/<extra-board-root>)``。使用 ``-DBOARD_ROOT=<board-root>`` 时，绝对路径和相对路径均可使用。相对路径会相对于应用目录进行解析。

.. note::

   使用 sysbuild 时，``BOARD_ROOT`` 必须在模块或 sysbuild 的 ``CMakeLists.txt`` 文件中定义，详情请参阅 :ref:`sysbuild_var_override`。

SOC 定义
========

与开发板支持类似，其结构与 Zephyr 代码树中维护 SOC 的方式相似，例如：

.. code-block:: none

        soc
        └── st
            └── stm32
                ├── common
                └── stm32l0x


文件 :zephyr_file:`soc/Kconfig` 将在 Kconfig 中创建顶层 ``SoC/CPU/Configuration Selection`` 菜单。

可以使用 ``SOC_ROOT`` CMake 变量将树外 SoC 定义添加到此菜单中。该变量包含一个以分号分隔的目录列表，这些目录中存放着 SoC 支持文件。

按照上述结构，可以添加以下文件以将更多 SoC 加载到菜单中。

.. code-block:: none

        soc
        └── st
            └── stm32
                └── stm32l0x
                    ├── Kconfig
                    ├── Kconfig.soc
                    └── Kconfig.defconfig

上述 Kconfig 文件可以描述 SoC，也可以加载其他 SoC Kconfig 文件。

在此结构中加载 ``stm32l0`` 专用 Kconfig 文件的示例：

.. code-block:: none

        soc
        └── st
            └── stm32
                ├── Kconfig.soc
                └── stm32l0x
                    └── Kconfig.soc

可通过 ``st/stm32/Kconfig.soc`` 中的以下内容实现：

.. code-block:: kconfig

   rsource "*/Kconfig.soc"

SOC 结构就绪后，你可以通过向 CMake 构建系统传入 ``-DSOC_ROOT`` 参数来指定自定义平台信息的位置，从而构建面向该平台的应用：

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DSOC_ROOT=<path to soc> -DBOARD_ROOT=<path to boards>
   :goals: build
   :compact:

这将使用你的自定义平台配置，并将 Zephyr 二进制文件生成到你的应用目录中。

有关在模块的 :file:`zephyr/module.yml` 文件中设置 SOC_ROOT 的信息，请参阅 :ref:`modules_build_settings`。

或者，你也可以在应用的 :file:`CMakeLists.txt` 文件中定义 ``SOC_ROOT`` 变量。请务必在使用 ``find_package(Zephyr ...)`` 引入 Zephyr 样板代码 **之前** 完成此操作。

.. note::

   在 CMakeLists.txt 中指定 ``SOC_ROOT`` 时，必须提供绝对路径，例如 ``list(APPEND SOC_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/<extra-soc-root>``。使用 ``-DSOC_ROOT=<soc-root>`` 时，绝对路径和相对路径均可使用。相对路径会相对于应用目录进行解析。

.. _dts_root:

Devicetree 定义
===============

Devicetree 目录树位于 ``APPLICATION_SOURCE_DIR``、``BOARD_DIR`` 和 ``ZEPHYR_BASE`` 中，但你也可以通过创建以下目录树来添加其他目录树（即 DTS_ROOT）::

    include/
    dts/common/
    dts/arm/
    dts/
    dts/bindings/

其中 “arm” 需替换为相应的架构。每个目录都是可选的。binding 目录存放 binding，而其他目录存放可从 DT 源文件包含的文件。

目录结构就绪后，你可以通过 ``DTS_ROOT`` CMake 缓存变量指定其位置来使用它：

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DDTS_ROOT=<path to dts root>
   :goals: build
   :compact:

你也可以在应用的 :file:`CMakeLists.txt` 文件中定义该变量。请务必在使用 ``find_package(Zephyr ...)`` 引入 Zephyr 样板代码 **之前** 完成此操作。

.. note::

   在 CMakeLists.txt 中指定 ``DTS_ROOT`` 时，必须提供绝对路径，例如 ``list(APPEND DTS_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/<extra-dts-root>``。使用 ``-DDTS_ROOT=<dts-root>`` 时，绝对路径和相对路径均可使用。相对路径会相对于应用目录进行解析。

Devicetree 源文件会经过 C 预处理器处理，因此你可以包含位于 ``DTS_ROOT`` 目录中的文件。按照约定，devicetree 包含文件的扩展名为 ``.dtsi``。

你还可以通过 ``DTS_EXTRA_CPPFLAGS`` CMake 缓存变量指定指令，从而使用预处理器控制 devicetree 文件的内容：

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DDTS_EXTRA_CPPFLAGS=-DTEST_ENABLE_FEATURE
   :goals: build
   :compact:

.. _CMake: https://www.cmake.org
.. _CMake introduction: https://cmake.org/cmake/help/latest/manual/cmake.1.html#description
.. _CMake list: https://cmake.org/cmake/help/latest/manual/cmake-language.7.html#lists
.. _example-application: https://github.com/zephyrproject-rtos/example-application
