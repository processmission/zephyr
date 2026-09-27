.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _api_overview:

API 概览
########

下表列出 Zephyr API 及其相关信息，包括当前 :ref:`稳定级别 <api_lifecycle>`。主要版本之间 API 变更的更多信息，见 :ref:`zephyr_release_notes`。

版本列采用 `semantic version <https://semver.org/>`_ （语义化版本），遵循以下规则：

 * 主版本号为零（0.y.z）表示初期开发阶段，任何内容都可能随时变化，不应将公共 API 视为稳定。

   * 次版本号不大于 1（0.1.z）时，API 视为 :ref:`实验性 <api_lifecycle_experimental>`。
   * 次版本号大于 1（0.y.z | y > 1）时，API 视为 :ref:`不稳定 <api_lifecycle_unstable>`。

 * 1.0.0 版本确立公共 API。此后版本号的递增方式取决于该公共 API 及其变化。

   * 主版本号大于或等于 1（x.y.z | x >= 1）的 API 视为 :ref:`稳定 <api_lifecycle_stable>`。
   * Zephyr 所有现有稳定 API 均从 1.0.0 版本起始。

 * 如果只引入向后兼容的缺陷修复，必须递增补丁版本号 Z（x.y.Z | x > 0）。缺陷修复指纠正错误行为的内部变更。

 * 如果公共 API 引入向后兼容的新功能，必须递增次版本号 Y（x.Y.z | x > 0）。任何公共 API 功能标记为弃用时，也必须递增次版本号。私有代码中引入大量新功能或改进时，可以递增次版本号。次版本更新可以包含补丁级变更。递增次版本号时，必须将补丁版本号重置为 0。

 * 如果 API 发生破坏兼容性的变更，必须递增主版本号 X（x.Y.z | x > 0）。

.. note::
   现有 API 的初始版本根据其当前状态设置：

    - 0.1.0 表示 :ref:`实验性 <api_lifecycle_experimental>` API；
    - 0.8.0 表示 :ref:`不稳定 <api_lifecycle_unstable>` API；
    - 1.0.0 则表示 :ref:`稳定 <api_lifecycle_stable>` API。

   未来修改 API 时，必须按照上述指南相应调整版本。


.. api-overview-table::
