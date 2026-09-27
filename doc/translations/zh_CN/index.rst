.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

..
    Zephyr Project documentation main file

.. _zephyr-home:

Zephyr 项目文档
###############

.. raw:: html

   <script>
     function openVersionSelector() {
       // Open the mobile menu if visible
       var mobileMenu = document.querySelector('[data-toggle="wy-nav-top"]');
       if (mobileMenu && mobileMenu.offsetParent !== null) {
         mobileMenu.click();
       }
       // Open the version selector
       var versionSelector = document.querySelector('[data-toggle="rst-current-version"]');
       if (versionSelector) {
         versionSelector.click();
       }
     }
   </script>

.. only:: release

   .. admonition:: 欢迎阅读 Zephyr 项目 |version| 版文档。
      :class: welcome

      其他 Zephyr 版本的文档请参阅 `官方文档站 <https://docs.zephyrproject.org/>`_。

.. only:: development

   .. admonition:: 欢迎阅读 Zephyr ``main`` 分支文档（|version|）。
      :class: welcome

      本站由 Process Mission 维护，提供与英文文档对应的中文译文。
      未翻译的页面及生成参考文档由上游英文站提供。页面右上角的 English 可打开对应原文。
      上游文档与译文可能存在同步时间差，请结合对应版本阅读。

.. raw:: html
   :file: index.html

.. toctree::
   :maxdepth: 1
   :hidden:

   introduction/index.rst
   develop/index.rst
   kernel/index.rst
   services/index.rst
   构建与配置系统 <build/index.rst>
   hardware/index.rst
   contribute/index.rst
   project/index.rst
   security/index.rst
   safety/index.rst
   示例与演示 <samples/index.rst>
   支持的开发板与扩展板 <boards/index.rst>
   releases/index.rst
