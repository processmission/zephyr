.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _requirements_catalog:

需求目录
########

Zephyr 的需求使用 `StrictDoc <https://github.com/strictdoc-project/strictdoc>`__ 在专用的 ``reqmgmt`` 仓库中维护。当工作区中存在该仓库时（该仓库作为 west 项目拉取），其中的需求会被导出，并直接渲染到本文档下方。

.. only:: reqmgmt

   .. toctree::
      :maxdepth: 2

      /build/requirements/index

.. only:: not reqmgmt

   由于工作区中不存在 ``reqmgmt`` 模块，本次构建未包含需求内容。已发布的版本请参阅 `Zephyr 项目需求 <https://zephyrproject-rtos.github.io/reqmgmt/>`__ 。
