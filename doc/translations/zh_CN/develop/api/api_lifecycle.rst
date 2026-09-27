.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _api_lifecycle:

API 生命周期
############

使用 Zephyr API 的开发者需要知道，可以在多长时间内相信某个 API 不会在后续版本中变化。同时，维护和扩展 Zephyr API 的开发者需要能够引入尚未充分验证的新 API，并在旧 API 不再是最佳选择或底层平台不再支持时，将其退役。


.. figure:: api_lifecycle.png
    :align: center
    :alt: API Life Cycle
    :figclass: align-center

    API 生命周期

所有 API 及其成熟度的最新列表见 :ref:`api_overview` 页面。


.. _api_lifecycle_experimental:

实验性
******

实验性 API 表示功能刚引入不久，未来版本中可能变化或移除。欢迎试用，并通过 `Developer mailing list <https://lists.zephyrproject.org/g/devel>`_ 向社区反馈。

所有新 API 都必须满足以下要求：

- 提供 API 使用文档，说明设计与假设、使用方式、当前实现限制，以及适用时的未来发展方向。
- 引入 API 时，应同时提供至少一个该 API 的实现；对于外设 API，即至少一个驱动程序。
- 至少提供一个使用新 API 的示例，可以仅支持在单块开发板上构建。

引入新的实验性 API 时，应在定义 API 的头文件中标注 API 版本。实验性 API 的次版本号应不大于 1（0.1.z）。参见 :ref:`api_overview`。

外设 API（硬件相关）
====================

为新的外设或驱动程序子系统引入 API（带文档的公共头文件）时，必须进行 API 审查，由各厂商代表组成的架构工作组负责推动。

在不同硬件平台上拥有至少两个实现后，应将 API 提升为 ``unstable``。

.. _api_lifecycle_unstable:

不稳定
******

API 正在逐渐定型，但尚未经过足够的实际使用测试，不能视为稳定。此时 API 被认为具有通用性，可以用于不同硬件平台。

API 状态变为不稳定时，应在定义 API 的头文件中标注版本。不稳定 API 的次版本号应大于 1（0.y.z | y > 1）。参见 :ref:`api_overview`。

.. note::

   变更不会另行公告。

Peripheral APIs (Hardware Related)
==================================

在不同硬件平台上拥有至少两个实现后，应将 API 从 ``experimental`` 提升为 ``unstable``。

与硬件无关的 API
================

与硬件无关的 API 必须有多个应用使用，才能从 ``experimental`` 提升为 ``unstable``。

.. _api_lifecycle_stable:

稳定
****

API 已证明能够满足需求，但底层代码清理可能导致小幅变更。在合理可行的情况下，会保持向后兼容。

满足以下要求后，可以将 API 声明为 ``stable``：

- 新 API 的测试用例达到 100% 覆盖率。
- 代码中具备完整文档。所有公共接口都必须有文档，并可在在线文档中查阅。
- API 已投入使用，并且已在至少两个开发版本中提供。
- 稳定 API 可以随时接收向后兼容的更新、缺陷修复和安全修复。

将 API 声明为 ``stable`` 时，必须执行以下步骤：

#. 创建拉取请求，修改 :ref:`api_overview` 表中的对应条目。
#. 向 ``devel`` 邮件列表发送邮件，公告 API 升级请求。
#. 将拉取请求提交到下一次 `Zephyr Architecture meeting`_ 讨论；如果没有异议，将合并该拉取请求。


API 状态变为稳定时，应在定义 API 的头文件中标注版本。稳定 API 的主版本号应大于或等于 1（x.y.z | x >= 1）。参见 :ref:`api_overview`。

.. _breaking_api_changes:

引入破坏兼容性的 API 变更
=========================

如上所述，稳定 API 力求在整个生命周期中保持向后兼容。但有时这一目标会阻碍技术进步，或给 API 及其实现的维护带来不合理的负担，使其难以实现。

破坏兼容性的 API 变更是指：用户必须修改现有代码，才能保持应用当前行为。仅需重新编译应用、无需修改应用本身的情况，不视为破坏兼容性的 API 变更。

为限制和控制破坏向后兼容承诺的变更，只要认为有必要进行此类变更，就必须执行以下步骤，项目才会接受：

#. 在 GitHub 上创建 :ref:`RFC 议题 <rfcs>`，包含以下内容：

   .. code-block:: none

      Title:     RFC: Breaking API Change: <subsystem>
      Contents:  - Problem Description:
                   - Background information on why the change is required
                 - Proposed Change (detailed):
                   - Brief description of the API change
                 - Detailed RFC:
                   - Function call changes
                   - Device Tree changes (source and bindings)
                   - Kconfig option changes
                 - Dependencies:
                   - Impact to users of the API, including the steps required
                     to adapt out-of-tree users of the API to the change

   RFC 议题可以链接到以代码形式提供变更的拉取请求，代替文字描述。
#. 为 RFC 议题添加 GitHub 标签 ``Breaking API Change``。
#. 将 RFC 议题提交到下一次 `Zephyr Architecture meeting`_ 讨论。
#. 向 ``devel`` 邮件列表发送邮件，主题与 RFC 议题标题一致，并包含指向该议题的链接。

随后，RFC 会通过议题评论收集反馈，并在 Zephyr 架构会议上讨论，让利益相关方和整个社区有机会详细讨论。

最后，如果第一步尚未创建拉取请求，则必须在 GitHub 上创建。提议者可以选择同时提出 RFC 和拉取请求，或等 RFC 达成足够共识、确信方案能够被接受后再着手实现。拉取请求必须包含：

- 与 RFC 议题一致的标题
- 指向 RFC 议题的链接
- API 的实际变更

  - API 头文件的变更
  - API 实现的变更
  - 相关 API 文档的变更
  - 设备树源码和绑定的变更

- 使源码树内 API 使用者适应变更所需的修改。根据工作范围，可能需要对应维护者协助。
- 在下一版本发行说明的“API Changes”一节中添加条目。
- 添加 ``API``、``Breaking API Change`` 和 ``Release Notes`` 标签，以及其他适用标签。
- 如果 RFC 尚未在 `Zephyr Architecture meeting`_ 中讨论并达成一致，添加 ``Architecture Review`` 标签。

完成上述步骤后，提案结果取决于对应子系统维护者是否批准实际拉取请求。与其他拉取请求一样，作者可以请求在 `Zephyr TSC meeting`_ 中讨论，必要时甚至进行表决。

如果拉取请求被合并，必须向 ``devel`` 和 ``user`` 邮件列表发送邮件，告知此项变更。

必须修改 API 版本以表明存在不向后兼容的变更，方法是递增主版本号（X.y.z | X > 1）。也可以同时包含次版本级和补丁级变更。主版本号递增时，补丁版本号和次版本号必须重置为 0。参见 :ref:`api_overview`。

.. note::

   破坏兼容性的 API 变更会在迁移指南中列出并说明。

已弃用
******

.. note::

   不稳定 API 可以随时直接移除，无需先弃用。API 的弃用和移除会在发行说明的“API Changes”一节中公告。

弃用现有 API 必须满足以下要求：

- 弃用期（稳定 API）：两个版本。API 必须在至少两个完整版本中标记为弃用。例如，某 API 首次在 4.0 中弃用，最早可在 4.2 中移除。架构工作组可以认定存在特殊情况，允许更早弃用 API。
- 弃用时需要完成的工作：

  - 标记为弃用。可以利用编译器支持（函数声明使用 ``__deprecated``，宏定义使用 ``__DEPRECATED_MACRO``），或引入 Kconfig 选项（名称通常包含 ``DEPRECATED``），启用后将 API 恢复为先前形式。
  - 记录弃用说明。
  - 在下一版本发行说明的“API Changes”中列出弃用。
  - 修改使用已弃用 API 的代码，移除对该 API 的使用。
  - 变更必须是原子的，且支持二分定位。
  - 在对应版本用于跟踪已弃用 API 移除的 `GitHub issue <https://github.com/zephyrproject-rtos/zephyr/labels/deprecation_tracker>`_ 中添加条目。在本例中，应添加到 4.2 版本对应的议题。

弃用等待期内，API 处于 ``deprecated`` 状态。Zephyr 维护者会在 ``docs.zephyrproject.org`` 上跟踪已弃用 API 的使用情况，并帮助开发者迁移代码。Zephyr 会持续提供警告：

- API 文档会告知用户该 API 已弃用。
- 构建时尝试使用已弃用 API，会在控制台输出警告。


已退役
******

在此阶段，API 被移除。

目标移除时间为宣布弃用后的两个版本。实际何时移除由 Zephyr 维护者决定，取决于有多少开发者已成功迁移，以及移除该 API 的紧迫程度。

如果可以移除 API，就将其移除。维护者会删除对应文档，并通过发行说明、邮件列表、GitHub 议题和拉取请求等常规渠道通知。

如果尚不能移除 API，维护者会继续协助迁移，并更新路线图，争取在下一版本移除。

.. _`Zephyr TSC meeting`: https://github.com/zephyrproject-rtos/zephyr/wiki/Zephyr-Committee-and-Working-Group-Meetings#technical-steering-committee-tsc
.. _`Zephyr Architecture meeting`: https://github.com/zephyrproject-rtos/zephyr/wiki/Architecture-Working-Group
