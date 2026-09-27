.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _system_timer_drivers:

系统定时器驱动程序
##################

本页介绍内核时钟节拍计数与产生这些时钟节拍的硬件驱动程序之间的接口。内核侧的计数处理，以及应用可见的所有内容，见 :ref:`kernel_timing`。

定时器驱动程序
==============

时钟节拍级别的内核计时由定时器驱动程序驱动，其 API 相对简单。

* 驱动程序应能够通过 :c:func:`sys_clock_announce` 调用向内核“通告”新的时钟节拍，传入自上次通告调用（或系统启动）以来经过的整数个时钟节拍。这些调用可在任意时刻发生，但驱动程序应尽量确保它们接近时钟节拍边界（而非在节拍“中途”）发生，具体精度受中断延迟等因素影响。最重要的是，计数必须长期保持正确，与其他计数器和真实世界时间之间的偏差应尽可能小。

* 驱动程序应向内核提供 :c:func:`sys_clock_set_timeout` 调用，用于指定再经过多少个时钟节拍后，内核必须收到通告调用以触发已注册的超时。在该时刻之前通告新的时钟节拍是允许的（但计数必须正确），而超过该时刻才通告则会导致错过事件。注意，这里传入的超时值是相对于当前时刻的差值，但驱动程序仍必须长期以稳定速率提供时钟节拍。简单草率的实现容易错误地“重置”不足一个时钟节拍的部分，导致时钟偏差。

* 驱动程序应提供 :c:func:`sys_clock_elapsed` 调用，报告从上次调用 :c:func:`sys_clock_announce` 到当前经过的时钟节拍数（与真实世界时钟相符），内核需要用它检查新到来的超时是否到期。

* 驱动程序可以选择提供 :c:func:`sys_clock_no_timeout` 调用。当没有待处理超时，即超时队列为空，且启用了 :kconfig:option:`CONFIG_SYSTEM_CLOCK_SLOPPY_IDLE` 时，内核调用它来代替 :c:func:`sys_clock_set_timeout`。

  此时不会有即将到来的时钟节拍通告，系统也不关心精确维护运行时间，因此驱动程序可以采取措施节省资源。下次调用 :c:func:`sys_clock_set_timeout` 时恢复正常运行；与 :c:func:`sys_clock_disable` 不同，这不是停用定时器。

  不得停止定时器的 *计数器*。:c:func:`sys_clock_cycle_get_32` 和 :c:func:`sys_clock_cycle_get_64` 必须持续递增，就像从未发生过该调用一样。

  .. note::

     超时队列为空时 CPU 仍会继续运行，例如就绪队列中仍有线程，或者发生了中断。这些线程和 ISR 可能调用 :c:func:`k_cycle_get_32` 或 :c:func:`k_busy_wait`。因此实现所能采取的措施受到限制：屏蔽定时器中断是安全的，但关闭定时器时钟很可能不安全。具体哪些措施安全取决于硬件。

  该钩子是可选的。如果未提供，内核会请求 :c:func:`sys_clock_set_timeout` 等待其能够表示的最长时间，即 ``UINT32_MAX`` 个时钟节拍。该数值与此处原来的 ``K_TICKS_FOREVER`` 相同，后者长期用于表示“没有截止时间”，因此尚未转换的驱动程序仍可继续工作。

* 驱动程序可以选择提供 :c:func:`sys_clock_idle_enter` 调用，当 CPU 即将进入低功耗空闲状态时，电源管理路径会用它代替 :c:func:`sys_clock_set_timeout`。它接收距离下一次预期唤醒的时钟节拍数；如果没有预期唤醒且允许运行时间计数发生漂移，则接收 ``SYS_CLOCK_IDLE_FOREVER``。

  需要移交给低功耗唤醒定时器，或以其他方式为休眠重新配置自身的驱动程序，应在这里执行这些操作。收到 ``SYS_CLOCK_IDLE_FOREVER`` 时，它还可以停止其时基，这是 :c:func:`sys_clock_no_timeout` 不允许的，因为 CPU 正在进入空闲状态，且保证在恢复时调用 :c:func:`sys_clock_idle_exit`。只有调用 CPU 会进入空闲状态，因此若驱动程序的时基由多个 CPU 共享，必须确保只有最后一个进入空闲状态的 CPU 才停止时钟。

  该钩子是可选的。如果未提供，调用 :c:func:`sys_clock_set_timeout` 时会将其已弃用的 ``idle`` 参数设为 ``true``，因此仍根据该参数执行低功耗处理的驱动程序可以继续工作。

最后三个入口对应系统可能处于的四种状态：

.. list-table::
   :header-rows: 1
   :widths: 15 45 40

   * -
     - 无待处理事件
     - 有待处理事件
   * - **运行**
     - ``sys_clock_no_timeout()``
     - ``sys_clock_set_timeout(ticks)``
   * - **空闲**
     - ``sys_clock_idle_enter(SYS_CLOCK_IDLE_FOREVER)``
     - ``sys_clock_idle_enter(ticks)``

未启用 :kconfig:option:`CONFIG_SYSTEM_CLOCK_SLOPPY_IDLE` 时，不会出现左列情况：内核持续设置人为生成的截止时间，以保持运行时间精确，因此驱动程序只会看到右列情况。

定时器驱动程序的锁定机制
========================

内核通过 :c:func:`sys_clock_lock` 和 :c:func:`sys_clock_unlock` 提供统一的定时器锁。该锁同时保护内核内部的时钟节拍计数（``curr_tick``、超时队列），以及必须与其保持一致的驱动程序私有状态，例如硬件周期计数器的基准值。

维护内部状态的定时器驱动程序，应在 ISR 开始时获取此锁，更新硬件状态，再将锁键传给 :c:func:`sys_clock_announce_locked`，由后者接管并释放锁。这确保驱动程序的周期计数器基准值与内核的 ``curr_tick`` 始终在同一把锁保护下更新，从而消除使用两把独立锁时可能在 SMP 系统中出现的竞态条件。这类问题也可能出现在较少见的 UP 场景中，即更高优先级 ISR 需要一致的实时时间参考时。

内核调用驱动程序提供的 :c:func:`sys_clock_set_timeout` 和 :c:func:`sys_clock_elapsed` 回调时，始终已经持有此锁。

为保持向后兼容，:c:func:`sys_clock_announce` 仍然可用，并在内部获取此锁。新驱动程序及已迁移的驱动程序应优先使用 :c:func:`sys_clock_lock` / :c:func:`sys_clock_announce_locked` 模式。

注意，该 API 的自然实现会形成“无节拍”内核，仅为已注册的事件接收和处理定时器中断，并依靠可编程硬件计数器提供不规则间隔的中断。不过，也很容易实现传统的“有节拍”或“简单”计数器驱动程序：

* 驱动程序可以按操作系统时钟节拍频率定期接收中断，并在每次中断中以参数一调用 :c:func:`sys_clock_announce`。

* 驱动程序可以忽略 :c:func:`sys_clock_set_timeout` 调用，因为无论超时状态如何，每个时钟节拍都会被通告。

* 驱动程序可以对每次 :c:func:`sys_clock_elapsed` 调用都返回零，因为不可能检测到已经过一个以上的时钟节拍，否则就已经收到了中断。

SMP 细节
========

总体而言，在多处理器环境中运行时，上述定时器 API 保持不变。内核会在内部正确同步所有访问，并确保所有临界区尽可能短小。不过，以下几点需要详细说明：

* Zephyr 不限定由哪个 CPU 处理定时器中断。让所有定时器中断都由单个处理器处理是允许的，尽管某些情况下可能并不理想。现有 SMP 架构实现的是对称定时器驱动程序。

* :c:func:`sys_clock_announce` 调用应在驱动程序层面进行全局同步。内核不按 CPU 跟踪计数；如果两个定时器中断几乎同时触发，内核期望只有一个向计时子系统提供当前时钟节拍数。另一个在没有经过新时钟节拍时，可以合法地通告零个时钟节拍。由于时间片的要求，它不应“跳过”通告调用（参见 :ref:`kernel_timing` 中关于时间片的说明）。

* 有些 SMP 硬件使用单个全局定时器设备，另一些则为每个 CPU 提供计数器。相关复杂性（例如确保 CPU 之间的计数器同步）应由驱动程序管理，而不是内核。

* 通过 :c:func:`sys_clock_set_timeout` 传回驱动程序的下一次超时值，对每个 CPU 都相同。因此，默认情况下，每个事件都会使所有 CPU 同时收到定时器中断，尽管按定义其中只有一个应以非零时钟节拍参数调用 :c:func:`sys_clock_announce`。对于时序敏感的应用，这可能是合理的默认行为，因为它尽量降低了异常 ISR 或中断锁定延迟超时的可能性；但在某些情况下也可能带来性能问题。当前设计将此类优化交由定时器驱动程序负责。

通用无节拍核心
==============

上述工作，即周期到时钟节拍的转换、通告基准值、对齐到时钟节拍的截止时间计算，以及计数器回绕和范围处理，在各个无节拍驱动程序中几乎相同。各自手工编写的实现反复引发定时器缺陷。:zephyr_file:`drivers/timer/system_timer_generic.h` 统一实现了这些逻辑。

这是实现头文件，而非声明头文件：包含它会 *定义* :c:func:`sys_clock_set_timeout`、:c:func:`sys_clock_elapsed` 以及 :c:func:`sys_clock_cycle_get_32` / :c:func:`sys_clock_cycle_get_64`。任意数量的驱动程序都可以基于它实现；每个驱动程序在提供下述宏和原语后包含它一次。一次构建只编译一个系统定时器驱动程序，因此这些定义只会出现一次。随后驱动程序只需处理周期，时钟节拍域由该核心负责。

核心会生成两个周期读取函数，无论计数器位宽如何都会生成 64 位版本：通告基准值为 64 位，而未被调用的读取函数会由链接器移除。

驱动程序仍可自行决定是否选择 :kconfig:option:`CONFIG_TIMER_HAS_64BIT_CYCLE_COUNTER`。此选项表示 64 位读取成本低，至少不高于 32 位读取，因此优先使用较窄的读取函数没有收益。启用 ``TIMER_CORE_COUNTER_NONATOMIC`` 时，两者都使用时钟锁，这一条件成立；对于小于 64 位的原子计数器，只有 64 位读取函数需要获取锁，32 位读取仍然无锁。

必须提供两个原语：读取硬件周期计数器的 ``timer_driver_cycle_get()``，以及根据后端选择的定时设置函数 ``timer_driver_set_compare()`` 或 ``timer_driver_set_reload()``。驱动程序的 ISR 应先应答硬件中断，再调用 ``timer_core_announce()``；初始化函数应先连接 IRQ，再调用 ``timer_core_init()``；在 SMP 系统中，其 ``smp_timer_init()`` 应调用 ``timer_core_smp_prime()``。

后端选择
--------

必须恰好选择以下一项来描述硬件：

``TIMER_CORE_BACKEND_COMPARE_ORDERED``
   绝对比较器，按大小匹配：计数器达到或超过编程值时触发中断，因此已过去的截止时间会立即触发。可用范围为计数器计数范围的一半。

``TIMER_CORE_BACKEND_COMPARE_EXACT``
   绝对比较器，相等匹配：如果写入某个值时计数器已越过该值，就会错过匹配，直到完整经过一个计数器周期。核心通过校验循环写入比较器，因此驱动程序无需自行设置最小延迟下限。

``TIMER_CORE_BACKEND_RELOAD``
   相对延迟：适用于递减计数器，以及比较匹配后复位的周期定时器。假定硬件会自动重装载，因此有节拍内核可按初始化时设置的值自由运行。

可选宏
------

仅在下述默认值不适用时，才定义相应宏：

``TIMER_CORE_CYCLES_PER_SEC``
   计数器频率，单位为 Hz，默认为内核系统时钟频率。计数器经过预分频或使用自身固定频率时应设置此项。核心据此派生 ``TIMER_CORE_CYC_PER_TICK``，驱动程序可读取它用于自身硬件配置，通常用于初始化时设置一个时钟节拍的周期，但不得自行定义它。

``TIMER_CORE_CYCLES_PER_SEC_RUNTIME``
   上述频率是变量而非构建时常量，因为它从时钟控制器读取或在初始化时计算。此时核心会预先计算一次每个时钟节拍的周期数，而不是依赖除法的常量折叠。在调用 ``timer_core_init()`` 之前，该变量必须已经具有最终值。

``TIMER_CORE_COUNTER_WIDTH``
   ``timer_driver_cycle_get()`` 返回计数值的位宽，最大为 64 位，默认为本机寄存器位宽。使用其他位宽的计数器必须明确指定：否则，32 位 CPU 上真正的 64 位计数器会沿用 32 位掩码，丢失超过 2^32 个周期的时间跨度。核心会按此位宽对每个差值应用掩码，因此窄计数器可以直接读取原始值，驱动程序无需在软件中扩展计数值。

``TIMER_CORE_COUNTER_NONMONOTONIC``
   计数器可能短暂读出小于先前观测值的数值，QEMU SMP 下的全局定时器即如此。核心将这种倒退读取视为未经过时间，而不是巨大的跳变。

``TIMER_CORE_COUNTER_NONATOMIC``
   ``timer_driver_cycle_get()`` 不是一次原子读取，而是由 ISR 也会访问的状态合成的值。此时核心会在时钟锁保护下读取它。

``TIMER_CORE_HAVE_CYCLE_GET_32``、``TIMER_CORE_HAVE_CYCLE_GET_64``
   驱动程序自行定义对应入口，核心不再定义。适用于需要缩放的计数器。包含头文件后可使用 ``timer_core_cycle_get()``，获取计数器自身计数域内的完整位宽计数值，作为缩放的输入。

   设置 ``TIMER_CORE_CYCLES_PER_SEC`` 的驱动程序必须提供 32 位读取函数，因为内核不能直接读取使用自身频率的计数器原始值。此时核心也不会生成 64 位读取函数，因为它属于驱动程序刚声明的不同计数域。如果需要，也应自行提供。

``TIMER_CORE_ALARM_MAX_CYCLES``
   定时设置原语能够表示的最大值，仅表示这一限制。默认值为 ``TIMER_CORE_COUNTER_WIDTH`` 的完整计数范围，因为定时中断和计数器通常由同一硬件提供。如果定时范围由其他因素决定，例如比较或重装载寄存器比计数器更窄，或使用独立设备，则应设置此项。

   它表示硬件容量，不包含安全余量。核心根据 ``TIMER_CORE_COUNTER_WIDTH`` 自行计算安全余量：设置的定时时刻相对于上次通告，不会超过计数器范围的一半；若启用 ``TIMER_CORE_COUNTER_NONMONOTONIC``，则不超过四分之一。这样，即使通告延迟，所得差值仍可通过掩码正确解析。两个限制中较先达到的一个生效。

``TIMER_CORE_ALARM_MIN_CYCLES``
   重装载下限，单位为周期，仅适用于 ``TIMER_CORE_BACKEND_RELOAD``。默认为 1。

``TIMER_CORE_ALARM_LEAD_CYCLES``
   比较值必须领先计数器的周期数，以确保能捕获匹配，仅适用于 ``TIMER_CORE_BACKEND_COMPARE_EXACT``。默认为 1，表示只要写入比较器时计数器仍小于该值，就能触发。对于必须先将写操作传递到计数器时钟域、且会漏掉距离小于此值的匹配的硬件，应增大此值。

新的无节拍驱动程序应基于此头文件构建，而不是重新实现时钟节拍计数。头文件中完整记录了每个宏和原语。
