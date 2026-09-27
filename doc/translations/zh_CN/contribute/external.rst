.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external-contributions:

贡献外部组件
############

在某些情况下，为了避免重新实现其他开源项目中已有的基本功能或特性，利用现有的外部源代码是可取的。

本节介绍可以将外部源代码导入 Zephyr 的情形，以及约束其纳入的流程。

在纳入过程中会考虑三个主要因素，以决定是否接受该组件。这些因素将在以下各节中说明。

请注意，本页大部分内容涉及最终会被编译并链接进最终镜像、并烧录到目标硬件中的外部组件。对于仅在编译、代码分析、测试或仿真期间使用的外部工具，请参阅本页末尾的 :ref:`external-tooling` 一节。

软件许可证
**********

.. note::

   以 Apache-2.0 许可证授权的外部源代码不适用本节的规定。

将采用 Apache 2.0 以外许可证的其他项目中的代码集成到 Zephyr 项目时，需要结合具体语境充分理解，并获得 `Zephyr governing board`_ 的批准，如 `Zephyr project charter`_ 所述。对于未经 `Open Source Initiative (OSI)`_ 批准的许可证，董事会将自动拒绝。更多细节请参阅 :ref:`external-src-process` 一节。

.. _Zephyr governing board:
   https://www.zephyrproject.org/governance/

.. _Zephyr project charter:
   https://www.zephyrproject.org/wp-content/uploads/2023/08/LF-Zephyr-Charter-2023.08.21.pdf

.. _Open Source Initiative (OSI):
   https://opensource.org/licenses/alphabetical

通过仔细审查潜在的贡献，并对贡献的代码执行 :ref:`DCO`，我们确保 Zephyr 社区能够基于 Zephyr 项目开发产品，而不必担心专利或版权问题。

价值
****

与任何其他常规贡献一样，包含外部代码的贡献也需要评估其价值。然而，对于来自现有项目的代码这一特殊情况，还需要回答一些额外问题才能接受该贡献。具体而言，以下方面将由技术指导委员会（Technical Steering Committee）考虑，并在外部源代码被项目接受之前进行仔细评估：

- 这是向项目引入该功能的最优方式吗？既需要评估在项目内部实现该功能的成本，也需要评估维护外部开发的代码库所产生的成本。
- 该外部项目是否在积极维护？对于涉及安全或密码学的源代码而言，这一点尤为重要。
- 是否考虑过所提议的特定实现方式的替代方案？是否有其他实现相同功能的开源项目？

集成方式
********

将外部源代码集成到 Zephyr 项目有两种方式，必须慎重考虑为每种具体情况选择合适的方式。

集成到主代码树中
================

将外部源代码集成到项目的第一种方式是，直接将源代码文件导入 ``zephyr`` 主仓库。这自然意味着导入的源代码成为“主线”代码库的一部分，因此要求：

- 代码按照 Zephyr :ref:`coding_style` 进行格式化
- 代码遵循项目的 :ref:`coding_guidelines`
- 代码与主代码树中的其他代码一样，需遵守相同的检查和验证要求，包括静态分析
- 所有文件在尚未包含 SPDX 标签时都应添加该标签
- 如果源代码不是以 Apache 2.0 授权的，则需在仓库根目录的 :zephyr_file:`REUSE.toml` 文件中添加描述该组件的 ``[[annotations]]`` 条目。:ref:`许可证页面 <zephyr_licensing>` 正是由此生成的。

这种集成方式既适用于小型外部代码库，也适用于大型外部代码库，但通常更多用于前者。

作为模块集成
============

将外部源代码集成到项目的第二种方式是，将第三方开源项目的全部或部分导入到一个单独的仓库，然后以 :ref:`module <modules>` 的形式纳入。采用这种方式时，代码被视为在外部开发，因此不会自动受上一节要求的约束。

集成到主清单文件（west.yaml）中
-------------------------------

将外部代码集成到主 :file:`west.yml` 清单文件仅限于 Zephyr 子系统（库）、平台、驱动（HAL）所使用的代码，或测试、构建 Zephyr 组件所需的工具。

这一组模块的集成由 Zephyr 项目 CI 验证，并在每个 Zephyr 版本中确认可正常工作。

已集成的模块在未提供详细迁移计划的情况下不会被从代码树中移除。

作为可选模块集成
----------------

对于不带有任何传入依赖的模块/项目，其独立或松散集成应设为可选并保持独立。那些通过 Zephyr 子系统或平台直接为用户提供价值的可选项目，应添加到默认被过滤的可选清单文件中（:file:`submanifests/optional.yml`）。

此类可选项目可以在各自的仓库中包含示例和测试。

不得在 Zephyr 代码树（Git 仓库）中添加任何直接依赖，所有示例或测试代码都应作为模块的一部分进行维护。

.. note::

   这适用于所有新的可选模块。Zephyr Git 仓库中带有示例和测试代码的现有可选模块将逐步迁移出去。

作为外部模块集成
----------------

与可选模块类似，但通过预定义模板以文档条目的形式添加到 Zephyr 项目。此类模块存在于 Zephyr 项目清单之外，并通过文档指导用户和开发者如何集成该功能。

持续维护
********

无论采用哪种集成方式，集成到 Zephyr 中的外部源代码都需要定期持续维护。因此，集成外部源代码提案的提交者必须承诺在可预见的未来维护此类代码的集成。作为流程的一部分，这可能需要向 :file:`MAINTAINERS.yml` 添加一个条目。

.. _external-src-process:

提交与审查流程
**************

在外部源代码被纳入项目之前，必须由技术指导委员会（TSC）审查并接受，在某些情况下还需获得 Zephyr 董事会的批准。

外部源代码集成请求必须通过在 GitHub 上的 Zephyr 项目 issue 跟踪系统中创建一个新 issue 来提出，其中需包含有关该源代码及其如何集成到项目的详细信息。

请按以下步骤开始提交流程：

#. 请务必详细阅读 :ref:`external-contributions` 一节，以便了解 TSC 和董事会用于批准或拒绝请求的标准
#. 使用 :github:`New External Source Code Issue <new?assignees=&labels=RFC&template=007_ext-source.yml>` 来打开一个 issue
#. 填写所有必需的部分，确保提供足够的细节，以便 TSC 评估该请求的价值。你还可以选择创建一个演示外部源代码集成的拉取请求，并在 issue 中链接到它
#. 等待 TSC 的反馈，并回复以 GitHub issue 评论形式提出的任何其他问题

如果经 TSC 审议后得出的结论是集成外部源代码是最佳解决方案，且该外部源代码以 Apache-2.0 许可证授权，则提交流程完成，可以集成该外部源代码。

然而，如果外部源代码使用的许可证不是 Apache-2.0，则必须遵循以下附加步骤：

#. TSC 主席会将早期提交流程中创建的 GitHub issue 链接转发给 Zephyr 董事会以进行进一步审查

#. Zephyr 董事会有两周时间进行审查和提问：

   - 如果没有异议，此事即告结束。如果在两周期限结束前获得董事会一致批准，则可以加快批准。

   - 如果有董事会成员提出无法通过电子邮件解决的异议，董事会将召开会议，讨论是推翻 TSC 的批准，还是寻找能够解决该异议的其他方案

#. 在 Zephyr TSC 和董事会批准后，提交流程即告完成

下图展示了该流程的概览：

.. figure:: media/ext-src-flowchart.svg
   :align: center

   提交流程

.. _external-tooling:

贡献外部工具
************

本节专门讨论将外部工具纳入 Zephyr 项目的问题，这里的工具是指协助编译、测试或仿真过程，但最终绝不会成为编译并链接到最终镜像中的代码的一部分的软件。此语境中的“纳入”是指成为 Zephyr 默认发行版的一部分，可以是直接位于 :file:`scripts/` 文件夹下的主代码树中，也可以是作为主 :file:`west.yml` 清单中的 west 项目间接纳入。因此，本节不适用于工具链、仿真器等第三方工具，它们可能仍会被 Zephyr 构建系统或文档引用，但并未被纳入 Zephyr。

工具组件必须依据 `Open Source Initiative (OSI)`_ 批准的许可证发布。

与常规外部组件一样，从其他项目导入的工具既可以集成到主代码树中，也可以作为 :ref:`west 项目 <west-workspace>` 集成。请注意，在这种情况下，相应的 west 项目不会是 :ref:`模块 <modules>`，因为工具并不使用 Zephyr 构建系统，也不需要由它处理。有关两者差异的更多信息，请参阅 :ref:`modules-vs-projects`。

如果工具集成到主代码树中，它应放在 :file:`scripts/` 文件夹下。如果工具作为 west 项目集成，则项目仓库可以托管在 zephyrproject-rtos GitHub 组织之外，前提是通过主 :file:`west.yml` 清单中的 ``group-filter:`` 字段将其设为可选。有关可选项目的更多信息，请参见 :ref:`本节 <west-manifest-groups>`。

TSC 必须批准每一个引入新外部工具组件的拉取请求。这将由 TSC 代表对所提议的添加内容进行逐个、逐项分析来完成。

关于主清单的其他考虑事项
************************

一般而言，对 `main manifest file`_ 中 ``projects:`` 部分的任何添加或移除都需要 TSC 批准。这包括但不限于：

- 添加和移除组及组过滤器
- 添加和移除项目
- 添加和移除 ``import`` 语句

.. _main manifest file:
   https://github.com/zephyrproject-rtos/zephyr/blob/main/west.yml
