.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _no-west:

不使用 west 的 Zephyr 开发
##########################

本页介绍不使用 west 时如何使用 Zephyr。由于需要额外工作，不建议初学者采用此方式。具体而言，需要手动完成以下功能：

- 克隆 Zephyr 使用的主 zephyr 仓库之外的其他源代码仓库，并保持更新
- 向 Zephyr 构建系统指定这些仓库的位置
- 在不必详细了解相关主机工具用法的情况下进行烧录和调试

.. note::

   如果之前安装了 west，现在希望停止使用，请先卸载：

   .. code-block:: console

      pip3 uninstall west

   否则，Zephyr 构建系统会找到它，并可能尝试使用它。

获取源代码
----------

除下载 zephyr 源代码仓库本身外，还需要手动克隆仓库内 :term:`west manifest` 文件中列出的其他项目。

.. code-block:: console

   mkdir zephyrproject
   cd zephyrproject
   git clone https://github.com/zephyrproject-rtos/zephyr
   # clone additional repositories listed in zephyr/west.yml,
   # and check out the specified revisions as well.

拉取 zephyr 仓库中的改动时，也需要维护这些附加仓库，按需添加新仓库，并将现有仓库更新至最新修订版本。

构建应用程序
------------

如果手动指定所有模块，就可以在未安装 west 的情况下，直接使用 CMake 和 Ninja（或 make）构建 Zephyr 应用程序。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :tool: cmake
   :goals: build
   :gen-args: -DZEPHYR_MODULES=module1;module2;...
   :compact:

安装 west 后进行构建时，Zephyr 构建系统会使用它设置 :ref:`ZEPHYR_MODULES <important-build-vars>`。

如果未安装 west，且应用程序不需要这些仓库，构建仍然可以正常进行。

如果未安装 west，而应用程序 *确实* 需要其中某个仓库，就必须按上文所示自行设置 :makevar:`ZEPHYR_MODULES`。

更多详情参见 :ref:`modules`。

同样，如果应用程序需要二进制 blob，而你不使用 west，就需要自行下载并将这些 blob 放到正确位置，不能使用 ``west blobs``。更多详情参见 :ref:`bin-blobs`。

烧录与调试
----------

烧录和调试通过 ``west flash``、``west debug``、``west debugserver``、``west attach`` 和 ``west rtt`` 命令完成，详见 :ref:`west-build-flash-debug`。这些命令需要 west，因此不使用 west 时无法使用它们。

不使用 west 时，仍可通过适用于开发板的任意 :ref:`flash-debug-host-tools` 进行烧录和调试（上述 west 命令也只是包装这些工具），但必须自行调用，并传入适合开发板和应用程序的选项。
