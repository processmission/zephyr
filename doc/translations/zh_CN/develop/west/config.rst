.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-config:

配置
####

本页介绍 west 的配置文件系统、``west config`` 命令，以及内置命令使用的配置选项。``west.configuration`` 模块的 API 文档见 :ref:`west-apis-configuration`。

West 配置文件
-------------

West 的配置文件使用类似 INI 的语法，示例如下：

.. code-block:: ini

   [manifest]
   path = zephyr

   [zephyr]
   base = zephyr

上例中，``manifest`` 节的 ``path`` 选项设置为 ``zephyr``。也可以说，此文件中的 ``manifest.path`` 为 ``zephyr``。

配置文件分为三种：

1. **系统**：此文件中的设置影响计算机上所有登录用户运行 west 时的行为。位置取决于平台：

   - Linux：:file:`/etc/westconfig`
   - macOS：:file:`/usr/local/etc/westconfig`
   - Windows：:file:`%PROGRAMDATA%\\west\\config`

2. **全局** （每用户）：此文件中的设置影响计算机上特定用户运行 west 时的行为。

   - 所有平台：默认使用用户主目录下的 :file:`.westconfig`。
   - Linux 注意事项：如果设置了环境变量 ``XDG_CONFIG_HOME``，则使用 :file:`$XDG_CONFIG_HOME/west/config`。
   - Windows 注意事项：按以下顺序检查环境变量以确定主目录：``%HOME%``、``%USERPROFILE%``，最后是 ``%HOMEDRIVE%`` 与 ``%HOMEPATH%`` 的组合。

3. **本地**：此文件中的设置影响当前 :term:`west workspace` 中 west 的行为。文件为相对于工作区根目录的 :file:`.west/config`。

列表中靠后文件中的设置会覆盖前面文件中的设置。例如，系统配置文件中的 ``color.ui`` 为 ``true``，而工作区配置文件中为 ``false``，最终值就是 ``false``。同理，用户配置文件中的设置会覆盖系统设置，依此类推。

.. _west-config-cmd:

west config
-----------

内置 ``config`` 命令用于获取和设置配置值。可以向 ``west config`` 传入 ``--system``、``--global`` 或 ``--local``，指定要使用的配置文件。这些选项一次只能使用一个。如果均未指定，写入默认使用 ``--local``，读取则显示应用覆盖规则后的最终值。

下面给出常见用法示例；详细帮助可运行 ``west config -h``，内置选项的更多说明见 :ref:`west-config-index`。

将 ``manifest.path`` 设置为 :file:`some-other-manifest`：

.. code-block:: console

   west config manifest.path some-other-manifest

这样设置后，``west update`` 等命令会在相对于工作区根目录的 :file:`some-other-manifest` 目录中查找 :term:`west manifest`，而不是在传给 ``west init`` 的目录中查找，因此请谨慎操作！

读取 ``zephyr.base``：如果调用环境未设置 ``ZEPHYR_BASE``，就会使用此值（同样相对于工作区根目录）：

.. code-block:: console

   west config zephyr.base

可以使用以下命令切换到另一个 zephyr 仓库，而不改变 ``manifest.path``，因此也不会改变 ``west update`` 等命令的行为：

.. code-block:: console

   west config zephyr.base some-other-zephyr

如果使用 ``git worktree`` 等命令创建自己的 zephyr 目录，并希望 ``west build`` 等命令使用它们，而不是清单指定的 zephyr 仓库，这会很有用。（运行 ``west config zephyr.base zephyr`` 可以恢复使用上游清单中的目录。）

将全局（用户级）配置文件中的 ``color.ui`` 设为 ``false``，使该用户在任何工作区运行 west 时都不再输出彩色文本：

.. code-block:: console

   west config --global color.ui false

撤销上述修改：

.. code-block:: console

   west config --global color.ui true

.. _west-config-index:

内置配置选项
------------

下表说明 west 内置命令支持的配置选项。Zephyr 扩展命令支持的选项记录在各命令对应的页面中。

.. NOTE: docs authors: keep this table sorted by section, then option.

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - 选项
     - 描述
   * - :samp:`alias.{ALIAS}`
     - 字符串。如果非空，``<ALIAS>`` 就可以作为 west 命令使用。参见 :ref:`west-aliases`。
   * - ``color.ui``
     - 布尔值。如果为 ``true`` （默认值），且 stdout 是终端，west 会输出彩色文本。
   * - ``commands.allow_extensions``
     - 布尔值，默认为 ``true``；设置为 ``false`` 会禁用 :ref:`west-extensions`。
   * - ``grep.color``
     - 字符串，默认为空。设为 ``never`` 可禁用 ``west grep`` 的彩色输出。如果已设置，``west grep`` 会将其值传给 grep 工具的 ``--color`` 选项。
   * - ``grep.tool``
     - 字符串，可取 ``"git-grep"`` （默认值）、``"ripgrep"`` 或 ``"grep"``，指定 ``west grep`` 应使用的 grep 工具。
   * - ``grep.<TOOL>-args``
     - 字符串，默认为空。``<TOOL>`` 部分可以替换为任意 ``grep.tool`` 值，例如 ``grep.ripgrep-args`` 就是一个配置选项。如果已设置，它指定 ``west grep`` 应传给相应 grep 工具的参数。详情可运行 ``west help grep``。
   * - ``grep.<TOOL>-path``
     - 字符串，默认为空。``<TOOL>`` 部分可以替换为任意 ``grep.tool`` 值，例如 ``grep.ripgrep-path`` 就是一个配置选项。它指定 ``west grep`` 应使用的相应工具路径，以代替搜索命令。详情可运行 ``west help grep``。
   * - ``manifest.file``
     - 字符串，默认为 ``west.yml``。指定从清单仓库根目录到清单文件的相对路径，供 ``west init`` 及其他解析清单的命令使用。
   * - ``manifest.group-filter``
     - 字符串，默认为空。以逗号分隔，列出要在工作区中启用和禁用的项目组。启用的组以 ``+`` 为前缀，禁用的组以 ``-`` 为前缀。例如，``"+foo,-bar"`` 启用组 ``foo``，禁用组 ``bar``。参见 :ref:`west-manifest-groups`。
   * - ``manifest.path``
     - 字符串，指定从 :term:`west workspace` 根目录到清单仓库的相对路径，供 ``west update`` 及其他解析清单的命令使用。由 ``west init`` 在本地设置。
   * - ``manifest.project-filter``
     - 以逗号分隔的字符串列表。

       该选项的值是以逗号分隔的正则表达式列表，每个表达式均以 ``+`` 或 ``-`` 为前缀，如下所示：

       .. code-block:: none

          +re1,-re2,-re3

       项目名称按顺序与列表中的各正则表达式（``re1``、``re2``、``re3`` 等）匹配。如果整个项目名称匹配某个表达式，该列表项就会停用或激活此项目。项目是否停用取决于列表项是否以 ``-`` 开头；以 ``+`` 开头则激活。（使用此选项时，项目名称不能包含 ``,``，因此正则表达式无需包含字面量 ``,`` 字符。）

       如果项目名称匹配列表中的多个正则表达式，使用最后一个匹配表达式的结果。例如，若 ``manifest.project-filter`` 为：

       .. code-block:: none

          -hal_.*,+hal_foo

       则名为 ``hal_bar`` 的项目处于非活动状态，而名为 ``hal_foo`` 的项目处于活动状态。

       如果列表项将某项目停用或激活，那么无论其部分或全部组是否被禁用，项目都会保持该项指定的活动状态。（目前，这是使不属于任何组的项目变为非活动状态的唯一方式。）

       否则，即项目未匹配列表中的任何正则表达式时，其活动状态按项目组相关的通常规则确定（此类示例见 :ref:`west-project-group-examples`）。

       ``manifest.project-filter`` 列表项的前导和末尾空白会被忽略。因此以下示例值等效：

       .. code-block:: none

          +foo,-bar
          +foo , -bar

       空列表项会被忽略。因此以下示例值等效：

       .. code-block:: none

           +foo,,-bar
           +foo,-bar

   * - ``update.auto-cache``
     - 字符串。如果非空，且命令行未指定 ``--auto-cache``，``west update`` 会将此值用作该选项的值。
   * - ``update.fetch``
     - 字符串，可取 ``"smart"`` （从 v0.6.1 起的默认行为）或 ``"always"`` （此前的行为）。设为 ``"smart"`` 时，如果项目在清单中的修订版本是本地已有的 SHA 或标签，:ref:`west-update` 命令会跳过从其远程仓库获取的操作。``"always"`` 则无条件从远程仓库获取。
   * - ``update.name-cache``
     - 字符串。如果非空，且命令行未指定 ``--name-cache``，``west update`` 会将此值用作该选项的值。
   * - ``update.narrow``
     - 布尔值。如果为 ``true``，``west update`` 的行为如同在命令行指定了 ``--narrow``。默认为 ``false``。
   * - ``update.path-cache``
     - 字符串。如果非空，且命令行未指定 ``--path-cache``，``west update`` 会将此值用作该选项的值。
   * - ``update.sync-submodules``
     - 布尔值。如果为 ``true`` （默认值），:ref:`west-update` 会先同步 Git 子模块，再更新它们。
   * - ``zephyr.base``
     - 字符串，指定 west 命令运行期间为 :envvar:`ZEPHYR_BASE` 环境变量设置的默认值。默认情况下，``west init`` 会将它设置为清单中路径为 :file:`zephyr` 的项目的路径（如果存在）。如果环境变量已设置，则忽略此配置，除非 ``zephyr.base-prefer`` 为 ``"configfile"``。
   * - ``zephyr.base-prefer``
     - 字符串，可取 ``"env"`` 和 ``"configfile"``。设为 ``"env"`` （默认值）时，调用环境中的 :envvar:`ZEPHYR_BASE` 会覆盖 ``zephyr.base`` 配置选项；设为 ``"configfile"`` 时，则配置选项优先。
