.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-aliases:

West 别名
#########

West 允许在本地、全局或系统配置文件中添加命令别名。通过别名可以为常用或难以记忆的命令建立快捷方式，方便开发。

与 ``git`` 别名类似，别名命令会被替换为别名的完整文本，再解析为新的 shell 参数列表（内部使用 Python 函数 `shlex.split()`_ 拆分该值）。这样，参数就可以像直接传给原始命令一样传递。空格被视为参数分隔符；如果不希望参数被拆分，请正确转义。

.. _shlex.split(): https://docs.python.org/3/library/shlex.html#shlex.split

只需调用 ``west config`` 命令即可添加新别名：

.. code-block:: shell

   west config alias.mylist "list -f '{name} {revision}'"

使用 :samp:`west help {some_alias}` 查看别名。

允许递归别名，即别名命令可以包含其他别名，从而组合出更复杂但易于记忆的命令。

也可以覆盖现有命令，例如为其传入默认参数：

.. code-block:: shell

   west config alias.update "update -o=--depth=1 -n"

.. warning::

   覆盖或遮蔽其他命令或内置命令属于高级用法，可能产生难以理解的副作用，必须格外谨慎。

示例
----

在全局配置中添加 ``west run`` 和 ``west menuconfig`` 快捷命令，以使用对应的 CMake 目标调用 ``west build``：

.. code-block:: shell

   west config --global alias.run "build --pristine=never --target run"
   west config --global alias.menuconfig "build --pristine=never --target menuconfig"

为正在开发的示例创建带有附加选项的别名：

.. code-block:: shell

   west config alias.sample "build -b native_sim samples/hello_world -t run -- -DCONFIG_ASSERT=y"

覆盖 ``west update``，使其检查本地缓存：

.. code-block:: shell

   west config alias.update "update --path-cache $HOME/.cache/zephyrproject"

通过 west 运行 :ref:`Twister <twister_script>` 时自动排除 32 位原生模拟器目标。在没有 32 位主机 C 库的主机系统（例如 Linux/AArch64）上运行时，这尤其有用：

.. code-block:: shell

   west config alias.twister "twister --exclude-platform native_sim/native"
