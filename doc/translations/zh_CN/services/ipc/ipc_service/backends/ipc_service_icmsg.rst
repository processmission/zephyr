.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ipc_service_backend_icmsg:

ICMsg 后端
##########

核间消息传递后端（ICMsg）是相较更重量级的 RPMsg 静态 vrings 后端而言更轻量的替代方案。它以很小的内存占用提供了最基本的功能集。ICMsg 后端构建在 :ref:`spsc_pbuf` 之上。

概述
====

ICMsg 后端使用共享内存和 MBOX 设备来交换数据。共享内存用于存储数据，MBOX 设备用于发送数据已写入的信号。

该后端支持在单个实例上注册单个端点。如果应用需要多个通信通道，则必须定义多个实例，每个实例都有自己专用的端点。

配置
====

该后端通过 Kconfig 和 devicetree 配置。配置该后端时，请执行以下操作：

* 如果至少有一个核在共享内存上使用数据缓存，请设置 ``dcache-alignment`` 的值。该值必须是通信双方的失效大小和回写大小中的最大值。如果通信双方都不在共享内存上使用数据缓存，则可以跳过该项。
* 定义两个内存区域，并将它们分别分配给某个实例的 ``tx-region`` 和 ``rx-region``。确保用于数据交换的内存区域是唯一的（不与其他任何区域重叠），并且两个域（或 CPU）都能访问。
* 定义用于发送信号的 MBOX 设备，该信号通知另一个域（或 CPU）数据已写入。确保另一个域（或 CPU）能够接收该信号。

.. caution::

    请确保为 ``dcache-alignment`` 设置正确的值。错误的值起初可能没有任何表现，从而让人误以为一切正常。但不稳定的行为迟早会出现。

参见以下其中一个实例的配置示例：

.. code-block:: devicetree

   reserved-memory {
      tx: memory@20070000 {
         reg = <0x20070000 0x0800>;
      };

      rx: memory@20078000 {
         reg = <0x20078000 0x0800>;
      };
   };

      ipc {
         ipc0: ipc0 {
            compatible = "zephyr,ipc-icmsg";
            dcache-alignment = <32>;
            tx-region = <&tx>;
            rx-region = <&rx>;
            mboxes = <&mbox 0>, <&mbox 1>;
            mbox-names = "tx", "rx";
            status = "okay";
         };
      };
   };


您必须为通信的另一侧（域或 CPU）提供类似的配置，但必须交换 MBOX 通道和内存区域（``tx-region`` 和 ``rx-region``）。

绑定
====

端点注册后，通过 IPC 实例连接的每个域（或 CPU）上都会发生以下情况：

1. 域（或 CPU）将一个 magic number 写入其共享内存的 ``tx-region``。
#. 随后，它会向另一个域或 CPU 发送信号，告知数据已写入。向另一个域或 CPU 发送信号的操作会以超时机制重复执行。
#. 当收到来自另一个域或 CPU 的信号时，会从 ``rx-region`` 读取 magic number。如果读取的值正确，则绑定过程完成，后端会通过调用 :c:member:`ipc_service_cb.bound` 回调来通知应用。

示例
====

 - :zephyr:code-sample:`ipc-icmsg`

详细协议规范
============

ICMsg 使用两个共享内存区域和两个 MBOX 通道。区域和通道组成的配对用于在一个方向上传输消息。另一对是对称的，用于在相反方向上传输消息。因此，下面的规范重点介绍其中一对。另一对完全相同。

ICMsg 每个实例仅提供一个端点。

共享内存区域组织
----------------

如果启用了数据缓存，则提供给 ICMsg 的共享内存区域必须根据缓存要求进行对齐。如果未启用缓存，则要求的对齐为 4 字节。

共享内存区域完全由一个 FIFO 使用。它包含读索引和写索引，之后是数据缓冲区。详细结构见下表：

.. list-table::
   :header-rows: 1

   * - 字段名称
     - 大小（字节）
     - 字节序
     - 描述
   * - ``rd_idx``
     - 4
     - 小端序
     - ``data`` 字段中第一个传入字节的索引。
   * - ``padding``
     - 取决于缓存对齐
     - 不适用
     - 为使 ``wr_idx`` 按缓存对齐而添加的填充。
   * - ``wr_idx``
     - 4
     - 小端序
     - ``data`` 字段中最后一个传入字节之后那个字节的索引。
   * - ``data``
     - 直至区域末尾的全部空间
     - 不适用
     - 包含实际要传输字节的环形缓冲区。

这是一个带有环形缓冲区的常规 FIFO：

* 当索引（``rd_idx`` 和 ``wr_idx``）到达 ``data`` 缓冲区末尾时，会回绕到开头。
* 如果 ``rd_idx == wr_idx``，则 FIFO 为空。
* FIFO 的容量比 ``data`` 缓冲区长度少一个字节。

数据包
------

数据包通过上一节所述的 FIFO 发送。如果数据包位于 FIFO 缓冲区末尾，则可能会发生回绕。

数据包结构如下：

.. list-table::
   :header-rows: 1

   * - 字段名称
     - 大小（字节）
     - 字节序
     - 描述
   * - ``len``
     - 2
     - 大端序
     - ``data`` 字段的长度。
   * - ``reserved``
     - 2
     - 不适用
     - 保留供将来使用。对于当前协议版本，该值必须为 0。
   * - ``data``
     - ``len``
     - 不适用
     - 数据包中的数据。
   * - ``padding``
     - 0-3
     - 不适用
     - 添加填充以使数据包总大小按 4 字节对齐。

数据包发送流程如下：

#. 检查数据包是否能放入缓冲区。
#. 从 ``wr_idx`` 开始，将数据包写入 ``data`` FIFO 缓冲区。如有需要，进行回绕。
#. 写入 ``wr_idx`` 的新值。
#. 通过 MBOX 通道通知接收方。

初始化
------

初始化流程如下：

#. 将 ``wr_idx`` 和 ``rd_idx`` 设置为 0。
#. 向 FIFO 推入一个包含 magic 数据的单个数据包：``45 6d 31 6c 31 4b 30 72 6e 33 6c 69 34``。此时尚未使用 MBOX。
#. 初始化 MBOX。
#. 以某个间隔（例如 1 ms）重复通过 MBOX 通道发送通知。
#. 等待包含 magic 数据的传入数据包。该数据包将通过另一对（共享内存区域和 MBOX）到达。
#. 停止重复 MBOX 通知。

此后，ICMsg 完成绑定，并准备好传输数据包。
