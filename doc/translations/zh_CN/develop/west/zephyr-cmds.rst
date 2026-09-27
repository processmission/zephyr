.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-zephyr-ext-cmds:

其他 Zephyr 扩展命令
####################

本页介绍其他 :ref:`west-zephyr-extensions`。

.. _west-boards:

列出开发板：``west boards``
***************************

``boards`` 命令可列出 Zephyr 支持的开发板，无需查阅其他信息源。

输入以下命令即可运行::

  west boards

此命令按默认格式列出所有受支持的开发板。如果希望自行指定显示格式，可以使用 ``--format`` （或 ``-f``）选项::

  west boards -f "{arch}:{name}"

运行以下命令可获取格式选项的更多帮助::

  west boards -h

.. _west-completion:

Shell 补全脚本：``west completion``
***********************************

``completion`` 扩展命令输出 shell 补全脚本，可直接用来为支持的 shell 启用补全。

目前支持以下 shell：

- bash
- zsh
- fish
- powershell（仅支持开发板限定符）

更多说明可查看命令帮助::

  west help completion

.. _west-zephyr-export:

安装 CMake 包：``west zephyr-export``
*************************************

此命令将当前 Zephyr 安装注册为 CMake 用户包注册表中的 CMake 配置包。

在 Windows 上，CMake 用户包注册表位于 ``HKEY_CURRENT_USER\Software\Kitware\CMake\Packages``。

在 Linux 和 macOS 上，CMake 用户包注册表位于 :file:`~/.cmake/packages`。

设置 Zephyr 工作区时可以运行此命令。之后，位于工作区之外的应用程序 CMakeLists.txt 文件就能通过以下方式找到 Zephyr 仓库：

.. code-block:: cmake

   find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

详情参见 :zephyr_file:`share/zephyr-package/cmake`。

.. _west-spdx:

软件物料清单：``west spdx``
***************************

此命令为 Zephyr 构建生成一组 `SPDX`_ 文档，作为软件物料清单（SBOM）。它记录参与构建的源文件、这些文件产生的构建产物，以及它们之间的关系。源文件中的 ``SPDX-License-Identifier`` 注释会被扫描并填入文档，同时记录文件哈希及尽可能提取的版权声明。

.. _west-spdx-versions:

选择 SPDX 版本
--------------

``west spdx`` 可以输出两个主要 SPDX 规范系列中的任意一种。默认使用 SPDX 2.3；可通过 ``--spdx-version`` 选项选择其他版本。

SPDX 2.3 是 2.2 的超集，增加了 ``PrimaryPackagePurpose`` 等字段。需要兼容尚不支持 SPDX 3 的工具时，选择 SPDX 2.x；需要 :ref:`west-spdx-build-profile` 中介绍的更丰富、机器可读的构建来源信息时，选择 SPDX 3.0 或更高版本。

.. note::

   SPDX 3.1 支持属于实验性质，因为 SPDX 3.1 规范仍在制定中。

生成 SPDX 文档
--------------

#. 在项目中启用 :kconfig:option:`CONFIG_BUILD_OUTPUT_META`，让构建记录 ``west spdx`` 所需的信息。

#. 构建应用程序：

   .. code-block:: bash

      west build -d BUILD_DIR [...]

#. 使用此构建目录生成 SPDX 文档：

   .. code-block:: bash

      west spdx -d BUILD_DIR

   默认生成 SPDX 2.3 标签-值格式文档。若需生成 SPDX 2.2 或 3.0 文档，传入 ``--spdx-version``：

   .. code-block:: bash

      west spdx -d BUILD_DIR --spdx-version 3.0

.. note::

   使用 :ref:`sysbuild` 构建时，务必以需要生成 SBOM 的实际应用程序为目标。例如，应用名为 ``hello_world`` 时：

   .. code-block:: bash

     west build --sysbuild -d BUILD_DIR
     west spdx -d BUILD_DIR/hello_world

输出文档
--------

文档写入 :file:`BUILD_DIR/spdx/` （可通过 ``-s`` 覆盖）。无论 SPDX 版本如何，生成的物料清单（BOM）文档集合相同；只有文件扩展名不同：SPDX 2.x 标签-值格式使用 ``.spdx``，SPDX 3.0 JSON-LD 格式使用 ``.jsonld``：

- ``app``：构建所用应用程序源文件的 BOM
- ``zephyr``：构建实际使用的 Zephyr 源代码文件的 BOM
- ``build``：构建输出文件的 BOM
- ``modules-deps``：模块依赖项的 BOM。更多详情参见 :ref:`模块 <modules-vulnerability-monitoring>`。

对于 SPDX 3.0，每份文档都声明符合 Core、Software 和 Simple Licensing 配置规范，:file:`build.jsonld` 还声明符合用于记录产物生成方式的 :ref:`Build 配置规范 <west-spdx-build-profile>`。

物料清单中的每个文件都会被扫描，以记录其哈希值（SHA256、SHA1 和 MD5）；如果文件中存在 ``SPDX-License-Identifier`` 注释，也会记录检测到的许可证。

版权声明通过 REUSE 团体提供的第三方 :command:`reuse` 工具提取。找到的声明会以 ``FileCopyrightText`` 字段（SPDX 2.x）或版权属性（SPDX 3.0）形式加入 SPDX 文档。

.. note::
   版权提取采用启发式方法，可能无法捕获完整声明文本，因此 ``FileCopyrightText`` 内容仅尽力提供。这符合 SPDX 规范的建议。

关系
----

SPDX 关系用于表示 CMake 构建目标之间的依赖、相互链接的构建目标，以及经编译生成库文件的源文件之间的关系。

两个规范系列采用不同方式表示构建来源：

- 在 **SPDX 2.x** 中，每个生成产物都有文件级 ``GENERATED_FROM`` 关系，指向编译它所用的源文件（使用 ``--analyze-includes`` 时还包括头文件）。

- 在 **SPDX 3.0** 中，来源信息改由 :ref:`Build 配置规范 <west-spdx-build-profile>` 承载，使用作用域为 ``build`` 生命周期的 ``hasInput``/``hasOutput``/``usesTool`` 关系。

.. _west-spdx-build-profile:

Build 配置规范（SPDX 3.0）
--------------------------

生成 SPDX 3.0 文档时，``west spdx`` 会填充 `SPDX 3.0 Build profile`_，使 SBOM 不仅记录构建了 *什么*，也记录 *如何* 构建。这些信息自动从 CMake file-API 收集，并保存在 :file:`build.jsonld` 中。

此配置规范添加一个 ``build_Build`` 元素，描述整体构建：构建类型、CMake 生成器和构建配置，以及 ``BOARD``、``ARCH`` 等选定的环境变量。工具链（CMake、编译器、汇编器、链接器和归档器）记录为 ``Tool`` 元素，每个元素包含路径和版本。构建作用域的关系再将构建与其输入（源代码包和参与编译的文件）、输出（最终镜像）及所用工具关联起来。

每个中间目标（例如静态库）也有独立子构建，记录生成该产物的确切源文件、工具和编译选项，因此任意输出都可追溯其构建方式。

命令行选项
----------

``west spdx`` 接受以下附加选项：

- ``-i``、``--init``：在构建目录配置之前，创建 CMake 基于文件的 API 查询。此选项已弃用，将在 Zephyr 5.0 中移除：启用 :kconfig:option:`CONFIG_BUILD_OUTPUT_META` 的构建现在会自行请求该查询。

- ``-n PREFIX``：生成的 SPDX 文档中使用的文档命名空间前缀。详情见 `SPDX specification clause 6`_。如果省略 ``-n``，则使用随机 UUID，按第 2.5 节所述的默认格式生成默认命名空间。

- ``-s SPDX_DIR``：指定写入 SPDX 文档的替代目录，而不是 :file:`BUILD_DIR/spdx/`。

- ``--spdx-version {2.2,2.3,3.0,3.1}``：指定使用的 SPDX 规范版本，默认为 ``2.3``。各版本差异见 :ref:`west-spdx-versions`。

- ``--analyze-includes``：除在物料清单中记录参与编译的源代码文件（如 ``.c``、``.S``）外，还尝试确定每个 ``.c`` 文件具体包含了哪些头文件。

  此操作耗时更长，因为它会针对每个 ``.c`` 文件，使用实际构建时传给 C 编译器的同一组参数执行一次试运行。

- ``--include-sdk``：配合 ``--analyze-includes`` 使用时，还会创建第四份 SPDX 文档 :file:`sdk.spdx` （或 :file:`sdk.jsonld`），列出从 SDK 引入的头文件。

.. warning::

   目前不支持为 ``native_sim`` 平台生成 SBOM 文档。

.. _SPDX: https://spdx.dev/

.. _SPDX 3.0 Build profile:
   https://spdx.github.io/spdx-spec/v3.0.1/model/Build/Build/

.. _SPDX specification clause 6:
   https://spdx.github.io/spdx-spec/v2.2.2/document-creation-information/

.. _west-blobs:

操作二进制 blob：``west blobs``
*******************************

``blobs`` 命令可操作一个或多个 :ref:`模块 <modules>` 通过 :ref:`module.yml <module-yml>` 文件声明的 :ref:`二进制 blob <bin-blobs>`。

``blobs`` 命令包含三个子命令，分别用于列出、获取或清理（即删除）二进制 blob 文件。

可以在列出二进制 blob 时指定输出格式::

  west blobs list -f '{module}: {type} {path}'

运行 ``west blobs -h`` 可查看 ``-f/--format`` 中可用的全部变量。

获取 blob 的方式类似::

  west blobs fetch

请注意，如 :ref:`模块章节 <modules-bin-blobs>` 所述，获取的 blob 保存在相应模块仓库根目录下的 :file:`zephyr/blobs/` 文件夹中。

删除方式也类似::

  west blobs clean

此外，还可以将模块名称作为命令行参数传入，指定要列出、获取或清理哪些模块的 blob。

可以向 ``west blobs fetch`` 传入 ``--allow-regex`` 参数，通过正则表达式限制获取的具体 blob::

  # For example, only download esp32 blobs, skip the other variants
  west blobs fetch hal_espressif --allow-regex 'lib/esp32/.*'

可以通过 ``--auto-cache`` 命令行参数或 ``blobs.auto-cache`` 配置选项指定自动缓存目录。启用后，每当某个 blob 缺失并被下载时，自动缓存目录都会填入该文件。

可以通过 ``--cache-dirs`` 命令行参数或 ``blobs.cache-dirs`` 配置选项指定一个或多个附加缓存目录，以 ``;`` 分隔。

``west blobs fetch`` 会在全部已配置的缓存目录（包括自动缓存）中搜索匹配的 blob 文件名。缓存文件可以使用原始文件名，也可以带有 SHA-256 后缀（``<filename>.<sha>``）。如果找到，则将 blob 从缓存复制到目标 blob 路径；否则，从其 URL 下载到该路径。

.. _west-twister:

Twister 包装命令：``west twister``
**********************************
此命令是 :ref:`twister <twister_script>` 的包装。

随后可通过 west 调用 Twister::

  west twister -help
  west twister -T tests/ztest/base

.. _west-bindesc:

操作二进制描述符：``west bindesc``
**********************************

``bindesc`` 命令允许读取可执行文件的 :ref:`二进制描述符<binary_descriptors>`。目前支持将 ``.bin``、``.hex``、``.elf`` 和 ``.uf2`` 文件作为输入。

可以搜索镜像中的特定描述符，例如::

   west bindesc search KERNEL_VERSION_STRING build/zephyr/zephyr.bin

可以按类型和 ID 搜索自定义描述符，例如::

   west bindesc custom_search STR 0x200 build/zephyr/zephyr.bin

可以使用以下命令转储镜像中的全部描述符::

   west bindesc dump build/zephyr/zephyr.bin

可以使用以下命令将镜像的描述符数据区域提取到文件::

   west bindesc extract

可以使用以下命令列出所有已知的标准描述符名称::

   west bindesc list

可以使用以下命令打印描述符在镜像中的偏移::

   west bindesc get_offset

使用 GNU Global 索引源码：``west gtags``
****************************************

.. important:: 使用此命令前，必须安装 `GNU Global`_ 提供的 ``gtags`` 和 ``global`` 程序。

``west gtags`` 命令可为整个 west 工作区创建 GNU Global 标签文件::

  west gtags

.. _GNU Global: https://www.gnu.org/software/global/

这会在工作区 :ref:`顶层目录 <west-workspace>` 创建名为 ``GTAGS`` 的标签文件（还会在同一位置创建名为 ``GPATH`` 和 ``GRTAGS`` 的其他 Global 元数据文件）。

然后可以在工作区内部任意位置运行 ``global``，通过该标签文件搜索符号位置。

例如，从 ``zephyr/drivers`` 目录搜索 ``arch_system_halt()`` 函数的定义::

  $ cd zephyr/drivers
  $ global -x arch_system_halt
  arch_system_halt   65 ../arch/arc/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt  455 ../arch/arm64/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt  137 ../arch/nios2/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt   18 ../arch/posix/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt   17 ../arch/x86/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt  126 ../arch/xtensa/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt   21 ../kernel/fatal.c FUNC_NORETURN __weak void arch_system_halt(unsigned int reason)

对于符号的每个定义位置，输出会打印搜索符号、定义所在行号、定义文件的相对路径，以及该行内容。

其他提示：

- 这也可用于搜索厂商 HAL 函数的定义。

- 有关此工具的更多用法，参见 ``global`` 命令的手册页。

- 应运行 ``global``，**而不是** ``west global``。无需单独提供 ``west global`` 命令，因为 ``global`` 已经会从当前工作目录开始查找 ``GTAGS`` 文件。因此，必须从工作区内部运行 ``global``。

.. _west-patch:

操作补丁：``west patch``
************************

``patch`` 命令允许以受控方式向 Zephyr 或 Zephyr 模块应用补丁，让使用 :ref:`T2 星形拓扑 <west-t2>` 的外部应用更容易实现自动化和跟踪。:ref:`patches.yml <patches-yml>` 文件保存补丁文件的元数据，弥补 Zephyr 官方版本之间的空缺，让用户能方便地查看各项上游贡献的状态，并确定升级到下一 Zephyr 版本前应移除哪些补丁。

以下子命令可用于管理工作区中 Zephyr 或其他模块的补丁：

* ``apply``：应用 ``patches.yml`` 中列出的补丁
* ``reverse``：反向应用 ``patches.yml`` 中此前已应用的补丁
* ``clean``：移除所有已应用补丁，并重置到清单指定的检出状态
* ``list``：列出 ``patches.yml`` 中的全部补丁
* ``gh-fetch``：从 GitHub 拉取请求获取补丁

.. code-block:: none

    west-workspace/
    └── application/
       ...
       ├── west.yml
       └── zephyr
           ├── module.yml
           ├── patches
           │   ├── bootloader
           │   │   └── mcuboot
           │   │       └── my-tweak-for-mcuboot.patch
           │   └── zephyr
           │       └── my-zephyr-change.patch
           └── patches.yml

在此示例中，:ref:`west 清单 <west-manifests>` 文件 ``west.yml`` 固定到特定 Zephyr 修订版本（例如 ``v4.1.0``），并针对该版本以及应用使用的其他模块的具体版本应用补丁。不过，此应用需要两项改动才能满足需求：一项针对 Zephyr，另一项针对 MCUBoot。

.. _patches-yml:

.. code-block:: yaml

    patches:
      - path: zephyr/my-zephyr-change.patch
        sha256sum: c676cd376a4d19dc95ac4e44e179c253853d422b758688a583bb55c3c9137035
        module: zephyr
        author: Obi-Wan Kenobi
        email: obiwan@jedi.org
        date: 2025-05-04
        upstreamable: false
        comments: |
          An application-specific change we need for Zephyr.
      - path: bootloader/mcuboot/my-tweak-for-mcuboot.patch
        sha256sum: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        module: mcuboot
        author: Darth Sidious
        email: sidious@sith.org
        date: 2025-05-04
        merge-pr: https://github.com/zephyrproject-rtos/zephyr/pull/<pr-number>
        issue: https://github.com/zephyrproject-rtos/zephyr/issues/<issue-number>
        merge-status: true
        merge-commit: 1234567890abcdef1234567890abcdef12345678
        merge-date: 2025-05-06
        apply-command: git apply
        comments: |
          A change to mcuboot that has been merged already. We can remove this
          patch when we are ready to upgrade to the next Zephyr release.

补丁可以方便地自动应用。例如：

.. code-block:: bash

    west init -m <manifest repo> <workspace>
    cd <workspace>
    west update
    west patch apply

需要升级到更新的 Zephyr 版本时，可以修改 ``west.yml``，使其指向下一版本，例如 ``v4.2.0``。不再需要的补丁（如上例中的 ``my-tweak-for-mcuboot.patch``）可从 ``patches.yml`` 和外部应用仓库中移除，然后运行以下命令。

.. code-block:: bash

    west patch clean
    west update
    west patch apply --roll-back # roll-back all patches if one does not apply cleanly

也可以选择反向应用补丁，而不是清理所有模块。这样会保留模块中不冲突且无关的修改，只移除补丁产生的改动。在开发补丁并在应用中测试时，如果不希望清理所有补丁而丢失对模块所做的手动修改，这种方式很有用。

.. code-block:: bash

    west patch reverse

如果需要重做补丁，记得用新的 SHA256 校验和更新 ``patches.yml``。

.. code-block:: bash

    sha256sum zephyr/patches/zephyr/my-zephyr-change.patch
    7d57ca78d5214f422172cc47fed9d0faa6d97a0796c02485bff0bf29455765e9

也可以使用 ``west patch gh-fetch`` 从 GitHub 拉取请求获取补丁，并自动创建或更新 ``patches.yml`` 文件。当作者已有多项改动包含在现有上游拉取请求中时，这很有用。

.. code-block:: bash

    west patch gh-fetch --owner zephyrproject-rtos --repo zephyr --pull-request <pr-number> \
      --module zephyr --split-commits

上述命令会创建下列目录和文件结构，其中包含指定拉取请求中每个提交对应的补丁。

.. code-block:: none

    zephyr
    ├── patches
    │   ├── first-commit-from-pr.patch
    │   ├── second-commit-from-pr.patch
    │   └── third-commit-from-pr.patch
    └── patches.yml

操作 Zephyr SDK：``west sdk``
*****************************

``west sdk`` 是 Zephyr 专用的 west 命令，用于列出和安装 Zephyr SDK 及其工具链。

列出 SDK 和工具链
-----------------

要列出已安装的 Zephyr SDK，以及可用的 SDK 版本和工具链，运行：

.. code-block:: console

   west sdk list

此命令显示：

- 已安装的 SDK 版本
- 可用的 SDK 发行版本
- 各 SDK 包含的工具链

安装 Zephyr SDK
---------------

要安装 Zephyr SDK，运行：

.. code-block:: console

   west sdk install

此命令可能以交互模式运行，提示选择 SDK 或工具链。通过 ``--toolchains`` 指定具体工具链时，命令采用非交互模式，适合自动化使用。

若只安装指定工具链，使用 ``--toolchains`` 选项：

.. code-block:: console

   west sdk install --toolchains arm-zephyr-eabi riscv64-zephyr-elf

如果不确定需要哪些工具链，先运行 ``west sdk list`` 查看可用选项，避免下载不需要的工具链，从而节省数 GB 磁盘空间和下载时间。
