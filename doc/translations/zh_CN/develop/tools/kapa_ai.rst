.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _kapa_ai:

Kapa.ai 文档助手
################

.. note::

   本站未启用 Kapa.ai 助手。下文介绍的是
   `Zephyr 官方文档站 <https://docs.zephyrproject.org/latest/>`_ 的功能。

Zephyr 文档网站提供由 Kapa.ai 驱动的 AI 助手。它使用 Zephyr 自身的文档、源码和 GitHub 活动作为知识来源，详见下方 `数据来源`_，可以用自然语言回答自由提问，并引用生成答案所依据的文档和资源。

同一知识库也通过 `Model Context Protocol <https://modelcontextprotocol.io/>`_ （MCP）服务器开放，让外部 AI 助手和 IDE 直接查询 Zephyr 知识，详见 `使用 MCP 服务器`_。

.. note::

   回答由 AI 生成，可能不准确。请始终对照官方文档核实重要信息，将助手作为探索起点，而非权威来源。

使用聊天助手
************

每个文档页面都可以打开聊天助手：

* 点击页面底部的聊天助手按钮，或者
* 按 :kbd:`Ctrl+K`，macOS 上按 :kbd:`Cmd+K`，即可随时打开。

助手在侧边栏打开，可以使用日常语言提问，例如 *“如何在设备树中配置 UART 设备？”* 或 *“工作队列与线程有什么区别？”*。回答会链接到相关文档、GitHub 议题或源文件，方便深入了解。

首次使用时，会显示一次性同意页面，说明功能工作方式和收集的数据，详见下方 `隐私`_。

.. tip::

   不必用英语提问。助手会检测所用语言，并用同一种语言回答，因此可以使用中文、英语、西班牙语、日语、法语、德语等多种语言交流。

AI 搜索
*******

除聊天助手外，Kapa.ai 也可以驱动文档搜索框：

#. 点击搜索框旁的齿轮图标 :guilabel:`Search settings`。
#. 从菜单选择 :guilabel:`Kapa AI search`。
#. 输入查询并按 :kbd:`Enter`。

查询将由 AI 助手回答，而不使用内置关键词搜索。选择会被保存，后续搜索持续使用所选引擎，直到再次更改。

使用 MCP 服务器
***************

Kapa.ai 也将 Zephyr 知识库作为 :abbr:`MCP (Model Context Protocol)` 服务器开放。MCP 是开放标准，让 AI 助手和支持 AI 的 IDE 连接外部工具与知识源。为助手添加 Zephyr MCP 服务器后，它即可代为查询最新 Zephyr 文档、源码和 GitHub 活动。

服务器使用可流式传输的 HTTP 传输方式，端点如下：

.. code-block:: none

   https://zephyrproject.mcp.kapa.ai

具体配置步骤取决于 MCP 客户端。多数客户端读取带有 ``mcpServers`` 部分的 JSON 配置文件，例如：

.. code-block:: json

   {
     "mcpServers": {
       "zephyr-docs": {
         "url": "https://zephyrproject.mcp.kapa.ai"
       }
     }
   }

另一些客户端要求通过本地 stdio 桥接启动服务器，例如 `mcp-remote <https://www.npmjs.com/package/mcp-remote>`_：

.. code-block:: json

   {
     "mcpServers": {
       "zephyr-docs": {
         "command": "npx", "args": ["-y", "mcp-remote", "https://zephyrproject.mcp.kapa.ai"]
       }
     }
   }

具体配置文件位置和语法，请参阅所用 MCP 客户端（AI 编程助手、IDE 扩展等）的文档。

.. tip::

   将 MCP 服务器连接到 AI 编程助手后，助手可以回答 Zephyr 问题，并根据项目实际文档和源码提出代码建议，而不只是依赖训练数据。

数据来源
********

Kapa.ai 仅根据以下 Zephyr 项目来源生成回答，并按所列频率同步：

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - 来源
     - 详情
     - 更新频率
   * - 源代码
     - ``zephyrproject-rtos/zephyr`` 仓库中除 ``boards/`` 和 ``doc/`` 目录外的 C、Markdown、Python 和文本文件
     - 每小时
   * - API 参考
     - https://docs.zephyrproject.org/latest/doxygen/html/index.html
     - 每天
   * - 设备树绑定
     - https://docs.zephyrproject.org/latest/build/dts/api/bindings.html
     - 每天
   * - 主文档
     - https://docs.zephyrproject.org/latest/，不包括 API 参考和设备树绑定部分
     - 每天
   * - 项目 Wiki
     - https://github.com/zephyrproject-rtos/zephyr/wiki
     - 每天
   * - GitHub 议题
     - ``zephyrproject-rtos/zephyr`` 最近 6 个月的议题
     - 每 5 分钟
   * - GitHub 拉取请求
     - ``zephyrproject-rtos/zephyr`` 最近 6 个月的拉取请求，不包括未合并便关闭的请求
     - 每 10 分钟

权威且最新的配置，参见 `Kapa.ai page on the Zephyr project infrastructure wiki <https://github.com/zephyrproject-rtos/infrastructure/wiki/Kapa.ai>`_。

隐私
****

助手根据你的问题，结合 Zephyr 文档、源码、GitHub 议题和拉取请求提供回答。问题与交互可能被匿名收集和分析，用于识别需要澄清的内容并改进文档。不会收集可识别个人身份的信息。
