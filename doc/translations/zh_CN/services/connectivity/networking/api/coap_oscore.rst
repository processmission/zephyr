.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _coap_oscore_interface:

OSCORE 支持（:rfc:`8613`）
##########################

.. contents::
    :local:
    :depth: 2


概述
====

Zephyr CoAP 库按照 :rfc:`8613` 的规定，为受限 RESTful 环境提供对象安全（OSCORE）支持。OSCORE 使用 COSE（CBOR Object Signing and Encryption）为 CoAP 消息提供端到端保护。

OSCORE 在应用层保护 CoAP 消息，提供以下特性：

1. **机密性**：消息载荷和敏感选项会被加密
2. **完整性**：使用 MAC 对消息进行身份验证
3. **重放保护**：序列号可防止重放攻击
4. **代理友好**：外层选项保持可见，以用于路由

与 DTLS 不同，OSCORE 提供端到端安全，即使在不同传输协议（UDP、TCP、HTTP）之间经过代理转换也能保持。

其他 OSCORE 配置选项：

- :kconfig:option:`CONFIG_COAP_OSCORE_MAX_CONTEXTS`：OSCORE 安全上下文的最大数量
- :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_CACHE_SIZE`：每个服务要跟踪的 OSCORE 交换数量
- :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS`：受跟踪 OSCORE 交换的生存时间，用于保护
   延迟（分离）响应
- :kconfig:option:`CONFIG_COAP_OSCORE_CONTEXT_REUSE`：启用对跨重启重用上下文的 OSCORE 支持
- :kconfig:option:`CONFIG_COAP_OSCORE_MASTER_SECRET_MAX_LEN`：OSCORE 主密钥的最大长度（字节）
- :kconfig:option:`CONFIG_COAP_OSCORE_MASTER_SALT_MAX_LEN`：OSCORE 主盐值的最大长度（字节）

配置
====

通过 :kconfig:option:`CONFIG_COAP_OSCORE` 启用 OSCORE 支持。此选项依赖于 uoscore-uedhoc 模块和 PSA Crypto 支持：

.. code-block:: kconfig

   CONFIG_COAP_OSCORE=y
   CONFIG_UOSCORE=y
   CONFIG_PSA_CRYPTO=y

uoscore 模块会自动选择所需的 PSA 加密算法（AES-CCM、HKDF-SHA256 等）。

服务器用法
==========

要在 CoAP 服务上启用 OSCORE，请使用 :c:macro:`COAP_SERVICE_DEFINE_OSCORE` 定义服务（对于 DTLS，使用 :c:macro:`COAPS_SERVICE_DEFINE_OSCORE`）。该宏会静态分配每个服务的 OSCORE 交换缓存。安全上下文通过 Zephyr OSCORE API 单独创建并添加到共享池中；应用不要直接包含底层 uoscore-uedhoc 头文件。传入请求会根据其 Recipient ID 和 ID Context 匹配到正确的上下文，因此单个服务可以服务多个客户端，每个客户端都有自己的上下文：

.. code-block:: c

   #include <zephyr/net/coap_oscore.h>
   #include <zephyr/net/coap_service.h>

   static struct coap_oscore_context *my_oscore_ctx;

   static uint16_t my_service_port = 5683;

   /* Final argument "true" requires OSCORE for all requests. */
   COAP_SERVICE_DEFINE_OSCORE(my_service, NULL, &my_service_port,
                              COAP_SERVICE_AUTOSTART, true);

   int my_service_oscore_init(void)
   {
       /* coap_oscore_context_add() copies the key material, so these
        * buffers need not outlive the call and can live on the stack.
        */
       const uint8_t master_secret[16] = { /* ... */ };
       const uint8_t master_salt[8] = { /* ... */ };
       const uint8_t sender_id[] = { /* ... */ };
       const uint8_t recipient_id[] = { /* ... */ };

       struct coap_oscore_init_params params = {
           .master_secret = master_secret,
           .master_secret_len = sizeof(master_secret),
           .sender_id = sender_id,
           .sender_id_len = sizeof(sender_id),
           .recipient_id = recipient_id,
           .recipient_id_len = sizeof(recipient_id),
           .master_salt = master_salt,
           .master_salt_len = sizeof(master_salt),
           .aead_alg = COAP_OSCORE_AEAD_AES_CCM_16_64_128,
           .hkdf = COAP_OSCORE_HKDF_SHA_256,
           .fresh_master_secret_salt = true,
       };

       /* Add the context to the shared pool once its key material is
        * available. Call once per client identity (Recipient ID).
        */
       return coap_oscore_context_add(&params, &my_oscore_ctx);
   }

可同时分配的上下文数量由 :kconfig:option:`CONFIG_COAP_OSCORE_MAX_CONTEXTS` 控制。使用 ``coap_oscore_context_remove()`` 释放上下文。上下文采用引用计数：当进行中的请求、活动交换或观察者仍引用某个上下文时，``coap_oscore_context_remove()`` 会返回 ``-EAGAIN``，该上下文会被保留。在这些引用释放后，请重试释放操作。

当服务启用了 OSCORE 时（使用 ``OSCORE`` 宏创建，且至少有一个上下文添加到池中）：

1. **传入请求**：服务器会自动验证并解密受 OSCORE 保护的请求（:rfc:`8613` 第 8.2 节）。资源处理函数接收解密后的 CoAP 消息，其中 Inner 选项可见。

2. **传出响应**：服务器会自动对源自 OSCORE 交换的响应和通知应用 OSCORE 保护（:rfc:`8613` 第 8.3 节）。给定的传出消息是否需要保护，按如下方式决定：

   - **同步响应** 在处理请求期间生成，会与
      每个服务的交换缓存进行匹配；如果找到匹配项，则对其进行保护。这些条目会在 :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS` 之后过期。在混合服务（同时服务 OSCORE 和非 OSCORE 客户端）上，如果交换缓存条目已过期，再发送同步响应将导致明文响应。
   - **Observe 通知** 的保护基于观察者存储的 OSCORE
      状态，该状态在观察期间一直存在。
   - **延迟（分离）响应** 在请求处理函数已
      返回后生成，会与每个服务的交换缓存进行匹配；如果找到匹配项，则对其进行保护。这些条目会在 :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS` 之后过期。在混合服务（同时服务 OSCORE 和非 OSCORE 客户端）上，如果交换缓存条目已过期，再发送延迟响应将导致明文响应。

3. **错误处理**：OSCORE 验证错误会作为简单的 CoAP 响应发送，
    **不进行** OSCORE 处理（:rfc:`8613` 第 8.2 节）：- COSE 解码失败 → 4.02 Bad Option；- 找不到安全上下文 → 4.01 Unauthorized；- 解密失败 → 4.00 Bad Request

4. **要求 OSCORE**：如果定义服务时将 ``_oscore_required`` 参数
    设置为 true，则未受保护的请求会被拒绝，并返回 4.01 Unauthorized。

5. **故障关闭行为**：如果响应的 OSCORE 保护失败，服务器不会回退为发送明文响应。在要求 OSCORE 的服务上，无法与任何 OSCORE 状态匹配的出站响应也会被丢弃，而不会以明文发送。Observe 通知永远不会被降级。在混合服务上，交换缓存条目已过期的任何响应（同步或延迟）都无法再匹配，并会以未保护方式发送。实际上，这会影响延迟（分离）响应，因为同步响应会与处理请求期间刚创建的条目进行匹配（参见第 2 项和 :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS`）。


已知限制
========

1. **混合服务中交换过期后的明文**：在混合服务（同时服务 OSCORE 和非 OSCORE 客户端）上，交换缓存条目已过期的响应无法再与其 OSCORE 状态匹配，并会以明文发送。这会影响同步响应和延迟（分离）响应（参见 :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS`）。对于任何承载敏感数据的服务，应将其定义为要求 OSCORE（将 ``_oscore_required`` 参数传为 true，例如通过 :c:macro:`COAP_SERVICE_DEFINE_OSCORE`），而不是运行混合服务。要求 OSCORE 的服务会拒绝未受保护的请求，并丢弃无法保护的响应，因此绝不会降级为明文。

安全上下文派生
==============

OSCORE 安全上下文由一小组参数派生而来（:rfc:`8613` 第 3 节）：

**必需参数**：

- **主密钥（Master Secret）**：共享密钥（对于 AES-CCM-16-64-128 通常为 16 字节）
- **发送方 ID（Sender ID）**：发送方的唯一标识符
- **接收方 ID（Recipient ID）**：接收方的唯一标识符

**可选参数**：

- **主盐值（Master Salt）**：附加熵（推荐，通常为 8 字节）
- **ID 上下文（ID Context）**：附加的上下文标识符
- **AEAD 算法**：默认为 AES-CCM-16-64-128
- **KDF**：默认为 HKDF-SHA-256

这些参数通常通过以下方式建立：

1. **预共享密钥**：在设备配置时设置
2. **EDHOC**：Ephemeral Diffie-Hellman Over COSE（参见 uoscore-uedhoc 模块）

安全注意事项
============

1. **序列号溢出**：对于 AES-CCM-16-64-128，发送方序列号（SSN）不得超过 2^23-1。uoscore 库会强制实施此限制。

2. **主密钥保护**：主密钥必须安全存储（例如存储在安全存储中，或通过 EDHOC 派生）。

3. **跨重启持久化**：如果重启后重用同一主密钥（即主密钥不是重新派生的，例如未通过 EDHOC 派生），则必须将发送方序列号持久化到非易失性存储器，以防止 nonce 重用，否则会破坏机密性和完整性。接收方的重放窗口不需要持久化：它保存在内存中，并在重启后使用 Echo 选项重新同步，如 :rfc:`8613` 附录 B.1.2 所述。

不支持 OSCORE 时的处理
----------------------

未启用 OSCORE 支持时（未设置 :kconfig:option:`CONFIG_COAP_OSCORE`），Zephyr CoAP 协议栈会按照 :rfc:`7252` 第 5.4.1 节对 OSCORE 选项实施故障关闭行为：

**服务器行为**：当 ``CONFIG_COAP_OSCORE=n`` 时：

- 带 OSCORE 选项的 **CON 请求**：返回 **4.02（Bad Option）** 响应
- 带 OSCORE 选项的 **NON 请求**：静默拒绝（丢弃）该消息
- 带 OSCORE 选项的 **响应**：对于 CON 发送 RST，对于 NON/ACK 静默丢弃

API 参考
========

.. doxygengroup:: coap_oscore
