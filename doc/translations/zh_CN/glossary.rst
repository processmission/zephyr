.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

.. _glossary:

术语表
######

.. glossary::
   :sorted:

   API
      （Application Program Interface，应用程序编程接口）用于构建应用软件的一组已定义例程和协议。

   应用
   application
      Zephyr 构建系统使用的一组用户提供的文件，用于为指定的开发板配置构建应用程序映像。其中可以包含应用专用代码、内核配置设置，以及至少一个 CMakeLists.txt 文件。应用的内核配置设置会指示构建系统创建定制内核，以高效利用开发板资源。如果应用不依赖任何开发板专用功能，有时可以为多种开发板配置构建，包括采用不同 CPU 架构的开发板。

   应用程序映像
   application image
      为特定开发板构建、并由该开发板加载和执行的二进制文件。每个应用程序映像都包含应用代码以及 Zephyr 内核为支持该应用所需的代码，并被编译为一个完整链接的二进制文件。映像加载到开发板后，会接管系统、完成初始化，并作为系统中唯一运行的应用。应用代码和内核代码都以特权代码身份在同一个共享地址空间中执行。

   架构
   architecture
      指令集架构（ISA）及其编程模型。

   开发板
   board
      一种目标系统，具有明确的一组设备和功能，能够加载并执行应用程序映像。它可以是真实硬件系统，也可以是在 QEMU 中运行的模拟系统。一个开发板可以包含一个或多个 :term:`片上系统 <SoC>`。Zephyr 内核支持多种 :ref:`开发板 <boards>`。

   开发板配置
   board configuration
      一组内核配置选项，用于指定内核如何使用开发板上的设备。Zephyr 构建系统会为每个受支持的开发板定义一个或多个开发板配置。应用可以按需覆盖构建系统指定的内核配置设置。

   开发板名称
   board name
      :term:`开发板 <board>` 的人类可读名称，用于唯一且明确地标识特定系统，但不包含实际构建 Zephyr 映像可能还需要的其他信息。详情见 :ref:`board_terminology`。

   开发板限定符
   board qualifiers
      一组附加标记，以正斜杠（``/``）分隔，位于 :term:`开发板名称 <board name>` 之后（可选附带 :term:`开发板修订版 <board revision>`），用来组成 :term:`开发板目标 <board target>`。当前支持的限定符包括 :term:`片上系统 <SoC>`、:term:`CPU 集群 <CPU cluster>` 和 :term:`变体 <variant>`。详情见 :ref:`board_terminology`。

   开发板修订版
   board revision
      用于标识硬件系统特定修订版的可选版本字符串。硬件系统仅有小幅变更时，修订版机制有助于避免重复维护开发板文件。更多信息见 :ref:`porting_board_revisions` 和 :ref:`application_board_version`。

   开发板目标
   board target
     可传递给任一 Zephyr 构建工具、用于为特定硬件系统编译和链接映像的完整字符串。该字符串唯一标识 :term:`开发板名称 <board name>`、:term:`开发板修订版 <board revision>` 和 :term:`开发板限定符 <board qualifiers>` 的组合。详情见 :ref:`board_terminology`。

   CPU 集群
   CPU cluster
     由一个或多个 :term:`CPU 核心 <CPU core>` 组成的一组处理单元。它们在同一个地址空间中执行相同映像，并采用对称多处理（SMP）配置。一个集群中的 :term:`CPU 核心 <CPU core>` 必须属于同一 :term:`架构 <architecture>`。同一个 :term:`片上系统 <SoC>` 中可以包含多个 CPU 集群，每个集群含一个或多个核心。

   CPU 核心
   CPU core
     一个独立的处理单元，拥有自己的程序计数器（Program Counter），并按顺序执行程序指令。CPU 核心属于 :term:`CPU 集群 <CPU cluster>`；一个集群可以包含一个或多个核心。

   设备运行时电源管理
   device runtime power management
      设备运行时电源管理（PM）是指设备能够独立于系统电源状态节省能耗。设备会跟踪自身的使用情况，并自动挂起或恢复。此功能通过 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME` Kconfig 选项启用。

   空闲线程
   idle thread
      当没有其他就绪线程可运行时执行的系统线程。

   IDT
      （Interrupt Descriptor Table，中断描述符表）x86 架构用于实现中断向量表的一种数据结构。IDT 用于确定对中断和异常的正确响应。

   内部 API
   internal API
      在 Zephyr 源码树任意位置定义的内部函数、结构体或宏。内部 API 用于“扩展”Zephyr，只能由特定的 :term:`软件组件 <software component>` 之间调用，通常用于树内组件；某些情况下也供树外组件使用（例如新增树外架构或驱动）。应用不得在自身范围之外调用内部 API。API 的调用或实现上下文有明确规定。例如，带有 ``arch_`` 前缀的函数供 Zephyr 内核调用架构专用代码。内部 API 大多保持稳定，但其稳定性保障弱于 :term:`公共 API <public API>`。

   ISR
      （Interrupt Service Routine，中断服务例程），也称中断处理程序。ISR 是一个回调函数，由硬件中断（或软件中断指令）触发执行，用于处理中断当前处理器代码的高优先级情况。

   内核
   kernel
      由 Zephyr 提供、用于实现 Zephyr 内核的一组文件，包括内核核心服务、设备驱动、网络协议栈等。

   电源域
   power domain
      一组设备构成一个电源域，对这些设备的供电和断电可以作为一个整体通过单次操作完成。电源域由 :c:struct:`device` 表示。

   电源门控
   power gating
      电源门控通过关闭集成电路中当前未使用的区域来降低功耗。

   私有 API
   private API
      在 Zephyr 源码树任意位置定义、仅供其所属 :term:`软件组件 <software component>` 内部使用的函数、结构体或宏。私有 API 可能随时变更，组件外部的代码不得使用。

   公共 API
   public API
      在 ``include/zephyr`` 目录中定义且未明确标记为私有的函数、结构体或宏。公共 API 供所有树内或树外 :term:`软件组件 <software component>` 使用。修改公共 API 必须遵循 :ref:`API 生命周期 <api_lifecycle>` 一节所述的规定，因此公共 API 对长期稳定性提供相应保障。

   SoC
      片上系统（`System on a chip`_），即至少包含一个由至少一个 :term:`CPU 核心 <CPU core>` 组成的 :term:`CPU 集群 <CPU cluster>`，以及外设和存储器的集成电路。

   SoC 系列族
   SoC family
      一个或多个具有足够共同特征、因而可以归为同一系列族的 :term:`SoC` 或 :term:`SoC 系列 <SoC series>`。

   SoC 系列
   SoC series
      一组具有相似特征和功能的不同 :term:`SoC`，通常由供应商统一命名并推广。

   软件组件
   software component
      软件组件是 Zephyr 源码中自包含、模块化且可替换的一部分。驱动、子系统和应用都是 Zephyr 中软件组件的示例。

   子系统
   subsystem
       操作系统中负责特定功能或提供特定服务的逻辑独立部分。

   系统电源状态
   system power state
      描述整个系统功耗情况的状态。系统电源状态由 :c:enum:`pm_state` 表示。

   变体
   variant
      在 :term:`开发板限定符 <board qualifiers>` 中，变体表示针对某种 :term:`SoC` 与 :term:`CPU 集群 <CPU cluster>` 组合的特定构建类型或配置。常见用途包括：为支持可信执行环境的平台分别选择安全和非安全构建，或选择构建中使用的 RAM 类型。

   west
      为 Zephyr 项目开发的多仓库管理工具。参见 :ref:`west`。

   west 安装目录
   west installation
      west 0.7 之前对 :term:`west 工作区 <west workspace>` 的旧称。

   west 清单
   west manifest
      通常名为 :file:`west.yml` 的 YAML 文件，用于描述项目（即构成 :term:`west 工作区 <west workspace>` 的 Git 仓库）及其他元数据。一般信息见 :ref:`west-basics`，详情见 :ref:`west-manifests`。

   west 清单仓库
   west manifest repository
      :term:`west 工作区 <west workspace>` 中包含 :term:`west 清单 <west manifest>` 的 Git 仓库。其位置由 :ref:`manifest.path 配置选项 <west-config-index>` 指定。参见 :ref:`west-basics`。

   west 项目
   west project
      :term:`west 清单 <west manifest>` 中的每个条目都描述一个 Git 仓库，west 在对应的 :term:`west 清单仓库 <west manifest repository>` 中工作时会克隆并管理这些仓库。west 项目不同于 :term:`Zephyr 模块 <zephyr module>`，但很多项目同时也是模块。更多信息见 :ref:`west-manifests-projects`。

   west 工作区
   west workspace
      系统中的一个目录，包含 ``.west`` 子目录和一个 :term:`west 清单仓库 <west manifest repository>`。运行 ``west init`` 命令创建 west 工作区后，可以将 Zephyr 源码及其 :term:`west 项目 <west project>` 克隆到本地。参见 :ref:`west-basics`。

   XIP
      （eXecute In Place，原地执行）一种直接从长期存储介质执行程序的方法，无需先将程序复制到 RAM，从而将可写内存留给动态数据，而不必用于存放静态程序代码。

   Zephyr 模块
   zephyr module
      包含 :file:`zephyr/module.yml` 文件的 Git 仓库。Zephyr 构建系统使用该文件，将模块的源码和配置文件集成到常规 Zephyr 构建中。Zephyr 模块可以是 west 项目，但不一定是。详情见 :ref:`modules`。

.. _System on a chip: https://en.wikipedia.org/wiki/System_on_a_chip
