.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_zscilib:

Zephyr 科学计算库（zscilib）
############################

简介
****

Zephyr 科学计算库（`zscilib`_）旨在为资源受限的嵌入式硬件设备提供科学计算、数据分析和数据处理函数。

该库完全使用 C 编写。虽然主要面向 Zephyr 项目开发，但力求尽可能可移植。仓库包含独立参考项目，用于在非 Zephyr 项目中使用该库。

在 Zephyr 中使用
****************

要将 zscilib 作为 Zephyr 模块引入，可以在 ``west.yaml`` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/zscilib.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: zscilib-
         url: https://github.com/zephyrproject-rtos/zscilib
         revision: master
         path: modules/lib/zscilib # adjust the path as needed

详细说明和 API 文档见 `zscilib documentation`_ 及随附的 `zscilib examples`_。


运行示例应用
============

要使用 QEMU 运行某个示例应用，执行以下命令：

.. code-block:: console

    $ west build -p -b qemu_cortex_a53 \
        samples/matrix/mult -t run
    ...
    *** Booting Zephyr OS build zephyr-v2.6.0-536-g89212a7fbf5f  ***
    zscilib matrix mult demo


    mtx multiply output (4x3 * 3x4 = 4x4):

    14.000000 17.000000 20.000000 23.000000
    35.000000 44.000000 53.000000 62.000000
    56.000000 71.000000 86.000000 101.000000
    7.000000 9.000000 11.000000 13.000000

按 CTRL+A，再按 x，即可退出 QEMU。

运行单元测试
============

要运行该库的单元测试，执行以下命令：

.. code-block:: console

    $ west twister --inline-logs -p mps2/an521/cpu0 -T tests
    See the tests folder for further details.



参考资料
********

.. _zscilib:
    https://github.com/zephyrproject-rtos/zscilib

.. _zscilib documentation:
    https://zephyrproject-rtos.github.io/zscilib/

.. _zscilib examples:
    https://github.com/zephyrproject-rtos/zscilib/tree/master/samples
