.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _async_notification:

异步通知
########

Zephyr API 中经常包含 :ref:`api_term_async` 函数：操作被发起后，应用程序需要获知操作何时完成以及是否成功。使用 :c:func:`k_poll` 通常是一种好方法，但某些应用架构可能更适合回调通知；而启用时钟和电源轨等操作可能需要在核函数可用之前调用，因此可能需要忙等待操作完成。

此 API 旨在嵌入特定子系统中，例如 :ref:`resource_mgmt_onoff` 以及其他支持异步事务的 API。子系统封装层负责从包含通知元素的请求中提取与操作相关的数据，并使用 API 所需的参数调用回调。

此 API 的一个局限是它不适用于 :ref:`syscalls`，原因如下：

* :c:struct:`sys_notify` 不是内核对象；
* 从用户空间复制通知内容会破坏实现函数中对 :c:macro:`CONTAINER_OF` 的使用；
* 自旋等待和回调通知两种方式都无法接受来自用户空间的调用者。

如果从用户模式线程发起的异步操作需要通知，子系统或驱动程序应提供一个使用 :c:struct:`k_poll_signal` 进行通知的系统调用 API。

API 参考
********

.. doxygengroup:: sys_notify_apis
