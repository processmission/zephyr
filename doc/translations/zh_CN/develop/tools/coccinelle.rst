.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _coccinelle:

..
   Copyright 2010 Nicolas Palix <npalix@diku.dk>
   Copyright 2010 Julia Lawall <julia.lawall@lip6.fr>
   Copyright 2010 Gilles Muller <Gilles.Muller@lip6.fr>

Coccinelle
##########

Coccinelle 是模式匹配与文本转换工具，在内核开发中用途广泛，包括应用复杂的全树补丁，以及检测有问题的编程模式。

.. note::
   支持 Linux 和 macOS 开发环境，不支持 Windows。

获取 Coccinelle
***************

内核附带的语义补丁使用 Coccinelle 1.0.0-rc11 及更新版本提供的功能和选项。由于 Coccinelle 文件和 ``coccicheck`` 使用的选项名称已更新，使用更早版本会失败。

许多发行版的包管理器都提供 Coccinelle，例如：

.. rst-class:: rst-columns

   * Debian
   * Fedora
   * Ubuntu
   * OpenSUSE
   * Arch Linux
   * NetBSD
   * FreeBSD

某些发行版的软件包已过时，建议使用 Coccinelle 主页 https://coccinelle.lip6.fr/ 发布的最新版本。

也可以从 GitHub 获取：

https://github.com/coccinelle/coccinelle

获取源码后，运行以下命令：

.. code-block:: console

   ./autogen
   ./configure
   make

以上命令以普通用户身份运行，再通过以下命令安装：

.. code-block:: console

   sudo make install

从源码构建的详细安装说明见：

https://github.com/coccinelle/coccinelle/blob/master/install.txt

补充文档
********

语义补丁语言（SmPL）语法文档见：

https://coccinelle.gitlabpages.inria.fr/website/documentation.html

在 Zephyr 上使用 Coccinelle
***************************

``coccicheck`` 检查器是 Coccinelle 基础设施的前端，提供多种模式：

四种基本模式为 ``patch``、``report``、``context`` 和 ``org``，通过 ``--mode=<mode>`` 或 ``-m=<mode>`` 指定。

* ``patch``：在可能时提出修复。

* ``report``：按 file:line:column-column: message 格式生成列表。

* ``context``：以类似 diff 的形式突出显示相关行及其上下文，相关行用 ``-`` 标记。

* ``org``：生成 Emacs Org mode 格式报告。

注意，并非每个语义补丁都实现所有模式。为便于使用，默认模式为 ``report``。

另外两种模式提供常用组合：

- ``chain``：按上述顺序尝试各模式，直到某个模式成功。

- ``rep+ctxt``：依次运行 report 和 context 模式，应配合后文介绍的 C 选项使用，按文件检查代码。

示例
****

要为每个语义补丁生成报告，运行：

.. code-block:: console

   ./scripts/coccicheck --mode=report

生成补丁，运行：

.. code-block:: console

   ./scripts/coccicheck --mode=patch

``coccicheck`` 目标将 ``scripts/coccinelle`` 子目录中的所有语义补丁应用到整个源码树。

每个语义补丁都会给出建议的提交说明，描述其检查的问题，并引用 Coccinelle。

与任何静态代码分析器一样，Coccinelle 会产生误报，因此必须仔细检查报告并审查补丁。

设置 ``--verbose=1`` 可启用详细消息，例如：

.. code-block:: console

   ./scripts/coccicheck --mode=report --verbose=1

Coccinelle 并行化
*****************

默认情况下，``coccicheck`` 会尽可能并行运行。通过 ``--jobs=<number>`` 调整并行度，例如使用 4 个 CPU：

.. code-block:: console

   ./scripts/coccicheck --mode=report --jobs=4

从 1.0.2 起，Coccinelle 使用 OCaml parmap 并行化。检测到相关支持后，即可利用 parmap 并行执行。

启用 parmap 后，``coccicheck`` 会通过 ``--chunksize 1`` 启用动态负载均衡，逐个向线程分派工作，避免大部分工作落在少数线程上。线程提前完成时，会继续获得更多工作。

启用 parmap 后，Coccinelle 发生错误时，错误值会向上传递，并由 ``coccicheck`` 命令返回。

使用单个语义补丁
****************

``--cocci`` 选项可用于检查单个语义补丁，此时其值必须为要应用的语义补丁名称。

例如：

.. code-block:: console

   ./scripts/coccicheck --mode=report --cocci=<example.cocci>

或者：

.. code-block:: console

   ./scripts/coccicheck --mode=report --cocci=./path/to/<example.cocci>


控制 Coccinelle 处理的文件
**************************

默认检查整个源码树。

要只处理特定目录，将目录路径作为参数传入。

例如，检查 ``drivers/usb/``：

.. code-block:: console

   ./scripts/coccicheck --mode=patch drivers/usb/

默认模式为 ``report``，可通过前述 ``--mode=<mode>`` 选择其他模式。

调试 Coccinelle SmPL 补丁
*************************

最好使用 ``coccicheck``，因为它会为 spatch 命令提供与内核编译一致的包含选项。通过详细输出可查看这些选项，再手动运行 Coccinelle 并添加调试选项。

也可以通过保留标准错误输出来调试 Coccinelle 对 SmPL 补丁的处理。默认标准错误被重定向到 /dev/null；要捕获它，可向 ``coccicheck`` 传入 ``--debug=file.err``，例如：

.. code-block:: console

   rm -f cocci.err
   ./scripts/coccicheck --mode=patch --debug=cocci.err
   cat cocci.err

仅 Coccinelle 1.0.2 及更新版本支持调试。

附加标志
********

可通过 SPFLAGS 变量向 spatch 传递附加标志。选项冲突时，Coccinelle 采用最后传入的标志，因此可以这样覆盖。

.. code-block:: console

   ./scripts/coccicheck --sp-flag="--use-glimpse"

Coccinelle 还支持 idutils，但要求版本至少为 1.0.6。未指定 ID 文件时，默认数据库为内核顶层的 .id-utils.index。Coccinelle 附带 scripts/idutils_index.sh 脚本，可通过以下方式创建数据库：

.. code-block:: console

   mkid -i C --output .id-utils.index

如果数据库使用其他文件名，也可以创建使用此名称的符号链接。

.. code-block:: console

   ./scripts/coccicheck --sp-flag="--use-idutils"

也可以明确指定数据库文件名，例如：

.. code-block:: console

   ./scripts/coccicheck --sp-flag="--use-idutils /full-path/to/ID"

有时由于定义不足，Coccinelle 无法识别或解析复杂宏变量。为使其可解析，可通过 ``---macro-file-builtins <headerfile.h>`` 标志显式提供复杂宏的原型。

``<headerfile.h>`` 应包含复杂宏的完整原型，供 spatch 引擎提取转换所需的类型信息。

例如：

Coccinelle 无法识别 ``Z_SYSCALL_HANDLER``，因此将其原型放入头文件，例如 ``mymacros.h``。

.. code-block:: console

   $ cat mymacros.h
   #define Z_SYSCALL_HANDLER int xxx

然后在转换时传入 ``mymacros.h`` 头文件：

.. code-block:: console

   ./scripts/coccicheck --sp-flag="---macro-file-builtins mymacros.h"

spatch 选项详情见 ``spatch --help``。

注意，``--use-glimpse`` 和 ``--use-idutils`` 需要外部工具为代码建立索引，因此默认均未启用。不过，使用这些工具之一建立索引后，视 cocci 文件而定，spatch 可能更快地处理整个代码库。


SmPL 补丁专用选项
*****************

SmPL 补丁可能对传给 Coccinelle 的选项有特定要求，可以将专用选项写在补丁顶部，例如：

.. code-block:: console

   // Options: --no-includes --include-headers

提出新的语义补丁
****************

内核开发者可以提出并提交新的语义补丁。为保持清晰，应按类别放在 ``scripts/coccinelle/`` 子目录中。

cocci 脚本应具有以下属性：

* 脚本 **必须** 提供 ``report`` 模式。

* 开头几行应使用 ``///`` 注释说明脚本用途。基于脚本提出补丁时，通常用这段说明作为提交日志。

示例
====

.. code-block:: console

   /// Use ARRAY_SIZE instead of dividing sizeof array with sizeof an element

* 更详细的脚本信息，包括特殊情况或可能的误报，可通过 ``//#`` 注释列出。

Example
=======

.. code-block:: console

   //# This makes an effort to find cases where ARRAY_SIZE can be used such as
   //# where there is a division of sizeof the array by the sizeof its first
   //# element or by any indexed element or the element type. It replaces the
   //# division of the two sizeofs by ARRAY_SIZE.

* Confidence：表示脚本准确程度的属性，根据观察到的误报数量设为 ``High``、``Moderate`` 或 ``Low``。

Example
=======

.. code-block:: console

   // Confidence: High

* 虚拟规则：用于支持脚本提供的各种模式。脚本中指定的虚拟规则应有对应的模式处理规则。

Example
=======

.. code-block:: console

   virtual context

   @depends on context@
   type T;
   T[] E;
   @@
   (
   * (sizeof(E)/sizeof(*E))
   |
   * (sizeof(E)/sizeof(E[...]))
   |
   * (sizeof(E)/sizeof(T))
   )

``report`` 模式详解
*******************

``report`` 按以下格式生成列表：

.. code-block:: console

   file:line:column-column: message

Example
=======

运行：

.. code-block:: console

   ./scripts/coccicheck --mode=report --cocci=scripts/coccinelle/array_size.cocci

将执行 SmPL 脚本中的以下部分：

.. code-block:: console

   <smpl>

   @r depends on (org || report)@
   type T;
   T[] E;
   position p;
   @@
   (
   (sizeof(E)@p /sizeof(*E))
   |
   (sizeof(E)@p /sizeof(E[...]))
   |
   (sizeof(E)@p /sizeof(T))
   )

   @script:python depends on report@
   p << r.p;
   @@

   msg="WARNING: Use ARRAY_SIZE"
   coccilib.report.print_report(p[0], msg)

   </smpl>

此 SmPL 片段向标准输出生成如下条目：

.. code-block:: console

   ext/hal/nxp/mcux/drivers/lpc/fsl_wwdt.c:66:49-50: WARNING: Use ARRAY_SIZE
   ext/hal/nxp/mcux/drivers/lpc/fsl_ctimer.c:74:53-54: WARNING: Use ARRAY_SIZE
   ext/hal/nxp/mcux/drivers/imx/fsl_dcp.c:944:45-46: WARNING: Use ARRAY_SIZE


``patch`` 模式详解
******************

提供 ``patch`` 模式时，会为每个发现的问题提出修复。

Example
=======

运行：

.. code-block:: console

   ./scripts/coccicheck --mode=patch --cocci=scripts/coccinelle/misc/array_size.cocci

将执行 SmPL 脚本中的以下部分：

.. code-block:: console

   <smpl>

   @depends on patch@
   type T;
   T[] E;
   @@
   (
   - (sizeof(E)/sizeof(*E))
   + ARRAY_SIZE(E)
   |
   - (sizeof(E)/sizeof(E[...]))
   + ARRAY_SIZE(E)
   |
   - (sizeof(E)/sizeof(T))
   + ARRAY_SIZE(E)
   )

   </smpl>

此 SmPL 片段向标准输出生成如下补丁块：

.. code-block:: console

   diff -u -p a/ext/lib/encoding/tinycbor/src/cborvalidation.c b/ext/lib/encoding/tinycbor/src/cborvalidation.c
   --- a/ext/lib/encoding/tinycbor/src/cborvalidation.c
   +++ b/ext/lib/encoding/tinycbor/src/cborvalidation.c
   @@ -325,7 +325,7 @@ static inline CborError validate_number(
   static inline CborError validate_tag(CborValue *it, CborTag tag, int flags, int recursionLeft)
   {
     CborType type = cbor_value_get_type(it);
   -    const size_t knownTagCount = sizeof(knownTagData) / sizeof(knownTagData[0]);
   +    const size_t knownTagCount = ARRAY_SIZE(knownTagData);
      const struct KnownTagData *tagData = knownTagData;
      const struct KnownTagData * const knownTagDataEnd = knownTagData + knownTagCount;

``context`` 模式详解
********************

``context`` 以类似 diff 的形式突出显示相关行及其上下文。

.. note::
 生成的类 diff 输出并非可应用的补丁。``context`` 模式旨在突出显示重要行（以减号 ``-`` 标记），并提供周围上下文。可以使用 Emacs 的 diff 模式审查此输出中的代码。

Example
=======

运行：

.. code-block:: console

   ./scripts/coccicheck --mode=context --cocci=scripts/coccinelle/array_size.cocci

将执行 SmPL 脚本中的以下部分：

.. code-block:: console

   <smpl>

   @depends on context@
   type T;
   T[] E;
   @@
   (
   * (sizeof(E)/sizeof(*E))
   |
   * (sizeof(E)/sizeof(E[...]))
   |
   * (sizeof(E)/sizeof(T))
   )

   </smpl>

此 SmPL 片段向标准输出生成如下 diff 块：

.. code-block:: console

   diff -u -p ext/lib/encoding/tinycbor/src/cborvalidation.c /tmp/nothing/ext/lib/encoding/tinycbor/src/cborvalidation.c
   --- ext/lib/encoding/tinycbor/src/cborvalidation.c
   +++ /tmp/nothing/ext/lib/encoding/tinycbor/src/cborvalidation.c
   @@ -325,7 +325,6 @@ static inline CborError validate_number(
   static inline CborError validate_tag(CborValue *it, CborTag tag, int flags, int recursionLeft)
   {
     CborType type = cbor_value_get_type(it);
   -    const size_t knownTagCount = sizeof(knownTagData) / sizeof(knownTagData[0]);
      const struct KnownTagData *tagData = knownTagData;
      const struct KnownTagData * const knownTagDataEnd = knownTagData + knownTagCount;

``org`` 模式详解
****************

``org``：生成 Emacs Org mode 格式报告。

Example
=======

运行：

.. code-block:: console

   ./scripts/coccicheck --mode=org --cocci=scripts/coccinelle/misc/array_size.cocci

将执行 SmPL 脚本中的以下部分：

.. code-block:: console

   <smpl>

   @r depends on (org || report)@
   type T;
   T[] E;
   position p;
   @@
   (
   (sizeof(E)@p /sizeof(*E))
   |
   (sizeof(E)@p /sizeof(E[...]))
   |
   (sizeof(E)@p /sizeof(T))
   )

   @script:python depends on org@
   p << r.p;
   @@
   coccilib.org.print_todo(p[0], "WARNING should use ARRAY_SIZE")

   </smpl>

此 SmPL 片段向标准输出生成如下 Org 条目：

.. code-block:: console

   * TODO [[view:ext/lib/encoding/tinycbor/src/cborvalidation.c::face=ovl-face1::linb=328::colb=52::cole=53][WARNING should use ARRAY_SIZE]]

Coccinelle 邮件列表
*******************

订阅 Coccinelle 邮件列表：

* https://systeme.lip6.fr/mailman/listinfo/cocci

归档：

* https://lore.kernel.org/cocci/
* https://systeme.lip6.fr/pipermail/cocci/
