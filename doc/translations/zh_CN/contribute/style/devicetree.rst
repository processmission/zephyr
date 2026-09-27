.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _devicetree_style:

Devicetree 风格指南
###################

  * 使用制表符缩进。
  * 制表符宽度为 8 个字符。
  * 遵循 Devicetree 规范的约定和规则。
  * 如果 `Devicetree 源文件（DTS）编码风格 <https://docs.kernel.org/devicetree/bindings/dts-coding-style.html>`_ 中的 Linux 内核规则给出了推荐做法，那么它在 Zephyr 中也是首选风格。
  * 如果有助于可读性，可以用一个空行（两个换行符）将相关的属性组分隔成“段落”。
  * 节点和属性名称使用短横线（ ``-`` ）作为单词分隔符。
  * 节点标签中使用下划线（ ``_`` ）作为单词分隔符。
  * 属性定义中等号（ ``=`` ）两侧各留一个空格。
  * 不要在减少缩进的 ``};`` 之前插入空行。
  * 在同一层级上插入一个空行来分隔节点。
  * 需要将较长的属性值拆分到多行时，第一个值应与左括号（ ``<`` 或 ``[`` ）放在同一行。右括号和分号（ ``>;`` 或 ``];`` ）应放在属性最后一个值之后的同一行。

示例：

.. literalinclude:: style-example.dts
  :language: devicetree
  :start-after: start-after-here
