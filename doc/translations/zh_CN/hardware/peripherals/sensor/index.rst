.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _sensor:

传感器
######

传感器驱动 API 提供统一的接口，用于读取和配置以具有实际意义的单位测量现实世界物理量的设备，并为其设置事件处理。

传感器种类繁多，既有采用固定比例系数、必须通过轮询读取的简单温度测量设备，也有接收多个传感器的读数，并自行推导出步数、存在检测、朝向等新传感器数据的复杂设备。

支持如此广泛的设备是一项艰巨的任务，传感器 API 力求为这些设备提供统一的接口。


.. _sensor-using:

使用传感器
**********

在应用中使用传感器时，了解一些 API 和术语会有所帮助。Zephyr 中的传感器由 :ref:`sensor-channel`、:ref:`sensor-attribute` 和 :ref:`sensor-trigger` 组成。属性和触发器可能针对特定设备或通道。

.. note::
   目前，可以通过两种方式使用传感器 API 获取传感器采样数据：一种是稳定且已长期使用的 API :ref:`sensor-fetch-and-get`，另一种是较新但正在迅速趋于稳定的 API :ref:`sensor-read-and-decode`。预计在不久的将来，:ref:`sensor-fetch-and-get` 将被弃用，转而采用 :ref:`sensor-read-and-decode`。:ref:`sensor-fetch-and-get` 和 :ref:`sensor-read-and-decode` 对触发器的处理方式完全不同，各自的章节中说明了这些差异。

.. toctree::
   :maxdepth: 1

   attributes.rst
   channels.rst
   triggers.rst
   power_management.rst
   device_tree.rst
   fetch_and_get.rst
   read_and_decode.rst


.. _sensor-implementing:

实现传感器驱动
**************

.. note::
   实现传感器 API 的驱动端需要了解这些 API 的使用方式。请先通读 :ref:`sensor-using`！

实现属性
========

* 应以阻塞方式实现属性设置。
* 如果设备支持，应提供获取和设置通道比例系数的能力。
* 如果设备支持，应提供获取和设置通道采样率的能力。

实现采集与获取
==============

* 应将 :c:type:`sensor_sample_fetch_t` 实现为阻塞调用，将指定通道（或所有传感器通道）的采样数据暂存为驱动实例数据。
* 应实现 :c:type:`sensor_channel_get_t`，使其返回暂存的传感器读数，且不产生修改驱动状态的副作用。
* 实现 :c:type:`sensor_trigger_set_t` 时，应存储 :c:struct:`sensor_trigger` 的地址，而不是复制其内容。这样便可使用 :c:macro:`CONTAINER_OF` 获取触发器回调的上下文。

实现读取与解码
==============

* 必须将 :c:type:`sensor_submit_t` 实现为非阻塞调用。
* 实现 :c:type:`sensor_submit_t` 时，应尽可能使用 :ref:`rtio` 进行非阻塞总线传输。
* 如果总线不支持 :ref:`rtio`，可以使用工作队列实现 :c:type:`sensor_submit_t`。
* 实现 :c:type:`sensor_submit_t` 时，应检查 :c:struct:`rtio_sqe` 的类型是否为 :c:enum:`RTIO_SQE_RX` （读取请求）。
* 实现 :c:type:`sensor_submit_t` 时，应检查是否支持所有请求的通道；如果不支持，则返回错误。
* 实现 :c:type:`sensor_submit_t` 时，应检查提供的缓冲区是否足够容纳所请求通道的数据。
* 实现 :c:type:`sensor_submit_t` 时，除少数例外情况外，应将数据直接读入提供的缓冲区，避免任何形式的复制。
* 必须使用无状态的纯函数实现 :c:struct:`sensor_decoder_api`。将原始传感器读数转换为以国际单位制（SI）单位表示的定点数值所需的全部状态，都必须包含在提供的缓冲区中。
* 必须实现 :c:type:`sensor_get_decoder_t`，使其返回对应设备类型的 :c:struct:`sensor_decoder_api`。

.. _sensor-api-reference:

API 参考
********

.. doxygengroup:: sensor_interface
.. doxygengroup:: sensor_emulator_backend
