.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _sensor-fetch-and-get:

采集与获取
##########

用于读取传感器数据和处理触发器的稳定且长期使用的 API 如下：

* :c:func:`sensor_sample_fetch`
* :c:func:`sensor_sample_fetch_chan`
* :c:func:`sensor_channel_get`
* :c:func:`sensor_trigger_set`

这些函数协同工作。采集 API 会阻塞调用上下文（必须是线程），直到请求的 :c:enum:`sensor_channel` （或所有通道）的数据已采集并存储到驱动实例的私有数据中。

随后，可针对每种通道类型调用 :c:func:`sensor_channel_get` ，以 :c:struct:`sensor_value` 的形式获取最近一次采集的通道数据。

.. warning::
   需要注意，在没有锁定机制的情况下，从多个上下文调用采集和获取函数的行为是未定义的，而且大多数传感器驱动不会在内部确保在这些调用期间或调用之间对设备的独占访问。

轮询
****

通过采集和获取函数，软件线程可以以轮询方式读取传感器数据。


.. literalinclude:: ../../../../samples/sensor/magn_polling/src/main.c
   :language: c

触发器
******

使用稳定 API 中的触发器，需要通过设备专用的 Kconfig 选项启用触发器。这些 Kconfig 选项通常允许选择触发器运行的上下文。随后，应用需要使用 :c:func:`sensor_trigger_set` ，为要监听的特定触发器（事件）注册一个函数签名与 :c:type:`sensor_trigger_handler_t` 匹配的回调函数。

.. note::
   不能从用户模式线程设置触发器，且回调函数不会在用户模式上下文中运行。

每个驱动通常提供两种运行触发器处理函数的方式：使用系统工作队列线程（ :ref:`workqueues_v2` ）或专用线程。BMI160 驱动就是一个很好的例子，它提供了用于选择触发器模式的 Kconfig 选项。请参阅 :kconfig:option:`CONFIG_BMI160_TRIGGER_NONE` 、 :kconfig:option:`CONFIG_BMI160_TRIGGER_GLOBAL_THREAD` （工作队列）和 :kconfig:option:`CONFIG_BMI160_TRIGGER_OWN_THREAD` （专用线程）。

与系统工作队列相比，使用驱动专用线程有以下几个值得注意的特点。

* 驱动专用线程具有专用栈（RAM），该栈仅供对应的单个触发器处理函数使用。
* 驱动专用线程通常 *确实* 具有独立的优先级，因此可以设置触发器处理相对于其他线程的优先级。
* 使用驱动专用线程时，即使驱动处理触发器需要一定时间，也不会造成队头阻塞。

.. note::
   在所有情况下，从实际中断发生到回调函数运行之间，很可能存在不固定的延迟。使用工作队列（GLOBAL_THREAD）时，工作队列本身就可能是不固定延迟的来源！

.. literalinclude:: tap_count.c
   :language: c
