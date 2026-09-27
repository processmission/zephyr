.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _usb_device_stack_next:

USB 设备支持
############

概述
****

USB 设备支持由 USB 设备控制器（UDC）驱动（:ref:`udc_api`）和 USB 设备协议栈（:ref:`usbd_api`）组成。:ref:`udc_api` 为 USB 设备控制器提供通用且与厂商无关的接口；尽管各层之间存在明确的分离，但 :ref:`udc_api` 的目的只是为 Zephyr 的 USB 设备协议栈服务。

设备协议栈支持多个设备控制器，这意味着如果 SoC 具有多个控制器，它们可以同时使用。支持全速和高速设备控制器。它还支持在运行时向某个配置注册多个功能或类实例，或稍后更改配置。它内置对多个 USB 类的支持，并提供用于实现自定义 USB 功能的 API。

示例
====

* :zephyr:code-sample:`usb-hid-keyboard`

* :zephyr:code-sample:`uac2-explicit-feedback`

* :zephyr:code-sample:`uac2-implicit-feedback`

* :zephyr:code-sample:`uvc`

* :zephyr:code-sample:`bluetooth_hci_usb`

* :zephyr:code-sample:`usb-cdc-acm`

* :zephyr:code-sample:`usb-cdc-acm-console`

* :zephyr:code-sample:`usb-mass`

* :zephyr:code-sample:`usb-hid-mouse`

* :zephyr:code-sample:`zperf` 要构建设备支持示例，请设置配置 overlay 文件 ``-DEXTRA_CONF_FILE=overlay-usbd.conf`` 和设备树 overlay 文件 ``-DDTC_OVERLAY_FILE=usbd_cdc_ecm.overlay``，可以直接设置，也可以通过 ``west`` 设置。

.. _usb_device_next_howto_configure:

如何配置和启用 USB 设备支持
***************************

对于 Zephyr 项目仓库中的 USB 设备支持示例，我们有一个用于实例化、配置和初始化的公共文件：:zephyr_file:`samples/subsys/usb/common/sample_usbd_init.c`。下面使用该文件中的代码片段作为示例。USB 示例中使用的、以 ``SAMPLE_USBD_`` 为前缀的 USB Samples Kconfig 选项具有 Zephyr 项目特定的默认值，且其作用范围仅限于项目示例。在以下示例中，你需要将这些 Kconfig 选项和其他默认值替换为适合你的应用或硬件的值。

USB 设备协议栈需要一个上下文结构来管理其属性和运行时数据。定义设备上下文的首选方式是使用 :c:macro:`USBD_DEVICE_DEFINE` 宏。这会创建一个具有给定名称的静态 :c:struct:`usbd_context` 变量。可以实例化任意数量的上下文。一个 USB 控制器设备可以分配给多个上下文，但同一时间只能初始化并使用一个上下文。应用不得直接访问或操作上下文属性。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc device instantiation start
   :end-before: doc device instantiation end

你的 USB 设备可能有制造商、产品和序列号字符串描述符。要实例化这些字符串描述符，应用应使用相应的 :c:macro:`USBD_DESC_MANUFACTURER_DEFINE`、:c:macro:`USBD_DESC_PRODUCT_DEFINE` 和 :c:macro:`USBD_DESC_SERIAL_NUMBER_DEFINE` 宏。字符串描述符还需要使用 :c:macro:`USBD_DESC_LANG_DEFINE` 宏实例化一次语言描述符。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc string instantiation start
   :end-before: doc string instantiation end

必须在运行时将字符串描述符添加到设备上下文，然后才能使用 :c:func:`usbd_add_descriptor` 初始化 USB 设备。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc add string descriptor start
   :end-before: doc add string descriptor end

USB 设备针对每种支持的速度至少需要一个配置实例。应用应使用 :c:macro:`USBD_CONFIGURATION_DEFINE` 实例化一个配置。之后，USB 设备功能会分配到配置中。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc configuration instantiation start
   :end-before: doc configuration instantiation end

在使用 :c:func:`usbd_add_configuration` 初始化 USB 设备之前，必须先在运行时将特定速度的每个配置实例添加到设备上下文。请注意 :c:enumerator:`USBD_SPEED_FS` 和 :c:enumerator:`USBD_SPEED_HS`。第一个全速或高速配置的 ``bConfigurationValue`` 为 1，后续配置依次递增。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc configuration register start
   :end-before: doc configuration register end


尽管我们已经做了很多工作，但这个 USB 设备还没有任何功能。一个设备可以具有多个配置，在不同速度下包含不同的功能集。可以使用 :c:func:`usbd_register_class` 在 USB 设备初始化之前向其注册功能或类。所需配置通过 :c:enumerator:`USBD_SPEED_FS` 或 :c:enumerator:`USBD_SPEED_HS` 以及配置编号来指定。对于简单情况，可以使用 :c:func:`usbd_register_all_classes` 注册所有可用实例。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc functions register start
   :end-before: doc functions register end

准备工作的最后一步是使用 :c:func:`usbd_init` 初始化设备。之后，设备配置便无法更改。可以使用 :c:func:`usbd_shutdown` 取消初始化设备，所有实例都可以重用，但必须重复之前的步骤。因此，可以先关闭设备、注册另一种类型的配置或功能，然后再次初始化。在 USB 控制器层面，:c:func:`usbd_init` 只执行检测 VBUS 变化所必需的操作。某些控制器类型只有在存在 VBUS 信号时才能执行下一步。

功能或类的实现可能需要自己特定的配置步骤，这些步骤应在初始化 USB 设备之前执行。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc device init start
   :end-before: doc device init end

启用 USB 设备的最后一步是调用 :c:func:`usbd_enable`；之后，如果 USB 设备已连接到 USB 主机控制器，主机就可以开始枚举该设备。应用可以使用 :c:func:`usbd_disable` 禁用 USB 设备。

.. literalinclude:: ../../../../../samples/subsys/usb/hid-keyboard/src/main.c
   :language: c
   :dedent:
   :start-after: doc device enable start
   :end-before: doc device enable end

USB 消息通知
============

应用可以使用 :c:func:`usbd_msg_register_cb` 注册回调，以接收来自 USB 设备支持子系统的消息通知。这些消息大多与通用设备状态变化有关，另有少数是来自 USB CDC ACM 实现的特定类型。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc device init-and-msg start
   :end-before: doc device init-and-msg end

辅助函数 :c:func:`usbd_msg_type_string()` 可用于将 :c:enumerator:`usbd_msg_type` 转换为便于日志记录的可读形式。

如果控制器支持 VBUS 状态变化检测，那么电池供电的应用可能只想在连接到主机时才启用 USB 设备。通用应用应使用 :c:func:`usbd_can_detect_vbus` 检查是否具备此能力。

.. literalinclude:: ../../../../../samples/subsys/usb/hid-keyboard/src/main.c
   :language: c
   :dedent:
   :start-after: doc device msg-cb start
   :end-before: doc device msg-cb end

内置功能
********

USB 设备协议栈具有内置 USB 功能。有些功能可以通过专用 API 直接在用户应用中使用，例如 HID 或音频类设备；另一些则使用通用的 Zephyr RTOS 驱动 API，例如 MSC 和 CDC 类实现。*标识字符串* 用于标识类或功能实例（``n``），并作为参数传递给 :c:func:`usbd_register_class`。

+-------------------------------------+---------------------------+---------------------------+
| 类或功能                            | 用户 API（如有）          | 标识字符串                |
+=====================================+===========================+===========================+
| USB Audio 2 类                      | :ref:`uac2_device`        | :samp:`uac2_{n}`          |
+-------------------------------------+---------------------------+---------------------------+
| USB CDC ACM 类                      | :ref:`uart_api`           | :samp:`cdc_acm_{n}`       |
+-------------------------------------+---------------------------+---------------------------+
| USB CDC ECM 类                      | 以太网设备                | :samp:`cdc_ecm_{n}`       |
+-------------------------------------+---------------------------+---------------------------+
| USB 大容量存储类（MSC）             | :ref:`usbd_msc_device`    | :samp:`msc_{n}`           |
+-------------------------------------+---------------------------+---------------------------+
| USB 人机接口设备（HID）             | :ref:`usbd_hid_device`    | :samp:`hid_{n}`           |
+-------------------------------------+---------------------------+---------------------------+
| 蓝牙 HCI USB 传输层                 | :ref:`bt_hci_raw`         | :samp:`bt_hci_{n}`        |
+-------------------------------------+---------------------------+---------------------------+
| USB 视频类（UVC）                   | 视频设备                  | :samp:`uvc_{n}`           |
+-------------------------------------+---------------------------+---------------------------+
