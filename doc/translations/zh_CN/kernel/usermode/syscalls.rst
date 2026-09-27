.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _syscalls:

系统调用
########
用户线程的特权少于特权线程：某些 CPU 指令不可使用，且只能访问内存映射中的有限部分。系统调用可以让用户线程执行原本无法直接执行的操作。

定义系统调用时，务必确保只能通过系统调用接口访问 API 的私有数据。绝不能让用户模式线程直接访问内核私有数据。例如，``k_queue`` API 特意未向用户模式开放，因为它们将队列管理信息直接存储在用户模式可见的队列缓冲区中。

允许用户注册在特权模式下运行的回调函数的 API，绝不能作为系统调用开放。这些 API 只能供特权模式访问。

本节介绍如何声明新的系统调用，并讨论一些相关实现细节。

组成部分
********

所有系统调用都包含以下组成部分：

* API 的 **C 函数原型**，以 :c:macro:`__syscall` 为前缀，声明在 ``include/`` 下或其他 ``SYSCALL_INCLUDE_DIRS`` 目录中的头文件内。此原型的实现无需手动编写，而由 :ref:`gen_syscalls.py` 脚本创建。生成的是一个内联函数：从特权模式调用时直接调用实现函数，从用户模式调用时则经过特权提升和验证步骤。

* **实现函数**，即系统调用的实际实现。如果从用户模式调用，实现函数可以假定所有传入参数都已验证。

* **验证函数**，封装实现函数并验证所有传入参数。

* **解组函数**，自动生成的处理函数，必须由用户源代码包含。

C 函数原型
**********

C 函数原型表示从用户模式或特权模式调用 API 的方式。例如，初始化信号量：

.. code-block:: c

    __syscall void k_sem_init(struct k_sem *sem, unsigned int initial_count,
                              unsigned int limit);

:c:macro:`__syscall` 属性非常特殊。对 C 编译器而言，它只是展开为 static inline；而对构建后脚本 :ref:`parse_syscalls.py` 而言，它表示此 API 是系统调用。:ref:`parse_syscalls.py` 脚本会解析函数原型，以确定返回值和参数的数据类型，但存在一些限制：

* 数组参数必须以指针形式传入，不能使用数组形式。例如，不允许 ``int foo[]`` 或 ``int foo[12]``，而应写成 ``int *foo``。

* 功能有限的解析器无法正确处理函数指针。解决方法是先使用 typedef 定义其类型，再在参数列表中使用该类型。

* :c:macro:`__syscall` 必须放在原型的最前面。

确定要生成的系统调用集合时，特意不使用预处理器。但对于实际未定义验证函数的已生成系统调用（因为内核配置未启用相关功能），会改为指向用于未实现系统调用的特殊验证函数。API 的数据类型定义不应对编译器采用条件可见性。

任何声明系统调用的头文件，都必须在文件最底部包含一个特殊的生成头文件。其命名约定为 ``syscalls/<name of header file>``。例如，在 :zephyr_file:`include/zephyr/drivers/sensor.h` 底部：

.. code-block:: c

    #include <zephyr/syscalls/sensor.h>

C 函数原型必须声明在 CMake 变量 ``SYSCALL_INCLUDE_DIRS`` 所列的某个目录中。设置 ``CONFIG_APPLICATION_DEFINED_SYSCALL`` 时，该列表始终包含 ``APPLICATION_SOURCE_DIR``；设置 ``CONFIG_ZTEST`` 时，则包含 ``${ZEPHYR_BASE}/subsys/testsuite/ztest/include``。可通过 CMake 命令行，或在 ``find_package(Zephyr ...)`` 之前执行的 CMake 代码，向列表添加其他路径。``${ZEPHYR_BASE}/include`` 始终会被扫描以查找可能的系统调用原型。

注意，并非所有系统调用都会包含在最终二进制文件中。CMake 函数 ``zephyr_syscall_header`` 和 ``zephyr_syscall_header_ifdef`` 用于指定包含系统调用原型的头文件，确保这些系统调用出现在最终二进制文件中。CMake 变量 ``SYSCALL_INCLUDE_DIRS`` 所列目录中的头文件，其系统调用始终会包含在最终二进制文件中。若要强制包含所有系统调用，请启用 :kconfig:option:`CONFIG_EMIT_ALL_SYSCALLS`。

调用上下文
==========

如果已知某个 C 文件内的全部代码只在用户模式或只在特权模式下运行，就可以提高使用系统调用 API 的源代码的效率。系统会检查宏 :c:macro:`__ZEPHYR_SUPERVISOR__` 或 :c:macro:`__ZEPHYR_USER__` 是否定义；通常在构建系统中将这些宏加入相关文件的编译器标志。

* 如果未启用 :kconfig:option:`CONFIG_USERSPACE`，所有 API 都直接调用实现函数。

* 否则，默认会在运行时检查处理器当前是否处于用户模式，并根据情况执行系统调用或直接调用实现函数。

* 如果定义了 :c:macro:`__ZEPHYR_SUPERVISOR__`，则假定全部代码都在特权模式下运行，所有 API 都直接调用实现函数。如果代码实际上在用户模式下运行，一旦尝试执行未获允许的操作，就会产生 CPU 异常。

* 如果定义了 :c:macro:`__ZEPHYR_USER__`，则假定全部代码都在用户模式下运行，并无条件执行系统调用。

实现细节
========

使用 :c:macro:`__syscall` 声明 API 后，:ref:`gen_syscalls.py` 脚本会在 C 文件和头文件中生成一些代码，均可在项目输出目录的 ``include/generated/`` 下找到：

* 系统调用会被加入系统调用 ID 的枚举类型，定义于 ``include/generated/zephyr/syscall_list.h``。其名称为大写 API 名称，前缀为 ``K_SYSCALL_``。

* 在分发表 ``_k_syscall_table`` 中为系统调用创建一个条目，该表定义于 ``include/generated/zephyr/syscall_dispatch.c``。

  * 启用 :kconfig:option:`CONFIG_EMIT_ALL_SYSCALLS` 时，该表仅包含原型声明在以下头文件中的系统调用：

    * 由 CMake 函数 ``zephyr_syscall_header`` 和 ``zephyr_syscall_header_ifdef`` 指定的头文件，或

    * 位于 CMake 变量 ``SYSCALL_INCLUDE_DIRS`` 指定目录中的头文件。

* 声明一个弱符号验证函数，它只是“未实现系统调用”验证函数的别名。由于真正的验证函数是否参与构建取决于内核配置，因此必须这样做。例如，用户线程调用传感器子系统 API，但传感器子系统未启用时，将改为调用该弱符号验证函数。

* 解组函数定义在 ``include/generated/zephyr/syscalls/<name>_mrsh.c`` 中。

在生成的系统头文件中创建 API 函数体。以 :c:func:`k_sem_init()` 为例，该 API 声明于 :zephyr_file:`include/zephyr/kernel.h`。:zephyr_file:`include/zephyr/kernel.h` 底部包含::

    #include <zephyr/syscalls/kernel.h>

该头文件内包含 :c:func:`k_sem_init()` 的函数体::

    static inline void k_sem_init(struct k_sem * sem, unsigned int initial_count, unsigned int limit)
    {
    #ifdef CONFIG_USERSPACE
            if (z_syscall_trap()) {
                    arch_syscall_invoke3(*(uintptr_t *)&sem, *(uintptr_t *)&initial_count, *(uintptr_t *)&limit, K_SYSCALL_K_SEM_INIT);
                    return;
            }
            compiler_barrier();
    #endif
            z_impl_k_sem_init(sem, initial_count, limit);
    }

这会生成一个接受三个参数、返回类型为 void 的内联函数。根据上下文，它会直接调用实现函数，或通过系统调用提升特权。实现函数的原型也会自动生成。

最后一层是系统调用本身的执行。所有实现系统调用的架构都必须实现从 :c:func:`_arch_syscall_invoke0` 到 :c:func:`_arch_syscall_invoke6` 的七个内联函数。它们将参数编组到指定 CPU 寄存器中，并执行必要的特权提升。API 内联函数的参数在作为系统调用参数传入前，会通过 C 类型转换转为与寄存器大小一致的 ``uintptr_t``。例外是在 32 位系统上传递 64 位参数：此时会将其拆分为低位和高位两部分，作为两个连续参数传递。返回值始终为 ``uintptr_t`` 类型，不需要时可以忽略。

.. figure:: syscall_flow.png
   :alt: System Call execution flow
   :width: 80%
   :align: center

   系统调用执行流程

有些系统调用的参数可能超过六个，但所有架构通过寄存器传递的参数都最多为六个。额外参数需要通过源内存空间中的数组传递，验证函数必须将其视为不可信内存。上述桩函数和解组函数中的相关代码（打包、解包和验证）会按需自动生成。

系统调用返回 ``uintptr_t`` 类型的值，再由包装函数通过 C 类型转换转为 API 原型声明的返回类型。这意味着在 32 位系统上，系统调用不能直接向包装函数返回 64 位值。为解决这一问题，自动生成的包装函数会在自身栈上定义一个被视为 **不可信** 缓冲区的 64 位中间变量，并将指向该变量的指针作为最后一个参数传给系统调用。系统调用返回后，包装函数返回写入该缓冲区的值。64 位系统能够直接返回 64 位值，因此不存在这一问题。

实现函数
********

实现函数实际完成 API 的工作。Zephyr 通常很少或完全不检查参数错误，或者通过断言检查。编写实现函数时，参数验证是可选的，且应使用断言完成。

所有实现函数都必须遵循命名约定，即在 API 名称前加上 ``z_impl_``。实现函数可以作为静态内联函数声明在与 API 相同的头文件中，也可以声明在某个 C 文件中。无需为实现函数编写原型，它们会自动生成。

验证函数
********

用户线程执行系统调用时，验证函数在内核侧运行。用户线程通过软件中断提升到特权模式后，通用系统调用入口点使用用户提供的系统调用 ID 查找对应的解组函数并跳转执行。解组函数随后调用验证函数。

只有从用户模式调用系统调用 API 时，才会运行验证函数和解组函数。如果从特权模式调用 API，则直接调用实现函数，不会发生软件陷入。

验证函数用于验证所有传入参数，包括：

* 提供的所有内核对象指针。例如，信号量 API 必须确保传入的信号量对象有效，且调用线程拥有该对象的权限。

* 用户模式传入的所有内存缓冲区。必须检查调用线程是否具有对所提供缓冲区的读或写权限。

* 有效值范围受限的其他参数。

验证函数涉及大量重复代码，:zephyr_file:`include/zephyr/internal/syscall_handler.h` 中的一些宏简化了这些代码。应使用这些宏声明验证函数。

参数验证
========

以下宏可用于验证参数：

* :c:macro:`K_SYSCALL_OBJ()` 检查内存地址，确保它是所需类型的有效内核对象、调用线程拥有其权限，且该对象已初始化。

* :c:macro:`K_SYSCALL_OBJ_INIT()` 与 :c:macro:`K_SYSCALL_OBJ()` 相同，但允许所提供的对象尚未初始化。这适用于对象初始化函数的验证函数。

* :c:macro:`K_SYSCALL_OBJ_NEVER_INIT()` 与 :c:macro:`K_SYSCALL_OBJ()` 相同，但要求所提供的对象尚未初始化。它不常使用，目前仅用于 :c:func:`k_thread_create()`。

* :c:macro:`K_SYSCALL_MEMORY_READ()` 验证指定大小的内存缓冲区，要求调用线程具有对整个缓冲区的读权限。

* :c:macro:`K_SYSCALL_MEMORY_WRITE()` 与 :c:macro:`K_SYSCALL_MEMORY_READ()` 相同，但还要求调用线程具有写权限。

* :c:macro:`K_SYSCALL_MEMORY_ARRAY_READ()` 验证数组，其总大小由分别表示元素数量和元素大小的参数给出。该宏计算总大小时会正确处理乘法溢出。调用线程必须具有对整个范围的读权限。

* :c:macro:`K_SYSCALL_MEMORY_ARRAY_WRITE()` 与 :c:macro:`K_SYSCALL_MEMORY_ARRAY_READ()` 相同，但还要求调用线程具有写权限。

* :c:macro:`K_SYSCALL_VERIFY_MSG()` 在运行时检查布尔表达式；表达式必须为真，否则检查失败。另有变体 :c:macro:`K_SYSCALL_VERIFY`，不接受消息参数，而在失败时打印被检查的表达式。后者应只用于含义最明显的检查。

* :c:macro:`K_SYSCALL_DRIVER_OP()` 在运行时检查驱动程序实例能否执行特定操作。虽然可以单独使用，但它主要用于构建为各驱动程序子系统自动生成的宏。例如，可以使用 :c:macro:`K_SYSCALL_DRIVER_GPIO()` 宏验证 GPIO 驱动程序。

* :c:macro:`K_SYSCALL_SPECIFIC_DRIVER()` 在运行时检查所提供的指针是否为特定设备驱动程序的有效实例、调用线程是否拥有其权限，以及该驱动程序是否已初始化。它通过检查驱动程序实例中存储的 API 结构体指针，确保其与提供的值相匹配；该值应为特定驱动程序 API 结构体的地址。

任何检查失败时，这些宏都会返回非零值。可以使用 :c:macro:`K_OOPS()` 宏触发内核 oops，从而终止调用线程。采用这种方式而不是返回错误，是为了使 API 与从特权模式调用时保持一致。

.. _syscall_verification:

验证函数定义
============

所有系统调用都会被分派到以系统调用名称加 ``z_vrfy_`` 前缀命名的验证函数。它们与所封装的系统调用具有完全相同的返回类型和参数类型，负责在验证所有参数后执行系统调用（通常通过调用实现函数）。

验证函数自身由自动生成的解组函数调用，后者负责解包架构层传来的寄存器参数，并转换为正确类型。解组函数定义在必须由用户代码包含的头文件中，通常放在翻译单元中验证函数定义之后，以便进行内联。

例如：

.. code-block:: c

    static int z_vrfy_k_sem_take(struct k_sem *sem, int32_t timeout)
    {
        K_OOPS(K_SYSCALL_OBJ(sem, K_OBJ_SEM));
        return z_impl_k_sem_take(sem, timeout);
    }
    #include <zephyr/syscalls/k_sem_take_mrsh.c>


验证时的内存访问策略
====================

以引用方式传给系统调用的参数需要特殊处理，因为任何能访问参数所指内存的用户线程，都可以随时修改这些参数的值。如果内核根据这些内存的内容作出逻辑判断，即使进行了检查，也可能遭到攻击。这类漏洞称为 TOCTOU（检查时与使用时之间的竞态）。

防范此类攻击的正确做法是在验证函数中创建副本，仅对用户线程永远无法访问的副本进行参数检查。传给实现函数的是副本，而非用户传入的原始数据。:c:func:`k_usermode_to_copy()` 和 :c:func:`k_usermode_from_copy()` API 就用于这一目的。

用户模式传入的 C 字符串也需要类似的处理，因为其长度事先未知，且必须在不越过调用者可访问内存的前提下找到终止字符 ``NUL``。:c:func:`k_usermode_string_copy()` 和 :c:func:`k_usermode_string_alloc_copy()` 辅助函数会安全地验证用户提供的字符串，并在实现函数使用之前将其复制到内核控制的内存中。

有一种例外：较大的数据缓冲区如果仅提供只写的内存区域，或者其内容从不用于任何验证或控制流，则可另行处理。本节稍后将进一步讨论。

首先考虑一个用来输出某个整数值的参数：


.. code-block:: c

    int z_vrfy_some_syscall(int *out_param)
    {
        int local_out_param;
        int ret;

        ret = z_impl_some_syscall(&local_out_param);
        K_OOPS(k_usermode_to_copy(out_param, &local_out_param, sizeof(*out_param)));
        return ret;
    }

这里在栈上分配了 ``local_out_param``，将其地址传给实现函数，然后使用 :c:func:`k_usermode_to_copy()` 填充调用者传入的内存。

更简洁的写法可能很有吸引力：

.. code-block:: c

    int z_vrfy_some_syscall(int *out_param)
    {
        K_OOPS(K_SYSCALL_MEMORY_WRITE(out_param, sizeof(*out_param)));
        return z_impl_some_syscall(out_param);
    }

但如果实现函数的逻辑会读取这块内存，这样做就不安全。例如，它可能用于存储计数器值，而能访问该内存的用户线程可以篡改该值。对于较小的整数值，采用第一个示例所示的复制方式最为安全。

有些参数既用于输入，也用于输出。例如，有些 API 会传入指向 ``size_t`` 的指针，其初值为允许的最大大小，随后由实现函数更新为实际处理的字节数。这种情况也应使用栈上副本：

.. code-block:: c

    int z_vrfy_in_out_syscall(size_t *size_ptr)
    {
        size_t size;
        int ret;

        K_OOPS(k_usermode_from_copy(&size, size_ptr, sizeof(size));
        ret = z_impl_in_out_syscall(&size);
        K_OOPS(k_usermode_to_copy(size_ptr, &size, sizeof(size)));
        return ret;
    }

许多系统调用会传入结构体，甚至链式数据结构。它们都应被复制，通常通过在栈上分配副本实现：

.. code-block:: c

    struct bar {
        ...
    };

    struct foo {
        ...
        struct bar *bar_left;
        struct bar *bar_right;
    };

    int z_vrfy_must_alloc(struct foo *foo)
    {
        int ret;
        struct foo foo_copy;
        struct bar bar_right_copy;
        struct bar bar_left_copy;

        K_OOPS(k_usermode_from_copy(&foo_copy, foo, sizeof(*foo)));
        K_OOPS(k_usermode_from_copy(&bar_right_copy, foo_copy.bar_right,
                                sizeof(struct bar)));
        foo_copy.bar_right = &bar_right_copy;
        K_OOPS(k_usermode_from_copy(&bar_left_copy, foo_copy.bar_left,
                                sizeof(struct bar)));
        foo_copy.bar_left = &bar_left_copy;

        return z_impl_must_alloc(&foo_copy);
    }

有时数据量在编译时未知，或太大而无法在栈上分配。这种情况下，可能需要通过 :c:func:`z_thread_malloc()` 从调用者的资源池分配内存，但始终应将其作为最后手段。功能安全编程指南强烈不建议使用堆，且必须明确记录使用了资源池。任何分配问题都必须通过返回 ``-ENOMEM`` 告知调用者。绝不能使用 ``K_OOPS()`` 检查资源分配是否成功。

.. code-block:: c

    struct bar {
        ...
    };

    struct foo {
        size_t count;
        struct bar *bar_list; /* array of struct bar of size count */
    };

    int z_vrfy_must_alloc(struct foo *foo)
    {
        int ret;
        struct foo foo_copy;
        struct bar *bar_list_copy;
        size_t bar_list_bytes;

        /* Safely copy foo into foo_copy */
        K_OOPS(k_usermode_from_copy(&foo_copy, foo, sizeof(*foo)));

        /* Bounds check the count member, in the copy we made */
        if (foo_copy.count > 32) {
            return -EINVAL;
        }

        /* Allocate RAM for the bar_list, replace the pointer in
         * foo_copy */
        bar_list_bytes = foo_copy.count * sizeof(struct_bar);
        bar_list_copy = z_thread_malloc(bar_list_bytes);
        if (bar_list_copy == NULL) {
            return -ENOMEM;
        }
        K_OOPS(k_usermode_from_copy(bar_list_copy, foo_copy.bar_list,
                                bar_list_bytes));
        foo_copy.bar_list = bar_list_copy;

        ret = z_impl_must_alloc(&foo_copy);

        /* All done with the memory, free it and return */
        k_free(foo_copy.bar_list_copy);
        return ret;
    }

最后需要考虑较大的数据缓冲区。它们表示用于复制出或复制入数据的用户内存区域，允许将其指针直接传给实现函数。但仍必须通过 ``K_SYSCALL_MEMORY`` API 验证调用者对缓冲区的访问权限，并满足以下约束：

 * 如果实现函数使用缓冲区写入数据，例如从某个 MMIO 区域采集的数据，则只能写入，绝不能读取这些数据。

 * 如果实现函数使用缓冲区读取数据，例如将一块内存写入某个硬件目标，则只能读取，不能进行处理。不能根据数据缓冲区内容执行条件逻辑；如果需要此类逻辑，就必须创建副本。

 * 缓冲区只能与调用同步使用。实现函数绝不能保存缓冲区地址并异步使用，例如在中断触发时使用。

.. code-block:: c

    int z_vrfy_get_data_from_kernel(void *buf, size_t size)
    {
        K_OOPS(K_SYSCALL_MEMORY_WRITE(buf, size));
        return z_impl_get_data_from_kernel(buf, size);
    }

验证返回值策略
==============

验证系统调用时，需要区分哪些验证失败应向调用者返回错误值，哪些应直接调用 :c:macro:`K_OOPS()` 终止调用线程。当前约定如下：

#. 对于已定义但未编译的系统调用，对它们的调用会被路由到 :c:func:`handler_no_syscall()`，进而调用 :c:macro:`K_OOPS()`。

#. ``K_SYSCALL_MEMORY`` 系列 API、:c:func:`k_usermode_from_copy()` 或 :c:func:`k_usermode_to_copy()` 发现的任何无效内存访问，都应触发 :c:macro:`K_OOPS`。调用者没有缓冲区的适当权限，或某些大小计算发生溢出时，会出现这种情况。

#. 大多数系统调用接受内核对象指针参数，使用 ``K_SYSCALL_OBJ`` 系列函数、``K_SYSCALL_DRIVER_nnnnn``，或手动调用 :c:func:`k_object_validate()` 检查。这些检查可能因多种原因失败：缺少驱动程序 API、内核对象指针无效、内核对象类型错误，或初始化状态不正确。这些问题始终应调用 :c:macro:`K_OOPS()`。

#. 任何因堆内存分配失败产生的错误（通常来自 :c:func:`z_thread_malloc()`），都应向调用者返回 ``-ENOMEM``。

#. 一般参数检查应在实现函数中进行，大多数情况下使用 ``CHECKIF()``。

   * ``CHECKIF()`` 的行为取决于内核配置，但启用用户模式时，会强制启用 :kconfig:option:`CONFIG_RUNTIME_ERROR_CHECKS`，保证执行这些检查并向调用者返回结果。

#. 严禁从用户模式注册任何内核模式回调函数。仅用于安装回调的 API 不得作为系统调用开放。有些驱动程序子系统 API 接受可选的回调函数指针，其用户模式验证函数必须确保这些指针为 NULL，否则应调用 :c:macro:`K_OOPS()`。

#. 有些参数检查仅在用户模式下强制执行。这些检查应放在验证函数中，并尽可能向调用者返回结果。

目前 Zephyr 中存在以下已知例外：

* 如果线程对象未初始化，:c:func:`k_thread_join()` 和 :c:func:`k_thread_abort()` 不执行任何操作。原因是线程的初始化位还兼用于表示线程是否正在运行，并在线程退出时清除。参见 #23030。

* :c:func:`k_thread_create()` 对参数检查使用 :c:macro:`K_OOPS()`，因为大量现有代码忽略返回值。#23030 也将处理这一问题。

* 终止关键线程时，:c:func:`k_thread_abort()` 会调用 :c:macro:`K_OOPS()`，因为该函数没有返回值。

* 与日志相关的多个系统调用不返回错误，因此传入错误参数时会调用 :c:macro:`K_OOPS()`。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_USERSPACE`
* :kconfig:option:`CONFIG_EMIT_ALL_SYSCALLS`

API
***

用于创建系统调用验证函数的辅助宏位于 :zephyr_file:`include/zephyr/internal/syscall_handler.h`：

* :c:macro:`K_SYSCALL_OBJ()`
* :c:macro:`K_SYSCALL_OBJ_INIT()`
* :c:macro:`K_SYSCALL_OBJ_NEVER_INIT()`
* :c:macro:`K_OOPS()`
* :c:macro:`K_SYSCALL_MEMORY_READ()`
* :c:macro:`K_SYSCALL_MEMORY_WRITE()`
* :c:macro:`K_SYSCALL_MEMORY_ARRAY_READ()`
* :c:macro:`K_SYSCALL_MEMORY_ARRAY_WRITE()`
* :c:macro:`K_SYSCALL_VERIFY_MSG()`
* :c:macro:`K_SYSCALL_VERIFY`

用于执行系统调用的函数定义在 :zephyr_file:`include/zephyr/syscall.h` 中：

* :c:func:`_arch_syscall_invoke0`
* :c:func:`_arch_syscall_invoke1`
* :c:func:`_arch_syscall_invoke2`
* :c:func:`_arch_syscall_invoke3`
* :c:func:`_arch_syscall_invoke4`
* :c:func:`_arch_syscall_invoke5`
* :c:func:`_arch_syscall_invoke6`
