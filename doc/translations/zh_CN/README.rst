.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. raw:: html

   <a href="https://www.zephyrproject.org">
     <p align="center">
       <picture>
         <source media="(prefers-color-scheme: dark)" srcset="doc/_static/images/logo-readme-dark.svg">
         <source media="(prefers-color-scheme: light)" srcset="doc/_static/images/logo-readme-light.svg">
         <img src="doc/_static/images/logo-readme-light.svg">
       </picture>
     </p>
   </a>

   <a href="https://bestpractices.coreinfrastructure.org/projects/74"><img src="https://bestpractices.coreinfrastructure.org/projects/74/badge"></a>
   <a href="https://scorecard.dev/viewer/?uri=github.com/zephyrproject-rtos/zephyr"><img src="https://api.securityscorecards.dev/projects/github.com/zephyrproject-rtos/zephyr/badge"></a>
   <a href="https://github.com/zephyrproject-rtos/zephyr/actions/workflows/twister.yaml?query=branch%3Amain"><img src="https://github.com/zephyrproject-rtos/zephyr/actions/workflows/twister.yaml/badge.svg?event=push"></a>


Zephyr 是一个可扩展的实时操作系统（RTOS），支持多种硬件架构，
针对资源受限的设备进行优化，并在设计中重视安全性。

Zephyr OS 基于小型内核，面向资源受限的系统，
适用于嵌入式环境传感器、LED 穿戴设备、智能手表和物联网无线网关等设备。

Zephyr 内核支持 ARM（Cortex-A、Cortex-R、Cortex-M）、Intel x86、ARC、
Tensilica Xtensa、RISC-V、SPARC、MIPS 等架构，以及大量 :ref:`开发板 <boards>`。

.. below included in doc/introduction/introduction.rst


入门指南
********

欢迎使用 Zephyr！请先阅读 :ref:`Zephyr 简介 <introducing_zephyr>`，
再按照 :ref:`入门指南 <getting_started>` 开始开发。

.. start_include_here

社区支持
********

社区通过邮件列表和 Discord 提供支持；详情见下方资源列表。

.. _project-resources:

资源
****

以下是帮助你快速了解项目的资源：

.. _getting-started:

入门指南
--------

  | 📖 :doc:`Zephyr 文档 </index>`
  | 🚀 :ref:`入门指南 <getting_started>`
  | 🙋🏽 :ref:`提问建议 <help>`
  | 💻 :doc:`代码示例 </samples/index>`

代码与开发
----------

  | 🌐 `源代码仓库 <Source Code Repository_>`_
  | 📦 `版本发布 <Releases_>`_
  | 🤝 :doc:`贡献指南 </contribute/index>`

社区与支持
----------

  | 💬 `Discord 社区 <Discord Server_>`_，用于实时交流
  | 📧 `用户邮件列表（users@lists.zephyrproject.org） <User mailing list (users@lists.zephyrproject.org)_>`_
  | 📧 `开发者邮件列表（devel@lists.zephyrproject.org） <Developer mailing list (devel@lists.zephyrproject.org)_>`_
  | 📬 `其他项目邮件列表 <Other project mailing lists_>`_
  | 📚 `项目 Wiki <Project Wiki_>`_

问题跟踪与安全
--------------

  | 🐛 `GitHub 问题跟踪 <GitHub Issues_>`_
  | 🔒 :doc:`安全文档 </security/index>`
  | 🛡️ `安全公告 <Security Advisories Repository_>`_
  | ⚠️ 在 vulnerabilities@zephyrproject.org 报告安全漏洞

其他资源
--------
  | 🌐 `Zephyr 项目网站 <Zephyr Project Website_>`_
  | 📺 `Zephyr 技术分享 <Zephyr Tech Talks_>`_

.. _Zephyr Project Website: https://www.zephyrproject.org
.. _Discord Server: https://chat.zephyrproject.org
.. _supported boards: https://docs.zephyrproject.org/latest/boards/index.html
.. _Zephyr Documentation: https://docs.zephyrproject.org
.. _Introduction to Zephyr: https://docs.zephyrproject.org/latest/introduction/index.html
.. _Getting Started Guide: https://docs.zephyrproject.org/latest/develop/getting_started/index.html
.. _Contribution Guide: https://docs.zephyrproject.org/latest/contribute/index.html
.. _Source Code Repository: https://github.com/zephyrproject-rtos/zephyr
.. _GitHub Issues: https://github.com/zephyrproject-rtos/zephyr/issues
.. _Releases: https://github.com/zephyrproject-rtos/zephyr/releases
.. _Project Wiki: https://github.com/zephyrproject-rtos/zephyr/wiki
.. _User mailing list (users@lists.zephyrproject.org): https://lists.zephyrproject.org/g/users
.. _Developer mailing list (devel@lists.zephyrproject.org): https://lists.zephyrproject.org/g/devel
.. _Other project mailing lists: https://lists.zephyrproject.org/g/main/subgroups
.. _Code samples: https://docs.zephyrproject.org/latest/samples/index.html
.. _Security documentation: https://docs.zephyrproject.org/latest/security/index.html
.. _Security Advisories Repository: https://github.com/zephyrproject-rtos/zephyr/security
.. _Tips when asking for help: https://docs.zephyrproject.org/latest/develop/getting_started/index.html#asking-for-help
.. _Zephyr Tech Talks: https://www.zephyrproject.org/tech-talks
