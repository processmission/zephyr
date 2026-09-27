.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _llext_debug:

调试扩展
########

调试扩展是一项复杂的任务。由于扩展代码按定义并非与 Zephyr 应用程序一起构建，最终的 Zephyr ELF 文件不包含扩展代码的符号。此外，扩展在运行时由 :c:func:`llext_load` 动态重定位，因此即使符号可用，调试器也无法知道扩展代码中符号的最终位置。

在这种情况下，正确设置调试器会话需要一些手动步骤。以下各节将提供一些提示，介绍如何结合 Zephyr SDK 和 ``west`` 提供的调试功能完成设置，但这些说明可以适用于任何基于 GDB 的调试环境。

扩展调试流程
============

1. 确保项目已设置为显示详细的 LLEXT 调试输出（已设置 :kconfig:option:`CONFIG_LOG` 和 :kconfig:option:`CONFIG_LLEXT_LOG_LEVEL_DBG` ）。

2. 构建 Zephyr 应用程序和扩展。

   对于当前构建中包含的每个目标 ``name`` ，将在构建根目录的 ``llext`` 子目录中生成两个文件：

   ``name_ext_debug.elf``

        一个包含完整调试信息的中间 ELF 文件。

   ``name.llext``

        最终的扩展二进制文件，已裁剪为加载到 Zephyr 应用程序所需的基本数据。

   根据目标架构和构建配置的不同，可能还存在其他文件。

3. 启动主 Zephyr 应用程序的调试会话。文档的 :ref:`调试 <west-debugging>` 一节对此进行了说明；在支持的开发板上，只需运行 ``west debug`` 即可，可能还需要一些额外参数。

4. 在代码中 :c:func:`llext_load` 函数刚执行完的位置设置断点，然后让它继续运行。这会将扩展加载到内存并进行重定位。输出日志中将包含一行 ``gdb add-symbol-file flags:`` ，其后是全部以 ``-s`` 开头的行。

5. 在 GDB 控制台中输入以下命令，以加载此扩展的符号：

   .. code-block::

      add-symbol-file <path-to-debug.elf> <load-addresses>

   其中 ``<path-to-debug.elf>`` 是第 2 步中确定的带调试信息的 ELF 文件的完整路径， ``<load-addresses>`` 是上一步从日志中收集的所有 ``-s`` 行以空格分隔的列表。

6. 现在调试器可以使用扩展符号了。您可以像往常一样设置断点、检查变量并单步执行代码。

如果应用程序加载了多个扩展，可以对每个扩展重复步骤 4-6。

符号查找问题
============

.. warning::

   几乎可以肯定，加载的符号会被主应用程序中的其他符号遮蔽；例如，它们可能位于 ELF 缓冲区或 LLEXT 堆的内存区域内。

   在这种情况下，GDB 会选择第一个已知符号，因此会将这些地址关联到某个 ``elf_buffer+0x123`` ，而不是预期的 ``ext_fn`` 。这会进一步扰乱其高层操作，例如源码单步执行或检查局部变量，因为这些操作在该上下文中没有意义。

以下段落讨论了这个问题的两种可能解决方案。

丢弃所有 Zephyr 符号
--------------------

最简单的选择是在第 5 步之前，通过不带参数调用 ``add-symbol-file`` 从 GDB 中删除所有 Zephyr 应用程序符号。不过，这会使调试会话只关注 llext，因为有关 Zephyr 应用程序的所有信息都将丢失。例如，调试器可能无法正确跟踪扩展代码之外的栈回溯。

可以在同一会话中多次使用该技术，根据需要切换主符号表和扩展符号表，但这很快就会变得繁琐。

编辑 ELF 文件
-------------

这种替代方案更复杂，但可以实现更无缝的调试体验。其思路是编辑主 Zephyr ELF 文件，删除与要调试扩展重叠的符号信息，这样在加载扩展符号时，GDB 就不会有任何歧义。可以使用 ``objcopy`` 及 ``-N <symbol>`` 选项来完成。

然而，识别有问题的符号是一个反复试验的过程，因为可能存在许多不同的层次；例如，ELF 缓冲区本身可能包含在数据段的某个符号中。幸运的是，这些知识随后可以多次使用，因为对于给定项目，该列表不太可能发生变化。

调试会话示例
============

本示例演示如何在基于 ARM Cortex-M3 的模拟 ``mps2/an385`` 开发板上调试 ``tests/subsys/llext`` 项目中的 ``detached_fn`` 扩展（具体为 ``writable`` 用例）。

.. note::

   以下日志使用 Zephyr 4.1 版和 Zephyr SDK 0.17.0 版获取。不过，即使使用相同的版本，确切的地址在不同运行之间仍可能有所不同。请调整以下命令，以匹配您自己的会话结果。

以下命令将构建项目并以调试模式启动模拟器：

.. code-block::
   :caption: 终端 1（构建、QEMU 模拟器、GDB 服务器）

   zephyr$ west build -p -b mps2/an385 tests/subsys/llext/ -T llext.writable -t debugserver_qemu
   -- west build: generating a build system
   [...]
   -- west build: running target debugserver_qemu
   [...]
   [186/187] To exit from QEMU enter: 'CTRL+a, x'[QEMU] CPU: cortex-m3

在另一个终端中，将 ``ZEPHYR_SDK_INSTALL_DIR`` 设置为您的安装中 Zephyr SDK 所在的目录，然后为目标启动 GDB 客户端：

.. code-block::
   :caption: 终端 2（GDB 客户端）

   zephyr$ export LLEXT_SDK_INSTALL_DIR=/opt/zephyr-sdk-0.17.0
   zephyr$ ${LLEXT_SDK_INSTALL_DIR}/arm-zephyr-eabi/bin/arm-zephyr-eabi-gdb build/zephyr/zephyr.elf
   GNU gdb (Zephyr SDK 0.17.0) 12.1
   [...]
   Reading symbols from build/zephyr/zephyr.elf...
   (gdb)

连接后，在 ``llext_load`` 函数上设置断点并运行，直到该函数结束：

.. code-block::
   :caption: Terminal 2 (GDB client)

   (gdb) target extended-remote :1234
   Remote debugging using :1234
   z_arm_reset () at zephyr/arch/arm/core/cortex_m/reset.S:124
   124         movs.n r0, #_EXC_IRQ_DEFAULT_PRIO
   (gdb) break llext_load
   Breakpoint 1 at 0x236c: file zephyr/subsys/llext/llext.c, line 168.
   (gdb) continue
   Continuing.

   Breakpoint 1, llext_load (ldr=ldr@entry=0x2000bef0 <ztest_thread_stack+3488>,
                             name=name@entry=0x9d98 "test_detached",
                             ext=ext@entry=0x2000abb8 <detached_llext>,
                             ldr_parm=ldr_parm@entry=0x2000bee8 <ztest_thread_stack+3480>)
                 at zephyr/subsys/llext/llext.c:168
   168             *ext = llext_by_name(name);
   (gdb) finish
   Run till exit from #0  llext_load ([...])
       at zephyr/subsys/llext/llext.c:168
   llext_test_detached () at zephyr/tests/subsys/llext/src/test_llext.c:481
   481             zassert_ok(res, "load should succeed");

第一个终端将打印大量与扩展加载相关的调试信息。找到包含地址的部分：

.. code-block::
   :caption: Terminal 1 (build, QEMU emulator, GDB server)

   [...]
   D: Allocate and copy regions...
   [...]
   D: gdb add-symbol-file flags:
   D: -s .text 0x20000034
   D: -s .data 0x200000b4
   D: -s .bss 0x2000c2e0
   D: -s .rodata 0x200000b8
   D: -s .detach 0x200001d0
   D: Counting exported symbols...
   [...]

使用这些地址将符号加载到 GDB 中：

.. code-block::
   :caption: Terminal 2 (GDB client)

   (gdb) add-symbol-file build/llext/detached_fn_ext_debug.elf -s .text 0x20000034 -s .data 0x200000b4 -s .bss 0x2000c2e0 -s .rodata 0x200000b8 -s .detach 0x200001d0
   add symbol table from file "build/llext/detached_fn_ext_debug.elf" at
           .text_addr = 0x20000034
           .data_addr = 0x200000b4
           .bss_addr = 0x2000c2e0
           .rodata_addr = 0x200000b8
           .detach_addr = 0x200001d0
   (y or n) y
   Reading symbols from build/llext/detached_fn_ext_debug.elf...
   (gdb) break detached_entry
   Breakpoint 2 at 0x200001d0 (2 locations)
   (gdb) continue
   Continuing.

   Breakpoint 2, 0x200001d0 in test_detached_ext ()
   (gdb) backtrace
   #0  0x200001d0 in test_detached_ext ()
   #1  0x200000ac in test_detached_ext ()
   #2  0x00000706 in llext_test_detached () at zephyr/tests/subsys/llext/src/test_llext.c:496
   #3  0x00001a36 in run_test_functions (suite=0x92bc <z_ztest_test_node_llext>, data=0x0 <cbvprintf_package>, test=0x92d8 <z_ztest_unit_test.llext.test_detached>) at zephyr/subsys/testsuite/ztest/src/ztest.c:328
   #4  test_cb (a=0x92bc <z_ztest_test_node_llext>, b=0x92d8 <z_ztest_unit_test.llext.test_detached>, c=0x0 <cbvprintf_package>) at zephyr/subsys/testsuite/ztest/src/ztest.c:662
   #5  0x00000e96 in z_thread_entry (entry=0x1a05 <test_cb>, p1=0x92bc <z_ztest_test_node_llext>, p2=0x92d8 <z_ztest_unit_test.llext.test_detached>, p3=0x0 <cbvprintf_package>) at zephyr/lib/os/thread_entry.c:48
   #6  0x00000000 in ?? ()

与断点位置和最后几个栈帧关联的符号错误地引用了 Zephyr 应用程序中的 ELF 缓冲区，而不是扩展符号。请注意，GDB 其实知道两者：

.. code-block::
   :caption: Terminal 2 (GDB client)

   (gdb) info sym 0x200001d0
   test_detached_ext + 464 in section datas of zephyr/build/zephyr/zephyr.elf
   detached_entry in section .detach of zephyr/build/llext/detached_fn_ext_debug.elf
   (gdb) info sym 0x200000ac
   test_detached_ext + 172 in section datas of zephyr/build/zephyr/zephyr.elf
   test_entry + 8 in section .text of zephyr/build/llext/detached_fn_ext_debug.elf

同样无法正确检查扩展中的变量或单步执行代码：

.. code-block::
   :caption: Terminal 2 (GDB client)

   (gdb) print bss_cnt
   No symbol "bss_cnt" in current context.
   (gdb) print data_cnt
   No symbol "data_cnt" in current context.
   (gdb) next
   Single stepping until exit from function test_detached_ext,
   which has no line number information.

   Breakpoint 2, 0x200001ea in test_detached_ext ()
   (gdb)

丢弃符号
--------

丢弃 Zephyr 符号并仅关注扩展可以恢复完整的调试功能，但代价是丢失全局上下文（请注意，栈回溯会在扩展之外停止）：

.. code-block::
   :caption: Terminal 2 (GDB client)

   (gdb) symbol-file
   Discard symbol table from `zephyr/build/zephyr/zephyr.elf'? (y or n) y
   Error in re-setting breakpoint 1: No symbol table is loaded.  Use the "file" command.
   No symbol file now.
   (gdb) add-symbol-file build/llext/detached_fn_ext_debug.elf -s .text 0x20000034 -s .data 0x200000b4 -s .bss 0x2000c2e0 -s .rodata 0x200000b8 -s .detach 0x200001d0
   add symbol table from file "build/llext/detached_fn_ext_debug.elf" at
           .text_addr = 0x20000034
           .data_addr = 0x200000b4
           .bss_addr = 0x2000c2e0
           .rodata_addr = 0x200000b8
           .detach_addr = 0x200001d0
   (y or n) y
   Reading symbols from build/llext/detached_fn_ext_debug.elf...
   (gdb) backtrace
   #0  detached_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:18
   #1  0x200000ac in test_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:26
   #2  0x00000706 in ?? ()
   Backtrace stopped: previous frame identical to this frame (corrupt stack?)
   (gdb) next
   19              zassert_true(data_cnt < 0);
   (gdb) print bss_cnt
   $1 = 1
   (gdb) print data_cnt
   $2 = -2
   (gdb)


编辑 ELF 文件
-------------

在这种替代方法中，对 Zephyr ELF 文件的修改必须在构建 Zephyr 二进制文件并在终端 1 上启动模拟器之后、在终端 2 上启动 GDB 客户端之前进行。

上述调试会话已将保存 ELF 文件的字符数组 ``test_detached_ext`` 识别为有问题的符号，因此将在第一轮中删除它。多次执行相同步骤后，还可以发现 ``__data_start`` 和 ``__data_region_start`` 与目标内存区域重叠。

以下命令将从 Zephyr ELF 文件中删除所有这些符号，然后在修改后的文件上启动调试会话：

.. code-block::
   :caption: Terminal 2 (GDB client)

   zephyr$ export LLEXT_SDK_INSTALL_DIR=/opt/zephyr-sdk-0.17.0
   zephyr$ ${LLEXT_SDK_INSTALL_DIR}/arm-zephyr-eabi/bin/arm-zephyr-eabi-objcopy -N test_detached_ext -N __data_start -N __data_region_start build/zephyr/zephyr.elf build/zephyr/zephyr-edit.elf
   zephyr$ ${LLEXT_SDK_INSTALL_DIR}/arm-zephyr-eabi/bin/arm-zephyr-eabi-gdb build/zephyr/zephyr-edit.elf
   GNU gdb (Zephyr SDK 0.17.0) 12.1
   [...]
   Reading symbols from build/zephyr/zephyr-edit.elf...
   (gdb)

可以再次执行上一次运行中使用的相同步骤，以连接到 GDB 服务器并加载扩展及其调试符号。不过，这次的结果大不相同：

 * ``break`` 命令包含行号信息；

 * ``backtrace`` 的输出包含来自扩展和 Zephyr 应用程序的函数；

 * 可以正确检查局部变量。

.. code-block::
   :caption: Terminal 2 (GDB client)

   (gdb) add-symbol-file build/llext/detached_fn_ext_debug.elf [...]
   [...]
   Reading symbols from build/llext/detached_fn_ext_debug.elf...
   (gdb) break detached_entry
   Breakpoint 2 at 0x200001d6: file zephyr/tests/subsys/llext/src/detached_fn_ext.c, line 17.
   (gdb) continue
   Continuing.

   Breakpoint 2, detached_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:17
   17              printk("bss %u @ %p\n", bss_cnt++, &bss_cnt);
   (gdb) backtrace
   #0  detached_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:17
   #1  0x200000ac in test_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:26
   #2  0x00000706 in llext_test_detached () at zephyr/tests/subsys/llext/src/test_llext.c:496
   #3  0x00001a36 in run_test_functions (suite=0x92bc <z_ztest_test_node_llext>, data=0x0 <cbvprintf_package>, test=0x92d8 <z_ztest_unit_test.llext.test_detached>) at zephyr/subsys/testsuite/ztest/src/ztest.c:328
   #4  test_cb (a=0x92bc <z_ztest_test_node_llext>, b=0x92d8 <z_ztest_unit_test.llext.test_detached>, c=0x0 <cbvprintf_package>) at zephyr/subsys/testsuite/ztest/src/ztest.c:662
   #5  0x00000e96 in z_thread_entry (entry=0x1a05 <test_cb>, p1=0x92bc <z_ztest_test_node_llext>, p2=0x92d8 <z_ztest_unit_test.llext.test_detached>, p3=0x0 <cbvprintf_package>) at zephyr/lib/os/thread_entry.c:48
   #6  0x00000000 in ?? ()
   (gdb) print bss_cnt
   $1 = 0
   (gdb) print data_cnt
   $2 = -3
   (gdb)
