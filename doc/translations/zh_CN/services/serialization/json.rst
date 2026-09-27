.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _json_api:

JSON
####

Zephyr 提供了一个 JSON 库，可用于对 JSON 数据进行编码和解码。

用法
****

定义数据结构
============

首先，定义与 JSON 对象对应的 C 结构体，以及将结构体字段映射到 JSON 标记的描述符。

.. code-block:: c

   #include <zephyr/data/json.h>

   struct foo {
       int bar;
       const char *baz;
   };

   static const struct json_obj_descr foo_descr[] = {
       JSON_OBJ_DESCR_PRIM(struct foo, bar, JSON_TOK_NUMBER),
       JSON_OBJ_DESCR_PRIM(struct foo, baz, JSON_TOK_STRING),
   };

编码
====

要将 C 结构体编码为 JSON 字符串，请使用 :c:func:`json_obj_encode_buf`。

.. code-block:: c

   void encode_example(void)
   {
       struct foo data = { .bar = 42, .baz = "hello" };
       char buffer[128];
       int ret;

       ret = json_obj_encode_buf(foo_descr, ARRAY_SIZE(foo_descr),
                                 &data,
                                 buffer, sizeof(buffer));
       if (ret < 0) {
           /* handle error */
       }
   }

解码
====

要将 JSON 字符串解码为 C 结构体，请使用 :c:func:`json_obj_parse`。

.. code-block:: c

   void decode_example(void)
   {
       struct foo data;
       const char *json_text = "{\"bar\": 42, \"baz\": \"hello\"}";
       int ret;

       ret = json_obj_parse(json_text, strlen(json_text),
                            foo_descr, ARRAY_SIZE(foo_descr),
                            &data);
       if (ret < 0) {
           /* handle error */
       }
   }

配置
****

要启用 JSON 支持，请启用 :kconfig:option:`CONFIG_JSON_LIBRARY` Kconfig 选项。

API 参考
********

.. doxygengroup:: json
