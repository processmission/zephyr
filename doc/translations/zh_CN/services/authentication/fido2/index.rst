.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _fido2_api:

FIDO2 认证器
############

概述
****

FIDO2 认证器子系统实现了 `FIDO2 CTAP2 Specification`_ （Client to Authenticator Protocol，客户端到认证器协议），使 Zephyr 设备可以用作无密码认证的硬件安全密钥。该子系统可以通过 :kconfig:option:`CONFIG_FIDO2` 选项启用。

FIDO2 安全密钥与 `WebAuthn Specification`_ Web 标准配合使用。依赖方（网站或服务）通过客户端（浏览器或操作系统平台）与认证器交互，以注册和验证用户凭据。认证器使用永不离开硬件的设备内密钥执行密码学操作。

该子系统目前支持以下 CTAP2 命令：

- ``authenticatorMakeCredential``
- ``authenticatorGetAssertion``
- ``authenticatorGetInfo``
- ``authenticatorClientPIN``
- ``authenticatorGetNextAssertion``
- ``authenticatorSelection``

架构
****

该子系统由可插拔的后端组件组成，每个组件都可以在构建时通过 Kconfig 选择：

传输
   处理主机与认证器之间的线协议通信。传输通过 :c:macro:`FIDO2_TRANSPORT_DEFINE` 宏注册，并在启动时遍历。可用的传输：

   - **USB HID（CTAPHID）** — :kconfig:option:`CONFIG_FIDO2_TRANSPORT_USB_HID`
   - **Bluetooth LE（CTAPBLE）** — :kconfig:option:`CONFIG_FIDO2_TRANSPORT_BLE`

用户在场（UP）
   确认有真人实际在场。后端通过 :kconfig:option:`CONFIG_FIDO2_UP_BACKEND` 选择：

   - **输入设备** — :kconfig:option:`CONFIG_FIDO2_UP_INPUT`
   - **始终批准** — :kconfig:option:`CONFIG_FIDO2_UP_ALWAYS`
   - **自定义** — :kconfig:option:`CONFIG_FIDO2_UP_CUSTOM` （由应用提供）

凭据存储
   持久保存可发现（常驻）凭据。后端通过 :kconfig:option:`CONFIG_FIDO2_STORAGE_BACKEND` 选择：

   - **设置子系统** — :kconfig:option:`CONFIG_FIDO2_STORAGE_SETTINGS`
   - **无** — :kconfig:option:`CONFIG_FIDO2_STORAGE_NONE` （仅支持不可发现的凭据）

证明
   对新创建的凭据签名以证明其来源。后端通过 :kconfig:option:`CONFIG_FIDO2_ATTESTATION_BACKEND` 选择：

   - **自证明** — :kconfig:option:`CONFIG_FIDO2_ATTESTATION_SELF` （默认）
   - **无** — :kconfig:option:`CONFIG_FIDO2_ATTESTATION_NONE`
   - **自定义** — :kconfig:option:`CONFIG_FIDO2_ATTESTATION_CUSTOM` （由应用提供）

用法
****

要使用 FIDO2 子系统，请包含主头文件：

.. code-block:: c

   #include <zephyr/authentication/fido2/fido2.h>

基本初始化
==========

认证器要能与主机通信，必须至少启用一种传输。

完整的初始化流程请参见 :zephyr:code-sample:`fido2`。

运行时状态监控
==============

该子系统提供一个运行时状态回调，应用可以用它驱动 LED 等状态指示器：

.. code-block:: c

   #include <zephyr/authentication/fido2/fido2.h>

   static void on_state_change(enum fido2_runtime_state state, void *user_data)
   {
       switch (state) {
       case FIDO2_RUNTIME_STATE_IDLE:
           /* LED off */
           break;
       case FIDO2_RUNTIME_STATE_WAITING_USER_PRESENCE:
           /* Blink LED */
           break;
       case FIDO2_RUNTIME_STATE_PROCESSING:
           /* LED on solid */
           break;
       default:
           break;
       }
   }

   fido2_set_state_callback(on_state_change, NULL);

扩展
****

CTAP2 扩展尚未实现。以下 Kconfig 选项是为将来实现保留的：

- **credProtect** — :kconfig:option:`CONFIG_FIDO2_EXT_CRED_PROTECT`
- **hmac-secret** — :kconfig:option:`CONFIG_FIDO2_EXT_HMAC_SECRET`
- **largeBlobKey** — :kconfig:option:`CONFIG_FIDO2_EXT_LARGE_BLOB_KEY`
- **credBlob** — :kconfig:option:`CONFIG_FIDO2_EXT_CRED_BLOB`
- **thirdPartyPayment** — :kconfig:option:`CONFIG_FIDO2_EXT_THIRD_PARTY_PAYMENT`

参考资料
********

* `FIDO2 CTAP2 Specification`_

.. _FIDO2 CTAP2 Specification:
   https://fidoalliance.org/specs/fido-v2.2-rd-20230321/fido-client-to-authenticator-protocol-v2.2-rd-20230321.html

* `WebAuthn Specification`_

.. _WebAuthn Specification:
   https://www.w3.org/TR/webauthn-2/

* `FIDO Alliance`_

.. _FIDO Alliance:
   https://fidoalliance.org/

API 参考
********

.. doxygengroup:: fido2
