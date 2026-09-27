.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _net_timeout_interface:

网络超时
########

.. contents::
    :local:
    :depth: 2

概述
****

Zephyr 的网络基础设施大多使用毫秒分辨率的运行时钟来跟踪超时，截止时间和持续时间都用 32 位无符号值表示。该 32 位值会在 49 天 17 小时 2 分 47.296 秒后回绕。

超时处理常常受到延迟的影响，因此检查超时的时刻可能晚于其本应到期的时刻。要在不对最大延迟做任意假设的前提下正确处理这种情况，可直接表示的最大延迟必须是 31 位非负数值（``INT32_MAX``），它会在 24 天 20 小时 31 分 23.648 秒后溢出。

大多数网络超时都短于延迟回绕时间，但少数协议允许以秒为单位的 32 位无符号值表示延迟，相当于 42 位毫秒计数。

net_timeout API 提供了通用的超时机制，用于正确跟踪这些持续时间更长的超时的剩余时间。

用法
****

该 API 最简单的用法如下：

#. 使用 :c:func:`net_timeout_set()` 配置网络超时。
#. 使用 :c:func:`net_timeout_evaluate()` 确定距离超时发生还有多长时间，并在该延迟之后安排一次超时。
#. 当超时回调被调用时，再次使用 :c:func:`net_timeout_evaluate()` 判断超时是否已经完成，还是仍有剩余时间。如果是后者，则重新安排回调。
#. 超时运行期间，可以使用 :c:func:`net_timeout_remaining` 获取距离超时到期还有多少秒。这可用于显式更新超时：应取消所有挂起的回调，然后以新的超时从第 1 步重新开始。

:c:struct:`net_timeout` 包含一个 ``sys_snode_t``，允许多个超时实例聚合在一起共享同一个内核定时器元素。应用必须对所有实例使用 :c:func:`net_timeout_evaluate()`，以确定下一个要发生的超时事件。

:c:func:`net_timeout_deadline()` 可用于重建超时的全精度截止时间。它主要用于测试，但在某些应用中也有用处，因为它确实允许以毫秒分辨率计算剩余时间。

API 参考
********

.. doxygengroup:: net_timeout
