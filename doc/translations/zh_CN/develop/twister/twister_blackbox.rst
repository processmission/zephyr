.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _twister_blackbox:

Twister 黑盒测试
################

本指南介绍测试文件结构，帮助读者理解现有文件并编写新测试。开发者应修复因自己的改动而失败的测试，并在引入新功能时添加测试，因此所有 Twister 开发者都应了解这些内容。

基础
****

Twister 黑盒测试使用 Python 和 ``pytest`` 库编写，详见 :ref:`此处 <integration_with_pytest>`。辅助测试数据保留原始格式。测试和数据全部位于 :zephyr_file:`scripts/tests/twister_blackbox`，名称以 ``test_`` 开头。

黑盒测试不应依赖 Twister 内部代码，而应像用户一样调用 Twister 并检查结果。

测试文件示例
************

.. literalinclude:: ./sample_blackbox_test.py
   :language: python
   :linenos:

与命令行比较
************

上面的测试运行以下命令：

.. code-block:: console

    twister -i --outdir $OUTDIR -T $TEST_DATA/tests -y --level $LEVEL
    --test-config $TEST_DATA/test_config.yaml -p qemu_x86 -p frdm_k64f

它假定命令行环境已执行 ``zephyr-env.sh`` 或 ``zephyr-env.cmd``。

借助 ``importlib`` 的 ``exec_module()`` [#f1]_，此测试可提供通常运行 Twister 时的全部输出。通过 ``args`` 变量 [#f2]_ 可方便地设置调用标志，并在 ``out`` 和 ``err`` 变量中检查标准输出和标准错误。

除标准输出外，还可检查通常位于 ``twister-out`` 目录中的文件输出。多数情况下会结合 ``out_path`` fixture 和 ``--outdir`` 标志（第 52 行），将测试生成的文件保存在临时目录。黑盒测试常读取 ``testplan.json``、``twister.xml`` 和 ``twister.log``。

其他功能
********

装饰器
======

* ``@pytest.mark.usefixtures('clear_log')``
    - 允许使用 ``conftest.py`` 中的 ``clear_log`` fixture。未来此 fixture 将改为 ``autouse``，届时可移除此装饰器。
* ``@pytest.mark.parametrize('level, expected_tests', TESTDATA_X, ids=['smoke', 'acceptance'])``
    - 这是 ``pytest`` 测试参数化示例，详见 `here <https://docs.pytest.org/en/7.1.x/example/parametrize.html#different-options-for-test-ids>`__。TESTDATA 通常声明为类字段。
* ``@mock.patch.object(TestPlan, 'TEST_DEFINITION_FILENAME', test_filename_mock)``
    - 此装饰器允许只使用 ``test_data`` 中定义的测试，忽略 ``tests`` 目录中的 Zephyr 用例。**注意，所有 test_data 测试使用的文件名是** ``test_data.yaml``，**不是** ``testcase.yaml``！``test_data`` 中的数据及 ``mock`` 库的更多说明见 `here <https://docs.python.org/3/library/unittest.mock.html>`__。

Fixture
=======

黑盒测试使用 ``pytest`` 的 fixture，更多介绍见 `here <https://docs.pytest.org/en/6.2.x/fixture.html>`__。

添加自己的 fixture 前，应考虑它只用于一个测试文件还是多个文件。

* 若用于多个文件，在 :zephyr_file:`scripts/tests/twister_blackbox/conftest.py` 中创建。

    - :zephyr_file:`scripts/tests/twister_blackbox/conftest.py` 已有一些 fixture，可作为参考。
* 若只用于一个文件，在该文件中声明。

    - 也可考虑改用类字段，参见 TESTDATA 示例。

如何……
******

在同一测试中多次调用 Twister？
==============================

有些测试需要先运行一次 Twister。例如，``--test-only`` 通常与前一次 ``--build-only`` 调用配合使用。该如何处理？

若直接调用两次 ``importlib`` 的 ``exec_module``，会导致日志重复。``twister.log`` 中每行会出现两次，调用三次则出现三次，而非覆盖日志或向末尾追加。

原因是 Twister 文件使用了模块级日志器变量，重新执行模块会使日志器拥有多个处理器。

为解决此问题，应在两次调用之间执行：

.. code:: python

    capfd.readouterr()   # To remove output from the buffer
                         # Note that if you want output from all runs after each other,
                         # skip this line.
    clear_log_in_test()  # To remove log duplication


------

.. rubric:: 脚注

.. [#f1] 注意类函数 ``setup_class()``，它允许像直接调用一样运行 ``twister`` Python 文件，绕过 ``__name__ == '__main__'`` 检查。

.. [#f2] 建议几乎所有测试都保留 ``args`` 定义的第一部分，因为它用于通用测试设置。
