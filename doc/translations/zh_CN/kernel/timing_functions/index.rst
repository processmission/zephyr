.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _timing_functions:

执行时间测量函数
################

计时函数可用于获取一段代码的执行时间，以帮助分析和优化。

请注意，计时函数可能使用与默认内核定时器不同的定时器，具体使用的定时器由架构、SoC 或开发板配置指定。

配置
****

要使用计时函数，需要启用 :kconfig:option:`CONFIG_TIMING_FUNCTIONS`。

用法
****

收集计时信息的步骤如下：

1. 调用 :c:func:`timing_init` 初始化定时器。

2. 调用 :c:func:`timing_start`，标记开始收集计时信息。这通常会启动定时器。

3. 调用 :c:func:`timing_counter_get`，标记代码执行的起点。

4. 调用 :c:func:`timing_counter_get`，标记代码执行的终点。

5. 调用 :c:func:`timing_cycles_get`，获取代码执行起点与终点之间的定时器周期数。

6. 以总周期数为参数调用 :c:func:`timing_cycles_to_ns`，将周期数转换为纳秒。

7. 从步骤 3 开始重复操作，收集其他代码块的计时信息。

8. 调用 :c:func:`timing_stop`，标记结束收集计时信息。这通常会停止定时器。

示例
----

以下示例展示如何使用计时函数：

.. code-block:: c

   #include <zephyr/timing/timing.h>

   void gather_timing(void)
   {
       timing_t start_time, end_time;
       uint64_t total_cycles;
       uint64_t total_ns;

       timing_init();
       timing_start();

       start_time = timing_counter_get();

       code_execution_to_be_measured();

       end_time = timing_counter_get();

       total_cycles = timing_cycles_get(&start_time, &end_time);
       total_ns = timing_cycles_to_ns(total_cycles);

       timing_stop();
   }

API 文档
********

.. doxygengroup:: timing_api
.. doxygengroup:: timing_api_arch
.. doxygengroup:: timing_api_soc
.. doxygengroup:: timing_api_board
