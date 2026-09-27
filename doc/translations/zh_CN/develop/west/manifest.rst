.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-manifests:

West 清单
#########

本页详细介绍 west 的多仓库模型、清单文件和 ``west manifest`` 命令。``west.manifest`` 模块的 API 文档见 :ref:`west-apis-manifest`。更一般的入门介绍和命令概览见 :ref:`west-basics`。

.. only:: html

   .. contents::
      :depth: 3

.. _west-mr-model:

多仓库模型
**********

West 对 :term:`west workspace` 内仓库及其历史的视图如下图所示（不过，此示例的部分内容专门对应上游 Zephyr 对 west 的用法）：

.. figure:: west-mr-model.png
   :align: center
   :alt: West multi-repo history
   :figclass: align-center

   West 多仓库历史

清单仓库的历史是“浮”在灰色平面上方的一条 Git 提交线。实线箭头从父提交指向子提交。下方平面包含工作区各仓库的 Git 提交历史，每个项目仓库用一个矩形框表示。各仓库内的父子提交关系也用实线箭头表示。

清单仓库中的每个提交都包含一个清单文件（对于上游 Zephyr，清单仓库就是 zephyr 仓库本身）。每个提交中的清单文件指定它期望各项目仓库使用的对应提交。图中以虚线箭头表示这种关系，每条虚线箭头都从清单仓库的一个提交指向项目仓库的对应提交。

请注意以下重要细节：

- 可以添加项目（例如清单仓库提交 ``D`` 与 ``E`` 之间的 ``P1``），也可以移除项目（同一对清单仓库提交之间的 ``P2``）

- 项目与清单仓库的历史不必一起前进或后退：

  - 从 ``A → B``，``P2`` 保持不变；从 ``F → G``，``P1`` 和 ``P3`` 也保持不变。
  - 从 ``A → B``，``P3`` 向前推进。
  - 从 ``C → D``，``P3`` 向后回退。

  回退项目历史的一个用途，是退回到引入回归问题之前的修订版本，从而“撤销”该问题。

- 可以“跳过”项目仓库中的提交：从 ``B → C``，``P3`` 在其历史中向前跨越了多个提交。

- 上图中，没有项目仓库在“同一时刻”具有两个修订版本：每份清单文件对其关注的每个项目都恰好引用一个提交。可以使用分支名称作为清单修订版本来放宽此限制，但代价是失去对清单仓库历史进行二分定位的能力。

.. _west-manifest-files:

清单文件
********

West 清单是 YAML 文件，顶层包含 ``manifest`` 节及若干子节，例如：

.. code-block:: yaml

   manifest:
     remotes:
       # short names for project URLs
     projects:
       # a list of projects managed by west
     defaults:
       # default project attributes
     self:
       # configuration related to the manifest repository itself,
       # i.e. the repository containing west.yml
     version: "<schema-version>"
     group-filter:
       # a list of project groups to enable or disable

用 YAML 术语来说，清单文件包含一个具有 ``manifest`` 键的映射。其他键及其内容均被忽略（west v0.5 还要求 ``west`` 键，但从 v0.6 起会忽略它）。

清单包含 ``defaults``、``remotes``、``projects`` 和 ``self`` 等子节。用 YAML 术语来说，``manifest`` 键的值也是一个映射，以这些“子节”为键。从 west v0.10 起，这些“子节”键全部可选。

``projects`` 的值是由 west 管理的仓库及其元数据的列表。稍后会讨论它；首先介绍可减少 ``projects`` 列表中重复输入的 ``remotes`` 节。

远程仓库
========

``remotes`` 子节包含一个序列，指定获取项目所用的基础 URL。

每个 ``remotes`` 元素都有名称和“基础 URL”，用于组成各项目完整的 Git 获取 URL。可以在远程基础 URL 后追加项目专用路径，形成项目获取 URL。（如下文所述，项目也可以直接指定完整获取 URL。）

例如：

.. code-block:: yaml

   manifest:
     # ...
     remotes:
       - name: remote1
         url-base: https://git.example.com/base1
       - name: remote2
         url-base: https://git.example.com/base2

``remotes`` 的键及用法见下表。

.. list-table:: remotes 的键
   :header-rows: 1
   :widths: 1 5

   * - 键
     - 描述

   * - ``name``
     - 必需；远程仓库的唯一名称。

   * - ``url-base``
     - 为使用此远程仓库的每个项目的获取 URL 添加的前缀。

上例给出两个远程仓库，名称为 ``remote1`` 和 ``remote2``，基础 URL 分别是 ``https://git.example.com/base1`` 和 ``https://git.example.com/base2``。也可以使用 SSH 基础 URL；例如，如果 ``remote1`` 也支持通过 SSH 使用 Git，就可以采用 ``git@example.com:base1``。任何 Git 接受的形式都可以。

.. _west-manifests-projects:

项目
====

``projects`` 子节包含描述 west 工作区中项目仓库的序列。每个项目具有唯一名称。可以指定克隆和获取项目时使用的 Git 远程 URL、要跟踪的修订版本，以及项目在本地文件系统中的存储位置。请注意，west 项目 :ref:`不同于模块 <modules-vs-projects>`。

以下示例采用上文定义的 ``remotes``。

.. Note: if you change this example, keep the equivalent manifest below in
   sync.

.. code-block:: yaml

   manifest:
     # [... same remotes as above...]
     projects:
       - name: proj1
         description: the first example project
         remote: remote1
         path: extra/project-1
       - name: proj2
         description: |
           A multi-line description of the second example
           project.
         repo-path: my-path
         remote: remote2
         revision: v1.3
       - name: proj3
         url: https://github.com/user/project-three
         revision: abcde413a111
       - name: proj4
         url: https://github.com/user/project-four
         revision: pull/69/head # GitHub Pull Request

在此清单中：

- ``proj1`` 使用远程仓库 ``remote1``，因此 Git 获取 URL 为 ``https://git.example.com/base1/proj1``。在远程 ``url-base`` 后追加 ``/`` 和项目 ``name``，即可形成此 URL。

  本地会将此项目克隆到相对于 west 工作区根目录的 ``extra/project-1`` 路径，因为其 ``path`` 属性显式指定了该值。

  项目未指定 ``revision``，因此默认使用 ``master``。West 下次更新此项目时，会获取该分支的当前顶端提交，并将其检出为分离的 ``HEAD``。

- ``proj2`` 同时具有 ``remote`` 和 ``repo-path``，因此其获取 URL 为 ``https://git.example.com/base2/my-path``。存在 ``repo-path`` 属性时，构造获取 URL 会用它覆盖默认的 ``name``。

  项目没有 ``path`` 属性，因此默认使用 ``name``，将其克隆到名为 ``proj2`` 的目录。West 更新项目时，会检出 ``v1.3`` 标签指向的提交。

- ``proj3`` 显式指定了 ``url``，因此从 ``https://github.com/user/project-three`` 获取。

  其本地路径默认为名称 ``proj3``。下次更新时会检出提交 ``abcde413a111``。

可用的项目键及用法见下表。其中有时会提到 ``defaults`` 子节，下一节将介绍它。

.. list-table:: projects 元素的键
   :header-rows: 1
   :widths: 1 5

   * - 键
     - 描述

   * - ``name``
     - 必需；项目的唯一名称。名称不能是保留值“west”或“manifest”，且在清单文件中必须唯一。

   * - ``description``
     - 可选，项目的说明性描述。在 west v1.2.0 中添加。

   * - ``remote``、``url``
     - 必需（二者选一，不能同时指定）。

       如果项目有 ``remote``，则将该远程仓库的 ``url-base`` 与项目的 ``name`` （若有 ``repo-path`` 则用后者）组合成获取 URL。

       如果项目有 ``url``，则该值就是远程 Git 仓库的完整获取 URL。

       如果项目二者都没有，``defaults`` 节就必须指定 ``remote``，作为该项目的远程仓库。否则清单无效。

   * - ``repo-path``
     - 可选。如果指定，则将其追加到远程仓库的 ``url-base`` 后，代替项目的 ``name`` 来形成获取 URL。项目不能同时具有 ``url`` 和 ``repo-path`` 属性。

   * - ``revision``
     - 可选。指定 ``west update`` 应检出的 Git 修订版本。默认以分离 HEAD 方式检出，避免与本地分支名称冲突。如果未指定，则使用 ``defaults`` 子节中的 ``revision`` 值（如果存在）。

       项目修订版本可以是任何可获取的 Git 引用：分支、标签、SHA、拉取请求等。

       未另行指定时，默认 ``revision`` 为 ``master``。

       将 ``HEAD~0`` [#f1]_ 用作 ``revision``，会使 west 保持项目的当前状态。

   * - ``path``
     - 可选。相对于 west 工作区顶层目录的路径，指定在本地何处克隆仓库。如果缺失，使用项目 ``name`` 作为目录名。

   * - ``clone-depth``
     - 可选。指定正整数，会将克隆仓库的浅历史限制为给定提交数。仅在 ``revision`` 为分支或标签时可用。

   * - ``west-commands``
     - 可选。指定项目内一个 YAML 文件的相对路径，该文件描述项目提供的附加 west 命令。按惯例名为 :file:`west-commands.yml`。详情见 :ref:`west-extensions`。

   * - ``import``
     - 可选。如果为 ``true``，则从指定仓库的清单文件中导入项目到当前清单。详情见 :ref:`west-manifest-import`。

   * - ``groups``
     - 可选，项目所属组的列表。详情见 :ref:`west-manifest-groups`。

   * - ``submodules``
     - 可选。可以让 ``west update`` 同时更新项目定义的 `Git submodules`_。详情见 :ref:`west-manifest-submodules`。

   * - ``userdata``
     - 可选，值可以是任意 YAML 值。参见 :ref:`west-project-userdata`。

.. rubric:: 脚注

.. [#f1] 在 Git 中，HEAD 是引用，而 HEAD~<n> 是有效修订版本，但不是引用。West 会获取 refs/heads/main、HEAD 等引用，以及本地不存在的提交，但不会获取本地已有的提交。HEAD~0 会解析为本地已有的特定提交，因此 west 只会检出这个由 HEAD~0 标识的本地提交。

.. _Git submodules: https://git-scm.com/book/en/v2/Git-Tools-Submodules

默认值
======

``defaults`` 子节可为项目属性提供默认值，特别是默认远程仓库名称和修订版本。前述清单也可使用 ``defaults`` 改写为：

.. code-block:: yaml

   manifest:
     defaults:
       remote: remote1
       revision: v1.3

     remotes:
       - name: remote1
         url-base: https://git.example.com/base1
       - name: remote2
         url-base: https://git.example.com/base2

     projects:
       - name: proj1
         description: the first example project
         path: extra/project-1
         revision: master
       - name: proj2
         description: |
           A multi-line description of the second example
           project.
         repo-path: my-path
         remote: remote2
       - name: proj3
         url: https://github.com/user/project-three
         revision: abcde413a111

可用的 ``defaults`` 键及用法见下表。

.. list-table:: defaults 的键
   :header-rows: 1
   :widths: 1 5

   * - 键
     - 描述

   * - ``remote``
     - 可选。如果项目没有设置 ``url`` 或 ``remote`` 键，就将此值用作项目的 ``remote``。

   * - ``revision``
     - 可选。如果项目未设置 ``revision``，就使用此值。未指定时默认为 ``master``。

自身
====

``self`` 子节可用于控制清单仓库本身。

例如，来看 zephyr 仓库 :file:`west.yml` 中的这个片段：

.. code-block:: yaml

   manifest:
     # ...
     self:
       path: zephyr
       west-commands: scripts/west-commands.yml

这确保 zephyr 仓库克隆到路径 ``zephyr``；不过如上文所述，从默认清单 URL ``https://github.com/zephyrproject-rtos/zephyr`` 克隆时，本来就会如此。由于 zephyr 仓库确实包含扩展命令，其 ``self`` 条目声明了对应 :file:`west-commands.yml` 相对于仓库根目录的位置。

可用的 ``self`` 键及用法见下表。

.. list-table:: self 的键
   :header-rows: 1
   :widths: 1 5

   * - 键
     - 描述

   * - ``path``
     - 可选。指定 ``west init`` 应将清单仓库克隆到的路径，相对于 west 工作区顶层目录。

       如果未指定，默认使用清单仓库 URL 中路径部分的基本名称。例如 URL 为 ``https://git.example.com/project-repo`` 时，清单仓库会克隆到 :file:`project-repo` 目录。

   * - ``west-commands``
     - 可选，与项目序列元素中的同名键类似。

   * - ``import``
     - 可选，同样类似于 ``projects`` 中的键，但允许从清单仓库中的其他文件导入项目。参见 :ref:`west-manifest-import`。

.. _west-manifest-schema-version:

版本
====

``version`` 子节声明清单文件使用了某个 west 版本引入的功能。尝试用旧版 west 加载时会失败，并显示说明所需最低 west 版本的错误消息。

示例如下：

.. code-block:: yaml

   manifest:
     # Marks that this file uses version 0.10 of the west manifest
     # file format.
     #
     # An attempt to load this manifest file with west v0.8.0 will
     # fail with an error message saying that west v0.10.0 or
     # later is required.
     version: "0.10"

清单节使用 `west source code repository`_ 中的 pykwalify 模式 :file:`manifest-schema.yml` 进行验证。

.. _west source code repository:
   https://github.com/zephyrproject-rtos/west

下表列出有效的 ``version`` 值，以及相应版本引入的清单文件功能。

.. list-table::
   :header-rows: 1
   :widths: 1 4

   * - ``version``
     - 新功能

   * - ``"0.7"``
     - 首次支持 ``version`` 功能。表中未另行列出的所有清单文件功能，均在 west v0.7.0 或更早版本中引入。

   * - ``"0.8"``
     - 支持 ``import: path-prefix:`` （:ref:`west-manifest-import-map`）

   * - ``"0.9"``
     - **不建议使用 west v0.9.x**。

       提供此模式版本，是为了让用户显式要求兼容 west :ref:`west_0_9_0`。但 west :ref:`west_0_10_0` 及后续版本对 v0.9.0 引入的功能采用了不兼容行为。应尽可能避开版本“0.9”。

   * - ``"0.10"``

     - 支持：

       - ``projects:`` 中的 ``submodules:`` （:ref:`west-manifest-submodules`）
       - ``manifest: group-filter:`` 以及 ``projects:`` 中的 ``groups:`` （:ref:`west-manifest-groups`）
       - ``import:`` 功能现在支持 ``allowlist:`` 和 ``blocklist:``，建议分别用它们替代旧名称，这是 Zephyr 全项目包容性语言调整的一部分。为保持向后兼容，旧键名仍受支持。（:ref:`west-manifest-import`、:ref:`west-manifest-import-map`）

   * - ``"0.12"``
     - 支持 ``projects:`` 中的 ``userdata:`` （:ref:`west-project-userdata`）

   * - ``"0.13"``
     - 支持 ``self: userdata:`` （:ref:`west-project-userdata`）

   * - ``"1.0"``
     - 与 ``"0.13"`` 相同，供不希望使用 ``"0.x"`` 版本字段的用户选择。

   * - ``"1.2"``
     - 支持 ``projects:`` 中的 ``description:`` （:ref:`west-manifests-projects`）

.. note::

   未引入清单文件格式新功能的 west 版本，不会改变有效 ``version`` 值列表。例如，``version: "0.11"`` **无效**，因为 west v0.11.x 没有引入清单文件格式的新功能。

像上文一样用引号包围 ``version`` 值，会强制 YAML 解析器将其视为字符串。如果没有引号，YAML 中的 ``0.10`` 就只是浮点值 ``0.1``。如果转换为字符串后值相同，可以省略引号，但最好保留。不确定时始终使用引号。

如果清单中不包含 ``version``，每个新发布的 west 版本都会尝试使用该版本已有的功能加载它。如果 west 版本过旧，无法加载清单，错误消息可能更难理解。

组过滤器
========

参见 :ref:`west-manifest-groups`。

.. _west-active-inactive-projects:

活动与非活动项目
****************

west 清单中定义的项目可以是 *非活动* 或 *活动* 的。区别在于，west 通常会忽略非活动项目。例如，``west update`` 不更新非活动项目，``west list`` 默认不打印它们的信息。非活动项目中的任何 :ref:`west-manifest-import` 也会被 west 忽略。

有两种方式可使项目变为非活动状态：

1. 使用 ``manifest.project-filter`` 配置选项。如果通过此选项激活或停用项目，就会忽略通过 ``groups:`` 停用项目的相关规则。也就是说，如果 ``manifest.project-filter`` 中的正则表达式适用于某项目，该项目的组就不再影响其活动状态。

   详情见 :ref:`west-config-index` 中该选项的条目。

2. 否则，如果项目有组，且所有组均被禁用，则项目处于非活动状态。

   详情见下一节。

.. _west-manifest-groups:

项目组
******

可以使用 :ref:`上文 <west-manifest-files>` 简要介绍的 ``groups`` 和 ``group-filter`` 键，将项目分组，并启用或禁用组。

例如，可以通过 ``west forall --group``，让 ``west forall`` 命令只对组内项目执行。这也可让项目变为非活动状态；关于非活动项目，见上一节。

下一节介绍项目组，随后一节介绍 :ref:`west-enabled-disabled-groups`。基本示例见 :ref:`west-project-group-examples`。最后，:ref:`west-group-filter-imports` 简要说明 ``group-filter`` 与 :ref:`west-manifest-import` 功能的交互。

组基础
======

``groups:`` 和 ``group-filter:`` 键在清单中的形式如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: some-project
         groups: ...
     group-filter: ...

``groups`` 键的值是组名列表。组名为字符串。

可使用 ``group-filter`` 启用或禁用项目组。如果项目的所有组均被禁用，且未通过 ``manifest.project-filter`` 配置选项另行激活，则该项目处于非活动状态。

例如，在以下清单片段中：

.. code-block:: yaml

  manifest:
    projects:
      - name: project-1
        groups:
          - groupA
      - name: project-2
        groups:
          - groupB
          - groupC
      - name: project-3

各项目所属组如下：

- ``project-1``：一个组，名为 ``groupA``
- ``project-2``：两个组，名为 ``groupB`` 和 ``groupC``
- ``project-3``：没有组

项目组名称不能包含逗号 (,)、冒号 (:) 或空白。

组名不能以短横线 (-) 或加号 (+) 开头，但可以在其他位置包含这些字符。例如，``foo-bar`` 和 ``foo+bar`` 是有效组名，``-foobar`` 和 ``+foobar`` 则无效。

除此之外，组名可以是任意字符串，且区分大小写。

一项限制是，任何项目都不能同时使用 ``import:`` 和 ``groups:``。（这是为了避免某些异常边界情况。）

.. _west-enabled-disabled-groups:

启用和禁用的项目组
==================

所有项目组默认启用。可以在清单文件和 :ref:`west-config` 中启用或禁用组。

在清单文件中，``manifest: group-filter:`` 是列出待启用和禁用组的 YAML 列表。

要启用组，在名称前加上加号 (+)。例如，以下清单片段启用 ``groupA``：

.. code-block:: yaml

   manifest:
     group-filter: [+groupA]

对于默认已启用的组，这样写虽然多余，但可用来覆盖导入清单文件中的设置。更多信息见 :ref:`west-group-filter-imports`。

要禁用组，在名称前加上短横线 (-)。例如，以下清单片段禁用 ``groupA`` 和 ``groupB``：

.. code-block:: yaml

   manifest:
     group-filter: [-groupA,-groupB]

.. note::

   由于 ``group-filter`` 是 YAML 列表，上述片段也可以写成：

   .. code-block:: yaml

      manifest:
        group-filter:
          - -groupA
          - -groupB

   不过，这种语法更难阅读，因此不推荐。

除清单文件外，还可以使用 ``manifest.group-filter`` 配置选项控制组的启用和禁用。此选项是以逗号分隔的组列表，用于启用和/或禁用组。

要启用组，将其名称加上 ``+`` 前缀后加入列表；要禁用组，则加上 ``-`` 前缀。例如，将 ``manifest.group-filter`` 设为 ``+groupA,-groupB``，会启用 ``groupA`` 并禁用 ``groupB``。

配置选项的值会覆盖清单文件中的数据。可以将其理解为把 ``manifest.group-filter`` 配置选项追加到 YAML 的 ``manifest: group-filter:`` 列表，采用“最后一项优先”的语义。

实用示例：减少工作区下载
------------------------

默认情况下，``west update`` 获取清单中定义的所有活动项目。大型工作区可能包含并非每种工作流都需要的可选模块、厂商 HAL、实验组件，或特定平台的依赖项及其漏洞。

项目组可以控制 ``west`` 操作期间，哪些已分组的项目被视为活动项目。

例如，考虑以下清单片段：

.. code-block:: yaml

  manifest:
    projects:
      - name: hal_nordic
        groups:
          - nordic
      - name: hal_stm32
        groups:
          - stm32
      - name: experimental_lib
        groups:
          - optional

面向 Nordic 设备的工作区，可以在运行 ``west update`` 前禁用 ``stm32`` 和 ``optional`` 组：

.. code-block:: shell

   west config manifest.group-filter -- "-stm32,-optional"

配置过滤器后，运行：

.. code-block:: shell

   west update

这会跳过仅属于已禁用组的项目。

.. note::

   项目组只影响清单中显式分配到匹配组的项目。没有匹配组定义的项目，无论 ``manifest.group-filter`` 配置值如何，都保持活动状态。

.. note::

   修改 ``manifest.group-filter`` 不会自动删除工作区中已经克隆的仓库。它影响后续 ``west`` 操作中项目是否被视为活动项目。

此工作流有助于减少不必要的下载，并简化大型多项目环境中的工作区管理。

.. _west-project-group-examples:

项目组示例
==========

本节给出涉及项目组和活动项目的示例，同时使用 ``manifest: group-filter:`` YAML 列表和 ``manifest.group-filter`` 配置列表，展示二者如何配合。

请注意，下列清单中的 ``defaults`` 和 ``remotes`` 数据仅用于使示例完整、独立，与讨论本身无关。

.. note::

   以下所有示例均假定未设置 ``manifest.project-filter`` 选项。

示例 1：未禁用任何组
--------------------

完整清单文件如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         groups:
           - groupA
       - name: bar
         groups:
           - groupA
           - groupB
       - name: baz

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

未设置 ``manifest.group-filter`` 配置选项（可运行 ``west config -D manifest.group-filter`` 确保这一点）。

所有组默认启用，因此没有被禁用的组。三个项目（``foo``、``bar`` 和 ``baz``）全部处于活动状态。请注意，项目 ``baz`` 没有组，因此无法使其变为非活动状态。

示例 2：通过清单禁用一个组
--------------------------

完整清单文件如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         groups:
           - groupA
       - name: bar
         groups:
           - groupA
           - groupB

     group-filter: [-groupA]

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

未设置 ``manifest.group-filter`` 配置选项（可运行 ``west config -D manifest.group-filter`` 确保这一点）。

由于 ``groupA`` 被禁用，项目 ``foo`` 为非活动状态。``groupB`` 仍启用，因此项目 ``bar`` 为活动状态。

示例 3：通过清单禁用多个组
--------------------------

完整清单文件如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         groups:
           - groupA
       - name: bar
         groups:
           - groupA
           - groupB

     group-filter: [-groupA,-groupB]

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

未设置 ``manifest.group-filter`` 配置选项（可运行 ``west config -D manifest.group-filter`` 确保这一点）。

``foo`` 和 ``bar`` 的所有组均被禁用，因此二者都为非活动状态。

示例 4：通过配置禁用组
----------------------

完整清单文件如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         groups:
           - groupA
       - name: bar
         groups:
           - groupA
           - groupB

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

将 ``manifest.group-filter`` 配置选项设为 ``-groupA`` （可运行 ``west config manifest.group-filter -- -groupA`` 确保这一点；额外的 ``--`` 必不可少，否则参数解析器会将 ``-groupA`` 视为值为 ``roupA`` 的命令行选项 ``-g``）。

``manifest.group-filter`` 配置选项禁用了 ``groupA``，因此项目 ``foo`` 为非活动状态。``groupB`` 仍启用，因此项目 ``bar`` 为活动状态。

示例 5：通过配置覆盖已禁用的组
------------------------------

完整清单文件如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         groups:
           - groupA
       - name: baz
         groups:
           - groupA
           - groupB

     group-filter: [-groupA]

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

将 ``manifest.group-filter`` 配置选项设为 ``+groupA`` （可运行 ``west config manifest.group-filter +groupA`` 确保这一点）。

此时，``groupA`` 被启用：``manifest.group-filter`` 配置选项的优先级高于清单文件中的 ``manifest: group-filter: [-groupA]`` 内容。

因此，项目 ``foo`` 和 ``bar`` 均为活动状态。

示例 6：通过配置覆盖多个已禁用的组
----------------------------------

完整清单文件如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         groups:
           - groupA
       - name: baz
         groups:
           - groupA
           - groupB

     group-filter: [-groupA,-groupB]

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

将 ``manifest.group-filter`` 配置选项设为 ``+groupA,+groupB`` （可运行 ``west config manifest.group-filter "+groupA,+groupB"`` 确保这一点）。

此时，配置值覆盖清单文件对这两个组的设置，因此 ``groupA`` 和 ``groupB`` 均启用。

因此，项目 ``foo`` 和 ``bar`` 均为活动状态。

示例 7：通过配置禁用多个组
--------------------------

完整清单文件如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         groups:
           - groupA
       - name: baz
         groups:
           - groupA
           - groupB

     defaults:
       remote: example-remote
     remotes:
       - name: example-remote
         url-base: https://git.example.com

将 ``manifest.group-filter`` 配置选项设为 ``-groupA,-groupB`` （可运行 ``west config manifest.group-filter -- "-groupA,-groupB"`` 确保这一点）。

此时，``groupA`` 和 ``groupB`` 均被禁用。

因此，项目 ``foo`` 和 ``bar`` 均为非活动状态。

.. _west-group-filter-imports:

组过滤器与导入
==============

本节简要介绍 ``manifest: group-filter:`` 值与 :ref:`west-manifest-import` 结合时的行为。完整细节见 :ref:`west-manifest-formal`。

.. warning::

   以下语义适用于 west v0.10.0 及后续版本。West v0.9.x 的语义不同，不建议在 v0.9.x 中结合使用 ``group-filter`` 和 ``import``。

概括而言：

- 如果只导入一份清单，它在 ``group-filter`` 中禁用的组，也会在你的清单中被禁用
- 可以通过清单文件的 ``manifest: group-filter:`` 值、工作区的 ``manifest.group-filter`` 配置选项，或同时使用二者覆盖此设置

以下是一些示例。

示例 1：不覆盖
--------------

使用以下 :file:`parent/west.yml` 清单：

.. code-block:: yaml

   # parent/west.yml:
   manifest:
     projects:
       - name: child
         url: https://git.example.com/child
         import: true
       - name: project-1
         url: https://git.example.com/project-1
         groups:
           - unstable

:file:`child/west.yml` 的内容如下：

.. code-block:: yaml

   # child/west.yml:
   manifest:
     group-filter: [-unstable]
     projects:
       - name: project-2
         url: https://git.example.com/project-2
       - name: project-3
         url: https://git.example.com/project-3
         groups:
           - unstable

解析后的清单中，只有 ``child`` 和 ``project-2`` 为活动项目。

:file:`child/west.yml` 禁用了 ``unstable`` 组，且 :file:`parent/west.yml` 未覆盖该设置。因此，解析后清单的最终 ``group-filter`` 为 ``[-unstable]``。

``project-1`` 和 ``project-3`` 属于 ``unstable`` 组，且不属于其他组，因此为非活动状态。

示例 2：通过清单覆盖导入的 ``group-filter``
-------------------------------------------

使用以下 :file:`parent/west.yml` 清单：

.. code-block:: yaml

   # parent/west.yml:
   manifest:
     group-filter: [+unstable,-optional]
     projects:
       - name: child
         url: https://git.example.com/child
         import: true
       - name: project-1
         url: https://git.example.com/project-1
         groups:
           - unstable

:file:`child/west.yml` 的内容如下：

.. code-block:: yaml

   # child/west.yml:
   manifest:
     group-filter: [-unstable]
     projects:
       - name: project-2
         url: https://git.example.com/project-2
         groups:
           - optional
       - name: project-3
         url: https://git.example.com/project-3
         groups:
           - unstable

只有 ``child``、``project-1`` 和 ``project-3`` 项目为活动状态。

:file:`parent/west.yml` 覆盖了 :file:`child/west.yml` 中的 ``[-unstable]`` 组过滤器，因此 ``unstable`` 组被启用。``project-1`` 和 ``project-3`` 属于 ``unstable`` 组，因此为活动状态。

同一 :file:`parent/west.yml` 文件禁用了 ``optional`` 组，因此 ``project-2`` 为非活动状态。

:file:`parent/west.yml` 指定的最终组过滤器为 ``[+unstable,-optional]``。

示例 3：通过配置覆盖导入的 ``group-filter``
-------------------------------------------

使用以下 :file:`parent/west.yml` 清单：

.. code-block:: yaml

   # parent/west.yml:
   manifest:
     projects:
       - name: child
         url: https://git.example.com/child
         import: true
       - name: project-1
         url: https://git.example.com/project-1
         groups:
           - unstable

:file:`child/west.yml` 的内容如下：

.. code-block:: yaml

   # child/west.yml:
   manifest:
     group-filter: [-unstable]
     projects:
       - name: project-2
         url: https://git.example.com/project-2
         groups:
           - optional
       - name: project-3
         url: https://git.example.com/project-3
         groups:
           - unstable

如果运行：

.. code-block:: shell

   west config manifest.group-filter +unstable,-optional

则只有 ``child``、``project-1`` 和 ``project-3`` 项目为活动状态。

``manifest.group-filter`` 配置选项覆盖了 :file:`child/west.yml` 中的 ``-unstable`` 组过滤器，因此 ``unstable`` 组被启用。``project-1`` 和 ``project-3`` 属于 ``unstable`` 组，因此为活动状态。

同一配置选项禁用了 ``optional`` 组，因此 ``project-2`` 为非活动状态。

:file:`parent/west.yml` 与 ``manifest.group-filter`` 配置选项共同指定的最终组过滤器为 ``[+unstable,-optional]``。

.. _west-manifest-submodules:

项目中的 Git 子模块
*******************

可使用 :ref:`上文 <west-manifest-files>` 简要介绍的 ``submodules`` 键，让 ``west update`` 同时处理项目 Git 仓库中配置的所有 `Git submodules`_。``submodules`` 键可以位于 ``projects`` 内，例如：

.. code-block:: YAML

   manifest:
     projects:
       - name: some-project
         submodules: ...

``submodules`` 键可以是布尔值或映射列表。下面依次介绍。

方式 1：布尔值
==============

这是使用 ``submodules`` 最简单的方式。

如果 ``projects`` 属性 ``submodules`` 为 ``true``，每当 ``west update`` 更新项目本身时，也会递归更新其 Git 子模块。如果为 ``false`` 或未指定，则不起作用。

例如，假设源代码仓库 ``foo`` 含有一些子模块，你希望 ``west update`` 将它们全部保持同步，同时更新同一工作区中名为 ``bar`` 的另一个项目。

可通过以下清单文件实现：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         submodules: true
       - name: bar

此处，``west update`` 会初始化并更新 ``foo`` 中的全部子模块。如果 ``bar`` 有子模块，它们会被忽略，因为 ``bar`` 未设置 ``submodules`` 值。

方式 2：映射列表
================

``submodules`` 键可以是映射列表，每个列表元素对应一个所需子模块。列出的每个子模块都会递归更新。未列出的子模块仍可通过 ``git`` 命令手动跟踪和更新；无论它们是否存在，``west`` 都会完全忽略。

``path`` 键必须与某个子模块相对于所属 west 项目的路径完全一致，该路径可在 ``git submodule status`` 的输出中查看。``name`` 键是可选的，west 目前不使用它，也不会将其传给 ``git submodule`` 命令。``name`` 键曾在 west 0.9.0 中短暂变为必需，但在 0.9.1 中改为可选。

例如，假设源代码仓库 ``foo`` 有许多子模块，你希望 ``west update`` 只同步其中一部分，同时更新同一工作区中名为 ``bar`` 的另一个项目。

可通过以下清单文件实现：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         submodules:
           - path: path/to/foo-first-sub
           - name: foo-second-sub
             path: path/to/foo-second-sub
       - name: bar

此处，``west update`` 只会递归初始化并更新 ``foo`` 中路径为 ``path/to/foo-first-sub`` 和 ``path/to/foo-second-sub`` 的子模块。``bar`` 中的所有子模块仍被忽略。

.. _west-project-userdata:

仓库用户数据
************

West v0.12 及后续版本支持项目中的可选 ``userdata`` 键。

West v0.13 及后续版本支持在 ``manifest: self:`` 节中使用此键。

它供需要用户特定项目元数据的程序使用。除将其按 YAML 解析外，west 本身完全忽略此值。

此键的值可以是任意 YAML。West 解析后，会通过相应 ``west.manifest.Project`` 对象的 ``userdata`` 属性，将其提供给使用 :ref:`west-apis` 的程序。

清单片段示例：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
       - name: bar
         userdata: a-string
       - name: baz
         userdata:
           key: value
     self:
       userdata: blub

Python 用法示例：

.. code-block:: python

   manifest = west.manifest.Manifest.from_file()

   foo, bar, baz = manifest.get_projects(['foo', 'bar', 'baz'])

   foo.userdata # None
   bar.userdata # 'a-string'
   baz.userdata # {'key': 'value'}
   manifest.userdata # 'blub'

.. _west-manifest-import:

清单导入
********

可以使用上文简要介绍的 ``import`` 键，将其他清单文件中的项目纳入 :file:`west.yml`。此键可以是 ``project`` 或 ``self`` 节的属性：

.. code-block:: yaml

   manifest:
     projects:
       - name: some-project
         import: ...
     self:
       import: ...

使用“self: import:”可从包含 :file:`west.yml` 的仓库中加载其他文件。使用“project: ... import:”可加载该项目 Git 历史中定义的其他文件。

West 按以下顺序从各个清单文件解析最终清单：

#. ``self`` 中导入的文件
#. 你的 :file:`west.yml` 文件
#. ``projects`` 中导入的文件

解析期间，west 会忽略其他文件中已定义的项目。例如，:file:`west.yml` 中名为 ``foo`` 的项目，会使 west 忽略从 ``projects`` 列表导入的其他同名 ``foo`` 项目。

``import`` 键可以是布尔值、路径、映射或序列。下面通过示例依次介绍：

- :ref:`布尔值 <west-manifest-import-bool>`

  - :ref:`west-manifest-ex1.1`
  - :ref:`west-manifest-ex1.2`
  - :ref:`west-manifest-ex1.3`

- :ref:`相对路径 <west-manifest-import-path>`

  - :ref:`west-manifest-ex2.1`
  - :ref:`west-manifest-ex2.2`
  - :ref:`west-manifest-ex2.3`

- :ref:`带附加配置的映射 <west-manifest-import-map>`

  - :ref:`west-manifest-ex3.1`
  - :ref:`west-manifest-ex3.2`
  - :ref:`west-manifest-ex3.3`
  - :ref:`west-manifest-ex3.4`

- :ref:`路径和映射的序列 <west-manifest-import-seq>`

  - :ref:`west-manifest-ex4.1`
  - :ref:`west-manifest-ex4.2`

其工作机制的更 :ref:`形式化描述 <west-manifest-formal>` 位于示例之后。

故障排查提示
============

如果使用此功能时对 west 的行为感到困惑，可以尝试 :ref:`解析清单 <west-manifest-resolve>`，查看导入完成后的最终结果。

.. _west-manifest-import-bool:

Option 1: Boolean
=================

这是使用 ``import`` 最简单的方式。

如果 ``projects`` 属性 ``import`` 为 ``true``，west 会从项目根目录的 :file:`west.yml` 导入项目。如果为 ``false`` 或未指定，则不起作用。例如，以下清单会从 ``p1`` Git 仓库的 ``v1.0`` 修订版本导入 :file:`west.yml`：

.. code-block:: yaml

   manifest:
     # ...
     projects:
       - name: p1
         revision: v1.0
         import: true    # Import west.yml from p1's v1.0 git tag
       - name: p2
         import: false   # Nothing is imported from p2.
       - name: p3        # Nothing is imported from p3 either.

在 ``self`` 中将 ``import`` 设为 ``true`` 或 ``false`` 都是错误的，例如：

.. code-block:: yaml

   manifest:
     # ...
     self:
       import: true  # Error

.. _west-manifest-ex1.1:

示例 1.1：基于 Zephyr 发行版的下游
----------------------------------

你有一个希望配合 Zephyr v1.14.1 LTS 使用的源代码仓库，希望通过 west 维护整个环境，又不想修改任何主线仓库。

换言之，需要的 west 工作区如下：

.. code-block:: none

   my-downstream/
   ├── .west/                     # west directory
   ├── zephyr/                    # mainline zephyr repository
   │   └── west.yml               # the v1.14.1 version of this file is imported
   ├── modules/                   # modules from mainline zephyr
   │   ├── hal/
   │   └── [...other directories..]
   ├── [ ... other projects ...]  # other mainline repositories
   └── my-repo/                   # your downstream repository
       ├── west.yml               # main manifest importing zephyr/west.yml v1.14.1
       └── [...other files..]

可使用以下 :file:`my-repo/west.yml` 实现：

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v1.14.1
         import: true

假设 ``my-repo`` 托管在 ``https://git.example.com/my-repo``，就可以按以下方式在计算机上创建工作区：

.. code-block:: console

   west init -m https://git.example.com/my-repo my-downstream
   cd my-downstream
   west update

运行 ``west init`` 后，:file:`my-downstream/my-repo` 会被克隆。

运行 ``west update`` 后，``zephyr`` 仓库 ``v1.14.1`` 修订版本的 :file:`west.yml` 中定义的所有项目，也会克隆到 :file:`my-downstream`。

此时可以按需向 :file:`my-repo` 添加并提交任意代码，包括自己的 Zephyr 应用程序、驱动程序等。参见 :ref:`application`。

.. _west-manifest-ex1.2:

示例 1.2：“滚动发布”的 Zephyr 下游
----------------------------------

这与 :ref:`west-manifest-ex1.1` 类似，只是 zephyr 仓库改用 ``revision: main``：

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: main
         import: true

可以用同样的方式创建工作区：

.. code-block:: console

   west init -m https://git.example.com/my-repo my-downstream
   cd my-downstream
   west update

这次，每次运行 ``west update``，``zephyr`` 仓库的特殊 :ref:`manifest-rev <west-manifest-rev>` 分支都会更新，指向从 https://github.com/zephyrproject-rtos/zephyr 新获取的 ``main`` 分支顶端。

随后会使用新 ``manifest-rev`` 中的 :file:`zephyr/west.yml` 内容，从 Zephyr 导入项目。这样可以跟上 Zephyr 项目的最新变化。代价是运行 ``west update`` 的结果不再可复现，因为每次运行时远程 ``main`` 分支都可能改变。

还必须理解，解析导入时，west 会完全 **忽略工作树中的** :file:`zephyr/west.yml`。从项目导入时，west 始终使用最近一次 ``manifest-rev`` 提交中保存的清单内容。

只有位于清单仓库工作树中的清单，才能直接从文件系统导入。示例见 :ref:`west-manifest-ex2.2`。

.. _west-manifest-ex1.3:

示例 1.3：基于 Zephyr 发行版、带模块分叉的下游
----------------------------------------------

此清单与 :ref:`west-manifest-ex1.1` 类似，但存在以下区别：

- 基于 Zephyr 2.0 的下游
- 包含该版本中 :file:`modules/hal/nordic` :ref:`模块 <modules>` 的下游分叉

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
       - name: my-remote
         url-base: https://git.example.com
     projects:
       - name: hal_nordic         # higher precedence
         remote: my-remote
         revision: my-sha
         path: modules/hal/nordic
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v2.0.0
         import: true             # imported projects have lower precedence

   # subset of zephyr/west.yml contents at v2.0.0:
   manifest:
     defaults:
       remote: zephyrproject-rtos
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
     # ...
     - name: hal_nordic           # lower precedence, values ignored
       path: modules/hal/nordic
       revision: another-sha

使用此清单文件时，名为 ``hal_nordic`` 的项目：

- 从 ``https://git.example.com/hal_nordic`` 克隆，而不是 ``https://github.com/zephyrproject-rtos/hal_nordic``。
- 由 ``west update`` 更新到提交 ``my-sha``，而不是主线提交 ``another-sha``

也就是说，顶层清单定义了 ``hal_nordic`` 这样的项目后，west 会忽略后续解析导入时遇到的其他同名定义。

这也意味着，在 :file:`my-repo/west.yml` 中定义 ``hal_nordic`` 时，必须复制 ``path: modules/hal/nordic`` 值。:file:`zephyr/west.yml` 中的值会被完全忽略。如果实际使用时对此感到困惑，故障排查建议见 :ref:`west-manifest-resolve`。

运行 ``west update`` 时，west 会：

- 更新 zephyr 的 ``manifest-rev``，使其指向 ``v2.0.0`` 标签
- 导入该 ``manifest-rev`` 中的 :file:`zephyr/west.yml`
- 在本地检出除 ``hal_nordic`` 外所有 zephyr 项目的 ``v2.0.0`` 对应修订版本
- 将 ``hal_nordic`` 更新到 ``my-sha``，而不是 ``another-sha``

.. _west-manifest-import-path:

方式 2：相对路径
================

``import`` 值也可以是指向清单文件或清单文件目录的相对路径。该路径相对于 ``import`` 键所在的 ``projects`` 或 ``self`` 仓库根目录。

示例如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: project-1
         revision: v1.0
         import: west.yml
       - name: project-2
         revision: main
         import: p2-manifests
     self:
       import: submanifests

这会导入以下内容：

- ``manifest-rev`` 中的 :file:`project-1/west.yml` 内容；运行 ``west update`` 后，该引用指向标签 ``v1.0``
- 由 ``west update`` 获取的 ``main`` 分支最新提交中，目录树 :file:`project-2/p2-manifests` 下的所有 YAML 文件，按文件名排序
- 清单仓库 :file:`submanifests` 中实际存在于文件系统的 YAML 文件，按文件名排序

注意，``projects`` 导入通过 ``manifest-rev`` 从 Git 获取数据，而 ``self`` 导入从文件系统获取数据。这是因为 west 一如既往地将清单仓库的版本控制交给你管理。

.. _west-manifest-ex2.1:

示例 2.1：基于 Zephyr 发行版、使用显式路径的下游
------------------------------------------------

这是以显式方式编写与 :ref:`west-manifest-ex1.1` 等效的清单。

.. code-block:: yaml

   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v1.14.1
         import: west.yml

``import: west.yml`` 表示使用 ``zephyr`` 项目内的 :file:`west.yml` 文件。此例虽是刻意构造的，但展示了基本思路。

实际使用中，要导入的清单文件不叫 :file:`west.yml` 时，这种方式很有用。

.. _west-manifest-ex2.2:

示例 2.2：包含清单文件目录的下游
--------------------------------

你的 Zephyr 下游有许多附加仓库，多到希望将其拆分到多个清单文件，但仍在一个清单仓库中统一跟踪，如下所示：

.. code-block:: none

   my-repo/
   ├── submanifests
   │   ├── 01-libraries.yml
   │   ├── 02-vendor-hals.yml
   │   └── 03-applications.yml
   └── west.yml

除 :file:`zephyr/west.yml` 中的项目外，还希望把 :file:`my-repo/submanifests` 中的全部文件加入主清单 :file:`my-repo/west.yml`。同时，希望跟踪 Zephyr 仓库 ``main`` 分支的最新开发代码，而不使用固定修订版本。

实现方式如下：

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: main
         import: true
     self:
       import: submanifests

解析时按以下顺序导入清单文件：

#. :file:`my-repo/submanifests/01-libraries.yml`
#. :file:`my-repo/submanifests/02-vendor-hals.yml`
#. :file:`my-repo/submanifests/03-applications.yml`
#. :file:`my-repo/west.yml`
#. :file:`zephyr/west.yml`

.. note::

   本例中，:file:`.yml` 文件名加上数字前缀，以确保按指定顺序导入。

   可以自由选择名称。West 导入目录内文件前，会先按名称排序。

注意，:file:`submanifests` 中的清单在 :file:`my-repo/west.yml` 和 :file:`zephyr/west.yml` *之前* 导入。一般而言，``self`` 节中的 ``import`` 会先于 ``projects`` 中的清单文件和主清单文件处理。

这意味着 :file:`my-repo/submanifests` 中定义的项目优先级最高。例如，若 :file:`01-libraries.yml` 定义了 ``hal_nordic``，:file:`zephyr/west.yml` 中的同名项目就会被直接忽略。故障排查建议仍可参见 :ref:`west-manifest-resolve`。

这可能看起来有些奇怪，但它允许“事后”重新定义项目，下一个示例会展示这一点。

.. _west-manifest-ex2.3:

示例 2.3：持续集成覆盖
----------------------

持续集成系统需要从开发者的分叉仓库，而不是主线开发仓库，获取并测试 west 工作区中的多个仓库，以检查这些改动能否协同工作。

以 :ref:`west-manifest-ex2.2` 为起点，CI 脚本在 :file:`my-repo/submanifests` 中添加文件 :file:`00-ci.yml`，内容如下：

.. code-block:: yaml

   # my-repo/submanifests/00-ci.yml:
   manifest:
     projects:
       - name: a-vendor-hal
         url: https://github.com/a-developer/hal
         revision: a-pull-request-branch
       - name: an-application
         url: https://github.com/a-developer/application
         revision: another-pull-request-branch

CI 脚本在 :file:`my-repo/submanifests` 中生成此文件后运行 ``west update``。:file:`00-ci.yml` 中定义的项目比 :file:`my-repo/submanifests` 中其他定义优先，因为 :file:`00-ci.yml` 的名称排在其他文件名之前。

因此，即使别处也定义了同名项目，``west update`` 仍会始终在 ``a-vendor-hal`` 和 ``an-application`` 项目中检出开发者的分支。

.. _west-manifest-import-map:

方式 3：映射
============

``import`` 键还可以包含具有以下键的映射：

- ``file``：可选。要导入的清单文件或目录名称。未指定时默认为 :file:`west.yml`。
- ``name-allowlist``：可选。指定一个要包含的项目名称，或项目名称序列。
- ``path-allowlist``：可选。指定一个要匹配的项目路径，或路径序列。它采用 shell 风格的通配模式，目前通过 `pathlib`_ 实现。请注意，这意味着是否区分大小写取决于平台。
- ``name-blocklist``：可选。类似 ``name-allowlist``，但包含要排除而不是纳入的项目名称。
- ``path-blocklist``：可选。类似 ``path-allowlist``，但包含要排除而不是纳入的项目路径。
- ``path-prefix``：可选（v0.8.0 新增）。如果指定，会将其加在项目及所有导入项目的工作区路径前面，可用于将这些项目放入工作区子目录。

.. _re: https://docs.python.org/3/library/re.html
.. _pathlib:
   https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.match

同时指定时，允许列表优先于阻止列表。例如，项目即使按路径被阻止，只要按名称被允许，仍会被导入。

.. _west-manifest-ex3.1:

示例 3.1：使用名称允许列表的下游
--------------------------------

以下是一对分别代表主线和下游的清单文件。但下游不希望使用全部主线项目。假定主线 :file:`west.yml` 托管在 ``https://git.example.com/mainline/manifest``。

.. code-block:: yaml

   # mainline west.yml:
   manifest:
     projects:
       - name: mainline-app                # included
         path: examples/app
         url: https://git.example.com/mainline/app
       - name: lib
         path: libraries/lib
         url: https://git.example.com/mainline/lib
       - name: lib2                        # included
         path: libraries/lib2
         url: https://git.example.com/mainline/lib2

   # downstream west.yml:
   manifest:
     projects:
       - name: mainline
         url: https://git.example.com/mainline/manifest
         import:
           name-allowlist:
             - mainline-app
             - lib2
       - name: downstream-app
         url: https://git.example.com/downstream/app
       - name: lib3
         path: libraries/lib3
         url: https://git.example.com/downstream/lib3

等效的单文件清单如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: mainline
         url: https://git.example.com/mainline/manifest
       - name: downstream-app
         url: https://git.example.com/downstream/app
       - name: lib3
         path: libraries/lib3
         url: https://git.example.com/downstream/lib3
       - name: mainline-app                   # imported
         path: examples/app
         url: https://git.example.com/mainline/app
       - name: lib2                           # imported
         path: libraries/lib2
         url: https://git.example.com/mainline/lib2

如果未使用允许列表，主线清单中的 ``lib`` 项目也会被导入。

.. _west-manifest-ex3.2:

示例 3.2：使用路径允许列表的下游
--------------------------------

以下示例展示如何使用 ``path-allowlist``，仅允许导入主线中的库。

.. code-block:: yaml

   # mainline west.yml:
   manifest:
     projects:
       - name: app
         path: examples/app
         url: https://git.example.com/mainline/app
       - name: lib
         path: libraries/lib                  # included
         url: https://git.example.com/mainline/lib
       - name: lib2
         path: libraries/lib2                 # included
         url: https://git.example.com/mainline/lib2

   # downstream west.yml:
   manifest:
     projects:
       - name: mainline
         url: https://git.example.com/mainline/manifest
         import:
           path-allowlist: libraries/*
       - name: app
         url: https://git.example.com/downstream/app
       - name: lib3
         path: libraries/lib3
         url: https://git.example.com/downstream/lib3

等效的单文件清单如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: lib                          # imported
         path: libraries/lib
         url: https://git.example.com/mainline/lib
       - name: lib2                         # imported
         path: libraries/lib2
         url: https://git.example.com/mainline/lib2
       - name: mainline
         url: https://git.example.com/mainline/manifest
       - name: app
         url: https://git.example.com/downstream/app
       - name: lib3
         path: libraries/lib3
         url: https://git.example.com/downstream/lib3

.. _west-manifest-ex3.3:

示例 3.3：使用路径阻止列表的下游
--------------------------------

以下示例展示如何通过工作区中共同的路径前缀阻止所有主线厂商 HAL，再为目标芯片添加自己的版本，同时保留其余所有项目。

.. code-block:: yaml

   # mainline west.yml:
   manifest:
     defaults:
       remote: mainline
     remotes:
       - name: mainline
         url-base: https://git.example.com/mainline
     projects:
       - name: app
       - name: lib
         path: libraries/lib
       - name: lib2
         path: libraries/lib2
       - name: hal_foo
         path: modules/hals/foo     # excluded
       - name: hal_bar
         path: modules/hals/bar     # excluded
       - name: hal_baz
         path: modules/hals/baz     # excluded

   # downstream west.yml:
   manifest:
     projects:
       - name: mainline
         url: https://git.example.com/mainline/manifest
         import:
           path-blocklist: modules/hals/*
       - name: hal_foo
         path: modules/hals/foo
         url: https://git.example.com/downstream/hal_foo

等效的单文件清单如下：

.. code-block:: yaml

   manifest:
     defaults:
       remote: mainline
     remotes:
       - name: mainline
         url-base: https://git.example.com/mainline
     projects:
       - name: app                  # imported
       - name: lib                  # imported
         path: libraries/lib
       - name: lib2                 # imported
         path: libraries/lib2
       - name: mainline
         repo-path: https://git.example.com/mainline/manifest
       - name: hal_foo
         path: modules/hals/foo
         url: https://git.example.com/downstream/hal_foo

.. _west-manifest-ex3.4:

示例 3.4：导入到子目录
----------------------

你希望导入一份清单及其项目，并将所有内容放入 :term:`west workspace` 的子目录。

例如，假设希望从项目 ``foo`` 导入以下清单，将该项目及其项目 ``bar`` 和 ``baz`` 加入工作区：

.. code-block:: yaml

   # foo/west.yml:
   manifest:
     defaults:
       remote: example
     remotes:
       - name: example
         url-base: https://git.example.com
     projects:
       - name: bar
       - name: baz

你希望将这三个项目仓库都放入 :file:`external-code` 子目录，而不是工作区顶层，如下所示：

.. code-block:: none

   workspace/
   └── external-code/
       ├── foo/
       ├── bar/
       └── baz/

可通过以下清单实现：

.. code-block:: yaml

   manifest:
     projects:
       - name: foo
         url: https://git.example.com/foo
         import:
           path-prefix: external-code

等效的单文件清单如下：

.. code-block:: yaml

   # foo/west.yml:
   manifest:
     defaults:
       remote: example
     remotes:
       - name: example
         url-base: https://git.example.com
     projects:
       - name: foo
         path: external-code/foo
       - name: bar
         path: external-code/bar
       - name: baz
         path: external-code/baz

.. _west-manifest-import-seq:

方式 4：序列
============

``import`` 键还可以包含由文件、目录和映射组成的序列。

.. _west-manifest-ex4.1:

示例 4.1：使用清单文件序列的下游
--------------------------------

此示例通过显式命名文件的序列，实现与 :ref:`west-manifest-ex2.2` 等效的清单。

.. code-block:: yaml

   # my-repo/west.yml:
   manifest:
     projects:
       - name: zephyr
         url: https://github.com/zephyrproject-rtos/zephyr
         import: west.yml
     self:
       import:
         - submanifests/01-libraries.yml
         - submanifests/02-vendor-hals.yml
         - submanifests/03-applications.yml

.. _west-manifest-ex4.2:

示例 4.2：导入顺序说明
----------------------

以下更复杂的示例展示 west 导入清单文件的顺序：

.. code-block:: yaml

   # my-repo/west.yml
   manifest:
     # ...
     projects:
       - name: my-library
       - name: my-app
       - name: zephyr
         import: true
       - name: another-manifest-repo
         import: submanifests
     self:
       import:
         - submanifests/libraries.yml
         - submanifests/vendor-hals.yml
         - submanifests/applications.yml
     defaults:
       remote: my-remote

对于此示例，west 按以下顺序解析导入：

#. 首先是 :file:`my-repo/submanifests` 中列出的文件，按出现顺序处理（例如，由于这是文件序列，:file:`libraries.yml` 先于 :file:`applications.yml`），因为 ``self: import:`` 总是最先导入
#. 然后是 :file:`my-repo/west.yml` （包含 ``my-library`` 等项目，前提是 :file:`submanifests` 中尚未定义它们）
#. 随后是 :file:`zephyr/west.yml`，因为它是 :file:`my-repo/west.yml` 的 ``projects`` 列表中的第一个 ``import`` 键
#. 最后是 :file:`another-manifest-repo/submanifests` 中的文件（按文件名排序），因为它是最后一个项目 ``import``

.. _west-manifest-formal:

清单导入细节
============

本节以更形式化的方式，描述 west 如何解析使用 ``import`` 的清单文件。

概述
----

``import`` 键可以出现在 west 清单的 ``projects`` 和 ``self`` 节中。一般形式如下：

.. code-block:: yaml

   # Top-level manifest file.
   manifest:
     projects:
       - name: foo
         import:
           ... # import-1
       - name: bar
         import:
           ... # import-2
       # ...
       - name: baz
         import:
           ... # import-N
     self:
       import:
         ... # self-import

导入键是可选的。如果 ``import-1, ..., import-N`` 中任意项缺失，west 就不从相应项目导入额外清单数据。如果缺少 ``self-import``，则除顶层文件外，不再导入清单仓库中的其他文件。

解析清单导入最终得到：

- ``projects`` 列表，由顶层文件与导入文件定义的 ``projects`` 合并而成

- 一组扩展命令，取自顶层文件和所有导入文件中的 ``west-commands`` 键

- ``group-filter`` 列表，由顶层和所有导入的过滤器合并而成

导入按以下顺序进行：

#. 先导入 ``self-import`` 指定的清单。
#. 然后处理顶层清单文件的定义。
#. 再依次导入 ``import-1``、……、``import-N`` 指定的清单。

当单个 ``import`` 键引用多个清单文件时，按以下顺序处理：

- 如果值是指向目录的相对路径（或 ``file`` 为目录的映射），其中的清单文件按字典序处理，即按文件名排序。
- 如果值是序列，则按元素出现的顺序递归导入。

必要时，此过程会递归执行。例如，如果 ``import-1`` 产生的清单文件包含 ``import`` 键，会先按相同规则递归解析，再继续处理其内容。

以下各节介绍这些结果。

Projects
--------

本节介绍最终 ``projects`` 列表的生成方式。

项目通过名称识别。如果同名项目出现在多份清单中，采用首个定义，忽略后续定义。例如，``import-1`` 中名为 ``bar`` 的项目会被忽略，因为顶层 :file:`west.yml` 已经定义了同名项目。

``import-1`` 到 ``import-N`` 指定文件的内容，从各项目最新 ``manifest-rev`` 修订版本的 Git 数据中导入。运行 ``west update`` 可将这些版本分别更新到 ``rev-1`` 至 ``rev-N``。如果某个 ``manifest-rev`` 引用缺失或过时，``west update`` 还会从远程获取 URL 获取项目数据并更新该引用。

还请注意，从根清单到定义项目 ``P`` 的仓库，所有导入清单都必须更新，west 才能更新 ``P`` 本身。例如，若 :file:`baz/west.yml` 定义了 ``P``，``west update P`` 就需要同时更新 ``baz`` 项目的 ``manifest-rev`` 和 ``P`` 的本地 Git 克隆中的 ``manifest-rev`` 分支。令人困惑的是，更新 ``baz`` 可能使 ``P`` 从 :file:`baz/west.yml` 中消失，此时 ``west update P`` “应当”因无法识别项目而失败！

因此，如果 ``P`` 定义在导入清单中，就不能运行 ``west update P``；必须通过不带项目参数的 ``west update``，将其与其他所有项目一起更新。

默认情况下，如果项目修订版本是本地已有的 SHA 或标签，west 不会通过网络获取该项目数据，因此除非确有需要，更新额外项目不应花费太多时间。更多信息见 :ref:`update.fetch <west-config-index>` 配置选项文档。

扩展
----

处理导入时发现的所有通过 ``west-commands`` 键定义的扩展命令，均可在解析后的清单中使用。

如果导入清单文件的 ``self:`` 节含有 ``west-commands:`` 定义，其中的扩展命令会在导入该清单时加入可用扩展集合。因此，它们优先于之后添加的所有同名扩展命令。

组过滤器
--------

解析后的清单具有 ``group-filter`` 值，由顶层清单和所有导入清单中的 ``group-filter`` 值连接而成。

导入顺序越靠前的清单文件优先级越高，因此在最终 ``group-filter`` 中越靠后连接。

换言之，设：

- 由 ``self-import`` 解析得到的子清单具有组过滤器 ``self-filter``
- 顶层清单文件具有组过滤器 ``top-filter``
- 从 ``import-1`` 至 ``import-N`` 解析得到的子清单，分别具有组过滤器 ``filter-1`` 至 ``filter-N``

则最终解析后的 ``group-filter`` 值为 ``filterN + ... + filter-2 + filter-1 + top-filter + self-filter``，其中 ``+`` 表示列表连接。

.. important::

   过滤器在上述列表中的顺序很重要。

   最终连接列表中，某个组的最后一个过滤器元素“胜出”，决定该组启用还是禁用。

例如，在 ``[-foo] + [+foo]`` 中，组 ``foo`` 被 *启用*；但在 ``[+foo] + [-foo]`` 中，组 ``foo`` 被 *禁用*。

为简明起见，west 和本文档可能按上述规则省略连接后冗余的组过滤器元素。例如，根据上述原因，``[+foo] + [-foo]`` 可以简写为 ``[-foo]``。又如，由于所有组默认启用，``[-foo] + [+foo]`` 可简写为空列表 ``[]``。

.. _west-manifest-cmd:

清单命令
********

``west manifest`` 命令用于操作清单文件，接受一个操作及其专用参数。

以下各节介绍每种操作，并提供简单用法的基本命令形式。所有选项的完整说明可运行 ``west manifest --help`` 查看。

.. _west-manifest-resolve:

解析清单
========

``--resolve`` 操作输出一份清单文件，等效于当前清单及其全部 :ref:`导入清单 <west-manifest-import>`：

.. code-block:: none

   west manifest --resolve [-o outfile]

此操作主要用于查看执行全部 ``import`` 后的“最终”清单内容。

要打印每个导入清单文件及解析期间项目处理方式的详细信息，使用 ``-v`` 设置最高详细程度：

.. code-block:: console

   west -v manifest --resolve

冻结清单
========

``--freeze`` 操作输出冻结清单：

.. code-block:: none

   west manifest --freeze [-o outfile]

“冻结”清单是每个项目修订版本均为 SHA 的清单文件。使用 ``--freeze`` 可生成与当前清单等效的冻结清单。``-o`` 选项指定输出文件；未指定时使用标准输出。

验证清单
========

``--validate`` 操作在当前清单文件有效时成功，否则失败并报错：

.. code-block:: none

   west manifest --validate

错误消息可以帮助诊断问题。

这里的“无效”是指清单文件语法不符合本页所述规则。

如果清单有效，但行为不符合预期，可以通过 ``-v`` 提高详细程度，了解 west 对清单作出了哪些决策，以及原因：

.. code-block:: none

   west -v manifest --validate

.. _west-manifest-path:

获取清单路径
============

``--path`` 操作打印顶层清单文件的路径：

.. code-block:: none

   west manifest --path

输出类似 ``/path/to/workspace/west.yml``，路径格式取决于操作系统。
