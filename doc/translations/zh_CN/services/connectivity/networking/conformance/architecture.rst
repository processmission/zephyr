.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ttcn3_architecture:

一致性测试是如何组织的
######################

.. contents::
    :local:
    :depth: 2

共有四个组成部分，分布在两个代码仓库中，并且它们仅在链路上交汇：Zephyr 应用、Twister 和 pytest 测试框架、围绕 Eclipse Titan 的 shell 封装脚本，以及 TTCN-3 测试套件本身。

各个组成部分
************

.. graphviz::
   :caption: 什么构建什么，以及两半在哪里交汇
   :alt: Diagram showing Twister and the pytest harness driving both a Zephyr
       application and a Titan built TTCN-3 suite, which meet only at a tap
       interface.

   digraph ttcn3_pieces {
       rankdir=TB;
       node [shape=box, style=filled, fillcolor="#e8e8e8", fontname="sans-serif"];
       edge [arrowsize=0.8];

       twister [label="Twister", fillcolor="#cce5ff"];
       harness [label="pytest harness\n(ttcn3_runner.py)", fillcolor="#cce5ff"];

       subgraph cluster_zephyr {
           label="zephyr";
           style=dashed;
           fontname="sans-serif";
           sut [label="System under test\n(native_sim)"];
       }

       subgraph cluster_nettools {
           label="net-tools";
           style=dashed;
           fontname="sans-serif";
           build [label="build.sh\n+ Eclipse Titan"];
           suite [label="TTCN-3 suite\nexecutable"];
       }

       tap [label="zeth / zethL2\ntap interface", shape=ellipse, fillcolor="#ffe0b2"];

       twister -> harness [label="harness: pytest"];
       harness -> sut [label="start, read ready line"];
       harness -> build [label="build"];
       build -> suite;
       harness -> suite [label="run, read verdict"];
       sut -> tap [dir=both, label="the protocol"];
       suite -> tap [dir=both];
   }

Twister
   构建被测系统、启动它，并针对它运行 pytest 测试框架。它提供测试标识符、平台限制以及整个测试的 900 秒预算。

pytest 测试框架
   :zephyr_file:`tests/net/conformance/ttcn3_runner.py` 由每个测试共享。它决定测试套件是否可以运行、获取接口锁、构建并运行套件，并读取判定结果。

被测系统
   一个启用了相应协议的普通 Zephyr 应用。测试相关的任何内容都不会编译到其中。

build.sh 和 Eclipse Titan
   主机侧构建。Titan 将 TTCN-3 编译为 C++ 并生成 makefile；:file:`build.sh` 负责组织源代码，以便完成这一过程。

TTCN-3 套件可执行文件
   测试本身，从外部驱动协议。

TAP 接口
   这是两部分唯一共享的内容。Zephyr 镜像中没有控制通道、共享内存或测试挂钩。

Zephyr 侧
*********

被测系统
========

每个应用都刻意保持普通：启用协议，执行测试套件需要观察的保持流量持续传输所需的操作，并打印一行独特的就绪信息。该行是应用与测试框架之间唯一的约定 — 测试框架借此在套件开始发送数据之前得知协议栈已启动。

套件目录包含：

.. code-block:: none

   tests/net/conformance/<suite>/
       CMakeLists.txt
       prj.conf
       README.rst
       tests.yaml
       src/main.c
       pytest/pytest.ini
       pytest/conftest.py
       pytest/test_<suite>_conformance.py

Twister 集成
============

每个 :file:`tests.yaml` 都共享同一个块：

.. code-block:: yaml

   common:
     harness: pytest
     slow: true
     timeout: 900
     platform_allow:
       - native_sim
     integration_platforms:
       - native_sim

``harness: pytest`` 将运行交给测试框架，而不是读取控制台输出以获取 ztest 摘要。``slow: true`` 使这些套件不参与普通的 Twister 运行，因为完整运行一次需要数十分钟。900 秒超时必须涵盖套件的构建和运行。``native_sim`` 是唯一的平台，因为正是 TAP 驱动将被测系统连接到真实链路上。

测试本身只有三行：请求锁、等待就绪行、运行套件。

.. code-block:: python

   def test_mdns_conformance(network_lock, dut, suite_binary):
       dut.readlines_until(regex='mDNS responder ready', timeout=30.0)
       run_suite(suite_binary, SUITE)

``network_lock`` 参数故意放在最前面；见下文。:file:`conftest.py` 在每个测试目录中都相同，只做一件事：将共享运行器放到 ``sys.path`` 中，并重新导出锁夹具。

.. _ttcn3_runner:

测试框架
********

.. mermaid::
   :caption: 一次一致性测试：从获取锁到得出判定结果
   :alt: Sequence diagram showing the harness taking the interface lock before
       starting the system under test, then building and running the suite and
       parsing its verdict before releasing the lock.

   sequenceDiagram
       participant T as Twister
       participant H as Harness<br/>(ttcn3_runner.py)
       participant Z as System under test
       participant B as build.sh + Titan
       participant S as TTCN-3 suite

       T->>H: start test (900 s budget)
       H->>H: flock(LOCK_EX) on the interface
       Note over H,Z: the lock is taken before the DUT fixture,<br/>so nothing starts while another test runs
       H->>Z: start
       Z-->>H: ready line (30 s)
       H->>B: build the suite (1800 s)
       B-->>H: executable
       H->>S: run against the running application (600 s)
       S-->>H: verdict statistics, overall verdict
       H->>H: release the lock
       H-->>T: pass or fail

下面的所有内容都位于 :zephyr_file:`tests/net/conformance/ttcn3_runner.py` 中。

持有接口
========

Twister 在自己的 pytest 进程中运行每个测试，因此在一个测试与另一个测试之间进行互斥必须在进程之间生效。测试框架在会话作用域的夹具中，对锁文件获取独占 ``flock``。

顺序与锁同样重要。夹具是在 ``dut`` 夹具 *之前* 请求的，因此在另一个一致性测试持有接口时，被测系统甚至不会启动 —— 两个应用同时应答 ``192.0.2.1`` 会使两个套件都陷入混乱。

锁文件名中包含有效用户 ID。特权套件以 root 运行，而 root 无法打开另一个用户在粘滞临时目录中留下的锁文件。由于一次运行要么完全具有特权，要么完全没有特权，按用户加锁仍能排除所有可能冲突的运行 — 这也是为什么不能同时启动特权运行和非特权运行。

套件特征
========

套件的三项信息从 :file:`suites/<name>/build.conf` 中读取：

``MODE=parallel``
   测试用例会创建并行测试组件，因此套件通过 Titan 的主控制器运行，而不是作为单个可执行文件运行，并且必须安装 ``expect``。

``PRIVILEGED=yes``
   套件会绑定特权端口或打开数据包套接字，因此必须以 root 运行。

``L2=yes``
   套件在 IP 层以下工作，因此它需要使用 ``zethL2`` 而不是 ``zeth``。

:file:`build.sh` 将该文件作为 shell 片段加载，这就是它使用 shell 赋值形式编写的原因；测试框架只在其内部匹配子字符串。

构建并运行套件
==============

构建过程会在 1800 秒预算内运行 :file:`build.sh <suite>`，生成 :file:`suites/<suite>/build/<suite>`。

运行过程必须应对 Titan 的两种不同安装方式。发行版软件包将其库放在 :file:`{TTCN3_DIR}/lib/titan` 中，源码构建则放在 :file:`{TTCN3_DIR}/lib` 中；测试框架会选择存在的那个路径，并将其添加到 ``LD_LIBRARY_PATH`` 前面，同时将 :file:`{TTCN3_DIR}/bin` 添加到 ``PATH`` 前面。并行套件使用 ``ttcn3_start`` 启动，其他套件则直接启动。

套件在新会话中启动，这样超时运行的套件可以连同它启动的所有内容一起被终止 — 否则仍在运行的主控制器会为下一个测试持有接口。

将判定结果转换为测试结果
========================

两个正则表达式匹配 Titan 在运行结束时打印的行，并断言三件事：确实打印了判定结果、至少运行了一个测试用例，以及总体判定结果为 ``pass``。没有产生输出的套件，或因为所有用例都被过滤掉而没有运行任何内容的套件，会判定为失败，而不是悄然通过。有关判定结果的含义，请参阅 :ref:`ttcn3_verdicts`。

主机侧
******

下面的所有内容都位于 ``net-tools`` 仓库的 :file:`ttcn3` 目录下。

布局
====

.. code-block:: none

   ttcn3/
       common/            shared TTCN-3 modules and the ethernet test port
       modules/           third party modules, cloned, not in git
       modules.txt        which modules, at which commit
       fetch-modules.sh   clone or check out the pinned commits
       build.sh           build one suite
       suites/<name>/     the suite, its sources.txt and its .cfg

套件是如何构建的
================

:file:`build.sh` 会清空套件的构建目录，并以扁平方式重新构建，将其需要的每个源代码文件通过符号链接并排放置在一个目录中。

扁平化并非为了整洁，而是一种变通方法。Titan 生成的 makefile 使用 ``sed`` 构建依赖规则，并把目标主干（target stem）用作模式，而一旦源代码通过包含斜杠的路径来命名，这种规则就会失效。因此，每个源代码文件都必须能通过其裸名称访问。

链接顺序依次是套件自身的源代码、:file:`common`、:file:`common/sources.txt` 中指定的模块源代码，以及套件自身 :file:`sources.txt` 中指定的模块源代码。然后由 ``ttcn3_makefilegen`` 生成 makefile — 对于单模式套件使用 ``-s``，并行套件则不使用 — 再由 ``make`` 构建。

共享 TTCN-3 层
==============

``Zephyr_SUT`` 保存每个套件共享的模块参数。套件绝不会将地址或超时写入自身；它从这里获取这些参数，因此只需编辑一个配置文件，就能将运行迁移到不同的链路上。

.. list-table::
   :header-rows: 1

   * - 参数
     - 默认值
     - 含义
   * - ``tsp_sut_ipv4``
     - ``192.0.2.1``
     - Zephyr 应答的地址
   * - ``tsp_sut_ipv6``
     - ``2001:db8::1``
     - Zephyr 应答的地址（IPv6）
   * - ``tsp_tester_ipv4``
     - ``192.0.2.2``
     - 套件应答的地址
   * - ``tsp_tester_ipv6``
     - ``2001:db8::2``
     - 套件应答的地址（IPv6）
   * - ``tsp_tester_interface``
     - ``zeth``
     - 链路本地组播所需
   * - ``tsp_sut_hostname``
     - ``zephyr``
     - 响应者拥有的名称
   * - ``tsp_response_timeout``
     - ``5.0``
     - 一个应答可以花费的最长时间
   * - ``tsp_silence_timeout``
     - ``2.0``
     - 静默监视的时长

``Zephyr_Transport`` 提供 ``Zephyr_Tester`` 组件，其中包含 ``IPL4asp`` 端口，以及用于监听、打开、发送、带保护定时器接收，以及断言没有数据到达的辅助函数。基于套接字的套件会扩展该组件，而不是自行打开套接字。

``ARP_Types`` 是手写的，位于 :file:`common` 而不是 ``arp`` 套件中，因为在没有其他组件应答的链路上，任何在 IP 层以下工作的套件都必须自行应答地址解析。Titan 项目没有发布 ARP 模块。

以太网测试端口
==============

Titan 发布了一个原始链路层测试端口 ``LANL2asp``，但此处不使用它。该端口使用 libpcap 进行捕获，并以零读取超时打开句柄，这在 Linux 上意味着“等到捕获块填满”。在像测试链路这样安静的链路上，帧永远不会到达测试，而且没有任何参数可以改变这一点。

:file:`common/Ethernet_PT.cc` 改为读取数据包套接字，每到达一个帧就将其上交。它接受三个测试端口参数：``interface`` （必需）；``source_address``，默认使用接口自身的地址；以及 ``ethertype``，设置后仅上传该类型的帧。

第三方模块
==========

这些套件基于 Titan 项目发布的协议模块和测试端口构建，而不是定义自己的消息格式。共使用十一个代码仓库，每个仓库都固定到 :file:`modules.txt` 中的某个提交，并由 :file:`fetch-modules.sh` 按需克隆。这些仓库并未以 vendored 方式纳入，且克隆目录被 git 忽略，因此今天通过测试的套件，明天仍然可以构建。移动固定版本只需修改一行并重新运行。

上游模块采用 EPL-2.0 许可证，而这里编写的所有内容均采用 Apache-2.0。两者都经过 OSI 批准，这正是 Zephyr 对永远不会成为 Zephyr 镜像一部分的工具所要求的；请参阅 :ref:`external-contributions`。

.. _ttcn3_test_network:

测试网络
********

``zeth`` 是一个普通的 TAP 接口，两侧都有地址，使用它的套件只是链路上的另一台主机。``zethL2`` 完全没有地址，并且主机被配置为不在其上应答，因此唯一响应地址解析的就是 Zephyr。:ref:`ttcn3_interfaces` 介绍了如何创建这些接口。

.. warning::

   ``zethL2`` 这个名称被写入三个必须保持一致的位置，但没有任何机制检查它们是否一致：

   * :zephyr_file:`tests/net/conformance/ttcn3_runner.py` 中的 ``L2_INTERFACE``，它决定测试运行之前必须存在哪个接口
   * 每个使用 ``zethL2`` 的测试的 :file:`boards/native_sim.overlay` 中的 ``host-interface``，它决定被测系统出现在哪里
   * 每个使用 ``zethL2`` 的套件的配置文件中的 ``system.pt.interface``，它决定套件在哪里监听

   不匹配会表现为套件看不到任何帧并超时，而不会表现为错误。

.. _ttcn3_adding_a_suite:

添加套件
********

一个套件由两部分组成，分别位于两个代码仓库中，并且在处理任何一部分之前需要做出一个决定。

选择形态
========

**套接字还是原始帧。** 如果套件可以通过 UDP 或 TCP 表达其意图，则应扩展 ``Zephyr_Tester``，使用 ``IPL4asp`` 端口，在 ``zeth`` 上运行，并且不需要特权。如果套件必须自己查看或发送帧，则应使用 ``Ethernet_Port``，在 ``zethL2`` 上运行，必须以 root 身份运行，并且必须自行应答地址解析，因为该链路上没有其他组件会这么做。优先使用套接字；原始帧方式需要额外一个接口并会触发密码提示。

**单模式还是并行模式。** 除非测试用例会创建并行测试组件，否则使用单模式。并行模式需要 Titan 的主控制器并依赖 ``expect``，而且会使套件更难手动运行。

The host side
=============

创建 :file:`suites/<name>`，其中包含 TTCN-3 源代码、一个列出套件所需模块源代码的 :file:`sources.txt`，以及一个包含模块参数和要执行的测试用例列表的 :file:`<name>.cfg`。仅运行第三方模块测试用例的套件不需要自己的源代码 — ``coap`` 就是一个完整示例。

从 ``Zephyr_SUT`` 获取地址和超时。将任何新的上游模块及其固定的提交添加到 :file:`modules.txt`。如果套件是并行、特权或工作在 IP 层以下，则添加一个 :file:`build.conf`。

The Zephyr side
===============

在 :zephyr_file:`tests/net/conformance` 下创建应用，采用如上所示的布局。:file:`src/main.c` 启用协议、生成套件需要观察的流量，并打印一行独特的就绪信息。:file:`tests.yaml` 复制公共块，并将测试命名为 ``net.conformance.<name>``。

在三个 pytest 文件中，:file:`pytest.ini` 和 :file:`conftest.py` 会原样复制；:file:`test_<name>_conformance.py` 仅在套件名称和它等待的就绪行上有所不同。

记录不一致之处
==============

如果套件断言的行为与标准不一致，请在做出断言的位置加以说明，以便记录这种差异，而不是将其悄然固化。任何套件都未覆盖的内容应放入 :ref:`ttcn3_known_gaps`，而添加新套件正是向 :ref:`ttcn3_suites` 添加一行记录的良机。

试用
====

首先按照 :ref:`ttcn3_running_by_hand` 中的说明手动运行这两部分，只有在套件通过后才通过 Twister 运行。预计首次构建会比较慢，并请记住，缺少前置条件会跳过测试而不是使其失败 — 看似瞬间通过的套件很可能从未运行过。
