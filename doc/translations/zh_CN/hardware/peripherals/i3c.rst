.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _i3c_api:

改进型集成电路间（I3C）总线
###########################

I3C（改进型集成电路间总线）是一种使用两根信号线的共享外设接口总线。总线上的设备可以扮演两种角色：发起事务并控制时钟的“控制器”，或响应事务命令的“目标设备”。

目前，该 API 基于 `I3C Specification`_ 1.1.1 版本。

.. contents::
    :local:
    :depth: 2

.. _i3c-controller-api:

I3C 控制器 API
**************

当 I3C 控制器控制总线，尤其是控制起始条件、停止条件和时钟时，使用 Zephyr 的 I3C 控制器 API。这是最常见的模式，用于与传感器等 I3C 目标设备交互。

由于 I3C 的特性，总线上的某些设备在上电时可能没有地址。因此，I3C 控制器还需要执行动态地址分配。为此，控制器需要维护独立的数据结构，以跟踪设备状态。这可以在构建时完成，例如，为 I3C 和 I\\ :sup:`2`\\ C 设备分别创建设备描述符数组：

.. code-block:: c

   static struct i3c_device_desc i3c_device_array[] = I3C_DEVICE_ARRAY_DT_INST(inst);
   static struct i3c_i2c_device_desc i2c_device_array[] = I3C_I2C_DEVICE_ARRAY_DT_INST(inst);

:c:macro:`I3C_DEVICE_ARRAY_DT_INST` 和 :c:macro:`I3C_I2C_DEVICE_ARRAY_DT_INST` 是辅助宏，用于创建与 I3C 控制器下的 Devicetree 节点对应的设备描述符数组。

以下是在设备驱动程序初始化函数中初始化 I3C 控制器和 I3C 总线的通用步骤：

#. 初始化 I3C 控制器设备驱动程序实例的数据结构。可以使用 :c:macro:`DEVICE_DT_INST_DEFINE` 等常用的设备定义宏，并将初始化函数作为参数传递给宏。

   * :c:struct:`i3c_addr_slots` 和 :c:struct:`i3c_dev_list` 是用于辅助地址分配和设备列表管理的结构体。如果使用这些结构体，需要调用 :c:func:`i3c_addr_slots_init` 进行初始化。这两个结构体也可以与各种辅助函数配合使用。

   * 如果控制器驱动程序需要，则初始化设备描述符。

#. 初始化硬件，包括但不限于：

   * 设置引脚复用和方向。

   * 设置控制器时钟。

   * 为硬件上电。

   * 配置硬件（例如 SCL 时钟频率）。

#. 执行总线初始化。通用辅助函数 :c:func:`i3c_bus_init` 会执行以下步骤。如果控制器在总线初始化期间不需要任何特殊处理，则可以使用此函数。

   #. 执行 ``RSTDAA`` 以重置已连接设备的动态地址。如果某些已连接设备已经分配了地址，管理用的数据结构中可能没有这些地址的记录，例如在上电时。因此，建议重置这些设备的地址，并为其分配新地址。

   #. 执行 ``DISEC`` 以禁用设备的所有事件。

   #. 如果需要，执行 ``SETDASA`` 以使用设备的静态地址分配动态地址。

      * 并非所有已连接设备都支持通过 ``SETAASA`` 将静态地址分配为动态地址。

      * 需要单独获取 BCR 和 DCR，以填充 I3C 目标设备描述符结构体中的相关字段。

   #. 如果仍有设备没有地址，则执行 ``ENTDAA`` 以启动动态地址分配。

      * 如果有设备正在等待分配地址，它会返回其预配置标识符（Provisioned ID）、BCR 和 DCR。将收到的预配置标识符与已注册的 I3C 设备列表进行匹配。

        * 如果匹配成功，则分配一个地址（如果尚未执行 ``SETDASA`` ，可以使用已声明的静态地址，也可以使用空闲地址）。

          * 同时，设置设备描述符结构体中的 BCR 和 DCR 字段。

        * 如果没有匹配项，则根据策略，可以为其分配一个空闲地址，也可以由设备驱动程序停止分配过程并报错。

          * 请注意，I3C API 需要设备描述符才能工作。没有设备描述符的设备无法通过该 API 访问。

      * 如果已连接的设备中没有需要动态地址分配（DAA）的设备，则可以跳过此步骤。

   #. 以下步骤是可选的，但强烈建议执行：

      * 执行 ``GETMRL`` 和 ``GETMWL`` 以获取最大读写长度。

      * 执行 ``GETMXDS`` 以获取最大读写速度和最大读取周转时间。

      * 辅助函数 :c:func:`i3c_bus_init` 会获取设备的基本信息，例如 BCR、DCR、MRL 和 MWL。

   #. 执行 ``ENEC`` 以重新启用设备事件。

      * 辅助函数 :c:func:`i3c_bus_init` 仅重新启用热加入事件。仅应在启用设备的 IBI 时启用 IBI 事件。

带内中断（IBI）
===============

如果目标设备能够产生带内中断（IBI），则需要告知控制器。

* 使用 :c:func:`i3c_ibi_enable` 启用目标设备的 IBI。

  * 某些控制器硬件具有 IBI 槽位，需要对其进行编程，以便控制器能够识别来自特定目标设备的 IBI。

    * 如果硬件具有 IBI 槽位，:c:func:`i3c_ibi_enable` 需要对这些 IBI 槽位进行编程。

    * 请注意，控制器上的 IBI 槽位数量通常有限，因此此操作可能失败。

  * 驱动中的实现还应发送 ``ENEC`` 命令，以启用此目标设备的中断。

* 使用 :c:func:`i3c_ibi_disable` 禁用目标设备的 IBI。

  * 如果控制器硬件使用 IBI 槽位，此操作会从槽位中移除目标设备的描述信息。

  * 驱动中的实现还应发送 ``DISEC`` 命令，以禁用此目标设备的中断。

设备树
======

以下是在 Devicetree 中定义 I3C 控制器的示例：

.. code-block:: devicetree

   i3c0: i3c@10000 {
           compatible = "vendor,i3c";

           #address-cells = <0x3>;
           #size-cells = <0x0>;

           reg = <0x10000 0x1000>;
           interrupts = <0x1F 0x0>;

           pinctrl-0 = <&pinmux-i3c>;
           pinctrl-names = "default";

           i2c-scl-hz = <400000>;

           i3c-scl-hz = <12000000>;

           status = "okay";

           i3c-dev0: i3c-dev0@420000ABCD12345678 {
                   compatible = "vendor,i3c-dev";

                   reg = <0x42 0xABCD 0x12345678>;

                   status = "okay";
           };

           i2c-dev0: i2c-dev0@380000000000000050 {
                   compatible = "vendor-i2c-dev";

                   reg = <0x38 0x0 0x50>;

                   status = "okay";
           };
   };

I3C 设备
--------

对于 I3C 设备，``reg`` 属性包含 3 个元素：

* 第一个元素是设备的静态地址。

  * 如果不使用静态地址，可以将其设为零。地址将在 DAA（动态地址分配）期间分配。

  * 如果此元素非零且未设置 ``assigned-address`` 属性，则在发出 SETDASA（根据静态地址设置动态地址）命令后，此元素的值将成为设备地址。

* 第二个元素是预置标识符（PID）的高 16 位，其中包含左移 1 位的制造商 ID。这对应于 48 位预置标识符的第 33 至 47 位（从零开始编号）。

  * 此元素必须非零。如下面所述，第二个元素为零会将节点标记为 I\\ :sup:`2`\\ C 设备，因此辅助宏会为其创建传统 I\\ :sup:`2`\\ C 描述符，而不是 I3C 描述符。即使设备通过 SETDASA 寻址且其他情况下不使用 PID，也应指定 PID。

* 第三个元素包含预置标识符的低 32 位，由器件 ID（左移 16 位，对应 PID 的第 16 至 31 位）和实例 ID（左移 12 位，对应 PID 的第 12 至 15 位）组合而成。

请注意，单元地址（``@`` 之后的部分）必须与 ``reg`` 属性完全匹配，其中每个元素均视为 32 位整数，组合形成一个 96 位整数。这是正确生成 Devicetree 宏的必要条件。

I\\ :sup:`2`\\ C 设备
---------------------

对于驱动支持在 I3C 总线上工作的 I\\ :sup:`2`\\ C 设备，可以将设备节点描述为 I3C 控制器的子节点。如果设备驱动仅支持 I\\ :sup:`2`\\ C 控制器，请按照下文说明，在 I\\ :sup:`2`\\ C 虚拟控制器下定义节点。否则，与 I3C 设备类似，``reg`` 属性包含 3 个元素：

* 第一个元素是设备的静态地址。此地址必须有效，因为 I\\ :sup:`2`\\ C 设备不支持动态地址分配。

* 第二个元素始终为零。

  * 各种辅助宏使用此元素来判断 Devicetree 条目是否对应于 I\\ :sup:`2`\\ C 设备。

* 第三个元素是 LVR（传统虚拟寄存器）：

  * bit[31:8] 未使用。

  * bit[7:5] 为 I\ :sup:`2`\ C 设备索引：

    * 索引 ``0``

      * I3C 设备具有 50 ns 尖峰滤波器，不受 SCL 上高频信号的影响。

    * 索引 ``1``

      * I\ :sup:`2`\ C 设备没有 50 ns 尖峰滤波器，但可以在 SCL 上存在高频信号的情况下工作。

    * 索引 ``2``

      * I3C 设备没有 50 ns 尖峰滤波器，且无法在 SCL 上存在高频信号的情况下工作。

  * bit[4] 为 I\ :sup:`2`\ C 模式指示位：

    * ``0`` 表示 FM+ 模式。

    * ``1`` 表示 FM 模式。

与 I3C 设备类似，unit-address 必须与 ``reg`` 属性完全匹配，其中每个元素均视为一个 32 位整数，组合起来构成一个 96 位整数。

I3C 设备的设备驱动程序
======================

I3C 控制器 API 的所有传输函数都需要使用设备描述符 :c:struct:`i3c_device_desc` 。该结构体包含 I3C 设备的运行时信息，例如动态地址、BCR、DCR、MRL 和 MWL。因此，I3C 设备的驱动程序应使用 :c:func:`i3c_device_find` 从控制器获取指向此设备描述符的指针。该函数接受一个类型为 :c:struct:`i3c_device_id` 的 ID 参数用于匹配。随后即可在对控制器的后续 API 调用中使用返回的指针。

I3C 总线上的 I\ :sup:`2`\ C 设备
================================

由于 I3C 向后兼容 I\ :sup:`2`\ C，如果控制器设备驱动程序实现了 I2C API，I3C 控制器 API 就能支持未经修改的 I2C API 调用。这样便可使用现有的 I2C 设备，而无需修改其设备驱动程序。不过，由于 I3C 控制器 API 基于设备描述符工作，每次调用 I2C API 时都需要根据 I2C 设备地址查找相应的设备描述符。这会为每次 I2C API 调用增加少量处理开销。

另一方面，也可以扩展设备驱动程序，通过 I3C 控制器 API 使用原生 I2C 设备支持。在设备初始化期间，需要调用 :c:func:`i3c_i2c_device_find` 来获取指向设备描述符的指针。此指针可用于后续的 API 调用。

请注意，无论使用上述哪种方法，都必须按照 I3C 标准声明 I2C 设备的 Devicetree 节点：

I\ :sup:`2`\ C 虚拟控制器设备驱动程序提供了一种访问 I3C 总线上 I\ :sup:`2`\ C 设备的方式，使相关设备驱动程序无需修改即可直接使用。这需要在 Devicetree 中添加一个中间节点：

.. code-block:: devicetree

   i3c0: i3c@10000 {
           <... I3C controller related properties ...>
           <... Nodes of I3C devices, if any ...>

           i2c-dev0: i2c-dev0@420000000000000050 {
                   compatible = "vendor-i2c-dev";

                   reg = <0x42 0x0 0x50>;

                   status = "okay";
           };
   };

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_I3C`
* :kconfig:option:`CONFIG_I3C_USE_IBI`
* :kconfig:option:`CONFIG_I3C_IBI_MAX_PAYLOAD_SIZE`
* :kconfig:option:`CONFIG_I3C_CONTROLLER_INIT_PRIORITY`

API 参考
********

.. doxygengroup:: i3c_interface
.. doxygengroup:: i3c_ccc
.. doxygengroup:: i3c_addresses
.. doxygengroup:: i3c_target_device

.. _I3C Specification: https://www.mipi.org/specifications/i3c-sensor-specification
