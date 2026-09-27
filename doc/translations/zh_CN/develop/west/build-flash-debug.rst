.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-build-flash-debug:

构建、烧录与调试
################

Zephyr 提供多条 :ref:`west 扩展命令 <west-extensions>`，用于构建、烧录，以及与开发板上运行的 Zephyr 程序交互：``build``、``flash``、``debug``、``debugserver``、``rtt`` 和 ``attach``。

关于如何为烧录和调试命令添加开发板支持，参见开发板移植指南中的 :ref:`flash-and-debug-support`。

.. Add a per-page contents at the top of the page. This page is nested
   deeply enough that it doesn't have any subheadings in the main nav.

.. only:: html

   .. contents::
      :local:

.. _west-building:

构建：``west build``
********************

.. tip:: 运行 ``west build -h`` 可快速了解用法。

``build`` 命令帮助你从源代码构建 Zephyr 应用程序。可以使用 :ref:`west config <west-config-cmd>` 配置其行为。

默认行为会尝试“按你的意图行事”：

- 如果当前工作目录中有名为 :file:`build` 的 Zephyr 构建目录，就在其中进行增量编译。从 Zephyr 构建目录内运行 ``west build`` 时也一样。

- 否则，如果从 Zephyr 应用程序源目录运行 ``west build``，且未找到构建目录，则创建新目录并在其中编译应用。

基础用法
========

使用 ``west build`` 最简单的方式，是进入应用程序根目录（即包含其 :file:`CMakeLists.txt` 的文件夹），然后运行::

  west build -b <BOARD>

其中 ``<BOARD>`` 为目标开发板名称，与直接调用 CMake 时在 ``cmake -DBOARD=<BOARD>`` 中使用的名称完全相同。

.. tip::

   可以使用 :ref:`west boards <west-boards>` 命令列出所有受支持的开发板。

命令会创建名为 :file:`build` 的构建目录；``west build`` 在其中运行 CMake 生成构建系统后，再编译应用。如果 ``west build`` 找到已有构建目录，则直接在其中增量编译，不重新运行 CMake。可通过 ``--cmake`` 强制再次运行 CMake。

如果已有构建目录，无需使用 ``--board`` 选项，``west build`` 可从 CMake 缓存确定开发板。对于新构建，依次检查 ``--board`` 选项、:envvar:`BOARD` 环境变量、``build.board`` 配置选项。

.. _west-multi-domain-builds:

Sysbuild（多域构建）
====================

:ref:`sysbuild` 可创建多域构建系统，将单个或多个开发板的多个镜像组合起来。

向 ``west build`` 传入 ``--sysbuild``，选择 :ref:`sysbuild` 构建基础设施来构建多个域。

sysbuild 的更详细用法见 :ref:`sysbuild` 指南。

.. tip::

   启用 ``build.sysbuild`` 配置选项，可让 ``west build`` 默认使用 sysbuild。对于某次构建，可使用 ``--no-sysbuild`` 禁用。

``west build`` 会通过 sysbuild 指定各域的顶层构建目录构建所有域。

可使用 ``--domain`` 参数，仅构建多域项目中的一个域。

示例
====

以下按主题列出 ``west build`` 用法示例。

强制重新运行 CMake
------------------

要强制重新运行 CMake，使用 ``--cmake`` （或 ``-c``）选项::

  west build -c

设置默认开发板
--------------

将 ``west build`` 配置为默认针对 ``reel_board`` 构建::

  west config build.board reel_board

（这里也可以使用 Zephyr 支持的其他开发板，不必是 ``reel_board``。）

.. _west-building-dirs:

设置源目录和构建目录
--------------------

要显式设置应用程序源目录，将路径作为位置参数传入::

  west build -b <BOARD> path/to/source/directory

要显式设置构建目录，使用 ``--build-dir`` （或 ``-d``）::

  west build -b <BOARD> --build-dir path/to/build/directory

要将默认构建目录从 :file:`build` 改为其他名称，使用 ``build.dir-fmt`` 配置选项。它允许通过格式字符串命名构建目录，例如::

  west config build.dir-fmt "build/{board}/{app}"

采用上述设置后，运行 ``west build -b reel_board samples/hello_world`` 会使用构建目录 :file:`build/reel_board/hello_world`。此选项的更多详情见 :ref:`west-building-config`。

设置构建系统目标
----------------

要指定运行的构建系统目标，使用 ``--target`` （或 ``-t``）。

例如，在装有 QEMU 的主机平台上，可以使用 ``run`` 目标，用一条命令为仿真的 :zephyr:board:`qemu_x86 <qemu_x86>` 开发板构建并运行 :zephyr:code-sample:`hello_world` 示例::

  west build -b qemu_x86 -t run samples/hello_world

另一个示例，使用 ``-t`` 列出所有构建系统目标::

  west build -t help

最后，使用 ``-t`` 运行 ``pristine`` 目标，删除构建目录中的全部文件::

  west build -t pristine

.. _west-building-pristine:

全新构建
--------

*全新（pristine）* 构建目录实质上等同于新建目录，之前构建产生的所有文件都已移除。

要强制 ``west build`` 在重新运行 CMake 生成构建系统前清空构建目录，使用 ``--pristine=always`` （或 ``-p=always``）选项。

不带值的 ``--pristine`` 或 ``-p``，效果与指定 ``always`` 相同。例如，以下命令等效::

  west build -p -b reel_board samples/hello_world
  west build -p=always -b reel_board samples/hello_world

默认情况下，``west build`` 不尝试检测构建目录是否需要清空。因此，尝试将构建目录复用于不同的 ``--board`` 等操作可能产生错误。

使用 ``--pristine=auto``，可让 ``west build`` 检测其中一些情况，并在尝试构建前清空构建目录。

.. tip::

   运行 ``west config build.pristine always`` 可始终执行全新构建，运行 ``west config build.pristine never`` 可禁用自动判断。详情见 ``west build`` 的 :ref:`west-building-config`。

.. _west-building-verbose:

详细构建输出
------------

要打印 ``west build`` 执行的 CMake 和编译器命令，使用 west 全局详细输出选项 ``-v``::

  west -v build -b reel_board samples/hello_world

.. _west-building-generator:
.. _west-building-cmake-args:

一次性 CMake 参数
-----------------

要向 ``west build`` 调用的 CMake 传入附加参数，将其放在命令行末尾的 ``--`` 之后。

.. important::

   以这种方式传入附加 CMake 参数，会强制 ``west build`` 重新执行 CMake 构建配置步骤，即使构建系统已经生成。这会减慢增量构建，但仍远快于从头构建。

   使用一次 ``--`` 生成构建目录后，后续运行使用 ``west build -d <build-dir>`` 进行增量构建。

   也可以按下一节所述永久保存 CMake 参数，这不会减慢增量构建。

例如，要使用 Unix Makefiles CMake 生成器，而不是 ``west build`` 默认使用的 Ninja，运行::

  west build -b reel_board -- -G'Unix Makefiles'

使用 Unix Makefiles，并将 `CMAKE_VERBOSE_MAKEFILE`_ 设为 ``ON``::

  west build -b reel_board -- -G'Unix Makefiles' -DCMAKE_VERBOSE_MAKEFILE=ON

请注意，即使传入多个 CMake 参数，``--`` 也只出现一次。``west build`` 中 ``--`` 之后的所有命令行参数都会传给 CMake。

.. _west-building-dtc-overlay-file:

将 :ref:`DTC_OVERLAY_FILE <important-build-vars>` 设为 :file:`enable-modem.overlay`，将该文件用作 :ref:`设备树覆盖文件 <dt-guide>`::

  west build -b reel_board -- -DDTC_OVERLAY_FILE=enable-modem.overlay

将 :file:`file.conf` Kconfig 片段合并到构建的 :file:`.config` 中::

  west build -- -DEXTRA_CONF_FILE=file.conf

.. _west-building-cmake-config:

永久 CMake 参数
---------------

上一节介绍了如何为单次 ``west build`` 命令添加 CMake 参数。如果希望保存参数，让 ``west build`` 每次生成新构建系统时都使用它们，应设置 ``build.cmake-args`` 配置选项。每当 ``west build`` 运行 CMake 生成构建系统，都会按 shell 规则拆分此选项的值，再将结果加入 ``cmake`` 命令行。

请记住，默认情况下，如果构建目录中已有构建系统，``west build`` **会尽量避免重新生成**。因此，设置 ``build.cmake-args`` 后，需要删除已有构建目录，或执行 :ref:`全新构建 <west-building-pristine>`，确保设置生效。

例如，要始终启用 :makevar:`CMAKE_EXPORT_COMPILE_COMMANDS`，可以运行::

  west config build.cmake-args -- -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

（额外的 ``--`` 强制将后续命令内容作为位置参数处理。否则，:ref:`west config <west-config-cmd>` 会将 ``-DVAR=VAL`` 语法解释为使用其 ``-D`` 选项。）

启用 :makevar:`CMAKE_VERBOSE_MAKEFILE`，使 CMake 始终生成详细输出的构建系统::

  west config build.cmake-args -- -DCMAKE_VERBOSE_MAKEFILE=ON

要在 ``build.cmake-args`` 中保存多个参数，使用可拆分为不同参数的单个字符串（``west build`` 内部使用 Python 函数 `shlex.split()`_ 拆分该值）。

.. _shlex.split(): https://docs.python.org/3/library/shlex.html#shlex.split

例如，同时启用 :makevar:`CMAKE_EXPORT_COMPILE_COMMANDS` 和 :makevar:`CMAKE_VERBOSE_MAKEFILE`::

  west config build.cmake-args -- "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_VERBOSE_MAKEFILE=ON"

如果希望将 CMake 参数保存在单独文件中，可以将 CMake 的 ``-C <initial-cache>`` 选项与 ``build.cmake-args`` 结合。例如，另一种设置上一示例选项的方式，是创建名为 :file:`~/my-cache.cmake` 的文件，内容如下：

.. code-block:: cmake

   set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE BOOL "")
   set(CMAKE_VERBOSE_MAKEFILE ON CACHE BOOL "")

然后运行::

  west config build.cmake-args "-C ~/my-cache.cmake"

更多详情见 `cmake(1) manual page`_ 和 `set() command`_ 文档。

.. _cmake(1) manual page:
   https://cmake.org/cmake/help/latest/manual/cmake.1.html

.. _set() command:
   https://cmake.org/cmake/help/latest/command/set.html

构建工具参数
------------

使用 ``-o`` 向底层构建工具传递选项。

这同时适用于基于 ``ninja`` （:ref:`默认值 <west-building-generator>`）和 ``make`` 的构建系统。

例如，向 ``ninja`` 传递 ``-dexplain``::

  west build -o=-dexplain

再如，向 ``make`` 传递 ``--keep-going``::

  west build -o=--keep-going

请注意，必须使用 ``-o=--foo``，而非 ``-o --foo``，以防 ``--foo`` 被视为 ``west build`` 选项。

构建并行度
----------

默认情况下，``ninja`` 使用全部核心构建，而 ``make`` 只用一个核心。可通过两者都支持的 ``-j`` 选项显式控制。

例如，使用 4 个核心构建::

  west build -o=-j4

``-o`` 选项已在上一节详细介绍。

构建单个域
----------

在包含 :zephyr:code-sample:`hello_world` 和 `MCUboot`_ 的多域构建中，可使用 ``--domain hello_world`` 仅构建该域::

  west build --sysbuild --domain hello_world

``--domain`` 可与 ``--target`` 参数结合，为选定域构建指定目标，例如::

  west build --sysbuild --domain hello_world --target help

使用 snippet
------------

参见 :ref:`using-snippets`。

.. _west-building-config:

配置选项
========

可以使用以下选项 :ref:`配置 <west-config-cmd>` ``west build``。

.. NOTE: docs authors: keep this table sorted alphabetically

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - 选项
     - 描述
   * - ``build.board``
     - 字符串。如果已设置，且未指定 ``--board``，环境中也未设置 ``BOARD``，:ref:`west build <west-building>` 就使用此开发板。
   * - ``build.board_warn``
     - 布尔值，默认为 ``true``。如果为 ``false``，则在 ``west build`` 无法确定目标开发板时不发出警告。
   * - ``build.cmake-args``
     - 字符串。如果存在，每次生成新构建系统时，都会按 shell 规则拆分其值并传给 CMake。参见 :ref:`west-building-cmake-config`。
   * - ``build.dir-fmt``
     - 字符串，默认为 ``build``。构建目录格式字符串，west 创建或定位构建目录时使用。当前可用参数如下：

         - ``west_topdir``：west 工作区的绝对路径，由 ``west_topdir`` 命令返回
         - ``board``：开发板名称
         - ``source_dir``：相对于当前工作目录的 CMake 源目录路径。如果当前工作目录位于源目录内，则为空字符串。未指定源目录时，默认使用当前工作目录。例如，在 ``<west_topdir>/app1`` 中运行 ``west build ../app``，``source_dir`` 解析为 ``../app`` （相对于当前工作目录的路径）。
         - ``source_dir_workspace``：相对于 ``west_topdir`` 的源目录路径（如果源目录位于工作区内）；否则相对于文件系统根目录（Unix 上为 ``/``，Windows 上为 ``C:/``）。例如，在 ``<west_topdir>/app1`` 中运行 ``west build ../app``，``source_dir`` 解析为 ``app`` （相对于 west 工作区目录的路径）。
         - ``app``：源目录名称。
   * - ``build.generator``
     - 字符串，默认为 ``Ninja``。用于创建构建系统的 `CMake Generator`_。（为单次构建设置生成器，参见 :ref:`上面的示例 <west-building-generator>`。）
   * - ``build.guess-dir``
     - 字符串，指定在使用 ``build.dir-fmt`` 且信息不足以解析构建目录名称时，west 是否尝试猜测要使用的目录。可取以下值：

         - ``never`` （默认值）：从不猜测，直接退出并要求用户通过 ``-d`` 指定构建目录。
         - ``runners``：使用任意 runner 命令时尝试猜测目录。通常包括所有调用外部工具的命令，例如 ``flash`` 和 ``debug``。
   * - ``build.pristine``
     - 字符串，控制 ``west build`` 在构建前清理构建目录的方式。可取以下值：

         - ``never`` （默认值）：从不自动清空构建目录。
         - ``auto``：如果已有构建系统，且不清理就会导致构建失败（例如用户指定的开发板或应用与最初创建构建目录时不同），``west build`` 会在构建前自动清空目录。
         - ``always``：如果已有构建系统，始终在构建前清空目录。
   * - ``build.sysbuild``
     - 布尔值，默认为 ``false``。如果为 ``true``，使用 sysbuild 基础设施构建应用。

.. _west-flashing:

烧录：``west flash``
********************

.. tip:: 运行 ``west flash -h`` 获取更多帮助。

Basics
======

在 Zephyr 构建目录中，重新构建二进制文件并烧录到开发板::

  west flash

要指定构建目录，使用 ``--build-dir`` （或 ``-d``）::

  west flash --build-dir path/to/build/directory

未指定构建目录时，``west flash`` 先在 :file:`build` 中查找，再查找当前工作目录。如果设置了 ``build.dir-fmt`` 配置选项（见 :ref:`west-building-dirs`），``west flash`` 则改为搜索该位置，而不是 :file:`build`。

选择运行器
==========

如果开发板的 Zephyr 集成支持多个烧录程序，可以通过 ``--runner`` （或 ``-r``）指定使用哪一个。例如，West 默认用 ``nrfjprog`` 烧录开发板，但也支持 JLink 时，可以按如下方式覆盖默认值::

  west flash --runner jlink

构建时可通过 CMake 变量 ``BOARD_FLASH_RUNNER`` 覆盖默认烧录运行器，通过 ``BOARD_DEBUG_RUNNER`` 覆盖调试运行器。

例如::

  # Set the default runner to "jlink", overriding the board's
  # usual default.
  west build [...] -- -DBOARD_FLASH_RUNNER=jlink

设置 CMake 参数的更多信息，见 :ref:`west-building-cmake-args` 和 :ref:`west-building-cmake-config`。

West 使用的 ``runner`` 库详见下文 :ref:`west-runner`。运行 ``west flash -H`` 可列出支持烧录的运行器；如果从构建目录运行，或指定 ``--build-dir``，还会打印该开发板可用运行器的更多信息。

覆盖配置
========

CMake 缓存包含 West 烧录时使用的默认值，例如开发板目录在文件系统中的位置、各种格式的待烧录 zephyr 二进制文件路径等。运行时可通过附加选项覆盖其中任意配置。

例如，要覆盖包含待烧录 Zephyr 镜像的 HEX 文件（假设运行器要求 HEX 文件），同时保持其他烧录配置的默认值::

  west flash --hex-file path/to/some/other.hex

``west flash -h`` 输出列出所有运行器支持的完整覆盖选项。

运行器专用覆盖选项
==================

各运行器可能支持其他烧录选项。例如，一些运行器支持 ``--erase``，在烧录 Zephyr 镜像前对开发板闪存执行整片擦除。

要查看开发板所支持运行器的全部可用选项及用法信息，使用 ``--context`` （或 ``-H``）::

  west flash --context

.. important::

   请注意，短选项中的 H 是大写。此操作会重新构建，以确保显示的信息最新！

在构建目录之外运行 West 时，``west flash -H`` 只打印运行器列表。可使用 ``west flash -H -r <runner-name>`` 查看该运行器支持选项的用法信息。

例如，打印 ``jlink`` 运行器的用法信息::

  west flash -H -r jlink

.. _west-multi-domain-flashing:

多域烧录
========

检测到 :ref:`west-multi-domain-builds` 目录时，``west flash`` 会按 sysbuild 定义的顺序烧录所有域。

可以使用 ``--domain``，仅烧录多域项目中某个域的镜像。

例如，在包含 :zephyr:code-sample:`hello_world` 和 `MCUboot`_ 的多域构建中，可以使用 ``--domain hello_world`` 只烧录该域的镜像::

  west flash --domain hello_world

.. _west-debugging:

Configuration Options
=====================

可以使用以下选项 :ref:`配置 <west-config-cmd>` ``west flash``。

.. NOTE: docs authors: keep this table sorted alphabetically

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - 选项
     - 描述
   * - ``flash.rebuild``
     - 布尔值，默认为 ``true``。如果为 ``false``，运行 west flash 时不重新构建。

调试：``west debug``、``west debugserver``
******************************************

.. tip::

   运行 ``west debug -h`` 或 ``west debugserver -h`` 获取更多帮助。

Basics
======

在 Zephyr 构建目录中，将调试器连接到开发板并打开调试控制台（例如 GDB 会话）::

  west debug

将调试器连接到开发板，并开放一个可供调试器（例如 IDE 调试器）连接的本地网络端口::

  west debugserver

要指定构建目录，使用 ``--build-dir`` （或 ``-d``）::

  west debug --build-dir path/to/build/directory
  west debugserver --build-dir path/to/build/directory

未指定构建目录时，这些命令先在 :file:`build` 中查找，再查找当前工作目录。如果设置了 ``build.dir-fmt`` 配置选项（见 :ref:`west-building-dirs`），``west debug`` 则搜索该位置，而不是 :file:`build`。

Choosing a Runner
=================

如果开发板的 Zephyr 集成支持多个调试程序，可以通过 ``--runner`` （或 ``-r``）指定使用哪一个。例如，West 默认使用 ``pyocd-gdbserver`` 调试开发板，但也支持 JLink 时，可以按如下方式覆盖默认值::

  west debug --runner jlink
  west debugserver --runner jlink

West 使用的 ``runner`` 库详见下文 :ref:`west-runner`。运行 ``west debug -H`` 可列出支持调试的运行器；如果从构建目录运行，或指定 ``--build-dir``，还会打印该开发板可用运行器的更多信息。

Configuration Overrides
=======================

CMake 缓存包含 West 调试时使用的默认值，例如开发板目录在文件系统中的位置、包含符号表的 zephyr 二进制文件路径等。运行时可以通过附加选项覆盖其中任意配置。

例如，覆盖包含 Zephyr 二进制和符号表的 ELF 文件（假设运行器要求 ELF 文件），同时保持其他调试配置的默认值::

  west debug --elf-file path/to/some/other.elf
  west debugserver --elf-file path/to/some/other.elf

``west debug -h`` 输出列出所有运行器支持的完整覆盖选项。

Runner-Specific Overrides
=========================

各运行器可能支持其他调试选项。例如，一些运行器支持设置调试服务器所用网络端口的选项。

要查看开发板所支持运行器的全部可用选项及用法信息，使用 ``--context`` （或 ``-H``）::

  west debug --context

（``west debugserver --context`` 命令会打印相同输出。）

.. important::

   请注意，短选项中的 H 是大写。此操作会重新构建，以确保显示的信息最新！

在构建目录之外运行 West 时，``west debug -H`` 只打印运行器列表。可使用 ``west debug -H -r <runner-name>`` 查看该运行器支持选项的用法信息。

例如，打印 ``jlink`` 运行器的用法信息::

  west debug -H -r jlink

.. _west-multi-domain-debugging:

多域调试
========

``west debug`` 一次只能调试一个域。检测到 :ref:`west-multi-domain-builds` 目录时，``west debug`` 会调试 sysbuild 指定的 ``default`` 域。

默认域为源目录指定的应用程序。见以下示例::

  west build --sysbuild path/to/source/directory

例如，使用 sysbuild 将 ``hello_world`` 与 `MCUboot`_ 一起构建时，``hello_world`` 成为默认域::

  west build --sysbuild samples/hello_world

因此，要调试 ``hello_world``，可以运行::

  west debug

或者::

  west debug --domain hello_world

如果希望调试 MCUboot，必须显式将 MCUboot 指定为待调试域::

  west debug --domain mcuboot

.. _west-runner:

Configuration Options
=====================

可以使用以下选项 :ref:`配置 <west-config-cmd>` ``west debug``，以及 :ref:`配置 <west-config-cmd>` ``west debugserver``。

.. NOTE: docs authors: keep this table sorted alphabetically

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - 选项
     - 描述
   * - ``debug.rebuild``
     - 布尔值，默认为 ``true``。如果为 ``false``，运行 west debug 时不重新构建。
   * - ``debugserver.rebuild``
     - 布尔值，默认为 ``true``。如果为 ``false``，运行 west debugserver 时不重新构建。

烧录和调试运行器
****************

烧录和调试命令使用 Python 包装各种 :ref:`flash-debug-host-tools`。这些包装均定义在 :zephyr_file:`scripts/west_commands/runners` 的 Python 库中，每个包装称为一个 *运行器*。运行器可以烧录和/或调试 Zephyr 程序。

该库的核心抽象是 ``ZephyrBinaryRunner``，一个表示运行器的抽象类。可用运行器集合由已导入的 ``ZephyrBinaryRunner`` 子类决定。``ZephyrBinaryRunner`` 位于 ``runners.core`` 模块；具体运行器实现则位于 ``runners.nrfjprog``、``runners.openocd`` 等其他子模块中。

运行 Robot Framework 测试：``west robot``
*****************************************

.. tip:: 运行 ``west robot -h`` 获取更多帮助。

Basics
======

目前此命令只支持一个使用 ``renode-test`` 的运行器（实质上是用于在 Renode 中运行 Robot 测试的包装），但可通过添加其他运行器轻松扩展。

在 Zephyr 构建目录中运行 Robot 测试套件::

  west robot --runner=renode-robot --testsuite path/to/testsuite.robot

这会运行 testsuite.robot 中的全部测试，并打印 Robot Framework 提供的输出。

使用 ``--renode-robot-args`` 选项向 Renode 传递附加参数。例如，除 Robot Framework 输出外，还显示 Renode 日志：

  west robot --runner=renode-robot --testsuite path/to/testsuite.robot --renode-robot-arg="--show-log"

Runner-Specific Overrides
=========================

要查看开发板支持的 Robot 运行器的全部可用选项及用法信息，使用 ``--context`` （或 ``-H``）::

  west robot --runner=renode-robot --context


要查看“renode-test”运行器支持的全部选项，使用::

  west robot --runner=renode-robot --renode-robot-help

仿真开发板：``west simulate``
*****************************

Basics
======

目前此命令只支持一个使用 Renode 的运行器，但可通过添加其他运行器轻松扩展。

在 Zephyr 构建目录中运行构建好的二进制文件::

  west simulate --runner=renode

这会启动 Renode，根据当前平台的默认 ``.resc`` 脚本配置仿真，并默认加载 zephyr.elf。随后可在 Renode Monitor 中输入“start”或“s”启动仿真。也可以使用运行器提供的参数向 Renode 传入命令：

  west simulate --runner=renode --renode-command start

向 Renode 本身传入参数，例如以控制台模式而不是独立窗口启动：

  west simulate --runner=renode --renode-arg="--console"

此后，Renode 在控制台和窗口模式下均可正常使用。详细用法见 `Renode - documentation`_。

.. _Renode - documentation:
   https://docs.renode.io

Runner-Specific Overrides
=========================

要查看运行器支持的全部可用选项及用法信息，使用 ``--context`` （或 ``-H``）::

  west simulate --runner=renode --context

要查看 Renode 支持的全部选项，使用::

  west simulate --runner=renode --renode-help

树外运行器
**********

:ref:`Zephyr 模块 <modules>` 可以通过在 :ref:`module.yml <modules-runners>` 中添加 Python 文件来发现外部运行器。创建外部运行器类时，继承 ``ZephyrBinaryRunner`` 并实现所有抽象方法。

.. note::

   支持自定义树外运行器意味着 ``runners.core`` 模块属于公共 API，不向后兼容的变更需要经过 :ref:`弃用流程 <breaking_api_changes>`。

开发与扩展
**********

本节介绍烧录和调试命令使用的 ``runners.core`` 模块，它是实现这些功能的核心抽象。

开发者可以通过实现新运行器，支持新的 Zephyr 程序烧录和调试方式。要将支持合入 Zephyr 上游，应将运行器加入新的或现有的 ``runners`` 模块，并从 :file:`runners/__init__.py` 导入。

.. note::

   :zephyr_file:`scripts/west_commands/tests` 中的测试用例为 runners 包和各运行器类提供单元测试覆盖。

   添加新运行器时，请尽量添加测试。请注意，如果改动破坏已有测试用例，上游拉取请求的 CI 测试会失败。

.. automodule:: runners.core
   :members:

手动操作
********

如果不希望使用 West 烧录或调试开发板，只需在构建目录中查找构建系统输出的二进制文件。根据开发板与构建系统的集成方式，它们的名称类似于 ``zephyr/zephyr.elf``、``zephyr/zephyr.hex`` 等。可以使用自己选择的其他工具将这些文件烧录到开发板，也可以按需用于调试，例如提供符号表。

默认情况下，这些 West 命令在烧录和调试前会重新构建二进制文件。当然，也可以使用 Zephyr 构建系统提供的常规目标完成此操作，事实上这些命令内部就是这样实现的。

.. _cmake(1):
   https://cmake.org/cmake/help/latest/manual/cmake.1.html

.. _CMAKE_VERBOSE_MAKEFILE:
   https://cmake.org/cmake/help/latest/variable/CMAKE_VERBOSE_MAKEFILE.html

.. _CMake Generator:
   https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html

.. _MCUboot: https://mcuboot.com/
