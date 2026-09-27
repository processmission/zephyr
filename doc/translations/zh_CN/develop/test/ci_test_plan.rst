.. SPDX-FileCopyrightText: Copyright The Process Mission

.. _ci_test_plan:

CI 测试计划选择器（test_plan_v2）
#################################

CI 测试计划选择器是位于 ``scripts/ci/test_plan_v2.py`` 的模块化 Python 脚本。它分析拉取请求中变更的文件，生成有针对性的 twister 测试计划，只运行可能受改动影响的测试，避免每次提交都执行全量测试。

脚本写出两个产物：

* ``testplan.json``：通过 ``twister --load-tests`` 传给 twister。
* ``.testplan``：供 CI 编排脚本使用的纯文本 ``KEY=value`` 环境文件，包含 ``TWISTER_TESTS``、``TWISTER_NODES`` 和 ``TWISTER_FULL``。

架构
****

选择器围绕 *策略流水线* 构建。每个策略都是独立分析器，执行以下操作：

1. 接收变更文件列表，或尚未被前序策略消费的子集。
2. 按自身逻辑检查这些文件。
3. 返回 :class:`TwisterCall` 描述符列表及已 *处理* 文件集合。

:class:`Orchestrator` 驱动流水线，将所有结果合并到 :class:`PlanAccumulator`，去除重复测试套件并写出文件。

策略顺序
********

策略按固定顺序执行，遵循两个原则：

**具体优先于通用。** 最精确的策略先运行。位于 ``tests/kernel/sched/`` 的文件先由 :class:`DirectTestStrategy` 明确处理，仅运行对应测试，之后兜底的 :class:`MaintainerAreaStrategy` 才有机会加入整个 Kernel 领域的测试。

**消费优先于追加。** 消费型策略先于追加型策略执行。一旦文件被消费，后续策略就不会再看到它。这样可防止同一开发板文件变更还触发驱动兼容性扫描和 Kconfig 全面检查。

当前顺序如下：

.. list-table::
   :header-rows: 1
   :widths: 5 20 10 65

   * - #
     - 策略
     - 是否消费
     - 理由
   * - 0
     - :class:`ComplexityStrategy`
     - 否
     - 使用 pydriller 和 lizard 对补丁集评分。必须最先运行，供 :class:`RiskClassifierStrategy` 使用评分。不生成 twister 调用。
   * - 1
     - :class:`IgnoreStrategy`
     - 是
     - 静默丢弃不可能影响测试的文件，例如文档、CI 工作流和工具。尽早运行可避免后续策略在忽略路径上浪费精力。
   * - 1b
     - :class:`BoilerplateFilter`
     - 是
     - 消费差异完全由空白调整、空行变化、SPDX 许可证标识、版权声明或单独注释分隔符组成的文件。这些改动不影响运行时行为，提前移除可让后续策略专注实质改动。需要 Git 提交范围，否则不执行操作。
   * - 2
     - :class:`DirectTestStrategy`
     - 是
     - 测试或示例文件变化应 *仅* 触发对应测试，而非整个领域的测试。消费该文件可防止修改 ``tests/kernel/sched/main.c`` 时，:class:`MaintainerAreaStrategy` 又加入整个 Kernel 领域的测试。
   * - 3
     - :class:`SnippetStrategy`
     - 是
     - 代码片段变更是独立的，只有在 ``required_snippets`` 中声明该片段的测试需要运行。消费文件可避免后续策略把片段 YAML 当作未知配置文件。
   * - 4
     - :class:`BoardStrategy`
     - 是
     - 开发板专用改动需要对每个开发板变体执行定向集成测试。消费文件可防止开发板 ``.yaml`` 同时匹配 Kconfig 和头文件策略。
   * - 5
     - :class:`SoCStrategy`
     - 是
     - SoC 级改动影响基于该 SoC 系列的所有开发板。消费后可避免同一 ``soc/`` 路径进入 Kconfig 全面检查。
   * - 6
     - :class:`ManifestStrategy`
     - 是
     - ``west.yml`` 变更需要带模块标签的集成测试，而非通用维护者领域测试。消费清单文件可防止兜底策略加入无关测试。
   * - 7
     - :class:`DriverCompatStrategy`
     - 否
     - 追加型：驱动文件也可能受领域模式覆盖，因此不消费文件，:class:`KconfigImpactStrategy` 和 :class:`MaintainerAreaStrategy` 可继续补充覆盖。
   * - 8
     - :class:`DtsBindingStrategy`
     - 否
     - 追加型：绑定变更同时采用基于 overlay 的测试选择和面向开发板的领域调用。
   * - 9
     - :class:`KconfigImpactStrategy`
     - 否
     - 追加型：Kconfig 变更可能影响许多不相关文件；仅发现非广泛使用符号时才消费文件，广泛使用符号所在文件留给兜底策略。
   * - 10
     - :class:`HeaderImpactStrategy`
     - 否
     - 追加型：头文件变更通过包含它的使用者追溯维护者领域。跳过被包含次数超过配置阈值的广泛使用头文件。
   * - 11
     - :class:`MaintainerAreaStrategy`
     - 否
     - 兜底策略：将剩余文件与 ``MAINTAINERS.yml`` 中的领域模式匹配，对每个 ``tests:`` 列表非空的匹配领域生成 ``--test-pattern`` 调用。

模板性内容过滤器
****************

:class:`BoilerplateFilter` 紧随 :class:`IgnoreStrategy`，先于所有测试选择策略运行。它通过 ``git diff`` 检查各变更文件的实际差异，消费所有内容改动均不具实质性的文件：

* **空白与空行改动**：通过 ``git diff -w --ignore-blank-lines`` 检测。如果某文件没有输出，则其所有改动行均仅涉及空白或空行。

* **SPDX 和版权头编辑**：以 ``SPDX-License-Identifier:``、``SPDX-FileCopyrightText:`` 或单词 ``Copyright`` 开头的行。

* **仅含注释分隔符的行**：非空白内容完全由 ``/*``、``*/``、``//``、``#`` 或 ``*`` 字符组成的行，例如重新排版的块注释边框。

只有差异中 **每一行** 新增或删除内容均属于上述类别时才消费文件。只要有一行实质改动，例如语句、宏或声明变化，文件就原样交给后续策略。

未提供 ``--commits`` 时，例如使用 ``--modified-files``，由于缺少提交范围而无法计算差异，过滤器不执行操作，所有文件留在待处理池中。

消费与追加行为
**************

每个策略子类都带有类属性 ``consumes: bool``。

当 ``consumes = True`` 时：
  下一策略运行前，从 ``remaining`` 池移除 *handled* 集合中的文件。适用于策略对其文件类型具有 *最终决定权* 的情况，即后续策略再处理会产生冗余或错误结果。

当 ``consumes = False`` （默认）时：
  无论策略返回什么，文件都留在池中，所有后续策略仍接收同一文件列表。适用于提供 *额外* 测试覆盖、但不要求独占处理权的追加型策略。

.. note::

   ``remaining`` 池为空时，:class:`Orchestrator` 完全跳过策略。非消费型策略不会减少文件，因此“剩余”池只会因消费型策略缩小。一旦池为空，编排器就停止调用策略。

全量运行和回退条件
******************

满足以下任一条件时，编排器在 ``.testplan`` 中设置 ``TWISTER_FULL=True``：

1. **存在未解析文件。** 所有策略运行后，至少一个变更文件未被任何策略 *处理*。脚本会回退到全量运行，避免静默漏掉未知路径的覆盖而放过回归。

2. **显式全量运行信号。** 策略返回 ``full_run=True`` 的 :class:`TwisterCall`。编排器遇到它会立即设置 ``TWISTER_FULL=True``，清空剩余池，停止执行后续调用。策略可借此放弃定向选择，例如整个代码树使用的核心子系统头文件发生变更时。

``TWISTER_FULL=True`` 时，CI 脚本应丢弃 ``testplan.json``，不带 ``--load-tests`` 运行 twister。

节点数量计算
************

``.testplan`` 中的 ``TWISTER_NODES`` 按以下方式计算：

* ``0``：未选中测试。
* ``1``：选中测试数小于 ``--tests-per-builder``，一个构建节点即可容纳。
* ``ceil(total / tests_per_builder)``：其他情况。向上取整确保除不尽时不会超过单个构建节点容量。

``--tests-per-builder`` 默认值为 ``900``。

添加新策略
**********

1. **继承** :class:`SelectionStrategy`，实现两个抽象成员：

   .. code-block:: python

      class MyStrategy(SelectionStrategy):

          consumes: bool = False  # or True if authoritative

          @property
          def name(self):
              return "MyStrategy"

          def analyze(self, changed_files):
              # inspect changed_files
              calls = [...]       # list of TwisterCall
              handled = {...}     # subset of changed_files this strategy owns
              return calls, handled

2. **决定消费还是追加。** 判断后续策略看到同一文件会增加有用覆盖，还是产生冗余／错误结果。若为后者，设 ``consumes = True``。

3. 在 :func:`build_strategies` 中 **插入正确位置**，一般遵循：

   * 消费型策略位于所有追加型策略之前。
   * 更具体的策略位于较通用的策略之前。
   * 不改变文件池的追加型策略可按成本排序，低成本优先。

4. **保护可选依赖**：在 ``analyze`` 内延迟导入，缺少依赖时平稳返回 ``[], set()``。使用 ``# noqa: PLC0415`` 注释抑制延迟导入警告。

5. 在 ``scripts/tests/ci/test_test_plan_v2.py`` 中 **编写单元测试**，覆盖：

   * 正常路径：正确识别文件并选择处理方式。
   * 无操作路径：无关文件不产生调用或已处理集合。
   * 边界情况：磁盘文件缺失、YAML 格式错误、空输入。

共享流水线上下文
****************

:class:`PipelineContext` 是通过 :func:`build_strategies` 传给所有策略的数据类，目前包含：

* ``complexity_score``：补丁集总评分，由 :class:`ComplexityStrategy` 写入、:class:`RiskClassifierStrategy` 读取。
* ``file_metrics``：每个文件对应的 :class:`ComplexityMetrics` 映射，用于详细日志及后续决策。

新增跨策略状态应作为带类型的字段加入 :class:`PipelineContext`，而非保存为策略级实例变量。

验证选择行为的测试策略
**********************

测试套件位于 ``scripts/tests/ci/test_test_plan_v2.py``，使用 pytest 运行：

.. code-block:: bash

   pytest scripts/tests/ci/test_test_plan_v2.py -v

每个策略或共享组件对应一个测试类。每个新策略应包含以下测试类别：

**单元测试（无需 Zephyr 代码树）**
  使用 ``tmp_path`` fixture 创建覆盖各代码路径所需的最小文件系统结构，例如 ``board.yml``、``snippet.yml``、``testcase.yaml``。测试应快速且与外部环境隔离。

**辅助方法测试**
  独立测试路径遍历、YAML 解析和正则提取等内部方法，传入人工构造内容，而不依赖仓库中的真实文件。

**编排器集成测试**
  使用模拟策略及模拟的 :class:`TwisterExecutor`，无需调用 twister 即可测试消费／追加逻辑、全量运行信号和 ``.testplan`` 输出。

**真实代码树集成测试** （可选，``@pytest.mark.integration``）
  可以添加此类测试并用 ``@pytest.mark.integration`` 标记，使其不参与默认运行。它们仅在完整 Zephyr 检出目录中有意义。

新策略的最小测试清单
====================

* 输入列表不含相关文件时，策略不返回调用或已处理文件。
* 对已知有效输入，策略正确识别并返回预期的 :class:`TwisterCall`。
* 文件系统缺少所需文件时，策略不会崩溃。
* 消费型策略的已处理集合必须恰好等于匹配文件。
* 追加型策略的已处理集合应为空，或仅包含其具有最终决定权的文件。

命令行参考
**********

.. code-block:: text

   usage: test_plan_v2.py [-c A..B] [-m FILE] [-f PATH]
                          [-o FILE] [-p PLATFORM] [--maintainers-file FILE]
                          [-T DIR] [--quarantine-list FILE]
                          [--tests-per-builder N] [--disable-strategy NAME]
                          [--detailed-test-id]

   -c A..B              Git commit range (e.g. ``main..HEAD``).  Changed files
                        are derived from ``git diff --name-only A..B``.
   -m FILE              JSON file containing a list of changed file paths.
   -f PATH              Treat PATH as a changed file (repeatable).
   -o FILE              Output JSON file (default: ``testplan.json``).
   -p PLATFORM          Restrict all selections to this platform (repeatable).
   --maintainers-file   Path to ``MAINTAINERS.yml``.
   -T DIR               Extra testsuite root forwarded to every twister call.
   --quarantine-list    Quarantine YAML forwarded to twister.
   --tests-per-builder  Tests per CI builder node (default: 900).
   --disable-strategy   Skip a strategy by name (repeatable).
   --detailed-test-id   Pass ``--detailed-test-id`` to twister.
