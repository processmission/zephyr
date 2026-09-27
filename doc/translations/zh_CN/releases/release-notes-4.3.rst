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

.. _zephyr_4.3:

Zephyr 4.3.0
############

我们很高兴地宣布 Zephyr 4.3.0 版本正式发布。

本次发布的主要增强包括：

**USB 设备 “Next” 栈现在是默认选项**
  新的 :ref:`USB 设备栈 <usb_device_stack_next>` 基于现代的 UDC（USB Device Controller）API 构建，取代了旧版协议栈，支持多个控制器同时工作、运行时配置，并具有整体更好的架构。旧版协议栈现已弃用，并将在 Zephyr 4.5 中移除。

**CPU 负载与动态频率调节子系统**
  新的实验性 :ref:`CPU 频率 <cpu_freq>` 调节子系统支持由策略驱动的动态时钟调整，以平衡功耗与性能。与之配套的新 :ref:`cpu_load` 子系统允许用户基于调度器统计信息获取 CPU 使用率指标，可用于驱动频率调节策略。

**插桩子系统**
  新的 :ref:`插桩子系统 <instrumentation>` 利用编译器管理的函数插桩，简化了 Zephyr 应用的跟踪与性能分析，可在运行时记录调用图跟踪和统计性能剖析数据。

**OCPP 1.6 库**
  新的 :ref:`OCPP（Open Charge Point Protocol） <ocpp_interface>` 库支持使用 Zephyr 开发电动汽车充电桩。该库通过 WebSocket 实现 OCPP 1.6 Charge Point 功能，支持核心配置文件操作，包括授权、事务管理以及与 Central System 服务器通信的电表值上报。

**Twister 显示测试装置**
  Twister 现在可以 :ref:`验证目标板上的显示输出 <twister_display_capture_harness>`，方法是采集 USB 摄像头的帧，并与预先录制的视觉“指纹”进行匹配。

**开发者体验改进**
  本次发布引入了多个新工具，帮助完成常见的开发与故障排查任务：

  - :ref:`dtdoctor`，用于帮助诊断设备树构建错误。
  - :ref:`traceconfig <kconfig_traceconfig>` 构建目标，用于帮助了解 Kconfig 符号的来源及其最终取值。
  - :ref:`交互式占用图表 <footprint_tools_plot>`，用于可视化应用的 RAM/ROM 使用情况。

**开发板支持扩展**
  本次发布新增了对 105 个 :ref:`新开发板 <boards_added_in_zephyr_4_3>` 和 39 个 :ref:`新扩展板 <shields_added_in_zephyr_4_3>` 的支持。

将应用从 Zephyr v4.2.0 迁移到 Zephyr v4.3.0 时需要或建议采取的变更概览，见单独的 :ref:`迁移指南 <migration_4.3>`。

以下小节按组件详细列出各项变更。

安全漏洞相关
************
本版本修复了以下 CVE：

* :cve:`2025-9408` `Zephyr 项目缺陷跟踪系统 GHSA-3r6j-5mp3-75wr <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-3r6j-5mp3-75wr>`_
* :cve:`2025-9557`：在 2025-11-24 之前处于禁运期
* :cve:`2025-9558`：在 2025-11-24 之前处于禁运期
* :cve:`2025-12035`：在 2025-12-13 之前处于禁运期
* :cve:`2025-12899`：在 2026-01-28 之前处于禁运期
* :cve:`2025-59438` `通过密码错误报告时序的填充预言机 <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-10-invalid-padding-error/>`_
* :cve:`2025-54764` `RSA 密钥生成和操作中的侧信道（SSBleed、M-Step） <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-10-ssbleed-mstep/>`_

更多详细信息请参阅：https://docs.zephyrproject.org/latest/security/vulnerabilities.html

API 变更
********

..
  Only removed, deprecated and new APIs, changes go in migration guide.

* 加密

  * :c:struct:`hash_pkt` 中的输入缓冲区现在为常量

移除的 API 和选项
=================

* TinyCrypt 库已被移除，因为上游版本不再维护。现在推荐使用 PSA Crypto API 作为 Zephyr 的加密库。
* 旧版管道对象 API 已移除。请改用新的管道 API。
* ``bt_le_set_auto_conn``
* ``CONFIG_BT_BUF_ACL_RX_COUNT``
* ``ok`` 枚举值现已从设备树中 ``base.yaml`` 绑定的 ``status`` 属性中完全移除。
* 通过 Kconfig 选择 STM32 LPTIM 时钟源的方式已被移除。现在必须改用设备树。受影响的 Kconfig 符号： :kconfig:option:`CONFIG_STM32_LPTIM_CLOCK_LSI` / :kconfig:option:`CONFIG_STM32_LPTIM_CLOCK_LSE`

已弃用的 API 和选项
===================

* :dtcompatible:`maxim,ds3231` 已弃用，请改用 :dtcompatible:`maxim,ds3231-rtc`。
* 为 :c:macro:`SPI_CONFIG_DT`、:c:macro:`SPI_CONFIG_DT_INST`、:c:macro:`SPI_DT_SPEC_GET`、:c:macro:`SPI_DT_SPEC_INST_GET` 提供第三个参数的做法已弃用。为 :c:macro:`SPI_CS_CONTROL_INIT` 提供第二个参数的做法已弃用。请改用新的设备树属性 ``spi-cs-setup-delay-ns`` 和 ``spi-cs-hold-delay-ns`` 来指定延迟。

* :c:enum:`bt_hci_bus` 已弃用，因为未使用。应改用 :c:macro:`BT_DT_HCI_BUS_GET`。

* :kconfig:option:`CONFIG_BT_AUTO_PHY_UPDATE` 已弃用，已被替换为按角色区分的选项（中心设备与外围设备），这些选项允许明确指定自动更新时首选哪个 PHY。

* :kconfig:option:`CONFIG_POSIX_READER_WRITER_LOCKS` 已弃用。请改用 :kconfig:option:`CONFIG_POSIX_RW_LOCKS`。

* :kconfig:option:`CONFIG_JWT_SIGN_RSA_LEGACY` 已弃用。请改用基于 PSA Crypto API 的替代方案（即 :kconfig:option:`CONFIG_JWT_SIGN_RSA_PSA`）。

* RISC-V 的 :kconfig:option:`CONFIG_EXTRA_EXCEPTION_INFO` 已弃用。请改用 :kconfig:option:`CONFIG_EXCEPTION_DEBUG`。

新增 API 和选项
===============

..
  Link to new APIs here, in a group if you think it's necessary, no need to get
  fancy just list the link, that should contain the documentation. If you feel
  like you need to add more details, add them in the API documentation code
  instead.

.. zephyr-keep-sorted-start re(^\* \w)

* CPU 频率调节

  * 引入了实验性的动态 CPU 频率调节子系统

    * :kconfig:option:`CONFIG_CPU_FREQ`

* LVGL（Light and Versatile Graphics Library）

  * :kconfig:option:`CONFIG_LV_Z_MEMORY_POOL_ZEPHYR_REGION`
  * :kconfig:option:`CONFIG_LV_Z_MEMORY_POOL_ZEPHYR_REGION_NAME`
  * :kconfig:option:`CONFIG_LV_Z_VDB_ZEPHYR_REGION`
  * :kconfig:option:`CONFIG_LV_Z_VDB_ZEPHYR_REGION_NAME`

* NVMEM

  * 新增了 :ref:`非易失性存储器 (NVMEM) <nvmem>` 子系统

    * :kconfig:option:`CONFIG_NVMEM`
    * :kconfig:option:`CONFIG_NVMEM_EEPROM`
    * :c:struct:`nvmem_cell`
    * :c:func:`nvmem_cell_read`
    * :c:func:`nvmem_cell_write`
    * :c:func:`nvmem_cell_is_ready`
    * :c:macro:`NVMEM_CELL_GET_BY_NAME` - 及其变体
    * :c:macro:`NVMEM_CELL_GET_BY_IDX` - 及其变体

* Newlib

  * :kconfig:option:`CONFIG_NEWLIB_LIBC_USE_POSIX_LIMITS_H`

* Settings

   * :kconfig:option:`CONFIG_SETTINGS_TFM_ITS`

* Shell

   * MQTT 后端

      * :kconfig:option:`CONFIG_SHELL_MQTT_TOPIC_RX_ID`
      * :kconfig:option:`CONFIG_SHELL_MQTT_TOPIC_TX_ID`
      * :kconfig:option:`CONFIG_SHELL_MQTT_CONNECT_TIMEOUT_MS`
      * :kconfig:option:`CONFIG_SHELL_MQTT_WORK_DELAY_MS`
      * :kconfig:option:`CONFIG_SHELL_MQTT_LISTEN_TIMEOUT_MS`

* Sys

  * :c:func:`sys_count_bits`

* USB

  * 视频

    * :c:func:`uvc_add_format`

* 以太网

   * 大多数以太网 PHY 新增了设备树属性 ``default-speeds``，用于在驱动初始化期间配置自动协商所通告的速度。

* 任务看门狗

  * :kconfig:option:`CONFIG_TASK_WDT_DUMMY`

* 内核

  * :kconfig:option:`CONFIG_HW_SHADOW_STACK`
  * :kconfig:option:`CONFIG_HW_SHADOW_STACK_ALLOW_REUSE`
  * :kconfig:option:`CONFIG_HW_SHADOW_STACK_MIN_SIZE`
  * :kconfig:option:`CONFIG_HW_SHADOW_STACK_PERCENTAGE_SIZE`
  * :c:macro:`K_THREAD_HW_SHADOW_STACK_SIZE`
  * :c:macro:`K_KERNEL_HW_SHADOW_STACK_DECLARE`
  * :c:macro:`K_KERNEL_HW_SHADOW_STACK_ARRAY_DECLARE`
  * :c:macro:`K_THREAD_HW_SHADOW_STACK_DEFINE`
  * :c:macro:`K_THREAD_HW_SHADOW_STACK_ARRAY_DEFINE`
  * :c:macro:`K_THREAD_HW_SHADOW_STACK_ATTACH`
  * :c:macro:`k_thread_hw_shadow_stack_attach`

* 加密

  * :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_BUILTIN_KEYS`

* 存储

    * :kconfig:option:`CONFIG_FILE_SYSTEM_SHELL_LS_SIZE`

* 工具链

  * :c:macro:`__deprecated_version`

* 插桩子系统

  * 引入了插桩子系统

    * :kconfig:option:`CONFIG_INSTRUMENTATION`
    * :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_CALLGRAPH`
    * :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_CALLGRAPH_BUFFER_SIZE`
    * :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_CALLGRAPH_BUFFER_OVERWRITE`
    * :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_STATISTICAL`
    * :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_STATISTICAL_MAX_NUM_FUNC`
    * :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_STATISTICAL_MAX_CALL_DEPTH`
    * :kconfig:option:`CONFIG_INSTRUMENTATION_TRIGGER_FUNCTION`
    * :kconfig:option:`CONFIG_INSTRUMENTATION_STOPPER_FUNCTION`
    * :kconfig:option:`CONFIG_INSTRUMENTATION_EXCLUDE_FUNCTION_LIST`
    * :kconfig:option:`CONFIG_INSTRUMENTATION_EXCLUDE_FILE_LIST`
    * :c:struct:`instr_header`
    * :c:struct:`instr_event_context`
    * :c:struct:`instr_record`
    * :c:func:`instr_tracing_supported`
    * :c:func:`instr_profiling_supported`
    * :c:func:`instr_fundamentals_initialized`
    * :c:func:`instr_init`
    * :c:func:`instr_initialized`
    * :c:func:`instr_enabled`
    * :c:func:`instr_enable`
    * :c:func:`instr_disable`
    * :c:func:`instr_turn_on`
    * :c:func:`instr_turn_off`
    * :c:func:`instr_turned_on`
    * :c:func:`instr_trace_enabled`
    * :c:func:`instr_profile_enabled`
    * :c:func:`instr_dump_buffer_uart`
    * :c:func:`instr_dump_deltas_uart`
    * :c:func:`instr_event_handler`
    * :c:func:`instr_set_trigger_func`
    * :c:func:`instr_set_stop_func`
    * :c:func:`instr_get_trigger_func`
    * :c:func:`instr_get_stop_func`

* 日志：

  * :kconfig:option:`CONFIG_LOG_BACKEND_SWO_SYNC_PACKETS`

  * 新增了用于在日志后端中跳过时间戳和级别的选项。

    * :kconfig:option:`CONFIG_LOG_BACKEND_SHOW_TIMESTAMP`
    * :kconfig:option:`CONFIG_LOG_BACKEND_SHOW_LEVEL`

  * 新增了限速日志宏，以防止消息频繁生成时日志泛滥。

    * :c:macro:`LOG_ERR_RATELIMIT` - 限速错误日志宏（便捷版）
    * :c:macro:`LOG_WRN_RATELIMIT` - 限速警告日志宏（便捷版）
    * :c:macro:`LOG_INF_RATELIMIT` - 限速信息日志宏（便捷版）
    * :c:macro:`LOG_DBG_RATELIMIT` - 限速调试日志宏（便捷版）
    * :c:macro:`LOG_HEXDUMP_ERR_RATELIMIT` - 限速错误十六进制转储宏（便捷版）
    * :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT` - 限速警告十六进制转储宏（便捷版）
    * :c:macro:`LOG_HEXDUMP_INF_RATELIMIT` - 限速信息十六进制转储宏（便捷版）
    * :c:macro:`LOG_HEXDUMP_DBG_RATELIMIT` - 限速调试十六进制转储宏（便捷版）
    * :c:macro:`LOG_ERR_RATELIMIT_RATE` - 限速错误日志宏（显式速率）
    * :c:macro:`LOG_WRN_RATELIMIT_RATE` - 限速警告日志宏（显式速率）
    * :c:macro:`LOG_INF_RATELIMIT_RATE` - 限速信息日志宏（显式速率）
    * :c:macro:`LOG_DBG_RATELIMIT_RATE` - 限速调试日志宏（显式速率）
    * :c:macro:`LOG_HEXDUMP_ERR_RATELIMIT_RATE` - 限速错误十六进制转储宏（显式速率）
    * :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT_RATE` - 限速警告十六进制转储宏（显式速率）
    * :c:macro:`LOG_HEXDUMP_INF_RATELIMIT_RATE` - 限速信息十六进制转储宏（显式速率）
    * :c:macro:`LOG_HEXDUMP_DBG_RATELIMIT_RATE` - 限速调试十六进制转储宏（显式速率）

* 显示

  * :c:enumerator:`PIXEL_FORMAT_AL_88`

  * SDL

    * :kconfig:option:`CONFIG_SDL_DISPLAY_DEFAULT_PIXEL_FORMAT_AL_88`
    * :kconfig:option:`CONFIG_SDL_DISPLAY_COLOR_TINT`

* 架构

  * :kconfig:option:`CONFIG_ARCH_HAS_HW_SHADOW_STACK`
  * :kconfig:option:`CONFIG_SRAM_SW_ISR_TABLE`

  * x86 Intel CET 支持

    * :kconfig:option:`CONFIG_X86_CET`
    * :kconfig:option:`CONFIG_X86_CET_IBT`
    * :kconfig:option:`CONFIG_X86_CET_SHADOW_STACK_ALIGNMENT`
    * :kconfig:option:`CONFIG_X86_CET_SOC_PREPARE_SHADOW_STACK_SWITCH`
    * :kconfig:option:`CONFIG_X86_CET_VERIFY_KERNEL_SHADOW_STACK`

  * ARM（Cortex-M）系统状态保存/恢复原语

    * :c:func:`z_arm_save_scb_context` / :c:func:`z_arm_restore_scb_context`
    * :c:func:`z_arm_save_mpu_context` / :c:func:`z_arm_restore_mpu_context`
    * 现有的 :c:func:`z_arm_save_fp_context` 和 :c:func:`z_arm_save_fp_context` 也已更新

  * Xtensa

    * :kconfig:option:`CONFIG_XTENSA_HIFI_SHARING_MODEL`
    * :kconfig:option:`CONFIG_XTENSA_EAGER_HIFI_SHARING`
    * :kconfig:option:`CONFIG_XTENSA_LAZY_HIFI_SHARING`
    * :kconfig:option:`CONFIG_XTENSA_EXCEPTION_ENTER_GDB`

* 状态机框架

  * :c:func:`smf_get_current_leaf_state`
  * :c:func:`smf_get_current_executing_state`

* 电源管理

   * :c:func:`pm_device_driver_deinit`
   * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_DEFAULT_ENABLE`
   * :kconfig:option:`CONFIG_PM_S2RAM` 已重构为无提示选项。应用现在只需在设备树中启用任意“挂起到 RAM”电源状态即可。
   * :kconfig:option:`PM_S2RAM_CUSTOM_MARKING` 已重命名为 :kconfig:option:`HAS_PM_S2RAM_CUSTOM_MARKING`，并重构为无提示选项。如果 SoC 的“挂起到 RAM”实现需要该选项，现在会由 SoC 选择它。

* 管理

  * hawkBit

    * :kconfig:option:`CONFIG_HAWKBIT_REBOOT_NONE`
    * :kconfig:option:`CONFIG_HAWKBIT_CONFIRM_IMG_ON_INIT`
    * :kconfig:option:`CONFIG_HAWKBIT_ERASE_SECOND_SLOT_ON_CONFIRM`

  * MCUmgr

    * :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_UDP_DTLS`
    * :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_ALLOW_CONFIRM_NON_ACTIVE_SLOT`

* 网络

  * CoAP

    * :c:struct:`coap_client_response_data`
    * :c:member:`coap_client_request.payload_cb`
    * :kconfig:option:`CONFIG_COAP_CLIENT_MAX_PATH_LENGTH`
    * :kconfig:option:`CONFIG_COAP_CLIENT_MAX_EXTRA_OPTIONS`

  * 连接管理器

    * :c:macro:`NET_EVENT_CONN_IF_IDLE_TIMEOUT`
    * :c:func:`conn_mgr_if_set_idle_timeout`
    * :c:func:`conn_mgr_if_get_idle_timeout`
    * :c:func:`conn_mgr_if_used`

  * DNS

    * :c:enumerator:`DNS_QUERY_TYPE_CNAME`
    * :c:enumerator:`DNS_QUERY_TYPE_TXT`
    * :c:enumerator:`DNS_QUERY_TYPE_SRV`
    * :c:func:`dns_resolve_enable_packet_forwarding`
    * :c:func:`dns_resolve_remove_server_addresses`

  * HTTP

    * :kconfig:option:`CONFIG_HTTP_SERVER_STATIC_FS_RESPONSE_SIZE`
    * :c:struct:`http_service_config`

  * IPv6

    * :kconfig:option:`CONFIG_NET_IPV6_NS_TIMEOUT`
    * :c:func:`net_ipv6_get_addr_mcast_scope`

  * LwM2M

    * :c:type:`lwm2m_cache_filter_cb_t`
    * :c:func:`lwm2m_set_cache_filter`

  * MQTT-SN

    * :c:func:`mqtt_sn_predefine_topic`
    * :c:func:`mqtt_sn_update_will_topic`
    * :c:func:`mqtt_sn_update_will_message`
    * :c:func:`mqtt_sn_define_short_topic`

  * 杂项

    * :kconfig:option:`CONFIG_NET_LATMON`
    * :kconfig:option:`CONFIG_NETMIDI2_HOST`
    * :kconfig:option:`CONFIG_OCPP`
    * :c:member:`npf_rule.priority`
    * :c:macro:`NPF_PRIORITY`
    * :kconfig:option:`CONFIG_NET_CONFIG_CLOCK_SNTP_SET_RTC`
    * :c:func:`ppp_peer_async_control_character_map`

  * OpenThread

    * :kconfig:option:`CONFIG_OPENTHREAD_ZEPHYR_BORDER_ROUTER`
    * :kconfig:option:`CONFIG_OPENTHREAD_BORDER_ROUTING_DHCP6_PD_CLIENT`
    * :kconfig:option:`CONFIG_OPENTHREAD_CHANNEL_MONITOR_AUTO_START`
    * :kconfig:option:`CONFIG_OPENTHREAD_MAC_BEACON_PAYLOAD_PARSING`
    * :kconfig:option:`CONFIG_OPENTHREAD_MULTIPLE_INSTANCE_NUM`
    * :kconfig:option:`CONFIG_OPENTHREAD_PLATFORM_RADIO_COEX_ENABLE`
    * :kconfig:option:`CONFIG_OPENTHREAD_PLATFORM_USEC_TIMER`
    * :kconfig:option:`CONFIG_OPENTHREAD_RCP_RESTORATION_MAX_COUNT`
    * :kconfig:option:`CONFIG_OPENTHREAD_SRP_SERVER_FAST_START`
    * :kconfig:option:`CONFIG_OPENTHREAD_TREL_MANAGE_DNSSD`

  * Socket

    * :c:func:`zsock_listen` 现在支持 ``backlog`` 参数，TCP 服务器套接字会将待处理的传入连接数限制为该值。
    * :c:macro:`IP_RECVTTL`
    * :c:macro:`IPV6_PKTINFO`
    * :c:macro:`IPV6_RECVHOPLIMIT`
    * :c:macro:`IPV6_HOPLIMIT`

  * Wi-Fi

    * :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_DEBUG_SHOW_KEYS`
    * 由于证书验证已禁用，将企业加密设置为不安全。
    * 如果使用模式选项启用了 AP，则自动启用 AP 模式。
    * 在 wpa_supplicant 中新增用于后台扫描（bgscan）的配置选项。
    * 新增对多个虚拟接口（VIF）的支持。

* 蓝牙

  * 音频

    * :c:struct:`bt_audio_codec_cfg` 现在包含 target_latency 选项和 target_phy 选项
    * :c:func:`bt_bap_broadcast_source_foreach_stream`
    * :c:func:`bt_cap_initiator_broadcast_foreach_stream`
    * :c:struct:`bt_bap_stream` 现在包含一个 ``iso`` 字段，作为对 ISO 通道的引用
    * :c:func:`bt_bap_unicast_group_get_info`
    * :c:func:`bt_cap_unicast_group_get_info`
    * :c:func:`bt_bap_unicast_client_unregister_cb`

  * 主机

    * :c:struct:`bt_iso_unicast_info` 现在包含 ``cig_id`` 和 ``cis_id`` 字段
    * :c:struct:`bt_iso_broadcaster_info` 现在包含 ``big_handle`` 和 ``bis_number`` 字段
    * :c:struct:`bt_iso_sync_receiver_info` 现在包含 ``big_handle`` 和 ``bis_number`` 字段
    * :c:struct:`bt_le_ext_adv_info` 现在包含 ``sid`` 字段，表示 Advertising Set ID。
    * :kconfig:option:`CONFIG_BT_AUTO_PHY_PERIPHERAL_NONE`
    * :kconfig:option:`CONFIG_BT_AUTO_PHY_PERIPHERAL_1M`
    * :kconfig:option:`CONFIG_BT_AUTO_PHY_PERIPHERAL_2M`
    * :kconfig:option:`CONFIG_BT_AUTO_PHY_PERIPHERAL_CODED`
    * :kconfig:option:`CONFIG_BT_AUTO_PHY_CENTRAL_NONE`
    * :kconfig:option:`CONFIG_BT_AUTO_PHY_CENTRAL_1M`
    * :kconfig:option:`CONFIG_BT_AUTO_PHY_CENTRAL_2M`
    * :kconfig:option:`CONFIG_BT_AUTO_PHY_CENTRAL_CODED`

* 蜂窝网络

  * :c:enumerator:`CELLULAR_EVENT_MODEM_COMMS_CHECK_RESULT`

* 视频

  * :c:member:`video_format.size` 字段
  * :c:func:`video_estimate_fmt_size`
  * :c:func:`video_transfer_buffer`

* 触觉反馈

  * :kconfig:option:`CONFIG_HAPTICS_SHELL`

* 调制解调器

  * :kconfig:option:`CONFIG_MODEM_DEDICATED_WORKQUEUE`

* 运算放大器

  * 新增了通过 :kconfig:option:`CONFIG_OPAMP` 选择的运算放大器设备驱动 API。它支持通过设备树进行初始配置，并通过厂商特定的 API 进行运行时配置。
  * 新增对 NXP OPAMP :dtcompatible:`nxp,opamp` 的支持。
  * 新增对 NXP OPAMP_FAST :dtcompatible:`nxp,opamp_fast` 的支持。

.. zephyr-keep-sorted-stop

.. _boards_added_in_zephyr_4_3:

新增开发板
**********

..
  You may update this list as you contribute a new board during the release cycle, in order to make
  it visible to people who might be looking at the working draft of the release notes. However, note
  that this list will be recomputed at the time of the release, so you don't *have* to update it.
  In any case, just link the board, further details go in the board description.

* Adafruit Industries, LLC

   * :zephyr:board:`adafruit_feather_adalogger_rp2040` (``adafruit_feather_adalogger_rp2040``)
   * :zephyr:board:`adafruit_feather_canbus_rp2040` (``adafruit_feather_canbus_rp2040``)
   * :zephyr:board:`adafruit_feather_esp32` (``adafruit_feather_esp32``)
   * :zephyr:board:`adafruit_feather_rfm95_rp2040` (``adafruit_feather_rfm95_rp2040``)
   * :zephyr:board:`adafruit_feather_rp2040` (``adafruit_feather_rp2040``)
   * :zephyr:board:`adafruit_itsybitsy_rp2040` (``adafruit_itsybitsy_rp2040``)
   * :zephyr:board:`adafruit_metro_rp2040` (``adafruit_metro_rp2040``)
   * :zephyr:board:`adafruit_metro_rp2350` (``adafruit_metro_rp2350``)
   * :zephyr:board:`adafruit_trinkey_qt2040` (``adafruit_trinkey_qt2040``)

* Advanced Micro Devices (AMD), Inc.

   * :zephyr:board:`versalnet_apu` (``versalnet_apu``)

* Ai-Thinker Co., Ltd.

   * :zephyr:board:`ai_m62_12f_kit` (``ai_m62_12f_kit``)
   * :zephyr:board:`esp32_cam` (``esp32_cam``)

* Ambiq Micro, Inc.

   * :zephyr:board:`apollo2_evb` (``apollo2_evb``)

* Analog Devices, Inc.

   * :zephyr:board:`max32658evkit` (``max32658evkit``)

* Arduino

   * :zephyr:board:`arduino_uno_q` (``arduino_uno_q``)

* Core Devices LLC

   * :zephyr:board:`p2d` (``p2d``)
   * :zephyr:board:`pt2` (``pt2``)

* DFRobot

   * :zephyr:board:`beetle_rp2040` (``beetle_rp2040``)

* Doctors of Intelligence & Technology

   * :zephyr:board:`dt_xt_zb1_devkit` (``dt_xt_zb1_devkit``)

* Egis Technology Inc

   * :zephyr:board:`egis_et171` (``egis_et171``)

* Espressif Systems

   * :zephyr:board:`esp32h2_devkitm` (``esp32h2_devkitm``)

* FANKE Technology Co., Ltd.

   * :zephyr:board:`fk723m1_zgt6` (``fk723m1_zgt6``)

* Firefly

   * :zephyr:board:`roc_rk3588_pc` (``roc_rk3588_pc``)

* FoBE Studio

   * :zephyr:board:`quill_nrf52840_mesh` (``quill_nrf52840_mesh``)

* Guangdong Embedsky Technology Co., Ltd.

   * :zephyr:board:`tq_h503a` (``tq_h503a``)

* Infineon Technologies

   * :zephyr:board:`kit_psc3m5_evk` (``kit_psc3m5_evk``)
   * :zephyr:board:`kit_pse84_ai` (``kit_pse84_ai``)
   * :zephyr:board:`kit_pse84_eval` (``kit_pse84_eval``)

* Intel Corporation

   * :zephyr:board:`intel_ptl_h_crb` (``intel_ptl_h_crb``)

* Microchip Technology Inc.

   * :zephyr:board:`pic32cm_jh01_cnano` (``pic32cm_jh01_cnano``)
   * :zephyr:board:`pic32cm_jh01_cpro` (``pic32cm_jh01_cpro``)
   * :zephyr:board:`pic32cx_sg61_cult` (``pic32cx_sg61_cult``)
   * :zephyr:board:`pic32cz_ca80_cult` (``pic32cz_ca80_cult``)
   * :zephyr:board:`sam_e54_xpro` (``sam_e54_xpro``)
   * :zephyr:board:`sama7d65_curiosity` (``sama7d65_curiosity``)

* Nuvoton Technology Corporation

   * :zephyr:board:`numaker_m3334ki` (``numaker_m3334ki``)
   * :zephyr:board:`numaker_m5531` (``numaker_m5531``)

* NXP Semiconductors

   * :zephyr:board:`frdm_imx91` (``frdm_imx91``)
   * :zephyr:board:`frdm_imx93` (``frdm_imx93``)
   * :zephyr:board:`frdm_k32l2b3` (``frdm_k32l2b3``)
   * :zephyr:board:`frdm_mcxa344` (``frdm_mcxa344``)
   * :zephyr:board:`frdm_mcxa266` (``frdm_mcxa266``)
   * :zephyr:board:`frdm_mcxa346` (``frdm_mcxa346``)
   * :zephyr:board:`frdm_mcxa366` (``frdm_mcxa366``)
   * :zephyr:board:`frdm_mcxe247` (``frdm_mcxe247``)
   * :zephyr:board:`frdm_mcxe31b` (``frdm_mcxe31b``)
   * :zephyr:board:`frdm_mcxw23` (``frdm_mcxw23``)
   * :zephyr:board:`imx91_qsb` (``imx91_qsb``)
   * :zephyr:board:`imx95_evk_15x15` (``imx95_evk_15x15``)
   * :zephyr:board:`mcx_n9xx_evk` (``mcx_n9xx_evk``)
   * :zephyr:board:`mcx_n5xx_evk` (``mcx_n5xx_evk``)
   * :zephyr:board:`mcxw23_evk` (``mcxw23_evk``)

* Panasonic Corporation

   * :zephyr:board:`panb611evb` (``panb611evb``)

* PCB Cupid

   * :zephyr:board:`glyph_c6` (``glyph_c6``)

* RAKwireless Technology Limited

   * :zephyr:board:`rak3112` (``rak3112``)

* Raspberry Pi Foundation

   * :zephyr:board:`rpi_debug_probe` (``rpi_debug_probe``)

* Renesas Electronics Corporation

   * :zephyr:board:`ek_ra4c1` (``ek_ra4c1``)
   * :zephyr:board:`ek_ra8d2` (``ek_ra8d2``)
   * :zephyr:board:`ek_ra8m2` (``ek_ra8m2``)
   * :zephyr:board:`ek_rx261` (``ek_rx261``)
   * :zephyr:board:`fpb_rx261` (``fpb_rx261``)
   * :zephyr:board:`mcb_rx26t` (``mcb_rx26t``)
   * :zephyr:board:`mck_ra8t2` (``mck_ra8t2``)
   * :zephyr:board:`rssk_ra2l1` (``rssk_ra2l1``)

* Seeed Technology Co., Ltd

   * :zephyr:board:`wio_wm1110_dev_kit` (``wio_wm1110_dev_kit``)
   * :zephyr:board:`xiao_nrf54l15` (``xiao_nrf54l15``)

* Shanghai Ruiside Electronic Technology Co., Ltd.

   * :zephyr:board:`art_pi` (``art_pi``)

* Shenzhen Holyiot Technology Co., Ltd.

   * :zephyr:board:`holyiot_yj17095` (``holyiot_yj17095``)

* SiFli Technologies(Nanjing) Co., Ltd

   * :zephyr:board:`sf32lb52_devkit_lcd` (``sf32lb52_devkit_lcd``)

* Silicon Laboratories

   * :zephyr:board:`bgm220_ek4314a` (``bgm220_ek4314a``)
   * :zephyr:board:`pg23_pk2504a` (``pg23_pk2504a``)
   * :zephyr:board:`pg28_pk2506a` (``pg28_pk2506a``)
   * :zephyr:board:`siwx917_dk2605a` (``siwx917_dk2605a``)
   * :zephyr:board:`bg22_ek4108a` (``bg22_ek4108a``)
   * :zephyr:board:`xg22_ek2710a` (``xg22_ek2710a``)
   * :zephyr:board:`mgm260p_ek2713a` (``mgm260p_ek2713a``)
   * :zephyr:board:`pg26_ek2711a` (``pg26_ek2711a``)
   * :zephyr:board:`xg26_ek2709a` (``xg26_ek2709a``)
   * :zephyr:board:`bg29_rb4420a` (``bg29_rb4420a``)
   * :zephyr:board:`slwrb4182a` (``slwrb4182a``)
   * :zephyr:board:`slwrb4311a` (``slwrb4311a``)
   * :zephyr:board:`xg24_rb4186c` (``xg24_rb4186c``)
   * :zephyr:board:`xg24_rb4187c` (``xg24_rb4187c``)
   * :zephyr:board:`xgm240_rb4316a` (``xgm240_rb4316a``)
   * :zephyr:board:`xgm240_rb4317a` (``xgm240_rb4317a``)
   * :zephyr:board:`mgm260p_rb4350a` (``mgm260p_rb4350a``)
   * :zephyr:board:`xg26_rb4118a` (``xg26_rb4118a``)
   * :zephyr:board:`xg26_rb4120a` (``xg26_rb4120a``)
   * :zephyr:board:`bg27_rb4110b` (``bg27_rb4110b``)
   * :zephyr:board:`bg27_rb4111b` (``bg27_rb4111b``)
   * :zephyr:board:`xg27_rb4194a` (``xg27_rb4194a``)
   * :zephyr:board:`xg28_rb4401c` (``xg28_rb4401c``)

* SparkFun Electronics

   * :zephyr:board:`sparkfun_samd21_breakout` (``sparkfun_samd21_breakout``)

* SteelSeries

   * :zephyr:board:`apex_pro_mini` (``apex_pro_mini``)

* STMicroelectronics

   * :zephyr:board:`nucleo_c092rc` (``nucleo_c092rc``)
   * :zephyr:board:`stm32mp257f_dk` (``stm32mp257f_dk``)
   * :zephyr:board:`stm32wba65i_dk1` (``stm32wba65i_dk1``)

* Texas Instruments

   * :zephyr:board:`lp_mspm0g3519` (``lp_mspm0g3519``)
   * :zephyr:board:`lp_mspm0l2228` (``lp_mspm0l2228``)

* Toradex AG

   * :zephyr:board:`verdin_am62` (``verdin_am62``)

* Waveshare Electronics

   * :zephyr:board:`rp2040_geek` (``rp2040_geek``)
   * :zephyr:board:`rp2040_keyboard_3` (``rp2040_keyboard_3``)
   * :zephyr:board:`rp2040_matrix` (``rp2040_matrix``)

* WeAct Studio

   * :zephyr:board:`blackpill_h523ce` (``blackpill_h523ce``)
   * :zephyr:board:`blackpill_u585ci` (``blackpill_u585ci``)
   * :zephyr:board:`weact_esp32c3_mini` (``weact_esp32c3_mini``)
   * :zephyr:board:`weact_esp32c6_mini` (``weact_esp32c6_mini``)
   * :zephyr:board:`weact_esp32s3_mini` (``weact_esp32s3_mini``)
   * :zephyr:board:`weact_stm32g030_core` (``weact_stm32g030_core``)
   * :zephyr:board:`weact_stm32wb55_core` (``weact_stm32wb55_core``)
   * :zephyr:board:`weact_esp32s3_b` (``weact_esp32s3_b``)

.. _shields_added_in_zephyr_4_3:

新增扩展板
**********

  * :ref:`Adafruit 24LC32 EEPROM Shield <adafruit_24lc32>`
  * :ref:`Adafruit AHT20 Shield <adafruit_aht20>`
  * :ref:`Adafruit APDS9960 Shield <adafruit_apds9960>`
  * :ref:`Adafruit DPS310 Shield <adafruit_dps310>`
  * :ref:`Adafruit DRV2605L Shield <adafruit_drv2605l>`
  * :ref:`Adafruit FeatherWing 128x32 OLED Shield <adafruit_featherwing_128x32_oled>`
  * :ref:`Adafruit HT16K33 LED Matrix Shield <adafruit_ht16k33>`
  * :ref:`Adafruit I2C to 8 Channel Solenoid Driver Shield <adafruit_8chan_solenoid>`
  * :ref:`Adafruit INA219 Shield <adafruit_ina219>`
  * :ref:`Adafruit INA237 Shield <adafruit_ina237>`
  * :ref:`Adafruit LIS2MDL Shield <adafruit_lis2mdl>`
  * :ref:`Adafruit LIS3DH Shield <adafruit_lis3dh>`
  * :ref:`Adafruit LTR-329 Shield <adafruit_ltr329>`
  * :ref:`Adafruit MCP9808 Shield <adafruit_mcp9808>`
  * :ref:`Adafruit PCF8523 Shield <adafruit_pcf8523>`
  * :ref:`Adafruit TSL2591 Shield <adafruit_tsl2591>`
  * :ref:`Adafruit VCNL4040 Shield <adafruit_vcnl4040>`
  * :ref:`Adafruit VEML7700 Shield <adafruit_veml7700>`
  * :ref:`ArduCam CU450 OV5640 Camera Module <arducam_cu450_ov5640>`
  * :ref:`Arduino Modulino Movement <arduino_modulino_movement>`
  * :ref:`Arduino Modulino Thermo <arduino_modulino_thermo>`
  * :ref:`MikroElektronika 3D Hall 3 Click <mikroe_3d_hall_3_click_shield>`
  * :ref:`MikroElektronika Air Quality 3 Click <mikroe_air_quality_3_click_shield>`
  * :ref:`MikroElektronika Ambient 2 Click <mikroe_ambient_2_click_shield>`
  * :ref:`MikroElektronika H Bridge 4 Click <mikroe_h_bridge_4_click_shield>`
  * :ref:`MikroElektronika Illuminance Click <mikroe_illuminance_click_shield>`
  * :ref:`MikroElektronika IR Gesture Click <mikroe_ir_gesture_click_shield>`
  * :ref:`MikroElektronika LSM6DSL Click <mikroe_lsm6dsl_click_shield>`
  * :ref:`MikroElektronika Pressure 3 Click <mikroe_pressure_3_click_shield>`
  * :ref:`MikroElektronika Proximity 9 Click <mikroe_proximity_9_click_shield>`
  * :ref:`MikroElektronika RTC 18 Click <mikroe_rtc_18_click_shield>`
  * :ref:`Nordic nPM1304 EK <npm1304_ek>`
  * :ref:`Olimex SHIELD-MIDI <olimex_shield_midi>`
  * :ref:`Renesas EK-RA8D1 to RTK7EKA6M3B00001BU Display Adapter <ek_ra8d1_rtk7eka6m3b00001bu>`
  * :ref:`Renesas RTK0EG0019B01002BJ Capacitive Touch Application Shield <rtk0eg0019b01002bj>`
  * :ref:`Sierra Wireless HL/RC Module Evaluation Kit Shield <swir_hl78xx_ev_kit>`
  * :ref:`Sparkfun Environmental Combo Shield with ENS160 and BME280 <sparkfun_environmental_combo>`
  * :ref:`Sparkfun RV8803 Shield <sparkfun_rv8803>`
  * :ref:`Sparkfun SHTC3 Shield <sparkfun_shtc3>`

新增驱动
********

..
  Same as above for boards, this will also be recomputed at the time of the release.
  Just link the driver, further details go in the binding description


* :abbr:`ADC（模数转换器）`

   * :dtcompatible:`adi,ad4170-adc`
   * :dtcompatible:`adi,ad4190-adc`
   * :dtcompatible:`adi,ad4195-adc`
   * :dtcompatible:`adi,max32-adc-b-me18`
   * :dtcompatible:`infineon,autanalog-sar-adc`
   * :dtcompatible:`infineon,hppass-sar-adc`
   * :dtcompatible:`nxp,sar-adc`
   * :dtcompatible:`renesas,rx-adc`
   * :dtcompatible:`renesas,rz-adc-c`
   * :dtcompatible:`silabs,iadc`

* ARM 架构

   * :dtcompatible:`microchip,sercom-g1`
   * :dtcompatible:`nuvoton,numaker-npu`
   * :dtcompatible:`renesas,ra-npu`

* 音频

   * :dtcompatible:`dlg,da7212`
   * :dtcompatible:`nxp,micfil`

* 辅助显示

   * :dtcompatible:`titanmec,tm1637`

* 缓存

   * :dtcompatible:`bflb,l1c`

* 充电器

   * :dtcompatible:`nxp,pca9422-charger`

* 时钟控制

   * :dtcompatible:`bflb,bl61x-clock-controller`
   * :dtcompatible:`bflb,bl70x-clock-controller`
   * :dtcompatible:`infineon,fixed-clock`
   * :dtcompatible:`infineon,fixed-factor-clock`
   * :dtcompatible:`infineon,peri-div`
   * :dtcompatible:`mediatek,mt818x_cpuclk`
   * :dtcompatible:`microchip,sam-d5x-e5x-clock`
   * :dtcompatible:`nordic,nrf-iron-hsfll-local`
   * :dtcompatible:`nxp,mc-cgm`
   * :dtcompatible:`renesas,ra-cgc-utasel`
   * :dtcompatible:`renesas,rz-cgc`
   * :dtcompatible:`sifli,sf32lb-rcc-clk`
   * :dtcompatible:`st,stm32f4-rcc`
   * :dtcompatible:`st,stm32fx-pllsai-clock`
   * :dtcompatible:`st,stm32h5-rcc`
   * :dtcompatible:`st,stm32l0-hsi-clock`
   * :dtcompatible:`st,stm32l4-pllsai-clock`
   * :dtcompatible:`ti,cc23x0-lf-xosc`

* 比较器

   * :dtcompatible:`nxp,cmp`
   * :dtcompatible:`renesas,ra-lvd`
   * :dtcompatible:`renesas,rx-lvd`
   * :dtcompatible:`st,stm32-comp`
   * :dtcompatible:`st,stm32g4-comp`
   * :dtcompatible:`st,stm32h7-comp`

* 计数器

   * :dtcompatible:`infineon,tcpwm-counter`
   * :dtcompatible:`microchip,tcc-g1`
   * :dtcompatible:`nxp,imx-snvs-rtc`
   * :dtcompatible:`nxp,lpit`
   * :dtcompatible:`nxp,lpit-channel`
   * :dtcompatible:`nxp,stm`
   * :dtcompatible:`renesas,rz-cmtw-counter`

* CPU

   * :dtcompatible:`arm,cortex-a78`
   * :dtcompatible:`arm,cortex-m52`
   * :dtcompatible:`arm,cortex-m52f`
   * :dtcompatible:`intel,panther-lake`
   * :dtcompatible:`renesas,rxv1`
   * :dtcompatible:`renesas,rxv2`
   * :dtcompatible:`renesas,rxv3`
   * :dtcompatible:`snps,av5rhx`
   * :dtcompatible:`snps,av5rmx`
   * :dtcompatible:`xuantie,e907`

* :abbr:`CRC (Cyclic Redundancy Check)`

   * :dtcompatible:`renesas,ra-crc`

* 加密加速器

   * :dtcompatible:`espressif,esp32-aes`
   * :dtcompatible:`espressif,esp32-sha`
   * :dtcompatible:`nxp,els`
   * :dtcompatible:`st,stm32-hash`

* :abbr:`DAC（数模转换器）`

   * :dtcompatible:`adi,ad5601`
   * :dtcompatible:`adi,ad5611`
   * :dtcompatible:`adi,ad5621`
   * :dtcompatible:`atmel,samd5x-dac`
   * :dtcompatible:`silabs,vdac`

* 调试

   * :dtcompatible:`nordic,coresight-nrf`

* 显示

   * :dtcompatible:`chipone,co5300`
   * :dtcompatible:`himax,hx8379c`
   * :dtcompatible:`jdi,lpm013m126`
   * :dtcompatible:`nxp,imx-lcdifv3`
   * :dtcompatible:`sitronix,st7305`
   * :dtcompatible:`sitronix,st7306`
   * :dtcompatible:`sitronix,st7567`
   * :dtcompatible:`solomon,ssd1357`
   * :dtcompatible:`ultrachip,uc8151d`
   * :dtcompatible:`waveshare,7inch-dsi-lcd-c`
   * :dtcompatible:`zephyr,hub12`

* :abbr:`DMA（直接内存访问）`

   * :dtcompatible:`andestech,atcdmacx00`
   * :dtcompatible:`bflb,dma`
   * :dtcompatible:`nuvoton,npcx-gdma`
   * :dtcompatible:`renesas,ra-dma`
   * :dtcompatible:`renesas,rz-dmac`
   * :dtcompatible:`sifli,sf32lb-dmac`
   * :dtcompatible:`silabs,gpdma`

* 以太网

   * :dtcompatible:`intel,eth-plat`
   * :dtcompatible:`intel,igc-mac`
   * :dtcompatible:`microchip,ksz9131`
   * :dtcompatible:`microchip,sam-ethernet-controller`
   * :dtcompatible:`nxp,imx-netc`
   * :dtcompatible:`nxp,imx-netc-blk-ctrl`
   * :dtcompatible:`virtio,net`

* Flash 控制器

   * :dtcompatible:`adi,max32-spixf-nor`
   * :dtcompatible:`bflb,flash-controller`
   * :dtcompatible:`ite,it51xxx-manual-flash-1k`
   * :dtcompatible:`microchip,nvmctrl-g1-flash`
   * :dtcompatible:`nordic,nrf-mramc`
   * :dtcompatible:`nxp,kinetis-ftfc`
   * :dtcompatible:`nxp,xspi-nor`
   * :dtcompatible:`renesas,ra-flash-lp-controller`
   * :dtcompatible:`renesas,ra-mram-controller`
   * :dtcompatible:`renesas,rz-qspi-spibsc`
   * :dtcompatible:`renesas,rz-qspi-xspi`

* 文件系统

   * :dtcompatible:`zephyr,fstab,ext2`

* 电量计

   * :dtcompatible:`adi,ltc2959`
   * :dtcompatible:`silergy,sy24561`
   * :dtcompatible:`ti,bq40z50`

* :abbr:`GPIO（通用输入/输出）`

   * :dtcompatible:`aesc,gpio`
   * :dtcompatible:`arducam,ffc-40pin-connector`
   * :dtcompatible:`bflb,bl60x_70x-gpio`
   * :dtcompatible:`bflb,bl61x-gpio`
   * :dtcompatible:`fobe,quill-header`
   * :dtcompatible:`microchip,port-g1-gpio`
   * :dtcompatible:`microchip,sam-pio4`
   * :dtcompatible:`nxp,pca6408`
   * :dtcompatible:`nxp,pcal6408`
   * :dtcompatible:`nxp,pcal6416`
   * :dtcompatible:`nxp,pcal9538`
   * :dtcompatible:`nxp,pcal9539`
   * :dtcompatible:`nxp,pcal9722`
   * :dtcompatible:`sifli,sf32lb-gpio`
   * :dtcompatible:`sifli,sf32lb-gpio-parent`
   * :dtcompatible:`silabs,exp-header`
   * :dtcompatible:`silabs,gpio`
   * :dtcompatible:`silabs,gpio-port`

* 硬件信息

   * :dtcompatible:`nxp,cmc-reset-cause`
   * :dtcompatible:`nxp,imx-src-rev2`
   * :dtcompatible:`nxp,rstctl-hwinfo`

* :abbr:`I2C（集成电路间总线）`

   * :dtcompatible:`infineon,cat1-i2c-pdl`
   * :dtcompatible:`renesas,ra-i2c-sci`
   * :dtcompatible:`renesas,rz-iic`
   * :dtcompatible:`silabs,i2c`
   * :dtcompatible:`ti,cc23x0-i2c`

* :abbr:`I3C（改进型集成电路间总线）`

   * :dtcompatible:`adi,max32-i3c`

* IEEE 802.15.4

   * :dtcompatible:`st,stm32wba-ieee802154`

* 输入

   * :dtcompatible:`chipsemi,chsc5x`
   * :dtcompatible:`nxp,mcux-kpp`
   * :dtcompatible:`renesas,ra-ctsu`
   * :dtcompatible:`renesas,rx-ctsu`

* 中断控制器

   * :dtcompatible:`hazard3,hazard3-intc`
   * :dtcompatible:`microchip,dmec-ecia-girq`
   * :dtcompatible:`nxp,wuu`
   * :dtcompatible:`renesas,rz-icu`
   * :dtcompatible:`renesas,rz-intc`
   * :dtcompatible:`sifive,clic-draft`

* :abbr:`LED（发光二极管）`

   * :dtcompatible:`leds-group-multicolor`
   * :dtcompatible:`nxp,pca9533`

* :abbr:`LED（发光二极管）` 灯带

   * :dtcompatible:`worldsemi,ws2812-uart`

* 邮箱

   * :dtcompatible:`renesas,ra-ipc-mbox`

* :abbr:`MDIO（管理数据输入/输出）`

   * :dtcompatible:`intel,igc-mdio`

* 内存控制器

   * :dtcompatible:`bflb,bl61x-psram`
   * :dtcompatible:`motorola,mc146818-bbram`
   * :dtcompatible:`nxp,xspi-psram`
   * :dtcompatible:`st,stm32-ospi-psram`

* :abbr:`MFD（多功能设备）`

   * :dtcompatible:`motorola,mc146818-mfd`
   * :dtcompatible:`nxp,pca9422`
   * :dtcompatible:`nxp,sc18is606`
   * :dtcompatible:`sifli,sf32lb-rcc`

* :abbr:`MIPI DSI（移动产业处理器接口显示串行接口）`

   * :dtcompatible:`nxp,mipi-dsi-dwc`
   * :dtcompatible:`st,stm32u5-mipi-dsi`

* 其他

   * :dtcompatible:`nxp,imx93-mediamix`
   * :dtcompatible:`nxp,rt600-dsp-ctrl`
   * :dtcompatible:`nxp,rt700-dsp-ctrl-hifi4`
   * :dtcompatible:`renesas,rx-dtc`
   * :dtcompatible:`st,stm32-npu`

* 调制解调器

   * :dtcompatible:`quectel,bg96`
   * :dtcompatible:`swir,hl7812`
   * :dtcompatible:`swir,hl7812-gnss`
   * :dtcompatible:`swir,hl7812-offload`
   * :dtcompatible:`swir,hl78xx`
   * :dtcompatible:`swir,hl78xx-gnss`
   * :dtcompatible:`swir,hl78xx-offload`

* 多比特 SPI

   * :dtcompatible:`nordic,nrf-qspi-v2`

* :abbr:`MTD（存储器技术设备）`

   * :dtcompatible:`andestech,qspi-nor-xip`
   * :dtcompatible:`atmel,at25xv021a`
   * :dtcompatible:`infineon,fm25xxx`
   * :dtcompatible:`jedec,qspi-nor`
   * :dtcompatible:`renesas,ra-nv-mram`
   * :dtcompatible:`renesas,ra-qspi-nor`
   * :dtcompatible:`sifli,sf32lb-mpi-qspi-nor`

* :abbr:`OPAMP（运算放大器）`

   * :dtcompatible:`nxp,opamp`
   * :dtcompatible:`nxp,opamp-fast`

* 引脚控制

   * :dtcompatible:`ambiq,apollo2-pinctrl`
   * :dtcompatible:`microchip,port-g1-pinctrl`
   * :dtcompatible:`nxp,imx-blkctrl-ns-aon`
   * :dtcompatible:`nxp,imx-blkctrl-wakeup`
   * :dtcompatible:`nxp,mcxe31x-siul2-pinctrl`
   * :dtcompatible:`sifli,sf32lb52x-pinmux`

* 电源管理

   * :dtcompatible:`ite,it8xxx2-power-elpm`
   * :dtcompatible:`nxp,cmc`
   * :dtcompatible:`nxp,spc`
   * :dtcompatible:`nxp,vbat`
   * :dtcompatible:`renesas,ra-battery-backup`
   * :dtcompatible:`sifli,sf32lb-aon`
   * :dtcompatible:`sifli,sf32lb52x-pmuc`

* 电源域

   * :dtcompatible:`nordic,nrfs-gdpwr`
   * :dtcompatible:`nordic,nrfs-swext`
   * :dtcompatible:`silabs,siwx91x-power-domain`

* :abbr:`PWM（脉宽调制）`

   * :dtcompatible:`ambiq,ctimer-pwm`
   * :dtcompatible:`ambiq,timer-pwm`
   * :dtcompatible:`infineon,tcpwm-pwm`
   * :dtcompatible:`microchip,tcc-g1-pwm`
   * :dtcompatible:`renesas,rz-mtu-pwm`
   * :dtcompatible:`ti,cc23x0-lgpt-pwm`

* 四线 SPI

   * :dtcompatible:`adi,max32-spixf`
   * :dtcompatible:`renesas,ra-qspi`
   * :dtcompatible:`renesas,rz-spibsc`
   * :dtcompatible:`renesas,rz-xspi`

* 稳压器

   * :dtcompatible:`nxp,pca9422-regulator`
   * :dtcompatible:`nxp,vrefv1`

* 保留内存

   * :dtcompatible:`renesas,ofs-memory`

* 复位控制器

   * :dtcompatible:`microchip,rstc-g1-reset`
   * :dtcompatible:`nxp,mrcc-reset`
   * :dtcompatible:`sifli,sf32lb-rcc-rctl`

* 保留内存

   * :dtcompatible:`sifli,sf32lb-rtc-backup`
   * :dtcompatible:`silabs,buram`

* :abbr:`RNG（随机数发生器）`

   * :dtcompatible:`ambiq,puf-trng`
   * :dtcompatible:`nxp,els-trng`

* :abbr:`RTC（实时时钟）`

   * :dtcompatible:`microcrystal,rv3032`
   * :dtcompatible:`nxp,pcf85063a`
   * :dtcompatible:`renesas,ra-rtc`
   * :dtcompatible:`sifli,sf32lb-rtc`
   * :dtcompatible:`silabs,rtcc`
   * :dtcompatible:`silabs,sysrtc`
   * :dtcompatible:`ti,mspm0-rtc`
   * :dtcompatible:`zephyr,rtc-counter`

* Renesas RX

   * :dtcompatible:`renesas,rx-swint`

* :abbr:`SDHC（安全数字主机控制器）`

   * :dtcompatible:`microchip,sama7g5-sdmmc`
   * :dtcompatible:`st,stm32-sdio`

* 传感器

   * :dtcompatible:`allegro,als31300`
   * :dtcompatible:`invensense,icm42686`
   * :dtcompatible:`invensense,icm4268x`
   * :dtcompatible:`maxbotix,mb7040`
   * :dtcompatible:`maxim,max32664c`
   * :dtcompatible:`microchip,mtch9010`
   * :dtcompatible:`nxp,pmc-tmpsns`
   * :dtcompatible:`nxp,tmpsns`
   * :dtcompatible:`omron,2smpb-02e`
   * :dtcompatible:`omron,d6f-p0001`
   * :dtcompatible:`omron,d6f-p0010`
   * :dtcompatible:`pni,rm3100`
   * :dtcompatible:`st,iis3dwb`
   * :dtcompatible:`ti,hdc302x`
   * :dtcompatible:`ti,ina228`
   * :dtcompatible:`ti,ina7xx`
   * :dtcompatible:`vishay,veml6046`
   * :dtcompatible:`we,wsen-isds-2536030320001`
   * :dtcompatible:`we,wsen-pdms-25131308XXX05`

* 串行控制器

   * :dtcompatible:`infineon,cat1-uart-pdl`
   * :dtcompatible:`microchip,sercom-g1-uart`
   * :dtcompatible:`sifli,sf32lb-usart`
   * :dtcompatible:`virtio,console`
   * :dtcompatible:`zephyr,uart-bitbang`

* :abbr:`SPI（串行外设接口）`

   * :dtcompatible:`egis,et171-spi`
   * :dtcompatible:`infineon,cat1-spi-pdl`
   * :dtcompatible:`nxp,sc18is606-spi`
   * :dtcompatible:`renesas,rz-spi`
   * :dtcompatible:`ti,omap-mcspi`

* 系统控制器

   * :dtcompatible:`sifli,sf32lb-cfg`

* 转速计

   * :dtcompatible:`zephyr,tach-gpio`

* 定时器

   * :dtcompatible:`ambiq,ctimer`
   * :dtcompatible:`ambiq,timer`
   * :dtcompatible:`infineon,tcpwm`
   * :dtcompatible:`microchip,xec-basic-timer`
   * :dtcompatible:`renesas,rz-cmtw`
   * :dtcompatible:`renesas,rz-mtu`
   * :dtcompatible:`st,stm32wb0-radio-timer`

* USB

   * :dtcompatible:`espressif,esp32-usb-otg`

* 视频

   * :dtcompatible:`himax,hm01b0`
   * :dtcompatible:`renesas,ra-ceu`
   * :dtcompatible:`st,stm32-jpeg`
   * :dtcompatible:`st,stm32-venc`

* 看门狗

   * :dtcompatible:`nxp,cop`
   * :dtcompatible:`renesas,rx-iwdt`
   * :dtcompatible:`renesas,rz-wdt`
   * :dtcompatible:`sifli,sf32lb-wdt`
   * :dtcompatible:`ti,j7-rti-wdt`
   * :dtcompatible:`xlnx,versal-wwdt`

* Wi-Fi

   * :dtcompatible:`nordic,wlan`

* :abbr:`XSPI（扩展串行外设接口）`

   * :dtcompatible:`nxp,xspi`

新增示例
********

..
  Same as above for boards and drivers, this will also be recomputed at the time of the release.
 Just link the sample, further details go in the sample documentation itself.

* :zephyr:code-sample:`adc_stream`
* :zephyr:code-sample:`capture`
* :zephyr:code-sample:`coap-upload`
* :zephyr:code-sample:`cpu_freq_on_demand`
* :zephyr:code-sample:`crc_drivers`
* :zephyr:code-sample:`crc_subsys`
* :zephyr:code-sample:`ext2-fstab`
* :zephyr:code-sample:`frdm_mcxa156_lpdac_opamp_lpadc`
* :zephyr:code-sample:`hello_hl78xx`
* :zephyr:code-sample:`instrumentation`
* :zephyr:code-sample:`latmon-client`
* :zephyr:code-sample:`max32664c`
* :zephyr:code-sample:`mctp-usb-endpoint`
* :zephyr:code-sample:`mctp_i2c_bus_endpoint`
* 基于 I2C+GPIO 的 PMCI MCTP（``mctp_i2c_bus_owner``）
* :zephyr:code-sample:`msg_queue`
* :zephyr:code-sample:`netmidi2`
* :zephyr:code-sample:`ocpp`
* :zephyr:code-sample:`opamp_output_measure`
* :zephyr:code-sample:`openthread-border-router`
* :zephyr:code-sample:`producer_consumer`
* :zephyr:code-sample:`quality-of-service`
* :zephyr:code-sample:`red-black-tree`
* :zephyr:code-sample:`renesas_lvd`
* :zephyr:code-sample:`rtk0eg0019b01002bj`
* :zephyr:code-sample:`veml6046`
* :zephyr:code-sample:`virtiofs`

库与子系统
**********

* 固件

  * SCMI

    * 新增了 :kconfig:option:`ARM_SCMI_CHAN_SEM_TIMEOUT_USEC`，以便配置通道信号量超时。
    * 直接使用 :c:func:`scmi_status_to_errno` 检查返回的命令状态码。
    * 为 :c:func:`scmi_send_message` 新增了一个参数，允许用户指定是否使用轮询。
    * [NXP] 与 NXP 专用 CPU 协议相关的多项新增。

* 日志：

  * 新增了混合限流日志宏，可在消息频繁生成时防止日志泛滥。系统既提供便捷宏（使用来自 :kconfig:option:`CONFIG_LOG_RATELIMIT_INTERVAL_MS` 的默认速率），也提供显式速率宏（带自定义速率参数）。这遵循了 Linux 的 ``printk_ratelimited`` 模式，同时提供了更大的灵活性。限流是按宏调用点进行的，这意味着对限流宏的每次不同调用都有各自独立的速率限制。通过 :kconfig:option:`CONFIG_LOG_RATELIMIT` 可全局启用/禁用限流日志。禁用限流时，可以通过 :kconfig:option:`CONFIG_LOG_RATELIMIT_FALLBACK` 控制行为，以记录所有消息或将其完全丢弃。有关更多详细信息，请参见 :ref:`logging_ratelimited`。

* Mbed TLS

  * 新增了 Kconfig 选项 :kconfig:option:`CONFIG_PSA_CRYPTO`，以简化 PSA Crypto API 提供程序的启用。如果启用了 :kconfig:option:`CONFIG_BUILD_WITH_TFM`，则为 TF-M；否则为 Mbed TLS。前者会设置 :kconfig:option:`CONFIG_PSA_CRYPTO_PROVIDER_TFM`，后者则设置 :kconfig:option:`CONFIG_PSA_CRYPTO_PROVIDER_MBEDTLS`。还新增了 :kconfig:option:`CONFIG_PSA_CRYPTO_PROVIDER_CUSTOM`，以允许最终用户提供自定义解决方案。

  * 已从 3.6.4 版本更新到 3.6.5 版本。本次发布的版本说明见以下链接：

    * https://github.com/Mbed-TLS/mbedtls/releases/tag/mbedtls-3.6.5

* 安全存储

  * 实验性状态已被移除（:github:`96483`）。

其他值得注意的变更
******************

..
  Any more descriptive subsystem or driver changes. Do you really want to write
  a paragraph or is it enough to link to the api/driver/Kconfig/board page above?

* Nordic Semiconductor nRF54L09 PDK（``nrf54l09pdk``）仅面向仿真器，现已从代码树中移除。一旦有正式的开发板定义可用，它将被替换。

* 移除了对 Nordic Semiconductor nRF54L20 PDK（``nrf54l20pdk``）的支持，因为它已被 :zephyr:board:`nrf54lm20dk` 取代（``nrf54lm20dk``）。
