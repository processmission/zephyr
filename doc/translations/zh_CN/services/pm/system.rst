.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _pm-system:

系统电源管理
############

简介
****

当内核没有可调度的任务时就会进入空闲状态。启用 :kconfig:option:`CONFIG_PM` 后，内核可以请求电源管理子系统把空闲系统置入某个受支持的电源状态。内核会给出希望挂起的时长，随后 PM 子系统根据配置的电源管理策略决定应转换到哪个合适的电源状态。

应用负责设置唤醒事件。唤醒事件通常是由 SoC 外设模块触发的中断，例如 SysTick、RTC、计数器或 GPIO。请注意，取决于具体的 SoC 和电源模式，并非所有外设都处于活动状态，因此某些唤醒源可能无法在所用电源模式下使用。

下图说明系统电源管理：

.. graphviz::
   :caption: 系统电源管理

   digraph G {
       compound=true
       node [height=1.2 style=rounded]

       lock [label="Lock interrupts"]
       config_pm [label="CONFIG_PM" shape=diamond style="rounded,dashed"]
       forced_state [label="state forced ?", shape=diamond style="rounded,dashed"]
       config_system_managed_device_pm [label="CONFIG_PM_DEVICE" shape=diamond style="rounded,dashed"]
       config_system_managed_device_pm2 [label="CONFIG_PM_DEVICE" shape=diamond style="rounded,dashed"]
       pm_policy [label="Check policy manager\nfor a power state "]
       pm_suspend_devices [label="Suspend\ndevices"]
       pm_resume_devices [label="Resume\ndevices"]
       pm_state_set [label="Enter power state\n(SoC API)" style="rounded,bold"]
       pm_system_resume [label="Resume bookkeeping\n(post ops, notify, clock)" style="rounded,bold"]
       unlock_irq [label="Unlock interrupts"]
       handle_interrupts [label="Handle interrupts\nand schedule threads"]
       k_cpu_idle [label="k_cpu_idle()"]

       subgraph cluster_idle {
           style=dashed
           label = "idle()"

           lock -> config_pm
           config_pm -> k_cpu_idle [label="no"]
           k_cpu_idle -> unlock_irq
       }

       subgraph cluster_pm_system_suspend {
           style=dashed
           label = "pm_system_suspend()"

           forced_state -> config_system_managed_device_pm [label="yes"]
           forced_state -> pm_policy [label="no"]
           pm_policy -> config_system_managed_device_pm
           config_system_managed_device_pm -> pm_state_set [label="no"]
           config_system_managed_device_pm -> pm_suspend_devices [label="yes"]
           pm_suspend_devices -> pm_state_set
           pm_state_set -> config_system_managed_device_pm2
           config_system_managed_device_pm2 -> pm_resume_devices [label="yes"]
           config_system_managed_device_pm2 -> pm_system_resume [label="no"]
           pm_resume_devices -> pm_system_resume
       }

       {rankdir=LR k_cpu_idle; forced_state}
       config_pm -> forced_state [label="yes"]
       pm_policy -> k_cpu_idle [label="PM_STATE_ACTIVE\n(no power state meets requirements)"]
       pm_system_resume -> unlock_irq [constraint=false]
       unlock_irq -> handle_interrupts
       handle_interrupts -> lock:n [label="no runnable thread"]
   }

空闲线程在调用 :c:func:`pm_system_suspend` 之前会关闭中断，并保持对原始架构中断键的所有权。如果 PM 子系统进入了低功耗状态，则在对所有由系统管理的设备完成恢复之后，PM 恢复记账仍在中断关闭的状态下运行，其中包括 :c:func:`pm_state_exit_post_ops`、PM 退出通知以及系统时钟的空闲退出计数。该记账完成且 :c:func:`pm_system_suspend` 返回之后，空闲线程才恢复原始的中断键。

未选择 ``CONFIG_PM_STATE_SET_IRQ_UNLOCKED`` 的架构和 SoC 在低功耗指令前后立即使用架构钩子，这样无需先派发唤醒源 ISR 也能观察到唤醒事件。在这种模式下，:c:func:`pm_state_set` 和 :c:func:`pm_state_exit_post_ops` 只能用于 SoC 相关的硬件操作，而不能用作最终的中断解除屏蔽点。

使用这一默认约定时，中断所有权的顺序如下：

.. mermaid::
   :caption: 系统 PM 中断恢复所有权
   :alt: Sequence diagram showing idle locking interrupts, PM entering the SoC
       power state, architecture PM state hooks allowing wake without ISR
       dispatch, PM resume bookkeeping, and idle unlocking interrupts.

   sequenceDiagram
        participant Workers as Other threads
        participant Idle as idle()<br/>(idle thread context)
        participant PM as pm_system_suspend()
        participant SoC as pm_state_set()<br/>(SoC hook)
        participant HW as Hardware

        loop Idle cycle
            Note over Workers: Thread enters SLEEP/PENDING state<br/>e.g. k_sleep() / k_sem_take()
            alt Runnable thread(s) remaining
                Workers-->>Workers: Schedule another thread
            else No runnable thread remaining
                Workers-->>Idle: Switch to idle thread
            end
            Idle->>Idle: Lock interrupts
            Note left of Idle: Interrupts are locked<br/>during PM sequence
            Idle->>PM: Suspend idle CPU
            PM->>PM: Suspend devices<br/>(if applicable)
            PM->>PM: Set idle timeout
            PM->>PM: Notify PM state entry
            PM->>SoC: Enter power state
            SoC->>SoC: SoC-specific pre-entry operations
            SoC->>SoC: Run arch PM prepare hook
            SoC->>HW: Trigger low-power state entry
            HW-->>SoC: Wake-up event occurs
            SoC->>SoC: Run arch PM finish hook
            SoC->>SoC: SoC-specific post-wakeup operations
            SoC-->>PM: Power state exit complete
            PM->>PM: Resume devices<br/>(if applicable)
            PM->>PM: Run post ops, notify exit, clock idle exit
            PM-->>Idle: Resume complete
            Idle->>Idle: Unlock interrupts
            HW-->>Idle: Pending interrupts are handled
            Idle-->>Workers: Idle thread yields<br/>or is preempted
            Note over Workers: Non-idle thread starts executing
        end

使用这一默认约定的 SoC 实现不得在 :c:func:`pm_state_set` 或 :c:func:`pm_state_exit_post_ops` 中解除中断屏蔽。仍从这些钩子调用 ``irq_unlock(0)``、``arch_irq_unlock(0)``、``__enable_irq()`` 或等效操作的旧实现，在完成迁移之前必须选择 ``CONFIG_PM_STATE_SET_IRQ_UNLOCKED``。

.. note::

    上述顺序保证只适用于 :c:func:`arch_irq_lock` 能够屏蔽的中断。零延迟中断不在此顺序范围内。参见 :ref:`zlis`。


电源状态
========

电源管理子系统定义了一组状态，每个状态由其功耗和上下文保持能力来描述。

电源状态集合由 :c:enum:`pm_state` 定义。一般来说，功耗越低的状态（在枚举中索引越大）越省电，但唤醒延迟也越高。

电源管理策略
============

电源管理子系统支持以下电源管理策略：

* 基于驻留时间
* 应用自定义

策略管理器是电源管理子系统中负责决定系统应转换到哪个电源状态的组件。策略管理器只能在平台已定义的状态之间选择。根据策略的不同，对决策的其他约束还可能包括禁止某些电源状态的锁，以及各种最小和最大延迟值。

有关状态定义的更多细节，请参阅 :dtcompatible:`zephyr,power-state` 绑定文档。

驻留时间
--------

在驻留策略下，系统会进入最省电的电源状态，其约束是：最小驻留值（参见 :dtcompatible:`zephyr,power-state`）与退出该模式的延迟之和，必须小于或等于内核调度的系统空闲时长。

因此，核心逻辑可以用下面的表达式概括：

.. code-block:: c

   if (time_to_next_scheduled_event >= (state.min_residency_us + state.exit_latency)) {
      return state
   }

应用
----

应用通过实现 :c:func:`pm_policy_next_state` 函数来定义电源管理策略。在该策略下，应用可以根据距离下一个已调度超时的剩余时间，自由决定系统应转换到哪个电源状态。

自定义策略的应用示例见 :zephyr_file:`tests/subsys/pm/power_mgmt/`。

自定义 tick 钩子
----------------

除了内核 tick 到期时间和 PM 策略事件列表之外，应用和 SoC 相关代码可能还需要从专有或硬件相关的数据源推导下一次唤醒时间。这些数据源包括硬件寄存器、仅提供二进制的第三方模块，或难以建模为标准 PM 策略事件的复杂或遗留数据结构。

启用 :kconfig:option:`CONFIG_PM_CUSTOM_TICKS_HOOK` 后，PM 核心会在 :c:func:`pm_system_suspend()` 期间调用可选函数 :c:func:`pm_policy_next_custom_ticks()`。该钩子返回距离下一个自定义事件的 tick 数；如果无需考虑任何自定义事件，则返回 ``K_TICKS_FOREVER``。

随后 PM 核心在以下各项中选择最早到期的一个：

* 内核 tick 到期时间，
* PM 策略事件列表的 tick（来自 :c:func:`pm_policy_next_event_ticks()`），
* 自定义 tick 值（来自 :c:func:`pm_policy_next_custom_ticks()`）。

这一机制让开发板和应用可以把额外的定时源纳入系统电源管理决策，而无需修改 PM 事件列表基础设施。

.. _pm-policy-power-states:

策略与电源状态
--------------

电源管理子系统允许不同的 Zephyr 组件和应用配置策略管理器，以阻止系统转换到某些电源状态。设备在后台执行任务时可以使用该机制，防止系统进入会丢失上下文的特定状态。参见 :c:func:`pm_policy_state_lock_get`。

示例
====

以下示例展示了不同的电源管理功能：

* :zephyr_file:`samples/boards/st/power_mgmt/blinky/`
* :zephyr_file:`samples/boards/espressif/deep_sleep/`
* :zephyr_file:`samples/subsys/pm/device_pm/`
* :zephyr_file:`tests/subsys/pm/power_mgmt/`
* :zephyr_file:`tests/subsys/pm/power_mgmt_soc/`
* :zephyr_file:`tests/subsys/pm/power_states_api/`
