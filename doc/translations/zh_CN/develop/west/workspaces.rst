.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-workspaces:

工作区
######

本页进一步介绍 :ref:`west-basics` 中引入的 *west 工作区* 概念。

.. _west-manifest-rev:

``manifest-rev`` 分支
*********************

West 在每个项目中创建并控制一个名为 ``manifest-rev`` 的 Git 分支。此分支指向上次运行 :ref:`west-update` 时，清单文件为该项目指定的修订版本。其他工作区管理命令可能将 ``manifest-rev`` 用作最近一次更新时的上游修订版本参考点。除其他用途外，``manifest-rev`` 分支还使清单文件能够使用 SHA 作为项目修订版本。

虽然 ``manifest-rev`` 是普通 Git 分支，west 仍会在下次更新时重新创建和/或重置它。因此，自行检出或修改它是 **危险的**。例如，手动添加到此分支的提交可能在下次运行 ``west update`` 时丢失。应改为检出另一个名称的本地分支，再将其变基到新的 ``manifest-rev`` 上，或将 ``manifest-rev`` 合并到该分支。

.. note::

   West 不会在清单仓库中创建 ``manifest-rev`` 分支，因为它不管理清单仓库的分支或修订版本。

``refs/west/*`` Git 引用
************************

West 还为自己保留本地项目仓库中所有以 ``refs/west/`` 开头的 Git 引用，例如 ``refs/west/foo``。与 ``manifest-rev`` 不同，这些引用不是常规分支。此处的行为属于实现细节，用户不应依赖这些引用的存在或行为。

.. _west-developing-in-a-git-repository:

在 Git 仓库中开发
*****************

工作区中的 ``west``“项目”都是普通 Git 仓库。默认情况下，west 只创建和更新 ``manifest-rev`` 分支以及 ``refs/west/`` 下的引用；你创建的分支由自己控制，west 只有在通过 ``west update --rebase`` 明确要求时才会对其变基。

这也解释了为什么普通的 :ref:`west update <west-update>` 会留下分离的 ``HEAD``：它检出新的 ``manifest-rev``，而让你的分支保持原样。设计理由见 :ref:`west-update-detached-heads`。

.. note::

   Zephyr *模块* 与 west 项目不是同一概念，虽然 west 项目往往也是模块；参见 :ref:`modules-vs-projects`。下述 Git 工作流适用于所有 west 项目，无论它们是否为 Zephyr 模块。

有本地修改时，以下工作流很适用：

#. 在仓库中创建分支，并照常提交：

   .. code-block:: console

      git -C <repository-path> switch --create <your-branch>

#. 使用 ``west update --rebase`` 更新工作区，再查看变更：

   .. code-block:: console

      west update --rebase
      west compare

   你的分支会保持检出状态，并变基到新的 ``manifest-rev`` 上。这是 west 唯一会修改你的分支的情况。如果产生冲突，命令会失败，此时照常使用 Git 解决冲突。

#. 如果不希望 west 对分支变基，普通的 ``west update`` 会改为切离该分支（除非这会引发 Git 冲突）。第三种选择是 ``west update --keep-descendants``，它不会失败。完整说明见 ``west update --help`` 中的 ``checked out branch behavior`` 选项组，以及 :ref:`west-update`。

在分离的 ``HEAD`` 上提交
========================

不要在 ``west update`` 留下的分离 ``HEAD`` 上提交：Git 会警告这些提交无法从任何分支到达，之后可能被垃圾回收。应为工作创建分支；也可以使用专为“无分支”工作设计的其他 Git 客户端，例如 `JJ`_。

.. _JJ: https://www.jj-vcs.dev/

私有仓库
********

可以使用 west 从私有仓库获取内容。这不需要任何 west 专用机制。

当项目的 ``manifest-rev`` 分支需要更新到新获取的提交时，``west update`` 命令实质上会运行 ``git fetch YOUR_PROJECT_URL``。需要由你的环境确保获取成功。

可以手动输入密码，也可以使用 `credential helpers built in to Git`_ （Git 内置的凭据辅助程序）。Git 已内置凭据存储功能，因此不需要 west 专用功能。

以下各节介绍运行 ``west update`` 时免输密码的常见情况，以及问题排查方法。

.. _credential helpers built in to Git:
   https://git-scm.com/docs/gitcredentials

通过 HTTPS 获取
===============

在 Windows 上从 GitHub 获取内容时，较新版本的 Git 会先在图形窗口中提示输入一次 GitHub 密码，然后保存以供后续使用（默认安装情况下）。因此，在 Windows 上完成首次操作后，从 GitHub 免密获取应当就能直接使用。

一般来说，可以通过 Git 的“store”凭据辅助程序将凭据保存到磁盘。详情见 `git-credential-store`_ 手册页。

要对工作区中的所有仓库使用此辅助程序，运行：

.. code-block:: shell

   west forall -c "git config credential.helper store"

要仅对项目 ``foo`` 和 ``bar`` 使用此辅助程序，运行：

.. code-block:: shell

   west forall -c "git config credential.helper store" foo bar

要在计算机上默认使用此辅助程序，运行：

.. code-block:: shell

   git config --global credential.helper store

在 GitHub 上，可以设置 `personal access token`_ （个人访问令牌）代替账户密码。（如果账户启用了双重身份验证，可能必须这样做；即使未启用，也可能比明文保存账户密码更合适。）

可以按以下方式，使用 Git 凭据存储通过 GitHub PAT（个人访问令牌）认证：

.. code-block:: shell

   echo "https://x-access-token:$GH_TOKEN@github.com" >> ~/.git-credentials

如果不希望在文件系统中保存任何凭据，可以改用 `git-credential-cache`_，将其临时保存在内存中。

如果已配置通过 SSH 获取，可以使用 Git 的 URL 重写功能。以下命令指示 Git 对 GitHub 使用 SSH URL，而不是 HTTPS URL：

.. code-block:: shell

   git config --global url."git@github.com:".insteadOf "https://github.com/"

.. _git-credential-store:
   https://git-scm.com/docs/git-credential-store#_examples
.. _git-credential-cache:
   https://git-scm.com/docs/git-credential-cache
.. _personal access token:
   https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

通过 SSH 获取
=============

如果 SSH 密钥没有密码，获取操作应可直接成功。如果有密码，可以使用 `ssh-agent`_ 避免每次手动输入。

有关 GitHub 的配置和密钥创建，参见 `Connecting to GitHub with SSH`_。

.. _ssh-agent:
   https://www.ssh.com/ssh/agent
.. _Connecting to GitHub with SSH:
   https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh

项目位置
********

项目可以位于工作区内部任意位置，但不能“越出”工作区。

换言之，项目仓库不必位于清单仓库的子目录中，也不必是顶层目录的直接子目录，但路径必须位于工作区内部。

可以将工作区中的项目仓库目录替换为指向计算机其他位置的符号链接，但 west 不会替你执行此操作。

.. _west-topologies:

支持的拓扑
**********

以下是 west 支持的源代码拓扑示例。

- T1：星形拓扑，zephyr 为清单仓库
- T2：星形拓扑，Zephyr 应用程序为清单仓库
- T3：森林拓扑，使用独立清单仓库

T1：星形拓扑，zephyr 为清单仓库
===============================

- zephyr 仓库作为中心仓库，在其 :file:`west.yml` 中指定 :ref:`modules`
- 与现有机制类比：以 zephyr 为超级项目的 Git 子模块

这是默认拓扑。主线 Zephyr 如何采用这种拓扑，见 :ref:`west-workspace`。

.. _west-t2:

T2：星形拓扑，应用程序为清单仓库
================================

- 适合专注于单个应用程序的开发者
- 包含 Zephyr 应用程序的仓库作为中心仓库，在其 :file:`west.yml` 中列出构建所需的其他项目，包括 zephyr 仓库和所有模块。
- 与现有机制类比：以应用程序为超级项目，以 zephyr 和其他项目为子模块的 Git 子模块

使用此拓扑的工作区如下：

.. code-block:: none

   west-workspace/
   │
   ├── application/         # .git/     │
   │   ├── CMakeLists.txt               │
   │   ├── prj.conf                     │  never modified by west
   │   ├── src/                         │
   │   │   └── main.c                   │
   │   └── west.yml         # main manifest with optional import(s) and override(s)
   │                                    │
   ├── modules/
   │   └── lib/
   │       └── zcbor/       # .git/ project from either the main manifest or some import.
   │
   └── zephyr/              # .git/ project
       └── west.yml         # This can be partially imported with lower precedence or ignored.
                            # Only the 'manifest-rev' version can be imported.


以下 :file:`application/west.yml` 示例使用 west 0.7 起提供的 :ref:`west-manifest-import`，将 Zephyr v2.5.0 及其模块导入应用程序清单文件：

.. code-block:: yaml

   # Example T2 west.yml, using manifest imports.
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v2.5.0
         import: true
     self:
       path: application

采用这种 ``import:`` 用法时，仍然可以选择性“覆盖”单个 Zephyr 模块；示例见 :ref:`west-manifest-ex1.3`。

另一种实现方式是将 :file:`zephyr/west.yml` 复制粘贴到 :file:`application/west.yml`，并为 zephyr 项目本身添加条目，如下所示：

.. code-block:: yaml

   # Equivalent to the above, but with manually maintained Zephyr modules.
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     defaults:
       remote: zephyrproject-rtos
     projects:
       - name: zephyr
         revision: v2.5.0
         west-commands: scripts/west-commands.yml
       - name: net-tools
         revision: some-sha-goes-here
         path: tools/net-tools
       # ... other Zephyr modules go here ...
     self:
       path: application

（``west-commands`` 用于 :ref:`west-build-flash-debug` 及其他 Zephyr 专用 :ref:`west-extensions`。使用 ``import`` 时不需要它。）

使用 ``import`` 的主要优点是无需单独跟踪导入项目的修订版本。在上例中，使用 ``import`` 意味着 Zephyr 的 :ref:`模块 <modules>` 版本会自动根据 :file:`zephyr/west.yml` 的修订版本确定，无需分别复制粘贴并维护。

T3：森林拓扑
============

- 适合需要支持多个独立应用程序，或没有“中心”仓库的下游发行版的开发者
- 专用清单仓库不包含 Zephyr 源代码，而是列出一组处于同一“层级”的项目
- 与现有机制类比：基于 Google repo 的源码分发

使用此拓扑的工作区如下：

.. code-block:: none

   west-workspace/
   ├── app1/               # .git/ project
   │   ├── CMakeLists.txt
   │   ├── prj.conf
   │   └── src/
   │       └── main.c
   ├── app2/               # .git/ project
   │   ├── CMakeLists.txt
   │   ├── prj.conf
   │   └── src/
   │       └── main.c
   ├── manifest-repo/      # .git/ never modified by west
   │   └── west.yml        # main manifest with optional import(s) and override(s)
   ├── modules/
   │   └── lib/
   │       └── zcbor/      # .git/ project from either the main manifest or
   │                       #       from some import
   │
   └── zephyr/             # .git/ project
       └── west.yml        # This can be partially imported with lower precedence or ignored.
                           # Only the 'manifest-rev' version can be imported.

以下 T3 :file:`manifest-repo/west.yml` 示例使用 west 0.7 起提供的 :ref:`west-manifest-import`，导入 Zephyr v2.5.0 及其模块，然后添加 ``app1`` 和 ``app2`` 项目：

.. code-block:: yaml

   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
       - name: your-git-server
         url-base: https://git.example.com/your-company
     defaults:
       remote: your-git-server
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v2.5.0
         import: true
       - name: app1
         revision: SOME_SHA_OR_BRANCH_OR_TAG
       - name: app2
         revision: ANOTHER_SHA_OR_BRANCH_OR_TAG
     self:
       path: manifest-repo

也可以像 :ref:`上文 <west-t2>` 的 T2 拓扑一样，通过复制粘贴 :file:`zephyr/west.yml` 手动实现，注意事项相同。

.. _workspace-as-git-repo:

不支持：将工作区顶层目录用作 .git 仓库
**************************************

有些用户希望将工作区 :ref:`顶层目录 <west-workspace>` 作为 Git 仓库，例如：

.. code-block:: none

   my-workspace/                  # workspace topdir
   ├── .git/                      # puts the entire workspace in a git repository
   ├── .west/                     # marks the location of the topdir
   └── [ ... other projects ...]

这 **不是** 官方支持的拓扑。West 在设计上假定工作区顶层目录本身不是 Git 仓库。

你或许能让类似布局满足自己的需要并“正常工作”，但 west 的后续版本可能引入破坏此配置的改动。
