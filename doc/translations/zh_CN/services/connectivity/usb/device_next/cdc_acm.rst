.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _usbd_cdc_acm:

USB 设备 CDC ACM
################

USB 设备协议栈提供的 CDC ACM 功能仅实现抽象控制模型串行仿真（Abstract Control Model Serial Emulation）。顾名思义，其唯一用途是仿真串行线路。大多数现代操作系统都应开箱即用地支持它。

CDC ACM 功能在主机侧和设备侧都表现为串行接口，而用户或应用接口则是 :ref:`uart_api` 驱动 API。这允许已经使用 UART API 的应用直接使用 CDC ACM 功能提供的串行接口，而无需修改负责数据通信的代码。只需进行额外的配置和 USB 设备协议栈初始化。

CDC ACM UART 配置
=================

与真实的 UART 控制器一样，虚拟 CDC ACM UART 在设备树中描述。CDC ACM UART 的设备树 compatible 属性为 :dtcompatible:`zephyr,cdc-acm-uart`。

当启用 USB 设备支持且设备树源文件中存在兼容节点时，会自动选择 CDC ACM 支持。如有必要，可以通过 :kconfig:option:`CONFIG_USBD_CDC_ACM_CLASS` 显式禁用 CDC ACM 支持。可用的 CDC ACM 实例数量取决于 USB 设备控制器上支持的端点数量。每个 CDC ACM 实例需要三个端点：两个批量端点（一个 IN，一个 OUT）和一个 MaxPacketSize 为 16 的中断 IN 端点。CDC ACM 节点可以使用 ``label`` 属性来区分主机侧的不同接口。下面是一个设备树 overlay 文件示例。

.. code-block:: devicetree

        &zephyr_udc0 {
                cdc_acm_uart0: cdc_acm_uart0 {
                        compatible = "zephyr,cdc-acm-uart";
                        label = "CDC_ACM_0";
                };
        };

在应用使用 CDC ACM UART 之前，可能需要等待 DTR 信号。有关如何实现该功能，请参阅 :zephyr:code-sample:`usb-cdc-acm`。

.. note::
  要与主机通信，除了 UART 配置外，应用还必须启用 USB 设备协议栈；有关这一点，请参阅 :ref:`usb_device_next_howto_configure`，并仔细阅读下一章。对于从旧版协议栈迁移的用户和应用，这是唯一需要适配的部分。

.. _cdc_acm_uart_as_serial_backend:

将 CDC ACM UART 用作串行后端
============================

使用上面的示例以及 ``zephyr,console`` chosen 节点属性，可以将 CDC ACM UART 配置为控制台设备。

.. code-block:: devicetree

        / {
                chosen {
                        zephyr,console = &cdc_acm_uart0;
                };
        };

        &zephyr_udc0 {
                cdc_acm_uart0: cdc_acm_uart0 {
                        compatible = "zephyr,cdc-acm-uart";
                        label = "CDC_ACM_0";
                };
        };

与上面示例中将控制台配置为使用 CDC ACM UART 的方式相同，可以使用 ``zephyr,shell-uart`` chosen 节点属性将 shell 配置为使用 CDC ACM UART 作为串行后端。请参见示例 :zephyr:code-sample:`shell-module` 和 :ref:`chosen 节点文档 <devicetree-chosen-nodes>`。

由于用作串行后端的场景非常常见，并且 CDC ACM UART 在运行时无需任何配置，协议栈提供了一个辅助函数来执行 :ref:`usb_device_next_howto_configure` 中描述的步骤。该辅助函数由 :kconfig:option:`CONFIG_CDC_ACM_SERIAL_INITIALIZE_AT_BOOT` 启用，并使用单个 CDC ACM 实例初始化 USB 设备协议栈。示例 :zephyr:code-sample:`usb-cdc-acm-console` 演示了如何使用它。

:kconfig:option:`CONFIG_CDC_ACM_SERIAL_INITIALIZE_AT_BOOT` 也应由 :zephyr:board:`nrf52840dongle` 等开发板使用；这些开发板没有调试适配器，而是带有 USB 设备控制器，并希望将 CDC ACM UART 用作日志和 shell 的默认串行后端。由于任何开发板的配置都相同，因此提供了通用的 :zephyr_file:`设备树文件 <boards/common/usb/cdc_acm_serial.dtsi>` 和 :zephyr_file:`Kconfig 文件 <boards/common/usb/Kconfig.cdc_acm_serial.defconfig>`，必须将其包含在开发板的设备树和 Kconfig.defconfig 文件中。

在应用中使用 CDC ACM UART
=========================

CDC ACM 实现了虚拟 UART 控制器，并提供中断驱动 UART API 和轮询 UART API。尚不支持 ASYNC API。如果应用希望通过 CDC ACM UART 通信，首选方式是使用中断驱动 UART API。理解 API 文档至关重要，下面仍给出一些说明。

中断驱动 UART API
-----------------

在内部，CDC ACM UART 实现使用两个环形缓冲区。它们接管了 :ref:`uart_interrupt_api` 中 TX/RX FIFO（TX/RX 缓冲区）的功能。

如 :ref:`uart_interrupt_api` 中所述，函数 :c:func:`uart_irq_update()`、:c:func:`uart_irq_is_pending`、:c:func:`uart_irq_rx_ready()`、:c:func:`uart_irq_tx_ready()`、:c:func:`uart_fifo_read()` 和 :c:func:`uart_fifo_fill()` 应从中断处理程序中调用，参见 :c:func:`uart_irq_callback_user_data_set()`。为防止未定义行为，这些函数的实现会检查调用上下文，如果不是中断处理程序则会失败。

此外，如 UART API 中所述，:c:func:`uart_irq_is_pending`、:c:func:`uart_irq_rx_ready()` 和 :c:func:`uart_irq_tx_ready()` 只能在调用 :c:func:`uart_irq_update()` 之后调用。

简而言之，应用的中断处理程序应类似于：

.. code-block:: c

        static void interrupt_handler(const struct device *dev, void *user_data)
        {
                while (true) {
                        uart_irq_update(dev);

                        if (uart_irq_is_pending(dev) <= 0) {
                                break;
                        }

                        if (uart_irq_rx_ready(dev)) {
                                int len;
                                int n;

                                /* ... */
                                n = uart_fifo_read(dev, buffer, len);
                                /* ... */
                        }

                        if (uart_irq_tx_ready(dev)) {
                                int len;
                                int n;

                                /* ... */
                                n = uart_fifo_fill(dev, buffer, len);
                          /* ... */
                        }
                }
        }

所有这些函数都不直接依赖 USB 设备的状态。填充 TX FIFO 并不意味着数据正在发送到主机，成功读取 RX FIFO 也不意味着设备仍连接到主机。如果 TX FIFO 中有空间且 TX 中断已启用，:c:func:`uart_irq_tx_ready()` 将成功返回。如果 RX FIFO 中有数据且 RX 中断已启用，:c:func:`uart_irq_rx_ready()` 将成功返回。函数 :c:func:`uart_irq_tx_complete()` 尚未实现。

轮询 UART API
-------------

CDC ACM 轮询输出实现遵循 :ref:`uart_polling_api`，仅当启用了 hw-flow-control 属性且从非 ISR 上下文调用时，才会在 TX FIFO 已满时阻塞。
