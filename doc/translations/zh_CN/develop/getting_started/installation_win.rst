.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _win-setup-alts:

Windows 备选安装说明
####################

.. _win-wsl:

Windows 10 WSL（适用于 Linux 的 Windows 子系统）
************************************************

如果你运行的是较新的 Windows 10 版本，可以使用内置功能，直接在标准命令提示符中运行 Ubuntu 二进制文件。这样无需搭建虚拟机即可使用 :ref:`Zephyr SDK <toolchain_zephyr_sdk>` 等软件。

.. warning::
      Windows 10 版本 1803 存在一个问题，会导致 CMake 无法正常工作，该问题已在 1809（及更高版本）中修复。更多信息见 :github:`Zephyr Issue 10420 <10420>`。

#. `Install the Windows Subsystem for Linux (WSL)`_。

   .. note::
         要让 Zephyr SDK 正常工作，需要 Windows 10 build 15002 或更高版本。可以在系统设置的“关于你的电脑”部分查看当前运行的 Windows 10 版本号。如果运行的是更旧的 Windows 10 版本，可能需要安装 Creator's Update。

#. 按照 :ref:`installation_linux` 文档中的 Ubuntu 说明操作。

.. NOTE FOR DOCS AUTHORS: as a reminder, do *NOT* put dependencies for building
   the documentation itself here.

.. _Install the Windows Subsystem for Linux (WSL): https://msdn.microsoft.com/en-us/commandline/wsl/install_guide
