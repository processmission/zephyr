.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _python_style:

Python 风格指南
###############

Python 代码应按 `PEP 8`_ 规范进行格式化。Zephyr 使用 `ruff formatter`_ 来实现这一点。这个有明确主张的格式化工具追求一致性、通用性和可读性，并尽量减少 git diff。

要应用该格式化工具，请运行：

.. code-block:: shell

   ruff check --select I --fix <file> # Sort imports
   ruff format <file>

Ruff 配置
*********

在默认配置之上应用了一小组选项：

* 行长不超过 100 列。
* 单引号 ``'`` 和双引号这两种引号风格都允许。
* 行尾将转换为 ``\n``，这是 Unix 上的默认行尾。

排除的文件
**********

该格式化工具在 CI 中强制执行，但仅针对新增的 Python 文件，因为引入它时项目已有大量 Python 代码。:zephyr_file:`.ruff-excludes.toml` 文件有一个 ``[format]`` 节，其中列出了当前所有被排除的文件。鼓励贡献者在修改被排除的文件时，将其从列表中移除，并在单独的提交中格式化。

.. _PEP 8:
   https://peps.python.org/pep-0008/

.. _ruff formatter:
   https://docs.astral.sh/ruff/formatter/
