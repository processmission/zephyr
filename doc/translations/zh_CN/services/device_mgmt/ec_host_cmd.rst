.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ec_host_cmd_backend_api:

EC 主机命令
###########

概述
****
主机命令协议定义了主机（或应用处理器）与目标嵌入式控制器（EC）通信的接口。EC 主机命令子系统实现了该协议的目标端，负责对主机发送的命令生成响应。主机命令协议接口支持多个版本，但此子系统实现仅支持协议版本 3。

架构
****
主机命令子系统包含以下几个组件：

* 后端
* 通用处理程序
* 命令处理程序

后端是外设驱动与通用处理程序之间的一层。它负责通过所选外设发送和接收命令。

通用处理程序会验证来自后端的数据，例如检查大小、校验和等。如果命令有效，并且用户为收到的命令 id 提供了处理程序，则会调用命令处理程序。

.. image:: ec_host_cmd.png
   :align: center

SHI（串行主机接口）与此不同，因为它仅用于与主机通信。SHI 本身没有 API，因此后端层和外设驱动层合并为一个后端层。

.. image:: ec_host_cmd_shi.png
   :align: center

另一种情况是 SPI。遗憾的是，当前 SPI API 无法用于处理主机命令通信。主要问题是主机发送的命令大小未知（SPI 事务发送/接收特定数量的字节），以及需要持续发送状态字节（SPI 模块按事务启用和禁用）。这迫使在某个后端内实现 SPI 驱动，就像 SHI 那样。这意味着必须为每个芯片系列实现一个 SPI 后端。不过，一旦 SPI API 扩展以满足主机命令需求，这种情况在未来可能会改变。请查看 `讨论 <https://github.com/zephyrproject-rtos/zephyr/issues/56091>`_。

该方法要求以特殊方式配置 SPI dts 节点。SPI 节点的主 compatible 字符串已改为使用主机命令版的 SPI 驱动。其余属性应按常规方式配置。以下是 STM32 的 SPI 节点示例：

.. code-block:: devicetree

   &spi1 {
           /* Change the compatible string to use the Host Command version of the
            * STM32 SPI driver
            */
           compatible = "st,stm32-spi-host-cmd";
           status = "okay";

           dmas = <&dma2 3 3 0x38440 0x03>,
                <&dma2 0 3 0x38480 0x03>;
           dma-names = "tx", "rx";
           /* This field is used to point at our CS pin */
           cs-gpios = <&gpioa 4 (GPIO_ACTIVE_LOW | GPIO_PULL_UP)>;
   };

STM32 SPI 主机命令后端驱动支持 :dtcompatible:`st,stm32h7-spi` 和 :dtcompatible:`st,stm32-spi-fifo` 变体实现。要启用这些变体，请追加相应的 compatible 字符串。例如，要启用 FIFO 支持以及 STM32H7 SoC 支持，请按所示修改 compatible 字符串。

.. code-block:: devicetree

   &spi1 {
       compatible = "st,stm32h7-spi", "st,stm32-spi-fifo", "st,stm32-spi-host-cmd";
       ...
   };

运行 Zephyr 的芯片是 SPI 从设备，``cs-gpios`` 属性用于指向我们的 CS 引脚。对于 SPI，需要设置后端 chosen 节点 ``zephyr,host-cmd-spi-backend``。

支持的后端和外设驱动：

* 模拟器
* SHI - ITE 和 NPCX
* eSPI - 任何支持 :kconfig:option:`CONFIG_ESPI_PERIPHERAL_EC_HOST_CMD` 和 :kconfig:option:`CONFIG_ESPI_PERIPHERAL_CUSTOM_OPCODE` 的 eSPI 从设备驱动
* UART - 任何支持异步 API 的 UART 驱动
* SPI - STM32

初始化
******

如果应用程序配置了以下后端 chosen 节点之一，并且设置了 :kconfig:option:`CONFIG_EC_HOST_CMD_INITIALIZE_AT_BOOT`，则相应的后端会通过调用 :c:func:`ec_host_cmd_init` 来初始化主机命令子系统：

* ``zephyr,host-cmd-espi-backend``
* ``zephyr,host-cmd-shi-backend``
* ``zephyr,host-cmd-uart-backend``
* ``zephyr,host-cmd-spi-backend``

如果未配置任何后端 chosen 节点，则应用程序必须直接调用 :c:func:`ec_host_cmd_init` 函数。当在运行时根据例如 GPIO 状态选择后端时，这种初始化方式很有用。

缓冲区
******

主机命令通信需要用于 rx 和 tx 的缓冲区。如果 rx 缓冲区的 :kconfig:option:`CONFIG_EC_HOST_CMD_HANDLER_RX_BUFFER_SIZE` > 0，并且 tx 缓冲区的 :kconfig:option:`CONFIG_EC_HOST_CMD_HANDLER_TX_BUFFER_SIZE` > 0，则这些缓冲区由通用处理程序提供。共享缓冲区对于使用多个后端的应用程序很有用。每个后端分别定义缓冲区会增加内存使用量。不过，某些缓冲区可以由外设驱动定义，例如 eSPI。应尽可能重用这些缓冲区。

日志记录
********

主机命令有一个用于记录正在进行通信的内嵌日志系统。日志级别有以下几种：

* :c:macro:`LOG_INF` 用于记录新命令的命令 id，而不记录成功响应。同一命令的重复项不会被记录
* :c:macro:`LOG_DBG` 记录每条命令，即使重复也会记录
* :c:macro:`LOG_DBG` + :kconfig:option:`CONFIG_EC_HOST_CMD_LOG_DBG_BUFFERS` 记录每条命令以及带数据缓冲区的响应

API 参考
********

.. doxygengroup:: ec_host_cmd_interface
