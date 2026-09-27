.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _test-framework:

测试框架
########

Zephyr 测试框架（Ztest）是用于开发阶段的简单测试框架，提供基本断言宏和通用测试结构。

该框架既可用作集成测试的通用框架，也可用于特定模块的单元测试。

.. contents::
   :depth: 1
   :local:
   :backlinks: top

快速入门：集成测试
******************

一个可直接使用的简单基础示例位于 :zephyr_file:`samples/subsys/testsuite/integration`。要为 **foo** 的 **bar** 组件创建测试应用，应将示例文件夹复制到 ``tests/foo/bar``，再按测试需求编辑其中的文件。

使用 :ref:`Twister <twister_script>` 构建并执行测试应用中定义的所有适用测试场景，例如：

.. code-block:: console

    west twister -T tests/foo/bar/

要仅选择一个测试场景，运行 Twister 时使用 ``--scenario``：

.. code-block:: console

   west twister --scenario tests/foo/bar/your.test.scenario.name

上面的 ``tests/foo/bar`` 是测试应用路径，``your.test.scenario.name`` 指向 :file:`tests.yaml` 中定义的测试场景，类似测试套件模板示例中的 ``sample.testing.ztest``。

Twister 如何处理 Ztest 应用，详见 :ref:`Twister 测试项目示意图 <twister_test_project_diagram>`。

示例包含以下文件：

.. literalinclude:: ../../../samples/subsys/testsuite/integration/CMakeLists.txt
   :language: CMake
   :caption: CMakeLists.txt
   :linenos:

.. literalinclude:: ../../../samples/subsys/testsuite/integration/tests.yaml
   :language: yaml
   :caption: tests.yaml
   :linenos:

.. literalinclude:: ../../../samples/subsys/testsuite/integration/prj.conf
   :language: text
   :caption: prj.conf
   :linenos:

.. literalinclude:: ../../../samples/subsys/testsuite/integration/src/main.c
   :language: c
   :caption: src/main.c
   :linenos:

测试应用可包含多个套件，用于测试功能或 API。实现测试用例的函数应遵循以下规则：

* 测试用例函数名应以 **test_** 开头
* 测试用例应使用 Doxygen 编写文档
* 测试用例函数名在被测部分或组件中应唯一

例如：

.. code-block:: C

   /**
    * @brief Test Asserts
    *
    * This test case verifies the zassert_true macro.
    */
   ZTEST(my_suite, test_assert)
   {
           zassert_true(1, "1 was false");
   }

列出测试
========

Zephyr 代码树中的测试应用包含许多测试场景，它们作为项目的一部分运行，测试相似功能，例如 API 或特性。``twister`` 脚本可解析所有或部分测试应用的场景、套件和用例，并生成细粒度报告，说明用例通过、失败、被阻止或跳过。

Twister 通过解析源文件查找测试用例名，例如可运行以下命令列出全部内核测试用例：

.. code-block:: console

   west twister --list-tests -T tests/kernel

跳过测试
========

特殊或架构专用测试不能在所有平台和架构上运行，但仍应计数并报告为跳过。由于测试清单从代码中提取，在套件内添加条件编译并非理想做法。因平台或特性而需跳过的测试，应使用 :c:func:`ztest_test_skip` 或 :c:macro:`Z_TEST_SKIP_IFDEF` 显式报告跳过。若测试执行，则必须报告通过或失败。例如：

.. code-block:: C

   #ifdef CONFIG_TEST1
   ZTEST(common, test_test1)
   {
        zassert_true(1, "true");
   }
   #else
   ZTEST(common, test_test1)
   {
        ztest_test_skip();
   }
   #endif

   ZTEST(common, test_test2)
   {
        Z_TEST_SKIP_IFDEF(CONFIG_BUGxxxxx);
        zassert_equal(1, 0, NULL);
   }

   ZTEST_SUITE(common, NULL, NULL, NULL, NULL, NULL);

.. _ztest_unit_testing:

快速入门：单元测试
******************

Ztest 可用于单元测试，将测试集中到具体模块，而不必为测试单个函数引入整个 Zephyr 操作系统。由于只编译该模块并直接调用被测函数，测试速度更快。

配置单元测试时，在单元测试源文件目录添加 CMakeLists.txt、tests.yaml 和 prj.conf。使用 -DBOARD=unit_testing 构建该目录生成的二进制文件。调用 twister 时，zephyr/scripts/pylib/twister/twisterlib/testplan.py 会过滤掉未设置 type: unit 的 tests.yaml。BOARD=unit_testing 的固件构建只执行单元测试。

.. note::
   单元测试作为主机上的 **原生** 应用运行，因此具有与 :ref:`POSIX 架构<Posix arch>` 文档相似的 :ref:`限制 <posix_arch_limitations>`。仅支持在 Linux 上运行单元测试；Windows 或 macOS 需要使用运行 Linux 的容器或虚拟机。依赖安装参照 :ref:`POSIX 架构依赖<posix_arch_deps>`。

.. _unit_testing_board:

``unit_testing`` 开发板
=======================

单元测试针对特殊的 ``unit_testing`` 开发板（:zephyr_file:`subsys/testsuite/boards/unit_testing`）构建。它既非真实硬件也非仿真目标，而是使用 ``arch: unit`` 的伪开发板，通过主机工具链生成普通原生可执行文件。使用 ``-DBOARD=unit_testing`` 选择它后，只构建并链接加入 ``testbinary`` 目标的源文件和 Ztest 单元测试适配器。Twister 会为 ``type: unit`` 场景自动这样选择。

关键是，**完全不构建 Zephyr 内核和操作系统**。没有启动流程、调度器、设备树驱动的设备初始化或驱动模型。被测函数编译进测试二进制文件并被直接调用。模块依赖的内核 API 或其他依赖必须由测试自身提供，通常使用桩函数或 :ref:`模拟对象 <mocking-fff>`。

.. _unit_testing_vs_native_sim:

与 ``native_sim`` 等开发板的区别
--------------------------------

``unit_testing`` 与 :zephyr:board:`native_sim` 都在主机上运行，容易混淆，但本质不同：

* :zephyr:board:`native_sim` 将 **完整 Zephyr 操作系统** （内核、设备树、Kconfig、驱动及子系统）构建为主机二进制文件，启动和运行方式与真实硬件上的 Zephyr 镜像完全相同，只是面向主机而非目标 SoC 编译。适合在主机上运行完整应用和集成测试。这些开发板的测试 **不** 设置 ``type: unit``。

* ``unit_testing`` **不构建上述任何部分**，仅链接被测代码和 Ztest，其余依赖使用桩或模拟实现，并直接调用被测函数。这使构建和运行更快，专注于单个模块，代价是必须为每项依赖提供桩。这些测试必须设置 ``type: unit``，见 :ref:`下文 <tests_yaml_unit>`。

因此，在运行中的 Zephyr 系统环境中验证代码应使用 ``native_sim``；不引入内核、测试独立模块则使用 ``unit_testing``。

CMakeLists.txt
==============

要声明源目录中的单元测试，需将相关源文件加入 CMake :zephyr_file:`unittest <cmake/modules/unittest.cmake>` 组件提供的 ``testbinary`` 目标。最小示例如下：

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.28.0)

   project(app)
   find_package(Zephyr COMPONENTS unittest REQUIRED HINTS $ENV{ZEPHYR_BASE})
   target_sources(testbinary PRIVATE main.c)

由于未引入多数代码依赖的基本内核数据结构，必须在测试中提供函数桩。Ztest 提供了模拟函数的辅助工具，如下所示。

单元测试中，模拟对象可模拟复杂真实对象的行为。通过验证是否发生了与对象的交互，必要时断言交互顺序，来判定测试通过或失败。

.. _tests_yaml_unit:

tests.yaml
==========

必须在 tests.yaml 中将“type”键设为“unit”。

.. code-block:: yaml

   tests:
      testscenario.testsuite:
         tags: your_tag
         type: unit

prj.conf
========

对于单元测试，此文件通常仅包含：

.. code-block:: kconfig

   CONFIG_ZTEST=y

如果单元测试需要额外库，例如数学库，必须通过 CMakeLists.txt 或 tests.yaml 添加：

.. code-block:: yaml

   tests:
      testscenario.testsuite:
         tags: your_tag
         type: unit
         extra_args:
            - EXTRA_LDFLAGS="-lm"

单元测试示例位于 :zephyr_file:`tests/unit/`。


创建测试套件
************

使用 Ztest 创建套件只需调用 :c:macro:`ZTEST_SUITE`，其参数如下：

* ``suite_name``：套件名称，必须在同一二进制文件中唯一。
* :c:type:`ztest_suite_predicate_t`：可选判定函数，用于选择套件何时运行。它接收 :c:func:`ztest_run_all` 传入的全局状态指针，并返回布尔值决定是否运行套件。
* :c:type:`ztest_suite_setup_t`：可选初始化函数，返回测试 fixture。每次运行套件时调用一次。
* :c:type:`ztest_suite_before_t`：可选前置函数，在套件内每个测试之前运行。
* :c:type:`ztest_suite_after_t`：可选后置函数，在套件内每个测试之后运行。
* :c:type:`ztest_suite_teardown_t`：可选清理函数，在套件全部测试结束时运行。

以下示例使用判定函数：

.. code-block:: C

   #include <zephyr/ztest.h>
   #include "test_state.h"

   static bool predicate(const void *global_state)
   {
        return ((const struct test_state*)global_state)->x == 5;
   }

   ZTEST_SUITE(alternating_suite, predicate, NULL, NULL, NULL, NULL);

向套件添加测试
**************

有 5 个用于向套件添加测试的宏：

* :c:macro:`ZTEST` ``(suite_name, test_name)``：将 ``test_name`` 指定的测试加入 ``suite_name`` 指定的套件。
* :c:macro:`ZTEST_P` ``(suite_name, test_name)``：向指定套件添加值参数化测试。测试体对每个已注册参数值执行一次。在测试体内调用 :c:func:`ztest_get_current_param` 或使用带类型的辅助宏 :c:macro:`ZTEST_GET_PARAM` 获取当前值。套件 fixture（``data`` 参数）独立于参数，绝不会被覆盖。完整 API 见 `值参数化测试`_。
* :c:macro:`ZTEST_USER` ``(suite_name, test_name)``：与 :c:macro:`ZTEST` 相同，但启用 :kconfig:option:`CONFIG_USERSPACE` 时在用户空间线程中运行测试。
* :c:macro:`ZTEST_F` ``(suite_name, test_name)``：与 :c:macro:`ZTEST` 相同，但测试函数中已包含名为 ``fixture``、类型为 ``<suite_name>_fixture`` 的变量。
* :c:macro:`ZTEST_USER_F` ``(suite_name, test_name)``：结合 :c:macro:`ZTEST_F` 的 fixture 功能和用户空间测试线程。

测试 fixture
============

测试 fixture 可简化重复初始化操作。同一套件的测试通常需要初始设置，并在各测试间重置状态。可按以下方式实现：

.. code-block:: C

   #include <zephyr/ztest.h>

   struct my_suite_fixture {
        size_t max_size;
        size_t size;
        uint8_t buff[1];
   };

   static void *my_suite_setup(void)
   {
        /* Allocate the fixture with 256 byte buffer */
        struct my_suite_fixture *fixture = malloc(sizeof(struct my_suite_fixture) + 255);

        zassume_not_null(fixture, NULL);
        fixture->max_size = 256;

        return fixture;
   }

   static void my_suite_before(void *f)
   {
        struct my_suite_fixture *fixture = (struct my_suite_fixture *)f;
        memset(fixture->buff, 0, fixture->max_size);
        fixture->size = 0;
   }

   static void my_suite_teardown(void *f)
   {
        free(f);
   }

   ZTEST_SUITE(my_suite, NULL, my_suite_setup, my_suite_before, NULL, my_suite_teardown);

   ZTEST_F(my_suite, test_feature_x)
   {
        zassert_equal(0, fixture->size);
        zassert_equal(256, fixture->max_size);
   }

在用户空间线程中使用 fixture 分配的内存，例如执行 :c:macro:`ZTEST_USER` 或 :c:macro:`ZTEST_USER_F` 时，必须将该内存声明为用户空间可访问，因为它由内核空间拥有并初始化。Ztest 提供 :c:macro:`ZTEST_DMEM` 和 :c:macro:`ZTEST_BMEM` 宏支持此类共享内存。

高级功能
********

.. _value-parameterized-tests:

值参数化测试
============

值参数化测试对给定列表中的每个值执行一次同一测试体，类似 GoogleTest 的 ``TEST_P`` / ``INSTANTIATE_TEST_SUITE_P`` 模式。fixture 与参数完全独立：套件 ``setup()`` 的返回值始终作为 ``data`` 传入，绝不会被参数值覆盖。

声明参数化测试体
----------------

:c:macro:`ZTEST_P` 的用法与 :c:macro:`ZTEST` 相同。测试体中的 ``data`` 指针承载套件 fixture，与 :c:macro:`ZTEST_F` 一致。通过以下运行时访问函数获取当前参数值：

.. code-block:: C

   #include <zephyr/ztest.h>

   struct my_suite_fixture {
        int initial_value;
   };

   static void *my_suite_setup(void) {
        static struct my_suite_fixture f = { .initial_value = 42 };
        return &f;
   }

   ZTEST_SUITE(my_suite, NULL, my_suite_setup, NULL, NULL, NULL);

   ZTEST_P(my_suite, test_multiply)
   {
        struct my_suite_fixture *f = (struct my_suite_fixture *)data;
        int factor = ZTEST_GET_PARAM(int);

        /* fixture is always intact, regardless of parameter */
        zassert_equal(f->initial_value, 42, "fixture corrupted");
        zassert_true(f->initial_value * factor > 0, "product must be positive");
   }

声明参数值
----------

使用 :c:macro:`ZTEST_DEFINE_PARAM_VALUES`，根据字面量值创建静态值集合：

.. code-block:: C

   ZTEST_DEFINE_PARAM_VALUES(small_factors, int, 1, 2, 3);

若值已存于数组中，使用 :c:macro:`ZTEST_DEFINE_PARAM_VALUES_ARRAY`：

.. code-block:: C

   static const int big_factors[] = { 10, 100, 1000 };
   ZTEST_DEFINE_PARAM_VALUES_ARRAY(big_factor_vals, big_factors);

数值范围使用 :c:macro:`ZTEST_DEFINE_PARAM_RANGE`，其语义与 GoogleTest 的 ``testing::Range(begin, end [, step])`` 相同。值为 ``{begin, begin+step, ...}``，直到但 **不包含** ``end``。不分配底层数组，因此大范围也没有 RAM 开销：

.. code-block:: C

   /* {0, 2, 4, 6, 8} — 5 values, step is supplied explicitly */
   ZTEST_DEFINE_PARAM_RANGE(even_vals, int, 0, 10, 2);

   /* {1, 2, 3, 4, 5} — step=1 is the common case */
   ZTEST_DEFINE_PARAM_RANGE(one_to_five, int, 1, 6, 1);

.. note::

   ``ZTEST_DEFINE_PARAM_RANGE`` 要求 ``end > begin`` 且 ``step > 0``，两者均通过 :c:macro:`BUILD_ASSERT` 在编译时检查。

必须 **在运行时计算** 的值，例如随机数、硬件传感器读数或自定义算法生成值，使用 :c:macro:`ZTEST_DEFINE_PARAM_GENERATOR` 或 :c:macro:`ZTEST_DEFINE_PARAM_GENERATOR_WITH_SETUP`。两者接受签名为 ``void gen(size_t index, void *out)`` 的用户生成器回调，每次调用写入一个值。与范围一样，不分配底层数组。

``_WITH_SETUP`` 变体还会在分派循环前调用 **一次** ``void setup(void)`` 钩子，适合初始化伪随机数种子、重置有状态计数器或打开生成器所需资源：

.. code-block:: C

   #include <zephyr/random/random.h>

   /* Seed the RNG before the first iteration so failures are reproducible. */
   static void seed_rng(void)
   {
        sys_rand_seed(MY_FUZZ_SEED);
   }

   static void rand_u32_gen(size_t idx, void *out)
   {
        ARG_UNUSED(idx);
        *(uint32_t *)out = sys_rand32_get();
   }

   ZTEST_DEFINE_PARAM_GENERATOR_WITH_SETUP(fuzz_vals, uint32_t, MY_FUZZ_ITERATIONS,
                                           seed_rng, rand_u32_gen);

无需初始化时，使用更简单的形式：

.. code-block:: C

   static void deterministic_gen(size_t idx, void *out)
   {
        /* Deterministic but computed at runtime (e.g. based on hardware ID). */
        *(uint32_t *)out = get_device_seed() ^ (uint32_t)idx;
   }

   ZTEST_DEFINE_PARAM_GENERATOR(hw_vals, uint32_t, 16U, deterministic_gen);

.. note::

   两个生成器宏的 ``count_`` 参数必须是常量表达式，例如数值字面量、``#define`` 或 ``MY_FUZZ_ITERATIONS`` 这样的 Kconfig 符号。不支持真正动态的数量。

结构体类型参数的使用方式相同：

.. code-block:: C

   struct point { int x; int y; };

   static const struct point corners[] = { {0,0}, {1,0}, {0,1}, {1,1} };
   ZTEST_DEFINE_PARAM_VALUES_ARRAY(corner_vals, corners);

   ZTEST_P(my_suite, test_in_unit_square)
   {
        const struct point *p = ZTEST_GET_PARAM_PTR(struct point);
        zassert_true(p->x >= 0 && p->x <= 1 && p->y >= 0 && p->y <= 1,
                    "point (%d, %d) outside unit square", p->x, p->y);
   }

实例化参数化测试
----------------

:c:macro:`ZTEST_INSTANTIATE_TEST_SUITE_P` 将值集合绑定到测试体。每次调用创建一个单独的具名实例；同一测试体可使用不同值集合多次实例化：

.. code-block:: C

   ZTEST_INSTANTIATE_TEST_SUITE_P(small, my_suite, test_multiply, small_factors);
   ZTEST_INSTANTIATE_TEST_SUITE_P(big,   my_suite, test_multiply, big_factor_vals);

首个参数（``small`` / ``big``）是在编译单元内任意但唯一的标识，记录在测试元数据中，不影响 Twister 报告中的测试命名。

获取当前参数
------------

在 :c:macro:`ZTEST_P` 测试体中，可使用以下辅助工具：

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 辅助工具
     - 描述
   * - ``ztest_has_current_param()``
     - 在参数化调用内部调用时返回 ``true``。
   * - ``ztest_get_current_param()``
     - 返回指向当前值的 ``const void *`` 指针。
   * - ``ZTEST_GET_PARAM_PTR(type)``
     - 返回指向当前值的 ``const type *`` 指针。
   * - ``ZTEST_GET_PARAM(type)``
     - 解引用当前值，并以 ``type`` 类型返回。
   * - ``ztest_get_current_param_index()``
     - 返回当前值在集合中的从零开始的索引。
   * - ``ztest_get_current_param_size()``
     - 返回一个参数元素的字节数。

非参数化测试（:c:macro:`ZTEST`、:c:macro:`ZTEST_F`）中，``ztest_has_current_param()`` 始终返回 ``false``，``ztest_get_current_param()`` 始终返回 ``NULL``。

测试结果预期
============

有些测试本就用于验证失败情形。如果因代码特性而预期测试失败或跳过，可以为测试添加相应注解，例如：

.. code-block:: C

   #include <zephyr/ztest.h>

   ZTEST_SUITE(my_suite, NULL, NULL, NULL, NULL, NULL);

   ZTEST_EXPECT_FAIL(my_suite, test_fail);
   ZTEST(my_suite, test_fail)
   {
     /** This will fail the test */
     zassert_true(false, NULL);
   }

   ZTEST_EXPECT_SKIP(my_suite, test_skip);
   ZTEST(my_suite, test_skip)
   {
     /** This will skip the test */
     zassume_true(false, NULL);
   }

上例中的测试本应分别标记为失败和跳过，但由于设置了预期，Ztest 将两者均标记为通过。

测试规则
========

测试规则可为每项测试和每个套件执行相同逻辑。有时需要为二进制文件中的每个测试重置状态，而不论当前运行哪个套件，例如重置模拟对象、重置仿真器或清空 UART：

.. code-block:: C

   #include <zephyr/fff.h>
   #include <zephyr/ztest.h>

   #include "test_mocks.h"

   DEFINE_FFF_GLOBALS;

   DEFINE_FAKE_VOID_FUN(my_weak_func);

   static void fff_reset_rule_before(const struct ztest_unit_test *test, void *fixture)
   {
        ARG_UNUSED(test);
        ARG_UNUSED(fixture);

        RESET_FAKE(my_weak_func);
   }

   ZTEST_RULE(fff_reset_rule, fff_reset_rule_before, NULL);

自定义 ``test_main``
====================

Ztest 提供默认 :c:func:`test_main`，但某些应用可能需要自定义行为，尤其当测试依赖某种无法复现或不重启进程就难以复现的全局状态时。例如某开发板具有多步上电流程，可用 ``predicate`` 控制套件在哪一步运行。这时 :c:func:`test_main` 可写为：

.. code-block:: C

   #include <zephyr/ztest.h>

   #include "my_test.h"

   void test_main(void)
   {
        struct power_sequence_state state;

        /* Only suites that use a predicate checking for phase == PWR_PHASE_0 will run. */
        state.phase = PWR_PHASE_0;
        ztest_run_all(&state, false, 1, 1);

        /* Only suites that use a predicate checking for phase == PWR_PHASE_1 will run. */
        state.phase = PWR_PHASE_1;
        ztest_run_all(&state, false, 1, 1);

        /* Only suites that use a predicate checking for phase == PWR_PHASE_2 will run. */
        state.phase = PWR_PHASE_2;
        ztest_run_all(&state, false, 1, 1);

        /* Check that all the suites in this binary ran at least once. */
        ztest_verify_all_test_suites_ran();
   }

:c:func:`ztest_run_all` 的签名为 ``ztest_run_all(const void *state, bool shuffle, int suite_iter, int case_iter)``：

* ``state``：传给各套件 ``predicate`` 的全局状态指针。
* ``shuffle``：为 ``true`` 时随机打乱套件和测试顺序，需要 :kconfig:option:`CONFIG_ZTEST_SHUFFLE`；为 ``false`` 时保持默认字母数字顺序。
* ``suite_iter``：每个测试套件的重复次数。
* ``case_iter``：每个测试用例的重复次数。

上例中，每次调用按顺序运行匹配套件一次，不打乱顺序。


声明测试套件的推荐做法
**********************

*twister* 等验证工具需要获取 Zephyr *ztest* 测试镜像提供的测试用例列表。

.. admonition:: 理由

   目的是可追溯性。仅有一个信号量测试应用还不够，还需展示所有 API 和功能都有对应测试点，并能追溯至 API 文档和功能需求。

   测试报告应展示每个用例的通过、失败、被阻止或跳过结果。仅报告高层测试应用过于模糊，尤其当测试同时承担太多功能时。

其他问题：

- 为什么不先通过 CPP 预扫描再解析，或构建后扫描 ELF 文件？

  如果 C 预处理或构建因任何问题失败，就无法识别子用例。

- 为什么不在 YAML 测试配置中声明？

  单独的用例描述文件比将信息直接保留在测试源文件中更难维护。变更时只更新一个文件，可避免重复信息。

压力测试框架
************

Zephyr 压力测试框架（Ztress）提供在多个优先级上下文中执行用户函数的环境，可验证代码对抢占的承受能力。框架跟踪每个上下文的执行和被抢占次数，支持超时、执行次数、被抢占次数等完成条件。

框架创建指定数量、优先级各异的线程，并可选择启动定时器。每个上下文调用各自的用户函数，然后休眠随机数量的系统时钟节拍。框架跟踪 CPU 负载并调整休眠间隔，以提高负载。为增加抢占概率，系统时钟频率应较高。QEMU x86 默认的 100 Hz 过低，建议提高到 100 kHz。

使用接受可变参数的 :c:macro:`ZTRESS_EXECUTE` 设置并执行压力测试环境。各参数通过 :c:macro:`ZTRESS_TIMER` 或 :c:macro:`ZTRESS_THREAD` 指定一个上下文，按优先级从高到低排列。每个上下文通过最少执行次数和被抢占次数指定完成条件。满足全部条件并执行完成后，打印报告，宏返回。测试运行期间还会定期打印进度。

可通过设置测试超时（:c:func:`ztress_set_timeout`）或显式中止（:c:func:`ztress_abort`）提前结束执行。

用户函数参数包含执行计数器和表示是否为最后一次执行的标志。

下例设置并运行 3 个上下文，其中一个为 k_timer 中断处理程序上下文。完成条件为每个上下文至少执行 10000 次，最低优先级上下文至少被抢占 1000 次。还设置了 10 秒超时，条件未满足也会结束。各上下文的最后一个参数为初始休眠时间，测试过程中会不断调整它，以达到最高 CPU 负载。

.. code-block:: C

   ztress_set_timeout(K_MSEC(10000));
   ZTRESS_EXECUTE(ZTRESS_TIMER(foo_0, user_data_0, 10000, Z_TIMEOUT_TICKS(20)),
                  ZTRESS_THREAD(foo_1, user_data_1, 10000, 0, Z_TIMEOUT_TICKS(20)),
                  ZTRESS_THREAD(foo_2, user_data_2, 10000, 1000, Z_TIMEOUT_TICKS(20)));

配置
====

Ztress 的静态配置包括：

 - :kconfig:option:`CONFIG_ZTRESS_MAX_THREADS`：支持的线程数。
 - :kconfig:option:`CONFIG_ZTRESS_STACK_SIZE`：创建线程的栈大小。
 - :kconfig:option:`CONFIG_ZTRESS_REPORT_PROGRESS_MS`：测试进度报告间隔。

API 参考
********

运行测试
========

.. doxygengroup:: ztest_test

断言
====

断言不成立时，这些宏立即使测试失败，并打印当前文件、行号、函数、失败原因及可选消息。若 :kconfig:option:`CONFIG_ZTEST_ASSERT_VERBOSE` 为 0，仅打印文件和行号，以减小测试二进制大小。

``zassert_equal(buf->ref, 2, "Invalid refcount")`` 断言失败时的输出示例：

.. code-block:: none

    Assertion failed at main.c:62: test_get_single_buffer: Invalid refcount (buf->ref not equal to 2)
    Aborted at unit test function

.. doxygengroup:: ztest_assert


期望
====

期望不成立时，这些宏继续执行测试，并在执行结束时将测试判为失败。它们打印当前文件、行号、函数、失败原因及可选消息，但不中断测试。若 :kconfig:option:`CONFIG_ZTEST_ASSERT_VERBOSE` 为 0，仅打印文件和行号，以减小二进制大小。

例如，以下期望不成立时：

.. code-block:: C

   zexpect_equal(buf->ref, 2, "Invalid refcount");
   zexpect_equal(buf->ref, 1337, "Invalid refcount");

输出类似于：

.. code-block:: none

   START - test_get_single_buffer
       Expectation failed at main.c:62: test_get_single_buffer: Invalid refcount (buf->ref not equal to 2)
       Expectation failed at main.c:63: test_get_single_buffer: Invalid refcount (buf->ref not equal to 1337)
    FAIL - test_get_single_buffer in 0.0 seconds

.. doxygengroup:: ztest_expect

假设
====

假设不成立时，这些宏立即跳过测试或套件，并打印当前文件、行号、函数、失败原因及可选消息。若 :kconfig:option:`CONFIG_ZTEST_ASSERT_VERBOSE` 为 0，仅打印文件和行号，以减小二进制大小。

``zassume_equal(buf->ref, 2, "Invalid refcount")`` 假设不成立时的输出示例：

.. code-block:: none

    START - test_get_single_buffer
        Assumption failed at main.c:62: test_get_single_buffer: Invalid refcount (buf->ref not equal to 2)
     SKIP - test_get_single_buffer in 0.0 seconds

.. doxygengroup:: ztest_assume


Ztress
======

.. doxygengroup:: ztest_ztress


.. _mocking-fff:

通过 FFF 模拟
=============

Zephyr 集成了 FFF 以支持模拟，文档见 `FFF`_。使用时包含对应头文件：

.. code-block:: C

   #include <zephyr/fff.h>

Zephyr 提供多个基于 FFF 的伪驱动，可用作桩或模拟实现。通过 :ref:`devicetree` 和 :ref:`kconfig` 配置伪驱动实例。更多信息见以下设备树绑定：

.. zephyr-keep-sorted-start

* :dtcompatible:`zephyr,fake-can`
* :dtcompatible:`zephyr,fake-comp`
* :dtcompatible:`zephyr,fake-eeprom`
* :dtcompatible:`zephyr,fake-leds`
* :dtcompatible:`zephyr,fake-pwm`
* :dtcompatible:`zephyr,fake-regulator`
* :dtcompatible:`zephyr,fake-rtc`
* :dtcompatible:`zephyr,fake-stepper-ctrl`
* :dtcompatible:`zephyr,fake-stepper-driver`

.. zephyr-keep-sorted-stop

Zephyr 还定义了 FFF 扩展以简化伪函数声明。参见 :ref:`FFF 扩展 <fff-extensions>`。

自定义测试输出
**************
将 :kconfig:option:`CONFIG_ZTEST_TC_UTIL_USER_OVERRIDE` 设为“y”，并添加包含覆盖定义的 :file:`tc_util_user_override.h` 文件，即可启用自定义。

在项目的 :file:`CMakeLists.txt` 中添加 ``zephyr_include_directories(my_folder)``，让 Zephyr 构建时能找到该头文件。

可覆盖的宏和定义见 :zephyr_file:`subsys/testsuite/include/zephyr/tc_util.h`，它们位于如下代码块中：

.. code-block:: C

   #ifndef SOMETHING
   #define SOMETHING <default implementation>
   #endif /* SOMETHING */

.. _ztest_shuffle:

打乱测试顺序
************
默认按字母数字顺序排序并运行测试，用例可能依赖这一顺序。启用 :kconfig:option:`CONFIG_ZTEST_SHUFFLE` 可随机打乱顺序。测试输出会显示失败测试的随机种子。原生模拟器构建可通过 Twister 的 ``--seed`` 参数指定种子。


重复测试
********
默认测试只执行一次。启用 :kconfig:option:`CONFIG_ZTEST_REPEAT` 可重复执行用例和套件。默认重复因子为 3，即每个套件执行 3 次，每个用例也执行 3 次。可通过 :kconfig:option:`CONFIG_ZTEST_SUITE_REPEAT_COUNT` 和 :kconfig:option:`CONFIG_ZTEST_TEST_REPEAT_COUNT` 更改。

选择测试
********
针对原生模拟器构建的测试，可用命令行参数列出或选择待运行测试。test 参数接受逗号分隔的 ``suite::test`` 列表。用 ``*`` 代替测试名可运行套件内所有测试。

例如

.. code-block:: bash

    $ zephyr.exe -list
    $ zephyr.exe -test="fixture_tests::test_fixture_pointer,framework_tests::test_assert_mem_equal"
    $ zephyr.exe -test="framework_tests::*"


.. _fff-extensions:

FFF 扩展
********

.. doxygengroup:: fff_extensions


.. _FFF: https://github.com/meekrosoft/fff
