.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth-ctlr-arch:

LE 控制器
#########

概述
****

.. image:: img/ctlr_overview.png

#. HCI

   * 主机控制器接口，蓝牙标准
   * 提供 Zephyr 蓝牙 HCI 驱动

#. HAL

   * 硬件抽象层
   * 厂商特定实现和 Zephyr 驱动用法

#. Ticker

   * 软实时射频/资源调度

#. LL_SW

   * 基于软件的链路层实现
   * 状态与角色、控制过程、数据包控制器

#. Util

   * 裸机内存池管理
   * 数量可变的队列，无锁使用
   * 固定数量的 FIFO，无锁使用
   * 基于 Mayfly 概念的延迟 ISR 执行


架构
****

执行概览
========

.. image:: img/ctlr_exec_overview.png


架构概览
========

.. image:: img/ctlr_arch_overview.png


调度
****

.. image:: img/ctlr_sched.png


Ticker
======

.. image:: img/ctlr_sched_ticker.png


上层链路层与下层链路层
======================

.. image:: img/ctlr_sched_ull_lll.png


调度变体
========

.. image:: img/ctlr_sched_variant.png


ULL 与 LLL 时序
===============

.. image:: img/ctlr_sched_ull_lll_timing.png


事件处理
********

.. image:: img/ctlr_sched_event_handling.png


调度间隔很近的事件
==================

.. image:: img/ctlr_sched_msc_close_events.png


中止活动事件
============

.. image:: img/ctlr_sched_msc_event_abort.png


取消待处理事件
==============

.. image:: img/ctlr_sched_msc_event_cancel.png


抢占活动事件
============

.. image:: img/ctlr_sched_msc_event_preempt.png


数据流
******

发送数据流
==========

.. image:: img/ctlr_dataflow_tx.png


接收数据流
==========

.. image:: img/ctlr_dataflow_rx.png


执行优先级
**********

.. image:: img/ctlr_exec_prio.png

- 事件处理 (0, 1) < 事件准备 (2, 3) < 事件/接收完成 (4) < 发送请求 (5) < 角色管理 (6) < 主机 (7)。

- LLL 是厂商 ISR，ULL 是 Mayfly ISR 概念，主机是内核线程。

链路层控制过程
**************

以下是 ULL 中控制过程处理实现主要概念的简要介绍。

三种主要执行上下文
==================

- HCI/LLCP API
   * 其他过程发起 API
   * 通过 ull_llcp.c::ull_cp_<proc>() 发起本地过程
   * 与正在运行的过程（本地和远程）交互

- 由 lll_prepare 上下文驱动 ull_cp_run()
   * LLCP 主状态机入口/时钟节拍
   * 通过 ull_conn_llcp() 从 ull_peripheral.c/ull_central.c::ticker_cb 进入

- rx_demux 上下文驱动 ull_cp_tx_ack() 和 ull_cp_rx()
   * LLCP Tx ACK 处理与 PDU 接收
   * 从 ull_conn.c::ull_conn_rx()
   * 负责将 PDU 传入正在运行的过程，也可能发起远程过程

数据结构和 PDU 辅助函数
=======================

- struct llcp_struct
   * LLCP 主数据存储
   * 定义于 ull_conn_types.h，并声明为 struct ll_conn 的一部分
   * 保存本地和远程过程请求队列以及连接特定的 LLCP 数据
   * 基本的连接级抽象

- struct proc_ctx
   * 通用过程上下文数据，包含各种过程数据和状态，以及用于入队的 sys_snode_t
   * 定义于 ull_llcp_internal.h，通过 ull_llcp.c::create_procedure() 声明/实例化
   * 还保存 tx_ack 中使用的节点引用以及 rx_node 保留机制

- struct llcp_mem_pool
   * 用于实现过程上下文资源的内存池，分别实例化本地版本和远程版本
   * 通过 ull_llcp.c::create_procedure() 使用

- 其他 PDU 处理技巧
   * 控制 PDU 的编码和解码由 ull_llcp_pdu.c::llcp_pdu_encode/decode_<PDU>() 完成
   * 其他 PDU 校验通过 ull_llcp.c::pdu_is_valid() 由 ull_llcp.c::pdu_validate_<PDU>() 处理

LLCP 本地和远程请求/过程状态机
==============================

- ull_llcp_local.c
   * 处理本地发起过程的状态机
   * 命名约定：lr _<...> => 本地请求状态机
   * 本地过程队列处理
   * 本地 run/rx/tx_ack 切换

- ull_llcp_remote.c
   * 上述内容的远程版本
   * 命名约定：rr_<...> => 远程请求状态机
   * 还处理由 llcp_rx_new() 发起的远程过程
   * 其他过程冲突处理（在 rr_st_idle() 中）

- ull_llcp_common/conn_upd/phy/enc/cc/chmu.c
   * 各个过程的实现（ull_llcp_common.c 汇集了较简单的过程）
   * 命名约定：lp_<...> => 本地发起的过程，rp_<...> => 远程发起的过程
   * 处理从初始化（可能经过 instant）到完成的过程流程，以及适用时的主机通知

其他概念
========

- 过程冲突处理
   * 有关说明，请参见蓝牙规范
   * 基本上，有些过程可以并行存在，有些则不能——例如同一时间只能有一个基于 instant 的过程
   * 规范规定了发生冲突时如何处理/解决冲突的规则

- 终止处理
   * 关于如何处理终止，适用特定规则。
   * 由于过程上下文涉及资源处理，而终止必须始终可用，因此将其作为特殊情况处理。
   * 另请注意：在多种情况下，对端行为无效会触发连接终止。

- 新远程过程处理
   * 表 new_proc_lut[] 将 LLCP PDU 映射到 llcp_rr_new() 中使用的过程/角色
   * 注意：对于任意给定连接，远程过程队列中始终只能有一个远程过程。

- 其他细节
   * 暂停/恢复概念——共有两种（详情参见规范）
   * 过程执行可被加密过程暂停
   * 数据发送可被 PHY、DLE 和 ENC 过程暂停
   * RX 节点保留——确保通知需要 RX 节点时无需等待分配


其他单元测试概念
================

- 为每个过程单独设置 ZTEST 单元测试
   * zephyr/tests/bluetooth/controller/ctrl_<proc>

- Rx 节点处理采用模拟实现
   * 不同配置由独立的 conf 文件处理（例如参见 ctrl_conn_update）
   * ZTEST(periph_rem_no_param_req, test_conn_update_periph_rem_accept_no_param_req)

- 单元测试中使用 rx_demux/prepare 上下文的模拟版本——仅测试过程 PDU 流程
   * 模拟 LLL 准备/完成流程的 event_prepare()/event_done() 辅助函数
   * lt_rx()/lt_tx() 模拟“下层测试器”的 rx/tx
   * ut_rx_node() 模拟“上层测试器”的通知流程处理
   * 用于生成和解析 PDU 的一组辅助函数，以及各种模拟的 ull_stuff()




下层链路层
**********

LLL 执行
========

.. image:: img/ctlr_exec_lll.png


LLL 恢复
--------

.. image:: img/ctlr_exec_lll_resume_top.png

.. image:: img/ctlr_exec_lll_resume_bottom.png


裸机工具
********

内存 FIFO 和内存队列
====================

.. image:: img/ctlr_mfifo_memq.png

Mayfly
======

.. image:: img/ctlr_mayfly.png


* Mayfly 是多实例、可扩展的 ISR 执行上下文
* Work 之于线程，犹如 Mayfly 之于 ISR
* 在 ISR 中执行的函数列表
* 执行优先级映射到 IRQ 优先级
* 便于跨执行上下文调度
* 尽快进入空闲（race-to-idle）执行
* 无锁、裸机

旧版控制器
**********

.. image:: img/ctlr_legacy.png

低功耗蓝牙控制器——厂商特定细节
******************************

硬件要求
========

Nordic Semiconductor
--------------------

Nordic Semiconductor 低功耗蓝牙控制器实现需要以下硬件外设。

.. list-table:: SoC 外设使用
   :header-rows: 1
   :widths: 15 15 15 10 50

   * - 资源
     - nRF 外设
     - 实例数
     - Zephyr 驱动可访问
     - 描述
   * - 时钟
     - NRF_CLOCK
     - 1
     - 是
     - * 低频时钟（LFCLOCK）或睡眠时钟，用于在蓝牙射频事件之间实现低功耗
       * 高频时钟（HFCLOCK）或有源时钟，用于高精度数据包定时，以及在蓝牙射频事件内借助帧间间隔（tIFS）时序完成基于软件的收发器状态切换。
   * - RTC [a]_
     - NRF_RTC0
     - 1
     - **否**
     - * 使用 2 个捕获/比较寄存器
   * - 定时器
     - NRF_TIMER0 或 NRF_TIMER4 [1]_，以及 NRF_TIMER1 [0]_
     - 2 或 1 [1]_
     - **否**
     - * 2 个实例，分别用于数据包定时和 tIFS 软件切换
       * 第一个实例有 7 个捕获/比较寄存器（3 个必需，1 个可选用于 ISR 性能分析，4 个用于单定时器 tIFS 切换）
       * 如果未使用单 tIFS 定时器，则第二个实例使用 4 个捕获/比较寄存器。
   * - PPI [b]_
     - NRF_PPI
     - 21 个通道（20 [2]_），以及 2 个通道组 [3]_
     - 是 [4]_
     - * 用于射频模式切换以实现 tIFS 时序，以及 PA/LNA 控制
   * - DPPI [c]_
     - NRF_DPPI
     -  20 个通道，以及 2 个通道组 [3]_
     - 是 [4]_
     - * 用于射频模式切换以实现 tIFS 时序，以及 PA/LNA 控制
   * - SWI [d]_
     - NRF_SWI4 和 NRF_SWI5，或 NRF_SWI2 和 NRF_SWI3 [5]_
     - 2
     - **否**
     - * 2 个实例，用于下层链路层和上层链路层的低优先级执行上下文
   * - 射频
     - NRF_RADIO
     - 1
     - **否**
     - * 2.4 GHz 射频收发器，支持多种射频标准，例如 1 Mbps、2 Mbps 和 Coded PHY S2/S8 远距离低功耗蓝牙技术
   * - RNG [e]_
     - NRF_RNG
     - 1
     - 是
     -
   * - ECB [f]_
     - NRF_ECB
     - 1
     - **否**
     -
   * - CBC-CCM [g]_
     - NRF_CCM
     - 1
     - **否**
     -
   * - AAR [h]_
     - NRF_AAR
     - 1
     - **否**
     -
   * - GPIO [i]_
     - NRF_GPIO
     - 2 个 GPIO 引脚，分别用于 PA 和 LNA，各 1 个
     - 是
     - * 此外还有 10 个调试 GPIO 引脚（可选）
   * - GPIOTE [j]_
     - NRF_GPIOTE
     - 1
     - 是
     - * 用于 PA/LNA
   * - TEMP [k]_
     - NRF_TEMP
     - 1
     - 是
     - * 用于 RC 源 LFCLOCK 校准
   * - UART [l]_
     - NRF_UART0
     - 1
     - 是
     - * 用于仅控制器构建中的 HCI 接口
   * - IPC [m]_
     - NRF_IPC [5]_
     - 1
     - 是
     - * 用于仅控制器构建中的 HCI 接口


.. [a] 实时计数器（RTC）
.. [b] 可编程外设互连（PPI）
.. [c] 分布式可编程外设互连（DPPI）
.. [d] 软件中断（SWI）
.. [e] 随机数生成器（RNG）
.. [f] AES 电子密码本模式加密（ECB）
.. [g] 密码块链接（CBC）——使用计数器模式加密的消息认证码（CCM）
.. [h] 加速地址解析器（AAR）
.. [i] 通用输入输出（GPIO）
.. [j] GPIO 任务和事件（GPIOTE）
.. [k] 温度传感器（TEMP）
.. [l] 通用异步收发器（UART）
.. [m] 进程间通信外设（IPC）


.. [0] :kconfig:option:`CONFIG_BT_CTLR_TIFS_HW` ``=n``
.. [1] :kconfig:option:`CONFIG_BT_CTLR_SW_SWITCH_SINGLE_TIMER` ``=y``
.. [2] 未使用预定义 PPI 通道时
.. [3] 用于基于软件的 tIFS 切换
.. [4] 使用 nRFx 接口的驱动
.. [5] 适用于 nRF53x 系列
