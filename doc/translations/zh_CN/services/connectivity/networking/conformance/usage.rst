.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ttcn3_running:

运行一致性测试套件
##################

.. contents::
    :local:
    :depth: 2

一次运行的过程如下。Twister 构建并启动被测系统，测试框架使用 Titan 构建 TTCN-3 套件，套件通过 TAP 接口与运行中的应用通信，Titan 的判定结果即成为测试结果。

一次运行需要什么
****************

* **Titan 安装**，并让 ``TTCN3_DIR`` 指向它。请参阅 :ref:`ttcn3_installing_titan`。
* **第三方 TTCN-3 模块**，使用 :file:`ttcn3/fetch-modules.sh` 获取一次。它们以固定的提交进行克隆，不属于 ``net-tools`` 仓库的一部分。
* **net-tools 的检出目录**，west 工作区中已包含：它位于 :file:`west.yml` 的 ``tools`` 组下，而该组不会被过滤掉。
* **make**，因为 Titan 正是通过它构建套件。
* **该** ``zeth`` **接口**，对于在 IP 层以下工作的套件则为 ``zethL2``。请参阅 :ref:`ttcn3_interfaces`。
* **Root**，对于无法避免使用特权端口或数据包套接字的套件。
* **expect**，对于通过 Titan 主控制器运行的套件。

:ref:`ttcn3_suites` 列出了哪些套件需要其中哪些内容，而 :zephyr_file:`scripts/net/run-conformance-tests.sh` ``--list`` 也会打印相同的信息。

测试框架会先查看是否设置了 ``NET_TOOLS_BASE``，如果设置了就在其中查找 net-tools，否则依次查找相对于 ``ZEPHYR_BASE`` 的 :file:`../tools/net-tools/ttcn3`，以及再向上一级的目录。所有这些都会在构建任何内容之前进行检查，缺少某个组件会附带原因跳过测试，而不是使测试失败。

.. _ttcn3_installing_titan:

安装 Titan
**********

大多数发行版都提供了 Titan 软件包：

.. code-block:: console

   sudo apt install --no-install-recommends eclipse-titan expect
   export TTCN3_DIR=/usr

发行版打包的版本落后于套件所依赖的协议模块，因此如果套件编译失败，请改为从源码构建最新版 Titan。

从源码构建 Titan
================

:file:`net-tools/docker/Dockerfile.ttcn3` 会将 Titan 构建到 :file:`/opt/titan`，它可作为手动构建的参考，既可以作为容器使用，也可以作为可遵循的构建配方。

手动构建 Titan 时必须正确完成两件事。Titan 通过其源代码树中的 :file:`Makefile.personal` 进行配置，而不是通过 ``configure`` 脚本，其中的 ``TTCN3_DIR`` 是安装前缀。另外，``make install`` 必须串行执行：运行时的某些部分会包含由另一部分生成的头文件，并行 make 会在这个竞态中失败。

使用脚本运行套件
****************

:zephyr_file:`scripts/net/run-conformance-tests.sh` 用一条命令完成接下来两节描述的操作，是运行套件的最简便方式：它会查找 net-tools、在缺失时获取模块、创建所选套件所需的接口、在所选套件需要 root 时于 ``sudo`` 下重新运行自身、运行一次 Twister，然后再次拆除这些接口。

.. code-block:: console

   export TTCN3_DIR=/usr
   ./scripts/net/run-conformance-tests.sh

指定套件名称时只会运行这些套件，这是在处理某个套件时保持非特权状态的快捷方式：

.. code-block:: console

   ./scripts/net/run-conformance-tests.sh mdns dns

``--list`` 显示套件以及每个套件所需的内容，``--keep`` 保留接口供下一次运行使用，``--start`` 和 ``--stop`` 仅执行相应的那一半操作。``--help`` 会列出其余选项，以及它检测到的目录。

由于特权运行会以 root 身份创建文件，脚本在退出前会将 Twister 输出目录和套件构建目录的所有权交还给调用用户。

.. _ttcn3_interfaces:

设置网络接口
************

这些套件使用两个 TAP 接口，因为在 IP 层以下工作的套件无法与一个自行应答的主机共享链路。

``zeth``，共享接口
==================

供通过套接字工作的套件使用，此时测试器只是链路上的另一台主机：

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools
   sudo ./net-setup.sh --config zeth.conf start

主机持有 ``192.0.2.2/24`` 和 ``2001:db8::2``；Zephyr 在 ``192.0.2.1`` 和 ``2001:db8::1`` 上应答。将 ``start`` 替换为 ``stop`` 即可拆除。

``zethL2``，无地址接口
======================

供在 IP 层以下工作的套件使用：

.. code-block:: console

   sudo ./net-setup.sh --config zeth-l2.conf --iface zethL2 start

此接口被有意配置为没有 IP 地址。除非另有指示，Linux 会为它在任意接口上持有的任何地址应答地址解析和邻居发现，而来自主机的应答与来自 Zephyr 的应答将无法区分。测试器发送原始帧，因此不需要自己的地址。

该配置设置了三个 sysctl 以阻止主机参与：``arp_ignore=8`` 使其完全不为任何本地地址应答地址解析，``arp_announce=2`` 使其从不使用此接口未持有的地址进行应答，``disable_ipv6=1`` 则不发送邻居通告或路由器请求。

``zethL2`` 这个名称不能随意选择；请参阅 :ref:`ttcn3_test_network`。

使用 Twister 运行套件
*********************

获取一次第三方模块。该脚本可以安全地重复运行：

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools
   ./ttcn3/fetch-modules.sh

然后运行测试：

.. code-block:: console

   export TTCN3_DIR=/usr
   cd $ZEPHYR_BASE
   ./scripts/twister -p native_sim --enable-slow -T tests/net/conformance

必须使用 ``--enable-slow``：这些套件将自己标记为 slow，因为完整运行一次需要数十分钟。``native_sim`` 是它们允许的唯一平台。

可以通过测试标识符选择单个套件，即 ``net.conformance.<suite>``：

.. code-block:: console

   ./scripts/twister -p native_sim --enable-slow -T tests/net/conformance \
       -s net.conformance.mdns

它们还带有 ``net`` 和 ``conformance`` 标签，因此 ``--tag conformance`` 可以选中全部套件。

以 root 身份运行
================

有些套件必须以 root 身份运行。DHCP 定义在端口 67 和 68 上，无法将其移到其他端口，因此测试器无法避免绑定特权端口；而从链路读取帧需要数据包套接字。这些测试在权限不足时会自行跳过。

使用 ``sudo -E``，以便保留 ``TTCN3_DIR`` 和其余环境变量。一次运行要么完全具有特权，要么完全没有特权 — 有关两者为何不能混用，请参阅 :ref:`ttcn3_runner`。

为什么运行是串行的
==================

每个被测系统都在同一接口上应答同一地址，因此同一时间只能运行一个一致性测试。它们会对接口获取独占锁并互相等待，这意味着无论 Twister 被赋予多少作业，整个目录的运行都是串行的。

.. _ttcn3_running_by_hand:

手动运行套件
************

Twister 很方便，但完整跑一圈很慢。在编写或调试套件时，请自行运行这两部分。

启动被测系统并使其保持运行：

.. code-block:: console

   cd $ZEPHYR_BASE
   west build -p -b native_sim -d ../build/mdns tests/net/conformance/mdns
   ../build/mdns/zephyr/zephyr.exe

构建套件并针对它运行：

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools/ttcn3
   ./build.sh mdns
   cd suites/mdns/build
   ./mdns ../mdns.cfg

对于测试用例会创建并行测试组件的套件，请改为通过主控制器启动：

.. code-block:: console

   ttcn3_start ./coap ../coap.cfg

通过指定名称来运行单个测试用例：

.. code-block:: console

   ./mdns ../mdns.cfg MDNS_Suite.tc_a_query

地址、接口和超时都来自套件配置文件的 ``[MODULE_PARAMETERS]`` 节，因此只需编辑一个文件而不是套件本身，就能将运行迁移到不同的链路上。

有一件事测试框架会做，但你必须自己做：将 Titan 的库目录添加到 ``LD_LIBRARY_PATH`` 中。

.. _ttcn3_verdicts:

读取结果
********

Titan 运行结束时，会输出每种判定结果的数量以及本次运行的判定结果：

.. code-block:: console

   Verdict statistics: 0 none (0.00 %), 7 pass (100.00 %), 0 inconc (0.00 %), 0 fail (0.00 %), 0 error (0.00 %).
   Test execution summary: 7 test cases were executed. Overall verdict: pass

``inconc`` 表示测试用例无法得出结论，通常是因为它所依赖的某个事件没有发生。这不是通过。``error`` 表示套件本身失败，而不是被测系统失败。

证据存在于两个位置。Titan 会按套件将日志写入构建目录，日志名称由配置文件中的 ``LogFile`` 设置决定。Twister 会在其输出目录下写入 :file:`twister_harness.log`，其中以 ``INFO`` 级别包含整个套件的输出。

当套件被跳过时
**************

套件所需的所有内容都会在构建任何东西之前检查，缺少某一项会跳过测试而不是使测试失败。原因按检查顺序列出如下：

.. list-table::
   :header-rows: 1

   * - 原因
     - 应如何处理
   * - ``TTCN3_DIR is unset``
     - 安装 Titan 并导出 ``TTCN3_DIR``；请参阅 :ref:`ttcn3_installing_titan`
   * - ``make is not installed``
     - 安装 make；Titan 使用生成的 makefile 构建套件
   * - ``no TTCN-3 suites under ...``
     - 未找到 net-tools；请设置 ``NET_TOOLS_BASE``
   * - ``... has no <suite> suite``
     - net-tools 检出目录早于该套件；请更新它
   * - ``third party modules are missing``
     - 运行 :file:`ttcn3/fetch-modules.sh`
   * - ``the <iface> interface does not exist``
     - 使用 :file:`net-setup.sh` 创建它；请参阅 :ref:`ttcn3_interfaces`
   * - ``ttcn3_start is not in TTCN3_DIR/bin``
     - 安装 ``expect`` 以及包含主控制器的 Titan
   * - ``has to be run as root``
     - 在 ``sudo -E`` 下重新运行，或使用该脚本

故障排查
********

套件无法编译
============

这几乎总是因为发行版打包的 Titan 落后于套件所依赖的协议模块。请从源码构建 Titan。

套件看不到任何内容并超时
========================

检查应用和套件是否在同一接口上：在 IP 层以下工作的套件需要使用 ``zethL2``，而应用必须使用名为同一接口的 ``host-interface`` 属性来构建，该属性由测试在 :file:`boards/native_sim.overlay` 中设置。如果是主机而不是 Zephyr 在链路上应答，则说明 ``zethL2`` 的 sysctl 未生效；可用 ``sysctl net.ipv4.conf.zethL2.arp_ignore`` 确认。

运行挂起或被中断
================

一次运行周围嵌套了四个超时，哪个超时触发就说明问题出在哪里：30 秒用于等待应用的就绪行，1800 秒用于构建套件，600 秒用于运行套件，900 秒用于整个 Twister 测试。运行超时的套件会连同其整个进程组一起被终止，因此不会留下主控制器。

遗留状态
========

使用 :file:`net-setup.sh` 和 ``stop`` 拆除接口。测试获取的锁是临时目录中名为 :file:`zephyr-net-conformance-<euid>.lock` 的文件；进程退出时会释放该锁，因此残留的锁文件是无害的。
