.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

..
  What goes here: removed/deprecated apis, new boards, new drivers, notable
  features. If you feel like something new can be useful to a user, put it
  under "Other Enhancements" in the first paragraph, if you feel like something
  is worth mentioning in the project media (release blog post, release
  livestream) put it under "Major enhancement".
..
  If you are describing a feature or functionality, consider adding it to the
  actual project documentation rather than the release notes, so that the
  information does not get lost in time.
..
  No list of bugfixes, minor changes, those are already in the git log, this is
  not a changelog.
..
  Does the entry have a link that contains the details? Just add the link, if
  you think it needs more details, put them in the content that shows up on the
  link.
..
  Are you thinking about generating this? Don't put anything at all.
..
  Does the thing require the user to change their application? Put it on the
  migration guide instead. (TODO: move the removed APIs section in the
  migration guide)

.. _zephyr_4.4:

Zephyr 4.4.0
############

我们很高兴地宣布 Zephyr 4.4.0 版本正式发布。

本次发布的主要增强包括：

**OpenRISC 支持**
  Zephyr 现在支持 :zephyr:board-catalog:`OpenRISC 架构 <#arch=openrisc>`。

**工具链更新：Zephyr SDK 1.0 与 C17**
  Zephyr 4.4 是首个支持 :ref:`Zephyr SDK 1.0 <toolchain_zephyr_sdk>` 的版本，带来了升级的 GNU 工具链、实验性的 Clang/LLVM 支持，以及多平台的 QEMU 和 OpenOCD 主机工具。

  Zephyr 现在默认将 C17 作为最低要求的 C 标准版本。

**网络增强**
  Wi-Fi 管理协议栈现在支持 :ref:`wifi_mgmt_p2p`，允许设备无需传统接入点即可直接发现并连接。

  网络协议栈还新增了对 :zephyr:code-sample:`WireGuard VPN <wireguard-vpn>` 的支持，可实现安全、低开销的隧道通信。

**USB 主机**
  实验性的 USB 主机支持得到显著扩展：新增了主机类驱动框架，并为充当 USB 主机的 Zephyr 设备提供 :abbr:`UVC (USB Video Class)` 摄像头支持。

**新增驱动类别**
  Zephyr 4.4 新增多项新的驱动 API，包括：

  - :ref:`一次性可编程 (OTP) 存储器件 <otp>`，用于烧录和读取永久性设备数据，

  - :ref:`生物特征识别 API <biometrics_api>`，用于集成指纹扫描仪或面部识别系统等生物特征传感器，以及

  - :ref:`唤醒控制器 (WUC) API <wuc_api>`，用于管理可将系统从低功耗状态唤醒的唤醒源。

**Zbus 异步监听器与代理 agent**
  Zbus 异步监听器通过工作队列实现非阻塞的观察者回调。

  :ref:`Zbus 代理 agent <zbus_proxy_agent>` 通过 IPC 将发布-订阅消息传递扩展到跨 CPU 和域的边界。

**基于压力的 CPU 频率调节**
  实验性的 :ref:`CPU 频率调节 <cpu_freq>` 子系统现在包含 :ref:`基于压力的策略 <pressure_policy>`，可根据调度器负载调整 CPU 频率。

**ARM Cortex-M 上下文切换性能改进**
  针对 ARM Cortex-M 的全新上下文切换实现（通过 :kconfig:option:`CONFIG_USE_SWITCH` 启用）带来了显著的性能提升。

**NAND 闪存支持**
  新增的闪存转换层 (FTL) 磁盘驱动（:dtcompatible:`zephyr,ftl-dhara`）提供磨损均衡和坏块管理，使 NAND 闪存可像标准磁盘设备一样使用。

**开发者体验改进**
  本次发布为开发和测试工作流新增了多项工具和改进：

  - 全新的 :ref:`仪表板 <dashboard>` 将 RAM 和 ROM 占用、设备树配置、子系统初始化级别等构建信息汇总到一份报告中。

  - 面向 QEMU 目标的新显示驱动，简化了在无法使用本机模拟器的环境中开发显示类应用的过程。

  - 新增的堆加固机制（:kconfig:option:`CONFIG_SYS_HEAP_HARDENING`）提供多级运行时保护，防止堆损坏。

  - 新增的 :ref:`基于作用域的清理辅助宏 <cleanup_api>` 在 C 语言中提供 :abbr:`RAII (Resource Acquisition Is Initialization)`/defer 风格的离开作用域自动清理。

  - 全新的 :ref:`ztest 基准测试框架 <ztest_benchmarking>` 提供了创建周期精确基准测试的标准化方式，支持自动数据采集、开销补偿和统计报告。

**Bluetooth LE 主机认证**
  本次发布包含一个已成功通过认证的 Bluetooth Low Energy (LE) 主机协议栈，符合 Bluetooth Core Specification 6.2。认证范围涵盖核心组件（GAP、ATT、GATT、L2CAP、SM）以及设备信息服务 (DIS)。认证列表和相应的设计编号 (DN) 见：https://qualification.bluetooth.com/ListingDetails/332380

**开发板支持扩展**
  本次发布新增了对 121 个 :ref:`新开发板 <boards_added_in_zephyr_4_4>` 和 31 个 :ref:`新扩展板 <shields_added_in_zephyr_4_4>` 的支持。

将应用从 Zephyr v4.3.0 迁移到 Zephyr v4.4.0 时需要或建议采取的变更概览，见单独的 :ref:`迁移指南 <migration_4.4>`。

以下小节按组件详细列出各项变更。

安全漏洞相关
************

本版本修复了以下 CVE：

* :cve:`2025-53022` `(TF-M) FWU 未检查 TLV 载荷的长度 <https://trustedfirmware-m.readthedocs.io/en/latest/security/security_advisories/fwu_tlv_payload_out_of_bounds_vulnerability.html>`_

* :cve:`2026-0849` `Zephyr 项目缺陷跟踪系统 GHSA-ff4p-3ggg-prp6 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-ff4p-3ggg-prp6>`_

* :cve:`2026-1677` 在 2026-04-15 之前处于禁运期

* :cve:`2026-1678` `Zephyr 项目缺陷跟踪系统 GHSA-536f-h63g-hj42 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-536f-h63g-hj42>`_

* :cve:`2026-1679` `Zephyr 项目缺陷跟踪系统 GHSA-qx3g-5g22-fq5w <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-qx3g-5g22-fq5w>`_

* :cve:`2026-1681` 在 2026-04-15 之前处于禁运期

* :cve:`2026-4179` `Zephyr 项目缺陷跟踪系统 GHSA-9xg7-g3q3-9prf <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-9xg7-g3q3-9prf>`_

* :cve:`2026-5066` 在 2026-06-01 之前处于禁运期

* :cve:`2026-5067` 在 2026-05-23 之前处于禁运期

* :cve:`2026-5068` 在 2026-05-21 之前处于禁运期

* :cve:`2026-5071` 在 2026-05-18 之前处于禁运期

* :cve:`2026-5072` 在 2026-05-18 之前处于禁运期

* :cve:`2026-5589` 在 2026-06-03 之前处于禁运期

* :cve:`2026-5590` `Zephyr 项目缺陷跟踪系统 GHSA-4vqm-pw24-g9jp <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-4vqm-pw24-g9jp>`_

API 变更
********

..
  Only removed, deprecated and new APIs. Changes go in migration guide.

移除的 API 与选项
=================

* 架构

  * Xtensa

    * 以下项已移除，因为它们属于架构特性：

      * :kconfig:option:`CONFIG_XTENSA_MMU_DOUBLE_MAP`
      * :kconfig:option:`CONFIG_XTENSA_RPO_CACHE`
      * :kconfig:option:`CONFIG_XTENSA_CACHED_REGION`
      * :kconfig:option:`CONFIG_XTENSA_UNCACHED_REGION`

* 蓝牙

  * ``CONFIG_BT_TBS_SUPPORTED_FEATURES``

  * 已弃用的 ``bt_hci_cmd_create()`` 函数已被移除，现由 :c:func:`bt_hci_cmd_alloc` 替代。

  * 控制器

    * :kconfig:option:`CONFIG_BT_CTLR_ADV_AUX_SET`、:kconfig:option:`CONFIG_BT_CTLR_ADV_SYNC_SET` 和 :kconfig:option:`CONFIG_BT_CTLR_ADV_DATA_BUF_MAX` 不再需要 :kconfig:option:`CONFIG_BT_CTLR_ADVANCED_FEATURES`

* 内核

  * :kconfig:option:`CONFIG_LINKER_USE_PINNED_SECTION` 和 :kconfig:option:`CONFIG_LINKER_GENERIC_SECTIONS_PRESENT_AT_BOOT` 已被移除。它们所启用的选择性内核固定模型在任何按需分页驱逐算法下都不安全：CPU 异常分发可能指向线程特权栈页面，而该页面不在显式 ``__pinned_*`` 集合中；若该页面已被驱逐，则会在 x86 上引发 #DF，或在 ARM64 上引发嵌套中止（:github:`108773`）。Zephyr 内核映像现在始终驻留在物理内存中；按需分页仅适用于匿名映射（:c:func:`k_mem_map`）和显式 ``__ondemand_*`` 链接器段。

  * ``__pinned_func``、``__pinned_data``、``__pinned_rodata``、``__pinned_bss`` 和 ``__pinned_noinit`` 属性宏已移除，其汇编别名 ``PINNED_TEXT``、``PINNED_RODATA``、``PINNED_DATA``、``PINNED_BSS`` 和 ``PINNED_NOINIT`` 也随之移除。

  * ``K_KERNEL_PINNED_STACK_DEFINE``、``K_KERNEL_PINNED_STACK_ARRAY_DEFINE``、``K_KERNEL_PINNED_STACK_ARRAY_DECLARE``、``K_THREAD_PINNED_STACK_DEFINE`` 和 ``K_THREAD_PINNED_STACK_ARRAY_DEFINE`` 宏已移除。请改用不带 pinned 的对应宏。

* Mbed TLS

  * ``CONFIG_PSA_WANT_KEY_TYPE_DES``
  * ``CONFIG_PSA_WANT_ECC_SECP_K1_192``
  * ``CONFIG_PSA_WANT_ECC_SECP_R1_192``
  * ``CONFIG_PSA_WANT_ECC_SECP_R1_224``
  * ``CONFIG_CUSTOM_MBEDTLS_CFG_FILE``
  * ``CONFIG_MBEDTLS_CHACHAPOLY_AEAD_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_AES_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_CAMELLIA_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_CCM_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_CHACHA20_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_DES_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_GCM_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_MODE_CBC_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_MODE_CTR_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_MODE_XTS_ENABLED``
  * ``CONFIG_MBEDTLS_CMAC``
  * ``CONFIG_MBEDTLS_DHM_C``
  * ``CONFIG_MBEDTLS_ECDH_C``
  * ``CONFIG_MBEDTLS_ECDSA_C``
  * ``CONFIG_MBEDTLS_ECDSA_DETERMINISTIC``
  * ``CONFIG_MBEDTLS_ECJPAKE_C``
  * ``CONFIG_MBEDTLS_ECP_ALL_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_C``
  * ``CONFIG_MBEDTLS_ECP_DP_BP256R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_BP384R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_BP512R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_CURVE25519_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_CURVE448_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP192K1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP192R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP224K1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP224R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP256K1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP256R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP384R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP521R1_ENABLED``
  * ``CONFIG_MBEDTLS_GENPRIME_ENABLED``
  * ``CONFIG_MBEDTLS_HKDF_C``
  * ``CONFIG_MBEDTLS_KEY_EXCHANGE_DHE_PSK_ENABLED``
  * ``CONFIG_MBEDTLS_KEY_EXCHANGE_DHE_RSA_ENABLED``
  * ``CONFIG_MBEDTLS_KEY_EXCHANGE_RSA_ENABLED``
  * ``CONFIG_MBEDTLS_KEY_EXCHANGE_RSA_PSK_ENABLED``
  * ``CONFIG_MBEDTLS_MD5``
  * ``CONFIG_MBEDTLS_PKCS1_V15``
  * ``CONFIG_MBEDTLS_PKCS1_V21``
  * ``CONFIG_MBEDTLS_POLY1305``
  * ``CONFIG_MBEDTLS_RSA_C``
  * ``CONFIG_MBEDTLS_SHA1``
  * ``CONFIG_MBEDTLS_SHA224``
  * ``CONFIG_MBEDTLS_SHA256``
  * ``CONFIG_MBEDTLS_SHA384``
  * ``CONFIG_MBEDTLS_SHA512``
  * ``CONFIG_MBEDTLS_USE_PSA_CRYPTO``

  * ``CONFIG_MBEDTLS_ENTROPY_POLL_ZEPHYR`` 已重命名为 :kconfig:option:`CONFIG_MBEDTLS_PSA_DRIVER_GET_ENTROPY`。

  * ``CONFIG_MBEDTLS_PEM_CERTIFICATE_FORMAT`` 已被其原先启用的底层选项取代：:kconfig:option:`CONFIG_MBEDTLS_PEM_PARSE_C`、:kconfig:option:`CONFIG_MBEDTLS_PEM_WRITE_C` 和 :kconfig:option:`CONFIG_MBEDTLS_BASE64_C`。

  * ``CONFIG_MBEDTLS_SERVER_NAME_INDICATION`` 已重命名为 :kconfig:option:`CONFIG_MBEDTLS_SSL_SERVER_NAME_INDICATION`。

  * ``CONFIG_MBEDTLS_TEST`` 已重命名为 :kconfig:option:`CONFIG_MBEDTLS_DEBUG_C`。

* 随机数

  * ``CONFIG_CSPRNG_AVAILABLE`` 已重命名为 :kconfig:option:`CONFIG_ENTROPY_NODE_ENABLED`。

已弃用的 API 和选项
===================

* 蓝牙

  * Mesh

    * 函数 :c:func:`bt_mesh_input_number` 已被弃用。应用应改用 :c:func:`bt_mesh_input_numeric`。
    * 结构体 :c:struct:`bt_mesh_prov` 中的回调 :c:member:`output_number` 已被弃用。应用应改用 :c:member:`output_numeric` 回调。
    * :kconfig:option:`CONFIG_BT_MESH_MODEL_VND_MSG_CID_FORCE` 选项已被弃用。

  * 主机

    * :c:member:`bt_conn_le_info.interval` 已被弃用。请改用 :c:member:`bt_conn_le_info.interval_us`。注意单位已发生变化：``interval`` 的单位为 1.25 毫秒，而 ``interval_us`` 的单位为微秒。
    * :kconfig:option:`CONFIG_DEVICE_NAME_GATT_WRITABLE_NONE` 选项已被弃用。应用应改用 :kconfig:option:`CONFIG_BT_DEVICE_NAME_GATT_WRITABLE_NONE` 选项。
    * :kconfig:option:`CONFIG_DEVICE_NAME_GATT_WRITABLE_ENCRYPT` 选项已被弃用。应用应改用 :kconfig:option:`CONFIG_BT_DEVICE_NAME_GATT_WRITABLE_ENCRYPT` 选项。
    * :kconfig:option:`CONFIG_DEVICE_NAME_GATT_WRITABLE_AUTHEN` 选项已被弃用。应用应改用 :kconfig:option:`CONFIG_BT_DEVICE_NAME_GATT_WRITABLE_AUTHEN` 选项。
    * :kconfig:option:`CONFIG_DEVICE_APPEARANCE_GATT_WRITABLE_AUTHEN` 选项已被弃用。应用应改用 :kconfig:option:`CONFIG_BT_DEVICE_APPEARANCE_GATT_WRITABLE_AUTHEN` 选项。

  * HCI

    * :c:macro:`BT_HCI_LE_SUPERVISON_TIMEOUT_MIN` 和 :c:macro:`BT_HCI_LE_SUPERVISON_TIMEOUT_MAX` 已被弃用。请改用 :c:macro:`BT_HCI_LE_SUPERVISION_TIMEOUT_MIN` 和 :c:macro:`BT_HCI_LE_SUPERVISION_TIMEOUT_MAX`。

* 熵源

   * :kconfig:option:`CONFIG_ENTROPY_PSA_CRYPTO_RNG` 已被弃用。

* I2S

  * 以下宏已被弃用，并替换为名称与 `latest revision of the I2S specification`_ 保持一致的等效宏。

    * :c:macro:`I2S_OPT_BIT_CLK_MASTER` -> :c:macro:`I2S_OPT_BIT_CLK_CONTROLLER`
    * :c:macro:`I2S_OPT_FRAME_CLK_MASTER` -> :c:macro:`I2S_OPT_FRAME_CLK_CONTROLLER`
    * :c:macro:`I2S_OPT_BIT_CLK_SLAVE` -> :c:macro:`I2S_OPT_BIT_CLK_TARGET`
    * :c:macro:`I2S_OPT_FRAME_CLK_SLAVE` -> :c:macro:`I2S_OPT_FRAME_CLK_TARGET`

.. _latest revision of the I2S specification: https://www.nxp.com/docs/en/user-manual/UM11732.pdf

* Mbed TLS

  * :kconfig:option:`CONFIG_MBEDTLS_USER_CONFIG_ENABLE` 和 :kconfig:option:`CONFIG_MBEDTLS_CFG_FILE` 已被弃用。请改用 :kconfig:option:`CONFIG_MBEDTLS_CONFIG_FILE`。

  * :kconfig:option:`CONFIG_MBEDTLS_LIBRARY` 已被弃用。请改用 :kconfig:option:`CONFIG_MBEDTLS_CUSTOM`。


* POSIX

  * :kconfig:option:`CONFIG_XOPEN_STREAMS` 已被弃用。请改用 :kconfig:option:`CONFIG_XSI_STREAMS`

* 随机数

  * :kconfig:option:`CONFIG_CTR_DRBG_CSPRNG_GENERATOR` 已被弃用。请改用 :kconfig:option:`CONFIG_PSA_CSPRNG_GENERATOR`。

* 传感器

  * NXP

    * 弃用 ``mcux_lpcmp`` 驱动（:zephyr_file:`drivers/sensor/nxp/mcux_lpcmp/mcux_lpcmp.c`）。该驱动目前计划在 Zephyr 4.6 中移除，``mcux_lpcmp`` 示例也将一并移除（:github:`100998`）。

* 定时器

  * 传统的 Cortex-M SysTick 低功耗伴随兼容宏 :c:macro:`z_cms_lptim_hook_on_lpm_entry` 和 :c:macro:`z_cms_lptim_hook_on_lpm_exit`，以及兼容头文件 :zephyr_file:`drivers/timer/cortex_m_systick.h`，已被弃用。树外 SoC/平台代码应迁移到 :c:func:`z_sys_clock_lpm_enter`、:c:func:`z_sys_clock_lpm_exit` 和 :zephyr_file:`include/zephyr/drivers/timer/system_timer_lpm.h`。以下传统 Kconfig 选项已被弃用：:kconfig:option:`CONFIG_CORTEX_M_SYSTICK_LPM_TIMER_NONE`、:kconfig:option:`CONFIG_CORTEX_M_SYSTICK_LPM_TIMER_COUNTER`、:kconfig:option:`CONFIG_CORTEX_M_SYSTICK_LPM_TIMER_HOOKS` 和 :kconfig:option:`CONFIG_CORTEX_M_SYSTICK_RESET_BY_LPM`，请改用 :kconfig:option:`CONFIG_SYSTEM_TIMER_LPM_COMPANION_NONE`、:kconfig:option:`CONFIG_SYSTEM_TIMER_LPM_COMPANION_COUNTER`、:kconfig:option:`CONFIG_SYSTEM_TIMER_LPM_COMPANION_HOOKS` 和 :kconfig:option:`CONFIG_SYSTEM_TIMER_RESET_BY_LPM`。chosen 属性 ``/chosen/zephyr,cortex-m-idle-timer`` 已被弃用，请改用 ``/chosen/zephyr,system-timer-companion``。该兼容垫片目前计划在 Zephyr 4.6.0 中移除。

新增 API 和选项
===============
..
  Link to new APIs here, in a group if you think it's necessary, no need to get
  fancy just list the link, that should contain the documentation. If you feel
  like you need to add more details, add them in the API documentation code
  instead.

.. zephyr-keep-sorted-start re(^\* \w)

* ADC

  * :c:macro:`ADC_DT_SPEC_GET_BY_IDX_OR`
  * :c:macro:`ADC_DT_SPEC_GET_BY_NAME_OR`
  * :c:macro:`ADC_DT_SPEC_GET_OR`
  * :c:macro:`ADC_DT_SPEC_INST_GET_BY_IDX_OR`
  * :c:macro:`ADC_DT_SPEC_INST_GET_BY_NAME_OR`
  * :c:macro:`ADC_DT_SPEC_INST_GET_OR`
  * :c:member:`adc_sequence.priority`
  * :kconfig:option:`CONFIG_ADC_SEQUENCE_PRIORITY`

* CPUFreq

  * :kconfig:option:`CONFIG_CPU_FREQ_POLICY_PRESSURE`

* DAC

  * 新增 DAC 驱动 API (:github:`104630`)

    * :c:struct:`dac_dt_spec`
    * :c:macro:`DAC_CHANNEL_CFG_DT`
    * :c:macro:`DAC_DT_SPEC_GET_BY_NAME`
    * :c:macro:`DAC_DT_SPEC_GET_BY_NAME_OR`
    * :c:macro:`DAC_DT_SPEC_INST_GET_BY_NAME`
    * :c:macro:`DAC_DT_SPEC_INST_GET_BY_NAME_OR`
    * :c:macro:`DAC_DT_SPEC_GET_BY_IDX`
    * :c:macro:`DAC_DT_SPEC_GET_BY_IDX_OR`
    * :c:macro:`DAC_DT_SPEC_INST_GET_BY_IDX`
    * :c:macro:`DAC_DT_SPEC_INST_GET_BY_IDX_OR`
    * :c:macro:`DAC_DT_SPEC_GET`
    * :c:macro:`DAC_DT_SPEC_GET_OR`
    * :c:macro:`DAC_DT_SPEC_INST_GET`
    * :c:macro:`DAC_DT_SPEC_INST_GET_OR`
    * :c:func:`dac_channel_setup_dt`
    * :c:func:`dac_write_value_dt`
    * :c:func:`dac_millivolts_to_raw`
    * :c:func:`dac_microvolts_to_raw`
    * :c:func:`dac_x_to_raw_dt_chan`
    * :c:func:`dac_millivolts_to_raw_dt`
    * :c:func:`dac_microvolts_to_raw_dt`
    * :c:func:`dac_is_ready_dt`

* DMA

  * 新增 DMA 驱动 (:dtcompatible:`nxp,4ch-dma`) (:github:`97841`)。

* Flash

  * :dtcompatible:`jedec,mspi-nor` 现在允许通过设备树分别配置读、写和控制命令的 MSPI。

  * 为 flash API 新增扩展操作，以支持将块标记为坏块（:c:enum:`FLASH_EX_OP_MARK_BAD_BLOCK`）以及检查块是否为坏块（:c:enum:`FLASH_EX_OP_IS_BAD_BLOCK`）。

* IPM

  * 邮箱后端的 IPM 回调现在能正确处理仅信号式的邮箱用法。当邮箱未提供数据缓冲区时，应用应准备好接收 IPM 回调中的 NULL 载荷指针。

* Mbed TLS

  * :kconfig:option:`CONFIG_TF_PSA_CRYPTO_USER_CONFIG_FILE`
  * :kconfig:option:`CONFIG_PSA_WANT_ALG_SHAKE128`
  * :kconfig:option:`CONFIG_PSA_WANT_ALG_SHAKE256`
  * :kconfig:option:`CONFIG_MBEDTLS_BASE64_C`
  * :kconfig:option:`CONFIG_MBEDTLS_PEM_PARSE_C`
  * :kconfig:option:`CONFIG_MBEDTLS_PEM_WRITE_C`
  * :kconfig:option:`CONFIG_MBEDTLS_PK_PARSE_C`
  * :kconfig:option:`CONFIG_MBEDTLS_SSL_KEYING_MATERIAL_EXPORT`
  * :kconfig:option:`CONFIG_MBEDTLS_VERSION_C`
  * :kconfig:option:`CONFIG_MBEDTLS_X509_CRT_PARSE_C`
  * :kconfig:option:`CONFIG_MBEDTLS_X509_RSASSA_PSS_SUPPORT`
  * :kconfig:option:`CONFIG_MBEDTLS_X509_USE_C`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS_ECDHE_ECDSA_WITH_AES_128_CCM_8`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA384`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS_PSK_WITH_AES_256_CBC_SHA384`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS_PSK_WITH_AES_128_GCM_SHA256`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_ECJPAKE_WITH_AES_128_CCM_8`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS1_3_AES_256_GCM_SHA384`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS1_3_AES_128_GCM_SHA256`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS1_3_AES_128_CCM_SHA256`
  * :kconfig:option:`CONFIG_MBEDTLS_CIPHERSUITE_TLS1_3_CHACHA20_POLY1305_SHA256`

* NVMEM

  * Flash 设备支持

    * :kconfig:option:`CONFIG_NVMEM_FLASH`
    * :kconfig:option:`CONFIG_NVMEM_FLASH_WRITE`

* OTP

  * 新的 OTP 驱动 API，提供烧录（:c:func:`otp_program()`）和读取（:c:func:`otp_read()`） :abbr:`OTP(One Time Programmable)` 存储器件的方法（:github:`101292`）。OTP 设备也可以通过 :ref:`非易失性存储器 (NVMEM)<nvmem>` 子系统访问。可用选项包括：

    * :kconfig:option:`CONFIG_OTP`
    * :kconfig:option:`CONFIG_OTP_PROGRAM`
    * :kconfig:option:`CONFIG_OTP_INIT_PRIORITY`

* PWM

  * 扩展 API，支持 PWM 事件

    * :c:struct:`pwm_event_callback`，用于保存 PWM 事件回调
    * :c:func:`pwm_init_event_callback`，用于初始化 :c:struct:`pwm_event_callback` 对象
    * :c:func:`pwm_add_event_callback`，用于添加回调
    * :c:func:`pwm_remove_event_callback`，用于移除回调
    * :c:struct:`pwm_driver_api` 中的 :c:member:`manage_event_callback`，用于管理 PWM 事件
    * :kconfig:option:`CONFIG_PWM_EVENT`

* Settings

  * :kconfig:option:`CONFIG_SETTINGS_SAVE_SINGLE_SUBTREE_WITHOUT_MODIFICATION`
  * :kconfig:option:`CONFIG_SETTINGS_SAVE_SINGLE_SUBTREE_WITHOUT_MODIFICATION_VALUE_SIZE`

* Shell

  * :c:func:`shell_readline`，用于 :ref:`用户输入 <shell-readline>`

* Sys

  * :c:macro:`COND_CASE_1`

* Zbus

   * :kconfig:option:`CONFIG_ZBUS_ASYNC_LISTENER`
   * :kconfig:option:`CONFIG_ZBUS_ASYNC_LISTENER_EXEC_TIMEOUT`
   * :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT`
   * :kconfig:option:`CONFIG_ZBUS_PROXY_AGENT_IPC`
   * :c:macro:`ZBUS_ASYNC_LISTENER_DEFINE`
   * :c:macro:`ZBUS_ASYNC_LISTENER_DEFINE_WITH_ENABLE`
   * :c:macro:`ZBUS_PROXY_AGENT_DEFINE`
   * :c:macro:`ZBUS_PROXY_ADD_CHAN`
   * :c:macro:`ZBUS_SHADOW_CHAN_DEFINE`
   * :c:macro:`ZBUS_SHADOW_CHAN_DEFINE_WITH_ID`
   * :c:func:`zbus_chan_from_name`。根据名称字符串获取 zbus 通道引用。
   * :c:func:`zbus_async_listener_set_work_queue`。为异步监听器观察者设置工作队列。
   * :c:func:`zbus_chan_pub_stats_msg_age`。获取自上次发布以来消息的存续时长（毫秒）。

* 以太网

  * 驱动 MAC 地址配置，支持 NVMEM cell。

    * :c:func:`net_eth_mac_load`
    * :c:struct:`net_eth_mac_config`
    * :c:macro:`NET_ETH_MAC_DT_CONFIG_INIT` 和 :c:macro:`NET_ETH_MAC_DT_INST_CONFIG_INIT`

  * 新增 :c:enum:`ethernet_stats_type`，并在 :c:struct:`ethernet_api` 中新增可选的 ``get_stats_type`` 回调，用于按类型（common、vendor 或 all）过滤以太网统计信息。支持厂商特定统计信息的驱动可实现 ``get_stats_type``，以便在仅请求 common 统计信息时跳过开销高昂的固件查询。现有 ``get_stats`` API 为保持向后兼容保持不变。

* 实用工具

  * :abbr:`COBS (Consistent Overhead Byte Stuffing)` 流式支持

    * :c:struct:`cobs_decoder`
    * :c:func:`cobs_decoder_init`
    * :c:func:`cobs_decoder_write`
    * :c:func:`cobs_decoder_close`
    * :c:struct:`cobs_encoder`
    * :c:func:`cobs_encoder_init`
    * :c:func:`cobs_encoder_write`
    * :c:func:`cobs_encoder_close`

  * 并查集支持 * :c:struct:`sys_set_node` * :c:func:`sys_set_makeset` * :c:func:`sys_set_find` * :c:func:`sys_set_union`

* 异常

  * :kconfig:option:`CONFIG_EXCEPTION_DUMP_HOOK_ONLY`

* 时间工具

  * :kconfig:option:`CONFIG_TIMEUTIL_APPLY_SKEW`

* 显示

  * :c:func:`display_register_event_cb` 和 :c:func:`display_unregister_event_cb`。
  * :kconfig:option:`CONFIG_SSD1325_DEFAULT_CONTRAST`
  * :kconfig:option:`CONFIG_SSD1325_CONV_BUFFER_LINES`
  * :kconfig:option:`CONFIG_SDL_DISPLAY_DEFAULT_PIXEL_FORMAT_XRGB_8888`
  * :kconfig:option:`CONFIG_SDL_DISPLAY_DEFAULT_PIXEL_FORMAT_BGR_888`
  * :kconfig:option:`CONFIG_SDL_DISPLAY_DEFAULT_PIXEL_FORMAT_ABGR_8888`
  * :kconfig:option:`CONFIG_SDL_DISPLAY_DEFAULT_PIXEL_FORMAT_RGBA_8888`
  * :kconfig:option:`CONFIG_SDL_DISPLAY_DEFAULT_PIXEL_FORMAT_BGRA_8888`
  * :c:enumerator:`PIXEL_FORMAT_XRGB_8888`
  * :c:enumerator:`PIXEL_FORMAT_BGR_888`
  * :c:enumerator:`PIXEL_FORMAT_ABGR_8888`
  * :c:enumerator:`PIXEL_FORMAT_RGBA_8888`
  * :c:enumerator:`PIXEL_FORMAT_BGRA_8888`
  * :c:macro:`PANEL_PIXEL_FORMAT_XRGB_8888`
  * :kconfig:option:`CONFIG_SDL_DISPLAY_ROUNDED_MASK`
  * :kconfig:option:`CONFIG_SDL_DISPLAY_ROUNDED_MASK_COLOR`
  * :dtcompatible:`sharp,ls0xx` 的 ``serial-vcom-inversion`` 和 ``serial-vcom-interval`` 属性。
  * :kconfig:option:`CONFIG_LS0XX_VCOM_THREAD_PRIO`

* 构建系统

  * 新增 ``zephyr_constants_library()`` CMake 函数，用于生成包含由 C 结构体布局推导出的构建时常量的头文件（:github:`104861`）。

  * 新增 :ref:`slot1-partition <snippet-slot1-partition>` 片段。

  * Sysbuild

    * 新增 :kconfig:option:`SB_CONFIG_MERGED_HEX_FILES`，允许生成 :ref:`合并的 hex 文件 <sysbuild_merged_hex_files>`。

    * 新增实验性的 ``ExternalZephyrVariantProject_Add()`` sysbuild CMake 函数，允许向基于构建中现有映像的项目添加 :ref:`变体映像<sysbuild_zephyr_application>`。

    * 新增 :kconfig:option:`SB_CONFIG_MCUBOOT_DIRECT_XIP_GENERATE_VARIANT`，在使用 direct-xip 模式的 MCUboot 时，可在 sysbuild 项目中自动生成 slot 1 映像。

* 架构

  * Xtensa

    * :kconfig:option:`CONFIG_XTENSA_MMU_USE_DEFAULT_MAPPINGS`

* 步进电机

  * :c:func:`stepper_ctrl_configure_ramp`

* 用户空间

  * :c:func:`k_object_access_check`
  * :c:func:`k_mem_domain_deinit`

* 电源

  * :dtcompatible:`st,stm32u5-pwr` 新增的 ``voltage-scale`` 属性可通过设备树在 STM32U5 系列上手动选择电压档位。这尤其使 USB 控制器能够在更低的系统时钟频率下使用。

* 硬件自旋锁

  * 新增 hwspinlock 驱动 (:dtcompatible:`nxp,sema42`) (:github:`101499`)。

* 管理

  * MCUmgr

    * :kconfig:option:`CONFIG_UART_MCUMGR_RAW_PROTOCOL`、:kconfig:option:`CONFIG_MCUMGR_TRANSPORT_RAW_UART`、:kconfig:option:`CONFIG_MCUMGR_TRANSPORT_RAW_UART_INPUT_TIMEOUT`、:kconfig:option:`CONFIG_MCUMGR_TRANSPORT_RAW_UART_INPUT_TIMEOUT_TIME_MS`，详见 :ref:`raw UART MCUmgr SMP transport <mcumgr_smp_transport_raw_uart>`。

* 网络

  * CoAP

    * :kconfig:option:`CONFIG_COAP_CLIENT_MULTICAST`

  * DHCP

    * :c:func:`net_dhcpv4_server_set_address_validator_cb`

  * LwM2M

    * :kconfig:option:`CONFIG_LWM2M_SEND_SCHEDULER`
    * :kconfig:option:`CONFIG_LWM2M_IPSO_MAGNETOMETER`
    * :c:func:`lwm2m_cache_free_slots_get`

  * 其他

    * :kconfig:option:`CONFIG_WIREGUARD`
    * :kconfig:option:`CONFIG_NET_ZPERF_RAW_TX`
    * :kconfig:option:`CONFIG_FTP_CLIENT`

  * OpenThread

    * :kconfig:option:`CONFIG_OPENTHREAD_ZEPHYR_BORDER_ROUTER_NAT64_TRANSLATOR`

  * 套接字

    * DTLS 服务器套接字现在支持在单个套接字上并行处理多个客户端会话。
    * :kconfig:option:`CONFIG_NET_SOCKETS_TLS_CONNECT_TIMEOUT`

  * Wi-Fi

    * 新增对 Wi-Fi Direct (P2P) 模式的支持。
    * 新增对 WEP（有线等效加密）安全机制的支持。该功能默认禁用，可通过 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WEP` 启用
    * 默认使用 PSA crypto 而非旧版实现。可通过 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_MBEDTLS_PSA` 选项控制。
    * :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CLEANUP_INTERVAL`
    * :kconfig:option:`CONFIG_WIFI_NM_HOSTAPD_CLEANUP_INTERVAL`

* 蓝牙

  * 音频

    * :c:func:`bt_bap_ep_get_conn`
    * :c:member:`bt_ccp_call_control_client_cb.user_data`
    * :kconfig:option:`CONFIG_BT_TBS_MAX_FRIENDLY_NAME_LENGTH`
    * :c:member:`bt_cap_handover_cb.unicast_to_broadcast_created`
    * :c:func:`bt_tbs_client_get_by_index`
    * :c:member:`bt_bap_unicast_client_cb.supported_contexts`

  * 主机

    * :c:func:`bt_gatt_cb_unregister`：新增用于注销 GATT 回调处理程序的 API。
    * :c:func:`bt_le_per_adv_sync_cb_unregister`

  * ISO

    * 对于单播（CIS）通道，:c:member:`bt_iso_chan_ops.disconnected` 现在将始终在 :c:member:`bt_conn_cb.disconnected` 之前调用，以提供更确定的回调事件顺序（:github:`104695`）。

  * Mesh

    * :c:func:`bt_mesh_input_numeric`，用于在配网过程中提供数字输入的 OOB 值。
    * :c:struct:`bt_mesh_prov` 结构体中的 :c:member:`output_numeric` 回调，用于在配网过程中输出数字值。
    * :kconfig:option:`CONFIG_BT_MESH_CDB_KEY_SYNC`，用于在密钥刷新过程中添加、删除或更新密钥时，在配置数据库（CDB）与本地 Subnet 和 AppKey 存储之间启用密钥同步。该选项默认启用。

  * 服务

    * 引入告警通知服务 (ANS) :kconfig:option:`CONFIG_BT_ANS`

* 视频

  * :kconfig:option:`CONFIG_VIDEO_BUFFER_POOL_HEAP_SIZE`
  * :kconfig:option:`CONFIG_VIDEO_BUFFER_POOL_ZEPHYR_REGION`
  * :kconfig:option:`CONFIG_VIDEO_BUFFER_POOL_ZEPHYR_REGION_NAME`
  * :c:func:`video_transform_cap`
  * :c:macro:`VIDEO_PIX_FMT_SBGGR8P16`
  * :c:macro:`VIDEO_PIX_FMT_SGBRG8P16`
  * :c:macro:`VIDEO_PIX_FMT_SGRBG8P16`
  * :c:macro:`VIDEO_PIX_FMT_SRGGB8P16`
  * :c:macro:`VIDEO_PIX_FMT_Y8P16`
  * :c:macro:`VIDEO_FMT_IS_SEMI_PLANAR`
  * :c:macro:`VIDEO_FMT_IS_PLANAR`
  * :c:macro:`VIDEO_FMT_IS_GRAYSCALE`
  * :c:macro:`VIDEO_FMT_IS_BAYER`
  * :c:macro:`VIDEO_FMT_IS_RGB`
  * :c:macro:`VIDEO_FMT_IS_YUV`
  * :c:macro:`VIDEO_FMT_IS_MIPI_PACKED`
  * :c:macro:`VIDEO_FMT_IS_PADDED`
  * :c:macro:`VIDEO_FMT_IS_SEMI_PLANAR`
  * :c:macro:`VIDEO_FMT_IS_FULL_PLANAR`
  * :c:macro:`VIDEO_FOREACH_BAYER`
  * :c:macro:`VIDEO_FOREACH_BAYER_PADDED`
  * :c:macro:`VIDEO_FOREACH_BAYER_MIPI_PACKED`
  * :c:macro:`VIDEO_FOREACH_BAYER_NON_PACKED`
  * :c:macro:`VIDEO_FOREACH_GRAYSCALE`
  * :c:macro:`VIDEO_FOREACH_GRAYSCALE_NON_PACKED`
  * :c:macro:`VIDEO_FOREACH_GRAYSCALE_PADDED`
  * :c:macro:`VIDEO_FOREACH_GRAYSCALE_MIPI_PACKED`
  * :c:macro:`VIDEO_FOREACH_RGB`
  * :c:macro:`VIDEO_FOREACH_RGB_PACKED`
  * :c:macro:`VIDEO_FOREACH_RGB_NON_PACKED`
  * :c:macro:`VIDEO_FOREACH_RGB_ALPHA`
  * :c:macro:`VIDEO_FOREACH_RGB_PADDED`
  * :c:macro:`VIDEO_FOREACH_YUV`
  * :c:macro:`VIDEO_FOREACH_YUV_NON_PLANAR`
  * :c:macro:`VIDEO_FOREACH_YUV_SEMI_PLANAR`
  * :c:macro:`VIDEO_FOREACH_YUV_FULL_PLANAR`
  * :c:macro:`VIDEO_FOREACH_COMPRESSED`
  * :c:func:`video_import_buffer`

* 触觉反馈

  * 为 API 新增错误回调

    * :c:enum:`haptics_error_type`，用于枚举触觉设备中的常见故障状态。
    * :c:type:`haptics_error_callback_t`，提供错误回调的函数原型。
    * :c:func:`haptics_register_error_callback`，用于向驱动注册错误回调。

* 调制解调器

  * :kconfig:option:`CONFIG_MODEM_HL78XX_AT_SHELL`
  * :kconfig:option:`CONFIG_MODEM_HL78XX_AIRVANTAGE`

* 随机数

  * :kconfig:option:`CONFIG_PSA_CSPRNG_GENERATOR`

* 音频

  * :c:macro:`PDM_DT_IO_CFG_GET`
  * :c:macro:`PDM_DT_HAS_LEFT_CHANNEL`
  * :c:macro:`PDM_DT_HAS_RIGHT_CHANNEL`

.. zephyr-keep-sorted-stop

.. _boards_added_in_zephyr_4_4:

新增开发板
**********

..
  You may update this list as you contribute a new board during the release cycle, in order to make
  it visible to people who might be looking at the working draft of the release notes. However, note
  that this list will be recomputed at the time of the release, so you don't *have* to update it.
  In any case, just link the board, further details go in the board description.


* Adafruit Industries, LLC

   * :zephyr:board:`adafruit_feather_propmaker_rp2040` (``adafruit_feather_propmaker_rp2040``)
   * :zephyr:board:`adafruit_feather_scorpio_rp2040` (``adafruit_feather_scorpio_rp2040``)

* Advanced Micro Devices (AMD), Inc.

   * :zephyr:board:`versal2_apu` (``versal2_apu``)
   * :zephyr:board:`versal_apu` (``versal_apu``)
   * :zephyr:board:`versal_rpu` (``versal_rpu``)

* Ai-Thinker Co., Ltd.

   * :zephyr:board:`ai_m61_32s_kit` (``ai_m61_32s_kit``)

* Alientek

   * :zephyr:board:`dnesp32s3b` (``dnesp32s3b``)

* Alif Semiconductor

   * :zephyr:board:`ensemble_e1c_dk` (``ensemble_e1c_dk``)
   * :zephyr:board:`ensemble_e8_dk` (``ensemble_e8_dk``)

* Analog Devices, Inc.

   * :zephyr:board:`adi_eval_adin2111d1z` (``adi_eval_adin2111d1z``)

* ARM Ltd.

   * :zephyr:board:`fvp_base_revc_2xaem` (``fvp_base_revc_2xaem``)

* BlackBerry Limited

   * :zephyr:board:`qnxhv_vm` (``qnxhv_vm``)

* Bouffalo Lab (Nanjing) Co., Ltd.

   * :zephyr:board:`bl706_iot_dvk` (``bl706_iot_dvk``)

* Cadence Design Systems Inc.

   * Cadence SweRV (``cdns_swerv``)

* Chengdu Heltec Automation Technology Co., Ltd.

   * :zephyr:board:`heltec_wifi_lora32_v3` (``heltec_wifi_lora32_v3``)
   * :zephyr:board:`heltec_wireless_tracker` (``heltec_wireless_tracker``)

* Cirrus Logic, Inc.

   * :zephyr:board:`crd40l50` (``crd40l50``)

* Cytron Technologies

   * :zephyr:board:`maker_nano_rp2040` (``maker_nano_rp2040``)
   * :zephyr:board:`maker_pi_rp2040` (``maker_pi_rp2040``)
   * :zephyr:board:`maker_uno_rp2040` (``maker_uno_rp2040``)
   * :zephyr:board:`motion_2350_pro` (``motion_2350_pro``)

* DFRobot

   * :zephyr:board:`beetle_esp32c3` (``beetle_esp32c3``)
   * :zephyr:board:`beetle_rp2350` (``beetle_rp2350``)

* Elan Microelectronic Corp.

   * :zephyr:board:`32f967_dv` (``32f967_dv``)

* Espressif Systems

   * :zephyr:board:`esp32c5_devkitc` (``esp32c5_devkitc``)
   * :zephyr:board:`esp_threadbr` (``esp_threadbr``)

* Ezurio

   * :zephyr:board:`lyra_24_dvk_p10` (``lyra_24_dvk_p10``)
   * :zephyr:board:`lyra_24_dvk_p20` (``lyra_24_dvk_p20``)
   * :zephyr:board:`lyra_24_dvk_p20rf` (``lyra_24_dvk_p20rf``)
   * :zephyr:board:`lyra_24_dvk_s10` (``lyra_24_dvk_s10``)
   * :zephyr:board:`lyra_dvk_p` (``lyra_dvk_p``)
   * :zephyr:board:`lyra_dvk_s` (``lyra_dvk_s``)
   * :zephyr:board:`rm126x_dvk_rm1261` (``rm126x_dvk_rm1261``)
   * :zephyr:board:`rm126x_dvk_rm1262` (``rm126x_dvk_rm1262``)

* FocalTech Systems Co.,Ltd

   * :zephyr:board:`ft9001_eval` (``ft9001_eval``)

* Framework Computer, Inc.

   * :zephyr:board:`framework_ledmatrix` (``framework_ledmatrix``)
   * :zephyr:board:`framework_laptop16_keyboard` (``framework_laptop16_keyboard``)

* Infineon Technologies

   * :zephyr:board:`cy8ckit_041s_max` (``cy8ckit_041s_max``)
   * :zephyr:board:`cy8cproto_041tp` (``cy8cproto_041tp``)
   * :zephyr:board:`kit_t2g_b_h_evk` (``kit_t2g_b_h_evk``)
   * :zephyr:board:`kit_t2g_b_h_lite` (``kit_t2g_b_h_lite``)

* Intel Corporation

   * :zephyr:board:`intel_wcl_crb` (``intel_wcl_crb``)

* Longan Labs (Shenzhen Longan Technology Co., Ltd.)

   * :zephyr:board:`canbed_rp2040` (``canbed_rp2040``)

* M5Stack

   * :zephyr:board:`m5stack_nanoc6` (``m5stack_nanoc6``)

* Makerbase Co., Ltd.

   * :zephyr:board:`mks_canable_v10` (``mks_canable_v10``)

* MediaTek Inc.

   * MT8365 ADSP (``mt8365``)

* Microchip Technology Inc.

   * :zephyr:board:`pic32cm_pl10_cnano` (``pic32cm_pl10_cnano``)
   * :zephyr:board:`pic32cx_sg41_cult` (``pic32cx_sg41_cult``)
   * :zephyr:board:`pic32cz_ca90_cult` (``pic32cz_ca90_cult``)
   * :zephyr:board:`pic64gx_curiosity_kit` (``pic64gx_curiosity_kit``)
   * :zephyr:board:`sam_e54_cult` (``sam_e54_cult``)

* Nordic Semiconductor

   * :zephyr:board:`nrf54l15tag` (``nrf54l15tag``)
   * :zephyr:board:`nrf7120dk` (``nrf7120dk``)

* Nuvoton Technology Corporation

   * :zephyr:board:`numaker_gai_m55m1` (``numaker_gai_m55m1``)

* NXP Semiconductors

   * :zephyr:board:`frdm_imxrt1186` (``frdm_imxrt1186``)
   * :zephyr:board:`frdm_ke16z` (``frdm_ke16z``)
   * :zephyr:board:`frdm_mcxa577` (``frdm_mcxa577``)
   * :zephyr:board:`frdm_mcxl255` (``frdm_mcxl255``)
   * :zephyr:board:`frdm_mcxw70` (``frdm_mcxw70``)
   * :zephyr:board:`s32k5xxcvb` (``s32k5xxcvb``)

* 其他

   * :zephyr:board:`doit_esp32_devkit_v1` (``doit_esp32_devkit_v1``)
   * :zephyr:board:`esp32c3_lckfb` (``esp32c3_lckfb``)

* PCB Cupid

   * :zephyr:board:`glyph_c3` (``glyph_c3``)
   * :zephyr:board:`glyph_h2` (``glyph_h2``)

* PHYTEC

   * :zephyr:board:`phyboard_atlas` (``phyboard_atlas``)

* Pimoroni Ltd.

   * :zephyr:board:`tiny2040` (``tiny2040``)

* QEMU

   * :zephyr:board:`qemu_or1k` (``qemu_or1k``)

* Qualcomm Technologies, Inc

   * :zephyr:board:`qcc744m_evk` (``qcc744m_evk``)

* RAKwireless Technology Limited

   * :zephyr:board:`rak11160` (``rak11160``)

* Realtek Semiconductor Corp.

   * :zephyr:board:`rtl8721f_evb` (``rtl8721f_evb``)
   * :zephyr:board:`rtl872xd_evb` (``rtl872xd_evb``)
   * :zephyr:board:`rtl872xda_evb` (``rtl872xda_evb``)
   * :zephyr:board:`rtl8752h_evb` (``rtl8752h_evb``)
   * :zephyr:board:`rtl87x2g_evb_a` (``rtl87x2g_evb_a``)
   * :zephyr:board:`rts5817_maa_evb` (``rts5817_maa_evb``)

* Renesas Electronics Corporation

   * :zephyr:board:`aik_ra8d1` (``aik_ra8d1``)
   * :zephyr:board:`cpkcor_ra8d1b` (``cpkcor_ra8d1b``)
   * :zephyr:board:`ek_ra8t2` (``ek_ra8t2``)
   * :zephyr:board:`fpb_ra0e1` (``fpb_ra0e1``)
   * :zephyr:board:`fpb_ra8e1` (``fpb_ra8e1``)
   * :zephyr:board:`fpb_rx140` (``fpb_rx140``)
   * :zephyr:board:`fpb_rx14t` (``fpb_rx14t``)
   * :zephyr:board:`mcb_rx14t` (``mcb_rx14t``)
   * :zephyr:board:`mck_ra4t1` (``mck_ra4t1``)
   * :zephyr:board:`rsk_rx140` (``rsk_rx140``)
   * :zephyr:board:`rzg3e_smarc` (``rzg3e_smarc``)
   * :zephyr:board:`rzn2h_evb` (``rzn2h_evb``)
   * :zephyr:board:`rzt2h_evb` (``rzt2h_evb``)

* Retronix Technology Inc.

   * :zephyr:board:`sparrowhawk_rcar_v4h` (``sparrowhawk_rcar_v4h``)

* Seeed Technology Co., Ltd

   * :zephyr:board:`reterminal_e1002` (``reterminal_e1002``)
   * :zephyr:board:`xiao_rp2350` (``xiao_rp2350``)

* Shenzhen Holyiot Technology Co., Ltd.

   * :zephyr:board:`holyiot_21014` (``holyiot_21014``)
   * :zephyr:board:`holyiot_25008` (``holyiot_25008``)

* Shenzhen Sipeed Technology Co., Ltd.

   * :zephyr:board:`maix_m0s_dock` (``maix_m0s_dock``)

* Shenzhen Xunlong Software CO.,Limited

   * :zephyr:board:`opi_zero` (``opi_zero``)
   * :zephyr:board:`orangepi_5_ultra_rk3588` (``orangepi_5_ultra_rk3588``)

* Silicon Laboratories

   * :zephyr:board:`efm32tg_stk3300` (``efm32tg_stk3300``)
   * :zephyr:board:`xg28_ek2705a` (``xg28_ek2705a``)
   * :zephyr:board:`siwx917_rb4338a` (``siwx917_rb4338a``)
   * :zephyr:board:`siwx917_rb4342a` (``siwx917_rb4342a``)

* Soldered Electronics

   * :zephyr:board:`inkplate_6color` (``inkplate_6color``)

* Space Cubics Inc.

   * :zephyr:board:`scobc_v1` (``scobc_v1``)

* SparkFun Electronics

   * :zephyr:board:`sparkfun_rp2040_mikrobus` (``sparkfun_rp2040_mikrobus``)

* STMicroelectronics

   * :zephyr:board:`nucleo_c542rc` (``nucleo_c542rc``)
   * :zephyr:board:`nucleo_c562re` (``nucleo_c562re``)
   * :zephyr:board:`nucleo_c5a3zg` (``nucleo_c5a3zg``)
   * :zephyr:board:`nucleo_u3c5zi_q` (``nucleo_u3c5zi_q``)
   * :zephyr:board:`nucleo_wba25ce1` (``nucleo_wba25ce1``)
   * :zephyr:board:`stm32h5f5j_dk` (``stm32h5f5j_dk``)
   * :zephyr:board:`stm32mp215f_dk` (``stm32mp215f_dk``)

* Synaptics

   * :zephyr:board:`sr100_rdk` (``sr100_rdk``)

* Texas Instruments

   * :zephyr:board:`am62l_evm` (``am62l_evm``)
   * :zephyr:board:`cc1312r1_launchxl` (``cc1312r1_launchxl``)

* Third Reality, Inc.

   * :zephyr:board:`3r_tnh_sensor_lite` (``3r_tnh_sensor_lite``)

* u-blox

   * :zephyr:board:`ubx_evkninab5` (``ubx_evkninab5``)

* Vicharak

   * :zephyr:board:`shrike_lite` (``shrike_lite``)

* VIEWE Display Co., Ltd.

   * :zephyr:board:`uedx24320028e_wb_a` (``uedx24320028e_wb_a``)

* Waveshare Electronics

   * :zephyr:board:`esp32s3_geek` (``esp32s3_geek``)
   * :zephyr:board:`esp32s3_rlcd_4_2` (``esp32s3_rlcd_4_2``)
   * :zephyr:board:`rp2350_zero` (``rp2350_zero``)

* WeAct Studio

   * :zephyr:board:`can485dbv1` (``can485dbv1``)
   * :zephyr:board:`rp2350b_core` (``rp2350b_core``)
   * :zephyr:board:`weact_stm32g0b1_core` (``weact_stm32g0b1_core``)

* WEMOS Electronics

   * :zephyr:board:`lolin32_lite` (``lolin32_lite``)

* WinChipHead

   * :zephyr:board:`ch32v307v_evt_r1` (``ch32v307v_evt_r1``)

.. _shields_added_in_zephyr_4_4:

新增扩展板
**********

..
  Same as above, this will also be recomputed at the time of the release.

* :ref:`Adafruit FeatherWing 128x64 OLED Shield <adafruit_featherwing_128x64_oled>`
* :ref:`Adafruit HTS221 Shield <adafruit_hts221>`
* :ref:`Adafruit INA3221 Shield <adafruit_ina3221>`
* :ref:`Adafruit MAX17048 Shield <adafruit_max17048>`
* :ref:`Adafruit MCP4728 Quad DAC Shield <adafruit_mcp4728>`
* :ref:`Analog Devices EVAL-CN0391-ARDZ <eval_cn0391_ardz>`
* :ref:`Arduino Modulino Latch Relay <arduino_modulino_latch_relay>`
* :ref:`ESP Thread BR / Zigbee GW Ethernet <esp_threadbr_ethernet>`
* :ref:`Microchip RNBD451 Add-on Board <rnbd451_add_on_shield>`
* :ref:`MikroElektronika 3 axis Accel 4 Click <mikroe_accel4_click_shield>`
* :ref:`MikroElektronika CAN FD 6 Click <mikroe_can_fd_6_click_shield>`
* :ref:`MikroElektronika EEPROM 13 Click <mikroe_eeprom_13_click_shield>`
* :ref:`MikroElektronika Flash 5 Click <mikroe_flash_5_click_shield>`
* :ref:`MikroElektronika Flash 6 Click <mikroe_flash_6_click_shield>`
* :ref:`MikroElektronika Flash 8 Click <mikroe_flash_8_click_shield>`
* :ref:`MikroElektronika LTE IoT 7 Click <mikroe_lte_iot7_click_shield>`
* :ref:`MikroElektronika MCP251x Click shields <mikroe_mcp251x_click_shield>`
* :ref:`MikroElektronika MCP251xFD Click shields <mikroe_mcp251xfd_click_shield>`
* :ref:`MikroElektronika RS485 Isolator 5 Click <mikroe_rs485_isolator_5_click_shield>`
* :ref:`MikroElektronika Temp&Hum Click <mikroe_temp_hum_click_shield>`
* :ref:`Nordic Semiconductor nRF7002 EB II <nrf7002eb2>`
* :ref:`NXP S32K5XX-MB Shield <nxp_s32k5xx_mb>`
* :ref:`Raspberry Pi Camera Module 2 <raspberry_pi_camera_module_2>`
* :ref:`Renesas AIK OV2640 Camera Shield <renesas_aik_ov2640_cam>`
* :ref:`Seeed Studio 24GHz mmWave Sensor for XIAO <seeed_xiao_hsp24>`
* :ref:`Semtech SX1261MB2BAS LoRa Shield <semtech_sx1261mb2bas>`
* :ref:`ST Microelectronics B-DSI-MB1314 <st_b_dsi_mb1314>`
* :ref:`ST Microelectronics ST87MXX shield <st87mxx_generic>`
* :ref:`ST Microelectronics X-NUCLEO-IKS5A1: MEMS Inertial and Environmental Multi sensor shield <x-nucleo-iks5a1>`
* :ref:`WIZnet W5500 Ethernet Shield <wiznet_w5500>`
* :ref:`ZHAW Luma Matrix Shield <zhaw_lumamatrix>`

新增驱动
********

..
  Same as above, this will also be recomputed at the time of the release.
  Just link the driver, further details go in the binding description

* :abbr:`ADC (Analog to Digital Converter)`

   * :dtcompatible:`bflb,adc` (:github:`98624`)
   * :dtcompatible:`infineon,sar-adc` (:github:`103453`)
   * :dtcompatible:`maxim,max2253x` (:github:`102115`)
   * :dtcompatible:`microchip,adc-g1` (:github:`99966`)
   * :dtcompatible:`microchip,mcp3221` (:github:`105751`)
   * :dtcompatible:`renesas,ra-adc12` (:github:`95710`)
   * :dtcompatible:`renesas,ra-adc16` (:github:`95710`)
   * :dtcompatible:`renesas,rz-adc-e` (:github:`100575`)
   * :dtcompatible:`renesas,rza2m-adc` (:github:`100637`)
   * :dtcompatible:`sifli,sf32lb-gpadc` (:github:`99460`)
   * :dtcompatible:`ti,ads7950` (:github:`101660`)
   * :dtcompatible:`ti,ads7951` (:github:`101660`)
   * :dtcompatible:`ti,ads7952` (:github:`101660`)
   * :dtcompatible:`ti,ads7953` (:github:`101660`)
   * :dtcompatible:`ti,ads7954` (:github:`101660`)
   * :dtcompatible:`ti,ads7955` (:github:`101660`)
   * :dtcompatible:`ti,ads7956` (:github:`101660`)
   * :dtcompatible:`ti,ads7957` (:github:`101660`)
   * :dtcompatible:`ti,ads7958` (:github:`101660`)
   * :dtcompatible:`ti,ads7959` (:github:`101660`)
   * :dtcompatible:`ti,ads7960` (:github:`101660`)
   * :dtcompatible:`ti,ads7961` (:github:`101660`)

* ARM 架构

   * :dtcompatible:`arm,axi-timing-adapter` (:github:`100356`)
   * :dtcompatible:`nordic,nrf-pwr-antswc` (:github:`101199`)
   * :dtcompatible:`nordic,nrf-tampc` (:github:`99295`)

* 音频

   * :dtcompatible:`awinic,aw88298` (:github:`97006`)
   * :dtcompatible:`infineon,pdm` (:github:`104698`)
   * :dtcompatible:`sifli,sf32lb-audcodec` (:github:`98701`)
   * :dtcompatible:`zephyr,pdm-dmic` (:github:`99351`)

* 生物特征识别

   * :dtcompatible:`adh-tech,gt5x` (:github:`100139`)
   * :dtcompatible:`zephyr,biometrics-emul` (:github:`100139`)
   * :dtcompatible:`zhiantec,zfm-x0` (:github:`100139`)

* 蓝牙

   * :dtcompatible:`bflb,bl70x-bt-hci` (:github:`104346`)
   * :dtcompatible:`infineon,bt-hci-uart` (:github:`103871`)
   * :dtcompatible:`realtek,bee-bt-hci` (:github:`104580`)
   * :dtcompatible:`sifli,sf32lb-mailbox` (:github:`96692`)

* :abbr:`CAN (Controller Area Network)`

   * :dtcompatible:`infineon,can` (:github:`105471`)
   * :dtcompatible:`infineon,canfd-controller` (:github:`105471`)

* 充电器

   * :dtcompatible:`nordic,npm10xx-charger` (:github:`105564`)
   * :dtcompatible:`ti,bq25186` (:github:`97157`)
   * :dtcompatible:`ti,bq25188` (:github:`97157`)
   * :dtcompatible:`zephyr,charger-gpio` (:github:`103112`)

* 时钟控制

   * :dtcompatible:`alif,clockctrl` (:github:`101244`)
   * :dtcompatible:`bflb,bl70x_l-clock-controller` (:github:`104625`)
   * :dtcompatible:`bflb,bl70x_l-dll` (:github:`104625`)
   * :dtcompatible:`bflb,f32k` (:github:`104738`)
   * :dtcompatible:`bflb,pll` (:github:`104738`)
   * :dtcompatible:`bflb,root-clk` (:github:`104738`)
   * :dtcompatible:`elan,em32-ahb` (:github:`97843`)
   * :dtcompatible:`elan,em32-apb` (:github:`97843`)
   * :dtcompatible:`focaltech,ft9001-cpm` (:github:`95959`)
   * :dtcompatible:`microchip,pic32cm-jh-clock` (:github:`97160`)
   * :dtcompatible:`microchip,pic32cm-jh-fdpll` (:github:`97160`)
   * :dtcompatible:`microchip,pic32cm-jh-gclkgen` (:github:`97160`)
   * :dtcompatible:`microchip,pic32cm-jh-gclkperiph` (:github:`97160`)
   * :dtcompatible:`microchip,pic32cm-jh-mclkcpu` (:github:`97160`)
   * :dtcompatible:`microchip,pic32cm-jh-mclkperiph` (:github:`97160`)
   * :dtcompatible:`microchip,pic32cm-jh-osc32k` (:github:`97160`)
   * :dtcompatible:`microchip,pic32cm-jh-osc48m` (:github:`97160`)
   * :dtcompatible:`microchip,pic32cm-jh-rtc` (:github:`97160`)
   * :dtcompatible:`microchip,pic32cm-jh-xosc` (:github:`97160`)
   * :dtcompatible:`microchip,pic32cm-jh-xosc32k` (:github:`97160`)
   * :dtcompatible:`microchip,pic32cm-pl-clock` (:github:`104337`)
   * :dtcompatible:`microchip,pic32cm-pl-gclkgen` (:github:`104337`)
   * :dtcompatible:`microchip,pic32cm-pl-gclkperiph` (:github:`104337`)
   * :dtcompatible:`microchip,pic32cm-pl-mclkcpu` (:github:`104337`)
   * :dtcompatible:`microchip,pic32cm-pl-mclkperiph` (:github:`104337`)
   * :dtcompatible:`microchip,pic32cm-pl-osc32k` (:github:`104337`)
   * :dtcompatible:`microchip,pic32cm-pl-oschf` (:github:`104337`)
   * :dtcompatible:`microchip,pic32cm-pl-rtc` (:github:`104337`)
   * :dtcompatible:`microchip,pic32cm-pl-xosc32k` (:github:`104337`)
   * :dtcompatible:`microchip,pic32cz-ca-clock` (:github:`101934`)
   * :dtcompatible:`microchip,pic32cz-ca-dfll48m` (:github:`101934`)
   * :dtcompatible:`microchip,pic32cz-ca-dpll` (:github:`101934`)
   * :dtcompatible:`microchip,pic32cz-ca-gclkgen` (:github:`101934`)
   * :dtcompatible:`microchip,pic32cz-ca-gclkperiph` (:github:`101934`)
   * :dtcompatible:`microchip,pic32cz-ca-mclkdomain` (:github:`101934`)
   * :dtcompatible:`microchip,pic32cz-ca-mclkperiph` (:github:`101934`)
   * :dtcompatible:`microchip,pic32cz-ca-rtc` (:github:`101934`)
   * :dtcompatible:`microchip,pic32cz-ca-xosc` (:github:`101934`)
   * :dtcompatible:`microchip,pic32cz-ca-xosc32k` (:github:`101934`)
   * :dtcompatible:`nordic,nrf71-hfxo` (:github:`103349`)
   * :dtcompatible:`nordic,nrf71-lfxo` (:github:`101199`)
   * :dtcompatible:`realtek,ameba-rcc` (:github:`104843`)
   * :dtcompatible:`realtek,bee-cctl` (:github:`102691`)
   * :dtcompatible:`realtek,rts5817-clock` (:github:`91486`)
   * :dtcompatible:`renesas,r8a779g0-cpg-mssr` (:github:`97783`)
   * :dtcompatible:`st,stm32c5-rcc` (:github:`105577`)
   * :dtcompatible:`st,stm32c5-xsik-clock` (:github:`105577`)
   * :dtcompatible:`st,stm32fx-pll-clock` (:github:`100757`)
   * :dtcompatible:`syna,sr100-clock` (:github:`100172`)
   * :dtcompatible:`ti,k2g-sci-clk` (:github:`90216`)

* 比较器

   * :dtcompatible:`microchip,ac-g1-comparator` (:github:`99155`)
   * :dtcompatible:`nxp,acomp` (:github:`100818`)
   * :dtcompatible:`nxp,hscmp` (:github:`100629`)
   * :dtcompatible:`nxp,lpcmp` (:github:`100998`)

* 计数器

   * :dtcompatible:`bflb,rtc` (:github:`104739`)
   * :dtcompatible:`bflb,timer` (:github:`104739`)
   * :dtcompatible:`bflb,timer-channel` (:github:`104739`)
   * :dtcompatible:`microchip,rtc-g1-counter` (:github:`102163`)
   * :dtcompatible:`microchip,sam-pit64b-counter` (:github:`93806`)
   * :dtcompatible:`microchip,tc-g1` (:github:`100070`)
   * :dtcompatible:`microchip,tc-g1-counter` (:github:`101941`)
   * :dtcompatible:`microchip,tc-g2-counter` (:github:`93401`)
   * :dtcompatible:`microchip,tcc-g1-counter` (:github:`100745`)
   * :dtcompatible:`microcrystal,rv3032-counter` (:github:`98918`)
   * :dtcompatible:`nuvoton,npck-lct` (:github:`98548`)
   * :dtcompatible:`nuvoton,npcx-lct-base` (:github:`98548`)
   * :dtcompatible:`nuvoton,npcx-lct-v1` (:github:`98548`)
   * :dtcompatible:`nuvoton,npcx-lct-v2` (:github:`98548`)
   * :dtcompatible:`nxp,imx-gpt` (:github:`101040`)
   * :dtcompatible:`raspberrypi,pico-pit` (:github:`85618`)
   * :dtcompatible:`raspberrypi,pico-pit-channel` (:github:`105006`)
   * :dtcompatible:`realtek,bee-counter-timer` (:github:`104805`)
   * :dtcompatible:`renesas,rza2m-ostm-counter` (:github:`100934`)
   * :dtcompatible:`silabs,burtc-counter` (:github:`102272`)
   * :dtcompatible:`silabs,protimer` (:github:`103428`)
   * :dtcompatible:`silabs,timer-counter` (:github:`103885`)

* CPU

   * :dtcompatible:`adi,max32-rv32` (:github:`97309`)
   * :dtcompatible:`arm,cortex-a320` (:github:`96852`)
   * :dtcompatible:`arm,cortex-a510` (:github:`96852`)
   * :dtcompatible:`arm,cortex-a7` (:github:`101582`)
   * :dtcompatible:`arm,cortex-a9` (:github:`101582`)
   * :dtcompatible:`cdns,swerv,s400` (:github:`102288`)
   * :dtcompatible:`cdns,swerv,s420` (:github:`102288`)
   * :dtcompatible:`intel,wildcat-lake` (:github:`99205`)
   * :dtcompatible:`riscv` (:github:`105006`)
   * :dtcompatible:`spinalhdl,vexriscv` (:github:`97925`)

* :abbr:`CRC (Cyclic Redundancy Check)`

   * :dtcompatible:`nxp,crc` (:github:`100875`)
   * :dtcompatible:`nxp,lpc-crc` (:github:`101528`)
   * :dtcompatible:`sifli,sf32lb-crc` (:github:`98997`)
   * :dtcompatible:`silabs,gpcrc` (:github:`104471`)
   * :dtcompatible:`st,stm32-crc` (:github:`105302`)

* 加密加速器

   * :dtcompatible:`bflb,sec-eng-aes` (:github:`104371`)
   * :dtcompatible:`bflb,sec-eng-sha` (:github:`104371`)
   * :dtcompatible:`bflb,sec-eng-trng` (:github:`104349`)
   * :dtcompatible:`microchip,aes-g1` (:github:`105389`)
   * :dtcompatible:`microchip,sha-g1-crypto` (:github:`98894`)
   * :dtcompatible:`nxp,s32-crypto-hse-mu` (:github:`79351`)
   * :dtcompatible:`raspberrypi,pico-sha256` (:github:`85036`)
   * :dtcompatible:`sifli,sf32lb-crypto` (:github:`100583`)

* :abbr:`DAC (Digital to Analog Converter)`

   * :dtcompatible:`microchip,dac-g1` (:github:`101431`)
   * :dtcompatible:`nxp,hpdac` (:github:`104642`)
   * :dtcompatible:`ti,dac5311` (:github:`90811`)
   * :dtcompatible:`ti,dac6311` (:github:`90811`)
   * :dtcompatible:`ti,dac7311` (:github:`90811`)
   * :dtcompatible:`ti,dac8311` (:github:`90811`)
   * :dtcompatible:`ti,dac8411` (:github:`90811`)
   * :dtcompatible:`zephyr,dac-emul` (:github:`100306`)

* 磁盘

   * :dtcompatible:`zephyr,ftl-dhara` (:github:`100858`)

* 显示

   * :dtcompatible:`eink,ac057tc1` (:github:`104142`)
   * :dtcompatible:`ilitek,ili9163c` (:github:`104071`)
   * :dtcompatible:`nxp,imx-lcdifv2` (:github:`103646`)
   * :dtcompatible:`qemu,ramfb` (:github:`103887`)
   * :dtcompatible:`sifli,sf32lb-lcdc` (:github:`99549`)
   * :dtcompatible:`sitronix,st7586s` (:github:`103296`)
   * :dtcompatible:`solomon,ssd1325` (:github:`102128`)
   * :dtcompatible:`waveshare,dsi2dpi` (:github:`100140`)

* :abbr:`DMA (Direct Memory Access)`

   * :dtcompatible:`infineon,dmac` (:github:`101583`)
   * :dtcompatible:`microchip,dmac-g1-dma` (:github:`96300`)
   * :dtcompatible:`microchip,dmac-g2-dma` (:github:`104404`)
   * :dtcompatible:`nxp,4ch-dma` (:github:`97841`)

* :abbr:`EDAC (Error Detection and Correction)`

   * :dtcompatible:`nxp,eim` (:github:`94111`)
   * :dtcompatible:`nxp,erm` (:github:`94111`)

* 以太网

   * :dtcompatible:`davicom,dm9051` (:github:`104715`)
   * :dtcompatible:`ethernet-phy-fixed-link` (:github:`100454`)
   * :dtcompatible:`maxlinear,gpy111` (:github:`100995`)
   * :dtcompatible:`microchip,lan8742` (:github:`96134`)
   * :dtcompatible:`motorcomm,yt8521` (:github:`97535`)
   * :dtcompatible:`motorcomm,yt8531` (:github:`104945`)
   * :dtcompatible:`nxp,t1s-phy` (:github:`105033`)
   * :dtcompatible:`renesas,ra-eswm` (:github:`100995`)
   * :dtcompatible:`renesas,ra-ethernet-rmac` (:github:`100995`)
   * :dtcompatible:`renesas,ra-mdio-rmac` (:github:`100995`)
   * :dtcompatible:`st,stm32h5-ethernet` (:github:`100910`)
   * :dtcompatible:`st,stm32mp13-ethernet` (:github:`96134`)
   * :dtcompatible:`wch,ethernet` (:github:`101390`)
   * :dtcompatible:`wch,ethernet-controller` (:github:`101390`)
   * :dtcompatible:`wch,mdio` (:github:`101390`)
   * :dtcompatible:`wiznet,w6100` (:github:`101753`)
   * :dtcompatible:`xlnx,xps-ethernetlite-1.00.a` (:github:`95073`)
   * :dtcompatible:`xlnx,xps-ethernetlite-1.00.a-mac` (:github:`95073`)
   * :dtcompatible:`xlnx,xps-ethernetlite-1.00.a-mdio` (:github:`103944`)
   * :dtcompatible:`xlnx,xps-ethernetlite-3.00.a` (:github:`95073`)
   * :dtcompatible:`xlnx,xps-ethernetlite-3.00.a-mac` (:github:`95073`)
   * :dtcompatible:`xlnx,xps-ethernetlite-3.00.a-mdio` (:github:`103944`)

* 固件

   * :dtcompatible:`arm,scmi-smc` (:github:`103584`)
   * :dtcompatible:`arm,scmi-system` (:github:`99037`)
   * :dtcompatible:`qemu,fw-cfg-ioport` (:github:`103717`)
   * :dtcompatible:`qemu,fw-cfg-mmio` (:github:`103717`)

* Flash 控制器

   * :dtcompatible:`nxp,c40-flash-controller` (:github:`97401`)
   * :dtcompatible:`renesas,rza2m-qspi-spibsc` (:github:`102175`)
   * :dtcompatible:`st,stm32c5-flash-controller` (:github:`105577`)

* 电量计

   * :dtcompatible:`hycon,hy4245` (:github:`105006`)

* :abbr:`GNSS (Global Navigation Satellite System)`

   * :dtcompatible:`globaltop,pa6h` (:github:`104789`)

* :abbr:`GPIO (General Purpose Input/Output)`

   * :dtcompatible:`elan,em32-gpio` (:github:`97843`)
   * :dtcompatible:`espressif,esp-threadbr-header` (:github:`99704`)
   * :dtcompatible:`infineon,cyw43-gpio` (:github:`104728`)
   * :dtcompatible:`infineon,shared-gpio` (:github:`105081`)
   * :dtcompatible:`microchip,xpro-header` (:github:`98043`)
   * :dtcompatible:`nordic,expansion-board-header` (:github:`104138`)
   * :dtcompatible:`nxp,sc18is606-gpio` (:github:`100743`)
   * :dtcompatible:`realtek,ameba-gpio` (:github:`78036`)
   * :dtcompatible:`realtek,bee-gpio` (:github:`102691`)
   * :dtcompatible:`renesas,rz-gpio-common` (:github:`101256`)
   * :dtcompatible:`renesas,rz-gpio-common-v2` (:github:`101256`)
   * :dtcompatible:`renesas,rz-gpio-common-v3` (:github:`104804`)
   * :dtcompatible:`solderedelectronics,easyc-connector` (:github:`104919`)

* 触觉反馈

   * :dtcompatible:`cirrus,cs40l5x` (:github:`100042`)

* 硬件信息

   * :dtcompatible:`microchip,hwinfo-g1` (:github:`100147`)
   * :dtcompatible:`nxp,rcm-hwinfo` (:github:`102490`)
   * :dtcompatible:`nxp,sim-uuid` (:github:`102490`)

* 硬件自旋锁

   * :dtcompatible:`nxp,sema42` (:github:`101499`)

* :abbr:`I2C (Inter-Integrated Circuit)`

   * :dtcompatible:`bflb,i2c` (:github:`98364`)
   * :dtcompatible:`microchip,sercom-g1-i2c` (:github:`98385`)
   * :dtcompatible:`renesas,rza2m-riic` (:github:`100513`)
   * :dtcompatible:`sifli,sf32lb-i2c` (:github:`96316`)

* :abbr:`I2S (Inter-IC Sound)`

   * :dtcompatible:`adi,max32-i2s` (:github:`91508`)
   * :dtcompatible:`infineon,i2s` (:github:`100606`)

* 输入

   * :dtcompatible:`adafruit,seesaw-gamepad` (:github:`105508`)
   * :dtcompatible:`bflb,irx` (:github:`100600`)
   * :dtcompatible:`chipsemi,chsc6540` (:github:`104710`)
   * :dtcompatible:`focaltech,ft6146` (:github:`96330`)
   * :dtcompatible:`hynitron,cst8xx` (:github:`105348`)
   * :dtcompatible:`nxp,tsi-input` (:github:`103116`)
   * :dtcompatible:`parade,tma525b` (:github:`101254`)
   * :dtcompatible:`realtek,bee-keyscan` (:github:`105110`)
   * :dtcompatible:`wch,ch9350l` (:github:`101976`)

* 中断控制器

   * :dtcompatible:`adi,max32-rv32-intc` (:github:`97309`)
   * :dtcompatible:`cdns,swerv-pic` (:github:`102288`)
   * :dtcompatible:`microchip,aic-g1-intc` (:github:`101016`)
   * :dtcompatible:`microchip,eic-g1-intc` (:github:`100928`)
   * :dtcompatible:`nxp,gint` (:github:`100240`)
   * :dtcompatible:`opencores,or1k-pic-level` (:github:`98160`)
   * :dtcompatible:`renesas,rx-grp-intc` (:github:`96451`)
   * :dtcompatible:`renesas,rz-icu-v2` (:github:`104804`)
   * :dtcompatible:`renesas,rz-intc-v2` (:github:`101256`)
   * :dtcompatible:`renesas,rz-tint` (:github:`101256`)
   * :dtcompatible:`riscv,aplic` (:github:`104730`)
   * :dtcompatible:`riscv,imsic` (:github:`102055`)

* :abbr:`LED (Light Emitting Diode)`

   * :dtcompatible:`issi,is31fl3197` (:github:`96821`)
   * :dtcompatible:`sct,sct2024` (:github:`98698`)

* LoRa

   * :dtcompatible:`semtech,llcc68` (:github:`100705`)
   * :dtcompatible:`semtech,sx1268` (:github:`100705`)
   * :dtcompatible:`semtech,sx1278` (:github:`100705`)

* 邮箱

   * :dtcompatible:`adi,mbox-max32-sema` (:github:`104547`)
   * :dtcompatible:`raspberrypi,pico-mbox` (:github:`94502`)
   * :dtcompatible:`xlnx,mbox-versal-ipi-mailbox` (:github:`92768`)

* :abbr:`MCTP (Management Component Transport Protocol)`

   * :dtcompatible:`zephyr,mctp-i3c-controller` (:github:`105006`)
   * :dtcompatible:`zephyr,mctp-i3c-endpoint` (:github:`105006`)
   * :dtcompatible:`zephyr,mctp-i3c-target` (:github:`105006`)

* 内存控制器

   * :dtcompatible:`adi,max32-backup-sram` (:github:`104528`)

* :abbr:`MFD (Multi-Function Device)`

   * :dtcompatible:`adi,max2221x` (:github:`97584`)
   * :dtcompatible:`microcrystal,rv3032-mfd` (:github:`98918`)
   * :dtcompatible:`nordic,npm10xx` (:github:`105447`)

* :abbr:`MIPI DBI (Mobile Industry Processor Interface Display Bus Interface)`

   * :dtcompatible:`bflb,dbi` (:github:`98752`)
   * :dtcompatible:`espressif,esp32-lcd-cam-mipi-dbi` (:github:`99863`)
   * :dtcompatible:`raspberrypi,pico-mipi-dbi-pio` (:github:`91350`)
   * :dtcompatible:`sifli,sf32lb-lcdc-mipi-dbi` (:github:`99549`)

* 其他

   * :dtcompatible:`adi,max2221x-misc` (:github:`97584`)
   * :dtcompatible:`espressif,esp32-lcd-cam` (:github:`99863`)
   * :dtcompatible:`nordic,axon` (:github:`102160`)
   * :dtcompatible:`raspberrypi,pico-sio` (:github:`94502`)
   * :dtcompatible:`renesas,ra-drw` (:github:`97163`)
   * :dtcompatible:`renesas,ra-sau` (:github:`102379`)
   * :dtcompatible:`renesas,ra-sau-channel` (:github:`102379`)
   * :dtcompatible:`skyworks,sky13348` (:github:`102321`)
   * :dtcompatible:`st,stm32-npu-cache` (:github:`102232`)

* 调制解调器

   * :dtcompatible:`st,st87mxx` (:github:`100366`)

* 多比特 SPI

   * :dtcompatible:`st,stm32-ospi-controller` (:github:`96670`)
   * :dtcompatible:`st,stm32-qspi-controller` (:github:`96670`)
   * :dtcompatible:`st,stm32-xspi-controller` (:github:`96670`)

* :abbr:`MTD (Memory Technology Device)`

   * :dtcompatible:`jedec,spi-nand` (:github:`100845`)
   * :dtcompatible:`mxicy,mx25u` (:github:`104357`)
   * :dtcompatible:`netsol,s3axx04` (:github:`97867`)
   * :dtcompatible:`nxp,c40-flash` (:github:`97401`)
   * :dtcompatible:`nxp,imx-flexspi-is66wvs8m8` (:github:`100976`)
   * :dtcompatible:`nxp,s32-xspi-device` (:github:`101487`)
   * :dtcompatible:`nxp,s32-xspi-hyperram` (:github:`101487`)
   * :dtcompatible:`zephyr,mapped-partition` (:github:`104398`)

* :abbr:`OPAMP (Operational Amplifier)`

   * :dtcompatible:`st,stm32-opamp` (:github:`99181`)
   * :dtcompatible:`st,stm32g4-opamp` (:github:`99181`)

* :abbr:`OTP (One Time Programmable)` Memory

   * :dtcompatible:`nxp,ocotp` (:github:`103089`)
   * :dtcompatible:`sifli,sf32lb-efuse` (:github:`101926`)
   * :dtcompatible:`st,stm32-bsec` (:github:`102403`)
   * :dtcompatible:`st,stm32-nvm-otp` (:github:`102976`)
   * :dtcompatible:`zephyr,otp-emul` (:github:`101292`)

* :abbr:`P-state (Performance State)`

   * :dtcompatible:`nxp,mcxn-pstate` (:github:`105006`)

* 引脚控制

   * :dtcompatible:`alif,pinctrl` (:github:`101244`)
   * :dtcompatible:`brcm,bcm2711-pinctrl` (:github:`101008`)
   * :dtcompatible:`nxp,s32k5-pinctrl` (:github:`100803`)
   * :dtcompatible:`realtek,ameba-pinctrl` (:github:`78036`)
   * :dtcompatible:`realtek,bee-pinctrl` (:github:`102691`)
   * :dtcompatible:`realtek,rts5817-pinctrl` (:github:`91486`)
   * :dtcompatible:`renesas,ra0-pinctrl-pfs` (:github:`102379`)
   * :dtcompatible:`st,stm32h5-pinctrl` (:github:`105856`)
   * :dtcompatible:`syna,sr100-pinctrl` (:github:`100172`)

* 电源管理 CPU 操作

   * :dtcompatible:`arm,fvp-pwrc` (:github:`96852`)

* 电源管理

   * :dtcompatible:`bflb,power-controller` (:github:`102063`)
   * :dtcompatible:`st,stm32-dualreg-pwr` (:github:`99171`)
   * :dtcompatible:`st,stm32-iocell` (:github:`100539`)
   * :dtcompatible:`st,stm32h5-iocell` (:github:`104599`)
   * :dtcompatible:`st,stm32h7-pwr` (:github:`99171`)
   * :dtcompatible:`st,stm32h7rs-pwr` (:github:`99171`)
   * :dtcompatible:`st,stm32u5-pwr` (:github:`100319`)
   * :dtcompatible:`st,stm32wba-pwr` (:github:`105279`)

* 电源域

   * :dtcompatible:`arm,scmi-power-domain` (:github:`102370`)

* :abbr:`PS/2 (Personal System/2)`

   * :dtcompatible:`ite,it51xxx-ps2` (:github:`102790`)

* :abbr:`PWM (Pulse Width Modulation)`

   * :dtcompatible:`adi,max2221x-pwm` (:github:`97584`)
   * :dtcompatible:`bflb,pwm-1` (:github:`99195`)
   * :dtcompatible:`bflb,pwm-2` (:github:`99195`)
   * :dtcompatible:`elan,em32-pwm` (:github:`97843`)
   * :dtcompatible:`microchip,tc-g1-pwm` (:github:`100070`)
   * :dtcompatible:`renesas,rza2m-gpt-pwm` (:github:`100932`)
   * :dtcompatible:`sifli,sf32lb-atim-pwm` (:github:`100137`)
   * :dtcompatible:`sifli,sf32lb-gpt-pwm` (:github:`99362`)

* 稳压器

   * :dtcompatible:`arduino,modulino-latch-relay` (:github:`104466`)
   * :dtcompatible:`bflb,aon-regulator` (:github:`102063`)
   * :dtcompatible:`bflb,rt-regulator` (:github:`102063`)
   * :dtcompatible:`bflb,soc-regulator` (:github:`102063`)
   * :dtcompatible:`espressif,esp32-regulator` (:github:`105076`)
   * :dtcompatible:`nordic,npm10xx-regulator` (:github:`105562`)
   * :dtcompatible:`nordic,vregusb-regulator` (:github:`97642`)
   * :dtcompatible:`st,stm32-vrefbuf` (:github:`99304`)
   * :dtcompatible:`ti,tps55287` (:github:`98662`)

* 复位控制器

   * :dtcompatible:`focaltech,ft9001-cpm-rctl` (:github:`95959`)
   * :dtcompatible:`realtek,rts5817-reset` (:github:`91486`)
   * :dtcompatible:`syna,sr100-reset` (:github:`100172`)

* :abbr:`RNG (Random Number Generator)`

   * :dtcompatible:`gd,gd32-trng` (:github:`101559`)
   * :dtcompatible:`microchip,trng-g1-entropy` (:github:`99183`)
   * :dtcompatible:`raspberrypi,pico-rng` (:github:`83346`)
   * :dtcompatible:`renesas,ra-rsip-e50d-trng` (:github:`100995`)
   * :dtcompatible:`sifli,sf32lb-trng` (:github:`98467`)
   * :dtcompatible:`ti,mspm0-trng` (:github:`94733`)
   * :dtcompatible:`wch,rng` (:github:`101390`)

* :abbr:`RTC (Real Time Clock)`

   * :dtcompatible:`adi,max31331` (:github:`100508`)
   * :dtcompatible:`maxim,ds1302` (:github:`103964`)
   * :dtcompatible:`microchip,rtc-g1` (:github:`99144`)
   * :dtcompatible:`microchip,rtc-g2` (:github:`99889`)
   * :dtcompatible:`nxp,rtc-jdp` (:github:`98114`)

* :abbr:`SDHC (Secure Digital Host Controller)`

   * :dtcompatible:`infineon,sdhc-sdio` (:github:`100644`)
   * :dtcompatible:`litex,mmc` (:github:`93816`)

* 传感器

   * :dtcompatible:`adi,ade7978` (:github:`104030`)
   * :dtcompatible:`adi,adt7410` (:github:`105009`)
   * :dtcompatible:`adi,adt7422` (:github:`105009`)
   * :dtcompatible:`adi,adxl355` (:github:`103387`)
   * :dtcompatible:`adi,max30210` (:github:`100511`)
   * :dtcompatible:`ams,as5048` (:github:`100382`)
   * :dtcompatible:`ams,as6221` (:github:`94899`)
   * :dtcompatible:`avia,hx711-spi` (:github:`104416`)
   * :dtcompatible:`iclegend,s3km1110` (:github:`104279`)
   * :dtcompatible:`invensense,icm45605` (:github:`101061`)
   * :dtcompatible:`invensense,icm45605s` (:github:`101061`)
   * :dtcompatible:`invensense,icm45686s` (:github:`101061`)
   * :dtcompatible:`invensense,icm45688p` (:github:`101061`)
   * :dtcompatible:`liteon,ltr553` (:github:`101669`)
   * :dtcompatible:`microcrystal,rv3032-temp` (:github:`98918`)
   * :dtcompatible:`nordic,npm10xx-adc` (:github:`105597`)
   * :dtcompatible:`nuvoton,npcx-adc-v2t` (:github:`105006`)
   * :dtcompatible:`nxp,mcux-qdc` (:github:`104880`)
   * :dtcompatible:`nxp,tempsense` (:github:`101525`)
   * :dtcompatible:`qst,qmi8658a` (:github:`104345`)
   * :dtcompatible:`sensirion,stcc4` (:github:`104929`)
   * :dtcompatible:`sifli,sf32lb-tsen` (:github:`99463`)
   * :dtcompatible:`st,ism6hg256x` (:github:`95802`)
   * :dtcompatible:`st,lsm6dsv320x` (:github:`95802`)
   * :dtcompatible:`st,lsm6dsv80x` (:github:`95802`)
   * :dtcompatible:`ti,ina232` (:github:`98791`)
   * :dtcompatible:`ti,opt3004` (:github:`99387`)

* 串行控制器

   * :dtcompatible:`focaltech,ft9001-usart` (:github:`95959`)
   * :dtcompatible:`microchip,dbgu-g1-uart` (:github:`101016`)
   * :dtcompatible:`realtek,ameba-loguart` (:github:`78036`)
   * :dtcompatible:`realtek,bee-uart` (:github:`102691`)
   * :dtcompatible:`renesas,ra-uart-sau` (:github:`102379`)
   * :dtcompatible:`rpmsg-uart` (:github:`98463`)

* :abbr:`SPI (Serial Peripheral Interface)`

   * :dtcompatible:`bflb,spi` (:github:`94752`)
   * :dtcompatible:`infineon,spi` (:github:`100644`)
   * :dtcompatible:`microchip,sercom-g1-spi` (:github:`101864`)
   * :dtcompatible:`realtek,rts5912-spi` (:github:`96006`)
   * :dtcompatible:`renesas,ra-spi-sci` (:github:`97339`)
   * :dtcompatible:`renesas,ra-spi-sci-b` (:github:`95014`)
   * :dtcompatible:`sensry,sy1xx-spi` (:github:`102323`)
   * :dtcompatible:`sifli,sf32lb-spi` (:github:`97626`)

* 步进电机

   * :dtcompatible:`adi,tmc50xx-stepper-ctrl` (:github:`101001`)
   * :dtcompatible:`adi,tmc50xx-stepper-driver` (:github:`101001`)
   * :dtcompatible:`adi,tmc51xx-stepper-ctrl` (:github:`101001`)
   * :dtcompatible:`adi,tmc51xx-stepper-driver` (:github:`101001`)
   * :dtcompatible:`adi,tmcm3216` (:github:`104508`)
   * :dtcompatible:`adi,tmcm3216-stepper-ctrl` (:github:`104508`)
   * :dtcompatible:`adi,tmcm3216-stepper-driver` (:github:`104508`)
   * :dtcompatible:`zephyr,fake-stepper-ctrl` (:github:`101001`)
   * :dtcompatible:`zephyr,fake-stepper-driver` (:github:`101001`)
   * :dtcompatible:`zephyr,gpio-step-dir-stepper-ctrl` (:github:`101001`)
   * :dtcompatible:`zephyr,h-bridge-stepper-ctrl` (:github:`101001`)

* 系统控制器

   * :dtcompatible:`ti,control-module` (:github:`103330`)

* 定时器

   * :dtcompatible:`adi,max32-rv32-sys-timer` (:github:`97309`)
   * :dtcompatible:`adi,max32-wut-timer` (:github:`104687`)
   * :dtcompatible:`arm,armv7-timer` (:github:`99675`)
   * :dtcompatible:`infineon,cat1-lp-timer-pdl` (:github:`97831`)
   * :dtcompatible:`infineon,lp-timer` (:github:`100644`)
   * :dtcompatible:`realtek,bee-basic-timer` (:github:`104805`)
   * :dtcompatible:`realtek,bee-enhanced-timer` (:github:`104805`)
   * :dtcompatible:`realtek,bee-timer` (:github:`104805`)
   * :dtcompatible:`renesas,rza2m-gpt` (:github:`100932`)
   * :dtcompatible:`renesas,rza2m-ostm-timer` (:github:`100934`)
   * :dtcompatible:`sifli,sf32lb-atim` (:github:`100137`)
   * :dtcompatible:`sifli,sf32lb-gptim` (:github:`99362`)

* :abbr:`UAOL (USB Audio Offload Link)`

   * :dtcompatible:`intel,adsp-uaol` (:github:`104137`)
   * :dtcompatible:`intel,uaol-dai` (:github:`104137`)

* USB

   * :dtcompatible:`atmel,sam-udp` (:github:`102041`)
   * :dtcompatible:`bflb,udc-1` (:github:`104244`)
   * :dtcompatible:`nordic,nrf-usbhs-wrapper` (:github:`97642`)
   * :dtcompatible:`nuvoton,numaker-hsusbd` (:github:`95709`)

* USB Type-C

   * :dtcompatible:`zephyr,usb-c-pwrctrl` (:github:`103883`)

* 视频

   * :dtcompatible:`arducam,mega` (:github:`96234`)
   * :dtcompatible:`himax,hm0360` (:github:`94904`)
   * :dtcompatible:`ovti,ov5642` (:github:`97106`)
   * :dtcompatible:`ovti,ov7675` (:github:`96319`)
   * :dtcompatible:`sony,imx219` (:github:`101754`)

* 唤醒控制器

   * :dtcompatible:`nxp,llwu` (:github:`100559`)

* 看门狗

   * :dtcompatible:`adi,max42500-watchdog` (:github:`102929`)
   * :dtcompatible:`bflb,wdt` (:github:`104243`)
   * :dtcompatible:`microchip,wdt-g1` (:github:`101335`)
   * :dtcompatible:`realtek,rts5817-watchdog` (:github:`91486`)

* Wi-Fi

   * :dtcompatible:`nordic,nrf7120-wifi` (:github:`104055`)

* :abbr:`XSPI (Expanded Serial Peripheral Interface)`

   * :dtcompatible:`nxp,s32-xspi` (:github:`101487`)
   * :dtcompatible:`nxp,s32-xspi-sfp-frad` (:github:`101487`)
   * :dtcompatible:`nxp,s32-xspi-sfp-mdad` (:github:`101487`)
   * :dtcompatible:`st,stm32-xspim` (:github:`104943`)

新增示例
********

* :zephyr:code-sample:`6dof_fifo_stream`，由 ``stream_fifo`` 重命名而来
* :zephyr:code-sample:`accel_stream`，由 ``accel_polling`` 重命名而来
* :zephyr:code-sample:`adc_stream`
* :zephyr:code-sample:`amp_talk`
* :zephyr:code-sample:`at_client`
* :zephyr:code-sample:`bflb-bl61x-wo-uart`
* :zephyr:code-sample:`ble_peripheral_ans`
* :zephyr:code-sample:`ble_peripheral_ets`
* :zephyr:code-sample:`ble_peripheral_gap_svc`
* :zephyr:code-sample:`bluetooth_a2dp_sink`
* :zephyr:code-sample:`bluetooth_a2dp_source`
* :zephyr:code-sample:`bluetooth_l2cap_coc_acceptor`
* :zephyr:code-sample:`bluetooth_l2cap_coc_initiator`
* :zephyr:code-sample:`bridge`
* :zephyr:code-sample:`button_interrupt`
* :zephyr:code-sample:`capture`
* :zephyr:code-sample:`coap-upload`
* :zephyr:code-sample:`codec`
* :zephyr:code-sample:`cpu_freq_on_demand`
* :zephyr:code-sample:`cpu_freq_pressure`
* :zephyr:code-sample:`crc_drivers`
* :zephyr:code-sample:`crc_subsys`
* :zephyr:code-sample:`cs40l5x`
* :zephyr:code-sample:`device_pm`
* :zephyr:code-sample:`dsa`
* :zephyr:code-sample:`event`
* :zephyr:code-sample:`ext2-fstab`
* :zephyr:code-sample:`fingerprint-sensor`
* :zephyr:code-sample:`flash-ipm`
* :zephyr:code-sample:`frdm_mcxa156_lpdac_opamp_lpadc`
* :zephyr:code-sample:`ftp-client`
* :zephyr:code-sample:`hello_hl78xx`
* :zephyr:code-sample:`hwspinlock`
* :zephyr:code-sample:`instrumentation`
* :zephyr:code-sample:`is31fl319x`
* :zephyr:code-sample:`latmon-client`
* :zephyr:code-sample:`lp-gpio-wakeup`
* :zephyr:code-sample:`lp-timer-wakeup`
* :zephyr:code-sample:`max32664c`
* :zephyr:code-sample:`mctp_i2c_bus_endpoint`
* PMCI MCTP over I2C+GPIO (``mctp_i2c_bus_owner``)
* :zephyr:code-sample:`mctp_i3c_bus_endpoint`
* PMCI MCTP over I3C (``mctp_i3c_bus_owner``)
* :zephyr:code-sample:`mctp-usb-endpoint`
* :zephyr:code-sample:`msg_queue`
* :zephyr:code-sample:`mtch9010`
* :zephyr:code-sample:`netmidi2`
* :zephyr:code-sample:`nrf_clock_control`
* :zephyr:code-sample:`ocpp`
* :zephyr:code-sample:`opamp_output_measure`
* :zephyr:code-sample:`openthread-border-router`
* :zephyr:code-sample:`pico-w-wifi-led`
* :zephyr:code-sample:`producer_consumer`
* :zephyr:code-sample:`quality-of-service`
* :zephyr:code-sample:`red-black-tree`
* :zephyr:code-sample:`regulator_shell`
* :zephyr:code-sample:`renesas_lvd`
* :zephyr:code-sample:`rtk0eg0019b01002bj`
* :zephyr:code-sample:`s3km1110`
* :zephyr:code-sample:`scmi`
* :zephyr:code-sample:`sct2024`
* :zephyr:code-sample:`shell-devmem-load`
* :zephyr:code-sample:`stm32_pwm_mastermode`
* :zephyr:code-sample:`t1s`
* :zephyr:code-sample:`tmcm3216`
* :zephyr:code-sample:`usb-c-drp`
* :zephyr:code-sample:`usb-host-uvc`
* :zephyr:code-sample:`veml6046`
* :zephyr:code-sample:`virtiofs`
* :zephyr:code-sample:`wireguard-vpn`
* :zephyr:code-sample:`zbus-async-listeners`
* :zephyr:code-sample:`zbus-proxy-agent-ipc`
* :zephyr:code-sample:`ztest_benchmark`

..
  Same as above, this will also be recomputed at the time of the release.
 Just link the sample, further details go in the sample documentation itself.

设备树
******

* 迁移指南：:ref:`migration_4.4_devicetree`

* 新增用于 reg 属性遍历的宏 (:github:`104223`)

  * :c:macro:`DT_FOREACH_REG`
  * :c:macro:`DT_FOREACH_REG_SEP`
  * :c:macro:`DT_FOREACH_REG_VARGS`
  * :c:macro:`DT_FOREACH_REG_SEP_VARGS`
  * 每个宏还提供基于实例编号的变体，例如 :c:macro:`DT_INST_FOREACH_REG`

* ``*-map`` 相关属性的定义 (:github:`87595`) 为 nexus 节点和 specifier 映射提供了一等支持。有关这些属性的更多细节，请参阅 Devicetree Specification v0.4 第 2.5 节。

* 新增 :dtcompatible:`zephyr,mapped-partition` 绑定及用于内存映射 flash 分区的相关 API。它是现有 :dtcompatible:`fixed-partitions` 绑定的后继者

* 绑定不再允许为 ``status``、``#address-cells`` 和 ``#size-cells`` 属性指定任何默认值。

* :c:macro:`DT_CHILD_BY_UNIT_ADDR_INT`

* :c:macro:`DT_INST_CHILD_BY_UNIT_ADDR_INT`

Kconfig
*******

* 新增预处理函数 ``dt_highest_controller_irq_number`` (:github:`104819`)

Kernel
******

* 移除了在 Zephyr 4.2.0 中已弃用的 CONFIG_SCHED_DUMB 和 CONFIG_WAITQ_DUMB 选项

* 新增分层堆加固机制，可通过 :kconfig:option:`CONFIG_SYS_HEAP_HARDENING` 选项（Basic、Moderate、Full、Extreme）启用，为 :c:func:`sys_heap_alloc` 和 :c:func:`sys_heap_free` 提供逐级增强的运行时损坏检测，包括双重释放检测、相邻块一致性检查以及可选的逐块 canary（:github:`104999`）。

* :ref:`cleanup_api`

  * :c:macro:`SCOPE_VAR_DEFINE`
  * :c:macro:`SCOPE_GUARD_DEFINE`
  * :c:macro:`SCOPE_DEFER_DEFINE`
  * :c:macro:`scope_var`
  * :c:macro:`scope_var_init`
  * :c:macro:`scope_guard`
  * :c:macro:`scope_defer`

库 / 子系统
***********

* LoRa/LoRaWAN

   * :c:func:`lora_airtime`
   * 为 LoRa API 新增信道活动检测 (CAD) 支持：:c:func:`lora_cad`、:c:func:`lora_cad_async`。CAD 参数和 LBT 模式通过 :c:struct:`lora_modem_config` 配置。
   * 新增 :c:func:`lora_recv_duty_cycle`，用于硬件驱动的无线电唤醒（RX 占空比循环）。

* Mbed TLS

  * 新增 :kconfig:option:`CONFIG_MBEDTLS_VERSION_C`，用于简化 Mbed TLS 版本信息的导出。若启用，将可使用 :c:func:`mbedtls_version_get_number()` 函数。

  * Mbed TLS 已升级到 4.1.0 版本。从此以后，本仓库将仅包含 TLS 和 X.509，而加密支持已迁移到 TF-PSA-Crypto。后者引入了新的 west 模块，基于上游 1.1.0 版本。两个项目的版本说明见：

    * https://github.com/Mbed-TLS/mbedtls/releases/tag/mbedtls-4.1.0
    * https://github.com/Mbed-TLS/TF-PSA-Crypto/releases/tag/tf-psa-crypto-1.1.0

* Zbus

   * 新增异步监听器支持。异步监听器在工作队列上下文中执行，而非在发布者的线程中执行，从而无需专用的订阅者线程即可实现非阻塞操作。
   * 新增 :zephyr:code-sample:`zbus-async-listeners`。
   * 新增实验性的代理 agent 通信，支持 IPC 后端，用于跨域转发通道数据。
   * 新增 :zephyr:code-sample:`zbus-proxy-agent-ipc`。
   * 新增 :c:func:`zbus_chan_from_name` 函数。根据名称字符串获取 zbus 通道。
   * 新增 :c:func:`zbus_async_listener_set_work_queue` 函数。为异步监听器设置工作队列。
   * 新增 :c:func:`zbus_chan_pub_stats_msg_age` 函数。获取自上次发布以来消息的存续时长（毫秒）。
   * 澄清了观察者优先级的文档说明，并修正了拼写和语法。
   * 更新了文档中的观察者类型示意图。
   * 过滤掉不支持 SMP 的测试。


其他重要变更
************

* TF-M 已从 2.2.0 升级到 2.2.2 版本。版本说明见：

  * https://trustedfirmware-m.readthedocs.io/en/tf-mv2.2.2/releases/2.2.1.html
  * https://trustedfirmware-m.readthedocs.io/en/tf-mv2.2.2/releases/2.2.2.html

* TF-M 非安全接口头文件现在通过 ``zephyr_interface`` CMake 库自动提供给非安全应用，无需再显式链接 ``tfm_api``。

* NXP SoC DTSI 文件已重新组织，移至 ``dts/arm/nxp`` 下按系列划分的子目录中。

* 基于 :zephyr:board:`native_sim` 的目标现在可以进行 :ref:`交叉编译<posix_arch_cross_compile>` (:github:`100182`)

..
  Any more descriptive subsystem or driver changes. Do you really want to write
  a paragraph or is it enough to link to the api/driver/Kconfig/board page above?
