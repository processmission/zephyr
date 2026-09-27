.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _sparse:

Sparse 支持
###########

`Sparse <https://www.kernel.org/doc/html/latest/dev-tools/sparse.html>`__ 是静态代码分析工具。除常规分析外，它支持 ``address_space`` 属性，可在 C 代码中引入不同地址空间，并验证不同地址空间的指针没有混淆。它还支持 ``force`` 属性，用于在不同地址空间之间转换指针。目前 Zephyr 定义了一个自定义地址空间 ``__cache``，用于识别 Xtensa 架构中缓存地址范围内的指针，从而发现混淆缓存和非缓存地址的情况。

使用 sparse 运行
****************

执行 sparse 验证构建时，调用 :ref:`west build <west-building>` 并传入 ``-DZEPHYR_SCA_VARIANT=sparse``，例如：

.. code-block:: shell

    west build -d hello -b intel_adsp/cavs25 zephyr/samples/hello_world -- -DZEPHYR_SCA_VARIANT=sparse
