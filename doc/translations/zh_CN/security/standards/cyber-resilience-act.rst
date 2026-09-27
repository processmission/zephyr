.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _cra_faq:

欧盟网络弹性法案（CRA）
#######################

.. warning::
   本文档仅供参考，不构成法律建议。请咨询您的法律顾问，以获取适用于您具体情况的合规指导。

概述
****

网络弹性法案（[CRA24]_）是一部欧盟法规，为投放欧盟市场的具有数字元素的产品（PDE）制定了网络安全要求。该法规于 2024 年 12 月 10 日生效。

.. admonition:: 关键日期
   :class: important

   * **2026 年 6 月 11 日**：评估机构开始运行
   * **2026 年 9 月 11 日**：制造商必须报告漏洞和事件
   * **2027 年 12 月 11 日**：法规全面适用

本页说明 CRA 与在商业产品中使用 Zephyr 的制造商之间的关系，以及 CRA 与作为开源软件管理者的 Zephyr 项目自身之间的关系。

对制造商而言，CRA 规定了基本的网络安全要求（`Annex I Part I`_），以及漏洞处理和报告义务（`Annex I Part II`_）。对于作为开源软件管理者的 Zephyr 项目，CRA 引入了一套量身定制的义务，包括维护网络安全政策、报告被积极利用的漏洞和严重事件，以及与市场监督机构合作。

面向使用 Zephyr 的制造商
************************

CRA 是否适用于我的产品？
========================

如果您为商业目的将具有数字元素的产品（PDE）投放欧盟市场，则 CRA 适用。这包括带有嵌入式软件的硬件设备以及独立软件产品。

我的产品属于哪一类别？
======================

CRA 根据风险将产品分为不同类别：**重要产品** （`Annex III`_）和 **关键产品** （`Annex IV`_）。未列入任一类别产品被视为 **默认产品**，其要求较低。

例如，默认产品通常可以依赖自我评估（参见 :ref:`合规路径 <compliance_path>`），所需的文档和保证要求较少。

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - 类别
     - 简要说明
     - Zephyr 用例示例
   * - 默认
     - 未列为“重要”或“关键”的具有数字元素的产品。
     - - Wi-Fi 智能灯泡或开关（例如运行 Matter over Thread/Wi-Fi）。
       - 用于个人健康管理的可穿戴活动追踪器或智能手表。
       - Bluetooth LE 音频配件或无线传感器标签。
   * - 重要产品（I 类）
     - 风险较高的产品，通常面向消费者，执行与安全或访问相关的功能。
     - - 住宅用智能门锁或门禁读卡器。
       - 管理网络流量的智能家居中枢或路由器。
       - 联网报警系统或安全传感器。
   * - 重要产品（II 类）
     - 用于企业/工业/基础设施场景或承担特权网络角色的高风险产品。
     - - 工业可编程逻辑控制器（PLC）或机器人控制器。
       - 用于设备身份标识的带安全飞地/TEE 的微控制器。
       - 执行边缘处理的工业 IoT 网关。
   * - 关键
     - 一旦遭到破坏可能严重影响关键基础设施或基本服务的产品。
     - - 支持远程关断的智能电表或水表。
       - 硬件安全模块（HSM）或智能卡固件。
       - 用于能源或交通网络的安全关键传感器。

.. admonition:: 核心功能与集成
   :class: important

   分类取决于最终产品的 **核心功能**，而不是它集成的各个组件（`Article 7`_）。

   * 将重要或关键组件（例如安全元件、嵌入式浏览器）集成到另一个产品中，并 **不会** 自动使该产品成为重要或关键产品。
   * 某产品 *能够* 执行重要/关键类别的功能，但其核心功能不同，则 **不** 视为具有该核心功能。

   **示例：**

   * 如果您使用 Zephyr 构建网络防火墙，其核心功能是安全，因此该产品属于重要产品（II 类）。
   * 如果您使用 Zephyr 构建咖啡机，并利用 Zephyr 的网络协议栈功能来保护设备，其核心功能仍然是制作咖啡。这是一款“默认”产品。

   简而言之，在设备中使用安全关键的 Zephyr 功能（如密码学或安全启动）并 **不会** 将该设备提升到更高的风险类别。

有关详细分类，请参见 `Annex III`_ 和 `Annex IV`_。带技术说明的产品类别完整列表见 `Implementing Regulation (EU) 2025/2392`_。

.. _compliance_path:

我必须选择哪条合规路径？
========================

CRA 根据您的产品类别定义了不同的合规评定程序。您必须选择与您的分类以及对协调标准依赖程度相对应的路径。

.. list-table:: CRA 产品类别与评定路径
  :widths: 20 55 25
  :header-rows: 1

  * - 类别
    - 合规评定程序
    - 是否需要第三方审核？
  * - 默认
    - 模块 A（内部生产控制）。由制造商进行自我评估。
    - 否
  * - 重要产品 I 类
    - **仅当** 协调标准完全适用时才可使用模块 A。否则：模块 B + 模块 C，或模块 H。
    - 是，如果标准未被完全使用
  * - 重要产品 II 类
    - 模块 B + 模块 C，或模块 H。（**不** 允许自我评估）。
    - 是（强制）
  * - 关键
    - **欧洲网络安全认证** （例如 EUCC），或模块 B + 模块 C + 模块 H（有待授权法案）。
    - 是（强制）

“模块”指 `Decision No 768/2008/EC`_ （“新立法框架”）中定义、并由 CRA 在 `Annex VIII`_ 中调整的特定评定程序：

* `Module A`_ （内部生产控制）：您自行编写技术文档、执行风险评估并声明合规。无需外部审核员。
* `Module B`_ （EC 型式检验）+ `Module C`_ （型式符合）：公告机构 [#nb]_ 审查技术设计（模块 B）并颁发证书。然后您需确保生产符合该型式（模块 C）。
* `Module H`_ （全面质量保证）：公告机构 [#nb]_ 审核您的质量管理体系（QMS），该体系涵盖设计、生产和测试。

.. [#nb]  公告机构将于 **2026 年 6 月 11 日** 开始运行。

作为制造商，我的主要义务有哪些？
================================

CRA 主要在 `Article 13`_ （产品要求和尽职调查）和 `Article 14`_ （漏洞处理和报告）中规定了制造商的义务。无论产品分类如何，以下核心义务适用于所有具有数字元素产品的制造商。

**风险评估**
  在整个产品生命周期中评估并记录网络安全风险。

**尽职调查**
  在集成第三方组件（包括 Zephyr 等开源软件）时进行尽职调查。

**漏洞处理**
  处理漏洞至少 5 年（支持期），包括接收报告和应用更新。

**事件报告**
  报告影响 Zephyr 的被积极利用的漏洞，以及影响项目基础设施的严重事件。

**技术文档**
  按照 `Article 31`_ 和 `Annex VII`_ 创建文档。

**合规评定**
  按照 `Article 32`_ 和 `Annex VIII`_ 进行合规评定。

**CE 标志**
  加贴 CE 标志并起草欧盟合规声明。

不合规会受到哪些处罚？
======================

* 最高 15,000,000 欧元或全球年营业额的 2.5%（违反 `Article 13`_ 和 `Article 14`_ 的情况）。
* 最高 10,000,000 欧元或营业额的 2%（违反其他义务的情况）。

.. _cra_vulnerability_reporting_obligations:

漏洞报告义务有哪些？
====================

CRA 区分“普通”漏洞（通过常规漏洞管理流程处理）和触发 `Article 14`_ 下严格通知时限的情况：**被积极利用的漏洞** 和 **严重事件**。

下表总结了最低报告步骤。

.. list-table:: 被积极利用的漏洞（`Article 14`_ (1) 和 (2)）
   :header-rows: 1
   :widths: 20 20 60

   * - 步骤
     - 截止时间
     - 内容（最低要求）
   * - 早期预警
     - 知悉后 24 小时内
     - 通过单一报告平台通知您的 CSIRT 协调员和 ENISA，说明您的产品受到被积极利用的漏洞影响。在已知的情况下，说明该产品在哪些成员国可用。
   * - 漏洞通知
     - 知悉后 72 小时内
     - 提供受影响产品的一般信息、漏洞利用和漏洞的一般性质、已采取的纠正或缓解措施，以及用户可以采取的措施。在适用的情况下，说明您认为所通知信息的敏感程度。
   * - 最终报告
     - 在纠正或缓解措施可用后不迟于 14 天
     - 描述该漏洞、其严重程度和影响、利用该漏洞的恶意行为者的信息（如有），以及所提供安全更新或其他纠正措施的详细信息。

.. list-table:: 严重事件（`Article 14`_ (3) 至 (6)）
   :header-rows: 1
   :widths: 20 20 60

   * - 步骤
     - 截止时间
     - 内容（最低要求）
   * - 早期预警
     - 知悉后 24 小时内
     - 通过单一报告平台通知您的 CSIRT 协调员和 ENISA，说明严重事件影响了您产品的安全。说明是否怀疑该事件由非法或恶意行为引起，并在已知的情况下说明该产品在哪些成员国可用。
   * - 事件通知
     - 知悉后 72 小时内
     - 提供事件性质的一般信息、初步评估（包括当时已知的影响/严重程度）、已采取的纠正或缓解措施，以及用户可以采取的措施。在适用的情况下，说明您认为所通知信息的敏感程度。
   * - 最终报告
     - 事件通知后 1 个月内
     - 提供事件的详细描述，包括严重程度和影响、威胁类型或可能根本原因，以及已实施和正在进行的缓解措施。

如何获取 SBOM（软件物料清单）？
===============================

Zephyr 可以使用 ``west spdx`` 命令为您的应用程序自动生成 SBOM。

有关如何配置和使用此工具的详细信息，请参见 :ref:`west spdx <west-spdx>`。

我应该如何处理 Zephyr 漏洞？
============================

作为将 Zephyr 集成到产品中的制造商，您仍需负责漏洞管理，并在适用时负责 CRA 报告。Zephyr 会提供漏洞信息，但您必须针对自己的产品进行评估并采取行动。

一种实用工作流程如下：

1. **及时了解信息**。注册 `Zephyr Vulnerability Alert Registry`_，以便在漏洞披露时收到通知。

2. **评估影响**。对于每份安全公告，使用您的 SBOM 和配置来确定产品中是否存在受影响的 Zephyr 组件、该组件是否可访问以及是否与安全相关。

3. **规划修复**。决定适当的响应措施（例如应用补丁、调整配置等）。

4. **部署修复**。集成、测试并推出所选修复，同时根据需要更新 SBOM 和产品文档。

5. **履行报告义务**。如果该漏洞影响您的产品且被积极利用，或导致严重事件，请按照 `Article 14`_ 的时限以及上一节 :ref:`CRA 漏洞报告义务 <cra_vulnerability_reporting_obligations>` 进行报告。

Zephyr 处理漏洞的时间线是怎样的？
=================================

Zephyr 运行自己的 PSIRT 流程，并设定了分类、通知和披露的目标时间线。这些是 *项目* 时间线，不是制造商的法律截止期限。

根据 `Article 14`_，您的 CRA 报告义务在 *您* 知悉您的产品受到被积极利用的漏洞或严重事件影响时触发。这可能 **早于** 下文列出的某些 Zephyr 里程碑，意味着您可能必须在 Zephyr 修复可用之前或公开披露之前发送早期预警或事件报告。

Zephyr 使用私有的 GitHub 安全公告和禁运期（最多 90 天）来协调修复和披露。完整流程在 :ref:`漏洞报告 <reporting>` 中描述，关键里程碑如下：

* **7 天内**：向初始报告者提供 PSIRT 反馈。
* **30 天内**：通过警报注册表通知制造商，并由项目提供修复。
* **总计最多 90 天**：安全敏感漏洞在禁运期后公开。

我需要在 Zephyr 中报告我发现的漏洞吗？
======================================

**需要**，根据 `Article 13(6)`_，如果您发现集成到您产品中的组件（包括 Zephyr）存在漏洞，则 **必须** 报告。此外，如果您为该漏洞开发了修复，还必须共享相关代码或文档。参见 :ref:`漏洞报告 <reporting>`。

此外，可以考虑根据 `Article 15`_ 向 CSIRT 或 ENISA 自愿报告。

Zephyr 作为开源软件管理者
*************************

Zephyr 在 CRA 下的角色是什么？
==============================

Zephyr 是 `Article 3`_ (14) 所定义的 **“开源软件管理者”**：一个为开发用于商业活动的 PDE 系统性地提供持续支持的法律主体。

Zephyr 在第 24 条下的义务：

**网络安全政策**
  记录安全政策和漏洞处理方式。

**合作**
  与市场监督机构合作以降低风险。

**事件报告**
  报告项目中影响 Zephyr 基础设施的被积极利用的漏洞和严重事件（在 Zephyr 涉及的范围内）。

CRA 是否适用于 Zephyr 贡献者？
==============================

**否。** CRA 不适用于 Zephyr 的个体贡献者（`Recital 18`_）。

开发功能或修复缺陷的贡献者不受 CRA 义务约束。

Zephyr 如何履行其管理者义务？
=============================

`Article 24(1)`_：安全政策（已完成）
  * 记录于 :ref:`安全概述 <security-overview>`
  * 漏洞报告流程：:ref:`漏洞报告 <reporting>`
  * 安全编码指南：:ref:`安全代码 <secure code>`

`Article 24(2)`_：与主管机构合作（进行中）
  * 自 2017 年起注册的 CVE 编号管理机构（CNA）
  * 活跃的 Zephyr 项目安全事件响应团队（PSIRT）
  * **进行中**：确定欧盟的 CSIRT 协调员

`Article 14(1)`_ 和 `Article 14(3)`_：事件报告（进行中）
  * **进行中**：确定 NVD 流程是否适用于 CSIRT/ENISA 报告
  * 计划与欧盟报告要求保持一致

`Article 14(8)`_：用户通知（已完成）
  * 面向制造商和集成商的漏洞警报注册表
  * CVE 发布和安全公告

`Article 52(3)`_：纠正措施（已完成）
  * 已与 CVE 主管机构建立流程
  * 通过 PSIRT 及时响应

外部资源
********

CRA 官方文档
============

* `欧盟 CRA 2024/2847 号条例 <https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847>`_
* `Implementing Regulation (EU) 2025/2392`_ （重要和关键产品类别的技术说明）
* `ENISA CRA 要求与标准映射 <https://www.enisa.europa.eu/publications/cyber-resilience-act-requirements-standards-mapping>`_
* `欧盟委员会 CRA 常见问题解答 <https://digital-strategy.ec.europa.eu/en/faqs/cyber-resilience-act-questions-and-answers>`_

标准和技术规范
==============

相关现有标准：

* `ETSI EN 303 645 <https://www.etsi.org/deliver/etsi_en/303600_303699/303645/>`_ —— 消费物联网网络安全：基线要求

ETSI 正在响应 `CRA Standardisation Request (M/606) <https://ec.europa.eu/growth/tools-databases/enorm/mandate/606_en>`_ 制定协调标准。公开草案标准包括以下产品的特定要求：

* 操作系统（prEN 304 626）
* 浏览器（prEN 304 617）
* 密码管理器（prEN 304 618）
* 防火墙（prEN 304 636）

有关草案标准完整列表以及参与公开咨询的信息，请参见 `ETSI Cyber Resilience Act Portal <https://docbox.etsi.org/cyber/CYBER/Open>`_。

教育资料
========

* `Linux Foundation：理解欧盟 CRA <https://training.linuxfoundation.org/express-learning/understanding-the-eu-cyber-resilience-act-cra-lfel1001>`_
* `Linux Foundation CRA 就绪报告 <https://www.linuxfoundation.org/research/cra-readiness>`_
* `Linux Foundation CRA 合规最佳实践 <https://www.linuxfoundation.org/research/cra-compliance-best-practices>`_
* `OpenSSF CRA 指南 <https://openssf.org/public-policy/eu-cyber-resilience-act/>`_

Zephyr 相关资源
===============

* :ref:`安全概述 <security-overview>`
* :ref:`漏洞报告 <reporting>`
* `Zephyr Vulnerability Alert Registry`_
* :ref:`Zephyr 漏洞 <vulnerabilities>`

..

.. _`Decision No 768/2008/EC`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008D0768
.. _`Module A`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008D0768#d1e41-98-1
.. _`Module B`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008D0768#d1e288-98-1
.. _`Module C`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008D0768#d1e439-98-1
.. _`Module H`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008D0768#d1e1719-98-1

.. _`CRA Requirements-Standards Mapping`: https://www.enisa.europa.eu/publications/cyber-resilience-act-requirements-standards-mapping

.. _`Recital 18`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#rct_18

.. _`Article 3`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_3
.. _`Article 7`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_7
.. _`Article 13`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_13
.. _`Article 13(6)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#013.006
.. _`Article 13(14)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#013.014
.. _`Article 14`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_14
.. _`Article 14(1)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#014.001
.. _`Article 14(3)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#014.003
.. _`Article 14(8)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#014.008
.. _`Article 15`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_15
.. _`Article 24(1)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#024.001
.. _`Article 24(2)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#024.002
.. _`Article 31`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_31
.. _`Article 32`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_32
.. _`Article 52(3)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#052.003

.. _`Annex I Part I`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_I
.. _`Annex I Part II`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_I
.. _`Annex III`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_III
.. _`Annex IV`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_IV
.. _`Annex VII`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_VII
.. _`Annex VIII`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_VIII

.. _`Implementing Regulation (EU) 2025/2392`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025R2392

.. _`Zephyr Vulnerability Alert Registry`: https://www.zephyrproject.org/vulnerability-registry/
