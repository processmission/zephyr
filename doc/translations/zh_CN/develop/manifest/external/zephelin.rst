.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_zephelin:

Zephelin
########

简介
****

`Zephyr Profiling Library`_ （ZPL），简称 Zephelin，可捕获和报告运行时性能指标，用于 Zephyr 应用的性能剖析及深入分析，尤其关注运行 AI/ML 推理工作负载的应用。

此外，Zephelin 还简化了对 `LiteRT`_、`microTVM`_ 等 AI 运行时的分析，帮助了解底层瓶颈及可能的优化机会。

Zephelin 的功能：

* 跟踪 Zephyr 应用在硬件上的执行
* 通过 UART、USB 或调试适配器等后端获取跟踪数据
* 以 CTF 和 TEF 格式输出跟踪数据
* 提供从设备捕获跟踪数据的脚本
* 从以下来源收集数据：

  * 内存：栈、堆、内核堆和内存 slab
  * 传感器：例如芯片温度传感器
  * 线程分析：CPU 使用率
  * AI 运行时：例如 LiteRT 中的张量内存区使用情况

* 显示 LiteRT 或 microTVM 运行时所执行神经网络层的详情：

  * 输入、输出和权重的维度
  * 层参数
  * 执行特定层耗费的时间和资源

* 支持编译时和运行时配置

* 可配置性能剖析级别，控制要收集的子系统及数据量

以上内容均可通过 `Zephelin Trace Viewer`_ 分析。

在 Zephyr 中使用
****************

要将 Zephelin 作为 Zephyr :ref:`模块 <modules>` 使用，添加以下条目：

.. code-block:: yaml

   manifest:
     projects:
       - name: zephelin
         url: https://github.com/antmicro/zephelin
         revision: main
         path: modules/zephelin # adjust the path as needed

将其加入 Zephyr 子清单，例如 ``zephyr/submanifests/zephelin.yaml``，并运行 ``west update``；也可以将其作为 West 项目加入项目的 ``west.yaml`` 清单。

更多信息见 `Zephelin documentation`_。

参考资料
********

.. target-notes::

.. _Zephyr Profiling Library:
   https://github.com/antmicro/zephelin

.. _Zephelin documentation:
   https://antmicro.github.io/zephelin/

.. _Zephelin Trace Viewer:
   https://antmicro.github.io/zephelin-trace-viewer

.. _LiteRT:
   https://ai.google.dev/edge/litert

.. _microTVM:
   https://tvm.apache.org/docs/
