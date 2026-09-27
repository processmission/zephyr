.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_arduino_core_api:

Arduino Core API
################

简介
****

Arduino-Core-Zephyr 模块起源于 `Google Summer of Code 2022 project`_，旨在为 Zephyr RTOS 应用提供 Arduino 风格的 API。该模块作为抽象层，让熟悉 Arduino 编程的开发者无需学习全新的 API 和库，也能使用 Zephyr 的能力。

组件说明
========

该模块由两个相互配合的关键组件构成：

**1. ArduinoCore-API（通用 Arduino API 定义）**

`ArduinoCore-API <https://github.com/arduino/ArduinoCore-API>`_ 是 Arduino 官方硬件抽象层，定义通用 Arduino API，包含抽象 API 定义 **以及** 与硬件无关的功能实现。

主要特点：

* 同时包含 API 定义（头文件）和与硬件无关的实现
* 提供 ``String``、``Print``、``Stream``、``IPAddress`` 等类的完整实现
* 定义硬件相关类的接口，例如 ``HardwareSerial``、``HardwareSPI``
* 由所有现代 Arduino 平台共享，以保持一致性
* 实现细节见 `ArduinoCore-API README <https://github.com/arduino/ArduinoCore-API#arduinocore-api>`_
* 采用 GNU 宽通用公共许可证 2.1 版（LGPL 2.1）。

**2. ArduinoCore-Zephyr（Zephyr 专用实现）**

`Arduino-Core-Zephyr <https://github.com/zephyrproject-rtos/ArduinoCore-zephyr>`_ 模块提供 Arduino API 的 **Zephyr 专用实现**，通过 Zephyr 原生 API 和驱动程序实现硬件相关的 Arduino 函数。

主要特点：

* ``cores/arduino`` 目录包含 Zephyr 实现，例如 ``zephyrCommon.cpp``、``zephyrSerial.cpp``
* 提供带有引脚映射和设备树 overlay 的开发板专用变体
* 包含 Zephyr 构建系统集成文件（CMake、Kconfig、west.yml）
* 链接到 ArduinoCore-API，以复用通用实现
* 实现细节见 `project documentation <https://github.com/zephyrproject-rtos/ArduinoCore-zephyr/tree/main/documentation>`_
* 采用 Apache-2.0 许可证。

提供的功能
==========

两个组件共同提供以下功能：

* ``pinMode()``、``digitalWrite()``、``analogRead()`` 等标准 Arduino API 函数
* 支持 Arduino 风格的 ``setup()`` 和 ``loop()`` 函数
* 将 Arduino 引脚编号映射到 Zephyr GPIO 定义
* 支持常用 Arduino 通信协议（Serial、I2C、SPI）
* 兼容现有 Arduino 库
* 为 Zephyr 已支持的多种硬件平台提供开发板变体

该模块将 Arduino 风格的编程方式带入 Zephyr，使从 Arduino 转向 Zephyr 的开发者更容易上手，同时仍能受益于 Zephyr 的高级功能、可扩展性和广泛的硬件支持。

在 Zephyr 中使用
****************

向 Zephyr 项目添加 Arduino Core API
===================================

#. 要将 Arduino Core for Zephyr 作为 Zephyr 模块引入，可以在 west.yml 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/arduinocore.yaml``：

   .. code-block:: yaml

      # Arduino API repository
      - name: ArduinoCore-zephyr
        path: modules/lib/arduinocore-zephyr
        revision: main
        url: https://github.com/zephyrproject-rtos/ArduinoCore-zephyr

#. 运行以下命令更新项目：

   .. code-block:: bash

      west update

#. Linux 用户可以使用模块中的 ``install.sh`` 脚本自动链接 ArduinoCore-API。如果无法使用此脚本，请按以下步骤手动操作。

   .. note::

      如果 install.sh 执行成功，可跳过下一步。下一步适用于模块安装位置不同，或使用自定义路径搭建 Zephyr 环境的 Linux 用户。

#. 将 ArduinoCore-API 仓库的 API 文件夹链接到 arduinocore-zephyr 文件夹，完成核心组件设置：

   .. code-block:: bash

      west blobs fetch

   ``cores`` 文件夹位于 ``<zephyr-project-path>/modules/lib/arduinocore-zephyr/cores``。

在应用中使用 Arduino Core API
=============================

#. 在应用的 ``prj.conf`` 中启用 Arduino API 配置，方式与 `blinky_arduino sample`_ 示例类似。

#. 使用 Arduino 风格的代码创建应用：

   .. code-block:: cpp

      #include <Arduino.h>

      void setup() {
        pinMode(LED_BUILTIN, OUTPUT);
      }

      void loop() {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(1000);
        digitalWrite(LED_BUILTIN, LOW);
        delay(1000);
      }

#. 为目标开发板构建应用：

   .. code-block:: bash

      west build -b <board_name> path/to/your/app

添加自定义开发板支持
====================

受支持的开发板位于 arduinocore-zephyr 的 ``variants/`` 目录中。添加自定义开发板支持时：

#. 在 ``variants/`` 中创建以开发板命名的新文件夹
#. 添加与开发板同名的 overlay 文件和引脚映射头文件
#. 在 ``variant.h`` 中的 ``#ifdef`` 语句内添加新头文件

添加开发板变体的详细说明见 `board variants documentation`_。

使用外部 Arduino 库
===================

要在 Zephyr 项目中使用外部 Arduino 库：

#. 将库的源文件，例如 ``MyLibrary.h`` 和 ``MyLibrary.cpp``，加入项目的 ``src`` 文件夹
#. 更新应用的 ``CMakeLists.txt``，纳入这些文件：

   .. code-block:: cmake

      target_sources(app PRIVATE src/MyLibrary.cpp)

#. 在源代码中包含该库：

   .. code-block:: cpp

      #include "MyLibrary.h"

使用外部库的更多信息见 `Arduino libraries documentation`_。

参考资料
********

#. `Arduino-Core-Zephyr GitHub Repository`_
#. `ArduinoCore-API Repository`_
#. `Golioth Article: Zephyr + Arduino: a Google Summer of Code story`_

.. target-notes::

.. _Arduino Core API: https://github.com/zephyrproject-rtos/ArduinoCore-zephyr
.. _board variants documentation: https://github.com/zephyrproject-rtos/ArduinoCore-zephyr/blob/main/documentation/variants.md
.. _Arduino libraries documentation: https://github.com/zephyrproject-rtos/ArduinoCore-zephyr/blob/main/documentation/arduino_libs.md
.. _Arduino-Core-Zephyr GitHub Repository: https://github.com/zephyrproject-rtos/ArduinoCore-zephyr
.. _ArduinoCore-API Repository: https://github.com/arduino/ArduinoCore-API
.. _Google Summer of Code 2022 project: https://dhruvag2000.github.io/Blog-GSoC22/
.. _Golioth Article\: Zephyr + Arduino\: a Google Summer of Code story: https://blog.golioth.io/zephyr-arduino-a-google-summer-of-code-story/
.. _blinky_arduino sample: https://github.com/zephyrproject-rtos/ArduinoCore-zephyr/blob/next/samples/blinky_arduino/prj.conf
