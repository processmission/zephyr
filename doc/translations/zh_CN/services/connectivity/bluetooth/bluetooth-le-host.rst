.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_le_host:

LE 主机
#######

蓝牙主机实现所有高层协议和配置文件，最重要的是为应用提供高层 API。下图展示了主机的主要协议层与配置文件层。

.. figure:: img/ble_host_layers.png
   :align: center
   :alt: 蓝牙主机协议与配置文件层

   蓝牙主机协议与配置文件层。

主机协议栈的最底层是所谓的 HCI 驱动，负责抽象 HCI 传输的细节。它提供一个基本 API，用于将数据从控制器传送到主机，反之亦然。

在 HCI 处理之上，最重要的模块或许是通用访问配置文件（Generic Access Profile，GAP）。GAP 定义了四种不同的蓝牙使用角色，从而简化了蓝牙 LE 接入：

* 面向连接的角色

  * 外围设备（例如智能传感器，通常用户界面有限）

  * 中心设备（通常是移动电话或 PC）

* 无连接角色

  * 广播者（发送蓝牙 LE 广播，例如智能信标）

  * 观察者（扫描蓝牙 LE 广播）

每个角色都有自己的构建时配置选项：:kconfig:option:`CONFIG_BT_PERIPHERAL`、:kconfig:option:`CONFIG_BT_CENTRAL`、:kconfig:option:`CONFIG_BT_BROADCASTER` 和 :kconfig:option:`CONFIG_BT_OBSERVER`。在面向连接的角色中，中心设备会隐式启用观察者角色，外围设备会隐式启用广播者角色。创建应用时，通常第一步是确定需要哪些角色，然后由此展开。蓝牙 Mesh 的情况稍特殊，至少需要观察者和广播者角色，可能还需要外围设备角色。后面的章节将对此进行更详细的说明。

外围设备角色
============

大多数基于 Zephyr 的蓝牙 LE 设备很可能都是外围设备角色。这意味着它们会执行可连接广播，并公开一个或多个 GATT 服务。使用 :c:func:`bt_gatt_service_register` API 注册服务后，应用通常会使用 :c:func:`bt_le_adv_start` API 开始可连接广播。

代码树中提供了多个外围设备示例应用，例如 :zephyr_file:`samples/bluetooth/peripheral_hr`。

中心设备角色
============

对于基于 Zephyr 的设备，中心设备角色可能不如外围设备角色常见，但它仍然是一种可行的角色，并且在 Zephyr 中同样得到良好支持。中心设备角色不会接受其他设备的连接，而是扫描可用的外围设备并选择其中一个进行连接。连接后，中心设备通常会充当 GATT 客户端，先发现可用服务，然后访问一个或多个受支持的服务。

为了先发现要连接的目标设备，应用可能会使用 :c:func:`bt_le_scan_start` API，等待找到合适的设备（通过扫描回调），使用 :c:func:`bt_le_scan_stop` 停止扫描，然后使用 :c:func:`bt_conn_le_create` 连接到该设备。

代码树中提供了一些中心设备角色的示例应用，例如 :zephyr_file:`samples/bluetooth/central_hr`。

观察者角色
==========

观察者角色设备会使用 :c:func:`bt_le_scan_start` API 扫描设备，但不会连接其中任何一个。它只是利用所发现设备的广播数据，并可选地结合接收信号强度（Received Signal Strength，RSSI）。

广播者角色
==========

广播者角色设备会使用 :c:func:`bt_le_adv_start` API 广播特定的广播数据，但广播类型为不可连接，即其他设备无法连接到它。

连接
====

连接处理及相关 API 请参见 :ref:`连接管理 <bluetooth_connection_mgmt>` 一节。

.. _bluetooth_callback_contexts:

回调执行上下文
==============

主机通过已注册的回调向应用传递事件，例如 :c:struct:`bt_conn_cb`、:c:struct:`bt_le_scan_cb` 或 :c:struct:`bt_l2cap_chan_ops` 中的回调。除非另有说明，这些回调都在线程上下文中调用，绝不会在 ISR 中调用。大多数回调运行在协议栈内部上下文中，但有些目前在触发它们的 API 调用中同步调用，因而在调用线程中运行：例如 :c:func:`bt_unpair` 会调用 ``bond_deleted``，而 :c:func:`bt_gatt_unsubscribe` 可能在使用 ``NULL`` 数据的情况下调用 ``notify``，然后才返回。这两种行为都不属于 API 约定：今天同步交付的回调在将来版本中可能会被推迟到协议栈内部上下文，反之亦然；而且具体在哪个线程中执行，在不同版本之间曾经发生过变化，以后也可能再次变化。应用只应依赖上面给出的保证，而不应依赖自己会从某个特定上下文被调用，也不应依赖某项调用会在特定操作返回之前发生。

当回调运行在协议栈内部上下文时，该上下文与协议栈自身的处理共享：回调中耗费的时间会延迟其他蓝牙活动，而阻塞还会带来额外风险，因为只有蓝牙处理本身才能满足的等待会变成死锁——在回调返回之前，该处理无法继续。典型例子是从一个由运行该回调的同一上下文补充的缓冲池中使用 ``K_FOREVER`` 分配缓冲区。由于应用无法确定给定回调使用哪个上下文，下面的做法适用于每一个回调。

虽然大多数蓝牙 API 可能会阻塞，但在回调中调用蓝牙 API 很常见且受支持；此时阻塞风险是被管理，而不是被避免：

* 保持回调简短，将长时间运行或会无限期阻塞的工作推迟到应用自有的线程或工作队列中。
* 优先使用 ``K_NO_WAIT`` 或有限超时进行分配，而不是 ``K_FOREVER``，并处理失败情况。
* 合理设置缓冲池大小（例如 :kconfig:option:`CONFIG_BT_L2CAP_TX_BUF_COUNT` 或 :kconfig:option:`CONFIG_BT_ATT_TX_COUNT`），使回调中进行的分配无需等待。

安全
====

要在两个蓝牙设备之间建立安全关系，需要使用称为配对（pairing）的过程。该过程既可以通过 GATT 服务的安全属性隐式触发，也可以使用连接对象上的 :c:func:`bt_conn_set_security` API 显式触发。

要达到更高的安全级别并防范中间人（Man-In-The-Middle，MITM）攻击，建议在配对期间使用某种带外通道。如果设备具备足够的用户界面，这个“通道”就是用户本身。设备的能力通过 :c:func:`bt_conn_auth_cb_register` API 注册。传递给该 API 的 :c:struct:`bt_conn_auth_cb` 结构体有一组可在配对期间使用的可选回调——如果设备缺少某项功能，可以将对应的回调设置为 NULL。例如，如果设备没有输入功能但有显示屏，则应将 ``passkey_entry`` 和 ``passkey_confirm`` 回调设置为 NULL，而将 ``passkey_display`` 设置为能够向用户显示配对码的回调。

根据本地和对端的安全需求与能力，可以达到四种可能的安全级别：

    :c:enumerator:`BT_SECURITY_L1`
        无加密，也不进行认证。

    :c:enumerator:`BT_SECURITY_L2`
        加密但不进行认证（无 MITM 防护）。

    :c:enumerator:`BT_SECURITY_L3`
        使用 Bluetooth 4.0 和 4.1 的传统配对方法进行加密和认证。

    :c:enumerator:`BT_SECURITY_L4`
        使用 Bluetooth 4.2 起提供的 LE Secure Connections 功能进行加密和认证。

.. note::
  在安全方面，Mesh 通过称为 Provisioning 的过程提供了自己的解决方案。它采用与配对类似的流程，但使用单独的 Mesh 专用 API 完成。

L2CAP
=====

L2CAP 是逻辑链路控制与适配协议（Logical Link Control and Adaptation Protocol）的缩写。它是所有蓝牙连接通信的公共层，但应用只有在使用所谓的面向连接通道（Connection-oriented Channels，CoC）模式时才会直接接触它。更多信息请参见 :ref:`L2CAP API 一节 <bt_l2cap>`。

术语
----

以下定义摘自 Core Specification 5.4 版第 3 卷第 A 部分 1.4 节。

.. list-table::
  :header-rows: 1

  * - 术语
    - 描述

  * - 上层
    - L2CAP 之上的层，以 SDU（Service Data Unit）的形式交换数据。它可以是应用或更高层协议。

  * - 下层
    - L2CAP 之下的层，以 PDU（Protocol Data Unit，或分片）的形式交换数据。通常为 HCI。

  * - 服务数据单元（Service Data Unit，SDU）
    - L2CAP 与上层交换的数据包。

      该术语仅适用于增强重传模式、流模式、重传模式和流控模式，不适用于基本 L2CAP 模式。

  * - 协议数据单元（Protocol Data Unit，PDU）
    - 包含 L2CAP 数据的数据包。PDU 始终以基本 L2CAP 头部开始。

      LE 的 PDU 类型：:ref:`B 帧 <bluetooth_l2cap_b_frame>` 和 :ref:`K 帧 <bluetooth_l2cap_k_frame>`。

      BR/EDR 的 PDU 类型：I 帧、S 帧、C 帧和 G 帧。

  * - 最大传输单元（Maximum Transmission Unit，MTU）
    - 上层能够接受的最大 SDU 大小。

  * - 最大载荷大小（Maximum Payload Size，MPS）
    - L2CAP 层能够接受的最大载荷大小。

      在基本 L2CAP 模式下，MTU 大小等于 MPS。在无分段的基于信用的通道中，MTU 等于 MPS 减 2。

  * - 基本 L2CAP 头部
    - 位于每个 PDU 的开头。它包含两个字段：PDU 长度和通道标识符（Channel Identifier，CID）。

PDU 类型
--------

.. _bluetooth_l2cap_b_frame:

B 帧：基本信息帧
^^^^^^^^^^^^^^^^

用于基本 L2CAP 模式的 PDU。它包含从上层接收或作为其载荷交付给上层的数据载荷。

.. image:: img/l2cap_b_frame.drawio.svg
  :align: center
  :width: 45%
  :alt: B 帧 PDU 的示意图。该 PDU 被划分为两个矩形，
        第一个是 L2CAP 头部，大小为 4 个八位组，
        由 PDU 长度和通道 ID 组成。第二个矩形表示
        信息载荷，大小小于或等于 MPS。

.. _bluetooth_l2cap_k_frame:

K 帧：基于信用的帧
^^^^^^^^^^^^^^^^^^

用于 LE 基于信用的流控模式和增强型基于信用的流控模式的 PDU。它包含一个 SDU 分段和附加协议信息。

.. image:: img/l2cap_k_frame_1.drawio.svg
  :width: 45%
  :alt: 起始 K 帧 PDU 的示意图。该 PDU 被划分为三个
        矩形，第一个是 L2CAP 头部，大小为 4 个八位组，
        由 PDU 长度和通道 ID 组成。第二个矩形
        表示 L2CAP SDU 长度，大小为 2 个八位组。第三个
        矩形表示信息载荷，其大小小于或
        等于 MPS 减去 2 个八位组。信息载荷包含 L2CAP
        SDU。

.. image:: img/l2cap_k_frame.drawio.svg
  :align: right
  :width: 45%
  :alt: 起始帧之后的 K 帧 PDU 的示意图。该 PDU 被划分
        为两个矩形，第一个是 L2CAP 头部，大小为 4
        个八位组，由 PDU 长度和通道 ID 组成。第二个
        矩形表示信息载荷，其大小小于或
        等于 MPS。信息载荷包含 L2CAP SDU。

相关 Kconfig
------------

.. list-table::
  :header-rows: 1

  * - Kconfig 符号
    - 描述

  * - :kconfig:option:`CONFIG_BT_BUF_ACL_RX_SIZE`
    - 表示 MPS

  * - :kconfig:option:`CONFIG_BT_L2CAP_TX_MTU`
    - 表示 L2CAP MTU

  * - :kconfig:option:`CONFIG_BT_L2CAP_DYNAMIC_CHANNEL`
    - 启用 LE 基于信用的流控，因此协议栈可能会使用 :ref:`K 帧 <bluetooth_l2cap_k_frame>` PDU

GATT
====

通用属性配置文件（Generic Attribute Profile，GATT）是通过 LE 连接进行通信的最常见方式。有关该层的更详细说明以及 API 参考，请参见 :ref:`GATT API 参考一节 <bt_gatt>`。

ATT 超时
--------

如果对端设备在 ATT 超时时间内未响应 ATT 请求（如读或写），主机会自动发起断开连接。这样可以将罕见的失败情况归结为常见的断开连接，从而简化错误处理，使开发者无需为 ATT 超时做特殊处理即可管理意外断开。

.. image:: img/att_timeout.svg
  :align: center
  :alt: ATT timeout

Mesh
====

在所需的 GAP 角色方面，Mesh 稍微特殊一些。默认情况下，Mesh 要求同时启用观察者和广播者角色。如果需要可选的 GATT Proxy 功能，则还应启用外围设备角色。

Mesh 的 API 参考请参见 :ref:`Mesh API 参考一节 <bluetooth_mesh>`。

LE 音频
=======
LE 音频是一组配置文件和服务的集合，利用 GATT 和等时通道（Isochronous Channel）通过低功耗蓝牙提供音频。其架构和 API 参考请参见 :ref:`蓝牙音频架构 <bluetooth_le_audio_arch>`。


.. _bluetooth-persistent-storage:

持久存储
========

蓝牙主机协议栈使用设置子系统实现到闪存的持久存储。这要求存在闪存驱动，并在闪存上有一个指定的“storage”分区。所需的一组典型配置选项大致如下：

  .. code-block:: cfg

    CONFIG_BT_SETTINGS=y
    CONFIG_FLASH=y
    CONFIG_FLASH_PAGE_LAYOUT=y
    CONFIG_FLASH_MAP=y
    CONFIG_NVS=y
    CONFIG_SETTINGS=y

启用后，应用负责在初始化蓝牙（使用 :c:func:`bt_enable` API）之后调用 settings_load()。
