.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _zephyr_doc:

文档生成
########

以下说明将引导你在本地系统上生成 Zephyr 项目的文档，所用的文档源与我们在 https://docs.zephyrproject.org 上创建在线文档时使用的文档源相同。

.. _documentation-overview:

文档概述
********

Zephyr 项目的内容使用 reStructuredText 标记语言（.rst 文件扩展名）并配合 Sphinx 扩展编写，再通过 Sphinx 处理，生成格式化的独立网站。开发者可以以 .rst 标记文件的原始形式查看这些内容，也可以生成 HTML 内容并在自己的工作站上用 Web 浏览器直接查看。同一份 .rst 内容也会送入 Zephyr 项目的公开网站文档区域（应用不同的主题）。

你可以从各自的网站阅读关于 `reStructuredText`_ 和 `Sphinx`_ 的详细信息。

项目的文档包含以下内容：

* 用于生成 https://docs.zephyrproject.org 网站上文档的 reStructuredText 源文件。大多数 reStructuredText 源文件位于 ``/doc`` 目录中，另一些则存放在代码树中靠近其所属组件的位置（例如 ``/samples`` 和 ``/boards``）。

* 用于生成所有 API 专属文档的 Doxygen 生成内容，这些文档同样位于 https://docs.zephyrproject.org 上。

* 根据源代码树中的 Kconfig 文件、由脚本生成的内核配置选项内容。

.. graphviz::
   :caption: 文档构建流程示意图

   digraph {
      rankdir=LR

      images [shape="rectangle" label=".png, .jpg\nimages"]
      rst [shape="rectangle" label="restructuredText\nfiles"]
      conf [shape="rectangle" label="conf.py\nconfiguration"]
      rtd [shape="rectangle" label="read-the-docs\ntheme"]
      header [shape="rectangle" label="c header\ncomments"]
      xml [shape="rectangle" label="XML"]
      html [shape="rectangle" label="HTML\nweb site"]
      sphinx[shape="ellipse" label="sphinx +\ndocutils"]
      images -> sphinx
      rst -> sphinx
      conf -> sphinx
      header -> doxygen
      doxygen -> xml
      xml-> sphinx
      rtd -> sphinx
      sphinx -> html
   }


reStructuredText 文件由 Sphinx 文档系统处理，并使用 doxygen 生成的 API 内容。如以下章节所述，在本地生成文档还需要额外的工具。

.. _documentation-processors:

安装文档处理工具
****************

我们的文档处理流程已在以下版本上测试通过：

* Doxygen 1.17.0 版本
* Graphviz 2.43
* Latexmk 4.83 版本
* 仓库文件 ``doc/requirements.txt`` 中列出的所有 Python 依赖

要安装文档工具，请先按照 :ref:`getting_started` 中的说明安装 Zephyr。然后安装仅在生成文档时才需要的额外工具，如下所述：

.. doc_processors_installation_start

.. tabs::

   .. group-tab:: Linux

      所有 Linux 安装方式通用：安装构建文档所需的 Python 依赖：

      .. code-block:: console

         pip install -U -r ~/zephyrproject/zephyr/doc/requirements.txt

      在 Ubuntu Linux 上：

      .. code-block:: console

         sudo apt-get install --no-install-recommends doxygen graphviz librsvg2-bin \
         texlive-latex-base texlive-latex-extra latexmk texlive-fonts-recommended imagemagick

      在 Fedora Linux 上：

      .. code-block:: console

         sudo dnf install doxygen graphviz texlive-latex latexmk \
         texlive-collection-fontsrecommended librsvg2-tools ImageMagick

      在 Clear Linux 上：

      .. code-block:: console

         sudo swupd bundle-add texlive graphviz ImageMagick

      在 Arch Linux 上：

      .. code-block:: console

         sudo pacman -S graphviz doxygen librsvg texlive-core texlive-bin \
         texlive-latexextra texlive-fontsextra imagemagick

   .. group-tab:: macOS

      安装构建文档所需的 Python 依赖：

      .. code-block:: console

         pip install -U -r ~/zephyrproject/zephyr/doc/requirements.txt

      使用 ``brew`` 和 ``tlmgr`` 安装这些工具：

      .. code-block:: console

         brew install doxygen graphviz mactex librsvg imagemagick
         tlmgr install latexmk
         tlmgr install collection-fontsrecommended

   .. group-tab:: Windows

      安装构建文档所需的 Python 依赖：

      .. code-block:: console

         pip install -U -r %HOMEPATH$\zephyrproject\zephyr\doc\requirements.txt

      以 **管理员** 身份打开 ``cmd.exe`` 窗口并运行以下命令：

      .. code-block:: console

         choco install doxygen.install graphviz strawberryperl miktex rsvg-convert imagemagick

      .. note::
         在 Windows 上，Sphinx 可执行文件 ``sphinx-build.exe`` 位于 Python 安装路径的 ``Scripts`` 文件夹中。根据你安装 Python 的方式，可能需要将该文件夹添加到 ``PATH`` 环境变量中。如有需要，请按照 `Windows Python Path`_ 中的说明进行添加。

.. doc_processors_installation_end

文档展示主题
************

Sphinx 支持通过主题轻松定制生成文档的外观。替换主题文件并再次执行 ``make html``，输出的布局和样式就会改变。``read-the-docs`` 主题会在入门指南的 :ref:`install_py_requirements` 步骤中一并安装。

运行文档处理工具
****************

你克隆的 Zephyr 项目 git 仓库中的 ``/doc`` 目录包含所有 .rst 源文件、额外工具以及用于在本地生成 Zephyr 项目技术文档的 Makefile。假设本地 Zephyr 项目副本位于主目录下的 ``zephyr`` 文件夹中，则在本地生成 HTML 内容的命令如下：

.. code-block:: console

   # On Linux/macOS
   cd ~/zephyrproject/zephyr/doc
   # On Windows
   cd %userprofile%\zephyrproject\zephyr\doc

   # Use cmake to configure a Ninja-based build system:
   cmake -GNinja -B_build .

   # Enter the build directory
   cd _build

   # To generate HTML output, run ninja on the generated build system:
   ninja html
   # If you modify or add .rst files, run ninja again:
   ninja html

   # To generate PDF output, run ninja on the generated build system:
   ninja pdf

.. warning::

   文档构建系统会在构建目录中为用于生成文档的每个 .rst 文件创建副本，以及这些 .rst 文件所引用的依赖项的副本。

   这意味着 Sphinx 的警告和错误指向的是 **副本**，而 **不是 Zephyr 中受版本控制的原始文件**。请注意不要误编辑错误消息中提到的文件副本，因为这些修改不会被保存。

根据开发系统的不同，收集并生成 HTML 内容最多需要 15 分钟。完成后，可以用浏览器从 ``doc/_build/html/index.html`` 开始查看 HTML 输出；如果生成了 PDF 文件，它位于 ``doc/_build/latex/zephyr.pdf``。

如果你想从头构建文档，只需删除构建文件夹的内容，然后再次运行 ``cmake`` 和 ``ninja``。

.. note::

   如果向文档中添加或删除文件，需要重新运行 CMake。

在 Unix 平台上，可以使用便捷的 :zephyr_file:`doc/Makefile` 直接在该目录中构建文档：

.. code-block:: console

   cd ~/zephyrproject/zephyr/doc

   # To generate HTML output
   make html

   # To generate PDF output
   make pdf

.. _building-translated-documentation:

构建中文文档
************

中文正文以完整的 reStructuredText 文件保存在 ``doc/translations/zh_CN/`` 下，
目录结构与汇集后的英文文档对应。例如，``doc/kernel/index.rst`` 对应
``doc/translations/zh_CN/kernel/index.rst``；
``boards/<vendor>/<board>/doc/index.rst`` 对应
``doc/translations/zh_CN/boards/<vendor>/<board>/doc/index.rst``。

只翻译人工编写的说明文档。从源码生成的 API 文档、Kconfig 选项参考、Devicetree 绑定参考
和硬件能力表保留英文。保留生成指令、代码、标识符、显式引用标签和链接目标。
没有中文源文件的页面使用完整的英文原文。

构建时先选择中文文件，再使用 Zephyr 原有的主题、扩展和参考文档生成器处理。
被包含的说明文档优先引用构建目录中对应的文件；代码示例和共用图片继续引用原始资源。
中文界面模板位于 ``doc/translations/zh_CN/_templates/``，项目不使用 gettext 翻译目录。

在 ``doc`` 目录执行::

   make html-zh

中文 HTML 输出到 ``_build/zh/html``。Pages 工作流设置 ``HW_FEATURES_TURBO_MODE=1``，
跳过 Twister 针对各开发板执行的 CMake 配置，只运行文档测试和 Sphinx，
不安装交叉编译器，也不构建固件示例。开发板目录保留名称、厂商和架构信息；
硬件能力及内存容量等详情请查看上游英文开发板文档。
Doxygen 和 Kconfig 元数据仍会生成，用于校验引用。``SKIP_*`` 选项仍仅用于本地预览。

GitHub Pages 工作流只构建并发布中文站。构建过程仍会读取英文源文档和 API 元数据来校验引用，
但不再渲染或托管英文文档镜像。页面右上角的 English 打开上游对应原文；
未翻译章节和独立的生成参考页也链接到上游。默认原文地址为
``https://docs.zephyrproject.org/latest/``；发布指定版本的译文时，应通过
``ZEPHYR_DOCS_UPSTREAM_BASE_URL`` 指定对应版本的官方文档地址。

``_scripts/package_translations.py`` 将中文页面、静态资源和旧英文路径的简短跳转页打包，
排除调试用 source map 及内部构建产物，并检查 GitHub Pages 的站点容量限制。

审阅时对照完整的英文源文、中文文章和渲染页面。
``translations/zh_CN/_meta/sources.json`` 记录各文件迁移时的原文基准；
此记录用于追溯来源，不代表译文已经通过人工审阅。上游更新后，应与记录的版本比较，
更新完整文章，并核对术语、引用、被包含文档和代码示例，再更新同步基准。

下游站点可以通过以下环境变量配置链接：

* ``ZEPHYR_DOCS_HTML_BASEURL``：当前语言的规范网址。
* ``ZEPHYR_DOCS_REFERENCE_PREFIX``：生成参考页的路径前缀。
* ``ZEPHYR_DOCS_SITE_BASE_URL``：中文站的根网址。
* ``ZEPHYR_DOCS_UPSTREAM_BASE_URL``：对应版本的官方英文文档根网址。
* ``ZEPHYR_DOCS_GH_BASE_URL``：源码和问题反馈的 GitHub 仓库。
* ``ZEPHYR_DOCS_GH_REF``：源码链接使用的分支或标签。

开发者模式的文档构建
********************

在对文档进行重大修改并测试时，我们提供了一个选项，可临时去掉自动生成的 Devicetree binding 文档，以加快文档构建过程。

要启用该模式，请在调用 cmake 时设置以下选项::

   -DDT_TURBO_MODE=1

另一个通常耗时较长的步骤是生成每个开发板受支持特性的列表。可以通过在调用 cmake 时设置以下选项来禁用::

   -DHW_FEATURES_TURBO_MODE=1

使用以下目标调用 :command:`make`，即可在不使用上述任一特性的情况下构建文档::

   cd ~/zephyrproject/zephyr/doc

   # To generate HTML output without detailed Devicetree bindings documentation
   # and supported features index
   make html-fast

在编写叙述性页面时，为进一步加快迭代速度，还可以使用额外的 ``SKIP_*`` 选项来跳过整个类别的自动生成内容：

``SKIP_DOXYGEN``
   跳过运行 Doxygen 以及构建 C API 参考。

``SKIP_KCONFIG``
   跳过生成 Kconfig 选项参考及其搜索页面。

``SKIP_EXTERNAL_CONTENT``
   跳过复制维护在 ``doc/`` 文件夹之外的开发板、示例和 snippet 页面（即 :zephyr_file:`boards`、:zephyr_file:`samples` 和 :zephyr_file:`snippets` 文件夹的内容）。

每个选项都可以单独启用::

   make html SKIP_DOXYGEN=1

:command:`make html-minimal` 目标在 ``html-fast`` 的基础上组合了以上所有选项，是预览叙述性页面修改的最快方式::

   make html-minimal

.. warning::

   被跳过的生成器本应产生的内容会被替换为占位符，指向它的交叉引用会渲染为纯文本，相关警告也会被抑制。因此，使用任何 ``SKIP_*`` 选项的构建只适合本地预览：它不能用于验证交叉引用，其输出也不得发布。

在处理特定厂商开发板的文档时，也可以将受支持特性列表的生成限制在部分开发板厂商。可以通过在调用 cmake 时设置以下选项来实现::

   -DHW_FEATURES_VENDOR_FILTER=vendor1,vendor2

该选项也可以与 :command:`make` 封装一起使用::

   cd ~/zephyrproject/zephyr/doc

   # To generate HTML output with supported features limited to a subset of vendors
   make html HW_FEATURES_VENDOR_FILTER=vendor1,vendor2

在本地查看生成的文档
********************

可以用 python 在本地托管生成的 HTML 文档，以便用 Web 浏览器查看：

.. code-block:: console

   $ python3 -m http.server -d _build/html

.. note::

   WSL2 用户可能需要显式将地址绑定到 ``127.0.0.1``，才能从宿主机器访问：

   .. code-block:: console

      $ python3 -m http.server -d _build/html --bind 127.0.0.1

或者，可以使用 ``make html-live`` （或 ``make html-live-fast``）命令构建文档，该命令会构建文档、在本地托管它，并监视文档目录的变更。检测到变更后，它会自动重新构建文档并刷新所托管的文件。

单独构建 Doxygen 文档
*********************

可以使用 ``doxygen`` 构建目标只构建 Doxygen（API）文档，这比构建完整的文档集快得多::

   cd ~/zephyrproject/zephyr/doc
   make doxygen

输出位于 ``_build/doxygen/html``。

``doxygen-xml`` 目标以仅启用 XML 输出的方式构建相同的文档，输出位于 ``_build/doxygen-xml/xml``。

在常规文档构建中，从 Doxygen 注释指向主文档的引用（例如 ``@kconfig{}``、``@dtcompatible{}`` 或 ``@rstref{}``，参见 :ref:`doxygen_sphinx_xrefs`）会自动解析为超链接。在单独的 Doxygen 构建中，由于文档的其余部分不可用，它们会保留为纯文本。

将外部 Doxygen 项目链接到 Zephyr
********************************

基于 Zephyr 功能构建、并希望在 Doxygen 中（通过 @ref）引用 Zephyr 文档的外部项目，可以使用导出在 `zephyr.tag <../../doxygen/html/zephyr.tag>`_ 的 tag 文件

下载后，可以在自定义的 ``doxyfile.in`` 中按如下方式使用该 tag 文件::

   TAGFILES = "/path/to/zephyr.tag=https://docs.zephyrproject.org/latest/doxygen/html/"

更多信息请参考 `Doxygen External Documentation`_。


.. _reStructuredText: https://sphinx-doc.org/rest.html
.. _Sphinx: https://sphinx-doc.org/
.. _Windows Python Path: https://docs.python.org/3/using/windows.html#finding-the-python-executable
.. _Doxygen External Documentation: https://www.doxygen.nl/manual/external.html
