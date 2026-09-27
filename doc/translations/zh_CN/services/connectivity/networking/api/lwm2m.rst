.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _lwm2m_interface:

轻量级 M2M（LwM2M）
###################

.. contents::
    :local:
    :depth: 2

概述
****

轻量级机器到机器（Lightweight Machine to Machine，LwM2M）是一种应用层协议，其设计考虑了设备管理、数据上报和设备致动。 `LwM2M`_ 基于 CoAP/UDP，是由 Open Mobile Alliance 定义的 `标准 <https://openmobilealliance.org/release/LightweightM2M/>`_，它通过 CoAP 数据包大小优化以及支持 REST API 的简单无状态流程，适用于受限设备。

LwM2M 与 CoAP 的关键区别之一是，LwM2M 客户端会主动发起与 LwM2M 服务器的连接。然后，服务器可以使用 REST API 管理与该客户端之间的各种接口。

LwM2M 使用简单的资源模型，其核心对象和资源集在规范中定义。

可通过 :kconfig:option:`CONFIG_LWM2M` Kconfig 选项启用 LwM2M 库。

LwM2M 对象和资源示例：Device
****************************

*对象定义*

.. list-table::
   :header-rows: 1

   * - 对象 ID
     - 名称
     - 实例
     - 必需

   * - 3
     - Device
     - 单个
     - 必需

*资源定义*

``* R=Read, W=Write, E=Execute``

.. list-table::
   :header-rows: 1

   * - ID
     - 名称
     - OP\*
     - 实例
     - 必需
     - 类型

   * - 0
     - 制造商
     - R
     - 单个
     - 可选
     - 字符串

   * - 1
     - 型号
     - R
     - 单个
     - 可选
     - 字符串

   * - 2
     - 序列号
     - R
     - 单个
     - 可选
     - 字符串

   * - 3
     - 固件版本
     - R
     - 单个
     - 可选
     - 字符串

   * - 4
     - 重启
     - E
     - 单个
     - 必需
     -

   * - 5
     - 恢复出厂设置
     - E
     - 单个
     - 可选
     -

   * - 6
     - 可用电源
     - R
     - 多个
     - 可选
     - 整数 0-7

   * - 7
     - 电源电压（mV）
     - R
     - 多个
     - 可选
     - 整数

   * - 8
     - 电源电流（mA）
     - R
     - 多个
     - 可选
     - 整数

   * - 9
     - 电池电量 %
     - R
     - 单个
     - 可选
     - 整数

   * - 10
     - 可用内存（Kb）
     - R
     - 单个
     - 可选
     - 整数

   * - 11
     - 错误代码
     - R
     - 多个
     - 可选
     - 整数 0-8

   * - 12
     - 重置错误
     - E
     - 单个
     - 可选
     -

   * - 13
     - 当前时间
     - RW
     - 单个
     - 可选
     - 时间

   * - 14
     - UTC 偏移
     - RW
     - 单个
     - 可选
     - 字符串

   * - 15
     - 时区
     - RW
     - 单个
     - 可选
     - 字符串

   * - 16
     - 支持的绑定方式
     - R
     - 单个
     - 必需
     - 字符串

   * - 17
     - 设备类型
     - R
     - 单个
     - 可选
     - 字符串

   * - 18
     - 硬件版本
     - R
     - 单个
     - 可选
     - 字符串

   * - 19
     - 软件版本
     - R
     - 单个
     - 可选
     - 字符串

   * - 20
     - 电池状态
     - R
     - 单个
     - 可选
     - 整数 0-6

   * - 21
     - 总内存（Kb）
     - R
     - 单个
     - 可选
     - 整数

   * - 22
     - ExtDevInfo
     - R
     - 多个
     - 可选
     - ObjLnk

服务器可以向客户端发送 ``READ 3/0/0`` 操作，以查询 ``Device`` 对象实例 0（默认且唯一的实例）的 ``Manufacturer`` 资源。

已注册对象和资源 ID 的完整列表可在 `OMA LwM2M registries`_ 中找到。

Zephyr 的 LwM2M 库位于 :zephyr_file:`subsys/net/lib/lwm2m` 中，客户端示例位于 :zephyr_file:`samples/net/lwm2m_client`。有关所提供示例的更多信息，请参见 :zephyr:code-sample:`lwm2m-client`。该示例可以配置为使用普通的不安全网络 socket，或使用通过 DTLS 保护的 socket。

Zephyr LwM2M 库实现以下内容：

* 用于处理网络事件和核心功能的引擎
* 执行 BOOTSTRAP 和 REGISTRATION 功能的 RD 客户端
* SenML CBOR、SenML JSON、CBOR、TLV、JSON 和纯文本格式化功能
* LwM2M 技术规范 Enabler 对象，例如 Security、Server、Device、Firmware Update 等。
* 扩展 IPSO 对象，例如 Light Control、Temperature Sensor 和 Timer

默认情况下，该库实现 `LwM2M specification 1.0.2`_，并可通过 Kconfig 选项设置为 `LwM2M specification 1.1.1`_。

有关 LwM2M 规范版本的更多信息，请访问 `OMA LwM2M releases`_ 页面。

用法示例
********

要使用 LwM2M 库，首先创建一个 LwM2M 客户端上下文 :c:struct:`lwm2m_ctx` 结构体：

.. code-block:: c

        /* LwM2M client context */
        static struct lwm2m_ctx client;

为 LwM2M 资源执行创建回调函数：

.. code-block:: c

        static int device_reboot_cb(uint16_t obj_inst_id, uint8_t *args,
                                    uint16_t args_len)
        {
                LOG_INF("Device rebooting.");
                LOG_PANIC();
                sys_reboot(0);
                return 0; /* won't reach this */
        }

LwM2M RD 客户端可以将事件发送回示例。要接收这些事件，请设置回调函数：

.. code-block:: c

        static void rd_client_event(struct lwm2m_ctx *client,
                                    enum lwm2m_rd_client_event client_event)
        {
                switch (client_event) {

                case LWM2M_RD_CLIENT_EVENT_NONE:
                        /* do nothing */
                        break;

                case LWM2M_RD_CLIENT_EVENT_BOOTSTRAP_REG_FAILURE:
                        LOG_DBG("Bootstrap registration failure!");
                        break;

                case LWM2M_RD_CLIENT_EVENT_BOOTSTRAP_REG_COMPLETE:
                        LOG_DBG("Bootstrap registration complete");
                        break;

                case LWM2M_RD_CLIENT_EVENT_BOOTSTRAP_TRANSFER_COMPLETE:
                        LOG_DBG("Bootstrap transfer complete");
                        break;

                case LWM2M_RD_CLIENT_EVENT_REGISTRATION_FAILURE:
                        LOG_DBG("Registration failure!");
                        break;

                case LWM2M_RD_CLIENT_EVENT_REGISTRATION_COMPLETE:
                        LOG_DBG("Registration complete");
                        break;

                case LWM2M_RD_CLIENT_EVENT_REG_TIMEOUT:
                        LOG_DBG("Registration timeout!");
                        break;

                case LWM2M_RD_CLIENT_EVENT_REG_UPDATE_COMPLETE:
                        LOG_DBG("Registration update complete");
                        break;

                case LWM2M_RD_CLIENT_EVENT_DEREGISTER_FAILURE:
                        LOG_DBG("Deregister failure!");
                        break;

                case LWM2M_RD_CLIENT_EVENT_DISCONNECT:
                        LOG_DBG("Disconnected");
                        break;

                case LWM2M_RD_CLIENT_EVENT_REG_UPDATE:
                        LOG_DBG("Registration update");
                        break;

                case LWM2M_RD_CLIENT_EVENT_DEREGISTER:
                        LOG_DBG("Deregistration client");
                        break;

                case LWM2M_RD_CLIENT_EVENT_SERVER_DISABLED:
                        LOG_DBG("LwM2M server disabled");
                  break;
                }
        }

接下来，我们为 ``Security`` 资源赋值，让客户端知道连接到哪里以及如何连接，同时使用一些数据以及前面定义的回调，设置 ``Device`` 对象中的 ``Manufacturer`` 和 ``Reboot`` 资源：

.. code-block:: c

        /*
         * Server URL of default Security object = 0/0/0
         * Use leshan.eclipse.org server IP (5.39.83.206) for connection
         */
        lwm2m_set_string(&LWM2M_OBJ(0, 0, 0), "coap://5.39.83.206");

        /*
         * Security Mode of default Security object = 0/0/2
         * 3 = NoSec mode (no security beware!)
         */
        lwm2m_set_u8(&LWM2M_OBJ(0, 0, 2), 3);

        #define CLIENT_MANUFACTURER "Zephyr Manufacturer"

        /*
         * Manufacturer resource of Device object = 3/0/0
         * We use lwm2m_set_res_data() function to set a pointer to the
         * CLIENT_MANUFACTURER string.
         * Note the LWM2M_RES_DATA_FLAG_RO flag which stops the engine from
         * trying to assign a new value to the buffer.
         */
        lwm2m_set_res_data(&LWM2M_OBJ(3, 0, 0), CLIENT_MANUFACTURER,
                           sizeof(CLIENT_MANUFACTURER),
                           LWM2M_RES_DATA_FLAG_RO);

        /* Reboot resource of Device object = 3/0/4 */
        lwm2m_register_exec_callback(&LWM2M_OBJ(3, 0, 4), device_reboot_cb);

最后，我们启动 LwM2M RD 客户端（同时也会启动 LwM2M 引擎）。 :c:func:`lwm2m_rd_client_start` 的第二个参数是客户端端点名称。这一点很重要，因为它需要在每个 LwM2M 服务器上唯一：

.. code-block:: c

        (void)memset(&client, 0x0, sizeof(client));
        lwm2m_rd_client_start(&client, "unique-endpoint-name", 0, rd_client_event);

.. _lwm2m_security:

LwM2M 安全模式
**************

Zephyr LwM2M 库可以在不使用安全机制的情况下使用，也可以使用 DTLS 来保护通信通道。将 DTLS 与 LwM2M 引擎一起使用时，可以使用 PSK（Pre-Shared Key，预共享密钥）和 X.509 证书这两种安全模式来保护通信。该引擎使用 LwM2M Security 对象（Id 0）读取存储的凭据，并将安全对象中的密钥提供给 TLS 凭据子系统，请参见 :ref:`安全 socket 文档 <secure_sockets_interface>`。启用 :kconfig:option:`CONFIG_LWM2M_DTLS_SUPPORT` Kconfig 选项即可使用该安全功能。

根据所选模式，安全对象必须包含以下数据：

PSK
  安全模式（资源 ID 2）设置为 0（预共享密钥模式）。身份（资源 ID 3）包含二进制形式的 PSK ID。密钥（资源 ID 5）包含二进制形式的 PSK 密钥。如果密钥或身份以十六进制字符串形式提供，则必须先转换为二进制，再存储到安全对象中。

X509
  使用 X509 证书时，将安全模式（ID 2）设置为 ``2`` （证书模式）。身份（ID 3）用于存储客户端证书，密钥（ID 5）必须具有与该证书关联的私钥。服务器公钥资源（ID 4）必须包含用于对证书链进行签名的服务器证书或 CA 证书。如果启用了 :kconfig:option:`CONFIG_MBEDTLS_PEM_PARSE_C` / :kconfig:option:`CONFIG_MBEDTLS_PEM_WRITE_C` Kconfig 选项，则可以 PEM 格式输入证书和私钥。否则，它们必须采用二进制 DER 格式。

NoSec
  不使用安全机制时，将安全模式（资源 ID 2）设置为 ``3`` （NoSec）。

在所有模式下，服务器 URI 资源（ID 0）必须包含目标服务器的完整 URI。使用 DNS 名称时，必须启用 DNS 解析器。

使用 DTLS 时，建议采用以下选项，以减少重新建立连接时的 DTLS 握手流量：

* :kconfig:option:`CONFIG_LWM2M_DTLS_CID` 启用 DTLS 连接标识符支持。当服务器支持该功能时，设备在长时间空闲后恢复运行时可完全省去握手。这在 NAT 映射超时时非常有用。
* :kconfig:option:`CONFIG_LWM2M_TLS_SESSION_CACHING` 会在回退到完整 DTLS 握手之前使用会话缓存。当服务器端仍缓存有会话时，可减少握手过程中的少量数据包。最显著的效果是避免完整注册。

LwM2M 协议栈在 :c:struct:`lwm2m_ctx` 结构中提供回调。它们用于将 LwM2M 安全对象中的密钥提供给 TLS 凭据子系统。默认情况下，可以将这些回调保留为 NULL 指针，此时会使用默认回调。当需要外部 TLS 协议栈或非默认 socket 选项时，可以覆盖 :c:func:`lwm2m_ctx.load_credentials` 或 :c:func:`lwm2m_ctx.set_socketoptions` 回调。

为 PSK 模式设置安全对象的示例：

.. code-block:: c

        /* "000102030405060708090a0b0c0d0e0f" */
        static unsigned char client_psk[] = {
                0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f
        };

        static const char client_identity[] = "Client_identity";

        lwm2m_set_string(&LWM2M_OBJ(LWM2M_OBJECT_SECURITY_ID, 0, 0), "coaps://lwm2m.example.com");
        lwm2m_set_u8(&LWM2M_OBJ(LWM2M_OBJECT_SECURITY_ID, 0, 2), LWM2M_SECURITY_PSK);
        /* Set the client identity as a string, but this could be binary as well */
        lwm2m_set_string(&LWM2M_OBJ(LWM2M_OBJECT_SECURITY_ID, 0, 3), client_identity);
        /* Set the client pre-shared key (PSK) */
        lwm2m_set_opaque(&LWM2M_OBJ(LWM2M_OBJECT_SECURITY_ID, 0, 5), client_psk, sizeof(client_psk));

为 X509 证书模式设置安全对象的示例：

.. code-block:: c

        static const char certificate[] = "-----BEGIN CERTIFICATE-----\nMIIB6jCCAY+gAw...";
        static const char key[] = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQ...";
        static const char root_ca[] = "-----BEGIN CERTIFICATE-----\nMIIBaz...";

        lwm2m_set_string(&LWM2M_OBJ(LWM2M_OBJECT_SECURITY_ID, 0, 0), "coaps://lwm2m.example.com");
        lwm2m_set_u8(&LWM2M_OBJ(LWM2M_OBJECT_SECURITY_ID, 0, 2), LWM2M_SECURITY_CERT);
        lwm2m_set_string(&LWM2M_OBJ(LWM2M_OBJECT_SECURITY_ID, 0, 3), certificate);
        lwm2m_set_string(&LWM2M_OBJ(LWM2M_OBJECT_SECURITY_ID, 0, 5), key);
        lwm2m_set_string(&LWM2M_OBJ(LWM2M_OBJECT_SECURITY_ID, 0, 4), root_ca);

在调用 :c:func:`lwm2m_rd_client_start` 之前，请为 tls_tag # 赋值，该值指定 LwM2M 库在连接前应存储 DTLS 信息的位置（这里通常使用值 1 即可）。

.. code-block:: c

        (void)memset(&client, 0x0, sizeof(client));
        client.tls_tag = 1; /* <---- */
        lwm2m_rd_client_start(&client, "endpoint-name", 0, rd_client_event);

更详细的 LwM2M 客户端示例请参见 :zephyr:code-sample:`lwm2m-client`。

多线程用法
**********
可以使用 lwm2m_set_u8 之类的函数向资源写入值。向多个资源写入时，lwm2m_registry_lock 函数将确保客户端暂停，直到所有写入操作完成：

.. code-block:: c

  lwm2m_registry_lock();
  lwm2m_set_u32(&LWM2M_OBJ(1, 0, 1), 60);
  lwm2m_set_u8(&LWM2M_OBJ(5, 0, 3), 0);
  lwm2m_set_f64(&LWM2M_OBJ(3303, 0, 5700), value);
  lwm2m_registry_unlock();

如果服务器正在对写入的资源进行复合观察，这一点尤其有用。此时加锁可确保客户端仅在所有操作完成后才更新并向服务器发送通知，从而总体上减少消息数量。

支持时间序列数据
****************

LwM2M 1.1 版增加了对 SenML CBOR 和 SenML JSON 数据格式的支持。这些数据格式增加了对时间序列数据的支持。时间序列格式可用于 READ、NOTIFY 和 SEND 操作。为资源启用数据缓存后，每次写入都会在缓存中创建带时间戳的条目，随后在针对给定资源的 READ、NOTIFY 或 SEND 操作中将其内容作为内容返回。

仅支持为具有固定数据大小的资源使用数据缓存。

支持的资源类型：

* 有符号和无符号 8-64 位整数
* 浮点数
* 布尔值

启用和配置
==========

通过选择 :kconfig:option:`CONFIG_LWM2M_RESOURCE_DATA_CACHE_SUPPORT` 启用数据缓存。应用需要分配一个 :c:struct:`lwm2m_time_series_elem` 结构体数组，然后针对给定资源调用 :c:func:`lwm2m_enable_cache` 启用缓存。每个资源都必须单独启用，并且每个资源都需要自己的存储空间。

.. code-block:: c

  /* Allocate data cache storage */
  static struct lwm2m_time_series_elem temperature_cache[10];
  /* Enable data cache */
  lwm2m_enable_cache(LWM2M_OBJ(IPSO_OBJECT_TEMP_SENSOR_ID, 0, SENSOR_VALUE_RID),
          temperature_cache, ARRAY_SIZE(temperature_cache));

应用可以使用 :c:func:`lwm2m_cache_free_slots_get` 检查缓存资源中的可用空间；该函数返回仍可存储的样本数，如果查询失败则返回负 errno 值。

LwM2M 引擎可为四个启用缓存的资源预留空间。可以通过修改 :kconfig:option:`CONFIG_LWM2M_MAX_CACHED_RESOURCES` 提高该限制。这会影响引擎的静态内存使用量。

数据缓存依赖以下 SenML 数据格式之一： :kconfig:option:`CONFIG_LWM2M_RW_SENML_CBOR_SUPPORT` 或 :kconfig:option:`CONFIG_LWM2M_RW_SENML_JSON_SUPPORT` ，并且需要 :kconfig:option:`CONFIG_POSIX_TIMERS` 才能从系统请求时间戳。

读取和写入操作
==============

当任何 READ、SEND 或 NOTIFY 操作在内部读取给定资源的内容时，数据缓存的全部内容都会写入载荷。这带来的副作用是，启用缓存后，为该资源注册的任何读取回调都会被忽略。调用任何 ``lwm2m_set_*`` 函数时，数据都会写入缓存。应用可以使用 :c:func:`lwm2m_set_cache_filter` 注册缓存过滤回调，以根据应用特定的规则丢弃原本有效的样本。

限制
====

应手动将缓存大小设置得足够小，以便内容能够适应正常的数据包大小。缓存已满时，新值将被丢弃。

SEND 调度器辅助对象
*******************

可选的 SEND 调度器扩展提供两个对象（Send scheduler Control ``10523`` 和 Sampling Rules ``10524``），它们位于缓存资源之上，用于决定何时保留样本以及客户端何时应触发 LwM2M SEND。

启用和关联
==========

* 选择 :kconfig:option:`CONFIG_LWM2M_SEND_SCHEDULER` （需要 LwM2M 1.1 SEND 支持以及 :kconfig:option:`CONFIG_LWM2M_RESOURCE_DATA_CACHE_SUPPORT`）。
* SEND 调度器对象会自动注册；请确保在启动 RD 客户端之前配置好缓存。
* 使用 :c:func:`lwm2m_set_cache_filter` 将 :c:func:`lwm2m_send_sched_cache_filter` 附加到每个应由调度器管理的缓存资源。
* 当注册或注册更新完成时（在 ``LWM2M_RD_CLIENT_EVENT_REGISTRATION_COMPLETE`` 和 ``LWM2M_RD_CLIENT_EVENT_REG_UPDATE_COMPLETE`` 时），从 RD 客户端回调中调用 :c:func:`lwm2m_send_sched_handle_registration_event`，以便在注册交互结束后立即发送缓存样本。

Scheduler Control 对象（10523）
===============================

该单实例控制对象用于配置全局行为：

* ``0: paused`` – 停止接受缓存中的样本。
* ``1: max-samples`` – 所有资源缓存样本的上限；达到该限制时强制发送 SEND （``0`` 表示禁用）。
* ``2: max-age`` – 触发 SEND 之前，最旧缓存样本的最大存在时间（秒）（``0`` 表示禁用）。
* ``3: flush`` – 执行资源，立即为所有已配置的规则路径触发 SEND。
* ``4: flush-on-update`` – 启用时（默认），成功注册或注册更新事件会触发缓存资源的 SEND。

Sampling Rules 对象（10524）
============================

每个实例描述一个要监视的缓存资源。 ``/10524/X/0`` 保存资源路径， ``/10524/X/1`` 最多包含四个规则字符串。支持的属性：

* ``gt=<float>`` – 当样本向上越过阈值时触发。
* ``lt=<float>`` – 当样本向下越过阈值时触发。
* ``st=<float>`` – 当与上次报告值的绝对差值大于或等于阈值时触发。
* ``pmin=<int>`` – 接受样本之间的最小秒数。
* ``pmax=<int>`` – 强制至少每隔 ``pmax`` 秒保留一个缓存样本，即使没有变化。

当某个实例未配置规则时，每个传入样本都会被缓存。当受控资源的缓存空间耗尽，或达到全局 ``max-samples``/``max-age`` 限制时，调度器也会强制触发 SEND。

LwM2M 引擎和应用事件
********************

Zephyr LwM2M 引擎定义了可通过回调函数发送回应用的事件。引擎状态机展示了这些事件的产生时机。图中描绘的事件在表中列出。事件名称以 ``LWM2M_RD_CLIENT_EVENT_`` 为前缀。

.. figure:: images/lwm2m_engine_state_machine.svg
    :alt: LwM2M 引擎状态机

    LwM2M 引擎的状态机

.. list-table:: LwM2M RD 客户端事件
   :widths: auto
   :header-rows: 1

   * - 事件 ID
     - 事件名称
     - 描述
   * - 0
     - NONE
     - 无事件
   * - 1
     - BOOTSTRAP_REG_FAILURE
     - 引导注册失败。如果引导注册超时或失败，则会发生此事件。
   * - 2
     - BOOTSTRAP_REG_COMPLETE
     - 引导注册完成。引导注册成功后发生。
   * - 3
     - BOOTSTRAP_TRANSFER_COMPLETE
     - 从服务器收到引导完成命令。
   * - 4
     - REGISTRATION_FAILURE
     - 向 LwM2M 服务器注册失败。如果服务器拒绝注册尝试，则会发生此事件。
   * - 5
     - REGISTRATION_COMPLETE
     - 向 LwM2M 服务器注册成功。在收到 LwM2M 服务器成功注册回复后，或使用会话恢复时发生。
   * - 6
     - REG_TIMEOUT
     - 注册状态丢失。如果出现 socket 错误或消息超时，则会发生此事件。客户端已与服务器断开连接。
   * - 7
     - REG_UPDATE_COMPLETE
     - 注册更新完成。在收到 LwM2M 服务器成功注册更新回复后发生。
   * - 8
     - DEREGISTER_FAILURE
     - 向 LwM2M 服务器注销失败。如果注销超时或失败，则会发生此事件。
   * - 9
     - DISCONNECT
     - LwM2M 客户端已从服务器注销并停止。仅当应用请求客户端停止时才会触发。
   * - 10
     - QUEUE_MODE_RX_OFF
     - 仅在队列模式下使用，此时不会主动监听传入数据包。在队列模式下，经过配置的时间段后，客户端无需主动监听传入数据包。
   * - 11
     - ENGINE_SUSPENDED
     - 表示客户端因调用 :c:func:`lwm2m_engine_pause` 而暂停。状态机不再运行，处理线程已挂起。所有定时器均已停止，因此不会触发通知。
   * - 12
     - SERVER_DISABLED
     - 服务器执行了禁用命令。客户端将注销，并在禁用期内保持空闲。
   * - 13
     - NETWORK_ERROR
     - 向网络发送消息失败次数过多。客户端无法连接任何服务器，也无法回退到引导。LwM2M 引擎无法恢复并已停止。

LwM2M 客户端引擎会自动处理大多数状态转换。应用只需处理那些表示客户端已停止或处于无法恢复状态的事件。

.. list-table:: 应用应如何响应事件
   :widths: auto
   :header-rows: 1

   * - 事件名称
     - 应用应如何响应
   * - NONE
     - 忽略该事件。
   * - BOOTSTRAP_REG_FAILURE
     - 尝试恢复网络连接。然后调用 :c:func:`lwm2m_rd_client_start` 重新启动客户端。这也可能表示存在配置问题。
   * - BOOTSTRAP_REG_COMPLETE
     - 无需操作
   * - BOOTSTRAP_TRANSFER_COMPLETE
     - 无需操作
   * - REGISTRATION_FAILURE
     - 无需操作。客户端会自动重新注册。可能需要引导或修复配置。无法发送或接收数据。
   * - REGISTRATION_COMPLETE
     - 无需操作。应用可以发送或接收数据。
   * - REG_TIMEOUT
     - 无需操作。客户端会自动重新注册。无法发送或接收数据。
   * - REG_UPDATE_COMPLETE
     - 无需操作。应用可以发送或接收数据。
   * - DEREGISTER_FAILURE
     - 无需操作，客户端会自动进入空闲状态。无法发送或接收数据。
   * - DISCONNECT
     - 引擎因调用 :c:func:`lwm2m_rd_client_stop` 而停止。如果需要连接，应用应调用 :c:func:`lwm2m_rd_client_start` 重新启动客户端。
   * - QUEUE_MODE_RX_OFF
     - 无需操作。应用可以发送数据，但不能接收数据。任何数据传输都会触发注册更新。
   * - ENGINE_SUSPENDED
     - 可以通过调用 :c:func:`lwm2m_engine_resume` 恢复引擎。无法发送或接收数据。
   * - SERVER_DISABLED
     - 无需操作，禁用期结束后客户端会重新注册。无法发送或接收数据。
   * - NETWORK_ERROR
     - 尝试恢复网络连接。然后调用 :c:func:`lwm2m_rd_client_start` 重新启动客户端。这也可能表示存在配置问题。

上表中的“发送数据”是指调用 :c:func:`lwm2m_send_cb` 或写入某个被观察资源，而观察会触发通知消息。“接收数据”是指从服务器接收读取、写入或执行操作。应用可以为这些操作注册回调。

配置生命周期和活动周期
**********************

在 LwM2M 引擎中，有三个 Kconfig 选项和一个运行时值用于配置客户端发送 LwM2M Update 消息的频率。

.. list-table:: 更新周期变量
   :widths: auto
   :header-rows: 1

   * - 变量
     - 作用
   * - LwM2M 注册生命周期
     - LwM2M 中的 lifetime 参数指定设备在 LwM2M 服务器上的注册保持有效的时长。设备应在 lifetime 到期之前发送 LwM2M Update 消息。
   * - :kconfig:option:`CONFIG_LWM2M_ENGINE_DEFAULT_LIFETIME`
     - 默认生命周期值，除非由引导服务器设置。它还定义了客户端可接受的生命周期下限。
   * - :kconfig:option:`CONFIG_LWM2M_UPDATE_PERIOD`
     - 客户端在发送下一次更新前可以保持空闲的时间。
   * - :kconfig:option:`CONFIG_LWM2M_SECONDS_TO_UPDATE_EARLY`
     - 在注册生命周期到期之前发送更新消息的最小时间余量。

.. figure:: images/lwm2m_lifetime_seconds_early.png
    :alt: LwM2M 提前更新的秒数

    计算何时更新注册的默认方式。

默认情况下，客户端使用 :kconfig:option:`CONFIG_LWM2M_SECONDS_TO_UPDATE_EARLY` 计算在生命周期到期前多少秒发送注册更新。默认模式的问题在于服务器会更改注册的生命周期。这会影响客户端执行更新的周期。如果将其用于 IPv4 网络中常见的 QUEUE 模式，还会影响设备可被服务器访问的时段。

.. figure:: images/lwm2m_lifetime_both.png
    :alt: 同时设置两个值时的 LwM2M 更新时间

    更新时间由 UPDATE_PERIOD 控制。

当同时设置 :kconfig:option:`CONFIG_LWM2M_UPDATE_PERIOD` 时，发送更新消息的时间为这些值中任一到期的最早时间。这样可以为注册设置较长的生命周期并准确配置周期，即使服务器更改了 lifetime 参数。

在运行时，更新频率限制为每 15 秒一次，以避免泛洪。

.. _lwm2m_shell:

LwM2M shell
***********
为了测试客户端，可以启用 Zephyr 的 shell 和 LwM2M 专用命令，这些命令支持更改客户端状态。支持的操作包括读取、写入和执行资源。还可以启动、停止、暂停和恢复客户端。通过选择 :kconfig:option:`CONFIG_LWM2M_SHELL` 启用该功能。shell 仅用于测试，因此生产系统不应启用它。

可以想象的一种使用 shell 的场景是：当服务器端测试需要触发客户端操作时，通过 UART 执行客户端侧操作。这里假设并非所有测试都能从服务器端触发所需操作。

.. code-block:: console

  uart:~$ lwm2m
  lwm2m - LwM2M commands
  Subcommands:
    send    :send PATHS
            LwM2M SEND operation

    exec    :exec PATH [PARAM]
            Execute a resource

    read    :read PATH [OPTIONS]
            Read value from LwM2M resource
            -x   Read value as hex stream (default)
            -s   Read value as string
            -b   Read value as bool (1/0)
            -uX  Read value as uintX_t
            -sX  Read value as intX_t
            -f   Read value as float
            -t   Read value as time_t

    write   :write PATH [OPTIONS] VALUE
            Write into LwM2M resource
            -s   Write value as string (default)
            -b   Write value as bool
            -uX  Write value as uintX_t
            -sX  Write value as intX_t
            -f   Write value as float
            -t   Write value as time_t

    create  :create PATH
            Create object or resource instance

    delete  :delete PATH
            Delete object or resource instance

    cache   :cache PATH NUM
            Enable data cache for resource
            PATH is LwM2M path
            NUM how many elements to cache

    start   :start EP_NAME [BOOTSTRAP FLAG]
            Start the LwM2M RD (Registration / Discovery) Client
            -b   Set the bootstrap flag (default 0)

    stop    :stop [OPTIONS]
            Stop the LwM2M RD (De-register) Client
            -f   Force close the connection

    update  :Trigger Registration Update of the LwM2M RD Client

    pause   :LwM2M engine thread pause
    resume  :LwM2M engine thread resume
    lock    :Lock the LwM2M registry
    unlock  :Unlock the LwM2M registry
    obs     : List observations
    ls      : ls [PATH]
            List objects, instances, resources




.. _lwm2m_api_reference:

API 参考
********

.. doxygengroup:: lwm2m_api

.. _LwM2M:
   https://www.openmobilealliance.org/specifications/lwm2m

.. _OMA LwM2M registries:
   https://www.openmobilealliance.org/specifications/registries

.. _OMA LwM2M releases:
   https://www.openmobilealliance.org/specifications/lwm2m/releases

.. _LwM2M specification 1.0.2:
   https://www.openmobilealliance.org/release/LightweightM2M/V1_0_2-20180209-A/OMA-TS-LightweightM2M-V1_0_2-20180209-A.pdf

.. _LwM2M specification 1.1.1:
   https://www.openmobilealliance.org/release/LightweightM2M/V1_1_1-20190617-A/
