.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-history:

历史与动机
##########

Zephyr 项目引入 west，是为了满足两个基本需求：

* 能够操作多个 Git 仓库
* 为基本 Zephyr 工作流提供可扩展且易用的命令行接口

在 west 开发过程中，确定了一组 :ref:`west-design-constraints`，以避免此类工具常见的问题。

要求
****

将 Zephyr 代码拆分到多个仓库的动机不在本页讨论范围内，但基本需求，以及不采用现有工具而选择开发新工具的明确理由，应在此说明。

基本需求如下：

* **R1**：将外部维护的代码保留在主 zephyr 仓库之外、分别维护的仓库中，同时无需用户逐个手动克隆这些外部仓库
* **R2**：提供一个 Zephyr 用户和发行方都能够使用、受益并扩展的工具
* **R3**：允许用户和下游发行版覆盖或移除仓库，而无需修改 zephyr 仓库
* **R4**：同时支持持续跟踪和基于提交（可二分定位）的项目更新


开发自定义工具的理由
********************

West 的部分功能与 `Git Submodules <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`_ 和 Google 的 `repo <https://gerrit.googlesource.com/git-repo/>`_ 类似。

在 west 最初设计和开发时，曾评估现有工具，但没有找到满足 Zephyr 需求的工具。具体而言，详细考察了以下工具：

* Google repo

  - 无法良好支持将 zephyr 用作清单仓库（**R4**）
  - 仅支持 Python 2
  - 与 Windows 配合不佳
  - 假定使用 Gerrit 进行代码审查

* Git 子模块

  - 不能完全满足 **R1**，因为外部维护的仓库仍需位于主 zephyr Git 树中
  - 不支持 **R3**，因为下游副本需要删除或替换子模块定义
  - 不支持持续跟踪外部仓库最新的 ``HEAD`` （**R4**）
  - 要求硬编码外部仓库的路径或位置

多个 Git 仓库
*************

Zephyr 旨在提供部署复杂物联网应用所需的全部构建组件。因此，Zephyr 项目远不止一个 RTOS 内核，而是一组协同工作的组件。在此背景下，项目需要以标准化方式操作多个 Git 仓库，原因包括：

* 清晰分离 Zephyr 原创代码与引入的项目和库
* 避免原创代码与引入代码之间的许可证不兼容
* 缩小 Zephyr 核心代码库的体积和范围，将可选组件放在附加仓库中，而非直接引入主代码树
* 功能安全与信息安全认证
* 推动组件模块化
* 基于部分受支持开发板和 SoC 进行树外开发

有关 west 工作区如何管理多个 Git 仓库，参见 :ref:`west-basics`。

.. _west-design-constraints:

设计约束
********

West 具有以下特性：

- **可选**：始终 *可以* 退回使用“原生”命令行工具，也就是不使用 west 来使用 Zephyr（不过可能仍需安装 west，并让构建系统能够找到它）。但这样做未必总是 *方便*。（如果 west 的全部功能都已有便捷的现成实现，就没有必要开发它。）

- **兼容 CMake**：构建、烧录、调试和仿真器支持，始终保持与直接使用 CMake 的方式兼容。

- **跨平台**：West 使用 Python 3 编写，可在 Zephyr 支持的所有平台上运行。

- **可作为库使用**：只要可能，west 的功能就实现为可供其他程序独立使用的库，再提供包装这些库的独立命令行接口。West 本身是名为 ``west`` 的 Python 包，其库实现为子包。

- **审慎增加功能**：没有充分且有说服力的动机，就不会接受新功能。

- **行为明确**：West 包装其他命令时，其行为都有明确规定和文档。这既支持与第三方工具互操作，也意味着 Zephyr 开发者始终可以了解使用 west 时“底层”发生了什么。

更多详情和讨论见 :github:`Zephyr issue #6205 <6205>`。

.. _west-update-detached-heads:

``west update`` 与分离的 HEAD
*****************************

:ref:`更新流程 <west-update-procedure>` 中使用分离的 Git ``HEAD`` 修订版本的做法，让一些用户感到困惑，甚至不满。

具体来说，用户经常问：为什么 ``west update`` 默认不让已有本地分支保持检出状态？

本节解释 ``west update`` 默认行为的原因，并介绍如何用其他选项管理有本地修改的项目。

``west update`` 有两个核心要求：

#. 安全性：命令不能丢失用户的任何工作
#. 确定性：两个用户对同一清单运行 ``west update``，应得到完全相同的 :ref:`工作区 <west-basics>` 内容

使用分离的 HEAD 有助于保证安全性。如更新流程所述，对已更新项目运行 ``git checkout --detach`` 以获得分离的 ``HEAD``，通常是不会丢失用户工作的安全操作：

- 如果工作已全部安全提交到本地 Git 分支，该分支会保持原样（详情见 ``git help checkout`` 输出）

- 如果有尚未提交的工作，只要可能，Git 就会将其安全保留在工作树中

- 如果无法保留，整个命令会失败，让你先决定如何处理这些工作，再重新运行 ``west update``

分离的 HEAD 也有助于保证确定性：

- 必须准确检出清单文件指定的项目修订版本，才能确保工作区文件符合主清单的规定。如果 west 默认不检出清单指定的修订版本，工作区就可能在不知不觉中偏离工作副本中清单文件所描述的预期状态。更糟的是，差异还会取决于运行 ``west update`` 之前分支中的具体内容。

- 这与 :ref:`west-manifest-import` 之间存在微妙的相互影响。如果项目本身包含一个或多个由 ``west update`` 导入的清单文件，west 就需要将这些文件检出到工作树中，才能解析完整的导入清单。如果 ``west update`` 让项目中的分支保持检出状态，工作树中的清单文件可能已过时。若 west 再使用这些旧文件完成导入，过程可能意外失败，或产生其他不确定结果。

West 不会直接检出 :ref:`manifest-rev <west-manifest-rev>` 分支，原因已在该分支的文档中说明。

此默认行为很早就已确定，用户已经依赖它，因此现在无法再更改。但如果默认行为不适合你，仍可使用其他方式运行 ``west update``。运行 ``west help update`` 并阅读 ``checked out branch behavior`` 选项组说明，即可了解详情。例如：

- 如果正在项目中编写代码，并希望在上游清单可能发生变化后继续保持更新，可使用 ``west update --rebase``

- 如果有希望保留的本地代码，只要项目的上游修订版本尚未前进到更新版本就继续保留，可使用 ``west update --keep-descendants``

如果希望在工作区中为其中某个命令设置更简短的输入方式，可以使用 :ref:`west-aliases`。也可以向以下地址提交拉取请求，为此选项组贡献新选项：

https://github.com/zephyrproject-rtos/west
