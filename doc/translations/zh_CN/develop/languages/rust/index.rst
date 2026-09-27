.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _language_rust:

Rust 语言支持
#############

Rust 是一种现代系统编程语言，旨在不牺牲底层控制能力的前提下，提供内存安全、并发能力和性能。它通过独特的所有权模型，在编译期消除空指针解引用、数据竞争等常见错误。

Rust 重视安全性和正确性，尤其适合嵌入式系统及可靠性至关重要的环境。它无需运行时或垃圾收集器即可提供强大的抽象，使开发者能够可靠、高效地编写高层代码及底层硬件交互代码。

这些特性使 Rust 很适合资源受限、强调系统稳定性的 Zephyr 项目。

启用 Rust 支持
**************

要在 Zephyr 应用中启用 Rust 支持，需要完成以下工作：

1.  Rust 当前是可选模块，因此需要先启用模块。最简单的方法是使用 west：

    .. code-block:: shell

       west config manifest.project-filter +zephyr-lang-rust
       west update

    这会将 Rust 语言支持放到 Zephyr 工作区的 :samp:`modules/lang/rust` 中。

2.  在 :file:`prj.conf` 中通过 :kconfig:option:`CONFIG_RUST` 启用 Rust。最简单的方法是从 :module_file:`modules/lang/rust/samples <zephyr-lang-rust:samples>` 中的某个示例开始，这也包含下一步的 CMake 设置。

3.  配置应用的 :file:`CMakeLists.txt` 以支持 Rust。最简单的方法同样是从示例复制，大致如下：

    .. code-block:: cmake

       cmake_minimum_required(VERSION 3.28.0)

       find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

       project(my_app)
       rust_cargo_application()

4.  创建 :file:`Cargo.toml`，描述如何构建 Rust 应用。以下取自 Hello World 示例：

    .. code-block:: toml

       [package]
       # This must be rustapp for now.
       name = "rustapp"
       version = "0.1.0"
       edition = "2021"
       description = "The description of my app"
       license = "Apache-2.0 or MIT"

       [lib]
       crate-type = ["staticlib"]

       [dependencies]
       zephyr = "0.1.0"
       log = "0.4.22"

    唯一必需的依赖是 ``zephyr``，它提供用于与 Zephyr 交互的 zephyr crate。

5.  像构建其他 Zephyr 应用一样构建即可。目前只有少数目标支持 Rust，可在 :module_file:`modules/lang/rust/etc/platforms.txt <zephyr-lang-rust:etc/platforms.txt>` 文件中查看。

API 文档
********

模块最新版本的 `API 文档`_ 保存在 gh-pages 上。

.. _`API Documentation`:
   https://zephyrproject-rtos.github.io/zephyr-lang-rust/nostd/zephyr/index.html

该文档针对通用目标生成，并启用全部功能。有了可构建的应用后，可以为自己的目标生成专用文档：

.. code-block:: shell

   west build -t rustdoc

   ...

   Generated /my/path/app/zephyr/build/doc/rust/target/riscv32i-unknown-none-elf/doc/rustapp/index.html

可以在浏览器中打开最后输出的路径。顶层文档属于应用本身；在左侧边栏找到 zephyr crate，即可进入 Zephyr 文档。还会为应用直接或间接使用的所有依赖生成本地文档。
