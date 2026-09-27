.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ttcn3_testing:

使用 TTCN-3 进行协议一致性测试
##############################

.. contents::
    :local:
    :depth: 2

Zephyr 的网络协议从两个方向进行覆盖。:zephyr_file:`tests/net` 下的测试使用 C 语言，从内部对实现进行检验，并构建到同一镜像中。用 TTCN-3 编写的一致性测试套件则从外部进行验证：它们通过真实网络接口使用协议进行通信，并根据标准要求检查 Zephyr 发送的内容。

两者能发现不同类型的问题。针对实现编写的测试往往会固化为实现当前的行为。而针对标准编写的套件并不知道实现的具体行为，这正是其意义所在。

TTCN-3 是 ETSI 标准化的测试编写语言。这里的套件使用开源 TTCN-3 编译器 `Eclipse Titan`_ 编译，并与其他用于网络测试的主机侧工具一起存放在 ``net-tools`` 仓库的 :file:`ttcn3` 下。

.. toctree::
   :maxdepth: 1

   usage.rst
   architecture.rst

各部分如何协同工作
******************

一致性测试的 Zephyr 侧仅是被测系统：一个普通应用，配置为启用被测协议。测试相关的任何内容都不会编译到其中，不存在控制通道，套件完全通过网络驱动它。

这些应用以及针对它们运行套件的测试框架位于 :zephyr_file:`tests/net/conformance` 下。Twister 构建并启动应用，一个小型 pytest 测试框架使用 Titan 构建并运行套件，并将 Titan 的判定结果转换为测试结果。

当 Titan、第三方 TTCN-3 模块或网络接口缺失时，每个测试都会自行跳过，因此在尚未为其做好设置的运行中，这些套件不会造成影响。有关一次运行需要什么，请参阅 :ref:`ttcn3_running`；有关各部分如何组合，请参阅 :ref:`ttcn3_architecture`。

.. _ttcn3_suites:

测试套件
********

套件使用哪个接口以及是否必须以 root 身份运行，取决于它的功能：在 IP 层以下工作的套件会从自己独有链路上的数据包套接字读取帧。

.. list-table::
   :header-rows: 1

   * - 套件
     - 被测系统
     - 接口
     - 运行身份
   * - :zephyr_file:`mdns <tests/net/conformance/mdns/README.rst>`
     - :zephyr_file:`tests/net/conformance/mdns`
     - ``zeth``
     - 任意用户
   * - :zephyr_file:`dnssd <tests/net/conformance/dnssd/README.rst>`
     - :zephyr_file:`tests/net/conformance/dnssd`
     - ``zeth``
     - 任意用户
   * - :zephyr_file:`dns <tests/net/conformance/dns/README.rst>`
     - :zephyr_file:`tests/net/conformance/dns`
     - ``zeth``
     - 任意用户
   * - :zephyr_file:`sntp <tests/net/conformance/sntp/README.rst>`
     - :zephyr_file:`tests/net/conformance/sntp`
     - ``zeth``
     - 任意用户
   * - :zephyr_file:`mqtt <tests/net/conformance/mqtt/README.rst>`
     - :zephyr_file:`tests/net/conformance/mqtt`
     - ``zeth``
     - 任意用户
   * - :zephyr_file:`coap <tests/net/conformance/coap/README.rst>`
     - :zephyr_file:`tests/net/conformance/coap`
     - ``zeth``
     - 任意用户
   * - :zephyr_file:`dhcpv4 <tests/net/conformance/dhcpv4/README.rst>`
     - :zephyr_file:`tests/net/conformance/dhcpv4`
     - ``zeth``
     - root
   * - :zephyr_file:`dhcpv4_server <tests/net/conformance/dhcpv4_server/README.rst>`
     - :zephyr_file:`tests/net/conformance/dhcpv4_server`
     - ``zeth``
     - root
   * - :zephyr_file:`arp <tests/net/conformance/arp/README.rst>`
     - :zephyr_file:`tests/net/conformance/arp`
     - ``zethL2``
     - root
   * - :zephyr_file:`ndp <tests/net/conformance/ndp/README.rst>`
     - :zephyr_file:`tests/net/conformance/ndp`
     - ``zethL2``
     - root
   * - :zephyr_file:`tcp <tests/net/conformance/tcp/README.rst>`
     - :zephyr_file:`tests/net/conformance/tcp`
     - ``zethL2``
     - root

添加套件的说明请参阅 :ref:`ttcn3_adding_a_suite`。

.. _ttcn3_known_gaps:

已知缺口
********

如果套件断言的行为与标准不一致，它会在这条断言所在的位置加以说明，以便记录这种差异，而不是将其悄然固化。下面介绍的是另一类缺口：目前没有任何套件覆盖的领域。

DNS-SD 传统单播查询
===================

mDNS 响应程序的主机名侧会按照 :rfc:`6762` 第 6.7 节的要求应答传统单播查询。服务发现侧则不会：它构建自己的消息，在属于单个实例的记录上设置缓存刷新位，使用本会用于组播应答的生命周期，并且既不回显标识符，也不回显问题。修复它意味着要重做那些全部基于固定头部大小计算的名称压缩偏移量。

``dnssd`` 套件在 ``f_check_legacy_shape`` 中记录此问题，而不是断言标准，这样测试就不会一直处于失败状态，直到有人处理它。其中的每项检查都说明了需要随之更改什么。

MQTT 5.0、数据包标识符和重发
============================

``mqtt`` 套件覆盖 MQTT 3.1.1。Zephyr 还实现了 MQTT 5.0（:kconfig:option:`CONFIG_MQTT_VERSION_5_0`），而 Titan 项目没有为其发布协议模块，因此要覆盖它就意味着先编写消息类型，再编写任何测试。

数据包标识符和重发也没有被覆盖。Zephyr 的客户端将两者都留给应用处理：:c:func:`mqtt_publish` 会发送传入的标识符和重复标志，因此针对其中任何一项的测试都会测试被测系统自身的计数器，而不是客户端。

CoAP 块传输和观察
=================

不会运行 ``TD_COAP_BLOCK_01`` 和 ``TD_COAP_OBS_01``。它们访问 ``/large`` 和 ``/obs``，而应用只提供 ``/test``；针对该应用运行时，observe（观察）用例会等待永远不会到达的通知，运行无法结束。添加这两个资源是显而易见的下一步。

重叠的 DNS 查询
===============

解析器在向没有未完成请求的服务器发送查询之前，会更新其源端口，而在默认一次一个查询的情况下，这意味着每次查询都会如此。在一个服务器上重叠的查询仍会共享端口，因此在这种情况下，``dns`` 套件中的检查无法捕获回归。请参阅 :rfc:`5452` 第 9.2 节。

其他 TTCN-3 套件
****************

Eclipse Titan 项目以独立仓库的形式，为大量协议发布了协议模块和测试端口，这些仓库位于 `gitlab.eclipse.org/eclipse/titan`_。这里的套件基于这些模块和端口构建，而不是定义自己的消息格式。

那里也存在一些完整的套件。``titan.misc`` 包含一个 CoAP 一致性测试套件，可以针对 :zephyr:code-sample:`coap-server` 示例运行；有关该套件，请参阅 :ref:`coap_sock_interface`。

一个较旧的 TCP TTCN-3 套件由 Intel 为 TCP 重写工作编写，为 ``tcp`` 套件的覆盖范围提供了参考，但其代码完全没有被使用。它通过 JSON 控制通道驱动 Zephyr，并断言协议栈的内部状态名称，而该通道所需的选项已被移除；请参阅 4.5 迁移指南。

.. _Eclipse Titan: https://projects.eclipse.org/projects/tools.titan
.. _gitlab.eclipse.org/eclipse/titan: https://gitlab.eclipse.org/eclipse/titan
