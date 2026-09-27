.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _gdbstub:

GDB stub
########

.. contents::
   :local:
   :depth: 2

概述
****

gdbstub 功能提供了 GDB 远程串行协议 (RSP) 的实现，允许使用 GDB 远程调试 Zephyr。

该协议支持不同的连接类型：串行、UDP/IP 和 TCP/IP。Zephyr 目前仅支持串行设备通信。

GDB 程序充当客户端，而 Zephyr gdbstub 充当服务器。启用此功能后，Zephyr 会在 :c:func:`gdb_init` 启动 gdbstub 服务后停止执行，并等待 GDB 连接。连接建立后，就可以与 Zephyr 进行同步交互。请注意，目前尚无法异步向目标发送命令。

功能
****

支持以下功能：

* 添加和删除断点
* 继续运行和单步执行目标
* 打印回溯
* 读取或写入通用寄存器
* 读取或写入内存

启用 GDB Stub
*************

可以使用 :kconfig:option:`CONFIG_GDBSTUB` 选项启用 GDB stub。

使用串行后端
============

可以使用 :kconfig:option:`CONFIG_GDBSTUB_SERIAL_BACKEND` 选项为 GDB stub 启用串行后端。

由于串行后端利用 UART 设备发送和接收 GDB 命令，

* 如果开发板上有空闲的 UART 设备，请将 chosen 节点的 ``zephyr,gdbstub-uart`` 属性设置为该空闲 UART 设备，这样 :c:func:`printk` 和日志消息就不会打印到用于 GDB 的同一 UART 设备上。

* 对于只有一个 UART 设备的开发板，如果 :c:func:`printk` 和日志功能也使用同一个 UART 设备进行输出，则必须禁用它们。GDB 相关消息可能会与日志消息交织，从而产生意外后果。通常可以通过禁用 :kconfig:option:`CONFIG_PRINTK` 和 :kconfig:option:`CONFIG_LOG` 来实现。

调试
****

Using Serial Backend
====================

#. 构建时启用 GDB stub 和串行后端。

#. 将构建的镜像烧写到开发板并复位开发板。

   * 此时执行应暂停在 :c:func:`gdb_init` 处。

#. 在开发机上执行 GDB 并连接到 GDB stub。

   .. code-block:: bash

      target remote <serial device>

   例如，

   .. code-block:: bash

      target remote /dev/ttyUSB1

#. 可以使用 GDB 命令开始调试。

示例
****

有一个测试应用 :zephyr_file:`tests/subsys/debug/gdbstub`，它的一个测试用例 ``debug.gdbstub.breakpoints`` 演示了如何使用 Zephyr GDB stub。该测试还有一个用例连接到 QEMU 的 GDB stub 实现（使用自定义端口 ``tcp:1235``），作为验证测试脚本本身的参考。

在 :envvar:`ZEPHYR_BASE` 目录中运行以下命令来执行测试：

   .. code-block:: console

      west twister -p qemu_x86 -T tests/subsys/debug/gdbstub

该测试应能成功运行，现在我们逐步执行类似操作，从 GDB 用户的角度演示 Zephyr GDB stub 的工作原理。

在下面的代码片段中，请使用你自己的相应目录，而不是 ``<SDK install directory>``、``<build_directory>``、``<ZEPHYR_BASE>``。


#. 打开两个终端窗口。

#. 在第一个终端中，构建并运行测试应用：

   .. zephyr-app-commands::
      :zephyr-app: tests/subsys/debug/gdbstub
      :host-os: unix
      :board: qemu_x86
      :gen-args: '-DCONFIG_QEMU_EXTRA_FLAGS="-serial tcp:localhost:5678,server"'
      :goals: build run

   请注意我们如何设置 :kconfig:option:`CONFIG_QEMU_EXTRA_FLAGS`，将 QEMU 串行控制台端口定向到 ``localhost`` TCP 端口 ``5678``，以等待我们将在后续步骤中执行的 GDB ``remote`` 命令发起连接。

#. 在第二个终端中，启动 GDB：

   .. code-block:: bash

      <SDK install directory>/x86_64-zephyr-elf/bin/x86_64-zephyr-elf-gdb

   #. 告诉 GDB 在哪里查找构建的 ELF 文件：

      .. code-block:: text

         (gdb) symbol-file <build directory>/zephyr/zephyr.elf

      GDB 的响应：

      .. code-block:: text

         Reading symbols from <build directory>/zephyr/zephyr.elf...

   #. 告诉 GDB 连接到 Zephyr gdbstub 串行后端；该后端此前已通过 QEMU 中的 TCP 端口 ``-serial`` 重定向作为服务器对外提供。

      .. code-block:: text

         (gdb) target remote localhost:5678

      GDB 的响应：

      .. code-block:: text

         Remote debugging using localhost:5678
         arch_gdb_init () at <ZEPHYR_BASE>/arch/x86/core/ia32/gdbstub.c:252
         252     }

      GDB 还会显示代码执行停止的位置。在本例中，它位于 :zephyr_file:`arch/x86/core/ia32/gdbstub.c` 的第 252 行。

   #. 使用命令 ``bt`` 或 ``backtrace`` 显示栈帧的回溯。

      .. code-block:: text

         (gdb) bt
         #0  arch_gdb_init () at <ZEPHYR_BASE>/arch/x86/core/ia32/gdbstub.c:252
         #1  0x00104140 in gdb_init () at <ZEPHYR_BASE>/zephyr/subsys/debug/gdbstub.c:852
         #2  0x00109c13 in z_sys_init_run_level (level=INIT_LEVEL_PRE_KERNEL_2) at <ZEPHYR_BASE>/kernel/init.c:360
         #3  0x00109e73 in z_cstart () at <ZEPHYR_BASE>/kernel/init.c:630
         #4  0x00104422 in z_prep_c (arg=0x1245bc <x86_cpu_boot_arg>) at <ZEPHYR_BASE>/arch/x86/core/prep_c.c:80
         #5  0x001000c9 in __csSet () at <ZEPHYR_BASE>/arch/x86/core/ia32/crt0.S:290
         #6  0x001245bc in uart_dev ()
         #7  0x00134988 in z_interrupt_stacks ()
         #8  0x00000000 in ?? ()

   #. 使用命令 ``list`` 显示代码执行停止处的源代码及周边内容。

      .. code-block:: text

         (gdb) list
         247             __asm__ volatile ("int3");
         248
         249     #ifdef CONFIG_GDBSTUB_TRACE
         250             printk("gdbstub:%s GDB is connected\n", __func__);
         251     #endif
         252     }
         253
         254     /* Hook current IDT. */
         255     _EXCEPTION_CONNECT_NOCODE(z_gdb_debug_isr, IV_DEBUG, 3);
         256     _EXCEPTION_CONNECT_NOCODE(z_gdb_break_isr, IV_BREAKPOINT, 3);

   #. 使用命令 ``s`` 或 ``step`` 单步执行程序，直到到达不同的源代码行。现在它已执行完 :c:func:`arch_gdb_init`，并继续在 :c:func:`gdb_init` 中执行。

      .. code-block:: text

         (gdb) s
         gdb_init () at <ZEPHYR_BASE>/subsys/debug/gdbstub.c:857
         857     return 0;

      .. code-block:: text

         (gdb) list
         852             arch_gdb_init();
         853
         854     #ifdef CONFIG_GDBSTUB_TRACE
         855             printk("gdbstub:%s exit\n", __func__);
         856     #endif
         857             return 0;
         858     }
         859
         860     #ifdef CONFIG_XTENSA
         861     /*

   #. 使用命令 ``br`` 或 ``break`` 设置断点。在本示例中，在 :c:func:`main` 处设置一个断点，然后使用命令 ``c`` （或 ``continue``）让代码执行在不进行任何干预的情况下继续。

      .. code-block:: text

         (gdb) break main
         Breakpoint 1 at 0x10064d: file <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c, line 27.

      .. code-block:: text

         (gdb) continue
         Continuing.

      一旦代码执行到达 :c:func:`main`，执行将停止，GDB 提示符返回。

      .. code-block:: text

         Breakpoint 1, main () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:27
         27              printk("%s():enter\n", __func__);

      现在 GDB 正等待在 :c:func:`main` 开头：

      .. code-block:: text

         (gdb) list
         22
         23      int main(void)
         24      {
         25              int ret;
         26
         27              printk("%s():enter\n", __func__);
         28              ret = test();
         29              printk("ret=%d\n", ret);
         30              return 0;
         31      }

   #. 要检查 ``ret`` 的值，可以使用命令 ``p`` 或 ``print``。

      .. code-block:: text

         (gdb) p ret
         $1 = 1273788

      由于 ``ret`` 尚未初始化，它包含一些随机值。

   #. 如果在这里使用单步（``s`` 或 ``step``），它将继续执行并跳过 :c:func:`test` 的内部。要检查 :c:func:`test` 内部的代码执行情况，可以为 :c:func:`test` 设置断点，或者直接使用 ``si`` （或 ``stepi``）执行一条机器指令，其副作用是会进入该函数。可以使用 GDB 命令 ``finish`` 让执行在不进行干预的情况下继续，直到该函数返回。

      .. code-block:: text

         (gdb) finish
         Run till exit from #0  test () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:17
         0x00100667 in main () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:28
         28              ret = test();
         Value returned is $2 = 30

   #. 再次检查 ``ret``，它应该包含 :c:func:`test` 的返回值。有时，需要再执行一次 ``step`` 才会完成赋值，本例就是如此。这是因为赋值代码在函数返回后才执行。赋值代码由工具链生成为机器指令，在查看对应的 C 源文件时不可见。

      .. code-block:: text

         (gdb) p ret
         $3 = 1273788
         (gdb) step
         29              printk("ret=%d\n", ret);
         (gdb) p ret
         $4 = 30

   #. 如果在这里发出 ``continue`` 命令，代码执行将无限期地继续，因为没有其他断点可以停止执行。通过 :kbd:`Ctrl-C` 中断 GDB 中的执行目前不起作用，因为 Zephyr gdbstub 尚不支持此功能。切换到运行 Zephyr 镜像的 QEMU 的第一个控制台，并使用 :kbd:`Ctrl+a x` 手动停止它。当同一测试由 Twister 执行时，它会自动处理停止 QEMU 实例的操作。
