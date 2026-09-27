.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _zyclictest:

Zyclictest
##########

zyclictest 模块可用于估算实时线程的最坏情况延迟。它可以测量从硬件中断到服务例程，再到 Zephyr 线程的时间。

该模块及其名称的灵感来自 Linux 上的 cyclictest 程序。这就是它被称为 Zephyr cyclictest 的原因。

其思路是使用定时器中断作为中断源，因为我们确切知道该中断发生的时间点。在中断服务例程中，我们获取时间并计算与定时器中断编程时间的差值。

此外，线程也会根据定时器进行同步，并测量与编程定时器时间的差值。

这两个时间值都会放入一个数组中，该数组作为测量结束时打印的直方图的数据源。

该测量以特定间隔时间循环进行。

如果有人想知道优先级为 <p> 的任务的最坏情况延迟，那么应用程序需要处于运行状态。在它运行期间，我们可以启动 zyclictest，其优先级数值至少比被探测的应用程序线程小 1。例如，如果目标线程所在应用程序的优先级为 -10，那么我们需要以 -11 或更小的优先级数值启动 zyclictest。

另一个重要参数是间隔时间。间隔时间不应小于测得的最坏情况延迟。因此，建议将间隔时间设置为预期或测得的最坏情况延迟的至少两倍。

如果测量结束时指示存在溢出，这意味着直方图范围内不存在确定性的最坏情况延迟。

为了获得有意义的输出，建议将 :kconfig:option:`CONFIG_SYS_CLOCK_TICKS_PER_SEC` 至少设置为 1000000，因为这意味着最小分辨率为 1 微秒。还需要无滴答内核（:kconfig:option:`CONFIG_TICKLESS_KERNEL`：）。

操作模式
********

Zyclictest 可以不指定固定循环次数，直接以自由运行方式启动。这是默认模式。停止后，会打印到目前为止的结果。

在循环模式下（使用 -l <loops> 选项启动），zyclictest 会运行预定义的循环次数。达到该循环次数时，shell 上会显示一条指示测试结束的消息。但可以使用 zyclictest stop -c 提前取消测试。

配置
****

使用以下选项配置此模块。

* :kconfig:option:`CONFIG_ZYCLICTEST_SHELL` 启用 shell 命令。


用法
****

zyclictest start [options]
  -i <interval>  以微秒为单位的间隔时间
  -l <loops>     使用具有预定义循环次数的循环模式
  -p <prio>      设置线程优先级

zyclictest stop [options]
  -c             提前取消循环模式
  -q             安静模式，打印摘要，但不打印直方图数据

示例
****

在此示例中，我们想知道一个由中断唤醒并以优先级 -10 作为协作式任务运行的线程的最坏情况延迟。我们预期延迟小于 200 微秒。我们使用自由运行模式。

1. 以 400 微秒的间隔（预期最坏情况延迟的两倍）和 -11 的优先级（比应用程序线程高一个数值）启动 zyclictest 线程：

   .. code-block:: console

      zyclictest start -i 400 -p -11

2. 执行需要测试的任何操作……

3. 停止测量：

   .. code-block:: console

      zyclictest stop

   zyclictest 的输出：

   ::

      Count: 547329
                         IRQ  Thread
      Max-Latency:        21      27
      Errors:              0       0
      Overflow:            0       0
      Histogram:
      [...]
       23                  0  547306
       24                  0       2
       25                  0       5
       26                  0       5
       27                  0       2
       28                  0       0
      [...]

4. 解读结果：

   没有错误，也没有溢出，这意味着该测量结果可以使用。测试中共有 547329 个循环。最坏情况中断延迟为 21 微秒，线程的最坏情况延迟为 27 微秒。
