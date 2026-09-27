.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_libiio:

libiio
######

简介
****

`libiio`_ 是主要由 Analog Devices 开发的开源库，用于访问 Linux 工业输入／输出（IIO）设备，包括但不限于 ADC、DAC、加速度计、陀螺仪、IMU、压力与温度传感器，以及射频收发器。libiio 既可在目标设备本地使用，也可从 Linux、Windows 或 macOS 主机经 USB、以太网或串口远程与目标通信。

libiio 仓库包含一个 Zephyr 模块，可将 Zephyr 应用变成可远程访问的目标。IIO 设备和通道与 Zephyr 设备模型集成，内置驱动程序适配已有 Zephyr 传感器及 ADC/DAC 驱动。IIO 守护进程 **iiod** 的 Zephyr 移植通过网络套接字、UART 控制台、USB CDC-ACM 或原生 USB 厂商类，向远程主机开放这些设备。因此，现有 libiio Python 绑定、命令行工具（例如 ``iio_info``）及 `Scopy`_ 桌面应用无需修改，即可从 Linux、Windows 或 macOS 主机访问 Zephyr 目标。完整说明见 `Zephyr port documentation`_。

核心库采用 GNU 宽通用公共许可证（LGPL）2.1 版，示例和测试应用采用 GNU 通用公共许可证（GPL）2.0 版。上述 Zephyr 集成采用 MIT 许可证，其静态链接的核心文件也采用 MIT 许可证。

在 Zephyr 中使用
****************

要将 libiio 作为 Zephyr 模块引入，可以在 ``west.yml`` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/libiio.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     remotes:
       - name: analogdevicesinc
         url-base: https://github.com/analogdevicesinc

     projects:
       - name: libiio
         remote: analogdevicesinc
         revision: main
         path: modules/lib/libiio

参考资料
********

.. target-notes::

.. _libiio:
   https://github.com/analogdevicesinc/libiio

.. _Zephyr port documentation:
   https://analogdevicesinc.github.io/libiio/main/zephyr/

.. _Scopy:
   https://analogdevicesinc.github.io/scopy
