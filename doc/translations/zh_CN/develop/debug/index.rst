.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _develop_debug:

调试
####

.. _application_debugging:

应用调试
********

本节提供使用 QEMU 调试应用的快速实践参考。大部分内容已在 `QEMU`_ 和 `GNU_Debugger`_ 参考手册中介绍。

.. _QEMU: https://wiki.qemu.org/Main_Page

.. _GNU_Debugger: https://www.gnu.org/software/gdb

本快速参考介绍一些快捷方法、专用环境变量和参数，帮助你快速搭建调试环境。

调试 QEMU 中运行的应用，最简单的方法是使用 GNU 调试器，并通过 QEMU 在开发系统上启动本地 GDB 服务器。

调试需要 :abbr:`ELF (Executable and Linkable Format)` 二进制镜像。构建系统在构建目录中生成该镜像。内核二进制文件默认名为 :file:`zephyr.elf`，可通过 :kconfig:option:`CONFIG_KERNEL_BIN_NAME` 更改。

GDB 服务器
==========

这里使用标准 TCP 端口 1234 启动 :abbr:`GDB (GNU Debugger)` 服务器实例。可根据开发环境更改端口号。有多种实现方式，每种方式都会启动一个处理器暂停执行的 QEMU 实例，并让 GDB 服务器实例监听连接。

直接运行 QEMU
~~~~~~~~~~~~~

可以让 QEMU 在执行任何代码之前监听“gdb 连接”，以便调试。

.. code-block:: bash

   qemu -s -S <image>

这会使 QEMU 监听端口 1234，等待 GDB 连接。

上述选项含义如下：

* ``-S``：启动时不运行 CPU；必须在监视器中输入 'c' 才会开始。
* ``-s``：:literal:`-gdb tcp::1234` 的简写，在 TCP 端口 1234 上启动 GDB 服务器。


通过 :command:`ninja` 运行 QEMU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在应用的构建目录中运行：

.. code-block:: console

   ninja debugserver

QEMU 将控制台输出写入通过 CMake 的 :makevar:`${QEMU_PIPE}` 指定的路径，通常为构建目录中的 :file:`qemu-fifo`。运行期间可用 :command:`tail -f qemu-fifo` 监视该文件。

通过 :command:`west` 运行 QEMU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在项目根目录运行：

.. code-block:: console

   west build -t debugserver_qemu

QEMU 将控制台输出写入调用 :command:`west` 的终端。

配置 :command:`gdbserver` 监听设备
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kconfig 选项 :kconfig:option:`CONFIG_QEMU_GDBSERVER_LISTEN_DEV` 控制监听设备，可以是 TCP 端口号或字符设备路径。GDB 9.0 及更新版本还支持 Unix 域套接字。

若未设置该选项，QEMU 调用将不带 ``-s`` 或 ``-gdb`` 参数。此时可通过 shell 环境变量 :envvar:`QEMU_EXTRA_FLAGS` 传入自定义监听设备配置。

GDB 客户端
==========

运行 :command:`gdb` 并输入以下命令连接服务器：

.. code-block:: bash

   $ path/to/gdb path/to/zephyr.elf
   (gdb) target remote localhost:1234
   (gdb) dir ZEPHYR_BASE

.. note::

   替换为系统上正确的 :ref:`ZEPHYR_BASE <important-build-vars>`。

可使用本地 GDB 配置文件 :file:`.gdbinit` 在每次运行时初始化 GDB 实例。:file:`.gdbinit` 通常放在主目录，但也可配置 GDB 从其他位置加载，包括调用 :command:`gdb` 的目录。以下示例文件与上述配置相同：

.. code-block:: none

   target remote localhost:1234
   dir ZEPHYR_BASE

其他界面
~~~~~~~~

GDB 提供在终端中运行的 curses 界面。调用 :command:`gdb` 时传入 ``--tui`` 选项，或在 :command:`gdb` 中执行 ``tui enable`` 命令。

.. note::

   开发系统上的 GDB 版本可能不支持 ``--tui`` 选项。请确保使用与构建该二进制文件所用工具链对应的 SDK 中的 GDB。

最后，以下命令使用 GDB 的图形前端 :abbr:`DDD (Data Display Debugger)` 连接 GDB 服务器。该命令从 ELF 二进制文件（此处为 :file:`zephyr.elf`）加载符号表。

.. code-block:: bash

   ddd --gdb --debugger "gdb zephyr.elf"

这两条命令均执行 :command:`gdb`。具体命令名称可能因工具链和交叉开发工具而异。

开发系统可能默认未安装 :command:`ddd`。请按系统说明安装，例如在 Ubuntu 上使用 :command:`sudo apt-get install ddd`。

Debugging
=========

按上述方式配置后，连接 GDB 客户端时，应用会停在系统启动阶段。你可以设置断点、单步执行代码等，操作方式与在 :command:`gdb` 中直接运行应用相同。

.. note::

   与直接在 GDB 中运行本机应用不同，:command:`gdb` 不会在应用运行时打印系统控制台输出。如果连接客户端后直接执行 :command:`continue`，应用会运行，但看起来没有任何变化。请按上述方法查看控制台输出。

使用 Eclipse 调试
*****************

概述
====

CMake 支持生成项目描述文件，可导入 Eclipse 集成开发环境（IDE）进行图形化调试。

`GNU MCU Eclipse plug-ins`_ 提供在 Eclipse 中通过 pyOCD、Segger J-Link 和 OpenOCD 调试工具调试 ARM 项目的机制。

以下教程演示在 Windows 上使用 Eclipse 和 pyOCD 调试 Zephyr 应用，假定已安装 GCC ARM Embedded 工具链和 pyOCD。

搭建 Eclipse 开发环境
=====================

#. 下载并安装 `Eclipse IDE for C/C++ Developers`_。

#. 在 Eclipse 中打开 ``Window->Eclipse Marketplace...`` 菜单，搜索 ``GNU MCU Eclipse``，在匹配结果中单击 ``Install``，安装 `GNU MCU Eclipse plug-ins`_。

#. 打开 ``Window->Preferences`` 菜单，进入 ``MCU``，设置 ``Global pyOCD Path``，以配置 pyOCD GDB 服务器路径。

生成并导入 Eclipse 项目
=======================

#. 按 :ref:`toolchain_gnuarmemb` 所述配置 GNU Arm Embedded 工具链。

#. 进入 Zephyr 目录树之外的文件夹构建应用。

   .. code-block:: console

      # On Windows
      cd %userprofile%

   .. note::
      如果构建目录像 Zephyr 通常的做法那样位于源代码目录下，CMake 会警告：

      “构建目录是源代码目录的子目录。

      Eclipse 对此支持不佳。强烈建议使用与源代码目录同级的构建目录。”

#. 使用 CMake 配置应用，再用 ninja 构建。注意，``-G"Eclipse CDT4 - Ninja"`` 参数指定了不同的 CMake 生成器。除通常的 ninja 构建文件外，还会生成 Eclipse 项目描述文件 :file:`.project`。

   .. zephyr-app-commands::
      :tool: all
      :zephyr-app: samples/synchronization
      :host-os: win
      :board: frdm_k64f
      :gen-args: -G"Eclipse CDT4 - Ninja"
      :goals: build
      :compact:

#. 在 Eclipse 中打开 ``File->Import...`` 菜单，选择 ``Existing Projects into Workspace``，导入生成的项目。在 ``Select root directory:`` 中选择应用构建目录。在找到的项目列表中勾选项目，然后单击 ``Finish``。

创建调试器配置
==============

#. 打开 ``Run->Debug Configurations...`` 菜单。

#. 选择 ``GDB PyOCD Debugging``，单击 ``New``，配置以下选项：

   - 在 Main 选项卡中：

     - Project：``my_zephyr_app@build``
     - C/C++ Application：:file:`zephyr/zephyr.elf`

   - 在 Debugger 选项卡中：

     - pyOCD 设置

       - Executable path：:file:`${pyocd_path}\\${pyocd_executable}`
       - 取消勾选“Allocate console for semihosting”

     - 开发板设置

       - Bus speed：8000000 Hz
       - 取消勾选“Enable semihosting”

     - GDB 客户端设置

       - Executable path 示例（使用你的 ``GNUARMEMB_TOOLCHAIN_PATH``）：:file:`C:\\gcc-arm-none-eabi-6_2017-q2-update\\bin\\arm-none-eabi-gdb.exe`

   - 在 SVD Path 选项卡中：

     - File path：:file:`<workspace top>\\modules\\hal\\nxp\\mcux\\devices\\MK64F12\\MK64F12.xml`

     .. note::
        此项可选，用于向调试器提供 SoC 的内存映射寄存器地址和位域。

#. 单击 ``Debug`` 开始调试。

RTOS 感知
=========

`pyOCD v0.11.0`_ 及更新版本支持 Zephyr RTOS 感知，可配合 Eclipse 中的 GDB PyOCD Debugging 使用，但必须在应用中启用 CONFIG_DEBUG_THREAD_INFO=y。

调试 I2C 通信
*************

可以记录应用执行的全部或部分 I2C 事务。通过 Kconfig 选项 :kconfig:option:`CONFIG_I2C_DUMP_MESSAGES` 启用此功能；由于它使用 :c:macro:`LOG_DBG` 打印内容，还必须启用 :kconfig:option:`CONFIG_I2C_LOG_LEVEL_DBG`。

转储输出示例如下::

   D: I2C msg: io_i2c_ctrl7_port0, addr=50
   D:    W      len=01: 00
   D:    R Sr P len=08:
   D: contents:
   D: 43 42 41 00 00 00 00 00 |CBA.....

第一行给出事务的 I2C 控制器和目标地址。上例中，I2C 控制器名为 ``io_i2c_ctrl7_port0``，目标设备地址为 ``0x50``。

.. note::

   地址、长度和内容均以十六进制表示，但不带 ``0x`` 前缀。

后续各行包含发送和接收的消息。写消息始终显示内容，读消息是否显示内容则由传给 ``i2c_dump_msgs_rw`` 的参数控制。用户可以调用此函数，``i2c_transfer`` API 也会在内部调用它，并启用读内容转储。消息长度前会用以下缩写打印消息头：

  - W：写消息
  - R：读消息
  - Sr：重复起始位
  - P：停止位

上例显示一条写消息，字节 ``0x00`` 表示要从 I2C 目标读取的寄存器地址。随后日志显示接收消息的长度，以及从目标读出的字节 ``43 42 41 00 00 00 00 00``。内容转储同时包含十六进制和 ASCII 表示。

过滤 I2C 通信转储
=================

默认记录所有 I2C 控制器与目标之间的全部通信。无关设备的日志可能淹没有用信息，使目标设备的通信难以调试。

启用 Kconfig 选项 :kconfig:option:`CONFIG_I2C_DUMP_MESSAGES_ALLOWLIST`，可创建要记录的 I2C 目标允许列表。通过设备树配置设备允许列表，例如::

  / {
      i2c {
          display0: some-display@a {
              ...
          };
          sensor3: some-sensor@b {
              ...
          };
      };

      i2c-dump-allowlist {
          compatible = "zephyr,i2c-dump-allowlist";
          devices = <&display0>, <&sensor3>;
      };
  };

过滤器节点通过值为 ``zephyr,i2c-dump-allowlist`` 的 compatible 字符串识别。``devices`` 属性通过指向 I2C 总线设备的 phandle 选择设备。

上例中，与 ``display0`` 和 ``sensor3`` 设备的通信将显示在日志中。



.. _Eclipse IDE for C/C++ Developers: https://www.eclipse.org/downloads/packages/eclipse-ide-cc-developers/oxygen2
.. _GNU MCU Eclipse plug-ins: https://gnu-mcu-eclipse.github.io/plugins/install/
.. _pyOCD v0.11.0: https://github.com/pyocd/pyOCD/releases/tag/v0.11.0
