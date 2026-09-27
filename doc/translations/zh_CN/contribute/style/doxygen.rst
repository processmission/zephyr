.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _doxygen_style:

Doxygen 风格指南
################

Zephyr 项目使用 `Doxygen`_ 从源代码注释生成 API 文档。本指南定义了以一致方式记录 Zephyr 公共 API 的约定。

即使本文档没有明确列出，所有 `Doxygen commands`_ 也都可以使用。

.. _Doxygen: https://www.doxygen.nl/
.. _Doxygen commands: https://www.doxygen.nl/manual/commands.html

要在本地构建并预览 Zephyr 的 Doxygen 文档，请参阅 :ref:`zephyr_doc`。

通用规则
********

所有 :term:`公共头文件及其公共 API 符号 <public API>` （函数、结构体、枚举、联合体、typedef、宏和全局变量）：

- 必须有完整的文档（例外情况请参阅 :ref:`doxygen_internals`）
- 必须属于至少一个 Doxygen 分组（请参阅 :ref:`doxygen_groups`）

记录公共 API 时必须使用以下语法：

- 使用 ``/**`` 开始块注释，使用 ``*/`` 结束块注释。
- 使用 ``/**<`` 表示与符号位于同一行的尾随注释。
- Doxygen 命令使用 ``@`` 而不是反斜杠（例如使用 ``@param`` 而不是 ``\param``）。
- ``@brief`` 命令是可选的。如果不使用它，则第一句话（以句号结尾）会被视为简要描述。

仅供内部使用的构造必须从公共文档中隐藏，如 :ref:`doxygen_internals` 所述。

需要记录的内容
==============

对于任何接受、返回或存储值的 API 元素（函数参数、返回值、结构体/联合体成员、枚举值、typedef 和宏），其文档在适用时必须描述以下内容：

语义
  该元素表示什么，以及调用者/用户应如何解释它。不要重复标识符或 C 类型。

  示例：

  - 避免： ``@param timeout Timeout value in ms.``
  - 推荐： ``@param timeout Maximum time to wait before returning, in milliseconds.``

有效取值
  接受哪些值，以及如何解释它们。请指定以下一项或多项：

  - 范围：最小/最大值（例如类型为 ``uint8_t``，但只有 0–100 是有效的）。
  - 离散集合：在只允许某个子集时，给出允许的值。
  - 枚举：该值是否必须是给定枚举的有效成员（以及是允许所有枚举项还是只允许其中一部分）。
  - 标志位/位掩码：哪些位是有效的，以及是否允许组合。
  - 可为空性：指针值是否允许为 ``NULL``，以及这表示什么。

单位
  当该值表示一个量时，请指明单位和基准（例如毫秒与 tick、赫兹、字节）。在适用时使用 SI 单位符号，并在数字与单位符号之间写一个空格（例如 ``10 ms``）。

表示方式
  任何不明显的编码或缩放方式（例如定点缩放、Q 格式、整数与小数部分分离的字段、字节序要求）。

所有权与生存期
  对于指针/缓冲区，说明由谁分配/释放以及内存必须保持有效多长时间。在相关时注明所需的大小/对齐要求。

写作风格
========

简要描述应使用祈使语气（动词短语），而不是第三人称叙述。这样可以使 API 摘要保持一致并便于浏览。

- 避免： “Transmits data through a pipe.”、“This function gets the device state.”
- 推荐： “Transmit data through a pipe.”、“Get the device state.”、“Initialize the subsystem.”

参数和成员的描述可以是句子片段，但应保持描述性，并避免重复参数/成员的名称。


.. _doxygen_groups:

分组
****

分组将相关符号组织成一个层次结构，帮助用户浏览 API。

- 使用 ``@defgroup`` 定义每个分组，且只定义一次。

  - 所提供的标题应是该分组简短且具描述性的名称。由于分组本身就会把各种接口/API 归并在一起，因此标题中 *不要* 使用 “API” 或 “Interface”（或这些词的任何其他变体），因为那样会显得冗余。
  - 分组的简要描述不应复述其标题。

- 分组名称使用 `snake_case <https://en.wikipedia.org/wiki/Snake_case>`_。
- 使用 ``@ingroup`` 指定一个分组所属的父分组。

示例：

.. code-block:: c
   :emphasize-lines: 2,3

   /**
    * @defgroup mqtt_socket MQTT Client library
    * @ingroup networking
    * @since 1.14
    * @version 0.8.0
    * @{
    */

    /* documented contents of the MQTT header file */

    /** @} */

.. note::

   一个分组可以属于多个父分组，因此可以有多个 ``@ingroup`` 命令。例如，设备驱动模拟器通常同时出现在 “Emulator Interfaces” 和 “Device drivers” 分组中。示例请参阅 :c:group:`i2c_emul_interface`。

.. important::

   没有父分组的分组会成为 :ref:`api_overview` 的顶层条目，而该页面的类别是刻意保持精简的。请始终通过 ``@ingroup`` 为新分组指定父分组。

   顶层条目在 :zephyr_file:`doc/_doxygen/toplevel_groups.txt` 中列入允许列表，并由 :zephyr_file:`scripts/ci/doxygen_toplevel_groups.py` 强制执行。新增顶层条目需要文档维护者批准。

.. _doxygen_api_versioning:

API 版本管理
============

在分组定义（ ``@defgroup`` ）上使用 ``@since`` 和 ``@version`` 来记录 API 的历史和成熟度：

- ``@since`` 表示该 API 引入时的 Zephyr 版本（例如 ``@since 3.7``）
- ``@version`` 表示当前 API 版本，遵循语义化版本规范

版本号反映 :ref:`api_overview` 中定义的 API 成熟度。

示例：

.. code-block:: c
   :caption: 以下示例针对在 Zephyr 1.14 中引入、当前版本为 0.8.0（不稳定）的 API。
   :emphasize-lines: 4,5

   /**
    * @defgroup mqtt_socket MQTT Client library
    * @ingroup networking
    * @since 1.14
    * @version 0.8.0
    * @{
    */

    /* documented contents of the MQTT header file */

    /** @} */

文件
****

每个公共头文件都必须在顶部有一个 ``@file`` 块，位于 SPDX 许可证和版权声明之后。

``@file`` 块还必须属于一个 Doxygen 分组，通常是同一头文件中定义的那个分组。这样，按文件浏览的用户可以方便地跳转到关联的分组。

.. code-block:: c
   :emphasize-lines: 2,4

   /**
    * @file
    * @brief Public API for the GPIO driver.
    * @ingroup gpio_interface
    */

类型定义
********

为 ``struct``、``enum``、``union`` 和 ``typedef`` 定义编写简要描述。

还应记录每个成员（结构体字段、枚举值等）。当只提供简要描述且能放在一行内时，建议使用 ``/**<`` 尾随注释风格。

.. code-block:: c
   :caption: 完整文档化的枚举、结构体和 typedef 示例。

   /** @brief Parity modes */
   enum uart_config_parity {
        UART_CFG_PARITY_NONE,   /**< No parity */
        UART_CFG_PARITY_ODD,    /**< Odd parity */
        UART_CFG_PARITY_EVEN,   /**< Even parity */
        UART_CFG_PARITY_MARK,   /**< Mark parity */
        UART_CFG_PARITY_SPACE,  /**< Space parity */
   };

   /**
    * GPIO pin configuration.
    *
    * Specifies direction, pull resistor, and interrupt settings.
    */
   struct gpio_config {
       uint32_t flags;    /**< Pin configuration flags. */
       gpio_pin_t pin;    /**< Pin number within the port. */
   };

   /**
    * @brief Identifies a set of pins associated with a port.
    *
    * The pin with index n is present in the set if and only if the bit
    * identified by (1U << n) is set.
    */
   typedef uint32_t gpio_port_pins_t;

函数
****

参数
====

- 按声明顺序使用 ``@param`` 记录参数
- 对于函数要写入的指针，使用 ``@param[out]``。
- 对于函数既读取又写入的指针，使用 ``@param[in,out]``。
- 对于 const 指针和标量（隐式为仅输入），可以省略方向说明符。

返回值
======

- 对于一般性描述（例如布尔值或计算得到的值），使用 ``@return <description>``。
- 对于具体的离散返回值（通常是错误码），使用 ``@retval <value> <description>``，并从成功的情况开始（在适用时）。``<value>`` 必须作为第一个词给出，其后是描述（例如使用 ``@retval -EINVAL Invalid arguments``，而不是 ``@retval -EINVAL if invalid arguments``）。

  .. note::

     由于同一个离散值可能有多个返回原因，因此允许在多个 ``@retval`` 语句中使用同一个值。

示例：

.. code-block:: c
   :caption: 完整文档化的函数示例。

   /**
    * @brief Write data to the TX queue from a provided buffer
    *
    * @param dev Pointer to the device structure for the driver instance.
    * @param buf Pointer to a buffer containing the data to transmit.
    * @param size Number of bytes to write. This value has to be equal or smaller
    *        than the size of the channel's TX memory block configuration.
    *
    * @retval 0 on success.
    * @retval -EIO The interface is not in READY or RUNNING state.
    * @retval -EBUSY Returned without waiting.
    * @retval -EAGAIN Waiting period timed out.
    * @retval -ENOMEM No memory in TX slab queue.
    * @retval -EINVAL Size parameter larger than TX queue memory block.
    */
   int i2s_buf_write(const struct device *dev, void *buf, size_t size);

   /**
    * @brief Add an application callback.
    *
    * @param port Pointer to the device structure for the driver instance.
    * @param callback A valid application's callback structure pointer.
    *
    * @return 0 on success, negative errno value on failure.
    * @retval -ENOSYS Driver does not implement the operation.
    */
   int gpio_add_callback(const struct device *port, struct gpio_callback *callback);

   /**
    * @brief Helper function for converting struct sensor_value to float.
    *
    * @param val A pointer to a sensor_value struct.
    * @return The converted value.
    */
   static inline float sensor_value_to_float(const struct sensor_value *val)
   {
       return (float)val->val1 + (float)val->val2 / 1000000;
   }


宏
***

对于类函数宏，像记录函数那样记录其参数。

.. code-block:: c
   :caption: 完整文档化的类函数宏示例。

   /**
    * @brief Get a node's (only) register block size
    *
    * Equivalent to DT_REG_SIZE_BY_IDX(node_id, 0).
    *
    * @param node_id node identifier
    * @return node's only register block's size
    */
   #define DT_REG_SIZE(node_id) DT_REG_SIZE_BY_IDX(node_id, 0)

.. _doxygen_sphinx_xrefs:

引用主文档
**********

API 文档可以使用下面描述的命令引用基于 Sphinx 的主文档中的内容。在生成的 API 文档页面中，这些引用会渲染为指向主文档相应页面的超链接。

``@kconfig{<option>}``
  按完整名称（包括 ``CONFIG_`` 前缀）引用一个 Kconfig 选项。这是 :rst:role:`kconfig:option` 角色在 Doxygen 中的对应形式。

  示例： ``@kconfig{CONFIG_GPIO}``

``@kconfig_regex{<regex>}``
  引用所有匹配某个正则表达式的 Kconfig 选项，形成一个指向已预填该模式的 Kconfig 搜索页面的链接。这是 :rst:role:`kconfig:option-regex` 角色在 Doxygen 中的对应形式。由于逗号在 Doxygen 命令中具有特殊含义，必须用反斜杠转义。

  示例： ``@kconfig_regex{CONFIG_SECURE_STORAGE_ITS_.*_CUSTOM}``

``@dtcompatible{<compatible>}``
  按 compatible 字符串引用一个 Devicetree 绑定。这是 :rst:role:`dtcompatible` 角色在 Doxygen 中的对应形式。由于逗号在 Doxygen 命令中具有特殊含义，必须用反斜杠转义。

  示例： ``@dtcompatible{zephyr\,input-longpress}``

``@rstref{<target>}`` 或 ``@rstref{<text> <target>}``
  按引用标签（或文档名称）引用任意文档页面或章节，类似于 Sphinx 的 :rst:role:`ref` 角色。未提供自定义文本时，将使用所引用页面或章节的标题作为链接文本。

  示例： ``@rstref{zephyr_licensing}`` 或 ``@rstref{the licensing page <zephyr_licensing>}``

构建文档时会检查这些引用：引用不存在的 Kconfig 选项、绑定或标签会导致文档构建警告。

.. note::

   当 Doxygen 文档独立构建（即不包含文档的其余部分）时，这些命令会展开为纯文本。详细信息请参阅 :ref:`zephyr_doc`。

.. _doxygen_rfc_refs:

引用 IETF RFC
*************

``@rfc{<number>}`` 或 ``@rfc{<number>,<anchor>}``
  按编号引用一个 IETF RFC，可选地指向其中的某个锚点。这是 :rst:role:`rfc` 角色在 Doxygen 中的对应形式，会渲染为指向 IETF Datatracker 上该 RFC 的超链接。

  锚点会被原样传递，因此它可以指向 Datatracker 为该 RFC 定义的任何内容，例如 ``section-3.1``、``appendix-B.1.2``、``figure-2`` 或 ``table-1``。存在哪些锚点取决于该 RFC：只有由 XML 源文件渲染的 RFC 才会为图和表提供锚点。

  不要在逗号后添加空白：Doxygen 会将其保留为参数的一部分，最终出现在 URL 片段中。渲染出的链接文本看起来仍然正确，因此只有实际访问链接时才会发现锚点已失效。

  示例： ``@rfc{7519}``、``@rfc{8613,section-3.1}`` 或 ``@rfc{8613,appendix-B.1.2}``

.. _doxygen_internals:

隐藏内部细节
************

使用 ``@cond INTERNAL_HIDDEN`` / ``@endcond`` 从生成的文档中隐藏内部细节。

你仍然可以选择记录这些内部符号，以便为内部使用者提供有用的参考。

.. code-block:: c
   :emphasize-lines: 7,11

   /** Timer structure.
    *
    * Opaque type for a timer object. All the fields in this structure are internal and should not
    * be accessed outside of kernel code.
    */
   struct k_timer {
       /** @cond INTERNAL_HIDDEN */

       /* ... internal members ... */

       /** @endcond */
   };

.. _doxygen_driver_backend:

驱动程序后端 API
****************

驱动子系统为应用提供公共 API，并为驱动实现者提供“后端”API。

虽然后端 API 并不打算供应用直接使用，但它仍然构成子系统与驱动实现者之间的公共契约，因此必须有适当的文档。它通常包括驱动操作结构体、定义各操作签名的 typedef，以及在某些情况下对驱动实现有用的额外辅助类型或宏。

后端 API 的 Doxygen 分组
========================

使用 ``@def_driverbackendgroup`` 创建一个子分组，它是主 API 分组的子级，并将包含与后端 API 关联的所有符号。该命令接受两个参数：后端 API 的人类可读名称（通常与父分组相同）和父分组标识符。

.. code-block:: c

   /**
    * @def_driverbackendgroup{Haptics,haptics_interface}
    * @{
    */

   /* callback typedefs, driver ops struct, helpers ... */

   /** @} */

驱动操作用的 typedef
====================

为每个驱动操作定义一个 ``typedef``。详细描述可以引用对应的公共 API 函数，因为它的签名通常类似。

.. code-block:: c

   /**
    * @brief Set the haptic device to stop output.
    * See haptics_stop_output() for argument description.
    */
   typedef int (*haptics_stop_output_t)(const struct device *dev);

驱动操作结构体
==============

使用 ``@driver_ops{Name}`` 标注该结构体（其中 *Name* 与传给 ``@def_driverbackendgroup`` 的名称一致）。对于每个成员，使用 ``@driver_ops_mandatory`` 或 ``@driver_ops_optional`` 指明驱动是否必须实现它，并使用 ``@copybrief`` 从公共 API 函数继承简要描述：

.. code-block:: c

   /**
    * @driver_ops{Haptics}
    */
   __subsystem struct haptics_driver_api {
       /**
        * @driver_ops_mandatory @copybrief haptics_start_output
        */
       haptics_start_output_t start_output;
       /**
        * @driver_ops_mandatory @copybrief haptics_stop_output
        */
       haptics_stop_output_t stop_output;
       /**
        * @driver_ops_optional @copybrief haptics_register_error_callback
        */
       haptics_register_error_callback_t register_error_callback;
   };

.. _doxygen_conditional_code:

条件编译代码
************

为确保条件编译的代码出现在文档中，请使用以下任一方法：

1. 将控制该代码的 Kconfig 宏（ ``CONFIG_...`` ）添加到 :zephyr_file:`doc/zephyr.doxyfile.in` 的 ``PREDEFINED`` 列表中。这样在生成文档时 Doxygen 就能看到该代码。

#. 或者，你可以依靠已定义的 ``__DOXYGEN__`` 宏来让 Doxygen 看到条件编译代码，因为该宏由 Doxygen 自动定义。

.. code-block:: c
   :emphasize-lines: 3,9

   struct coap_packet {
       uint8_t *data;  /**< User allocated buffer. */
   #if defined(CONFIG_COAP_KEEP_USER_DATA) || defined(__DOXYGEN__)
       /**
        * Application-specific user data.
        * @kconfig_dep{CONFIG_COAP_KEEP_USER_DATA}
        */
       void *user_data;
   #endif
   };

.. _doxygen_kconfig_dep:

Kconfig 依赖
============

``@kconfig_dep`` 命令可用于记录使某个 API 符号对用户可用所需的 Kconfig 选项。该命令可接受一个、两个或三个 Kconfig 选项。

例如，在某个 API 符号的 Doxygen 文档中添加 ``@kconfig_dep{CONFIG_PM,CONFIG_SMP}``，会使生成的文档包含一条注释：“Available only when the following Kconfig options are enabled: ``CONFIG_PM``, ``CONFIG_SMP``.”。

你可以在 :c:struct:`coap_packet` 的文档中看到 ``@kconfig_dep`` 用法的示例。
