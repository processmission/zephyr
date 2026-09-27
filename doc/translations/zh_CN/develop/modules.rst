.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _modules:

模块（外部项目）
################

Zephyr 使用多个由外部维护的项目的源代码，以避免重复造轮子，并在合适的地方尽可能复用经过实践检验的成熟代码。在 Zephyr 构建系统中，这些项目称为 *模块*。模块必须集成到 Zephyr 构建系统中，本页其他章节会详细说明。

外部项目要成为默认模块列表的候选项，必须在 Zephyr 项目之外拥有独立的生命周期：有自己的仓库、贡献和维护流程，以及发布流程。Zephyr 模块不应包含专为 Zephyr 编写的代码；这类代码应提交到 Zephyr 主仓库。

要纳入 Zephyr 项目默认清单，模块提供的功能或特性必须获得项目技术指导委员会的认可和批准，并符合 :ref:`模块许可要求 <modules_licensing>` 和 :ref:`贡献指南 <modules_contributing>`。还应有一名 Zephyr 开发者承诺维护该模块的代码库。

Zephyr 依赖的模块类别包括但不限于：

- 调试器集成
- 芯片厂商硬件抽象层（HAL）
- 密码学库
- 文件系统
- 进程间通信（IPC）库

此外，在某些情况下，模块（尤其是厂商 HAL）可能包含对可选 :ref:`二进制文件 <bin-blobs>` 的引用。

本页汇总了用于更好地组织 Zephyr 模块工作流程的政策和实践建议。

.. _modules-vs-projects:

模块与 west 项目
****************

本页介绍的 Zephyr 模块与 :ref:`west 项目 <west-workspace>` 并不相同。事实上，模块完全 :ref:`不要求使用 west <modules_without_west>`。不过，:ref:`配合 west 使用模块 <modules_using_west>` 时，构建系统会通过 west 查找模块。

具体而言：

模块是包含 :file:`zephyr/module.yml` 文件的仓库，Zephyr 构建系统可据此将仓库中的源代码纳入构建。:ref:`West 项目 <west-manifests-projects>` 则是 :file:`west.yml` 清单文件中 ``projects:`` 部分的条目。west 项目通常也是模块，但并非总是如此。某些 west 项目不会包含在最终固件映像中，例如工具，因此无需作为模块。Zephyr 构建系统通过 :ref:`west 本身 <modules_using_west>` 或 :ref:`ZEPHYR_MODULES CMake 变量 <modules_without_west>` 查找模块。

本页内容仅适用于模块，不适用于一般意义上的 west 项目，除非该项目本身也是模块。

模块仓库
********

* 默认清单中的所有模块都应托管在 zephyrproject-rtos GitHub 组织下的仓库中。

* 模块仓库必须在仓库根目录的 :file:`zephyr/` 文件夹中包含一个 *module.yml* 文件。

* 模块仓库名称应使用小写字母和连字符，而非下划线。此规则适用于所有新模块仓库，但直接跟踪外部 Git 项目的仓库除外：这类模块可以沿用对应外部项目的名称。

  .. note::

     不符合上述命名约定的现有模块仓库无需重命名。

* 应在 :file:`zephyr/module.yml` 文件中显式设置模块仓库名称。

* 模块仓库主分支的默认名称应为“zephyr”。特定用途的分支，例如面向 Zephyr LTS 版本的模块分支，其名称必须以 'zephyr\_' 为前缀。

* 如果模块有对应的外部（上游）项目仓库，应保留上游仓库的目录结构。

  .. note::

     模块仓库无需维护一个镜像外部仓库 master 分支的“master”分支。也不建议这样做，因为这可能使人混淆模块的主分支；主分支应为“zephyr”。

* 模块对外提供的所有头文件，其包含路径应以模块名称开头。例如，mcuboot 应将 ``bootutil/bootutil.h`` 以“mcuboot/bootutil/bootutil.h”的路径提供。

.. _modules_synchronization:

与上游同步
==========

模块仓库应优先同步到对应外部项目的最新稳定版本。不过，为获取重要更新，也允许将 Zephyr 模块仓库更新到上游最新开发分支的顶端提交。与上游同步时，必须记录选择该次更新的理由。

允许采用的做法须满足的要求
--------------------------

对模块仓库主分支的修改，包括与上游代码库同步，只能通过拉取请求进行。拉取请求必须能由 Zephyr CI *验证*，且能够 *合并*，例如通过 GitHub 界面的 *Rebase and merge* 或 *Create a merge commit* 操作。这样可确保传入的修改始终 **可供审查**，并使 *下游* 模块仓库的历史保持增量增长，即始终保留已有提交、标签等。该政策还允许直接针对待引入模块仓库的变更运行 Zephyr CI、Git 格式、身份和许可证检查。

.. note::

     不允许强制推送到模块的主分支。

允许采用的做法
--------------

以下做法符合上述要求，所有模块仓库都应遵循。模块代码负责人可以选择适合的同步方式，但必须在相应模块仓库中始终一致地采用该方式。

**通过上游差异更新模块：** 将上游变更作为单个 *快照* 提交（手动生成差异），向模块主分支提交拉取请求，再使用 *Rebase & merge* 合并。此方法简单，适用于所有模块，但缺点是模块仓库中不保留上游历史。

  .. note::

     如果外部项目没有托管在上游 Git 仓库中，则只能采用上述方式。

提交说明应标明上游项目 URL、模块更新到的版本（如上游版本、标签、适用时的提交 SHA 等），以及此次更新的原因。

**通过合并上游分支更新模块：** 对目标上游分支（例如主分支或最新发布分支）执行 Git 合并，将结果作为针对模块主分支的拉取请求提交，再使用 *Create a merge commit* 合并。此方式适用于具有上游 Git 仓库的模块。主要优点是模块仓库保留上游历史，即原始提交 SHA；缺点是下游主分支会额外产生两个合并提交。


为 Zephyr 模块贡献代码
**********************

.. _modules_contributing:


个人角色与职责
==============

为便于管理 Zephyr 模块仓库，定义以下个人角色。

**管理员：** 每个 Zephyr 模块都必须有一名管理员，负责管理仓库访问权限，例如根据模块负责人的请求，将相关人员添加为仓库协作者。模块管理员属于 Administrators 团队，该团队由具有模块 GitHub 仓库管理员权限的项目成员组成。

**模块负责人：** 每个模块都必须有一名代码负责人，对 Zephyr 模块仓库的内容承担总体责任。具体而言，模块负责人需要：

* 协调模块仓库中的代码审查
* 担任针对仓库主分支的拉取请求的默认受理人
* 按需请求为仓库添加其他协作者
* 按照 :ref:`modules_synchronization` 中的政策，定期将模块仓库与对应上游同步
* 关注外部项目的安全漏洞，并在上游提供修复后尽快将修复纳入模块仓库
* 在 Zephyr 发布说明中列出模块代码库中已知的安全漏洞。


  .. note::

     模块负责人不必是 Zephyr :ref:`维护者 <project_roles>`。

**合并者：** Zephyr 发布工程团队有权也有责任，将已批准的拉取请求合并到模块仓库主分支。


维护模块代码库
==============

Zephyr 主仓库的更新，例如公共 API 的变更，可能要求修改模块代码库。保持模块代码库同步更新的责任，由这些 Zephyr 变更的 **贡献者** 与模块 **负责人** 共同承担。具体而言：

* Zephyr 原始变更的贡献者必须向模块仓库提交相应的必要修改，确保包含原始变更的拉取请求通过 Zephyr CI，且模块集成测试成功。

* 模块负责人对模块代码库与 Zephyr 主仓库的同步和测试承担总体责任。除了 Zephyr CI 执行的测试，还应不定期进行深入测试。对于 Zephyr 拉取请求 CI 未发现的模块问题，模块负责人必须予以修复。


.. _modules_changes:

向模块贡献变更
==============

直接向模块代码库提交并合并变更，即在变更进入对应外部项目仓库之前就合并，应仅限于以下情况：

* Zephyr 主仓库更新所要求的变更
* 不宜等待外部项目先行合并的紧急变更，例如安全漏洞修复。

如果模块具有上游项目仓库，应避免直接对模块代码库进行重大修改，包括设计或功能变更。这类变更应直接提交到上游项目。

:ref:`向模块提交变更 <submitting_new_modules>` 详细介绍了向模块仓库贡献变更的流程。

贡献指南
--------

为 Zephyr 模块贡献代码必须遵循项目通用的 :ref:`贡献指南 <contribute_guidelines>`。

**拉取请求：** 至少获得两人批准后才能合并，其中必须包括 PR 受理人的批准。此外，模块仓库中的拉取请求只有在引入的变更经过 Zephyr CI 工具验证后才能合并，详见本页其他章节。

模块仓库主分支的拉取请求合并，必须与 Zephyr 主仓库中对应清单文件的更新配套进行。

**问题报告：** 为集中管理问题报告，模块仓库特意禁用了 `GitHub issues`_。模块中的缺陷或改进建议等问题应在 Zephyr 主仓库中提出，并在适用时使用对应模块的 GitHub 标签进行标记。

  .. note::

     允许为 Zephyr 模块提交缺陷报告，以便在 Zephyr 中跟踪相应上游项目的问题。这些报告不应影响 :ref:`发布质量标准 <release_quality_criteria>`。


.. _modules_licensing:

许可要求与政策
**************

模块代码库中的所有源文件都必须包含许可证头，除非仓库具有涵盖无许可证头文件的 **主许可证文件**。

只有当外部项目本身提供主许可证文件，且其内容为符合 OSI 要求的宽松许可证时，Zephyr 开发者才可将其加入模块代码库。主许可证文件应优先包含完整许可文本，而非仅列出 SPDX 标识符。如果存在多个主许可证文件，必须明确每个源文件适用哪一个。

模块源文件中的独立许可证头优先于主许可证。

模块仓库中的任何新增内容都必须有许可证覆盖。

  .. note::

     Zephyr 建议通过各文件的许可证头和主许可证文件说明模块许可，但这并非硬性要求。如果外部项目有自己的许可说明方式，例如使用一个或多个主许可证文件，只要满足 OSI 合规等许可要求，Zephyr 模块也可以接受并引用该方式。

许可证政策
==========

创建模块仓库时，开发者必须：

* 导入外部项目已有的主许可证文件，以及
* 记录覆盖模块代码库的默认许可证，例如在模块 README 或 .yml 文件中说明。

许可证检查
----------

必须对模块仓库中所有添加新内容的拉取请求启用 CI 许可证检查。


文档要求
********

所有 Zephyr 模块仓库都必须包含一个 .rst 文件，说明以下内容：

* 模块的范围和用途
* 模块如何与 Zephyr 集成
* 模块仓库的负责人
* 与外部项目的同步信息，例如提交、SHA、版本等
* :ref:`modules_licensing` 中要求的许可信息。

该文件是纳入模块的必要条件，其中的信息应保持更新。


测试要求
********

所有 Zephyr 模块都应提供一定程度的 **集成** 测试，确保它们与 Zephyr 正确集成。集成测试：

* 可以是位于 Zephyr 主仓库中的一组最小示例和测试
* 应验证模块与 Zephyr 集成后的基本用法，如配置和功能 API 等
* 必须在修改模块仓库的拉取请求所触发的 Twister 运行中构建并执行，例如在 QEMU 中执行。

  .. note::

     申请纳入 Zephyr 默认清单的新模块必须提供一定程度的集成测试。

  .. note::

     厂商 HAL 已通过在目标平台上构建或执行的 Zephyr 测试间接验证，因此无需另外提供集成测试。

集成测试并非用于验证模块自身的功能；功能验证应由外部项目的测试框架承担。

某些外部项目的测试套件位于上游测试基础设施中，但专为 Zephyr 编写。这类测试可以纳入 Zephyr 测试框架，但并非必须。

弃用和移除模块
**************

模块可能因以下原因被弃用，原因不限于此：

* 模块缺少维护者
* 外部项目的许可证发生变化
* 代码库已过时

模块信息必须标明模块是否已弃用。尝试使用已弃用模块构建 Zephyr 时，构建系统必须发出警告。

模块弃用后，经过两个 Zephyr 发布版本，可以将其从默认清单中移除。

  .. note::

     移除模块后，其仓库必须仍可通过原始 URL 访问，因为旧版 Zephyr 仍需要它们。


将模块集成到 Zephyr 构建系统
****************************

构建系统变量 :makevar:`ZEPHYR_MODULES` 是一个 `CMake list`_，其中包含各 Zephyr 模块目录的绝对路径。模块内的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件分别说明如何构建和配置模块。构建过程通过 CMake 的 `add_subdirectory()`_ 命令加入模块的 :file:`CMakeLists.txt`，并将 :file:`Kconfig` 文件纳入构建的 Kconfig 菜单树。

如果已安装 :ref:`west <west>`，除非要添加新模块，否则无需关心该变量如何定义，构建系统会通过 west 设置 :makevar:`ZEPHYR_MODULES`。可以通过设置 :makevar:`EXTRA_ZEPHYR_MODULES` CMake 变量，或在 ``.zephyrrc`` 中加入 :makevar:`EXTRA_ZEPHYR_MODULES` 行，来添加额外模块，详见 :ref:`env_vars`。这适用于既保留 west 找到的模块，又加入自定义模块的情况。如果在多处设置 :makevar:`EXTRA_ZEPHYR_MODULES`，例如同时设置环境变量和 CMake 变量，最终的额外模块列表会合并所有来源。

.. note::
   如果 :ref:`west <west>` 提供模块 ``FOO``，同时又通过 ``-DEXTRA_ZEPHYR_MODULES=/<path>/foo`` 指定该模块，则命令行变量 :makevar:`EXTRA_ZEPHYR_MODULES` 指定的模块优先。这样既可在构建时使用自定义版本的 ``FOO``，又能继续使用 :ref:`west <west>` 提供的其他 Zephyr 模块，例如用于特定测试。

如果希望永久向 Zephyr 工作区添加模块，且使用 Zephyr 作为清单仓库，也可以向 :zephyr_file:`submanifests` 目录添加 west 清单文件。详见 :zephyr_file:`submanifests/README.txt`。

有关 west 工作区的更多信息，见 :ref:`west-basics`。

也可以通过多种方式自行指定模块列表；如果应用不需要模块，还可以完全不使用模块。

.. _module-yml:

模块 YAML 文件说明
******************

可以使用名为 :file:`zephyr/module.yml` 的文件描述模块。下文介绍 :file:`zephyr/module.yml` 的格式。

模块名称
========

每个 Zephyr 模块都有一个名称，构建系统通过该名称引用它。

应在 :file:`zephyr/module.yml` 中指定名称，以避免用户自定义目录名或 ``west`` 清单文件改变模块名称：

.. code-block:: yaml

   name: <name>

在 CMake 中，可以通过 ``ZEPHYR_<MODULE_NAME>_MODULE_DIR`` 变量引用模块位置，而 ``ZEPHYR_<MODULE_NAME>_CMAKE_DIR`` 保存包含模块 :file:`CMakeLists.txt` 文件的目录位置。

.. note::
   用于 CMake 和 Kconfig 变量时，模块名称中的字母全部转为大写，所有非字母数字字符都转为下划线（_）。例如，模块 ``foo-bar`` 必须在 CMake 和 Kconfig 中以 ``ZEPHYR_FOO_BAR_MODULE_DIR`` 引用。

下面以 Zephyr 模块 ``foo`` 为例：

.. code-block:: yaml

   name: foo

.. note::
   如果未指定 ``name`` 字段，模块名称就采用模块文件夹名。例如，位于 :file:`<workspace>/modules/bar` 的模块，如果 :file:`zephyr/module.yml` 中未指定名称，就使用 ``bar``。

模块集成文件（模块内部）
========================

可以按以下方式描述要纳入构建的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件：

.. code-block:: yaml

   build:
     cmake: <cmake-directory>
     kconfig: <directory>/Kconfig

``cmake: <cmake-directory>`` 表示 :file:`<cmake-directory>` 中包含要使用的 :file:`CMakeLists.txt`；``kconfig: <directory>/Kconfig`` 指定要使用的 Kconfig 文件。两者均为可选项：``cmake`` 默认为 ``zephyr``，``kconfig`` 默认为 ``zephyr/Kconfig``。

以下 :file:`module.yml` 示例引用模块根目录中的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件：

.. code-block:: yaml

   build:
     cmake: .
     kconfig: Kconfig

.. _sysbuild_module_integration:

Sysbuild 集成
=============

:ref:`Sysbuild <sysbuild>` 是 Zephyr 的构建系统，允许将多个映像作为单个应用的一部分进行构建。可以按需通过外部模块扩展 sysbuild 构建过程，例如添加自定义构建步骤或额外目标。可按以下方式描述 sysbuild 专用的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件：

.. code-block:: yaml

   build:
     sysbuild-cmake: <cmake-directory>
     sysbuild-kconfig: <directory>/Kconfig

``sysbuild-cmake: <cmake-directory>`` 表示 :file:`<cmake-directory>` 中包含要使用的 :file:`CMakeLists.txt`；``sysbuild-kconfig: <directory>/Kconfig`` 指定要使用的 Kconfig 文件。

以下 :file:`module.yml` 示例引用模块 ``sysbuild`` 目录中的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件：

.. code-block:: yaml

   build:
     sysbuild-cmake: sysbuild
     sysbuild-kconfig: sysbuild/Kconfig

模块描述文件 :file:`zephyr/module.yml` 还可以指定构建文件 :file:`CMakeLists.txt` 和 :file:`Kconfig` 位于 :ref:`modules_module_ext_root` 中。

位于 ``MODULE_EXT_ROOT`` 中的构建文件可按以下方式描述：

.. code-block:: yaml

   build:
     sysbuild-cmake-ext: True
     sysbuild-kconfig-ext: True

这样便可在 Zephyr 模块之外描述如何将其纳入构建。

.. _modules-vulnerability-monitoring:

漏洞监测
========

模块描述文件 :file:`zephyr/module.yml` 可用于改进漏洞监测。

如果模块需要通过外部引用跟踪漏洞，例如模块是从其他仓库派生的，可以使用 ``security`` 部分。其 ``external-references`` 字段列出需要为模块监测的引用，支持以下格式：

- CPE（通用平台枚举）
- PURL（软件包 URL）

.. code-block:: yaml

   security:
     external-references:
       - <module-related-cpe>
       - <an-other-module-related-cpe>
       - <module-related-purl>

Mbed TLS 模块的实际示例可能如下：

.. code-block:: yaml

   security:
     external-references:
       - cpe:2.3:a:arm:mbed_tls:3.5.2:*:*:*:*:*:*:*
       - pkg:github/Mbed-TLS/mbedtls@V3.5.2

.. note::
   CPE 字段必须遵循 `NVD <https://csrc.nist.gov/projects/security-content-automation-protocol/specifications/cpe>`_ 提供的 CPE 2.3 模式；PURL 字段必须遵循 `Github <https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst>`_ 提供的 PURL 规范。


构建系统集成
============

模块包含 :file:`module.yml` 文件时，会自动纳入 Zephyr 构建系统，随后可通过 Kconfig 和 CMake 变量访问模块路径。

Zephyr 模块
-----------

在 Kconfig 和 CMake 中，``ZEPHYR_<MODULE_NAME>_MODULE_DIR`` 都包含模块的绝对路径。

此外，构建系统会为可用模块自动生成 ``ZEPHYR_<MODULE_NAME>_MODULE`` 符号；如果模块声明了二进制文件，还会生成 ``ZEPHYR_<MODULE_NAME>_MODULE_BLOBS``。依赖该模块或其二进制文件的其他 Kconfig 符号可用它们声明依赖。为使缺少该模块时的 Zephyr 构建也能通过合规检查，建议在 Zephyr 主仓库 ``modules/`` 下对应的 Kconfig 文件中，为这些符号提供默认定义。

在 CMake 中，``ZEPHYR_<MODULE_NAME>_CMAKE_DIR`` 包含纳入 CMake 构建系统的 :file:`CMakeLists.txt` 所在目录的绝对路径。如果 module.yml 未指定 CMakeLists.txt，该变量为空。

对于名为 ``foo`` 的 Zephyr 模块，可按以下方式读取这些变量：

- 在 CMake 中，使用 ``${ZEPHYR_FOO_MODULE_DIR}`` 获取模块顶层目录，使用 ``${ZEPHYR_FOO_CMAKE_DIR}`` 获取 :file:`CMakeLists.txt` 所在目录
- 在 Kconfig 中，使用 ``$(ZEPHYR_FOO_MODULE_DIR)`` 获取模块顶层目录

注意，在 CMake 和 Kconfig 中，小写模块名 ``foo`` 都会转为大写 ``FOO``。

也可以用这些变量检查指定模块是否存在。例如，验证 ``foo`` 是否为 Zephyr 模块的名称：

.. code-block:: cmake

  if(ZEPHYR_FOO_MODULE_DIR)
    # Do something if FOO exists.
  endif()

在 Kconfig 中，可以使用该变量查找要包含的其他文件。例如，包含模块 ``foo`` 中的 :file:`some/Kconfig`：

.. code-block:: kconfig

  source "$(ZEPHYR_FOO_MODULE_DIR)/some/Kconfig"

CMake 处理每个 Zephyr 模块时，还可使用以下变量：

- 当前模块名称：``${ZEPHYR_CURRENT_MODULE_NAME}``
- 当前模块顶层目录：``${ZEPHYR_CURRENT_MODULE_DIR}``
- 当前模块的 :file:`CMakeLists.txt` 所在目录：``${ZEPHYR_CURRENT_CMAKE_DIR}``

因此，Zephyr 模块在 CMake 处理阶段无需知道自身名称，可以使用这些 ``CURRENT`` 变量引入其他 CMake 文件。例如：

.. code-block:: cmake

  include(${ZEPHYR_CURRENT_MODULE_DIR}/cmake/code.cmake)

可以从模块的第一个 CMakeLists.txt 文件向 Zephyr 的 `CMake list`_ 变量追加值。先追加值，再将该列表设置到此 CMakeLists.txt 的 PARENT_SCOPE 中。例如，向 Zephyr CMakeLists.txt 作用域中的 ``FOO_LIST`` 追加 ``bar``：

.. code-block:: cmake

  list(APPEND FOO_LIST bar)
  set(FOO_LIST ${FOO_LIST} PARENT_SCOPE)

需要向 ``SYSCALL_INCLUDE_DIRS`` 列表添加额外目录时，这种方式就很有用。

Sysbuild 模块
-------------

在 Kconfig 和 CMake 中，``SYSBUILD_CURRENT_MODULE_DIR`` 都包含 sysbuild 模块的绝对路径。在 CMake 中，``SYSBUILD_CURRENT_CMAKE_DIR`` 包含纳入 CMake 构建系统的 :file:`CMakeLists.txt` 所在目录的绝对路径。如果 module.yml 未指定 CMakeLists.txt，该变量为空。

对于 sysbuild 模块，可按以下方式读取这些变量：

- 在 CMake 中，使用 ``${SYSBUILD_CURRENT_MODULE_DIR}`` 获取模块顶层目录，使用 ``${SYSBUILD_CURRENT_CMAKE_DIR}`` 获取 :file:`CMakeLists.txt` 所在目录
- 在 Kconfig 中，使用 ``$(SYSBUILD_CURRENT_MODULE_DIR)`` 获取模块顶层目录

在 Kconfig 中，可以使用该变量查找要包含的其他文件。例如，包含 :file:`some/Kconfig`：

.. code-block:: kconfig

  source "$(SYSBUILD_CURRENT_MODULE_DIR)/some/Kconfig"

模块可以通过这些变量引入其他 CMake 文件。例如：

.. code-block:: cmake

  include(${SYSBUILD_CURRENT_MODULE_DIR}/cmake/code.cmake)

可以从模块的第一个 CMakeLists.txt 文件向 Zephyr 的 `CMake list`_ 变量追加值。先追加值，再将该列表设置到此 CMakeLists.txt 的 PARENT_SCOPE 中。例如，向 Zephyr CMakeLists.txt 作用域中的 ``FOO_LIST`` 追加 ``bar``：

.. code-block:: cmake

  list(APPEND FOO_LIST bar)
  set(FOO_LIST ${FOO_LIST} PARENT_SCOPE)

Sysbuild 模块钩子
-----------------

Sysbuild 提供了一套机制，使 sysbuild 模块能够定义函数，并在 CMake 流程中的预定位置调用。

Sysbuild 会调用以下函数：

- ``<module-name>_pre_cmake(IMAGES <images>)``：在为所有映像执行 CMake 配置之前，对每个 sysbuild 模块调用该函数。
- ``<module-name>_post_cmake(IMAGES <images>)``：所有映像的 CMake 配置完成之后，对每个 sysbuild 模块调用该函数。
- ``<module-name>_pre_domains(IMAGES <images>)``：sysbuild 创建 domains YAML 文件之前，对每个 sysbuild 模块调用该函数。
- ``<module-name>_post_domains(IMAGES <images>)``：sysbuild 创建 domains YAML 文件之后，对每个 sysbuild 模块调用该函数。

Sysbuild 传给模块所定义函数的参数：

- ``<images>`` 是构建系统将要创建的 Zephyr 映像列表。

如果模块 ``foo`` 要提供 CMake 配置后执行的函数，就必须在模块的 sysbuild :file:`CMakeLists.txt` 中定义 ``foo_post_cmake()``。

为方便命名，sysbuild CMake 加载模块的 sysbuild :file:`CMakeLists.txt` 时，会通过 ``SYSBUILD_CURRENT_MODULE_NAME`` CMake 变量提供模块名称。

以下示例展示 ``foo`` sysbuild 模块如何定义 ``foo_post_cmake()``：

.. code-block:: cmake

   function(${SYSBUILD_CURRENT_MODULE_NAME}_post_cmake)
     cmake_parse_arguments(POST_CMAKE "" "" "IMAGES" ${ARGN})

     message("Invoking ${CMAKE_CURRENT_FUNCTION}. Images: ${POST_CMAKE_IMAGES}")
   endfunction()

Zephyr 模块依赖
===============

Zephyr 模块可能需要其他模块存在才能正常工作；也可能因某些 CMake 目标的依赖关系，必须在另一个模块之后处理。

可以使用 ``depends`` 字段描述此类依赖。

.. code-block:: yaml

   build:
     depends:
       - <module>

以下示例中，Zephyr 模块 ``foo`` 要求构建系统中存在模块 ``bar``：

.. code-block:: yaml

   name: foo
   build:
     depends:
       - bar

此示例既确保纳入 ``foo`` 时存在 ``bar``，也确保先处理 ``bar``，再处理 ``foo``。

.. _modules_module_ext_root:

模块集成文件（模块外部）
========================

模块集成文件可以位于模块自身之外。``MODULE_EXT_ROOT`` 变量保存一个根目录列表，这些根目录包含位于 Zephyr 模块之外的集成文件。

Zephyr 中的模块集成文件
-----------------------

Zephyr 仓库为某些已知模块提供了 :file:`CMakeLists.txt` 和 :file:`Kconfig` 构建文件。

这些文件位于以下位置：

.. code-block:: none

   <ZEPHYR_BASE>
   └── modules
       └── <module_name>
           ├── CMakeLists.txt
           └── Kconfig

自定义位置中的模块集成文件
--------------------------

可以为其他模块创建类似的 ``MODULE_EXT_ROOT``，让 Zephyr 构建系统能够识别它们。

按以下结构创建 ``MODULE_EXT_ROOT``：

.. code-block:: none

   <MODULE_EXT_ROOT>
   └── modules
       ├── modules.cmake
       └── <module_name>
           ├── CMakeLists.txt
           └── Kconfig

然后在构建应用时，向 CMake 构建系统指定 ``-DMODULE_EXT_ROOT`` 参数。``MODULE_EXT_ROOT`` 接受一个由根目录组成的 `CMake list`_。

可以通过模块描述文件 :file:`zephyr/module.yml`，将 Zephyr 模块自动添加到 ``MODULE_EXT_ROOT`` 列表，见 :ref:`modules_build_settings`。

.. note::

   ``ZEPHYR_BASE`` 始终以最低优先级加入 ``MODULE_EXT_ROOT``。因此，可以在自己的 ``MODULE_EXT_ROOT`` 中提供实现，覆盖 ``<ZEPHYR_BASE>/modules/<module_name>`` 下的集成文件。

:file:`modules.cmake` 必须包含相应逻辑，通过特定名称的 CMake 变量为 Zephyr 模块指定集成文件。

要纳入模块的 CMake 文件，将 ``ZEPHYR_<MODULE_NAME>_CMAKE_DIR`` 设为该文件所在目录的路径。

要纳入模块的 Kconfig 文件，将 ``ZEPHYR_<MODULE_NAME>_KCONFIG`` 设为该文件的路径。

以下示例展示如何添加对 ``FOO`` 模块的支持。

创建以下目录结构：

.. code-block:: none

   <MODULE_EXT_ROOT>
   └── modules
       ├── modules.cmake
       └── foo
           ├── CMakeLists.txt
           └── Kconfig

然后在 :file:`modules.cmake` 中添加以下内容：

.. code-block:: cmake

   set(ZEPHYR_FOO_CMAKE_DIR ${CMAKE_CURRENT_LIST_DIR}/foo)
   set(ZEPHYR_FOO_KCONFIG   ${CMAKE_CURRENT_LIST_DIR}/foo/Kconfig)

模块集成文件（zephyr/module.yml）
---------------------------------

模块描述文件 :file:`zephyr/module.yml` 可指定构建文件 :file:`CMakeLists.txt` 和 :file:`Kconfig` 位于 :ref:`modules_module_ext_root` 中。

位于 ``MODULE_EXT_ROOT`` 中的构建文件可按以下方式描述：

.. code-block:: yaml

   build:
     cmake-ext: True
     kconfig-ext: True

这样便可在 Zephyr 模块之外描述如何将其纳入构建。

Zephyr 仓库自身始终会被加入 Zephyr 模块扩展根目录列表。

.. _modules_build_settings:

构建设置
========

可以指定将模块纳入构建系统时必须使用的额外构建设置。

所有 ``root`` 设置都相对于模块根目录。

:file:`module.yml` 支持以下构建设置：

- ``board_root``：包含构建系统可用的额外开发板。开发板必须位于 :file:`<board_root>/boards` 文件夹中。
- ``dts_root``：包含与架构或 SoC 系列有关的额外 DTS 文件，必须位于 :file:`<dts_root>/dts` 文件夹中。
- ``snippet_root``：包含额外的可用 snippet。它们必须通过 :file:`<snippet_root>/snippets` 下的 :file:`snippet.yml` 定义。例如，设置 ``snippet_root: foo`` 时，模块的 :file:`snippet.yml` 应放在 :file:`<your-module>/foo/snippets` 或其任意子目录中。
- ``soc_root``：包含构建系统可用的额外 SoC，必须位于 :file:`<soc_root>/soc` 文件夹中。
- ``arch_root``：包含构建系统可用的额外架构，必须位于 :file:`<arch_root>/arch` 文件夹中。
- ``module_ext_root``：包含 Zephyr 模块的 :file:`CMakeLists.txt` 和 :file:`Kconfig` 文件，另见 :ref:`modules_module_ext_root`。
- ``sca_root``：包含构建系统可用的额外 :ref:`SCA <sca>` 工具实现。每个工具必须位于 :file:`<sca_root>/sca/<tool>` 文件夹中，并包含 :file:`sca.cmake`。

以下示例给出了包含额外根目录的 :file:`module.yaml` 文件及对应文件系统布局。

.. code-block:: yaml

   build:
     settings:
       board_root: .
       dts_root: .
       soc_root: .
       arch_root: .
       module_ext_root: .


需要以下目录结构：

.. code-block:: none

   <zephyr-module-root>
   ├── arch
   ├── boards
   ├── dts
   ├── modules
   └── soc

测试运行器（Twister）集成
=========================

要执行模块中的测试和示例，需要为 Zephyr 测试运行器（twister）指定这些文件所在的目录。可以在 :file:`zephyr/module.yml` 中设置测试和示例路径。此外，如果模块定义了树外开发板，也可以在该文件中指明开发板文件在模块内的维护位置，供 twister 使用。例如：

.. code-block:: yaml

    build:
      cmake: .
    samples:
      - samples
    tests:
      - tests
    boards:
      - boards

Twister 不会自动检测 :file:`zephyr/module.yml` 中定义的测试和示例。要让它识别这些内容，必须在运行 twister 时将相应路径加入命令行，例如：

.. code-block:: shell

  ./scripts/zephyr_module.py --twister-out module_tests.args
  if [ -s module_tests.args ]; then
      west twister +module_tests.args --outdir module_tests ...
  fi


.. _modules-bin-blobs:

二进制文件
==========

Zephyr 支持获取和使用 :ref:`二进制文件 <bin-blobs>`，其元数据全部存放在 :file:`zephyr/module.yml` 中。这是因为二进制文件必须关联到某个 Zephyr 模块，因此元数据应属于模块描述本身。

使用 :ref:`west blobs <west-blobs>` 获取二进制文件。如果 :ref:`不使用 <modules_without_west>` ``west``，则必须手动下载和验证。

:file:`zephyr/module.yml` 中的 ``blobs`` 部分是一组映射，每个映射包含以下条目：

- ``path``：二进制文件相对于模块仓库 :file:`zephyr/blobs/` 文件夹的路径
- ``sha256``：二进制文件的 `SHA-256 <https://en.wikipedia.org/wiki/SHA-2>`_ 校验和
- ``type``：:ref:`二进制文件类型 <bin-blobs-types>`，目前仅支持 ``img`` 或 ``lib``
- ``version``：版本字符串
- ``license-path``：该二进制文件的许可证文件路径，相对于模块仓库根目录
- ``url``：指定二进制文件获取位置和获取方式的 URL。如果提供的是列表而非单个字符串，其中各 URL 会作为获取同一文件的备用地址。
- ``description``：便于人阅读的二进制文件说明
- ``doc-url``：指向该二进制文件官方文档的 URL

还可以包含以下条目：

- ``click-through``：布尔值，表示下载该二进制文件是否必须先点击接受许可证
- ``size``：二进制文件的大小，以字节为单位。某些获取工具可能要求提供
- ``fetcher``：下载二进制文件的方法。未指定时，根据 URL 推断

包管理器依赖
============

Zephyr 模块可以描述通过包管理器提供的依赖，目前仅支持 ``pip``。

west 扩展命令 ``west packages <manager>`` 可以列出 Zephyr 以及当前存在、并在 ``module.yml`` 中使用此功能的模块的依赖。详情可运行 ``west help packages``。

Python pip
----------

调用 ``west packages pip`` 可列出 Zephyr 和模块的 `requirement files`_。如果当前存在已激活的虚拟环境，传入 ``--install`` 即可安装其中的依赖。

以下示例展示一个 ``zephyr/module.yml`` 文件，依赖声明文件位于模块的 ``scripts`` 目录中。


.. code-block:: yaml

    package-managers:
      pip:
        requirement-files:
          - scripts/requirements-build.txt
          - scripts/requirements-doc.txt


.. _modules-runners:

外部运行器
==========

如果模块中的树外开发板需要自定义 :ref:`运行器 <west-runner>`，可以在 ``zephyr/module.yml`` 中添加一个列表，例如：


.. code-block:: yaml

    runners:
      - file: scripts/my-runner.py


执行 ``west flash`` 或 ``west debug`` 时会导入列表中的各个文件，并注册 ``ZephyrBinaryRunner`` 子类供使用。

纳入模块
========

.. _modules_using_west:

使用 west
---------

如果已安装 west，且尚未设置 :makevar:`ZEPHYR_MODULES`，构建系统会查找并使用 :term:`west installation` 中的所有模块。它通过运行 :ref:`west list <west-built-in-misc>` 获取各项目路径，再筛选出具有必要模块元数据文件的项目。

对 ``west list`` 输出中的每个项目，按以下方式检查：

- 如果项目包含 :file:`zephyr/module.yml`，则使用其内容确定应纳入构建的文件，具体见上一节。

- 否则，即项目不含 :file:`zephyr/module.yml` 时，构建系统会查找项目中的 :file:`zephyr/CMakeLists.txt` 和 :file:`zephyr/Kconfig`。如果两者都存在，则将该项目视为模块，并将这两个文件纳入构建。

- 如果两项检查均未通过，则不将该项目视为模块，也不会将其加入 :makevar:`ZEPHYR_MODULES`。

.. _modules_without_west:

不使用 west
-----------

如果未安装 west，或不希望构建系统通过 west 查找 Zephyr 模块，可以用以下任一方式自行设置 :makevar:`ZEPHYR_MODULES`。如上一节所述，列表中的每个目录都必须包含 :file:`zephyr/module.yml`，或同时包含 :file:`zephyr/CMakeLists.txt` 和 :file:`Kconfig`。

#. 在 CMake 命令行中设置，例如：

   .. code-block:: console

      cmake -DZEPHYR_MODULES=<path-to-module1>[;<path-to-module2>[...]] ...

#. 在应用顶层 :file:`CMakeLists.txt` 的开头设置，例如：

   .. code-block:: cmake

      set(ZEPHYR_MODULES <path-to-module1> <path-to-module2> [...])
      find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

   选择此方式时，务必如上所示，在调用 ``find_package(Zephyr ...)`` **之前** 设置该变量。

#. 在用于预填 CMake 缓存的独立 CMake 脚本中设置，例如：

   .. code-block:: cmake

      # Put this in a file with a name like "zephyr-modules.cmake"
      set(ZEPHYR_MODULES <path-to-module1> <path-to-module2>
        CACHE STRING "pre-cached modules")

   在 CMake 命令行中添加 ``-C zephyr-modules.cmake``，即可让构建系统使用此文件。

不使用模块
----------

如果未安装 west，也未自行设置 :makevar:`ZEPHYR_MODULES`，则不会向构建添加额外模块。仍可构建不依赖外部仓库代码或 Kconfig 选项的应用。

向模块提交变更
**************

提交新模块或修改现有模块时，Zephyr 主仓库需要引用这些变更，以便验证。主仓库通过 revision 实现引用：对于已经合并的代码，可以使用提交哈希、标签或分支名称；对于拉取请求，则必须在 revision 字段中指定拉取请求编号，以便将模块中的拟议变更用于构建 Zephyr 主仓库。

为避免将含有拉取请求引用的修改误合入 master，应将拉取请求标记为 ``DNM`` （Do Not Merge），更推荐设为草稿，以确保模块先合并并获得永久提交哈希。草稿在标记为“Ready for review”之前不会自动通知他人，因此可减少通知干扰。模块合并后，提交者或维护者需要将 revision 改为模块仓库中体现这些变更的提交哈希。

对多个模块进行相互依赖的修改时，也可以使用相同流程。此时需要修改所有相关模块的清单条目，使其指向各自的拉取请求。

.. _submitting_new_modules:

提交新模块的流程
================

请遵循 :ref:`external-src-process` 中的流程，取得 TSC 批准后，将外部源代码作为模块集成。

申请获批后，项目团队会创建新仓库并初始化基本信息，使贡献者可以按照项目贡献指南向模块项目提交代码。

如果模块作为其他 GitHub 项目的派生仓库维护，则 Zephyr 模块相关文件以及相对于上游的变更必须保存在名为 ``zephyr`` 的专用分支中。

Zephyr 项目维护者会创建并初始化仓库，并将你添加为协作者。请按照 :ref:`此处 <modules_using_west>` 的指南向新仓库提交模块代码，再向 :zephyr_file:`west.yml` 添加包含以下信息的新条目：

   .. code-block:: console

        - name: <name of repository>
          path: <path to where the repository should be cloned>
          revision: <ref pointer to module pull request>


例如，将 *my_module* 加入清单：

.. code-block:: console

    - name: my_module
      path: modules/lib/my_module
      revision: pull/23/head


上述示例中的 23 表示向 *my_module* 仓库提交的拉取请求编号。模块变更通过审查并合并后，需要将 revision 改为模块仓库的提交哈希。

.. _changes_to_existing_module:

修改现有模块的流程
==================

#. 按照 :ref:`贡献指南 <contribute_guidelines>` 和 :ref:`贡献者要求 <contributor-expectations>`，通过拉取请求向现有仓库提交变更。
#. 向 Zephyr 主仓库提交拉取请求，修改 :zephyr_file:`west.yml` 中引用该模块的条目，使用以下信息：

   .. code-block:: console

        - name: <name of repository>
          path: <path to where the repository should be cloned>
          revision: <ref pointer to module pull request>


例如，将 *my_module* 加入清单：

.. code-block:: console

    - name: my_module
      path: modules/lib/my_module
      revision: pull/23/head

上述示例中的 23 表示向 *my_module* 仓库提交的拉取请求编号。模块变更通过审查并合并后，需要将 revision 改为模块仓库的提交哈希。



.. _CMake list: https://cmake.org/cmake/help/latest/manual/cmake-language.7.html#lists
.. _add_subdirectory(): https://cmake.org/cmake/help/latest/command/add_subdirectory.html
.. _GitHub issues: https://github.com/zephyrproject-rtos/zephyr/issues
.. _requirement files: https://pip.pypa.io/en/stable/reference/requirements-file-format/
