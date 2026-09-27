.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

.. _migration_3.7:

Zephyr v3.7.0 迁移指南
######################

本文档介绍将应用从 Zephyr v3.6.0 迁移到 Zephyr v3.7.0 所需的变更。

其他变更（与迁移应用不直接相关）请参见 :ref:`版本说明 <zephyr_3.7>`。

.. contents::
    :local:
    :depth: 2

构建系统
********

* 彻底重构了 SoC 和开发板的定义方式。这要求所有树外 SoC 和开发板都移植到新模型。更详细的信息请参见 :ref:`hw_model_v2`。（:github:`69607`）

* 以下构建时生成的头文件：

  .. list-table::
     :header-rows: 1

     * - 受影响的头文件
     * - ``app_version.h``
     * - ``autoconf.h``
     * - ``cmake_intdef.h``
     * - ``core-isa-dM.h``
     * - ``devicetree_generated.h``
     * - ``driver-validation.h``
     * - ``kobj-types-enum.h``
     * - ``linker-kobject-prebuilt-data.h``
     * - ``linker-kobject-prebuilt-priv-stacks.h``
     * - ``linker-kobject-prebuilt-rodata.h``
     * - ``mcuboot_version.h``
     * - ``offsets.h``
     * - ``otype-to-size.h``
     * - ``otype-to-str.h``
     * - ``strerror_table.h``
     * - ``strsignal_table.h``
     * - ``syscall_list.h``
     * - ``version.h``
     * - ``zsr.h``

  以及系统调用头文件和源文件，现在都已纳入 ``zephyr/`` 文件夹的命名空间。此变更基本上是自动完成的，脚本见 :github:`63973`。目前，兼容性 Kconfig（:kconfig:option:`CONFIG_LEGACY_GENERATED_INCLUDE_PATH`）默认启用，以便下游应用仍能编译，但在 CMake 配置期间会产生一条警告消息。该 Kconfig 将在未来弃用并最终移除，建议开发者尽快更新这些受影响头文件的包含路径。

内核
****

* 现在要求所有架构都定义新的 ``struct arch_esf``，用于描述栈帧的成员。这个新结构体取代了具名结构体 ``z_arch_esf_t``。（:github:`73593`）

* 具名结构体 ``z_arch_esf_t`` 现已弃用。请改用 ``struct arch_esf``。（:github:`73593`）

* 头文件 :zephyr_file:`include/zephyr/arch/arch_interface.h` 已从 ``include/zephyr/sys/`` 移到 ``include/zephyr/arch/``。树外源文件需要更新包含路径。（:github:`64987`）

开发板
******

* 重新排列了 SparkFun Pro Micro RP2040 的 ``pro_micro`` 连接器 gpio-map 中 D1 和 D0 的顺序，以与原始 Pro Micro 定义一致。树外扩展板必须更新以反映此变更。（:github:`69994`）
* ITE：重命名所有 SoC 变体 Kconfig 选项，例如 ``CONFIG_SOC_IT82202_AX`` 重命名为 :kconfig:option:`CONFIG_SOC_IT82202AX`。所有符号的重命名如下：``SOC_IT81202BX``、``SOC_IT81202CX``、``SOC_IT81302BX``、``SOC_IT81302CX``、``SOC_IT82002AW``、``SOC_IT82202AX``、``SOC_IT82302AX``。此外，将 ``SOC_SERIES_ITE_IT8XXX2`` 重命名为 ``SOC_SERIES_IT8XXX2``。（:github:`71680`）
* 对于 native_sim/posix：当设置了 :kconfig:option:`CONFIG_I2C` 时，:kconfig:option:`CONFIG_EMUL` 不再默认启用。需要启用该设置的用户应在其项目配置文件中自行设置。（:github:`73067`）

* LiteX：将 LiteX VexRiscV 中断控制器节点的 ``compatible`` 从 ``vexriscv-intc0`` 重命名为 :dtcompatible:`litex,vexriscv-intc0`。（:github:`73211`）

* ``lairdconnect`` 开发板现在改为 ``ezurio`` 开发板。Laird Connectivity 已更名为 `Ezurio <https://www.ezurio.com/laird-connectivity>`_。

模块
****

Mbed TLS
========

* TLS 1.2、RSA、AES、DES 以及除 SHA-256 之外的所有哈希算法（SHA-224、SHA-384、SHA-512、MD5 和 SHA-1）不再默认启用。现在需要显式启用各自的 Kconfig 选项才能使用它们。（:github:`72078`）
* 以前命名为 ``CONFIG_MBEDTLS_MAC_*_ENABLED`` 的 Kconfig 选项已重命名，名称中的 ``_MAC`` 和 ``_ENABLED`` 部分已被去掉。（:github:`73267`）
* :kconfig:option:`CONFIG_MBEDTLS_HASH_ALL_ENABLED` Kconfig 选项已修复，现在会真正启用所有可用的哈希算法。以前它只启用 SHA-2 系列。（:github:`73267`）
* ``CONFIG_MBEDTLS_HASH_SHA*_ENABLED`` Kconfig 选项已被移除。它们与其他 Kconfig 选项重复，后者现在命名为 ``CONFIG_MBEDTLS_SHA*``。（:github:`73267`）
* ``CONFIG_MBEDTLS_MAC_ALL_ENABLED`` Kconfig 选项已被移除。其等效项是 :kconfig:option:`CONFIG_MBEDTLS_HASH_ALL_ENABLED` 与 :kconfig:option:`CONFIG_MBEDTLS_CMAC` 的组合。（:github:`73267`）
* Kconfig 选项 ``CONFIG_MBEDTLS_MAC_MD4_ENABLED``、``CONFIG_MBEDTLS_CIPHER_ARC4_ENABLED`` 和 ``CONFIG_MBEDTLS_CIPHER_BLOWFISH_ENABLED`` 已被移除，因为 Mbed TLS 不再支持它们。（:github:`73222`）
* 当系统中存在任何 PSA 加密提供者时（即设置了 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_CLIENT`），所需的 PSA 加密功能必须通过相应的 ``CONFIG_PSA_WANT_*`` 显式启用。（:github:`72243`）
* 只要系统中存在任何 PSA 加密提供者（即设置了 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_CLIENT`），TLS/X509/PK/MD 模块就会使用 PSA 加密 API，而不再使用旧版 API。（:github:`72243`）

Trusted Firmware-M
==================

* 默认的 MCUboot 签名类型已从 RSA-3072 改为 EC-P256。这会影响在 TF-M 中启用 MCUboot 的构建（:kconfig:option:`CONFIG_TFM_BL2`）。如果你希望继续使用 RSA-3072，需要将 :kconfig:option:`CONFIG_TFM_MCUBOOT_SIGNATURE_TYPE` 设置为 ``"RSA-3072"``。否则，请确保拥有并使用该签名类型对应的签名密钥。

LVGL
====

* :kconfig:option:`CONFIG_LV_Z_POINTER_KSCAN` 已被移除，你需要将基于 kscan 的驱动转换为输入子系统，并改为在设备树中使用 :dtcompatible:`zephyr,lvgl-pointer-input`。（:github:`73800`）


设备驱动与设备树
****************

* :dtcompatible:`nxp,kinetis-pit` pit 驱动的兼容属性已改为 :dtcompatible:`nxp,pit`，并已更新为支持多个通道。要配置各个通道，必须添加一个兼容属性为 :dtcompatible:`nxp,pit-channel` 的子节点，并按下面所示进行配置。随着 pit 绑定的重命名，:kconfig:option:`CONFIG_COUNTER_MCUX_PIT` 也已重命名为 :kconfig:option:`CONFIG_COUNTER_NXP_PIT`。（:github:`66336`）示例如下：

  .. code-block:: devicetree

    / {
        pit0: pit@40037000 {
            /* Other Pit DT Attributes */
            compatible = "nxp,pit";
            status = "disabled";
            num-channels = <1>;
            #address-cells = <1>;
            #size-cells = <0>;

            pit0_channel0: pit0_channel@0 {
                compatible = "nxp,pit-channel";
                reg = <0>;
                status = "disabled";
            };
    };

* :dtcompatible:`nxp,kinetis-ethernet` 已弃用，取而代之的是 :dtcompatible:`nxp,enet`。所有树内 SoC 都已改用这一新方案。因此，所有使用 NXP ENET 外设的开发板都需要在设备树中改为使用该绑定，同时也需要配套使用不同版本的驱动。或者，也可以删除以太网节点，并按旧绑定重新定义，以使用已弃用的旧版驱动。新绑定的主要优势是能够通过 MDIO API 抽象任意 PHY。（:github:`70400`）基本开发板级 ENET 设备树定义示例：

  .. code-block:: devicetree

    &enet_mac {
        status = "okay";
        pinctrl-0 = <&pinmux_enet>;
        pinctrl-names = "default";
        phy-handle = <&phy>;
        zephyr,random-mac-address;
        phy-connection-type = "rmii";
    };

    &enet_mdio {
        status = "okay";
        pinctrl-0 = <&pinmux_enet_mdio>;
        pinctrl-names = "default";
        phy: phy@3 {
            compatible = "ethernet-phy";
            reg = <3>;
            status = "okay";
        };
    };

* :dtcompatible:`nxp,kinetis-lptmr` 的兼容字符串已改为 :dtcompatible:`nxp,lptmr`。旧字符串在短时间内仍可使用，但应尽早替换，因为它将在未来移除。

* 一些驱动 API 结构体已重命名，以带上必需的 ``_driver_api`` 后缀。（:github:`72182`）以下类型已重命名：

  * ``emul_sensor_backend_api`` 改为 :c:struct:`emul_sensor_driver_api`
  * ``emul_bbram_backend_api`` 改为 :c:struct:`emul_bbram_driver_api`
  * ``usbc_ppc_drv`` 改为 :c:struct:`usbc_ppc_driver_api`

* :dtcompatible:`maxim,max31790` 的驱动已拆分为一个 MFD 和一个实际的 PWM 驱动。（:github:`68433`）以前，该器件的一个实例可以这样定义：

  .. code-block:: devicetree

    max31790_max31790: max31790@20 {
        compatible = "maxim,max31790";
        status = "okay";
        reg = <0x20>;
        pwm-controller;
        #pwm-cells = <2>;
    };

  可以转换为：

  .. code-block:: devicetree

    max31790_max31790: max31790@20 {
        compatible = "maxim,max31790";
        status = "okay";
        reg = <0x20>;

        max31790_max31790_pwm: max31790_max31790_pwm {
            compatible = "maxim,max31790-pwm";
            status = "okay";
            pwm-controller;
            #pwm-cells = <2>;
        };
    };

* :dtcompatible:`invensense,icm42688` 的驱动现在能正确支持设备树配置（:github:`74267`）。以前的设备树可能尝试使用绑定来设置加速度计/陀螺仪的采样率和量程，但没有任何效果。现在使用设备树时应使用所提供的定义和包含文件，以及采用这些值的新绑定。

  例如：

  .. code-block:: devicetree

    #include <zephyr/dt-bindings/sensor/icm42688.h>

    icm42688: icm42688@0 {
        accel-pwr-mode = <ICM42688_ACCEL_LN>;
        accel-fs = <ICM42688_ACCEL_FS_16G>;
        accel-odr = <ICM42688_ACCEL_ODR_2000>;
        gyro-pwr-mode= <ICM42688_GYRO_LN>;
        gyro-fs = <ICM42688_GYRO_FS_2000>;
        gyro-odr = <ICM42688_GYRO_ODR_2000>;
    };

* :dtcompatible:`st,lis2mdl` 的属性 ``spi-full-duplex`` 已改为 ``duplex = SPI_FULL_DUPLEX``。全双工现在是默认设置。

* :dtcompatible:`nxp,lpc-lpadc` 驱动的设备树属性 ``nxp,reference-supply`` 已被移除，如果设备树中存在该属性，用户应将其删除。新增了 phandle-array 类型的设备树属性 ``nxp,references``，用户可以用该属性指定 lpadc 要使用的参考电压及其数值。（:github:`75005`）

 * :dtcompatible:`microchip,ksz8081` PHY 绑定的设备树属性 ``mc,interface-type``、``mc,reset-gpio`` 和 ``mc,interrupt-gpio`` 已分别改为 ``microchip,interface-type``、``reset-gpios`` 和 ``int-gpios``，参见 :github:`73725`

充电器
======

* 从 ``charger_max20335`` 驱动中删除了 ``constant-charge-current-max-microamp`` 属性，因为它不能反映芯片的真实功能。（:github:`69910`）

* 在 ``maxim,max20335-charger`` 绑定中为 ``constant-charge-voltage-max-microvolt`` 属性添加了枚举键，以便在构建时指示无效的设备树值。（:github:`69910`）

控制器局域网（CAN）
===================

* 移除了以下已弃用的 CAN 控制器设备树属性。使用这些属性的树外开发板可以改用 ``bitrate``、``sample-point``、``bitrate-data`` 和 ``sample-point-data`` 设备树属性（或依赖 :kconfig:option:`CONFIG_CAN_DEFAULT_BITRATE` 和 :kconfig:option:`CONFIG_CAN_DEFAULT_BITRATE_DATA`）来指定初始 CAN 位速率：

  * ``sjw``
  * ``prop-seg``
  * ``phase-seg1``
  * ``phase-seg2``
  * ``sjw-data``
  * ``prop-seg-data``
  * ``phase-seg1-data``
  * ``phase-seg2-data``

  CAN 控制器的设备树属性 ``bus-speed`` 和 ``bus-speed-data`` 已弃用。

  （:github:`68714`）

* 手动总线关闭恢复的支持已重构（:github:`69460`）：

  * 无论 Kconfig 选项如何，自动总线恢复都将在驱动初始化时启用。由于 CAN 控制器初始化时处于 “stopped” 状态，此时不会启动不必要的总线关闭恢复。
  * Kconfig ``CONFIG_CAN_AUTO_BUS_OFF_RECOVERY`` 已重命名（并取反）为 :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE`，后者默认禁用。该 Kconfig 选项启用对 :c:func:`can_recover()` API 函数以及新的手动恢复模式的支持（参见下一条）。
  * 新增了 CAN 控制器运行模式 :c:macro:`CAN_MODE_MANUAL_RECOVERY`。仅当启用 :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE` 时才支持该模式。将其作为一种模式，使应用可以通过 :c:func:`can_get_capabilities` API 函数查询 CAN 控制器是否支持手动恢复模式。随后应用可以选择让初始化失败，或者依赖自动总线关闭恢复。将其作为一种模式还可以让不支持手动恢复模式的 CAN 控制器驱动在应用启动期间的 :c:func:`can_set_mode` 中提前失败，而不是在稍后调用 :c:func:`can_recover` 时才失败。

加密
====

* CSS 驱动在 NXP lpc55s36 上已弃用（:github:`71173`）。

显示
====

* 基于 GC9X01 的显示屏现在使用 MIPI DBI 驱动类。这些显示屏现在必须声明在 MIPI DBI 驱动包装设备中，由后者管理与显示屏的接口。（:github:`73686`）示例请见下文：

  .. code-block:: devicetree

    /* Legacy GC9X01 display definition */
    &spi0 {
        gc9a01: gc9a01@0 {
            status = "okay";
            compatible = "galaxycore,gc9x01x";
            reg = <0>;
            spi-max-frequency = <100000000>;
            cmd-data-gpios = <&gpio0 8 GPIO_ACTIVE_HIGH>;
            reset-gpios = <&gpio0 14 GPIO_ACTIVE_LOW>;
            ...
        };
    };

    /* New display definition with MIPI DBI device */

    #include <zephyr/dt-bindings/mipi_dbi/mipi_dbi.h>

    ...

    mipi_dbi {
        compatible = "zephyr,mipi-dbi-spi";
        dc-gpios = <&gpio0 8 GPIO_ACTIVE_HIGH>;
        reset-gpios = <&gpio0 14 GPIO_ACTIVE_LOW>;
        spi-dev = <&spi0>;
        #address-cells = <1>;
        #size-cells = <0>;

        gc9a01: gc9a01@0 {
            status = "okay";
            compatible = "galaxycore,gc9x01x";
            reg = <0>;
            mipi-max-frequency = <100000000>;
            ...
        };
    };


* 基于 ST7735R 的显示屏现在使用 MIPI DBI 驱动类。这些显示屏现在必须声明在 MIPI DBI 驱动包装设备中，由后者管理与显示屏的接口。请注意，随着此次更新，``cmd-data-gpios`` 引脚极性已改变，以更好地与新名称 ``dc-gpios`` 保持一致。示例请见下文：

  .. code-block:: devicetree

    /* Legacy ST7735R display definition */
    &spi0 {
        st7735r: st7735r@0 {
            compatible = "sitronix,st7735r";
            reg = <0>;
            spi-max-frequency = <32000000>;
            reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
            cmd-data-gpios = <&gpio0 12 GPIO_ACTIVE_LOW>;
            ...
        };
    };

    /* New display definition with MIPI DBI device */

    #include <zephyr/dt-bindings/mipi_dbi/mipi_dbi.h>

    ...

    mipi_dbi {
        compatible = "zephyr,mipi-dbi-spi";
        reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
        dc-gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
        spi-dev = <&spi0>;
        #address-cells = <1>;
        #size-cells = <0>;

        st7735r: st7735r@0 {
            compatible = "sitronix,st7735r";
            reg = <0>;
            mipi-max-frequency = <32000000>;
            mipi-mode = <MIPI_DBI_MODE_SPI_4WIRE>;
            ...
        };
    };

* 基于 UC81XX 的显示屏现在使用 MIPI DBI 驱动类。这些显示屏现在必须声明在 MIPI DBI 驱动包装设备中，由后者管理与显示屏的接口。（:github:`73812`）请注意，随着此次更新，``dc-gpios`` 引脚极性已改变，示例请见下文：

  .. code-block:: devicetree

    /* Legacy UC81XX display definition */
    &spi0 {
        uc8179: uc8179@0 {
            compatible = "ultrachip,uc8179";
            reg = <0>;
            spi-max-frequency = <4000000>;
            reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
            dc-gpios = <&gpio0 12 GPIO_ACTIVE_LOW>;
            ...
        };
    };

    /* New display definition with MIPI DBI device */

    #include <zephyr/dt-bindings/mipi_dbi/mipi_dbi.h>

    ...

    mipi_dbi {
        compatible = "zephyr,mipi-dbi-spi";
        reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
        dc-gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
        spi-dev = <&spi0>;
        #address-cells = <1>;
        #size-cells = <0>;
        uc8179: uc8179@0 {
            compatible = "ultrachip,uc8179";
            reg = <0>;
            mipi-max-frequency = <4000000>;
            ...
        };
    };

* 基于 ST7789V 的显示屏现在使用 MIPI DBI 驱动类。这些显示屏现在必须声明在 MIPI DBI 驱动包装设备中，由后者管理与显示屏的接口。（:github:`73750`）请注意，随着此次更新，``cmd-data-gpios`` 引脚极性已改变，以更好地与新名称 ``dc-gpios`` 保持一致。示例请见下文：

  .. code-block:: devicetree

    /* Legacy ST7789V display definition */
    &spi0 {
        st7789: st7789@0 {
            compatible = "sitronix,st7789v";
            reg = <0>;
            spi-max-frequency = <32000000>;
            reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
            cmd-data-gpios = <&gpio0 12 GPIO_ACTIVE_LOW>;
            ...
        };
    };

    /* New display definition with MIPI DBI device */

    #include <zephyr/dt-bindings/mipi_dbi/mipi_dbi.h>

    ...

    mipi_dbi {
        compatible = "zephyr,mipi-dbi-spi";
        reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
        dc-gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
        spi-dev = <&spi0>;
        #address-cells = <1>;
        #size-cells = <0>;

        st7789: st7789@0 {
            compatible = "sitronix,st7789v";
            reg = <0>;
            mipi-max-frequency = <32000000>;
            mipi-mode = <MIPI_DBI_MODE_SPI_4WIRE>;
            ...
        };
    };

* 基于 SSD16XX 的显示屏现在使用 MIPI DBI 驱动类（:github:`73946`）。这些显示屏现在必须声明在 MIPI DBI 驱动包装设备中，由后者管理与显示屏的接口。请注意，随着此次更新，``dc-gpios`` 引脚极性已改变。示例请见下文：

  .. code-block:: devicetree

    /* Legacy SSD16XX display definition */
    &spi0 {
        ssd1680: ssd1680@0 {
            compatible = "solomon,ssd1680";
            reg = <0>;
            spi-max-frequency = <4000000>;
            reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
            dc-gpios = <&gpio0 12 GPIO_ACTIVE_LOW>;
            ...
        };
    };

    /* New display definition with MIPI DBI device */

    #include <zephyr/dt-bindings/mipi_dbi/mipi_dbi.h>

    ...

    mipi_dbi {
        compatible = "zephyr,mipi-dbi-spi";
        reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
        dc-gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
        spi-dev = <&spi0>;
        #address-cells = <1>;
        #size-cells = <0>;

        ssd1680: ssd1680@0 {
            compatible = "solomon,ssd1680";
            reg = <0>;
            mipi-max-frequency = <4000000>;
            ...
        };
    };

* SSD16XX 显示驱动中的 ``orientation-flipped`` 属性已被移除，因为该驱动现在支持显示旋转。用户应从设备树中删除该属性，并在运行时通过 :c:func:`display_set_orientation` 设置方向（:github:`73360`）

增强型串行外设接口（eSPI）
==========================

* 宏 ``ESPI_SLAVE_TO_MASTER`` 和 ``ESPI_MASTER_TO_SLAVE`` 已分别重命名为 ``ESPI_TARGET_TO_CONTROLLER`` 和 ``ESPI_CONTROLLER_TO_TARGET``，以反映 eSPI 1.5 规范中的新术语。枚举值 ``ESPI_VWIRE_SIGNAL_SLV_BOOT_STS``、``ESPI_VWIRE_SIGNAL_SLV_BOOT_DONE`` 以及所有 ``ESPI_VWIRE_SIGNAL_SLV_GPIO_<NUMBER>`` 信号已分别重命名为 ``ESPI_VWIRE_SIGNAL_TARGET_BOOT_STS``、``ESPI_VWIRE_SIGNAL_TARGET_BOOT_DONE`` 和 ``ESPI_VWIRE_SIGNAL_TARGET_GPIO_<NUMBER>``，以反映 eSPI 1.5 规范中的新术语。（:github:`68492`）Kconfig ``CONFIG_ESPI_SLAVE`` 已重命名为 :kconfig:option:`CONFIG_ESPI_TARGET`，类似地 ``CONFIG_ESPI_SAF`` 已重命名为 :kconfig:option:`CONFIG_ESPI_TAF`，参见 :github:`73887`

GNSS
====

* ``gnss-nmea-generic`` 驱动新增了基本的电源管理支持。如果 ``CONFIG_PM_DEVICE=y``，该驱动现在会以挂起模式初始化，应用需要调用 :c:func:`pm_device_action_run` 并传入 :c:macro:`PM_DEVICE_ACTION_RESUME` 来启动驱动。（:github:`71774`）

输入
====

* ``analog-axis`` 死区校准值已改为相对于原始 ADC 值，与最小值和最大值类似。数据结构与属性也已相应重命名（从 ``out-deadzone`` 改为 ``in-deadzone``），迁移到新定义时，该值应按比例缩放。（:github:`70377`）

* ``holtek,ht16k33-keyscan`` 驱动已改为使用 :ref:`input` 子系统，回调必须迁移为使用输入 API，:dtcompatible:`zephyr,kscan-input` 可用于向后兼容。（:github:`69875`）

中断控制器
==========

* 多级中断控制器查找表的静态自动生成已被弃用，只有在启用新的兼容性 Kconfig :kconfig:option:`CONFIG_LEGACY_MULTI_LEVEL_TABLE_GENERATION` 时才会编译，后者最终将在未来版本中移除。

  多级中断控制器驱动应更新为使用新建的 ``IRQ_PARENT_ENTRY_DEFINE`` 宏，以便向新的多级中断架构注册自身。为便于使用该宏，新增了 ``INTC_INST_ISR_TBL_OFFSET`` 宏，用于推导给定驱动实例的软件 ISR 表偏移量；对于伪中断控制器子节点，请改用 ``INTC_CHILD_ISR_TBL_OFFSET`` 宏。此外还新增了设备树宏（``DT_INTC_GET_AGGREGATOR_LEVEL`` 和 ``DT_INST_INTC_GET_AGGREGATOR_LEVEL``），供中断控制器驱动实例将自己的聚合器层级传递给 ``IRQ_PARENT_ENTRY_DEFINE`` 宏。

LED 灯带
========

* :dtcompatible:`worldsemi,ws2812-gpio` 中定义的 ``in-gpios`` 属性已重命名为 ``gpios``。（:github:`68514`）

* ``chain-length`` 和 ``color-mapping`` 属性已添加到所有 LED 灯带绑定中，并且现在是必需的。

* 新增了必需的 ``length`` 函数，用于返回 LED 灯带设备的长度（像素数量）。

* 将 ``update_channels`` 函数改为可选，并移除了未实现的函数。

* ``CONFIG_WS2812_STRIP_DRIVER`` Kconfig 选项已被移除。以前，使用 :kconfig:option:`CONFIG_WS2812_STRIP_SPI`、:kconfig:option:`CONFIG_WS2812_STRIP_I2S`、:kconfig:option:`CONFIG_WS2812_STRIP_GPIO` 或 :kconfig:option:`CONFIG_WS2812_STRIP_RPI_PICO_PIO` 时必须通过 ``CONFIG_WS2812_STRIP_DRIVER`` 选择其中之一，但现在不再需要。请直接设置各个选项。

MDIO
====

* :kconfig:option:`CONFIG_MDIO_NXP_ENET_TIMEOUT` 现在的单位是微秒，而不再是毫秒。（:github:`75625`）

传感器
======

* :dtcompatible:`sensirion,shtcx` 传感器驱动的 ``chip`` 设备树属性已被移除。芯片变体现在通过匹配的 compatible 属性选择（:github:`74033`）。新的 shtc3 配置示例请见下文：

  .. code-block:: devicetree

    &i2c0 {
        status = "okay";

        shtc3: shtc3@70 {
            compatible = "sensirion,shtc3", "sensirion,shtcx";
            reg = <0x70>;
            measure-mode = "normal";
            clock-stretching;
        };
    };

串行接口
========

* Raspberry Pi UART 驱动 ``uart_rpi_pico`` 已被移除。请改用 ``uart_pl011`` 驱动（:dtcompatible:`arm,pl011`）。（:github:`71074`）

稳压器
======

* :dtcompatible:`nxp,vref` 驱动不再支持地选择功能，因为该设置不应由用户修改。设备树属性 ``nxp,ground-select`` 已被移除，如果设备树中存在该属性，用户应将其删除。（:github:`70642`）

W1
==

* :dtcompatible:`zephyr,w1-gpio` 1-Wire 主机驱动不再默认启用 GPIO 引脚的内部上拉电阻。现在该配置取自设备树中指定的引脚配置标志。（:github:`71789`）

看门狗
======

* ``nuvoton,npcx-watchdog`` 驱动已更改，以延长最大超时时间。一次看门狗计数的时长会随不同的预分频设置而变化。移除了 :kconfig:option:`CONFIG_WDT_NPCX_DELAY_CYCLES`，因为它不再适合用于设置前置警告时间。取而代之，新增了 :kconfig:option:`CONFIG_WDT_NPCX_WARNING_LEADING_TIME_MS`，用于以毫秒为单位设置前置警告时间。

蓝牙
****

蓝牙 HCI
========

 * 引入了新的 HCI 驱动 API（:github:`72323`），旧 API 已弃用。新 API 遵循 Zephyr 常规的驱动模型，使用设备树节点等。主机现在通过查找 ``zephyr,bt-hci`` chosen 属性来选择使用哪个驱动实例作为控制器。所有 HCI 驱动的设备树绑定都派生自通用的 ``bt-hci.yaml`` 基础绑定。

  * 作为新 HCI 驱动 API 的一部分，不再使用 ``zephyr,bt-uart`` chosen 属性；UART HCI 驱动改为查找 HCI 驱动实例节点的父设备树节点来选择其 UART。
  * 作为新 HCI 驱动 API 的一部分，``zephyr,bt-hci-ipc`` chosen 属性仅用于控制器侧，而 HCI 驱动现在依赖兼容字符串为 ``zephyr,bt-hci-ipc`` 的节点。
  * ``BT_NO_DRIVER`` Kconfig 选项已被移除。HCI 驱动不再置于 Kconfig choice 之下，现在可以独立启用和禁用，主要取决于各自设备树节点是否启用。
  * ``BT_HCI_VS_EXT`` Kconfig 选项已被删除，该功能现已包含在 :kconfig:option:`CONFIG_BT_HCI_VS` Kconfig 选项中。
  * ``BT_HCI_VS_EVT`` Kconfig 选项已被移除，因为只要启用 :kconfig:option:`CONFIG_BT_HCI_VS` 选项，厂商事件支持就是隐含的。
  * bt_read_static_addr() API 已被移除。它严格来说并不是一个完全公开的 API，但由于它经由公开的 hci_driver.h 头文件暴露，因此在此提及这一移除。请改为启用 :kconfig:option:`CONFIG_BT_HCI_VS` Kconfig 选项，并使用厂商特定的 HCI 命令 API 在可用时获取控制器的蓝牙静态地址。

蓝牙 Mesh
=========

* :c:struct:`bt_mesh_model` 的模型元数据指针声明已更改，添加了 ``const`` 限定符。:c:struct:`bt_mesh_models_metadata_entry` 的数据指针也加上了 ``const`` 限定符。模型的元数据结构体和元数据原始值可以声明为非易失性存储器中的永久常量。（:github:`69679`）

* :c:struct:`bt_mesh_model` 的模型元数据指针声明已改为单个 ``const *``，并移除了 :c:struct:`bt_mesh_health_srv` 中多余的元数据指针。因此，:code:`BT_MESH_MODEL_HEALTH_SRV` 定义已改为使用可变参数表示法。现在，当你的实现支持 :kconfig:option:`CONFIG_BT_MESH_LARGE_COMP_DATA_SRV` 并且需要为 Health Server 模型指定元数据时，只需将元数据作为最后一个参数传给 :code:`BT_MESH_MODEL_HEALTH_SRV` 宏；否则省略最后一个参数。（:github:`71281`）

蓝牙音频
========

* 启用 :kconfig:option:`CONFIG_BT_BAP_UNICAST_SERVER` 时，:kconfig:option:`CONFIG_BT_ASCS`、:kconfig:option:`CONFIG_BT_PERIPHERAL` 和 :kconfig:option:`CONFIG_BT_ISO_PERIPHERAL` 不再自动启用，现在必须在项目配置文件中显式设置。（:github:`71993`）

* CAP 的发现回调函数 :code:`bt_cap_initiator_cb.unicast_discovery_complete` 和 :code:`bt_cap_commander_cb.discovery_complete` 现在多了一个用于集合成员的参数。所有已定义的 CAP 发现回调函数实例都需要添加该参数。（:github:`72797`）

* :c:func:`bt_bap_stream_start` 不再连接 CIS。要连接 CIS，现在应在 :c:func:`bt_bap_stream_start` 之前调用 :c:func:`bt_bap_stream_connect`。（:github:`73032`）

* 将 ``stream_lang`` 重命名为 ``lang``，以更好地与分配编号文档保持一致。这会影响 ``BT_AUDIO_METADATA_TYPE_LANG`` 宏以及以下函数：

  * :c:func:`bt_audio_codec_cap_meta_set_lang`
  * :c:func:`bt_audio_codec_cap_meta_get_lang`
  * :c:func:`bt_audio_codec_cfg_meta_set_lang`
  * :c:func:`bt_audio_codec_cfg_meta_get_lang`

  （:github:`72584`）

* 将 ``lang`` 从 ``uint32_t`` 改为 ``uint8_t [3]``。这会修改以下函数：

  * :c:func:`bt_audio_codec_cap_meta_set_lang`
  * :c:func:`bt_audio_codec_cap_meta_get_lang`
  * :c:func:`bt_audio_codec_cfg_meta_set_lang`
  * :c:func:`bt_audio_codec_cfg_meta_get_lang`

  这样做的结果是，现在可以使用 ``"eng"`` 和 ``"deu"`` 之类的字符串值来设置新值，并且可以避免获取值时不必要的数据拷贝。（:github:`72584`）

* 所有 ``set_sirk`` 的出现都已改为 ``sirk``，因为 ``sirk`` 中的 ``s`` 就代表 set。（:github:`73413`）

* 为 :c:func:`bt_audio_codec_cfg_get_chan_allocation` 添加了 ``fallback_to_default`` 参数。要保持现有行为，请将该参数设置为 ``false``。（:github:`72090`）

* 为 :c:func:`bt_audio_codec_cap_get_supported_audio_chan_counts` 添加了 ``fallback_to_default`` 参数。要保持现有行为，请将该参数设置为 ``false``。（:github:`72090`）

* 为 :c:func:`bt_audio_codec_cap_get_max_codec_frames_per_sdu` 添加了 ``fallback_to_default`` 参数。要保持现有行为，请将该参数设置为 ``false``。（:github:`72090`）

* 为 :c:func:`bt_audio_codec_cfg_meta_get_pref_context` 添加了 ``fallback_to_default`` 参数。要保持现有行为，请将该参数设置为 ``false``。（:github:`72090`）

经典蓝牙
========

* Host BR/EDR 的源文件已移到 ``subsys/bluetooth/host/classic``。Host BR/EDR 的头文件已移到 ``include/zephyr/bluetooth/classic``。移除了 :kconfig:option:`CONFIG_BT_BREDR`，它已被新选项 :kconfig:option:`CONFIG_BT_CLASSIC` 取代。（:github:`69651`）

蓝牙主机
========

* 广播选项 :code:`BT_LE_ADV_OPT_USE_NAME` 和 :code:`BT_LE_ADV_OPT_FORCE_NAME_IN_AD` 在此版本中已弃用。应用需要显式包含设备名称。一种做法是将以下内容添加到传给主机的广播数据或扫描响应数据中：

  .. code-block:: c

   BT_DATA(BT_DATA_NAME_COMPLETE, CONFIG_BT_DEVICE_NAME, sizeof(CONFIG_BT_DEVICE_NAME) - 1)

  （:github:`71686`）

* :c:type:`bt_l2cap_le_endpoint` 中的字段 :code:`init_credits` 已被移除，因为它在 Zephyr 3.4.0 及更高版本中已不再使用。任何对该字段的引用都应删除。无需其他操作。

* :c:macro:`BT_LE_ADV_PARAM` 现在返回 :code:`const` 指针。任何将结果存储到局部变量的地方，例如 :code:`struct bt_le_adv_param *param = BT_LE_ADV_CONN;`，都需要改为 :code:`const struct bt_le_adv_param *param = BT_LE_ADV_CONN;`，或者像 :code:`struct bt_le_adv_param param = *BT_LE_ADV_CONN;` 这样用于初始化

  对 :c:macro:`BT_LE_ADV_PARAM` 的更改也影响其所有派生宏，包括但不限于：

  * :c:macro:`BT_LE_ADV_CONN`
  * :c:macro:`BT_LE_ADV_NCONN`
  * :c:macro:`BT_LE_EXT_ADV_SCAN`
  * :c:macro:`BT_LE_EXT_ADV_CODED_NCONN_NAME`

  （:github:`75065`）

* :kconfig:option:`CONFIG_BT_BUF_ACL_RX_COUNT` 现在需要大于 :kconfig:option:`CONFIG_BT_MAX_CONN`。由于 HCI 接口的设计，这一直是必需的。现在通过构建时断言强制执行。

  （:github:`75592`）

蓝牙加密
========

* 新增了 :kconfig:option:`CONFIG_BT_USE_PSA_API`，用于显式请求加密操作使用 PSA API 而不是 TinyCrypt。当然，只有在系统中存在可用的 PSA 加密提供者（即设置了 :kconfig:option:`CONFIG_PSA_CRYPTO_CLIENT`）时才能这样做。（:github:`73378`）

网络
****

* 弃用 :kconfig:option:`CONFIG_NET_SOCKETS_POSIX_NAMES` 选项。这是一个旧选项，用于允许用户在未启用 POSIX API 的情况下调用 BSD 套接字 API。这可能会在构建希望启用 :kconfig:option:`CONFIG_POSIX_API` 选项的应用时带来复杂性。这意味着，如果应用想使用常规 BSD 套接字接口，就需要启用 :kconfig:option:`CONFIG_POSIX_API`。如果应用不想或无法启用该选项，则套接字 API 调用需要以 ``zsock_`` 字符串为前缀。所有使用 BSD 套接字接口的示例应用都已改为启用 :kconfig:option:`CONFIG_POSIX_API`。在网络协议栈内部，将不再启用 POSIX API 选项，这意味着各种使用套接字的网络库都已改为使用 ``zsock_*`` API 调用。（:github:`69950`）

* zperf 的 zperf_results 结构体已更改，以支持 64 位的传输字节数（total_len）和测试时长（time_in_us 和 client_time_in_us），而不再是 32 位。这将使长时间的 zperf 测试显示正确的吞吐量结果。（:github:`69500`）

* 分配给网络接口的每个 IPv4 地址现在各自带有一个 IPv4 子网掩码，而不再为整个接口设置一个。如果网络接口只指定了一个 IPv4 地址，则从用户角度看没有任何变化。但如果存在多个 IPv4 地址/网络接口，则必须为每个 IPv4 地址单独指定子网掩码。（:github:`68419`）

* 虚拟网络接口 API 不再提供 ``input`` 回调。input 回调过去用于读取 IP 隧道中的内部 IPv4/IPv6 报文。这种入向隧道读取现在改在 ``recv`` 回调中实现。（:github:`70549`）

* 虚拟局域网（VLAN）的实现已改为使用虚拟网络接口。API 没有变化，但 VLAN 网络接口的类型已从 ``ETHERNET`` 改为 ``VIRTUAL``。这可能需要改动为网络接口设置 VLAN 标签的代码。例如在 :c:func:`net_eth_is_vlan_enabled()` API 中，第 2 个接口参数必须指向主以太网接口，而不是 VLAN 接口。（:github:`70345`）

* 将 ``wifi connect`` 命令改为对参数使用键值格式。在此前的实现中，我们通过选项在参数字符串中的位置来识别它。这使得处理可选参数或扩展对其他选项的支持变得困难。采用键值格式后，更容易扩展可传给 connect 命令的选项。``wifi -h`` 会提供有关 connect 命令用法的更多信息。（:github:`70024`）

* Kconfig :kconfig:option:`CONFIG_NET_TCP_ACK_TIMEOUT` 已弃用。它的用途仅限于 TCP 握手，而在这种情况下，总超时应该取决于总重传超时（与其他情况一样），这使得该配置项既多余又容易混淆。请改用 :kconfig:option:`CONFIG_NET_TCP_INIT_RETRANSMISSION_TIMEOUT` 和 :kconfig:option:`CONFIG_NET_TCP_RETRY_COUNT` 来控制 TCP 层的总超时。（:github:`70731`）

* 在 LwM2M API 中，回调类型 :c:type:`lwm2m_engine_set_data_cb_t` 现在多了一个 ``offset`` 参数。该参数用于指示 CoAP 块传输（Block-wise transfer）期间数据的偏移量。任何写入后、校验或固件相关的回调都应更新以包含该参数。（:github:`72590`）

* DNS 解析器以及 mDNS/LLMNR 应答器已改为使用套接字服务 API。这意味着系统中可轮询套接字数量可能需要增加。请检查 ``CONFIG_NET_SOCKETS_POLL_MAX`` 和 :kconfig:option:`CONFIG_POSIX_MAX_FDS` 的值是否足够大。遗憾的是，无法给出这两个值的准确数值，因为这取决于应用的需求和使用情况。（:github:`72834`）

* ``socket`` API 调用中数据包套接字（类型 ``AF_PACKET``）的协议字段已更改。协议字段应使用网络字节序，以便与 Linux 套接字调用兼容。如果希望接收所有网络报文，Linux 期望协议字段为 ``htons(ETH_P_ALL)``。详情请参见 https://www.man7.org/linux/man-pages/man7/packet.7.html 文档。（:github:`73338`）

* TCP 现在使用 SHA-256 而不是 MD5 来生成 ISN。该哈希计算的加密支持也已从 Mbed TLS 改为 PSA API。实现方式是将 :kconfig:option:`CONFIG_NET_TCP_ISN_RFC6528` 改为依赖 :kconfig:option:`PSA_WANT_ALG_SHA_256`，而不再依赖旧的 ``CONFIG_MBEDTLS_*`` 特性。（:github:`71827`）

其他子系统
**********

Flash 映射
==========

* flash 校验功能（:kconfig:option:`CONFIG_FLASH_AREA_CHECK_INTEGRITY_BACKEND`）的加密后端以前由 TinyCrypt 或 Mbed TLS 提供，现在改为由 PSA 或 Mbed TLS 提供。更新后的 Mbed TLS 实现比先前的 TinyCrypt 实现占用略小，而 PSA 实现对于使用 TF-M 构建的设备能进一步减小占用。PSA 是受支持的未来方向，不过目前如果你无法承担启用 PSA API 的一次性开销（对于没有 TF-M 的设备是 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_C`），仍然可以使用 Mbed TLS。:github:`73511`

hawkBit
=======

* :kconfig:option:`CONFIG_HAWKBIT_PORT` 现在是 int 类型而不是字符串类型。使用 hawkBit 需要启用 :kconfig:option:`CONFIG_SETTINGS`，因为它现在使用 settings 子系统来存储 hawkBit 配置。（:github:`68806`）

MCUmgr
======

* 对 SHA-256 的支持（在使用校验和/哈希函数时）以前由 TinyCrypt 或 Mbed TLS 提供，现在改为由 PSA 或 Mbed TLS 提供。PSA 是今后推荐的 API，不过，如果尚未启用它（:kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_CLIENT`）并且你在代码大小上有严格限制，那么改用 Mbed TLS 也许可以节省 1.3 KB。

调制解调器
==========

* ``CONFIG_MODEM_CHAT_LOG_BUFFER`` Kconfig 选项已重命名为 :kconfig:option:`CONFIG_MODEM_CHAT_LOG_BUFFER_SIZE`。（:github:`70405`）

.. _zephyr_3.7_posix_api_migration:

POSIX API
=========

* :ref:`POSIX API Kconfig 弃用项 <zephyr_3.7_posix_api_deprecations>` 可能需要对 Kconfig 文件（``prj.conf`` 等）进行更改，具体如版本说明中所述。也可以通过所提供的迁移脚本采用更自动化的方式。只需运行以下命令：

  .. code-block:: bash

    $ python ${ZEPHYR_BASE}/scripts/utils/migrate_posix_kconfigs.py -r root_path

状态机框架
==========

* :c:macro:`SMF_CREATE_STATE` 宏现在始终接受 5 个参数。参数数量现在与 :kconfig:option:`CONFIG_SMF_ANCESTOR_SUPPORT` 和 :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION` 的取值无关。如果不使用额外的参数，则必须将它们设置为 ``NULL``。（:github:`71250`）
* 当转换源是 :c:func:`smf_run_state` 所调用状态的父状态时，SMF 现在遵循更接近 UML 的转换流程。将执行从转换源到转换目标状态的最小公共祖先（LCA，不含该祖先）为止的所有退出动作，以及从 LCA（不含该 LCA）向下到目标状态的所有进入动作。（:github:`71675`）
* 以前，使用设置为 NULL 的 ``new_state`` 调用 :c:func:`smf_set_state` 会执行从当前状态到最顶层父状态的所有退出动作，并期望最顶层的退出动作会终止状态机。现在不允许传入 ``NULL``。请改为在最顶层创建一个“终止”状态，并在其进入动作中调用 :c:func:`smf_set_terminate`。

UpdateHub
=========

* 用于执行完整性检查的 SHA-256 实现不再通过 :kconfig:option:`CONFIG_FLASH_AREA_CHECK_INTEGRITY_BACKEND` 选择。现在，所使用的实现（Mbed TLS 或 PSA）根据 :kconfig:option:`CONFIG_PSA_CRYPTO_CLIENT` 来选择。除非开发板使用 TF-M 构建或启用了 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_C`，否则仍默认使用 Mbed TLS（占用比之前更小）。（:github:`73511`）

架构
****

* 函数 :c:func:`arch_start_cpu` 已重命名为 :c:func:`arch_cpu_start`。（:github:`64987`）

* ``CONFIG_ARM64_ENABLE_FRAME_POINTER`` 已弃用。请改用 :kconfig:option:`CONFIG_FRAME_POINTER`。（:github:`72646`）

* x86

  * Kconfig 选项 ``CONFIG_DISABLE_SSBD`` 和 ``CONFIG_ENABLE_EXTENDED_IBRS`` 已弃用。请改用 :kconfig:option:`CONFIG_X86_DISABLE_SSBD` 和 :kconfig:option:`CONFIG_X86_ENABLE_EXTENDED_IBRS`。（:github:`69690`）

* POSIX 架构：

  * LLVM 模糊测试支持已重构。测试应用现在需要提供自己的 ``LLVMFuzzerTestOneInput()`` 钩子，而不再依赖开发板提供的钩子。示例请参见 ``samples/subsys/debug/fuzz/``。（:github:`71378`）
