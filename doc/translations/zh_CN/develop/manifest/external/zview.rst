.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_zview:

ZView
#####

简介
****

`ZView <zview_>`_ 是 Zephyr RTOS 应用的运行时可视化工具，通过 SWD 调试探针实时提供全系统线程和堆统计。

它通过 APB 总线读取内核对象位置并检查内存，期间不会暂停 CPU，因此目标端开销接近零：无需 UART，无需 Shell，除标准线程内省选项外，也无需额外的 Kconfig 配置开销。

该工具完全在主机上运行，是一个 TUI 应用，可实时显示栈水位、各线程的 CPU 使用率及堆运行时统计。

在 Zephyr 中使用
****************

在工作区清单中声明模块，或通过子清单引入。例如，创建 ``zephyrproject/zephyr/submanifests/zview.yaml``，内容如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: zview
         url: https://github.com/wkhadgar/zview
         revision: main
         path: modules/tools/zview
         west-commands: scripts/west-commands.yml

应用必须以适当的 Kconfig 选项编译并运行，至少需要：

.. code-block:: cfg

   CONFIG_INIT_STACKS=y
   CONFIG_THREAD_MONITOR=y
   CONFIG_THREAD_STACK_INFO=y

然后更新工作区，并通过集成的 west 命令运行 ZView：

.. code-block:: sh

   west update
   west zview

完整选项列表和 CLI 用法见 `ZView repository <zview_>`_。

参考资料
********

- `ZView repository <zview_>`_

.. _zview: https://github.com/wkhadgar/zview
