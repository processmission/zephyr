.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-install:

安装 west
#########

West 使用 Python 3 编写，通过 `PyPI`_ 分发。使用 :file:`pip3` 安装或升级 west：

在 Linux 上::

  pip3 install --user -U west

在 Windows 和 macOS 上::

  pip3 install -U west

.. note::
   有关 ``--user`` 选项用法的更多说明，参见 :ref:`python-pip`。

之后可以运行 ``pip3 show -f west``，查看 west 可执行文件及相关文件的安装位置。

安装 west 后，即可使用它 :ref:`克隆 Zephyr 仓库 <clone-zephyr>`。

.. _west-struct:

结构
****

West 的代码通过 PyPI 上名为 ``west`` 的 Python 包分发。此发行包包含一个启动器可执行文件，也名为 ``west`` （Windows 上为 ``west.exe``）。

安装 west 时，:file:`pip3` 会将启动器放到用户文件系统中的某个位置（具体位置取决于操作系统，但应位于 ``PATH`` :ref:`环境变量 <env_vars>` 中）。此启动器是运行 ``west init``、``west update`` 等内置命令以及工作区中发现的扩展命令的命令行入口。

除命令行接口外，还可以直接使用 west 的 Python API。详见 :ref:`west-apis`。

.. _west-shell-completion:

启用 shell 补全
***************

West 目前支持以下 shell 的补全：

* bash
* zsh
* fish
* powershell（仅支持开发板限定符）

要启用 shell 补全，需要获取相应的补全脚本，并在当前 shell 中加载它。补全脚本的使用方式如下：

.. tabs::

  .. group-tab:: bash

    *一次性设置*：

    .. code-block:: bash

      source <(west completion bash)

    *永久设置*：

    .. code-block:: bash

      west completion bash > ~/west-completion.bash; printf '\n%s\n' "source ~/west-completion.bash" >> ~/.bashrc

  .. group-tab:: zsh

    *一次性设置*：

    .. code-block:: zsh

      source <(west completion zsh)

    *永久设置*：

    .. code-block:: zsh

      west completion zsh > "${fpath[1]}/_west"

  .. group-tab:: fish

    *一次性设置*：

    .. code-block:: fish

      west completion fish | source

    *永久设置*：

    .. code-block:: fish

      west completion fish > $HOME/.config/fish/completions/west.fish

  .. group-tab:: powershell

    *一次性设置*：

    .. code-block:: powershell

      west completion powershell | Out-String | Invoke-Expression

    *永久设置*：

    .. code-block:: powershell

      Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
      New-item -type file -force $PROFILE
      west completion powershell > $HOME/west-completion.ps1
      (Add-Content -Path $PROFILE -Value ". '{$HOME/west-completion.ps1}'")

.. _PyPI:
   https://pypi.org/project/west/
