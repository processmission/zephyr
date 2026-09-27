.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _instrumentation:

插桩
####

概述
****

插桩子系统为 Zephyr 应用提供由编译器管理的运行时系统插桩能力。它使开发者能够跟踪函数调用、观察上下文切换，并只需极少的手工插桩即可分析应用性能。

与提供 RTOS 感知跟踪和结构化事件 API 的 :ref:`跟踪 <tracing>` 子系统不同，插桩子系统工作在更底层，利用编译器插桩钩子。这种方式使得几乎可以捕获任意函数的进入和退出事件，而无需在代码中手工插入跟踪调用。

.. admonition:: 跟踪与插桩的对比
   :class: hint

   **何时使用跟踪**：当需要 RTOS 感知的事件跟踪（例如线程切换、信号量操作等）并希望把开销降到最低时，请选择跟踪子系统。

   **何时使用插桩**：当需要详细了解函数级执行情况以更好地理解代码流程，或者在不添加手工跟踪点的情况下定位性能瓶颈时，请选择插桩。

插桩子系统依赖编译器对自动函数插桩的支持。启用后，编译器会在应用中每个函数的入口和出口自动插入对特殊插桩处理函数的调用（显式标记为 ``__no_instrumentation__`` 的函数除外）。目前只支持使用 ``-finstrument-functions`` 编译选项的 GCC。

该子系统在 RAM 初始化后自动初始化，并使用 trigger/stopper 函数来控制何时开始记录。默认的 trigger 和 stopper 函数都设为 ``main()`` （可通过 Kconfig 配置），这意味着插桩会捕获从 ``main()`` 开始到其返回的整个执行过程。

记录的数据存放在 RAM 中，并可通过一个 UART 后端从主机访问，该后端提供了一组简单的命令。:zephyr_file:`scripts/instrumentation/zaru.py` 脚本允许通过高层命令行接口执行这些命令，便于以适合进一步分析的格式获取数据（例如 `Perfetto`_）。

运行模式
********

插桩子系统支持两种模式，它们可以单独启用，也可以同时启用：

调用图模式（跟踪）
==================

在调用图模式下（通过 :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_CALLGRAPH` 启用），该子系统把函数进入和退出事件连同时间戳和上下文信息记录到内存缓冲区中。这样可以：

- 重建完整的函数调用图
- 观察线程上下文切换
- 分析执行流程和时序关系

跟踪缓冲区可以工作在环形缓冲区模式（默认，会覆盖旧条目）或固定缓冲区模式（写满即停止）。缓冲区大小可通过 :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_CALLGRAPH_TRACE_BUFFER_SIZE` 配置。

.. code-block:: console
   :caption: 调用图模式输出示例。更多细节请参见 :ref:`zaru_usage`。

   $ ./scripts/instrumentation/zaru.py trace

      Thread Name      Thread ID  CPU  Mode     Timestamp          Function(s)
   ------------------------------------------------------------------------------------------------
               ... (truncated) ...

               main    0x20001a38   0)    0 |    187837720 ns |               sys_dlist_append();
               main    0x20001a38   0)    0 |    188802680 ns |             };   /* z_priq_simple_add */
               main    0x20001a38   0)    0 |    189282840 ns |           };   /* add_to_waitq_locked */
               main    0x20001a38   0)    0 |    189770000 ns |           add_thread_timeout();
               main    0x20001a38   0)    0 |    190732920 ns |         };   /* pend_locked */
               main    0x20001a38   0)    0 |    191198480 ns |         k_spin_release();
               main    0x20001a38   0)    0 |    192125560 ns |         z_swap() {
               main    0x20001a38   0)    0 |    192590080 ns |           k_spin_release();
               main    0x20001a38   0)    0 |    193520000 ns |           z_swap_irqlock() {
               main    0x20001a38   0)    0 |    193987840 ns |             __set_BASEPRI() {
               main    0x20001a38   0)    0 |    194474640 ns | /* --> Scheduler switched OUT from thread 'main' */
        thread-none   none-thread   0)    0 |    195178000 ns | /* <-- Scheduler switched IN thread 'thread-none' */
        thread-none   none-thread   0)    0 |    195851520 ns | z_thread_entry() {
        thread-none   none-thread   0)    0 |    196312600 ns |   k_sched_current_thread_query() {
        thread-none   none-thread   0)    0 |    196774680 ns |     z_impl_k_sched_current_thread_query();
        thread-none   none-thread   0)    0 |    197694480 ns |   };   /* k_sched_current_thread_query */
           thread_A    0x200000d8   0)    7 |    198160000 ns | thread_A() {
           thread_A    0x200000d8   0)    7 |    198443400 ns |   get_sem_and_exec_function() {
           thread_A    0x200000d8   0)    7 |    198727440 ns |     k_sem_take() {
           thread_A    0x200000d8   0)    7 |    199011840 ns |       z_impl_k_sem_take() {
           thread_A    0x200000d8   0)    7 |    199397520 ns |         k_spin_lock() {
           thread_A    0x200000d8   0)    7 |    199784200 ns |           __get_BASEPRI();
           thread_A    0x200000d8   0)    7 |    200557840 ns |           __set_BASEPRI_MAX();
           thread_A    0x200000d8   0)    7 |    201333640 ns |           __ISB();
           thread_A    0x200000d8   0)    7 |    202111360 ns |           z_spinlock_validate_pre();
           thread_A    0x200000d8   0)    7 |    202891000 ns |           z_spinlock_validate_post();
           thread_A    0x200000d8   0)    7 |    203664760 ns |         };   /* k_spin_lock */
           thread_A    0x200000d8   0)    7 |    204058000 ns |         k_spin_unlock() {
           thread_A    0x200000d8   0)    7 |    204450840 ns |           __set_BASEPRI();
           thread_A    0x200000d8   0)    7 |    205231640 ns |           __ISB();
           thread_A    0x200000d8   0)    7 |    206009600 ns |         };   /* k_spin_unlock */
           thread_A    0x200000d8   0)    7 |    206291600 ns |       };   /* z_impl_k_sem_take */
           thread_A    0x200000d8   0)    7 |    206572920 ns |     };   /* k_sem_take */

           ... (truncated) ...

统计模式（性能分析）
====================

在统计模式下（通过 :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_STATISTICAL` 启用），该子系统会累计 trigger 与 stopper 之间执行的每个函数的计时统计。这样可以得到每个函数的总执行时间，有助于定位性能瓶颈。该子系统最多跟踪 :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_STATISTICAL_MAX_NUM_FUNC` 个不同的函数。

.. code-block:: console
   :caption: 统计模式输出示例（开销最大的前 10 个函数）。更多细节请参见 :ref:`zaru_usage`。

   $ ./scripts/instrumentation/zaru.py profile -n 10

   9.45% 0000061d main
   6.00% 0000049d k_msleep
   5.98% 00000469 k_sleep
   5.95% 0000aea1 k_sleep_ticks
   5.93% 0000ad6d z_impl_k_sleep_ticks
   5.66% 00000431 k_sem_take
   5.65% 00007e65 z_impl_k_sem_take
   5.51% 0000ac29 z_pend_curr
   2.83% 000063ed sys_clock_isr
   2.67% 0000d361 sys_clock_announce

配置
****

使用以下方式启用插桩：

.. code-block:: cfg

   CONFIG_INSTRUMENTATION=y
   CONFIG_INSTRUMENTATION_MODE_CALLGRAPH=y    # For tracing
   CONFIG_INSTRUMENTATION_MODE_STATISTICAL=y  # For profiling

插桩子系统通过 UART 控制台与目标设备通信。请确保 ``zephyr_console`` chosen 节点指向所需的 UART 控制器。

:ref:`保留内存 <retention_api>` 可以让 trigger/stopper 函数的地址在重启后继续保留。此功能是可选的，通过 :kconfig:option:`CONFIG_INSTRUMENTATION_DYNAMIC_TRIGGER` Kconfig 选项启用。启用后，devicetree 必须指定一个保留内存区域：

.. code-block:: devicetree

   / {
       sram@2003FC00 {
           compatible = "zephyr,memory-region", "mmio-sram";
           reg = <0x2003FC00 DT_SIZE_K(1)>;
           zephyr,memory-region = "RetainedMem";

           retainedmem {
               compatible = "zephyr,retained-ram";
               status = "okay";

               instrumentation_triggers: retention@0 {
                   compatible = "zephyr,retention";
                   status = "okay";
                   reg = <0x0 0x10>;
               };
           };
       };
   };

   /* Adjust main SRAM to exclude retained region */
   &sram0 {
       reg = <0x20000000 DT_SIZE_K(255)>;
   };

完整的配置示例请参见 :zephyr:code-sample:`instrumentation` 示例。其他选项包括缓冲区大小、trigger 函数以及函数或文件排除列表（参见以 :kconfig:option-regex:`CONFIG_INSTRUMENTATION_*` 开头的 Kconfig 选项）。

.. _zaru_usage:

``zaru.py`` 用法
****************

``zaru.py`` 命令行工具（位于 :zephyr_file:`scripts/instrumentation/zaru.py`）提供了通过 UART 控制插桩并从目标提取数据的接口。

该工具提供以下命令：

- ``status``：检查目标设备是否支持

  - 调用图（跟踪）模式
  - 统计（性能分析）模式
  - 动态 trigger/stopper 函数配置

- ``trace``：捕获并显示函数调用跟踪数据。
- ``profile``：捕获并显示函数性能分析数据。
- ``reboot``：重启目标设备。

可以通过运行 ``zaru.py <command> --help`` 获取每个命令的帮助。

默认情况下，``zaru.py`` 尝试使用 ``/dev/ttyACM0`` 连接目标设备。可以使用 ``--serial`` 选项指定其他串口：

.. code-block:: console

   $ ./scripts/instrumentation/zaru.py --serial /dev/ttyACM1 status

``--build-dir`` 选项可用于指定 Zephyr 构建目录，定位 ELF 文件以进行符号解析时需要该目录。如果未提供，``zaru.py`` 会尝试自动查找。

详细用法说明请参见 :zephyr:code-sample:`instrumentation` 示例文档。

限制与注意事项
**************

编译器支持
  插桩子系统要求 GCC 支持 ``-finstrument-functions``。不支持其他编译器。

栈大小要求
  插桩会为每次函数调用增加开销，从而增加栈使用量。你可能需要增大线程栈大小，以容纳插桩处理函数和嵌套函数调用所需的额外空间。

执行开销
  所有函数调用都会产生插桩开销。代码体积会因新增插桩调用而增大，性能也会受到影响。

初始化约束
  在 RAM 初始化之前运行的代码（例如早期启动函数）不会被捕获，因为它们运行在插桩子系统初始化之前。

为减少开销，请使用 trigger/stopper 函数只对关注的代码区域进行插桩，并通过 :kconfig:option:`CONFIG_INSTRUMENTATION_EXCLUDE_FUNCTION_LIST` 和 :kconfig:option:`CONFIG_INSTRUMENTATION_EXCLUDE_FILE_LIST` 排除性能关键的函数。

API 参考
********

.. doxygengroup:: instrumentation_api

.. _Perfetto: https://perfetto.dev/
