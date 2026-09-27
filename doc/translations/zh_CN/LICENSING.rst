.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

:orphan:

.. _zephyr_licensing:

Zephyr 项目组件的许可
#####################

Zephyr 整体按 `Apache 2.0 License`_ 授权，但它导入或复用了一小部分受其他许可证约束的软件包、脚本和其他文件。某些情况下无法为这些文件添加许可证头，因此其许可信息以机器可读的形式集中声明在仓库根目录的 :zephyr_file:`REUSE.toml` 文件中（遵循 `REUSE specification`_）。

以下各节由该元数据 **自动生成**，因此始终反映代码树的实际状态。要添加、更新或删除条目，请编辑 :zephyr_file:`REUSE.toml` 中对应的 ``[[annotations]]`` 块，而不要修改本页（参见 :ref:`external-contributions`）。

.. note::

   本页只列出许可 *例外* 情况，并不定义 Zephyr 项目本身的许可证；Zephyr 项目本身按仓库根目录 :zephyr_file:`LICENSE` 文件中指定的 Apache 2.0 授权。

.. contents:: 已记录的组件
   :local:
   :depth: 1

.. zephyr-licensing-exceptions::

.. _Apache 2.0 License:
   https://github.com/zephyrproject-rtos/zephyr/blob/main/LICENSE

.. _REUSE specification:
   https://reuse.software/spec/
