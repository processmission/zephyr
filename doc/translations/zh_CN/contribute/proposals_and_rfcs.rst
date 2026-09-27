.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _rfcs:

提案与 RFC
##########

许多变更，包括缺陷修复和文档改进，都可以通过常规的 GitHub 拉取请求工作流来实施和审查。

然而，许多变更是“重大”的，需要经历设计流程并在项目利益相关者之间达成共识。

“RFC”（请求意见稿）流程旨在为新特性进入项目提供一条一致且受控的路径。

如果贡献者和项目利益相关者打算对 Zephyr 或其文档进行“重大”变更，应考虑使用此流程。以下一些示例可以从 RFC 中获益：

- 会形成新 API 表面积的新特性，若将其引入则需要特性标志。
- 修改现有的稳定 API。
- 移除已作为 Zephyr 一部分发布的特性。
- 引入新的惯用用法或约定，即使其中不包含对 Zephyr 本身的代码更改。

RFC 流程是一个绝佳的机会，可以让更多人在提案成为 Zephyr 的一部分之前审视来自贡献者的提案。很多时候，即使是看似“显而易见”的提案，在更广泛的感兴趣群体有机会发表意见后也能得到显著改进。

当提案特性仍在设计过程中时，RFC 流程也有助于鼓励围绕该特性展开讨论，并在设计尚未完全实现、更容易修改的时候将重要约束纳入设计。

对于重大特性（Major Feature），首先创建一个 issue 并概述你的提案，以便对其进行讨论。这也能让我们更好地协调工作、避免重复劳动，并帮助你打磨变更，使其成功被项目接受。提供以下信息将提高你的 issue 得到快速处理的可能性：

  * 提案概述
  * 动机或用例
  * 设计细节
  * 备选方案
  * 测试策略

有些变更或贡献不需要 RFC，但变更的依据和细节应当作为拉取请求的一部分：

- 对现有已确立子系统的少量增强和修改。
- 改写、重组或重构
- 添加或移除警告
- 为现有子系统添加新开发板、SoC 或驱动
- ...

该流程本身是创建一个带有 :ref:`RFC 标签 <gh_labels>` 的 GitHub issue，并在其中详尽记录提案。鼓励你使用 `RFC form`_ 来确保提案遵循项目参与者已经熟悉的模板。

与拉取请求一样，RFC 可能需要在一场 `Zephyr meetings`_ 的语境中讨论，以便在存在分歧或意见不足难以推进的情况下推动其前进。请务必为其打上恰当的标签，或将其纳入相应的 GitHub 项目，以便在下次会议上对其进行审议。

.. _`RFC form`: https://github.com/zephyrproject-rtos/zephyr/issues/new?template=003_rfc-proposal.yml
.. _`Zephyr meetings`: https://github.com/zephyrproject-rtos/zephyr/wiki/Zephyr-Committee-and-Working-Groups
