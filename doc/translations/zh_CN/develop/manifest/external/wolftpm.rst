.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_wolftpm:

wolfTPM
#######

简介
****

wolfTPM 是针对嵌入式系统、RTOS 环境及资源受限设备优化的轻量级、可移植 TPM 2.0 库，提供完整 TPM 2.0 实现，支持密码学操作、密钥生成、安全存储和证明。

wolfTPM 已作为 Zephyr 模块集成，并提供 CMake 和 Kconfig 支持，便于将 TPM 功能加入任意 Zephyr 项目。模块支持通过设备树配置与 TPM 设备的 I2C 通信：在 ``user_settings.h`` 中，将 ``WOLFTPM_ZEPHYR_I2C_BUS`` 设为描述设备 I2C 总线的节点，并通过 ``WOLFTPM_ZEPHYR_I2C_SPEED`` 设置 I2C 速度。

wolfTPM 同时提供 GPLv3 和商业许可证。

GitHub 仓库：`wolfTPM Repository`_

要求
****

* :ref:`external_module_wolfssl`，用于密码学操作

在 Zephyr 中使用
****************

将 wolfTPM 作为项目添加到 west.yml：

.. code-block:: yaml

  manifest:
    remotes:
    # <your other remotes>
    - name: wolftpm
      url-base: https://github.com/wolfssl
  projects:
    # <your other projects>
    - name: wolftpm
      path: modules/crypto/wolftpm
      revision: v3.10.0
      remote: wolftpm

.. note::

   上述 revision 仅为示例。请在 `wolfTPM Repository`_ 发布页面查看最新发布标签，确保选择所需版本。

更新 west 模块：

.. code-block:: bash

   west update

现在 west 会将 ``wolftpm`` 识别为模块，并将其 Kconfig 和 CMakeLists.txt 纳入构建系统。

示例应用
********

wolfTPM 提供两个 Zephyr 示例应用：

* **wolftpm_wrap_test** —— 测试 TPM 封装的核心功能
* **wolftpm_wrap_caps** —— 显示 TPM 能力

两个示例均可在 qemu_x86 上成功构建和运行，可作为开发基础。

配置
****

模块使用 ``user_settings.h`` 配置文件，可按项目需求自定义。与 TPM 设备进行 I2C 通信时，配置以下选项：

* ``WOLFTPM_ZEPHYR_I2C_BUS`` —— 设为描述 I2C 总线的设备树节点
* ``WOLFTPM_ZEPHYR_I2C_SPEED`` —— 设置 I2C 线路速度

其他资源
********

在 Zephyr 中使用 wolfTPM 的更多说明见 `wolfTPM Zephyr Example Usage`_ 和 `wolfTPM Zephyr Announcement`_。

Zephyr 应用代码示例见 `wolfSSL NXP AppCodeHub`_。

wolfTPM API 文档见 `wolfTPM Documentation`_。

参考资料
********

.. target-notes::

.. _wolfTPM Repository:
    https://github.com/wolfSSL/wolfTPM

.. _wolfTPM Zephyr Example Usage:
    https://github.com/wolfSSL/wolfTPM/blob/master/zephyr/README.md

.. _wolfSSL NXP AppCodeHub:
    https://github.com/wolfSSL/nxp-appcodehub

.. _wolfTPM Documentation:
    https://www.wolfssl.com/documentation/manuals/wolftpm/

.. _wolfTPM Zephyr Announcement:
    https://www.wolfssl.com/wolftpm-support-for-zephyr-rtos/
