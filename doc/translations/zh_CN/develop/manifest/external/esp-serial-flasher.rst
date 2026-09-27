.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_esp_serial_flasher:

ESP Serial Flasher
##################

简介
****

ESP Serial Flasher 是乐鑫开发和维护的可移植 C 库，允许运行嵌入式操作系统的主机微控制器对乐鑫 SoC（ESP8266、ESP32 系列）编程并与之交互。它通过统一 API，支持经 UART、USB CDC ACM、SPI 和 SDIO 等接口执行闪存操作、RAM 下载与执行，以及设备管理。

对于需要在没有 PC 或 Python 运行环境时为乐鑫目标设备编程或与其交互的 Zephyr 应用，该模块尤其有用。它提供类似 esptool 的功能，但针对资源受限的嵌入式系统优化，适用于生产烧录工具、引导加载程序和固件更新机制。

ESP Serial Flasher 支持多种乐鑫 SoC。支持的目标列表及更多信息见 `ESP Serial Flasher GitHub`_。

ESP Serial Flasher 采用 Apache License 2.0。

在 Zephyr 中使用
****************

要将 ESP Serial Flasher 作为 Zephyr 模块引入，可以在 ``west.yml`` 中将其添加为 West 项目，也可以添加包含以下内容的子清单，例如 ``zephyr/submanifests/esp-serial-flasher.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: esp-serial-flasher
         url: https://github.com/espressif/esp-serial-flasher
         revision: master
         path: modules/esp-serial-flasher # adjust path or leave blank for west workspace root directory

添加模块后，即可在应用代码中包含主头文件：

.. code-block:: c

   #include <esp_loader.h>

Zephyr 集成提供设备树绑定 ``espressif,esp-loader``，应用的设备树中必须至少定义一个实例。通过 ``zephyr,esp-loader`` chosen 属性选择活动实例。驱动程序负责 UART 通信、启动与复位引脚的 GPIO 控制，并提供闪存操作、设备连接和目标管理的高层 API。

可以将目标固件映像嵌入主机应用。将二进制文件放入 ``target-firmware/``，并在 ``target-firmware/images.csv`` 中描述闪存地址：每行一个映像，格式为 ``<filename>;<offset>``，偏移使用十六进制，且 **不带** ``0x`` 前缀，例如 ``app.bin;10000``。

包含 Zephyr 示例中的 ``bin_images_sections.cmake`` 后，应用 ``CMakeLists.txt`` 中的 ``create_resources()`` 会将这些文件转换为 C 数组。在 ``prj.conf`` 中设置 ``CONFIG_ESP_SERIAL_FLASHER=y`` 可启用驱动程序。``images.csv``、CMake 和设备树配置示例见 `ESP Serial Flasher GitHub`_ 仓库中的 ``examples/zephyr_example``。

需要通过 shell 交互时，以 ``CONFIG_ESP_SERIAL_FLASHER_SHELL=y`` 构建 ``examples/zephyr_example``。该示例提供 ``esf`` 命令组，可在 Zephyr shell 中连接 ESP 目标、读写闪存、检测闪存大小、擦除闪存，以及读写寄存器。

参考资料
********

- `ESP Serial Flasher Component Registry`_
- `Zephyr Modules Documentation`_

.. target-notes::

.. _ESP Serial Flasher GitHub:
   https://github.com/espressif/esp-serial-flasher

.. _ESP Serial Flasher Component Registry:
   https://components.espressif.com/components/espressif/esp-serial-flasher

.. _Zephyr Modules Documentation:
   https://docs.zephyrproject.org/latest/develop/modules.html
