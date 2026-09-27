.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _create_first_safety_requirements:

创建你的第一条 Zephyr RTOS 需求
###############################

仓库概述
********

Zephyr 需求在 ``reqmgmt`` 仓库中使用 `StrictDoc <https://github.com/strictdoc-project/strictdoc>`_ 进行管理。该仓库包括：

- :file:`docs/` ：包含 StrictDoc 格式的需求文档
- :file:`tools/` ：实用脚本和配置
- :file:`strictdoc.toml` ：StrictDoc 的项目配置
- :file:`tasks.py` ：使用 Invoke 实现任务自动化


步骤 1：创建或编辑需求文件
**************************

进入仓库中的 :file:`docs/` 文件夹。

文件夹概述
----------

:file:`docs/` 文件夹包含所有以 StrictDoc 格式编写的需求文档。

:file:`docs/` 文件夹包含两个子文件夹，其组织方式如下：

- :file:`system_requirements/` 包含高层系统需求，用于描述 Zephyr RTOS 的总体目标、约束和预期行为。

  - :file:`system_requirements.sgra` 包含 GRAMMAR，用于定义需求的形式化结构
  - :file:`index.sdoc` 包含实际的需求陈述

- :file:`software_requirements/` 包含组件级需求。此文件夹中的每个文件都对应一个特定的子系统或模块。

  - :file:`software_requirements.sgra` 包含所有软件需求的 GRAMMAR
  - 一组 :file:`.sdoc` 片段文件，这些文件汇编成一份大型软件需求文档，例如：

    - :file:`interrupts.sdoc`
    - :file:`queues.sdoc`
    - :file:`semaphore.sdoc`
    - :file:`threads.sdoc`

这些文件采用模块化组织方式，允许贡献者独立处理系统的特定部分。你可以编辑现有的 :file:`.sdoc` 文件，也可以创建新文件。以下是需求块的一个基本示例：

.. code-block:: text

   [REQUIREMENT]
   UID: ZEP-SRS-17-1
   STATUS: Draft
   TYPE: Functional
   COMPONENT: File System
   TITLE: Create file
   STATEMENT: >>>
   Zephyr shall provide file create capabilities for files on the file system.
   <<<

将 UID 设置为 ``TBD`` ，以便 StrictDoc 在后续步骤中自动生成 UID。

步骤 2：保存文件
****************

将文件保存到 :file:`docs/` 文件夹中的系统需求或软件需求子文件夹中。如果创建新文件，请为其取一个有意义的名称，通常应体现其内容所针对的组件或功能。

步骤 3：自动分配 UID
********************

在仓库根目录下运行以下命令：

.. code-block:: bash

   strictdoc manage auto-uid .

此命令将执行以下操作：

- 遍历项目目录

- 查找包含 ``UID: TBD`` 的需求

- 为每项需求分配唯一标识符

步骤 4：验证 UID 分配结果
*************************

再次打开文件。此时应看到类似以下内容：

.. code-block:: text

   UID: ZEP-SRS-17-2
   STATUS: Draft
   TYPE: Functional
   COMPONENT: File System
   TITLE: Create file
   STATEMENT: >>>
   Zephyr shall provide file create capabilities for files on the file system.
   <<<

注意：可以在 :file:`strictdoc.toml` 中配置 UID 格式。

可选：生成 HTML 文档
********************

要构建 HTML 版本的需求文档：

.. code-block:: bash

   strictdoc export .

这将在 :file:`output/` 文件夹中生成可浏览的文档。

可选：启动 Web 编辑器
*********************

要以交互方式浏览和编辑需求：

.. code-block:: bash

   strictdoc server .

这将启动一个本地 Web 界面，用于编辑和评审需求。

总结
****

- 在 :file:`docs/` 中创建或编辑需求，并将 UID 设置为 ``UID: TBD``
- 运行 ``strictdoc manage auto-uid .`` 以分配 UID
- 可选择生成 HTML 文档或启动 Web 编辑器

StrictDoc 帮助 Zephyr 在各个平台上维护结构化、可追溯且可编辑的需求。
