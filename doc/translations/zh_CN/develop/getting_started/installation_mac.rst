.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mac-setup-alts:

macOS 备选安装说明
##################

.. _mac-gatekeeper:

关于 Gatekeeper 的重要说明
**************************

从 macOS 10.15 Catalina 开始，从“终端”等终端模拟器启动的应用同样受制于 Dock 启动应用时适用的系统安全策略。这意味着如果通过浏览器下载可执行文件，macOS 默认不允许在终端中运行它们。可以通过以下两种方式解决：

* 运行 ``xattr -r -d com.apple.quarantine /path/to/folder``，其中 ``path/to/folder`` 是包含要运行的可执行文件所在的文件夹路径。

* 打开 :menuselection:`System Preferences --> Security and Privacy --> Privacy`，向下滚动到 “Developer Tools”，解锁后勾选你使用的终端模拟器对应的复选框。这样从该终端程序启动的任何可执行文件都会应用该设置。

注意：本节内容不适用于通过 Homebrew 安装的可执行文件，因为 ``brew`` 会自动取消它们的隔离属性。但这对于大多数 :ref:`工具链 <toolchains>` 来说是相关的。

.. _macOS Gatekeeper: https://en.wikipedia.org/wiki/Gatekeeper_(macOS)

MacPorts 用户补充说明
*********************

虽然本指南不正式支持 MacPorts，但在 macOS 上也可以使用 MacPorts 代替 Homebrew 安装所需的全部依赖。另外需要注意，为了让 Python 依赖正确安装，你可能需要安装 ``rust`` 和 ``cargo``。
