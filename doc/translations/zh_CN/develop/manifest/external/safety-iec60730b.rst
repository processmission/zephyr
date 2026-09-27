.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_safety_iec60730b:

IEC 60730 B 类安全测试子系统
############################

简介
****

`safety_iec60730b`_ 是一个 Zephyr :ref:`模块 <modules>`，提供可由 Zephyr 应用运行 IEC 60730 B 类安全自检的测试子系统。

`IEC 60730-1`_ 是一项国际标准，规定家用电器及类似设备所用自动电气控制装置的安全要求。附录 H 的 B 类描述了控制装置必须实现的软件故障／错误检测措施，用于检测否则可能导致危险功能失效的随机硬件故障。

该子系统通过统一、与厂商无关的 API 暴露这些“持续执行”的自检，通过 Kconfig 和设备驱动模型与 Zephyr 集成，并将实际测试交给可选后端执行。NXP SoC 的默认后端是 `NXP IEC 60730 Class B Safety Library`_。

提供以下 B 类测试例程，每项都可通过 Kconfig 单独选择：

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 测试
     - Kconfig 符号
     - 检测的故障
   * - CPU 寄存器
     - ``CONFIG_IEC60730B_TEST_CPU``
     - 核心寄存器的固定值故障
   * - FPU 寄存器
     - ``CONFIG_IEC60730B_TEST_FPU``
     - 浮点寄存器的固定值故障
   * - 程序计数器
     - ``CONFIG_IEC60730B_TEST_PC``
     - 程序计数器损坏、无效执行流程
   * - RAM
     - ``CONFIG_IEC60730B_TEST_RAM``
     - 使用 March C / March X 算法检测 RAM 存储单元故障
   * - 闪存／ROM
     - ``CONFIG_IEC60730B_TEST_FLASH``
     - 使用 CRC16 / CRC32 检测不变存储内容的损坏
   * - 栈
     - ``CONFIG_IEC60730B_TEST_STACK``
     - 栈上溢和下溢
   * - 时钟
     - ``CONFIG_IEC60730B_TEST_CLOCK``
     - 相对于独立计数器测量系统时钟漂移
   * - 模拟 I/O
     - ``CONFIG_IEC60730B_TEST_AIO``
     - 利用已知内部参考值验证 ADC 信号通路故障
   * - 数字 I/O
     - ``CONFIG_IEC60730B_TEST_DIO``
     - GPIO 固定值故障和短路
   * - 看门狗
     - ``CONFIG_IEC60730B_TEST_WDOG``
     - 看门狗超时及复位产生

API 后面的测试例程由以下三个可互换的硬件抽象层（HAL）后端之一提供：

* **NXP HAL** （``CONFIG_IEC60730B_HAL_NXP``）调用同一仓库随附、预先获得认证的 NXP IEC 60730 B 类裸机安全库。NXP SoC 默认选择此后端，其底层实现已通过认证。
* **Zephyr HAL** （``CONFIG_IEC60730B_HAL_ZEPHYR``）基于标准 Zephyr 驱动 API 实现相同测试，使子系统可用于 Zephyr 支持的任意平台。非 NXP SoC 默认选择此后端。
* **无 HAL** （``CONFIG_IEC60730B_HAL_NONE``）仅构建弱符号桩，因此所有测试都返回 ``IEC60730B_TEST_NOT_SUPPORTED``。可将其作为自定义后端的起点：实现公共头文件中声明的函数，即可在链接时覆盖弱符号实现。

.. warning::

   Zephyr HAL 仍为实验性功能，不使用任何经厂商认证的库，其代码也均未通过 IEC 60730 B 类认证。在将其用于任何安全关键产品之前，用户必须自行负责针对具体应用和目标平台，对全部代码进行评估、验证和认证。

测试子系统、HAL 后端、示例及模块元数据，即 ``zephyr/`` 下的全部内容，采用 Apache-2.0 许可证。作为后端的 NXP 安全库，即 ``source/`` 下的全部内容，采用 *LA_OPT_Online Code Hosting NXP_Software_License* 分发；完整文本见仓库中的 ``IEC60730-LICENSE.txt``。

在 Zephyr 中使用
****************

向现有工作区添加模块
====================

在 ``west.yml`` 清单中将模块添加为 West 项目，或添加包含以下内容的子清单，例如 :file:`zephyr/submanifests/iec60730b.yaml`：

.. code-block:: yaml

   manifest:
     projects:
       - name: safety_iec60730b
         url: https://github.com/nxp-mcuxpresso/mcux-safety-iec60730b
         revision: main_github
         path: modules/safety/iec60730b # adjust the path as needed

然后获取模块：

.. code-block:: console

   west update safety_iec60730b

创建独立工作区
==============

仓库还附带自己的清单，仅引入 Zephyr 本身及模块所需的 HAL：

.. code-block:: console

   west init -m https://github.com/nxp-mcuxpresso/mcux-safety-iec60730b <workspace>
   cd <workspace>
   west update

配置
====

在应用的 :file:`prj.conf` 中启用测试子系统：

.. code-block:: cfg

   CONFIG_IEC60730B=y

默认启用所有测试例程。可禁用不需要的测试，并在必要时覆盖自动选择的 HAL。

应用接口
========

公共 API 声明于 ``iec60730b_test.h``，模块会将其加入应用头文件搜索路径。包含该文件即可直接调用测试函数。测试通常分为应用启动前执行一次的启动测试，以及由专用安全线程或中断周期执行的运行时测试。每个函数成功时返回 ``0``，检测到故障时返回负错误码，测试被禁用或目标不支持时返回 ``IEC60730B_TEST_NOT_SUPPORTED``。

示例应用
========

``zephyr/samples/safety/`` 下的 ``safety`` 示例是参考集成。它运行完整的启动和运行时测试，在控制台报告每项结果，为 Zephyr 任务看门狗通道喂狗，并在安全线程存活期间闪烁 LED。

从工作区根目录为某个受支持开发板构建并烧录：

.. code-block:: console

   west build -p -b frdm_mcxa266 modules/safety/iec60730b/zephyr/samples/safety
   west flash

示例在看门狗测试中会故意让看门狗超时，因此开发板会复位一次，启动横幅和启动测试结果会出现两次。

参考资料
********

.. target-notes::

.. _safety_iec60730b:
   https://github.com/nxp-mcuxpresso/mcux-safety-iec60730b

.. _IEC 60730-1:
   https://webstore.iec.ch/publication/66089

.. _NXP IEC 60730 Class B Safety Library:
   https://www.nxp.com/applications/technologies/functional-safety/iec-60730-safety-standard-for-household-appliances:APIEC60730
