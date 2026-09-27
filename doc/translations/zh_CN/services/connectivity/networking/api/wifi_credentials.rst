.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _lib_wifi_credentials:

Wi-Fi 凭据库
############

.. contents::
   :local:
   :depth: 2

Wi-Fi 凭据库提供加载和存储 Wi-Fi® 网络凭据的方法。

概述
****

该库使用 Zephyr 的 settings 子系统或平台安全架构（PSA）内部可信存储（ITS）来存储凭据。它还在 RAM 中保存 SSID 列表，以便使用 SSID 作为键进行类似字典的访问。

配置
****

要使用 Wi-Fi 凭据库，请启用 :kconfig:option:`CONFIG_WIFI_CREDENTIALS` Kconfig 选项。

可以使用以下选项选择后端：

* :kconfig:option:`CONFIG_WIFI_CREDENTIALS_BACKEND_PSA` —— 非安全目标的默认选项，其中包含 TF-M 分区（非最小 TF-M 配置文件类型）。
* :kconfig:option:`CONFIG_WIFI_CREDENTIALS_BACKEND_SETTINGS` —— 安全目标的默认选项。

要配置最大网络数量，请使用 :kconfig:option:`CONFIG_WIFI_CREDENTIALS_MAX_ENTRIES` Kconfig 选项。

IEEE 802.11 标准未规定 SAE 密码的最大长度。要更改默认值，请使用 :kconfig:option:`CONFIG_WIFI_CREDENTIALS_SAE_PASSWORD_LENGTH` Kconfig 选项。

添加凭据
********

可以使用 :c:func:`wifi_credentials_set_personal` 和 :c:func:`wifi_credentials_set_personal_struct` 函数添加凭据。前者会根据给定字段构建内部使用的结构体，后者则直接接收结构体。如果两次添加具有相同 SSID 的凭据，旧条目将被覆盖。

查询凭据
********

给定 SSID 后，可以使用 :c:func:`wifi_credentials_get_by_ssid_personal` 和 :c:func:`wifi_credentials_get_by_ssid_personal_struct` 函数查询凭据。

可以使用 :c:func:`wifi_credentials_for_each_ssid` 函数遍历所有已存储的凭据。允许在遍历过程中删除或覆盖凭据，因为这些操作不会更改内部索引。

移除凭据
********

可以使用 :c:func:`wifi_credentials_delete_by_ssid` 函数移除凭据。

Shell 命令
**********

``wifi cred`` 是 Wi-Fi 命令行的扩展。它添加了以下子命令，用于与 Wi-Fi 凭据库交互：

.. list-table:: Wi-Fi 凭据 shell 子命令
   :header-rows: 1

   * - 子命令
     - 描述
   * - add
     - | 使用以下参数向凭据存储区添加网络：
       | <-s --ssid \"<SSID>\">: SSID.
       | [-c --channel]：需要为连接扫描的通道。0：任意通道
       | [-b, --band] 0：任意频段（2：2.4GHz，5：5GHz，6：6GHz）
       | [-p, --passphrase]：密码短语（仅对安全 SSID 有效）
       | [-k, --key-mgmt]：密钥管理类型。
       | 0:None, 1:WPA2-PSK, 2:WPA2-PSK-256, 3:SAE-HNP, 4:SAE-H2E, 5:SAE-AUTO, 6:WAPI,"
       | " 7:EAP-TLS, 8:WEP, 9: WPA-PSK, 10: WPA-Auto-Personal, 11: DPP
       | [-w, --ieee-80211w]：MFP（可选：需要指定安全类型）
       | : 0：禁用，1：可选，2：必需。
       | [-m, --bssid]：AP 的 MAC 地址（BSSID）。
       | [-t, --timeout]：连接尝试失败前允许的持续时间。
       | [-a, --identity]：企业模式的身份标识。
       | [-K, --key-passwd]：企业模式的私钥密码。
       | [-h, --help]：打印 connect 命令的帮助信息。
   * - delete <SSID>
     - 从凭据存储区移除网络。
   * - list
     - 列出凭据存储区中的网络。
   * - auto_connect
     - 自动连接到任意已存储的网络。

限制
****

该库具有以下限制：

* 尽管 IEEE 802.11 标准允许，但该库不支持零长度 SSID。
* 仅部分支持 Wi-Fi 保护访问（WPA）企业级凭据。
* 存储的网络数量在编译时固定。

API 文档
********

以下小节概述并参考 Zephyr 中可用的 Wi-Fi 凭据 API：

.. doxygengroup:: wifi_credentials
