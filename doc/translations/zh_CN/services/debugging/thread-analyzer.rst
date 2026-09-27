.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _thread_analyzer:

线程分析器
##########

线程分析器模块会启用跟踪线程信息（例如线程栈使用量和其他运行时线程统计数据）所需的所有 Zephyr 选项。

当应用程序调用 :c:func:`thread_analyzer_run` 或 :c:func:`thread_analyzer_print` 时，将按需执行分析。

例如，要在启用线程分析器的情况下构建 synchronization 示例，请执行以下操作：

   .. zephyr-app-commands::
      :zephyr-app: samples/synchronization/
      :board: qemu_x86
      :goals: build
      :gen-args: -DCONFIG_QEMU_ICOUNT=n -DCONFIG_THREAD_ANALYZER=y \
                   -DCONFIG_THREAD_ANALYZER_USE_PRINTK=y -DCONFIG_THREAD_ANALYZER_AUTO=y \
                   -DCONFIG_THREAD_ANALYZER_AUTO_INTERVAL=5


在 Qemu 中运行生成的应用时，你将获得来自线程分析器的附加信息::


        thread_a: Hello World from cpu 0 on qemu_x86!
        Thread analyze:
         thread_b            : STACK: unused 740 usage 284 / 1024 (27 %); CPU: 0 %
         thread_analyzer     : STACK: unused 8 usage 504 / 512 (98 %); CPU: 0 %
         thread_a            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 98 %
         idle                : STACK: unused 204 usage 116 / 320 (36 %); CPU: 0 %
        thread_b: Hello World from cpu 0 on qemu_x86!
        thread_a: Hello World from cpu 0 on qemu_x86!
        thread_b: Hello World from cpu 0 on qemu_x86!
        thread_a: Hello World from cpu 0 on qemu_x86!
        thread_b: Hello World from cpu 0 on qemu_x86!
        thread_a: Hello World from cpu 0 on qemu_x86!
        thread_b: Hello World from cpu 0 on qemu_x86!
        thread_a: Hello World from cpu 0 on qemu_x86!
        Thread analyze:
         thread_b            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 7 %
         thread_analyzer     : STACK: unused 8 usage 504 / 512 (98 %); CPU: 0 %
         thread_a            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 9 %
         idle                : STACK: unused 204 usage 116 / 320 (36 %); CPU: 82 %
        thread_b: Hello World from cpu 0 on qemu_x86!
        thread_a: Hello World from cpu 0 on qemu_x86!
        thread_b: Hello World from cpu 0 on qemu_x86!
        thread_a: Hello World from cpu 0 on qemu_x86!
        thread_b: Hello World from cpu 0 on qemu_x86!
        thread_a: Hello World from cpu 0 on qemu_x86!
        thread_b: Hello World from cpu 0 on qemu_x86!
        thread_a: Hello World from cpu 0 on qemu_x86!
        Thread analyze:
         thread_b            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 7 %
         thread_analyzer     : STACK: unused 8 usage 504 / 512 (98 %); CPU: 0 %
         thread_a            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 8 %
         idle                : STACK: unused 204 usage 116 / 320 (36 %); CPU: 83 %
        thread_b: Hello World from cpu 0 on qemu_x86!
        thread_a: Hello World from cpu 0 on qemu_x86!
        thread_b: Hello World from cpu 0 on qemu_x86!


配置
****
使用以下选项配置此模块。

:kconfig:option:`CONFIG_THREAD_ANALYZER`
   启用该模块。
:kconfig:option:`CONFIG_THREAD_ANALYZER_USE_PRINTK`
   使用 printk 输出线程统计信息。
:kconfig:option:`CONFIG_THREAD_ANALYZER_USE_LOG`
   使用日志记录器输出线程统计信息。
:kconfig:option:`CONFIG_THREAD_ANALYZER_AUTO`
   自动运行线程分析器。使用该选项时，无需向应用程序添加任何代码。
:kconfig:option:`CONFIG_THREAD_ANALYZER_AUTO_INTERVAL`
   在自动模式下，模块在连续两次打印线程分析结果之间的休眠时间。
:kconfig:option:`CONFIG_THREAD_ANALYZER_AUTO_STACK_SIZE`
  线程分析器自动线程使用的栈。
:kconfig:option:`CONFIG_THREAD_NAME`
  打印线程的名称而不是其 ID。
:kconfig:option:`CONFIG_THREAD_RUNTIME_STATS`
  打印线程运行时数据，例如利用率。该选项由 :kconfig:option:`CONFIG_THREAD_ANALYZER` 自动选择。
:kconfig:option:`CONFIG_THREAD_ANALYZER_LONG_FRAME_PER_INTERVAL`
  打印后重置 Longest Frame 值统计信息。当使用 :kconfig:option:`SCHED_THREAD_USAGE_ANALYSIS` 获取平均和最长的帧线程统计信息时，请在每次打印线程统计信息后将 Longest Frame 值重置为零。这样可以观察最近一个间隔内的最长帧，而不是自启动以来的最长帧。
:kconfig:option:`CONFIG_THREAD_ANALYZER_PRINT_THREAD_PRIORITY`
  打印每个线程的优先级。

API 文档
********

.. doxygengroup:: thread_analyzer
