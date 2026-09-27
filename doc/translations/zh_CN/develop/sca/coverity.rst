.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _coverity:

Coverity
########

Coverity Scan 是 Black Duck 提供的服务，为在该服务注册项目的开源开发者提供开源项目分析结果。

此集成仅针对 scan.coverity.com 及该服务提供的工具发行版进行过测试。

生成构建数据文件
****************

使用此集成时，必须能在 :envvar:`PATH` 中找到 Coverity 工具，并在调用 :ref:`west build <west-building>` 时传入 ``-DZEPHYR_SCA_VARIANT=coverity``，例如：

.. code-block:: shell

    west build -b qemu_cortex_m3 samples/hello_world -- -DZEPHYR_SCA_VARIANT=coverity


扫描结果生成在 :file:`build/sca/coverity`。

也可以通过 :envvar:`COVERITY_OUTPUT_DIR` 指定多次扫描或增量扫描结果的存放目录。

结果分析
********

按照 https://scan.coverity.com 上的说明上传结果。
