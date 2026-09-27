.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _os_services:

服务
####

Zephyr 提供了一整套全面的子系统及相关服务，供应用程序使用。这些服务提供标准化 API，将硬件实现细节抽象出来，使应用程序可以在不同平台之间移植。

.. grid:: 1
   :class-container: sd-index-grid
   :gutter: 0

   .. grid-item-card:: :ref:`连接 <connectivity_services>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`hub;7em`

      .. toctree::
         :maxdepth: 2

         connectivity/index

   .. grid-item-card:: :ref:`输入 / 输出 <io_services>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`swap_horiz;7em`

      .. toctree::
         :maxdepth: 2

         io

   .. grid-item-card:: :ref:`进程间通信 <ipc_services>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`forum;7em`

      .. toctree::
         :maxdepth: 2

         messaging

   .. grid-item-card:: :ref:`日志、跟踪与调试 <observability_services>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`bug_report;7em`

      .. toctree::
         :maxdepth: 2

         observability

   .. grid-item-card:: :ref:`存储与配置 <storage_services>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`storage;7em`

      .. toctree::
         :maxdepth: 2

         storage/index

   .. grid-item-card:: :ref:`内存管理 <memory_management_services>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`memory;7em`

      .. toctree::
         :maxdepth: 2

         memory_management

   .. grid-item-card:: :ref:`电源管理 <power_management_services>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`bolt;7em`

      .. toctree::
         :maxdepth: 2

         power_management

   .. grid-item-card:: :ref:`安全 <security_services>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`security;7em`

      .. toctree::
         :maxdepth: 2

         security

   .. grid-item-card:: :ref:`设备管理 <device_mgmt>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`devices;7em`

      .. toctree::
         :maxdepth: 2

         device_mgmt/index

   .. grid-item-card:: :ref:`算法与数据 <algorithms_services>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`functions;7em`

      .. toctree::
         :maxdepth: 2

         algorithms

   .. grid-item-card:: :ref:`框架 <frameworks>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`widgets;7em`

      .. toctree::
         :maxdepth: 2

         frameworks

   .. grid-item-card:: :ref:`操作系统抽象 <osal>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`layers;7em`

      .. toctree::
         :maxdepth: 2

         portability/index
