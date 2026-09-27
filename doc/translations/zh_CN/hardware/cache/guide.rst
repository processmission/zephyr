.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _cache_guide:

缓存基础
########

本节介绍缓存一致性的基础知识，以及用户需要显式处理缓存的情形。有关 Zephyr 缓存工具的更多详细信息，请参阅 :ref:`cache_config` 了解 Zephyr Kconfig 选项，或参阅 :ref:`cache_api` 查看 API 参考。本节主要关注数据缓存，不过支持缓存的系统通常也有指令缓存。

.. note::

  此处的信息假定已启用架构特定的 MPU 支持。详情请参阅相应架构的文档。

.. note::

  虽然 SMP 核心之间共享的数据可能涉及缓存一致性问题，但 Zephyr 通常会确保多个核心看到的内存状态一致。大多数应用仅在与 DMA 控制器或运行不同操作系统映像的外部 CPU 等外部硬件交互时，才需要使用缓存 API。有关 SMP 核心之间缓存一致性的更多信息，请参阅 :kconfig:option:`CONFIG_KERNEL_COHERENCE` 。

处理处理器核心与其他总线主设备之间共享的内存时，需要考虑缓存一致性。通常，处理器缓存会尽可能靠近各个处理器核心，以最大限度地提升性能。因此，当 DMA 引擎向内存写入数据或从内存读取数据时，处理器缓存与内存中的数据可能不一致，导致数据看起来已损坏。如果使用 DMA 传输数据时，处理器看到的数据与预期不符，问题可能出在缓存一致性上。

有多种方法可以确保处理器核心与外设看到的数据一致。最简单的方法是直接禁用缓存，但这违背了使用硬件缓存的初衷，并会显著降低性能。许多架构提供了仅对部分内存禁用缓存的方法。当缓存一致性比性能更重要时，例如通过 DMA 进行 SPI 传输时，这种方法会很有用。最后，还可以在运行时对指定内存区域的缓存执行刷新或无效化操作。

全局禁用数据缓存
----------------

如上所述，全局禁用数据缓存会显著影响性能，但有助于调试。

要求：

* :kconfig:option:`CONFIG_DCACHE` ：在 Zephyr 中启用 DCACHE 控制。

* :kconfig:option:`CONFIG_CACHE_MANAGEMENT` ：启用缓存 API。

* 调用 :c:func:`sys_cache_data_disable()` 可全局禁用数据缓存。

禁用内存区域的缓存
------------------

如果应用对不缓存内存的访问性能要求不高，那么仅对部分内存禁用缓存可以在性能方面取得较好的折中。如果应用需要许多小于缓存行且彼此无关的小缓冲区，这是一种合适的选择。

要求：

* :kconfig:option:`CONFIG_DCACHE` ：在 Zephyr 中启用 DCACHE 控制。

* :kconfig:option:`CONFIG_MEM_ATTR` ：启用 ``mem-attr`` 库，用于处理 Devicetree 中的内存属性。

* 按照 :ref:`mem_mgmt_api` 中的说明，为 Devicetree 添加标注。

如果已启用 MPU 驱动，它会在内核初始化期间根据指定的内存属性配置相应区域。使用专门的不缓存内存区域时，需要指示链接器将缓冲区放入该区域。可以使用 ``Z_GENERIC_SECTION`` 显式指定内存区域来实现：

.. code-block:: c

  /* SRAM4 marked as uncached in device tree */
  uint8_t buffer[BUF_SIZE] Z_GENERIC_SECTION("SRAM4");

.. note::

  配置具有独立缓存规则的单独内存区域需要使用一个 MPU 区域，而在某些架构上，MPU 区域可能是有限的资源。其他内存保护功能也可能需要 MPU 区域，例如 :ref:`用户空间 <mpu_userspace>` 、 :ref:`栈保护 <mpu_stack_objects>` 或 :ref:`内存域<memory_domain>` 。

按变量自动禁用缓存
------------------

Zephyr 可以自动在内存中定义一个不缓存区域，并使用 ``__nocache`` 将变量分配到该区域。带有此属性的所有变量都会放入内存中一个特殊的 ``nocache`` 链接器区域。MPU 驱动会在初始化期间将该区域配置为不缓存。与显式声明某个内存区域不缓存相比，这种方法更简单，但对这些变量存放位置的控制较少，因为链接器可能将该区域分配在 RAM 中的任意位置。

要求：

* :kconfig:option:`CONFIG_DCACHE` ：在 Zephyr 中启用 DCACHE 控制。

* :kconfig:option:`CONFIG_NOCACHE_MEMORY` ：启用 ``nocache`` 链接器区域的分配，并将其配置为不缓存。

* 在任何不缓存的缓冲区定义末尾添加 ``__nocache`` 属性：

.. code-block:: c

  uint8_t buffer[BUF_SIZE] __nocache;

.. note::

  有关 MPU 区域可能存在的限制，请参阅上面的说明。尽管 ``nocache`` 区域由 Zephyr 自动创建，而非由用户显式定义，但它仍然是一个独立的 MPU 区域。

运行时缓存控制
--------------

性能最佳但也最复杂的方法是在运行时控制数据缓存。在这种情况下，最相关的两种缓存操作是 **刷新** 和 **无效化** 。这两种操作都以可缓存内存的最小单位——缓存行为操作对象。数据缓存行的大小通常为 16 到 128 字节，请参阅 :kconfig:option:`CONFIG_DCACHE_LINE_SIZE` 。缓存行大小通常由硬件固定，无法配置，但 Zephyr 需要知道缓存行大小，才能正确、高效地管理缓存。如果相关缓冲区小于数据缓存行，将其放入不缓存区域可能更高效，因为无效化操作可能会破坏位于同一缓存行中的无关数据。

刷新缓存是指将指定区域内所有已修改的缓存行写回共享内存。在处理器写入缓冲区之后、远端总线主设备读取该区域之前，应刷新该缓冲区对应的缓存。

.. note::

  某些架构支持一种称为 **直写** 的缓存配置。在这种配置下，处理器核心写入的数据会直接传递到共享内存。虽然这解决了 CPU 写入时的缓存一致性问题，但也会增加主存访问流量，可能导致性能下降。

缓存无效化的工作方式类似，但方向相反。它将指定区域内的缓存行标记为失效，确保处理器下次读取该区域时，会从主存重新加载相应缓存行。读取外设已写入的缓冲区之前，应先将该缓冲区的数据缓存无效化。

在某些情况下，同一个缓冲区可能被重复用于 DMA 读取和 DMA 写入等操作。此时，可以先刷新该缓冲区对应的缓存，再将其无效化，以确保处理器下次读取该缓冲区时会重新加载缓存。

要求：

* :kconfig:option:`CONFIG_DCACHE` ：在 Zephyr 中启用 DCACHE 控制。

* :kconfig:option:`CONFIG_CACHE_MANAGEMENT` ：启用缓存 API。

* 调用 :c:func:`sys_cache_data_flush_range()` 可刷新某个内存区域的缓存。

* 调用 :c:func:`sys_cache_data_invd_range()` 使指定内存区域的缓存失效。

* 调用 :c:func:`sys_cache_data_flush_and_invd_range()` 将缓存数据写回内存并使缓存失效。

对齐
----

如 :c:func:`sys_cache_data_invd_range()` 及相关函数的说明所述，缓冲区应按缓存行大小对齐。这可以通过使用 ``__aligned`` 来实现：

.. code-block:: c

  uint8_t buffer[BUF_SIZE] __aligned(CONFIG_DCACHE_LINE_SIZE);
