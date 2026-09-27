.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-release-notes:

West 发行说明
#############

v1.5.0
******

主要变更：

- 新增自动缓存支持。向 ``west update`` 传入 ``--auto-cache <directory>`` 参数即可使用。

其他变更：

- 允许在 ``west update`` 中同时使用 ``--name-cache`` 和 ``--path-cache``。

- 在清单模式中记录默认修订版本值。

缺陷修复：

- 允许清单项目列表为空或缺失。

- 冻结或解析清单文件时，确保 ``manifest.group-filter`` 列表顺序具有确定性。

v1.4.0
******

变更：

- 允许向配置字符串追加数据。要向 ``<name>`` 的值追加内容，输入：``west config -a <name> <value>``。

- 为 ``west manifest`` 添加 ``--untracked`` 参数选项。在工作区中运行 ``west manifest --untracked``，可打印所有未被 west 跟踪或管理的文件和目录。

- 为 ``west list`` 添加 ``--inactive`` 参数选项，支持打印非活动项目。

- ``west manifest --resolve`` 和 ``west manifest --freeze`` 命令支持 ``--active-only`` 参数选项，因此可以冻结启用了项目或组过滤器的工作区。

API 变更：

- ``west.manifest.Manifest`` 的 ``as_dict()``、``as_frozen_dict()``、``as_yaml()`` 和 ``as_frozen_yaml()`` 方法现在接受可选参数 ``active_only`` （默认为 ``False``），用于返回包含全部项目或仅活动项目的对象。

v1.3.0
******

主要变更：

- 新增对 :ref:`west-aliases` 命令的支持。

- 采用 `pyproject TOML specification`_ 进行打包。

.. _pyproject TOML specification:
   https://packaging.python.org/en/latest/specifications/pyproject-toml/

其他变更：

- 新增子模块缓存支持。

- 默认将清单文件按 UTF-8 解码。

- 将 ``west diff`` 和 ``west status`` 的未知参数传给底层 ``git`` 命令。

- 为 ``west diff`` 添加 ``--manifest`` 参数，用于将当前工作区与清单修订版本比较。

- west forall 可以使用环境变量，已定义以下变量：

  - ``WEST_PROJECT_NAME``
  - ``WEST_PROJECT_PATH``
  - ``WEST_PROJECT_ABSPATH``
  - ``WEST_PROJECT_REVISION``
  - ``WEST_PROJECT_URL``
  - ``WEST_PROJECT_REMOTE``

- 支持提前处理参数 ``-q/--quiet``，以减少输出。

- 为 ``west init`` 添加 ``-o/--clone-opt`` 参数，用于传给 ``git clone``。

- 支持 Python 3.13，停止支持 Python 3.8。

- 禁止清单将项目放在 ``.west`` 目录中。

- 为 ``west init`` 添加 NTFS 兼容处理和 ``--rename-delay``。

- 在 ``-vvv`` 调试模式下调用 die 时打印堆栈跟踪。

缺陷修复：

- 使用 ``'backslashreplace'``，避免子进程输出格式错误的 UTF 数据时崩溃。

- 修复 ``west diff`` 对存在合并冲突的仓库的处理，同时改进错误输出和 ``git diff`` 返回码处理。

- 修复使用 Git 子模块时，``west manifest`` 命令的 ``--freeze`` 和 ``--resolve`` 行为。

v1.2.0
******

主要变更：

- 新增 ``west grep`` 命令，用于在 west 工作区的仓库中运行“grep 工具”。目前支持的工具包括 ``git grep``、`ripgrep`_ 和标准 ``grep``。

  要从所有已克隆的活动仓库中获取 ``git grep foo`` 的结果，运行：

  .. code-block:: console

     west grep foo

  以下是使用 ``west grep`` 运行不同 grep 命令的其他示例：

  .. list-table::

     * - ``git grep --untracked``
       - ``west grep --untracked foo``
     * - ``ripgrep``
       - ``west grep --tool ripgrep foo``
     * - ``grep --recursive``
       - ``west grep --tool grep foo``

  要切换工作区中的默认 grep 工具，运行下表中的相应命令：

  .. list-table::

     * - ``ripgrep``
       - ``west config grep.tool ripgrep``
     * - ``grep``
       - ``west config grep.tool grep``

  更多详情可运行 ``west help grep``。

其他变更：

- 清单文件格式现在支持在每个 ``projects:`` 元素中设置 ``description`` 字段。示例见 :ref:`west-manifests-projects`。

- ``west list --format`` 现在接受格式字符串中的 ``{description}``，用于打印项目的 ``description:`` 值。

- ``west compare`` 现在始终打印 :ref:`west-manifest-rev` 的相关信息。

缺陷修复：

- 如果目标目录已存在，``west init`` 会中止。

API 变更：

- ``west.commands.WestCommand`` 的 ``check_call()`` 和 ``check_output()`` 方法，现在接受可传给底层 subprocess 函数的任意关键字参数。

- ``west.commands.WestCommand.run_subprocess()``：新增对 ``subprocess.run()`` 的包装。由于 ``WestCommand`` 已有同名方法，因此不能命名为 ``run()``。

- ``west.commands.WestCommand`` 的 ``dbg()``、``inf()``、``wrn()`` 和 ``err()`` 方法现在均接受 ``end`` 关键字参数，并将其传给 ``print()``。

- ``west.manifest.Project`` 现在具有 ``description`` 属性，包含清单数据中 ``description:`` 字段解析后的值。

.. _ripgrep: https://github.com/BurntSushi/ripgrep#readme

v1.1.0
******

主要变更：

- ``west compare``：新增命令，将工作区状态与清单比较。

- 支持新的 ``manifest.project-filter`` 配置选项，详情见 :ref:`west-config-index`。设置此选项时，目前不能使用 ``west manifest --freeze`` 和 ``west manifest --resolve`` 命令。此限制可能在后续版本中移除。

- 项目名称包含逗号（``,``）或空白时，现在会产生警告。如果设置了新的 ``manifest.project-filter`` 配置选项，这些警告会变为错误。未来 west 的主要版本可能将这些警告统一提升为错误。

其他变更：

- ``west forall`` 现在接受 ``--group`` 参数，可将命令限制为只在一个或多个组中运行。详情可运行 ``west help forall``。

- 所有 west 命令现在都会输出 west API 模块产生的警告及以上级别日志。此外，向 west 传入一次 ``--verbose`` 参数，会包含各命令的信息级消息；传入两次，则包含调试消息。

缺陷修复：

- 改进了多处错误消息、调试日志和错误处理。

API 变更：

- ``west.manifest.Manifest.is_active()`` 现在遵循 ``manifest.project-filter`` 配置选项的值。

v1.0.1
******

主要变更：

- 此版本开始支持清单模式版本“1.0”。其功能与“0.13”完全相同，但不希望使用“0.x”清单“version:”字段的应用可以采用它。此功能详情见 :ref:`west-manifest-schema-version`。

缺陷修复：

- West 收到中断信号时，不再以成功状态码退出，而是返回平台特定的错误码，向调用环境表明进程被中断。

v1.0.0
******

此版本的主要变更：

- :ref:`west-apis` 现已声明为稳定。任何破坏兼容性的变更，都会通过主版本从 v1.x.y 升至 v2.x.y 来表达。

- West v1.0 不再适用于 Zephyr v1.14 LTS。该长期支持版本早已被 Zephyr v2.7 LTS 取代。如果必须使用 Zephyr v1.14，需要使用 west v0.14 或更早版本。

- 与 Zephyr 其他部分一致，west 现在要求 Python v3.8 或更高版本

- West 命令不再接受缩写命令行参数。例如，现在必须指定 ``west update --keep-descendants``，不能使用 ``west update --keep-d`` 等缩写。这是针对 Zephyr 全部 Python 脚本命令行接口的统一改动。当命令新增与现有选项名称相似但行为不同的选项时，缩写在实践中会产生问题。

其他变更：

- 所有 west 内置函数均已停止使用 ``west.log``

- ``west update``：新增 ``--submodule-init-config`` 选项。详情见提交 `9ba92b05`_。

缺陷修复：

- 加载失败的 west 扩展命令有时会输出堆栈。此问题已修复，现在会打印合理的错误消息。

- ``west config`` 现在会拒绝选项名称中缺少 ``.`` 的无效配置选项参数

API 变更：

- west 包现在包含一些静态分析器（如 `mypy`_）自动发现其类型标注所需的元数据文件。详情见提交 `d9f00e24`_。

- 移除了为兼容 Zephyr v1.14 LTS 而保留的已弃用 ``west.build`` 模块

- 移除了为兼容 Zephyr v1.14 LTS 而保留的已弃用 ``west.cmake`` 模块

- ``west.log`` 模块现已弃用。此模块使用全局状态，在多个不同 Python 模块可能依赖它作为 API 时，使用起来不够方便。

- :ref:`west-apis-commands` 模块新增一些 API，为后续对命令输出添加全局详细程度控制，以及移除 ``west`` 包 API 中的全局状态打下基础：

  - ``west.commands.WestCommand.__init__()`` 新增关键字参数：``verbosity``
  - ``west.commands.WestCommand`` 新增属性：``color_ui``
  - ``west.commands.WestCommand`` 新增方法，扩展命令应使用这些方法输出信息，而不是直接写入 sys.stdout 或 sys.stderr：``inf()``、``wrn()``、``err()``、``die()``、``banner()``、``small_banner()``
  - 新增 ``west.commands.VERBOSITY`` 枚举

.. _9ba92b05: https://github.com/zephyrproject-rtos/west/commit/9ba92b054500d75518ff4c4646590bfe134db523
.. _d9f00e24: https://github.com/zephyrproject-rtos/west/commit/d9f00e242b8cb297b56e941982adf231281c6bae
.. _mypy: https://www.mypy-lang.org/

v0.14.0
*******

缺陷修复：

- 使用错误的本地配置文件运行 west 命令时，过去会输出令人困惑的堆栈。此问题已修复，现在会打印合理的错误消息。

- 修复了 west 查找 zephyr 仓库方式中的缺陷。该缺陷通常出现在新工作区第一次运行 ``west build`` 等扩展命令时：除非从工作区顶层目录运行，否则首次调用会失败，而后续调用不会。

- 用户无权打开清单文件时，west 现在会打印合理的错误消息，而不是输出堆栈跟踪。

API 变更：

- ``west.manifest.MalformedConfig`` 异常类型已移至 ``west.configuration`` 模块

- ``west.manifest.MalformedConfig`` 异常类型已移至 :ref:`west.configuration <west-apis-configuration>` 模块

- ``west.configuration.Configuration`` 类在某些情况下现在会抛出 ``MalformedConfig``，而非 ``RuntimeError``

v0.13.1
*******

缺陷修复：

- 在工作区外调用 west.manifest.Manifest.from_file() 时，west 再次支持退回使用 ZEPHYR_BASE 环境变量定位工作区。

v0.13.0
*******

新功能：

- 现在可以在 ``manifest: self: userdata:`` 值中，将任意用户数据关联到清单仓库本身，例如：

  .. code-block:: YAML

     manifest:
       self:
         userdata: <any YAML value can go here>

缺陷修复：

- 在 [issue #572](https://github.com/zephyrproject-rtos/west/issues/572) 所述的特定情况下，west 报告的清单仓库路径可能不正确。此问题已随 ``west.manifest`` API 模块中更大范围的路径处理改进一并修复。

- 修复了 ``west.Manifest.ManifestProject.__repr__`` 的返回值

:ref:`API <west-apis>` 变更：

- ``west.configuration.Configuration``：新增面向对象的当前配置接口。它反映系统、全局和工作区本地配置值，并允许读取、写入和删除任意或所有位置的配置选项。

- ``west.commands.WestCommand``：

  - ``config``：新增属性，返回 ``Configuration`` 对象；如果未设置，则中止程序。此属性始终可在扩展命令的 ``do_run()`` 实现中使用。
  - ``has_config``：新增布尔属性，当且仅当读取 ``self.config`` 会中止程序时为 ``True``。

- ``west.manifest`` 包的路径处理经过了不向后兼容的重构。更多详情见提交 [56cfe8d1d1](https://github.com/zephyrproject-rtos/west/commit/56cfe8d1d1f3c9b45de3e793c738acd62db52aca)。

- ``west.manifest.Manifest.validate()``：现在以 Python dict 返回验证后的数据。当传入值为 str，而需要 dict 时，这会很有用。

- ``west.manifest.Manifest`` 新增：

  - 路径属性 ``abspath``、``posixpath``、``relative_path``、``yaml_path``、``repo_path``、``repo_posixpath``
  - ``userdata`` 属性，包含 ``manifest: self: userdata:`` 解析后的值，或为 None
  - ``from_topdir()`` 工厂方法

- ``west.manifest.ManifestProject``：新增 ``userdata`` 属性，同样包含 ``manifest: self: userdata:`` 解析后的值，或为 None

- ``west.manifest.ManifestImportFailed``：构造函数现在接受任意值，可用于表示从 :ref:`映射 <west-manifest-import-map>` 或其他复合值导入失败。

- 已弃用的配置 API：

  以下 API 现已弃用，应改用 ``Configuration`` 对象。通常通过 ``WestCommand`` 实例的 ``self.config`` 使用，也可直接实例化 ``Configuration`` 对象满足其他用途。

  - ``west.configuration.config``
  - ``west.configuration.read_config``
  - ``west.configuration.update_config``
  - ``west.configuration.delete_config``

v0.12.0
*******

新功能：

- West 现在可在 `MSYS2 <https://www.msys2.org/>`_ 平台运行。

- West 清单文件现在可以包含与各项目关联的任意用户数据。详情见 :ref:`west-project-userdata`。

缺陷修复：

- 修复了 ``west list`` 命令对清单仓库使用 ``{sha}`` 格式键的行为；现在会按预期打印 ``N/A`` （“不适用”）。

:ref:`API <west-apis>` 变更：

- 新增 ``west.manifest.Project.userdata`` 属性，支持项目用户数据。

v0.11.1
*******

新功能：

- ``west status`` 现在只为状态非空的项目打印输出。

缺陷修复：

- 清单文件解析器此前错误地允许项目名称包含路径分隔符 ``/`` 和 ``\``，现在会拒绝这些无效字符。

  注意：如果需要将项目放在工作区顶层目录的子目录中，使用 ``path:`` 键。如果需要定制相对于远程 ``url-base:`` 的项目获取 URL，使用 ``repo-path:``。示例见 :ref:`west-manifests-projects`。

- west v0.10.1 对 ``west init --manifest-rev`` 选项的改动会选择默认分支名称，但使清单仓库处于分离 HEAD 状态。现已通过在内部使用 ``git clone`` 代替 ``git init`` 和 ``git fetch`` 修复。详情见 `issue #522`_。

- ``WEST_CONFIG_LOCAL`` 环境变量现在可以正确覆盖默认位置 :file:`<workspace topdir>/.west/config`。

- ``west update --fetch=smart`` （``smart`` 为默认值）现在会正确跳过项目修订版本为 `lightweight tags`_ 时的获取操作（带注释标签原本就正常，只有轻量标签会被不必要地获取）。

其他变更：

- 上文提到的 issue #522 修复引入了新的限制。如果指定 ``west init --manifest-rev`` 选项，其值现在必须是分支或标签。尤其是，之前可用于获取拉取请求的“伪分支”，例如 GitHub 的 ``pull/1234/head`` 引用，不能再传给 ``--manifest-rev``。用户现在必须在运行 ``west init`` 后手动获取并检出这些修订版本。

:ref:`API <west-apis>` 变更：

- ``west.manifest.Manifest.get_projects()`` 避免了 `issue #523`_ 所述某些边界情况下的错误结果。

- ``west.manifest.Project.sha()`` 现在能正确处理标签修订版本，包括轻量标签和带注释标签。

.. _lightweight tags: https://git-scm.com/book/en/v2/Git-Basics-Tagging
.. _issue #522: https://github.com/zephyrproject-rtos/west/issues/522
.. _issue #523: https://github.com/zephyrproject-rtos/west/issues/523

v0.11.0
*******

新功能：

- ``west update`` 现在支持 ``--narrow``、``--name-cache`` 和 ``--path-cache`` 选项，分别受 ``update.narrow``、``update.name-cache`` 和 ``update.path-cache`` :ref:`west-config` 选项影响，可用于优化更新速度。
- ``west update`` 现在支持 ``--fetch-opt`` 选项，其值会传给更新各项目时用于获取远程修订版本的 ``git fetch`` 命令。

缺陷修复：

- ``west update`` 现在默认同步项目中的 Git 子模块，避免清单文件中的 URL 自子模块首次初始化后发生变化时出现问题。将 ``update.sync-submodules`` 配置选项设为 ``false`` 可禁用此行为。

其他变更：

- 修复了 :ref:`west-apis-manifest` 模块中 Project 类的文档字符串

v0.10.1
*******

新功能：

- :ref:`west-init` 命令的 ``--manifest-rev`` （``--mr``）选项不再默认为 ``master``。命令会查询仓库默认分支名称并使用它。因此，用户可以从 ``master`` 迁移到 ``main``，而不会破坏未指定此选项的脚本。

.. _west_0_10_0:

v0.10.0
*******

新功能：

- 项目 :ref:`子模块列表 <west-manifest-submodules>` 中的 ``name`` 键现在是可选的。

缺陷修复：

- West 现在检查清单模式版本是否为 :ref:`west-manifest-schema-version` 中明确允许的值。旧行为仅检查模式版本是否晚于引入 ``manifest: version:`` 键的 west 版本，因此错误地允许了 ``0.8.2`` 等无效模式版本。

其他变更：

- 清单文件的 ``group-filter`` 现在会通过 ``import`` 传播。这与 west v0.9.x 的处理方式不同：在 v0.9.x 中，只有顶层清单文件的 ``group-filter`` 生效，所有导入清单中的组过滤列表都会被忽略。

  从 west v0.10.0 起，导入清单中的组过滤列表也会被导入。详情见 :ref:`west-group-filter-imports`。

  未指定 ``manifest: version:``，或其值至少为 ``0.10`` 时，新行为生效。只有在顶层清单文件中显式指定 ``manifest: version: 0.9``，才能继续使用旧行为。模式版本的更多信息见 :ref:`west-manifest-schema-version`。

  此变更的动机及更多背景，参见 `west pull request #482 <https://github.com/zephyrproject-rtos/west/pull/482>`_。

v0.9.1
******

缺陷修复：

- ``west manifest --resolve`` 等命令现在会正确包含组和组过滤信息。

其他变更：

- 同时使用 ``import`` 与 ``group-filter`` 时，west 现在会发出警告。此组合的语义从 v0.10.x 起发生变化，更多信息见上面的 v0.10.0 发行说明。

.. _west_0_9_0:

v0.9.0
******

.. warning::

   下文所述的 ``west config`` 修复有一个代价：通过此命令或 ``west.configuration`` API 设置配置选项时，配置文件中的所有注释和其他手动编辑内容都会被移除。

.. warning::

   不建议将此版本引入的 ``group-filter`` 功能与清单导入结合使用。相应行为已在 west v0.10 中改变。

新功能：

- West 清单现在支持 :ref:`west-manifest-submodules`。除克隆项目仓库本身外，还可以将 `Git submodules <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`_ 克隆到 west 项目仓库中。

- West 清单现在支持 :ref:`west-manifest-groups`。可以通过启用或禁用项目组，决定哪些项目处于“活动”状态，从而由以下命令处理：``west update``、``west list``、``west diff``、``west status``、``west forall``。

- ``west update`` 默认不再更新非活动项目。现在支持 ``--group-filter`` 选项，可对启用和禁用的项目组集合进行一次性调整。

- 不带参数运行 ``west list``、``west diff``、``west status`` 或 ``west forall`` 时，默认不再打印非活动项目信息。如果用户在命令行显式指定项目列表，则无论项目是否活动，都会包含其输出。

  这些命令现在还支持 ``--all`` 参数，以包含所有项目，包括非活动项目。

- ``west list`` 的 ``--format`` 参数现在支持 ``{groups}`` 格式字符串键。

缺陷修复：

- ``west config`` 命令和 ``west.configuration`` API 此前无法正确保存某些配置值，例如包含逗号的字符串。此问题已修复，详情见 `commit 36f3f91e <https://github.com/zephyrproject-rtos/west/commit/36f3f91e270782fb05f6da13800f433a9c48f130>`_。

- ``manifest: self: path:`` 为空的清单文件无效，但 west 过去会静默接受。现在会拒绝此类清单。

- 修复了影响 ``west init -l .`` 命令行为的缺陷，见 `issue #435 <https://github.com/zephyrproject-rtos/west/issues/435>`_。

:ref:`API <west-apis>` 变更：

- 新增 ``west.manifest.Manifest.is_active()``
- 新增 ``west.manifest.Manifest.group_filter``
- 为 ``west.manifest.Project`` 新增 ``submodules`` 属性，其类型为新添加的 ``west.manifest.Submodule``

其他变更：

- :ref:`west-manifest-import` 功能现在支持术语 ``allowlist`` 和 ``blocklist``，分别代替 ``whitelist`` 和 ``blacklist``。

  为保持兼容性，旧术语仍受支持，但文档已全部更新为新术语。

v0.8.0
******

这是一个功能版本，通过在 ``import:`` 映射中支持 ``path-prefix:`` 键扩展清单模式，同时包含其他功能和修复。

- 清单导入映射现在支持 ``path-prefix:`` 键，可将项目及其导入的仓库放到工作区的子目录中。示例见 :ref:`west-manifest-ex3.4`。
- 现在还可通过 ``python3 -m west`` 运行 west 命令行应用程序，从而无需修改 :envvar:`PATH` 环境变量，就能更方便地使用指定 Python 解释器运行 west。
- :ref:`west manifest --path <west-manifest-path>` 打印 west.yml 的绝对路径
- ``west init`` 现在支持 ``--mf foo.yml`` 选项，使用 :file:`foo.yml` 而不是 :file:`west.yml` 初始化工作区。
- ``west list`` 现在根据 ``manifest.path`` :ref:`配置选项 <west-config>` 打印清单仓库路径，该路径可能与清单数据中的 ``self: path:`` 值不同。旧行为仍可使用，但需要传入新选项 ``--manifest-path-from-yaml``。
- 多项 Python API 变更，详情见 :ref:`west-apis`。

v0.7.3
******

这是一个缺陷修复版本。

- 修复了导入失败可能导致工作区不可用的问题（详情见 [PR #415](https://github.com/zephyrproject-rtos/west/pull/415)）

v0.7.2
******

这是一个包含缺陷修复和小型新功能的版本。

- 过滤清单导入带来的重复扩展命令
- 修复 ``west.Manifest.get_projects()`` 按路径查找清单仓库的行为

v0.7.1
******

这是一个包含缺陷修复和小型新功能的版本。

- ``west update --stats`` 现在会打印调用子进程的操作耗时、每个项目在 west Python 进程中花费的时间，以及更新每个项目的总耗时。
- ``west topdir`` 始终打印 POSIX 风格路径
- 控制台输出的小幅调整

v0.7.0
******

west 0.7 面向用户的主要新功能是 :ref:`west-manifest-import`。它允许用户从多个不同文件加载 west 清单数据，并将结果解析为单个逻辑清单。

其他用户可见变更：

- 本文档及 west API 文档中的“west installation”概念已更名为“west workspace”。对大多数人而言，新术语似乎比旧术语更容易理解和使用。
- West 清单现在支持 :ref:`模式版本 <west-manifest-schema-version>`。
- “west config”命令现在可在工作区之外运行，例如通过 ``west config --global section.key value`` 全局设置配置选项。
- 新增 :ref:`west topdir <west-built-in-misc>` 命令，用于打印当前 west 工作区的根目录。
- ``west -vv init`` 命令现在会打印正在执行的 Git 操作及其结果。
- 现在强制禁止将项目命名为“manifest”；该名称保留给清单仓库，可在 ``west list manifest`` 等命令中使用，不再只能通过 ``west list path-to-manifest-repository`` 指代它
- 不存在名为“zephyr”的项目时不再报错。这是为了让 west 也能通用于非 Zephyr 场景。
- 多项缺陷修复。

:ref:`west-apis` 中面向开发者的变更如下：

- west.build 和 west.cmake：已弃用；这些功能专用于 Zephyr，本不应属于 west。由于 Zephyr v1.14 LTS 依赖它们，仍将随发行包提供，直到该 Zephyr 版本淘汰时移除。
- west.commands：

  - WestCommand.requires_installation：已弃用，改用 requires_workspace
  - WestCommand.requires_workspace：新增
  - WestCommand.has_manifest：新增
  - WestCommand.manifest：现在可设置
- west.configuration：调用者现在可以在读取和写入配置文件时指定工作区目录
- west.log：

  - msg()：新增
- west.manifest：

  - 该模块现在使用标准 logging 模块，而不是 west.log
  - QUAL_REFS_WEST：新增
  - SCHEMA_VERSION：新增
  - Defaults：已移除
  - Manifest.as_dict()：新增
  - Manifest.as_frozen_yaml()：新增
  - Manifest.as_yaml()：新增
  - Manifest.from_file() 和 from_data()：这些工厂方法使用更灵活，对全局状态的依赖更少
  - Manifest.validate()：新增
  - ManifestImportFailed：新增
  - ManifestProject：部分弃用，之后可能移除。
  - Project：构造函数现在接受 topdir 参数
  - Project.format() 及其调用者已移除，请改用 f-string。
  - Project.name_and_path：新增
  - Project.remote_name：新增
  - Project.sha() 现在会捕获 stderr
  - Remote：已移除

West 现在要求 Python 3.6 或更高版本。此外，某些功能可能依赖 Python 字典保持插入顺序；这在 CPython 3.6 中只是实现细节，但自 Python 3.7 起已成为语言规范的一部分。

v0.6.3
******

此补丁版本修复了已弃用 ``west.cmake`` 模块的行为错误。

v0.6.2
******

此补丁版本修复了 v0.6.1 引入的 ``west update --fetch=smart`` 行为错误。

所有 v0.6.1 用户都必须升级。

v0.6.1
******

.. warning::

   不要使用此补丁版本，应改用 v0.6.2。

此补丁版本的用户可见功能如下：

- :ref:`west-update` 命令新增 ``--fetch`` 命令行选项和 ``update.fetch`` :ref:`配置选项 <west-config>`。默认值“smart”会跳过获取本地已有的 SHA 和标签。
- 改进并统一了 ``west diff``、``west status``、``west forall`` 和 ``west update`` 命令的错误处理。这些命令都可操作多个项目；与某个项目相关的子进程失败时，现在会继续处理其他项目。任意子进程失败时，所有这些命令也都会让 west 进程返回非零错误码（此前尤其是 ``west forall`` 并非如此）。
- :ref:`west manifest <west-built-in-misc>` 命令的错误处理也得到改进。
- 只要格式字符串仅需要可从清单文件读取的信息，:ref:`west list <west-built-in-misc>` 命令现在即使项目未克隆也能工作。如果格式字符串需要项目仓库中保存的数据，例如包含 ``{sha}`` 格式键，则仍会失败。
- 操作 Git 修订版本的命令和选项现在接受缩写 SHA。例如，``west init --mr SHA_PREFIX`` 现在可以使用。此前，如果 ``--mr`` 参数不是分支或标签，就必须是完整的 40 字符 SHA。

:ref:`west-apis` 中面向开发者的变更如下：

- west.log.banner()：新增
- west.log.small_banner()：新增
- west.manifest.Manifest.get_projects()：新增
- west.manifest.Project.is_cloned()：新增
- west.commands.WestCommand 实例现在可在 do_run() 调用期间，通过新增 self.manifest 属性访问解析后的 Manifest 对象。读取此属性会返回 Manifest 对象；如果无法解析，则中止命令。
- west.manifest.Project.git() 现在具有 capture_stderr 关键字参数


v0.6.0
******

- 不再使用独立引导程序

  在 west v0.5.x 中，程序分为引导程序和每个安装实例中的克隆两个组件。更多详情见 `Multiple Repository Management in the v1.14 documentation`_。

  这类似于 Google Repo 工具的工作方式，让 west 初期能够快速迭代。但它也造成了困惑；现在 west 已足够稳定，可以完全作为单个组件通过 PyPI 分发。

  从 v0.6.x 起，所有 west 核心命令和辅助类都属于通过 PyPI 分发的 west 包。这消除了复杂性，也使系统中任意位置都能导入 west 模块，而不再局限于扩展命令。
- 为保持向后兼容，``selfupdate`` 命令仍然存在，但现在只会打印错误消息并退出。
- 清单语法变更

  - west 清单文件的 ``projects`` 元素现在可以直接指定获取 URL，如下所示：

    .. code-block:: yaml

       manifest:
         projects:
           - name: example-project-name
             url: https://github.com/example/example-project

    采用此方式设置 ``url`` 属性的项目元素，不能同时具有 ``remote`` 属性。
  - 项目名称必须唯一。这是支持后续工作所需的限制，但在 west v0.5.x 中无法施加，因为不同项目的 URL 可能具有相同的最后一个路径组件，例如：

    .. code-block:: yaml

       manifest:
         remotes:
           - name: remote-1
             url-base: https://github.com/remote-1
           - name: remote-2
             url-base: https://github.com/remote-2
         projects:
           - name: project
             remote: remote-1
             path: remote-1-project
           - name: project
             remote: remote-2
             path: remote-2-project

    现在可以将这些清单改写为使用 ``url`` 而不是 ``remote`` 的项目，如下所示：

    .. code-block:: yaml

       manifest:
         projects:
           - name: remote-1-project
             url: https://github.com/remote-1/project
           - name: remote-2-project
             url: https://github.com/remote-2/project

- ``west list`` 命令现在支持 ``{sha}`` 格式字符串键

- ``west list`` 的默认格式字符串改为 ``"{name:12} {path:28} {revision:40} {url}"``。

- 现在可以运行 ``west manifest --validate`` 来加载并验证当前清单文件，同时还修复了其他清单解析相关的错误处理问题。

- West API 发生了不兼容变更。在 west v1.0 声明 API 稳定之前，预计还会继续变化。

  - ``west.manifest.Project`` 构造函数的 ``remote`` 和 ``defaults`` 位置参数现在改为关键字参数。还新增了 ``url`` 关键字参数；如果指定，``Project`` 的 URL 将设为该值，并忽略 ``remote`` 关键字参数。

  - 移除了 ``west.manifest.MANIFEST_SECTIONS``，现在只有一个节，即 ``manifest``。同时移除了 ``west.manifest.Manifest`` 工厂方法和构造函数中的 *sections* 关键字参数。

  - 移除了 ``west.manifest.SpecialProject`` 类，请改用 ``west.manifest.ManifestProject``。


v0.5.x
******

West v0.5.x 是 Zephyr 项目在 v1.14 长期支持（LTS）版本中首次广泛使用的 west 版本。`west v0.5.x documentation`_ 作为 Zephyr v1.14 文档的一部分保留。

West v0.5.x 的主要功能如下：

- 使用 Git 仓库进行多仓库管理，包括 west 自身更新
- 分层配置文件
- 扩展命令

v0.5.x 之前的版本
*****************

west 仓库中早于 v0.5.x 的标签都是原型，仅供历史参考。

.. _Multiple Repository Management in the v1.14 documentation:
   https://docs.zephyrproject.org/1.14.0/guides/west/repo-tool.html

.. _west v0.5.x documentation:
   https://docs.zephyrproject.org/1.14.0/guides/west/index.html
