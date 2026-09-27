.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _timeutil_api:

时间实用工具
############

概述
****

Zephyr 中的 :ref:`kernel_timing_uptime` 基于时钟节拍计数器。在默认启用 :kconfig:option:`CONFIG_TICKLESS_KERNEL` 时，该计数器从系统启动瞬间的零值开始，以标称恒定速率递增。POSIX 中与其类似的是 ``CLOCK_MONOTONIC``，或 Linux 中的 ``CLOCK_MONOTONIC_RAW``。:c:func:`k_uptime_get()` 提供该时间的毫秒表示。

应用通常需要将 Zephyr 内部时间与日常生活中使用的外部时间尺度关联，例如本地时间或协调世界时。这些系统以不同方式解释时间，并可能因 `闰秒 <https://what-if.xkcd.com/26/>`__ 以及夏令时等本地时间偏移而出现不连续。

由于这些不连续性，以及周期计数器底层时钟存在的明显误差，根据 Zephyr 时钟估算的时间与“真实”民用时间尺度中的实际时间之间的偏移并非常量，可能在 Zephyr 应用运行期间发生很大变化。

时间实用工具 API 支持：

* :ref:`时间表示之间的转换 <timeutil_repr>`
* :ref:`时间尺度的同步和对齐 <timeutil_sync>`
* :ref:`时间表示的比较、加法和减法 <timeutil_manip>`

与这些功能相关的术语和概念，参见 :ref:`timeutil_concepts`。

时间实用工具 API
****************

.. _timeutil_repr:

表示形式转换
============

时间尺度中的时刻可以用多种方式表示，包括：

* 自某个纪元起经过的秒数。POSIX 中采用这种形式的时间表示包括 ``time_t`` 和 ``struct timespec``，通常将它们解释为“UNIX 时间”的表示（参见 :rfc:`8536#section-2`）。

* 相对于某个纪元，以年、月、日、时、分、秒表示的日历时间。POSIX 中采用这种形式的时间表示包括 ``struct tm``。

请记住，这些只是时间的表示形式，必须结合某个时间尺度解释，该尺度可以是本地时间、UTC，或其他连续或不连续的尺度。

标准 C 库函数提供了一些必要的转换。例如，可使用 `gmtime() <https://pubs.opengroup.org/onlinepubs/9699919799/functions/gmtime.html>`__，将表示自 POSIX 纪元起经过秒数的 ``time_t`` 转换为表示日历时间的 ``struct tm``。``struct timespec`` 等具有亚秒精度的时间戳也可使用该函数生成日历时间表示，并单独处理不足一秒的偏移量。

逆向转换尚未标准化：``mktime()`` 等 API 需要时区信息。Zephyr 通过 :c:func:`timeutil_timegm` 和 :c:func:`timeutil_timegm64` 提供此转换。

使用 :c:func:`timespec_to_timeout` 和 :c:func:`timespec_from_timeout`，可在 ``struct timespec`` 和 ``k_timeout_t`` 表示的时长之间转换。

.. code-block:: c

    k_timeout_t to;
    struct timespec ts;

    timespec_from_timeout(K_FOREVER, &ts);
    to = timespec_to_timeout(&ts); /* to == K_FOREVER */

    timespec_from_timeout(K_MSEC(100), &ts);
    to = timespec_to_timeout(&ts); /* to == K_MSEC(100) */

.. doxygengroup:: timeutil_repr_apis

.. _timeutil_sync:

时间尺度同步
============

影响时间尺度同步的因素有多个：

* 离散时刻表示值的变化速率。例如，Zephyr 运行时间以时钟节拍跟踪，节拍随标称频率为 :kconfig:option:`CONFIG_SYS_CLOCK_TICKS_PER_SEC` Hz 的事件递增；外部时间源则可能以整秒或小数秒（例如微秒）提供数据。
* 在某一时刻对齐两个时间尺度所需的绝对偏移量。
* 各尺度中可观测时刻之间的相对误差，为一致地对齐多个时刻，需要考虑这一误差。例如，由 GPS 每秒一个脉冲信号校准的参考时钟，比误差为 +/- 250 ppm 的 RC 振荡器驱动的 Zephyr 系统时钟准确得多。

时间尺度之间的同步或对齐通过以下多步过程完成：

* 时间尺度中的时刻用（无符号）64 位整数表示，假定该整数以固定标称速率递增。
* :c:struct:`timeutil_sync_config` 记录参考时间尺度／时间源（例如 TAI）和本地时间源（例如 :c:func:`k_uptime_ticks`）的标称速率。
* :c:struct:`timeutil_sync_instant` 记录同一时刻在参考时间尺度和本地时间尺度中的表示。
* :c:struct:`timeutil_sync_state` 提供存储空间，保存初始时刻、最近收到的第二次观测，以及用于补偿两个时间尺度实际速率相对误差的偏斜系数。
* :c:func:`timeutil_sync_ref_from_local()` 和 :c:func:`timeutil_sync_local_from_ref()` 在两个时间尺度之间转换时刻，并考虑偏斜系数；该系数可通过 :c:func:`timeutil_sync_estimate_skew`，根据状态结构体中保存的两个时刻估算。

.. doxygengroup:: timeutil_sync_apis

.. _timeutil_manip:

``timespec`` 操作
=================

可使用 :c:func:`timespec_is_valid` 检查 ``timespec`` 是否有效。

.. code-block:: c

    struct timespec ts = {
        .tv_sec = 0,
        .tv_nsec = -1, /* out of range! */
    };

    if (!timespec_is_valid(&ts)) {
        /* error-handing code */
    }

某些情况下，可使用 :c:func:`timespec_normalize` 将无效的 ``timespec`` 对象重新规范化。

.. code-block:: c

    if (!timespec_normalize(&ts)) {
        /* error-handling code */
    }

    /* ts should be normalized */
    __ASSERT(timespec_is_valid(&ts) == true, "expected normalized timespec");

可使用 :c:func:`timespec_equal` 比较两个 ``timespec`` 对象是否相等。

.. code-block:: c

    if (timespec_equal(then, now)) {
        /* time is up! */
    }

可使用 :c:func:`timespec_compare` 比较有效的 ``timespec`` 对象，并建立完整的大小顺序。

.. code-block:: c

    int cmp = timespec_compare(a, b);

    switch (cmp) {
    case 0:
        /* a == b */
        break;
    case -1:
        /* a < b */
        break;
    case +1:
        /* a > b */
        break;
    }

可分别使用 :c:func:`timespec_add`、:c:func:`timespec_sub` 和 :c:func:`timespec_negate`，对 ``timespec`` 对象执行加法、减法和取负操作。与 :c:func:`timespec_normalize` 一样，在不会导致溢出的情况下，这些函数会输出规范化的 ``timespec``。成功时返回 ``true``；如果会发生溢出，则返回 ``false``。

.. code-block:: c

    /* a += b */
    if (!timespec_add(&a, &b)) {
        /* overflow */
    }

    /* a -= b */
    if (!timespec_sub(&a, &b)) {
        /* overflow */
    }

    /* a = -a */
    if (!timespec_negate(&a)) {
        /* overflow */
    }

.. doxygengroup:: timeutil_timespec_apis


.. _timeutil_concepts:

Zephyr 时间支持的基础概念
*************************

以下术语来自 `ISO/TC 154/WG 5 N0038 <https://www.loc.gov/standards/datetime/iso-tc154-wg5_n0038_iso_wd_8601-1_2016-02-16.pdf>`__ （ISO/WD 8601-1）及其他来源：

* *时间轴* 将时间表示为按顺序排列的时刻序列。
* *时间尺度* 是相对于作为纪元的原点表示时刻的一种方式。
* 如果相继时刻的表示值从不减小，则该时间尺度是 *单调* （递增）的。
* 如果表示值没有突变，例如在相继时刻之间没有向前或向后跳变，则该时间尺度是 *连续* 的。
* `民用时间 <https://en.wikipedia.org/wiki/Civil_time>`__ 通常指由地方政府等民事主管机关依法定义的时间尺度，其目的往往是使当地午夜与太阳时对齐。

相关时间尺度
============

`国际原子时 <https://en.wikipedia.org/wiki/International_Atomic_Time>`__ （TAI）是一种基于以国际单位制秒计时的多个时钟的平均值建立的时间尺度。TAI 是单调且连续的时间尺度。

`世界时 <https://en.wikipedia.org/wiki/Universal_Time>`__ （UT）是一种基于地球自转的时间尺度。UT 是不连续的时间尺度，因为它需要不时进行调整（`闰秒 <https://en.wikipedia.org/wiki/Leap_second>`__），以保持与地球自转变化一致。因此，TAI 与 UT 之间的差值会随时间变化。UT 有多个变体，其中 `UTC <https://en.wikipedia.org/wiki/Coordinated_Universal_Time>`__ 最为常见。

UT 时间与地点无关。UT 是标准时间（或“本地时间”）的基础，后者表示某个特定地点的时间。在任意给定时刻，标准时间相对于 UT 都有固定偏移，主要受经度影响，但该偏移可能通过“夏令时”调整，使标准时间与当地太阳时对齐。从某种意义上说，本地时间比 UT“更加不连续”。

POSIX 时间（参见 :rfc:`8536#section-2`）是从 1970-01-01T00:00:00Z（即 UTC 1970 年的起点）这个“POSIX 纪元”开始计秒的时间尺度。UNIX 时间是 POSIX 时间的扩展，使用负值表示 POSIX 纪元之前的时间。这两种尺度都假定每天恰好有 86400 秒。通常，这些尺度中的时刻对应 UTC 尺度中的时间，因此继承了其不连续性。

与之对应的连续尺度是 UNIX 闰秒时间，即 UNIX 时间加上 POSIX 纪元之后引入的所有闰秒修正（该纪元时 TAI-UTC 为 8 秒）。

时间尺度差异示例
----------------

2016 年末引入了一个正闰秒，使 TAI 与 UTC 的差值从 36 秒增加到 37 秒。1999 年末没有引入闰秒，当时两者差值仅为 32 秒。下表列出了几个时间尺度中对应的民用日期时间和纪元计时值：

+----------------------+------------+---------------------+---------+----------------+
| UTC 日期             | UNIX 时间  | TAI 日期            | TAI-UTC | UNIX 闰秒时间  |
+======================+============+=====================+=========+================+
| 1970-01-01T00:00:00Z | 0          | 1970-01-01T00:00:08 | +8      | 0              |
+----------------------+------------+---------------------+---------+----------------+
| 1999-12-31T23:59:28Z | 946684768  | 2000-01-01T00:00:00 | +32     | 946684792      |
+----------------------+------------+---------------------+---------+----------------+
| 1999-12-31T23:59:59Z | 946684799  | 2000-01-01T00:00:31 | +32     | 946684823      |
+----------------------+------------+---------------------+---------+----------------+
| 2000-01-01T00:00:00Z | 946684800  | 2000-01-01T00:00:32 | +32     | 946684824      |
+----------------------+------------+---------------------+---------+----------------+
| 2016-12-31T23:59:59Z | 1483228799 | 2017-01-01T00:00:35 | +36     | 1483228827     |
+----------------------+------------+---------------------+---------+----------------+
| 2016-12-31T23:59:60Z | 未定义     | 2017-01-01T00:00:36 | +36     | 1483228828     |
+----------------------+------------+---------------------+---------+----------------+
| 2017-01-01T00:00:00Z | 1483228800 | 2017-01-01T00:00:37 | +37     | 1483228829     |
+----------------------+------------+---------------------+---------+----------------+

功能要求
--------

Zephyr 时钟节拍计数器没有闰秒或标准时间偏移的概念，是一种连续时间尺度。不过，其精度可能较低，漂移可达每小时三分钟（假定使用容差为 5% 的 RC 定时器）。

要支持 Zephyr 时间与日常使用的时间尺度之间的转换，需要两个阶段：

* 在连续但不精确的 Zephyr 时间尺度与精确、稳定的外部时间尺度之间转换；
* 在稳定时间尺度与可能不连续的民用时间尺度之间转换。

围绕 :c:func:`timeutil_sync_state_update()` 的 API 支持第一步，即连续时间尺度之间的转换。

第二步需要外部信息，包括闰秒安排和本地时间偏移变化。这部分最好由外部库提供，目前不属于时间实用工具 API 的范围。

选择外部时间源和时间尺度
------------------------

如果应用要求民用时间误差在数秒以内，可使用 UTC 作为稳定时间源。但是，如果外部时间源进行闰秒调整，就会出现不连续：以 1 Hz 采样得到的两次观测之间实际经过的时间，不等于其时间戳的数值差。

对于精确计时活动，采用独立于本地时间和太阳时调整的连续尺度，可显著简化处理。合适的连续尺度包括：

- GPS 时间：纪元为 1980-01-06T00:00:00Z，连续跟随 TAI，偏移为 TAI-GPS=19 秒。
- 蓝牙 Mesh 时间：纪元为 2000-01-01T00:00:00Z，连续跟随 TAI，偏移为 -32。
- UNIX 闰秒时间：纪元为 1970-01-01T00:00:00Z，连续跟随 TAI，偏移为 -8。

由于 C 和 Zephyr 库函数支持使用 UNIX 纪元在整数时间表示和日历时间表示之间转换，UNIX 闰秒时间是外部时间尺度的理想选择。

用于获取同步点的具体机制无关紧要：可以读取本地高精度 RTC 外设，通过 NTP 或 PTP 等协议在网络上交换数据包，或处理 GPS 接收器发来的 NMEA 消息，无论是否伴有每秒一个脉冲的信号。

``timespec`` 概念
=================

``struct timespec`` 最初来自 POSIX，自 C11 起成为 C 标准的一部分。``struct timespec`` 的定义如下所示。

.. code-block:: c

   struct timespec {
       time_t tv_sec;  /* seconds */
       long   tv_nsec; /* nanoseconds */
   };

``tv_nsec`` 字段的有效值范围仅为 ``[0, 999999999]``。``tv_sec`` 字段表示自纪元起经过的秒数。如果使用 ``struct timespec`` 表示时间差，``tv_sec`` 字段可以为负值。
