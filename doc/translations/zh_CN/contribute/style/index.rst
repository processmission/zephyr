.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _coding_style:


编码风格指南
############

.. toctree::
   :maxdepth: 1

   naming.rst
   code.rst
   doxygen.rst
   cmake.rst
   devicetree.rst
   kconfig.rst
   python.rst


风格工具
********

Checkpatch
==========

使用 Linux 内核中采用 GPL 许可的工具 ``checkpatch`` 检查编码风格的合规性。

.. note::
   checkpatch 目前无法在 Windows 上运行。

Checkpatch 位于 scripts 目录中。要在提交代码时调用它，请将 *$ZEPHYR_BASE/.git/hooks/pre-commit* 文件设为可执行，并编辑其内容为：

.. code-block:: bash

    #!/bin/sh
    set -e exec
    exec git diff --cached | ${ZEPHYR_BASE}/scripts/checkpatch.pl -

如果不想在每次提交时都运行 checkpatch，也可以只在向 Zephyr 仓库推送之前运行。为此，请将 *$ZEPHYR_BASE/.git/hooks/pre-push* 文件设为可执行，并编辑其内容为：

.. code-block:: bash

    #!/bin/sh
    remote="$1"
    url="$2"

    z40=0000000000000000000000000000000000000000

    echo "Run push hook"

    while read local_ref local_sha remote_ref remote_sha
    do
        args="$remote $url $local_ref $local_sha $remote_ref $remote_sha"
        exec ${ZEPHYR_BASE}/scripts/series-push-hook.sh $args
    done

    exit 0

如果希望忽略 checkpatch 的判定，在报告了问题的情况下仍然推送分支，可以在 git push 命令中加上 --no-verify 选项。

运行 ``checkpatch`` 的另一种方式是使用 :ref:`check_compliance_py` 脚本，它还会执行额外的风格和合规性检查。

clang-format
============

`clang-format 工具 <https://clang.llvm.org/docs/ClangFormat.html>`_ 配合仓库中提供的 ``.clang-format`` 配置文件，有助于快速将大量新增源代码重新格式化为符合我们的 `编码风格指南`_ 标准。``clang-format`` 已很好地集成到大多数编辑器中，但你也可以像下面这样手动运行它：

.. code-block:: bash

   clang-format -i my_source_file.c

``clang-format`` 是 LLVM 的一部分，可以从项目的 `发布页面 <https://github.com/llvm/llvm-project/releases>`_ 下载。请注意，如果你使用 Linux，``clang-format`` 很可能已作为软件包包含在你的发行版仓库中。

当 `编码风格指南`_ 指南与代码格式化工具生成的格式存在差异时，以 `编码风格指南`_ 指南为准。如果格式化工具与指南之间存在歧义，维护者可以决定应采用哪种风格。

dts-linter
==========

`dts-linter <https://www.npmjs.com/package/dts-linter>`_ 有助于快速将大量 devicetree 文件重新格式化为符合我们的 `编码风格指南`_ 标准。你也可以像下面这样手动运行它：

针对单个文件

.. code-block:: bash

   npx --prefix ./scripts/ci dts-linter --format --file board.dts --file board_pinctrl.dtsi --patchFile diff.patch
   git apply diff.patch

可以省略 ``--file``，这样会格式化命令所在目录下的所有文件。也可以通过 ``--cwd`` 设置该工具查找文件的基础目录。该选项还用于使补丁文件中的路径变为相对路径。

你也可以就地修复，命令如下

.. code-block:: bash

   npx --prefix ./scripts/ci dts-linter --formatFixAll


编辑器集成
~~~~~~~~~~

* VS Code：从 `VS Code Marketplace <https://marketplace.visualstudio.com/items?itemName=KyleMicallefBonnici.dts-lsp>`_ 或 `Open VSIX <https://open-vsx.org/extension/KyleMicallefBonnici/dts-lsp>`_ 安装扩展
* 其他支持 LSP 客户端的编辑器：使用 devicetree-language-server `devicetree-language-server <https://www.npmjs.com/package/devicetree-language-server>`_

请务必遵循 `Devicetree 风格指南 <https://docs.zephyrproject.org/latest/contribute/style/devicetree.html>`_ 的要求，以便正确配置编辑器。
