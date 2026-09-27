.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mcumgr_handlers:

MCUmgr 处理程序
###############

概述
****

MCUmgr 通过组处理程序来工作，这些处理程序标识与特定管理区域相关的一组功能；管理区域由 16 位标识值寻址。:c:enum:`mcumgr_group_t` 包含 Zephyr 中可用的管理组及其对应的组 ID 值。组 ID 包含在 SMP 头中，用于标识命令所属的组；此外还有一个 8 位命令 ID，用于标识要执行的该组功能——有关 SMP 协议和头部的详细信息，请参阅 :ref:`mcumgr_smp_protocol_specification`。每个唯一 ID 只能注册一个组。

实现
****

MCUmgr 处理程序可以由应用程序代码或模块代码在外部添加，它们不必位于上游 Zephyr 树中才能使用。创建处理程序的第一步是创建其文件夹结构，典型的 Zephyr MCUmgr 组布局如下：

.. code-block:: none

   <dir>/grp/<grp_name>_mgmt/
   ├── CMakeLists.txt
   ├── Kconfig
   ├── include
   ├──── <grp_name>_mgmt.h
   ├──── <grp_name>_mgmt_callbacks.h
   ├── src
   └──── <grp_name>_mgmt.c

请注意，上游 Zephyr MCUmgr 处理程序中的头文件位于 ``zephyr/include/zephyr/mgmt/mcumgr/grp/<grp_name>_mgmt`` 目录中，以便应用程序可以全局包含这些文件。

初始头文件 <grp_name>_mgmt.h
============================

头文件的作用是提供可供 MCUmgr 处理程序本身和应用程序代码使用的定义，例如用于引用执行功能所需的命令 ID。示例文件类似于：

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/include/example_mgmt.h
   :language: c
   :linenos:

这为 ``test`` 和 ``other`` 这 2 个命令提供了定义，并设置 SMP 版本 2 错误响应（与返回 :c:enum:`mcumgr_err_t` 的旧版 SMP 版本 1 错误响应不同，版本 2 的每个组都有唯一错误码——应始终有一个值为 0 的 OK 错误码和一个值为 1 的未知错误码。上述示例随后添加了值为 2 的 ``not wanted`` 错误码。此外，组 ID 设置为 :c:enumerator:`MGMT_GROUP_ID_PERUSER`，它是用户定义组的起始组 ID。请注意，组 ID 必须唯一，因此其他自定义组应使用不同的值；可以使用集中索引头文件（如上游 Zephyr 中所做的那样）来更轻松地分配组 ID。

初始头文件 <grp_name>_mgmt_callbacks.h
======================================

头文件的作用是提供可供 MCUmgr 处理程序本身和应用程序代码使用的定义，例如用于引用执行功能所需的命令 ID。示例文件类似于：

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/include/example_mgmt_callbacks.h
   :language: c
   :linenos:

这会设置一个事件，应用程序（或模块）代码可以注册该事件，以便在函数处理程序执行时收到回调；这允许更改处理程序的流程（即返回错误而不是继续执行）。事件组 ID 设置为 :c:enumerator:`MGMT_EVT_GRP_USER_CUSTOM_START`，它是用户定义组的起始事件 ID。请注意，事件 ID 必须唯一，因此其他自定义组应使用不同的值；可以使用集中索引头文件（如上游 Zephyr 中所做的那样）来更轻松地分配事件 ID。

初始源文件 <grp_name>_mgmt.c
============================

此源文件的作用是处理传入的 MCUmgr 命令、提供响应，并向 MCUmgr 注册传输，以便将命令发送给它。示例文件类似于：

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/src/example_mgmt.c
   :language: c
   :linenos:

上述代码创建了 2 个函数处理程序，其中 ``test`` 支持读请求并接受 2 个必需参数，而 ``other`` 支持写请求并接受 1 个可选参数。此函数处理程序具有可选的通信回调功能，允许代码的其他部分监听该事件并采取任何必要的措施，或者通过返回错误来阻止函数的进一步执行。有关 MCUmgr 回调功能的更多详细信息，请参阅 :ref:`mcumgr_callbacks`。

请注意，引用自定义 MCUmgr 处理程序回调的其他代码需要同时包含基础 Zephyr 回调包含文件和自定义处理程序回调文件；包含上游 Zephyr 回调头文件时，只会包含树内 Zephyr 处理程序头文件。

初始 Kconfig
============

Kconfig 文件的作用是提供与所实现处理程序功能相关的选项，供用户启用或更改。示例文件类似于：

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/Kconfig
   :language: kconfig

初始 CMakeLists.txt
===================

CMakeLists.txt 文件由构建系统使用，用于设置要编译的文件、要添加的包含目录以及指定可更改的选项。基本文件只需在启用 Kconfig 选项时包含源文件。示例文件类似于：

.. tabs::

   .. group-tab:: Zephyr 模块

      .. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/CMakeLists.txt
         :language: cmake

   .. group-tab:: 应用程序

      .. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/CMakeLists.txt
         :language: cmake
         :start-after: Include handler files

从应用程序包含
**************

可以通过创建/编辑应用程序构建文件来添加特定于应用程序的 MCUmgr 处理程序。下面显示了示例修改。

CMakeLists.txt 示例
===================

通过添加以下内容，应用程序 ``CMakeLists.txt`` 文件可以加载示例 MCUmgr 处理程序的 CMake 文件：

.. code-block:: cmake

    add_subdirectory(mcumgr/grp/<grp_name>)

Kconfig 示例
============

通过将以下内容添加到应用程序目录中的 ``Kconfig`` 文件（如果不存在则创建它），应用程序 Kconfig 文件可以包含示例 MCUmgr 处理程序的 Kconfig 文件：

.. code-block:: kconfig

    rsource "mcumgr/grp/<grp_name>/Kconfig"

    # Include Zephyr's Kconfig
    source "Kconfig.zephyr"

从 Zephyr 模块包含
******************

Zephyr :ref:`modules` 可用于将自定义 MCUmgr 处理程序添加到多个不同的应用程序，而无需在每个应用程序的源代码树中重复代码；有关如何设置模块文件的详细信息，请参阅 :ref:`module-yml`。下面显示了示例文件。

zephyr/module.yml 示例
======================

这是一个示例文件，可用于从模块目录的根目录加载 Kconfig 和 CMake 文件，它应放置于 ``zephyr/module.yml``：

.. code-block:: yaml

    build:
      kconfig: Kconfig
      cmake: .

Example CMakeLists.txt
======================

这是一个示例 CMakeLists.txt 文件，它加载示例 MCUmgr 处理程序的 CMake 文件，并应放置于 ``CMakeLists.txt``：

.. code-block:: cmake

    add_subdirectory(mcumgr/grp/<grp_name>)

Example Kconfig
===============

这是一个示例 Kconfig 文件，它加载示例 MCUmgr 处理程序的 Kconfig 文件，并应放置于 ``Kconfig``：

.. code-block:: kconfig

    rsource "mcumgr/grp/<grp_name>/Kconfig"

演示处理程序
************

有一个演示项目，其中包含应用程序和 Zephyr 模块 MCUmgr 处理程序的配置，可作为创建自己的处理程序的基础，位于 :zephyr_file:`tests/subsys/mgmt/mcumgr/handler_demo/`。
