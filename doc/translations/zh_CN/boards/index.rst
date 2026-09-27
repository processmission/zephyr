.. SPDX-FileCopyrightText: Copyright The Process Mission
.. SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
.. SPDX-License-Identifier: Apache-2.0

.. _boards:

支持的开发板与扩展板
####################

本页列出 Zephyr 当前支持的所有开发板和扩展板。

如果要为新的开发板添加 Zephyr 支持，请先阅读 :ref:`board_porting_guide`。
编写开发板支持文档时，请使用 :zephyr_file:`doc/templates/board.tmpl` 中的模板。

扩展板（Shield）是可以叠加在开发板上的硬件附件，用于增加功能。
有关扩展板移植的说明，请参阅 :ref:`shield_porting_guide`。

.. admonition:: 搜索提示
   :class: dropdown

   * 使用下方表单筛选支持的开发板与扩展板。留空的字段不参与筛选。
   * 名称、厂商和硬件能力筛选同时适用于开发板与扩展板，其余字段仅适用于开发板。
   * 开发板或扩展板必须满足不同字段中的 **所有** 条件。例如，同时选择厂商和架构时，
     只显示同时符合两项条件的开发板。同一字段中选择多个选项（例如两个架构）时，
     只要符合其中 **任意一个** 选项就会显示。
   * 按 RAM 或 Flash 容量筛选时，只要开发板的至少一个构建目标满足条件，就会显示该开发板。
   * 找不到完全相同的开发板时，可以从使用相同或相近 MCU 的开发板入手，
     以它为 :ref:`起点 <create-your-board-directory>` 添加自己的开发板支持。

.. note::

   下方硬件目录由源码元数据自动生成，型号、厂商名称及硬件参数保留原文。
   本站不运行逐开发板的构建探测。硬件能力和内存容量等详情请查看上游英文文档；
   下方开发板详情链接会打开相应的上游页面。

.. toctree::
   :maxdepth: 2
   :glob:
   :hidden:

   */index

.. zephyr:board-catalog::
