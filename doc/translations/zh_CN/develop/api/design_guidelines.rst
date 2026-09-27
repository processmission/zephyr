.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _design_guidelines:

API 设计指南
############

Zephyr 的开发和演进依赖团队协作。为简化维护和增强工作，开发新功能或接口时应遵循一些通用策略。

所有公共 API 都必须使用 Doxygen 编写文档，详见 :ref:`doxygen_style`。

使用回调
********

许多 API 通过参数或配置结构体成员传递回调。定义回调签名时应遵循以下策略：

* 第一个参数应为指向与回调关系最密切的对象的指针。对于设备驱动程序，应为 ``const struct device *dev``。对于库函数，可以是指向提供回调时所引用的其他对象的指针。

* 接下来的参数应提供本次回调特有的信息，例如通道标识符、新状态值，或消息指针及其后的消息长度。

* 最后一个参数应为 ``void *user_data`` 指针，携带上下文，使共用回调函数能找到处理此次回调所需的其他信息。

如果回调本身通过一个会嵌入其他结构体的结构体提供，可以例外地不将 ``user_data`` 作为最后一个参数。例如 :c:struct:`gpio_callback`，通常定义在与回调函数代码配套的数据结构中。此时，回调可以通过 :c:macro:`CONTAINER_OF` 间接访问更多上下文。

示例
====

* 系统定时器闹钟触发时调用的 :c:type:`k_timer_expiry_t`，可通过以下签名满足要求::

    void handle_timeout(struct k_timer *timer)
    { ... }

  这里与 :c:struct:`gpio_callback` 一样，假定定时器嵌入某个结构体，可以通过 :c:macro:`CONTAINER_OF` 找到该结构体，为回调提供更多上下文。

* 计数器设备闹钟触发时调用的 :c:type:`counter_alarm_callback_t`，可通过以下签名满足要求::

    void handle_alarm(const struct device *dev,
                      uint8_t chan_id,
                      uint32_t ticks,
                      void *user_data)
    { ... }

  这提供了更完整的有效信息，包括超时的计数器通道、超时发生时的计数值，以及用户上下文。根据用户需要，该上下文可以是注册回调时使用的 :c:struct:`counter_alarm_cfg`，也可以不是。

条件数据与 API
**************

API 和库可能提供占用较多 RAM 或代码空间的可选功能，某些应用无需这些功能也能实现。例如 :kconfig:option:`采集时间戳 <CONFIG_CAN_RX_TIMESTAMP>` 或 :kconfig:option:`提供替代接口 <CONFIG_SPI_ASYNC>`。开发者必须与社区协商，决定是否通过 Kconfig 选项控制这些功能的启用。

如果某个功能被确定为可选，应遵循以下做法。

* 仅在启用该功能时访问的数据，应在结构体或联合体声明中通过 ``#ifdef CONFIG_MYFEATURE`` 条件包含，从而减少不需要该功能的应用的内存占用。
* 仅在启用选项时可用的函数，其声明仍应无条件提供。在说明中注明函数仅在启用指定功能时可用，并引用所需 Kconfig 符号的名称。使用了函数但未启用功能时，应将函数定义排除在编译之外，使对不受支持 API 的引用产生链接错误。
* 如果功能专用代码单独位于一个不含其他内容的源文件中，应在 ``CMakeLists.txt`` 中有条件地包含该文件::

    zephyr_sources_ifdef(CONFIG_MYFEATURE foo_funcs.c)
* 如果功能专用代码与其他内容位于同一源文件中，应使用 ``#ifdef CONFIG_MYFEATURE`` 条件处理该代码。

如何确保 Doxygen 能看到条件代码并将其纳入公共 API 文档，详见 :ref:`doxygen_conditional_code`。

返回码
******

API 实现（例如外设访问 API）可能只实现满足基本操作所需的一部分函数。需要区分不支持的 API，以及未实现或可选的 API：

- 支持但尚未实现的 API 应返回 ``-ENOSYS``。

- 硬件不支持的可选 API 也应提供实现，此时返回码应为 ``-ENOTSUP``。

- 如果 API 已实现，但无法满足调用中请求的特定选项组合，应返回 ``-ENOTSUP``。例如，在仅支持边沿触发中断的硬件上请求电平触发 GPIO 中断。
