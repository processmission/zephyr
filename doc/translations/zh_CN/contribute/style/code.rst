.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _general_code_style:

C 代码和通用风格指南
####################

任何新增或修改的代码都必须遵守编码风格，但不要求贡献者修正他们没有修改的既有代码的风格。

对于指南未给出明确指引、或允许多种有效写法的风格方面，贡献者应遵循代码库中既有代码的风格，其中“邻近”代码的优先级更高（先看该函数，再看同一文件，然后是子系统，依此类推）。

通常应遵循 `Linux kernel coding style`_，但有以下例外和说明：

* 制表符宽度为 8 个字符。
* 代码和变量使用 `snake case`_。
* 行长不超过 100 列。在文档中，URL 引用所在的行较长是允许的例外。
* 为每个 ``if``、``else``、``do``、``while``、``for`` 和 ``switch`` 语句体都加上花括号，即使是单行代码块也不例外。
* 如需对齐声明之后的注释，请使用空格而不是制表符。
* 使用 C89 风格的单行注释 ``/*  */``。不允许使用 C99 风格的单行注释 ``//``。
* 需要在文档中显示的 Doxygen 注释请使用 ``/**  */``。
* 避免使用二进制字面量（以 ``0b`` 开头的常量）。
* 避免在代码中使用非 ASCII 符号，除非这样做能显著提升清晰度；在任何情况下都应避免使用表情符号。
* 在代码注释中正确使用名词的大小写（例如使用 ``UART`` 而不是 ``uart``，使用 ``CMake`` 而不是 ``cmake``）。

.. _Linux kernel coding style:
   https://kernel.org/doc/html/latest/process/coding-style.html

.. _snake case:
   https://en.wikipedia.org/wiki/Snake_case
