.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _shell_api:

Shell
#####

.. contents::
    :local:
    :depth: 2

概述
****

本模块允许您创建并处理带有用户自定义命令集的 shell。在需要超出简单按钮或 LED 用户交互的示例中，可以使用本模块。本模块是一个类 Unix shell，具有以下特性：

* 支持多个实例。
* 与 :ref:`日志 API <logging_api>` 的高级协作。
* 支持静态和动态命令。
* 支持字典命令。
* 使用 :kbd:`Tab` 键进行智能命令补全。
* 内置命令：:command:`aliases`、:command:`clear`、:command:`shell`、:command:`colors`、:command:`echo`、:command:`history` 和 :command:`resize`。
* 使用 :kbd:`↑` :kbd:`↓` 或元键查看最近执行的命令。
* 使用 :kbd:`←`、:kbd:`→`、:kbd:`Backspace`、:kbd:`Delete`、:kbd:`End`、:kbd:`Home`、:kbd:`Insert` 编辑文本。
* 支持 ANSI 转义码：``VT100`` 和 ``ESC[n~``，用于光标控制和彩色打印。
* 支持编辑多行命令。
* 内置处理程序，用于显示命令的帮助信息。
* 支持通配符：``*`` 和 ``?``。
* 支持元键。
* 支持 getopt 和 getopt_long。
* 通过 Kconfig 配置优化内存占用。

.. note::
        其中一些特性会显著影响 RAM 和 flash 占用，但在不需要时可以禁用许多特性。若希望默认采用优先降低 RAM 和 flash 需求而非增加特性的选项，您应启用 :kconfig:option:`CONFIG_SHELL_MINIMAL`，并只选择性地启用您需要的特性。

.. _backends:

后端
****

本模块可以连接到任何传输层以进行命令输入和输出。目前实现了以下传输层：

* MQTT
* Segger RTT
* SMP
* Telnet
* UART
* USB
* Bluetooth LE (NUS)
* RPMSG
* DUMMY - 不是物理传输层。

Telnet
======

启用 :kconfig:option:`CONFIG_SHELL_BACKEND_TELNET` 将允许用户将 telnet 用作 shell 后端。可以使用 PuTTY 或任何 ``telnet`` 客户端连接到它。例如：

.. code-block:: none

  telnet <ip address> <port>

默认情况下，telnet 客户端不会处理 telnet 命令和配置。尽管可以通过 :kconfig:option:`CONFIG_SHELL_TELNET_SUPPORT_COMMAND` 启用命令支持。这将使 telnet 客户端能够访问一组非常有限的受支持命令，但如果需要仍可开启。它支持的命令选项之一是 ``ECHO`` 选项。这将允许客户端处于字符模式（一次一个字符），在这方面与 UART 后端类似。这会使客户端在键入字符后立即发送该字符，从而显著增加网络流量。付出这一代价后，它将启用 shell 的行编辑、`Tab 补全 <tab-feature_>`_ 和 `历史记录 <history-feature_>`_ 功能。

USB CDC ACM
===========

要配置 Shell USB CDC ACM 后端，只需将片段 ``cdc-acm-console`` 添加到您的构建中：

.. code-block:: console

   west build -S cdc-acm-console [...]

配置设置的详细信息记录在以下文件中：

- :zephyr_file:`snippets/cdc-acm-console/cdc-acm-console.conf`.
- :zephyr_file:`snippets/cdc-acm-console/cdc-acm-console.overlay`.

Bluetooth LE (NUS)
==================

要配置 Bluetooth LE (NUS) 后端，只需将片段 ``nus-console`` 添加到您的构建中：

.. code-block:: console

   west build -S nus-console [...]

配置设置的详细信息记录在以下文件中：

- :zephyr_file:`snippets/nus-console/nus-console.conf`.
- :zephyr_file:`snippets/nus-console/nus-console.overlay`.

Segger RTT
==========

要配置 Segger RTT 后端，请将以下配置添加到您的构建中：

- :kconfig:option:`CONFIG_USE_SEGGER_RTT`
- :kconfig:option:`CONFIG_SHELL_BACKEND_RTT`
- :kconfig:option:`CONFIG_SHELL_BACKEND_SERIAL`

其他配置设置的详细信息记录在：:zephyr_file:`samples/subsys/shell/shell_module/prj_minimal_rtt.conf`。

.. _shell_rtt_west:

使用 west
---------

使用以下命令连接并配置 RTT：

.. code-block:: console

   $ west rtt

.. note::

   如果默认 runner 不支持 RTT，请查看开发板文档页面，了解其他支持 RTT 的 runner。然后您可以使用 ``--runner`` 选项指定不同的 runner。

  .. code-block:: console

     $ west rtt --runner <runner>

.. _shell_rtt_putty:

使用 PuTTY
----------

使用以下过程：

* 打开调试会话并继续运行应用。

  .. code-block:: none

     west attach

* 打开 ``PuTTY``。使用 telnet 端口 19021 和特定的 Terminal 配置。将 ``Local echo`` 设为 ``Force off``，将 ``Local line editing`` 设为 ``Force off`` （见下图）。


.. image:: images/putty_rtt.png
      :align: center
      :alt: RTT PuTTY 终端配置。

* 现在您应该已经与 RTT 建立了网络连接，可以向 shell 输入内容。

通过 TCP 连接 Segger RTT（以 macOS 为例）
-----------------------------------------

在 macOS 上 JLinkRTTClient 不允许您输入。请改用以下过程：

* 打开第一个 Terminal 窗口并输入：

  .. code-block:: none

     JLinkRTTLogger -Device NRF52840_XXAA -RTTChannel 1 -if SWD -Speed 4000 ~/rtt.log

  （如有需要请更改设备）

* 打开第二个 Terminal 窗口并输入：

  .. code-block:: none

     nc localhost 19021

* 现在您应该已经与 RTT 建立了网络连接，可以向 shell 输入内容。不过，与 `PuTTY <shell_rtt_putty_>`_ 不同，``Tab`` 补全等某些功能无法使用。


命令
****

Shell 命令以树状结构组织，并分为以下类型：

* 根命令（第 0 级）：收集并按字母顺序排列在专用的内存段中。
* 静态子命令（级别 > 0）：数量和语法必须在编译时已知。在软件模块中创建。
* 动态子命令（级别 > 0）：数量和语法无需在编译时已知。在软件模块中创建。


常用命令组
==========

以下列表列出了一组有用的命令组及其启用方法：

GPIO
----

- :kconfig:option:`CONFIG_GPIO`
- :kconfig:option:`CONFIG_GPIO_SHELL`

I2C
---

- :kconfig:option:`CONFIG_I2C`
- :kconfig:option:`CONFIG_I2C_SHELL`

传感器
------

- :kconfig:option:`CONFIG_SENSOR`
- :kconfig:option:`CONFIG_SENSOR_SHELL`

Flash
-----

- :kconfig:option:`CONFIG_FLASH`
- :kconfig:option:`CONFIG_FLASH_SHELL`

文件系统
--------

- :kconfig:option:`CONFIG_FILE_SYSTEM`
- :kconfig:option:`CONFIG_FILE_SYSTEM_SHELL`

ADC
---

- :kconfig:option:`CONFIG_ADC`
- :kconfig:option:`CONFIG_ADC_SHELL`
- :kconfig:option:`CONFIG_ADC_EMUL_SHELL` （需要 :kconfig:option:`CONFIG_ADC_EMUL`）

创建命令
========

使用以下宏添加 shell 命令：

* :c:macro:`SHELL_CMD_REGISTER` - 创建根命令。所有根命令的名称必须不同。
* :c:macro:`SHELL_COND_CMD_REGISTER` - 有条件地（如果设置了编译时标志）创建根命令。所有根命令的名称必须不同。
* :c:macro:`SHELL_CMD_ARG_REGISTER` - 创建带参数的根命令。所有根命令的名称必须不同。
* :c:macro:`SHELL_COND_CMD_ARG_REGISTER` - 有条件地（如果设置了编译时标志）创建带参数的根命令。所有根命令的名称必须不同。
* :c:macro:`SHELL_CMD` - 初始化命令。
* :c:macro:`SHELL_COND_CMD` - 如果设置了编译时标志，则初始化命令。
* :c:macro:`SHELL_EXPR_CMD` - 如果编译时表达式非零，则初始化命令。
* :c:macro:`SHELL_CMD_ARG` - 初始化带参数的命令。
* :c:macro:`SHELL_COND_CMD_ARG` - 如果设置了编译时标志，则初始化带参数的命令。
* :c:macro:`SHELL_EXPR_CMD_ARG` - 如果编译时表达式非零，则初始化带参数的命令。
* :c:macro:`SHELL_STATIC_SUBCMD_SET_CREATE` - 创建静态子命令数组。
* :c:macro:`SHELL_SUBCMD_DICT_SET_CREATE` - 创建字典子命令数组。
* :c:macro:`SHELL_DYNAMIC_CMD_CREATE` - 创建动态子命令数组。

可以在系统中任何包含 :zephyr_file:`include/zephyr/shell/shell.h` 的文件中创建命令。所有创建的命令对所有 shell 实例都可用。

静态命令
--------

演示如何创建带静态子命令的根命令的示例代码。

.. image:: images/static_cmd.PNG
      :align: center
      :alt: 带静态命令的命令树。

.. code-block:: c

        /* Creating subcommands (level 1 command) array for command "demo". */
        SHELL_STATIC_SUBCMD_SET_CREATE(sub_demo,
                SHELL_CMD(params, NULL, "Print params command.",
                                                       cmd_demo_params),
                SHELL_CMD(ping,   NULL, "Ping command.", cmd_demo_ping),
                SHELL_SUBCMD_SET_END
        );
        /* Creating root (level 0) command "demo" */
        SHELL_CMD_REGISTER(demo, &sub_demo, "Demo commands", NULL);

示例实现可在以下位置找到：:zephyr_file:`samples/subsys/shell/shell_module/src/main.c`。

字典命令
========
这是一种特殊的静态命令。每当您想在命令处理程序中使用一对数据（字符串 <-> 对应数据）时，都可以使用字典命令。字符串通常是对给定数据的文字描述。其思路是把字符串用作可由 shell 提示的命令语法，并使用对应数据来处理命令。

让我们看一个例子。假设您创建了一个设置 ADC 增益的命令。这正是可以使用字典的理想场景。字典将是一组键值对：(string: gain_value, int: value)，其中 int 值可用于 ADC 驱动 API。

此任务的抽象代码大致如下：

.. code-block:: c

        static int gain_cmd_handler(const struct shell *sh,
                                    size_t argc, char **argv, void *data)
        {
                int gain;

                /* data is a value corresponding to called command syntax */
                gain = (int)data;
                adc_set_gain(gain);

                shell_print(sh, "ADC gain set to: %s\n"
                                   "Value send to ADC driver: %d",
                                   argv[0],
                                   gain);

                return 0;
        }

        SHELL_SUBCMD_DICT_SET_CREATE(sub_gain, gain_cmd_handler,
                (gain_1, 1, "gain 1"), (gain_2, 2, "gain 2"),
                (gain_1_2, 3, "gain 1/2"), (gain_1_4, 4, "gain 1/4")
        );
        SHELL_CMD_REGISTER(gain, &sub_gain, "Set ADC gain", NULL);


它在 shell 中看起来会是这样：

.. image:: images/dict_cmd.png
      :align: center
      :alt: 字典命令示例。

动态命令
--------

演示如何创建带静态和动态子命令的根命令的示例代码。开始时动态命令列表为空。可以通过键入以下命令添加新命令：

.. code-block:: none

        dynamic add <new_dynamic_command>

可以使用 :kbd:`Tab` 键提示或自动补全新添加的命令。

.. image:: images/dynamic_cmd.PNG
      :align: center
      :alt: 带静态和动态命令的命令树。

.. code-block:: c

        /* Buffer for 10 dynamic commands */
        static char dynamic_cmd_buffer[10][50];

        /* commands counter */
        static uint8_t dynamic_cmd_cnt;

        /* Function returning command dynamically created
         * in  dynamic_cmd_buffer.
         */
        static void dynamic_cmd_get(size_t idx,
                                    struct shell_static_entry *entry)
        {
                if (idx < dynamic_cmd_cnt) {
                        entry->syntax = dynamic_cmd_buffer[idx];
                        entry->handler  = NULL;
                        entry->subcmd = NULL;
                        entry->help = "Show dynamic command name.";
                } else {
                        /* if there are no more dynamic commands available
                         * syntax must be set to NULL.
                         */
                        entry->syntax = NULL;
                }
        }

        SHELL_DYNAMIC_CMD_CREATE(m_sub_dynamic_set, dynamic_cmd_get);
        SHELL_STATIC_SUBCMD_SET_CREATE(m_sub_dynamic,
                SHELL_CMD(add, NULL,"Add new command to dynamic_cmd_buffer and"
                          " sort them alphabetically.",
                          cmd_dynamic_add),
                SHELL_CMD(execute, &m_sub_dynamic_set,
                          "Execute a command.", cmd_dynamic_execute),
                SHELL_CMD(remove, &m_sub_dynamic_set,
                          "Remove a command from dynamic_cmd_buffer.",
                          cmd_dynamic_remove),
                SHELL_CMD(show, NULL,
                          "Show all commands in dynamic_cmd_buffer.",
                          cmd_dynamic_show),
                SHELL_SUBCMD_SET_END
        );
        SHELL_CMD_REGISTER(dynamic, &m_sub_dynamic,
                   "Demonstrate dynamic command usage.", cmd_dynamic);

示例实现可在以下位置找到：:zephyr_file:`samples/subsys/shell/shell_module/src/dynamic_cmd.c`。

命令执行
========

每个命令或子命令都可以有处理程序。shell 会执行在命令树中找到的最深层处理程序，而后续没有处理程序的子命令会作为参数传递。括号内的字符会被视为一个参数。如果 shell 找不到处理程序，它将显示错误消息。

也可以从用户应用中使用任何活动后端和 :c:func:`shell_execute_cmd` 函数执行命令，如本示例所示：

.. code-block:: c

        int main(void)
        {
                /* Below code will execute "clear" command on a DUMMY backend */
                shell_execute_cmd(NULL, "clear");

                /* Below code will execute "shell colors off" command on
                 * an UART backend
                 */
                shell_execute_cmd(shell_backend_uart_get_ptr(),
                                  "shell colors off");
        }

通过设置 Kconfig :kconfig:option:`CONFIG_SHELL_BACKEND_DUMMY` 选项来启用 DUMMY 后端。

命令执行示例
------------

假设命令结构如下图所示，其中：

* :c:macro:`root_cmd` - 没有处理程序的根命令
* :c:macro:`cmd_xxx_h` - 命令有处理程序
* :c:macro:`cmd_xxx` - 命令没有处理程序

.. image:: images/execution.png
      :align: center
      :alt: Command tree with static commands.

示例 1
^^^^^^
序列：:c:macro:`root_cmd` :c:macro:`cmd_1_h` :c:macro:`cmd_12_h` :c:macro:`cmd_121_h` :c:macro:`parameter` 将执行命令 :c:macro:`cmd_121_h`，并将 :c:macro:`parameter` 作为参数传递。

示例 2
^^^^^^
序列：:c:macro:`root_cmd` :c:macro:`cmd_2` :c:macro:`cmd_22_h` :c:macro:`parameter1` :c:macro:`parameter2` 将执行命令 :c:macro:`cmd_22_h`，并将 :c:macro:`parameter1` :c:macro:`parameter2` 作为参数传递。

示例 3
^^^^^^
序列：:c:macro:`root_cmd` :c:macro:`cmd_1_h` :c:macro:`parameter1` :c:macro:`cmd_121_h` :c:macro:`parameter2` 将执行命令 :c:macro:`cmd_1_h`，并将 :c:macro:`parameter1`、:c:macro:`cmd_121_h` 和 :c:macro:`parameter2` 作为参数传递。

示例 4
^^^^^^
序列：:c:macro:`root_cmd` :c:macro:`parameter` :c:macro:`cmd_121_h` :c:macro:`parameter2` 不会执行任何命令。


命令处理程序
------------

简单的命令处理程序实现：

.. code-block:: c

        static int cmd_handler(const struct shell *sh, size_t argc,
                                char **argv)
        {
                ARG_UNUSED(argc);
                ARG_UNUSED(argv);

                shell_fprintf(sh, SHELL_INFO, "Print info message\n");

                shell_print(sh, "Print simple text.");

                shell_warn(sh, "Print warning text.");

                shell_error(sh, "Print error text.");

                return 0;
        }

:c:func:`shell_fprintf` 函数或 shell 打印宏 :c:macro:`shell_print`、:c:macro:`shell_info`、:c:macro:`shell_warn` 和 :c:macro:`shell_error` 可以在命令处理程序或线程中使用，但不能在中断上下文中使用。中断处理程序应改用 :ref:`日志 API <logging_api>` 进行打印。

命令帮助
--------

每个用户自定义命令或子命令都可以有自己的帮助描述。命令和子命令的帮助可以使用相应的宏创建：:c:macro:`SHELL_CMD_REGISTER`、:c:macro:`SHELL_CMD_ARG_REGISTER`、:c:macro:`SHELL_CMD` 和 :c:macro:`SHELL_CMD_ARG`。

当您使用 ``-h`` 或 ``--help`` 参数调用命令或子命令时，shell 会打印此帮助消息。

父命令
------

在子命令处理程序中，您可以访问传递给命令的参数或父命令，具体取决于您如何索引 ``argv``。

* 使用正数索引 ``argv`` 时，您可以访问参数。
* 使用负数索引 ``argv`` 时，您可以访问父命令。
* 处理程序所属的子命令的 ``argv`` 索引为 0。

.. code-block:: c

        static int cmd_handler(const struct shell *sh, size_t argc,
                               char **argv)
        {
                ARG_UNUSED(argc);

                /* If it is a subcommand handler parent command syntax
                 * can be found using argv[-1].
                 */
                shell_print(sh, "This command has a parent command: %s",
                              argv[-1]);

                /* Print this command syntax */
                shell_print(sh, "This command syntax is: %s", argv[0]);

                /* Print first argument */
                shell_print(sh, "%s", argv[1]);

                return 0;
        }

内置命令
========

这些命令通过将 :kconfig:option:`CONFIG_SHELL_CMDS` 设置为 ``y`` 来激活。

* :command:`aliases` - 显示当前配置的别名。此命令需要额外激活：将 :kconfig:option:`CONFIG_SHELL_CMDS_ALIASES` 设置为 ``y``。
* :command:`clear` - 清除屏幕。
* :command:`history` - 显示最近输入的命令。
* :command:`resize` - 当终端宽度不是 80 个字符时，或在每次更改终端宽度后，必须执行此命令。它确保正确显示多行文本并正确处理 :kbd:`←`、:kbd:`→`、:kbd:`End`、:kbd:`Home` 键。目前此命令仅在启用 UART 流控时有效。也可以用子命令调用它：

        * :command:`default` - shell 会把终端宽度 = 80 发送到终端，并假定已成功送达。

  这些命令需要额外激活：将 :kconfig:option:`CONFIG_SHELL_CMDS_RESIZE` 设置为 ``y``。
* :command:`select` - 可用于设置新的根命令。使用 alt+r 退出到主命令树。此命令需要额外激活：将 :kconfig:option:`CONFIG_SHELL_CMDS_SELECT` 设置为 ``y``。
* :command:`shell` - 根命令，带有以下有用的 shell 相关子命令：

        * :command:`echo` - 切换 shell 回显。
        * :command:`colors` - 切换彩色语法。在使用 Bluetooth shell 时，这有助于限制传输的字节数。
        * :command:`stats` - 显示 shell 统计信息。

别名支持
********

当启用 :kconfig:option:`CONFIG_SHELL_ALIASES` 时，shell 可以在执行命令之前展开别名。Zephyr 始终提供内置别名 :command:`?`，它会展开为 :command:`help`。

要从主机文件加载其他别名，请设置 :kconfig:option:`CONFIG_SHELL_ALIASES_FILE`，并从应用的 ``CMakeLists.txt`` 文件生成相应的包含文件。当 :kconfig:option:`CONFIG_SHELL_ALIASES_FILE` 非空时，会自动启用 :kconfig:option:`CONFIG_SHELL_ALIASES_HAS_FILE`。

.. code-block:: cmake

   if(CONFIG_SHELL_ALIASES_HAS_FILE)
     set(gen_dir ${ZEPHYR_BINARY_DIR}/include/generated/)
     set(aliases_src ${CONFIG_SHELL_ALIASES_FILE})

     generate_shell_aliases_inc_file_for_target(
       app
       ${aliases_src}
       ${gen_dir}/generated-shell-aliases.inc
     )
   endif()

别名文件每行使用一个 ``alias=command`` 条目。以 ``#`` 开头的行是注释，包含空格的命令字符串必须加引号。:zephyr_file:`samples/net/sockets/echo_service/shell_aliases.txt` 中的示例使用以下格式：

.. code-block:: none

   # Example shell aliases file
   stacks="kernel thread stacks"
   scan="wifi scan"
   connect="wifi connect"

使用 :command:`aliases` 命令查看运行中的 shell 中可用的别名。

.. _tab-feature:

Tab 功能
********

Tab 按钮可用于提示命令或子命令。通过将 :kconfig:option:`CONFIG_SHELL_TAB` 设置为 ``y`` 来启用此功能。它还可用于命令的部分或完整自动补全。通过将 :kconfig:option:`CONFIG_SHELL_TAB_AUTOCOMPLETION` 设置为 ``y`` 来激活此功能。当用户开始输入命令并按 :kbd:`Tab` 按钮时，shell 将执行以下 3 种可能操作之一：

* 自动补全命令。
* 提示可用命令，并在可能时部分补全命令。
* 如果没有可用或匹配的命令，则不执行任何操作。

.. image:: images/tab_prompt.png
      :align: center
      :alt: Tab 功能使用示例

.. _history-feature:

历史记录功能
************

此功能在 shell 中启用命令历史记录。通过将 :kconfig:option:`CONFIG_SHELL_HISTORY` 设置为 ``y`` 来激活。如果元键处于活动状态，可以使用以下按键访问历史记录：:kbd:`↑` :kbd:`↓` 或 :kbd:`Ctrl+n` 和 :kbd:`Ctrl+p`。可以存储的命令数量取决于 :kconfig:option:`CONFIG_SHELL_HISTORY_BUFFER` 参数的大小。

通配符功能
**********

shell 模块可以处理通配符。当被展开的命令及其子命令没有处理程序时，通配符会被正确解释。例如，如果您想为 ``app`` 和 ``app_test`` 模块将日志级别设置为 ``err``，可以执行以下命令：

.. code-block:: none

        log enable err a*

.. image:: images/wildcard.png
      :align: center
      :alt: 通配符使用示例

通过将 :kconfig:option:`CONFIG_SHELL_WILDCARD` 设置为 ``y`` 来激活此功能。

.. note::
        启用通配符功能后，字符 ``*`` 和 ``?`` 不能作为普通字符用于命令或参数中。

元键功能
********

shell 模块支持以下元键：

.. list-table:: 已实现的元键
   :widths: 10 40
   :header-rows: 1

   * - 元键
     - 操作
   * - :kbd:`Ctrl+a`
     - 将光标移动到行首。
   * - :kbd:`Ctrl+b`
     - 将光标向后移动一个字符。
   * - :kbd:`Ctrl+c`
     - 在屏幕上保留最后一条命令，并在新行中开始新命令。
   * - :kbd:`Ctrl+d`
     - 删除光标下的字符。
   * - :kbd:`Ctrl+e`
     - 将光标移动到行尾。
   * - :kbd:`Ctrl+f`
     - 将光标向前移动一个字符。
   * - :kbd:`Ctrl+k`
     - 删除从光标到行尾的内容。
   * - :kbd:`Ctrl+l`
     - 清除屏幕，并将当前输入的命令留在屏幕顶部。
   * - :kbd:`Ctrl+n`
     - 在历史记录中移到下一项。
   * - :kbd:`Ctrl+p`
     - 在历史记录中移到上一项。
   * - :kbd:`Ctrl+t`
     - 当设置了 :kconfig:option:`CONFIG_SHELL_LOG_BACKEND` 时，切换 shell 上的日志输出。
   * - :kbd:`Ctrl+u`
     - 清除当前输入的命令。
   * - :kbd:`Ctrl+w`
     - 删除光标左侧的单词或单词的一部分。以句点而不是空格分隔的单词会被视为一个单词。
   * - :kbd:`Alt+b`
     - 将光标向后移动一个单词。
   * - :kbd:`Alt+f`
     - 将光标向前移动一个单词。

通过将 :kconfig:option:`CONFIG_SHELL_METAKEYS` 设置为 ``y`` 来激活此功能。

sys_getopt 功能
***************

除子命令之外，一些 shell 用户可能还需要使用选项。参数字符串，用于查找受支持的选项。通常，这项任务由 ``getopt`` 系列函数完成。

为此，shell 支持来自 FreeBSD 项目的 getopt 和 getopt_long 库的变体，称为 sys_getopt 和 sys_getopt_long。通过将 :kconfig:option:`CONFIG_GETOPT` 设置为 ``y`` 并将 :kconfig:option:`CONFIG_GETOPT_LONG` 设置为 ``y`` 来激活此功能。

此功能既可以以线程安全的方式使用，也可以以非线程安全的方式使用。前者与常规 getopt 用法完全兼容，而后者略有不同。

非线程安全用法示例：

.. code-block:: c

  char *cvalue = NULL;
  while ((char c = sys_getopt(argc, argv, "abhc:")) != -1) {
        switch (c) {
        case 'c':
                cvalue = sys_getopt_optarg;
                break;
        default:
                break;
        }
  }

线程安全用法示例：

.. code-block:: c

  char *cvalue = NULL;
  struct sys_getopt_state *state;
  while ((char c = sys_getopt(argc, argv, "abhc:")) != -1) {
        state = sys_getopt_state_get();
        switch (c) {
        case 'c':
                cvalue = state->optarg;
                break;
        default:
                break;
        }
  }

通过将 :kconfig:option:`CONFIG_SHELL_GETOPT` 设置为 ``y`` 来激活线程安全的 sys_getopt 功能。

遮蔽输入功能
************

借助遮蔽输入功能，shell 可用于实现登录提示或其他用户交互，在这种情况下，用户键入的字符不应显示在屏幕上，例如输入密码时。

一旦遮蔽输入被接受，通常希望让 shell 恢复正常运行。使用 ``shell_obscure_set`` 函数即可进行这种运行时控制。

使用此功能的登录和注销命令示例位于 :zephyr_file:`samples/subsys/shell/shell_module/src/main.c` 和配置文件 :zephyr_file:`samples/subsys/shell/shell_module/prj_login.conf` 中。

通过将 :kconfig:option:`CONFIG_SHELL_START_OBSCURED` 设置为 ``y``，此功能会在启动时激活。无论该选项如何设置，之后仍可在运行时控制。借助 ``shell_set_root_cmd`` 函数，:kconfig:option:`CONFIG_SHELL_CMDS_SELECT` 有助于阻止输入除登录命令之外的任何其他命令。同样，:kconfig:option:`CONFIG_SHELL_PROMPT_UART` 允许您在启动时设置提示符，但之后可以用 ``shell_prompt_change`` 函数更改。

.. _shell-readline:

读取用户输入
************

shell 提供 :c:func:`shell_readline` 函数，允许命令处理程序以交互方式从用户读取一行输入。这对于实现需要向用户提示额外信息的命令很有用，例如确认对话框、多步向导或交互式数据输入。

该函数从 shell 传输层读取数据，直到收到换行字符，并将数据存储到提供的缓冲区中。缓冲区中不包含换行字符本身。成功时缓冲区会自动以空字符结尾。

调用 :c:func:`shell_readline` 之前，使用 :c:func:`shell_readline_prompt_set` 显示提示字符串（例如 ``"Proceed? [y/N]: "``）。提示会在开始 readline 时自动打印，并在任何中断输入行的日志消息之后恢复。当 :c:func:`shell_readline` 返回时，提示会被清除。

.. note::

   应在 shell 命令处理程序中从 shell 线程调用 :c:func:`shell_readline` 函数，它会阻塞该线程，直到返回结果。

用法示例：

.. code-block:: c

   static int cmd_read_secret(const struct shell *sh, size_t argc, char **argv)
   {
           uint8_t input_buf[256];
           int ret;

           shell_obscure_set(sh, true);
           shell_readline_prompt_set(sh, "Enter your secret: ");
           ret = shell_readline(sh, input_buf, sizeof(input_buf), K_SECONDS(10));
           shell_obscure_set(sh, false);

           if (ret < 0) {
                   if (ret == -ETIMEDOUT) {
                           shell_error(sh, "Timeout waiting for input");
                   } else if (ret == -ECANCELED) {
                           shell_error(sh, "Input canceled");
                   } else if (ret == -ENOBUFS) {
                           shell_error(sh, "Input too long");
                   }
                   return ret;
           }

           shell_print(sh, "Secret input received (%d bytes)", ret);
           return 0;
   }

Shell 日志记录器后端功能
************************

Shell 实例可以充当 :ref:`日志 API <logging_api>` 后端。shell 确保日志消息与 shell 输出正确地多路复用。来自日志记录器线程的日志消息会入队，并在 shell 线程中处理。如果队列已满，日志记录器线程将阻塞可配置的一段时间，在这段时间内阻塞日志记录器线程上下文。超时后会从队列中移除最旧的日志消息，并将新消息入队。使用 ``shell stats show`` 命令可获取 shell 实例丢弃的日志消息数量。日志队列大小和超时是 :c:macro:`SHELL_DEFINE` 的参数。

通过将 :kconfig:option:`CONFIG_SHELL_LOG_BACKEND` 设置为 ``y`` 来激活此功能。

.. warning::
        当系统中使用多个后端时，必须谨慎设置入队超时。shell 实例的传输层可能较慢，或者可能被阻塞，例如被带硬件流控的 UART 阻塞。如果超时设置得过高，日志记录器线程可能会被阻塞，并影响其他日志记录器后端。

.. warning::
        由于 shell 是一个复杂的日志记录器后端，如果应用在 shell 线程运行之前崩溃，它就无法输出日志。在这种情况下，您可以改为启用一种简单的日志记录后端，例如 UART （:kconfig:option:`CONFIG_LOG_BACKEND_UART`）或 RTT （:kconfig:option:`CONFIG_LOG_BACKEND_RTT`），这些后端在系统初始化期间更早可用。

.. note::
        shell 日志后端由 :c:func:`shell_start` 启用。当 :kconfig:option:`CONFIG_SHELL_AUTOSTART` 设置为 ``y`` 时，这会在 shell 线程首次被调度时发生。默认情况下 shell 线程以低优先级运行，因此这一时刻取决于更高优先级的线程（包括执行系统初始化的主线程）何时阻塞或结束。在此之前发出的、通过日志记录器路由的日志消息和 ``printk()`` 输出（:kconfig:option:`CONFIG_LOG_PRINTK`）由日志核心处理，而不是由 shell 处理：

        * 在延迟模式（:kconfig:option:`CONFIG_LOG_MODE_DEFERRED`）下，只要它们能放进 :kconfig:option:`CONFIG_LOG_BUFFER_SIZE`，就会被缓冲，并在 shell 启动后打印。
        * 在立即模式（:kconfig:option:`CONFIG_LOG_MODE_IMMEDIATE`）下，它们会丢失，因为没有活动后端来输出它们。

        如果应用需要在 shell 上尽早输出，请将 :kconfig:option:`CONFIG_SHELL_AUTOSTART` 设置为 ``n``，并显式调用 :c:func:`shell_start`，例如从优先级高于 shell 后端初始化优先级的 :c:macro:`SYS_INIT` 钩子中调用（例如 :kconfig:option:`CONFIG_SHELL_BACKEND_SERIAL_INIT_PRIORITY`）。或者，不要让 ``printk()`` 经由日志记录器路由。

RTT 后端通道选择
****************

除了将 shell 用作日志记录器后端之外，RTT shell 后端和 RTT 日志后端也可以同时使用，但需使用不同的通道。通过将它们分开，可以在没有 shell 输出的情况下捕获或监控日志，也可以在没有日志干扰的情况下对 shell 编写脚本。默认情况下同时启用 Shell RTT 后端和 Log RTT 后端不可行，因为两者默认都使用通道 ``0``。有两种选择：

1. Shell 缓冲区可以使用备用通道，例如将 :kconfig:option:`CONFIG_SHELL_BACKEND_RTT_BUFFER` 设置为 ``1``。这样，在脚本通过通道 1 进行交互的同时，可以使用 `JLinkRTTViewer <https://www.segger.com/products/debug-probes/j-link/technology/about-real-time-transfer/#j-link-rtt-viewer>`_ 监控日志。

2. 日志缓冲区可以使用备用通道，例如将 :kconfig:option:`CONFIG_LOG_BACKEND_RTT_BUFFER` 设置为 ``1``。这样可以通过 JLinkRTTViewer 交互使用 shell，同时将日志写入文件。

有关如何启用 RTT 作为 Shell 后端的详细信息，请参见 `shell 后端 <后端_>`_。

.. _shell_remote:

远程 shell
**********

shell 模块支持远程 shell。远程 shell 允许使用主核的 shell 接口在远程核上执行命令。远程 shell 客户端支持 ``Tab`` 自动补全或历史记录导航等用户界面功能。可以有多个远程客户端连接到主核 shell。每个远程客户端都有自己的命令树。远程客户端命令在远程客户端核的上下文中执行。远程 shell 使用 :ref:`IPC 服务 <ipc_service>` 与远程核通信。

如果只启用一个远程客户端，则 ``remote_shell`` 命令会注册为远程核命令树的根命令。如果启用多个远程客户端，则 ``remote_shell <core_name>`` 将用作给定远程客户端的根。

远程客户端实现支持禁用线程的情况（:kconfig:option:`CONFIG_MULTITHREADING` 设置为 ``n``）。

这种方法有两个主要优点：

1. 它允许主核和远程核使用相同的 shell 接口。
2. 完整的 shell 实现仅存在于主机核上，从而显著减少远程核的内存占用。每个远程客户端的实现使用不到 3 kB 内存。其中一半内存用于字符串格式化，并可以与其他使用字符串格式化的模块（例如日志记录）共享。

有关如何启用远程 shell 的详细信息，请参见 :zephyr:code-sample:`shell-module`。

配置
====

以下 Kconfig 选项可用于远程 shell 主机配置：

:kconfig:option:`CONFIG_SHELL_REMOTE`：在主机核上启用远程 shell。

:kconfig:option:`CONFIG_SHELL_REMOTE_MULTI_CLI`：启用多个远程客户端。

:kconfig:option:`CONFIG_SHELL_REMOTE_TMP_BUF_SIZE`：远程 shell 命令数据的临时缓冲区大小。需要足够大，以容纳命令及其参数。

以下 Kconfig 选项可用于远程 shell 客户端配置：

:kconfig:option:`CONFIG_SHELL_REMOTE_CLI`：在远程核上启用远程 shell 客户端。

:kconfig:option:`CONFIG_SHELL_REMOTE_CLI_BUF_SIZE`：用于远程消息的内部缓冲区大小。需要足够大，以容纳命令语法和帮助文本。如果缓冲区太小，帮助文本会被截断。它还用于存放 shell 打印消息的数据。如果缓冲区太小，打印消息会被错误消息替换。

:kconfig:option:`CONFIG_SHELL_REMOTE_CLI_KWORK`：使用 kwork 上下文执行命令。

:kconfig:option:`CONFIG_SHELL_REMOTE_CLI_STACK_SIZE`：远程 shell 客户端的线程栈大小。

如果使用单个客户端，则会根据 devicetree 配置自动选择 IPC 服务设备。用户可以使用 chosen 节点指定 IPC 设备树节点。如果未指定，那么在只有一个 IPC 设备可用时将使用该设备。

IPC 服务设备树节点配置示例：

.. code-block:: dts

        chosen {
                zephyr,ipc_shell = &ipc0;
        };


限制
====

远程 shell 客户端不支持某些 shell 功能：

* 远程 shell 客户端不支持旁路模式。
* 远程 shell 客户端不支持选择模式。

IPC 通信假定两端数据的字节序和对齐方式相同。它已在以下核组合上测试过：

* Cortex-M33（主机）和 Cortex-M33（客户端）
* Cortex-M33（主机）和 RISC-V 32（客户端）

用法
****

以下代码展示了此库的一个简单用例：

.. code-block:: c

        int main(void)
        {

        }

        static int cmd_demo_ping(const struct shell *sh, size_t argc,
                                 char **argv)
        {
                ARG_UNUSED(argc);
                ARG_UNUSED(argv);

                shell_print(sh, "pong");
                return 0;
        }

        static int cmd_demo_params(const struct shell *sh, size_t argc,
                                   char **argv)
        {
                int cnt;

                shell_print(sh, "argc = %d", argc);
                for (cnt = 0; cnt < argc; cnt++) {
                        shell_print(sh, "  argv[%d] = %s", cnt, argv[cnt]);
                }
                return 0;
        }

        /* Creating subcommands (level 1 command) array for command "demo". */
        SHELL_STATIC_SUBCMD_SET_CREATE(sub_demo,
                SHELL_CMD(params, NULL, "Print params command.",
                                                       cmd_demo_params),
                SHELL_CMD(ping,   NULL, "Ping command.", cmd_demo_ping),
                SHELL_SUBCMD_SET_END
        );
        /* Creating root (level 0) command "demo" without a handler */
        SHELL_CMD_REGISTER(demo, &sub_demo, "Demo commands", NULL);

        /* Creating root (level 0) command "version" */
        SHELL_CMD_REGISTER(version, NULL, "Show kernel version", cmd_version);


用户可以使用 :kbd:`Tab` 键补全命令/子命令，或查看当前输入的命令级别可用的子命令。例如，当光标位于命令行开头并按下 :kbd:`Tab` 键时，用户将看到所有根（第 0 级）命令：

.. code-block:: none

          clear  demo  shell  history  log  resize  version


.. note::
        要查看特定命令可用的子命令，必须先在该命令后键入 :kbd:`space`，然后按 :kbd:`Tab`。

这些命令由各个模块注册，例如：

* :command:`clear`、:command:`shell`、:command:`history` 和 :command:`resize` 是由 :zephyr_file:`subsys/shell/shell.c` 注册的内置命令
* :command:`demo` 和 :command:`version` 已在上面由 main.c 的示例代码中注册
* :command:`log` 由 :zephyr_file:`subsys/logging/log_cmds.c` 注册

然后，如果用户键入 :command:`demo` 命令并按 :kbd:`Tab` 键，shell 将只打印为此命令注册的子命令：

.. code-block:: none

          params  ping

API 参考
********

.. doxygengroup:: shell_api
