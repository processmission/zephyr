.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_wolfmqtt:

wolfMQTT
########

简介
****

wolfMQTT 是针对嵌入式系统、RTOS 环境及资源受限设备优化的轻量级、可移植 MQTT 客户端库，支持 MQTT v3.1.1 和 v5.0。它提供 QoS 0—2 级、遗嘱消息（LWT）等功能，并兼容多种 MQTT 消息代理。多种构建配置使它适用于使用 Zephyr RTOS 的各类物联网应用和硬件平台。

wolfMQTT 支持 Zephyr 网络协议栈，应用可通过其 API，经网络与消息代理及其他设备或服务建立 MQTT 连接。

wolfMQTT 同时提供 GPLv3 和商业许可证。

GitHub 仓库：`wolfMQTT Repository`_

要求
****

* :ref:`external_module_wolfssl`，用于安全通信（TLS 支持）

在 Zephyr 中使用
****************

将 wolfMQTT 作为项目添加到 west.yml：

.. code-block:: yaml

  manifest:
    remotes:
    # <your other remotes>
    - name: wolfmqtt
      url-base: https://github.com/wolfssl
  projects:
    # <your other projects>
    - name: wolfmqtt
      path: modules/lib/wolfmqtt
      revision: v1.21.0
      remote: wolfmqtt

.. note::

   上述 revision 仅为示例。请在 `wolfMQTT Repository`_ 发布页面查看最新发布标签，确保选择所需版本。

更新 west 模块：

.. code-block:: bash

   west update

现在 west 会将 ``wolfmqtt`` 识别为模块，并将其 Kconfig 和 CMakeLists.txt 纳入构建系统。

在 Zephyr 中使用 wolfMQTT 的更多说明见 `wolfMQTT Zephyr Example Usage`_。

Zephyr 应用代码示例见 `wolfSSL NXP AppCodeHub`_。

wolfMQTT API 文档见 `wolfMQTT Documentation`_。

参考资料
********

.. target-notes::

.. _wolfMQTT Repository:
    https://github.com/wolfSSL/wolfMQTT

.. _wolfMQTT Zephyr Example Usage:
    https://github.com/wolfSSL/wolfMQTT/tree/master/zephyr

.. _wolfSSL NXP AppCodeHub:
    https://github.com/wolfSSL/nxp-appcodehub

.. _wolfMQTT Documentation:
    https://www.wolfssl.com/documentation/manuals/wolfmqtt/
