.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_wolfssh:

wolfSSH
#######

简介
****

wolfSSH 是针对嵌入式系统、RTOS 环境及资源受限设备优化的轻量级、可移植 SSH 库。它提供安全 shell 功能，包括 SSH 服务端和客户端实现，以及 SCP、SFTP 支持。多种构建配置使它适用于使用 Zephyr RTOS 的各类应用和硬件平台。

wolfSSH 支持 Zephyr 网络协议栈，应用可通过其 API，经网络与其他设备或服务建立安全 SSH 连接。

wolfSSH 同时提供 GPLv3 和商业许可证。

GitHub 仓库：`wolfSSH Repository`_

要求
****

* :ref:`external_module_wolfssl`，用于密码学操作

在 Zephyr 中使用
****************

将 wolfSSH 作为项目添加到 west.yml：

.. code-block:: yaml

  manifest:
    remotes:
    # <your other remotes>
    - name: wolfssh
      url-base: https://github.com/wolfssl
  projects:
    # <your other projects>
    - name: wolfssh
      path: modules/lib/wolfssh
      revision: master
      remote: wolfssh

更新 west 模块：

.. code-block:: bash

   west update

现在 west 会将 ``wolfssh`` 识别为模块，并将其 Kconfig 和 CMakeLists.txt 纳入构建系统。

在 Zephyr 中使用 wolfSSH 的更多说明见 `wolfSSH Zephyr Example Usage`_。

Zephyr 应用代码示例见 `wolfSSL NXP AppCodeHub`_。

wolfSSH API 文档见 `wolfSSH Documentation`_。

参考资料
********

.. target-notes::

.. _wolfSSH Repository:
    https://github.com/wolfSSL/wolfssh

.. _wolfSSH Zephyr Example Usage:
    https://github.com/wolfSSL/wolfssh/blob/master/zephyr/README.md#build-and-run-samples

.. _wolfSSL NXP AppCodeHub:
    https://github.com/wolfSSL/nxp-appcodehub

.. _wolfSSH Documentation:
    https://www.wolfssl.com/documentation/manuals/wolfssh/
