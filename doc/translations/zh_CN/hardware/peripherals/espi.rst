.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _espi_api:

增强型串行外设接口（eSPI）总线
##############################

概述
****

eSPI（增强型串行外设接口）是一种基于 SPI 的串行总线。它同样采用四线接口（接收、发送、时钟和目标选择），并支持三种配置：单 IO、双 IO 和四 IO。

其技术改进包括更低的信号电压电平（从 3.3V 降至 1.8V）、更少的引脚数量，以及提高一倍的频率（从 33MHz 提升至 66MHz）。凭借这些改进，eSPI 被用于替代 LPC（低引脚数）接口、SPI、SMBus 和边带信号。

更多详细信息请参见 `eSPI interface specification`_ 。


API 参考
********

.. doxygengroup:: espi_interface

.. _eSPI interface specification:
    https://downloadmirror.intel.com/27055/327432%20espi_base_specification%20R1-5.pdf
