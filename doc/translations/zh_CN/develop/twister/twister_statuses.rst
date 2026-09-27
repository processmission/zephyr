.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _twister_statuses:

Twister 状态
############

什么是 Twister 状态？
=====================

Twister 状态以全面、易懂的方式表示以下对象的当前状态：

- ``Harness``
- ``TestCase``
- ``TestSuite``
- ``TestInstance``

实际使用中，多数用户关注的是 Twister 运行结束后实例和用例的状态。

.. tip::

   术语回顾：

   .. tabs::

      .. tab:: ``Harness``

         ``Harness`` 是 Twister 内部的 Python 类，用于捕获并分析外部程序输出。它不出现在最终报告中，因此本页为清晰起见不再展开。

      .. tab:: ``TestCase``

         ``TestCase``，也称 Case，是验证某项断言的代码，是 Zephyr 测试的最小单位。

      .. tab:: ``TestSuite``

         ``TestSuite``，也称 Suite，是一组用例。可通过 ``testcase.yaml`` 按套件修改 Twister 行为。归为一组的用例应有足够共同点，才适合让 Twister 统一处理。

      .. tab:: ``TestInstance``

         ``TestInstance``，也称 Instance，是套件在某个平台上的实例。Twister 通常报告实例结果，尽管报告中称其为“Suites”。适用于套件的状态也适用于实例。本节无需区分二者，所说“套件”同样指实例。

   更详细说明见 :ref:`此处 <twister_tests_long_version>`。

可能的 Twister 状态
===================

.. list-table:: Twister 状态
   :widths: 10 10 66 7 7
   :header-rows: 1

   * - 代码中
     - 文本中
     - 描述
     - 套件
     - 用例
   * - FILTER
     - filtered
     - 静态或运行时过滤器已将测试从待使用列表中排除。
     - ✓
     - ✓
   * - NOTRUN
     - not run
     - 测试在当前配置下不可运行，因此没有执行，但已成功构建。
     - ✓
     - ✓
   * - BLOCK
     - blocked
     - 测试因套件发生错误或崩溃而未运行。
     - ✕
     - ✓
   * - SKIP
     - skipped
     - 测试因上述情况之外的其他原因被跳过。
     - ✓
     - ✓
   * - ERROR
     - error
     - 执行测试本身时发生错误。
     - ✓
     - ✓
   * - FAIL
     - failed
     - 测试结果与预期不同。
     - ✓
     - ✓
   * - PASS
     - passed
     - 测试结果符合预期。
     - ✓
     - ✓

**代码中** 和 **文本中** 表示状态名称的使用场合：前者主要供 Twister 内部使用并出现在日志中，后者用于 JSON 报告。

.. note::

   Twister 还有两个内部状态：``NONE`` 是用例和套件的初始状态，``STARTED`` 表示用例正在执行。它们不应出现在最终报告中。报告文件出现这些非终态，说明 Twister 存在问题。


Case and Suite Status combinations
==================================

.. list-table:: 用例与套件的状态组合
   :widths: 22 13 13 13 13 13 13
   :align: center
   :header-rows: 1
   :stub-columns: 1

   * - ↓ 用例\套件 →
     - FILTER
     - ERROR
     - FAIL
     - PASS
     - NOTRUN
     - SKIP
   * - FILTER
     - ✓
     - ✕
     - ✕
     - ✕
     - ✕
     - ✕
   * - ERROR
     - ✕
     - ✓
     - ✕
     - ✕
     - ✕
     - ✕
   * - BLOCK
     - ✕
     - ✓
     - ✓
     - ✕
     - ✕
     - ✕
   * - FAIL
     - ✕
     - ✓
     - ✓
     - ✕
     - ✕
     - ✕
   * - PASS
     - ✕
     - ✓
     - ✓
     - ✓
     - ✕
     - ✕
   * - NOTRUN
     - ✕
     - ✕
     - ✕
     - ✕
     - ✓
     - ✕
   * - SKIP
     - ✕
     - ✓
     - ✓
     - ✓
     - ✕
     - ✓

✕ 表示正常 Twister 运行中不应出现的组合，即列所示状态的套件不应包含行所示状态的用例。

✓ 表示有效组合。

各套件状态的详细说明
--------------------

``FILTER``：
  表示整个套件已被本次 Twister 运行的静态过滤器排除，因此其中所有用例也应为该状态。

``ERROR``：
  套件执行测试时遇到问题，至少有一个用例为 ``ERROR`` 或 ``BLOCK``。此状态优先于所有其他用例状态，因此该套件中可包含任意有效终态的用例。

``FAIL``：
  套件中至少一个用例未满足其断言。在未满足 ERROR 条件时，此状态优先于其他用例状态。

``PASS``：
  套件正常通过，不得包含 ``BLOCK``、``ERROR`` 或 ``FAIL`` 用例，因为这些状态表示套件运行有问题。

``NOTRUN``：
  整个套件仅构建而未运行，因此其中所有用例都必须未运行。可运行性按套件决定，所以其用例只适用 ``NOTRUN``。

``SKIP``：
  整个套件在运行时被跳过，所有用例也必须为 ``SKIP``。
