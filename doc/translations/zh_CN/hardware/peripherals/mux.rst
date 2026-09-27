.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mux_api:

多路复用器（MUX）
#################

概述
****

MUX 子系统为硬件信号多路复用器提供统一的 API，使使用方驱动能够通过标准 Devicetree 属性 ``mux-controls`` 或 ``mux-states`` （类型为 phandle-array）引用 MUX 控制器，将输入信号路由到输出，而无需依赖任何供应商特定的 HAL。

该子系统区分了使用方的两种使用模式：

* ``mux-controls`` — 使用方引用控制器，并在运行时通过 :c:func:`mux_control_set` 提供 *状态* （要路由的输入，或要写入的输出模式）。当路由在正常运行期间会发生变化时，使用此模式。

* ``mux-states`` — 使用方在 Devicetree 中引用控制器 *以及* 一个固定状态（说明符的最后一个单元为状态值）。运行时调用 :c:func:`mux_state_apply` 即可用一行代码设置该固定状态。当路由在集成时确定且初始化后不再变化时，使用此模式。

Devicetree 绑定
***************

控制器端
========

每个 MUX 控制器绑定都包含 ``mux-controller.yaml`` （位于 ``dts/bindings/mux/`` ），并声明两个用于指定单元数量的属性：

* ``#mux-control-cells`` — ``mux-controls`` 说明符中的单元数量，这些单元仅用于寻址控制器内所需的控制线。
* ``#mux-state-cells`` — ``mux-states`` 说明符中的单元数量，等于 ``#mux-control-cells + 1`` 。最后一个单元承载状态值，框架会在编译时将其提取到 ``mux_state::state`` 中。

后端可以根据硬件自行命名寻址单元（ ``channel`` 、 ``output`` 、 ``index`` 、 ``device`` / ``input`` 等），并根据硬件语义命名末尾的状态单元（ ``state`` 、 ``input`` 、 ``connection`` 、 ``source`` 等）。

使用方端
========

使用方包含 ``mux-consumer.yaml`` ，并可设置以下属性：

* ``mux-controls`` — 由 phandle 和寻址单元组成的元组列表。
* ``mux-control-names`` — 与 ``mux-controls`` 条目对应的可选名称。
* ``mux-states`` — 由 phandle、寻址单元和末尾状态单元组成的元组列表。
* ``mux-state-names`` — 与 ``mux-states`` 条目对应的可选名称。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_MUX`

API 参考
********

.. doxygengroup:: mux_interface
