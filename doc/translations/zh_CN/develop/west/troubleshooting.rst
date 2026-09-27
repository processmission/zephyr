.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-troubleshooting:

West 故障排查
#############

本页介绍 west 的常见问题及解决方法。

``west update`` 获取失败
************************

排查获取问题的一个好方法是以详细模式运行 ``west update``，如下所示：

.. code-block:: shell

   west -v update

输出包含 west 执行的 Git 命令及其输出。查找类似以下内容：

.. code-block:: none

   === updating your_project (path/to/your/project):
   west.manifest: your_project: checking if cloned
   [...other west.manifest logs...]
   --- your_project: fetching, need revision SOME_SHA
   west.manifest: running 'git fetch ... https://github.com/your-username/your_project ...' in /some/directory

上述最后一行中的 ``git fetch`` 命令必须能够成功执行。

一种方法是进入 ``/path/to/your/project``，复制粘贴并运行完整的 ``git fetch`` 命令，再根据凭据存储辅助程序的文档继续排查。

如果处于公司防火墙之后，可能存在代理或其他问题，``curl -v FETCH_URL`` （HTTPS URL）或 ``ssh -v FETCH_URL`` （SSH URL）可能有助于排查。

如果直接运行 ``git fetch`` 命令时可以成功且无需输入密码，就可以在同一 shell 中运行 ``west update`` 而无需输入密码。

“'west' 不是内部或外部命令，也不是可运行的程序或批处理文件。”
*************************************************************

在 Windows 上，这意味着尚未安装 west，或者 :envvar:`PATH` 环境变量不包含 pip 安装 :file:`west.exe` 的目录。

首先确保已安装 west，参见 :ref:`west-install`。然后尝试在新的 ``cmd.exe`` 窗口中运行 ``west``。如果仍然无效，请继续阅读。

需要找到包含 :file:`west.exe` 的目录，并将其添加到 :envvar:`PATH` 中。（安装 Python 和 pip 时通常已经完成此 :envvar:`PATH` 设置，因此一般不需要执行以下步骤。）

在 ``cmd.exe`` 中运行此命令::

  pip3 show west

然后：

#. 在输出中查找类似 ``Location: C:\foo\python\python38\lib\site-packages`` 的行。计算机上的实际位置会有所不同。
#. 在 ``scripts`` 目录 ``C:\foo\python\python38\scripts`` 中查找名为 ``west.exe`` 的文件。

   .. important::

      注意，``pip3 show`` 输出中的 ``lib\site-packages`` 已替换为 ``scripts``！
#. 如果在 ``scripts`` 目录中找到 ``west.exe``，使用类似以下命令将 ``scripts`` 的完整路径加入 :envvar:`PATH`::

     setx PATH "%PATH%;C:\foo\python\python38\scripts"

   **不要直接复制粘贴此命令**。你的系统上 ``scripts`` 目录的位置会有所不同。
#. 关闭 ``cmd.exe`` 窗口并打开新窗口。现在应该可以运行 ``west``。

“invalid choice: 'build'”（或 'flash' 等）
******************************************

如果尝试运行 Zephyr 扩展命令（如 :ref:`west flash <west-flashing>`、:ref:`west build <west-building>` 等）时，看到如下意外错误：

.. code-block:: none

   $ west build [...]
   west: error: argument <command>: invalid choice: 'build' (choose from 'init', [...])

   $ west flash [...]
   west: error: argument <command>: invalid choice: 'flash' (choose from 'init', [...])

最可能的原因是在 :ref:`west 工作区 <west-workspace>` 之外运行了命令。West 需要知道工作区的位置才能找到 :ref:`west-extensions`。

有两种解决方法：

#. 从工作区内部运行命令（例如 :ref:`入门 <getting_started>` 时创建的 :file:`zephyrproject` 目录）。

   例如，在工作区内部创建构建目录，或者在工作区内部运行 ``west flash --build-dir YOUR_BUILD_DIR``。

#. 设置 :envvar:`ZEPHYR_BASE` :ref:`环境变量 <env_vars>`，然后重新运行 west 扩展命令。如果已设置，west 会使用 :envvar:`ZEPHYR_BASE` 查找工作区。

如果不确定某个命令是内置命令还是扩展命令，请在工作区内部运行 ``west help``。输出会单独列出扩展命令，对于 Zephyr 主线版本，内容如下：

.. code-block:: none

   $ west help

   built-in commands for managing git repositories:
     init:                 create a west workspace
     [...]

   other built-in commands:
     help:                 get help for west or a command
     [...]

   extension commands from project manifest (path: zephyr):
     build:                compile a Zephyr application
     flash:                flash and run a binary on a board
     [...]

“invalid choice: 'post-init'”
*****************************

如果运行 ``west init`` 时看到此错误：

.. code-block:: none

   west: error: argument <command>: invalid choice: 'post-init'
   (choose from 'init', 'update', 'list', 'manifest', 'diff',
   'status', 'forall', 'config', 'selfupdate', 'help')

说明已安装的 west 版本较旧，而当前工作区需要更新的版本。

最简单的解决办法是升级 west，并按以下步骤重试：

#. 按 :ref:`west-install` 所示，为 ``pip3 install`` 添加 ``-U`` 选项，安装最新版本的 west。

#. 备份 :file:`zephyrproject/.west/config` 中希望保留的内容。（如果未设置任何配置选项，可安全跳过此步骤。）

#. 彻底删除 :file:`zephyrproject/.west` 目录（否则会出现下文讨论的“already in a workspace”错误）。

#. 重新运行 ``west init``。
