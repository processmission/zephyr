.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-extensions:

扩展
####

West 支持“插件”：无需修改其源代码，就可以添加自己的命令。这些命令称为 **west 扩展命令**，简称“扩展”。扩展会显示在 ``west --help`` 输出中，归入定义它们的项目所对应的专门分区。本页介绍 west 扩展命令的基本信息，并提供编写自定义扩展的教程。

配合 Zephyr 使用 west 时，一些可用命令属于扩展，例如用于 :ref:`构建、烧录和调试 <west-build-flash-debug>` 的命令，以及 :ref:`此处介绍的命令 <west-zephyr-ext-cmds>`。因此，它们的帮助在 ``west --help`` 中显示如下：

.. code-block:: none

   extension commands from project manifest (path: zephyr):
     completion:           display shell completion scripts
     boards:               display information about supported boards
     shields:              display list of supported shields
     build:                compile a Zephyr application
     twister:              west twister wrapper
     sign:                 sign a Zephyr binary for bootloader chain-loading
     flash:                flash and run a binary on a board
     debug:                flash and interactively debug a Zephyr application
     debugserver:          connect to board and launch a debug server
     attach:               interactively debug a board
     ...

实现细节参见 :file:`zephyr/scripts/west-commands.yml` 和 :file:`zephyr/scripts/west_commands` 目录。

禁用扩展命令
************

要禁用扩展命令支持，将 ``commands.allow_extensions`` :ref:`配置 <west-config>` 选项设为 ``false``。若要全局设置，使每次运行 west 时都生效，请使用：

.. code-block:: console

   west config --global commands.allow_extensions false

之后如有需要，可以在特定 :term:`west workspace` 中重新启用：

.. code-block:: console

   west config --local commands.allow_extensions true

请注意，除非显式运行扩展命令，否则 west 不会导入包含它们的文件。详见下文。

添加 West 扩展
**************

添加自定义扩展需要三个步骤：

#. 编写实现命令的代码。
#. 将命令信息添加到 :file:`west-commands.yml` 文件中。
#. 确保 :term:`west manifest` 引用了该 :file:`west-commands.yml` 文件。

请注意，west 会忽略与内置命令同名的扩展命令。

步骤 1：实现命令
================

创建一个 Python 文件，存放命令实现（当前支持的 Python 版本，参见 `west PyPI page`_ 上的 west 项目元数据）。可以将文件放在 :term:`west manifest` 跟踪的任意项目中，也可以放在清单仓库本身。此文件必须包含 ``west.commands.WestCommand`` 的子类。运行扩展时，west 会实例化并使用该类。

以下基础框架可作为起点。它包含一个 ``WestCommand`` 子类，并实现了全部抽象方法。有关可用 west API 的更多信息，参见 :ref:`west-apis`。

.. code-block:: py

   '''my_west_extension.py

   Basic example of a west extension.'''

   from textwrap import dedent            # just for nicer code indentation

   from west.commands import WestCommand  # your extension must subclass this

   class MyCommand(WestCommand):

       def __init__(self):
           super().__init__(
               'my-command-name',  # gets stored as self.name
               '', # ignored self.help, will not be required by future west versions
               # self.description:
               description=dedent('''
               A multi-line description of my-command.

               You can split this up into multiple paragraphs and they'll get
               reflowed for you. You can also pass
               formatter_class=argparse.RawDescriptionHelpFormatter when calling
               parser_adder.add_parser() below if you want to keep your line
               endings.'''))

       def do_add_parser(self, parser_adder):
           # This is a bit of boilerplate, which allows you full control over the
           # type of argparse handling you want. The "parser_adder" argument is
           # the return value of an argparse.ArgumentParser.add_subparsers() call.
           parser = parser_adder.add_parser(self.name,
                                            description=self.description)

           # Add some example options using the standard argparse module API.
           parser.add_argument('-o', '--optional', help='an optional argument')
           parser.add_argument('required', help='a required argument')

           return parser           # gets stored as self.parser

       def do_run(self, args, unknown):
           # This gets called when the user runs the command, e.g.:
           #
           #   $ west my-command-name -o FOO BAR
           #   --optional is FOO
           #   required is BAR
           self.inf('--optional is', args.optional)
           self.inf('required is', args.required)

可以忽略 ``do_run()`` 的第二个参数（上例中的 ``unknown``），因为 ``WestCommand`` 默认会拒绝未知参数。如果希望接收未知参数列表，则在 ``super().__init__()`` 的参数中添加 ``accepts_unknown_args=True``。

步骤 2：添加或更新 :file:`west-commands.yml`
============================================

现在需要在项目中添加 :file:`west-commands.yml` 文件，向 west 描述此扩展。

对于上述类定义，假设其位于项目根目录的 :file:`my_west_extension.py` 中，配置示例如下：

.. code-block:: yaml

   west-commands:
     - file: my_west_extension.py
       commands:
         - name: my-command-name
           class: MyCommand
           help: one-line help for what my-command-name does

此 YAML 文件顶层是一个含有 ``west-commands`` 键的映射。该键的值是“命令描述符”序列。每个命令描述符给出实现 west 扩展的文件位置、扩展名称，以及可选的实现类名称（如果未指定，``class`` 默认与 ``name`` 相同）。

此文件中的一些信息与 Python 代码中的定义重复。这是因为用户运行 ``west my-command-name`` 之前，west 不会导入 :file:`my_west_extension.py`，原因如下：

- 用户可以对不可信来源的清单运行 ``west update``，然后使用其他 west 命令，而不会在过程中导入你的代码。由于导入 Python 模块等同于执行 shell 命令，这样可以让用户更放心。

- 这也是一个小优化，因为只有需要时才会导入你的代码。

因此，除非显式运行你的命令，否则 west 只会加载 :file:`west-commands.yml` 文件，获取基本信息，用于在 ``west --help`` 等输出中向用户展示该扩展。

如果有多个扩展，或希望将扩展拆分到多个文件，:file:`west-commands.yml` 会类似如下：

.. code-block:: yaml

   west-commands:
     - file: my_west_extension.py
       commands:
         - name: my-command-name
           class: MyCommand
           help: one-line help for what my-command-name does
     - file: another_file.py
       commands:
         - name: command2
           help: another cool west extension
         - name: a-third-command
           class: ThirdCommand
           help: a third command in the same file as command2

上例中：

- :file:`my_west_extension.py` 通过 ``MyCommand`` 类定义扩展 ``my-command-name``
- :file:`another_file.py` 定义两个扩展：

  #. ``command2``，对应类 ``command2``
  #. ``a-third-command``，对应类 ``ThirdCommand``

:file:`west-commands.yml` 内容的模式定义参见 `west repository`_ 中的 :file:`west-commands-schema.yml` 文件。

步骤 3：更新清单
================

最后，需要在 west 清单中指定刚编辑的 :file:`west-commands.yml` 的位置。如果扩展位于某个项目中，按如下方式添加：

.. code-block:: yaml

   manifest:
      # [... other contents ...]

      projects:
        - name: your-project
          west-commands: path/to/west-commands.yml
        # [... other projects ...]

其中 :file:`path/to/west-commands.yml` 相对于项目根目录。请注意，虽然建议使用 :file:`west-commands.yml` 这一名称，但它只是约定；如有需要，可以改用其他文件名。

如果扩展位于清单仓库中，则在清单的 ``self`` 部分执行相同操作，如下所示：

.. code-block:: yaml

   manifest:
     # [... other contents ...]

     self:
       west-commands: path/to/west-commands.yml

至此即可运行 ``west my-command-name``。命令名称、帮助信息及其代码所属的项目，也会出现在 ``west --help`` 输出中。如果将更新后的仓库分享给他人，他们也能使用此扩展。

.. _west PyPI page:
   https://pypi.org/project/west/

.. _west repository:
   https://github.com/zephyrproject-rtos/west/
