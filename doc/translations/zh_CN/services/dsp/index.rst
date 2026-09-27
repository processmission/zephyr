.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _zdsp_api:

数字信号处理（DSP）
###################

.. contents::
    :local:
    :depth: 2

DSP API 提供了一种与架构无关的信号处理方式。目前，该 API 可在任何架构上运行，但可能未针对具体架构进行优化。各架构的状态如下：

+--------------+---------------+
| 架构         | 状态          |
+==============+===============+
| ARC          | 已优化        |
+--------------+---------------+
| ARM          | 已优化        |
+--------------+---------------+
| ARM64        | 已优化        |
+--------------+---------------+
| MIPS         | 未优化        |
+--------------+---------------+
| POSIX        | 未优化        |
+--------------+---------------+
| RISCV        | 未优化        |
+--------------+---------------+
| RISCV64      | 未优化        |
+--------------+---------------+
| SPARC        | 未优化        |
+--------------+---------------+
| X86          | 未优化        |
+--------------+---------------+
| XTENSA       | 未优化        |
+--------------+---------------+

使用 zDSP
*********

zDSP 提供多种后端选项，这些选项会为应用自动选择。默认情况下，包含 CMSIS 模块将使所有架构都能使用 zDSP API。可以通过以下设置完成::

        CONFIG_CMSIS_DSP=y

如果你的应用需要一些额外的自定义，可以启用 :kconfig:option:`CONFIG_DSP_BACKEND_CUSTOM`，这意味着应用负责提供 zDSP 库的实现。

针对你的架构进行优化
********************

如果你的架构显示为 ``Unoptimized``，可以添加一个新的 zDSP 后端来更好地支持它。为此，需要向 :file:`subsys/dsp/Kconfig` 添加一个新的 Kconfig 选项，同时添加所需的依赖项，并为 ``DSP_BACKEND`` Kconfig 选择项设置 ``default``。

接下来，应在 ``subsys/dsp/<backend>/`` 处添加实现，并在 :file:`subsys/dsp/CMakeLists.txt` 中将其链接进来。要添加架构特定的属性，应将其对应的 Kconfig 选项添加到 :file:`subsys/dsp/Kconfig`，并使用这些属性更新 :file:`include/zephyr/dsp/dsp.h` 中的 ``DSP_DATA`` 和 ``DSP_STATIC_DATA``。

API 参考
********

.. doxygengroup:: math_dsp

.. _subsys/dsp/Kconfig: https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/dsp/Kconfig
.. _subsys/dsp/CMakeLists.txt: https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/dsp/CMakeLists.txt
.. _include/zephyr/dsp/dsp.h: https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/dsp/dsp.h
