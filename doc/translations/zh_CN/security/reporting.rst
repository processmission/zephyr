.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _reporting:

安全漏洞报告
############

简介
====

Zephyr 项目中的漏洞最好通过在 Zephyr 仓库的 `security advisories page <security advisory_>`_ 上创建草稿 `security advisory <security advisories page_>`_ 来报告。或者，也可以通过电子邮件将报告发送至 vulnerabilities@zephyrproject.org 提交给项目安全事件响应团队。这些报告将在 1 周内由安全响应团队确认并分析。

所有漏洞都通过 GitHub 上 Zephyr 项目的 `security advisories page`_ 进行跟踪和管理，原始提交者将获得查看其所报告问题的权限。

.. _security advisory: https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability#privately-reporting-a-security-vulnerability
.. _security advisories page: https://github.com/zephyrproject-rtos/zephyr/security/advisories

漏洞报告准则
============

安全研究和漏洞报告是对 Zephyr 项目的宝贵贡献。为了让这一过程对每个人都安全且富有成效，所有报告及相关活动都必须遵守 Zephyr 项目的 `Code of Conduct`_。

以下准则描述了在研究并报告 Zephyr 安全漏洞时应达到的期望。

.. _Code of Conduct: https://github.com/zephyrproject-rtos/zephyr/blob/main/CODE_OF_CONDUCT.md

报告期望
--------

为帮助安全响应团队高效地分类和解决问题，报告应：

- 描述受影响的组件、版本、开发板或平台，以及复现问题所需的配置。

- 包含清晰的逐步复现说明，并尽可能提供最小化的概念验证。

- 说明安全影响（例如机密性、完整性或可用性损失）以及任何已知的缓解措施。

- 避免包含可能对用户或系统造成损害的破坏性载荷或组件，以免报告被意外公开。

在公开披露之前，报告者应本着善意，给项目留出合理的机会来调查和修复问题，并遵循后续章节所述的禁运与披露流程。

安全问题管理
============

此缺陷跟踪系统中的问题将按照下图在各状态之间流转：

.. graphviz::

   digraph {
      node [style = rounded];
      init [shape = point];
      New [shape = box];
      Triage [shape = box];
      {
        rank = same;
        rankdir = LR;
        Assigned [shape = box];
        Rejected [shape = box];
      }
      Review [shape = box];
      Accepted [shape = box];
      Public [shape = box];

      init -> New;
      New -> Triage;
      Triage -> Rejected [dir = both];
      Triage -> Assigned;
      Assigned -> Review [dir = both];
      Review -> Accepted;
      Review -> Rejected;
      Accepted -> Public;

   }

- 新建：此状态表示由报告者直接录入的新报告。当响应团队根据电子邮件录入问题时，问题应直接流转到分类状态。

- 分类：此问题正等待响应团队分类。响应团队将分析问题、确定负责实体、将其分配给相应人员，并将问题移至已分配状态。分类工作的一部分是设置问题的优先级。

- 已分配：该问题已分配，正在等待被分配者修复。

- 审查：一旦该问题有了 Zephyr 拉取请求，PR 链接将被添加到问题评论中，问题将移至审查状态。

- 已接受：表示该问题已合并到 Zephyr 中相应的分支。

- 公开：禁运期已结束。问题将公开可见，关联的 CVE 将更新，文档中的漏洞页面也将更新以包含详细信息。

由于安全报告的敏感性，创建的安全公告会保持私有。问题仅对特定方可见：

- PSIRT 邮件列表成员

- 报告者

- 由 Zephyr 安全子委员会提议并批准的其他方。一般情况下，将包括：

  - 负责修复的代码所有者。

  - 受此漏洞影响的相应版本的 Zephyr 发布负责人。

Zephyr 安全子委员会应在出席人数超过三人的任何会议上审查所报告的漏洞。在审查期间，他们应确定是否需要禁运新问题。

禁运准则将基于：1. 问题的严重性，2. 问题的可利用性。子委员会决定无需禁运的问题将在 Zephyr 项目的常规缺陷跟踪系统中复现。

.. _vulnerability_timeline:

安全敏感漏洞应在最长 90 天的禁运期后公开。其目的是让 Zephyr 项目内部有 30 天时间修复这些问题，并让使用 Zephyr 构建产品的外部相关方有 60 天时间应用和分发这些修复。

.. _vulnerability_fix_recommendations:

代码修复应通过 Zephyr 项目 GitHub 上的拉取请求 PR 进行。开发者应尽量不暴露正在修复内容的敏感性质，也不应提及已分配给该问题的 CVE 编号。开发者只应描述已修复的内容。

安全子委员会将维护禁运 CVE 与这些 PR 的映射信息（该信息位于 GitHub 安全公告中），并定期生成安全问题状态报告。

每个被视为安全漏洞的问题都应分配一个 CVE 编号。随着修复的创建，可能需要分配额外的 CVE 编号，或撤销已分配的编号。

漏洞通知
========

每个 Zephyr 版本都应包含该版本中已修复 CVE 的报告。由于这些漏洞具有敏感性，版本中只应包含已修复 CVE 的列表。禁运期结束后，应更新漏洞页面以包含这些漏洞的更多详细信息。漏洞页面应注明报告者的贡献，除非报告者明确要求匿名。

Zephyr 项目应维护一个漏洞警报邮件列表。该列表最初将包含来自每个项目成员的一名联系人。其他相关方可以通过填写 `Vulnerability Registry`_ 中的表单申请加入该列表。项目负责人将对这些相关方进行审核，以确定他们在禁运期内了解安全漏洞具有正当利益。

.. _Vulnerability Registry: https://www.zephyrproject.org/vulnerability-registry/

安全子委员会将定期向该邮件列表发送信息，说明已知的禁运问题及其在项目中的回移状态。这些信息旨在帮助他们确定是否需要将这些变更回移到任何内部代码树。

问题完成分类后，将向该列表通知以下内容：

- Zephyr 项目安全公告链接（GitHub）。

- 分配的 CVE 编号。

- 涉及的子系统。

- 问题的严重性。

在修复问题的 PR 被接受（合并）后，除上述内容外，还将向该列表通知：

- CVE 编号与修复该问题的 PR 之间的关联。

- Zephyr 项目内的回移计划。

安全漏洞的回移
==============

Zephyr 中修复的每个安全问题都应回移到以下版本：

- 当前的长期稳定（LTS）版本。

- 最近的两个版本。

修复的开发者应负责所有必要的回移，并将其应用到上述任一发布分支，除非该修复不适用（漏洞是在该版本发布之后引入的）。有关 :ref:`漏洞修复 <vulnerability_fix_recommendations>` 的所有建议都适用于回移拉取请求（及相关问题）。此外，建议开发者私下告知相应的发布负责人，该回移拉取请求和问题正在处理一个漏洞。

回移将在安全公告中跟踪。

按需知悉
========

由于安全漏洞具有敏感性，务必只与需要知悉的相关方共享详细信息和修复。在禁运期结束之前，以下相关方需要了解安全漏洞的详细信息：

- 维护者只能访问其所属领域内的所有信息。

- 当前发布负责人，以及受该漏洞影响的历史版本的发布负责人（参见上文回移部分）。

- 项目安全事件响应（PSIRT）团队将拥有完全的信息访问权限。PSIRT 由白金会员代表以及其他会员中参与分类工作的志愿者组成。

- 必要时，可邀请发布负责人和维护者参加额外的安全会议，讨论漏洞。
