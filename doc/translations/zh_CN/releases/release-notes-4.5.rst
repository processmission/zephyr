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

.. _zephyr_4.5:

Zephyr 4.5.0（工作草案）
########################

我们很高兴地宣布 Zephyr 4.5.0 版本正式发布。

本次发布的主要增强包括：

**Infineon TriCore 支持**
  Zephyr 现在支持 :zephyr:board-catalog:`Infineon TriCore 架构 <#arch=tricore>`。

**新增驱动类别**

  Zephyr 4.5 新增多项新的驱动 API，包括：

  - :ref:`时钟监视器 <clock_monitor_api>`，用于在运行时观测时钟频率

**新增子系统**

  Zephyr 4.5 新增多项新的子系统 API，包括：

  - :ref:`视频 <video_api>`，用于控制视频驱动

将应用从 Zephyr v4.4.0 迁移到 Zephyr v4.5.0 时需要或建议采取的变更概览，见单独的 :ref:`迁移指南 <migration_4.5>`。

以下小节按组件详细列出各项变更。

安全漏洞相关
************

本次发布修复了以下 CVE：

* :cve:`2026-8718` 在 2026-08-08 前处于禁运期

* :cve:`2026-9263` 在 2026-06-28 前处于禁运期

API 变更
********

..
  Only removed, deprecated and new APIs. Changes go in migration guide.

移除的 API 和选项
=================

* 架构

   * ARM

      * ``CONFIG_PLATFORM_SPECIFIC_INIT``
      * ``z_arm_platform_init()``

   * RISC-V

      * ``CONFIG_EXTRA_EXCEPTION_INFO``

   * x86

      * ``CONFIG_SSE``
      * ``CONFIG_SSE_FP_MATH``

   * Xtensa

      * ``CONFIG_XTENSA_BACKTRACE_EXCEPTION_DUMP_HOOK``

* 蓝牙

  * 控制器

    * ``CONFIG_BT_CTRL_ADV_ADI_IN_SCAN_RSP``

  * 主机

    * ``CONFIG_BT_RECV_CONTEXT`` Kconfig 选择项及其选项 ``CONFIG_BT_RECV_WORKQ_SYS`` 和 ``CONFIG_BT_RECV_WORKQ_BT`` 已被移除。主机现在始终在专用的蓝牙 RX 工作队列上处理低优先级 HCI 数据包（即原先 ``CONFIG_BT_RECV_WORKQ_BT`` 的行为）。参见迁移指南。

    * 部分主机工作项已从系统工作队列移至专用的蓝牙 RX 工作队列。由这些工作项触发的应用回调现在运行在蓝牙 RX 线程中。受影响的回调系列参见迁移指南。

    * ``CONFIG_BT_HCI_RAW_H4`` 和 ``CONFIG_BT_HCI_RAW_H4_ENABLE`` 这两个 Kconfig 选项已被移除。自 Zephyr 4.2 起，HCI raw 层已改为对所有缓冲区无条件使用 H:4 数据包编码，因此这两个选项一直不起任何作用。仍然设置这些选项的应用可以直接删除它们。

    * ``CONFIG_BT_AUTO_PHY_UPDATE``，已由 ``BT_AUTO_PHY_CENTRAL`` 和 ``BT_AUTO_PHY_PERIPHERAL`` 选项取代
    * ``_bt_gatt_ccc``
    * ``BT_GATT_CCC_INITIALIZER``
    * ``CONFIG_BT_CONN_TX_MAX``
    * ``CONFIG_BT_FIXED_PASSKEY``
    * ``bt_passkey_set()``
    * ``BT_PASSKEY_INVALID``

  * Mesh

    * ``CONFIG_BT_MESH_BLOB_IO_FLASH_WITH_ERASE``
    * ``CONFIG_BT_MESH_BLOB_IO_FLASH_WITHOUT_ERASE``

  * 服务

    * ``CONFIG_BT_DIS_MANUF``
    * ``CONFIG_BT_DIS_MODEL``

* 开发板

    * 移除了以下已弃用的开发板别名：

      * ``arduino_uno_r4_minima``
      * ``arduino_uno_r4_wifi``
      * ``esp32c6_devkitc``
      * ``esp32_devkitc_wroom/esp32/procpu``
      * ``esp32_devkitc_wroom/esp32/appcpu``
      * ``esp32_devkitc_wrover/esp32/procpu``
      * ``esp32_devkitc_wrover/esp32/appcpu``
      * ``neorv32``
      * ``panb511evb``
      * ``raytac_an54l15q_db/nrf54l15/cpuapp``
      * ``scobc_module1``
      * ``xiao_esp32c6``

    * 以下开发板已被弃用并重命名：

      * ``adafruit_metro_rp2350/rp2350b/m33`` 重命名为 ``adafruit_metro_rp2350/rp2350b/m33_0``
      * ``motion_2350_pro/rp2350a/m33`` 重命名为 ``motion_2350_pro/rp2350a/m33_0``
      * ``motion_2350_pro/rp2350a/hazard3`` 重命名为 ``motion_2350_pro/rp2350a/hazard3_0``
      * ``beetle_rp2350/rp2350a/m33`` 重命名为 ``beetle_rp2350/rp2350a/m33_0``
      * ``beetle_rp2350/rp2350a/hazard3`` 重命名为 ``beetle_rp2350/rp2350a/hazard3_0``
      * ``pico2_spe/rp2350a/m33`` 重命名为 ``pico2_spe/rp2350a/m33_0``
      * ``pico_plus2/rp2350b/m33`` 重命名为 ``pico_plus2/rp2350b/m33_0``
      * ``pico_plus2/rp2350b/hazard3`` 重命名为 ``pico_plus2/rp2350b/hazard3_0``
      * ``rpi_pico2/rp2350a/m33`` 重命名为 ``rpi_pico2/rp2350a/m33_0``
      * ``rpi_pico2/rp2350a/m33/w`` 重命名为 ``rpi_pico2/rp2350a/m33_0/w``
      * ``rpi_pico2/rp2350a/m33/mcuboot`` 重命名为 ``rpi_pico2/rp2350a/m33_0/mcuboot``
      * ``rpi_pico2/rp2350a/m33/w/mcuboot`` 重命名为 ``rpi_pico2/rp2350a/m33_0/w/mcuboot``
      * ``rpi_pico2/rp2350a/hazard3`` 重命名为 ``rpi_pico2/rp2350a/hazard3_0``
      * ``xiao_rp2350/rp2350a/m33`` 重命名为 ``xiao_rp2350/rp2350a/m33_0``
      * ``xiao_rp2350/rp2350a/hazard3`` 重命名为 ``xiao_rp2350/rp2350a/hazard3_0``
      * ``rp2350_zero/rp2350a/m33`` 重命名为 ``rp2350_zero/rp2350a/m33_0``
      * ``rp2350_zero/rp2350a/hazard3`` 重命名为 ``rp2350_zero/rp2350a/hazard3_0``
      * ``rp2350b_core/rp2350b/m33`` 重命名为 ``rp2350b_core/rp2350b/m33_0``
      * ``rp2350b_core/rp2350b/hazard3`` 重命名为 ``rp2350b_core/rp2350b/hazard3_0``
      * ``w5500_evb_pico2/rp2350a/m33`` 重命名为 ``w5500_evb_pico2/rp2350a/m33_0``
      * ``w6100_evb_pico2/rp2350a/m33`` 重命名为 ``w6100_evb_pico2/rp2350a/m33_0``
      * ``w6300_evb_pico2/rp2350a/m33`` 重命名为 ``w6300_evb_pico2/rp2350a/m33_0``

* 构建系统

    * ``CONFIG_BUILD_NO_GAP_FILL``
    * ``cmake/app/boilerplate.cmake``
    * 名为 ``<board>_<revision>.conf`` 的开发板版本 Kconfig 片段，已替换为 ``<board>_<revision>_defconfig``
    * ``zephyr_code_relocate(FILES ...)`` 中的模式展开，已替换为 ``file(GLOB ...)``
    * CMake 的 ``flash``、``debug``、``debugserver``、``attach`` 和 ``rtt`` 目标，已替换为对应的 ``west`` 命令
    * ``WEST_DIR`` 构建系统变量
    * ``ZephyrUnittest`` CMake 包，已替换为 ``find_package(Zephyr COMPONENTS unittest)``

* CAN

    * ``bus-speed``
    * ``bus-speed-data``

* 比较器

    * :dtcompatible:`nxp,kinetis-acmp` 的 ``nxp,enable-output-pin``、``nxp,use-unfiltered-output``、``nxp,high-speed-mode``、``nxp,enable-sample``、``nxp,filter-count``、``nxp,filter-period`` 和 ``nxp,window-mode`` 属性

* 计数器

    * ``CONFIG_COUNTER_MAXIM_DS3231``
    * :dtcompatible:`nxp,lptmr` 的 ``prescaler`` 属性

* hawkBit

    * ``<zephyr/mgmt/hawkbit.h>``

* 设备树

    * ``zephyr,memory-region-mpu``

* 以太网

    * 使用 ``CONFIG_ETH_NUMAKER`` 的 NuMaker 以太网驱动已被 :kconfig:option:`CONFIG_ETH_NUMAKER_DWC_ETHER_1000` 取代。参见迁移指南。

* LLEXT

    * ``llext_get_fn_table``，已替换为 ``llext_get_fn_table_entry``

* Mbed TLS

    * ``CONFIG_MBEDTLS_MD``
    * ``CONFIG_MBEDTLS_LMS``
    * ``CONFIG_MBEDTLS_TLS_VERSION_1_2``
    * ``CONFIG_MBEDTLS_DTLS``
    * ``CONFIG_MBEDTLS_TLS_VERSION_1_3``
    * ``CONFIG_MBEDTLS_TLS_SESSION_TICKETS``
    * ``CONFIG_MBEDTLS_CTR_DRBG_ENABLED``
    * ``CONFIG_MBEDTLS_HMAC_DRBG_ENABLED``

* MCUboot

    * ``CONFIG_MCUBOOT_BOOTLOADER_MODE_SWAP_WITHOUT_SCRATCH``，已替换为 :kconfig:option:`CONFIG_MCUBOOT_BOOTLOADER_MODE_SWAP_USING_MOVE`

* MCUmgr

    * ``CONFIG_MCUMGR_GRP_OS_INFO_HARDWARE_INFO_SHORT_HARDWARE_PLATFORM``

* 网络

    * ``CONFIG_NET_TC_SKIP_FOR_HIGH_PRIO``
    * ``CONFIG_NET_SOCKETS_POLL_MAX``
    * ``CONFIG_NET_TEST_PROTOCOL``，以及作为其唯一被测系统的 ``samples/net/sockets/tcp`` 示例。
    * ``CONFIG_NET_GPTP_CLOCK_ACCURACY_*``
    * ``net_ipv6_set_hop_limit()``
    * ``net_if_ipv4_get_netmask()``
    * ``net_if_ipv4_set_netmask()``
    * ``net_if_ipv4_set_netmask_by_index()``
    * ``openthread_state_changed_cb_register()``
    * ``openthread_state_changed_cb_unregister()``
    * ``openthread_start()``
    * ``openthread_api_mutex_lock()``
    * ``openthread_api_mutex_try_lock()``
    * ``openthread_api_mutex_unlock()``
    * ``struct openthread_state_changed_cb``
    * ``TLS_CREDENTIAL_SERVER_CERTIFICATE``
    * ``start_11r_roaming``
    * ``IEEE802154_HW_SLEEP_TO_TX``

* Nordic

    * :dtcompatible:`nordic,owned-memory` 和 :dtcompatible:`nordic,owned-partitions` 的 ``owner-id``、``perm-read``、``perm-write``、``perm-execute``、``perm-secure`` 和 ``non-secure-callable`` 属性
    * ``CONFIG_BOARD_ENABLE_CPUNET``，由 :kconfig:option:`CONFIG_SOC_NRF53_CPUNET_ENABLE` 取代
    * ``CONFIG_GPIO_AS_PINRESET``
    * ``CONFIG_NRFS_LOCAL_DOMAIN_DVFS_SCALE_DOWN_AFTER_INIT``，由 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_HSFLL_LOCAL_REQ_LOW_FREQ` 取代
    * ``CONFIG_SOC_DCDC_NRF52X``
    * ``CONFIG_SOC_DCDC_NRF52X_HV``
    * ``CONFIG_SOC_DCDC_NRF53X_APP``
    * ``CONFIG_SOC_DCDC_NRF53X_NET``
    * ``CONFIG_SOC_DCDC_NRF53X_HV``

* POSIX

    * ``CONFIG_POSIX_READER_WRITER_LOCKS``

* 随机数

    * ``CONFIG_CTR_DRBG_CSPRNG_GENERATOR``
    * ``CONFIG_CS_CTR_DRBG_PERSONALIZATION``

* Shell

    * ``kernel log_level``，由 ``log enable`` 取代

* SPI

    * :c:macro:`SPI_CONFIG_DT`、:c:macro:`SPI_CONFIG_DT_INST`、:c:macro:`SPI_DT_SPEC_GET`、:c:macro:`SPI_DT_SPEC_INST_GET`、:c:macro:`SPI_DT_IODEV_DEFINE`、:c:macro:`SPI_DT_INST_IODEV_DEFINE` 和 :c:macro:`SPI_CS_CONTROL_INIT` 的可选 delay 参数已被移除。

* 流式 Flash

    * ``stream_flash_erase_page()``

* ZTest

    * ``CONFIG_ZTEST_SHUFFLE_SUITE_REPEAT_COUNT``
    * ``CONFIG_ZTEST_SHUFFLE_TEST_REPEAT_COUNT``

* imgtool 的 West 签名支持在 Zephyr 4.0 中已弃用，现已被移除。

* ``scripts/logging/dictionary/log_parser_uart.py`` 字典日志脚本在 Zephyr 4.3 中已弃用，现已被移除。请改用 :zephyr_file:`scripts/logging/dictionary/live_log_parser.py`。

* ``west flash``、``west debug`` 以及其他调用 runner 的命令的 ``--skip-rebuild`` 选项在 Zephyr 4.3 中已弃用，现已被移除。请改用 ``--no-rebuild``。

已弃用的 API 和选项
===================

* 音频编解码器

  * :c:struct:`audio_codec_api` 结构体已弃用。音频编解码器驱动现在应使用 :c:macro:`DEVICE_API` 宏来声明其驱动 API。

* 蓝牙

  * :kconfig:option:`CONFIG_BT_CUSTOM` 协议栈选择项已弃用。它源自过去可将整个蓝牙主机卸载到 Zephyr Bluetooth API 之后的年代，如今树内已无使用者；HCI 传输只是普通的设备驱动。基于 HCI 的协议栈 :kconfig:option:`CONFIG_BT_HCI` 是树内仅存的选择项；该选择本身保留，作为树外协议栈的扩展点。

* 构建系统

  * ``zephyr_file_copy()`` CMake 函数已弃用。请改用原生 ``file(COPY_FILE ...)`` CMake 命令。

* 时钟控制

  * :c:func:`z_nrf_clock_control_get_onoff` 函数已弃用。详见 :ref:`迁移指南 <migration_4.5>`。

  * 宏 :c:macro:`CLOCK_CONTROL_NRF_K32SRC_ACCURACY` 已弃用。详见 :ref:`迁移指南 <migration_4.5>`。

  * 宏 :c:macro:`CLOCK_CONTROL_NRF_K32SRC` 已弃用。详见 :ref:`迁移指南 <migration_4.5>`。

  * 宏 :c:macro:`CLOCK_CONTROL_NRF_SUBSYS_HFAUDIO` 已弃用。详见 :ref:`迁移指南 <migration_4.5>`。

  * 宏 :c:macro:`CLOCK_CONTROL_NRF_SUBSYS_HFAUDIO` 已弃用。详见 :ref:`迁移指南 <migration_4.5>`。

  * 宏 :c:macro:`CLOCK_CONTROL_NRF_SUBSYS_HF24M` 已弃用。详见 :ref:`迁移指南 <migration_4.5>`。

  * 宏 :c:macro:`CLOCK_CONTROL_NRF_SUBSYS_HF24M` 已弃用。详见 :ref:`迁移指南 <migration_4.5>`。

  * 宏 :c:macro:`CLOCK_CONTROL_NRF_SUBSYS_HF` 已弃用。详见 :ref:`迁移指南 <migration_4.5>`。

  * 枚举 :c:enumerator:`clock_control_nrf_type` 已弃用。详见 :ref:`迁移指南 <migration_4.5>`。

  * Kconfig 选项 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF` 及所有依赖的 Kconfig 均已弃用。详见 :ref:`迁移指南 <migration_4.5>`。这些 Kconfig 位于 ``drivers/clock_control/Kconfig.nrf`` 和 ``modules/hal_nordic/nrfx/Kconfig`` 文件中。

* 控制器局域网（CAN）

  * :c:func:`can_set_state_change_callback` 已弃用，取而代之的是 :c:func:`can_init_state_change_callback`、:c:func:`can_add_state_change_callback` 和 :c:func:`can_remove_state_change_callback`。新增的 API 函数允许添加多个 CAN 控制器状态变更回调（:github:`117889`）。

* CPU 负载

  * :kconfig:option:`CONFIG_CPU_LOAD_METRIC` 和 :c:func:`cpu_load_metric_get` 已弃用。CPU 负载指标模块已合并到统一的 :ref:`cpu_load` 模块中；请使用 :kconfig:option:`CONFIG_CPU_LOAD`，并搭配 :kconfig:option:`CONFIG_CPU_LOAD_BACKEND_RUNTIME_STATS` 后端和 :c:func:`cpu_load_get_cpu`。

* :abbr:`DMIC (Digital Microphone Interface)`

  * :c:struct:`_dmic_ops` 结构体已弃用。DMIC 驱动现在应使用 :c:macro:`DEVICE_API` 宏来声明其驱动 API。

* 电量计

  * 弃用了多个电量计属性枚举和联合体字段，改用带显式单位后缀的新版本。

* LoRa

  * 已将 :c:func:`lora_recv_duty_cycle` 重命名为 :c:func:`lora_recv_duty_cycle_async`，以与现有的同步/异步命名约定保持一致。

* Nordic

  * Nordic 内部的 SoC 平台 Kconfig 符号 ``NRF_PLATFORM_HALTIUM`` 和 ``NRF_PLATFORM_LUMOS`` 已弃用。请改用具体的 SOC_SERIES_* Kconfig 选项。

  * sysbuild 的 Kconfig 选项 ``SB_CONFIG_NRF_HALTIUM_GENERATE_UICR`` 已重命名为 :kconfig:option:`SB_CONFIG_NRF_GENERATE_UICR`。

  * Nordic SoC 头文件 :file:`<haltium_power.h>` 和 :file:`<haltium_pm_s2ram.h>` 已分别重命名为 :file:`<soc_power.h>` 和 :file:`<soc_pm_s2ram.h>`。

* Raspberry Pi

  * RP2350 的 ``SOC_RP2350A_HAZARD3``、``SOC_RP2350A_M33``、``SOC_RP2350B_HAZARD3`` 和 ``SOC_RP2350B_M33`` Kconfig 符号，以及 ``soc.yml`` 中对应的裸 ``hazard3``/``m33`` cpucluster 均已弃用，取而代之的是 ``SOC_RP2350A_HAZARD3_0``、``SOC_RP2350A_M33_0``、``SOC_RP2350B_HAZARD3_0`` 和 ``SOC_RP2350B_M33_0`` 及其 ``hazard3_0``/``m33_0`` cpucluster，以使 RP2350 双核簇命名与硬件模型 v2 保持一致。旧的 Kconfig 符号和 ``soc.yml`` 条目都将在未来版本中移除。所有树内开发板均已完成迁移。

* 环形缓冲区

  * 环形缓冲区的 item API（:c:func:`ring_buf_item_init`、:c:func:`ring_buf_item_put`、:c:func:`ring_buf_item_get`、:c:func:`ring_buf_item_space_get`）已弃用，改用 :c:struct:`sys_ringq` （参见 :ref:`fixed_size_ringq_api`）。

  * 零拷贝的 claim/finish API（:c:func:`ring_buf_put_claim`、:c:func:`ring_buf_put_finish`、:c:func:`ring_buf_get_claim`、:c:func:`ring_buf_get_finish`）已弃用，改用新的 :c:func:`ring_buf_put_ptr` / :c:func:`ring_buf_get_ptr` API。仍在使用该 API 的代码必须启用 :kconfig:option:`CONFIG_RING_BUFFER`。

  * :kconfig:option:`CONFIG_RING_BUFFER` 已弃用。环形缓冲区 API 现在完全由头文件实现且始终可用，因此使用环形缓冲区不再需要该选项。它现在仅作为已弃用的开关保留：树外代码迁移到替代 API 期间，可用它恢复旧版的 claim/finish API 和 item API。

* 网络缓冲区

  * :c:func:`net_buf_max_len` 和 :c:func:`net_buf_simple_max_len` 已弃用。请改用 :c:func:`net_buf_tailroom` 和 :c:func:`net_buf_simple_tailroom`。详情请参见 :ref:`迁移指南 <migration_4.5>`。

* 网络

  * LLMNR 支持已弃用（:kconfig:option:`CONFIG_LLMNR_RESOLVER` 和 :kconfig:option:`CONFIG_LLMNR_RESPONDER`）。LLMNR 正在被逐步淘汰；请改用 mDNS（:kconfig:option:`CONFIG_MDNS_RESOLVER` / :kconfig:option:`CONFIG_MDNS_RESPONDER`）。

* 网络链路层

  * :kconfig:option:`CONFIG_NET_L2_PTP` 已弃用。请改用 :kconfig:option:`CONFIG_NET_L2_PTP_TIMESTAMPING`。

* SPI

  * SPI API 现在使用包容性术语（controller/peripheral、SDO/SDI）。以下旧名称已弃用：``SPI_OP_MODE_MASTER``/``SPI_OP_MODE_SLAVE`` （请使用 :c:macro:`SPI_OP_MODE_CONTROLLER`/:c:macro:`SPI_OP_MODE_PERIPHERAL`）、:c:struct:`spi_config` 的 ``slave`` 成员（请使用 ``peripheral``）、``SPI_MOSI_OVERRUN_*`` 宏（请使用 :c:macro:`SPI_SDO_OVERRUN_UNKNOWN`、:c:macro:`SPI_SDO_OVERRUN_DT`、:c:macro:`SPI_SDO_OVERRUN_DT_INST`）、``CONFIG_SPI_SLAVE`` （请使用 :kconfig:option:`CONFIG_SPI_PERIPHERAL`）、``zephyr,bt-hci-spi-slave`` 设备树 compatible（请使用 :dtcompatible:`zephyr,bt-hci-spi-peripheral`）以及迁移指南中列出的绑定的 ``mosi-gpios``/``miso-gpios`` 风格设备树属性。

* 定时器

  * 新增 :c:func:`sys_clock_no_timeout` 钩子，用于处理 :kconfig:option:`CONFIG_SYSTEM_CLOCK_SLOPPY_IDLE`，取代以 ``ticks=K_TICKS_FOREVER`` 调用 :c:func:`sys_clock_set_timeout`。
  * 新增 :c:func:`sys_clock_idle_enter` 钩子，用于处理进入低功耗状态的情况，取代以 ``idle=true`` 调用 :c:func:`sys_clock_set_timeout`。

* :abbr:`USB (Universal Serial Bus)`

  * :dtcompatible:`st,stm32u5-otghs-phy` 的 ``clock-reference`` 属性已弃用。请勿指定该属性；底层驱动不再需要它。

* 视频

  * 视频驱动 API（``<zephyr/drivers/video.h>``）中的所有函数已移至视频子系统（``<zephyr/video/video.h>``）。应用只需重命名 ``#include``。

* West

  * ``west spdx --init`` 已弃用。启用 :kconfig:option:`CONFIG_BUILD_OUTPUT_META` 的构建现在会向 CMake 请求 ``west spdx`` 所读取的基于文件的 API，因此构建目录不再需要在配置之前预先准备。参见 :ref:`west-spdx`。

* 工作队列

  * :c:member:`k_work_q.thread` 已弃用。请改用 :c:member:`k_work_q.thread_id`。

新增 API 和选项
===============
..
  Link to new APIs here, in a group if you think it's necessary, no need to get
  fancy just list the link, that should contain the documentation. If you feel
  like you need to add more details, add them in the API documentation code
  instead.

.. zephyr-keep-sorted-start re(^\* \w) ignorecase

* ADC

  * 新增可选的 :c:member:`adc_driver_api.ref_get` 回调和 :c:func:`adc_ref_get`，使应用和 :c:func:`adc_raw_to_millivolts_dt` 可以对任意 :c:enum:`adc_reference` 使用驱动自有的运行时毫伏标度。当回调为 NULL 时，静态的 :c:member:`adc_driver_api.ref_internal` 仍是 :c:enumerator:`ADC_REF_INTERNAL` 的回退值。:c:func:`adc_raw_to_millivolts_dt` 在 :c:func:`adc_ref_get` 失败时会回退到通道设备树属性 ``zephyr,vref-mv``。

* CPU 频率调节

  * :kconfig:option:`CONFIG_CPU_FREQ_POLICY_TIMING_NOISE`

* FIDO2

  * :c:func:`fido2_up_reset`
  * :c:macro:`FIDO2_BLE_SERVICE_UUID_VAL`
  * :c:macro:`FIDO2_BLE_SERVICE_DATA_PAIRING_MODE`
  * :kconfig:option:`CONFIG_FIDO2_TRANSPORT_BLE`
  * :kconfig:option:`CONFIG_FIDO2_BLE_REQUIRE_AUTHENTICATED_LINK`
  * :kconfig:option:`CONFIG_FIDO2_BLE_RX_WORKQ_STACK_SIZE`
  * :kconfig:option:`CONFIG_FIDO2_BLE_CONTROL_POINT_LENGTH`
  * :kconfig:option:`CONFIG_FIDO2_BLE_RX_QUEUE_DEPTH`
  * :kconfig:option:`CONFIG_FIDO2_BLE_TX_FRAME_COUNT`
  * :kconfig:option:`CONFIG_FIDO2_BLE_KEEPALIVE_INTERVAL_MS`
  * :kconfig:option:`CONFIG_FIDO2_BLE_RX_TIMEOUT_MS`

* HWSPINLOCK

  * :c:macro:`HWSPINLOCK_SPINLOCK_ARRAY_DT_DEFINE`
  * :c:macro:`HWSPINLOCK_SPINLOCK_ARRAY_DT_INST_DEFINE`
  * :c:macro:`HWSPINLOCK_COMMON_CONFIG_FROM_DT_NODE`
  * :c:macro:`HWSPINLOCK_COMMON_CONFIG_FROM_DT_INST`

* Kconfig

  * 新增 ``dt_partition_mtd`` 预处理函数（:github:`111599`）

* LoRa

  * :c:func:`lora_recv_duty_cycle`
  * :c:func:`lora_recv_duty_cycle_async`
  * :c:func:`lora_energy_detect`
  * :c:func:`lora_rssi`

* USB Type-C

  * :kconfig:option:`CONFIG_USBC_LOG_PD_MSG_NAMES`

* Zbus

  * :kconfig:option:`CONFIG_ZBUS_RUNTIME_CHANNEL_REGISTRATION`
  * :c:func:`zbus_runtime_channel_init`
  * :c:func:`zbus_runtime_channel_register`
  * :c:func:`zbus_runtime_channel_unregister`

* 内核

  * :c:func:`k_thread_runtime_stats_is_enabled`
  * :c:func:`atomic_test_and_set_bit_to`
  * :c:macro:`K_MSGQ_DEFINE_STATIC`
  * :c:macro:`K_MSGQ_DEFINE_TYPE`
  * :c:macro:`K_MSGQ_DEFINE_STATIC_TYPE`
  * :c:func:`k_sleep_ticks`
  * 中断控制 API 的命名空间等效函数，推荐用于新代码；不带前缀的名称仍完全支持：:c:func:`k_irq_lock`、:c:func:`k_irq_unlock`、:c:func:`k_irq_enable`、:c:func:`k_irq_disable`、:c:func:`k_irq_is_enabled`、:c:func:`k_irq_connect_dynamic` 和 :c:func:`k_irq_disconnect_dynamic`

* 加密

  * :c:enumerator:`CRYPTO_CIPHER_MODE_CFB`
  * :c:enumerator:`CRYPTO_CIPHER_MODE_OFB`
  * :c:func:`cipher_cfb_op`
  * :c:func:`cipher_ofb_op`

* 多媒体流水线

  * :kconfig:option:`CONFIG_MPIPE` （参见 :ref:`mpipe`）

* 安全存储

  * 新增 :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_CRYPT_CUSTOM`，用于实现自己的 :c:func:`secure_storage_its_transform_aead_crypt`。（:github:`118542`）
  * :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_SCHEME_IS_CONFIGURABLE`
  * :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_KEY_SIZE_IS_CONFIGURABLE`


* 定时器

  * :c:func:`z_sys_clock_lpm_enter`

* 时钟控制

  * :kconfig:option:`CLOCK_CONTROL_NRF_ONOFF`
  * 对于兼容 ``nordic,nrf-clock-hfclk``、``nordic,nrf-clock-lfclk``、``nordic,nrf-clock-hfclk192m``、``nordic,nrf-clock-hfclk24m``、``nordic,nrf-clock-hfclkaudio``、``nordic,nrf-clock-xo`` 和 ``nordic,nrf-clock-xo24m`` 的设备，现在支持以下函数。详情请参见 :ref:`迁移指南 <migration_4.5>`。 * :c:func:`clock_control_request` * :c:func:`clock_control_request_sync` * :c:func:`clock_control_release` * :c:func:`clock_control_cancel_or_release`

* 显示

  * :c:enumerator:`PIXEL_FORMAT_YUYV`
  * :c:macro:`PANEL_PIXEL_FORMAT_YUYV`

* 架构

  * :kconfig:option:`CONFIG_ARM_MPU_CM7_UNMAPPED_REGION` （Arm Cortex-M7 用于未映射地址的兜底 MPU 区域，勘误 1013783 的规避措施）
  * :kconfig:option:`CONFIG_CORTEX_M_ERRATUM_440977_WORKAROUND` （在提升优先级的 BASEPRI 写入后保留一条 ISB 指令；在 Arm Cortex-M7 上默认启用，勘误 440977 影响 r0p0/r0p1 内核。其他 Cortex-M 内核不再在中断加锁/解锁快速路径中执行屏障，从而加快内核热路径）
  * :kconfig:option:`CONFIG_EXCEPTION_DUMP` （默认启用，可禁用以在空间受限的构建中编译掉故障处理程序的输出）
  * :kconfig:option:`CONFIG_RISCV_ISA_EXT_ZKR` （RISC-V Zkr 熵源扩展，通过 ``riscv,isa-extensions`` 设备树属性启用）
  * :kconfig:option:`CONFIG_RISCV_USER_STRING_NLEN_VALIDATE` （RISC-V，在 ``arch_user_string_nlen()`` 中逐块校验用户字符串，而不依赖故障修正机制，适用于加载访问故障不精确的 SoC）
  * :kconfig:option:`CONFIG_RISCV_SOC_HAS_SYSCALL_INTMASK` （RISC-V SoC 钩子，用于在用户态系统调用主体中屏蔽中断，而不清除 ``mstatus.MIE``）
  * :kconfig:option:`CONFIG_RISCV_SOC_SYSCALL_CLOSE_ECALL` （RISC-V SoC 钩子，用于在用户态系统调用主体运行前退出 ecall 异常，适用于在该异常仍处于打开状态时无法递送由系统调用主体引发的故障的 SoC）

* 熵源

  * :kconfig:option:`CONFIG_ENTROPY_RISCV_ZKR` （基于 RISC-V Zkr 扩展 ``seed`` CSR 的架构级熵源驱动）

* 环形缓冲区

  * :c:struct:`sys_ringq` （参见 :ref:`fixed_size_ringq_api`）
  * :c:func:`ring_buf_put_ptr`
  * :c:func:`ring_buf_get_ptr`
  * :c:func:`ring_buf_commit`
  * :c:func:`ring_buf_consume`

* 电源管理

  * :c:macro:`LOG_DBG_PM_DEVICE_RUNTIME_GET`
  * :c:macro:`LOG_WRN_PM_DEVICE_RUNTIME_GET`
  * :c:macro:`LOG_ERR_PM_DEVICE_RUNTIME_GET`
  * :c:macro:`LOG_DBG_PM_DEVICE_RUNTIME_PUT`
  * :c:macro:`LOG_WRN_PM_DEVICE_RUNTIME_PUT`
  * :c:macro:`LOG_ERR_PM_DEVICE_RUNTIME_PUT`
  * :c:macro:`LOG_INST_DBG_PM_DEVICE_RUNTIME_GET`
  * :c:macro:`LOG_INST_WRN_PM_DEVICE_RUNTIME_GET`
  * :c:macro:`LOG_INST_ERR_PM_DEVICE_RUNTIME_GET`
  * :c:macro:`LOG_INST_DBG_PM_DEVICE_RUNTIME_PUT`
  * :c:macro:`LOG_INST_WRN_PM_DEVICE_RUNTIME_PUT`
  * :c:macro:`LOG_INST_ERR_PM_DEVICE_RUNTIME_PUT`

* 电量计

  * :c:func:`fuel_gauge_set_buffer_prop` 以及可选的 :c:member:`fuel_gauge_driver_api.set_buffer_property` 回调，用于写入可变长度缓冲区属性，与 :c:func:`fuel_gauge_get_buffer_prop` 对称。

* 管理

  * MCUmgr

    * 新增对 SPI MCUmgr SMP 传输的支持，可通过 :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_SPI` 启用。

    * 新增实验性的 :ref:`传输管理组 <mcumgr_smp_group_11>`：:kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT`、:kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_LOCKING`、:kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_MAX_BRIDGES`、:kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_GROUP_ID_DEFAULT`、:kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_GROUP_ID_CUSTOM_VALUE`、:kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_GROUP_ID_CUSTOM_VALUE_GROUP_ID`、:kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_GROUP_ID_CUSTOM_FUNCTION` 和 :kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_INFO_FUNCTIONS`。

* 网络

  * 新增 :c:func:`net_eth_set_if_type_wifi`，用于将以太网接口类型设置为 Wi-Fi。
  * 新增公开的邻居缓存 API：:c:func:`net_if_ipv4_nbr_flush` 和 :c:func:`net_if_ipv6_nbr_flush` 用于丢弃接口已学习到的邻居，:c:func:`net_if_ipv4_nbr_rm` 和 :c:func:`net_if_ipv6_nbr_rm` 则移除单个邻居。在以太网链路上，IPv4 缓存就是 ARP 缓存。
  * 新增 :c:func:`net_dhcpv4_set_reboot_hint`，用于为 DHCPv4 客户端预置先前租用的地址，以支持 INIT-REBOOT。
  * 新增 mDNS 应答器接口策略（:kconfig:option:`CONFIG_MDNS_RESPONDER_IFACE_POLICY_ALLOWLIST`、:kconfig:option:`CONFIG_MDNS_RESPONDER_IFACE_POLICY_DENYLIST`），以及 :kconfig:option:`CONFIG_MDNS_RESPONDER_IFACE_LIST`，用于控制 mDNS 应答器在哪些网络接口上运行。
  * 新增 :c:func:`mdns_responder_enable_iface` 和 :c:func:`mdns_responder_disable_iface` （:kconfig:option:`CONFIG_MDNS_RESPONDER_RUNTIME_IFACE_CONTROL`），用于在运行时启用或停用某个网络接口上的 mDNS 应答器。
  * 新增支持 IPv6 前缀委派的 DHCPv6 服务器（:kconfig:option:`CONFIG_NET_DHCPV6_SERVER`）：:c:func:`net_dhcpv6_server_start`、:c:func:`net_dhcpv6_server_stop` 和 :c:func:`net_dhcpv6_server_foreach_lease`。
  * 新增 IPv6 路由器角色，即发送路由器通告（:kconfig:option:`CONFIG_NET_IPV6_ND_RA_TX`）：:c:func:`net_if_ipv6_router_start`、:c:func:`net_if_ipv6_router_stop` 和 :c:func:`net_if_ipv6_prefix_set_advertise`。
  * 为 DHCPv6 客户端新增请求路由器支持，委派前缀可通过 :c:member:`net_dhcpv6_params.downstream_ifaces` 再委派到下游链路。
  * 新增 :c:func:`net_eth_mcast_addr_add`、:c:func:`net_eth_mcast_addr_rm` 和 :c:func:`net_eth_mcast_addr_foreach`。以太网 L2 现在会跟踪接口所监听的链路层组播地址，因此只有当某个组的第一个用户加入或最后一个用户离开时，才会要求以太网驱动更改其接收过滤器。此前，IP 层的加入和数据包套接字成员关系是分别转发给驱动的，离开某个组可能导致设备不再监听另一个需要相同链路层地址的组。由于 IPv4 组播地址与链路层地址按 32:1 映射，这种情况很容易发生。驱动还可以把 ``ETHERNET_CONFIG_TYPE_FILTER`` 视为地址已变化的提示，并通过 :c:func:`net_eth_mcast_addr_foreach` 遍历这些地址来重新配置其过滤器，这适合按地址哈希进行过滤的设备。一个接口能跟踪多少地址，等于各已启用子系统请求的数量之和；如果应用需要更多，可用 :kconfig:option:`CONFIG_NET_L2_ETHERNET_MCAST_FILTER_COUNT` 提高。传给 :c:func:`net_eth_mac_filter` 或 ``NET_REQUEST_ETHERNET_SET_MAC_FILTER`` 的组播目的地址也按同样方式计数，因此应用设置的每个此类过滤器现在也必须由应用取消设置，而取消设置一个从未设置过的过滤器会失败并返回 ``-ENOENT``。
  * 在 ``ZSOCK_SOL_PACKET`` 层新增 ``ZSOCK_PACKET_ADD_MEMBERSHIP`` 和 ``ZSOCK_PACKET_DROP_MEMBERSHIP`` 套接字选项（:kconfig:option:`CONFIG_NET_SOCKETS_PACKET_MCAST_MEMBERSHIP`），使数据包套接字可以请求网络接口开始或停止监听额外的 L2 组播地址。在以太网上，如果设备支持过滤，该地址会被写入设备的接收过滤器；不支持过滤的设备则仍会将组播向上传递。接口无法满足的加入请求会报告给应用：接口无法再跟踪更多地址时返回 ``ENOMEM``，不是以太网接口时返回 ``ENOTSUP``。成员关系变化由 :c:macro:`NET_EVENT_PACKET_MCAST_MEMBERSHIP_ADD` 和 :c:macro:`NET_EVENT_PACKET_MCAST_MEMBERSHIP_DROP` 网络管理事件报告。套接字关闭时仍持有的成员关系会自动丢弃，:kconfig:option:`CONFIG_NET_SOCKETS_PACKET_MCAST_MEMBERSHIP_COUNT` 用于设置同一时间可激活的成员关系数量。
  * 新增对接收数据的 TCP 选择性确认（:rfc:`2018`，:kconfig:option:`CONFIG_NET_TCP_SACK`，默认启用）。Zephyr 现在在握手阶段提供 SACK，并报告保存在接收队列中的乱序数据，从而使支持 SACK 的发送方只需重发缺失的数据。重传时还不会使用接收到的 SACK 块。
  * :kconfig:option:`CONFIG_PTP_NETWORK_MODE_HYBRID`
  * 新增 SNTP 服务器（:kconfig:option:`CONFIG_SNTP_SERVER`），它在所有已启用的地址族上应答 UDP 端口 123 的时间查询。应用先设置系统时钟，然后通过 :c:func:`sntp_server_clock_source` 告知服务器其时钟源；在此之前，服务器会告知客户端不得使用其时间。SNTP 客户端现在仅由 :kconfig:option:`CONFIG_SNTP` 选择，二者共用 :kconfig:option:`CONFIG_SNTP_LIB`。
  * 新增 :c:func:`dns_resolve_is_active`，用于在不读取解析上下文内部信息的情况下检查某个 DNS 解析上下文是否处于活动状态。

* 脉冲 IO

  * 新增了 :ref:`脉冲 IO <pulse_io_api>` 子系统，为在 GPIO 线上生成和捕获定时数字边沿的硬件提供与厂商无关的 API。

* 蓝牙

  * 音频

    * :c:func:`bt_aics_client_free_instance`
    * :c:func:`bt_ascs_register`
    * :c:func:`bt_ascs_unregister`
    * :c:func:`bt_bap_unicast_client_qos_from_group`
    * :c:func:`bt_bap_qos_cfg_eq`
    * :c:member:`bt_bap_unicast_group_info.c_to_p_interval`
    * :c:member:`bt_bap_unicast_group_info.p_to_c_interval`
    * :c:member:`bt_bap_unicast_group_info.c_to_p_latency`
    * :c:member:`bt_bap_unicast_group_info.p_to_c_latency`
    * :c:member:`bt_bap_unicast_group_info.framing`
    * :c:member:`bt_bap_unicast_group_info.packing`
    * :c:member:`bt_bap_unicast_group_info.has_been_connected`
    * :c:member:`bt_bap_unicast_group_info.c_to_p_ft`
    * :c:member:`bt_bap_unicast_group_info.p_to_c_ft`
    * :c:member:`bt_bap_unicast_group_info.iso_interval`
    * :c:member:`bt_cap_initiator_cb.unicast_start_codec_configured`
    * :c:member:`bt_cap_initiator_cb.unicast_start_qos_configured`
    * :c:member:`bt_cap_initiator_cb.unicast_start_enabled`
    * :c:member:`bt_cap_initiator_cb.unicast_start_connected`
    * :c:member:`bt_cap_initiator_cb.unicast_start_started`
    * :c:member:`bt_cap_initiator_cb.unicast_stop_disabled`
    * :c:member:`bt_cap_initiator_cb.unicast_stop_stopped`
    * :c:member:`bt_cap_initiator_cb.unicast_stop_released`
    * :c:func:`bt_vocs_client_free_instance`

  * 经典蓝牙

    * :kconfig:option:`CONFIG_BT_SMP_DERIVE_LTK`
    * :kconfig:option:`CONFIG_BT_SMP_DERIVE_LK`
    * :c:func:`bt_sdp_unregister_service`

  * HCI 驱动

    * :c:macro:`BT_HCI_PKT_CMD_DEFINE`
    * :c:macro:`BT_HCI_PKT_CMD_DEFINE_STATIC`
    * :c:func:`bt_hci_pkt_reset_cmd`
    * :c:func:`bt_hci_pkt_push_cmd_hdr`
    * :c:func:`bt_hci_pkt_pull_cmd_complete`
    * :c:func:`bt_hci_pkt_pull_cmd_status`
    * :c:func:`bt_hci_pkt_parse_cmd_rsp`
    * :c:func:`bt_hci_lockstep_cmd_send_sync`
    * :c:func:`bt_hci_lockstep_reset`
    * :c:func:`bt_hci_set_public_addr` 和 :c:func:`bt_hci_get_public_addr`
    * :c:func:`bt_hci_can_close`

  * 主机

    * :c:func:`bt_conn_take`
    * :c:func:`bt_conn_drop`
    * :c:func:`bt_id_reset_irk`
    * :c:macro:`BT_IRK_SIZE`
    * :c:func:`bt_iso_chan_state_str`
    * :c:member:`bt_iso_chan_ops.send_failed`
    * :c:func:`bt_iso_get_chan_by_conn`
    * :c:func:`bt_le_per_adv_update_did`
    * :c:member:`bt_le_adv_param.tx_power` 和 :c:enumerator:`BT_LE_ADV_OPT_TX_POWER`，用于为每个扩展广播集请求特定的 TX 功率级别。
    * :c:member:`bt_conn_cb.le_param_update_rejected`
    * ``BT_HCI_QUIRK_NO_FLOW_CONTROL`` HCI 设备特殊行为，适用于宣称支持却拒绝控制器到主机流控命令的控制器。
    * :c:member:`bt_rfcomm_dlc.rx_credit_limit`，用于配置每个 DLC 的初始 RX 信用数。
    * :c:func:`bt_rfcomm_dlc_recv_complete`，用于向对端返还 RX 信用。应用可以从 :c:member:`bt_rfcomm_dlc_ops.recv` 回调返回 ``-EINPROGRESS``，将缓冲区释放和流控信用补充推迟到处理完成之后。
    * :c:func:`bt_le_bond_addr_res_support`、:c:enum:`bt_le_addr_res_support` 和 :c:member:`bt_conn_auth_info_cb.addr_res_support_read`
    * :c:enumerator:`BT_LE_SCAN_OPT_EXT_FILTER_POLICY`
    * :kconfig:option:`CONFIG_BT_SCAN_EXT_FILTER_POLICY`
    * :c:member:`bt_le_scan_recv_info.direct_addr`

  * Mesh

    * :c:struct:`bt_mesh_lpn_timing`
    * :c:func:`bt_mesh_stat_lpn_timing_get`
    * :c:func:`bt_mesh_stat_lpn_timing_reset`
    * :kconfig:option:`CONFIG_BT_MESH_LPN_OFFER_WAIT_TIMEOUT`

* 触觉反馈

  * :c:enum:`haptics_monitor`
  * :c:enum:`haptics_monitor_type`
  * :c:enum:`haptics_source`
  * :c:enum:`haptics_trigger_type`
  * :c:union:`haptics_config`
  * :c:func:`haptics_calibrate`
  * :c:func:`haptics_monitor_get`
  * :c:func:`haptics_monitor_set`
  * :c:func:`haptics_select_source`
  * :c:func:`haptics_set_level`
  * :c:func:`haptics_set_trigger`
  * :c:func:`haptics_stream_samples`
  * :c:func:`haptics_trigger`

* 设备树

  * :c:macro:`DT_IRQN_BY_NAME`
  * :c:macro:`DT_INST_IRQN_BY_NAME`

* 调制解调器

  * :c:enumerator:`CELLULAR_MODEM_INFO_SERIAL_NUMBER`

* 音频

  * :c:member:`pcm_stream_cfg.gain_db`
  * :c:struct:`audio_codec_eq_cfg`

.. zephyr-keep-sorted-stop

新增开发板
**********

..
  You may update this list as you contribute a new board during the release cycle, in order to make
  it visible to people who might be looking at the working draft of the release notes. However, note
  that this list will be recomputed at the time of the release, so you don't *have* to update it.
  In any case, just link the board, further details go in the board description.

* Adafruit Industries, LLC

  * :zephyr:board:`adafruit_feather_esp32c6` (``adafruit_feather_esp32c6``)
  * :zephyr:board:`adafruit_trrs_trinkey` (``adafruit_trrs_trinkey``)

* Advanced Micro Devices (AMD), Inc.

  * :zephyr:board:`acp_7_0_adsp` (``acp_7_0_adsp``)
  * :zephyr:board:`acp_7_x_adsp` (``acp_7_x_adsp``)
  * :zephyr:board:`zynqmp_apu` (``zynqmp_apu``)
  * :zephyr:board:`zynqmp_rpu` (``zynqmp_rpu``)

* Aesc Silicon

  * :zephyr:board:`elemrv_flask_h` (``elemrv_flask_h``)

* Ai-Thinker Co., Ltd.

  * :zephyr:board:`ai_m64p_32s_kit` (``ai_m64p_32s_kit``)
  * :zephyr:board:`aipi_eyes_s2` (``aipi_eyes_s2``)

* Alif Semiconductor

  * :zephyr:board:`balletto_b1_dk` (``balletto_b1_dk``)
  * :zephyr:board:`ensemble_e8_ak` (``ensemble_e8_ak``)

* Analog Devices, Inc.

  * :zephyr:board:`max32651evkit` (``max32651evkit``)

* Antmicro

  * :zephyr:board:`stm32h7_hdmi_board` (``stm32h7_hdmi_board``)
  * :zephyr:board:`stm32h7_renode_reference_board` (``stm32h7_renode_reference_board``)

* Arduino

  * :zephyr:board:`arduino_nano_connect` (``arduino_nano_connect``)
  * :zephyr:board:`arduino_nesso_n1` (``arduino_nesso_n1``)

* ARM Ltd.

  * :zephyr:board:`fvp_corstone1000` (``fvp_corstone1000``)

* Armfly

  * :zephyr:board:`armfly_stm32h743xih6` (``armfly_stm32h743xih6``)

* Barth Elektronik GmbH

  * :zephyr:board:`stg_800` (``stg_800``)

* BeagleBoard.org Foundation

  * :zephyr:board:`beaglebadge` (``beaglebadge``)
  * :zephyr:board:`beagleconnect_zepto` (``beagleconnect_zepto``)
  * :zephyr:board:`pocketbeagle_2_industrial` (``pocketbeagle_2_industrial``)

* BLIIoT Technology Co., Ltd.

  * :zephyr:board:`am62x_m4_bl350` (``am62x_m4_bl350``)

* Bouffalo Lab (Nanjing) Co., Ltd.

  * :zephyr:board:`bl618g0` (``bl618g0``)

* CAN-module, FOP

  * :zephyr:board:`canbridge_g473` (``canbridge_g473``)
  * :zephyr:board:`usbcan_iso` (``usbcan_iso``)
  * :zephyr:board:`usbcanfd_dual` (``usbcanfd_dual``)
  * :zephyr:board:`usbcanfd_solo` (``usbcanfd_solo``)

* Chengdu Ebyte Electronic Technology

  * :zephyr:board:`e80_900mbl_01` (``e80_900mbl_01``)
  * :zephyr:board:`eora_hub_900tb` (``eora_hub_900tb``)

* Chengdu Heltec Automation Technology Co., Ltd.

  * :zephyr:board:`heltec_t114_v2` (``heltec_t114_v2``)

* Cirrus Logic, Inc.

  * :zephyr:board:`crd40l26` (``crd40l26``)

* emtrion GmbH

  * :zephyr:board:`emsbc_neon_cm7` (``emsbc_neon_cm7``)

* Espressif Systems

  * :zephyr:board:`esp32p4_function_ev_board` (``esp32p4_function_ev_board``)
  * :zephyr:board:`esp32p4x_function_ev_board` (``esp32p4x_function_ev_board``)
  * :zephyr:board:`esp32s3_box3` (``esp32s3_box3``)

* Eurovibes

  * :zephyr:board:`eurovibes_stm32g431_sertest-ng` (``eurovibes_stm32g431_sertest-ng``)

* FlySky

  * :zephyr:board:`fs_i6s` (``fs_i6s``)

* Heimann Sensor GmbH

  * :zephyr:board:`htpa_eval` (``htpa_eval``)

* Intel Corporation

  * :zephyr:board:`intel_nvl_s_rvp` (``intel_nvl_s_rvp``)

* Jhoinrch

  * :zephyr:board:`rh02` (``rh02``)
  * :zephyr:board:`rh02_plus_2026` (``rh02_plus_2026``)

* KAGA FEI Co., Ltd.

  * :zephyr:board:`ec4l15ba1` (``ec4l15ba1``)

* KinCony Electronics Co., Ltd.

  * :zephyr:board:`kincony_kc868_a8` (``kincony_kc868_a8``)

* Lilygo Shenzhen Xinyuan Electronic Technology Co., Ltd

  * :zephyr:board:`t_deck` (``t_deck``)

* M5Stack

  * :zephyr:board:`m5stack_paper_color` (``m5stack_paper_color``)
  * :zephyr:board:`m5stack_sticks3` (``m5stack_sticks3``)
  * :zephyr:board:`m5stack_unitc6l` (``m5stack_unitc6l``)

* Makerfabs

  * :zephyr:board:`matouch_mtro128g` (``matouch_mtro128g``)

* Microchip Technology Inc.

  * :zephyr:board:`m2s010_mkr_kit` (``m2s010_mkr_kit``)
  * :zephyr:board:`m2s_hello_fpga_kit` (``m2s_hello_fpga_kit``)
  * :zephyr:board:`pic32ck_gc01_cult` (``pic32ck_gc01_cult``)
  * :zephyr:board:`pic32cm_gc00_cpro` (``pic32cm_gc00_cpro``)
  * :zephyr:board:`pic32cm_sg00_cpro` (``pic32cm_sg00_cpro``)
  * :zephyr:board:`sama5d27_som1_ek1` (``sama5d27_som1_ek1``)

* MuseLab Electronics

  * :zephyr:board:`nano_ch32v317` (``nano_ch32v317``)
  * :zephyr:board:`nano_ch57x` (``nano_ch57x``)

* Nordic Semiconductor

  * :zephyr:board:`nrf93m1dk` (``nrf93m1dk``)

* Norik Systems

  * :zephyr:board:`dect_nr_plus_usb_dongle` (``dect_nr_plus_usb_dongle``)

* NUCODE Co., Ltd. (nuworks.io)

  * :zephyr:board:`nucode_nu32` (``nucode_nu32``)
  * :zephyr:board:`nucode_nu40` (``nucode_nu40``)

* Nuvoton Technology Corporation

  * :zephyr:board:`numaker_m031ki` (``numaker_m031ki``)
  * :zephyr:board:`numaker_m3351ki` (``numaker_m3351ki``)

* NXP Semiconductors

  * :zephyr:board:`frdm_imxrt1152` (``frdm_imxrt1152``)
  * :zephyr:board:`frdm_imxrt700` (``frdm_imxrt700``)
  * :zephyr:board:`imx952_evk` (``imx952_evk``)
  * :zephyr:board:`lpc845brk` (``lpc845brk``)
  * :zephyr:board:`lpcxpresso54628` (``lpcxpresso54628``)
  * :zephyr:board:`mimxrt685_aud_evk` (``mimxrt685_aud_evk``)
  * :zephyr:board:`mr_navq95b` (``mr_navq95b``)

* OLIMEX Ltd.

  * :zephyr:board:`esp32p4_pc` (``esp32p4_pc``)

* 其他

  * :zephyr:board:`bl704l_dvk` (``bl704l_dvk``)
  * :zephyr:board:`esp32h2_supermini` (``esp32h2_supermini``)
  * :zephyr:board:`jz_f407vet6` (``jz_f407vet6``)
  * :zephyr:board:`stm32_debug_probe` (``stm32_debug_probe``)

* Pine64

  * :zephyr:board:`pinecone` (``pinecone``)

* QEMU

  * :zephyr:board:`qemu_cortex_a72` (``qemu_cortex_a72``)

* Radxa

  * :zephyr:board:`rock_3b` (``rock_3b``)
  * :zephyr:board:`rock_5b_plus` (``rock_5b_plus``)

* Raspberry Pi Foundation

  * :zephyr:board:`rpi_zero_2w` (``rpi_zero_2w``)

* Raytac Corporation

  * :zephyr:board:`raytac_an54lv_db_15` (``raytac_an54lv_db_15``)

* Realtek Semiconductor Corp.

  * :zephyr:board:`pke8721daf_c13_f10` (``pke8721daf_c13_f10``)

* Renesas Electronics Corporation

  * :zephyr:board:`rcar_ironhide_x5h` (``rcar_ironhide_x5h``)
  * :zephyr:board:`rza3m_ek` (``rza3m_ek``)

* Seeed Technology Co., Ltd

  * :zephyr:board:`reterminal_e1001` (``reterminal_e1001``)
  * :zephyr:board:`reterminal_e1003` (``reterminal_e1003``)
  * :zephyr:board:`wio_tracker_l1` (``wio_tracker_l1``)
  * :zephyr:board:`xiao_esp32c5` (``xiao_esp32c5``)
  * :zephyr:board:`xiao_nrf54lm20a` (``xiao_nrf54lm20a``)

* SEGGER Microcontroller GmbH

  * :zephyr:board:`nandeval_h743zi` (``nandeval_h743zi``)

* SHAKTI Processor Program

  * :zephyr:board:`nexys_ganga` (``nexys_ganga``)

* Shanghai Ruiside Electronic Technology Co., Ltd.

  * :zephyr:board:`ra8p1_titan` (``ra8p1_titan``)
  * :zephyr:board:`ra8p1_titan_mini` (``ra8p1_titan_mini``)

* Shenzhen JLC Technology Group Co., Ltd.

  * :zephyr:board:`skystar_gd32f407vet6` (``skystar_gd32f407vet6``)

* Shenzhen Luckfox Technology Co., Ltd.

  * :zephyr:board:`pico_ultra` (``pico_ultra``)

* Shenzhen Sipeed Technology Co., Ltd.

  * :zephyr:board:`m0sense` (``m0sense``)
  * :zephyr:board:`m1s_dock` (``m1s_dock``)

* Shenzhen Xunlong Software CO.,Limited

  * :zephyr:board:`opi_zero2w` (``opi_zero2w``)

* Silicon Laboratories

  * :zephyr:board:`kg100s_rb4332a` (``kg100s_rb4332a``)
  * :zephyr:board:`siwx917_ek2708a` (``siwx917_ek2708a``)
  * :zephyr:board:`xg26_dk2608a` (``xg26_dk2608a``)
  * :zephyr:board:`xg26_rb4121a` (``xg26_rb4121a``)

* STMicroelectronics

  * :zephyr:board:`nucleo_g491re` (``nucleo_g491re``)
  * :zephyr:board:`nucleo_u545re_q` (``nucleo_u545re_q``)

* Sutajio Ko-Usagi PTE Ltd.

  * :zephyr:board:`tomu` (``tomu``)

* Texas Instruments

  * :zephyr:board:`lp_am13e230` (``lp_am13e230``)
  * :zephyr:board:`lp_am243` (``lp_am243``)
  * :zephyr:board:`lp_mspm33c321a` (``lp_mspm33c321a``)

* Trenz Electronic

  * :zephyr:board:`te0950` (``te0950``)

* Tuya Inc.

  * :zephyr:board:`tyzs3` (``tyzs3``)

* u-blox

  * :zephyr:board:`ubx_evknorab2` (``ubx_evknorab2``)

* Udoo

  * :zephyr:board:`udoo_key` (``udoo_key``)

* Umeta & Ikki Automotive Parts

  * :zephyr:board:`uiapduino_pro_micro_ch32v003` (``uiapduino_pro_micro_ch32v003``)

* VIEWE Display Co., Ltd.

  * :zephyr:board:`uedx24240013_md50e` (``uedx24240013_md50e``)
  * :zephyr:board:`uedx32480035e_wb_a` (``uedx32480035e_wb_a``)

* Waveshare Electronics

  * :zephyr:board:`esp32c6_lcd_1_47` (``esp32c6_lcd_1_47``)
  * :zephyr:board:`esp32p4_wifi6` (``esp32p4_wifi6``)
  * :zephyr:board:`esp32p4_wifi6_dev_kit` (``esp32p4_wifi6_dev_kit``)
  * :zephyr:board:`waveshare_esp32p4_eth` (``waveshare_esp32p4_eth``)

* WeAct Studio

  * :zephyr:board:`ch32v00x_core` (``ch32v00x_core``)
  * :zephyr:board:`usb2canfdv2` (``usb2canfdv2``)
  * :zephyr:board:`weact_ra4m1_core` (``weact_ra4m1_core``)

* WinChipHead

  * :zephyr:board:`ch32h417evt` (``ch32h417evt``)
  * :zephyr:board:`ch32v103evt` (``ch32v103evt``)
  * :zephyr:board:`ch32v203c8t6evt` (``ch32v203c8t6evt``)
  * :zephyr:board:`ch32v305f_evt_r0` (``ch32v305f_evt_r0``)

* WIZnet Co., Ltd.

  * :zephyr:board:`w55rp20_evb_pico` (``w55rp20_evb_pico``)
  * :zephyr:board:`w6100_evb_pico` (``w6100_evb_pico``)
  * :zephyr:board:`w6100_evb_pico2` (``w6100_evb_pico2``)
  * :zephyr:board:`w6300_evb_pico2` (``w6300_evb_pico2``)

新增扩展板
**********

..
  Same as above, this will also be recomputed at the time of the release.

* :ref:`AD-APARDPFW-SL 扩展板 <ad_apardpfw_sl>`
* :ref:`Adafruit FeatherWing MAX3421E 扩展板 <adafruit_featherwing_max3421e>`
* :ref:`Analog Devices 低速混合信号实验平台 <adi_lsmspg>`
* :ref:`ArduCam Mega SPI 摄像头扩展板 <arducam_mega>`
* :ref:`DFRobot Gravity TM6605 触觉电机驱动模块 <dfrobot_gravity_tm6605>`
* :ref:`EVAL-AD5529R-ARDZ 评估板 <eval_ad5529r_ardz>`
* :ref:`M5Stack Unit Gesture 手势传感器 <m5stack_unit_gesture_shield>`
* :ref:`M5Stack Unit Mini OLED 显示模块 <m5stack_unit_minioled_shield>`
* :ref:`MB1280 STMod+ 扇出扩展板 <mb1280_stmod_plus>`
* :ref:`MikroElektronika EERAM 3.3V Click 扩展板 <mikroe_eeram_33v_click_shield>`
* :ref:`MikroElektronika Two Wire ETH Click 扩展板 <mikroe_two_wire_eth_click_shield>`
* :ref:`NXP MX8 DSI OLED1A 面板 <nxp_mx8_dsi_oled1a>`
* :ref:`NXP MX9 DSI OLED 面板 <nxp_mx9_dsi_oled>`
* :ref:`OD-6010 SLCD 面板扩展板 <od_6010_shield>`
* :ref:`Seeed Studio 面向 XIAO 的 COB LED 驱动板 <seeed_xiao_cob_led>`
* :ref:`ST B-M2MEM-PACK1 M.2 串行存储扩展板 <st_b_m2mem_pack1_shield>`
* :ref:`X-NUCLEO-67W61M1：Wi-Fi 6 扩展板 <x_nucleo_67w61m1>`
* :ref:`X-NUCLEO-GNSS1A1：基于 Teseo-LIV3F 的 GNSS 扩展板 <x-nucleo-gnss1a1>`
* :ref:`X-NUCLEO-PGEEZ1 页式 EEPROM 扩展板 <x_nucleo_pgeez1_shield>`
* :ref:`X-NUCLEO-WBA25A1：BLE 扩展板 <x-nucleo-wba25a1>`

新增驱动
********

..
  Same as above, this will also be recomputed at the time of the release.
  Just link the driver, further details go in the binding description

* :abbr:`ADC (Analog to Digital Converter)`

  * :dtcompatible:`adi,ad4190-8-adc` (:github:`111922`)
  * :dtcompatible:`adi,ad4195-8-adc` (:github:`111922`)
  * :dtcompatible:`infineon,autanalog-sar-fifo` (:github:`110289`)
  * :dtcompatible:`infineon,autanalog-sar-fir` (:github:`110289`)
  * :dtcompatible:`m5stack,m5pm1-adc` (:github:`109961`)
  * :dtcompatible:`realtek,ameba-adc` (:github:`106677`)
  * :dtcompatible:`realtek,bee-adc` (:github:`105264`)
  * :dtcompatible:`ti,adc081c021` (:github:`114289`)
  * :dtcompatible:`ti,adc081c027` (:github:`114289`)
  * :dtcompatible:`ti,adc101c021` (:github:`114289`)
  * :dtcompatible:`ti,adc101c027` (:github:`114289`)
  * :dtcompatible:`ti,adc121c021` (:github:`114289`)
  * :dtcompatible:`ti,adc121c027` (:github:`114289`)
  * :dtcompatible:`ti,ads1118` (:github:`94152`)
  * :dtcompatible:`ti,ads1220` (:github:`102479`)
  * :dtcompatible:`ti,ads7828` (:github:`114359`)
  * :dtcompatible:`ti,ads7830` (:github:`114359`)
  * :dtcompatible:`ti,mspm0-adc12` (:github:`94736`)
  * :dtcompatible:`ti,tla2528-adc` (:github:`110722`)

* ARM 架构

  * :dtcompatible:`infineon,edge-npu` (:github:`106826`)
  * :dtcompatible:`nordic,nrf-wicr` (:github:`108141`)
  * :dtcompatible:`nordic,nrf71-uicr` (:github:`106134`)

* 音频

  * :dtcompatible:`st,stm32-dfsdm` (:github:`108302`)
  * :dtcompatible:`st,stm32-dfsdm-dmic` (:github:`108302`)
  * :dtcompatible:`ti,tas2563` (:github:`103148`)
  * :dtcompatible:`ti,tlv320aic26` (:github:`106836`)
  * :dtcompatible:`wolfson,wm8960` (:github:`106212`)
  * :dtcompatible:`zephyr,dummy-codec` (:github:`109891`)
  * :dtcompatible:`zephyr,native-sim-dmic` (:github:`109898`)

* 辅助显示

  * :dtcompatible:`nxp,slcd` (:github:`102796`)
  * :dtcompatible:`slcd-panel` (:github:`102796`)

* 蓝牙

  * :dtcompatible:`espressif,esp-hosted-mcu-bt-hci` (:github:`114532`)
  * :dtcompatible:`realtek,ameba-bt-hci` (:github:`109287`)

* 蜂鸣器

  * :dtcompatible:`gpio-buzzer` (:github:`108911`)
  * :dtcompatible:`pwm-buzzer` (:github:`108911`)

* :abbr:`CAN (Controller Area Network)`

  * :dtcompatible:`bflb,bl61x-can` (:github:`110672`)
  * :dtcompatible:`espressif,esp32-twaifd` (:github:`107680`)
  * :dtcompatible:`realtek,bee-can` (:github:`105411`)

* 充电器

  * :dtcompatible:`adi,adp5360-charger` (:github:`105258`)
  * :dtcompatible:`silergy,sy6974b` (:github:`107439`)
  * :dtcompatible:`ti,bq24295` (:github:`114650`)
  * :dtcompatible:`ti,bq24296` (:github:`114650`)
  * :dtcompatible:`ti,bq24296m` (:github:`114650`)
  * :dtcompatible:`ti,bq24297` (:github:`114650`)
  * :dtcompatible:`ti,bq24298` (:github:`114650`)

* 时钟控制

  * :dtcompatible:`aesc,clock-controller` (:github:`116703`)
  * :dtcompatible:`bflb,bl616cl-clock-controller` (:github:`112738`)
  * :dtcompatible:`bflb,bl808-clock-controller` (:github:`105580`)
  * :dtcompatible:`bflb,mm-clk` (:github:`105580`)
  * :dtcompatible:`microchip,pic32cm-sg-gc-clock` (:github:`112582`)
  * :dtcompatible:`microchip,pic32cm-sg-gc-dfll48m` (:github:`112582`)
  * :dtcompatible:`microchip,pic32cm-sg-gc-dpll` (:github:`112582`)
  * :dtcompatible:`microchip,pic32cm-sg-gc-gclkgen` (:github:`112582`)
  * :dtcompatible:`microchip,pic32cm-sg-gc-gclkperiph` (:github:`112582`)
  * :dtcompatible:`microchip,pic32cm-sg-gc-mclkdomain` (:github:`112582`)
  * :dtcompatible:`microchip,pic32cm-sg-gc-mclkperiph` (:github:`112582`)
  * :dtcompatible:`microchip,pic32cm-sg-gc-rtc` (:github:`112582`)
  * :dtcompatible:`microchip,pic32cm-sg-gc-xosc` (:github:`112582`)
  * :dtcompatible:`microchip,pic32cm-sg-gc-xosc32k` (:github:`112582`)
  * :dtcompatible:`microchip,smartfusion2-clock` (:github:`106926`)
  * :dtcompatible:`nordic,nrf-clock-hfclk` (:github:`104658`)
  * :dtcompatible:`nordic,nrf-clock-hfclk192m` (:github:`104658`)
  * :dtcompatible:`nordic,nrf-clock-hfclkaudio` (:github:`104658`)
  * :dtcompatible:`nordic,nrf-clock-lfclk` (:github:`104658`)
  * :dtcompatible:`nordic,nrf-clock-xo` (:github:`104658`)
  * :dtcompatible:`nordic,nrf-clock-xo24m` (:github:`104658`)
  * :dtcompatible:`nuvoton,m4-hclk-clock` (:github:`103668`)
  * :dtcompatible:`nuvoton,m4-hxt-clock` (:github:`103668`)
  * :dtcompatible:`nuvoton,m4-lxt-clock` (:github:`103668`)
  * :dtcompatible:`nuvoton,m4-pll-clock` (:github:`103668`)
  * :dtcompatible:`nuvoton,numicro-m4-pcc` (:github:`103668`)
  * :dtcompatible:`nuvoton,numicro-m4-scc` (:github:`103668`)
  * :dtcompatible:`nxp,imxrt118x-arm-pll` (:github:`106881`)
  * :dtcompatible:`nxp,imxrt11xx-arm-pll` (:github:`106881`)
  * :dtcompatible:`nxp,lpc84x-clock` (:github:`105928`)
  * :dtcompatible:`nxp,mcxw7x-clock` (:github:`101937`)
  * :dtcompatible:`silabs,series0-cmu` (:github:`111754`)
  * :dtcompatible:`silabs,series0-hfxo` (:github:`111754`)
  * :dtcompatible:`silabs,series0-lfrco` (:github:`111754`)
  * :dtcompatible:`silabs,series0-lfxo` (:github:`111754`)
  * :dtcompatible:`st,stm32h5-pll-clock` (:github:`110914`)
  * :dtcompatible:`st,stm32n6-msi-clock` (:github:`108997`)
  * :dtcompatible:`wch,ch32h41x-pll-clock` (:github:`111725`)

* 时钟监视器

  * :dtcompatible:`nxp,cmu-fc` (:github:`107879`)
  * :dtcompatible:`nxp,cmu-fm` (:github:`107879`)
  * :dtcompatible:`nxp,freqme` (:github:`112403`)

* 比较器

  * :dtcompatible:`espressif,esp32-ana-cmpr` (:github:`113625`)
  * :dtcompatible:`infineon,autanalog-ptcomp-comp` (:github:`107488`)
  * :dtcompatible:`infineon,hppass-csg-comp` (:github:`109879`)
  * :dtcompatible:`infineon,lp-comp` (:github:`104636`)
  * :dtcompatible:`infineon,lp-comp-channel` (:github:`104636`)
  * :dtcompatible:`ti,mspm0-comparator` (:github:`94737`)

* 计数器

  * :dtcompatible:`arm,crsas-ma2-counter` (:github:`112815`)
  * :dtcompatible:`arm,crsas-ma2-timer` (:github:`112815`)
  * :dtcompatible:`nxp,irtc-wake-timer` (:github:`111552`)
  * :dtcompatible:`nxp,sysctr` (:github:`106300`)
  * :dtcompatible:`nxp,tstmr` (:github:`112255`)
  * :dtcompatible:`nxp,wake-timer` (:github:`110811`)
  * :dtcompatible:`realtek,ameba-counter` (:github:`106664`)
  * :dtcompatible:`realtek,bee-counter-rtc` (:github:`105193`)
  * :dtcompatible:`ti,k3-rtc-counter` (:github:`104048`)
  * :dtcompatible:`wch,adtm` (:github:`109728`)
  * :dtcompatible:`xlnx,ttc` (:github:`103117`)
  * :dtcompatible:`xlnx,ttc-counter` (:github:`103117`)
  * :dtcompatible:`xlnx,zynqmp-rtc` (:github:`107684`)

* :abbr:`CPU (Central Processing Unit)`

  * :dtcompatible:`adi,max32-m4f-cpu1` (:github:`105310`)
  * :dtcompatible:`arm,armv8` (:github:`114145`)
  * :dtcompatible:`arm,cortex-a32` (:github:`107644`)
  * :dtcompatible:`arm,cortex-a57` (:github:`114109`)
  * :dtcompatible:`arm,cortex-a720` (:github:`113087`)
  * :dtcompatible:`arm,cortex-r8f` (:github:`114145`)
  * :dtcompatible:`intel,nova-lake` (:github:`111818`)
  * :dtcompatible:`intel,x86_64` (:github:`115174`)
  * :dtcompatible:`spinalhdl,vexiiriscv` (:github:`109932`)
  * :dtcompatible:`wch,qingke-v3c` (:github:`111171`)
  * :dtcompatible:`wch,qingke-v3f` (:github:`111725`)
  * :dtcompatible:`wch,qingke-v5f` (:github:`111725`)

* :abbr:`CPU (Central Processing Unit)` 频率调节

  * :dtcompatible:`zephyr,cpu-freq-thermal-cap` (:github:`108242`)

* :abbr:`CRC (Cyclic Redundancy Check)`

  * :dtcompatible:`ambiq,hw-crc32` (:github:`110366`)

* 加密加速器

  * :dtcompatible:`infineon,mxcrypto-crypto` (:github:`108439`)
  * :dtcompatible:`infineon,mxcrypto-trng` (:github:`108439`)
  * :dtcompatible:`infineon,mxcryptolite-crypto` (:github:`109693`)
  * :dtcompatible:`infineon,mxcryptolite-trng` (:github:`109693`)
  * :dtcompatible:`realtek,bee-aes` (:github:`114817`)
  * :dtcompatible:`realtek,bee-sha256` (:github:`114817`)
  * :dtcompatible:`ti,mspm0-aes` (:github:`94734`)

* :abbr:`DAC (Digital to Analog Converter)`

  * :dtcompatible:`adi,ad5529r` (:github:`106256`)
  * :dtcompatible:`infineon,autanalog-ctdac` (:github:`107490`)
  * :dtcompatible:`infineon,hppass-csg-dac` (:github:`109967`)
  * :dtcompatible:`microchip,dac-g2` (:github:`109820`)
  * :dtcompatible:`ti,dac43508` (:github:`112038`)
  * :dtcompatible:`ti,dac53508` (:github:`112038`)
  * :dtcompatible:`ti,dac63508` (:github:`112038`)
  * :dtcompatible:`ti,mspm0-dac` (:github:`94725`)

* :abbr:`DAI (Digital Audio Interface)`

  * :dtcompatible:`amd,acp-sdw-dai` (:github:`104450`)
  * :dtcompatible:`amd,tdm-dai` (:github:`108314`)

* :abbr:`DALI (Digital Addressable Lighting Interface)`

  * :dtcompatible:`zephyr,dali-pwm` (:github:`88128`)

* 磁盘

  * :dtcompatible:`virtio,blk` (:github:`112581`)
  * :dtcompatible:`zephyr,memc-ram-disk` (:github:`111528`)

* 显示

  * :dtcompatible:`charlieplex-led-matrix` (:github:`110137`)
  * :dtcompatible:`chipwealth,ch1115` (:github:`107434`)
  * :dtcompatible:`chipwealth,ch1116` (:github:`107434`)
  * :dtcompatible:`eink,ed2208-doa` (:github:`109961`)
  * :dtcompatible:`eink,ed2208-gca` (:github:`107510`)
  * :dtcompatible:`fitipower,ek79007` (:github:`116543`)
  * :dtcompatible:`himax,hx8353e` (:github:`108055`)
  * :dtcompatible:`ite,it8951` (:github:`108591`)
  * :dtcompatible:`levetop,lt7680` (:github:`112389`)
  * :dtcompatible:`raspberrypi,bcm2711-framebuffer` (:github:`109522`)
  * :dtcompatible:`raydium,rm67199` (:github:`98554`)
  * :dtcompatible:`raydium,rm692c9` (:github:`93134`)
  * :dtcompatible:`sinowealth,sh1107` (:github:`107434`)
  * :dtcompatible:`socionext,dpu` (:github:`93134`)
  * :dtcompatible:`solomon,ssd1305` (:github:`107434`)
  * :dtcompatible:`solomon,ssd1306b` (:github:`107434`)
  * :dtcompatible:`solomon,ssd1315` (:github:`107434`)
  * :dtcompatible:`solomon,ssd1683` (:github:`112893`)
  * :dtcompatible:`st,neochrom-gpu2d` (:github:`105970`)
  * :dtcompatible:`st,stm32-dma2d` (:github:`103687`)
  * :dtcompatible:`ultrachip,uc8253` (:github:`113230`)
  * :dtcompatible:`zephyr,panel-color-palette` (:github:`107945`)

* :abbr:`DMA (Direct Memory Access)`

  * :dtcompatible:`amd,acp-host-dma` (:github:`104450`)
  * :dtcompatible:`amd,acp-sdw-dma` (:github:`104450`)
  * :dtcompatible:`amd,acp-tdm-dma` (:github:`108314`)
  * :dtcompatible:`amd,versal2-dma-1.0` (:github:`101685`)
  * :dtcompatible:`infineon,mdma` (:github:`110847`)
  * :dtcompatible:`microchip,dmac-g3-dma` (:github:`109209`)
  * :dtcompatible:`nxp,gdma` (:github:`104868`)
  * :dtcompatible:`realtek,ameba-gdma` (:github:`105366`)
  * :dtcompatible:`realtek,bee-dma` (:github:`104754`)
  * :dtcompatible:`renesas,rza2m-dma` (:github:`107009`)
  * :dtcompatible:`ti,mspm0-dma` (:github:`91502`)
  * :dtcompatible:`xlnx,zynqmp-dma-1.0` (:github:`101685`)

* :abbr:`DSP (Digital Signal Processor)`

  * :dtcompatible:`nxp,powerquad` (:github:`110745`)

* :abbr:`EDAC (Error Detection and Correction)`

  * :dtcompatible:`nxp,mecc` (:github:`105341`)

* :abbr:`ESPI (Enhanced Serial Peripheral Interface)`

  * :dtcompatible:`intel,espi-peci` (:github:`103773`)

* 以太网

  * :dtcompatible:`brcm,genet` (:github:`113360`)
  * :dtcompatible:`brcm,genet-mdio` (:github:`113360`)
  * :dtcompatible:`microchip,gmac-g1-eth` (:github:`105275`)
  * :dtcompatible:`microchip,gmac-g1-mdio` (:github:`105275`)
  * :dtcompatible:`microchip,lan8840` (:github:`110896`)
  * :dtcompatible:`nxp,imx-netc-vsi` (:github:`114331`)
  * :dtcompatible:`snps,dwmac` (:github:`114760`)
  * :dtcompatible:`snps,dwmac-mdio` (:github:`108046`)
  * :dtcompatible:`snps,dwmac-ptp-clock` (:github:`114242`)
  * :dtcompatible:`wch,ch9120` (:github:`111708`)
  * :dtcompatible:`wiznet,w5100s` (:github:`113315`)
  * :dtcompatible:`wiznet,w6300` (:github:`102727`)
  * :dtcompatible:`xlnx,gem-mdio` (:github:`87313`)
  * :dtcompatible:`zephyr,native-ptp-clock` (:github:`109265`)

* 固件

  * :dtcompatible:`arm,scmi-reset` (:github:`106306`)
  * :dtcompatible:`raspberrypi,bcm283x-firmware` (:github:`107536`)

* Flash 控制器

  * :dtcompatible:`aesc,spi-flash-controller` (:github:`110957`)
  * :dtcompatible:`infineon,rram-controller` (:github:`108532`)
  * :dtcompatible:`intel,pflash-cfi01` (:github:`112714`)
  * :dtcompatible:`microchip,igloo2-envm-controller` (:github:`111817`)
  * :dtcompatible:`microchip,nvmctrl-g2` (:github:`108440`)
  * :dtcompatible:`microchip,nvmctrl-g3` (:github:`109747`)
  * :dtcompatible:`microchip,smartfusion2-flash-controller` (:github:`106926`)
  * :dtcompatible:`nxp,iap-fmc84x` (:github:`105928`)
  * :dtcompatible:`realtek,ameba-flash-controller` (:github:`106690`)
  * :dtcompatible:`realtek,bee-nor-flash-controller` (:github:`107007`)

* :abbr:`FPGA (Field Programmable Gate Array)`

  * :dtcompatible:`renesas,slg47910` (:github:`107551`)

* 电量计

  * :dtcompatible:`adi,adp5360-fuel-gauge` (:github:`105258`)

* :abbr:`GNSS (Global Navigation Satellite System)`

  * :dtcompatible:`ericsson,f5521gw` (:github:`113055`)
  * :dtcompatible:`u-blox,m10` (:github:`110846`)

* :abbr:`GPIO (General Purpose Input/Output)` 与排针

  * :dtcompatible:`allwinner,sun50i-h618-gpio` (:github:`110502`)
  * :dtcompatible:`allwinner,sunxi-gpio` (:github:`110502`)
  * :dtcompatible:`arduino-mega-header` (:github:`105160`)
  * :dtcompatible:`diodes,pi4ioe5v6408` (:github:`108505`)
  * :dtcompatible:`esp-01-header` (:github:`109705`)
  * :dtcompatible:`gpio-mmio-latch` (:github:`105732`)
  * :dtcompatible:`m5stack,m5pm1-gpio` (:github:`109961`)
  * :dtcompatible:`nordic,npm10xx-gpio` (:github:`108508`)
  * :dtcompatible:`raspberrypi,bcm283x-gpio` (:github:`110788`)
  * :dtcompatible:`realtek,rts5817-gpio` (:github:`105542`)
  * :dtcompatible:`st,m2-memory-connector` (:github:`109004`)
  * :dtcompatible:`st,stmod-plus-connector` (:github:`109705`)
  * :dtcompatible:`st-zio-header` (:github:`115412`)
  * :dtcompatible:`ti,tca9554` (:github:`111041`)
  * :dtcompatible:`ti,tla2528-gpio` (:github:`110722`)
  * :dtcompatible:`virtio,gpio` (:github:`114983`)
  * :dtcompatible:`wch,ch5xx-gpio` (:github:`111171`)

* 触觉反馈

  * :dtcompatible:`cirrus,cs40l26` (:github:`106934`)
  * :dtcompatible:`cirrus,cs40l27` (:github:`106934`)
  * :dtcompatible:`cirrus,cs40l50` (:github:`105683`)
  * :dtcompatible:`cirrus,cs40l51` (:github:`105683`)
  * :dtcompatible:`cirrus,cs40l52` (:github:`105683`)
  * :dtcompatible:`cirrus,cs40l53` (:github:`105683`)
  * :dtcompatible:`titanmec,tm6605` (:github:`109104`)

* 硬件信息

  * :dtcompatible:`nxp,lpc-pmc-hwinfo` (:github:`114693`)
  * :dtcompatible:`nxp,mc-rgm` (:github:`111359`)
  * :dtcompatible:`nxp,otp-uid` (:github:`111493`)
  * :dtcompatible:`zephyr,hwinfo-nvmem` (:github:`118693`)

* :abbr:`I2C (Inter-Integrated Circuit)`

  * :dtcompatible:`ambiq,ios-i2c` (:github:`96059`)
  * :dtcompatible:`brcm,bcm2711-i2c` (:github:`105601`)
  * :dtcompatible:`ene,kb106x-i2c` (:github:`106693`)
  * :dtcompatible:`realtek,ameba-i2c` (:github:`108235`)
  * :dtcompatible:`realtek,bee-i2c` (:github:`105028`)
  * :dtcompatible:`zephyr,i2c-target-tmp103` (:github:`114727`)

* :abbr:`I2S (Inter-Integrated Circuit Sound)`

  * :dtcompatible:`zephyr,native-sim-i2s` (:github:`109902`)

* :abbr:`I3C (Improved Inter-Integrated Circuit)`

  * :dtcompatible:`microchip,xec-i3c` (:github:`116252`)

* IEEE 802.15.4

  * :dtcompatible:`silabs,efr32-ieee802154` (:github:`108596`)

* 输入

  * :dtcompatible:`tbs,crsf` (:github:`106941`)
  * :dtcompatible:`virtio,input` (:github:`111029`)

* 中断控制器

  * :dtcompatible:`amd,acp-intc` (:github:`104450`)
  * :dtcompatible:`brcm,bcm2835-armctrl-ic` (:github:`110189`)
  * :dtcompatible:`brcm,bcm2836-l1-intc` (:github:`110189`)
  * :dtcompatible:`microchip,smartfusion2-h2f-irqctrl` (:github:`106926`)

* :abbr:`IPC (Inter-Processor Communication)`

  * :dtcompatible:`nxp,ipc-rpmsg-lite` (:github:`104807`)

* :abbr:`LED (Light Emitting Diode)`

  * :dtcompatible:`issi,is31fl3193` (:github:`107555`)
  * :dtcompatible:`nordic,npm10xx-led` (:github:`108756`)
  * :dtcompatible:`nxp,pca9530` (:github:`112203`)
  * :dtcompatible:`nxp,pca9531` (:github:`112203`)
  * :dtcompatible:`nxp,pca9532` (:github:`112203`)
  * :dtcompatible:`ti,lp5860` (:github:`108801`)
  * :dtcompatible:`ti,lp5861` (:github:`108801`)
  * :dtcompatible:`ti,lp5862` (:github:`108801`)
  * :dtcompatible:`ti,lp5864` (:github:`108801`)
  * :dtcompatible:`ti,lp5866` (:github:`108801`)
  * :dtcompatible:`ti,lp5868` (:github:`108801`)
  * :dtcompatible:`zephyr,fake-leds` (:github:`110819`)
  * :dtcompatible:`zephyr,native-linux-leds` (:github:`111189`)

* :abbr:`LED (Light Emitting Diode)` 灯带

  * :dtcompatible:`worldsemi,ws2812-bflb-wo` (:github:`105325`)
  * :dtcompatible:`worldsemi,ws2812-pulse-io` (:github:`110466`)

* LoRa

  * :dtcompatible:`semtech,lr1121` (:github:`109912`)

* 邮箱

  * :dtcompatible:`arm,mhuv2` (:github:`110686`)
  * :dtcompatible:`brcm,bcm2711-mbox` (:github:`107536`)
  * :dtcompatible:`renesas,rcar-mfis-mbox` (:github:`108868`)

* MCUmgr

  * :dtcompatible:`zephyr,smp-spi` (:github:`106947`)

* 内存控制器

  * :dtcompatible:`bflb,bl808-psram-uhs` (:github:`110702`)
  * :dtcompatible:`bflb,bl808-psram-uhs-controller` (:github:`110702`)
  * :dtcompatible:`bflb,sf-bank` (:github:`107223`)
  * :dtcompatible:`bflb,sf-controller` (:github:`107223`)
  * :dtcompatible:`nxp,imx-snvs-gpr` (:github:`109842`)

* 其他

  * :dtcompatible:`adi,tmc6460` (:github:`113438`)
  * :dtcompatible:`nxp,imx93-video-pll` (:github:`98554`)
  * :dtcompatible:`nxp,mcxw-hw-params` (:github:`108974`)
  * :dtcompatible:`ti,tdp2004` (:github:`111950`)

* 调制解调器

  * :dtcompatible:`fibocom,le250` (:github:`114755`)
  * :dtcompatible:`nordic,nrf91-sm-v2` (:github:`115058`)
  * :dtcompatible:`nordic,nrf93m1` (:github:`106289`)
  * :dtcompatible:`quectel,bc66` (:github:`111279`)
  * :dtcompatible:`quectel,bc660k` (:github:`111279`)
  * :dtcompatible:`quectel,bc66x` (:github:`111279`)
  * :dtcompatible:`quectel,eg21-g` (:github:`115561`)
  * :dtcompatible:`quectel,eg915u` (:github:`95921`)
  * :dtcompatible:`telit,le910c1tx` (:github:`106716`)
  * :dtcompatible:`telit,lex10q1` (:github:`109206`)
  * :dtcompatible:`trasna,lexi-r10` (:github:`107308`)

* :abbr:`MTD (Memory Technology Device)`

  * :dtcompatible:`bflb,sf-device` (:github:`107223`)
  * :dtcompatible:`bflb,sf-flash` (:github:`107223`)
  * :dtcompatible:`is66wv` (:github:`111074`)
  * :dtcompatible:`microchip,flash-g2` (:github:`108440`)
  * :dtcompatible:`microchip,flash-g3` (:github:`109747`)
  * :dtcompatible:`nordic,tz-nonsecure` (:github:`108883`)
  * :dtcompatible:`nordic,tz-secure` (:github:`108883`)
  * :dtcompatible:`nxp,imx-flexspi-nand` (:github:`104870`)
  * :dtcompatible:`nxp,mcxw-ifr` (:github:`108974`)
  * :dtcompatible:`realtek,bee-nor-flash` (:github:`107007`)

* 多比特 :abbr:`SPI (Serial Peripheral Interface)`

  * :dtcompatible:`microchip,xec-qmspi-controller` (:github:`113243`)
  * :dtcompatible:`microchip,xec-qmspi-device` (:github:`113243`)
  * :dtcompatible:`st,nor` (:github:`113368`)
  * :dtcompatible:`st,psram-device` (:github:`105219`)
  * :dtcompatible:`zephyr,peripheral-device` (:github:`103754`)

* 多功能设备

  * :dtcompatible:`ambiq,ios` (:github:`96059`)
  * :dtcompatible:`infineon,autanalog` (:github:`106227`)
  * :dtcompatible:`infineon,autanalog-ac-state` (:github:`106227`)
  * :dtcompatible:`infineon,autanalog-ctb` (:github:`107489`)
  * :dtcompatible:`infineon,autanalog-prb` (:github:`107487`)
  * :dtcompatible:`infineon,autanalog-ptcomp` (:github:`107488`)
  * :dtcompatible:`infineon,hppass-ac-state` (:github:`109196`)
  * :dtcompatible:`infineon,hppass-analog` (:github:`109196`)
  * :dtcompatible:`infineon,hppass-csg` (:github:`109694`)
  * :dtcompatible:`infineon,mxcrypto` (:github:`108439`)
  * :dtcompatible:`infineon,mxcryptolite` (:github:`109693`)
  * :dtcompatible:`m5stack,m5pm1` (:github:`109961`)
  * :dtcompatible:`ti,tla2528` (:github:`110722`)

* :abbr:`MUX (Multiplexer)`

  * :dtcompatible:`adi,adgm3121` (:github:`112088`)
  * :dtcompatible:`adi,adgm3121-gpio` (:github:`112088`)
  * :dtcompatible:`gpio-mux` (:github:`112088`)
  * :dtcompatible:`nxp,inputmux` (:github:`109379`)
  * :dtcompatible:`nxp,trgmux` (:github:`112088`)

* 网络

  * gPTP

    * :kconfig:option:`CONFIG_NET_GPTP_STATIC_TIME_RECEIVER` 将该节点作为静态配置的时间接收端运行，使其可以通过不发送 Announce 消息的 IEEE 802.1AS 车载配置文件（automotive profile）网桥进行同步。

  * :dtcompatible:`st,stm32wba-radio` (:github:`110546`)

* :abbr:`OPAMP (Operational Amplifier)`

  * :dtcompatible:`infineon,autanalog-ctb-opamp` (:github:`107489`)

* :abbr:`OTP (One-Time Programmable)` 存储器

  * :dtcompatible:`adi,axi-sysid` (:github:`115280`)
  * :dtcompatible:`nxp,otpc` (:github:`111707`)
  * :dtcompatible:`nxp,rt7xx-ocotp` (:github:`108075`)
  * :dtcompatible:`realtek,rts5817-ocotp` (:github:`111141`)

* :abbr:`PCIe (Peripheral Component Interconnect Express)`

  * :dtcompatible:`brcm,iproc-pcie-ep-v2` (:github:`111490`)

* PHY

  * :dtcompatible:`st,stm32f7-usbphyc` (:github:`114696`)
  * :dtcompatible:`st,stm32n6-usbphyc` (:github:`114696`)

* 引脚控制

  * :dtcompatible:`aesc,pinctrl` (:github:`108137`)
  * :dtcompatible:`arm,v2m_musca_b1-pinctrl` (:github:`114671`)
  * :dtcompatible:`elan,em32-pinctrl` (:github:`103037`)
  * :dtcompatible:`nxp,lpc84x-iocon` (:github:`105928`)
  * :dtcompatible:`nxp,lpc84x-swm` (:github:`105928`)
  * :dtcompatible:`renesas,rcar-pfc-x5h` (:github:`108871`)
  * :dtcompatible:`wch,ch570-pinctrl` (:github:`111171`)
  * :dtcompatible:`wch,h41x-afio` (:github:`111725`)

* 电源域

  * :dtcompatible:`raspberrypi,bcm283x-power` (:github:`112918`)

* 电源管理

  * :dtcompatible:`microchip,supc-g1` (:github:`115872`)
  * :dtcompatible:`nxp,smc` (:github:`102228`)
  * :dtcompatible:`sifli,sf32lb52x-pmuc` (:github:`108093`)
  * :dtcompatible:`st,stm32-pwr-wkupctrl` (:github:`114092`)
  * :dtcompatible:`st,stm32f1-pwr-wkupctrl` (:github:`114092`)
  * :dtcompatible:`st,stm32f7-pwr-wkupctrl` (:github:`114092`)

* 脉冲 IO

  * :dtcompatible:`espressif,esp32-rmt` (:github:`110466`)
  * :dtcompatible:`zephyr,pulse-io-loopback` (:github:`110466`)

* :abbr:`PWM (Pulse Width Modulation)`

  * :dtcompatible:`realtek,ameba-pwm` (:github:`106669`)
  * :dtcompatible:`realtek,bee-pwm` (:github:`105014`)
  * :dtcompatible:`ti,am3352-ecap` (:github:`88860`)
  * :dtcompatible:`ti,am3352-ehrpwm` (:github:`88757`)
  * :dtcompatible:`wch,adtm-pwm` (:github:`109728`)
  * :dtcompatible:`zephyr,pwm-bitbang` (:github:`106536`)

* 稳压器

  * :dtcompatible:`gd,gd32-bldo` (:github:`106501`)
  * :dtcompatible:`infineon,autanalog-prb-vref` (:github:`107487`)
  * :dtcompatible:`m5stack,m5pm1-regulator` (:github:`109961`)
  * :dtcompatible:`realtek,rts5817-regulator` (:github:`108545`)
  * :dtcompatible:`sifli,sf32lb52x-ldo` (:github:`108093`)
  * :dtcompatible:`ti,mspm0-vref` (:github:`94732`)

* 复位控制器

  * :dtcompatible:`wch,ch32-rcc-rctl` (:github:`115714`)

* 保持内存

  * :dtcompatible:`gd,gd32-backup-sram` (:github:`106501`)

* :abbr:`RNG (Random Number Generator)`

  * :dtcompatible:`brcm,bcm2835-rng` (:github:`110191`)
  * :dtcompatible:`microchip,trng-g2-entropy` (:github:`108155`)
  * :dtcompatible:`realtek,ameba-trng` (:github:`106670`)
  * :dtcompatible:`realtek,bee-trng` (:github:`105335`)

* :abbr:`RTC (Real Time Clock)`

  * :dtcompatible:`ite,it8xxx2-rtc` (:github:`106350`)
  * :dtcompatible:`microchip,rtc-mss` (:github:`110842`)
  * :dtcompatible:`microchip,xec-hibtimer` (:github:`111476`)
  * :dtcompatible:`microchip,xec-rtc` (:github:`106116`)
  * :dtcompatible:`microcrystal,rv3028-rtc` (:github:`112978`)
  * :dtcompatible:`nxp,rtc-analog` (:github:`107196`)
  * :dtcompatible:`realtek,ameba-rtc` (:github:`105376`)

* :abbr:`SDHC (Secure Digital High Capacity)`

  * :dtcompatible:`bflb,sdhc` (:github:`105243`)
  * :dtcompatible:`microchip,sdhc-g1` (:github:`109211`)
  * :dtcompatible:`nuvoton,numaker-sdhc` (:github:`105437`)
  * :dtcompatible:`realtek,ameba-sdhost` (:github:`106687`)
  * :dtcompatible:`ti,am654-sdhci` (:github:`97172`)

* 传感器

  * :dtcompatible:`adi,adis1647x` (:github:`110012`)
  * :dtcompatible:`adi,adxl313` (:github:`114936`)
  * :dtcompatible:`adi,ltc4286` (:github:`105618`)
  * :dtcompatible:`adi,max30009` (:github:`112988`)
  * :dtcompatible:`bflb,tsen` (:github:`107717`)
  * :dtcompatible:`hamamatsu,s9706` (:github:`107607`)
  * :dtcompatible:`invensense,icm56622` (:github:`112362`)
  * :dtcompatible:`invensense,icm56686` (:github:`112362`)
  * :dtcompatible:`invensense,tad2144` (:github:`107994`)
  * :dtcompatible:`maxim,max30102` (:github:`108697`)
  * :dtcompatible:`maxim,max31826` (:github:`112398`)
  * :dtcompatible:`meas,htu21d` (:github:`106318`)
  * :dtcompatible:`meas,htu31d` (:github:`107532`)
  * :dtcompatible:`meas,ms5637` (:github:`106344`)
  * :dtcompatible:`microchip,pac194x` (:github:`105902`)
  * :dtcompatible:`nordic,nrf-vbat` (:github:`106102`)
  * :dtcompatible:`nxp,mcux-eqdc` (:github:`111927`)
  * :dtcompatible:`plantower,pmsa003i` (:github:`113377`)
  * :dtcompatible:`raspberrypi,bcm283x-vc-thermal` (:github:`110192`)
  * :dtcompatible:`realtek,bee-aon-qdec` (:github:`105129`)
  * :dtcompatible:`realtek,bee-basic-qdec` (:github:`105129`)
  * :dtcompatible:`realtek,bee-qdec` (:github:`105129`)
  * :dtcompatible:`sensylink,cht8315` (:github:`106391`)
  * :dtcompatible:`st,stm32-vddcore` (:github:`108053`)
  * :dtcompatible:`ti,fdc1004` (:github:`107233`)
  * :dtcompatible:`ti,tmp451` (:github:`108384`)
  * :dtcompatible:`zephyr,flow-meter` (:github:`111366`)
  * :dtcompatible:`zephyr,native-linux-temp` (:github:`114563`)

* 串行控制器

  * :dtcompatible:`elan,em32-uart` (:github:`103037`)
  * :dtcompatible:`microchip,uart-g1` (:github:`114034`)
  * :dtcompatible:`nxp,lpc84x-uart` (:github:`105928`)
  * :dtcompatible:`shakti,uart` (:github:`113000`)
  * :dtcompatible:`wch,ch5xx-uart` (:github:`111171`)
  * :dtcompatible:`wch,sdi-console` (:github:`109777`)

* :abbr:`SMbus (System Management Bus)`

  * :dtcompatible:`ite,it51xxx-smbus` (:github:`114832`)

* :abbr:`SPI (Serial Peripheral Interface)`

  * :dtcompatible:`microchip,flexcom-g1-spi` (:github:`107467`)
  * :dtcompatible:`nuvoton,numaker-usci-spi` (:github:`109123`)
  * :dtcompatible:`realtek,ameba-spi` (:github:`108234`)
  * :dtcompatible:`realtek,bee-spi` (:github:`104958`)
  * :dtcompatible:`realtek,rts5817-spi` (:github:`106346`)
  * :dtcompatible:`renesas,rz-spi-b` (:github:`107073`)
  * :dtcompatible:`ti,mspm0-spi` (:github:`94726`)
  * :dtcompatible:`xlnx,zynqmp-qspi-1.0` (:github:`88466`)

* 转速计

  * :dtcompatible:`ene,kb106x-tach` (:github:`106739`)

* 定时器

  * :dtcompatible:`microchip,pit-g1-timer` (:github:`114034`)
  * :dtcompatible:`st,stm32u5-lptim` (:github:`112400`)
  * :dtcompatible:`ti,am26-rtitimer` (:github:`102545`)

* :abbr:`USB (Universal Serial Bus)`

  * :dtcompatible:`espressif,esp32-usb-otg-fs` (:github:`111508`)
  * :dtcompatible:`espressif,esp32-usb-otg-hs` (:github:`111508`)
  * :dtcompatible:`infineon,usbhs` (:github:`106841`)
  * :dtcompatible:`microchip,udphs-g1-udc` (:github:`99620`)
  * :dtcompatible:`nordic,nrf-usbhs-bc12` (:github:`106759`)

* 唤醒控制器

  * :dtcompatible:`nxp,sleepcon-wuc` (:github:`113447`)
  * :dtcompatible:`nxp,wuc-wuu` (:github:`100866`)

* 看门狗

  * :dtcompatible:`arm,crsas-ma2-watchdog` (:github:`112700`)
  * :dtcompatible:`m5stack,m5pm1-wdt` (:github:`109961`)
  * :dtcompatible:`nordic,npm10xx-wdt` (:github:`109381`)
  * :dtcompatible:`nordic,nrf-gswdt` (:github:`110067`)
  * :dtcompatible:`nuvoton,numaker-wdt` (:github:`105247`)
  * :dtcompatible:`realtek,ameba-watchdog` (:github:`106672`)
  * :dtcompatible:`realtek,bee-core-wdt` (:github:`107021`)
  * :dtcompatible:`ti,mspm0-watchdog` (:github:`95304`)

* Wi-Fi

  * :dtcompatible:`bflb,wifi6` (:github:`113078`)
  * :dtcompatible:`espressif,esp-hosted-mcu` (:github:`114532`)
  * :dtcompatible:`espressif,esp-hosted-mcu-wifi` (:github:`114532`)
  * :dtcompatible:`realtek,ameba-wifi` (:github:`105614`)
  * :dtcompatible:`st,st67w611m1` (:github:`111583`)
  * :dtcompatible:`zephyr,wifi-hwsim` (:github:`111236`)

新增示例
********

..
  Same as above, this will also be recomputed at the time of the release.
  Just link the sample, further details go in the sample documentation itself.

* :zephyr:code-sample:`adi-gpio-wakeup`
* :zephyr:code-sample:`adi-pm`
* :zephyr:code-sample:`autanalog_fir_fifo`
* :zephyr:code-sample:`bluetooth_cap_handover`
* :zephyr:code-sample:`buzzer-tone`
* :zephyr:code-sample:`coap-client-tcp`
* :zephyr:code-sample:`color-palette`
* :zephyr:code-sample:`coredump-udp-demo-shell`
* :zephyr:code-sample:`coresight_stm_shell`
* :zephyr:code-sample:`cpu_freq_thermal_cap`
* :zephyr:code-sample:`cpu_freq_timing_noise`
* :zephyr:code-sample:`cs40l26`
* :zephyr:code-sample:`dali`
* :zephyr:code-sample:`dhcpv6-pd`
* :zephyr:code-sample:`esp32-qdec-trigger`
* :zephyr:code-sample:`espnow`
* :zephyr:code-sample:`fido2`
* :zephyr:code-sample:`flow-meter`
* :zephyr:code-sample:`frdm-mcxe31b-system-off`
* :zephyr:code-sample:`i2c-tiny-usb`
* :zephyr:code-sample:`logging_multidomain`
* :zephyr:code-sample:`lora-duty-cycle`
* :zephyr:code-sample:`lp586x`
* :zephyr:code-sample:`mcp-server-hello-world`
* :zephyr:code-sample:`mfd_charger`
* :zephyr:code-sample:`mspi-throughput`
* :zephyr:code-sample:`net-rtp`
* :zephyr:code-sample:`nrf-sys-event`
* :zephyr:code-sample:`nxp_mcx_s2ram`
* :zephyr:code-sample:`nxp_mcx_system_off`
* :zephyr:code-sample:`nxp_smartdma_mem_to_mem`
* :zephyr:code-sample:`pm-latency`
* :zephyr:code-sample:`pulse_io_byte_transfer`
* :zephyr:code-sample:`qdec_multi`
* :zephyr:code-sample:`quic-client-echo`
* :zephyr:code-sample:`quic-service-echo`
* :zephyr:code-sample:`riscv-aia-smp-uart-echo`
* :zephyr:code-sample:`riscv-aia-uart-echo`
* :zephyr:code-sample:`rpi-board-info`
* :zephyr:code-sample:`rpmsg-lite`
* :zephyr:code-sample:`rw612_pm_flash_check`
* :zephyr:code-sample:`spi-rtio-loopback`
* :zephyr:code-sample:`ssh-server-client`
* :zephyr:code-sample:`sx9500`
* :zephyr:code-sample:`tad2144`
* :zephyr:code-sample:`tflite-neutron`
* :zephyr:code-sample:`tfm_fwu`
* :zephyr:code-sample:`tm6605`
* :zephyr:code-sample:`tmc6460`
* :zephyr:code-sample:`tracing-pipeline`
* :zephyr:code-sample:`tsn-switch`
* :zephyr:code-sample:`wifi-ble-provisioning`
* :zephyr:code-sample:`wifi-mesh`
* :zephyr:code-sample:`wifi-mesh-ip`
* :zephyr:code-sample:`zms-cycle-count`
* :zephyr_file:`samples/drivers/clock_monitor/check_freq`
* :zephyr_file:`samples/drivers/clock_monitor/measure_freq`

库 / 子系统
***********

* 加密

  * 新增对 AES CFB 和 OFB 密码模式的支持。

* Mbed TLS

  * Mbed TLS 已更新至 4.1.1 版本。版本说明见 `此处 <https://github.com/Mbed-TLS/mbedtls/releases/tag/mbedtls-4.1.1>`_。

  * TF-PSA-Crypto 已更新至 1.1.1 版本。版本说明见 `此处 <https://github.com/Mbed-TLS/TF-PSA-Crypto/releases/tag/tf-psa-crypto-1.1.1>`_。

  * 新增 :kconfig:option:`CONFIG_TF_PSA_CRYPTO_DISPATCH_DIR`，使 TF-PSA-Crypto 能够使用加密操作分发的自定义实现。这样，借助可感知加速器的分发实现，即可对加密操作进行硬件加速。

* TF-M

  * TF-M 已从 2.2.2 版本更新至 2.3.1 版本。版本说明见：

    * https://trustedfirmware-m.readthedocs.io/en/latest/releases/2.3.0.html
    * https://trustedfirmware-m.readthedocs.io/en/tf-mv2.3.1/releases/2.3.1.html

  * 现在可以通过将 ``ZEPHYR_TOOLCHAIN_VARIANT`` 设置为 ``zephyr/llvm``，使用 LLVM 编译 TF-M。

* DFU

  * 新增 :kconfig:option:`CONFIG_IMG_CUSTOM_SECTOR_SIZE`，允许 MCUboot 使用不同的扇区大小，以缩小 swap-using-offset 状态区的大小。

* LoRa / LoRaWAN

  * 新增原生 LoRaWAN 后端（:kconfig:option:`CONFIG_LORA_MODULE_BACKEND_NATIVE`），它直接在 LoRa 无线电驱动之上实现 LoRaWAN 1.0.x Class A，不依赖 Semtech LoRaMac-node。目前支持 EU868 区域。
  * :c:member:`lora_modem_config.sync_word`

* 管理

  * MCUmgr

    * 镜像管理客户端现在支持 SHA-512 镜像摘要。对于使用 :kconfig:option:`CONFIG_MCUBOOT_BOOTLOADER_USES_SHA512` 构建的目标，它可以列出并选择镜像以进行测试或确认。
* 网络

  * CoAP

    * CoAP 服务器接受携带空令牌的 Observe 注册（:rfc:`7641` 允许这种做法），并以端点和该空令牌作为观察者的键。

* 安全存储

  * 对于认证失败或格式错误的条目，``psa_its_get*()`` 函数现在返回 ``PSA_ERROR_INVALID_SIGNATURE`` 或 ``PSA_ERROR_DATA_CORRUPT``，而不再返回 ``PSA_ERROR_GENERIC_ERROR``。

  * 修改条目的 ITS 操作现已串行化，丢弃无法读回的条目时会记录一条警告。

  * 以 0 作为 ``data_size`` 调用 ``psa_its_get()`` 时，现在会报告该条目是否存在且有效，而不再总是返回 ``PSA_SUCCESS``。

* 多媒体流水线

  * 引入 :ref:`mpipe`，这是用于以可复用元素（源、变换和接收端）构建多媒体应用的新子系统，这些元素链接在一起构成流水线。它让应用可以描述自己想要的媒体流，而不必亲自驱动每个音频、视频或显示设备。

* 视频

  * 引入视频子系统，它继承了此前视频驱动中的所有函数名。

* Zbus

  * :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_ISOLATION` 现在无需在每个通道上使用专用池即可工作（在调用 :c:func:`zbus_chan_set_msg_sub_pool` 之前，通道会回退到共享池）

* __assert

   * ``__ASSERT_ON`` 定义已被移除。


Devicetree
**********
* 节点现在可以使用 phandle 引用其子节点，而不会在依赖图中形成循环并导致构建错误。有关如何使用这一新特性，请参见 :ref:`dt-bindings-dependency-mode`。 (:github:`108892`)

  * :c:macro:`DT_NODELABEL_C_TOKEN`
  * :c:macro:`DT_NODELABEL_C_TOKEN_BY_IDX`

* 绑定可以使用新增的 ``class:`` 键声明设备类别成员关系（参见 :ref:`dt-bindings-class`），从而在构建时枚举某个设备类别的所有节点：

  * :c:macro:`DT_NODE_HAS_CLASS`
  * :c:macro:`DT_HAS_CLASS_STATUS_OKAY`
  * :c:macro:`DT_NUM_CLASS_STATUS_OKAY`
  * :c:macro:`DT_FOREACH_CLASS_STATUS_OKAY`
  * :c:macro:`DT_FOREACH_CLASS_STATUS_OKAY_VARGS`
  * ``$(dt_class_enabled,<class name>)`` Kconfig 预处理函数

* ADC shell 现在通过 ``adc`` 设备类别枚举 ADC 控制器，而不再使用硬编码的 compatible 列表，因此也能覆盖树外的 ADC 驱动。

* I3C shell 现在通过 ``i3c`` 设备类别枚举 I3C 控制器，而不再使用硬编码的 compatible 列表，因此也能覆盖树外的 I3C 驱动。

其他值得注意的变更
******************

* 蓝牙

  * :kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_PRIORITY` 不再仅因启用 :kconfig:option:`CONFIG_BT` 而被强制设为协作式优先级。现在只有向系统工作队列提交工作的组件才需要该设置，因此不包含这些组件的构建（例如驱动外部控制器的 HCI raw 镜像）可以重新选择可抢占优先级 (:github:`119123`)。

* 构建系统

  * 要求的最低 CMake 版本已提升至 3.28.0，Ubuntu 24.04 LTS 软件包仓库中的 CMake 软件包即满足这一版本要求。如果所用发行版提供的版本较旧，可选方案参见 :ref:`迁移指南 <migration_4.5>`。

* 内核

  * :kconfig:option:`CONFIG_SCHED_CPU_MASK` 不再依赖 :kconfig:option:`CONFIG_SCHED_SIMPLE`。CPU 亲和性掩码现在受全部三种调度器后端支持：``SCHED_SIMPLE`` （O(N) 链表扫描）、``SCHED_SCALABLE`` （O(N) 红黑树遍历）和 ``SCHED_MULTIQ`` （O(P·N) 逐优先级桶扫描）。各后端的性能说明参见更新后的 :ref:`SMP 文档 <smp_cpu_mask>`。

  * :kconfig:option:`CONFIG_SCHED_CPU_MASK_PIN_ONLY` 现在会在 API 边界（``cpu_mask_mod()``）和入队时（``thread_runq()``）同时强制满足单 CPU 位这一不变式。在 PIN_ONLY 模式下调用 :c:func:`k_thread_cpu_mask_clear`、:c:func:`k_thread_cpu_mask_enable_all` 或 :c:func:`k_thread_cpu_mask_disable` 会触发断言失败。可使用 :c:func:`k_thread_cpu_pin` 将线程重新分配到其他 CPU。

* 定时器

  * 启用 :kconfig:option:`CONFIG_SYSTEM_CLOCK_SLOPPY_IDLE` 后，如果停止时基会破坏 :c:func:`sys_clock_cycle_get_32` / :c:func:`sys_clock_cycle_get_64`，则驱动不得在无待处理超时时立即停止时基。这些函数在 CPU 运行期间必须保持计数。仅允许从 :c:func:`sys_clock_idle_enter` 停止时基，因为随后保证会调用 :c:func:`sys_clock_idle_exit`。

  * Tickless 系统定时器驱动现在可以基于共享实现头文件 :file:`drivers/timer/system_timer_generic.h` 构建；该头文件负责此前由各驱动自行实现的 tick 核算：周期到 tick 的转换、announce 基准、按 tick 对齐的期限，以及计数器回绕与范围处理。驱动只需实现少量周期域原语，即读取周期计数器并设置绝对比较定时。有关如何使用它，参见 :ref:`迁移指南 <migration_4.5>` (:github:`115844`)。

* 网络

  * DHCPv4 客户端现在会在所有放弃租约的路径上，把租约地址、该租约的 DNS 服务器以及它安装的网关从接口上移除，并在请求被拒绝或地址被拒绝后等待约十秒再重新启动。

* Wi-Fi

  * 移除了 ``samples/net/wifi/test_certs/rsa2k`` 企业测试证书（DES 加密的私钥）。请改用 ``rsa2k_no_des``。

  * 连接结果事件现在可以通过新增的 :c:enumerator:`WIFI_STATUS_CONN_AUTH_REJECT` 和 :c:enumerator:`WIFI_STATUS_CONN_ASSOC_REJECT` 值表明接入点拒绝了认证或关联，并且 :c:struct:`wifi_status` 会携带失败背后的原始 IEEE 802.11 状态码和原因码。supplicant 会填充这些信息，Wi-Fi shell 会在连接和断开连接结果中打印它们。 (:github:`116704`)

  * ``wifi-tx-power-2g.yaml`` 和 ``wifi-tx-power-5g.yaml`` 中的发射功率上限属性不再是 ``required``，并且现在带有保守的默认值，因此尚未标定的开发板宁可发射功率偏小，也不会超出法规限制。已自行测量限值的开发板仍会显式声明这些限值，因此没有任何开发板的行为发生变化。

* MCUboot

  * :kconfig:option:`SB_CONFIG_BOOT_SIGNATURE_KEY_FILE` 现在接受以逗号分隔的密钥文件列表，并将每个密钥的公钥部分嵌入 MCUboot 引导加载程序。提供多个密钥时，MCUboot 接受由其中任一密钥签名的镜像——典型用法是使用开发用引导加载程序，它可同时引导开发签名和生产签名的镜像，而生产引导加载程序只嵌入生产密钥。列表中的第一项是用于签名应用的密钥，其余各项为仅用于验证的公钥。参见 :ref:`build-signing`。

  * Espressif 开发板在 sysbuild 下不再强制使用仅覆盖模式和未签名镜像。这些开发板现在会构建采用偏移量交换并支持回退的 MCUboot，以及使用 RSA-2048 签名的应用；共享的 Espressif 分区表也不再保留 scratch 分区。参见 :ref:`迁移指南 <migration_4.5>`。

* NXP

  * NXP LPC DTSI 文件已从扁平的 ``dts/arm/nxp/lpc/`` 目录重组为按系列划分的子目录（``lpc11u6x/``、``lpc51u68/``、``lpc54xxx/``、``lpc55xxx/``、``lpc84x/``）。有关如何更新树外开发板的包含路径，参见 :ref:`迁移指南 <migration_4.5>`。

  * NXP Kinetis DTSI 文件已从扁平的 ``dts/arm/nxp/kinetis/`` 目录重组为按系列划分的子目录（``k2x/``、``k32lx/``、``k6x/``、``k8x/``、``ke1xf/``、``ke1xz/``、``kl2x/``、``kv5x/``、``kwx/``）。有关如何更新树外开发板的包含路径，参见 :ref:`迁移指南 <migration_4.5>`。

  * NXP MCX DTSI 文件已从扁平的 ``dts/arm/nxp/mcx/`` 目录重组为按系列划分的子目录（``mcxa/``、``mcxc/``、``mcxe/``、``mcxl/``、``mcxn/``、``mcxw/``）。有关如何更新树外开发板的包含路径，参见 :ref:`迁移指南 <migration_4.5>`。

  * NXP i.MX RT DTSI 文件已从扁平的 ``dts/arm/nxp/imxrt/`` 目录重组为按系列划分的子目录（``imxrt10xx/``、``imxrt11xx/``、``imxrt5xx/``、``imxrt6xx/``、``imxrt7xx/``、``imxrt118x/``）。有关如何更新树外开发板的包含路径，参见 :ref:`迁移指南 <migration_4.5>`。

* Arm

  * 非安全变体的
      :zephyr:board:`Arm Musca-S1 <v2m_musca_s1>` (``v2m_musca_s1/musca_s1/ns``) 已被移除，原因是 TF-M 移除了对该开发板的平台支持。

  * 作为上述变更的结果， :zephyr:board:`Arm Musca-S1 <v2m_musca_s1>` (``v2m_musca_s1``) 的安全变体已被弃用，以避免出现部分支持这种令人困惑的状态。

..
  Any more descriptive subsystem or driver changes. Do you really want to write
  a paragraph or is it enough to link to the api/driver/Kconfig/board page above?

Trusted Firmware-A
******************

* 引入 ``CONFIG_TFA_BUILD_FIP`` 以配置 FIP (Firmware Image Package) 的生成。FIP 生成默认处于禁用状态，可以通过在 ``prj.conf`` 中设置 ``CONFIG_TFA_BUILD_FIP=y`` 来启用；对于自定义开发板，也可以在开发板的 ``<board>_defconfig`` 文件中设置。
