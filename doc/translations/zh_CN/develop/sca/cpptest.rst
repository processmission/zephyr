.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _cpptest:

Parasoft C/C++test 支持
#######################

Parasoft `C/C++test <https://www.parasoft.com/products/parasoft-c-ctest/>`__ 是面向 C/C++ 的软件测试和静态分析工具。它是商业软件，使用前必须取得商业许可证。

C/C++test 文档位于 https://docs.parasoft.com/，使用方法请参阅该文档。

生成构建数据文件
****************

使用 C/C++test 时，必须能在 :envvar:`PATH` 中找到 ``cpptestscan``，并在调用 :ref:`west build <west-building>` 时传入 ``-DZEPHYR_SCA_VARIANT=cpptest``，例如：

.. code-block:: shell

    west build -b qemu_cortex_m3 zephyr/samples/hello_world -- -DZEPHYR_SCA_VARIANT=cpptest


将生成 ``.bdf`` 文件 :file:`build/sca/cpptest/cpptestscan.bdf`。

生成报告文件
************

更多信息请参阅 Parasoft C/C++test 文档。

可以使用类似以下方式导入并生成报告文件。

.. code-block:: shell

    cpptestcli -data out -localsettings local.conf -bdf build/sca/cpptest/cpptestscan.bdf -config "builtin://Recommended Rules" -report out/report


可能需要将 ``bdf.import.c.compiler.exec``、``bdf.import.cpp.compiler.exec`` 和 ``bdf.import.linker.exec`` 设置为 :ref:`west build <west-building>` 使用的工具链。
