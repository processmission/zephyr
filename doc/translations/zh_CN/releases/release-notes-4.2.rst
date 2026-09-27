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

.. _zephyr_4.2:

Zephyr 4.2.0
############

我们很高兴地宣布 Zephyr 4.2.0 版本正式发布。

本次发布的主要增强包括：

**Renesas RX 初步支持**
  现在支持 Renesas RX 架构，包括基于 QEMU 的 :zephyr:board:`开发板目标 <qemu_rx>`。

**USB 视频类驱动**
  USB 设备栈现在支持 USB Video Class（UVC），可将摄像头设备和其他图像/视频源作为标准 USB 视频设备对外提供。参见 :zephyr:code-sample:`uvc` 开始使用。

**Twister 功耗测试装置**
  全新的 :ref:`Twister 测试装置 <twister_power_harness>` 可以测量被测设备的功耗，并确保其保持在给定容差范围内。

**MQTT 5.0**
  网络协议栈现在全面支持 :ref:`MQTT 5.0 <mqtt_socket_interface>` 协议。

**Bluetooth Classic 改进**
  Bluetooth Classic 协议栈现在支持 **Hands-Free Profile** 规范（HFP），涵盖 Audio Gateway（AG）和 Hands-Free（HF）两种角色。

**Zbus**
  :ref:`Zbus 库 <zbus>` 随 API v1.0.0 的发布升级为稳定状态。

**开发板支持扩展**
  本次发布新增了对 96 个 :ref:`新开发板 <boards_added_in_zephyr_4_2>` 和 22 个 :ref:`新扩展板 <shields_added_in_zephyr_4_2>` 的支持。

将应用从 Zephyr v4.1.0 迁移到 Zephyr v4.2.0 时需要或建议采取的变更概览，见单独的 :ref:`迁移指南 <migration_4.2>`。

以下小节按组件详细列出各项变更。

安全漏洞相关
************

本次发布修复了以下 CVE：

* :cve:`2025-12890` `蓝牙：外设：对畸形连接请求的处理不当 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8hrf-pfww-83v9>`_
* :cve:`2025-27809` `TLS 客户端可能无意中跳过服务器认证 <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-03-1/>`_
* :cve:`2025-27810` `TLS 握手中可能存在的认证绕过 <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-03-2/>`_
* :cve:`2025-2962` `dns_copy_qname 中的无限循环 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-2qp5-c2vq-g2ww>`_
* :cve:`2025-52496` `AESNI 支持检测中的竞态条件 <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-1/>`_
* :cve:`2025-52497` `解析 PEM 加密数据时发生堆缓冲区下溢读取 <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-2/>`_
* :cve:`2025-49600` `LMS 验证中未检查返回值导致可绕过签名 <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-3/>`_
* :cve:`2025-49601` `mbedtls_lms_import_public_key() 中的越界读取 <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-4/>`_
* :cve:`2025-49087` `使用 PKCS#7 填充的块密码解密中存在时序侧信道 <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-5/>`_
* :cve:`2025-48965` `使用 mbedtls_asn1_store_named_data() 后发生空指针解引用 <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-6/>`_
* :cve:`2025-47917` `mbedtls_x509_string_to_names() 中具有误导性的内存管理 <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-7/>`_
* :cve:`2025-7403`：在 2025-09-05 前处于保密状态

更多详细信息见：https://docs.zephyrproject.org/latest/security/vulnerabilities.html

API 变更
********

移除的 API 和选项
=================

* 移除了已弃用的 ``net_buf_put()`` 和 ``net_buf_get()`` API 函数。

* 移除了已弃用的 ``include/zephyr/net/buf.h`` 头文件。

* 移除了 ``--disable-unrecognized-section-test`` Twister 选项。该测试已删除，该选项对应的行为成为默认行为。

* 移除了已弃用的 ``kscan`` 子系统。

* 移除了 :dtcompatible:`meas,ms5837`，改用 :dtcompatible:`meas,ms5837-30ba` 和 :dtcompatible:`meas,ms5837-02ba`。

* 从 :c:struct:`video_driver_api` 中移除了 ``get_ctrl`` 驱动 API。

* 移除了 ``CONFIG_I3C_USE_GROUP_ADDR`` 以及对 I3C 设备组地址的支持。

已弃用的 API 和选项
===================

* 调度器 Kconfig 选项 CONFIG_SCHED_DUMB 和 CONFIG_WAITQ_DUMB 已重命名并弃用。请改用 :kconfig:option:`CONFIG_SCHED_SIMPLE` 和 :kconfig:option:`CONFIG_WAITQ_SIMPLE`。

* Kconfig 选项 :kconfig:option:`CONFIG_LWM2M_ENGINE_MESSAGE_HEADER_SIZE` 已被移除。所需的报头大小应计入消息大小，并通过 :kconfig:option:`CONFIG_LWM2M_COAP_MAX_MSG_SIZE` 配置。需要特别注意确保所用的 CoAP 块大小（:kconfig:option:`CONFIG_LWM2M_COAP_BLOCK_SIZE`）在包含报头的情况下仍能容纳给定的消息大小。此前的预留空间为 48 字节。

* TLS 凭证类型 ``TLS_CREDENTIAL_SERVER_CERTIFICATE`` 已重命名并弃用，请改用 :c:enumerator:`TLS_CREDENTIAL_PUBLIC_CERTIFICATE`。

* ``arduino_uno_r4_minima`` 和 ``arduino_uno_r4_wifi`` 开发板目标已弃用，改用带有修订版本的新开发板 ``arduino_uno_r4`` （``arduino_uno_r4@minima`` 和 ``arduino_uno_r4@wifi``）。

* ``esp32c6_devkitc`` 开发板目标已弃用，并重命名为 ``esp32c6_devkitc/esp32c6/hpcore``。

* ``xiao_esp32c6`` 开发板目标已弃用，并重命名为 ``xiao_esp32c6/esp32c6/hpcore``。

* Kconfig 选项 :kconfig:option:`CONFIG_HAWKBIT_DDI_NO_SECURITY` 已弃用，因为 hawkBit 服务器 0.8.0 版本已移除对匿名认证的支持。

* Kconfig 选项 :kconfig:option:`CONFIG_BT_CONN_TX_MAX` 已弃用。待处理的 TX 缓冲区数量现在与 :kconfig:option:`CONFIG_BT_BUF_ACL_TX_COUNT` Kconfig 选项保持一致。

* Kconfig 选项 :kconfig:option:`CONFIG_CRYPTO_TINYCRYPT_SHIM` 已被移除。该选项自 Zephyr 4.0 起弃用，当时建议用户迁移到其他加密后端。

* Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_USES_TINYCRYPT` 已被移除。该选项自 Zephyr 4.0 起弃用。当时建议用户改用 :kconfig:option:`CONFIG_BT_MESH_USES_MBEDTLS_PSA` 或 :kconfig:option:`CONFIG_BT_MESH_USES_TFM_PSA`。

本版本中的稳定 API 变更
=======================

* ``net_mgmt`` 事件处理函数 :c:type:`net_mgmt_event_handler_t` 和请求处理函数 :c:type:`net_mgmt_request_handler_t` 的 API 签名已变更。事件值类型从 ``uint32_t`` 改为 ``uint64_t``。

新增 API 和选项
===============

..
  Link to new APIs here, in a group if you think it's necessary, no need to get
  fancy just list the link, that should contain the documentation. If you feel
  like you need to add more details, add them in the API documentation code
  instead.

.. zephyr-keep-sorted-start re(^\* \w)

* I2C

  * :c:func:`i2c_configure_dt`.
  * :c:macro:`I2C_DEVICE_DT_DEINIT_DEFINE`
  * :c:macro:`I2C_DEVICE_DT_INST_DEINIT_DEFINE`

* I3C

  * :kconfig:option:`CONFIG_I3C_MODE`
  * :kconfig:option:`CONFIG_I3C_CONTROLLER_ROLE_ONLY`
  * :kconfig:option:`CONFIG_I3C_TARGET_ROLE_ONLY`
  * :kconfig:option:`CONFIG_I3C_DUAL_ROLE`
  * :c:func:`i3c_ccc_do_rstdaa`

* LVGL（Light and Versatile Graphics Library）

    * LVGL 模块已同步到 v9.3，带来了大量上游改进和新功能。
    * LVGL 子系统现在支持多个显示器同时工作，包括正确的输入设备与显示器绑定。
    * 为 SSD1327、SSD1320、SSD1322 和 ST75256 等显示器新增 L8/Y8 像素格式支持。
    * :kconfig:option:`CONFIG_LV_Z_COLOR_MONO_HW_INVERSION`

* LoRaWAN

   * :c:func:`lorawan_request_link_check`

* PCIe

   * :kconfig:option:`CONFIG_NVME_PRP_PAGE_SIZE`

* SPI

  * :c:macro:`SPI_DEVICE_DT_DEINIT_DEFINE`
  * :c:macro:`SPI_DEVICE_DT_INST_DEINIT_DEFINE`

* Sys

  * :c:func:`util_eq`
  * :c:func:`util_memeq`
  * :c:func:`sys_clock_gettime`
  * :c:func:`sys_clock_settime`
  * :c:func:`sys_clock_nanosleep`

* USB

  * :c:func:`uvc_set_video_dev`

* UpdateHub

  * :c:func:`updatehub_report_error`

* ZBus

  * 随着 API 版本 v1.0.0 的发布，Zbus 已达到稳定状态。
  * 运行时观察者可以在不使用堆的情况下工作。现在可以为运行时观察者节点选择静态分配、动态分配或不分配。
  * 使用 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_NONE` 的运行时观察者必须使用新函数 :c:func:`zbus_chan_add_obs_with_node`。

  * :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_DYNAMIC`
  * :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_STATIC`
  * :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_NONE`
  * :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_POOL_SIZE`

* 传感器

  * :c:func:`sensor_value_to_deci`
  * :c:func:`sensor_value_to_centi`

* 内核

 * :c:macro:`K_TIMEOUT_ABS_SEC`
 * :c:func:`timespec_add`
 * :c:func:`timespec_compare`
 * :c:func:`timespec_equal`
 * :c:func:`timespec_is_valid`
 * :c:func:`timespec_negate`
 * :c:func:`timespec_normalize`
 * :c:func:`timespec_from_timeout`
 * :c:func:`timespec_to_timeout`
 * :c:func:`k_heap_array_get`

* 存储

  * :c:func:`flash_area_copy()`

* 显示

    * 新增 :c:func:`display_clear` API，可按标准化方式清除显示内容。
    * 字符帧缓冲（CFB）子系统现在支持通过 :c:func:`cfb_draw_circle` 绘制圆形。

* 构建系统

  * Sysbuild

    * 使用 :kconfig:option:`SB_CONFIG_MCUBOOT_MODE_FIRMWARE_UPDATER` 时，sysbuild 新增固件加载器镜像的设置/选择支持，可通过 ``SB_CONFIG_FIRMWARE_LOADER`` 配置，例如用 :kconfig:option:`SB_CONFIG_FIRMWARE_LOADER_IMAGE_SMP_SVR` 选择 :zephyr:code-sample:`smp-svr`。
    * sysbuild 新增单应用 RAM 加载支持，使用 :kconfig:option:`SB_CONFIG_MCUBOOT_MODE_SINGLE_APP_RAM_LOAD`。

* 架构

  * NIOS2 架构已从 Zephyr 中移除。
  * :kconfig:option:`ARCH_HAS_VECTOR_TABLE_RELOCATION`
  * :kconfig:option:`CONFIG_SRAM_VECTOR_TABLE` 从 ``zephyr/Kconfig.zephyr`` 移到 ``zephyr/arch/Kconfig``，并为其添加了依赖关系。

* 步进电机

  * :c:func:`stepper_stop()`

* 电源管理

    * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_USE_SYSTEM_WQ`
    * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_USE_DEDICATED_WQ`
    * :kconfig:option:`CONFIG_PM_DEVICE_DRIVER_NEEDS_DEDICATED_WQ`
    * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_DEDICATED_WQ_STACK_SIZE`
    * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_DEDICATED_WQ_PRIO`
    * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_DEDICATED_WQ_INIT_PRIO`
    * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_ASYNC`

* 管理

  * MCUmgr

    * image mgmt 组新增固件加载器支持，使用 :kconfig:option:`CONFIG_MCUBOOT_BOOTLOADER_MODE_FIRMWARE_UPDATER`。
    * OS 组的 reset 命令新增可选启动模式（使用 retention boot mode），通过 :kconfig:option:`CONFIG_MCUMGR_GRP_OS_RESET_BOOT_MODE` 配置。

* 网络：

  * CoAP

    * :c:macro:`COAPS_SERVICE_DEFINE`

  * DHCPv4

    * :kconfig:option:`CONFIG_NET_DHCPV4_INIT_REBOOT`

  * DNS

    * :c:func:`dns_resolve_service`
    * :c:func:`dns_resolve_reconfigure_with_interfaces`

  * HTTP

    * :kconfig:option:`CONFIG_HTTP_SERVER_COMPRESSION`

  * IPv4

    * :kconfig:option:`CONFIG_NET_IPV4_MTU`

  * LwM2M

    * :kconfig:option:`CONFIG_LWM2M_SERVER_BOOTSTRAP_ON_FAIL`
    * 实现了大于、小于和步长（Step）观察属性的处理（参见 :kconfig:option:`CONFIG_LWM2M_MAX_NOTIFIED_NUMERICAL_RES_TRACKED`）。

  * 杂项

    * :c:func:`net_if_oper_state_change_time`

  * MQTT

    * :kconfig:option:`CONFIG_MQTT_VERSION_5_0`
    * :c:member:`mqtt_transport.if_name`

  * OpenThread

    * 将 OpenThread 相关的 Kconfig 选项从 :zephyr_file:`subsys/net/l2/openthread/Kconfig` 移至 :zephyr_file:`modules/openthread/Kconfig`。
    * 重构了 OpenThread 网络 API，参见 :ref:`迁移指南 <migration_4.2>` 中的 OpenThread 部分。
    * :kconfig:option:`CONFIG_OPENTHREAD_SYS_INIT`
    * :kconfig:option:`CONFIG_OPENTHREAD_SYS_INIT_PRIORITY`

  * SNTP

    * :c:func:`sntp_init_async`
    * :c:func:`sntp_send_async`
    * :c:func:`sntp_read_async`
    * :c:func:`sntp_close_async`

  * Socket

    * :kconfig:option:`CONFIG_NET_SOCKETS_INET_RAW`
    * :c:func:`socket_offload_dns_enable`
    * 为 :ref:`socket_service_interface` 库新增了文档页面。
    * 新增 socket 选项：

      * :c:macro:`IP_MULTICAST_LOOP`
      * :c:macro:`IPV6_MULTICAST_LOOP`
      * :c:macro:`TLS_CERT_VERIFY_RESULT`

  * Wi-Fi

    * :kconfig:option:`CONFIG_WIFI_USAGE_MODE`
    * 在 Wi-Fi 管理文档（``doc/connectivity/networking/api/wifi.rst``）中新增了一节，逐步介绍如何使用 FreeRADIUS 脚本为 Wi-Fi 生成测试证书。这有助于用户在自己的测试环境中复现这一过程。
    * 将 hostap 的 IPC 机制从 socketpair 改为 k_fifo。根据所启用的 Wi-Fi 配置选项，使用原生 Wi-Fi 协议栈时最多可节省 6-8 kB 内存。

  * zperf

    * :kconfig:option:`CONFIG_ZPERF_SESSION_PER_THREAD`
    * :c:member:`zperf_upload_params.data_loader`
    * :kconfig:option:`CONFIG_NET_ZPERF_SERVER`

* 蓝牙

  * 音频

    * :c:macro:`BT_BAP_ADV_PARAM_CONN_QUICK`
    * :c:macro:`BT_BAP_ADV_PARAM_CONN_REDUCED`
    * :c:macro:`BT_BAP_CONN_PARAM_SHORT_7_5`
    * :c:macro:`BT_BAP_CONN_PARAM_SHORT_10`
    * :c:macro:`BT_BAP_CONN_PARAM_RELAXED`
    * :c:macro:`BT_BAP_ADV_PARAM_BROADCAST_FAST`
    * :c:macro:`BT_BAP_ADV_PARAM_BROADCAST_SLOW`
    * :c:macro:`BT_BAP_PER_ADV_PARAM_BROADCAST_FAST`
    * :c:macro:`BT_BAP_PER_ADV_PARAM_BROADCAST_SLOW`
    * :c:func:`bt_csip_set_member_set_size_and_rank`
    * :c:func:`bt_csip_set_member_get_info`
    * :c:func:`bt_bap_unicast_group_foreach_stream`
    * :c:func:`bt_cap_unicast_group_create`
    * :c:func:`bt_cap_unicast_group_reconfig`
    * :c:func:`bt_cap_unicast_group_add_streams`
    * :c:func:`bt_cap_unicast_group_delete`
    * :c:func:`bt_cap_unicast_group_foreach_stream`

  * 主机

    * :c:func:`bt_le_get_local_features`
    * :c:func:`bt_le_bond_exists`
    * :c:func:`bt_br_bond_exists`
    * :c:func:`bt_conn_lookup_addr_br`
    * :c:func:`bt_conn_get_dst_br`
    * LE Connection Subrating 不再是实验性功能。
    * 从 :c:func:`bt_unpair` 中移除对经典蓝牙绑定信息的删除操作，并新增 :c:func:`bt_br_unpair`。
    * 从 :c:func:`bt_foreach_bond` 中移除对经典蓝牙绑定信息的查询，并新增 :c:func:`bt_br_foreach_bond`。
    * 为 :c:func:`bt_br_set_discoverable` 新增 ``limited`` 参数，以支持经典蓝牙的受限可发现模式。
    * 为经典蓝牙 L2CAP 启用重传和流控，涉及 :kconfig:option:`CONFIG_BT_L2CAP_RET`、:kconfig:option:`CONFIG_BT_L2CAP_FC`、:kconfig:option:`CONFIG_BT_L2CAP_ENH_RET` 和 :kconfig:option:`CONFIG_BT_L2CAP_STREAM`。
    * :c:func:`bt_avrcp_get_cap`
    * 改进经典蓝牙免提单元，包括 :kconfig:option:`CONFIG_BT_HFP_HF_CODEC_NEG`、:kconfig:option:`CONFIG_BT_HFP_HF_ECNR`、:kconfig:option:`CONFIG_BT_HFP_HF_3WAY_CALL`、:kconfig:option:`CONFIG_BT_HFP_HF_ECS`、:kconfig:option:`CONFIG_BT_HFP_HF_ECC`、:kconfig:option:`CONFIG_BT_HFP_HF_VOICE_RECG_TEXT`、:kconfig:option:`CONFIG_BT_HFP_HF_ENH_VOICE_RECG`、:kconfig:option:`CONFIG_BT_HFP_HF_VOICE_RECG`、:kconfig:option:`CONFIG_BT_HFP_HF_HF_INDICATORS`、:kconfig:option:`CONFIG_BT_HFP_HF_HF_INDICATOR_ENH_SAFETY` 和 :kconfig:option:`CONFIG_BT_HFP_HF_HF_INDICATOR_BATTERY`。
    * 改进经典蓝牙免提音频网关，包括 :kconfig:option:`CONFIG_BT_HFP_AG_CODEC_NEG`、:kconfig:option:`CONFIG_BT_HFP_AG_ECNR`、:kconfig:option:`CONFIG_BT_HFP_AG_3WAY_CALL`、:kconfig:option:`CONFIG_BT_HFP_AG_ECS`、:kconfig:option:`CONFIG_BT_HFP_AG_ECC`、:kconfig:option:`CONFIG_BT_HFP_AG_VOICE_RECG_TEXT`、:kconfig:option:`CONFIG_BT_HFP_AG_ENH_VOICE_RECG`、:kconfig:option:`CONFIG_BT_HFP_AG_VOICE_TAG`、:kconfig:option:`CONFIG_BT_HFP_AG_HF_INDICATORS`、:kconfig:option:`CONFIG_BT_HFP_AG_HF_INDICATOR_ENH_SAFETY`、:kconfig:option:`CONFIG_BT_HFP_AG_HF_INDICATOR_BATTERY` 和 :kconfig:option:`CONFIG_BT_HFP_AG_REJECT_CALL`。
    * 为 :c:struct:`bt_hfp_ag_cb` 新增回调函数 ``get_ongoing_call()``。
    * :c:func:`bt_hfp_ag_ongoing_calls`
    * 支持经典蓝牙 L2CAP 信令回显请求和响应功能，涉及 :c:struct:`bt_l2cap_br_echo_cb`、:c:func:`bt_l2cap_br_echo_cb_register`、:c:func:`bt_l2cap_br_echo_cb_unregister`、:c:func:`bt_l2cap_br_echo_req` 和 :c:func:`bt_l2cap_br_echo_rsp`。
    * :c:func:`bt_a2dp_get_conn`
    * :c:func:`bt_rfcomm_send_rpn_cmd`

* 视频

  * :c:type:`video_api_ctrl_t`
  * :c:func:`video_query_ctrl`
  * :c:func:`video_print_ctrl`
  * :c:type:`video_api_selection_t`
  * :c:func:`video_set_selection`
  * :c:func:`video_get_selection`
  * :ref:`video-sw-generator <snippet-video-sw-generator>`
  * :c:func:`video_get_csi_link_freq`
  * :c:macro:`VIDEO_CID_LINK_FREQ`
  * :c:macro:`VIDEO_CID_AUTO_WHITE_BALANCE` 以及 BASE 控制类中的其他控制项。
  * :c:macro:`VIDEO_CID_EXPOSURE_ABSOLUTE` 以及 CAMERA 控制类中的其他控制项。
  * :c:macro:`VIDEO_PIX_FMT_Y10` 以及 ``Y12``、``Y14``、``Y16`` 变体
  * :c:macro:`VIDEO_PIX_FMT_SRGGB10P` 以及 ``12P``、``14P`` 变体，适用于全部 4 种 Bayer 变体。
  * :c:member:`video_buffer.index` 字段
  * :c:member:`video_ctrl_query.int_menu` 字段
  * :c:macro:`VIDEO_MIPI_CSI2_DT_NULL` 以及其他 MIPI 标准值

* 计数器

  * :c:func:`counter_reset`

* 调试

  * 核心转储

    * :kconfig:option:`CONFIG_DEBUG_COREDUMP_THREAD_STACK_TOP` 在 ARM Cortex M 上默认启用，前提是选择了 :kconfig:option:`CONFIG_DEBUG_COREDUMP_MEMORY_DUMP_MIN`。
    * :kconfig:option:`CONFIG_DEBUG_COREDUMP_BACKEND_IN_MEMORY`
    * :kconfig:option:`CONFIG_DEBUG_COREDUMP_BACKEND_IN_MEMORY_SIZE`

.. zephyr-keep-sorted-stop

.. _boards_added_in_zephyr_4_2:

新增开发板
**********

..
  You may update this list as you contribute a new board during the release cycle, in order to make
  it visible to people who might be looking at the working draft of the release notes. However, note
  that this list will be recomputed at the time of the release, so you don't *have* to update it.
  In any case, just link the board, further details go in the board description.

* Adafruit Industries, LLC

   * :zephyr:board:`adafruit_feather_esp32s2` (``adafruit_feather_esp32s2``)
   * :zephyr:board:`adafruit_feather_esp32s2_tft` (``adafruit_feather_esp32s2_tft``)
   * :zephyr:board:`adafruit_feather_esp32s2_tft_reverse` (``adafruit_feather_esp32s2_tft_reverse``)
   * :zephyr:board:`adafruit_feather_esp32s3` (``adafruit_feather_esp32s3``)
   * :zephyr:board:`adafruit_feather_esp32s3_tft` (``adafruit_feather_esp32s3_tft``)
   * :zephyr:board:`adafruit_feather_esp32s3_tft_reverse` (``adafruit_feather_esp32s3_tft_reverse``)

* Advanced Micro Devices (AMD), Inc.

   * :zephyr:board:`versal2_rpu` (``versal2_rpu``)
   * :zephyr:board:`versalnet_rpu` (``versalnet_rpu``)

* Aesc Silicon

   * :zephyr:board:`elemrv_flask_n` (``elemrv``)

* Ai-Thinker Co., Ltd.

   * :zephyr:board:`ai_wb2_12f_kit` (``ai_wb2_12f_kit``)

* Ambiq Micro, Inc.

   * :zephyr:board:`apollo510_evb` (``apollo510_evb``)

* Analog Devices, Inc.

   * :zephyr:board:`max32657evkit` (``max32657evkit``)

* Arduino

   * :zephyr:board:`arduino_nano_matter` (``arduino_nano_matter``)
   * :zephyr:board:`arduino_portenta_c33` (``arduino_portenta_c33``)

* ARM Ltd.

   * :zephyr:board:`mps4` (``mps4``)

* BeagleBoard.org Foundation

   * :zephyr:board:`pocketbeagle_2` (``pocketbeagle_2``)

* Blues Wireless

   * :zephyr:board:`cygnet` (``cygnet``)

* Bouffalo Lab (Nanjing) Co., Ltd.

   * :zephyr:board:`bl604e_iot_dvk` (``bl604e_iot_dvk``)

* Doctors of Intelligence & Technology

   * :zephyr:board:`dt_bl10_devkit` (``dt_bl10_devkit``)

* ENE Technology, Inc.

   * :zephyr:board:`kb1062_evb` (``kb1062_evb``)

* Espressif Systems

   * :zephyr:board:`esp32_devkitc` (``esp32_devkitc``)

* Ezurio

   * :zephyr:board:`bl54l15_dvk` (``bl54l15_dvk``)
   * ``bl54l15u_dvk``

* FANKE Technology Co., Ltd.

   * :zephyr:board:`fk743m5_xih6` (``fk743m5_xih6``)

* IAR Systems AB

   * :zephyr:board:`stm32f429ii_aca` (``stm32f429ii_aca``)

* Infineon Technologies

   * :zephyr:board:`kit_xmc72_evk` (``kit_xmc72_evk``)

* Intel Corporation

   * :zephyr:board:`intel_btl_s_crb` (``intel_btl_s_crb``)

* ITE Tech. Inc.

   * ``it515xx_evb``

* KWS Computersysteme Gmbh

   * :zephyr:board:`pico2_spe` (``pico2_spe``)
   * :zephyr:board:`pico_spe` (``pico_spe``)

* Lilygo Shenzhen Xinyuan Electronic Technology Co., Ltd

   * :zephyr:board:`tdongle_s3` (``tdongle_s3``)
   * :zephyr:board:`ttgo_tbeam` (``ttgo_tbeam``)
   * :zephyr:board:`ttgo_toiplus` (``ttgo_toiplus``)
   * :zephyr:board:`twatch_s3` (``twatch_s3``)

* M5Stack

   * :zephyr:board:`m5stack_fire` (``m5stack_fire``)

* Microchip Technology Inc.

   * :zephyr:board:`mec_assy6941` (``mec_assy6941``)
   * :zephyr:board:`sama7g54_ek` (``sama7g54_ek``)

* MikroElektronika d.o.o.

   * :zephyr:board:`mikroe_quail` (``mikroe_quail``)

* Nordic Semiconductor

   * :zephyr:board:`nrf54lm20dk` (``nrf54lm20dk``)

* Nuvoton Technology Corporation

   * :zephyr:board:`npck3m8k_evb` (``npck3m8k_evb``)
   * :zephyr:board:`numaker_m55m1` (``numaker_m55m1``)

* NXP Semiconductors

   * :zephyr:board:`frdm_mcxa153` (``frdm_mcxa153``)
   * :zephyr:board:`imx943_evk` (``imx943_evk``)
   * :zephyr:board:`mcx_n9xx_evk` (``mcx_n9xx_evk``)
   * :zephyr:board:`s32k148_evb` (``s32k148_evb``)

* Octavo Systems LLC

   * :zephyr:board:`osd32mp1_brk` (``osd32mp1_brk``)

* OpenHW Group

   * :zephyr:board:`cv32a6_genesys_2` (``cv32a6_genesys_2``)
   * :zephyr:board:`cv64a6_genesys_2` (``cv64a6_genesys_2``)

* Pimoroni Ltd.

   * :zephyr:board:`pico_plus2` (``pico_plus2``)

* QEMU

   * :zephyr:board:`qemu_rx` (``qemu_rx``)

* Raytac Corporation

   * :zephyr:board:`raytac_an54lq_db_15` (``raytac_an54lq_db_15``)
   * :zephyr:board:`raytac_an7002q_db` (``raytac_an7002q_db``)
   * :zephyr:board:`raytac_mdbt50q_cx_40_dongle` (``raytac_mdbt50q_cx_40_dongle``)

* Renesas Electronics Corporation

   * :zephyr:board:`ek_ra8p1` (``ek_ra8p1``)
   * :zephyr:board:`rsk_rx130` (``rsk_rx130``)
   * :zephyr:board:`rza2m_evk` (``rza2m_evk``)
   * :zephyr:board:`rza3ul_smarc` (``rza3ul_smarc``)
   * :zephyr:board:`rzg2l_smarc` (``rzg2l_smarc``)
   * :zephyr:board:`rzg2lc_smarc` (``rzg2lc_smarc``)
   * :zephyr:board:`rzg2ul_smarc` (``rzg2ul_smarc``)
   * :zephyr:board:`rzn2l_rsk` (``rzn2l_rsk``)
   * :zephyr:board:`rzt2l_rsk` (``rzt2l_rsk``)
   * :zephyr:board:`rzt2m_rsk` (``rzt2m_rsk``)
   * :zephyr:board:`rzv2h_evk` (``rzv2h_evk``)
   * :zephyr:board:`rzv2l_smarc` (``rzv2l_smarc``)
   * :zephyr:board:`rzv2n_evk` (``rzv2n_evk``)

* Seeed Technology Co., Ltd

   * :zephyr:board:`xiao_mg24` (``xiao_mg24``)
   * :zephyr:board:`xiao_ra4m1` (``xiao_ra4m1``)

* sensry.io

   * :zephyr:board:`ganymed_sk` (``ganymed_sk``)

* Shanghai Ruiside Electronic Technology Co., Ltd.

   * :zephyr:board:`art_pi2` (``art_pi2``)
   * :zephyr:board:`ra8d1_vision_board` (``ra8d1_vision_board``)

* Silicon Laboratories

   * :zephyr:board:`siwx917_rb4342a` (``siwx917_rb4342a``)
   * :zephyr:board:`slwrb4180b` (``slwrb4180b``)

* Space Cubics, LLC

   * :zephyr:board:`scobc_a1` (``scobc_a1``)

* STMicroelectronics

   * :zephyr:board:`nucleo_f439zi` (``nucleo_f439zi``)
   * :zephyr:board:`nucleo_u385rg_q` (``nucleo_u385rg_q``)
   * :zephyr:board:`nucleo_wba65ri` (``nucleo_wba65ri``)
   * :zephyr:board:`stm32h757i_eval` (``stm32h757i_eval``)
   * :zephyr:board:`stm32mp135f_dk` (``stm32mp135f_dk``)
   * :zephyr:board:`stm32mp257f_ev1` (``stm32mp257f_ev1``)
   * :zephyr:board:`stm32u5g9j_dk1` (``stm32u5g9j_dk1``)
   * :zephyr:board:`stm32u5g9j_dk2` (``stm32u5g9j_dk2``)

* Texas Instruments

   * :zephyr:board:`am243x_evm` (``am243x_evm``)
   * :zephyr:board:`lp_mspm0g3507` (``lp_mspm0g3507``)
   * :zephyr:board:`sk_am64` (``sk_am64``)

* u-blox

   * :zephyr:board:`ubx_evk_iris_w1` (``ubx_evk_iris_w1``)

* Variscite Ltd.

   * :zephyr:board:`imx8mp_var_dart` (``imx8mp_var_dart``)
   * :zephyr:board:`imx8mp_var_som` (``imx8mp_var_som``)
   * :zephyr:board:`imx93_var_dart` (``imx93_var_dart``)
   * :zephyr:board:`imx93_var_som` (``imx93_var_som``)

* Waveshare Electronics

   * :zephyr:board:`esp32s3_matrix` (``esp32s3_matrix``)
   * :zephyr:board:`rp2040_plus` (``rp2040_plus``)

* WeAct Studio

   * :zephyr:board:`bluepillplus_ch32v203` (``bluepillplus_ch32v203``)
   * :zephyr:board:`weact_stm32f446_core` (``weact_stm32f446_core``)

* WinChipHead

   * :zephyr:board:`ch32v003f4p6_dev_board` (``ch32v003f4p6_dev_board``)
   * :zephyr:board:`ch32v006evt` (``ch32v006evt``)
   * :zephyr:board:`ch32v303vct6_evt` (``ch32v303vct6_evt``)
   * :zephyr:board:`linkw` (``linkw``)

* WIZnet Co., Ltd.

   * :zephyr:board:`w5500_evb_pico2` (``w5500_evb_pico2``)

* Würth Elektronik GmbH.

   * :zephyr:board:`ophelia4ev` (``ophelia4ev``)

.. _shields_added_in_zephyr_4_2:

新增扩展板
==========

* :ref:`Arduino Giga Display Shield <arduino_giga_display_shield>`
* :ref:`Arduino Modulino Buttons <arduino_modulino_buttons>`
* :ref:`Arduino Modulino SmartLEDs <arduino_modulino_pixels>`
* :ref:`DVP 20-pin OV7670 <dvp_20pin_ov7670>`
* :ref:`EVAL AD4052 ARDZ <eval_ad4052_ardz>`
* :ref:`EVAL ADXL367 ARDZ <eval_adxl367_ardz>`
* :ref:`M5Stack Cardputer <m5stack_cardputer>`
* :ref:`MikroElektronika LTE IoT10 Click <mikroe_lte_iot10_click_shield>`
* :ref:`MikroElektronika Stepper 18 Click <mikroe_stepper_18_click_shield>`
* :ref:`MikroElektronika Stepper 19 Click <mikroe_stepper_19_click_shield>`
* :ref:`NPM2100 Evaluation Kit <npm2100_ek>`
* :ref:`NXP ADTJA1101 <nxp_adtja1101>`
* :ref:`NXP M2 WiFi BT <nxp_m2_wifi_bt>`
* :ref:`OpenThread RCP Arduino <openthread_rcp_arduino_shield>`
* :ref:`RTK7 EKA6M3B00001BU <rtk7eka6m3b00001bu>`
* :ref:`RTKLCDPAR1S00001BE Display <rtklcdpar1s00001be>`
* :ref:`ST B-CAMS-IMX-MB1854 <st_b_cams_imx_mb1854>`
* :ref:`ST MB1897 camera module <st_mb1897_cam>`
* :ref:`ST STM32F4DIS CAM <st_stm32f4dis_cam>`
* :ref:`Waveshare Pico LCD 1.14 <waveshare_pico_lcd_1_14>`
* :ref:`Waveshare Pico OLED 1.3 <waveshare_pico_oled_1_3>`
* :ref:`X-Nucleo-GFX01M2 <x_nucleo_gfx01m2_shield>`

新增驱动
********

..
  Same as above for boards, this will also be recomputed at the time of the release.
  Just link the driver, further details go in the binding description

* :abbr:`ADC（模数转换器）`

   * :dtcompatible:`adi,ad4050-adc`
   * :dtcompatible:`adi,ad4052-adc`
   * :dtcompatible:`adi,ad4130-adc`
   * :dtcompatible:`ene,kb106x-adc`
   * :dtcompatible:`ite,it51xxx-adc`
   * :dtcompatible:`microchip,mcp356xr`
   * :dtcompatible:`realtek,rts5912-adc`
   * :dtcompatible:`renesas,rz-adc`
   * :dtcompatible:`silabs,siwx91x-adc`
   * :dtcompatible:`ti,am335x-adc`
   * :dtcompatible:`ti,cc23x0-adc`
   * :dtcompatible:`wch,adc`

* 音频

   * :dtcompatible:`ambiq,pdm`
   * :dtcompatible:`maxim,max98091`
   * :dtcompatible:`ti,pcm1681`
   * :dtcompatible:`ti,tlv320aic3110`
   * :dtcompatible:`wolfson,wm8962`

* 辅助显示

   * :dtcompatible:`gpio-7-segment`

* :abbr:`CAN（控制器局域网）`

   * :dtcompatible:`adi,max32-can`
   * :dtcompatible:`renesas,rz-canfd`
   * :dtcompatible:`renesas,rz-canfd-global`

* 充电器

   * :dtcompatible:`ti,bq25713`
   * :dtcompatible:`x-powers,axp2101-charger`

* 时钟控制

   * :dtcompatible:`bflb,bclk`
   * :dtcompatible:`bflb,bl60x-clock-controller`
   * :dtcompatible:`bflb,bl60x-pll`
   * :dtcompatible:`bflb,bl60x-root-clk`
   * :dtcompatible:`bflb,clock-controller`
   * :dtcompatible:`ite,it51xxx-ecpm`
   * :dtcompatible:`microchip,sam-pmc`
   * :dtcompatible:`microchip,sama7g5-sckc`
   * :dtcompatible:`nordic,nrf51-hfxo`
   * :dtcompatible:`nordic,nrf52-hfxo`
   * :dtcompatible:`nordic,nrf54l-hfxo`
   * :dtcompatible:`nordic,nrfs-audiopll`
   * :dtcompatible:`renesas,rx-cgc-pclk`
   * :dtcompatible:`renesas,rx-cgc-pclk-block`
   * :dtcompatible:`renesas,rx-cgc-pll`
   * :dtcompatible:`renesas,rx-cgc-root-clock`
   * :dtcompatible:`renesas,rza2m-cpg`
   * :dtcompatible:`st,stm32mp13-cpu-clock-mux`
   * :dtcompatible:`st,stm32mp13-pll-clock`
   * :dtcompatible:`st,stm32mp2-rcc`
   * :dtcompatible:`st,stm32u3-msi-clock`
   * :dtcompatible:`ti,mspm0-clk`
   * :dtcompatible:`ti,mspm0-osc`
   * :dtcompatible:`ti,mspm0-pll`
   * :dtcompatible:`wch,ch32v20x_30x-pll-clock`

* 比较器

   * :dtcompatible:`ite,it51xxx-vcmp`
   * :dtcompatible:`renesas,ra-acmphs`
   * :dtcompatible:`renesas,ra-acmphs-global`

* 计数器

   * :dtcompatible:`adi,max32-wut`
   * :dtcompatible:`espressif,esp32-counter`
   * :dtcompatible:`ite,it51xxx-counter`
   * :dtcompatible:`ite,it8xxx2-counter`
   * :dtcompatible:`neorv32,gptmr`
   * :dtcompatible:`realtek,rts5912-timer`
   * :dtcompatible:`ti,cc23x0-lgpt`
   * :dtcompatible:`ti,cc23x0-rtc`
   * :dtcompatible:`ti,mspm0-timer-counter`
   * :dtcompatible:`wch,gptm`
   * :dtcompatible:`zephyr,native-sim-counter`

* CPU

   * :dtcompatible:`arm,cortex-r8`
   * :dtcompatible:`intel,bartlett-lake`
   * :dtcompatible:`openhwgroup,cva6`
   * :dtcompatible:`renesas,rx`
   * :dtcompatible:`wch,qingke-v4b`
   * :dtcompatible:`wch,qingke-v4c`
   * :dtcompatible:`wch,qingke-v4f`
   * :dtcompatible:`zephyr,native-sim-cpu`

* 加密加速器

   * :dtcompatible:`ite,it51xxx-sha`
   * :dtcompatible:`realtek,rts5912-sha`
   * :dtcompatible:`ti,cc23x0-aes`

* :abbr:`DAC（数模转换器）`

   * :dtcompatible:`nxp,dac12`
   * :dtcompatible:`ti,dac161s997`

* 调试

   * :dtcompatible:`silabs,pti`

* 显示

   * :dtcompatible:`sinowealth,sh1122`
   * :dtcompatible:`sitronix,st75256`
   * :dtcompatible:`sitronix,st7567`
   * :dtcompatible:`sitronix,st7701`
   * :dtcompatible:`solomon,ssd1320`
   * :dtcompatible:`solomon,ssd1327fb`
   * :dtcompatible:`solomon,ssd1331`
   * :dtcompatible:`solomon,ssd1351`
   * :dtcompatible:`solomon,ssd1363`
   * :dtcompatible:`zephyr,displays`

* :abbr:`DMA（直接内存访问）`

   * :dtcompatible:`renesas,rz-dma`
   * :dtcompatible:`ti,cc23x0-dma`
   * :dtcompatible:`wch,wch-dma`

* :abbr:`EDAC（错误检测与纠正）`

   * :dtcompatible:`xlnx,zynqmp-ddrc-2.40a`

* :abbr:`eSPI（增强型串行外设接口）`

   * :dtcompatible:`realtek,rts5912-espi`

* 以太网

   * :dtcompatible:`ethernet-phy`
   * :dtcompatible:`microchip,vsc8541`
   * :dtcompatible:`nxp,netc-ptp-clock`
   * :dtcompatible:`nxp,tja11xx`
   * 引入了 :dtcompatible:`st,stm32-ethernet-controller`，以简化与 :dtcompatible:`st,stm32-mdio` 的互操作。
   * :dtcompatible:`st,stm32n6-ethernet`
   * :dtcompatible:`ti,dp83867`
   * :dtcompatible:`xlnx,axi-ethernet-1.00.a`

* 固件

   * :dtcompatible:`nxp,scmi-cpu`
   * :dtcompatible:`ti,k2g-sci`

* Flash 控制器

   * :dtcompatible:`realtek,rts5912-flash-controller`
   * :dtcompatible:`renesas,ra-ospi-b-nor`
   * :dtcompatible:`renesas,rx-flash`
   * :dtcompatible:`silabs,series2-flash-controller`
   * :dtcompatible:`st,stm32u3-flash-controller`

* 文件系统

   * :dtcompatible:`zephyr,fstab,fatfs`

* 电量计

   * :dtcompatible:`onnn,lc709203f`
   * :dtcompatible:`x-powers,axp2101-fuel-gauge`

* :abbr:`GNSS（全球导航卫星系统）`

   * :dtcompatible:`u-blox,f9p`

* :abbr:`GPIO（通用输入/输出）`

   * :dtcompatible:`adi,max14915-gpio`
   * :dtcompatible:`adi,max14917-gpio`
   * :dtcompatible:`adi,max22199-gpio`
   * :dtcompatible:`arducam,dvp-20pin-connector`
   * :dtcompatible:`bflb,gpio`
   * :dtcompatible:`ene,kb106x-gpio`
   * :dtcompatible:`espressif,esp32-lpgpio`
   * :dtcompatible:`ite,it51xxx-gpio`
   * :dtcompatible:`nordic,npm1304-gpio`
   * :dtcompatible:`nxp,lcd-pmod`
   * :dtcompatible:`raspberrypi,csi-connector`
   * :dtcompatible:`raspberrypi,pico-gpio-port`
   * :dtcompatible:`renesas,ra-parallel-graphics-header`
   * :dtcompatible:`renesas,rx-gpio`
   * :dtcompatible:`renesas,rza2m-gpio`
   * :dtcompatible:`renesas,rza2m-gpio-int`
   * :dtcompatible:`st,stm32mp2-gpio`
   * :dtcompatible:`ti,mspm0-gpio`

* IEEE 802.15.4 HDLC RCP 接口

   * :dtcompatible:`spi,hdlc-rcp-if`

* :abbr:`I2C（集成电路间总线）`

   * :dtcompatible:`cdns,i2c`
   * :dtcompatible:`ite,it51xxx-i2c`
   * :dtcompatible:`litex,litei2c`
   * :dtcompatible:`realtek,rts5912-i2c`
   * :dtcompatible:`renesas,ra-i2c-sci-b`
   * :dtcompatible:`renesas,rx-i2c`
   * :dtcompatible:`renesas,rz-riic`
   * :dtcompatible:`sensry,sy1xx-i2c`
   * :dtcompatible:`wch,i2c`

* :abbr:`I2S（集成电路间音频）`

   * :dtcompatible:`ambiq,i2s`
   * :dtcompatible:`nordic,nrf-tdm`
   * :dtcompatible:`renesas,ra-i2s-ssie`
   * :dtcompatible:`silabs,siwx91x-i2s`
   * :dtcompatible:`st,stm32-sai`

* :abbr:`I3C（改进型集成电路间总线）`

   * :dtcompatible:`ite,it51xxx-i3cm`
   * :dtcompatible:`ite,it51xxx-i3cs`
   * :dtcompatible:`renesas,ra-i3c`

* IEEE 802.15.4

   * :dtcompatible:`espressif,esp32-ieee802154`

* 输入

   * :dtcompatible:`arduino,modulino-buttons`
   * :dtcompatible:`ite,it51xxx-kbd`
   * :dtcompatible:`realtek,rts5912-kbd`
   * :dtcompatible:`st,stm32-tsc`
   * :dtcompatible:`tsc-keys`
   * :dtcompatible:`vishay,vs1838b`

* 中断控制器

   * :dtcompatible:`ite,it51xxx-intc`
   * :dtcompatible:`ite,it51xxx-wuc`
   * :dtcompatible:`ite,it51xxx-wuc-map`
   * :dtcompatible:`renesas,rx-icu`
   * :dtcompatible:`riscv,clic`
   * :dtcompatible:`wch,exti`

* :abbr:`LED（发光二极管）`

   * :dtcompatible:`arduino,modulino-buttons-leds`
   * :dtcompatible:`dac-leds`
   * :dtcompatible:`nordic,npm1304-led`
   * :dtcompatible:`x-powers,axp192-led`
   * :dtcompatible:`x-powers,axp2101-led`

* :abbr:`LED（发光二极管）` 灯带

   * :dtcompatible:`arduino,modulino-smartleds`

* 邮箱

   * :dtcompatible:`arm,mhuv3`
   * :dtcompatible:`renesas,rz-mhu-mbox`
   * :dtcompatible:`ti,secure-proxy`

* :abbr:`MDIO（管理数据输入/输出）`

   * :dtcompatible:`xlnx,axi-ethernet-1.00.a-mdio`

* 内存控制器

   * :dtcompatible:`adi,max32-hpb`
   * :dtcompatible:`realtek,rts5912-bbram`
   * :dtcompatible:`silabs,siwx91x-qspi-memory`
   * :dtcompatible:`st,stm32-xspi-psram`

* :abbr:`MFD（多功能设备）`

   * :dtcompatible:`adi,maxq10xx`
   * :dtcompatible:`ambiq,iom`
   * :dtcompatible:`microchip,sam-flexcom`
   * :dtcompatible:`nordic,npm1304`
   * :dtcompatible:`x-powers,axp2101`

* :abbr:`MIPI DBI（移动产业处理器接口显示总线接口）`

   * :dtcompatible:`nxp,mipi-dbi-dcnano-lcdif`

* 其他

   * :dtcompatible:`ene,kb106x-gcfg`
   * :dtcompatible:`nordic,ironside-call`
   * :dtcompatible:`nordic,nrf-mpc`
   * :dtcompatible:`nxp,rtxxx-dsp-ctrl`
   * :dtcompatible:`renesas,ra-elc`
   * :dtcompatible:`renesas,ra-ulpt`
   * :dtcompatible:`renesas,rx-external-interrupt`
   * :dtcompatible:`renesas,rx-mtu`
   * :dtcompatible:`renesas,rx-sci`
   * :dtcompatible:`renesas,rz-sci`
   * :dtcompatible:`renesas,rz-sci-b`
   * :dtcompatible:`st,stm32n6-ramcfg`

* 调制解调器

   * :dtcompatible:`quectel,eg800q`
   * :dtcompatible:`simcom,a76xx`

* 多比特 SPI

   * :dtcompatible:`nordic,nrf-exmif`
   * :dtcompatible:`snps,designware-ssi`

* :abbr:`MTD（存储器技术设备）`

   * :dtcompatible:`fixed-subpartitions`
   * :dtcompatible:`jedec,mspi-nor`
   * :dtcompatible:`mspi-aps-z8`
   * :dtcompatible:`mspi-is25xX0xx`
   * :dtcompatible:`renesas,ra-nv-code-flash`
   * :dtcompatible:`renesas,ra-nv-data-flash`
   * :dtcompatible:`renesas,rx-nv-flash`
   * :dtcompatible:`ti,tmp11x-eeprom`

* 网络

   * :dtcompatible:`nordic,nrf-nfct-v2`
   * :dtcompatible:`silabs,siwx91x-nwp`

* 八线 SPI

   * :dtcompatible:`renesas,ra-ospi-b`

* 引脚控制

   * :dtcompatible:`ambiq,apollo5-pinctrl`
   * :dtcompatible:`arm,mps2-pinctrl`
   * :dtcompatible:`arm,mps3-pinctrl`
   * :dtcompatible:`arm,mps4-pinctrl`
   * :dtcompatible:`arm,v2m_beetle-pinctrl`
   * :dtcompatible:`bflb,pinctrl`
   * :dtcompatible:`ene,kb106x-pinctrl`
   * :dtcompatible:`microchip,sama7g5-pinctrl`
   * :dtcompatible:`nuvoton,npcx-pinctrl-npckn`
   * :dtcompatible:`renesas,rx-pinctrl`
   * :dtcompatible:`renesas,rx-pinmux`
   * :dtcompatible:`renesas,rza-pinctrl`
   * :dtcompatible:`renesas,rza2m-pinctrl`
   * :dtcompatible:`renesas,rzn-pinctrl`
   * :dtcompatible:`renesas,rzt-pinctrl`
   * :dtcompatible:`renesas,rzv-pinctrl`
   * :dtcompatible:`st,stm32n6-pinctrl`
   * :dtcompatible:`ti,mspm0-pinctrl`
   * :dtcompatible:`wch,00x-afio`
   * :dtcompatible:`wch,20x_30x-afio`

* 电源管理

   * :dtcompatible:`infineon,cat1b-power`
   * :dtcompatible:`realtek,rts5912-ulpm`

* 电源域

   * :dtcompatible:`ti,sci-pm-domain`

* :abbr:`PSI5（外设传感器接口第 5 代）`

   * :dtcompatible:`nxp,s32-psi5`

* :abbr:`PWM（脉宽调制）`

   * :dtcompatible:`arduino-header-pwm`
   * :dtcompatible:`ene,kb106x-pwm`
   * :dtcompatible:`ite,it51xxx-pwm`
   * :dtcompatible:`neorv32,pwm`
   * :dtcompatible:`realtek,rts5912-pwm`
   * :dtcompatible:`renesas,rx-mtu-pwm`
   * :dtcompatible:`silabs,letimer-pwm`
   * :dtcompatible:`silabs,siwx91x-pwm`
   * :dtcompatible:`silabs,timer-pwm`
   * :dtcompatible:`ti,mspm0-timer-pwm`
   * :dtcompatible:`wch,gptm-pwm`

* 稳压器

   * :dtcompatible:`nordic,npm1304-regulator`
   * :dtcompatible:`x-powers,axp2101-regulator`

* 复位控制器

   * :dtcompatible:`microchip,mpfs-reset`
   * :dtcompatible:`reset-mmio`

* :abbr:`RNG（随机数发生器）`

   * :dtcompatible:`adi,maxq10xx-trng`
   * :dtcompatible:`brcm,iproc-rng200`
   * :dtcompatible:`virtio,device4`
   * :dtcompatible:`zephyr,native-sim-rng`

* :abbr:`RTC（实时时钟）`

   * :dtcompatible:`nxp,pcf2123`
   * :dtcompatible:`realtek,rts5912-rtc`
   * :dtcompatible:`silabs,siwx91x-rtc`

* :abbr:`SDHC（安全数字主机控制器）`

   * :dtcompatible:`ambiq,sdio`
   * :dtcompatible:`xlnx,versal-8.9a`

* 传感器

   * :dtcompatible:`adi,ad2s1210`
   * :dtcompatible:`bosch,bmm350`
   * :dtcompatible:`brcm,afbr-s50`
   * :dtcompatible:`everlight,als-pt19`
   * :dtcompatible:`invensense,icm40627`
   * :dtcompatible:`invensense,icm45686`
   * :dtcompatible:`invensense,icp201xx`
   * :dtcompatible:`liteon,ltr329`
   * :dtcompatible:`meas,ms5837-02ba`
   * :dtcompatible:`meas,ms5837-30ba`
   * :dtcompatible:`nordic,npm1304-charger`
   * :dtcompatible:`nxp,lpadc-temp40`
   * :dtcompatible:`nxp,tpm-qdec`
   * :dtcompatible:`peacefair,pzem004t`
   * :dtcompatible:`pixart,paa3905`
   * :dtcompatible:`pixart,paj7620`
   * :dtcompatible:`pixart,pat9136`
   * :dtcompatible:`pni,rm3100`
   * :dtcompatible:`rohm,bh1730`
   * :dtcompatible:`rohm,bh1790`
   * :dtcompatible:`st,lsm6dsv32x`
   * :dtcompatible:`st,lsm9ds1_mag`
   * :dtcompatible:`ti,tmp11x`
   * :dtcompatible:`vishay,veml6031`
   * :dtcompatible:`we,wsen-itds-2533020201601`

* :abbr:`SENT（单边半字节传输）`

   * :dtcompatible:`nxp,s32-sent`

* 串行控制器

   * :dtcompatible:`aesc,uart`
   * :dtcompatible:`ambiq,pl011-uart`
   * :dtcompatible:`bflb,uart`
   * :dtcompatible:`ene,kb106x-uart`
   * :dtcompatible:`espressif,esp32-lpuart`
   * :dtcompatible:`ite,it51xxx-uart`
   * :dtcompatible:`nuvoton,npcx-uart-npckn`
   * :dtcompatible:`renesas,rx-uart-sci`
   * :dtcompatible:`renesas,rx-uart-sci-qemu`
   * :dtcompatible:`renesas,rz-sci-b-uart`
   * :dtcompatible:`renesas,rz-sci-uart`
   * :dtcompatible:`renesas,rza2m-scif-uart`
   * :dtcompatible:`ti,mspm0-uart`
   * :dtcompatible:`zephyr,native-pty-uart`
   * :dtcompatible:`zephyr,uart-bridge`

* :abbr:`SPI（串行外设接口）`

   * :dtcompatible:`cdns,spi`
   * :dtcompatible:`ite,it51xxx-spi`
   * :dtcompatible:`microchip,mec5-qspi`
   * :dtcompatible:`renesas,rx-rspi`
   * :dtcompatible:`renesas,rz-rspi`
   * :dtcompatible:`silabs,gspi`
   * :dtcompatible:`ti,cc23x0-spi`
   * :dtcompatible:`wch,spi`

* 步进电机

   * :dtcompatible:`adi,tmc51xx`
   * :dtcompatible:`allegro,a4979`

* 系统控制器

   * :dtcompatible:`bflb,efuse`

* 转速计

   * :dtcompatible:`ite,it51xxx-tach`
   * :dtcompatible:`realtek,rts5912-tach`

* :abbr:`TCPC（USB Type-C 端口控制器）`

   * :dtcompatible:`onnn,fusb307-tcpc`

* 定时器

   * :dtcompatible:`infineon,cat1-lp-timer`
   * :dtcompatible:`ite,it51xxx-timer`
   * :dtcompatible:`microchip,sam-pit64b`
   * :dtcompatible:`renesas,ra-ulpt-timer`
   * :dtcompatible:`renesas,rx-timer-cmt`
   * :dtcompatible:`renesas,rx-timer-cmt-start-control`
   * :dtcompatible:`renesas,rz-gtm-os-timer`
   * :dtcompatible:`renesas,rza2m-ostm`
   * :dtcompatible:`silabs,series2-letimer`
   * :dtcompatible:`silabs,series2-timer`
   * :dtcompatible:`ti,mspm0-timer`

* USB

   * :dtcompatible:`adi,max32-usbhs`
   * :dtcompatible:`nxp,uhc-ehci`
   * :dtcompatible:`nxp,uhc-ip3516hs`
   * :dtcompatible:`nxp,uhc-khci`
   * :dtcompatible:`nxp,uhc-ohci`
   * :dtcompatible:`st,stm32n6-otghs`
   * :dtcompatible:`zephyr,uvc-device`

* 视频

   * :dtcompatible:`ovti,ov9655`
   * :dtcompatible:`sony,imx335`
   * :dtcompatible:`st,mipid02`
   * :dtcompatible:`st,stm32-dcmipp`
   * :dtcompatible:`zephyr,video-sw-generator`

* Virtio

   * :dtcompatible:`virtio,mmio`
   * :dtcompatible:`virtio,pci`

* 看门狗

   * :dtcompatible:`ene,kb106x-watchdog`
   * :dtcompatible:`ite,it51xxx-watchdog`
   * :dtcompatible:`nordic,npm1304-wdt`
   * :dtcompatible:`nxp,ewm`
   * :dtcompatible:`realtek,rts5912-watchdog`
   * :dtcompatible:`renesas,ra-wdt`
   * :dtcompatible:`silabs,siwx91x-wdt`
   * :dtcompatible:`ti,cc23x0-wdt`
   * :dtcompatible:`wch,iwdg`

* Wi-Fi

   * :dtcompatible:`espressif,esp-hosted`

新增示例
********

..
  Same as above for boards and drivers, this will also be recomputed at the time of the release.
 Just link the sample, further details go in the sample documentation itself.

* :zephyr:code-sample:`amp_audio_loopback`
* :zephyr:code-sample:`amp_audio_output`
* :zephyr:code-sample:`amp_blinky`
* :zephyr:code-sample:`amp_mbox`
* :zephyr:code-sample:`auxdisplay_digits`
* :zephyr:code-sample:`bmg160`
* :zephyr:code-sample:`debug-ulp`
* :zephyr:code-sample:`distance_polling`
* :zephyr:code-sample:`echo-ulp`
* :zephyr:code-sample:`fatfs-fstab`
* :zephyr:code-sample:`fuel_gauge`
* :zephyr:code-sample:`heart_rate`
* :zephyr:code-sample:`interrupt-ulp`
* :zephyr:code-sample:`light_sensor_polling`
* :zephyr:code-sample:`lvgl-multi-display`
* :zephyr:code-sample:`min-heap`
* :zephyr:code-sample:`mspi-timing-scan`
* :zephyr:code-sample:`net-pkt-filter`
* :zephyr:code-sample:`nrf_ironside_update`
* :zephyr:code-sample:`paj7620_gesture`
* :zephyr:code-sample:`pressure_interrupt`
* :zephyr:code-sample:`pressure_polling`
* :zephyr:code-sample:`psi5`
* :zephyr:code-sample:`renesas-elc`
* :zephyr:code-sample:`renesas_comparator`
* :zephyr:code-sample:`rz-openamp-linux-zephyr`
* :zephyr:code-sample:`sent`
* :zephyr:code-sample:`spis-wakeup`
* :zephyr:code-sample:`stepper`
* :zephyr:code-sample:`stream_drdy`
* :zephyr:code-sample:`uart_async`
* :zephyr:code-sample:`usb-cdc-acm-bridge`
* :zephyr:code-sample:`uuid`
* :zephyr:code-sample:`uvc`
* :zephyr:code-sample:`veml6031`

其他值得注意的变更
******************

..
  Any more descriptive subsystem or driver changes. Do you really want to write
  a paragraph or is it enough to link to the api/driver/Kconfig/board page above?

* 新增对 Armv8.1-M MPU 的 PXN（Privileged Execute Never）属性的支持。因此，使用 ``CONFIG_ARM_MPU_PXN`` 和 ``CONFIG_USERSPACE`` 编译时，``__ramfunc`` 和 ``__ram_text_reloc`` 的 MPU 属性会被修改，以便为这些区域设置 PXN 属性。这会改变从这些区域执行代码的行为：如果这些区域设置了 PXN 属性，则无法在特权模式下执行。

* 移除了对 Nucleo WBA52CG 开发板（``nucleo_wba52cg``）的支持，因为它属于 NRND（Not Recommended for New Design，不建议用于新设计），并且从 STM32CubeWBA 1.1.0 版本（2023 年 7 月）起不再受支持。建议改用 :zephyr:board:`nucleo_wba55cg` 开发板（``nucleo_wba55cg``）。

* 将 Mbed TLS 更新到 3.6.4 版本（从 3.6.2 更新）。3.6.3 和 3.6.4 的版本说明如下：

  * 3.6.3: https://github.com/Mbed-TLS/mbedtls/releases/tag/mbedtls-3.6.3
  * 3.6.4: https://github.com/Mbed-TLS/mbedtls/releases/tag/mbedtls-3.6.4

* 将 TF-M 更新到 2.2.0 版本（从 2.1.1 更新）。版本说明见：https://trustedfirmware-m.readthedocs.io/en/latest/releases/2.2.0.html

* 更新了所有带有外部 I2C 连接器（Qwiic、Stemma、Grove...）的开发板，使其使用 ``zephyr_i2c`` 设备树标签。这样便可利用现有的 :ref:`shields` 构建系统特性（``west build --shield``），将任何带连接器的 i2c 模块接入任何具有兼容 i2c 端口的开发板，而不受具体 i2c 连接器品牌的限制。

* 撤销了 Nordic UART 驱动中接收器选项的弃用。此前，使用额外 TIMER 外设计数接收字节的接收模式已被弃用（例如 :kconfig:option:`CONFIG_CONFIG_UART_0_NRF_HW_ASYNC`）。然而事实证明，该模式是唯一能够在没有硬件流控的情况下可靠接收数据的方式，因此应保留在驱动中。
