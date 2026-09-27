.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _fatal:

致命错误
########

在源代码中触发的软件错误
************************

Zephyr 提供多种方法，可通过构建时检查、条件编译的断言，或显式调用 panic 或 oops 来触发致命错误。

运行时断言
==========

Zephyr 提供了一些可通过条件编译启用的运行时断言宏，其定义位于 :zephyr_file:`include/zephyr/sys/__assert.h`。

将预处理符号 ``__ASSERT_ON`` 设置为非零值即可启用断言。有以下两种方法：

- 使用 :kconfig:option:`CONFIG_ASSERT` 和 :kconfig:option:`CONFIG_ASSERT_LEVEL` Kconfig 选项。
- 在构建命令行或 CMakeLists.txt 中，将 ``-D__ASSERT_ON=<level>`` 添加到项目的 CFLAGS。

若同时使用两种方法，``__ASSERT_ON`` 的优先级高于 Kconfig 选项。

将断言级别设为 1 时，编译器会警告内核包含调试用的 ``__ASSERT()`` 语句；之所以发出提醒，是因为最终产品中通常不应存在断言代码。将断言级别设为 2 则会抑制这些警告。

运行 Zephyr 测试用例时，默认根据 :kconfig:option:`CONFIG_TEST` 选项启用断言。

断言失败后的处理策略由 :c:func:`assert_post_action` 的实现决定。Zephyr 提供一个弱链接的默认实现：如果断言失败的线程运行在用户模式，则触发内核 oops；否则触发内核 panic。

__ASSERT()
----------

内核和应用代码可使用 ``__ASSERT()`` 宏执行可选的运行时检查；检查不通过时将触发致命错误。该宏接受一条字符串消息，打印它以提供断言的上下文信息。此外，内核还会打印所求值表达式的代码文本，以及断言所在的文件和行号。

例如：

.. code-block:: c

  __ASSERT(foo == 0xF0CACC1A, "Invalid value of foo, got 0x%x", foo);

如果运行时 ``foo`` 的值不符合预期，产生的错误可能如下所示：

.. code-block:: none

        ASSERTION FAIL [foo == 0xF0CACC1A] @ ZEPHYR_BASE/tests/kernel/fatal/src/main.c:367
                Invalid value of foo, got 0xdeadbeef
        [00:00:00.000,000] <err> os: r0/a1:  0x00000004  r1/a2:  0x0000016f  r2/a3:  0x00000000
        [00:00:00.000,000] <err> os: r3/a4:  0x00000000 r12/ip:  0x00000000 r14/lr:  0x00000a6d
        [00:00:00.000,000] <err> os:  xpsr:  0x61000000
        [00:00:00.000,000] <err> os: Faulting instruction address (r15/pc): 0x00009fe4
        [00:00:00.000,000] <err> os: >>> ZEPHYR FATAL ERROR 4: Kernel panic
        [00:00:00.000,000] <err> os: Current thread: 0x20000414 (main)
        [00:00:00.000,000] <err> os: Halting system

__ASSERT_EVAL()
---------------

``__ASSERT_EVAL()`` 宏也可用于内核和应用代码，它对参数求值具有特殊语义。

它使用 ``__ASSERT()`` 宏，但更加灵活，允许开发者根据是否启用 ``__ASSERT()`` 宏来指定不同操作。这尤其适合解决以下情况：某变量仅在 ``__ASSERT()`` 中使用，禁用 ``__ASSERT()`` 宏后变量虽被赋值却不再使用，从而导致编译器产生诊断信息（错误、警告或提示）。

考虑以下示例：

.. code-block:: c

  int x;
  x = foo();
  __ASSERT(x != 0, "foo() returned zero!");

如果禁用 ``__ASSERT()``，则 'x' 被赋值却从未使用。这类情况可通过 __ASSERT_EVAL() 宏解决。

.. code-block:: c

  __ASSERT_EVAL ((void) foo(),
                 int x = foo(),
                 x != 0,
                 "foo() returned zero!");

第一个参数告诉 ``__ASSERT_EVAL()`` 在禁用 ``__ASSERT()`` 时应执行什么操作。第二个参数告诉 ``__ASSERT_EVAL()`` 在启用 ``__ASSERT()`` 时应执行什么操作。第三、第四个参数则传递给 ``__ASSERT()``。

__ASSERT_NO_MSG()
-----------------

``__ASSERT_NO_MSG()`` 宏可执行断言并报告失败的检查及其位置，但不提供帮助用户诊断问题的额外调试信息，因此不建议使用。

自定义头文件
============

某些情况下需要在宏层面重定向断言。此时可使用 :kconfig:option:`CONFIG_ASSERT_CUSTOM_HEADER`，在 :zephyr_file:`include/zephyr/sys/__assert.h` 末尾引入由应用提供的 ``zephyr_custom_assert.h`` 头文件。

构建时断言
==========

Zephyr 提供了执行构建时断言检查的宏。该宏完全在编译时求值，且始终进行检查。

BUILD_ASSERT()
--------------

该宏与 C 的 ``_Static_assert`` 或 C++ 的 ``static_assert`` 语义相同。如果求值失败，编译器将生成构建错误。如果编译器支持，还会打印提供的消息以补充上下文。

与 ``__ASSERT()`` 不同，这里的消息必须是静态字符串，不能包含类似 :c:func:`printf()` 的格式说明符或额外参数。

例如，假设以下检查失败：

.. code-block:: c

        BUILD_ASSERT(FOO == 2000, "Invalid value of FOO");

使用 GCC 时，输出类似于：

.. code-block:: none

        tests/kernel/fatal/src/main.c: In function 'test_main':
        include/zephyr/toolchain/gcc.h:28:37: error: static assertion failed: "Invalid value of FOO"
         #define BUILD_ASSERT(EXPR, MSG) _Static_assert(EXPR, "" MSG)
                                         ^~~~~~~~~~~~~~
        tests/kernel/fatal/src/main.c:370:2: note: in expansion of macro 'BUILD_ASSERT'
          BUILD_ASSERT(FOO == 2000,
          ^~~~~~~~~~~~~~~~

内核 Oops
=========

内核 oops 是通过 :c:func:`k_oops()` 触发的软件致命错误，应当用于指示应用逻辑中不可恢复的状况。

生成的致命错误原因代码为 ``K_ERR_KERNEL_OOPS``。

内核 Panic
==========

内核 panic 是通过 :c:func:`k_panic()` 触发的软件致命错误，应当用于指示 Zephyr 内核处于不可恢复的状态。内核发生 panic 时，:c:func:`k_sys_fatal_error_handler()` 的实现不应返回，因为整个系统需要复位。

在用户模式下运行的线程不允许调用 :c:func:`k_panic()`，这样做会改为触发内核 oops。其他情况下，生成的致命错误原因代码为 ``K_ERR_KERNEL_PANIC``。

异常
****

伪中断
======

如果 CPU 收到硬件中断，而对应中断线尚未通过 ``IRQ_CONNECT()`` 或 :c:func:`irq_connect_dynamic()` 安装处理程序，内核就会生成致命错误，原因代码为 ``K_ERR_SPURIOUS_IRQ()``。

栈溢出
======

如果线程压入执行栈的数据量超过栈缓冲区容量，内核可能能够检测到这一情况，并生成原因代码为 ``K_ERR_STACK_CHK_FAIL`` 的致命错误。

如果线程运行在用户模式，栈溢出始终会被捕获，因为线程没有权限写入栈缓冲区之外的相邻内存地址。此限制由内存保护硬件强制执行，因此不会破坏线程原本就无权写入的内存中的数据。

如果线程运行在特权模式，或者未启用 :kconfig:option:`CONFIG_USERSPACE`，能否捕获栈溢出取决于配置。某些架构支持 :kconfig:option:`CONFIG_HW_STACK_PROTECTION`，可捕获特权模式下的栈溢出，包括代表用户线程处理系统调用时发生的溢出。通常这通过专用 CPU 功能，或紧邻栈缓冲区放置的只读 MMU/MPU 保护区实现。这种方式能够检测到栈溢出，但不能保证数据不受破坏，应将此视为影响整个系统运行的严重问题。

如果平台缺少内存管理硬件支持，可使用 :kconfig:option:`CONFIG_STACK_SENTINEL` 提供的纯软件栈溢出检测功能。它定期检查栈缓冲区末尾的哨兵值是否已被破坏。此功能不需要硬件支持，但无法防止数据损坏。由于检查通常在中断退出时进行，实际发生栈溢出后，可能过了相当一段时间才会被检测到。

最后，Zephyr 通过 :kconfig:option:`CONFIG_STACK_CANARIES` 支持 GCC 编译器的栈金丝雀机制。启用后，编译器在函数栈帧中插入启动时随机生成的金丝雀值，并在函数退出时检查它是否被覆盖。如果检查失败，编译器调用 :c:func:`__stack_chk_fail()`，其 Zephyr 实现会触发致命的栈溢出错误。这里的错误并不表示整个栈缓冲区已溢出，而是表示当前函数的栈帧已被破坏。更多详情请参见编译器文档。

默认情况下，所有线程共享一个启动时生成的金丝雀值。启用 :kconfig:option:`CONFIG_STACK_CANARIES_TLS` 后，金丝雀值改为存放在 :ref:`线程局部存储 <thread_local_storage>` 中，让每个线程拥有独立的值。这使金丝雀的位置和值更难预测，代价是增加每个线程的初始化工作。

作为补充加固措施，:kconfig:option:`CONFIG_STACK_POINTER_RANDOM` 在线程创建时为其初始栈指针添加随机偏移。这是一种有限的地址空间布局随机化措施，使任意给定栈帧的位置不再确定，从而阻碍某些类型的安全攻击；代价是每个线程的栈区域最多会额外消耗配置指定的字节数。

其他异常
========

其他任何类型的未处理 CPU 异常都会生成错误代码 ``K_ERR_CPU_EXCEPTION``。

致命错误处理
************

发生致命错误时的处理策略由 :c:func:`k_sys_fatal_error_handler()` 函数的实现决定。该函数有一个弱链接的默认实现：调用 ``LOG_PANIC()`` 输出所有待处理的日志消息，然后使用 :c:func:`k_fatal_halt()` 无条件停止系统。

应用可以覆盖 :c:func:`k_sys_fatal_error_handler()` 的实现，制定自己的错误处理策略。如果该实现返回，出错线程将被终止，系统的其他部分则继续运行。更多细节和约束请参见该函数的文档。

API 参考
********

.. doxygengroup:: fatal_apis
