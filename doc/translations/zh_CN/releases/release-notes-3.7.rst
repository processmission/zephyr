.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

.. _zephyr_3.7:

Zephyr 3.7.0
############

我们很高兴地宣布 Zephyr 3.7.0 版本正式发布。

本次发布是 3.x 系列最后一个非维护版本，因此也将成为下一个 :ref:`长期支持（LTS）版本 <release_process_lts>`。

本次发布的主要增强包括：

* 引入了全新的、彻底 :ref:`重构的硬件模型 <hw_model_v2>`。它改变了 Zephyr 中 SoC 和开发板的命名、定义与构建方式。更多信息参见 :ref:`开发板移植指南 <board_porting_guide>`。
* 期待已久的 :ref:`HTTP 服务器 <http_server_interface>` 库及相关服务 API，让在 Zephyr 中实现 HTTP/1.1 和 HTTP/2 服务器变得简单。资源可以静态或动态注册，并包含 WebSocket 支持。
* :ref:`POSIX 支持 <posix_support>` 得到扩展，IEEE 1003-2017 的 :ref:`系统接口 <posix_system_interfaces_required>` 中大部分选项都已获得支持，:ref:`PSE51 <posix_aep_pse51>`、:ref:`PSE52 <posix_aep_pse52>` 和 :ref:`PSE53 <posix_aep_pse53>` 所需的大部分选项和选项组也已支持。
* Bluetooth Host 已扩展支持 Nordic UART Service（NUS）、Hands-free Audio Gateway（AG）、Advanced Audio Distribution Profile（A2DP）和 Audio/Video Distribution Transport Protocol（AVDTP）。
* 传感器抽象模型进行了重构，采用 :ref:`先读取再解码的方式 <sensor-read-and-decode>`，相比之前的 fetch/get API 能支持更多类型的传感器和数据流。
* 新的 :ref:`LLEXT 扩展开发工具包（EDK） <llext_build_edk>` 让开发和集成自定义扩展更加容易，包括 Zephyr 代码树之外的扩展。
* :zephyr:board:`原生模拟器 <native_sim>` 现在支持直接利用原生主机的网络协议栈，无需依赖复杂的主机环境配置。
* Trusted Firmware-M（TF-M）2.1.0 和 Mbed TLS 3.6.0 已集成到 Zephyr 中。这两个版本都是 LTS 版本。此外，:ref:`psa_crypto` 已替代 TinyCrypt，提供更强的安全性和性能。
* :ref:`精确时间协议 <ptp_interface>` 的新实验性实现（PTP，IEEE 1588）可通过亚微秒级精度在多设备间同步时间。
* 新增了文档页面，帮助开发者搭建 :ref:`vscode_ide` 和 :ref:`clion_ide` 的本地开发环境。

将应用从 Zephyr v3.6.0 迁移到 Zephyr v3.7.0 时需要或建议采取的变更概览，见单独的 :ref:`迁移指南 <migration_3.7>`。

虽然可以查阅之前 3.x 版本的版本说明以了解完整变更日志，但自上一个 LTS 版本 Zephyr 2.7.0 以来的其他主要增强和变更包括：

* 新增对 Picolibc 的支持，并将其作为新的默认 C 库。
* 新增对以下类型硬件外设的支持：

  * 1-Wire
  * 电池充电器
  * 蜂窝调制解调器
  * 电量计
  * GNSS
  * 硬件自旋锁
  * I3C
  * RTC（实时时钟）
  * SMBus

* 新增对代码片段（snippet）的支持。代码片段是可在不同平台间共用的通用配置设置。
* 新增对可链接可加载扩展（LLEXT）的支持。
* 破坏性变更摘要（更多细节请参阅之前版本的版本说明和迁移指南）：

  * 所有 Zephyr 公共头文件已移至 :file:`include/zephyr` ，这意味着包含它们时需要加上 ``<zephyr/...>`` 前缀。
  * Pinmux API 已被移除。需要使用引脚控制（pin control）作为替代，更多细节请参阅 :ref:`pinctrl-guide`。

  * 以下已弃用或实验性功能已被移除：

    * 6LoCAN
    * civetweb 模块。可参阅 Zephyr 3.7 新增的 :ref:`http_server_interface` 作为替代。
    * tinycbor 模块。可以使用 zcbor 作为替代。

以下各节按组件提供详细的变更列表。

安全漏洞相关
************
本版本修复了以下 CVE：

更多详细信息请参阅：https://docs.zephyrproject.org/latest/security/vulnerabilities.html

* CVE-2024-3077 `Zephyr 项目缺陷跟踪器 GHSA-gmfv-4vfh-2mh8 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gmfv-4vfh-2mh8>`_

* CVE-2024-3332  `Zephyr 项目缺陷跟踪器 GHSA-jmr9-xw2v-5vf4 <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-jmr9-xw2v-5vf4>`_

* CVE-2024-4785：在 2024-08-07 之前处于禁运期

* CVE-2024-5754：在 2024-09-04 之前处于禁运期

* CVE-2024-5931：在 2024-09-10 之前处于禁运期

* CVE-2024-6135：在 2024-09-11 之前处于禁运期

* CVE-2024-6137：在 2024-09-11 之前处于禁运期

* CVE-2024-6258：在 2024-09-05 之前处于禁运期

* CVE-2024-6259：在 2024-09-12 之前处于禁运期

* CVE-2024-6442：在 2024-09-22 之前处于禁运期

* CVE-2024-6443：在 2024-09-22 之前处于禁运期

* CVE-2024-6444：在 2024-09-22 之前处于禁运期

API 变更
********

本版本移除的 API
================

 * 蓝牙子系统专用的调试符号已被移除，它们已替换为 Zephyr 日志符号。

 * 从 PCIe API 中移除了已弃用的 ``pcie_probe`` 和 ``pcie_bdf_lookup`` 函数。

 * 移除了已弃用的 ``CONFIG_EMUL_EEPROM_AT2X`` Kconfig 选项。

 * 从设备电源管理（Device PM）API 中移除了 ``pm_device_state_lock`` 、``pm_device_state_is_locked`` 和 ``pm_device_state_unlock`` 函数。

 * 移除了已弃用的 MCUmgr 传输 API 函数：``zephyr_smp_rx_req`` 、``zephyr_smp_alloc_rsp`` 和 ``zephyr_smp_free_buf`` 。

本版本弃用的内容
================

 * 蓝牙广播选项 :code:`BT_LE_ADV_OPT_USE_NAME` 和 :code:`BT_LE_ADV_OPT_FORCE_NAME_IN_AD` 现已弃用。这意味着以下宏已弃用：

    * :c:macro:`BT_LE_ADV_CONN_NAME`
    * :c:macro:`BT_LE_ADV_CONN_NAME_AD`
    * :c:macro:`BT_LE_ADV_NCONN_NAME`
    * :c:macro:`BT_LE_EXT_ADV_CONN_NAME`
    * :c:macro:`BT_LE_EXT_ADV_SCAN_NAME`
    * :c:macro:`BT_LE_EXT_ADV_NCONN_NAME`
    * :c:macro:`BT_LE_EXT_ADV_CODED_NCONN_NAME`

   应用开发者现在需要自行更新广播数据或扫描响应数据来设置广播名称。

* CAN

  * 弃用了 :c:func:`can_calc_prescaler` API 函数，因为它允许比特率误差。同一网络中节点间的比特率误差会在完成帧起始（SOF）同步后使节点逐渐漂移，从而导致总线错误。
  * 弃用了 :c:func:`can_get_min_bitrate` 和 :c:func:`can_get_max_bitrate` API 函数，改用 :c:func:`can_get_bitrate_min` 和 :c:func:`can_get_bitrate_max` 。
  * 弃用了 :c:macro:`CAN_MAX_STD_ID` 和 :c:macro:`CAN_MAX_EXT_ID` 宏，改用 :c:macro:`CAN_STD_ID_MASK` 和 :c:macro:`CAN_EXT_ID_MASK` 。

* PM

  * 弃用了 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_EXCLUSIVE` 。使用 :kconfig:option:`CONFIG_PM_DEVICE_SYSTEM_MANAGED` 可以实现类似行为。

.. _zephyr_3.7_posix_api_deprecations:

* POSIX API

  * 已弃用的 :c:macro:`PTHREAD_BARRIER_DEFINE` 已被移除。
  * 已弃用的 :c:macro:`EFD_IN_USE` 和 :c:macro:`EFD_FLAGS_SET` 已被移除。

  * 为了使用与 IEEE 1003.1-2017 中 Options 和 Option Groups 直接对应的 Kconfig 选项，以下 Kconfig 选项已被弃用（括号内为替代选项）：

    * :kconfig:option:`CONFIG_EVENTFD_MAX` (:kconfig:option:`CONFIG_ZVFS_EVENTFD_MAX`)
    * :kconfig:option:`CONFIG_FNMATCH` (:kconfig:option:`CONFIG_POSIX_C_LIB_EXT`)
    * :kconfig:option:`CONFIG_GETOPT` (:kconfig:option:`CONFIG_POSIX_C_LIB_EXT`)
    * :kconfig:option:`CONFIG_MAX_PTHREAD_COUNT` (:kconfig:option:`CONFIG_POSIX_THREAD_THREADS_MAX`)
    * :kconfig:option:`CONFIG_MAX_PTHREAD_KEY_COUNT` (:kconfig:option:`CONFIG_POSIX_THREAD_KEYS_MAX`)
    * :kconfig:option:`CONFIG_MAX_TIMER_COUNT` (:kconfig:option:`CONFIG_POSIX_TIMER_MAX`)
    * :kconfig:option:`CONFIG_POSIX_LIMITS_RTSIG_MAX` (:kconfig:option:`CONFIG_POSIX_RTSIG_MAX`)
    * :kconfig:option:`CONFIG_POSIX_CLOCK` (:kconfig:option:`CONFIG_POSIX_CLOCK_SELECTION`,
      :kconfig:option:`CONFIG_POSIX_CPUTIME`, :kconfig:option:`CONFIG_POSIX_MONOTONIC_CLOCK`,
      :kconfig:option:`CONFIG_POSIX_TIMERS`, and :kconfig:option:`CONFIG_POSIX_TIMEOUTS`)
    * :kconfig:option:`CONFIG_POSIX_FS` (:kconfig:option:`CONFIG_POSIX_FILE_SYSTEM`)
    * :kconfig:option:`CONFIG_POSIX_MAX_FDS` (:kconfig:option:`CONFIG_POSIX_OPEN_MAX` and
      :kconfig:option:`CONFIG_ZVFS_OPEN_MAX`)
    * :kconfig:option:`CONFIG_POSIX_MAX_OPEN_FILES` (:kconfig:option:`CONFIG_POSIX_OPEN_MAX` and
      :kconfig:option:`CONFIG_ZVFS_OPEN_MAX`)
    * :kconfig:option:`CONFIG_POSIX_MQUEUE` (:kconfig:option:`CONFIG_POSIX_MESSAGE_PASSING`)
    * :kconfig:option:`CONFIG_POSIX_PUTMSG` (:kconfig:option:`CONFIG_XOPEN_STREAMS`)
    * :kconfig:option:`CONFIG_POSIX_SIGNAL` (:kconfig:option:`CONFIG_POSIX_SIGNALS`)
    * :kconfig:option:`CONFIG_POSIX_SYSCONF` (:kconfig:option:`CONFIG_POSIX_SINGLE_PROCESS`)
    * :kconfig:option:`CONFIG_POSIX_UNAME` (:kconfig:option:`CONFIG_POSIX_SINGLE_PROCESS`)
    * :kconfig:option:`CONFIG_PTHREAD` (:kconfig:option:`CONFIG_POSIX_THREADS`)
    * :kconfig:option:`CONFIG_PTHREAD_BARRIER` (:kconfig:option:`CONFIG_POSIX_BARRIERS`)
    * :kconfig:option:`CONFIG_PTHREAD_COND` (:kconfig:option:`CONFIG_POSIX_THREADS`)
    * :kconfig:option:`CONFIG_PTHREAD_IPC` (:kconfig:option:`CONFIG_POSIX_THREADS`)
    * :kconfig:option:`CONFIG_PTHREAD_KEY` (:kconfig:option:`CONFIG_POSIX_THREADS`)
    * :kconfig:option:`CONFIG_PTHREAD_MUTEX` (:kconfig:option:`CONFIG_POSIX_THREADS`)
    * :kconfig:option:`CONFIG_PTHREAD_RWLOCK` (:kconfig:option:`CONFIG_POSIX_READER_WRITER_LOCKS`)
    * :kconfig:option:`CONFIG_PTHREAD_SPINLOCK` (:kconfig:option:`CONFIG_POSIX_SPIN_LOCKS`)
    * :kconfig:option:`CONFIG_SEM_NAMELEN_MAX` (:kconfig:option:`CONFIG_POSIX_SEM_NAMELEN_MAX`)
    * :kconfig:option:`CONFIG_SEM_VALUE_MAX` (:kconfig:option:`CONFIG_POSIX_SEM_VALUE_MAX`)
    * :kconfig:option:`CONFIG_TIMER` (:kconfig:option:`CONFIG_POSIX_TIMERS`)
    * :kconfig:option:`CONFIG_TIMER_DELAYTIMER_MAX` (:kconfig:option:`CONFIG_POSIX_DELAYTIMER_MAX`)

    请参阅 :ref:`POSIX API 迁移指南 <zephyr_3.7_posix_api_migration>` 。

 * SPI

  * 已弃用的 :c:func:`spi_is_ready` API 函数已被移除。
  * 已弃用的 :c:func:`spi_transceive_async` API 函数已被移除。
  * 已弃用的 :c:func:`spi_read_async` API 函数已被移除。
  * 已弃用的 :c:func:`spi_write_async` API 函数已被移除。

架构
****

* ARC

  * 新增对 ARC-V 目标的 ARC MWDT 工具链支持
  * 新增对多核目标的硬件内存屏障 API 支持
  * 在 ARC MWDT 工具链下使用 C++ 时默认启用 TLS
  * 修复了 ARC MWDT 工具链配合最小化 LibC 时，因标记 C 库边界检查接口扩展支持的定义错误而导致 mbedtls 无法构建的问题
  * 修复了使用 ARC MWDT 工具链时设备延迟初始化的问题

* ARM

  * 新增对 Cortex-M85 内核的初步支持

* ARM64

  * 在回溯信息中实现了符号名显示，可通过选择 :kconfig:option:`CONFIG_SYMTAB` 启用

  * 为 Cortex-R82 新增编译器调优

* RISC-V

  * 由故障触发的致命错误消息现在包含被调用者保存寄存器（callee-saved registers）的状态。

  * 实现了栈展开

    * 可以选择帧指针（frame pointer）来启用精确的栈回溯，代价是体积略有增加、速度略有下降。

    * 选择 :kconfig:option:`CONFIG_EXCEPTION_STACK_TRACE_SYMTAB` 即可启用符号名

* Xtensa

  * 新增保存和恢复 HiFi AudioEngine 寄存器的支持。

  * 新增利用 MPU 的支持。

  * 新增自动生成中断处理程序的支持。

  * 新增在构建时生成向量表并将其包含到链接脚本中的支持。

  * 新增 Kconfig 选项 :kconfig:option:`CONFIG_XTENSA_BREAK_ON_UNRECOVERABLE_EXCEPTIONS` ，用于控制在不可恢复异常时是否使用 break 指令。通过该 Kconfig 启用 break 指令可能导致无限中断风暴，从而妨碍调试工作。

  * 修复了通过系统调用传递第 7 个参数时处理错误的问题。

  * 修复了 :c:func:`arch_user_string_nlen` 访问未映射内存时导致不可恢复异常的问题。

内核
****

  * 新增 :c:func:`k_uptime_seconds` 函数，以简化 ``k_uptime_get() / 1000`` 的用法。

  * 新增 :c:func:`k_realloc` ，它使用内核堆来实现传统的 :c:func:`realloc` 语义。

  * 设备现在可以通过开启 :kconfig:option:`CONFIG_DEVICE_DT_METADATA` 来存储节点标签（nodelabel）等设备树元数据。该选项在 shell 等场景中很有用，因为借助 :c:func:`device_get_by_dt_nodelabel` 等 API，可以使用易读的名称获取设备。

  * 如果设备关联的设备树节点设置了特殊的 ``zephyr,deferred-init`` 属性，该设备的初始化就可以推迟。之后可以使用 :c:func:`device_init` 在稍后的时间初始化该设备。

  * 静态分配线程栈的声明已更新，单线程栈声明和线程栈数组声明现在都使用 :c:macro:`K_THREAD_STACK_LEN` 。这确保了所有线程栈的正确对齐。对于用户线程，根据架构对齐要求，这可能会增加静态分配的栈对象的大小。

  * 修复了 :c:func:`k_thread_abort` （以及 join）中的一个边缘情况死锁：SMP 系统上相互竞争的 ISR 可能一直空转，试图向彼此被中断的线程发送信号。

  * 修复了 :kconfig:option:`CONFIG_SCHED_SCALABLE` 和 :kconfig:option:`CONFIG_SCHED_DEADLINE` 一起使用时破坏调度队列的 bug。

蓝牙
****

* 音频

  * 从 :c:struct:`bt_bap_broadcast_assistant_cb.recv_state_removed` 中移除了 ``err`` ，因为它是多余的。

  * broadcast_audio_assistant 示例已重命名为 bap_broadcast_assistant；broadcast_audio_sink 示例已重命名为 bap_broadcast_sink；broadcast_audio_source 示例已重命名为 bap_broadcast_source；unicast_audio_client 示例已重命名为 bap_unicast_client；unicast_audio_server 示例已重命名为 bap_unicast_server；public_broadcast_sink 示例已重命名为 pbp_public_broadcast_sink；public_broadcast_source 示例已重命名为 pbp_public_broadcast_source。

  * CAP Commander 和 CAP Initiator 现在不再要求为 :code:`BT_CAP_SET_TYPE_AD_HOC` 集合发现 CAS。这使得应用可以在例如未实现 CAP Acceptor 角色的 BAP Unicast Server 上使用这些 API。

* 主机

  * 新增 Nordic UART Service（NUS），由 :kconfig:option:`CONFIG_BT_ZEPHYR_NUS` 启用。该服务支持声明多个 GATT 服务实例，从而可以为不同用途使用多个串行端点。

  * 实现了免手持音频网关（AG），由 :kconfig:option:`CONFIG_BT_HFP_AG` 启用。它作为音频网关设备工作，典型的音频网关设备是蜂窝电话。它控制免手持单元（Hands-free Unit），即远程音频输入和输出机制。

  * 实现了高级音频分发配置文件（A2DP）和音视频分发传输协议（AVDTP），A2DP 由 :kconfig:option:`CONFIG_BT_A2DP` 启用，AVDTP 由 :kconfig:option:`CONFIG_BT_AVDTP` 启用。它们实现了以单声道、立体声或多声道模式分发高质量音频内容的协议和流程。典型用例是将音乐内容从立体声音乐播放器流式传输到耳机或扬声器。音频数据以适当的格式压缩，以高效利用有限的带宽。

  * 重构了数据和命令的传输路径。“BT TX”线程已被移除，HCI 分片和 L2CAP 段的缓冲区池也随之移除。与控制器（Controller）的所有通信现在都只在系统工作队列上下文中进行。

  * :kconfig:option:`CONFIG_BT_PER_ADV_SYNC_TRANSFER_RECEIVER` 和 :kconfig:option:`CONFIG_BT_PER_ADV_SYNC_TRANSFER_SENDER` 现在依赖 :kconfig:option:`CONFIG_BT_CONN` ，因为没有连接时它们无法工作。

  * 改进 :c:func:`bt_foreach_bond` 以支持蓝牙经典（Bluetooth Classic）密钥遍历。

* HCI 驱动

  * 完全重新设计了 HCI 驱动接口。更多信息请参阅 :ref:`migration_3.7` 中的蓝牙 HCI 章节。
  * 新增对 Ambiq Apollo3 Blue 系列的支持。
  * 新增对 NXP RW61x 的支持。
  * 新增对 Infineon CYW208XX 的支持。
  * 新增对 Renesas SmartBond DA1469x 的支持。
  * 移除了无人维护的 B91 驱动。
  * 新增对开发板 mimxrt1170_evkb 和 mimxrt1040_evk 上 NXP IW612 的支持。可通过 :kconfig:option:`CONFIG_BT_NXP_NW612` 启用。

开发板与 SoC 支持
*****************

* 新增对以下 SoC 系列的支持：

  * 新增对 Ambiq Apollo3 Blue 和 Apollo3 Blue Plus SoC 系列的支持。
  * 新增对 Synopsys ARC-V RMX1xx 仿真平台的支持。
  * 新增对 STM32H7R/S SoC 系列的支持。
  * 新增对 NXP mke15z7、mke17z7、mke17z9、MCXNx4x、RW61x 的支持
  * 新增对 Analog Devices MAX32 SoC 系列的支持。
  * 新增对 Infineon Technologies AIROC™ CYW20829 Bluetooth LE SoC 系列的支持。
  * 新增对 MediaTek MT8195 音频 DSP 的支持
  * 新增对 Nuvoton Numaker M2L31X SoC 系列的支持。
  * 新增对 Microchip PolarFire ICICLE Kit SMP 变体的支持。
  * 新增对 Renesas RA8 系列 SoC 的支持。

* 对其他 SoC 系列做了以下更改：

  * Intel ACE 音频 DSP：使用专用寄存器而不是任意内存来报告启动状态。
  * ITE：为所有 ITE SoC 变体重命名 Kconfig 符号。
  * STM32：在兼容系列上启用了 ART Accelerator、I-cache、D-cache 和预取。
  * STM32H5：新增对 Stop 模式和 :kconfig:option:`CONFIG_PM` 的支持。
  * STM32WL：将 Sub-GHz SPI 频率从 12MHz 降低到 8MHz。
  * STM32C0：新增对 :kconfig:option:`CONFIG_POWEROFF` 的支持。
  * STM32U5：新增对 Stop3 模式的支持。
  * Synopsys：

    * nsim：将 nsim 平台拆分为 arc_classic（基于 ARCv2 和 ARCv3 ISA）和 arc_v（基于 RISC-V ISA）
    * nsim/nsim_hs5x/smp：使系统时钟频率与其他 SMP nSIM 配置保持一致

  * NXP IMX8M：新增资源域控制器支持
  * NXP s32k146：将 RTC 时钟源设置为内部振荡器
  * GD32F4XX：修复了 uart4 中断号错误的问题。
  * Nordic nRF54L：新增对 FLPR（快速轻量级处理器）RISC-V CPU 的支持。
  * Espressif：从所有 ESP32 SoC 变体中移除了 idf-bootloader 依赖。
  * Espressif：为 ESP32 SoC 变体新增简单启动（Simple boot）支持，允许使用单个二进制映像加载应用，而无需二级引导程序。
  * Espressif：重新设计并优化了所有 SoC 的内存映射。
  * LiteX：

    * 新增对 :c:func:`sys_arch_reboot()` 的支持。
    * :kconfig:option:`CONFIG_RISCV_ISA_EXT_A` 不再被错误地选为 y。
  * rp2040：专有 UART 驱动已停用，并替换为 PL011。

  * Renesas RZ/T2M：新增系统时钟控制寄存器的默认值。

* 新增支持以下开发板：

  * 新增对 :zephyr:board:`Ambiq Apollo3 Blue 开发板 <apollo3_evb>` 的支持：``apollo3_evb``。
  * 新增对 :zephyr:board:`Ambiq Apollo3 Blue Plus 开发板 <apollo3p_evb>` 的支持：``apollo3p_evb``。
  * 新增对 :zephyr:board:`Raspberry Pi 5 开发板 <rpi_5>` 的支持：``rpi_5``。
  * 新增对 :zephyr:board:`Seeed Studio XIAO RP2040 开发板 <xiao_rp2040>` 的支持：``xiao_rp2040``。
  * 新增对 :zephyr:board:`Mikroe RA4M1 Clicker 开发板 <mikroe_clicker_ra4m1>` 的支持：``mikroe_clicker_ra4m1``。
  * 新增对 :zephyr:board:`Arduino UNO R4 WiFi 开发板 <arduino_uno_r4>` 的支持：``arduino_uno_r4_wifi``。
  * 新增对 :zephyr:board:`Renesas EK-RA8M1 开发板 <ek_ra8m1>` 的支持：``ek_ra8m1``。
  * 新增对 :zephyr:board:`ST Nucleo H533RE <nucleo_h533re>` 的支持：``nucleo_h533re``。
  * 新增对 :zephyr:board:`ST STM32C0116-DK 探索套件 <stm32c0116_dk>` 的支持：``stm32c0116_dk``。
  * 新增对 :zephyr:board:`ST STM32H745I Discovery <stm32h745i_disco>` 的支持：``stm32h745i_disco``。
  * 新增对 :zephyr:board:`ST STM32H7S78-DK Discovery <stm32h7s78_dk>` 的支持：``stm32h7s78_dk``。
  * 新增对 :zephyr:board:`ST STM32L152CDISCOVERY 开发板 <stm32l1_disco>` 的支持：``stm32l152c_disco``。
  * 新增对 :zephyr:board:`ST STEVAL STWINBX1 开发套件 <steval_stwinbx1>` 的支持：``steval_stwinbx1``。
  * 新增对 NXP 开发板的支持：``frdm_mcxn947`` 、``ke17z512`` 、``rd_rw612_bga`` 、``frdm_rw612`` 、``frdm_ke15z`` 、``frdm_ke17z``
  * 新增对 :zephyr:board:`Synopsys ARC-V RMX1xx 基于 nSIM 的仿真平台 <nsim_arc_v>` 的支持：``nsim_arc_v/rmx100``。
  * 新增对 :zephyr:board:`Analog Devices MAX32690EVKIT <max32690evkit>` 的支持：``max32690evkit``。
  * 新增对 :zephyr:board:`Analog Devices MAX32680EVKIT <max32680evkit>` 的支持：``max32680evkit``。
  * 新增对 :zephyr:board:`Analog Devices MAX32672EVKIT <max32672evkit>` 的支持：``max32672evkit``。
  * 新增对 :zephyr:board:`Analog Devices MAX32672FTHR <max32672fthr>` 的支持：``max32672fthr``。
  * 新增对 :zephyr:board:`Analog Devices MAX32670EVKIT <max32670evkit>` 的支持：``max32670evkit``。
  * 新增对 :zephyr:board:`Analog Devices MAX32655EVKIT <max32655evkit>` 的支持：``max32655evkit``。
  * 新增对 :zephyr:board:`Analog Devices MAX32655FTHR <max32655fthr>` 的支持：``max32655fthr``。
  * 新增对 :zephyr:board:`Analog Devices AD-APARD32690-SL <apard32690>` 的支持：``ad_apard32690_sl``。
  * 新增对 :zephyr:board:`Infineon Technologies CYW920829M2EVK-02 <cyw920829m2evk_02>` 的支持：``cyw920829m2evk_02``。
  * 新增对 :zephyr:board:`Nuvoton Numaker M2L31KI 开发板 <numaker_m2l31ki>` 的支持：``numaker_m2l31ki``。
  * 新增对 :zephyr:board:`Espressif ESP32-S2 DevKit-C <esp32s2_devkitc>` 的支持：``esp32s2_devkitc``。
  * 新增对 :zephyr:board:`Espressif ESP32-S3 DevKit-C <esp32s3_devkitc>` 的支持：``esp32s3_devkitc``。
  * 新增对 :zephyr:board:`Espressif ESP32-C6 DevKit-C <esp32c6_devkitc>` 的支持：``esp32c6_devkitc``。
  * 新增对 :zephyr:board:`Waveshare ESP32-S3-Touch-LCD-1.28 <esp32s3_touch_lcd_1_28>` 的支持：``esp32s3_touch_lcd_1_28``。
  * 新增对 :zephyr:board:`M5Stack ATOM Lite <m5stack_atom_lite>` 的支持：``m5stack_atom_lite``。
  * 新增对 :zephyr:board:`CTHINGS.CO Connectivity Card nRF52840 <ctcc>` 的支持：``ctcc``。

* 对开发板做了以下变更：

  * 在 :zephyr:board:`ST STM32H7B3I Discovery Kit <stm32h7b3i_dk>` （``stm32h7b3i_dk``）上，启用了完整的缓存管理、Chrom-ART、双帧缓冲和全刷新，以获得最佳的 LVGL 性能。
  * 在 ST STM32 开发板上，现在可以使用 stm32cubeprogrammer runner 并通过 ``--extload`` 选项对片外 flash 进行编程。
  * 为所有 NXP 开发板的 Linkserver 添加 HEX 文件支持
  * 更新了 Linkserver west runner，以反映 LinkServer v1.5.xx 的 CLI 变化
  * 为 NXP ``mimxrt1010_evk`` 、``mimxrt1160_evk`` 、``frdm_rw612`` 、``rd_rw612_bga`` 、``frdm_mcxn947`` 添加 LinkServer 支持
  * 引入了 :ref:`nrf54l15bsim<nrf54l15bsim>` 仿真目标。
  * nrf5x bsim 目标现在支持 BT LE Coded PHY。
  * 重构了 LLVM fuzzing 支持，同时为 native_sim 添加了该支持。
  * nRF54H20 PDK（预发布版）已转换为 :zephyr:board:`nrf54h20dk`
  * :zephyr:board:`nrf54h20dk` 中的 PPR 核心目标默认从 RAM 运行。新增了从 MRAM（XIP）运行的 ``xip`` 变体。
  * 重构了 :zephyr:board:`beagleconnect_freedom` 的外部天线切换处理。
  * 为 nRF5340 Audio DK 添加了 Arduino 设备树节点标签。
  * 将 nRF54L15 PDK 的默认修订版本从 0.2.1 改为 0.3.0。
  * 在基于 nRF5340 SoC 的开发板中，将对控制网络核心 Force-OFF 信号的寄存器的直接访问替换为一个模块，该模块使用开关管理器跟踪网络核心的使用情况，并在 ``<nrf53_cpunet_mgmt.h>`` 中暴露其 API。
  * Laird Connectivity 开发板已更名为 Ezurio。

* 新增对以下扩展板的支持：

  * :ref:`adafruit_2_8_tft_touch_v2` (``adafruit_2_8_tft_touch_v2``)
  * :ref:`adafruit_neopixel_grid_bff` (``adafruit_neopixel_grid_bff``)
  * :ref:`arduino_uno_click` (``arduino_uno_click``)
  * :ref:`dvp_fpc24_mt9m114` (``dvp_fpc24_mt9m114``)
  * :ref:`lcd_par_s035` (``lcd_par_s035``)
  * :ref:`mikroe_weather_click` (``mikroe_weather_click``)
  * :ref:`nxp_btb44_ov5640` (``nxp_btb44_ov5640``)
  * :ref:`reyax_lora` (``reyax_lora``)
  * :ref:`rk043fn02h_ct` (``rk043fn02h_ct``)
  * :ref:`rk043fn66hs_ctg` (``rk043fn66hs_ctg``)
  * :ref:`rpi_pico_uno_flexypin` (``rpi_pico_uno_flexypin``)
  * :ref:`seeed_xiao_expansion_board` (``seeed_xiao_expansion_board``)
  * :ref:`seeed_xiao_round_display` (``seeed_xiao_round_display``)
  * :ref:`sparkfun_carrier_asset_tracker` (``sparkfun_carrier_asset_tracker``)
  * :ref:`st_b_lcd40_dsi1_mb1166` (``st_b_lcd40_dsi1_mb1166``)
  * :ref:`waveshare_epaper` (``waveshare_epaper``)
  * :ref:`x_nucleo_bnrg2a1` (``x_nucleo_bnrg2a1``)

构建系统与基础设施
******************

  * 新增了 CI 启用的黑盒测试，用于验证大多数 Twister 标志的正确性。

  * 为应用引入了 ``socs`` 文件夹，允许为使用特定 SoC 和开发板限定符（board qualifier）的所有开发板目标应用 Kconfig 片段和设备树 overlay（:github:`70418`）。sysbuild 也已添加支持（:github:`71320`）。

  * 已添加 :ref:`开发板/SoC 烧录配置<flashing-soc-board-config>` 设置（:github:`69748`）。

  * 弃用了全局 CSTD cmake 属性，改用 :kconfig:option:`CONFIG_STD_C` 选项来选择 C 标准版本。此外，子系统可以选择所需的最低 C 标准版本，例如 :kconfig:option:`CONFIG_REQUIRES_STD_C11` 。

  * 修复了向使用 sysbuild 的应用传递 UTF-8 配置的问题（:github:`74152`）。

  * 修复了以下问题：如果 sysbuild 配置发生更改，sysbuild 项目中的 domain 文件会被加载并使用过时的信息，且之后会直接运行 ``west flash`` （:github:`73864`）。

  * 修复了 Zephyr 模块未设置 Kconfig 文件时不会在 sysbuild 中列出的问题（:github:`72070`）。

  * 新增 sysbuild Kconfig 选项 ``SB_CONFIG_COMPILER_WARNINGS_AS_ERRORS`` ，用于为所有映像打开“警告视为错误”的工具链标志（如果已设置）（:github:`70217`）。

  * 修复了项目中使用的文件（例如设备树 overlay 或 Kconfig 片段）未被正确监视、修改后 CMake 不会重新配置的问题（:github:`74655`）。

  * 为 LinkServer runner 新增对 Intel Hex 文件的烧录支持。

  * 新增 sysbuild ``sysbuild/CMakeLists.txt`` 入口点，并新增对 ``APPLICATION_CONFIG_DIR`` 的支持，可用于调整 sysbuild 的工作方式（:github:`72923`）。

  * 修复了 armfvp 查找路径包含冒号分隔列表时的问题（:github:`74868`）。

  * 修复了 version.cmake 字段大小未被执行的问题（:github:`74357`）。

  * 修复了 sysbuild 在处理映像前未清除 ``EXTRA_CONF_FILE`` ，导致该选项无法传递给映像的问题（:github:`74082`）。

  * 新增 sysbuild root 支持，其工作方式与现有 root 模块类似，会相对于 ``APP_DIR`` 调整路径（:github:`73390`）。

  * 为缺失的 blob 添加了警告和错误消息（:github:`73051`）。

  * 修复了在某些系统上检测正确 python 可执行文件的问题（:github:`72232`）。

  * 新增为整个应用启用 LTO 的支持（:github:`69519`）。

  * 修复了 ``FILE_SUFFIX`` 相关问题，包括后缀被重复应用、在 sysbuild 中未应用以及 CMake 函数中的变量名冲突（:github:`70124` 、:github:`71280`）。

  * 新增了新的激进尺寸优化标志（适用于 GCC 和 Clang）支持，通过 :kconfig:option:`CONFIG_SIZE_OPTIMIZATIONS_AGGRESSIVE` 启用（:github:`70511`）。

  * 修复了 ``BUILD_VERSION`` 为空时打印输出的问题（:github:`70970`）。

  * 修复了 sysbuild 中 ``sysbuild_cache_set()`` cmake 函数在去重时错误检测部分匹配的问题（:github:`71381`）。

  * 修复了检测到错误的 ``VERSION`` 文件的问题（:github:`71385`）。

  * 新增对禁用带源码的反汇编输出的支持，通过 :kconfig:option:`CONFIG_OUTPUT_DISASSEMBLY_WITH_SOURCE` 启用（:github:`71535`）。

  * Twister 现在支持 ``--flash-before`` 参数，允许在打开串口之前烧录 DUT（:github:`47037`）。

驱动与传感器
************

* ADC

  * 新增 ``ADC_DT_SPEC_*BY_NAME()`` 宏，用于按名称从设备树获取 ADC IO 通道信息。
  * 新增电压偏置支持：

    * 新增 :kconfig:option:`CONFIG_ADC_CONFIGURABLE_VBIAS_PIN` ，由支持电压偏置的驱动选择。
    * 为 adc-controller 基础绑定新增 ``zephyr,vbias-pins`` 属性，用于描述电压偏置引脚。
    * 已在 TI ADC114s08 ADC 驱动中实现。
  * 示例变更

    * 将现有 ADC 示例重命名为 adc_dt。
    * 新增名为 adc_sequence 的示例，展示了更多运行时的 :c:struct:`adc_sequence` 特性。
  * 新增 ADC 驱动

    * 新增 ENE KB1200 驱动。
    * 新增 NXP GAU ADC 驱动。
  * ADI AD559x 变更

    * 新增对 ADI ad5593 的支持。
    * 为 ADI ad559x 新增 I2C 总线支持。
    * 为 ad559x 新增内部参考电压值配置，以支持调用 :c:func:`adc_raw_to_millivolts()` 。
    * 修复了 ad559x 驱动中因驱动初始化导致与 :kconfig:option:`CONFIG_THREAD_NAME` 可用性相关的异常操作的问题。
    * 提高了 ad559x 驱动中 ADC 读取的效率和校验能力。
  * ESP32 变更

    * 更新 ESP32 ADC 驱动以兼容 hal_espressif 5.1 版本。
    * 新增对 ESP32S3 和 ESP32C3 的 DMA 模式操作的支持。
  * nRF 变更

    * 在 nrfx_saadc 驱动中新增对 nRF54L15 和 nRF54H20 的支持。
    * 改进 nRF SAADC 驱动：在未使用的通道上禁用突发（burst）模式，避免出现卡死。
    * 修复了使用 ``adc_nrfx_saadc.c`` 设备驱动时单端模式允许负 ADC 读数的问题。注意，由于硬件限制，此修复会使 nRF54H 和 nRF54L 系列无法执行 8 位分辨率的单端读数。
  * NXP LPADC 变更

    * 在 NXP LPADC 驱动中启用了采集时间（acquisition time）特性。
    * 为 NXP LPADC 新增对使用稳压器输出作为参考电压的支持。
    * 在 ``nxp,lpc-lpadc`` 绑定中，将 phandle 类型的设备树属性 ``nxp,reference-supply`` 改为 phandle-array 类型的设备树属性 ``nxp,references`` 。NXP LPADC 驱动现在支持通过 ``nxp,references`` 传递参考电压值。
  * Smartbond 变更

    * 为 Smartbond SDADC 和 GPADC 驱动新增电源管理支持。
    * 修复了 Smartbond ADC 驱动中对 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME` 的支持。
  * STM32 变更

    * 修复了 STM32 ADC 驱动中 DMA 支持的多个问题。
    * 新增对 STM32H7R/S 系列的支持。
  * 其他驱动变更

    * 在 numaker ADC 驱动中新增对 Nuvoton m2l31x 的支持。
    * 修复了 ads1119 驱动中配置寄存器访问的问题。
    * 修复了静态分析发现的 kb1200 驱动中未初始化值的问题。
    * 修复了 tla2021 驱动中 :c:func:`adc_raw_to_millivolts` 返回实际电压一半的问题，方法是修正参考电压值。


  * 新增对 Nuvoton Numaker M2L31X 系列的支持。

* 电池

  * 为 ``battery`` 绑定新增 ``re-charge-voltage-microvolt`` 属性。这样可以设置自动重新开始充电的阈值。

* 后备电池 RAM

  * 新增对 STM32G0 和 STM32H5 系列的支持。

* CAN

  * 扩展了自动采样点定位支持，现在也覆盖 :c:func:`can_calc_timing` 和 :c:func:`can_calc_timing_data` 。
  * 为 CAN 收发器新增可选的 ``min-bitrate`` 设备树属性。
  * 新增设备树宏 :c:macro:`DT_CAN_TRANSCEIVER_MIN_BITRATE` 和 :c:macro:`DT_INST_CAN_TRANSCEIVER_MIN_BITRATE` ，用于获取 CAN 收发器支持的最低比特率。
  * 在内部宏 ``CAN_DT_DRIVER_CONFIG_GET`` 和 ``CAN_DT_DRIVER_CONFIG_INST_GET`` 中新增对指定 CAN 控制器支持的最低比特率的支持。
  * 新增 :c:func:`can_get_bitrate_min` 和 :c:func:`can_get_bitrate_max` ，用于获取给定 CAN 控制器和 CAN 收发器组合支持的最低与最高比特率，表明获取比特率上下限不再会失败。弃用了现有的 :c:func:`can_get_max_bitrate` API 函数。
  * 更新了 CAN 定时函数，在校验比特率时会考虑支持的最低比特率。
  * 将 ``sample-point`` 和 ``sample-point-data`` 设备树属性改为可选。
  * 将 :c:struct:`can_driver_config` 的 ``bus_speed`` 和 ``bus_speed_data`` 字段重命名为 ``bitrate`` 和 ``bitrate_data`` 。
  * 新增 :dtcompatible:`nordic,nrf-can` 驱动。
  * 在 :dtcompatible:`nuvoton,numaker-canfd` 驱动中新增对 Numaker M2L31X 的驱动支持。
  * 新增主机通信测试套件。

* 充电器

  * 为 ``maxim,max20335-charger`` 新增 ``chgin-to-sys-current-limit-microamp`` 属性。
  * 为 ``maxim,max20335-charger`` 新增 ``system-voltage-min-threshold-microvolt`` 属性。
  * 为 ``maxim,max20335-charger`` 新增 ``re-charge-threshold-microvolt`` 属性。
  * 为 ``maxim,max20335-charger`` 新增 ``thermistor-monitoring-mode`` 属性。

* 时钟控制

  * 在 STM32H5 系列上新增对微控制器时钟输出（MCO）的支持。
  * 在 STM32WL 系列上新增对 MSI 时钟的支持。
  * 新增 Analog Devices MAX32 SoC 系列的驱动。
  * 新增对 Nuvoton Numaker M2L31X 系列的支持。
  * 重构 ESP32 时钟控制驱动以支持 ESP32-C6。
  * 在 LiteX（:file:`drivers/clock_control/clock_control_litex.c`）中，为 :c:func:`litex_clk_get_duty_cycle()` 和 :c:func:`litex_clk_get_clkout_divider` 增加了返回码检查。

* 计数器

  * 新增对 Ambiq Apollo3 系列的支持。
  * 新增对 STM32H7R/S 系列的支持。
  * 为 NXP MCXN947 新增 LPTMR 驱动
  * 在 ``nxp,lptmr`` 绑定中新增 ``resolution`` 属性，用于表示 LPTMR 外设计数器使用的最大位宽。

* DAC

  * 新增对 NXP RW SoC 系列 DAC 的支持（:dtcompatible:`nxp,gau-dac`）。
  * 新增对 Analog Devices AD5691 / AD5692 / AD5693 DAC 的支持（:dtcompatible:`adi,ad5691` 、:dtcompatible:`adi,ad5692` 和 :dtcompatible:`adi,ad5693`）。
  * 新增对 Texas Instruments DACx0501 系列 DAC 的支持（:dtcompatible:`ti,dacx0501`）。

* 磁盘

  * STM32 SD 驱动新增了对 eMMC 设备的支持。可通过 :kconfig:option:`CONFIG_SDMMC_STM32_EMMC` 启用。
  * 新增回环磁盘（loopback disk）驱动，用于暴露由文件支持的磁盘设备。可以使用 :c:func:`loopback_disk_access_register` 向回环磁盘驱动注册文件
  * 新增对 :c:macro:`DISK_IOCTL_CTRL_INIT` 和 :c:macro:`DISK_IOCTL_CTRL_DEINIT` 宏的支持，允许在运行时初始化和取消初始化磁盘。这使得可热插拔的磁盘设备（如 SD 卡）可以在运行时移除并重新插入。
  * 为 STM32H5 系列新增 SDMMC 支持。

* 显示

  * 所有能够支持 :ref:`mipi_dbi_api` 的树内显示器都已改为使用该 API。基于 GC9X01X、UC81XX、SSD16XX、ST7789V、ST7735R 的显示器均已转换到此 API。使用这些显示器的开发板需要更新其设备树，转换过程示例请参阅 :ref:`migration_3.7` 的显示器章节。
  * 新增 ST7796S 显示控制器驱动（:dtcompatible:`sitronix,st7796s`）
  * 为 ILI9XXX 显示驱动新增对 :c:func:`display_read` API 的支持，可通过 :kconfig:option:`CONFIG_ILI9XXX_READ` 启用
  * 为 SSD16XXX 显示驱动新增对 :c:func:`display_set_orientation` API 的支持
  * 新增 NT35510 MIPI-DSI 显示控制器驱动（:dtcompatible:`frida,nt35510`）
  * 新增用于将 LED 灯带设备抽象为显示器的驱动（:dtcompatible:`led-strip-matrix`）
  * 为 NXP eLCDIF 驱动新增对 :c:func:`display_set_pixel_format` API 的支持。支持 ARGB8888、RGB888 和 BGR565 格式。
  * 通过 :c:func:`display_set_pixel_format` API，为 SSD1306 驱动新增运行时反转颜色的支持。
  * 现在可以使用 ``inversion-off`` 属性在 ST7789V 驱动（:dtcompatible:`sitronix,st7789v`）中禁用反转模式。
  * 新增对 NXP MCXNx4x 的支持

* DMA

  * 错误回调配置已重命名，以更好地表明启用或禁用状态
  * 新增对 NXP MCXN947 的支持

* DMIC

  * 新增对 NXP ``rd_rw612_bga`` 的支持

* 熵源

  * 新增对 STM32H7R/S 系列的支持。

* EEPROM

  * 为 :dtcompatible:`zephyr,i2c-target-eeprom` 新增用于指定 ``address-width`` 的属性。

* eSPI

  * 重命名了 eSPI 虚拟线方向宏、枚举值和 Kconfig，以匹配 eSPI 1.5 规范中的新术语。

* 以太网

  * 引入 :kconfig:option:`CONFIG_ETH_DRIVER_RAW_MODE` 。该选项允许在没有 Zephyr L2 以太网层的情况下构建以太网驱动。
  * 移除了 ethernet-fixed-link 设备树绑定。
  * 从以太网驱动中移除了 VLAN 处理，因为现在由通用以太网 L2 代码处理。
  * 在 eth_mcux、eth_nxp_enet、eth_nxp_s32_gmac、eth_stm32 和 eth_nxp_s32_netc 驱动中实现并重构了硬件 MAC 地址过滤。
  * 新增驱动

    * 为 NXP MCXN SoC 上的以太网控制器新增 eth_nxp_enet_qos 驱动。
    * 新增对 adin1100 phy 的支持。
    * 新增对 Realtek RTL8211F PHY 的支持。
  * NXP ENET 驱动变更

    * eth_nxp_enet 驱动不再是实验性的。
    * 弃用了 eth_mcux 驱动。
    * 所有具有 :dtcompatible:`nxp,kinetis-ethernet` 兼容节点的开发板和 SoC 都已改为使用新的 :dtcompatible:`nxp,enet` 绑定。
    * 在 Kinetis 平台上新增对使用 nxp_enet 驱动进行网络设备电源管理的支持。
    * 将 eth_nxp_enet 驱动改为使用由内核管理的专用工作队列处理 RX，而不是手动无限循环。
    * 在 eth_nxp_enet 中启用 IPV6 时禁用硬件校验和加速，因为硬件不支持加速 ICMPv6 校验和。
    * 新增对 :dtcompatible:`nxp,enet1g` 的支持。
    * 在某些平台上新增对 nxp_enet MAC 使用熔断（fused）MAC 地址的支持。
    * 修复了未设置 LAA 位的问题，以及 nxp_enet 驱动所用 nxp,unique-mac 属性说明令人困惑的问题。
    * 修复了 nxp_enet 驱动中使用非缓存 DMA 缓冲区时仍启用缓存维护的问题。
    * 为 nxp_enet 驱动新增 MMIO 映射。
    * 澄清了 eth_nxp_enet 对 DSA 的支持。
  * NXP S32 以太网变更

    * eth_nxp_s32_gmac 驱动现在会隐含启用 :kconfig:option:`CONFIG_MDIO` 。
    * eth_nxp_s32_netc 驱动已更新为使用新的 MBOX API。
  * Adin2111 驱动变更

    * 修正了 adin2111 驱动中 IAMSK1 TX_READY_MASK 的位域位置。
    * 将 adin2111 驱动改为始终在帧末尾追加 crc32。
    * 调整 eth_adin2111 驱动，使其具有合适的多播过滤器掩码。
    * 修复了 adin2111 驱动的“不使用 crc8 的通用 SPI”模式。
    * 为 adin2111 驱动新增 Open Alliance SPI 协议支持。
    * 为 adin2111 驱动新增自定义驱动扩展 API。
    * 在 adin2111 驱动中启用了混杂（promiscuous）模式支持。
    * 将 OA 缓冲区从 adin2111 驱动的设备数据中移出，以便在使用通用 SPI 协议时节省约 32KB 空间。
    * 修复了 64 位平台上 eth_adin2111 驱动的构建警告。
    * 对 adin2111 驱动做了各种小幅修改。
  * STM32 以太网驱动变更

    * 在兼容的 STM32 系列（STM32F7、STM32H5 和 STM32H7）上新增 PTP 支持。
    * 将 eth_stm32 改为使用 PHY API 访问 PHY，以避免多任务时发生冲突。
    * 移除了对 STM32 F4、F7 和 H7 系列的旧版 STM32Cube HAL API 支持。
    * 为 eth_stm32_hal 驱动新增 RX/TX 时间戳支持。
  * ESP32 以太网驱动变更

    * 为 esp32 以太网驱动新增在运行时设置 MAC 地址的支持。
    * 更新 esp32 以太网驱动以兼容 hal_espressif 5.1 版本。
    * 修复了启用 :kconfig:option:`CONFIG_NET_STATISTICS` 时 esp32 以太网驱动的构建问题。
    * 修复了 ESP32 以太网驱动无法通过 GPIO 正确为外部 PHY 提供时钟的问题。
  * 其他以太网驱动变更

    * 为 w5500 以太网驱动新增链路状态检测，可通过 Kconfig 配置。
    * 为 eth_liteeth 驱动新增在运行时设置 MAC 地址的能力。
    * 修复了 eth_stellaris 驱动中未考虑驱动接收的中断数可能少于以太网控制器接收的数据包数的问题。
    * 为 enc28j60 新增用于设置 RX 过滤器的设备树属性。
    * 修复了 enc28j60 驱动中出错时未清除 ESTAT TXABRT 位的问题。
    * 新增条件，在启用 PTP 子系统时为 native_posix 以太网驱动启用 ptp_clock 驱动实现。
    * 修复了 KSZ8xxx 的 DSA 驱动无法正确初始化 LAN 设备的问题。
    * 修复了 ksz8863 中使用错误寄存器地址使能尾部标签（tail tag）的问题。
  * Phy 驱动变更

    * 修复了 KSZ8081 PHY 驱动中复位、自动协商、链路检测以及日志消息缺失或刷屏等各种控制问题。
    * 更改了 KSZ8081 设备树绑定中复位和中断 GPIO 的属性名。
    * 修复了使用 fixed-link 模式时 phy_mii 驱动的总线故障。

* Flash

  * 新增对 Ambiq Apollo3 系列的支持。
  * 新增对 SPI NOR 驱动（spi_nor.c）多实例的支持。
  * 为不支持擦除的设备新增了初步支持：在 :c:struct:`flash_parameters` 中引入设备能力，并新增工具函数 :c:func:`flash_params_get_erase_cap` ，用于获取设备提供的擦除类型；新增 :c:macro:`FLASH_ERASE_C_EXPLICIT` ，它是目前唯一支持的擦除类型，由所有 flash 设备设置。
  * 新增 :c:func:`flash_flatten` 函数，可用于有擦除要求或无擦除要求的设备，适用于擦除不是为随机数据写入做准备，而是要从设备中移除或扰乱数据的场景。
  * 新增 :c:func:`flash_fill` 工具函数，允许在选定设备的指定范围内写入同一个值。
  * 新增对 nrf54l15 设备上 RRAM 的支持。
  * 在 STM32 OSPI 驱动中新增对非忙等待轮询（non busy wait polling）的支持。
  * 新增对 STM32 XSPI 外部 NOR flash 驱动的支持（:dtcompatible:`st,stm32-xspi-nor`）。
  * 在 STM32 OSPI、QSPI 和 XSPI 驱动中新增对外部 NOR flash 上 XIP 的支持。
  * STM32 OSPI 驱动：clk、dqs、ncs 端口现在可以通过设备树配置（参见 :dtcompatible:`st,stm32-ospi`）。
  * 为 NXP MCXN947 新增 FlexSPI 支持
  * 新增对 Nuvoton Numaker M2L31X 系列的支持。

* 电量计

  * max17048：将电压单位从 mV 修正为 uV。

* GNSS

  * 新增 GNSS 设备驱动 API 测试套件。
  * 新增对 u-blox UBX 协议的支持。
  * 新增 u-blox M8 GNSS 调制解调器的设备驱动（:dtcompatible:`u-blox,m8`）。
  * 新增 Luatos Air530z GNSS 调制解调器的设备驱动（:dtcompatible:`luatos,air530z`）。

* GPIO

  * 新增对 Ambiq Apollo3 系列的支持。
  * 新增 Broadcom 机顶盒（brcmstb）SoC GPIO 驱动。
  * 新增 :c:macro:`STM32_GPIO_WKUP` 标志，允许在 STM32 L4、U5、WB 和 WL SoC 系列上将特定引脚配置为从 Power Off 状态唤醒的唤醒源。
  * 新增 Analog Devices MAX32 SoC 系列的驱动。
  * 新增对 Nuvoton Numaker M2L31X 系列的支持。
  * 为 Renesas RZ/T2M GPIO 驱动（:dtcompatible:`renesas,rzt2m-gpio`）新增中断支持。

* 硬件信息

  * 为 STM32WB、STM32WBA 和 STM32WL 系列新增设备 EUI64 ID 支持及实现。

* I2C

  * 新增对 Ambiq Apollo3 系列的支持。
  * 在 STM32 V2 驱动中新增对新的 :kconfig:option:`CONFIG_I2C_STM32_V2_TIMING` 的支持，该选项会根据所用的时钟配置自动计算用于配置硬件模块的总线时序。为了避免在生产应用中嵌入这一重量级算法，提供了一个专用示例 :zephyr:code-sample:`stm32_i2c_v2_timings` 来获取算法输出。一旦获得总线时序配置，就可以禁用 :kconfig:option:`CONFIG_I2C_STM32_V2_TIMING` ，并改用设备树配置总线时序。
  * 新增对 STM32H5 系列的支持。
  * 为 NXP MCXN947 新增支持
  * 新增 Analog Devices MAX32 SoC 系列的驱动。
  * 新增对 Nuvoton Numaker M2L31X 系列的支持。
  * LiteX I2C 驱动（:file:`drivers/i2c/i2c_litex.c`）：

    * 新增从设备树设置比特率的支持。
    * 新增 :c:func:`i2c_litex_recover_bus()` 和 :c:func:`i2c_litex_get_config()` API 实现。

* I2S

  * 新增对 STM32H5 系列的支持。
  * 扩展 MCUX Flexcomm 驱动以支持更多通道和格式。
  * 新增对 Nordic nRF54L 系列的支持。
  * 修复了 nRF I2S 驱动中的分频计算。

* I3C

  * 新增用于查询总线和 CCC 命令的 shell 支持。

  * 新增支持 NPCX 上 I3C 控制器的驱动。

  * 对 :dtcompatible:`nxp,mcux-i3c` 的改进和缺陷修复，包括更优雅地处理总线忙的情况，而不是直接返回错误。

* 输入

  * 新驱动：:dtcompatible:`adc-keys` 、:dtcompatible:`chipsemi,chsc6x` 、:dtcompatible:`cirque,pinnacle` 、:dtcompatible:`futaba,sbus` 、:dtcompatible:`pixart,pat912x` 、:dtcompatible:`pixart,paw32xx` 、:dtcompatible:`pixart,pmw3610` 和 :dtcompatible:`sitronix,cf1133` 。
  * 将 :dtcompatible:`holtek,ht16k33` 和 :dtcompatible:`microchip,xec-kbd` 从 kscan 迁移到 input 子系统。

* LED

  * 为 LED shell 命令新增设备补全，并使 ``get_info`` 命令以字符串显示颜色。

  * 新增 Lumissil Microsystems（ISSI 旗下部门）IS31FL3194 控制器驱动（:dtcompatible:`issi,is31fl3194`）。

* LED 灯带

  * 已将 ``chain-length`` 和 ``color-mapping`` 属性添加到所有 LED 灯带绑定中。

  * 现在更新灯带之前会检查其长度，如果提供的数据过长则返回错误。

  * 新增了返回 LED 灯带长度的长度函数（:c:func:`led_strip_length`）。

  * 更新通道的函数现在是可选的，可以不实现。

  * 相应 :dtcompatible:`worldsemi,ws2812-gpio` 和 :dtcompatible:`worldsemi,ws2812-rpi_pico-pio` 设备树绑定中的 ``in-gpios`` 和 ``output-pin`` 属性已重命名为 ``gpios`` 。

  * 移除了 ``CONFIG_WS2812_STRIP`` 和 ``CONFIG_WS2812_STRIP_DRIVER`` Kconfig 选项。重构后它们已无用。

  * 新增 Texas Instruments TLC59731 RGB 控制器驱动。

* LoRa

  * 新增 Reyax LoRa 模块驱动

* 邮箱

  * 新增基于 HSEM 的 STM32 驱动支持。

* MDIO

  * 将 ``bus_enable`` 和 ``bus_disable`` 函数改为驱动可选实现，并移除了许多驱动中的空实现。
  * 新增 NXP ENET QOS MDIO 控制器驱动。
  * 修复了 NXP ENET MDIO 驱动阻塞系统工作队列的 bug。
  * :kconfig:option:`CONFIG_MDIO_NXP_ENET_TIMEOUT` 的单位改为微秒。
  * 新增对 STM32 MDIO 控制器驱动的支持。

* MFD

  * 新驱动 :dtcompatible:`nxp,lp-flexcomm` 。
  * 新驱动 :dtcompatible:`rohm,bd8lb600fs` 。
  * 新驱动 :dtcompatible:`maxim,max31790` 。
  * 新驱动 :dtcompatible:`infineon,tle9104`
  * 新驱动 :dtcompatible:`adi,ad559x`
  * 新增用于禁用 :dtcompatible:`x-powers,axp192` 的 N_VBUSEN 的选项。
  * 为 :dtcompatible:`nordic,npm1300` 新增 GPIO 输入边沿事件。
  * 为 :dtcompatible:`nordic,npm1300` 新增长按复位配置。
  * 修复了 :dtcompatible:`nordic,npm6001` 迟滞模式（hysteretic mode）的初始化。

* 调制解调器

  * 移除了已弃用的 ``GSM_PPP`` 驱动及其设备树兼容字符串 ``zephyr,gsm-ppp`` 。

  * 移除了 ``GSM_PPP`` 之前使用的已弃用 ``UART_MUX`` 和 ``GSM_MUX`` 。

  * 从 ``MODEM_CELLULAR`` 驱动中移除了对设备树兼容字符串 ``zephyr,gsm-ppp`` 的支持。

  * 从 ``MODEM_IFACE_UART_INTERRUPT`` 模块中移除了与 ``UART_MUX`` 的集成。

  * 从 ``MODEM_SHELL`` 模块中移除了与 ``UART_MUX`` 的集成。

  * 在 ``MODEM_CELLULAR`` 驱动中实现了调制解调器管道链路（pipelink），以支持不同调制解调器提供的额外 DLCI 通道。这包括通用 AT 模式 DLCI 通道（命名为 ``user_pipe_<index>``）以及为 GNSS 隧道保留的 DLCI 通道（命名为 ``gnss_pipe``）。

  * 新增一组 shell 命令，可使用新实现的调制解调器管道链路直接向调制解调器发送 AT 命令。新 shell 命令的实现既实用，又与 ``MODEM_CELLULAR`` 驱动一起提供了如何实现和使用调制解调器管道链路模块的示例。

* PCIE

  * ``pcie_bdf_lookup`` 和 ``pcie_probe`` 已被移除，因为它们自 v3.3.0 起就已弃用。

* MIPI-DBI

  * 新增 release API
  * 新增通过设备树进行模式选择的支持

* MSPI

  * 新增实验性的 :ref:`MSPI（多位 SPI） <mspi_api>` API，支持通常需要命令、地址和数据阶段以及可变传输延迟的高级 SPI 控制器和外设。该 API 现在支持从单线 SDR 到六线 DDR 的同步和异步通信。
  * 在总线仿真器下新增 MSPI 总线仿真器，用于展示 MSPI API 的实现。
  * 新增 MSPI flash 设备仿真器，用于展示 MSPI API 的使用以及与 MSPI 总线控制器的对接。
  * 新增 APS6404L QPI pSRAM 设备驱动。
  * 新增 ATXP032 OPI NOR flash 设备驱动。
  * 新增 Ambiq Apollo3p MSPI 控制器驱动。
  * 新增 :zephyr:code-sample:`mspi-async` 和 :zephyr:code-sample:`mspi-flash` 示例，以展示 MSPI 设备驱动的用法。
  * 新增 mspi/api 和 mspi/flash 测试用例，供开发者检查自己的实现。

* 引脚控制

  * 新增 Renesas RA8 系列驱动
  * 新增 Infineon PSoC6 驱动（旧版）
  * 新增 Analog Devices MAX32 SoC 系列的驱动。
  * 新增 Ambiq Apollo3 驱动
  * 新增 ENE KB1200 驱动
  * 新增 NXP RW 驱动
  * Espressif 驱动现在支持 ESP32C6
  * STM32 驱动现在支持 STM32C0 的重映射（remap）功能
  * 新增对 Nuvoton Numaker M2L31X 系列的支持。

* PWM

  * 新增对 STM32H7R/S 系列的支持。
  * 为 NXP imxrt11xx 新增 QTMR PWM 驱动
  * 使 NXP MCUX PWM 驱动线程安全
  * 修复 :zephyr:code-sample:`pwm-blinky` 代码示例，以演示 :zephyr:board:`beagleconnect_freedom` 的 PWM 支持。
  * 新增 ENE KB1200 的驱动。
  * 新增对 Nordic nRF54H 和 nRF54L 系列 SoC 的支持。
  * 新增对 Nuvoton Numaker M2L31X 系列的支持。

* 稳压器

  * 新驱动 :dtcompatible:`cirrus,cp9314` 。
  * 为通用稳压器驱动新增 ``regulator-boot-off`` 属性。已将 :dtcompatible:`adi,adp5360-regulator` 、:dtcompatible:`nordic,npm1300-regulator` 、:dtcompatible:`nordic,npm6001-regulator` 和 :dtcompatible:`x-powers,axp192-regulator` 更新为使用该新属性。
  * 为 :dtcompatible:`renesas,smartbond-regulator` 新增电源管理。
  * 新增 ``is_enabled`` shell 命令。
  * 移除了单线程系统中对忙等待的使用。
  * 修复了 :dtcompatible:`x-powers,axp192-regulator` 的 DCDC2 输出控制。
  * 修复了 :dtcompatible:`renesas,smartbond-regulator` 的电流和电压获取函数。
  * 修复了 NXP VREF 的 Kconfig 泄漏问题。
  * 修复了 shell 中微单位值的显示。
  * 修复了 ``adset`` shell 命令中 strcmp 用法错误的问题。

* 复位

  * 新增 Nuvoton NPCX 芯片上复位控制器的驱动。
  * 新增 NXP SYSCON 的复位控制器驱动。
  * 新增 NXP RSTCTL 的复位控制器驱动。
  * 新增对 Nuvoton Numaker M2L31X 系列的支持。

* RTC

  * 新增 Raspberry Pi Pico RTC 驱动。
  * 在所有 STM32 MCU 系列（STM32F1 除外）上新增对 :kconfig:option:`CONFIG_RTC_ALARM` 的支持。
  * 新增对 Nuvoton Numaker M2L31X 系列的支持。

* RTIO

  * 将无锁队列从 RTIO 移到 lib 中，并为 SPSC 和 MPSC 队列去掉 ``rtio_`` 前缀。
  * 新增测试并修复了与链式回调请求相关的 bug。
  * 为 p4wq（RTIO workq）创建了包装层，以便在原生异步 RTIO 功能不可用时从阻塞行为转为非阻塞行为。

* SDHC

  * 新增 ESP32 SDHC 驱动（:dtcompatible:`espressif,esp32-sdhc`）。
  * 新增 Renesas MMC 控制器（:dtcompatible:`renesas,rcar-mmc`）的 SDHC 驱动。

* 传感器

  * 通用

    * 为新的读取/解码 API 新增通道说明符（channel specifier）。
    * 新增阻塞式传感器读取调用 :c:func:`sensor_read` 。
    * 使用 RTIO 工作队列服务解耦 RTIO 请求，使 :c:func:`sensor_submit_callback` 变为异步请求。
    * 将大多数驱动移动到厂商子目录中。

  * AMS

    * 新增 TSL2591 光传感器驱动（:dtcompatible:`ams,tsl2591`）。

  * Aosong

    * 新增 DHT20 数字输出湿度和温度传感器驱动（:dtcompatible:`aosong,dht20`）。

    * 为 dht11 驱动新增 :kconfig:option:`CONFIG_DHT_LOCK_IRQS` ，允许在读取传感器期间锁定中断，以避免读取传感器时出现问题。

  * Bosch

    * 将 BME280 更新到新的异步 API。

  * Infineon

    * 新增 TLE9104 动力总成开关诊断传感器驱动（:dtcompatible:`infineon,tle9104-diagnostics`）。

  * Maxim

    * 新增 DS18S20 1-Wire 温度传感器驱动（:dtcompatible:`maxim,ds18s20`）。
    * 新增 MAX31790 风扇转速和风扇故障传感器（:dtcompatible:`maxim,max31790-fan-fault` 和 :dtcompatible:`maxim,max31790-fan-speed`）。

  * NXP

    * 新增低功耗比较器驱动（:dtcompatible:`nxp,lpcmp`）。

  * Rohm

    * 新增 BD8LB600FS 诊断传感器驱动（:dtcompatible:`rohm,bd8lb600fs-diagnostics`）。

  * Silabs

    * 对 SI7006 湿度和温度传感器驱动做了多项修复和增强。

  * ST

    * QDEC 驱动现在支持编码器模式配置（参见 :dtcompatible:`st,stm32-qdec`）。
    * 新增对 STM32 数字温度传感器（:dtcompatible:`st,stm32-digi-temp`）的支持。
    * 新增 IIS328DQ I2C/SPI 加速度计传感器驱动（:dtcompatible:`st,iis328dq`）。

  * TDK

    * 为 MPU6050 驱动新增对 MPU6500 三轴加速度计和三轴陀螺仪传感器的支持。

  * TI

    * 新增 TMP114 驱动（:dtcompatible:`ti,tmp114`）。
    * 新增 INA226 双向电流和功率监测器驱动（:dtcompatible:`ti,ina226`）。
    * 新增 LM95234 四路远程二极管和本地温度传感器驱动（:dtcompatible:`national,lm95234`）。

  * 其他厂商

    * 新增 Angst+Pfister FCX-MLDX5 O2 传感器驱动（:dtcompatible:`ap,fcx-mldx5`）。
    * 新增 ENE KB1200 转速计传感器驱动（:dtcompatible:`ene,kb1200-tach`）。
    * 新增 Festo VEAA-X-3 系列比例压力调节器驱动（:dtcompatible:`festo,veaa-x-3`）。
    * 新增 Innovative Sensor Technology TSic xx6 温度传感器驱动（:dtcompatible:`ist,tsic-xx6`）。
    * 新增 ON Semiconductor NCT75 温度传感器驱动（:dtcompatible:`onnn,nct75`）。
    * 新增 ScioSense ENS160 数字金属氧化物多气体传感器驱动（:dtcompatible:`sciosense,ens160`）。
    * 对 GROW_R502A 指纹传感器驱动做了多项修复和增强。

* 串行接口

  * 新增使用 NUS（Nordic UART Service）通过蓝牙 LE 支持 UART 的驱动。该驱动使蓝牙可以作为当前 UART 支持的所有子系统（例如 Console、Shell、Logging）的传输通道。
  * 在 STM32 驱动的异步 DMA 模式下新增 :kconfig:option:`CONFIG_NOCACHE_MEMORY` 支持。现在只要将 DMA 缓冲区放在非缓存内存段中，就可以在启用 :kconfig:option:`CONFIG_DCACHE` 的 STM32 F7 和 H7 SoC 系列上使用 DMA 模式的 UART。
  * 新增对 STM32H7R/S 系列的支持。

  * 为 Renesas RCar 平台的 UART 驱动新增对 HSCIF（带 FIFO 的高速串行通信接口）的支持。

  * 新增 ENE KB1200 UART 驱动。

  * 新增 Analog Devices MAX32 系列微控制器上 UART 的驱动。

  * 新增 Renesas RA8 设备上 UART 的驱动。

  * ``uart_emul`` (:dtcompatible:`zephyr,uart-emul`):

    * 为仿真 UART 驱动新增异步 API 支持。

  * ``uart_esp32`` (:dtcompatible:`espressif,esp32-uart`):

    * 新增反转 TX 和 RX 引脚信号的支持。

    * 新增对 ESP32C6 SoC 的支持。

  * ``uart_native_tty`` (:dtcompatible:`zephyr,native-tty-uart`):

    * 新增仿真中断驱动 UART 的支持。

  * ``uart_mcux_lpuart`` (:dtcompatible:`nxp,kinetis-lpuart`):

    * 新增单线半双工通信支持。

    * 新增反转 TX 和 RX 引脚信号的支持。

  * ``uart_npcx`` (:dtcompatible:`nuvoton,npcx-uart`):

    * 新增异步 API 支持。

    * 新增 3MHz 波特率支持。

  * ``uart_nrfx_uarte`` (:dtcompatible:`nordic,nrf-uarte`):

    * 新增在 UART 不活动时将 TX 和 RX 引脚置于低功耗模式的支持。

  * ``uart_nrfx_uarte2`` (:dtcompatible:`nordic,nrf-uarte`):

    * 防止设备挂起时 UART 发送数据。

    * 修复了部分事件未被触发的问题。

  * ``uart_pl011`` (:dtcompatible:`arm,pl011`):

    * 新增运行时配置支持。

    * 新增复位设备支持。

    * 新增使用时钟控制确定频率的支持。

    * 新增硬件流控支持。

    * 新增 Ambiq Apollo3 SoC 上 UART 的支持。

  * ``uart_smartbond`` (:dtcompatible:`renesas,smartbond-uart`):

    * 新增电源管理支持。

    * 新增通过 DTR 和 RX 线唤醒的支持。

  * ``uart_stm32`` (:dtcompatible:`st,stm32-uart`):

    * 新增识别 DMA 缓冲区位于数据缓存还是不可缓存内存的支持。

  * 新增对 Nuvoton Numaker M2L31X 系列的支持。

* SPI

  * 为 NXP MCXN947 新增支持
  * 新增对 Ambiq Apollo3 系列通用 IOM 的 SPI 支持。
  * 新增对基于 Ambiq Apollo3 BLEIF 的 SPI 的支持，该 SPI 专用于内部 HCI。
  * 在 STM32 SPI 驱动上新增对 :kconfig:option:`CONFIG_PM` 和 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME` 的支持。
  * 在 STM32F7x SoC 系列的 DMA SPI 模式中新增对 :kconfig:option:`CONFIG_NOCACHE_MEMORY` 的支持。
  * 新增对 STM32H7R/S 系列的支持。
  * 新增 Analog Devices MAX32 SoC 系列的驱动。
  * 修复了 gd32 SPI 中寄存器赋值错误的问题。

* USB

  * 为 NXP EHCI 和 IP3511 USB 控制器新增 UDC shim 驱动。
  * 对 IT82xx2、DWC2、STM32、RP2040、Smartbond USB 控制器驱动做了多项修复和改进。

* 视频

  * 新增对 STM32 数字摄像头接口（DCMI）驱动的支持（:dtcompatible:`st,stm32-dcmi`）。
  * 启用了 NXP USB 设备控制器
  * 新增对 ov7670 摄像头的支持
  * 新增对 ov5640 摄像头的支持
  * 为 NXP MCUX 新增 CSI-2 MIPI 驱动
  * 新增对 DVP FPC 24 引脚 mt9m114 摄像头模块扩展板的支持

* 看门狗

  * 新增 :kconfig:option:`CONFIG_WDT_NPCX_WARNING_LEADING_TIME_MS` ，用于以毫秒为单位设置前置警告时间。移除了不再使用的 :kconfig:option:`CONFIG_WDT_NPCX_DELAY_CYCLES` 。
  * 新增对 Ambiq Apollo3 系列的支持。
  * 新增对 STM32H7R/S 系列的支持。
  * 新增对 Nuvoton Numaker M2L31X 系列的支持。
  * 为 ESP32 SoC 变体新增外部 32kHz 晶振看门狗。

* Wi-Fi

  * 修复了 esp-at 的消息解析。
  * 修复了 esp-at 连接失败的问题。
  * 为 esp-at 的 UDP socket 实现 :c:func:`bind` 和 :c:func:`recvfrom` 。
  * 新增设置 eswifi 最大数据大小的选项。
  * 修复了 ESP32 Wi-Fi 驱动的内存泄漏。

网络
****

* ARP:

  * 新增免费 ARP（gratuitous ARP）发送支持。
  * 修复了 ARP 模块内 TX 和 RX 线程之间可能出现的死锁。
  * 修复了可能出现的 ARP 表项泄漏。
  * 改进了 ARP 调试日志。

* CoAP：

  * 修复了 CoAP observe 的 age 值溢出问题。
  * 提高了 CoAP 重传次数上限（:kconfig:option:`CONFIG_COAP_MAX_RETRANSMIT`）。
  * 修复了 CoAP 客户端库中的 CoAP 观察（observation）功能。
  * 新增 CoAP 客户端 :c:func:`coap_client_cancel_requests` API，可用于取消活动的观察（observation）。
  * 修复了 CoAP Server 示例中响应的 CoAP ID 生成。

* 连接管理器：

  * 新增对新的 net_mgmt 事件的支持，可以分别跟踪 IPv4 和 IPv6 连接状态：

    * :c:macro:`NET_EVENT_L4_IPV4_CONNECTED`
    * :c:macro:`NET_EVENT_L4_IPV4_DISCONNECTED`
    * :c:macro:`NET_EVENT_L4_IPV6_CONNECTED`
    * :c:macro:`NET_EVENT_L4_IPV6_DISCONNECTED`

* DHCPv4:

  * 新增对封装形式厂商特定选项的支持。通过启用 :kconfig:option:`CONFIG_NET_DHCPV4_OPTION_CALLBACKS_VENDOR_SPECIFIC` ，可以使用 :c:func:`net_dhcpv4_add_option_vendor_callback` 注册回调，以便在用 :c:func:`net_dhcpv4_init_option_vendor_callback` 初始化后处理这些选项。
  * 新增对“厂商类标识符”选项的支持。使用 :kconfig:option:`CONFIG_NET_DHCPV4_VENDOR_CLASS_IDENTIFIER` 启用，使用 :kconfig:option:`CONFIG_NET_DHCPV4_VENDOR_CLASS_IDENTIFIER_STRING` 设置。
  * 现在可以使用 DHCPv4 选项中的 NTP 服务器来设置系统时间。如果启用了 :kconfig:option:`CONFIG_NET_CONFIG_CLOCK_SNTP_INIT` ，默认就会这样做。
  * 现在可以通过 DHCPv4 选项设置 syslog 服务器地址。如果启用了 :kconfig:option:`CONFIG_LOG_BACKEND_NET_USE_DHCPV4_OPTION` ，默认就会这样做。
  * 修复了不会向服务器请求已注册回调的选项的 bug。
  * 修复了从服务器收到的网络掩码未正确应用的 bug。
  * 重新实现了 DHCPv4 客户端的 RENEW/REBIND 逻辑，以符合 RFC2131。
  * 改进了 DHCPv4 服务器中已拒绝地址的管理，这些地址现在可以在配置的时间之后重新使用。
  * 修复了 DHCPv4 服务器响应中未按 RFC6842 包含客户端 ID 选项的问题。
  * 新增 :kconfig:option:`CONFIG_NET_DHCPV4_SERVER_NAK_UNRECOGNIZED_REQUESTS` ，允许覆盖 RFC 定义的行为，对来自未识别客户端的请求返回 NAK。
  * 修复了 DHCPv4 服务器中的客户端 ID 生成。
  * DHCPv4 客户端和服务器实现中的其他小幅修复。

* DHCPv6:

  * 修复了 net_mgmt 事件中不正确的 DHCPv6 事件代码基。
  * 新增 :kconfig:option:`CONFIG_NET_DHCPV6_DUID_MAX_LEN` ，可用于配置支持的最大 DUID 长度。
  * 新增 DHCPv6 文档页面。

* DNS/mDNS/LLMNR:

  * 修复了同时启用 mDNS Resolver 时 mDNS Responder 无法工作的问题。现在可以同时使用 mDNS Resolver 和 mDNS Responder。
  * 重构了 LLMNR 和 mDNS 响应器以及 DNS 解析器，使其使用 socket 和 socket 服务 API。
  * 新增 ANY 查询资源类型。
  * 新增 mDNS 在运行时提供记录的支持。
  * 新增缓存 DNS 记录的支持。
  * 修复了 socket 创建失败时以及所有结果都已返回时返回的错误码。
  * 修复了 DNS 重传超时计算。

* gPTP/PTP:

  * 新增对 IEEE 1588-2019 PTP 的支持。
  * 新增 SO_TIMESTAMPING socket 选项支持，以在 socket 辅助数据中获取时间戳信息。
  * 修复了时间戳回调上的竞态条件。
  * 修复了本地不是 GM 时钟时主时钟同步发送状态机（SM）的问题。

* HTTP:

  * 新增 HTTP/2 服务器库和示例应用，支持静态、动态和 Websocket 资源类型。
  * 新增 HTTP shell 组件。
  * 改进 HTTP 客户端错误报告。
  * 将 HTTP 客户端库移出实验性阶段。
  * 在 HTTP 客户端发送响应时新增 POLLOUT 监控。

* IPSP:

  * 移除了 IPSP 支持。``CONFIG_NET_L2_BT`` 已不复存在。

* IPv4:

  * 根据 RFC 5227 实现了 IPv4 地址冲突检测。
  * 新增 :c:func:`net_ipv4_is_private_addr` API 函数。
  * IPv4 网络掩码现在为每个地址单独设置，而不是为整个接口设置。
  * 其他小幅修复和改进。

* IPv6:

  * 根据 RFC 8981 实现了 IPv6 隐私扩展。
  * 新增 :c:func:`net_ipv6_is_private_addr` API 函数。
  * 为 IPv6 实现了可达性提示。上层可以使用 :c:func:`net_if_nbr_reachability_hint` 报告邻居可达性，避免不必要的邻居发现请求。
  * 新增 :kconfig:option:`CONFIG_NET_IPV6_MTU` ，允许设置自定义 IPv6 MTU。
  * 新增 :kconfig:option:`CONFIG_NET_MCAST_ROUTE_MAX_IFACES` ，允许为多播转发表项设置多个接口。
  * 新增 :kconfig:option:`CONFIG_NET_MCAST_ROUTE_MLD_REPORTS` ，允许在 MLDv2 报告中报告多播路由。
  * 修复了多播数据包的 IPv6 跳数限制处理。
  * 改进了 IPv6 邻居发现的测试覆盖率。
  * 修复了报告重复地址检测冲突的邻居通告数据包被丢弃的 bug。
  * 其他小幅修复和改进。

* LwM2M:

  * 新增 API 函数：

    * :c:func:`lwm2m_set_bulk`
    * :c:func:`lwm2m_rd_client_set_ctx`

  * 为 :c:type:`lwm2m_engine_set_data_cb_t` 回调类型新增 ``offset`` 参数。这会影响写入后回调和校验回调以及一些固件回调。
  * 修复了块传输中收到块号 0 时块上下文未重置的问题。
  * 修复了块传输中与服务器的块大小协商。
  * 新增 :kconfig:option:`CONFIG_LWM2M_ENGINE_ALWAYS_REPORT_OBJ_VERSION` ，允许强制客户端始终报告对象版本。
  * 现在即使资源未注册回调也可以进行块传输。
  * 修复了已注册回调发送的空 ACK 不会立即发出的 bug。
  * 移除了已弃用的 API 函数和定义。
  * 其他小幅修复和改进。

* 杂项：

  * 改进了整体网络 API 的 Doxygen 文档。
  * 将 TFTP 库改为使用 ``zsock_*`` API。
  * 新增 SNTP :c:func:`sntp_simple_addr` API 函数，用于在已知服务器 IP 地址时执行 SNTP 查询。
  * 新增 :kconfig:option:`CONFIG_NET_TC_THREAD_PRIO_CUSTOM` ，允许覆盖默认的流量类别（traffic class）线程优先级。
  * 修复了网络配置库中 IPv6 事件处理程序的初始化顺序。
  * 重构了 telnet shell 后端，使其使用 socket 和 socket 服务 API。
  * 修复了 IGMP 数据包的双重解引用问题。
  * 在各种测试和示例中将支持从 ``native_posix`` 迁移到 ``native_sim`` 。
  * 新增在网络缓冲区中复制用户数据的支持。
  * 修复了零大小网络缓冲区的克隆。
  * 新增处理 40 位数据格式的 net_buf API。
  * 为 dummy L2 新增接收回调，适用于某些用例（例如抓包）。
  * 实现了伪接口（pseudo interface），即抓包用例中的“any”接口。
  * 新增 cooked 模式抓包支持。这样可以捕获非基于 IP 的网络数据。
  * 在启动或停止抓包时生成网络事件。
  * 移除了过时且未使用的 ``tcp_first_msg`` :c:struct:`net_pkt` 标志。
  * 新增 :zephyr:code-sample:`secure-mqtt-sensor-actuator` 示例。
  * 新增对部分 L3 和 L4 校验和卸载的支持。
  * 使用新的 CA 证书更新了 :zephyr:code-sample:`mqtt-azure` ，当前证书即将过期。
  * 新增用于原生模拟器卸载（offloaded）socket 的驱动。
  * 重构 VLAN 支持以使用虚拟网络接口。
  * 新增虚拟网络接口的统计信息收集。
  * 修复了启用 :kconfig:option:`CONFIG_NET_MGMT_EVENT_SYSTEM_WORKQUEUE` 时 :c:func:`mgmt_event_work_handler` 中系统工作队列阻塞的问题。

* MQTT:

  * 为 MQTT TLS 后端新增 ALPN 支持。
  * 在 :c:struct:`mqtt_client` 上下文结构中新增用户数据字段。
  * 修复了 MQTT Websockets 传输中可能出现的 socket 泄漏。

* 网络接口：

  * 新增 API 函数：

    * :c:func:`net_if_ipv4_maddr_foreach`
    * :c:func:`net_if_ipv6_maddr_foreach`

  * 改进了网络接口代码中的调试日志。
  * 为 :c:struct:`net_if_addr` 结构新增引用计数器。
  * 修复了接口启用（up）时的 IPv6 DAD 和 MLDv2 操作。
  * 为 OpenThread 接口新增唯一的默认名称。
  * 其他小幅修复。

* OpenThread

  * 移除了已弃用的 ``openthread_set_state_changed_cb()`` 函数。
  * 新增 BLE TCAT 广播 API 的实现。

* PPP

  * 移除了已弃用的 ``gsm_modem`` 驱动和示例。
  * 优化了 PPP 驱动中的内存分配。
  * 对 :zephyr:code-sample:`cellular-modem` 示例进行了杂项改进
  * 新增 PPP 低层抓包支持。

* Shell：

  * 新增 ``net ipv4 gateway`` 命令，用于设置 IPv4 网关地址。
  * 在网络 shell 宏中新增参数校验。
  * 修复了 net_mgmt socket 信息打印。
  * 重构了 VLAN 信息打印。
  * 新增使用 ``net iface set_mac`` 命令设置随机 MAC 地址的选项。
  * 在打印多播地址信息时新增多播加入状态。

* Sockets：

  * 实现了新的网络 POSIX API：

    * :c:func:`if_nameindex`
    * :c:func:`inet_ntoa`
    * :c:func:`inet_addr`

  * 新增对 socket API 调用跟踪的支持。
  * TLS socket 不再是实验性 API。
  * 修复了 ``AF_PACKET`` 类型 socket 的协议字段字节序。
  * 修复了 TCP 的 :c:func:`getsockname` 。
  * 改进使用 DTLS socket 时的 :c:func:`sendmsg` 支持。
  * 修复了 socket 服务线程停止时 :c:func:`net_socket_service_register` 函数停滞的问题。
  * 修复了注销服务时可能导致 socket 服务线程停止的问题。
  * 移除了 socket 服务库中对异步超时的支持。
  * 修复了文件描述符不足时使用 :c:func:`zsock_accept` 可能出现的忙循环。

* Syslog：

  * 新增 API 函数：

    * :c:func:`log_backend_net_set_ip` ，用于直接使用 IP 地址初始化 syslog 网络后端。
    * :c:func:`log_backend_net_start` ，用于简化 syslog 网络后端的激活。

  * 为 syslog 网络后端新增结构化日志支持。
  * 为 syslog 网络后端新增 TCP 支持。

* TCP:

  * 修复了接受新 TCP 连接时可能出现的死锁。
  * 修复了连接拆除期间的 ACK 编号校验。
  * 修复了 FIN 包中包含的数据字节被忽略的 bug。
  * 修复了初始 SYN 包发送失败时可能出现的 TCP 上下文泄漏。
  * 弃用了 :kconfig:option:`CONFIG_NET_TCP_ACK_TIMEOUT` ，因为它与其他配置重复。
  * 改进调试日志，使其在高负载下更易于跟踪。
  * ISN 生成现在使用 SHA-256 而不是 MD5。此外，哈希计算现在依赖 PSA API，而不是旧版 Mbed TLS 函数。
  * 改进了不存在 PSH 标志时的 ACK 回复逻辑，以减少冗余 ACK。

* Websocket：

  * 新增 Websocket API：

    * :c:func:`websocket_register`
    * :c:func:`websocket_unregister`

  * 将 Websocket 库改为使用 ``zsock_*`` API。
  * 为 Websocket socket 新增 Object Core 支持。
  * 新增发送时的 POLLOUT 监控。

* Wi-Fi：

  * 减少 5 GHz 信道列表的内存占用。
  * 在 AP 模式中新增信道有效性检查。
  * 新增在连接调用中配置 BSSID 的支持。
  * 修复了 Wi-Fi shell 帮助文本，并修复了选项解析。
  * 支持 WPA 自动个人安全模式。
  * 收集单播接收和发送的网络数据包统计信息。
  * 新增 RTS 阈值配置支持。用户可以设置 RTS 阈值，也可以禁用 RTS 机制。
  * 新增 AP 参数配置支持。用户可以在构建时和运行时设置 AP 参数。
  * 新增配置 ``max_inactivity`` BSS 参数的支持。用户可以在构建时和运行时设置该时长，以控制 STA 不活动多久后 AP 可能会断开该 STA。
  * 新增配置 ``inactivity_poll`` BSS 参数的支持。用户可以设置仅构建时的 AP 参数，以控制 AP 在因 STA 不活动而丢弃 STA 之前是否可以先轮询 STA。
  * 新增配置 ``max_num_sta`` BSS 参数的支持。用户可以在构建时和运行时设置该参数，以控制 STA 表项的最大数量。

* zperf：

  * 修复了 zperf 中 ``IP_TOS`` 和 ``IPV6_TCLASS`` 选项的处理。
  * 修复了长时间 zperf 会话期间的吞吐量计算。
  * 修复了使用多播 IP 地址时 TCP 上传会话结束时的错误。
  * 修复了 IPv6 socket 绑定 IPv4 地址时报错的 bug。
  * 新增用于指定 zperf 会话期间使用哪个网络接口的选项。
  * 新增 ``ZPERF_SESSION_PERIODIC_RESULT`` 事件，用于 TCP 上传会话期间的周期性更新。
  * 修复了 zperf 会话出错时可能出现的 socket 泄漏。
  * 改进了 zperf 示例默认配置下的性能。

USB
***

* 新的 USB 设备栈：

  * 新增对 HID 设备的支持
  * 引入了针对速度的配置，并使高速支持符合 USB2.0 规范
  * 新增通知支持和初步的 BOS 支持

设备树
******

* 新增 :c:macro:`DT_INST_NODE_HAS_COMPAT` ，用于检查节点是否具有某个 compatible。这对具有多个 compatible 的节点很有用。
* 新增 :c:macro:`DT_CHILD_NUM` 及其变体，用于统计节点的子节点数量。
* 新增 :c:macro:`DT_FOREACH_NODELABEL` 及其变体，可用于遍历设备树节点的节点标签。
* 新增 :c:macro:`DT_NODELABEL_STRING_ARRAY` 和 :c:macro:`DT_NUM_NODELABELS` 及其变体。
* 新增 :c:macro:`DT_REG_HAS_NAME` 及其变体。
* 重构了 :c:macro:`DT_ANY_INST_HAS_PROP_STATUS_OKAY` ，使其结果可用于 :c:macro:`IS_ENABLED` 、IF_ENABLED 或 COND_CODE_x 等宏。
* 重构了 :c:macro:`DT_NODE_HAS_COMPAT_STATUS` ，使其可以在预处理阶段求值。
* 将 dts 脚本中使用的 PyYaml 版本更新到 6.0，以消除供应链漏洞。

Kconfig
*******

* 新增 ``substring`` Kconfig 预处理函数。
* 新增 ``dt_node_ph_prop_path`` Kconfig 预处理函数。
* 新增 ``dt_compat_any_has_prop`` Kconfig 预处理函数。

库 / 子系统
***********

* 调试

  * symtab

   * 启用 :kconfig:option:`CONFIG_SYMTAB` 后，在支持的架构上会随 Zephyr 链接阶段的可执行文件生成符号表。

* 按需分页

  * NRU（最近未使用）淘汰算法已更新其选择逻辑，以避免不断选中同一页进行淘汰。更新后的逻辑现在会从上次淘汰的页之后线性搜索新的候选页。

  * 新增 LRU（最近最少使用）淘汰算法。

* 格式化输出

  * 修复使用 ARCMWDT 编译 cbprintf 时的警告。

* 管理

  * hawkBit

    * hawkBit 子系统已重构为使用 settings 子系统来存储 hawkBit 配置。

    * 通过启用 :kconfig:option:`CONFIG_HAWKBIT_SET_SETTINGS_RUNTIME` ，可以在运行时配置 hawkBit 设置。使用 :c:func:`hawkbit_set_config` 函数设置 hawkBit 配置，也可以通过 hawkBit shell 使用 ``hawkbit set`` 命令设置。

    * 使用 hawkBit autohandler 且安装了更新时，设备现在会在安装完成后自动重启。

    * 通过启用 :kconfig:option:`CONFIG_HAWKBIT_CUSTOM_DEVICE_ID` ，可以注册回调函数来设置设备 ID。使用 :c:func:`hawkbit_set_device_identity_cb` 函数注册回调。

    * 通过启用 :kconfig:option:`CONFIG_HAWKBIT_CUSTOM_ATTRIBUTES` ，可以注册回调函数来设置发送给 hawkBit 服务器的设备属性。使用 :c:func:`hawkbit_set_custom_data_cb` 函数注册回调。

  * MCUmgr

    * 已移除已弃用的 mcumgr go 工具的说明，受支持的替代客户端列表可在 :ref:`mcumgr_tools_libraries` 找到。

    * 修复了 SMP 结构未打包的问题，这会在不支持非对齐内存访问的设备上导致故障。

    * 新增 :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_BT_DYNAMIC_SVC_REGISTRATION` ，允许用户选择 MCUmgr BT 服务是在编译时静态注册还是在运行时动态注册。

    * 在 FS 组中，SHA 计算已用 PSA 调用替换 TinyCrypt。

* 日志记录

  * 通过启用 :kconfig:option:`CONFIG_LOG_BACKEND_NET_USE_DHCPV4_OPTION` ，网络后端的 syslog 服务器 IP 地址由 DHCPv4 日志服务器选项（7）设置。

  * 在 POSIX 上使用实时时钟作为时间戳。

  * 新增 syslog（POSIX）支持。

  * 新增 :c:macro:`LOG_WRN_ONCE` ，用于记录仅在首次出现时输出的警告消息。

  * 新增 :c:func:`log_thread_trigger` ，用于触发日志消息的处理。

  * 修复了在禁用 :kconfig:option:`CONFIG_MULTITHREADING` 时延迟日志无法编译的情况。

  * 修复了基于字典的日志与非字典日志混用时，日志字符串可能从二进制中被剥离的情况。

  * 修复了某些情况下不生成字典数据库的问题。

  * 修复了字典日志解析器无法正确处理 long long 参数的问题。

  * 修复对 :kconfig:option:`CONFIG_LOG_MSG_APPEND_RO_STRING_LOC` 的支持。

* 调制解调器模块

  * 新增调制解调器管道链路（pipelink）模块，它全局共享调制解调器管道，允许设备驱动创建并设置管道供应用使用。

  * 简化了调制解调器管道模块的同步机制，现在只保护回调和用户数据。这与树内调制解调器管道的实际用法一致。

  * 新增 ``modem_stats`` 模块，用于跟踪整个调制解调器子系统中的缓冲区使用情况。

* 电源管理

  * 设备现在可以声明哪些系统电源状态会导致断电。当设备需要时，可以利用这些信息设置和释放电源状态约束。该特性通过 :kconfig:option:`CONFIG_PM_POLICY_DEVICE_CONSTRAINTS` 启用。使用函数 :c:func:`pm_policy_device_power_lock_get` 和 :c:func:`pm_policy_device_power_lock_put` 可以锁定和解锁设备中所有会导致断电的电源状态。

  * 新增设备电源管理的 shell 支持。

  * 设备电源管理已与系统电源管理解耦。新增的 :kconfig:option:`CONFIG_PM_DEVICE_SYSTEM_MANAGED` 选项用于控制系统休眠时是否必须挂起设备。

  * 现在可以使用 ``zephyr,pm-device-disabled`` 按电源状态单独禁用系统设备电源管理。这允许目标调整哪些状态应（以及哪些不应）触发设备电源管理。

* 加密

  * TinyCrypt 仍然可用，但现在正逐步弃用，转而使用 PSA Crypto 以获得更高的安全性和性能。
  * Mbed TLS 已更新到 3.6.0。版本说明见：https://github.com/Mbed-TLS/mbedtls/releases/tag/v3.6.0
  * 当系统中存在任何 PSA 加密提供程序（启用了 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_CLIENT`）时，现在必须通过 ``CONFIG_PSA_WANT_xxx`` 符号显式选择所需的 PSA 特性。
  * 新增选择符号 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_LEGACY_RNG` 和 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_EXTERNAL_RNG` ，以便用户指定 Mbed TLS PSA 加密核心应如何生成随机数。前者是默认选项，依赖旧版熵源和 CTR_DRBG/HMAC_DRBG 模块；后者依赖 CSPRNG 驱动。
  * :kconfig:option:`CONFIG_MBEDTLS_PSA_P256M_DRIVER_ENABLED` 启用对 Mbed TLS p256-m 驱动 PSA 加密库的支持。这是针对 Cortex-M 软件优化的 secp256r1 曲线实现。

* CMSIS-NN

  * CMSIS-NN 已从 v4.1.0 更新到 v6.0.0：https://arm-software.github.io/CMSIS-NN/latest/rev_hist.html

* FPGA

  * 改进了对缺少 ``reset`` 、``load`` 、``get_status`` 和 ``get_info`` 方法的驱动的处理。
  * 新增对 Agilex 和 Agilex 5 的支持。

* 随机数

  * 除了现有的 :c:func:`sys_rand32_get` 函数，现在还提供 :c:func:`sys_rand8_get` 、:c:func:`sys_rand16_get` 和 :c:func:`sys_rand64_get` 。这些函数都基于 :c:func:`sys_rand_get` 实现。

* SD

  * 重新设计了 SDMMC 和 SDIO 的频率与时序选择逻辑，以解决当所用 SDHC 设备未报告支持某时序模式下的最高频率时不会选择该时序模式的问题。现在，如果主机控制器和 card 都报告支持某个时序模式但不支持该模式支持的最高频率，则会选择该时序模式并以较低的频率进行配置（:github:`72705`）。

* 状态机框架

  * :c:macro:`SMF_CREATE_STATE` 宏现在始终接受 5 个参数。
  * 作为已运行状态父节点的转换源现在会选择正确的最低公共祖先（Least Common Ancestor）来执行退出和进入动作。
  * 现在不允许向 :c:func:`smf_set_state` 传递 ``NULL`` 。

* 存储

  * FAT FS：现在可以通过设置 :kconfig:option:`CONFIG_FS_FATFS_MKFS` Kconfig 选项，在不启用挂载失败时自动格式化的前提下，为 FAT 提供文件系统格式化功能。如果设置了 :kconfig:option:`CONFIG_FILE_SYSTEM_MKFS` ，该选项默认启用。

  * FS：现在可以在打开文件时通过 :c:func:`fs_open` 并传入 ``FS_O_TRUNC`` 标志来截断文件。

  * Flash Map：Flash Area 完整性检查中已用 PSA Crypto 替换 TinyCrypt。

  * Flash Map：新增 :c:func:`flash_area_flatten` ，用于擦除操作此前是用于移除或扰乱数据而不是为随机数据写入做准备的场景。

  * Flash Map：新增 :c:macro:`FIXED_PARTITION_NODE_OFFSET` 、:c:macro:`FIXED_PARTITION_NODE_SIZE` 和 :c:macro:`FIXED_PARTITION_NODE_DEVICE` ，允许从设备树节点而不是标签获取固定分区信息。

  * 新增 :kconfig:option:`CONFIG_NVS_DATA_CRC` ，为数据添加 CRC 保护。注意，启用该选项会使 NVS 与之前未对数据使用 CRC 的现有存储不兼容。

  * 修复了 NVS 中 :c:func:`nvs_calc_free_space` 返回的空间大于可用空间的问题，原因是未扣除保留 ATE 的空间。

  * 修复了 ext2 在尝试格式化分区时错误计算可用空间的问题。

  * 修复了 FAT 驱动在卸载后仍使磁盘保持已初始化状态的问题。

* 任务看门狗

  * 新增 shell（主要用于开发期间的测试）。

* POSIX API

  * 改进 Kconfig 选项，以反映标准的 POSIX 选项和选项组。

  * 新增对以下选项组的支持

    * :ref:`POSIX_MAPPED_FILES <posix_option_group_mapped_files>`
    * :ref:`POSIX_MEMORY_PROTECTION <posix_option_group_memory_protection>`
    * :ref:`POSIX_NETWORKING <posix_option_group_networking>`
    * :ref:`POSIX_SINGLE_PROCESS <posix_option_group_single_process>`
    * :ref:`POSIX_TIMERS <posix_option_group_timers>`
    * :ref:`XSI_SYSTEM_LOGGING <posix_option_group_xsi_system_logging>`

  * 新增对以下选项的支持

    * :ref:`_POSIX_ASYNCHRONOUS_IO <posix_option_asynchronous_io>`
    * :ref:`_POSIX_CPUTIME <posix_option_cputime>`
    * :ref:`_POSIX_FSYNC <posix_option_fsync>`
    * :ref:`_POSIX_MEMLOCK <posix_option_memlock>`
    * :ref:`_POSIX_MEMLOCK_RANGE <posix_option_memlock_range>`
    * :ref:`_POSIX_READER_WRITER_LOCKS <posix_option_reader_writer_locks>`
    * :ref:`_POSIX_SHARED_MEMORY_OBJECTS <posix_shared_memory_objects>`
    * :ref:`_POSIX_THREAD_CPUTIME <posix_option_thread_cputime>`
    * :ref:`_POSIX_THREAD_PRIO_PROTECT <posix_option_thread_prio_protect>`
    * :ref:`_POSIX_THREAD_PRIORITY_SCHEDULING <posix_option_thread_priority_scheduling>`
    * :ref:`_XOPEN_STREAMS <posix_option_xopen_streams>`

  * 修复了 eventfd 的 ``F_SETFL`` 处理，以避免覆盖内部标志。
  * 修复了调试消息中打印的线程栈地址。
  * 修复了信号代码中的宏参数使用。

* LoRa/LoRaWAN

  * 新增分片数据块传输（Fragmented Data Block Transport）服务，可通过 :kconfig:option:`CONFIG_LORAWAN_FRAG_TRANSPORT` 启用。除了 Semtech 的默认分片解码器实现，还提供了内存占用更小的树内实现。

  * 新增示例，用于演示 LoRaWAN 空中固件升级（FUOTA）。

* ZBus

  * 改进 VDED 过程，优化了消息订阅者投递通知期间为克隆体复制通道引用的操作。

  * 改进初始化阶段，静态初始化信号量和运行时观察者列表。这缩短了 zbus 初始化的时间。

  * 新增隔离通道消息订阅者池的方法。现在一些通道可以共享隔离池，以避免投递失败并缩短通信延迟。只需启用 :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_ISOLATION` 并使用函数 :c:func:`zbus_chan_set_msg_sub_pool` 更改通道使用的消息池即可。通道可以共享同一个消息池。

HAL
***

* Nordic

  * 将 nrfx 更新到 3.5.0 版本。
  * 新增 nRF Services（nrfs）库。

* STM32

  * 将 STM32F0 更新到 cube V1.11.5 版本。
  * 将 STM32F3 更新到 cube V1.11.5 版本。
  * 将 STM32F4 更新到 cube V1.28.0 版本。
  * 将 STM32F7 更新到 cube V1.17.2 版本。
  * 将 STM32G0 更新到 cube V1.6.2 版本。
  * 将 STM32G4 更新到 cube V1.5.2 版本。
  * 将 STM32H5 更新到 cube V1.2.0 版本。
  * 将 STM32H7 更新到 cube V1.11.2 版本。
  * 将 STM32L5 更新到 cube V1.5.1 版本。
  * 将 STM32U5 更新到 cube V1.5.0 版本。
  * 将 STM32WB 更新到 cube V1.19.1 版本。
  * 将 STM32WBA 更新到 cube V1.3.1 版本。
  * 新增 STM32H7R/S，cube 版本为 V1.0.0。

* ADI

  * 引入 ``hal_adi`` 模块，它是 Maxim 软件开发套件（MSDK）的子集，包含设备头文件和裸机外设驱动（:github:`72391`）。

* Espressif

  * 将 HAL 更新到 v5.1 版本，其中包含新的 SoC 底层文件。

MCUboot
*******

  * 修复了 bootutil HKDF 实现中的内存泄漏

  * 修复了强制 TLV 条目受保护的问题

  * 修复了禁用指令和数据缓存的问题

  * 修复了估计映像开销大小的计算

  * 修复了 swap-move 算法无法验证多映像的问题

  * 修复了 imgtool 中的对齐脚本错误

  * 修复了 imgtool 中 hex 文件格式的映像验证

  * 修复了读取 flash 映像复位向量的问题

  * 修复了 mbedtls 中过早包含 ``check_config.h`` 的问题

  * 重构映像依赖函数以减小代码体积

  * 新增 ``ESP32-C6`` 的 MCUboot 支持

  * 新增可选的 MCUboot 启动横幅

  * 新增受保护区域的 TLV 查询

  * 新增在 bootutil 中使用内置密钥进行验证

  * 为 PSA Crypto 后端新增内置 ECDSA 密钥支持

  * 为次级映像新增 ``OVERWRITE_ONLY_KEEP_BACKUP`` 选项

  * 新增 ``SOC_FLASH_0_ID`` 和 ``SPI_FLASH_0_ID`` 的定义

  * 修复了对 mbedtls 3.1 及以上版本的 ASN.1 支持

  * 修复了 ``boot_read_enc_key`` 中 bootutil 有符号与无符号比较的问题

  * 更新 imgtool 的 version.py 以接受命令行参数

  * 新增 imgtool dumpinfo 的改进

  * 修复了 imgtool dumpinfo 的多个问题

  * 修复了 edcsa-p384 签名映像的 imgtool verify 命令

  * 新增对 NXP MCXN947 的支持

  * 本版本中的 MCUboot 版本为 ``2.1.0+0-dev`` 。

OSDP
****

* 修复了 CP 安全通道握手中的一个问题：恶意 PD 可以通过发送乱序的安全通道响应，使 R-MAC 回退到旧值，从而导致重放攻击。

Trusted Firmware-M
******************

* TF-M 已更新到 2.1.0。版本说明见：https://tf-m-user-guide.trustedfirmware.org/releases/2.1.0.html

* 新增对 RSA-3072 之外的 MCUboot 签名类型的支持。可以通过 :kconfig:option:`CONFIG_TFM_MCUBOOT_SIGNATURE_TYPE` Kconfig 选项选择类型。使用新的默认值 EC-P256 相比 RSA 可减少数 KB 的 flash 占用。

LVGL
****

LVGL 已更新到 8.4.0。版本说明见：https://docs.lvgl.io/8.4/CHANGELOG.html#v8-4-0-19-march-2024

此外，Zephyr 中还做了以下更改：

  * 新增通过启用 :kconfig:option:`CONFIG_LV_Z_MEMORY_POOL_CUSTOM_SECTION` 将内存池缓冲区放到 ``.lvgl_heap`` 段的支持

  * 移除了基于 kscan 的指针输入包装代码。

  * 修正了编码器按钮行为，使其正确发出 ``LV_KEY_ENTER`` 事件。

  * 改进对 :samp:`invert-{x,y}` 和 ``swap-xy`` 配置的处理。

  * 在文件关闭时新增 ``LV_MEM_CUSTOM_FREE`` 调用。

  * 为 DMA2D 符号新增缺失的 Kconfig 桩。

  * 集成对 LVGL rounder 回调函数的支持。

测试与示例
**********

  * 新增 snippet，可在 ``west build`` 时传入 ``-S nus-console`` 轻松启用基于蓝牙 LE 的 UART。该 snippet 会设置 :kconfig:option:`CONFIG_BT_ZEPHYR_NUS_AUTO_START_BLUETOOTH` ，使使用 UART API 的非蓝牙示例（例如 Console 和 Logging 示例）无需修改即可运行。

  * 从示例 ``net/cloud/tagoio`` 和 ``net/mgmt/updatehub`` 中移除了 ``GSM_PPP`` 专用配置 overlay。``GSM_PPP`` 设备驱动已被弃用并移除。替换它的新 ``MODEM_CELLULAR`` 设备驱动使用原生网络协议栈和 ``PM`` 子系统，与以太网类似，无需应用执行特定操作来设置网络。

  * 移除了 ``net/gsm_modem`` 示例，因为它所依赖的 ``GSM_PPP`` 设备驱动已被弃用并移除。该示例已替换为基于 ``MODEM_CELLULAR`` 设备驱动的 ``net/cellular_modem`` 示例。

  * BT LE Coded PHY 现在在 CI 中使用 nrf5x bsim 目标进行运行时测试。

  * ``tests/net`` 测试中的外部以太网网络接口已被禁用，因为这些测试旨在使用仿真网络接口。

问题相关事项
************

已知问题
========

- :github:`74345` - 蓝牙：nRF51 上出现故障时无法正常工作
