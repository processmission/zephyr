.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _cache_config:

缓存控制配置
############

本文概述了 Zephyr 的缓存接口以及与缓存控制器相关的 Kconfig 选项。API 参考资料请参阅 :ref:`cache_api` 。

Zephyr 提供了不同的 Kconfig 选项，用于控制缓存控制器的实现方式和控制方式。

* :kconfig:option:`CONFIG_CPU_HAS_DCACHE` / :kconfig:option:`CONFIG_CPU_HAS_ICACHE` ：当 CPU 确实支持数据缓存或指令缓存时，应在 SoC / 平台层选择这些隐藏选项。缓存控制器可以位于核心内部，也可以是提供了相应驱动的外部缓存控制器。

  这些选项用于表明硬件具备某项功能，无论是否计划在 Zephyr 中支持和使用缓存控制，都应设置这些选项。

* :kconfig:option:`CONFIG_DCACHE` / :kconfig:option:`CONFIG_ICACHE` ：当 Zephyr 中具备数据缓存或指令缓存支持且能正常工作时，必须选择这些选项。请注意，即使禁用这些选项，缓存仍可能处于启用状态，具体取决于硬件的默认设置。

  所有与缓存控制相关的代码路径都必须根据这些符号有条件地启用。设置相应符号后，即认为缓存已启用并正在使用。

  这些符号并不说明实际向用户提供了什么 API 接口。例如，使用数据缓存的平台可以启用 :kconfig:option:`CONFIG_DCACHE` 符号，并在平台专用代码中使用 HAL 导出的某个函数来启用和管理数据缓存。

* :kconfig:option:`CONFIG_CACHE_MANAGEMENT` ：当通过标准 API 向用户提供缓存操作时，必须选择此选项（请参阅 :ref:`cache_api` ）。

  启用此选项后，即假定所有缓存函数均已在架构代码或外部缓存控制器驱动中实现。

* :kconfig:option:`CONFIG_MEM_ATTR` ：此选项允许用户使用 :ref:`内存区域属性<mem_mgmt_api>` 指定一个固定的内存区域，内核初始化完成后，该区域的缓存将被禁用。

* :kconfig:option:`CONFIG_NOCACHE_MEMORY` ：此选项允许用户使用 ``__nocache`` 将单个全局变量指定为不缓存。这会指示链接器将所有带有此标记的变量放入内存中的特殊 ``nocache`` 区域，MPU 驱动会将该区域配置为不缓存。

* :kconfig:option:`CONFIG_ARCH_CACHE` / :kconfig:option:`CONFIG_EXTERNAL_CACHE` ：这两个选项是 :kconfig:option:`CACHE_TYPE` 的互斥选项，用于定义缓存操作是在架构层实现，还是通过具有相应驱动的外部缓存控制器实现。

  * :kconfig:option:`CONFIG_ARCH_CACHE` ：缓存 API 由架构代码实现

  * :kconfig:option:`CONFIG_EXTERNAL_CACHE` ：缓存 API 由支持外部缓存控制器的驱动实现。在这种情况下，驱动必须按惯例放在 :file:`drivers/cache/` 目录中

.. _cache_api:

缓存 API
********

.. doxygengroup:: cache_interface
