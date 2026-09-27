.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _posix_overview:

概述
####

可移植操作系统接口（POSIX）是由 `IEEE Computer Society`_ 制定的一系列标准，用于维护操作系统之间的兼容性。Zephyr 实现了由 `IEEE 1003.1-2017`_ （也称为 POSIX-1.2017）规定的标准 POSIX API 的一个子集。

..  figure:: posix.svg
    :align: center
    :alt: Zephyr 中的 POSIX 支持

    Zephyr 中的 POSIX 支持

.. note::
    本页不介绍 Zephyr 的 :ref:`POSIX 架构 <Posix arch>`，该架构用于将 Zephyr 作为原生应用运行在宿主操作系统之下，以实现原型设计、测试和诊断目的。

借助 Zephyr 提供的 POSIX 支持，现有的符合 POSIX 的应用可以移植到 Zephyr 内核上运行，从而利用 Zephyr 的特性与功能。此外，为符合 POSIX 而设计的库无需任何更改即可移植到基于 Zephyr 内核的应用中。

POSIX API 是一种日益流行的操作系统抽象层（OSAL），适用于 IoT 和嵌入式应用，Zephyr、AWS:FreeRTOS、TI-RTOS 和 NuttX 中都能看到这一点。

在 Zephyr 中支持 POSIX 的好处包括：

- 为非嵌入式程序员（尤其是来自 Linux 的程序员）提供熟悉的 API
- 支持复用（可移植性）基于 POSIX API 的现有库
- 提供适用于小型（MCU）嵌入式系统的高效 API 子集

.. _posix_subprofiles:

POSIX 子配置
============

虽然 Zephyr 支持运行多个 :ref:`线程 <threads_v2>` （可能处于 :ref:`SMP <smp_arch>` 配置中），并支持 :ref:`虚拟内存与 MMU <memory_management_api>`，但 Zephyr 的代码和数据通常共享一个公共地址空间，该地址空间被划分为多个独立的 :ref:`内存域 <memory_domain>`。Zephyr 内核可执行代码与应用可执行代码通常编译到同一个二进制产物中。从这个角度来看，Zephyr 应用可以视为在单个进程的上下文中运行。

虽然多用途操作系统（OS）提供完整的 POSIX 符合性，但像 Zephyr 这样的实时操作系统（RTOS）通常面向固定用途，硬件资源有限，用户交互也较少。在这类系统中，完整的 POSIX 符合性可能既不切实际，也没有必要。

因此，POSIX 在 `IEEE 1003.13-2003`_ （也称为 POSIX.13-2003）中定义了以下 :ref:`应用环境配置文件（AEP） <posix_aep>`。每个 AEP 都会在必需的 :ref:`POSIX 系统接口 <posix_system_interfaces>` 基础上逐步增加更多特性。

..  figure:: aep.svg
    :align: center
    :scale: 150%
    :alt: POSIX Application Environment Profiles (AEP)

    POSIX 应用环境配置文件（AEP）

* 最小实时系统配置文件（:ref:`PSE51 <posix_aep_pse51>`）
* 实时控制器系统配置文件（:ref:`PSE52 <posix_aep_pse52>`）
* 专用实时系统配置文件（:ref:`PSE53 <posix_aep_pse53>`）
* 多用途实时系统（PSE54）

POSIX.13-2003 AEP 于 2003 年通过“功能单元”正式确定，但该规范现已失效（仅供参考）。尽管如此，其意图仍通过 :ref:`选项 <posix_options>` 和 :ref:`选项组 <posix_option_groups>` 体现在 POSIX-1.2017 中。

更多信息请参阅 `IEEE 1003.1-2017, Section E, Subprofiling Considerations`_。

.. _posix_apps:

Zephyr 中的 POSIX 应用
======================

Zephyr 中的 POSIX 应用与 :ref:`任何其他应用 <application>` 一样构建，因此需要常见的 :file:`prj.conf`、:file:`CMakeLists.txt` 和源代码。例如，下面的应用使用了 ``nanosleep()`` 和 ``perror()`` 这两个 POSIX 函数。

.. code-block:: cfg
   :caption: Zephyr 中一个简单 POSIX 应用的 `prj.conf`

    CONFIG_POSIX_API=y

.. code-block:: c
   :caption: 一个使用 Zephyr POSIX API 的简单应用

    #include <stddef.h>
    #include <stdio.h>
    #include <time.h>

    void megasleep(size_t megaseconds)
    {
        struct timespec ts = {
            .tv_sec = megaseconds * 1000000,
            .tv_nsec = 0,
        };

        printf("See you in a while!\n");
        if (nanosleep(&ts, NULL) == -1) {
            perror("nanosleep");
        }
    }

    int main()
    {
        megasleep(42);
        return 0;
    }

有关 POSIX 应用的更多示例，请参阅 :zephyr:code-sample-category:`POSIX 示例应用 <posix>`。

.. _posix_config:

配置
====

与 Zephyr 中的大多数特性一样，POSIX 特性 :ref:`高度可配置 <zephyr_intro_configurability>`，但默认处于禁用状态。用户必须通过 :ref:`Kconfig <kconfig>` 选择显式启用 POSIX 选项。

子配置
++++++

启用下面某个 Kconfig 选项，即可快速配置预定义的 :ref:`POSIX 子配置 <posix_subprofiles>`。

* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_BASE` （:ref:`基础 <posix_system_interfaces_required>`）
* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_PSE51` （:ref:`PSE51 <posix_aep_pse51>`）
* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_PSE52` （:ref:`PSE52 <posix_aep_pse52>`）
* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_PSE53` （:ref:`PSE53 <posix_aep_pse53>`）

可根据需要通过 Kconfig 启用其他 POSIX :ref:`选项和选项组 <posix_option_groups>` （例如 ``CONFIG_POSIX_C_LIB_EXT=y``）。进一步的微调可通过 :ref:`其他 POSIX 相关的 Kconfig 选项 <posix_kconfig_options>` 完成。

今后应把子配置、选项和选项组视为在 Zephyr 中配置 POSIX 的首选方式。

旧版
++++

历史上，Zephyr 使用 :kconfig:option:`CONFIG_POSIX_API` 来配置一组 POSIX 特性，这组特性负担过重且规模一直在增长。

* :kconfig:option:`CONFIG_POSIX_API`

该选项现已冻结，可认为它等同于以下选项：

* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_PSE51`
* :kconfig:option:`CONFIG_POSIX_FD_MGMT`
* :kconfig:option:`CONFIG_POSIX_MESSAGE_PASSING`
* :kconfig:option:`CONFIG_POSIX_NETWORKING`

不过，:kconfig:option:`CONFIG_POSIX_API` 应被视为旧版选项，不应在新 Zephyr 应用中使用。

.. _IEEE: https://www.ieee.org/
.. _IEEE Computer Society: https://www.computer.org/
.. _IEEE 1003.1-2017: https://standards.ieee.org/ieee/1003.1/7101/
.. _IEEE 1003.13-2003: https://standards.ieee.org/ieee/1003.13/3322/
.. _IEEE 1003.1-2017, Section E, Subprofiling Considerations:
    https://pubs.opengroup.org/onlinepubs/9699919799/xrat/V4_subprofiles.html
