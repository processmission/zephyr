.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _random_api:

随机数生成
##########

概述
****

随机 API 子系统同时提供密码学安全和非密码学安全的随机数生成 API。使用哪种随机 API 取决于随机数的密码学要求。如果只需要非密码学随机值，非密码学 API 返回随机值的速度要快得多。

- 将 :c:func:`sys_rand_get` 及相关函数用于非密码学用途，例如随机化延时、打乱数据或通用随机化。这些函数速度更快，但不适合用于安全应用。

- 将 :c:func:`sys_csrand_get` 用于密码学用途，例如生成加密密钥、nonce、初始化向量，或任何必须对攻击者不可预测的数据。

.. warning::

   切勿将非密码学随机函数（:c:func:`sys_rand_get`、:c:func:`sys_rand8_get`、:c:func:`sys_rand16_get`、:c:func:`sys_rand32_get`、:c:func:`sys_rand64_get`）用于安全敏感操作。这些函数不提供密码学安全的随机数。

API 用法
********

非密码学安全随机数
==================

以下函数提供非密码学安全的随机数：

- :c:func:`sys_rand_get` - 用随机字节填充缓冲区
- :c:func:`sys_rand8_get` - 获取一个随机 8 位值
- :c:func:`sys_rand16_get` - 获取一个随机 16 位值
- :c:func:`sys_rand32_get` - 获取一个随机 32 位值
- :c:func:`sys_rand64_get` - 获取一个随机 64 位值

用法示例：

.. code-block:: c

   #include <zephyr/random/random.h>

   void example_random_usage(void)
   {
       uint8_t buffer[16];
       uint32_t random_value;

       /* Fill buffer with random bytes */
       sys_rand_get(buffer, sizeof(buffer));

       /* Get a single random 32-bit value */
       random_value = sys_rand32_get();
   }

密码学安全随机数
================

对于密码学用途，请使用 :c:func:`sys_csrand_get`：

.. code-block:: c

   #include <zephyr/random/random.h>

   int generate_encryption_key(uint8_t *key, size_t key_len)
   {
       int ret;

       ret = sys_csrand_get(key, key_len);
       if (ret != 0) {
           /* Handle error - entropy source may have failed */
           return ret;
       }

       return 0;
   }

.. note::

   :c:func:`sys_csrand_get` 成功时返回 0，如果熵源失败则返回 ``-EIO``。生成密码学材料时，务必检查返回值。

.. _random_kconfig:

Kconfig 选项
************

所有配置选项均可在 :zephyr_file:`subsys/random/Kconfig` 中找到。

通用选项
========

:kconfig:option:`CONFIG_TEST_RANDOM_GENERATOR`
 用于测试时，此选项允许使用非随机数生成器，并允许随机数 API 返回并非真正随机的值。

 .. warning::

    此选项仅用于在不具备硬件熵源支持的平台上进行测试。启用此选项后生成的随机数可预测，不适合任何安全敏感用途。

非密码学随机数生成器选择

:kconfig:option:`CONFIG_ENTROPY_DEVICE_RANDOM_GENERATOR`
   直接使用硬件熵驱动生成随机数。这样可以提供高质量的随机数，但可能比伪随机方案更慢。当硬件熵源的性能足以满足应用需求时，请选择此选项。

:kconfig:option:`CONFIG_XOSHIRO_RANDOM_GENERATOR`
   使用由硬件熵源播种的 Xoshiro128++ 伪随机数生成器。这是一种快速的通用 PRNG，具有 128 位状态，可通过所有标准随机性测试。

   对于大多数需要快速非密码学随机数的应用，这是推荐选择。

:kconfig:option:`CONFIG_TIMER_RANDOM_GENERATOR`
   使用系统定时器生成伪随机数。此生成器产生的值可预测，在不具备硬件熵源支持的平台上 **仅用于测试**。

   要求启用 :kconfig:option:`CONFIG_TEST_RANDOM_GENERATOR`。

密码学安全随机数生成器选择
==========================

:kconfig:option:`CSPRNG_GENERATOR_CHOICE` Kconfig 选择项用于选择密码学安全随机数生成的来源。

要在开发板或 SoC 配置文件中覆盖默认值：

.. code-block:: kconfig

   choice CSPRNG_GENERATOR_CHOICE
           default PSA_CSPRNG_GENERATOR
   endchoice

可用的生成器：

:kconfig:option:`CONFIG_HARDWARE_DEVICE_CS_GENERATOR`
 直接使用硬件熵驱动作为密码学安全随机数的来源。当硬件随机数生成器已通过密码学用途的认证或验证时，请选择此项。

:kconfig:option:`CONFIG_PSA_CSPRNG_GENERATOR`
 启用使用 PSA Crypto API 的密码学安全随机数生成器。此 CSPRNG 实现利用底层 PSA Crypto 库的安全随机数生成能力，在硬件熵源可用时可能会使用这些熵源。PSA CSPRNG 提供适合安全敏感应用的密码学安全随机数。

:kconfig:option:`CONFIG_TEST_CSPRNG_GENERATOR`
 将对 :c:func:`sys_csrand_get` 的调用路由到 :c:func:`sys_rand_get`。这样可以在不具备硬件熵源支持的平台上测试需要 CSPRNG 的库。

 要求启用 :kconfig:option:`CONFIG_TEST_RANDOM_GENERATOR`。

 .. warning::

    此选项 **不提供密码学安全性**。仅用于测试。

Devicetree 配置
***************

随机数子系统使用 ``zephyr,entropy`` chosen 节点来标识硬件熵设备：

.. code-block:: devicetree

   / {
       chosen {
           zephyr,entropy = &rng;
       };
   };

如果平台具有硬件随机数生成器，请确保开发板的 Devicetree 正确指定此 chosen 节点。

API 参考
********

.. doxygengroup:: random_api
