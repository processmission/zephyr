.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _profiling-perf:

Perf
####

Perf 是一款基于栈跟踪的性能分析工具。它以极小的代码开销实现轻量级性能分析。

工作原理
********

``perf record`` shell 命令会使用 perf 跟踪函数启动一个定时器。定时器由中断驱动，因此 perf 跟踪函数会在中断期间被调用。Zephyr 内核在调用中断处理程序之前，会将返回地址和帧指针保存在中断栈、``callee_saved`` 结构或架构特定的异常帧中。因此，perf 跟踪函数利用返回地址和帧指针来生成栈回溯。

在 Cortex-M 上，perf 会包装 SysTick 处理程序，从而能够在普通定时器 ISR 使用处理程序栈之前，采样被中断的线程模式进程栈指针（PSP）帧。后端会在将该帧传递给 Arm 栈遍历器之前对其进行校验。

对于非安全 Trusted Execution 镜像，Cortex-M 后端不可用，因为非安全固件无法访问安全异常帧。

可以使用 :zephyr_file:`scripts/profiling/stackcollapse.py` 脚本，借助 ELF 文件中的符号将栈回溯中的返回地址转换为函数名，并按 `FlameGraph`_ 期望的格式输出。

配置
****

你可以使用以下选项配置此模块：

* :kconfig:option:`CONFIG_PROFILING_PERF`：启用该模块。此选项会向 shell 添加 ``perf`` 命令。

* :kconfig:option:`CONFIG_PROFILING_PERF_BUFFER_SIZE`：设置 perf 缓冲区的大小，样本在打印之前保存在该缓冲区中。

架构后端可能需要额外的栈展开支持。Cortex-M 后端需要 SysTick、线程栈信息、额外的异常信息、Arm 栈遍历支持以及单处理器配置。

用法
****

关于如何使用 perf 工具的示例，请参见 :zephyr:code-sample:`profiling-perf` 示例。

 .. _FlameGraph: https://github.com/brendangregg/FlameGraph/
