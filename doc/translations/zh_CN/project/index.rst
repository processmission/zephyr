.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _development_model:

项目与治理
##########


.. toctree::
   :maxdepth: 1

   tsc
   project_roles
   working_groups
   release_process
   proposals
   code_flow
   dev_env_and_tools
   issues
   communication
   documentation



Zephyr 项目定义了一套开发流程，使用 GitHub **Issues** 跟踪功能请求、增强建议和缺陷报告，并使用 GitHub **Pull Requests** （PR）提交和评审变更。Zephyr 社区成员共同评审这些 Issue 和 PR，通过定期发布的版本推进 Zephyr 的功能增强和质量改进，详见 :ref:`release_process` 。

面对大量的 Issue 和 PR，只有要求社区和贡献者及时开展评审、提供反馈并作出回应，才能有效管理；这既适用于首次提交，也适用于后续的问题和澄清请求。请阅读项目的 :ref:`开发流程和工具 <dev-environment-and-tools>` 以及 :ref:`评审时限 <review_time>` 的具体说明，了解项目为活跃开发者社区制定的目标和准则。

:ref:`project_roles` 详细介绍了 Zephyr 项目在开发流程中的各个角色及其相应权限。


术语
****

- 主线：用于开发核心功能和核心特性的主代码树。
- 子系统/功能分支：同一仓库内的分支。在本项目中，我们也使用“分支”一词来指代位于不同仓库中的分支；这些仓库是共享同一历史记录的仓库副本。
- 上游：源代码所基于的父分支。你从该分支拉取代码，并向其推送代码，因此它就是你的上游。
- LTS：长期支持
