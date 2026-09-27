.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_wolfssl:

wolfSSL
#######

简介
****

wolfSSL 是针对嵌入式系统、RTOS 环境及资源受限设备优化的轻量级、可移植 SSL/TLS 库。它提供多种密码学功能、安全通信协议（最高支持 TLS 1.3 和 DTLS 1.3），以及后量子密码学支持。多种构建配置使它适用于使用 Zephyr RTOS 的各类应用和硬件平台。

wolfSSL 支持 Zephyr 网络协议栈，应用可通过其 API，经网络与其他设备或服务建立安全连接。

wolfSSL 同时提供 GPLv3 和商业许可证。

GitHub 仓库：`wolfSSL Repository`_

在 Zephyr 中使用
****************

将 wolfssl 作为项目添加到 west.yml：

.. code-block:: yaml

  manifest:
    remotes:
    # <your other remotes>
    - name: wolfssl
      url-base: https://github.com/wolfssl
  projects:
    # <your other projects>
    - name: wolfssl
      path: modules/crypto/wolfssl
      revision: master
      remote: wolfssl

更新 west 模块：

.. code-block:: bash

   west update

现在 west 会将 ``wolfssl`` 识别为模块，并将其 Kconfig 和 CMakeLists.txt 纳入构建系统。

在 Zephyr 中使用 wolfSSL 的更多说明见 `wolfSSL Zephyr Example Usage`_。

Zephyr 应用代码示例见 `wolfSSL NXP AppCodeHub`_。

wolfSSL API 文档见 `wolfSSL Documentation`_。

参考资料
********

.. target-notes::

.. _wolfssl Repository:
    https://github.com/wolfSSL/wolfssl

.. _wolfSSL Zephyr Example Usage:
    https://github.com/wolfSSL/wolfssl/blob/master/zephyr/README.md#build-and-run-wolfcrypt-benchmark-application

.. _wolfSSL NXP AppCodeHub:
    https://github.com/wolfSSL/nxp-appcodehub

.. _wolfSSL Documentation:
    https://www.wolfssl.com/docs/
