.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _code-documentation:

代码文档
########

API 文档
********

完善的 API 文档能够提升开发者体验，也是 API 取得成功的基本条件。Doxygen 是一种通用文档工具，Zephyr 项目使用它编写 API 文档。它可以生成在线文档浏览页面（HTML 格式），也可以为其他工具提供输入，以便根据带有文档注释的源文件生成参考手册。其中，Doxygen 的 XML 输出用于生成 Zephyr 项目的在线文档。

引用需求
********

API 文档主要记录需求或宣称支持的功能的实现，并可追溯到相应功能。我们将 API 文档作为把实现追溯到已记录功能的主要入口。这通过 Doxygen 原生的需求可追溯性命令（ ``@satisfies`` 和 ``@verifies`` ）实现，这些命令引用在其他位置的需求目录中维护的需求。

测试文档
********

为了帮助理解各项测试的作用及其测试的功能，我们也使用相同的工具，在相同的上下文中为所有测试代码编写文档，并为同一环境中维护的所有单元测试和集成测试生成文档。测试文档通过链接到所验证的 API 并引用原始需求，来说明测试所验证的 API 或功能。


文档编写指南
************

测试代码
========

Zephyr 项目使用多种测试方法，其中最常用的是 :ref:`Ztest 框架 <test-framework>` 。只应为测试入口函数（通常以 test\\_ 为前缀）以及由 Ztest 框架直接调用的函数编写测试文档。这些测试将出现在测试报告中，使用其名称和标识符是识别测试并从需求追溯到测试的最佳方式。

测试文档不应干扰实际的 API 文档，需要采用新的结构以避免混淆。通过采用一致的命名规则和明确定义的结构，我们可以将这些文档归入独立的模块，并在解析测试数据以生成可追溯性报告时唯一识别它们。应遵循以下指南：

- 所有测试代码文档都应归入 ``all_tests`` Doxygen 组
- 所有测试文档都应归入以 tests\\_ 为前缀的 Doxygen 组

记录需求
========

使用 Doxygen 的 ``@requirement`` 命令记录需求，该命令接受一个唯一标识符和一个可选标题。Doxygen 将所有需求汇总到同一个页面，并允许在任意位置通过标识符引用需求。请使用专门用于该需求的注释块，通常在需求目录中维护::

    /**
    * @requirement ZEPH-015 (Give a semaphore)
    *
    * The kernel shall provide a mechanism to give a semaphore, increasing its
    * count up to its configured maximum.
    */

这里使用的标识符（例如 ``ZEPH-015`` ）与下文 ``@satisfies`` 和 ``@verifies`` 命令引用的标识符相同，由此将实现和测试关联到相应需求。

Doxygen 的 ``@verifies`` 命令表示某项测试验证了一项需求::

    /**
    * @brief Tests for the Semaphore kernel object
    * @defgroup kernel_semaphore_tests Semaphore
    * @ingroup all_tests
    * @{
    */

    ...
    /**
    * @brief A brief description of the tests
    * Some details about the test
    * more details
    *
    * @verifies ZEPH-015
    */
    void test_sema_thread2thread(void)
    {
    ...
    }
    ...

    /**
    * @}
    */

为了了解实现或某段代码对需求的满足情况，我们使用 Doxygen 的 ``@satisfies`` 命令::

    /**
    * @brief Give a semaphore.
    *
    * This routine gives @a sem, unless the semaphore is already at its maximum
    * permitted count.
    *
    * @note Can be called by ISRs.
    *
    * @param sem Address of the semaphore.
    *
    * @satisfies ZEPH-015
    */
    __syscall void k_sem_give(struct k_sem *sem);



要生成矩阵，首先需要构建文档，具体来说，需要生成 Doxygen 的 XML 输出::

   $ make doxygen

解析 Doxygen 生成的 XML 数据，以生成可追溯性矩阵。
