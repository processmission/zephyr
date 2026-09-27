.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ztest_benchmarking:

基准测试框架
############

Zephyr 基准测试框架提供周期级精度的性能测量，自动采集数据和计算统计值，为评估整个 Zephyr 生态系统的执行指标提供统一方式。

概述
****

该框架通过以下能力帮助发现性能回退和优化关键路径：

* **标准化 API**：宏遵循现有 ``ztest`` 约定。
* **统计分析**：计算均值、标准差、标准误及最小／最大值。
* **开销补偿**：加入对照测试，计入基准测试框架自身的执行时间。

配置
****

要使用基准测试框架，必须启用以下 Kconfig 选项：

.. code-block:: cfg

   CONFIG_ZTEST=y
   CONFIG_ZTEST_BENCHMARK=y

用法
****

基准测试套件的定义方式类似普通 ztest 套件：先用 ``ZTEST_BENCHMARK_SUITE`` 定义套件，再用 ``ZTEST_BENCHMARK`` 或 ``ZTEST_BENCHMARK_TIMED`` 宏添加各项基准测试。

.. code-block:: c

   #include <zephyr/ztest.h>

   ZTEST_BENCHMARK_SUITE(<test suite name>, <setup_fn>, <teardown_fn>);


标准基准测试
============

标准基准测试基于采样，执行指定次数的测试并测量总周期数，适合用周期数衡量关键路径的原始 CPU 性能。它可反映代码效率，帮助识别 CPU 使用瓶颈，适用于执行时间稳定、不易受 I/O 操作或上下文切换等外部因素影响的代码。

.. code-block:: c

   #include <zephyr/ztest.h>

   ZTEST_BENCHMARK_SUITE(<suite name>, NULL, NULL);

   ZTEST_BENCHMARK(<suite name>, <benchmark name>, <number of samples>, <setup_fn>, <teardown_fn>)
   {
       /* Code to benchmark */
   }

标准基准测试在每次采样前调用 setup 函数，按指定采样次数执行测试函数，并在每次采样后调用 teardown 函数。

计时基准测试
============

与标准基准测试不同，计时基准测试测量代码执行时间而非周期数，适合执行时间不固定的代码，或需要衡量关键路径实际耗时的情况。它能更全面地反映性能，尤其适用于涉及 I/O、上下文切换或其他超出原始 CPU 性能影响范围的因素的代码。

.. code-block:: c

   ZTEST_BENCHMARK_TIMED(<suite name>, <benchmark name>, <time in ms>, <setup_fn>, <teardown_fn>)
   {
         /* Code to benchmark */
   }


标准基准测试侧重隔离，计时基准测试则只执行一次 setup 和 teardown，让测试函数在专用时间窗口内持续运行。这样会计入实际场景中的中断、上下文切换和其他后台任务等系统开销，使测量更贴近实际。

理解结果
********

标准基准测试结果
================

.. code-block:: console

   <suite name> ###############################################
   <benchmark name> ===========================================
      Sample size:<number of samples>, total cycles: <total amount of cycles>
      Mean(u): <mean cycles per sample>
      Standard deviation(s): <cycles>
      Standard Error(SE): <cycles>
      Min: <cycles> (run #<sample number>)
      Max: <cycles> (run #<sample number>)


统计指标
""""""""

* **均值（u）**：每次采样消耗周期数的平均值，表示预期执行成本的中心值。

* **标准差（s）**：衡量执行成本相对于均值的变化或波动程度。标准差低表示行为确定且一致。

* **标准误（SE）**：估计样本均值可能与系统“真实”均值相差多远，反映测试的统计可靠性。SE 越低，结果的可信度越高。

* **最小／最大值**：观测到的最小和最大周期数，以及它们出现在哪次采样。

简单来说，这些指标均越低越好。均值、最小值和最大值越低，原始性能越好；标准差和标准误越低，性能越一致，也越可靠。

计时基准测试结果
================

.. code-block:: console

   <benchmark name> ===============================================
      Samples: <Number of samples executed during the benchmark>
      Total Time: <Gross execution time>
      Work Time: <Net execution time> ns (Net)
      Ops/Sec: <average operations per second>
      Cycles/Op: <average cycles per operation>

Statistical Metrics
"""""""""""""""""""
* **总时间**：基准测试所有采样的总耗时，包括开销。

* **工作时间**：被测代码的总耗时，不含基准测试框架自身开销，更准确地反映被测代码的实际性能。

* **Ops/Sec**：每秒可执行的操作（采样）数，由采样数除以净工作时间（秒）得到，尤其适合衡量被测代码的吞吐量。

* **Cycles/Op**：每次操作平均消耗的 CPU 周期数，由净周期数除以采样数得到，反映代码使用 CPU 的效率。

通常 Ops/Sec 越高越好，表示吞吐量更高；Cycles/Op 则越低越好。两者由同一组底层数据推导，从不同角度反映相同的性能特征。较高 Ops/Sec 应对应较低 Cycles/Op，反之亦然。


基准测试输出选项
================

框架提供多种结果输出方式，默认使用详细、易于阅读和理解的格式。也可启用 :kconfig:option:`CONFIG_ZTEST_BENCHMARK_OUTPUT_CSV`，以 CSV 格式输出，便于脚本导入后进一步分析。CSV 包含与详细输出相同的全部指标，但更适合自动分析和报告。

标准基准测试的 CSV 输出格式如下：

.. code-block:: console

   S,<suite name>,<benchmark name>,<sample size>,<total cycles>,<mean>,<stddev>,<stderr>,<min>,<min sample>,<max>,<max sample>

计时基准测试的 CSV 输出格式如下：

.. code-block:: console

   T,<suite name>,<benchmark name>,<samples>,<total time>,<work time>,<ops/sec>,<cycles/op>


注意事项
********

* **噪声**：基准测试本身对系统噪声敏感。为尽量获得准确结果，应禁用可能干扰计时的不必要后台任务和中断。

* **缓存预热**：首次采样常因缓存未命中而较慢，样本较少时可能使结果产生偏差。应选取足够大的样本数来减轻此影响。

* **使用 setup/teardown 函数**：*强烈* 建议使用这些函数尽可能隔离被测代码。基准测试代码中包含过多初始化或清理代码会引入噪声，对很短的关键路径可能产生 *显著* 偏差。


API 参考
********

.. doxygengroup:: ztest_benchmark
