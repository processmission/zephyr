.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _posix_details:

实现细节
########

在许多方面，Zephyr 提供的支持与任何 POSIX OS 类似：API 绑定以 C 编程语言提供；进行配置后，POSIX 头文件可在标准包含路径中使用。

与其他多用途 POSIX 操作系统不同：

- Zephyr 并不是“一个 POSIX OS”。Zephyr 内核并非围绕 POSIX 标准设计，POSIX 支持是一项需要显式启用的特性
- Zephyr 应用不会单独链接，也不作为子进程执行
- Zephyr、库和应用代码一起编译和链接，在单个（可能是虚拟的）地址空间中以类似单进程应用的方式运行
- Zephyr 不提供 POSIX shell、编译器或实用工具，也不具备自托管能力。

.. note::
   与 Linux 内核或 FreeBSD 不同，Zephyr 不为每种受支持的架构维护静态的系统调用编号表，而是在构建时动态生成系统调用。更多信息请参阅 :ref:`系统调用 <syscalls>`。

设计
====

作为一个库，Zephyr 的 POSIX API 实现力求成为应用、中间件与 Zephyr 内核之间的薄抽象层。

一些通用设计考虑：

- POSIX 接口及实现应属于 Zephyr 的 POSIX 库，而不应放在其他地方，除非 POSIX API 实现和某个其他特性都需要它们。实现应保留在 POSIX 实现内部的例子是 ``getopt()``。实现应作为独立库的例子是多线程和网络功能。

- 当 POSIX API 与另一个 Zephyr 子系统都依赖某个特性时，该特性的实现应作为一个独立的 Zephyr 库，供 POSIX API 以及另一个库或子系统共同使用。这可以降低代码中出现依赖环的可能性。在可行的情况下，该规则还应扩展到宏。在下面的示例中，``libposix`` 依赖 ``libzfoo`` 来实现 Zephyr 中的某项功能“foo”。如果 ``libzfoo`` 也依赖 ``libposix``，就会形成依赖环。这一环可以通过相互依赖的 ``libcommon`` 来消除。

.. graphviz::
   :caption: POSIX 与另一个 Zephyr 库之间的依赖环

   digraph {
       node [shape=rect, style=rounded];
       rankdir=LR;

       libposix [fillcolor="#d5e8d4"];
       libzfoo [fillcolor="#dae8fc"];

       libposix -> libzfoo;
       libzfoo -> libposix;
   }

.. graphviz::
   :caption: POSIX 与其他 Zephyr 库之间的相互依赖

   digraph {
       node [shape=rect, style=rounded];
       rankdir=LR;

       libposix [fillcolor="#d5e8d4"];
       libzfoo [fillcolor="#dae8fc"];
       libcommon [fillcolor="#f8cecc"];

       libposix -> libzfoo;
       libposix -> libcommon;
       libzfoo -> libcommon;
   }

- POSIX API 调用应当以普通的可调用 C 函数形式提供；如果实现中需要使用 Zephyr 的 :ref:`系统调用 <syscalls>`，该系统调用的声明和实现应隐藏在 POSIX API 之后。
