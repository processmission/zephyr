.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _secure_storage:

安全存储
########

| 安全存储子系统提供 `Platform Security Architecture (PSA) Secure Storage API <https://arm-software.github.io/psa-api/storage/>`_ 中定义函数的实现。
| 它可以在尚未实现该 API 的 :term:`board targets<board target>` 上启用。

概述
****

安全存储子系统使 PSA Secure Storage API 可在所有具有非易失性存储器支持的板目标上使用。因此，它在尚未实现该 API 的板目标上提供 API 实现，从而确保对该 API 的功能支持。例如，启用了 :ref:`tfm` 的板目标（以 ``/ns`` 结尾）无法启用该子系统，因为 TF-M 已经提供了该 API 的实现。

| 除了为 API 提供功能支持外，根据设备特定的安全特性和配置，该子系统还可以对通过 PSA Secure Storage API 存储的静态数据进行保护。
| 但是，请记住，在可能的情况下，最好使用像 TF-M 这样的安全处理环境，因为凭借隔离保证，它可以提供更高的安全性。

限制
****

安全存储子系统对 PSA Secure Storage API 的实现：

* 并不以完全符合规范为目标。

  | 它的首要目标是在所有板目标上提供对 API 的功能支持。
  | 下文介绍了该实现偏离规范的一些重要方式。

* 不保证其存储的数据在所有情况下都能在静态时保持安全。

  这取决于设备特定的安全特性和配置。

* 截至撰写本文时，尚未提供 Protected Storage (PS) API 的实现。

  相反，PS API 会直接调用 Internal Trusted Storage (ITS) API（除非提供了 PS API 的 `custom implementation <#whole-api>`_）。

以下列出了该实现有意偏离规范的一些方式及其原因。这并不是一个详尽的列表。

* 默认情况下，UID 类型只有 30 位。（与 `2.5 UIDs <https://arm-software.github.io/psa-api/storage/1.0/overview/architecture.html#uids>`_ 不符。）

  | 这是一项优化，使直接将 UID 用作存储条目 ID 更加方便（例如，在启用 :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_STORE_IMPLEMENTATION_ZMS` 时，与 :ref:`ZMS <zms_api>` 一起使用）。
  | Zephyr 定义了供 API 不同使用者使用的数值范围，以保证不会发生冲突，并且它们都适合 30 位。有关更多信息，请参见 :zephyr_file:`include/zephyr/psa` 中的头文件。

* 默认情况下，存储在 ITS 中的数据会经过加密和身份验证（与 `3.2. Internal Trusted Storage requirements <https://arm-software.github.io/psa-api/storage/1.0/overview/requirements.html#internal-trusted-storage-requirements>`_ 中的 ``1.`` 不符。）

  | 规范认为 ITS 底层的存储 ``implicitly confidential and protected from replay`` （即 `2.4. The Internal Trusted Storage API <https://arm-software.github.io/psa-api/storage/1.0/overview/architecture.html#the-internal-trusted-storage-api>`_），因为 ``most embedded microprocessors (MCU) have on-chip flash storage that can be made inaccessible except to software running on the MCU`` （即 `2.2. Technical Background <https://arm-software.github.io/psa-api/storage/1.0/overview/architecture.html#technical-background>`_）。
  | 并非所有 MCU 都是这种情况。因此，会对存储的数据提供额外保护。

  然而，这并不能保证存储的数据在所有情况下都能在静态时保持安全，因为这取决于设备特定的安全特性和配置。它需要随机熵源，尤其是安全的加密密钥提供程序（:kconfig:option:`CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_KEY_PROVIDER`）。

  此外，存储在 ITS 中的数据不受重放攻击保护，因为这需要由硬件保护的存储。

* 通过 PSA Secure Storage API 存储的数据不受软件或调试直接读/写的保护。（与 `3.2. Internal Trusted Storage requirements <https://arm-software.github.io/psa-api/storage/1.0/overview/requirements.html#internal-trusted-storage-requirements>`_ 中的 ``2.`` 和 ``10.`` 不符。）

  它只在静态时受到保护。要在运行时也保护它，需要特定的硬件机制来支持。

* ``PSA_STORAGE_FLAG_WRITE_ONCE`` 标志仅保护条目免受通过 API 进行的修改，而不保护存储介质本身免受修改。

  | 要维持该标志，需要知道条目最初已被创建，而这一状态必须在存储介质被重写后仍然存在。与重放保护一样，这需要由硬件保护的存储。
  | 因此，能够写入存储介质的攻击者可以覆盖或删除一次性写入条目：要么篡改该条目，随后子系统将其视为已损坏并允许替换它；要么直接擦除它，之后它看起来从未存在过。加密和验证条目都无法防止这两种情况。

* ``psa_its_get*()`` 函数可以返回 ``PSA_ERROR_INVALID_SIGNATURE`` 和 ``PSA_ERROR_DATA_CORRUPT``。

  规范没有为 ITS API 定义这些错误，因为它假定 ITS 底层存储受硬件保护，因此从其中读回的数据始终完好无损。由于此处并非如此，这些错误代码会传递下去，让调用者能够区分被篡改的条目和内部故障。

配置
****

要配置 Zephyr 提供的 PSA Secure Storage API 实现，请查看可用的 :kconfig:option-regex:`Kconfig 选项 <CONFIG_SECURE_STORAGE_.*>`。它们定义在 :zephyr_file:`subsys/secure_storage/` 下的各个 Kconfig 文件中。

自定义
******

如果现有实现提供的功能不够，自定义实现也可以在不同层面替代 Zephyr 的实现。

整个 API
========

如果你已经有整个 ITS 或 PS API 的实现并希望使用它，可以通过启用以下 Kconfig 选项并实现相关函数来做到这一点：

* :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_IMPLEMENTATION_CUSTOM`，用于 ITS API。
* :kconfig:option:`CONFIG_SECURE_STORAGE_PS_IMPLEMENTATION_CUSTOM`，用于 PS API。

ITS API
=======

Zephyr 对 ITS API 的实现（:kconfig:option:`CONFIG_SECURE_STORAGE_ITS_IMPLEMENTATION_ZEPHYR`）使用 ITS transform 和 store 模块，这些模块可以分别配置和自定义。请查看 :kconfig:option-regex:`ITS transform 和 store Kconfig 选项 <CONFIG_SECURE_STORAGE_ITS_(TRANSFORM|STORE)_.*>` 以了解不同的配置方式。

特别建议使用或实现安全的 :kconfig:option-regex:`加密密钥提供程序 <CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_KEY_PROVIDER_.*>`。

示例
****

* :zephyr:code-sample:`persistent_key`
* :zephyr:code-sample:`psa_its`

PSA Secure Storage API 参考
***************************

.. doxygengroup:: psa_secure_storage
