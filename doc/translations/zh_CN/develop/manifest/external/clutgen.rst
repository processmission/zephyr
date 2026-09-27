.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_clutgen:

CLUTGen
#######

简介
****

`CLUTGen <clutgen-zephyr_>`_ 可自动为嵌入式系统创建 **查找表**，将 ADC 原始读数转换为经过校准的物理量，如温度、压力或距离。

给定一组校准样本后，CLUTGen 会拟合插值曲线，并生成可用于生产的 ``.c``/``.h`` 文件对，预先计算所有可能 ADC 读数对应的完整查找表。运行时，转换只需一次数组索引操作，因而可将 ``math.h`` 等库中代价较高的 RAM 操作，换成固定且可预测的 ROM 开销。

此 Zephyr 模块将 CLUTGen 直接集成到 west 构建系统中。查找表在 CMake 配置阶段生成，生成文件会自动链接到应用。


在 Zephyr 中使用
****************

在工作区清单中声明该模块，或通过子清单引入。

例如，创建 ``zephyrproject/zephyr/submanifests/clutgen.yaml``，内容如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: clutgen
         url: https://github.com/wkhadgar/clutgen-zephyr
         revision: zephyr
         path: modules/clutgen
         submodules: true

然后更新工作区，并将 Python 依赖安装到 west 虚拟环境中：

.. code-block:: sh

   west update
   west packages pip --install


参考资料
********

- `CLUTGen Zephyr module <clutgen-zephyr_>`_
- `CLUTGen CLI tool <clutgen-cli_>`_


.. _clutgen-zephyr: https://github.com/wkhadgar/clutgen-zephyr

.. _clutgen-cli: https://github.com/wkhadgar/clutgen
