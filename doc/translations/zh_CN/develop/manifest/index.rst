.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

.. _west_projects_index:

West 项目索引
#############

本页索引了与 :ref:`West <west>` 元工具兼容的项目（模块）。

这里主要列出 Zephyr 默认 :zephyr_file:`清单文件 <west.yml>` 中声明的组件。有关这些导入组件的贡献和审查流程，详见 :ref:`external-contributions`。

此外，本页还登记了在 Zephyr 项目之外维护、能够方便地集成到 Zephyr 工作区的 :ref:`外部项目 <west_external_projects>`。

默认启用的项目／模块
++++++++++++++++++++

以下项目默认启用，调用 :command:`west update` 时会下载。许多项目或模块是构建一般 Zephyr 应用所必需的，其中包括对 Zephyr 多种平台的硬件支持。

要禁用任意已启用模块，例如某个特定 HAL，可使用以下命令::

        west config manifest.project-filter -- -hal_FOO
        west update

.. manifest-projects-table::
   :filter: active

未启用及可选的项目／模块
++++++++++++++++++++++++

以下项目是可选的，调用 :command:`west update` 时不会下载。可以添加这些项目或模块，用它们编写应用代码，并为工作区扩展功能。

要启用以下任一模块，可使用以下命令::

        west config manifest.project-filter -- +nanopb
        west update

.. manifest-projects-table::
   :filter: inactive

.. _west_external_projects:

外部项目／模块
++++++++++++++

以下项目属于外部项目，不会直接纳入默认清单。要使用它们，需要定义包含相应项目的自有清单文件。如何在仍继承 Zephyr :file:`west.yml` 必需模块的前提下实现这一点，详见 :ref:`west-manifest-import`。

请使用 :zephyr_file:`专用模板文件 <doc/develop/manifest/external/external.rst.tmpl>` 向以下列表贡献新的外部模块：

.. toctree::
   :titlesonly:
   :maxdepth: 1
   :glob:

   external/*
