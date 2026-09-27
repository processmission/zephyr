.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_wamr:

WebAssembly 微型运行时（WAMR）
##############################

简介
****

`WebAssembly Micro Runtime`_ （WAMR）是面向嵌入式及资源受限设备的轻量级独立 WebAssembly 运行时。应用可以在运行时加载和执行 WebAssembly（WASM）模块，从而无需重新烧录固件即可更新或扩展功能，并让不受信任的代码在 WASM 规范定义的沙箱中运行。运行时 API、执行模式及 ``wamrc`` AOT 编译器的说明见 `WAMR documentation`_。

WAMR 通过专用平台层支持 Zephyr，并在自身仓库中提供模块适配文件 ``zephyr/module.yml``、``zephyr/Kconfig`` 和 ``zephyr/CMakeLists.txt``。因此，应用只需选择几个 Kconfig 选项，即可将运行时链接到映像中。

WAMR 采用附带 LLVM 例外条款的 Apache License 2.0。

在 Zephyr 中使用
****************

要将 WAMR 作为 Zephyr 模块使用，添加以下条目：

.. code-block:: yaml

   manifest:
     projects:
       - name: wasm-micro-runtime
         url: https://github.com/wasm-micro-runtime/wasm-micro-runtime
         revision: main
         path: modules/wasm-micro-runtime # adjust the path as needed

将其加入 Zephyr 子清单，例如 ``zephyr/submanifests/wamr.yaml``，并运行 ``west update``；也可以将其作为 West 项目加入项目的 ``west.yml`` 清单。

配置运行时
==========

运行时默认禁用。在应用的 ``prj.conf`` 中，使用 ``CONFIG_WAMR_*`` 选项启用它并选择所需功能：

.. code-block:: cfg

   CONFIG_WAMR=y
   CONFIG_WAMR_INTERP=y
   CONFIG_WAMR_AOT=y
   CONFIG_WAMR_LIBC_BUILTIN=y
   CONFIG_WAMR_GLOBAL_HEAP_POOL=y
   CONFIG_WAMR_GLOBAL_HEAP_SIZE=131072

每个选项都映射到常规 WAMR 构建脚本使用的对应 ``WAMR_BUILD_*`` CMake 变量。进行一次性构建时，仍可通过 CMake 命令行覆盖这些值，例如 ``-DWAMR_BUILD_AOT=0``。

``WAMR_BUILD_TARGET`` 根据开发板架构推导，通常无需显式传入。

WAMR 附带一组 `Zephyr samples`_，构建和运行方式见各自的 ``README.md``。

参考资料
********

.. target-notes::

.. _WebAssembly Micro Runtime:
   https://github.com/wasm-micro-runtime/wasm-micro-runtime

.. _WAMR documentation:
   https://github.com/wasm-micro-runtime/wasm-micro-runtime/tree/main/doc

.. _Zephyr samples:
   https://github.com/wasm-micro-runtime/wasm-micro-runtime/tree/main/product-mini/platforms/zephyr
