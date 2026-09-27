.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_lz4:

LZ4——极速压缩
#############

简介
****

LZ4 是无损压缩算法，单核压缩速度超过 500 MB/s，并可随多核 CPU 扩展。其解码器速度极快，单核可达每秒数 GB，在多核系统上通常可达到 RAM 速度上限。

可以通过选择“加速”因子动态调整速度，以压缩率换取更高速度。另一端还提供高压缩率变体 LZ4_HC，以更多 CPU 时间换取更好的压缩率。所有版本的解压速度相同。

LZ4 的 API 和 CLI 均支持字典压缩。它可以将任意输入文件作为字典，但只使用最后 64KB。此能力还可以与其他能力组合使用。


在 Zephyr 中使用
****************

要将 lz4 作为 Zephyr 模块引入，可以在 ``west.yaml`` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/lz4.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: lz4
         url: https://github.com/zephyrproject-rtos/lz4
         revision: zephyr
         path: modules/lib/lz4 # adjust the path as needed

详细说明和 API 文档见 `lz4 documentation`_ 及随附的 `lz4 examples`_。


参考资料
********

.. _lz4 documentation:
    https://github.com/lz4/lz4/tree/dev/doc

.. _lz4 examples:
   https://github.com/zephyrproject-rtos/lz4/tree/zephyr/zephyr/samples
