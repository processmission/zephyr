.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

..
  See
  https://docs.zephyrproject.org/latest/releases/index.html#migration-guides
  for details of what is supposed to go into this document.

.. _migration_4.3:

Zephyr v4.3.0 迁移指南
######################

本文档介绍将应用从 Zephyr v4.2.0 迁移到 Zephyr v4.3.0 所需的变更。

其他变更（与迁移应用不直接相关）请参见 :ref:`版本说明 <zephyr_4.3>`。

.. contents::
    :local:
    :depth: 2

构建系统
********

内核
****

* :c:func:`device_init` 早期版本在设备初始化失败时会因缺陷返回正的 +errno 值。此问题现已修复，改为返回正确的负 -errno 值。针对该问题实现了变通方案的应用应相应更新其代码。

基础库
******

* UTF-8 工具函数声明（:c:func:`utf8_trunc`、:c:func:`utf8_lcpy`）已从 ``util.h`` 移至单独的 :zephyr_file:`include/zephyr/sys/util_utf8.h` 文件。

* ``Z_MIN``、``Z_MAX`` 和 ``Z_CLAMP`` 宏已重命名为 :c:macro:`min`、:c:macro:`max` 和 :c:macro:`clamp`。

* 不应再使用头文件 ``<zephyr/posix/time.h>`` 和 ``<zephyr/posix/signal.h>``，而应通过 C 库提供的标准路径 ``<time.h>`` 和 ``<signal.h>`` 包含它们。非 POSIX C 库的维护者可以包含 :zephyr_file:`include/zephyr/posix/posix_time.h` 和 :zephyr_file:`include/zephyr/posix/posix_signal.h`，以便可移植地提供 POSIX 定义。

* POSIX 限制值不再定义在 ``<zephyr/posix/posix_features.h>`` 中。类似地，应通过 C 库提供的标准路径 ``<limits.h>`` 包含它们。非 POSIX C 库的维护者可以包含 :zephyr_file:`include/zephyr/posix/posix_limits.h` 以使用 Zephyr 的定义。某些运行时不变的值可能需要通过 :c:func:`sysconf` 查询。

* 文件描述符表的容量及其可用性现在由 ``ZVFS_OPEN_SIZE`` 定义决定，而不再由 :kconfig:option:`CONFIG_ZVFS_OPEN_MAX` Kconfig 选项决定。子系统可以通过指定以 ``CONFIG_ZVFS_OPEN_ADD_SIZE_`` 为前缀的 Kconfig 选项，来声明各自所需的文件描述符表大小。旧的 Kconfig 选项仍然存在，但如果自定义需求更大，它将被覆盖。若要在其值小于所指示的自定义需求时仍强制使用旧的 Kconfig 选项，可使用新引入的 :kconfig:option:`CONFIG_ZVFS_OPEN_IGNORE_MIN` 选项（默认处于禁用状态）。

开发板
******

* b_u585i_iot02a/ns：flash 布局已更改，以与上游 TF-M 2.2.1 的开发板配置保持一致。新布局扩展了 flash 分区，将次级分区移至外部 NOR flash。目前此变更会阻止从较早的 Zephyr 版本镜像升级到 Zephyr 4.3 版本镜像。更多细节请参见 TF-M 迁移指南和版本说明。

* nucleo_h753zi：flash 布局已更新，由于与先前布局不兼容，固件升级可能会失败。新布局将存储分区扩大到 2 个扇区、移除了暂存分区，并重新排列了所有 flash 分区以获得更好的结构。

* mimxrt11x0：将 lpadc1 重命名为 lpadc2，将 lpadc0 重命名为 lpadc1。

* NXP 的 ``frdm_mcxa166`` 已重命名为 ``frdm_mcxa346``。
* NXP 的 ``frdm_mcxa276`` 已重命名为 ``frdm_mcxa266``。

* Panasonic 的 ``panb511evb`` 已重命名为 ``panb611evb``。

* STM32 开发板的 OpenOCD 配置文件已更改，以支持最新的 OpenOCD 版本（> v0.12.0），这些版本已弃用 HLA/SWD 传输方式（参见 https://review.openocd.org/c/openocd/+/8523 以及提交 https://sourceforge.net/p/openocd/code/ci/34ec5536c0ba3315bc5a841244bbf70141ccfbb4/）。连接运行 v2j24 之前固件的 ST-Link 适配器时可能会遇到问题，因为这些旧固件不支持新的传输方式。此时应升级 ST-Link 固件；如果无法升级，则应修改 OpenOCD 配置脚本，改为 source “interface/stlink-hla.cfg” 并显式选择 “hla_swd” 接口。与 OpenOCD v0.12.0 或更早版本的向后兼容性仍然保留。

设备驱动与设备树
****************

.. zephyr-keep-sorted-start re(^\w)

ADC
===

* ``iadc_gecko.c`` 驱动已被 ``adc_silabs_iadc.c`` 取代。:dtcompatible:`silabs,gecko-iadc` 已被 :dtcompatible:`silabs,iadc` 取代。

* :dtcompatible:`st,stm32-adc` 及其派生绑定现在要求定义 ``clock-names`` 属性，且其中列出的时钟数量必须与 ``clocks`` 属性中的时钟数量一致。预期的时钟名称为：``adcx`` 表示寄存器时钟，``adc-ker`` 表示内核源时钟，``adc-pre`` 用于设置 ADC 预分频器（适用于预分频器位于 RCC 寄存器中的系列）。

DMA
===

* DMA 的 API 不再实现用户模式系统调用。经评估，这些系统调用在访问范围上定义得过于宽泛，无法以安全的方式实现系统调用参数校验步骤。

MFD
===

* AXP2101 的驱动支持已从 AXP192 中分离出来。因此，Kconfig 符号 ``MFD_AXP192_AXP2101`` 已被移除。现在 AXP192 器件应使用 :kconfig:option:`MFD_AXP192`，而 AXP2101 器件应使用 :kconfig:option:`MFD_AXP2101`。

MISC
====

* nrf_etr 驱动已迁移到 drivers/debug。因此，相关 Kconfig 符号已从 ``NRF_ETR`` 重命名为 :kconfig:option:`DEBUG_NRF_ETR`，其余 ``NRF_ETR`` 符号也一并重命名。此外，该驱动需要经由 :kconfig:option:`DEBUG_DRIVER` 显式启用，因为它不再默认构建。

PHY
===

* 具有 :dtcompatible:`st,stm32u5-otghs-phy` 兼容属性的节点现在需要使用新属性 clock-reference，在 SYSCFG_OTGHSPHYCR 寄存器中选择 CLKSEL（PHY 基准时钟）。该选择直接取决于 RCC_CCIPR2 寄存器中 OTGHSSEL（OTG_HS PHY 内核时钟源选择）的值。

PWM
===

* :dtcompatible:`nxp,pca9685` 的 ``invert`` 属性已被移除，现在可以使用 :c:macro:`PWM_POLARITY_INVERTED` 或 :c:macro:`PWM_POLARITY_NORMAL` 标志作为 pwm 说明符单元：它们现在命名为 ``['channel', 'period', 'flags']`` （旧值：``['channel', 'period']``），并且 ``#pwm-cells`` 的常量值已从 2 改为 3。

SPI
===

* 宏 :c:macro:`SPI_CS_CONTROL_INIT`、:c:macro:`SPI_CS_CONTROL_INIT_INST`、:c:macro:`SPI_CONFIG_DT`、:c:macro:`SPI_CONFIG_DT_INST`、:c:macro:`SPI_DT_SPEC_GET` 和 :c:macro:`SPI_DT_SPEC_INST_GET` 已发生变更，不再需要提供延迟参数。这是因为 SPI 外设片选的时序参数现在应通过设备树中的 ``spi-cs-setup-delay-ns`` 和 ``spi-cs-hold-delay-ns`` 属性指定。（:github:`87427`）。

USB
===

* USB Video Class 过去会配置源视频设备的帧率和格式。现在这一工作应由应用在主机选择格式之后完成（:github:`93192`）。

以太网
======

* :dtcompatible:`microchip,vsc8541` PHY 驱动现在要求，当复位引脚以低电平有效方式使用时，reset-gpios 条目必须指定 GPIO_ACTIVE_LOW 标志。此前低电平有效特性被硬编码在驱动中。（:github:`91726`）。

* 在 Xilinx GEM 以太网驱动（:dtcompatible:`xlnx,gem`）中，CRC 校验和生成到硬件的卸载现在改为显式禁用，而不是显式启用。默认情况下，为提升性能，卸载现已默认启用；不过，由于 QEMU 目标不会模拟硬件校验和生成，无论是否通过设备树显式禁用，卸载在 QEMU 目标上始终处于禁用状态。（:github:`95435`）

  * 用于启用 RX 校验和卸载的设备树属性 ``rx-checksum-offload`` 已替换为 ``disable-rx-checksum-offload``，后者现在会主动禁用该功能。
  * 用于启用 TX 校验和卸载的设备树属性 ``tx-checksum-offload`` 已替换为 ``disable-tx-checksum-offload``，后者现在会主动禁用该功能。

* Xilinx GEM 以太网驱动（:dtcompatible:`xlnx,gem`）现在会在运行时从设计配置寄存器中获取与当前目标 SoC（Zynq-7000 或 ZynqMP）匹配的 AMBA AHB 数据总线宽度，这使设备树属性 ``amba-ahb-dbus-width`` 不再需要，因此已被移除。

* :dtcompatible:`nxp,enet-mac` 和 :dtcompatible:`xlnx,gem` 驱动在初始化时不再通过 :c:func:`phy_configure_link` 配置 PHY 的链路速度和双工模式。当 MAC 仅支持 PHY 所支持速度的一个子集时，如果用户希望限制自动协商通告的速度，则需要使用 PHY 的 ``default-speeds`` 设备树属性。（:github:`91572`）

传感器
======

* 具有 :dtcompatible:`invensense,icm42688` 兼容属性的节点现在还需要同时包含 :dtcompatible:`invensense,icm4268x` 才能正常工作。

时钟控制
========

* :kconfig:option:`CONFIG_CLOCK_STM32_HSE_CLOCK` 不再可由用户配置。其值现在始终取自 ``&clk_hse`` 设备树节点的 ``clock-frequency`` 属性，但仅在节点已启用时才有效（否则该符号不会被定义）。此变更只影响基于 STM32 MPU 的平台，并使其与 STM32 MCU 平台的既有做法保持一致。

* :dtcompatible:`st,stm32f1-rcc` 和 :dtcompatible:`st,stm32f3-rcc` 已不复存在。因此 ``adc-prescaler``、``adc12-prescaler`` 和 ``adc34-prescaler`` 属性也不再定义。它们已被替换为在 ADC ``clocks`` 属性中把预分频器作为附加时钟添加。

步进电机
========

* :dtcompatible:`zephyr,gpio-stepper` 已被 :dtcompatible:`zephyr,h-bridge-stepper` 取代。

比较器
======

* :dtcompatible:`nordic,nrf-comp` 和 :dtcompatible:`nordic,nrf-lpcomp` 的 ``psel`` 与 ``extrefsel`` 属性类型已改为整数。这些属性的取值范围为 :c:macro:`NRF_COMP_AIN0` 到 :c:macro:`NRF_COMP_AIN_VDDH_DIV5`，其中 :c:macro:`NRF_COMP_AIN0` 到 :c:macro:`NRF_COMP_AIN7` 表示外部输入 AIN0 到 AIN7，:c:macro:`NRF_COMP_AIN_VDD_DIV2` 表示内部基准 VDD/2，:c:macro:`NRF_COMP_AIN_VDDH_DIV5` 表示 VDDH/5。旧的 ``string`` 属性类型已弃用。

.. zephyr-keep-sorted-stop

蓝牙
****

* :c:struct:`bt_le_cs_test_param` 和 :c:struct:`bt_le_cs_create_config_params` 现在要求将主模式和子模式作为单个参数提供。
* :c:struct:`bt_conn_le_cs_config` 现在将主模式和子模式作为单个参数上报。
* :c:struct:`bt_conn_le_cs_main_mode` 和 :c:struct:`bt_conn_le_cs_sub_mode` 已被 :c:struct:`bt_conn_le_cs_mode` 取代。

蓝牙控制器
==========

* 以下内容已重命名：

  * :kconfig:option:`CONFIG_BT_CTRL_ADV_ADI_IN_SCAN_RSP` 重命名为 :kconfig:option:`CONFIG_BT_CTLR_ADV_ADI_IN_SCAN_RSP`
  * :c:struct:`bt_hci_vs_fata_error_cpu_data_cortex_m` 重命名为 :c:struct:`bt_hci_vs_fatal_error_cpu_data_cortex_m`，并且现在包含程序计数器值。

.. zephyr-keep-sorted-start re(^\w)

蓝牙音频
========

* :c:struct:`bt_audio_codec_cfg` 现在要求显式设置目标延迟和目标 PHY，而不再总是将目标延迟设为 “Balanced”、将目标 PHY 设为 LE 2M。为保持现有功能，请将 ``target_latency`` 设为 :c:enumerator:`BT_AUDIO_CODEC_CFG_TARGET_LATENCY_BALANCED`，并将 ``target_phy`` 设为 :c:enumerator:`BT_AUDIO_CODEC_CFG_TARGET_PHY_2M`。:c:macro:`BT_AUDIO_CODEC_CFG` 宏默认使用这些值。（:github:`93825`）
* 为 GMAP 设置 BGS 角色现在还需要支持和实现 :kconfig:option:`CONFIG_BT_BAP_BROADCAST_ASSISTANT`。可参考 :zephyr:code-sample:`bluetooth_bap_broadcast_assistant` 示例。
* BAP Scan Delegator 不再自动更新 PA 同步状态，必须使用 :c:func:`bt_bap_scan_delegator_set_pa_state` 来更新状态。如果 BAP Scan Delegator 与 BAP Broadcast Sink 一起使用，则 :c:struct:`bt_bap_broadcast_sink` 接收状态的 PA 状态仍会在 PA 状态变化时自动更新。（:github:`95453`）


.. zephyr-keep-sorted-stop

蓝牙 HCI
========

* 已弃用的 ``ipm`` 值已从 ``bt-hci-bus`` 设备树属性中移除。应改用 ``ipc``。

蓝牙 Mesh
=========

* Kconfig 选项 ``CONFIG_BT_MESH_USES_MBEDTLS_PSA`` 和 ``CONFIG_BT_MESH_USES_TFM_PSA`` 已被移除。PSA 加密提供者的选择现在由 Kconfig :kconfig:option:`CONFIG_PSA_CRYPTO` 自动控制。

蓝牙主机
========

* :kconfig:option:`CONFIG_BT_FIXED_PASSKEY` 已弃用。应用可以改用 :c:member:`bt_conn_auth_cb.app_passkey` 回调为配对提供通行密钥，该回调在启用 :kconfig:option:`CONFIG_BT_APP_PASSKEY` 时可用。应用可以返回用于配对的通行密钥，也可以返回 :c:macro:`BT_PASSKEY_RAND`，由主机改为生成随机通行密钥。

电源管理
********

* :kconfig:option:`CONFIG_PM_S2RAM` 和 :kconfig:option:`PM_S2RAM_CUSTOM_MARKING` 已重构为由 SoC 和设备树自动管理。应用不应再直接启用它们，而应在设备树中启用或禁用 “suspend-to-ram” 电源状态。

* 对于 NXP RW61x，设备树属性 ``exit-latency-us`` 已更新为更准确的实测唤醒时间。对于使用待机模式（PM3）的应用，此更新以及对 ``min-residency-us`` 设备树属性的增大，可能会影响系统在电源模式之间的切换方式。某些情况下，这可能导致功耗变化。

网络
****

* HTTP 服务器现在会遵循所配置的 ``_config`` 值。请检查你为 :c:macro:`HTTP_SERVICE_DEFINE_EMPTY`、:c:macro:`HTTPS_SERVICE_DEFINE_EMPTY`、:c:macro:`HTTP_SERVICE_DEFINE` 和 :c:macro:`HTTPS_SERVICE_DEFINE` 提供了适用的值。

* 套接字地址长度类型 :c:type:`socklen_t` 的大小已更改。为了与 Linux 保持一致，它现在始终定义为 32 位的 ``uint32_t``。以前它定义为 ``size_t``，这意味着其大小可能是 32 位或 64 位，取决于系统配置。

* :c:func:`net_icmp_init_ctx` API 已更改，现在接受一个额外的 ``family`` 参数，用于指示该上下文应处理的报文族。对于 ICMPv4 上下文，使用 ``AF_INET``；对于 ICMPv6 上下文，使用 ``AF_INET6``。

.. zephyr-keep-sorted-start re(^\w)

CoAP
====

* :c:type:`coap_client_response_cb_t` 的签名已更改。参数列表现在通过 :c:struct:`coap_client_response_data` 指针传递。

* :c:struct:`coap_client_request` 已更改，以提升该库对错误配置（例如在结构体中使用临时指针）的健壮性：

  * :c:member:`coap_client_request.path` 现在是 ``char`` 数组，而不再是指针。数组大小可通过 :kconfig:option:`CONFIG_COAP_CLIENT_MAX_PATH_LENGTH` 配置。
  * :c:member:`coap_client_request.options` 现在是 :c:struct:`coap_client_option` 数组，而不再是指针。数组大小可通过 :kconfig:option:`CONFIG_COAP_CLIENT_MAX_EXTRA_OPTIONS` 配置。

.. zephyr-keep-sorted-stop

调制解调器
**********

* ``CONFIG_MODEM_AT_SHELL_USER_PIPE`` 已重命名为 :kconfig:option:`CONFIG_MODEM_AT_USER_PIPE`。
* ``CONFIG_MODEM_CMUX_WORK_BUFFER_SIZE`` 已更新为 :kconfig:option:`CONFIG_MODEM_CMUX_WORK_BUFFER_SIZE_EXTRA`，后者只取在默认值（:kconfig:option:`CONFIG_MODEM_CMUX_MTU` + 7）之上额外需要的字节数。

显示
****

* 显示示例中曾把 RGB565 和 BGR565 像素格式混用。此问题现已修复。基于先前示例进行测试或开发的开发板和应用可能会受此变更影响（更多信息请参见 :github:`79996`）。

* SSD1363 使用 'greyscale' 的属性现在改用 'grayscale'。

PTP 时钟
********

* :c:func:`ptp_clock_rate_adjust` API 的文档未提供恰当而清晰的函数说明。驱动实现该函数时是相对于当前频率调整速率比。现在 PTP 和 gPTP 中引入了 PI 伺服，该 API 函数改为基于标称频率调整速率比。实现 :c:func:`ptp_clock_rate_adjust` 的驱动应做出相应调整，以适配新的行为。

视频
****

* ``min_line_count`` 和 ``max_line_count`` 字段已从 :c:struct:`video_caps` 中移除。应用应基于新的 :c:member:`video_format.size` 来分配缓冲区。

其他子系统
**********

.. zephyr-keep-sorted-start re(^\w)

Flash 映射
==========

* 出于将 PSA Crypto API 作为 Zephyr 唯一加密支持的长期目标，:kconfig:option:`FLASH_AREA_CHECK_INTEGRITY_MBEDTLS` 已弃用。:kconfig:option:`FLASH_AREA_CHECK_INTEGRITY_PSA` 现在是默认选择：如果未启用 TF-M 或平台不支持 TF-M，则将使用 Mbed TLS 作为 PSA Crypto API 提供者。

MCUmgr
======

* :ref:`OS 管理 <mcumgr_smp_group_0>` :ref:`mcumgr_os_application_info` 命令针对硬件平台的响应已更新，改为输出开发板目标，而不是开发板和开发板版本；开发板目标现在包含 SoC 和开发板变体。旧行为已弃用，但仍可通过启用 :kconfig:option:`CONFIG_MCUMGR_GRP_OS_INFO_HARDWARE_INFO_SHORT_HARDWARE_PLATFORM` 来使用。

* 对旧版 Mbed TLS 哈希加密的支持已被移除，现在只使用 PSA Crypto API。如果构建中未启用 TF-M，:kconfig:option:`CONFIG_MCUMGR_GRP_FS_HASH_SHA256` 会自动启用 Mbed TLS 及其 PSA Crypto 实现。

Mbed TLS
========

* 为了改善 Zephyr Kconfig 与 Mbed TLS 构建符号之间的一一对应关系，以下 Kconfig 已重命名：

  * :kconfig:option:`CONFIG_MBEDTLS_MD` -> :kconfig:option:`CONFIG_MBEDTLS_MD_C`
  * :kconfig:option:`CONFIG_MBEDTLS_LMS` -> :kconfig:option:`CONFIG_MBEDTLS_LMS_C`
  * :kconfig:option:`CONFIG_MBEDTLS_TLS_VERSION_1_2` -> :kconfig:option:`CONFIG_MBEDTLS_SSL_PROTO_TLS1_2`
  * :kconfig:option:`CONFIG_MBEDTLS_DTLS` -> :kconfig:option:`CONFIG_MBEDTLS_SSL_PROTO_DTLS`
  * :kconfig:option:`CONFIG_MBEDTLS_TLS_VERSION_1_3` -> :kconfig:option:`CONFIG_MBEDTLS_SSL_PROTO_TLS1_3`
  * :kconfig:option:`CONFIG_MBEDTLS_TLS_SESSION_TICKETS` -> :kconfig:option:`CONFIG_MBEDTLS_SSL_SESSION_TICKETS`
  * :kconfig:option:`CONFIG_MBEDTLS_CTR_DRBG_ENABLED` -> :kconfig:option:`CONFIG_MBEDTLS_CTR_DRBG_C`
  * :kconfig:option:`CONFIG_MBEDTLS_HMAC_DRBG_ENABLED` -> :kconfig:option:`CONFIG_MBEDTLS_HMAC_DRBG_C`

RTIO
====

* 回调操作现在多接受一个参数，对应该链中第一个错误的错误码。
* 无论链中先前提交处于成功还是错误状态，回调操作现在都会被调用。

Shell
=====

* 与 :kconfig:option:`SHELL_BACKEND_MQTT` 相关的 MQTT 主题已重命名。``<device_id>_rx`` 重命名为 ``<device_id>/sh/rx``，``<device_id>_tx`` 重命名为 ``<device_id>/sh/tx``。``<device_id>`` 之后的部分现在可通过 :kconfig:option:`SHELL_MQTT_TOPIC_RX_ID` 和 :kconfig:option:`SHELL_MQTT_TOPIC_TX_ID` 配置。这样可以保留先前的主题以保持向后兼容。（:github:`92677`）。

UpdateHub
=========

* 旧版 Mbed TLS 作为加密支持选项已被移除，现在所有情况都使用 PSA Crypto。如果构建中未启用 TF-M，:kconfig:option:`CONFIG_UPDATEHUB` 会自动启用 PSA Crypto 的 Mbed TLS 实现。

加密
====

* 哈希操作现在要求 :c:struct:`hash_pkt` 中的输入为常量。这不应影响任何现有代码，除非某个树外哈希后端确实会就地执行该操作（参见 :github:`94218`）

安全存储
========

* 用于标识存储条目的 :c:type:`psa_storage_uid_t` 大小已从 64 位改为 30 位。此变更破坏了与先前存储条目的向后兼容性，这些条目的身份验证将开始失败。如果你要从较早版本的 Zephyr 升级现有安装并希望保留已有条目，请启用 :kconfig:option:`CONFIG_SECURE_STORAGE_64_BIT_UID`。（:github:`94171`）

日志记录
========

* UART 字典日志解析脚本 ``scripts/logging/dictionary/log_parser_uart.py`` 已弃用。应改用更通用的 :zephyr_file:`scripts/logging/dictionary/live_log_parser.py` 脚本。新脚本支持相同的功能（并有所扩展），但调用时需要不同的命令行参数。

蜂窝网络
========

 * :c:enum:`cellular_access_technology` 的值已重新定义，以与 3GPP TS 27.007 保持一致。
 * :c:enum:`cellular_registration_status` 的值已扩展，以与 3GPP TS 27.007 保持一致。

.. zephyr-keep-sorted-stop

模块
****

* TinyCrypt 库已被移除，因为上游版本不再维护。现在推荐使用 PSA Crypto API 作为 Zephyr 的加密库。

MCUboot
=======

* MCUboot 的默认运行模式已改为 swap using offset，这种模式可提供更快的交换更新、更少的开销，并减少执行一次更新所需的 flash 擦写次数；此前的默认模式是 swap using move。如果某个开发板此前为优化 swap using move 而将主槽做得比次槽大一个扇区，则需改为次槽比主槽大一个扇区（为获得优化效果，仍支持两个槽的扇区数相同）。或者，也可以在 sysbuild 中通过 :kconfig:option:`SB_CONFIG_MCUBOOT_MODE_SWAP_USING_MOVE` 选择先前的 swap using move 模式。

Silabs
======

* 将 Rail 选项的名称与其他 SiSDK 相关选项对齐：

  * :kconfig:option:`CONFIG_RAIL_PA_CURVE_HEADER` -> :kconfig:option:`CONFIG_SILABS_SISDK_RAIL_PA_CURVE_HEADER`
  * :kconfig:option:`CONFIG_RAIL_PA_CURVE_TYPES_HEADER` -> :kconfig:option:`CONFIG_SILABS_SISDK_RAIL_PA_CURVE_TYPES_HEADER`
  * :kconfig:option:`CONFIG_RAIL_PA_ENABLE_CALIBRATION` -> :kconfig:option:`CONFIG_SILABS_SISDK_RAIL_PA_ENABLE_CALIBRATION`

* 修正了 :kconfig:option:`CONFIG_SOC_*` 的名称。这些选项的名称中含有 PART_NUMBER，而它们本不应包含。

* Series 2 SoC 中单独的 ``em3`` 电源状态已被移除。系统会根据振荡器的硬件外设请求自动转换到 EM2 或 EM3。

LVGL
====

* PIXEL_FORMAT_MONO10 和 PIXEL_FORMAT_MONO01 格式在 :zephyr_file:`modules/lvgl/lvgl_display_mono.c` 中被交换了，这导致单色显示屏使用 LVGL 时黑白颜色反转。此问题现已修复。此前为实现预期行为而采用的任何变通方案都应移除，否则黑白颜色将再次反转。

LED 灯带
========

* 将 ``arduino,modulino-smartleds`` 重命名为 :dtcompatible:`arduino,modulino-pixels`

Trusted Firmware-M
==================

* BL2（MCUboot）的签名流程已更新。使用 TF-M NS 且需要 BL2 的开发板，其 flash 布局必须包含 flash 控制器信息。这可以确保在签名 hex/bin 文件时，所有细节都会出现在 S 和 NS 镜像中。现在镜像中已包含相关细节，使 FWU 状态机保持正确并支持 FOTA。（:github:`94470`）

  * ``--align`` 参数原先固定为 1。现在它设置为 flash 设备树的 ``write_block_size`` 属性，但对特定厂商仍提供 1 作为回退值。
  * ``--max-sectors`` 的值现在根据镜像数量计算，并考虑最大镜像的大小。
  * ``--confirm`` 选项现在会同时确认 S 和 NS HEX 镜像，确保运行的任何镜像在生产环境和开发环境中都有效。
  * 现在提供 S 和 NS 的 BIN 镜像。这些是 FOTA 中应使用的正确镜像。请注意，S 和 NS 镜像默认处于未确认状态，应用需要通过 ``psa_fwu_accept()`` 负责确认它们，否则镜像将在下次重启时回滚。

* TF-M v2.1.0 版本发布后引入的 TF-M 证明流程中发现了一个兼容性问题。因此，使用 TF-M v2.1 的系统在不遇到故障的情况下无法升级到任何更高版本的 TF-M。此限制影响使用 TF-M v2.1.0 到 v2.1.2 的 Zephyr 版本，具体来说是从 Zephyr v3.7 到 v4.2，使这些版本之间无法无缝升级。该问题已于 10 月 25 日在主线 TF-M 中解决，修复已包含在 Zephyr v4.3.0 中。建议用户直接从任何较早的 Zephyr 版本迁移到 Zephyr v4.3.0 或更高版本，以确保完整的 TF-M 证明功能和升级兼容性。（:github:`94859`）对于最初使用 Zephyr v4.0 到 v4.2 构建的任何应用，必须设置 :kconfig:option:`CONFIG_TFM_ZEPHYR_4_0_TO_4_2_COMPATIBILITY` 才能成功升级到 v4.2 之后的任何版本，并且需在所有后续升级中保持设置。（:github:`103793`）

* 构建时通过 CMake 自动下载 MCUboot 和 ethos 的支持已被移除，将改为使用这些模块的树内版本。要使用自定义版本，请创建 :ref:`west manifest <west-manifest-files>`，在其中引入所需版本的这些仓库。
