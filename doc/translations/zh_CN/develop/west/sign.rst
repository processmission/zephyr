.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _west-sign:

签名二进制文件
##############

``west sign`` :ref:`扩展 <west-extensions>` 命令可以借助外部工具，为供引导加载程序使用的 Zephyr 应用程序二进制文件签名。在某些配置中，``west sign`` 还用于调用外部后处理工具，将镜像的最终组件“拼接”在一起。运行 ``west sign -h`` 获取命令行帮助。

rimage
******

rimage 配置不依赖 Kconfig 或 CMake，而是采用 :ref:`west config<west-config>`，与 :ref:`west-building-cmake-config` 类似。

签名涉及多层相互叠加的“包装”脚本：``west flash`` 调用 ``west build``，后者调用 ``cmake`` 和 ``ninja``，再调用 ``west sign``，最终调用 ``imgtool`` 或 `rimage`_。只要所需签名参数采用默认值且相对固定，这些间接调用就没有问题。但如果要将 ``imgtool`` 或 ``rimage`` 的选项穿过所有层传下去，就会出现多层包装却没有实质抽象时常见的问题。首先，通常需要在每一层编写重复代码。让空格或其他特殊字符的引用正确穿过所有包装层也很困难。为调试构建问题而复现底层 ``west sign`` 命令可能非常耗时：至少需要启用并搜索详细构建日志，才能找到实际使用的选项。从构建日志复制这些选项可能并不可靠，因为细微的环境差异可能导致不同结果。最后，也是最严重的问题：在每一层添加更多重复代码之前，新的签名功能和选项根本无法使用。

为避免这些问题，可以在 ``west config`` 中设置 ``rimage`` 参数。以下是一个 ``workspace/.west/config`` 示例：

.. code-block:: ini

   [sign]
   # Not needed when invoked from CMake
   tool = rimage

   [rimage]
   # Quoting is optional and works like in Unix shells
   # Not needed when rimage can be found in the default PATH
   path = "/home/me/zworkspace/build-rimage/rimage"

   # Not needed when using the default development key
   extra-args = -i 4 -k 'keys/key argument with space.pem'

为支持引用，值使用 Python 的 ``shlex.split()`` 解析，与 :ref:`west-building-cmake-args` 相同。

``extra-args`` 会直接传给 ``rimage`` 命令。上例等同于将这些参数附加在命令行的 ``--`` 之后：``west sign --tool rimage -- -i 4 -k 'keys/key argument with space.pem'``。如果两种方式同时使用，命令行参数位于最后。

.. _rimage:
   https://github.com/thesofproject/rimage


silabs_commander
****************

``silabs_commander`` 工具用于为 Silicon Labs 设备的二进制文件签名、添加 MIC 或加密。将 ``sign.tool`` 配置设置为 ``silabs_commander`` 后，可通过 ``west sign`` 调用它；设置 ``CONFIG_SIWX91X_SIGN_KEY`` 或 ``CONFIG_SIWX91X_MIC_KEY`` 后，也可通过 ``west build`` 调用。

如果设置了 ``CONFIG_SIWX91X_SIGN_KEY`` 或 ``CONFIG_SIWX91X_MIC_KEY``，``west flash`` 会自动烧录已签名的二进制版本。

``silabs_commander`` 要求主机安装 `Simplicity Commander`_。设备密钥的预置方法见 `UG574 SiWx917 SoC Manufacturing Utility User Guide`_。

.. _Simplicity Commander:
   https://www.silabs.com/developer-tools/simplicity-studio/simplicity-commander?tab=downloads
.. _UG574 SiWx917 SoC Manufacturing Utility User Guide:
   https://www.silabs.com/documents/public/user-guides/ug574-siwx917-soc-manufacturing-utility-user-guide.pdf
