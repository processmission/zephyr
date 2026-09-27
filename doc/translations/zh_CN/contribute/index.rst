.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _contribute_to_zephyr:

参与 Zephyr 项目
################

来自社区的贡献是项目的支柱。无论是提交代码、改进文档还是提出新特性，您的努力都备受赞赏。本页面列出了有助于您参与贡献的有用资源和指南。

通用指南
========

.. toctree::
   :maxdepth: 1
   :hidden:

   guidelines.rst
   contributor_expectations.rst
   reviewer_expectations.rst
   coding_guidelines/index.rst
   style/index.rst
   proposals_and_rfcs.rst
   modifying_contributions.rst
   pr_lifecycle_policy.rst


:ref:`贡献指南 <contribute_guidelines>`
   了解为 Zephyr 项目做贡献的总体流程和指南。

   本页面是首次贡献者的必读内容，其中包含如何确保您的贡献能够被项目考虑纳入并可能被合并的重要信息。

:ref:`贡献者期望 <contributor-expectations>`
   本文档同样属于必读内容，描述了项目 *所有* 贡献者应有的行为。

:ref:`审查者期望 <reviewer-expectations>`
   本文档同样属于必读内容，描述了审查项目贡献时应有的行为。

:ref:`编码指南 <coding_guidelines>`
   代码贡献应遵循一套编码指南，以确保整个代码库的一致性和可读性。

:ref:`代码风格 <coding_style>`
   代码贡献应遵循一套风格指南，以确保整个代码库的一致性和可读性。

:ref:`RFC <rfcs>`
   了解何时以及如何为新特性和项目变更提交 RFC（Request for Comments，征求意见稿）。

:ref:`修改贡献 <modifying_contributions>`
   关于修改其他开发者所做贡献的指南，以及如何处理长期未更新的拉取请求。

:ref:`拉取请求生命周期策略 <pr_lifecycle_policy>`
   关于使未关闭的拉取请求专注于正在积极推进且可能被合并的工作的策略。

文档
====

Zephyr 项目因良好的文档而蓬勃发展。无论是作为代码贡献的一部分，还是独立进行，贡献文档对项目都特别有价值。

.. toctree::
   :maxdepth: 1
   :hidden:

   documentation/guidelines.rst
   documentation/generation.rst

:ref:`文档指南 <doc_guidelines>`
   本页面提供了一些使用 reStructuredText（reST）标记语言和 Sphinx 文档生成器编写文档的简单指南。

:ref:`Zephyr 文档 <zephyr_doc>`
   编写文档时，查看渲染后的效果会很有帮助。

   本页面介绍如何在本地构建 Zephyr 文档。


处理外部组件
============

.. toctree::
   :maxdepth: 1
   :hidden:

   external.rst
   bin_blobs.rst

:ref:`外部贡献 <external-contributions>`
   对 Zephyr 有用的基础功能或特性可能已存在于其他开源项目中，建议并鼓励重用此类代码。本页面更详细地介绍何时以及如何将外部源代码导入 Zephyr。

:ref:`外部工具 <external-tooling>`
   类似地，编译、代码分析、测试或仿真期间使用的外部工具也可能带来好处，本节将对此进行介绍。

:ref:`二进制 blob <bin-blobs>`
   由于某些功能可能只能借助以二进制形式分发的可执行代码提供，本页面介绍向项目 :ref:`贡献二进制 blob <blobs-process>` 的流程和指南。

需要帮助？
==========

如果您对贡献流程有疑问，Zephyr 社区随时为您提供帮助。您可以加入我们的 Discord_ 频道，或使用 `Developer Mailing List`_。


.. _Discord: https://chat.zephyrproject.org
.. _Developer Mailing List: https://lists.zephyrproject.org/g/devel
