.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-built-in-cmds:

内置命令
########

本页详细介绍 west 的内置命令，其中一部分已在 :ref:`west-basics` 中介绍。

一些命令与同名 Git 命令相关，但作用于整个工作区。例如，``west diff`` 显示工作区内多个 Git 仓库中的本地修改。

某些命令接受项目作为参数。参数可以是清单文件指定的项目名称，也可以退而使用项目在本地文件系统中的路径。对于接受项目参数的命令（例如 ``west list``、``west forall`` 等），省略参数时，通常默认使用清单中的全部项目及清单仓库本身。

运行 ``west <command> -h`` （例如 ``west init -h``）可获取更多帮助。

.. _west-init:

west init
*********

此命令创建 west 工作区，有两种用法：

1. 从远程 URL 克隆新的清单仓库
2. 围绕已有本地清单仓库创建工作区

**方式 1**：从远程 URL 克隆新的清单仓库，使用：

.. code-block:: none

   west init [-m URL] [--mr REVISION] [--mf FILE] [directory]

新工作区创建在指定的 :file:`directory` 中，并在该目录内创建新的 :file:`.west`。可以通过 ``-m`` 指定清单 URL，通过 ``--mr`` 指定初始检出的修订版本，通过 ``--mf`` 指定清单文件在仓库中的位置。

例如，运行：

.. code-block:: shell

   west init -m https://github.com/zephyrproject-rtos/zephyr --mr v1.14.0 zp

会将官方上游 zephyr 仓库克隆到 :file:`zp/zephyr`，并检出 ``v1.14.0`` 版本。此命令创建 :file:`zp/.west`，并将 ``manifest.path`` :ref:`配置选项 <west-config>` 设为 ``zephyr``，记录清单仓库在工作区中的位置。清单文件使用默认位置。

``-m`` 选项默认为 ``https://github.com/zephyrproject-rtos/zephyr``。``--mf`` 选项默认为 ``west.yml``。从 west v0.10.1 起，除非通过 ``--mr`` 覆盖，west 会使用清单仓库的默认分支。（更早版本的 ``--mr`` 默认为 ``master``。）

如果未指定 ``directory``，则使用当前工作目录。

**方式 2**：围绕已有本地清单仓库创建工作区，使用：

.. code-block:: none

   west init -l [--mf FILE] directory

这会在文件系统中与 :file:`directory` **同级** 的位置创建 :file:`.west`，并将 ``manifest.path`` 设为 ``directory``。

与上文一样，``--mf`` 默认为 ``west.yml``。

**重新配置工作区**：

运行 ``west init`` 后，如果改变主意，可以通过 :ref:`west-config-cmd` 修改 ``manifest.path`` 和 ``manifest.file``。只需确保随后运行 ``west update``，将工作区更新为与新清单文件一致。

.. _west-update:

west update
***********

.. code-block:: none

   west update [-f {always,smart}] [-k] [-r]
               [--group-filter FILTER] [--stats] [PROJECT ...]

**更新哪些项目：**

默认情况下，此命令解析清单文件（通常是 :file:`west.yml`），并更新其中指定的每个项目。如果清单使用 :ref:`项目组 <west-manifest-groups>`，则只更新活动项目。

如果只需操作部分项目，可传入一个或多个 ``PROJECT`` 参数。每个 ``PROJECT`` 可以是清单中的项目名称，也可以是指向工作区内项目的路径。显式指定的项目无论是否处于活动状态，都会更新。

.. _west-update-procedure:

**项目更新流程：**

对于每个要更新的项目，此命令会：

#. 如果本地 Git 仓库尚不存在，则在工作区中为项目初始化仓库
#. 检查清单中项目的 ``revision`` 字段，如果相应修订版本在本地尚不可用，则从远程仓库获取
#. 将项目的 :ref:`manifest-rev <west-manifest-rev>` 分支设置为上一步修订版本所指定的提交
#. 在本地工作副本中，将 ``manifest-rev`` 检出为 `detached HEAD <https://git-scm.com/docs/git-checkout#_detached_head>`_ （分离的 HEAD，关于此选择的说明见 :ref:`west-update-detached-heads`）
#. 如果清单为该项目指定了 :ref:`submodules <west-manifest-submodules>` 键，则按下文所述递归更新其子模块。

为避免不必要的获取，如果项目 ``revision`` 值是本地已有的 Git SHA 或标签，``west update`` 就不会获取。这是 ``-f`` （``--fetch``）选项采用默认值 ``smart`` 时的行为。如果希望即使修订版本似乎已在本地可用，仍强制从项目远程仓库获取，可以使用 ``-f always``，或将 ``update.fetch`` :ref:`配置选项 <west-config>` 设为 ``always``。只要 Git 接受，SHA 可以用唯一前缀表示 [#fetchall]_。

如果项目 ``revision`` 是既非标签也非 SHA 的 Git 引用（即项目跟踪某个分支），``west update`` 就始终执行获取，不受 ``-f`` 和 ``update.fetch`` 影响。

有些分支名称看起来像短 SHA，例如 ``deadbeef``。West 会将其视为 SHA。可以在 ``revision`` 值前加上 ``refs/heads/`` 消除歧义，例如 ``revision: refs/heads/deadbeef``。

为保证安全，``west update`` 使用 ``git checkout --detach``，在每个更新项目的清单修订版本处检出分离的 ``HEAD``，不再检出此前的分支。这通常是安全操作，不会修改任何本地分支。

但是，如果曾在 west 先前检出的分离 ``HEAD`` 上添加本地提交，Git 会警告有些留下的提交已不被任何分支引用。它们将来可能被垃圾回收而丢失。项目中有本地提交时，为避免此问题，应确保在运行 ``west update`` 前检出本地分支。

如果希望改为对本地已检出的分支变基，使用 ``-r`` （``--rebase``）选项。

如果希望只要本地分支指向新 ``manifest-rev`` 的后代提交，``west update`` 就保持该分支检出，使用 ``-k`` （``--keep-descendants``）选项。

.. note::

   如果项目中你的分支与清单引入的新提交存在 Git 冲突，``west update --rebase`` 会失败。应立即照常使用 ``git`` 解决冲突，或使用 ``git -C <project_path> rebase --abort`` 暂时忽略传入的改动。

   工作树干净时，普通的 ``west update`` 不会失败，因为它不会尝试保留你的提交在当前检出历史中，而只是将它们留在一旁。

   ``west update --keep-descendants`` 提供一种同样不会失败的折中方案，但对各项目的处理不同：

   - 如果项目中的分支与传入提交已分叉，它不会尝试变基，而是像普通 ``west update`` 一样切离原分支；
   - 其他不需要变基或合并的项目则保持原分支检出。

**一次性调整项目组：**

``--group-filter`` 选项可在单次 ``west update`` 命令期间，改变启用或禁用的项目组。项目组功能详情见 :ref:`west-manifest-groups`。

``west update`` 的行为等同于将 ``--group-filter`` 的值附加到 ``manifest.group-filter`` :ref:`配置选项 <west-config-index>`。

例如，运行 ``west update --group-filter=+foo,-bar``，等同于临时将字符串 ``"+foo,-bar"`` 附加到 ``manifest.group-filter`` 的值，运行 ``west update``，然后恢复 ``manifest.group-filter`` 的原值。

请注意，如果只想禁用一个组，使用 ``--group-filter=VALUE`` 而不是 ``--group-filter VALUE`` 可以避免命令行选项解析问题，例如 ``--group-filter=-bar``。

**子模块更新流程：**

如果清单中的项目含有 ``submodules`` 键，则根据 ``submodules`` 键的值按以下方式更新子模块。

如果项目设置了 ``submodules: true``，west 首先使用以下命令同步项目子模块：

.. code-block::

   git submodule sync --recursive

然后根据运行 ``west update`` 时是否带有 ``--rebase`` 选项，在项目仓库中运行以下命令之一：

.. code-block::

   # without --rebase, e.g. "west update":
   git submodule update --init --checkout --recursive

   # with --rebase, e.g. "west update --rebase":
   git submodule update --init --rebase --recursive

否则，项目设置的是 ``submodules: <list-of-submodules>``。此时 west 使用以下命令同步项目子模块：

.. code-block::

   git submodule sync --recursive -- <submodule-path>

随后根据运行 ``west update`` 时是否带有 ``--rebase``，按以下方式更新列表中的每个子模块：

.. code-block::

   # without --rebase, e.g. "west update":
   git submodule update --init --checkout --recursive <submodule-path>

   # with --rebase, e.g. "west update --rebase":
   git submodule update --init --rebase --recursive <submodule-path>

如果 ``update.sync-submodules`` :ref:`west-config` 选项为 false，则跳过 ``git submodule sync`` 命令。

.. _west-built-in-misc:

其他项目命令
************

West 还提供一些管理工作区项目的命令，概述如下。运行 ``west <command> -h`` 获取详细帮助。

- ``west compare``：将工作区状态与清单比较
- ``west diff``：在本地项目仓库中运行 ``git diff``
- ``west forall``：在本地项目仓库中运行任意命令
- ``west grep``：在本地项目仓库中搜索模式
- ``west list``：按格式字符串，为清单中的每个项目打印一行信息
- ``west manifest``：管理清单文件。参见 :ref:`west-manifest-cmd`。
- ``west status``：在本地项目仓库中运行 ``git status``

其他内置命令
************

最后，以下概述其他内置命令。

- ``west config``：获取或设置 :ref:`配置选项 <west-config>`
- ``west topdir``：打印 west 工作区的顶层目录
- ``west help``：获取某个命令的帮助，或打印工作区内所有命令的信息，包括 :ref:`west-extensions`

.. rubric:: 脚注

.. [#fetchall]

   当修订版本指定为 SHA 时，west 可能从 Git 服务器获取所有引用。这是因为一些 Git 服务器过去不允许直接获取 SHA。
