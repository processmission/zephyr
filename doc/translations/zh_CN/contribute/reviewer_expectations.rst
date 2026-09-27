.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _reviewer-expectations:

审查者期望
##########

- 在评论 PR 时要保持尊重。更多细节请参阅 Zephyr 的 `Code of Conduct`_。

- Zephyr 项目认识到审查者和维护者的精力是有限的。作为审查者，请按以下顺序安排审查请求的优先级：

    #. 与 `Zephyr Release Plan`_ 中的事项相关的 PR，或在稳定期（RC1 之后）内以即将发布的版本为目标的 PR。
    #. 审查者已请求阻塞性变更的 PR。
    #. 作为领域维护者分配给审查者的 PR。
    #. 所有其他 PR。

- 审查者应通过提供反馈并与 PR 作者互动，努力推动 PR 达到可合并状态。

- 尽量一次性对整个 PR 提供反馈。这样贡献者就有机会在下一次 PR 更新中处理所有评论。

- 允许进行部分审查，但审查者必须添加评论说明其审查了 PR 的哪些部分。有用的部分审查示例包括：

  - 特定领域的审查（例如 Devicetree）。
  - 影响 PR 可读性的代码风格变更。
  - 当请求的变更会级联影响到后续提交时，可以逐个提交分别审查。

- 避免通过请求新特性来扩大 PR 的范围，尤其是当该 PR 关联有相应的 :ref:`RFC <rfcs>` 时。相反，审查者应将建议作为评论添加到 :ref:`RFC <rfcs>` 中。这也有助于促进更多协作，因为一旦最小实现被合并，多个贡献者就更容易围绕某个特性协同工作。

- 使用“Request Changes”选项时，应在评论中将琐碎的、非功能性的请求标记为“Non-blocking”。一旦只剩非阻塞性变更，审查者就应批准 PR。PR 作者可自行决定是否处理所有非阻塞性评论。PR 作者应以某种方式回应每一条审查评论，哪怕只是用一个表情符号。

- 审查者不赞同但项目文档中未记录的风格变更，可以作为非阻塞项指出，但不能构成请求变更的理由。审查者可以选择修正代码树中任何潜在的不一致之处，记录新的指南或规则，然后在审查中执行这些规则。

- 每当请求与风格相关的变更时，审查者应当能够指出项目文档中对应的指南、规则或理由。这不适用于某些类型的变更请求，特别是那些针对所提交变更本身的请求（例如使用特定的数据结构或选择特定的加锁原语）。

- 在使用“Request Changes”选项时，审查者应当 *clear* 地说明其请求的变更。请求的变更应当处于相关 PR 的范围之内，并遵循项目的贡献与风格指南。此外，审查者必须能够指出 PR 中触发变更请求的确切问题。

- 审查者不应对 CI 能自动发现的问题请求变更，因为这会导致拉取请求即使在 CI 失败得到解决后仍保持阻塞状态，并可能不必要地延迟其合并。

- 审查者不得因技术或结构性分歧而关闭 PR。如果请求的变更无法在审查流程内解决，则应使用 :ref:`pr_technical_escalation` 路径寻求可能的解决途径，其中可能包括关闭该 PR。

- 使用 AI 工具协助审查代码或起草回复时：

  - 审查者负责跟进其可能使用的 AI 工具（例如 GitHub Copilot）生成的评论。
  - 审查者绝不能将未经核实的 LLM 原始输出直接粘贴为 PR 评论。
  - 一般而言：所有 AI 生成的反馈都必须由人类审查者审核、核实并加以结合语境，该审查者对评论或审查的准确性和语气承担全部责任。

.. _Code of Conduct: https://github.com/zephyrproject-rtos/zephyr/blob/main/CODE_OF_CONDUCT.md

.. _Zephyr Release Plan: https://github.com/orgs/zephyrproject-rtos/projects/13
