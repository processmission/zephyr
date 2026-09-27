.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-basics:

基础知识
########

本页介绍 west 的基本概念，并提供进一步阅读的参考。

West 的内置命令让你可以在同一个 :term:`工作区 <west workspace>` 目录下操作多个 :term:`项目 <west project>` （Git 仓库）。

West 的工作方式如下：``west init`` 命令创建 :term:`west workspace` 并克隆 :term:`清单仓库 <west manifest repository>`；``west update`` 命令则在首次运行时克隆、之后更新清单中列出的工作区 :term:`项目 <west project>`。

工作区示例
**********

如果已按照 :ref:`getting_started` 操作，本地 :term:`west workspace` （此例中为名为 :file:`zephyrproject` 的文件夹及其全部子文件夹）的结构如下：

.. code-block:: none

   zephyrproject/                 # west topdir
   ├── .west/                     # marks the location of the topdir
   │   └── config                 # per-workspace local configuration file
   │
   │   # The manifest repository, never modified by west after creation:
   ├── zephyr/                    # .git/ repo
   │   ├── west.yml               # manifest file
   │   └── [... other files ...]
   │
   │   # Projects managed by west:
   ├── modules/
   │   └── lib/
   │       └── zcbor/             # .git/ project
   ├── tools/
   │   └── net-tools/             # .git/ project
   └── [ ... other projects ...]

.. _west-workspace:

工作区概念
**********

以下是理解此结构所需的基本概念。更多详情见 :ref:`west-workspaces`。

topdir
  上例中，:file:`zephyrproject` 是工作区顶层目录的名称，即 *topdir*。（:file:`zephyrproject` 只是示例名称，也可以是 ``z``、``my-zephyr-workspace`` 等任何名称。）

  通常通过 :ref:`west init <west-init-basics>` 创建顶层目录及其他几个文件和目录。

.west 目录
  顶层目录包含 :file:`.west` 目录。West 需要查找顶层目录时，会搜索 :file:`.west` 并使用其父目录。搜索从当前工作目录开始；如果失败，则退回到 :envvar:`ZEPHYR_BASE` 环境变量指定的位置，重新搜索。

配置文件
  :file:`.west/config` 是工作区的 :ref:`本地配置文件 <west-config>`。

清单仓库
  每个 west 工作区恰好包含一个 *清单仓库*，即包含 *清单文件* 的 Git 仓库。清单仓库的位置由本地配置文件中的 :ref:`manifest.path 配置选项 <west-config-index>` 指定。

  对于上游 Zephyr，:file:`zephyr` 是清单仓库，但可以配置 west，将工作区中的任意 Git 仓库用作清单仓库。唯一要求是其中包含有效的清单文件。其他选择见 :ref:`west-topologies`，清单文件格式的详细说明见 :ref:`west-manifests`。

清单文件
  清单文件是定义 *项目* 的 YAML 文件；这些项目是工作区中由 west 管理的附加 Git 仓库。清单文件默认名为 :file:`west.yml`，可通过本地配置选项 ``manifest.file`` 覆盖。

  使用 :ref:`west update <west-update-basics>` 命令，根据清单文件内容更新工作区中的项目。

项目
  项目是由 west 管理的 Git 仓库。项目在清单文件中定义，可位于工作区内部任意位置。在上述工作区示例中，``zcbor`` 和 ``net-tools`` 都是项目。

  默认情况下，Zephyr :ref:`构建系统 <build_overview>` 使用 west 获取工作区中所有项目的位置，以便将其中的代码用作 :ref:`modules`。但请注意，模块与项目 :ref:`在概念上不同 <modules-vs-projects>`。

扩展
  West 已知的任何仓库（清单仓库或任意项目仓库）都可以定义 :ref:`west-extensions`。扩展是在使用该工作区时可运行的额外 west 命令。

  zephyr 仓库利用此功能提供 :ref:`west build <west-building>` 等 Zephyr 专用命令。将这些命令定义为扩展，使 west 核心不必了解各工作区使用的 Zephyr 版本等具体细节。

忽略的文件
  工作区可以包含不由 west 管理的其他 Git 仓库、文件和目录。除了 :file:`.west`、清单仓库，以及清单文件中指定的项目，west 基本上会忽略工作区内的所有内容。

west init 与 west update
************************

与工作区相关的两个最重要命令是 ``west init`` 和 ``west update``。

.. _west-init-basics:

``west init`` 基础
------------------

此命令创建 west 工作区。

.. important::

   运行 ``west init`` 后，west 不再修改清单仓库的内容。请使用常规 Git 命令拉取新版本等。

通常只需运行一次，如下所示：

.. code-block:: shell

   west init -m https://github.com/zephyrproject-rtos/zephyr --mr v2.5.0 zephyrproject

这将：

#. 创建顶层目录 :file:`zephyrproject`，以及其中的 :file:`.west` 和 :file:`.west/config`
#. 从 https://github.com/zephyrproject-rtos/zephyr 克隆清单仓库，放到 :file:`zephyrproject/zephyr`
#. 在本地 zephyr 克隆中检出 Git 标签 ``v2.5.0``
#. 在 :file:`.west/config` 中将 ``manifest.path`` 设置为 ``zephyr``
#. 将 ``manifest.file`` 设置为 ``west.yml``

工作区现在已基本就绪；只需运行 ``west update``，将其余项目克隆到工作区即可完成。

更多详情参见 :ref:`west-init`。

.. _west-update-basics:

``west update`` 基础
--------------------

此命令确保工作区中包含与清单文件所列项目相符的 Git 仓库。

.. important::

   每当在清单仓库中检出不同的修订版本，都应运行 ``west update``，确保工作区中包含新版本所需的项目仓库。

``west update`` 命令按以下步骤读取清单文件内容：

#. 找到顶层目录。在上面的 ``west init`` 示例中，即找到 :file:`zephyrproject`。
#. 加载顶层目录中的 :file:`.west/config`，读取 ``manifest.path`` （如 ``zephyr``）和 ``manifest.file`` （如 ``west.yml``）选项。
#. 加载这些选项指定的清单文件（例如 :file:`zephyrproject/zephyr/west.yml`）。

然后根据清单文件，确定缺失项目应放在工作区的什么位置、从哪些 URL 克隆，以及本地应检出哪些 Git 修订版本。对于已经存在的项目仓库，则在原位置获取并检出清单文件中各自对应的 Git 修订版本。

更多详情参见 :ref:`west-update`。

其他内置命令
************

参见 :ref:`west-built-in-cmds`。

.. _west-zephyr-extensions:

Zephyr 扩展
***********

有关 Zephyr 扩展命令的信息，参见以下页面：

- :ref:`west-build-flash-debug`
- :ref:`west-sign`
- :ref:`west-zephyr-ext-cmds`
- :ref:`west-shell-completion`

故障排查
********

参见 :ref:`west-troubleshooting`。
