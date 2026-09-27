.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_provisioning:

配网
####

配网是将设备加入 Mesh 网络的过程。它需要两个设备分别承担以下角色：

* *配网器* 代表网络所有者，负责将新节点加入 Mesh 网络。
* *被配网设备* 是通过配网过程加入网络的设备。在配网过程开始之前，被配网设备是 *未配网设备*。

Zephyr Bluetooth Mesh 协议栈中的配网模块支持被配网设备角色的广播和 GATT 配网承载，以及配网器角色的广播配网承载。

配网过程
********

所有 Bluetooth Mesh 节点都必须先完成配网，才能加入 Bluetooth Mesh 网络。配网 API 提供了设备成为已配网 Mesh 节点所需的全部功能。配网是一个包含以下步骤的五步过程：

* 信标广播
* 邀请
* 公钥交换
* 认证
* 配网数据传输

Beaconing
=========

要开始配网过程，未配网设备必须首先开始广播 Unprovisioned Beacon。这使其对附近的配网器可见，配网器可以发起配网。要指示设备需要配网，请调用 :c:func:`bt_mesh_prov_enable`。设备使用设备 UUID 和 ``OOB information`` 字段开始广播 Unprovisioned Beacon，具体如传递给 :c:func:`bt_mesh_init` 的 ``prov`` 参数中所指定。此外，还可以指定统一资源标识符（URI），它可以将配网器指向某些带外信息的位置，例如设备的公钥或认证值数据库。URI 在单独的信标中广播，未配网信标中包含 URI 哈希，以将两者关联起来。


统一资源标识符
--------------

统一资源标识符应遵循 Bluetooth Core Specification Supplement 中指定的格式。URI 必须以 URI 方案开头，该方案编码为单个 UTF-8 数据点，或者使用特殊 ``none`` 方案，编码为 ``0x01``。可用的方案列在 `Bluetooth 网站 <https://www.bluetooth.com/specifications/assigned-numbers/>`_ 上。

编码 URI 示例：

.. list-table:: URI 编码示例

  * - URI
    - 编码
  * - ``http://example.com``
    - ``\x16//example.com``
  * - ``https://www.zephyrproject.org/``
    - ``\x17//www.zephyrproject.org/``
  * - ``just a string``
    - ``\x01just a string``

配网邀请
========

配网器通过发送 Provisioning invitation 来发起配网过程。如果可用，该邀请会提示被配网设备使用 Health Server :ref:`bluetooth_mesh_models_health_srv_attention` 引起注意。

未配网设备通过提供其能力列表来自动响应邀请，能力列表包括支持的带外认证方法和算法。

Public key exchange
===================

在配网过程开始之前，配网器和未配网设备会通过带内或带外（OOB）方式交换公钥。

带内公钥交换是配网过程的一部分，未配网设备和配网器始终支持。

如果应用希望通过 OOB 支持公钥交换，则需要向 Mesh 协议栈提供公钥和私钥。未配网设备将在其能力中反映这一点。配网器通过任何可用的 OOB 机制获取公钥（例如，设备可以广播包含公钥的数据包，或者公钥可以编码在设备包装上印刷的 QR 码中）。请注意，即使未配网设备已指定用于带外交换的公钥，如果配网器无法通过 OOB 机制获取公钥，也可以选择带内交换公钥。在这种情况下，Mesh 协议栈将为每次配网过程生成一个新的密钥对。

要在未配网设备侧启用 OOB 公钥支持，需要启用 :kconfig:option:`CONFIG_BT_MESH_PROV_OOB_PUBLIC_KEY`。应用必须在配网过程开始之前，通过初始化指向 :c:member:`bt_mesh_prov.public_key_be` 和 :c:member:`bt_mesh_prov.private_key_be` 的指针来提供公钥和私钥。密钥需要按大端字节序提供。

要在配网器侧提供通过 OOB 获取的设备公钥，请调用 :c:func:`bt_mesh_prov_remote_pub_key_set`。

Authentication
==============

初始交换之后，配网器选择一种带外（OOB）认证方法。这使用户能够确认配网器连接的设备确实是他们想要的设备，而不是恶意的第三方。

配网 API 支持以下用于被配网设备的认证方法：

* **静态 OOB：** 在生产过程中为设备分配一个认证值，配网器可以通过某种应用特定的方式查询该值。要使用 BTM_ECDH_P256_HMAC_SHA256_AES_CCM 算法进行安全配网，静态 OOB 值应包含超过 128 位的熵，以提供足够的抗攻击安全性。
* **输入 OOB：** 由用户输入认证值。可用的输入操作列在 :c:enum:`bt_mesh_input_action_t` 中。
* **输出 OOB：** 向用户显示认证值。可用的输出操作列在 :c:enum:`bt_mesh_output_action_t` 中。

应用必须在 :c:struct:`bt_mesh_prov` 中为支持的认证方法提供回调，并在 :c:member:`bt_mesh_prov.output_actions` 和 :c:member:`bt_mesh_prov.input_actions` 中启用支持的操作。

选择输出 OOB 操作后，应在调用输出回调时向用户显示认证值，并保持显示，直到调用 :c:member:`bt_mesh_prov.input_complete` 或 :c:member:`bt_mesh_prov.complete` 回调。如果操作为 ``blink``、``beep`` 或 ``vibrate``，则应在延迟三秒或更长时间后重复该序列。

选择输入 OOB 操作后，当应用收到 :c:member:`bt_mesh_prov.input` 回调时，应提示用户。用户响应应通过 :c:func:`bt_mesh_input_string` 或 :c:func:`bt_mesh_input_numeric` 反馈给配网 API。如果在 60 秒内未记录到用户响应，则配网过程中止。

如果被配网设备想要强制使用 OOB 认证，则必须使用 BT_MESH_ECDH_P256_HMAC_SHA256_AES_CCM 算法。

数据传输
========

设备成功通过认证后，配网器会传输配网数据：

* 单播地址
* 一个网络密钥
* IV 索引
* 网络标志

  * 密钥刷新
  * IV 更新

此外，还会为节点生成设备密钥。所有这些数据都由 Mesh 协议栈存储，并调用配网的 :c:member:`bt_mesh_prov.complete` 回调。

配网安全
********

根据公钥交换机制和认证方法的选择，配网过程可能是安全的或不安全的。

2021 年 5 月 24 日，ANSSI `披露 <https://kb.cert.org/vuls/id/799380>`_ 了 Bluetooth Mesh 配网协议中的一组漏洞，展示了 Blink、Vibrate、Push、Twist 以及输入/输出数字 OOB 方法提供的低熵如何被用于冒充和 MITM 攻击。作为回应，Bluetooth SIG 在 Bluetooth Mesh Profile Specification v1.0.1 `勘误 16350 <https://www.bluetooth.org/docman/handlers/DownloadDoc.ashx?doc_id=516072>`_ 中将这些 OOB 方法重新归类为不安全，因为 AuthValue 可能会被实时暴力破解。为确保安全配网，应用应使用静态 OOB 值和 OOB 公钥传输。

API 参考
********

.. doxygengroup:: bt_mesh_prov
