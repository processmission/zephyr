.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _binary_descriptors:

二进制描述符
############

二进制描述符是存放二进制可执行文件相关信息的常量数据对象。与“常规”常量不同，二进制描述符被链接到二进制文件中已知的偏移位置，因此其他程序（例如同一设备上运行的另一镜像或主机工具）可以访问它们。适合用作二进制描述符的常量示例包括：内核版本、应用版本、构建时间、编译器版本、环境变量、编译主机名等。

二进制描述符使用 ``DEFINE_BINDESC_*`` 宏创建。例如：

.. code-block:: c

   #include <zephyr/bindesc.h>

   BINDESC_STR_DEFINE(my_string, 2, "Hello world!"); // Unique ID is 2

随后可以通过以下方式访问 ``my_string``：

.. code-block:: c

   printk("my_string: %s\n", BINDESC_GET_STR(my_string));

也可以通过 ``west bindesc`` 获取：

.. code-block:: bash

   $ west bindesc custom_search STR 2 build/zephyr/zephyr.bin
   "Hello world!"

实现原理
********
二进制描述符使用 TLV（tag、length、value）头部实现，并链接到二进制镜像中已知的偏移位置。该偏移因架构而异，但通常描述符会被链接到尽可能靠近镜像开头的位置。在镜像必须以向量表开头的架构（如 ARM）中，描述符被链接在向量表之后。复位向量指向 text 段的起始位置，也就是描述符之后。在镜像必须以可执行代码开头的架构（如 x86）中，会在镜像开头注入一条跳转指令，以跳过紧随其后的二进制描述符。

每个 tag 都是一个 16 位无符号整数，其中最高半字节（4 位）表示类型（目前为 uint、string 或 bytes），其余部分表示 ID。ID 对每个描述符全局唯一。例如，应用版本字符串的 ID 为 ``0x800``，字符串用 0x1 表示，因此应用版本 tag 为 ``0x1800``。length 是一个 16 位数值，等于数据长度（以字节为单位）。data 是描述符的实际取值。所有二进制描述符数值（magic、tag、uint）在内存中都按 SoC 原生字节序存放。``west bindesc`` 默认假定为小端，因此如果镜像属于大端 SoC，应给该工具指定相应的标志。

二进制描述符头部以魔数 ``0xb9863e5a7ea46046`` 开头，其后是各个 TLV，最后以 ``DESCRIPTORS_END`` （``0xffff``）tag 结束。tag 始终按 32 位对齐。如果前一个描述符的取值长度未对齐，则会添加零填充以确保当前 tag 对齐。

综合起来，上面的示例在小端 SoC 内存中的布局如下：

.. code-block::

    46 60 a4 7e 5a 3e 86 b9 02 10  0d 00  48 65 6c 6c 6f 20 77 6f 72 6c 64 21 00 00 00 00 ff ff 00 00
   |         magic         | tag |length| H  e  l  l  o     w  o  r  l  d  !    |   pad  |    end    |

用法
****
二进制描述符始终通过 ``BINDESC_*_DEFINE`` 宏创建。如上面的示例所示，可以从任意字符串或整数生成描述符，并使用任意 ID。不过建议遵循 ``include/zephyr/bindesc.h`` 中定义的标准 tag，这样做有以下好处：

 1. ``west bindesc`` 工具能够识别该描述符的含义并打印有意义的 tag
 2. 可以保证来自不同来源的各个应用保持一致
 3. 便于把描述符生成功能合入上游（参见标准描述符）

要使用标准 tag 定义描述符，只需使用从 ``bindesc.h`` 引入的 tag：

.. code-block:: c

   #include <zephyr/bindesc.h>

   BINDESC_STR_DEFINE(app_version, BINDESC_ID_APP_VERSION_STRING, "1.2.3");

标准描述符
==========
有些描述符实现起来很简单，因此可以在上游 Zephyr 中以标准方式实现。这样就可以通过 Kconfig 启用它们，而不必让每个用户重新实现。这些描述符包括构建时间、内核版本和主机信息。例如，要以字符串形式添加构建日期和时间，应启用以下配置：

.. code-block:: kconfig

   # Enable binary descriptors
   CONFIG_BINDESC=y

   # Enable definition of binary descriptors
   CONFIG_BINDESC_DEFINE=y

   # Enable default build time binary descriptors
   CONFIG_BINDESC_DEFINE_BUILD_TIME=y
   CONFIG_BINDESC_BUILD_DATE_TIME_STRING=y

为避免与用户自定义描述符冲突，标准描述符分配了 ``0x800-0xfff`` 范围，而 ``0x000-0x7ff`` 留给用户。更多信息请阅读这些 Kconfig 符号的 ``help`` 部分。按照约定，每个 Kconfig 符号对应一个二进制描述符，其名称是该 Kconfig 名称去掉 ``CONFIG_BINDESC_`` 后的小写形式。例如，``CONFIG_BINDESC_KERNEL_VERSION_STRING`` 创建的描述符可以用 ``BINDESC_GET_STR(kernel_version_string)`` 访问。

读取描述符
==========
应用也可以读取和解析二进制描述符。这既适用于镜像读取自身的描述符，也适用于镜像读取另一个镜像的描述符。读取可以通过以下三种后端之一完成：

 #. RAM - 假定描述符已被（例如被引导加载程序）复制到 RAM，则可以从它们所处的缓冲区中读取。

 #. 内存映射 flash - 如果要读取的镜像位于 flash 中，并且可以通过程序地址空间访问，则可以直接从 flash 读取。此选项占用的 RAM 最少，但如果 flash 未做内存映射就无法使用；出于安全考虑，也不建议用它读取引导加载程序的描述符。

 #. Flash - 使用内部缓冲区，通过 flash API 逐个读取描述符，并在它们位于缓冲区期间交给用户。

要启用描述符读取功能，请启用 :kconfig:option:`CONFIG_BINDESC_READ`。这三种后端分别由以下 Kconfig 符号启用：:kconfig:option:`CONFIG_BINDESC_READ_RAM`、:kconfig:option:`CONFIG_BINDESC_READ_MEMORY_MAPPED_FLASH` 和 :kconfig:option:`CONFIG_BINDESC_READ_FLASH`。

要读取描述符，应首先初始化一个描述符句柄：

.. code-block:: c

   struct bindesc_handle handle;

   /* Assume buffer holds a copy of the descriptors */
   bindesc_open_ram(&handle, buffer);

``bindesc_open_*`` 函数是唯一与所用后端相关的函数，API 的其余部分与数据所在位置无关。句柄初始化后，即可与 API 的其余部分一起使用：

.. code-block:: c

   char *version;
   bindesc_find_str(&handle, BINDESC_ID_KERNEL_VERSION_STRING, &version);
   printk("Kernel version: %s\n", version);

west bindesc 工具
=================
``west`` 能够解析并显示给定可执行镜像中的二进制描述符。

更多信息请参阅 ``west bindesc --help`` 或 :ref:`文档<west-bindesc>`。

API 参考
********

.. doxygengroup:: bindesc_define

.. doxygengroup:: bindesc_read
