.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _doc_guidelines:

文档准则
########

.. highlight:: rst

.. note::

   有关构建文档的说明，请参见 :ref:`zephyr_doc`。

Zephyr 项目的内容使用 `reStructuredText`_ 标记语言（.rst 文件扩展名）并配合 Sphinx 扩展编写，再通过 Sphinx 处理，生成格式化的独立网站。开发者可以以 .rst 标记文件的原始形式查看这些内容，也可以在安装 Sphinx 后 :ref:`在本地构建文档 <zephyr_doc>`，生成 HTML 或 PDF 格式的文档。随后可以使用 Web 浏览器查看 HTML 内容。同一份 .rst 内容也由 `Zephyr documentation`_ 网站提供。

你可以从各自的网站阅读关于 `reStructuredText`_ 和 `Sphinx extensions`_ 的详细信息。

.. _Sphinx extensions: https://www.sphinx-doc.org/en/stable/contents.html
.. _reStructuredText: https://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
.. _Sphinx Inline Markup:  https://sphinx-doc.org/markup/inline.html#inline-markup
.. _Zephyr documentation:  https://docs.zephyrproject.org

本文档为用于创建你正在阅读的文档的常用 reST 与 Sphinx 定义的指令和角色提供快速参考。

关于编写良好 C API 文档的说明，请参见 :ref:`doxygen_style`。

内容结构
********

制表符、空格与缩进
==================

在 reST 文件内容中，缩进非常重要，建议使用空格。额外的缩进也可能（在无意中）改变内容的渲染方式。对于列表和指令，请将内容文本缩进到与前一行中第一个非空白字符对齐。例如::

   * List item that spans multiple lines of text
     showing where to indent the continuation line.

   1. And for numbered list items, the continuation
      line should align with the text of the line above.

   .. code-block::

      The text within a directive block should align with the
      first character of the directive name.

其他要求请参见 Zephyr :ref:`编码风格 <coding_style>`。

.. _headings:

标题
====

虽然 reST 允许同时使用上划线和匹配的下划线来标识标题，但我们仅使用下划线来标识标题。

* 文档标题（h1）使用 ``#`` 作为下划线字符
* 第一节标题级别（h2）使用 ``*``
* 第二节标题级别（h3）使用 ``=``
* 第三节标题级别（h4）使用 ``-``

标题下划线的长度必须与标题文本相同。

例如::

   This is a title heading
   #######################

   some content goes here

   First section heading
   *********************


列表
====

对于项目符号列表，请在段首放置星号（``*``）或连字符（``-``），并使用两个空格缩进续行。

列表（或子列表）中的第一项之前必须有一个空行，并且应与前一段落保持相同的缩进级别（自身不缩进）。

对于编号列表，可以以 1. 或 a. 开头，并使用 ``#`` 号继续自动编号。续行使用三个空格缩进::

   * This is a bulleted list.
   * It has two items, the second
     item and has more than one line of reST text.  Additional lines
     are indented to the first character of the
     text of the bullet list.

   1. This is a new numbered list. If the wasn't a blank line before it,
      it would be a continuation of the previous list (or paragraph).
   #. It has two items too.

   a. This is a numbered list using alphabetic list headings
   #. It has three items (and uses autonumbering for the rest of the list)
   #. Here's the third item

   #. This is an autonumbered list (default is to use numbers starting
      with 1).

      #. This is a second-level list under the first item (also
         autonumbered).  Notice the indenting.
      #. And a second item in the nested list.
   #. And a second item back in the containing list.  No blank line
      needed, but it wouldn't hurt for readability.

定义列表（包含术语及其定义）是记录词语或短语并加以解释的便捷方式。例如以下 reST 内容::

   The Makefile has targets that include:

   html
      Build the HTML output for the project

   clean
      Remove all generated output, restoring the folders to a
      clean state.

将渲染为：

   该 Makefile 包含以下目标：

   html
      构建项目的 HTML 输出

   clean
      删除所有生成的文件，将文件夹恢复到干净状态。

多列列表
========

如果有一个较长的项目符号列表，且每一项都很短，可以用特殊的 ``.. rst-class:: rst-columns`` 指令指明列表项应以多列方式渲染。该指令将应用于下一个非注释元素（例如段落），或应用于该指令下缩进的内容。例如，以下无序列表::

   .. rst-class:: rst-columns

   * A list of
   * short items
   * that should be
   * displayed
   * horizontally
   * so it doesn't
   * use up so much
   * space on
   * the page

将渲染为：

.. rst-class:: rst-columns

   * 一个列表
   * 包含很短的项
   * 应当
   * 横向
   * 显示
   * 这样就不会
   * 在页面上
   * 占用
   * 太多空间

最多显示三列，并根据显示窗口的可用宽度变化，必要时在窄屏（手机）上缩减为一列。我们已弃用 ``hlist`` 指令，因为它在较小的屏幕上表现异常。

表格
====

有几种创建表格的方式，各有其限制或怪癖。`Grid tables <https://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#grid-tables>`_ 在定义合并行和列方面功能最强，但难以维护::

   +------------------------+------------+----------+----------+
   | Header row, column 1   | Header 2   | Header 3 | Header 4 |
   | (header rows optional) |            |          |          |
   +========================+============+==========+==========+
   | body row 1, column 1   | column 2   | column 3 | column 4 |
   +------------------------+------------+----------+----------+
   | body row 2             | ...        | ...      | you can  |
   +------------------------+------------+----------+ easily   +
   | body row 3 with a two column span   | ...      | span     |
   +------------------------+------------+----------+ rows     +
   | body row 4             | ...        | ...      | too      |
   +------------------------+------------+----------+----------+

此示例将渲染为：

+-----------------------------+--------------+------------+------------------+
| 表头行第 1 列（表头行可选） | 表头 2       | 表头 3     | 表头 4           |
+=============================+==============+============+==================+
| 正文行 1 第 1 列            | 第 2 列      | 第 3 列    | 第 4 列          |
+-----------------------------+--------------+------------+------------------+
| 正文行 2                    | ...          | ...        | 你也可以轻松跨行 |
+-----------------------------+--------------+------------+                  |
| 跨两列的正文行 3                           | ...        |                  |
+-----------------------------+--------------+------------+                  |
| 正文行 4                    | ...          | ...        |                  |
+-----------------------------+--------------+------------+------------------+

`List tables <https://docutils.sourceforge.net/docs/ref/rst/directives.html#list-table>`_ 维护起来容易得多，但不支持跨行或跨列::

   .. list-table:: Table title
      :widths: 15 20 40
      :header-rows: 1

      * - Heading 1
        - Heading 2
        - Heading 3
      * - body row 1, column 1
        - body row 1, column 2
        - body row 1, column 3
      * - body row 2, column 1
        - body row 2, column 2
        - body row 2, column 3

此示例将渲染为：

.. list-table:: 表格标题
   :widths: 15 20 40
   :header-rows: 1

   * - 标题 1
     - 标题 2
     - 标题 3
   * - body row 1, column 1
     - 正文行 1 第 2 列
     - 正文行 1 第 3 列
   * - 正文行 2 第 1 列
     - 正文行 2 第 2 列
     - 正文行 2 第 3 列

``:widths:`` 参数用于定义相对的列宽。默认各列等宽。如果表格有三列，希望第一列的宽度是另外两列（等宽）的一半，可以写成 ``:widths: 1 2 2``。如果希望浏览器根据列内容自动设置列宽，可以使用 ``:widths: auto``。

选项卡内容
==========

如 :ref:`getting_started` 中所介绍，你可以通过选项卡界面向读者提供备选内容。读者点击某个选项卡时，就会显示该选项卡的内容，例如::

   .. tabs::

      .. tab:: Apples

         Apples are green, or sometimes red.

      .. tab:: Pears

         Pears are green.

      .. tab:: Oranges

         Oranges are orange.

将显示为：

.. tabs::

   .. tab:: 苹果

      苹果是绿色的，有时是红色的。

   .. tab:: 梨

      梨是绿色的。

   .. tab:: 橙子

      橙子是橙色的。

选项卡也可以分组，这样在一个区域中更改当前选项卡时，页面上所有同名选项卡都会随之更改。例如：

.. tabs::

   .. group-tab:: Linux

      Linux 第 1 行

   .. group-tab:: macOS

      macOS 第 1 行

   .. group-tab:: Windows

      Windows 第 1 行

.. tabs::

   .. group-tab:: Linux

      Linux 第 2 行

   .. group-tab:: macOS

      macOS 第 2 行

   .. group-tab:: Windows

      Windows 第 2 行

在后一种情况下，我们使用 ``.. group-tab::`` 而不是简单的 ``.. tab::``。在底层，我们使用了 Zephyr 环境中包含的 `sphinx-tabs <https://github.com/executablebooks/sphinx-tabs>`_ 扩展。在选项卡内，除了 *标题* 之外，你可以包含大多数内容（code-block、有序和无序列表、图片、段落等）。你可以通过上面的链接了解更多关于 sphinx-tabs 的信息。


文本格式化
**********

reStructuredText 支持多种文本格式化选项。本节为 Zephyr 文档中最常用的一些文本格式化选项提供快速参考。完整列表请参考 `reStructuredText Quick Reference`_、`reStructuredText Interpreted Text Roles`_ 以及 `additional roles provided by Sphinx`_。

.. _reStructuredText Quick Reference: https://docutils.sourceforge.io/docs/user/rst/quickref.html
.. _reStructuredText Interpreted Text Roles: https://docutils.sourceforge.io/docs/ref/rst/roles.html
.. _additional roles provided by Sphinx: https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html

内容高亮
========

一些常见的 reST 行内标记示例：

* 一个星号：``*text*`` 表示强调（*斜体*），
* 两个星号：``**text**`` 表示强烈强调（**粗体**），以及
* 两个反引号：````text```` 用于 ``inline code`` 示例。

如果星号或反引号出现在正文中，并可能与行内标记分隔符混淆，可以在其前面添加反斜杠（``\``）来消除混淆。

文件名与命令
============

Sphinx 扩展了 reST，支持额外的行内标记元素（称为“角色”），用于为文本赋予特殊含义并允许输出格式化的样式。（完整列表可参考 `Sphinx Inline Markup`_ 文档）。

虽然可以使用双引号将文本渲染为“代码”，但推荐使用以下角色来标记文件名、命令名和其他“特殊”文本。

* :rst:role:`file` 用于文件名，例如 ``:file:`CMakeLists.txt``` 会渲染为 :file:`CMakeLists.txt`

  .. note::

     如果要表示“variable”（可变）文件路径，可以用花括号把路径中的可变部分括起来，例如 ``:file:`{boardname}_defconfig``` 会渲染为 :file:`{boardname}_defconfig`。

* :rst:role:`command` 用于命令名，例如 ``:command:`make``` 会渲染为 :command:`make`

* :rst:role:`envvar` 用于环境变量，例如 ``:envvar:`ZEPHYR_BASE``` 会渲染为 :envvar:`ZEPHYR_BASE`

关于创建指向 Zephyr 组织在 GitHub 上托管的文件的引用，请参见下文的 :ref:`linking_to_zephyr_files` 一节。

用户交互
========

在记录用户交互（例如组合键或 GUI 交互）时，请使用以下角色以有意义的方式突出显示这些命令：

* :rst:role:`kbd` 用于键盘输入，例如 ``:kbd:`Ctrl-C``` 会渲染为 :kbd:`Ctrl-C`

* :rst:role:`menuselection` 用于菜单选择，例如 ``:menuselection:`File --> Open``` 会渲染为 :menuselection:`File --> Open`

* :rst:role:`guilabel` 用于 GUI 标签，例如 ``:guilabel:`Cancel``` 会渲染为 :guilabel:`Cancel`

数学公式
========

你可以使用 :rst:role:`math` 角色或 :rst:dir:`math` 指令来包含数学公式。如果公式较为复杂，使用指令会提供更大的灵活性。

数学公式的输入语言是 LaTeX 标记。例如::

   The answer to life, the universe, and everything is :math:`30 + 2^2 + \sqrt{64} = 42`.

将渲染为：

   生命、宇宙以及一切的终极答案是 :math:`30 + 2^2 + \sqrt{64} = 42`。

非 ASCII 字符
=============

除非为了正确性或约定俗成的排版而需要特定符号（例如 µ 这样的单位，或 ™ 这样的公知标记），否则请优先使用纯 ASCII。

避免纯粹为了美观而添加非 ASCII 字符。

:zephyr_file:`doc/substitutions.txt` 文件包含一些用于特殊格式需求（例如强制换行）的基本 HTML 替换定义，但 Unicode 字符可以也应该直接用在文档源文件中。

代码块与命令示例
================

使用 reST 的 :rst:dir:`code-block` 指令可创建带高亮的等宽文本块，通常用于展示格式化的代码或控制台命令及其输出。它还支持智能语法高亮（使用 Pygments 包）。你也可以直接指定高亮语言。例如::

   .. code-block:: c

      struct k_object {
         char *name;
         uint8_t perms[CONFIG_MAX_THREAD_BYTES];
         uint8_t type;
         uint8_t flags;
         uint32_t data;
      } __packed;

请注意 :rst:dir:`code-block` 指令与代码块正文第一行之间的空行，正文内容缩进三个空格（缩进到指令名的第一个非空白字符处）。

将渲染为：

   .. code-block:: c

      struct k_object {
         char *name;
         uint8_t perms[CONFIG_MAX_THREAD_BYTES];
         uint8_t type;
         uint8_t flags;
         uint32_t data;
      } __packed;


当然也支持其他语言（参见 `languages supported by Pygments`_），特别鼓励你在合适的时候使用以下语言：

.. _`languages supported by Pygments`: https://pygments.org/languages/

* ``c`` 用于 C 代码
* ``cpp`` 用于 C++ 代码
* ``python`` 用于 Python 代码
* ``console`` 用于控制台输出，即交互式 shell 会话：其中的命令带有提示符前缀（例如 Linux 的 ``$``，或 Zephyr shell 的 ``uart:~$``），并且同时显示输出。命令会被高亮，而输出不会。此外，使用“copy”按钮复制代码块时，只会自动复制命令，不包括提示符和命令的输出。
* ``shell`` 或 ``bash`` 用于 shell 命令。两种语言的高亮效果相同，但你可以用 ``bash`` 表示命令是 bash 特有的，用 ``shell`` 表示通用的 shell 命令。

  .. note::

     如果你的代码块中包含提示符，请不要使用 ``bash`` 或 ``shell``，而应改用 ``console``。

     反之，如果你的代码块不包含提示符，也不是在展示带命令及其输出的交互式会话，请不要使用 ``console``。

     .. list-table:: 何时使用 ``bash``/``shell`` 与 ``console``
        :class: wrap-normal
        :header-rows: 1
        :widths: 20,40,40

        * - 使用场景
          - ``code-block`` 片段
          - 预期输出

        * - 一条或多条命令，无输出

          - .. code-block:: rst

               .. code-block:: shell

                  echo "Hello World!"

          - .. code-block:: shell

               echo "Hello World!"

        * - 带命令及其输出的交互式 shell 会话

          - .. code-block:: rst

               .. code-block:: console

                  $ echo "Hello World!"
                  Hello World!

          - .. code-block:: console

               $ echo "Hello World!"
               Hello World!

        * - 带命令及其输出的交互式 Zephyr shell 会话

          - .. code-block:: rst

               .. code-block:: console

                  uart:~$ version
                  Zephyr version 3.5.99
                  uart:~$ kernel uptime
                  Uptime: 20970 ms

          - .. code-block:: console

               uart:~$ version
               Zephyr version 3.5.99
               uart:~$ kernel uptime
               Uptime: 20970 ms

* ``bat`` 用于 Windows 批处理文件
* ``cfg`` 用于包含“KEY=value”条目的配置文件（例如 Kconfig ``.conf`` 文件）
* ``cmake`` 用于 CMake
* ``devicetree`` 用于 Devicetree
* ``kconfig`` 用于 Kconfig
* ``yaml`` 用于 YAML
* ``rst`` 用于 reStructuredText

未指定语言时，语言会被设为 ``none``，代码块不会高亮。你也可以显式使用 ``none`` 来达到相同效果；例如::

   .. code-block:: none

      This would be a block of text styled with a background
      and box, but with no syntax highlighting.

将显示为：

   .. code-block:: none

      This would be a block of text styled with a background
      and box, but with no syntax highlighting.

代码块还有一种简写形式：以双冒号（``::``）结束引导段落，并将其后的代码块内容缩进三个空格。输出时只会显示一个冒号。该代码块不会高亮（即 ``none``）。不过，你可以使用 :rst:dir:`highlight` 指令来自定义文档中使用的默认语言（例如参见本文档开头的做法）。


链接与交叉引用
**************

.. _internal-linking:

交叉引用内部内容
================

传统 reST 链接仅支持在当前文件内使用，记法如下::

   Refer to the `internal-linking`_ page

它渲染为，

   参见 `internal-linking`_ 页面

注意使用末尾的下划线来表示出站链接。在此示例中，标签紧邻标题之前添加，因此显示的文本就是标题文本本身。你可以通过这样书写来更改链接显示的文本::

   Refer to the `show this text instead <internal-linking_>`_ page

它渲染为，

   参见 `show this text instead <internal-linking_>`_ 页面


交叉引用外部内容
================

借助 Sphinx，我们可以创建指向 Zephyr 项目文档中任何带标签文本的链接引用。

文档中的目标位置使用标签指令定义::

      .. _my label name:

      Heading
      =======

注意开头的下划线，它表示这是一个入站链接。紧跟在该标签之后的内容必须是一个标题，该标题就是 Zephyr 文档中任意位置通过 ``:ref:`my label name``` 引用的目标。引用该标签时会显示标题文本。你还可以修改该链接显示的文本，例如::

   :ref:`some other text <my label name>`


为便于站点内的跨页面链接，每个文件应在其标题之前有一个引用标签，以便可从其他文件引用它。这些引用标签在整个站点内必须唯一，因此应避免使用“samples”这类通用名称。例如，本文档的 .rst 文件开头是::

   .. _doc_guidelines:

   Documentation Guidelines for the Zephyr Project
   ###############################################


其他 .rst 文档可以使用 ``:ref:`doc_guidelines``` 标签链接到本文档，并显示为 :ref:`doc_guidelines`。这种内部交叉引用可以跨文件使用，且链接文本取自文档源文件，因此标题变化时链接文本也会随之更新。

你也可以定义指向任意 URL 的链接，然后在文档中引用它。例如，在文档中定义以下标签::

   .. _Zephyr Wikipedia Page:
      https://en.wikipedia.org/wiki/Zephyr_(operating_system)

就可以这样引用它::

   Read the `Zephyr Wikipedia Page`_ for more information about the
   project.

.. tip::

   当文档包含许多外部链接时，在文档末尾用一个“References”章节列出它们会很有用。这可以通过 :rst:dir:`target-notes` 指令实现。例如::

      References
      ==========

      .. target-notes::

      .. _external_link1: https://example.com
      .. _external_link2: https://example.org

交叉引用 C 文档
===============

.. rst:role:: c:member
              c:data
              c:var
              c:func
              c:macro
              c:struct
              c:union
              c:enum
              c:enumerator
              c:type

   你可以使用这些角色交叉引用 C 函数、宏、类型等的 Doxygen 文档。

   在 HTML 输出中，它们会渲染为指向该项相应 Doxygen 文档的链接。例如::

      Check out :c:func:`gpio_pin_configure` for more information.

   将渲染为：

      更多信息请查看 :c:func:`gpio_pin_configure`。

   你可以像内置的 :rst:role:`ref` 角色那样提供自定义链接文本。

交叉引用 CMake 文档
===================

你可以使用以下角色交叉引用 Zephyr 的 CMake 模块、命令和变量的文档。

.. rst:role:: cmake:module

   该角色用于引用 CMake 模块。例如::

      See :cmake:module:`extensions` for more information.

   将渲染为：

      更多信息请参见 :cmake:module:`extensions`。

.. rst:role:: cmake:command

   该角色用于引用 CMake 命令。例如::

      See :cmake:command:`yaml_load` for more information.

   将渲染为：

      更多信息请参见 :cmake:command:`yaml_load`。

   由 CMake 自身记录的命令通过其完全限定名引用，并作为显式链接目标给出::

      See :cmake:command:`target_sources <command:target_sources>` for more information.

   将渲染为：

      更多信息请参见 :cmake:command:`target_sources <command:target_sources>`。

.. rst:role:: cmake:variable

   该角色用于引用 CMake 变量。例如::

      See :cmake:variable:`CMAKE_C_COMPILER` for more information.

   将渲染为：

      更多信息请参见 :cmake:variable:`CMAKE_C_COMPILER`。

可视元素
********

.. _doc_images:

图片
====

在文档中使用 :rst:dir:`image` 指令来包含图片::

   .. image:: ../../images/doc-gen-flow.png
      :align: center
      :alt: alt text for the image

或者，如果你想添加图片标题，请使用::

    .. figure:: ../../images/doc-gen-flow.png
       :alt: image description

       Caption for the figure

指定的文件名相对于文档源文件，我们建议将图片放在文档源文件所在目录的 ``images`` 文件夹中。

支持 Web 浏览器通常处理的图片格式：WebP、PNG、GIF、JPEG 和 SVG。

图片大小应仅保持所需的大小，通常宽度至少 500 px，但不超过 1000 px，且不超过 100 KB，除非为了清晰需要特别大的图片。

根据内容推荐的图片格式
----------------------

* **屏幕截图**：WebP 或 PNG。
* **示意图**：简单示意图可考虑使用 Graphviz（参见下文的 :ref:`专门章节 <graphviz_diagrams>`）。如果使用外部工具，建议使用 SVG。
* **照片** （例如开发板）：WebP，最大尺寸不超过 600 px。只要主体能与背景分离（开发板照片通常如此），就应以透明背景保存图片，使其能同时融入浅色和深色文档主题。

  你可以使用 `cwebp`_ 或 `ImageMagick`_ 将现有图片转换为大小合适的 WebP。例如::

     # Using cwebp (resize width to 600 px, height auto, ~80% quality).
     # For a portrait image, use "-resize 0 600" to cap the height instead.
     cwebp -resize 600 0 board_name.png -o board_name.webp

     # Using ImageMagick
     magick board_name.png -resize 600x600 -quality 80 board_name.webp

  当源图片已有透明背景（例如带 alpha 通道的 PNG）时，这两种工具都会在生成的 WebP 中保留透明度。``-resize 600 0``/``600x600`` 参数只会缩小图片，并保持其宽高比。

.. _cwebp: https://developers.google.com/speed/webp/download
.. _ImageMagick: https://imagemagick.org/

.. _graphviz_diagrams:

Graphviz
========

`Graphviz`_ 是一款用简单文本语言描述示意图的工具。由于让文档中使用的示意图易于维护很重要，我们鼓励使用 Graphviz 来创建示意图。Graphviz 特别适合创建状态图、流程图以及其他可以用图表示的类型。

要在文档中包含 Graphviz 示意图，请使用 :rst:dir:`graphviz` 指令。例如::

   .. graphviz::
      :caption: An example graph using Graphviz

      digraph G {
         rankdir=LR;
         A -> B;
         B -> C;
         C -> D;
      }

将渲染为：

   .. graphviz::
      :caption: 使用 Graphviz 的示例图

      digraph G {
         rankdir=LR;
         A -> B;
         B -> C;
         C -> D;
      }

关于如何使用 Graphviz 的 DOT 语言创建示意图的更多信息，请参考 `Graphviz documentation`_。

.. _Graphviz: https://graphviz.org
.. _Graphviz documentation: https://graphviz.org/documentation

Mermaid
=======

`Mermaid`_ 是一款使用简单文本语法的示意图与可视化创建工具。它特别适合创建流程图、时序图、类图和状态转换图。

要在文档中包含 mermaid 示意图，请使用 :rst:dir:`mermaid` 指令。例如::

   .. mermaid::
      :caption: State transition diagram for a GPIO debounce
      :alt: GPIO debounce state diagram showing transitions between inactive and active states
            through maybe_active and maybe_inactive intermediate states before each state becomes
            stable.

      ---
      config:
        state:
          useMaxWidth: false
      ---
      stateDiagram-v2

          State inactive {
              [*] --> stable_inactive
              stable_inactive --> maybe_active : edge to active
              maybe_active --> stable_inactive : edge to inactive
          }

          State active {
              [*] --> stable_active
              stable_active --> maybe_inactive : edge to inactive
              maybe_inactive --> stable_active : edge to active
          }

          [*] --> inactive

          maybe_active --> active : After(x ms)
          maybe_inactive --> inactive : After(x ms)


将渲染为：

.. mermaid::
   :caption: GPIO 去抖的状态转换图
   :alt: GPIO debounce state diagram showing transitions between inactive and active states
         through maybe_active and maybe_inactive intermediate states before each state becomes
         stable.

   ---
   config:
     state:
       useMaxWidth: false
   ---
   stateDiagram-v2

       State inactive {
           [*] --> stable_inactive
           stable_inactive --> maybe_active : edge to active
           maybe_active --> stable_inactive : edge to inactive
       }

       State active {
           [*] --> stable_active
           stable_active --> maybe_inactive : edge to inactive
           maybe_inactive --> stable_active : edge to active
       }

       [*] --> inactive

       maybe_active --> active : After(x ms)
       maybe_inactive --> inactive : After(x ms)


示意图会按页面宽度绘制，其高度由宽高比决定，因此高大于宽的示意图最终会比实际需要的大得多。如上面的示例那样关闭 ``useMaxWidth``，可以让示意图保持 Mermaid 为它计算的大小；它仍会缩小以适应窄屏。该设置属于示意图类型：此处是 ``state``，在其他地方则是 ``flowchart``、``sequence`` 或其他类型。

关于受支持的示意图、语法和示例的参考资料，请查阅 `Mermaid documentation`_。在创建或更新示意图时如需快速迭代，可以使用 `Mermaid live editor`_。

.. _Mermaid: https://mermaid.js.org/
.. _Mermaid documentation: https://mermaid.js.org/intro/
.. _Mermaid live editor: https://mermaid.live/

自定义 Sphinx 角色与指令
************************

Zephyr 文档使用自定义的 Sphinx 角色和指令来提供额外功能，并使编写和维护一致的文档更加容易。

应用构建命令
============

.. rst:directive:: .. zephyr-app-commands::

   生成一致的文档，说明管理（构建、烧写等）应用所需的 shell 命令

   例如，要生成针对 ``qemu_x86`` 构建 ``samples/hello_world`` 的命令，请使用::

      .. zephyr-app-commands::
         :zephyr-app: samples/hello_world
         :board: qemu_x86
         :goals: build

   这将渲染为：

      .. zephyr-app-commands::
         :zephyr-app: samples/hello_world
         :board: qemu_x86
         :goals: build

   .. rubric::  选项

   .. rst:directive:option:: tool
      :type: string

      使用哪个工具。当前有效选项为 ``cmake``、``west`` 和 ``all``。默认值为 ``west``。

   .. rst:directive:option:: app
      :type: string

      要构建的应用的路径。

   .. rst:directive:option:: zephyr-app
      :type: string

      要构建的应用路径，该应用位于上游 Zephyr 仓库中。与 ``:app:`` 互斥。

   .. rst:directive:option:: cd-into
      :type: no value

      如果设置，构建指令将从 ``:app:`` 文件夹内部给出，而不是在它之外。

   .. rst:directive:option:: generator
      :type: string

      生成哪种构建系统。

      当前有效选项为 ``ninja`` 和 ``make``。默认值为 ``ninja``。该选项不区分大小写。

   .. rst:directive:option:: host-os

      这些说明针对哪个主机操作系统。

      有效选项为 ``unix``、``win`` 和 ``all``。默认值为 ``all``。

   .. rst:directive:option:: board
      :type: string

      如果设置，构建命令将针对指定的开发板。

   .. rst:directive:option:: shield
      :type: string

      如果设置，构建命令将针对指定的 shield。

      可以用逗号分隔的列表提供多个 shield。

   .. rst:directive:option:: conf

      如果设置，构建命令将使用指定的配置文件。

      如果提供了多个配置文件，请用双引号括起以空格分隔的文件列表，例如 `“a.conf b.conf”`。

   .. rst:directive:option:: gen-args
      :type: string

      如果设置，表示为 CMake 调用提供的附加参数。

   .. rst:directive:option:: build-args
      :type: string

      如果设置，表示为构建调用提供的附加参数。

   .. rst:directive:option:: west-args
      :type: string

      如果设置，表示为 west 调用提供的附加参数（对 ``:tool: cmake`` 会忽略）。

   .. rst:directive:option:: flash-args
      :type: string

      如果设置，表示为烧写调用提供的附加参数。

   .. rst:directive:option:: debug-args
      :type: string

      如果设置，表示为调试调用提供的附加参数。

   .. rst:directive:option:: debugserver-args
      :type: string

      如果设置，表示为 debugserver 调用提供的附加参数。

   .. rst:directive:option:: attach-args
      :type: string

      如果设置，表示为 attach 调用提供的附加参数。

   .. rst:directive:option:: snippets
      :type: string

      如果设置，表示应用应使用列出的 snippet 进行编译。

      可以用逗号分隔的列表提供多个 snippet。

   .. rst:directive:option:: build-dir
      :type: string

      如果设置，应用的构建目录会把该相对路径（以 Unix 分隔符分隔） *追加* 到标准构建目录之后。这主要用于在同一页面中区分同一个应用的多次构建。

   .. rst:directive:option:: build-dir-fmt
      :type: string

      如果设置，则假定 `west config build.dir-fmt`` 已被设置为该路径。

      与 ``:build-dir:`` 互斥，并依赖 ``:tool: west``。

   .. rst:directive:option:: goals
      :type: string

      以空白分隔的列表，说明要对应用执行哪些操作（可以是 ``build``、``flash``、``debug``、``debugserver``、``run`` 中的任意组合）。

      完成这些任务的命令将按正确的顺序生成。

   .. rst:directive:option:: maybe-skip-config
      :type: no value

      如果设置，表示读者可能已经创建了构建目录并切换到其中，该选项会调整文本以说明无需再次执行这些操作。

   .. rst:directive:option:: compact
      :type: no value

      如果设置，生成的输出是单个代码块，不包含额外的注释行。


.. _linking_to_zephyr_files:

交叉引用 Zephyr 代码树中的文件
==============================

可以使用特殊的角色来引用 Zephyr 代码树中的文件。例如，可以使用 :rst:role:`zephyr_file` 角色引用本文件。

.. rst:role:: zephyr_file

   该角色用于引用 Zephyr 代码树中的文件。例如::

      Check out :zephyr_file:`doc/contribute/documentation/guidelines.rst` for more information.

   将渲染为：

      更多信息请查看 :zephyr_file:`doc/contribute/documentation/guidelines.rst`。

   你可以在文件路径后附加 :samp:`#L{line_number}` 或 :samp:`#L{start_line}-L{end_line}` 来引用文件中的特定行或行范围::

      See :zephyr_file:`doc/contribute/documentation/guidelines.rst#L3` for the main heading of
      this document.

   将渲染为：

      本文档的主标题请参见 :zephyr_file:`doc/contribute/documentation/guidelines.rst#L3`。

   该角色会自动验证所引用的文件是否存在于 Zephyr 代码树中，如果找不到该文件，会在文档构建期间产生警告。

   .. note::

      请谨慎使用行引用，因为链接文件的内容可能发生变化，长期保持其准确性并非易事。

   如果你想引用“原始”内容，可以改用 :rst:role:`zephyr_raw` 角色。

.. rst:role:: zephyr_raw

   该角色用于引用 Zephyr 代码树中文件的原始内容。例如::

      Check out :zephyr_raw:`doc/contribute/documentation/guidelines.rst` for more information.

   将渲染为：

      更多信息请查看 :zephyr_raw:`doc/contribute/documentation/guidelines.rst`。

.. rst:role:: module_file

   该角色用于引用 Zephyr 代码树中的模块。例如::

         Check out :module_file:`hal_stm32:CMakeLists.txt` for more information.

   将渲染为：

         更多信息请查看 :module_file:`hal_stm32:CMakeLists.txt`。

   与 :rst:role:`zephyr_file` 类似，你可以引用文件中的特定行或行范围。

交叉引用 GitHub 问题和拉取请求
==============================

.. rst:role:: github

   该角色用于引用 GitHub 问题或拉取请求。

   例如，要引用问题 #1234::

      Check out :github:`1234` for more background about this known issue.

   这将渲染为：

      关于该已知问题的更多背景信息，请查看 :github:`1234`。

Doxygen API 文档
================

.. app.add_directive("doxygengroup", DoxygenGroupDirective)
.. app.add_role_to_domain("c", "group", CXRefRole())

.. rst:directive:: .. doxygengroup:: name

   该指令用于输出 Doxygen 组的简短描述，以及指向相应 Doxygen 生成文档的链接。

   所有声明了该组为相关组的代码示例（使用 :rst:dir:`zephyr:code-sample` 指令声明）都会在渲染输出中自动列出并引用。

   例如::

      .. doxygengroup:: can_interface

   将渲染为：

      .. doxygengroup:: can_interface


   .. rubric:: Options

   .. rst:directive:option:: project
      :type: project name (optional)

      关联的 Doxygen 项目。当配置了多个 Doxygen 项目时，这会很有用。

.. rst:role:: c:group

   该角色用于引用 Zephyr 代码树中的 Doxygen 组。在 HTML 文档中，它们会渲染为指向该组相应 Doxygen 生成文档的链接。例如::

      Check out :c:group:`gpio_interface` for more information.

   将渲染为：

      更多信息请查看 :c:group:`gpio_interface`。

   你可以像内置的 :rst:role:`ref` 角色那样提供自定义链接文本。


Kconfig 选项
============

如果你想在文档中引用某个 Kconfig 选项，可以使用 :rst:role:`kconfig:option` 角色并提供要引用的选项名称。在构建 HTML 输出时，该角色会自动生成指向该 Kconfig 选项文档的链接。

请务必使用 Kconfig 选项的完整名称，包括 ``CONFIG_`` 前缀。

.. rst:role:: kconfig:option

   该角色用于引用 Zephyr 代码树中的 Kconfig 选项。例如::

      Check out :kconfig:option:`CONFIG_GPIO` for more information.

   将渲染为：

      更多信息请查看 :kconfig:option:`CONFIG_GPIO`。

.. rst:role:: kconfig:option-regex

   该角色用于创建指向 Kconfig 选项正则搜索的链接。它会生成指向 Kconfig 搜索页面的链接，并自动将提供的正则表达式填入搜索查询中。这对于引用共享同一前缀或属于同一类别的多个 Kconfig 选项很有用。例如::

      Check out :kconfig:option-regex:`CONFIG_SECURE_STORAGE_ITS_(STORE|TRANSFORM)_.*_CUSTOM` for
      the various customization possibilities.

   将渲染为：

      各种自定义可能性的说明请查看 :kconfig:option-regex:`CONFIG_SECURE_STORAGE_ITS_(STORE|TRANSFORM)_.*_CUSTOM`。

   建议提供自定义链接文本，使引用更易读。例如::

      Check out the :kconfig:option-regex:`ITS Kconfig options <CONFIG_SECURE_STORAGE_ITS_.*>`
      for more information.

   将渲染为：

      更多信息请查看 :kconfig:option-regex:`ITS Kconfig 选项 <CONFIG_SECURE_STORAGE_ITS_.*>`。

Devicetree binding
==================

如果你想在文档中引用 Devicetree binding，可以使用 :rst:role:`dtcompatible` 角色并提供要引用的 binding 的 compatible 字符串。在构建 HTML 文档输出时，该角色会自动生成指向该 binding 文档的链接。

.. rst:role:: dtcompatible

   该角色可在行内使用，用于引用作为参数给出的 Devicetree compatible 的生成文档。

   单个 compatible 可能对应多个页面。例如，当某个 binding 的行为取决于节点所在的总线时就会出现这种情况。此时，引用会指向一个“消歧义”页面，该页面链接到所有可能的情况，与 Wikipedia 消歧义页面的工作方式类似。例如::

      Check out :dtcompatible:`zephyr,input-longpress` for more information.

   将渲染为：

      更多信息请查看 :dtcompatible:`zephyr,input-longpress`。

代码示例
========

.. rst:directive:: .. zephyr:code-sample:: id

   该指令用于描述代码示例，包括它可能用到哪些值得注意的 API。

   例如::

      .. zephyr:code-sample:: blinky
         :name: Blinky
         :relevant-api: gpio_interface

         Blink an LED forever using the GPIO API.

   该指令的内容将用作代码示例的描述。

   .. rubric:: Options

   .. rst:directive:option:: name
      :type: text

      表示示例的人类可读短名称。

   .. rst:directive:option:: relevant-api
      :type: text

      可选的、以空格分隔的 Doxygen 组名称列表，对应代码示例所用的 API。

.. rst:role:: zephyr:code-sample

   该角色用于引用使用 :rst:dir:`zephyr:code-sample` 描述的代码示例。

   例如::

      Check out :zephyr:code-sample:`blinky` for more information.

   将渲染为：

      更多信息请查看 :zephyr:code-sample:`blinky`。

   它的用法与内置的 :rst:role:`ref` 角色完全相同，即你可以提供自定义链接文本。例如::

      Check out :zephyr:code-sample:`blinky code sample <blinky>` for more information.

   将渲染为：

      更多信息请查看 :zephyr:code-sample:`blinky 代码示例 <blinky>`。

.. rst:directive:: .. zephyr:code-sample-category:: id

   该指令用于定义用于对代码示例分组的类别。

   例如::

      .. zephyr:code-sample-category:: gpio
         :name: GPIO
         :show-listing:

         Samples related to the GPIO subsystem.

   该指令的内容将用作类别的描述。它可以包含任何有效的 reStructuredText 内容。

   .. rubric:: Options

   .. rst:directive:option:: name
      :type: text

      表示类别的可读名称。

   .. rst:directive:option:: show-listing
      :type: flag

      如果设置，将显示该类别中代码示例的列表。该列表根据当前文档子目录中找到的所有代码示例自动生成。

   .. rst:directive:option:: glob
      :type: text

      用于匹配要包含在列表中的文件的 glob 模式。默认为 `*/*`，但可以覆盖，例如当示例位于并非直接隶属于类别目录的目录中时。

.. rst:role:: zephyr:code-sample-category

   该角色用于引用使用 :rst:dir:`zephyr:code-sample-category` 描述的代码示例类别。

   例如::

      Check out :zephyr:code-sample-category:`cloud` samples for more information.

   将渲染为：

      更多信息请查看 :zephyr:code-sample-category:`cloud` 示例。

.. rst:directive:: .. zephyr:code-sample-listing::

   该指令用于显示在一个或多个类别中找到的所有代码示例的列表。

   例如::

      .. zephyr:code-sample-listing::
         :categories: cloud

   将渲染为：

      .. zephyr:code-sample-listing::
         :categories: cloud

   .. rubric:: Options

   .. rst:directive:option:: categories
      :type: text

      要显示列表的类别 ID 列表，以空格分隔。

   .. rst:directive:option:: live-search
      :type: flag

      一个用于在列表正上方包含搜索框的标志。搜索框允许用户按代码示例的名称/描述筛选列表，这对于示例数量较多的类别很有用。该选项仅在 HTML 构建器中可用。

开发板
======

.. rst:directive:: .. zephyr:board:: name

   该指令用于在文档开头指明这是某个开发板的主文档页面，开发板名称作为指令参数给出。

   例如::

      .. zephyr:board:: wio_terminal

   开发板的元数据从各种配置文件中读取，并用于自动填充开发板文档的某些章节。使用该指令的开发板文档页面可以通过 :rst:role:`zephyr:board` 角色链接。

.. rst:role:: zephyr:board

   该角色用于引用使用 :rst:dir:`zephyr:board` 记录的开发板。

   例如::

      Check out :zephyr:board:`wio_terminal` for more information.

   将渲染为：

      更多信息请查看 :zephyr:board:`wio_terminal`。

.. rst:directive:: .. zephyr:board-catalog::

   该指令用于生成 Zephyr 支持的开发板目录，可用于快速浏览所有受支持开发板的列表，并按各种条件进行筛选。

.. rst:role:: zephyr:board-catalog

   该角色用于引用开发板目录页面，可选地带有筛选参数。例如::

      Check out :zephyr:board-catalog:`` for more information.

   将渲染为：

      更多信息请查看 :zephyr:board-catalog:`` 。

   它的用法可以与内置的 :rst:role:`ref` 角色完全相同，即你可以提供自定义链接文本。例如::

      Check out the :zephyr:board-catalog:`boards using this compatible <#compatibles=ti,hdc2080>`
      for more information.

   将渲染为：

      更多信息请查看 :zephyr:board-catalog:`使用该 compatible 的开发板 <#compatibles=ti,hdc2080>`。

.. rst:directive:: .. zephyr:board-supported-hw::

   该指令用于显示当前页面所记录开发板的所有目标所支持的硬件特性。这些表格根据开发板的 Devicetree 自动生成。

   该指令必须用在同时包含 :rst:dir:`zephyr:board` 指令的文档中，因为它依赖开发板信息来生成表格。

   .. note::

      该指令要求构建文档时启用硬件特性生成（将 ``zephyr_generate_hw_features`` 配置选项设为 ``True``）。如果禁用，将显示警告消息而不是硬件特性表格。

      可以在不完全禁用硬件特性表格的前提下，将硬件特性生成限制为特定厂商列表中的开发板，以加快文档构建速度。将配置选项 ``zephyr_hw_features_vendor_filter`` 设为要为其生成特性的厂商列表。如果该选项为空，则为所有厂商的所有开发板生成硬件特性。

      配置选项 ``zephyr_hw_features_twister_extra_flags`` 可用于为 twister 命令提供附加标志。

.. rst:directive:: .. zephyr:board-supported-runners::

   该指令用于显示当前页面所记录开发板支持的 runner，包括默认用于烧写和调试的 runner。

   该指令必须用在同时包含 :rst:dir:`zephyr:board` 指令的文档中，因为它依赖开发板信息来生成表格。

   .. note::

      与 :rst:dir:`zephyr:board-supported-hw` 类似，该指令要求启用硬件特性生成（将 ``zephyr_generate_hw_features`` 配置选项设为 ``True``）才能生成完整的表格。如果禁用，将显示警告消息而不是 runner 表格。

无障碍准则
**********

无障碍是文档的一个重要方面，它确保所有用户（包括残障用户）都能访问并理解内容。

在编写和维护 Zephyr 项目文档时，请遵循以下准则，为所有人改善无障碍体验。

图片与插图
==========

所有图片和插图都必须包含适当的替代文本（alt 文本），以便向依赖屏幕阅读器或无法查看图片的用户传达视觉内容的含义。

* 使用 :rst:dir:`image` 指令插入图片时，请使用 ``:alt:`` 属性。示例：

  .. code-block:: rst
     :emphasize-lines: 2

     .. image:: image/doc-gen-flow.png
        :alt: Documentation generation process overview

* 如果图片中包含文字，请确保 alt 文本逐字包含这些文字。

* 使用 :rst:dir:`figure` 指令（它允许添加题注）时，``:alt:`` 文本仍然很重要。alt 文本应描述图片本身，而题注提供额外的上下文或解释。示例：

  .. code-block:: rst
     :emphasize-lines: 4

     .. figure:: ../../images/arch-diagram.png
        :alt: High-level overview of Zephyr OS architecture showing layers and components.

        High-level overview of Zephyr OS architecture.

- 对于可以用文字清楚说明的信息，避免将图片作为唯一的传达方式。

.. admonition:: 编写 alt 文本的最佳实践
   :class: tip

   * **准确且等效**：呈现与图片相同的关键信息。
   * **简明扼要**：简练地传达图片的核心信息。
   * **避免冗余**：不要使用“Image of……”或“Picture of……”这类措辞，因为屏幕阅读器通常会将该元素播报为图片。
   * **描述而非解释**：坚持描述图片上实际呈现的内容。
   * **复杂图片**：对于图表、示意图或其他复杂视觉内容，请在 alt 文本中提供摘要。如果充分理解需要更多细节，可以考虑在周边文字中或作为插图标题的一部分提供更详细的描述。使用 :ref:`Graphviz <graphviz_diagrams>` 这类基于文本的示意图工具也可以改善无障碍体验。


标题与结构
==========

使用 :ref:`标题 <headings>` 来合理地组织文档结构。这样可以让使用辅助技术的用户理解文档的组织方式并高效地浏览。

Tables
======

表格应仅用于表格数据，并且必须能被屏幕阅读器访问。

* 请始终为行和列定义表头。

* 尽可能使用 :rst:dir:`list-table` 指令，以获得更好的响应性和无障碍性。

* 对于上下文不直观的表格，请包含标题。例如：

  .. code-block:: rst
     :emphasize-lines: 1

     .. list-table:: GPIO Pin Configuration Options
        :widths: 15 30
        :header-rows: 1

        * - Field
          - Description
        * - GPIO_INPUT
          - Configures pin as input
        * - GPIO_OUTPUT
          - Configures pin as output

其他资源
========

关于 Web 无障碍的更通用指南，可以参考 W3C 的 `Web Content Accessibility Guidelines (WCAG)`_

.. _`Web Content Accessibility Guidelines (WCAG)`: https://www.w3.org/WAI/standards-guidelines/wcag/

参考资料
********

.. target-notes::
