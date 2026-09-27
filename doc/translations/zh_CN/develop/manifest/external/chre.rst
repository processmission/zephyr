.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_chre:

Context Hub 运行时环境（CHRE）
##############################

简介
****

`Context Hub Runtime Environment`_ （CHRE）是 Android 的常驻应用平台，这类应用称为 *nanoapp*，运行在 Android 应用处理器旁的低功耗处理器上。Nanoapp 基于跨平台标准化的 CHRE API 编写，由 CHRE 框架承载；该框架是此 API 的 AOSP 参考实现。

`zephyrproject-rtos/chre`_ 仓库派生自 AOSP 框架，在 ``platform/zephyr`` 中提供 Zephyr 移植。该移植在专用线程中运行 CHRE 事件循环，并提供框架所需的平台原语，包括内存、定时器、系统时间、日志及主机连接。目前尚未为 Zephyr 实现音频、GNSS、传感器、WiFi 和 WWAN 的平台抽象层（PAL）。

CHRE 采用 Apache-2.0 许可证。

在 Zephyr 中使用
****************

要将 CHRE 作为 Zephyr :ref:`模块 <modules>` 引入，可以在 ``west.yaml`` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/chre.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: chre
         url: https://github.com/zephyrproject-rtos/chre
         revision: zephyr
         path: modules/lib/chre # adjust the path as needed

通过 ``CONFIG_CHRE=y`` 启用框架。CHRE 使用 C++ 编写，并选择 :kconfig:option:`CONFIG_REQUIRES_FULL_LIBCPP`，因此工具链必须提供完整的 C++ 标准库。模块 ``platform/zephyr/Kconfig`` 中其余 ``CONFIG_CHRE_*`` 选项用于设置事件循环线程和内存池的大小，并启用各个 PAL 框架。

模块在 ``zephyr/sample`` 中提供示例应用，依次启动事件循环、加载 nanoapp、向其递送事件，最后关闭。在 :zephyr:board:`native_sim` 上构建和运行：

.. code-block:: console

   west build -b native_sim modules/lib/chre/zephyr/sample -t run

参考资料
********

.. target-notes::

.. _Context Hub Runtime Environment:
   https://source.android.com/docs/core/interaction/contexthub

.. _zephyrproject-rtos/chre:
   https://github.com/zephyrproject-rtos/chre
