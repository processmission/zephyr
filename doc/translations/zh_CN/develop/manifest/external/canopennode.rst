.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_canopennode:

CANopenNode 协议栈
##################

简介
****

`CANopenNode`_ 是自由开源的 CANopen 协议栈。将其与 Zephyr 集成的适配代码位于独立的 `CANopenNodeZephyr`_ 仓库中，该仓库通过 Git 子模块引入 CANopenNode。

CANopenNode 和 CANopenNodeZephyr 均采用 Apache-2.0 许可证。

在 Zephyr 中使用
****************

要将 CANopenNodeZephyr 作为 Zephyr :ref:`模块 <modules>` 引入，可以在 ``west.yaml`` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/canopennodezephyr.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: canopennodezephyr
         url: https://github.com/zephyrproject-rtos/CANopenNodeZephyr.git
         revision: main
         submodules:
           - path: CANopenNode
         path: custom/canopennodezephyr # adjust the path as needed

.. _CANopenNode:
   https://github.com/CANopenNode/CANopenNode

.. _CANopenNodeZephyr:
   https://github.com/zephyrproject-rtos/CANopenNodeZephyr
