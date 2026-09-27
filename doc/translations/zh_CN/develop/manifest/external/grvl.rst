.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_grvl:

grvl
####

简介
****

`Graphics Rendering Visual Library`_ （grvl）是面向 Zephyr 微控制器的轻量级 GUI 库，提供可移植方案，既适合资源受限设备，也能带来现代、响应灵敏的用户体验。

grvl 内部链接标准 XML 库 `tinyxml`_，用于解析 GUI 配置，以配置替代相应代码。借助集成的 `Duktape`_ JavaScript 引擎，可以用 JavaScript 脚本编写 UI 交互。

grvl 的功能：

* 原生支持 PNG 和 JPEG 图像
* 兼容 Simple DirectMedia Layer
* 符合 POSIX，并支持 Zephyr
* 一组内置组件

  * 弹出窗口
  * 字体
  * 标签
  * 按钮
  * 滑块

* 用户自定义预制组件，可用于在运行时实例化复杂结构
* 基于 XML 的布局与 JavaScript 引擎

grvl 采用 Apache License 2.0；tinyxml 采用 Zlib 许可证；Duktape 采用 MIT 许可证。

在 Zephyr 中使用
****************

要将 grvl 作为 Zephyr :ref:`模块 <modules>` 使用，添加以下条目：

.. code-block:: yaml

   manifest:
     projects:
       - name: grvl
         url: https://github.com/antmicro/grvl
         revision: main
         path: modules/grvl # adjust the path as needed

将其加入 Zephyr 子清单，例如 ``zephyr/submanifests/grvl.yaml``，并运行 ``west update``；也可以将其作为 West 项目加入项目的 ``west.yaml`` 清单。

更多信息见 `grvl documentation`_ 或 `grvl blog article`_。

也可以体验交互式 `Zephyr calendar demo`_。

参考资料
********

.. target-notes::

.. _Graphics Rendering Visual Library:
   https://github.com/antmicro/grvl

.. _tinyxml:
   https://github.com/leethomason/tinyxml2

.. _Duktape:
   https://github.com/svaarala/duktape

.. _grvl documentation:
   https://antmicro.github.io/grvl/

.. _Zephyr calendar demo:
   https://github.com/antmicro/grvl-zephyr-calendar-demo

.. _grvl blog article:
  https://antmicro.com/blog/2025/12/grvl-a-lightweight-gui-library-for-zephyr-based-mcus
