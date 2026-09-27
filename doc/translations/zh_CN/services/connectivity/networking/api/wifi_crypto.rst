.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _wifi_crypto_mapping:

Wi-Fi feature to crypto mapping
###############################

本页将 Zephyr 支持的 Wi-Fi 功能（通过基于 hostap 的 wpa_supplicant）映射到底层 MbedTLS crypto 原语。可用它查看哪些功能需要 bignum、ECDH、TLS 等，以及在启用 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_MBEDTLS_PSA` 时，哪些代码路径使用 **Legacy crypto** （MbedTLS 旧版 API）而非 **PSA crypto** （Platform Security Architecture API）。

实现位于 hostap 模块中：``crypto_mbedtls_alt.c`` （通用 crypto）和 ``tls_mbedtls_alt.c`` （TLS/EAP）。此处仅考虑 MbedTLS 后端。

功能集（来自 hostap Kconfig）
*****************************

功能由 Kconfig 控制。相关选项包括：

* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WEP` —— WEP（旧版）
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3_COMMON` —— 选择 Internal 或 External 时启用 WPA3-SAE（``WIFI_NM_WPA_SUPPLICANT_WPA3_IMPLEMENTATION``；默认为 Internal）。:kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3` 没有提示，并且在选择 Internal 时启用内部 bignum SAE 路径（请在 ``prj.conf`` 中设置实现选择，而不是此符号）。
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_DPP` —— Wi-Fi Easy Connect（DPP）
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPS` —— Wi-Fi Protected Setup（Wi-Fi 保护设置）
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_P2P` —— P2P / Wi-Fi Direct（隐含 WPS）
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_ENTERPRISE` —— EAP（EAP-TLS、EAP-TTLS-MSCHAPV2、EAP-PEAP-MSCHAPV2、EAP-PEAP-GTC、EAP-PEAP-TLS）

只要 crypto 未设置为 ``CRYPTO_NONE``，WPA2-PSK 和 WPA2-PSK-256 就可用。

功能 → crypto 原语（MbedTLS）
*****************************

.. list-table:: Wi-Fi 功能到 crypto 的映射
   :widths: 18 22 30 30
   :header-rows: 1

   * - 功能
     - crypto 原语
     - 旧版 crypto
     - PSA crypto
   * - **WPA3-SAE**
     - * Bignum（mpi）、模运算、幂运算
       * EC 组
       * HMAC-SHA256
       * AES（CCMP）。SAE 使用 Dragonfly（PWE）以及 bignum + 模运算。
     - * Bignum（mbedtls_mpi）
       * EC
       * HMAC、AES（除非为 PSA 构建）
     - * 启用 PSA 时使用哈希、HMAC、AES
       * Bignum/EC 仍为旧版
   * - **SAE-PK**
     - 与 WPA3-SAE 相同，另加 ECDH 和 EC 密钥操作（基于证书的 SAE）。
     - ECDH/EC 密钥操作（取决于配置，使用旧版 MbedTLS 或 PSA ECDH）。
     - * ECDH 可以使用 PSA
       * Bignum/SAE 核心仍为旧版
   * - **DPP（Easy Connect）**
     - * ECDH（P-256、P-384、P-521）
       * EC 密钥生成/签名/验证
       * 哈希、AES。DPP2 增加了 PKCS#7；DPP3 增加了 HPKE。
     - * ECDH、EC、RSA（如使用）
       * TLS/crypto 层中的 X.509/CSR
     - * 通过 PSA 使用哈希、HMAC、AES
       * ECDH/EC 可能使用 PSA
       * TLS/CSR/PKCS#7/HPKE 层为旧版
   * - **WPA2-PSK / WPA2-PSK-256**
     - * PBKDF2-SHA1（-256 使用 SHA256）
       * HMAC
       * AES（CCMP）
       * OMAC1-AES（密钥封装）
     - 如果禁用 PSA，全部通过 mbedtls（PBKDF2、HMAC、AES、CMAC）。
     - 启用 PSA 时，PBKDF2、HMAC、AES、OMAC1 通过 PSA 实现。
   * - **WEP**
     - * RC4/ARC4（流密码）
       * 某些封装可选使用 AES。已弃用。
     - 仅使用旧版 MbedTLS（当前代码中 WEP 没有 PSA 路径）。
     - 不适用（WEP 未迁移到 PSA）。
   * - **WPS**
     - * DH（有限域）
       * Bignum
       * 哈希、HMAC、AES、TLS-PRF。注册器使用 TLS。
     - * DH（mbedtls_dhm）、bignum（mbedtls_mpi）
       * tls_mbedtls_alt 中的 TLS
     - * 通过 PSA 使用哈希、HMAC、AES、PBKDF2
       * DH/bignum 和 TLS 为旧版
   * - **EAP-TLS / EAP-TTLS / EAP-PEAP**
     - * TLS 1.2（可选 1.3）
       * RSA
       * X.509 解析/验证
       * 哈希、HMAC、AES（密码套件）
     - * 完整 TLS 协议栈（mbedtls_ssl_*、mbedtls_x509_*）
       * RSA
       * tls_mbedtls_alt 中不使用 PSA
     - * TLS 层仍为旧版
       * 底层哈希/HMAC/AES 可在 crypto_mbedtls_alt 中使用 PSA
   * - **EAP-PWD**
     - * TLS-PRF
       * Bignum
       * DH（有限域）
       * EC（可选）
       * 哈希、HMAC
     - 如果使用 Bignum、DH、EC，则通过旧版 MbedTLS。
     - * 通过 PSA 使用哈希/HMAC
       * Bignum/DH/EC 为旧版
   * - **EAP-IKEV2**
     - * 密码（AES）、bignum、DH
       * TLS-PRF 风格的操作
     - 旧版密码、bignum、DH。
     - * 通过 PSA 使用 AES/哈希/HMAC
       * Bignum/DH 为旧版
   * - **开放**
     - 无身份验证/加密。
     - 不适用
     - 不适用

.. note::

   必须使用 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WEP` 显式启用 WEP。它已弃用且不安全；仅用于旧版网络。

摘要：Legacy 与 PSA 对比（MbedTLS 后端）
****************************************

启用 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_MBEDTLS_PSA` 后，``crypto_mbedtls_alt.c`` （以及 ``supp_psa_api.h`` / ``supp_psa_api.c``）中的实现按如下方式划分。可使用此表查看哪些操作使用 **PSA** 而非 **Legacy** MbedTLS。

.. list-table:: 按 crypto 操作划分的 Legacy 与 PSA
   :widths: 28 10 42
   :header-rows: 1

   * - 操作
     - API
     - 使用者/说明
   * - 消息摘要（MD5、SHA1、SHA256、SHA384、SHA512）
     - PSA
     -
   * - HMAC（上述所有哈希类型）
     - PSA
     -
   * - PBKDF2-SHA1
     - PSA
     - WPA2-PSK 密钥派生
   * - AES（块、CBC、CTR、OMAC1-AES）
     - PSA
     - 密钥封装、CCMP 等。
   * - Bignum（crypto_bignum_*）
     - 旧版
     - SAE、EAP-PWD、EAP-EKE、EAP-IKEV2、WPS；hostap 中没有 PSA bignum
   * - ECDH / EC 密钥操作
     - 旧版
     - DPP、SAE-PK、EAP-PWD（EC）。当 ``MBEDTLS_ECDH_C`` / ``CONFIG_PSA_WANT_ALG_ECDH`` 时可能由 PSA 支持；封装层通用
   * - TLS/SSL
     - 旧版
     - EAP-TLS、EAP-TTLS、EAP-PEAP；完整协议栈位于 ``tls_mbedtls_alt.c`` 中
   * - RSA
     - 旧版
     - TLS, X.509
   * - X.509 / CSR
     - 旧版
     - 解析与生成
   * - WEP
     - 旧版
     - 无 PSA 路径

因此：**WPA2-PSK 和 WPA2-PSK-256** 的 crypto 仅使用 PSA；**WPA3-SAE** 、**DPP** 、**SAE-PK** 、**WPS** 和 **Enterprise EAP** 仍依赖旧版 bignum、EC 或 TLS。有关每项功能的影响，请参见上方的功能表。
