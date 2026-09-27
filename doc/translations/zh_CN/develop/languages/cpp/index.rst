.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _language_cpp:

C++ 语言支持
############

C++ 是基于 C 语言的通用面向对象编程语言。

启用 C++ 支持
*************

Zephyr 支持用 C 和 C++ 编写应用。要在应用中使用 C++，必须在应用配置文件中选择 :kconfig:option:`CONFIG_CPP`，使 Zephyr 包含 C++ 支持。

编译器工具链还必须包含 Zephyr 构建系统支持的 C++ 编译器。Zephyr 支持附带 GNU C++ 编译器（GCC 的一部分）的 :ref:`toolchain_zephyr_sdk`，本文介绍的功能及其可用性均以使用 Zephyr SDK 为前提。

Zephyr 应用默认使用 C++11 标准，即传给编译器的标志所指定的语言版本。可以通过 Kconfig 选择其他标准，例如 :kconfig:option:`CONFIG_STD_CPP98`。Zephyr 支持并测试的最早标准为 C++98。

编译源文件时，构建系统根据文件后缀（扩展名）选择 C++ 编译器。后缀为 **cpp** 或 **cxx** 的文件使用 C++ 编译器，例如 :file:`myCplusplusApp.cpp`。

C++ 标准要求 ``main()`` 的返回类型为 ``int``，``main()`` 必须定义为 ``int main(void)`` 或 ``int main(int, char **)``。带参数的 main 需要选择 ``CONFIG_BOOTARGS``。Zephyr 忽略 main 返回值，但应用仍必须返回零（0），所有非零返回值均为保留值。

.. note::
    不要使用 C++ 编写内核、驱动程序或系统初始化代码。

语言功能
********

Zephyr 目前仅提供部分 C++ 功能，以下功能 *不受支持*：

* 静态全局对象析构
* 依赖操作系统的 C++ 标准库类，例如 ``std::thread``、``std::mutex``

已支持的功能包括但不限于：

* 继承
* 虚函数
* 虚函数表
* 静态全局对象构造函数
* 通过 **new** 和 **delete** 运算符动态管理对象
* 异常
* :abbr:`RTTI (runtime type information)` （运行时类型信息）
* 标准模板库（STL）

静态全局对象构造函数在驱动程序初始化之后、应用 :c:func:`main()` 之前执行。因此，C++ 仅限用于应用代码。

要使用 C++ 异常，必须在应用配置文件中选择 :kconfig:option:`CONFIG_CPP_EXCEPTIONS`。

Zephyr 最小 C++ 库
******************

Zephyr 最小 C++ 库（:file:`lib/cpp/minimal`）提供 C++ 标准库与应用二进制接口（ABI）函数的最小子集，以支持基本 C++ 语言功能，包括：

* ``new`` 和 ``delete`` 运算符
* 虚函数桩和虚函数表
* 用于全局构造函数的静态全局初始化器

最小 C++ 库严格限于提供基本语言支持，不实现任何 `Standard Template Library (STL)`_ 类或函数。因此，它只适合自行实现非标准类库、且不依赖标准模板库组件的应用。

使用 ``std::string``、``std::vector`` 等标准模板库（STL）组件的应用，必须启用 C++ 标准库支持。

C++ 标准库
**********

`C++ 标准库`_ 是 ISO C++ 标准规定的一组类和函数，位于 ``std`` 命名空间中。

Zephyr 不以源码形式包含任何 C++ 标准库实现，而是允许配置构建系统，链接 C++ 编译器工具链附带的预编译标准库。

要启用 C++ 标准库，请在应用配置文件的 :kconfig:option:`CONFIG_LIBCPP_IMPLEMENTATION` 中选择适用的工具链专用 C++ 标准库类型。

例如，使用 :ref:`toolchain_zephyr_sdk` 构建时，可在应用配置文件中选择 :kconfig:option:`CONFIG_GLIBCXX_LIBCPP`，使构建系统链接 GNU C++ 库（``libstdc++.a``）。这是功能完整的 C++ 标准库，提供包括标准模板库（STL）在内的 ISO C++ 标准所需全部功能。

Zephyr 支持以下 C++ 标准库：

* GNU C++ 库（:kconfig:option:`CONFIG_GLIBCXX_LIBCPP`）
* ARC MetaWare C++ 库（:kconfig:option:`CONFIG_ARCMWDT_LIBCPP`）

需要完整 C++ 标准库功能的 Zephyr 子系统，可以在配置中选择 :kconfig:option:`CONFIG_REQUIRES_FULL_LIBCPP`。除非已选择具体 C++ 标准库的 Kconfig 符号，否则它会自动选择兼容的标准库。

头文件与 C、C++ 之间的不兼容性
******************************

C 和 C++ 要互相协作，必须通过头文件共享数据结构、宏、静态函数等代码。两者虽然有大量重叠，却是存在 `known incompatibilities`_ 的不同语言；C 并非只是 C++ 的子集。标准版本（例如 C++11）又增加了一层复杂性：新功能常借鉴另一门语言，却在多年后才引入，并有细微差异。编译器还经常在功能标准化之前提供早期实现；标准中的歧义可能被不同编译器作不同解释；编译器本身也可能有缺陷，需要变通处理。为简化问题，许多项目限制可用工具链的数量，而 Zephyr 没有这样做。

这些兼容性问题对头文件的影响尤其大。不仅因为头文件要兼容 C 和 C++，还因为实际项目中常见的 *间接* 包含以及 `lack of structure and headers organization`_，使它们最终会在数量惊人的其他源文件中被编译。因此，头文件面对的工具链和项目配置组合更多。此外，Zephyr 对代码风格、编译器警告、静态分析器和标准符合性（例如 MISRA）还有严格要求。

这些约束叠加后，编写头文件可能非常困难。本节旨在记录 Zephyr 场景下编写头文件的良好实践和经验。虽然许多内容并非 Zephyr 独有，但它不能替代对 C/C++ 标准、教材及其他参考资料的学习。

测试
----

幸运的是，Zephyr 有完善的测试和 CI 基础设施，用于提供覆盖基线、尽早发现问题、执行策略，并在一定程度上控制组合爆炸。``tests/lib/cpp/cxx/`` 在这方面很有用，其 ``testcase.yaml`` 配置可让 ``twister`` 快速遍历多个 ``-std`` 参数，例如 ``-std=c++98``、``-std=c++11`` 等。

请记住，未使用的宏不会被编译。

指定初始化器
------------

头文件中常使用初始化宏来减少重复代码。C99 引入了通过指定成员名称初始化 ``struct`` 和 ``union`` 的方式，不必再使用 *无标识* 表达式列表。某些 GCC 版本甚至在 C90 模式下也支持指定初始化器。

在简单用法下，指定初始化器更不易出错、更易读、更灵活。但 C99 允许的形式非常多且宽松：可以乱序、重复、嵌套（``.a.x =``），可以省略多处花括号，也可以混用指定和非指定初始化器等。

二十年后，C++20 也引入指定初始化器，但限制严格得多，部分原因是 C++ 的 ``struct`` 实际上是 ``class``。C++ 提案 P0329（含与 C 的对比）及完整 C++ 参考资料均说明：不能混用两种形式，初始化器必须按顺序排列，但允许跳过成员。

有趣的是，C++20 的新限制可能使 ``gcc -std=c++20`` 无法编译可由 ``gcc -std=c++17`` 成功编译的代码。例如，``gcc -std=c++17`` 及更早模式允许 C 风格的指定初始化器与无标识表达式混用，而使用 *同一个 GCC 版本* 的 ``gcc -std=c++20`` 则无法编译。

建议：为尽可能兼容不同 C/C++ 工具链和标准，Zephyr 头文件中的指定初始化器应遵守 C++20 的全部规则和限制。C99 之前的非指定初始化方式兼容性更好，也允许使用，但指定初始化更易读，是首选风格。无论采用哪种方式，都不得在同一个初始化器中混用。

警告：编译成功不代表兼容性问题已经解决。例如，C99 未规定初始化表达式的 *求值顺序*，而 C++20 规定为通常预期的从左到右。其他标准版本可能不同。不确定时，不要依赖求值顺序，无论此处还是其他场合。

匿名联合体
----------

匿名联合体（也称无名联合体）似乎从 C++ 诞生时就已存在，但直到 C11 才正式加入 C。两种语言在此也有差异：例如，C 仅允许匿名联合体作为外围 ``struct`` 或 ``union`` 的成员；C++ 始终允许空列表 ``{ }``，C 则要到 C23 才允许，等等。

初始化匿名成员时，表达式可以带或不带花括号，也可以采用指定或无标识形式。为最大程度保证可移植性，初始化 *匿名联合体* 时：

- *不要* 用花括号包围 *指定* 初始化器。C++20 及之后版本要求如此，否则会将这些花括号视为把无标识表达式与其他指定初始化器混用，导致编译失败。

- 应当用花括号包围 *无标识* 表达式，这是 C 的要求。可能因为 C 较宽松，允许多种初始化形式，因此需要花括号消除歧义。注意，C 虽然允许省略初始化表达式中的大多数花括号，但使用无标识表达式初始化匿名联合体的这种情况除外。

某些 C11 之前的 GCC 版本支持某种形式的匿名联合体，但要求用花括号包围其指定初始化器，与此建议冲突。可通过 ``#ifdef __STDC_VERSION__`` 解决，参见 Zephyr 提交 `c15f029a7108 <https://github.com/zephyrproject-rtos/zephyr/commit/c15f029a7108>`_ 及对应代码审查。


.. _`C++ Standard Library`: https://en.wikipedia.org/wiki/C%2B%2B_Standard_Library
.. _`Standard Template Library (STL)`: https://en.wikipedia.org/wiki/Standard_Template_Library
.. _`known incompatibilities`: https://en.wikipedia.org/wiki/Compatibility_of_C_and_C%2B%2B
..  _`lack of structure and headers organization`:
    https://github.com/zephyrproject-rtos/zephyr/issues/41543
.. _`gcc commit [C++ PATCH] P0329R4: Designated Initialization`:
    https://gcc.gnu.org/pipermail/gcc-patches/2017-November/487584.html
