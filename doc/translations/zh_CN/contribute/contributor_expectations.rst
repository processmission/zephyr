.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _contributor-expectations:

贡献者期望
##########

Zephyr 项目鼓励 :ref:`贡献者 <contributor>` 以较小的拉取请求提交变更。较小的拉取请求（PR）具有以下好处：

- 审查更快、更彻底。对审查者来说，抽出几分钟多次审查较小的变更，比分配大块时间来审查一个大型 PR 更容易。

- 如果审查者或维护者否决了变更的方向，浪费的工作更少。

- 更容易 rebase 和合并。较小的 PR 不太可能与代码树中的其他变更发生冲突。

- 如果 PR 破坏了功能，也更容易回退。

.. note::
  本页不适用于草稿 PR；草稿 PR 可以是任意大小、包含任意数量的提交，也可以出于测试和预览目的组合多个较小的 PR。草稿 PR 没有审查期望，并且从一开始就作为草稿创建的 PR 默认不会通知任何人。


较小 PR 的定义
**************

- 较小的 PR 应包含一个自包含的逻辑变更。

- 在添加大型新特性或 API 时，PR 应只涉及该特性的一部分。在这种情况下，请创建一个 :ref:`RFC 提案 <rfcs>`，向审查者描述该特性的其余部分。

- 在以下情况下，PR 应包含测试或示例：

  - 添加新特性或功能时。

  - 修改特性时，尤其是涉及 API 行为契约变更时。

  - 修复与硬件无关的缺陷时。该测试在缺陷未修复时应失败，在应用修复后应通过。

- PR 必须更新受功能性代码变更影响的任何文档。

- 如果引入新的 API，PR 必须包含该 API 的用法示例。这为审查者提供了上下文，并避免提交包含未使用 API 的 PR。


单个 PR 中的多个提交
********************

我们进一步鼓励贡献者将 PR 拆分为多个提交。请记住，PR 中的每个提交仍必须能干净地构建并通过所有 CI 测试。

例如，在引入某个 API 的扩展时，贡献者可以将 PR 拆分为针对以下具体变更的多个提交：

#. 引入新的 API，包括共享的 devicetree binding
#. 更新驱动实现 X，并包含驱动特定的 devicetree binding
#. 更新驱动实现 Y
#. 为新 API 添加测试
#. 添加使用该 API 的示例
#. 更新文档

大型变更
********

对 Zephyr 项目的大型变更必须提交 :ref:`RFC 提案 <rfcs>`，描述变更的完整范围和后续工作。RFC 提案为审查者提供了必要的上下文，同时允许以更小的增量 PR 被审查并合并到项目中。RFC 还应定义最小可行实现。

需要 RFC 提案的变更包括：

- 提交新特性。
- 提交新 API。
- :ref:`全树范围的变更 <treewide-changes>`。
- 其他可以从 RFC 提案流程中受益的大型变更。

维护者有权自行决定要求贡献者为过大或过于复杂的 PR 创建 RFC。

.. _pr_requirements:

PR 要求
*******

.. important::

   不符合下文所述质量期望的拉取请求不太可能得到审查者的参与，审查者可能会对这类拉取请求提出修改要求，但不提供详细反馈。

   贡献者应先自行审查自己的变更，并确保满足所有要求，然后再请求审查。

- PR 中的每个提交都必须提供符合 :ref:`提交信息准则 <commit-guidelines>` 的提交信息。

- 不允许使用 fixup 提交或合并提交，更多信息请参见 :ref:`贡献工作流 <Contribution workflow>`。

- PR 描述必须包含变更的摘要及其理由。

- PR 中的所有文件都必须符合 :ref:`许可要求 <licensing_requirements>`。

- 代码必须遵循 Zephyr 的 :ref:`编码风格 <coding_style>` 和 :ref:`编码准则 <coding_guidelines>`。

- PR 必须通过所有 CI 检查，如 :ref:`合并标准 <merge_criteria>` 所述。即使 CI 检查失败，贡献者也可以将 PR 标记为草稿，并明确请求审查者提供早期反馈。

- 拉取请求中的提交应代表清晰、逻辑明确的变更单元，既便于审查，又能保持可二分性。以下准则对该原则做了进一步说明：

  1. 独立且逻辑明确的变更单元

     每个提交应对应一个自包含且有意义的变更。例如，添加特性、修复缺陷或重构现有代码应是各自独立的提交。避免在同一个提交中混入不同类型的变更（例如特性实现与无关的重构）。

  2. 保持可二分性

     拉取请求中的每个提交都必须成功构建并通过所有相关测试。这可确保能够有效地使用 git bisect 来定位引入缺陷或问题的具体提交。

  3. 压缩（squash）中间或非最终的开发历史

     在开发过程中，提交可能包含中间变更（例如部分实现、临时文件或调试代码）。这些内容应在提交拉取请求之前压缩或重写。请移除以下非最终产物：

     * 临时重命名、之后又被再次重命名的文件。
     * 在后续提交中被重写或大幅修改的代码。

  4. 提交前确保历史干净

     在提交拉取请求之前，使用交互式 rebase（git rebase -i）清理提交历史。这有助于：

     * 将零散的小提交压缩（squash）为一个连贯的提交。
     * 确保每个提交保持可二分。
     * 在提高清晰度的同时保持正确的作者归属。

  5. 重命名与代码重写

     如果在开发过程中文件或代码在后续提交中被重命名或重写，请压缩或重写较早的提交，以反映最终结构。这可确保：

     * 历史保持干净且易于理解。
     * 通过消除冗余的重命名或部分重写来保持可二分性。

  6. 作者归属

     在清理提交历史时，请确保作者归属保持准确。

  7. 可读且可审查的历史

     最终的提交历史应便于未来的维护者理解。逻辑变更单元应归组到能清晰、连贯地讲述所做工作的提交中。

- 添加重要新功能时，应将该新功能的测试添加到自动化测试套件中。所有 API 函数都应有测试用例，并且应有针对 API 行为契约的测试。维护者和审查者有权自行判断所提供的测试是否充分。下面的示例展示了如何有效测试 API 的最佳实践。

    - :zephyr_file:`内核定时器测试 <tests/kernel/timer/timer_behavior>` 为 :zephyr_file:`内核定时器 <kernel/timer.c>` 提供了约 85% 的测试覆盖率（按代码行数计算）。
    - 片外外设的模拟器是测试驱动 API 的有效方式。:zephyr_file:`电量计测试 <tests/drivers/fuel_gauge/sbs_gauge>` 使用了 :zephyr_file:`智能电池模拟器 <drivers/fuel_gauge/sbs_gauge/emul_sbs_gauge.c>`，为 :zephyr_file:`电量计 API <include/zephyr/drivers/fuel_gauge.h>` 和 :zephyr_file:`智能电池驱动 <drivers/fuel_gauge/sbs_gauge/sbs_gauge.c>` 提供了测试覆盖。
    - Zephyr 项目的代码覆盖率报告可在 `Codecov`_ 上查看。

- 对 API 的不兼容变更还必须更新下一版本的版本说明，详细说明该变更。标记为 experimental 的 API 不受此要求约束。

- 对 API 的变更必须按照 API 版本规则递增 API 版本号。

- 必须添加和/或更新文档，以反映 PR 引入的代码变更。文档变更必须使用现有页面中已有的适当术语，并且必须使用美式英语撰写。如果文档中包含图片，则这些图片必须遵循 :ref:`文档图片 <doc_images>` 中的规则。更多信息请参见 :ref:`文档准则 <doc_guidelines>`。

- 在发布工程团队的成员将 PR 合并到 zephyr 代码树之前，PR 还必须满足所有 :ref:`合并标准 <merge_criteria>`。

维护者可以要求贡献者将 PR 拆分为更小的 PR，也可以要求他们创建 :ref:`RFC 提案 <rfcs>`。

.. _`Codecov`: https://app.codecov.io/gh/zephyrproject-rtos/zephyr

有助于审查者的工作流建议
========================

- 除非完全按照审查者的建议进行了修改，否则作者不得自行解决并隐藏评论，而应让最初的审查者来完成。Zephyr 项目不要求合并前解决所有评论。有时保留一些已完成的讨论处于打开状态有助于理解整体情况。

- 在“Files changed”视图中使用“Start Review”和“Add Review”绿色按钮回复评论。这样可以一次回复多条评论并批量发布回复，从而减少发送给审查者的邮件数量。

- 由于 GitHub 未实现 |git range-diff|_，请尽量减少审查过程中的 rebase。如果必须 rebase，请将其作为单独的更新推送，且自上次推送 PR 以来不包含其他变更。仅推送 rebase 时，请在 PR 中添加评论说明哪个提交是 rebase。

.. |git range-diff| replace:: ``git range-diff``
.. _`git range-diff`: https://git-scm.com/docs/git-range-diff

让 PR 得到审查
==============

Zephyr 社区由多元化的个体组成，他们的投入程度和优先级各不相同。因此，审查者和维护者可能不会立即处理某个 PR。

- 如果 1 周没有动静，请在 PR 上添加评论以提醒指派者或审查者。

- 如果 2 周没有动静，请在 Discord 的 `#pr-help`_ 频道发布消息并附上该 PR 的链接。

.. _pr_technical_escalation:

PR 技术升级
===========

如果贡献者对审查者提出的修改请求有异议，Zephyr 定义了以下升级流程来解决技术分歧。

在升级技术分歧之前，请遵循以下步骤：

- 在 PR 中由指派者、维护者和审查者共同解决。

  - 如适用，由指派者担任调解人。

- 如果没有取得进展，指派者（维护者）有权驳回审查者提出的过时、不相关或无关紧要的修改请求，同时至少给审查者 1 个工作日的时间进行回应并重新考虑其最初的修改请求，或启动升级流程。

  指派者有责任在 PR 中记录驳回任何审查的理由，并应通知审查者其审查已被驳回。

  为了给审查者留出回应和升级的时间，指派者应通过不批准该 PR 或设置 *DNM* 标签来阻止 PR 被合并。

参与审查过程的任何一方（指派者、审查者或变更的原始作者）都可以按照以下步骤触发升级：

- 通过在 PR 上添加 ``Architecture Review`` 标签可升级到 `Architecture Working Group`_。除了处理此类升级的每周例会之外，如有要求，`Architecture Working Group`_ 还应协助对升级进行线下审查，尤其是在任何一方无法出席会议时。

- 如果所有解决和升级途径都失败了，指派者可以在 PR 上添加 *TSC* 标签，将问题升级到 TSC，并在 TSC 获得具有约束力的裁决。

- 指派者应确保升级得到解决，并将结果记录在 Github 上相关的拉取请求或问题中。

.. _#pr-help: https://discord.com/channels/720317445772017664/997527108844798012

.. _Architecture Project: https://github.com/zephyrproject-rtos/zephyr/projects/18

.. _Architecture Working Group: https://github.com/zephyrproject-rtos/zephyr/wiki/Architecture-Working-Group
