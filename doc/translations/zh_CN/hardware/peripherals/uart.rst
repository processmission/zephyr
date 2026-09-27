.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _uart_api:

通用异步收发器（UART）
######################

概述
****

Zephyr 提供三种访问 UART 外设的方式。根据所选方式，使用的 API 函数也有所不同，具体参见以下各节：

1. :ref:`uart_polling_api`
2. :ref:`uart_interrupt_api`
3. 使用 :ref:`dma_api` 的 :ref:`uart_async_api`

轮询是访问 UART 外设最基本的方式。读取函数 :c:func:`uart_poll_in` 是非阻塞函数，会返回一个字符；没有有效数据时，返回 ``-1`` 。写入函数 :c:func:`uart_poll_out` 是阻塞函数，线程会等待，直到给定字符发送完毕。

使用中断驱动 API 时，可能较慢的通信可以在后台进行，而线程可以继续执行其他任务。内核的 :ref:`kernel_data_passing_api` 功能可用于线程与 UART 驱动之间的通信。

异步 API 允许使用 DMA 在后台读写数据，完全无需中断 MCU。不过，其配置比其他方式更复杂。

.. warning::

   对于同一个硬件外设，不应同时使用中断驱动 API 和异步 API，因为这两种 API 都需要硬件中断才能正常工作。同时使用这两种 API 的回调会导致相互干扰。:kconfig:option:`CONFIG_UART_EXCLUSIVE_API_CALLBACKS` 默认启用，以确保同一时刻只有一种 API 的回调处于活动状态。


配置选项
********

最重要的是，Kconfig 选项决定了是否可以使用轮询 API（默认）、中断驱动 API 或异步 API。为尽量减少内存占用，请仅启用所需的功能。

相关配置选项：

* :kconfig:option:`CONFIG_SERIAL`
* :kconfig:option:`CONFIG_UART_INTERRUPT_DRIVEN`
* :kconfig:option:`CONFIG_UART_ASYNC_API`
* :kconfig:option:`CONFIG_UART_WIDE_DATA`
* :kconfig:option:`CONFIG_UART_USE_RUNTIME_CONFIGURE`
* :kconfig:option:`CONFIG_UART_LINE_CTRL`
* :kconfig:option:`CONFIG_UART_DRV_CMD`


API 参考
********

.. doxygengroup:: uart_interface


.. _uart_polling_api:

轮询 API
========

.. doxygengroup:: uart_polling


.. _uart_interrupt_api:

中断驱动 API
============

.. doxygengroup:: uart_interrupt


.. _uart_async_api:

异步 API
========

.. doxygengroup:: uart_async
