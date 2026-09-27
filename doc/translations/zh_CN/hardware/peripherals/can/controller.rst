.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _can_api:

CAN 控制器
##########

.. contents::
    :local:
    :depth: 2

概述
****

控制器局域网（CAN）是一种双线串行总线，由博世 CAN 规范、博世可变数据速率 CAN 规范以及 ISO 11898-1:2003 标准定义。CAN 最为人熟知的是其在汽车领域的应用。不过，它也用于家庭和工业自动化以及其他产品。

.. warning::

   只有当总线处于空闲（隐性）状态且持续至少 11 个隐性位的时间时，CAN 控制器才能初始化。因此，必须确保 CAN RX 至少在一小段时间内保持高电平。回环模式也有这一要求。

ISO 11898-1:2003 定义的位时序如下所示：

.. image:: timing.svg
   :width: 40%
   :align: center
   :alt: CAN 时序

一个位分为四个段。

* Sync_Seg：节点在 Sync_Seg 的边沿进行同步。其长度始终为一个时间量子。

* Prop_Seg：用于补偿总线的信号传播延迟以及收发器和节点的其他延迟。

* Phase_Seg1 和 Phase_Seg2：定义采样点。在 Phase_Seg1 结束时对该位进行采样。

位速率根据一个时间量子的时长和上述各段的值计算。一个位的时长等于 Sync_Seg、Prop_Seg、Phase_Seg1 和 Phase_Seg2 之和乘以单个时间量子的时长。位速率是单个位时长的倒数。

在采样点对位进行采样。采样点位于 Phase_Seg1 和 PhaseSeg2 之间，因此是一个需要用户选择的参数。CiA 建议将采样点设在位时长的 87.5% 处。

再同步跳转宽度（SJW）定义了采样点可移动的时间量子数。需要再同步时，采样点会发生移动。

时序参数（SJW、位速率和采样点，或位速率、Prop_Seg、Phase_Seg1 和 Phase_Seg2）最初由 Devicetree 设置，可在运行时通过时序 API 修改。

CAN 使用所谓的标识符来标识帧，而不是使用地址来标识节点。该标识符的宽度可以是 11 位（标准帧或基本帧），对于扩展帧则为 29 位。Zephyr CAN API 支持同时使用标准标识符和扩展标识符。CAN 帧以一个显性的帧起始位开始，随后是标识符。这一阶段称为仲裁阶段。仲裁阶段允许发生写入冲突，并利用显性位覆盖隐性位的特性来解决冲突。节点监测总线，一旦发现自己发送的位被覆盖，就会中止发送。这实际上使数值较小的标识符具有比数值较大的标识符更高的优先级。

过滤器用于将特定节点关注的标识符加入允许列表。不匹配任何过滤器的标识符会被忽略。过滤器可以完全匹配标识符，也可以只匹配标识符的指定部分。这种方法称为掩码匹配。例如，对于标准标识符，若掩码的 11 个位均置位，或对于扩展标识符，若掩码的 29 个位均置位，则要求完全匹配。匹配标识符时，掩码中设为零的位会被忽略。大多数 CAN 控制器在硬件中实现的过滤器数量有限。为节省内存，Kconfig 中也限制了过滤器的数量。

传输过程中可能发生错误。如果节点检测到错误帧，就会使用错误标志帧覆盖当前帧的一部分。根据控制器的状态，错误标志帧可以是被动错误帧或主动错误帧。如果控制器处于错误主动状态，就会发送六个连续的显性位，这违反了位填充规则，所有节点都能检测到。发送方随后可立即重发该帧。

初始化后的节点可以处于以下状态之一：

* 错误主动
* 错误被动
* 总线关闭

初始化后，节点处于错误主动状态。在此状态下，节点可以发送主动错误帧、ACK 和过载帧。每个节点都有接收错误计数器和发送错误计数器。如果接收错误计数器或发送错误计数器中的任意一个超过 127，节点就会转入错误被动状态。在此状态下，节点不再允许发送主动错误帧。如果发送错误计数器进一步增加到 255，节点就会转入总线关闭状态。在此状态下，节点不允许向总线发送任何显性位。处于总线关闭状态的节点在接收到 128 次由 11 个连续隐性位组成的序列后，可以恢复。

有关 CAN 总线的更多信息，请参阅这篇 `维基百科 CAN 条目 <https://en.wikipedia.org/wiki/CAN_bus>`_ 。

Zephyr 支持以下 CAN 特性：

* 标准标识符和扩展标识符
* 支持掩码匹配的过滤器
* 回环模式和静默模式
* 远程请求

发送
****

以下代码片段展示了如何发送数据。


这个基础示例发送一个标准标识符为 0x123、包含八字节数据的 CAN 帧。如本示例所示，将 NULL 作为回调参数传入时，发送函数会阻塞，直到帧发送完成并得到至少一个其他节点的确认，或发生错误。超时仅在获取邮箱时生效。一旦分配了发送邮箱，就无法取消发送。

.. code-block:: C

  struct can_frame frame = {
          .flags = 0,
          .id = 0x123,
          .dlc = 8,
          .data = {1,2,3,4,5,6,7,8}
  };
  const struct device *const can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));
  int ret;

  ret = can_send(can_dev, &frame, K_MSEC(100), NULL, NULL);
  if (ret != 0) {
          LOG_ERR("Sending failed [%d]", ret);
  }


此示例展示了如何发送扩展标识符为 0x1234567、包含两个字节数据的帧。当消息发送完成或发生错误时，会调用所提供的回调函数。将超时参数设为 :c:macro:`K_FOREVER` 会使函数阻塞，直到为该帧分配了发送邮箱或发生错误。它不会像上面的示例那样一直阻塞到消息发送完成。

.. code-block:: C

  void tx_callback(const struct device *dev, int error, void *user_data)
  {
          char *sender = (char *)user_data;

          if (error != 0) {
                  LOG_ERR("Sending failed [%d]\nSender: %s\n", error, sender);
          }
  }

  int send_function(const struct device *can_dev)
  {
          struct can_frame frame = {
                  .flags = CAN_FRAME_IDE,
                  .id = 0x1234567,
                  .dlc = 2
          };

          frame.data[0] = 1;
          frame.data[1] = 2;

          return can_send(can_dev, &frame, K_FOREVER, tx_callback, "Sender 1");
  }

接收
****

只有与过滤器匹配的帧才会被接收。以下代码片段展示了如何通过添加过滤器来接收帧。

下面是用于 :c:func:`can_add_rx_filter` 的接收回调函数示例。用户数据参数在添加过滤器时传入。

.. code-block:: C

  void rx_callback_function(const struct device *dev, struct can_frame *frame, void *user_data)
  {
          ... do something with the frame ...
  }

以下代码片段展示了如何添加带有回调函数的过滤器。这是接收消息最高效的方式，但也是最需要谨慎处理的方式。回调函数在中断上下文中调用，这意味着回调函数应尽可能简短，并且不得阻塞。不允许在用户空间上下文中添加回调函数。

此示例中的过滤器配置为精确匹配标识符 0x123。

.. code-block:: C

  const struct can_filter my_filter = {
          .flags = 0U,
          .id = 0x123,
          .mask = CAN_STD_ID_MASK
  };
  int filter_id;
  const struct device *const can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));

  filter_id = can_add_rx_filter(can_dev, rx_callback_function, callback_arg, &my_filter);
  if (filter_id < 0) {
    LOG_ERR("Unable to add rx filter [%d]", filter_id);
  }

下面展示了 :c:func:`can_add_rx_filter_msgq` 的使用示例。通过此函数，可以同步接收帧。此函数可以在用户空间上下文中调用。消息队列的容量应足以容纳预计积压的消息。

此示例中的过滤器配置为精确匹配扩展标识符 0x1234567。

.. code-block:: C

  const struct can_filter my_filter = {
          .flags = CAN_FILTER_IDE,
          .id = 0x1234567,
          .mask = CAN_EXT_ID_MASK
  };
  CAN_MSGQ_DEFINE(my_can_msgq, 2);
  struct can_frame rx_frame;
  int filter_id;
  const struct device *const can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));

  filter_id = can_add_rx_filter_msgq(can_dev, &my_can_msgq, &my_filter);
  if (filter_id < 0) {
    LOG_ERR("Unable to add rx msgq [%d]", filter_id);
    return;
  }

  while (true) {
    k_msgq_get(&my_can_msgq, &rx_frame, K_FOREVER);
    ... do something with the frame ...
  }

:c:func:`can_remove_rx_filter` 用于移除指定的过滤器。

.. code-block:: C

  can_remove_rx_filter(can_dev, filter_id);

设置比特率
**********

比特率和采样点在运行时进行初始设置。要在应用中更改这些设置，可以使用 :c:func:`can_set_timing` API。:c:func:`can_calc_timing` 函数可以根据比特率和以千分比表示的采样点计算时序。以下示例将比特率设为 250k 波特，采样点设为 87.5%。

.. code-block:: C

  struct can_timing timing;
  const struct device *const can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));
  int ret;

  ret = can_calc_timing(can_dev, &timing, 250000, 875);
  if (ret > 0) {
    LOG_INF("Sample-Point error: %d", ret);
  }

  if (ret < 0) {
    LOG_ERR("Failed to calc a valid timing");
    return;
  }

  ret = can_stop(can_dev);
  if (ret != 0) {
    LOG_ERR("Failed to stop CAN controller");
  }

  ret = can_set_timing(can_dev, &timing);
  if (ret != 0) {
    LOG_ERR("Failed to set timing");
  }

  ret = can_start(can_dev);
  if (ret != 0) {
    LOG_ERR("Failed to start CAN controller");
  }

对于支持 CAN FD 的控制器，也有类似的 API 用于计算和设置数据阶段的时序。请参阅 :c:func:`can_set_timing_data` 和 :c:func:`can_calc_timing_data` 。

SocketCAN
*********

Zephyr 还支持 SocketCAN，它是 Zephyr CAN API 的 BSD 套接字实现。SocketCAN 将广为人知的 BSD 套接字 API 的便利性带到了控制器局域网。它与 Linux SocketCAN 实现兼容，许多其他高层 CAN 项目都构建在该实现之上。请注意，帧会被路由到网络协议栈，而不是直接传递，这会增加一些计算和内存开销。

示例
****

我们提供了两个可直接构建的示例，用于演示 Zephyr CAN API 的用法：:zephyr:code-sample:`Zephyr CAN 计数器示例 <can-counter>` 和 :zephyr:code-sample:`SocketCAN 示例 <socket-can>` 。


CAN 控制器 API 参考
*******************

.. doxygengroup:: can_controller

.. doxygengroup:: can_fake
