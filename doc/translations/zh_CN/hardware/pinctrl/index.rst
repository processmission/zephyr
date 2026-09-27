.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _pinctrl-guide:

引脚控制
########

本文是引脚控制的概括性指南。API 参考资料请参见 :ref:`pinctrl_api` 。

简介
****

控制引脚复用以及引脚方向、上拉/下拉电阻等引脚配置参数的硬件模块称为 **引脚控制器** 。引脚控制器的主要使用者是 SoC 硬件外设，因为它能够将外设信号引出，例如将 ``I2C0`` 的 ``SDA`` 信号映射到引脚 ``PX0`` 。此外，它通常还允许配置外设正常工作所必需的某些引脚设置，例如根据工作频率设置压摆率。可用的配置选项取决于厂商和 SoC，范围涵盖简单的上拉/下拉选项，以及去抖、低功耗模式等更高级的设置。

引脚控制在硬件中的实现方式因厂商和 SoC 而异。常见的是 *集中式* 方案，即所有引脚配置参数（包括信号映射）都由单个硬件模块控制，该模块通常称为 pinmux。下图展示了这种方案。根据 ``AF`` 控制位的设置，``PX0`` 可以映射到 ``UART0_TX`` 、``I2C0_SCK`` 或 ``SPI0_MOSI`` 。上拉/下拉等其他配置参数也在同一模块中通过 ``CONFIG`` 位进行控制。多个 SoC 系列族采用了这种模型，例如 NXP 和 STM32 的许多 SoC 系列族。

.. figure:: images/hw-cent-control.svg

    将每个引脚的控制集中在单个模块中的示例

其他厂商或 SoC 采用 *分布式* 方案。在这种情况下，引脚映射和配置由多个硬件模块控制。下图展示了一种由外设控制引脚映射的分布式方案，例如 Nordic nRF SoC 所采用的方案。

.. figure:: images/hw-dist-control.svg

    引脚控制分布在外设寄存器和各引脚模块中的示例

从用户角度看，无论硬件如何实现，引脚控制器的使用方式都没有区别：用户始终通过应用某个状态来使用它。区别仅在于驱动的实现。通常，为采用分布式方案的硬件实现引脚控制器驱动需要投入更多工作，因为驱动需要掌握各外设相关寄存器的信息。

引脚控制与 GPIO 的比较
======================

引脚控制器驱动提供的某些功能与 GPIO 驱动重叠。例如，通常既可以通过引脚控制驱动，也可以通过 GPIO 驱动来启用上拉/下拉电阻。在 Zephyr 中，引脚控制驱动的作用是完成外设信号复用，并配置该外设正常工作所需的其他引脚参数。因此，引脚控制驱动的主要使用者是 SoC 外设。相比之下，GPIO 驱动用于对引脚进行通用控制，即手动读取或控制引脚的逻辑电平。

状态模型
********

设备驱动要正常工作，需要应用特定的引脚配置。有些设备驱动需要静态配置，通常在初始化时设置。另一些则需要根据工作条件在运行时更改配置，例如在挂起设备时启用低功耗模式。这些需求通过 **状态** 来建模，这一概念借鉴了 Linux 内核中的状态概念。每个设备驱动都拥有一组状态。每个状态都有唯一的名称，并包含一套完整的引脚配置（见下图）。这意味着各状态相互独立，无须按任何特定顺序应用。状态模型的另一个优点是将设备驱动与引脚配置分离。

.. table:: 使用状态模型表示引脚配置的示例
    :align: center

    +-------------------------------------------------------+
    | ``UART0`` 外设                                        |
    +===========================+===========================+
    | ``default`` 状态          | ``sleep`` 状态            |
    +------+--------------------+------+--------------------+
    | TX   | - 引脚：PA0        | TX   | - 引脚：PA0        |
    |      | - 上拉/下拉：无    |      | - 上拉/下拉：无    |
    |      | - 低功耗：否       |      | - 低功耗：是       |
    +------+--------------------+------+--------------------+
    | RX   | - 引脚：PA1        | RX   | - 引脚：PA1        |
    |      | - 上拉/下拉：上拉  |      | - 上拉/下拉：无    |
    |      | - 低功耗：否       |      | - 低功耗：是       |
    +------+--------------------+------+--------------------+

标准状态
========

引脚控制状态的名称和数量取决于设备驱动的需求。在许多情况下，只需在初始化时应用一个状态即可，但在其他一些情况下则需要更多状态。为保持一致性，针对最常见的用例制定了命名约定。下图详细列出了标准化的状态及其用途。

.. table:: 标准化的状态名称
    :align: center

    +---------------+------------------------------------+--------------------------------------+
    | 状态          | 标识符                             | 用途                                 |
    +---------------+------------------------------------+--------------------------------------+
    | ``default``   | :c:macro:`PINCTRL_STATE_DEFAULT`   | 设备处于工作状态时的引脚状态         |
    +---------------+------------------------------------+--------------------------------------+
    | ``sleep``     | :c:macro:`PINCTRL_STATE_SLEEP`     | 设备处于低功耗或睡眠模式时的引脚状态 |
    +---------------+------------------------------------+--------------------------------------+

请注意，未来可能会引入其他标准状态。

自定义状态
==========

某些设备驱动可能需要使用标准状态之外的自定义状态。为此，设备驱动需要在其作用域内定义名为 ``PINCTRL_STATE_{STATE_NAME}`` 的自定义状态标识符，其中 ``{STATE_NAME}`` 是大写的状态名称。例如，如果需要支持 ``mystate`` ，则驱动的作用域内需要有一个名为 ``PINCTRL_STATE_MYSTATE`` 的定义。

.. note::
    自定义状态标识符的取值必须从 :c:macro:`PINCTRL_STATE_PRIV_START` 开始。

如果需要从驱动外部访问自定义状态，例如执行动态引脚控制，则应将自定义标识符放在可公开访问的头文件中。

跳过状态
========

在大多数情况下，Devicetree 中定义的状态都会用于编译生成的固件。不过，在某些情况下，特定状态是否使用取决于编译标志。一个典型的例子是 ``sleep`` 状态。实际上，只有启用 :kconfig:option:`CONFIG_PM` 或 :kconfig:option:`CONFIG_PM_DEVICE` 时才会使用此状态。如果需要不包含这些电源管理配置的固件变体，理论上应从 Devicetree 中移除 ``sleep`` 状态，以免存储这种未使用的状态而浪费 ROM 空间。

如果在定义引脚控制配置时，存在名为 ``PINCTRL_SKIP_{STATE_NAME}`` 且展开为 ``1`` 的定义， ``pinctrl`` Devicetree 宏就可以跳过相应状态。对于 ``sleep`` 状态， ``pinctrl`` API 已根据设备电源管理是否可用提供了这样的条件定义：

.. code-block:: c

    #if !defined(CONFIG_PM) && !defined(CONFIG_PM_DEVICE)
    /** Out of power management configurations, ignore "sleep" state. */
    #define PINCTRL_SKIP_SLEEP 1
    #endif

动态引脚控制
************

动态引脚控制是指在运行时更改引脚配置的能力。当同一固件需要在略有不同的开发板上运行，且各开发板将某个外设连接到不同的一组引脚时，此功能就会很有用。可以通过设置 :kconfig:option:`CONFIG_PINCTRL_DYNAMIC` 来启用此功能。

.. note::

    动态引脚控制应仅用于尚未初始化的设备。在设备运行期间更改引脚配置可能导致意外行为。由于 Zephyr 尚不支持设备反初始化，因此此功能应仅在启动早期阶段使用。

启用动态引脚控制后， :c:struct:`pinctrl_dev_config` 将存储在 RAM 中，而非 ROM 中（但状态和引脚配置不受影响）。随后，用户可以使用 :c:func:`pinctrl_update_states` ，以一组新状态替换 :c:struct:`pinctrl_dev_config` 中存储的状态。这实际上意味着，设备驱动在应用某个状态时，将应用更新后的状态中存储的引脚配置。

Devicetree 表示方式
*******************

由于 Devicetree 用于描述硬件，因此自然适合存储引脚控制配置。以下各节将概述如何在 Devicetree 中表示状态和引脚配置。

状态
====

对于给定设备，其每个引脚控制状态都由 Devicetree 中的 ``pinctrl-N`` 属性表示，其中 ``N`` 是从零开始的状态索引。然后使用 ``pinctrl-names`` 属性，按索引为每个状态属性分配唯一标识符。例如， ``pinctrl-names`` 列表中索引为 0 的条目就是 ``pinctrl-0`` 的名称。

.. code-block:: devicetree

    periph0: periph@0 {
        ...
        /* state 0 ("default") */
        pinctrl-0 = <...>;
        ...
        /* state N ("mystate") */
        pinctrl-N = <...>;
        /* names for state 0 up to state N */
        pinctrl-names = "default", ..., "mystate";
        ...
    };

引脚配置
========

在 Devicetree 中有多种表示引脚配置的方式，但它们最终编码的信息相同：引脚复用以及引脚配置参数。例如，将 ``UART_RX`` 映射到 ``PX0`` 并启用上拉。表示方式的选择主要取决于各厂商或 SoC，因此要了解详细信息，最好查阅引脚控制驱动的 Devicetree 绑定文件。

下面的示例展示了一种常用且灵活的方案。此方案的一个优点是能够根据共有的引脚配置进行分组，从而使引脚控制定义更简洁。另一个优点是，特定状态的引脚配置参数都包含在同一个 Devicetree 节点中。

.. code-block:: devicetree

    /* board.dts */
    #include "board-pinctrl.dtsi"

    &periph0 {
        pinctrl-0 = <&periph0_default>;
        pinctrl-names = "default";
    };

.. code-block:: c

    /* vnd-soc-pkgxx.h
     * File with valid mappings for a specific package (may be autogenerated).
     * This file is optional, but recommended.
     */
    ...
    #define PERIPH0_SIGA_PX0 VNDSOC_PIN(X, 0, MUX0)
    #define PERIPH0_SIGB_PY7 VNDSOC_PIN(Y, 7, MUX4)
    #define PERIPH0_SIGC_PZ1 VNDSOC_PIN(Z, 1, MUX2)
    ...

.. code-block:: devicetree

    /* board-pinctrl.dtsi */
    #include <vnd-soc-pkgxx.h>

    &pinctrl {
        /* Node with pin configuration for default state */
        periph0_default: periph0_default {
            group1 {
                /* Mappings: PERIPH0_SIGA -> PX0, PERIPH0_SIGC -> PZ1 */
                pinmux = <PERIPH0_SIGA_PX0>, <PERIPH0_SIGC_PZ1>;
                /* Pins PX0 and PZ1 have pull-up enabled */
                bias-pull-up;
            };
            ...
            groupN {
                /* Mappings: PERIPH0_SIGB -> PY7 */
                pinmux = <PERIPH0_SIGB_PY7>;
            };
        };
    };

另一种常见模型是为每种引脚配置和状态组合设置一个节点。虽然这种模型可以缩短开发板引脚控制文件，但也要求为每种引脚映射和状态组合设置一个节点，因为通常无法在多个状态之间复用节点。如果无法自动生成，则不建议使用这种方法。

.. note::

   由于所有 Devicetree 信息都会被解析到一个 C 头文件中，因此应确保该文件的大小尽可能小。为此，应为预先生成的节点添加 ``/omit-if-no-ref/`` 前缀。此前缀可确保未使用的节点被丢弃。

.. code-block:: devicetree

    /* board.dts */
    #include "board-pinctrl.dtsi"

    &periph0 {
        pinctrl-0 = <&periph0_siga_px0_default &periph0_sigb_py7_default
                     &periph0_sigc_pz1_default>;
        pinctrl-names = "default";
    };

.. code-block:: devicetree

    /* vnd-soc-pkgxx.dtsi
     * File with valid nodes for a specific package (may be autogenerated).
     * This file is optional, but recommended.
     */

    &pinctrl {
        /* Mapping for PERIPH0_SIGA -> PX0, to be used for default state */
        /omit-if-no-ref/ periph0_siga_px0_default: periph0_siga_px0_default {
            pinmux = <VNDSOC_PIN(X, 0, MUX0)>;
        };

        /* Mapping for PERIPH0_SIGB -> PY7, to be used for default state */
        /omit-if-no-ref/ periph0_sigb_py7_default: periph0_sigb_py7_default {
            pinmux = <VNDSOC_PIN(Y, 7, MUX4)>;
        };

        /* Mapping for PERIPH0_SIGC -> PZ1, to be used for default state */
        /omit-if-no-ref/ periph0_sigc_pz1_default: periph0_sigc_pz1_default {
            pinmux = <VNDSOC_PIN(Z, 1, MUX2)>;
        };
    };

.. code-block:: devicetree

    /* board-pinctrl.dts */
    #include <vnd-soc-pkgxx.dtsi>

    /* Enable pull-up for PX0 (default state) */
    &periph0_siga_px0_default {
        bias-pull-up;
    };

    /* Enable pull-up for PZ1 (default state) */
    &periph0_sigc_pz1_default {
        bias-pull-up;
    };

.. note::

    不建议在预定义节点中添加引脚配置默认值。通常，引脚配置取决于开发板设计或外设的工作条件，因此应由开发板决定。例如，默认启用上拉并不总是合适，因为开发板上可能已经有上拉电阻，或者上拉电阻的阻值取决于总线的运行速度。默认值的另一个缺点是用户可能不知道它们的存在，例如：

    .. code-block:: devicetree

        /* not evident that "periph0_siga_px0_default" also implies "bias-pull-up" */
        /omit-if-no-ref/ periph0_siga_px0_default: periph0_siga_px0_default {
            pinmux = <VNDSOC_PIN(X, 0, MUX0)>;
            bias-pull-up;
        };

实现指南
********

引脚控制驱动
============

引脚控制驱动只需实现一个函数： :c:func:`pinctrl_configure_pins` 。此函数接收一个包含待应用引脚配置的数组。此外，如果设置了 :kconfig:option:`CONFIG_PINCTRL_STORE_REG` ，它还会接收给定引脚所关联的设备寄存器地址。某些驱动可能需要此信息来执行设备特定的操作。

引脚配置存储在一个依赖于厂商或 SoC 的不透明类型中：``pinctrl_soc_pin_t`` 。该类型需要在名为 ``pinctrl_soc.h`` 的头文件中定义，该文件必须位于 Zephyr 的头文件搜索路径中。该类型可以是简单的整数，也可以是包含多个字段的结构体。``pinctrl_soc.h`` 还需要定义一个名为 ``Z_PINCTRL_STATE_PINS_INIT`` 的宏，该宏接受两个参数：节点标识符和属性名称（``pinctrl-N`` ）。宏需要根据这些信息，为给定节点的 ``pinctrl-N`` 属性中包含的所有引脚配置定义初始化器。

对于 Devicetree 中引脚配置的表示方式，厂商可以决定哪种方案更适合其设备。不过，应遵循以下准则：

- 使用 ``pinctrl-N`` （N=0, 1, ...）和 ``pinctrl-names`` 属性定义引脚控制状态。这些属性在 :file:`dts/bindings/pinctrl/pinctrl-device.yaml` 中定义。
- 使用 :file:`dts/bindings/pinctrl/pincfg-node.yaml` 中定义的标准引脚配置属性。

如果同一厂商已在其他操作系统（例如 Linux）中使用某种表示方式，那么即使该表示方式不遵循这些准则，也可能被接受。

设备驱动程序
============

本节介绍设备驱动程序如何使用 ``pinctrl`` API 正确配置所需引脚的一些建议。

需要修改设备 compatible 对应的绑定，使其包含 ``pinctrl-device.yaml`` 。例如：

.. code-block:: yaml

    include: [base.yaml, pinctrl-device.yaml]

需要此文件来为设备添加 ``pinctrl-N`` 和 ``pinctrl-names`` 属性。

从设备驱动程序的角度来看，使用 ``pinctrl`` API 需要执行两个步骤。首先，需要定义引脚控制配置，包括所有状态和引脚。为此，应使用 :c:macro:`PINCTRL_DT_DEFINE` 或 :c:macro:`PINCTRL_DT_INST_DEFINE` 宏。其次，需要保存对该设备实例的 :c:struct:`pinctrl_dev_config` 的引用，因为后续使用 API 时需要此引用。这可以通过 :c:macro:`PINCTRL_DT_DEV_CONFIG_GET` 和 :c:macro:`PINCTRL_DT_INST_DEV_CONFIG_GET` 宏实现。

需要注意，设备与其关联的引脚控制配置之间的唯一联系建立在变量命名约定之上。与设备实例对应的 :c:struct:`pinctrl_dev_config` 实例采用特定的命名方式，使得后续可以根据设备的 Devicetree 节点标识符获取对该配置实例的引用。这样可以尽量减少 ROM 占用，因为只有需要引脚控制的设备才会持有对引脚控制配置的引用。

驱动程序定义引脚控制配置并保存对它的引用后，就可以使用 API 了。应用状态最常用的方式是使用 :c:func:`pinctrl_apply_state` 。如果已提前缓存状态（例如在初始化时），也可以使用更底层的函数 :c:func:`pinctrl_apply_state_direct` 来跳过状态查找。由于状态查找预计耗时很短，因此建议使用 :c:func:`pinctrl_apply_state` 。

下面给出了一个使用 ``pinctrl`` API 的完整设备驱动程序示例。

.. code-block:: c

    /* A driver for the "mydev" compatible device */
    #define DT_DRV_COMPAT mydev

    ...
    #include <zephyr/drivers/pinctrl.h>
    ...

    struct mydev_config {
        ...
        /* Reference to mydev pinctrl configuration */
        const struct pinctrl_dev_config *pcfg;
        ...
    };

    ...

    static int mydev_init(const struct device *dev)
    {
        const struct mydev_config *config = dev->config;
        int ret;
        ...
        /* Select "default" state at initialization time */
        ret = pinctrl_apply_state(config->pcfg, PINCTRL_STATE_DEFAULT);
        if (ret < 0) {
            return ret;
        }
        ...
    }

    #define MYDEV_DEFINE(i)                                                    \
        /* Define all pinctrl configuration for instance "i" */                \
        PINCTRL_DT_INST_DEFINE(i);                                             \
        ...                                                                    \
        static const struct mydev_config mydev_config_##i = {                  \
            ...                                                                \
            /* Keep a ref. to the pinctrl configuration for instance "i" */    \
            .pcfg = PINCTRL_DT_INST_DEV_CONFIG_GET(i),                         \
            ...                                                                \
        };                                                                     \
        ...                                                                    \
                                                                               \
        DEVICE_DT_INST_DEFINE(i, mydev_init, NULL, &mydev_data##i,             \
                              &mydev_config##i, ...);

    DT_INST_FOREACH_STATUS_OKAY(MYDEV_DEFINE)

.. _pinctrl_api:

引脚控制 API
************

.. doxygengroup:: pinctrl_interface

Dynamic pin control
===================

.. doxygengroup:: pinctrl_interface_dynamic


其他参考资料
************

- `Linux 下的引脚复用与 GPIO 控制简介 <https://elinux.org/images/a/a7/ELC-2021_Introduction_to_pin_muxing_and_GPIO_control_under_Linux.pdf>`_
