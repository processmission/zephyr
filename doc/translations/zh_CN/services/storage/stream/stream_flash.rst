.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _stream_flash:

流式 Flash
##########
Stream Flash 模块接收数据流中连续的片段（例如来自无线电数据包的片段），将它们聚合到用户提供的缓冲区中，当缓冲区填满（或数据流结束）时，将其写入原始 Flash 分区。该模块支持向客户端提供回读缓冲区，以用于验证持久化的流内容。

流写入操作的一个典型用例是在 DFU 操作中接收要使用的新固件映像。

之所以可能希望使用缓冲写入，而不是在数据一旦可用时直接写入，原因有几点。某些设备存在硬件限制，不允许 Flash 写入与其他操作（例如无线电 RX 和 TX）并行执行。此外，较少的写入操作会让应用看到的响应时间更快。

持久化流写入进度
****************
某些流写入操作（例如 DFU 操作）可能会运行很长时间。执行此类长时间运行的操作时，能够将流写入进度保存到持久存储会很有用，这样在意外中断后，操作可以从同一点恢复。

Stream Flash 模块提供 API，用于使用 :ref:`Settings <settings_api>` 模块将流写入进度加载、保存和清除到持久存储。该 API 可以通过 :kconfig:option:`CONFIG_STREAM_FLASH_PROGRESS` 启用。

API 参考
********

.. doxygengroup:: stream_flash
