.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ipc_service:

IPC 服务
########

.. contents::
    :local:
    :depth: 2

IPC 服务 API 提供了一个用于在两个域或 CPU 之间交换数据的接口。

概述
====

一个 IPC 服务通信通道由一个实例以及与该实例关联的一个或多个端点组成。

实例是两个域或 CPU 之间物理通信通道的外部表示。实例的实际实现和内部表示因每个后端而异。

不能使用单个实例在域/CPU 之间发送数据。要发送和接收数据，用户必须在实例中创建（注册）一个端点。这样便可将两个相关的域连接起来。

一个实例可以有零个或多个端点，这些端点的优先级可以不同，并可使用每个端点交换数据。端点的优先级排序和多实例能力很大程度上取决于所使用的后端。

端点是用户在两个域（由实例连接）之间发送和接收数据时必须使用的实体。端点始终与某个实例关联。

实例的创建由后端负责，通常在初始化时进行。端点的注册由用户负责，通常在运行时进行。

该 API 不强制后端以何种方式创建实例，但强烈建议使用 devicetree 来获取实例的配置参数。目前，每个后端都定义了自己的与 DT 兼容的配置，用于在启动时配置接口。

支持以下使用场景：

* 简单数据交换。
* 使用零拷贝 API 的数据交换。

简单数据交换
============

要在域或 CPU 之间发送数据，必须将端点注册到实例上。

参见以下示例：

.. note::

   在注册端点之前，必须使用 :c:func:`ipc_service_open_instance` 函数打开实例。


.. code-block:: c

   #include <zephyr/ipc/ipc_service.h>

   static void bound_cb(void *priv)
   {
      /* Endpoint bounded */
   }

   static void recv_cb(const void *data, size_t len, void *priv)
   {
      /* Data received */
   }

   static struct ipc_ept_cfg ept0_cfg = {
      .name = "ept0",
      .cb = {
         .bound    = bound_cb,
         .received = recv_cb,
      },
   };

   int main(void)
   {
      const struct device *inst0;
      struct ipc_ept ept0;
      int ret;

      inst0 = DEVICE_DT_GET(DT_NODELABEL(ipc0));
      ret = ipc_service_open_instance(inst0);
      ret = ipc_service_register_endpoint(inst0, &ept0, &ept0_cfg);

      /* Wait for endpoint bound (bound_cb called) */

      unsigned char message[] = "hello world";
      ret = ipc_service_send(&ept0, &message, sizeof(message));
   }

使用零拷贝 API 的数据交换
=========================

如果后端支持零拷贝 API，则可以使用它直接读写共享内存区域。

参见以下示例：

.. code-block:: c

   #include <zephyr/ipc/ipc_service.h>
   #include <stdint.h>
   #include <string.h>

   static struct ipc_ept ept0;

   static void bound_cb(void *priv)
   {
      /* Endpoint bounded */
   }

   static void recv_cb_nocopy(const void *data, size_t len, void *priv)
   {
      int ret;

      ret = ipc_service_hold_rx_buffer(&ept0, (void *)data);
      /* Process directly or put the buffer somewhere else and release. */
      ret = ipc_service_release_rx_buffer(&ept0, (void *)data);
   }

   static struct ipc_ept_cfg ept0_cfg = {
      .name = "ept0",
      .cb = {
         .bound    = bound_cb,
         .received = recv_cb,
      },
   };

   int main(void)
   {
      const struct device *inst0;
      int ret;

      inst0 = DEVICE_DT_GET(DT_NODELABEL(ipc0));
      ret = ipc_service_open_instance(inst0);
      ret = ipc_service_register_endpoint(inst0, &ept0, &ept0_cfg);

      /* Wait for endpoint bound (bound_cb called) */
      void *data;
      unsigned char message[] = "hello world";
      uint32_t len = sizeof(message);

      ret = ipc_service_get_tx_buffer(&ept0, &data, &len, K_FOREVER);

      memcpy(data, message, len);

      ret = ipc_service_send_nocopy(&ept0, data, sizeof(message));
   }

后端
====

实现后端所需的要求为 IPC 服务提供了灵活性。这些要求允许为特定用例添加仅具有部分功能的专用后端。

后端必须至少支持以下功能：

* 在初始化时创建实例。
* 在运行时向实例注册端点。

此外，后端还可以支持以下功能：

* 在运行时从实例注销端点。
* 在运行时关闭实例。
* 零拷贝 API。

每个后端都可以有自己的限制和特性，这使每个后端都独一无二，并专用于特定的用例。IPC 服务 API 可以同时与多个后端一起使用，从而综合每个后端的优点和缺点。

.. toctree::
   :maxdepth: 1

   backends/ipc_service_icmsg.rst
   backends/ipc_service_icbmsg.rst

API 参考
========

IPC 服务 API
************

.. doxygengroup:: ipc_service_api

IPC 服务后端 API
****************

.. doxygengroup:: ipc_service_backend
