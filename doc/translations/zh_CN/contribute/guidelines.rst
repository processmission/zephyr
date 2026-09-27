.. SPDX-FileCopyrightText: Copyright The Process Mission

.. _contribute_guidelines:

贡献指南
########

作为一个开源项目，我们欢迎并鼓励社区直接向本项目提交补丁。在我们的协作式开源环境中，提交变更的标准和方法有助于减少活跃的开发社区可能带来的混乱。

本文档介绍如何参与项目讨论、记录缺陷和改进请求，以及如何向项目提交补丁，以便你的补丁能尽快被代码库接受。


前置条件
********

.. _Zephyr Project website: https://zephyrproject.org

作为贡献者，你需要熟悉 Zephyr 项目，了解如何按照 `Zephyr Project website`_ 中的说明配置、安装和使用它，以及如何按照 Zephyr :ref:`getting_started` 中的介绍搭建开发环境。

你应当熟悉 Git 和 CMake 等常见开发工具，以及 GitHub 等平台。

如果你还没有这样做，需要先在 https://github.com 上创建一个（免费的）GitHub 账号，并在开发系统上准备好 Git 工具。

.. note::
   Zephyr 开发工作流支持所有三种主流操作系统（Linux、macOS 和 Windows），但下文部分章节使用的工具仅在 Linux 和 macOS 上可用。在 Windows 上，你无法自行运行这些工具，而需要依赖基于 Github Actions 的持续集成（CI）服务：当你提交拉取请求（PR）时，该服务会在 GitHub 上自动运行。任何失败结果都可以在 PR 讨论列表末尾附近的工作流详情链接中看到。更多信息请参见 `Continuous Integration`_。


.. _licensing_requirements:

许可证
******

许可证对开源项目非常重要，它有助于确保软件始终按照作者期望的条款可用。

.. _Apache 2.0 license:
   https://github.com/zephyrproject-rtos/zephyr/blob/main/LICENSE

.. _GitHub repo: https://github.com/zephyrproject-rtos/zephyr

Zephyr 使用 `Apache 2.0 license`_ （见项目 `GitHub repo`_ 中的 LICENSE 文件），以在开放贡献与允许你随意使用软件之间取得平衡。Apache 2.0 许可证是一种宽松的开源许可证，允许你自由使用、修改、分发和销售包含 Apache 2.0 许可软件的自有产品。（关于这一点的更多信息，可参考 `Why choose Apache 2.0 licensing`_ 和 `Top 10 Apache License Questions Answered`_ 等文章。）

.. _Why choose Apache 2.0 licensing:
   https://www.zephyrproject.org/faqs/#1571346989065-9216c551-f523

.. _Top 10 Apache License Questions Answered:
   https://www.whitesourcesoftware.com/whitesource-blog/top-10-apache-license-questions-answered/

许可证说明了版权所有者赋予你作为开发者的权利。贡献者充分理解并同意这些许可权利非常重要。有时版权所有者并非贡献者本人，例如贡献者代表公司进行工作时就是如此。

使用其他许可证的组件
====================

Zephyr 项目中有一些导入或复用的组件采用了其他许可证，详见 :ref:`Zephyr_Licensing`。

从其他项目向 Zephyr OS 导入使用非 Apache 2.0 许可证的代码，需要结合具体场景充分理解，并经由 Zephyr 管理委员会批准。

通过仔细审查潜在的贡献，并对贡献的代码强制执行 :ref:`DCO`，我们可以确保 Zephyr 社区能够基于 Zephyr 项目开发产品，而不必担心专利或版权问题。

关于导入组件的贡献与审查流程，详见 :ref:`external-contributions`。

.. only:: latex

   .. toctree::
      :maxdepth: 1

      ../LICENSING.rst

.. _copyrights:

版权与许可证声明
================

Zephyr 遵循 SPDX/REUSE 风格的文件头。请在每个文件顶部添加机器可读的版权声明和许可证标识符，以便工具能够识别它们（例如使用 `REUSE tool`_ 的 :ref:`west spdx <west-spdx>`）。

Zephyr 项目遵循 Linux 基金会关于版权声明的 `Community Best Practice`_，因此我们建议使用以下版权声明：

.. code-block:: none

   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors

并在其旁边包含许可证标识符：

.. code-block:: none

   SPDX-License-Identifier: Apache-2.0

实用建议：

- 使用文件原生的注释语法，将这两行放在文件的最顶部。
- 如果你编写了实质性的原创内容，你 *可以* 额外添加一行归属于你自己或你所在组织的信息。

.. _Community Best Practice:
   https://www.linuxfoundation.org/blog/copyright-notices-in-open-source-software-projects/

.. _REUSE tool:
   https://github.com/fsfe/reuse-tool

.. _DCO:

开发者原创证书（DCO）
*********************

为尽最大努力确保满足许可标准，Zephyr 项目要求遵循开发者原创证书（DCO）流程。

DCO 是每位开发者所做的每次贡献都要附带的证明。在贡献的提交信息中（本文档后文有更详细的说明），开发者只需添加 ``Signed-off-by`` 声明，即表示同意 DCO。

当开发者提交补丁时，即承诺其有权按照许可证提交该补丁。DCO 协议内容如下，也可在 https://developercertificate.org/ 查看。

.. code-block:: none

    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the
        best of my knowledge, is covered under an appropriate open
        source license and I have the right under that license to
        submit that work with modifications, whether created in whole
        or in part by me, under the same open source license (unless
        I am permitted to submit under a different license), as
        Indicated in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including
        all personal information I submit with it, including my
        sign-off) is maintained indefinitely and may be redistributed
        consistent with this project or the open source license(s)
        involved.

DCO 签署
========

DCO 中的“sign-off”即每个提交日志信息中的“Signed-off-by:”行。Signed-off-by: 行必须采用以下格式::

   Signed-off-by: Your Name <your.email@example.com>

对于你的提交，请替换：

- 将 ``Your Name`` 替换为你的法定姓名（不允许使用笔名、黑客昵称或团体名称）

- 将 ``your.email@example.com`` 替换为你用于撰写提交的真实电子邮箱地址。不允许使用 ``you-id+your-username@users.noreply.github.com`` 这类化名或匿名邮箱。该邮箱必须与你撰写提交时使用的邮箱一致（如果不一致，CI 将会失败）。

你可以使用 ``git commit -s`` 自动将 Signed-off-by: 行添加到提交正文中。可以参考 zephyr git 历史中的其他提交。有关在 Git 中配置用户名和邮箱的说明，请参见 :ref:`git_setup`。

附加要求：

- 如果你修改的是他人创建的现有提交，你必须添加自己的 Signed-off-by: 行，并且不能删除原有的行。

.. _ai_coding_assistants:

AI 编码助手
***********

本节为在向 Zephyr 项目贡献时使用 AI 工具和助手的贡献者提供指导。

许可与法律要求
==============

所有贡献都必须符合项目的许可要求，并与 Zephyr 的许可证兼容（例如 Apache-2.0，详见 :ref:`licensing_requirements`）。

Signed-off-by 与开发者原创证书
==============================

AI 代理 **不得** 添加 ``Signed-off-by`` 标记。只有人类才能依法证明 :ref:`DCO`。人类提交者负责：

- 审查所有 AI 生成的代码。
- 确保符合许可要求。
- 添加自己的 Signed-off-by 标记以证明 DCO。
- 对贡献承担全部责任。

使用披露与署名
==============

当使用 AI 工具协助撰写贡献内容时，适当的署名有助于追踪 AI 在开发过程中不断变化的角色。贡献内容应包含 ``Assisted-by:`` 标记，格式如下：

.. code-block:: none

   Assisted-by: [Agent Name]:[Model Version] [Tool1] [Tool2]

位置：

- ``[Agent Name]`` 是 AI 工具或框架的名称。
- ``[Model Version]`` 是所使用的具体模型版本。
- ``[Tool1] [Tool2]`` 是可选的专用分析工具。

基本的开发工具（git、gcc、make、编辑器）不应列出。

示例：

.. code-block:: none

   Assisted-by: Claude:claude-opus-4.6 coccinelle

.. _source_tree_v2:

源码树结构
**********

要克隆 Zephyr 项目主仓库，请按照 :ref:`get_the_code` 中的说明操作。

本节介绍主仓库的源码树。除了 Zephyr 内核本身，你还能找到技术文档、示例代码、受支持的开发板配置以及一系列子系统测试的源码。这些内容都可供开发者贡献和改进。

了解 Zephyr 源码树有助于定位与特定 Zephyr 特性相关的代码。

在源码树顶层，有几个重要文件：

:file:`CMakeLists.txt`
    CMake 构建系统的顶层文件，包含构建 Zephyr 所需的大量逻辑。

:file:`Kconfig`
    顶层 Kconfig 文件，它会引用同样位于顶层目录的 :file:`Kconfig.zephyr` 文件。

    详细的 Kconfig 文档请参见 :ref:`the Kconfig section of the manual <kconfig>`。

:file:`west.yml`
    :ref:`west` 清单，列出由 west 命令行工具管理的外部仓库。

Zephyr 源码树还包含以下顶层目录，其中每个目录都可能有一层或多层此处未描述的子目录。

:file:`arch`
    特定架构的内核和片上系统（SoC）代码。每种受支持的架构（例如 x86 和 ARM）都有自己的子目录，其中还包含以下方面的子目录：

    * 特定架构的内核源文件
    * 特定架构的私有 API 内核头文件

:file:`soc`
    SoC 相关的代码和配置文件。

:file:`boards`
    开发板相关的代码和配置文件。

:file:`doc`
    Zephyr 技术文档源文件，以及用于生成 https://docs.zephyrproject.org 网站内容的工具。

:file:`drivers`
    设备驱动代码。

:file:`dts`
    用于描述无法自动发现的开发板特定硬件细节的 :ref:`devicetree <dt-guide>` 源文件。

:file:`include`
    所有公共 API 的头文件，但 :file:`lib` 下定义的 API 除外。

:file:`kernel`
    与架构无关的内核代码。

:file:`lib`
    库代码，包括最小标准 C 库。

:file:`misc`
    不属于任何其他顶层目录的杂项代码。

:file:`samples`
    演示 Zephyr 特性用法的示例应用。

:file:`scripts`
    用于构建和测试 Zephyr 应用的各种程序及其他文件。

:file:`cmake`
    构建 Zephyr 所需的附加构建脚本。

:file:`subsys`
    Zephyr 的子系统，包括：

    * USB 设备栈代码
    * 网络代码，包括蓝牙栈和网络协议栈
    * 文件系统代码
    * 蓝牙主机和控制器

:file:`tests`
    Zephyr 特性的测试代码和基准测试。

:file:`share`
    与架构无关的附加数据。它目前包含 Zephyr 的 CMake 包。

拉取请求与问题
**************

.. _Zephyr Project Issues: https://github.com/zephyrproject-rtos/zephyr/issues

.. _open pull requests: https://github.com/zephyrproject-rtos/zephyr/pulls

.. _Zephyr devel mailing list: https://lists.zephyrproject.org/g/devel

.. _Zephyr Discord Server: https://chat.zephyrproject.org

在开始编写补丁之前，请先在我们的 `Zephyr Project Issues`_ 系统中查询，看看你想要解决的问题是否已有报告。可以在 `Zephyr devel mailing list`_ （或 `Zephyr Discord Server`_）上讨论，了解其他人对你的问题（以及建议的解决方案）的看法。你可能会发现有其他人也遇到过你发现的这个问题，或者对变更或新增内容有类似的想法。请向 `Zephyr devel mailing list`_ 发送邮件，向开发社区介绍并讨论你的想法。

在提交自己的问题之前，先搜索已有或相关的问题始终是个好习惯。当你提交问题（缺陷或特性请求）时，分类团队会对其进行审查和评论，通常在几个工作日内完成。

你可以在 GitHub 上找到所有 `open pull requests`_，并在 Github issues 中打开 `Zephyr Project Issues`_。

.. _git_setup:

Git 设置
********

我们需要知道你是谁以及如何联系你。要将这些信息添加到 Git 安装中，请将 Git 配置变量 ``user.name`` 设置为你的全名，将 ``user.email`` 设置为你的邮箱地址。

例如，如果你的姓名是 ``Zephyr Developer``，邮箱地址是 ``z.developer@example.com``：

.. code-block:: console

   git config --global user.name "Zephyr Developer"
   git config --global user.email "z.developer@example.com"

.. note::
   ``user.name`` 必须是你的全名（至少包含名和姓），而不是笔名或黑客昵称。你在 Git 配置中使用的邮箱地址必须与你签署提交时使用的邮箱地址一致。如果不一致，CI 系统会让你的拉取请求失败。

   如果你打算使用 Github.com 的界面编辑提交，请确保你的 github 个人资料中的 ``email address`` 和 ``name`` 也与 git 配置中使用的值（``user.name`` & ``user.email``）一致。

拉取请求准则
************
在创建新的拉取请求时，请遵循以下准则，以确保符合 Zephyr 标准并便于审查流程。

如果有疑问，建议浏览 Zephyr 仓库中已有的拉取请求。使用搜索过滤器和标签来定位与你所提议的变更类似的 PR。

.. note::
   GitHub 默认的代码界面使用 4 字符制表符。然而，Zephyr 遵循 `Linux kernel coding style`_，使用 8 字符制表符。

   为确保你看到的代码与其他开发者一致，请转到你的 `user preferences on GitHub`_，将制表符宽度改为 8 个空格。

.. _Linux kernel coding style:
   https://kernel.org/doc/html/latest/process/coding-style.html#indentation

.. _user preferences on GitHub:
   https://github.com/settings/appearance

.. _commit-guidelines:

提交信息准则
============

变更以 Git 提交的形式提交。每个提交都有一段描述该变更的 *提交信息*。可接受的提交信息如下所示：

.. code-block:: none

   [area]: [summary of change]

   [Commit message body (must be non-empty)]

   Signed-off-by: [Your Full Name] <[your.email@address]>

你需要将上面方括号中的内容（``[like this]``）修改为适合你提交的内容。

以下是一个良好提交信息的示例。

.. code-block:: none

   drivers: sensor: abcd1234: fix bus I/O error handling

   The abcd1234 sensor driver is failing to check the flags field in
   the response packet from the device which signals that an error
   occurred. This can lead to reading invalid data from the response
   buffer. Fix it by checking the flag and adding an error path.

   Signed-off-by: Zephyr Developer <z.developer@example.com>

[area]: [summary of change]
---------------------------

这一行称为提交的 *标题*。标题必须满足：

* 只有一行
* 长度小于 72 个字符
* 后面紧跟一个完全空白的行

[area]
  ``[area]`` 前缀通常标识被修改的代码领域。如果涉及多个领域，它也可以标识该变更更广泛的上下文。

  以下是一些示例：

  * ``doc: ...`` 用于文档变更
  * ``drivers: foo:`` 用于 ``foo`` 驱动变更
  * ``Bluetooth: Shell:`` 用于蓝牙 shell 的变更
  * ``net: ethernet:`` 用于以太网相关的网络变更
  * ``dts:`` 用于全树范围的 devicetree 变更
  * ``style:`` 用于代码风格变更

  如果你不确定该使用什么前缀，可以尝试运行 ``git log FILE``，其中 ``FILE`` 是你正在修改的文件，并参考修改过同一文件的过往提交。

[summary of change]
  ``[summary of change]`` 部分应简要描述你所做的改动。以下是一些示例：

  * ``doc: update wiki references to new site``
  * ``drivers: sensor: sensor_shell: fix channel name collision``

提交信息正文
------------

.. warning::

   提交信息正文不允许为空。即使是微不足道的变更，也请包含描述性的提交信息正文，否则你的拉取请求将无法通过 CI 检查。

提交的这一部分应说明你的变更做了什么以及为什么需要它。请具体一些。只写 ``“Fixes stuff”`` 这样的正文会被拒绝。请务必在相关时包含以下内容：

* 变更 **做了什么**，
* 你 **为什么** 选择该方案，
* 做了 **哪些** 假设，以及
* 你 **如何** 知道它有效——例如运行了哪些测试。

提交信息中的每一行通常应不超过 75 个字符。对于较长的行，请使用换行符折行。例外情况包括包含长 URL、邮箱地址等的行。

关于可接受的提交信息示例，可以参考 Zephyr GitHub 的 `changelog <https://github.com/zephyrproject-rtos/zephyr/commits/main>`__。


Signed-off-by: ...
------------------

.. tip::

   你应当已经完成 :ref:`git_setup`。使用 ``git commit -s`` 创建提交，即可利用这些信息自动添加 Signed-off-by: 行。

出于开源许可方面的原因，你的提交必须包含如下所示的 Signed-off-by: 行：

.. code-block:: none

   Signed-off-by: [Your Full Name] <[your.email@address]>

例如，如果你的全名是 ``Zephyr Developer``，邮箱地址是 ``z.developer@example.com``：

.. code-block:: none

   Signed-off-by: Zephyr Developer <z.developer@example.com>

这意味着你已亲自确认自己的变更符合 :ref:`DCO`。因此，你必须使用法定姓名。不允许使用笔名或“黑客别名”。

你使用的姓名和邮箱地址必须与 Git 提交中 ``Author:`` 字段的姓名和邮箱一致。

关于贡献者和审查者期望的更完整讨论，请参见 :ref:`contributor-expectations`。

添加链接
--------

.. _GitHub references:
   https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls

如果你的变更解决了某个特定的 GitHub 问题，请在拉取请求描述中按以下格式添加引用：

.. code-block:: none

   Fixes zephyrproject-rtos/zephyr#[issue number]

仅对于提交给 Zephyr 项目的拉取请求，也可以使用简写形式，例如：

.. code-block:: none

   Fixes #[issue number]

将 [issue number] 替换为相关的 GitHub 问题编号。例如：

.. code-block:: none

   Fixes zephyrproject-rtos/zephyr#1234

该语法可确保在拉取请求被合并时自动关闭该问题。请始终指定完整的仓库路径（zephyrproject-rtos/zephyr），以避免歧义，尤其是在跨多个仓库工作时。

相同的格式也可以用在提交信息中。

要链接到其他外部资源——例如相关问题、数据手册或技术参考手册——请使用 ``Link:`` 标签：

.. code-block:: none

   Link: https://github.com/zephyrproject-rtos/zephyr/issues/<issue number>

.. _Continuous Integration:

持续集成（CI）
==============

Zephyr 项目运行着一套持续集成（CI）系统，它会在每个拉取请求（PR）上运行，以验证 PR 的多个方面：

* Git 提交格式
* 代码风格
* 针对多种架构和开发板的 Twister 构建
* 用于验证任何文档变更的文档构建

CI 在 Github Actions 上运行，使用的工具与 `CI Tests`_ 一节中描述的相同。CI 结果必须为绿色，即显示“All checks have passed”，拉取请求才能被合并。CI 会在创建 PR 时运行，并在每次通过提交修改 PR 时再次运行。

CI 运行的当前状态始终可以在 GitHub PR 页面底部、审查状态下方找到。根据运行成功或失败，你会看到：

* “All checks have passed
* “All checks have failed

如果失败，你可以点击失败消息下方显示的“Details”链接，跳转到 ``Github Actions`` 并查看结果。点击该链接后，你会进入 ``Github actions`` 的结果摘要页面，其中会显示包含所有不同构建的表格。要查看哪个构建或测试失败，请点击包含失败（即非绿色）构建的行。

.. _CI Tests:

在本地运行 CI 测试
==================

.. _check_compliance_py:

check_compliance.py
-------------------

:zephyr_file:`scripts/ci/check_compliance.py` 脚本是评估代码是否符合 Zephyr 既定准则和最佳实践的有力工具。该脚本封装了一组执行各种检查（包括 linter 和格式化工具）的工具。

我们鼓励开发者在创建新的拉取请求之前在本地运行该脚本，以验证自己的变更：

.. code-block:: bash

   ./scripts/ci/check_compliance.py -c <commit range>

各项检查会并行运行，每个 CPU 使用一个工作进程。传入 ``-p N`` 可将工作进程数限制为 ``N``，或使用 ``-p 1`` 顺序运行各项检查。

.. code-block:: bash

   ./scripts/ci/check_compliance.py -p 1 -c <commit range>

.. note::
   在 Windows 上，如果 .pl 扩展名尚未与某个应用程序关联，那么在未指定解释器的情况下首次运行 .pl 文件时，Windows 会询问使用哪个应用程序打开 Perl 文件。请将默认应用设置为 Strawberry Perl。默认情况下，该可执行文件安装在 ``C:\Strawberry\perl\bin\perl.exe``。

KeepSorted 检查
^^^^^^^^^^^^^^^

KeepSorted 检查确保指定的代码、配置或文档块保持有序。

要使用 KeepSorted 检查，请将需要排序的内容包在包含起始和停止标记的专用行之间，通常使用注释：

.. code-block:: c

   // zephyr-keep-sorted-start
   option_a
   option_b
   option_c
   // zephyr-keep-sorted-stop

KeepSorted 标记选项
"""""""""""""""""""

每个块的排序行为可以通过多种方式定制。为此，可以在起始标记所在的行上添加以下一个或多个参数：

**re(regex_pattern)**
   启用正则表达式模式，只有匹配指定正则表达式的行才会参与排序检查，其他行将被忽略。

   检查 yaml 文件中属性排序的示例：

   .. code-block:: yaml

      # zephyr-keep-sorted-start re(^\s+\- name:)
      projects:
        - name: application
          revision: main
        - name: library1
          revision: feature-branch
        - name: library2
          revision: main
      # zephyr-keep-sorted-stop

**strip(characters)**
   在执行排序比较之前从各行中去掉指定字符。当各行带有在排序时应忽略的可选前缀或后缀时，这很有用。

   从 yaml 字典键中去掉引号的示例：

   .. code-block:: yaml

      # zephyr-keep-sorted-start strip(":)
      ACPI:
        status: odd fixes
      "West project: acpica":
        status: odd fixes
      # zephyr-keep-sorted-stop

**nofold**
   禁用行折叠。默认情况下，主行之后的缩进行会被拼接（折叠）在一起进行排序比较。``nofold`` 选项会禁用该行为并忽略缩进行。

**ignorecase**
   使用 Python 的 `str.casefold`_ 启用不区分大小写的排序。这样可以在已排序的块中混合使用大写和小写项，而不会造成排序顺序违规。如果省略，则使用 Python 的字符串排序。

.. _str.casefold: https://docs.python.org/3/library/stdtypes.html#str.casefold

多个选项可以组合在同一标记行上：

.. code-block:: rst

   .. zephyr-keep-sorted-start re(^\* \w) ignorecase
   * Shell
     Some important message about the shell.

   * STM32
     Updates for this vendor.
   .. zephyr-keep-sorted-stop

twister
-------

.. note::
   twister 仅在 Linux 上得到完全支持；在 Windows 和 MacOS 上，并非所有目标设备都支持执行测试。

如果你认为自己的变更可能会破坏某些测试，可以将 PR 作为草稿提交，让项目 CI 自动为你运行 :ref:`twister_script`。

如果测试失败，你可以从 CI 运行日志中查看如何在本地重新运行它，例如：

.. code-block:: bash

   west twister -p native_sim -s tests/drivers/build_all/sensor/drivers.sensor.generic_test

.. _static_analysis:

静态代码分析
************

Coverity Scan 是一项对开源项目免费提供的静态代码分析服务。它基于 Coverity 的商业产品，能够分析 C、C++ 和 Java 代码。

Coverity 的静态代码分析并不运行代码，而是使用抽象解释来获取有关代码控制流和数据流的信息。它能够跟踪程序可能经过的所有代码路径。例如，分析器知道 malloc() 返回的内存之后必须用 free() 释放。它会跟踪所有分支和函数调用，以检查所有可能的组合是否都释放了内存。该分析器能够检测各种问题，例如资源泄漏（内存、文件描述符）、NULL 解引用、释放后使用、未检查的返回值、死代码、缓冲区溢出、整数溢出、未初始化变量等等。

分析结果可在 `Coverity Scan <https://scan.coverity.com/projects/zephyr>`_ 网站上查看。要访问这些结果，你必须自行创建账号。在 Zephyr 项目页面上，你可以选择“Add me to project”来加入该项目。新成员必须经过管理员批准。

对 Zephyr 代码库的静态分析每两周进行一次。静态分析工具检测到的任何问题都会自动创建 GitHub 问题。这些问题最初会具有与工具中定义相同（或等效）的优先级。

为确保责任明确并高效解决问题，这些问题会被分配给负责受影响代码的相应维护者。

一个由具备静态分析、代码质量和软件安全专业知识的成员组成的专门团队负责确保静态分析流程的有效性，并核实发现的问题得到妥善分类和及时解决。

工作流
======

如果分析 Coverity 报告后得出结论认为它是误报，请将分类设置为“False positive”或“Intentional”，将操作设置为“Ignore”，将负责人设置为你自己的账号，并添加注释说明为何该问题被认为是误报或有意的。

在 zephyr 项目中更新相关 Github 问题并附上详细信息，并在扫描服务网站上完成上述步骤后才关闭该问题。任何在未修复、也未在扫描服务中忽略该条目的情况下关闭的问题，如果该问题在代码中依然存在，都会被自动重新打开。

.. _Contribution workflow:

贡献工作流
**********

我们鼓励的一个通用做法是进行小而可控的变更。这种做法可以简化审查、使合并和 rebase 更容易，并保持变更历史清晰明了。

在向 Zephyr 项目贡献时，同样重要的是尽可能提供关于你的变更的信息、更新相应的文档，并在提交前充分测试你的变更。

Zephyr 开发者使用的通用 GitHub 工作流结合了命令行 Git 命令和与 GitHub 的浏览器交互。与 Git 一样，完成任务有多种方式。这里我们描述一个典型的工作流：

.. _Create a Fork of Zephyr:
   https://github.com/zephyrproject-rtos/zephyr#fork-destination-box

#. 将 `Create a Fork of Zephyr`_ 创建到你在 GitHub 上的个人账号中。（点击 GitHub 中 Zephyr 项目仓库页面右上角的 fork 按钮。）

#. 在你的开发计算机上，进入你 :ref:`获取代码 <get_the_code>` 时创建的 :file:`zephyr` 文件夹::

     cd zephyrproject/zephyr

   将指向 `upstream repository <https://github.com/zephyrproject-rtos/zephyr>`_ 的默认远端从 ``origin`` 重命名为 ``upstream``::

     git remote rename origin upstream

   让 Git 知道你刚创建的 fork，并将其命名为 ``origin``::

     git remote add origin https://github.com/<your github id>/zephyr

   然后验证远端仓库::

     git remote -v

   输出应类似如下::

     origin   https://github.com/<your github id>/zephyr (fetch)
     origin   https://github.com/<your github id>/zephyr (push)
     upstream https://github.com/zephyrproject-rtos/zephyr (fetch)
     upstream https://github.com/zephyrproject-rtos/zephyr (push)

#. 为你的工作创建一个主题分支（基于 ``main``）（如果你要解决某个问题，建议在分支名中包含问题编号）::

     git switch main
     git switch -c fix_comment_typo

   一些 Zephyr 子系统在与 ``main`` 不同的分支上进行开发工作，因此你可能需要在检出时指明这一点::

     git switch -c fix_out_of_date_patch origin/net

#. 修改、在本地测试、再修改、再测试、再测试……（也请查看前面关于 `twister`_ 的章节）。

#. 当一切看起来没问题时，通过添加已修改的文件来开始拉取请求流程::

     git add [file(s) that changed, add -p if you want to be more specific]

   可以使用以下命令查看尚未暂存的文件::

     git status

#. 验证将要提交的变更是否符合你的预期::

     git diff --cached

#. 将你的变更提交到本地仓库::

     git commit -s

   ``-s`` 选项会自动将你的 ``Signed-off-by:`` 添加到提交信息中。如果没有这一行表明你同意 :ref:`DCO`，你的提交会被拒绝。有关编写提交信息的具体准则，请参见 :ref:`commit-guidelines` 一节。

#. 将包含变更的主题分支推送到你个人 GitHub 账号中的 fork::

     git push origin fix_comment_typo

#. 在浏览器中打开你的 fork 仓库，并为你刚刚处理、想要提交拉取请求的分支点击 ``Compare & pull request`` 按钮。

#. 检查拉取请求中的变更，并确认你是在为 ``main`` 分支创建拉取请求。提交信息中的标题和内容也应一并显示出来。

#. 机器人会（根据仓库中的 MAINTAINERS 文件）分配一个或多个建议的审查者。如果你是项目成员，现在还可以选择其他审查者。

#. 点击提交按钮，你的拉取请求就会被发送并等待审查。有审查评论时你会收到邮件，你也可以在 https://github.com/zephyrproject-rtos/zephyr/pulls 上查看你的拉取请求。

#. 在等待拉取请求被接受和合并期间，你可以创建另一个分支来处理其他问题。（请确保新分支基于 ``main``，而不是之前的分支。）::

     git switch main
     git switch -c fix_another_issue

   然后使用上述相同的流程来处理这个新的主题分支。

#. 如果审查者确实要求修改你的补丁，你可以通过交互式 rebase 提交来修正审查中发现的问题。在你的开发仓库中::

     git rebase -i <offending-commit-id>^

   在交互式 rebase 编辑器中，将 ``pick`` 替换为 ``edit`` 以选择特定的提交（如果你的拉取请求中有多个提交），或者删除该行以完全删除某个提交。然后编辑文件以修正审查中发现的问题。

   与之前一样，检查并测试你的变更。准备好后，继续提交补丁::

     git add [file(s)]
     git rebase --continue

   如有需要，更新提交注释，然后继续::

     git push --force origin fix_comment_typo

   通过强制推送你的更新，原有的拉取请求会随之更新，因此你无需重新提交拉取请求。

#. 推送所要求的变更后，请在 PR 页面上检查是否存在合并冲突。如果有，请对本地分支执行 rebase::

      git fetch --all
      git rebase --ignore-whitespace upstream/main

   ``--ignore-whitespace`` 选项会阻止 ``git apply`` （由 rebase 调用）改动任何空白字符。解决冲突后再次推送::

      git push --force origin fix_comment_typo

   .. note:: 虽然修改提交并强制推送是 GitHub 之外常见的审查模式，也是 Zephyr 推荐的方式，但它并不是 GitHub 主要支持的模式。强制推送可能导致意外行为，例如除了最后一个之外无法使用“View Changes”按钮——GitHub 会报错说找不到更早的提交。你也不总能将最新审查的版本与最新提交的版本进行比较。重写历史时，GitHub 只保证能访问最新的版本。

#. 如果 CI 运行失败，你需要修改代码以修正问题，并按上述方式通过 rebase 修订提交。关于 CI 系统的更多信息，请参见 `Continuous Integration`_。

.. _contribution_tips:

贡献技巧
========

以下是一些改进并加速拉取请求审查流程的技巧。如果你遵循这些技巧，你的拉取请求就更有可能获得所需的关注，并能更快地准备好合并：

.. _git-rebase:
   https://git-scm.com/docs/git-rebase#Documentation/git-rebase.txt---keep-base

#. 推送后续变更时，使用 `git-rebase`_ 的 ``--keep-base`` 选项

#. 在 PR 页面上检查该变更是否仍能无合并冲突地合并

#. 确保 PR 标题说明正在修复或新增什么内容

#. 确保你的 PR 有正文，更详细地说明所提交的内容

#. 确保在 PR 正文中引用你正在修复的问题

#. 提交后立即关注早期的 CI 结果，并在发现问题时及时修复

#. 1-2 小时后再查看 PR，了解所有 CI 检查的状态，确保全部为绿色

#. 如果你收到修改请求并提交了相应的变更，请务必在 GitHub 界面上点击“Re-request review”按钮，以通知提出修改请求的人

标明贡献来源
============

向代码树添加新文件时，重要的是在文件中详细说明来源、提供署名信息，并详细说明预期用途。如果该文件是 Zephyr 原创的，提交信息应包含以下内容（如果没有 Origin 标签，则默认为“Original”）::

      Origin: Original

如果该文件是 :ref:`从外部项目导入 <external-contributions>` 的，提交信息应包含有关原始项目、项目位置、该文件来源提交的 SHA-id 以及预期用途的详细信息。

例如，本地维护的导入副本::

      Origin: Contiki OS
      License: BSD 3-Clause
      URL: https://www.contiki-os.org/
      commit: 853207acfdc6549b10eb3e44504b1a75ae1ad63a
      Purpose: Introduction of networking stack.

例如，模块仓库中外部维护的导入副本::

      Origin: Tiny Crypt
      License: BSD 3-Clause
      URL: https://github.com/01org/tinycrypt
      commit: 08ded7f21529c39e5133688ffb93a9d0c94e5c6e
      Purpose: Introduction of TinyCrypt

对外部模块的贡献
****************

贡献 :ref:`新模块 <submitting_new_modules>` 以及向 :ref:`现有模块 <changes_to_existing_module>` 提交变更时，请遵循 :ref:`modules` 一节中的准则。

.. _treewide-changes:

全树范围的变更
**************

本节介绍属于全树范围变更的贡献，以及适用于它们的一些附加要求。由于这类变更影响巨大，这些要求旨在为其提供更多的审查和用户可见性。

定义与决策
==========

*全树范围的变更* 定义为对 Zephyr API、编码实践或其他开发要求的任何变更：它意味着需要对整个 zephyr 源代码仓库进行相应修改，或者可以合理预期会对一大类基于 Zephyr 的外部源代码产生这样的影响。

这个定义必然是非正式的，因为判断某个具体变更是否属于全树范围可能是主观的，并且可能取决于额外的背景信息。

在判断某项提议的变更是否属于全树范围时，项目维护者应做出良好判断，并优先考虑 Zephyr 开发者的体验。长期的分歧可以由 Zephyr 项目的技术指导委员会（TSC）解决，但请避免过早升级到 TSC。

全树范围变更的要求
==================

- zephyr 仓库必须为任何属于全树范围变更的问题或拉取请求添加 'treewide' GitHub 标签

- 提议全树范围变更的人必须先创建一个 `RFC issue <https://github.com/zephyrproject-rtos/zephyr/issues/new?assignees=&labels=RFC&template=003_rfc-proposal.yml>`_，描述该变更、其理由和影响等，然后才能合并与该变更相关的任何拉取请求

- 项目的 `Architecture Working Group (WG) <https://github.com/zephyrproject-rtos/zephyr/wiki/Architecture-Working-Group>`_ 必须将该问题列入议程，并讨论项目是接受还是拒绝该变更，然后才能合并与该变更相关的任何拉取请求（如果在工作组中未达成共识，则升级到 TSC）

- 架构工作组必须为每个全树范围变更指定合并相关 PR 的流程，包括影响特定子系统的拉取请求所需的批准，或额外的审查时间要求

- 如果 RFC 被架构工作组接受，提议全树范围变更的人必须先向 devel@lists.zephyrproject.org 发送关于该 RFC 的邮件，然后才能合并与该变更相关的任何拉取请求

示例
====

过去一些全树范围变更的示例：

- 废弃 :ref:`日志 API <logging_api>` 的版本 1 转而使用版本 2（参见提交 `262cc55609 <https://github.com/zephyrproject-rtos/zephyr/commit/262cc55609b73ea61b5f999c6c6daaba20bc5240>`_）
- 移除对旧式 :ref:`dt-bindings` 语法的支持（`6bf761fc0a <https://github.com/zephyrproject-rtos/zephyr/commit/6bf761fc0a2811b037abec0c963d60b00c452acb>`_）

请注意，在保留对旧版本支持的同时新增广泛使用的 API 的新版本并不属于全树范围的变更。然而，废弃和移除此类 API 属于全树范围的变更。

专用驱动的要求
**************

独立设备的驱动应尽可能使用 Zephyr 总线 API（SPI、I2C……），这样该设备就能用于任何厂商实现了兼容总线的任何 SoC。

如果由于特定 SoC 系列中的专用加速器，在技术上无法使用 Zephyr API 达到完整性能，可以为该 SoC 系列提供一条专用路径，从而扩展对外部设备的支持。但是，驱动仍必须为所有其他 SoC 提供常规路径（通过 Zephyr API）。每一个例外都必须经架构工作组批准，以便进行验证并有可能从中学习或改进。
