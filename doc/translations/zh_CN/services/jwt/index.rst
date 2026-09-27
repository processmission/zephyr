.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _jwt_api:

JSON Web Token (JWT)
####################

概述
****

JSON Web Token（JWT）是一种开放的行业标准方法（:rfc:`7519`），用于安全地在两方之间表示声明。尽管 JWT 相当灵活，但此 API 仅限于创建向 Google Core IoT 基础设施进行身份验证所需的简单令牌。

从较高层面来看，JWT 只是一个经过签名的 JSON 数据块，客户端可以将其作为令牌出示，而不必每次都发送用户名/密码等信息。

用法
====

要使用 JWT API，请包含以下头文件：

.. code-block:: c

   #include <zephyr/data/jwt.h>

生成 JWT
--------

JWT 子系统提供了一个轻量级的、基于构建器的 API，用于构造 JSON Web Token（JWT）。它允许创建的令牌，其负载（声明）包含：过期时间、签发时间和受众。然后使用提供的私钥对该令牌进行签名。

.. code-block:: c

   #include <zephyr/data/jwt.h>

   struct jwt_builder builder;
   char buffer[1024];
   int ret;

   /* Initialize the builder */
   ret = jwt_init_builder(&builder, buffer, sizeof(buffer));
   if (ret < 0) {
       /* Handle error */
   }

   /* Add payload: expiration, issued at, audience */
   ret = jwt_add_payload(&builder, 1767221999, 1764605987, "project-id");
   if (ret < 0) {
       /* Handle error */
   }

   /* Sign the token using a DER-encoded private key */
   ret = jwt_sign(&builder, private_key_der, private_key_der_len);
   if (ret < 0) {
       /* Handle error */
   }

   /*
    * buffer now contains the JWT; it can be passed to a third-party service that will be able
    * to validate it against the public key associated with `private_key_der`.
    */

配置
****

相关配置选项：

* :kconfig:option:`CONFIG_JWT`
* :kconfig:option-regex:`CONFIG_JWT_.*`


API 参考
********

.. doxygengroup:: jwt
