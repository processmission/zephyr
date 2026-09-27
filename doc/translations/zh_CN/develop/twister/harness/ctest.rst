.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _twister_ctest_harness:

Ctest
#####

ctest_args: <list of arguments>（默认为空）
    指定传给 ``ctest`` 的附加参数列表，例如 ``ctest_args: [‘--repeat until-pass:5’]``。可以多次传入 ``--ctest-args``，向 ctest 提供多个参数。
