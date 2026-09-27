.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

设备树
######

对于传感器，Devicetree 为每个传感器设备提供初始硬件配置。每个设备都必须在 Zephyr 中指定一个 Devicetree 绑定，理想情况下还应提供一组硬件配置选项，例如通道电源模式、数据速率、滤波器、抽取和量程。随后，可在开发板的 Devicetree 中使用这些选项，将传感器配置为其初始状态。

.. code-block:: dts

   #include <zephyr/dt-bindings/icm42688.h>

   &spi0 {
       /* SPI bus options here, not shown */

       accel_gyro0: icm42688p@0 {
           compatible = "invensense,icm42688", "invensense,icm4268x";
           reg = <0>;
           int-gpios = <&pioc 6 GPIO_ACTIVE_HIGH>; /* SoC specific pin to select for interrupt line */
           spi-max-frequency = <DT_FREQ_M(24)>; /* Maximum SPI bus frequency */
           accel-pwr-mode = <ICM42688_ACCEL_LN>; /* Low noise mode */
           accel-odr = <ICM42688_ACCEL_ODR_2000>; /* 2000 Hz sampling */
           accel-fs = <ICM42688_ACCEL_FS_16>; /* 16G scale */
           gyro-pwr-mode = <ICM42688_GYRO_LN>; /* Low noise mode */
           gyro-odr = <ICM42688_GYRO_ODR_2000>; /* 2000 Hz sampling */
           gyro-fs = <ICM42688_GYRO_FS_16>; /* 16G scale */
       };
    };
