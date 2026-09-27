.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _biometrics_api:

生物识别
########

概述
****

生物识别 API 为指纹扫描仪、虹膜扫描仪和人脸识别模块等生物识别传感器提供统一接口。这些传感器通常用于嵌入式系统、门禁设备和 IoT 应用中的安全身份验证。

该 API 支持生物识别操作的完整生命周期，包括录入、模板管理和匹配。根据硬件能力，传感器可以将模板存储在设备本地或主机系统上。

典型的指纹录入过程需要多次采集同一根手指的样本，以创建可靠的模板。匹配过程将采集到的样本与已存储的模板进行比较，以验证身份。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_BIOMETRICS`
* :kconfig:option:`CONFIG_BIOMETRICS_INIT_PRIORITY`

API 参考
********

.. doxygengroup:: biometrics_interface
