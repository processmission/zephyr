.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

.. _west-apis:
.. _west-apis-west:

West API
########

本页介绍 :ref:`west <west>` 提供的 Python API，以及 Zephyr 仓库中的 :ref:`west 扩展 <west-extensions>` 使用的一些附加 API。

**目录**：

.. contents::
   :local:

.. NOTE: documentation authors:

   1. keep these sorted by package/module name.
   2. if you add a :ref: target here, add it to west-not-found.rst too.

.. _west-apis-commands:

west.commands
*************

.. module:: west.commands

所有内置命令和扩展命令都通过继承这里定义的 :py:class:`WestCommand` 实现。此外，这里还提供一些异常类型。

WestCommand
===========

.. autoclass:: west.commands.WestCommand

   实例属性：

   .. py:attribute:: name

      与传给构造函数的值相同。

   .. py:attribute:: help

      与传给构造函数的值相同。内置命令必须提供，扩展命令会忽略它，见 https://github.com/zephyrproject-rtos/west/issues/927

   .. py:attribute:: description

      与传给构造函数的值相同。

   .. py:attribute:: accepts_unknown_args

      与传给构造函数的值相同。

   .. py:attribute:: requires_workspace

      与传给构造函数的值相同。

   .. versionadded:: 0.7.0

   .. py:attribute:: parser

      调用 ``WestCommand.add_parser()`` 创建的参数解析器。

   实例属性访问器：

   .. py:attribute:: manifest

      返回当前清单文件对应的 :py:class:`west.manifest.Manifest` 实例；如果未提供实例，则终止程序。只能在 ``do_run()`` 方法中安全使用该属性。

   .. versionadded:: 0.6.1
   .. versionchanged:: 0.7.0
      现在可以设置该属性。

   .. py:attribute:: has_manifest

      如果读取 manifest 属性会成功而非报错，则为 True。

   .. py:attribute:: config

      可设置的属性，返回 :py:class:`west.configuration.Configuration` 实例；如果未提供实例，则终止程序。只能在 ``do_run()`` 方法中安全使用。

   .. versionadded:: 0.13.0

   .. py:attribute:: has_config

      如果读取 config 属性会成功而非报错，则为 True。

   .. versionadded:: 0.13.0

   .. py:attribute:: git_version_info

      包含 Git 版本信息的元组。

   .. versionadded:: 0.11.0

   .. py:attribute:: color_ui

      west 配置允许彩色输出时为 True，否则为 False。

   .. versionadded:: 1.0.0

   构造函数：

   .. automethod:: __init__

   .. versionadded:: 0.6.0
      *requires_installation* 参数（在 v0.13.0 中移除）。
   .. versionadded:: 0.7.0
      *requires_workspace* 参数。
   .. versionchanged:: 0.8.0
      *topdir* 参数现在可以是任意 ``os.PathLike`` 对象。
   .. versionchanged:: 0.13.0
      已弃用的 *requires_installation* 参数被移除。
   .. versionadded:: 1.0.0
      *verbosity* 参数。

   方法：

   .. automethod:: run

   .. versionchanged:: 0.6.0
      新增 *topdir* 参数。

   .. automethod:: add_parser

   .. automethod:: add_pre_run_hook
   .. versionadded:: 1.0.0

   .. NOTE: the following 'method' (not 'automethod') directives were added for
      expediency during the west v1.2 release time frame to work around a build
      failure in this zephyr documentation that could not be fixed without
      cutting a west point release. (The docstrings in west had some RST syntax
      errors).

      These should be reverted back to automethod calls at the next release.

   .. method:: check_call(args, **kwargs)

      先以 ``Verbosity.DBG_MORE`` 级别记录调用，再运行 ``subprocess.check_call(args, **kwargs)``。

   .. versionchanged:: 1.2.0
      *cwd* 关键字参数被用于接收任意关键字参数的 ``**kwargs`` 替代。
   .. versionchanged:: 0.11.0

   .. method:: check_output(args, **kwargs)

      先以 Verbosity.DBG_MORE 级别记录调用，再运行 ``subprocess.check_output(args, **kwargs)``。

   .. versionchanged:: 1.2.0
      The *cwd* keyword argument was replaced with a catch-all ``**kwargs``.
   .. versionchanged:: 0.11.0

   .. method:: run_subprocess(args, **kwargs)

      先以 Verbosity.DBG_MORE 级别记录调用，再运行 ``subprocess.run(args, **kwargs)``。

   .. versionadded:: 1.2.0

   所有子类都必须提供以下抽象方法，用于实现上述功能：

   .. automethod:: do_add_parser

   .. automethod:: do_run

   命令需要输出信息时应使用以下方法。它们用于从已弃用的 ``west.log`` 模块迁移到按命令提供的接口，以便在未来版本中为 west 命令实现全局“静默”模式：

   .. automethod:: dbg
   .. versionchanged:: 1.2.0
      *end* 参数。
   .. versionadded:: 1.0.0

   .. automethod:: inf
   .. versionchanged:: 1.2.0
      The *end* argument.
   .. versionadded:: 1.0.0

   .. automethod:: wrn
   .. versionchanged:: 1.2.0
      The *end* argument.
   .. versionadded:: 1.0.0

   .. automethod:: err
   .. versionchanged:: 1.2.0
      The *end* argument.
   .. versionadded:: 1.0.0

   .. automethod:: die
   .. versionadded:: 1.0.0

   .. automethod:: banner
   .. versionadded:: 1.0.0

   .. automethod:: small_banner
   .. versionadded:: 1.0.0

.. _west-apis-commands-output:

输出详细程度
============

自 west v1.0 起，west 命令应使用 west.commands.WestCommand.dbg()、west.commands.WestCommand.inf() 等方法输出信息，见上文。本节介绍用于声明输出详细程度的相关枚举。

.. autoclass:: west.commands.Verbosity

   .. autoattribute:: QUIET
   .. autoattribute:: ERR
   .. autoattribute:: WRN
   .. autoattribute:: INF
   .. autoattribute:: DBG
   .. autoattribute:: DBG_MORE
   .. autoattribute:: DBG_EXTREME

.. versionadded:: 1.0.0

异常
====

.. autoclass:: west.commands.CommandError
   :show-inheritance:

   .. py:attribute:: returncode

      此错误建议使用的程序退出码。

.. autoclass:: west.commands.CommandContextError
   :show-inheritance:

.. _west-apis-configuration:

west.configuration
******************

.. automodule:: west.configuration

自 west v0.13 起，推荐通过 :py:class:`west.configuration.Configuration` 读取配置。

编写 :ref:`west 扩展 <west-extensions>` 时，可通过 ``self.config`` 访问当前 ``Configuration`` 对象，见 :py:class:`west.commands.WestCommand`。

配置 API
========

这是自 west v0.13 起推荐使用的 API。

.. autoclass:: west.configuration.ConfigFile

.. autoclass:: west.configuration.Configuration
   :members:

   .. versionadded:: 0.13.0

已弃用的 API
============

以下 API 也使用 :py:class:`west.configuration.ConfigFile`，但默认操作保存当前工作区配置的全局对象。由于 west API 可用于多个工作区，这已被证明是不恰当的设计。这些 API 在 west v0.13.0 中被弃用。

这些 API 为兼容旧扩展而保留。如果新代码可以假定使用 west v0.13.0 或更高版本，就不应使用它们。

.. autofunction:: west.configuration.read_config

.. versionchanged:: 0.8.0
   已弃用的 *read_config* 参数被移除。

.. versionchanged:: 0.6.0
   无法找到本地配置文件所导致的错误会被忽略。

.. autofunction:: west.configuration.update_config

.. py:data:: west.configuration.config

   用于当前配置的模块级全局 ConfigParser 实例。读取之前应使用 :py:func:`west.configuration.read_config` 初始化。

.. _west-apis-log:

west.log（已弃用）
******************

.. automodule:: west.log

控制输出详细程度
================

使用 ``set_verbosity()`` 设置全局输出详细程度。

.. autofunction:: set_verbosity

定义了以下详细程度级别。

.. autodata:: VERBOSE_NONE
.. autodata:: VERBOSE_NORMAL
.. autodata:: VERBOSE_VERY
.. autodata:: VERBOSE_EXTREME

输出函数
========

主要函数为 ``dbg()``、``inf()``、``wrn()``、``err()`` 和 ``die()``。还提供 ``inf()`` 的两个特殊形式 ``banner()`` 和 ``small_banner()``，用于将输出分组为不同“章节”。

.. autofunction:: dbg
.. autofunction:: inf
.. autofunction:: wrn
.. autofunction:: err
.. autofunction:: die

.. autofunction:: banner
.. autofunction:: small_banner

.. _west-apis-manifest:

west.manifest
*************

.. automodule:: west.manifest

主要类是 :py:class:`Manifest` 和 :py:class:`Project`，用于表示 :ref:`清单文件 <west-manifests>` 的内容。推荐使用 :py:meth:`Manifest.from_topdir` 解析 west 清单。

常量与函数
==========

.. autodata:: MANIFEST_PROJECT_INDEX
.. autodata:: MANIFEST_REV_BRANCH
.. autodata:: QUAL_MANIFEST_REV_BRANCH
.. autodata:: QUAL_REFS_WEST
.. autodata:: SCHEMA_VERSION

.. autofunction:: west.manifest.manifest_path

.. autofunction:: west.manifest.validate

.. versionchanged:: 0.13.0
   返回经过验证、包含已解析 YAML 数据的字典。

清单及其子对象
==============

.. autoclass:: west.manifest.Manifest

   .. automethod:: __init__
   .. versionchanged:: 0.7.0
      *importer* 和 *import_flags* 关键字参数。
   .. versionchanged:: 0.13.0
      所有参数改为仅限关键字传入。*source_file* 参数被移除，请改用 *topdir*。此函数不再抛出 ``WestNotFound``。
   .. versionadded:: 0.13.0
      *config* 参数。
   .. versionadded:: 0.13.0
      *abspath*、*posixpath*、*relative_path*、*yaml_path*、*repo_path*、*repo_posixpath* 和 *userdata* 属性。

   .. automethod:: from_topdir
   .. versionadded:: 0.13.0

   .. automethod:: from_file
   .. versionchanged:: 0.7.0
      新增 ``**kwargs``。
   .. versionchanged:: 0.8.0
      *source_file*、*manifest_path* 和 *topdir* 参数现在可以是任意 ``os.PathLike`` 对象。
   .. versionchanged:: 0.13.0
      *manifest_path* 和 *topdir* 参数被移除。

   .. automethod:: from_data
   .. versionchanged:: 0.7.0
      新增 ``**kwargs``，且 *source_data* 可以是 ``str``。
   .. versionchanged:: 0.13.0
      The *manifest_path* and *topdir* arguments were removed.

   以下辅助方法用于按名称或其他标识访问子对象：

   .. automethod:: get_projects
   .. versionchanged:: 0.8.0
      *project_ids* 序列现在可以包含任意 ``os.PathLike`` 对象。
   .. versionadded:: 0.6.1

   其他方法：

   .. automethod:: as_dict
   .. versionadded:: 1.4.0
      *active_only* 参数。
   .. versionadded:: 0.7.0
   .. automethod:: as_frozen_dict
   .. versionadded:: 1.4.0
      The *active_only* argument.
   .. automethod:: as_yaml
   .. versionadded:: 1.4.0
      The *active_only* argument.
   .. versionadded:: 0.7.0
   .. automethod:: as_frozen_yaml
   .. versionadded:: 1.4.0
      The *active_only* argument.
   .. versionadded:: 0.7.0
   .. automethod:: is_active
   .. versionadded:: 0.9.0
   .. versionchanged:: 1.1.0
      遵循 ``manifest.project-filter`` 配置选项，见 :ref:`west-config-index`。

.. autoclass:: west.manifest.ImportFlag
   :members:
   :member-order: bysource

.. autoclass:: west.manifest.Project

   .. (note: attributes are part of the class docstring)

   .. versionchanged:: 0.7.0
      *remote* 属性被移除。增加清单 ``import`` 键支持后，无法继续保持该属性的语义。

   .. versionadded:: 0.7.0
      *remote_name* 和 *name_and_path* 属性。

   .. versionchanged:: 0.8.0
      *west_commands* 属性现在始终为列表；旧版中也可能为字符串或 ``None``。

   .. versionadded:: 0.9.0
      *group_filter* 和 *submodules* 属性。

   .. versionadded:: 0.12.0
      *userdata* 属性。

   .. versionadded:: 1.2.0
      *description* 属性。

   构造函数：

   .. automethod:: __init__

   .. versionchanged:: 0.8.0
      *path* 和 *topdir* 参数现在可以是任意 ``os.PathLike`` 对象。

   .. versionchanged:: 0.7.0
      参数相对于此前版本发生了不兼容变更。

   方法：

   .. automethod:: as_dict
   .. versionadded:: 0.7.0

   .. automethod:: git
   .. versionchanged:: 0.6.1
      *capture_stderr* 关键字参数。
   .. versionchanged:: 0.7.0
      不再对参数调用现已移除的 ``Project.format`` 方法。

   .. automethod:: sha
   .. versionchanged:: 0.7.0
      现在会捕获标准错误。

   .. automethod:: is_ancestor_of
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任意 ``os.PathLike`` 对象。

   .. automethod:: is_cloned
   .. versionchanged:: 0.8.0
      The *cwd* parameter can now be any ``os.PathLike``.
   .. versionadded:: 0.6.1

   .. automethod:: is_up_to_date_with
   .. versionchanged:: 0.8.0
      The *cwd* parameter can now be any ``os.PathLike``.

   .. automethod:: is_up_to_date
   .. versionchanged:: 0.8.0
      The *cwd* parameter can now be any ``os.PathLike``.

   .. automethod:: read_at
   .. versionchanged:: 0.8.0
      The *cwd* parameter can now be any ``os.PathLike``.
   .. versionadded:: 0.7.0

   .. automethod:: listdir_at
   .. versionchanged:: 0.8.0
      The *cwd* parameter can now be any ``os.PathLike``.
   .. versionadded:: 0.7.0

.. autoclass:: west.manifest.ManifestProject

   仅支持 Project 方法的有限子集，调用其他方法的结果未作规定。

   .. versionchanged:: 0.8.0
      *url* 属性现在为空字符串，而非 ``None``。*abspath* 属性改用 ``os.path.abspath()`` 创建，而非 ``os.path.realpath()``，以改善符号链接支持。

   .. automethod:: as_dict

.. versionadded:: 0.6.0

.. autoclass:: west.manifest.Submodule

.. versionadded:: 0.9.0

Exceptions
==========

.. autoclass:: west.configuration.MalformedConfig
   :show-inheritance:

.. autoclass:: west.manifest.MalformedManifest
   :show-inheritance:

.. autoclass:: west.manifest.ManifestVersionError
   :show-inheritance:

   .. versionchanged:: 0.8.0
      *file* 参数现在可以是任意 ``os.PathLike`` 对象。

.. autoclass:: west.manifest.ManifestImportFailed
   :show-inheritance:

   .. versionchanged:: 0.8.0
      *filename* 参数现在可以是任意 ``os.PathLike`` 对象。

   .. versionchanged:: 0.13.0
      *filename* 参数改名为 *imp*，现在可以接受任意值。

.. _west-apis-util:

west.util
*********

.. canon_path(), escapes_directory(), etc. intentionally not documented here.

.. automodule:: west.util

函数
====

.. autofunction:: west.util.west_dir

   .. versionchanged:: 0.8.0
      *start* 参数可以是任意 ``os.PathLike`` 对象。

.. autofunction:: west.util.west_topdir

   .. versionchanged:: 0.8.0
      The *start* parameter can be any ``os.PathLike``.

Exceptions
==========

.. autoclass:: west.util.WestNotFound
   :show-inheritance:
