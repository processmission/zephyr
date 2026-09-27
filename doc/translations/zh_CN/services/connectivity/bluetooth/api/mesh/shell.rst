.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_shell:

蓝牙 Mesh Shell
###############

蓝牙 Mesh shell 子系统为 :ref:`shell_api` 模块提供了一组蓝牙 Mesh shell 命令。它允许通过交互式界面测试和探索蓝牙 Mesh API，而无需编写应用程序。

蓝牙 Mesh shell 接口提供对大多数蓝牙 Mesh 功能的访问，包括配网、配置和消息发送。

前置条件
********

蓝牙 Mesh shell 子系统依赖应用程序创建组成数据并完成 Mesh 初始化。

应用程序
********

使用蓝牙 Mesh shell 子系统最简单的方式是通过 ``tests/bluetooth/mesh_shell`` 下的蓝牙 Mesh shell 应用程序。有关如何连接蓝牙 Mesh shell 应用程序并与之交互的信息，请参阅 :ref:`shell_api`

基本用法
********

蓝牙 Mesh shell 子系统添加了一个 ``mesh`` 命令，其中包含一组子命令。设备每次启动时，请确保在调用任何其他蓝牙 Mesh shell 命令之前调用 ``mesh init``::

        uart:~$ mesh init

这样做是为了确保所有可用的日志都会打印到 shell 输出中。

配网
====

Mesh 节点必须完成配网才能加入网络。仅在设备首次启动时需要执行此操作，因为设备会在重启之间记住其配网数据。

最简单的设备配网方式是通过自身配网。为此，用户必须使用默认网络密钥和地址 ``0x0001`` 为设备配网，请执行::

        uart:~$ mesh prov local 0 0x0001

由于所有 Mesh 节点都使用相同的默认网络密钥值，因此只要为多个设备分配不重叠的单播地址，就可以在这些设备上执行此操作。或者，要将设备配网到现有网络中，可以使用 ``mesh prov pb-adv on`` 或 ``mesh prov pb-gatt on`` 启用未配网信标。外部配网器可以接收这些信标，并将节点配网到其网络中。

Mesh 节点加入网络后，可以通过通用配置命令控制其传输参数：

* 要设置目标地址，请调用 ``mesh target dst <Addr>``
* 要设置网络密钥索引，请调用 ``mesh target net <NetKeyIdx>``
* 要设置应用密钥索引，请调用 ``mesh target app <AppKeyIdx>``

默认情况下，传输参数设置为将消息发送到配网时获得的地址和网络密钥。

配置
====

通过将目标地址设置为本地单播地址，也就是 ``0x0001`` 这个地址（上面 ``mesh prov local`` 命令中的地址），我们可以通过任意 :ref:`bluetooth_mesh_shell_cfg_cli` 命令执行自配置。

第一步最好是读取节点自身的组成数据::

        uart:~$ mesh models cfg get-comp

这将打印节点的组成数据列表，其中包括其模型 ID 列表。

接下来，由于设备默认没有应用密钥，因此最好添加一个::

        uart:~$ mesh models cfg appkey add 0 0

消息发送
========

添加应用密钥后（见上文），Mesh 节点的传输参数全部有效，蓝牙 Mesh shell 可以通过网络发送原始 Mesh 消息。

例如，要发送 Generic OnOff Set 消息，请调用::

        uart:~$ mesh test net-send 82020100

.. note::
        模型消息中的所有多字节字段都采用小端序，操作码除外。

消息将使用当前网络密钥索引和应用密钥索引发送到当前目标地址。由于目标地址默认指向本地单播地址，设备只会向自身发送数据包。要将目标地址更改为 All Nodes 广播地址，请调用::

        uart:~$ mesh target dst 0xffff

将目标地址设置为 ``0xffff`` 后，网络中已配置网络密钥和应用密钥的任何其他 Mesh 节点都将接收并处理我们发送的消息。

.. note::
        要更改设备的配置，必须在发出任何配置命令之前将目标地址重新设置为本地单播地址。

发送原始 Mesh 数据包是在开发期间测试模型消息处理程序实现的好方法，因为无需实现发送方模型即可完成测试。默认情况下，通过此方式只能测试模型消息的接收，因为蓝牙 Mesh shell 只包含基础模型。要在 Mesh 节点中接收数据包，必须将带有有效操作码处理程序列表的模型添加到 ``subsys/bluetooth/mesh/shell.c`` 中的组成数据，并在处理程序回调中将传入消息打印到 shell。

Parameter formats
*****************

蓝牙 Mesh shell 命令可使用多种格式进行解析：

.. list-table:: 参数格式
        :widths: 1 4 2
        :header-rows: 1

        * - 类型
          - 描述
          - 示例
        * - 整数
          - 默认格式，除非另有指定。可以是十进制或十六进制。
          - ``1234``, ``0xabcd01234``
        * - 十六进制字符串
          - 对于原始字节数组，如 UUID、密钥值和消息有效载荷，参数应格式化为不带任何前缀的连续十六进制字符串。
          - ``deadbeef01234``
        * - 布尔值
          - 布尔值在 API 文档中表示为 ``<val(off, on)>``
          - ``on``, ``off``, ``enabled``, ``disabled``, ``1``, ``0``

命令
****

蓝牙 Mesh shell 实现了大量命令。部分命令接受参数，这些参数在命令名后的括号中列出。例如 ``mesh lpn set <value: off, on>`` 。必需参数使用尖括号标记为 ``<NetKeyIdx>`` 形式，可选参数使用方括号标记为 ``[DstAddr]`` 形式。

蓝牙 Mesh shell 命令分为以下几组：

.. contents::
        :depth: 1
        :local:

.. note::
        某些命令依赖于应用程序编译时配置中启用的特定功能。默认情况下并非所有功能都已启用。在 shell 中调用不带任何参数的 ``mesh`` 可以显示可用的蓝牙 Mesh shell 命令列表。

常规配置
========

``mesh init``
-------------

        初始化 Mesh shell。必须在任何其他 Mesh 命令之前运行此命令。

``mesh reset-local``
--------------------

        将本地 Mesh 节点重置为最初的未配网状态。如果存在配置数据库（CDB），此命令也会将其清除。

目标
====

target 命令使用户能够监视和设置 shell 的目标地址、网络索引和应用索引。这些参数供多个命令使用，例如配网、配置客户端等。

``mesh target dst [DstAddr]``
-----------------------------

        获取或设置消息的目标地址。目标地址决定通过 shell 发送 Mesh 数据包的目的地，但对 shell 控制之外的模块没有影响。

        * ``DstAddr`` ：如果存在，则设置新的 16 位 Mesh 目标地址；如果省略，则打印当前目标地址。


``mesh target net [NetKeyIdx]``
-------------------------------

        获取或设置消息的网络索引。网络索引决定使用哪个网络密钥来加密通过 shell 发送的 Mesh 数据包，但对 shell 控制之外的模块没有影响。网络密钥必须已经添加到设备中，可以通过配网或由配置客户端添加。

        * ``NetKeyIdx`` ：如果存在，则设置新的网络索引；如果省略，则打印当前网络索引。


``mesh target app [AppKeyIdx]``
-------------------------------

        获取或设置消息的应用索引。应用索引决定使用哪个应用密钥来加密通过 shell 发送的 Mesh 数据包，但对 shell 控制之外的模块没有影响。应用密钥必须已经由配置客户端添加到设备中，并且必须绑定到当前网络索引。

        * ``AppKeyIdx`` ：如果存在，则设置新的应用索引；如果省略，则打印当前应用索引。


低功耗节点
==========

``mesh lpn set <Val(off, on)>``
-------------------------------

        启用或禁用低功耗运行。启用后，设备将关闭无线电并开始轮询好友节点。

        * ``Val`` ：设置是否启用低功耗运行。

``mesh lpn poll``
-----------------

        向好友节点执行轮询，以接收任何待处理的消息。仅在启用 LPN 时可用。

测试
====

``mesh test net-send <HexString>``
----------------------------------

        使用当前的目标地址、网络索引和应用索引发送原始 Mesh 消息。消息操作码必须手动编码。

        * ``HexString`` 要发送消息的原始十六进制表示。

``mesh test iv-update``
-----------------------

        强制执行一次 IV 更新。


``mesh test iv-update-test <Val(off, on)>``
-------------------------------------------

        设置 IV 更新测试模式。在测试模式下，IV 更新的时间要求会被绕过。

        * ``Val`` ：启用或禁用 IV 更新测试模式。


``mesh test rpl-clear``
-----------------------

        清除重放保护列表，强制节点忘记所有已接收的消息。

.. warning::

        清除重放保护列表会破坏 Mesh 节点的安全机制，使其容易受到消息重放攻击。在实际部署中绝不应执行此操作。

健康服务器测试
--------------

``mesh test health-srv add-fault <FaultID>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        为 Linux Foundation Company ID 注册新的健康服务器故障。

        * ``FaultID`` ：要注册的故障 ID（ ``0x0001`` 到 ``0xFFFF`` ）


``mesh test health-srv del-fault [FaultID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        移除为 Linux Foundation Company ID 注册的健康服务器故障。

        * ``FaultID`` ：如果存在，则删除给定的故障 ID；如果省略，则清除所有已注册的故障。

Provisioning
============

要允许设备广播可连接的未配网信标，必须启用 :kconfig:option:`CONFIG_BT_MESH_PROVISIONEE` 配置选项，以及 :kconfig:option:`CONFIG_BT_MESH_PB_GATT` 选项。

``mesh prov pb-gatt <Val(off, on)>``
------------------------------------

        开始或停止广播可连接的未配网信标。可连接的未配网信标允许附近的基于 GATT 的配网器发现该 Mesh 节点，并通过 GATT 承载对其进行配网。

        * ``Val`` ：启用或禁用通过 GATT 配网

要允许设备广播未配网信标，必须启用 :kconfig:option:`CONFIG_BT_MESH_PROVISIONEE` 配置选项，以及 :kconfig:option:`CONFIG_BT_MESH_PB_ADV` 选项。

``mesh prov pb-adv <Val(off, on)>``
-----------------------------------

        开始或停止广播未配网信标。未配网信标允许附近的基于广播的配网器发现该 Mesh 节点，并通过广播承载对其进行配网。

        * ``Val`` ：启用或禁用通过广播器配网

要允许设备为其他设备配网，必须启用 :kconfig:option:`CONFIG_BT_MESH_PROVISIONER` 和 :kconfig:option:`CONFIG_BT_MESH_PB_ADV` 配置选项。

``mesh prov remote-adv <UUID(1-16 hex)> <NetKeyIdx> <Addr> <AttDur(s)>``
------------------------------------------------------------------------

        将附近的设备配网到 Mesh 网络中。Mesh 节点开始使用给定的 UUID 扫描未配网信标。找到后，该未配网设备将以给定的单播地址加入 Mesh 网络，并获得 ``NetKeyIdx`` 所指示的网络密钥。

        * ``UUID`` 表示未配网设备的 UUID。如果提供的十六进制字符串短于 16 字节，则会填充数组中最高有效的 N 个字节，其余字节补零。
        * ``NetKeyIdx`` 表示要传递给设备的网络密钥的索引。
        * ``Addr`` 表示要分配给未配网设备的第一个单播地址。设备占用的地址数量等于其元素数量，且所有这些地址都必须可用。
        * ``AttDur`` 表示未配网设备在支持该功能时用于标识自身的持续时间，单位为秒。有关详情，请参见 :ref:`bluetooth_mesh_models_health_srv_attention` 。

要允许设备通过 GATT 为其他设备配网，必须启用 :kconfig:option:`CONFIG_BT_MESH_PROVISIONER` 和 :kconfig:option:`CONFIG_BT_MESH_PB_GATT_CLIENT` 配置选项。

``mesh prov remote-gatt <UUID(1-16 hex)> <NetKeyIdx> <Addr> <AttDur(s)>``
-------------------------------------------------------------------------

        将附近的设备配网到 Mesh 网络中。Mesh 节点开始使用给定的 UUID 扫描针对 PB-GATT 的可连接广播。找到后，该未配网设备将以给定的单播地址加入 Mesh 网络，并获得 ``NetKeyIdx`` 所指示的网络密钥。

        * ``UUID`` 表示未配网设备的 UUID。如果提供的十六进制字符串短于 16 字节，则会填充数组中最高有效的 N 个字节，其余字节补零。
        * ``NetKeyIdx`` 表示要传递给设备的网络密钥的索引。
        * ``Addr`` 表示要分配给未配网设备的第一个单播地址。设备占用的地址数量等于其元素数量，且所有这些地址都必须可用。
        * ``AttDur`` 表示未配网设备在支持该功能时用于标识自身的持续时间，单位为秒。有关详情，请参见 :ref:`bluetooth_mesh_models_health_srv_attention` 。

``mesh prov uuid [UUID(1-16 hex)]``
-----------------------------------

        获取或设置 Mesh 节点的 UUID，该 UUID 用于未配网信标。

        * ``UUID`` 为可选参数，如果提供，则表示新的 128 位 UUID 值。如果提供的十六进制字符串短于 16 字节，则会填充数组中最高有效的 N 个字节，其余字节补零。如果省略，则打印当前 UUID。要启用此命令，必须启用 :kconfig:option:`CONFIG_BT_MESH_SHELL_PROV_CTX_INSTANCE` 选项。


``mesh prov input-num <Number>``
--------------------------------

        输入数字形式的 OOB 认证值。仅在配网过程中由 shell 提示时有效。输入的数字必须与配网中另一方给出的数字一致。

        * ``Number`` 表示十进制认证数字。


``mesh prov input-str <String>``
--------------------------------

        输入字母数字形式的 OOB 认证值。仅在配网过程中由 shell 提示时有效。输入的字符串必须与配网中另一方给出的字符串一致。

        * ``String`` 表示不带引号的字母数字认证字符串。


``mesh prov static-oob [Val(1-32 hex)]``
----------------------------------------

        设置或清除静态 OOB 认证值。静态 OOB 认证值必须在配网开始前设置才会生效。配网双方的静态 OOB 值必须相同。要启用此命令，必须启用 :kconfig:option:`CONFIG_BT_MESH_SHELL_PROV_CTX_INSTANCE` 选项。

        * ``Val`` 为可选参数，如果提供，则表示静态 OOB 的新十六进制值。如果提供的十六进制字符串短于 16 字节，则会填充数组中最高有效的 N 个字节，其余字节补零。如果省略，则清除静态 OOB 值。


``mesh prov local <NetKeyIdx> <Addr> [IVI]``
--------------------------------------------

        对 Mesh 节点自身进行配网。如果启用了配置数据库，则必须创建网络密钥。否则将使用默认密钥值。

        * ``NetKeyIdx`` 表示要用于配网的网络密钥的索引。
        * ``Addr`` 表示要分配给该设备的第一个单播地址。设备占用的地址数量等于其元素数量，且所有这些地址都必须可用。
        * ``IVI`` 表示当前的网络 IV 索引。如果省略，默认为 0。


``mesh prov beacon-listen <Val(off, on)>``
------------------------------------------

        启用或禁用收到的未配网信标的打印。这使配网设备能够检测附近的未配网设备并对其进行配网。要启用此命令，必须启用 :kconfig:option:`CONFIG_BT_MESH_SHELL_PROV_CTX_INSTANCE` 选项。

        * ``Val`` 表示是否启用未配网信标打印。

``mesh prov remote-pub-key <PubKey>``
-------------------------------------
        提供设备公钥。

        * ``PubKey`` 表示设备公钥，采用大端序。

``mesh prov auth-method input <Action> <Size>``
-----------------------------------------------
        在配网设备端指示未配网设备使用指定的输入 OOB 认证操作。

        * ``Action`` 表示输入操作，允许的取值如下：

                * ``0`` 表示无输入操作。
                * ``1`` 表示 Push 操作集。
                * ``2`` 表示 Twist 操作集。
                * ``4`` 表示 Enter number 操作集。
                * ``8`` 表示 Enter String 操作集。
        * ``Size`` 表示认证大小。

``mesh prov auth-method output <Action> <Size>``
------------------------------------------------
        在配网设备端指示未配网设备使用指定的输出 OOB 认证操作。

        * ``Action`` 表示输出操作，允许的取值如下：

                * ``0`` 表示无输出操作。
                * ``1`` 表示 Blink 操作集。
                * ``2`` 表示 Vibrate 操作集。
                * ``4`` 表示 Display number 操作集。
                * ``8`` 表示 Display String 操作集。
        * ``Size`` 表示认证大小。

``mesh prov auth-method static <Val(1-16 hex)>``
------------------------------------------------
        在配网设备端指示未配网设备使用静态 OOB 认证，并在配网时使用指定的静态认证值。

        * ``Val`` 为静态 OOB 值。如果提供的十六进制字符串短于 32 字节，则会填充数组中最高有效的 N 个字节，其余字节补零。

``mesh prov auth-method none``
------------------------------
        在配网设备端，配网新设备时不使用任何认证。这是默认行为。

代理
====

代理服务器模块是一个可选 Mesh 子系统，可通过 :kconfig:option:`CONFIG_BT_MESH_GATT_PROXY` 配置选项启用。

``mesh proxy identity-enable``
------------------------------

        启用代理节点身份信标，允许代理设备显式连接到此设备。该信标将运行 60 秒，之后节点恢复为正常的代理信标。

代理客户端模块是一个可选 Mesh 子系统，可通过 :kconfig:option:`CONFIG_BT_MESH_PROXY_CLIENT` 配置选项启用。

``mesh proxy connect <NetKeyIdx>``
----------------------------------

        自动将附近的代理服务器接入 Mesh 网络。

        * ``NetKeyIdx`` ：要连接的网络密钥索引。


``mesh proxy disconnect <NetKeyIdx>``
-------------------------------------

        断开现有的代理连接。

        * ``NetKeyIdx`` ：要断开代理连接的网络密钥索引。


``mesh proxy solicit <NetKeyIdx>``
----------------------------------

        开始对子网进行代理 Solicitation。此功能可通过 :kconfig:option:`CONFIG_BT_MESH_PROXY_SOLICITATION` 配置选项启用。

        * ``NetKeyIdx`` ：要向其发送 Solicitation PDU 的网络密钥索引。

.. _bluetooth_mesh_shell_cfg_cli:

模型
====

配置客户端
----------

配置客户端模型是一个可选 Mesh 子系统，可通过 :kconfig:option:`CONFIG_BT_MESH_CFG_CLI` 配置选项启用。它作为独立模块 ``mesh models cfg`` 实现，位于 ``mesh models`` 子命令列表中。只要启用了上述 shell 配置选项，且应用的模型组成中存在配置客户端模型，该模块就能作用于配置客户端模型的任何实例。此 shell 模块可用于配置自身以及 Mesh 网络中的其他节点。

配置客户端使用由 ``mesh target dst`` 和 ``mesh target net`` 设置的通用消息参数来指定目标节点。当蓝牙 Mesh shell 节点完成配网后，如果启用了 :kconfig:option:`CONFIG_BT_MESH_SHELL_PROV_CTX_INSTANCE` 选项并初始化了 shell 配网上下文，配置客户端模型默认以自身为目标。类似地，当另一个节点由蓝牙 Mesh shell 完成配网后，配置客户端模型会以新节点为目标。在大多数常见用例中，配置客户端依赖配网功能和配置数据库才能完全正常工作。配置客户端始终使用绑定到目标地址的设备密钥发送消息，因此它只能配置自身以及由其配网的 Mesh 节点。以下步骤是一个示例，介绍如何设置设备以开始使用配置客户端命令：

* 初始化客户端节点，即运行 ``mesh init`` 命令。
* 创建 CDB，即运行 ``mesh cdb create`` 命令。
* 对本地设备进行配网，即运行 ``mesh prov local`` 命令。
* 此时 shell 模块应以自身为目标。
* 监控本地节点的组成数据，即运行 ``mesh models cfg get-comp`` 命令。
* 使用配置客户端命令按需配置本地节点。
* 为其他设备配网，例如 ``mesh prov beacon-listen`` 、 ``mesh prov remote-adv`` 和 ``mesh prov remote-gatt`` 命令。
* 此时 shell 模块应以新添加的节点为目标。
* 监控新配网的节点及其地址，即运行 ``mesh cdb show`` 命令。
* 监控目标设备的组成数据，即运行 ``mesh models cfg get-comp`` 命令。
* 使用配置客户端命令按需配置该节点。

``mesh models cfg target get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取配置客户端模型的目标配置服务器。

``mesh models cfg help``
^^^^^^^^^^^^^^^^^^^^^^^^

        打印配置客户端 shell 模块的信息。

``mesh models cfg reset``
^^^^^^^^^^^^^^^^^^^^^^^^^

        重置目标设备。

``mesh models cfg timeout [Timeout(s)]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取或设置发送消息时使用的配置客户端模型超时时间。

        * ``Timeout`` ：如果存在，则以秒为单位设置配置客户端模型的超时时间。如果省略，则打印当前超时时间。


``mesh models cfg get-comp [Page]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        读取组成数据页。将打印完整的组成数据页。如果目标设备没有给定的页，则返回该页之前编号最大的页。

        * ``Page`` ：要请求的组成数据页。如果省略，默认为 0。


``mesh models cfg beacon [Val(off, on)]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取或设置网络信标的发送。

        * ``Val`` ：如果存在，则启用或禁用网络信标的发送。如果省略，则打印当前网络信标状态。


``mesh models cfg ttl [TTL]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取或设置默认 TTL 值。

        * ``TTL`` ：如果存在，则设置新的默认 TTL 值。合法的 TTL 值为 0x00 和 0x02-0x7f。如果省略，则打印当前默认 TTL 值。


``mesh models cfg friend [Val(off, on)]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取或设置 Friend 功能。

        * ``Val`` ：如果存在，则启用或禁用 Friend 功能。如果省略，则打印当前 Friend 功能状态：

                * ``0x00`` ：该功能受支持，但已禁用。
                * ``0x01`` ：该功能已启用。
                * ``0x02`` ：不支持该功能。


``mesh models cfg gatt-proxy [Val(off, on)]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取或设置 GATT 代理功能。

        * ``Val`` ：如果存在，则启用或禁用 GATT 代理功能。如果省略，则打印当前 GATT 代理功能状态：

                * ``0x00`` ：该功能受支持，但已禁用。
                * ``0x01`` ：该功能已启用。
                * ``0x02`` ：不支持该功能。


``mesh models cfg relay [<Val(off, on)> [<Count> [Int(ms)]]]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取或设置中继功能及其参数。

        * ``Val`` ：如果存在，则启用或禁用中继功能。如果省略，则打印当前中继功能状态：

                * ``0x00`` ：该功能受支持，但已禁用。
                * ``0x01`` ：该功能已启用。
                * ``0x02`` ：不支持该功能。

        * ``Count`` ：如果 ``val`` 为 ``on`` ，则设置新的中继重传次数。如果 ``val`` 为 ``off`` ，则忽略。合法的重传次数为 0-7。如果省略，默认为 ``2`` 。
        * ``Int`` ：如果 ``val`` 为 ``on`` ，则设置新的中继重传间隔（单位为毫秒）。合法间隔范围为 10-320 毫秒。如果 ``val`` 为 ``off`` ，则忽略。如果省略，默认为 ``20`` 。

``mesh models cfg node-id <NetKeyIdx> [Identity]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取或设置子网的当前节点身份状态。

        * ``NetKeyIdx`` ：要获取或设置的网络密钥索引。
        * ``Identity`` ：如果存在，则设置节点身份状态的值。

``mesh models cfg polltimeout-get <LPNAddr>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取好友节点内 LPN 的 PollTimeout 定时器当前值。

        * ``LPNAddr`` ：低功耗节点地址。

``mesh models cfg net-transmit-param [<Count> <Int(ms)>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取或设置网络传输参数。

        * ``Count`` ：设置每条已发送消息的额外网络传输次数。合法的重传次数为 0-7。
        * ``Int`` ：设置新的网络重传间隔（单位为毫秒）。合法间隔范围为 10-320 毫秒。


``mesh models cfg netkey add <NetKeyIdx> [Key(1-16 hex)]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        向目标节点添加网络密钥。如果已启用，则将该密钥添加到配置数据库。

        * ``NetKeyIdx`` ：要添加的网络密钥索引。
        * ``Key`` ：如果存在，则将密钥值设置为 128 位十六进制值。如果提供的十六进制字符串短于 16 字节，则会填充数组的 N 个最高有效字节，其余部分补零。仅当该密钥在配置数据库中尚不存在时才有效。如果省略，则使用默认密钥值。


``mesh models cfg netkey upd <NetKeyIdx> [Key(1-16 hex)]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        更新目标节点的网络密钥。

        * ``NetKeyIdx`` ：要更新的网络密钥索引。
        * ``Key`` ：如果存在，则将密钥值设置为 128 位十六进制值。如果提供的十六进制字符串短于 16 字节，则会填充数组的 N 个最高有效字节，其余部分补零。如果省略，则使用默认密钥值。

``mesh models cfg netkey get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取已知网络密钥索引的列表。


``mesh models cfg netkey del <NetKeyIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        从目标节点删除网络密钥。

        * ``NetKeyIdx`` ：要删除的网络密钥索引。


``mesh models cfg appkey add <NetKeyIdx> <AppKeyIdx> [Key(1-16 hex)]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        向目标节点添加应用密钥。如果已启用，则将该密钥添加到配置数据库。

        * ``NetKeyIdx`` ：应用密钥绑定到的网络密钥索引。
        * ``AppKeyIdx`` ：要添加的应用密钥索引。
        * ``Key`` ：如果存在，则将密钥值设置为 128 位十六进制值。如果提供的十六进制字符串短于 16 字节，则会填充数组的 N 个最高有效字节，其余部分补零。仅当该密钥在配置数据库中尚不存在时才有效。如果省略，则使用默认密钥值。

``mesh models cfg appkey upd <NetKeyIdx> <AppKeyIdx> [Key(1-16 hex)]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        更新目标节点的应用密钥。

        * ``NetKeyIdx`` ：应用密钥绑定到的网络密钥索引。
        * ``AppKeyIdx`` ：要更新的应用密钥索引。
        * ``Key`` ：如果存在，则将密钥值设置为 128 位十六进制值。如果提供的十六进制字符串短于 16 字节，则会填充数组的 N 个最高有效字节，其余部分补零。如果省略，则使用默认密钥值。

``mesh models cfg appkey get <NetKeyIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取绑定到给定网络密钥索引的已知应用密钥索引列表。

        * ``NetKeyIdx`` ：要从中获取应用密钥索引列表的网络密钥索引。


``mesh models cfg appkey del <NetKeyIdx> <AppKeyIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        从目标节点删除应用密钥。

        * ``NetKeyIdx`` ：应用密钥绑定到的网络密钥索引。
        * ``AppKeyIdx`` 为要删除的应用密钥索引。


``mesh models cfg model app-bind <Addr> <AppKeyIdx> <MID> [CID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        将应用密钥绑定到模型。模型只能加密和解密使用其绑定的应用密钥发送的消息。

        * ``Addr`` 为模型所在元素的地址。
        * ``AppKeyIdx`` 为要绑定到模型的应用密钥。
        * ``MID`` 为要绑定密钥的目标模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。


``mesh models cfg model app-unbind <Addr> <AppKeyIdx> <MID> [CID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        从模型解绑应用密钥。

        * ``Addr`` 为模型所在元素的地址。
        * ``AppKeyIdx`` 为要从模型解绑的应用密钥。
        * ``MID`` 为要解除密钥绑定的模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。


``mesh models cfg model app-get <ElemAddr> <MID> [CID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取绑定到模型的应用密钥列表。

        * ``ElemAddr`` 为模型所在元素的地址。
        * ``MID`` 为要获取其绑定密钥的模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。


``mesh models cfg model pub <Addr> <MID> [CID] [<PubAddr> <AppKeyIdx> <Cred(off, on)> <TTL> <PerRes> <PerSteps> <Count> <Int(ms)>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取或设置模型的发布参数。如果包含所有发布参数，则这些参数将成为模型的新发布参数。如果省略所有发布参数，则打印模型当前的发布参数。

        * ``Addr`` 为模型所在元素的地址。
        * ``MID`` 为要获取其绑定密钥的模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。

        发布参数：

                * ``PubAddr`` 为要发布到的目标地址。
                * ``AppKeyIdx`` 为发布时使用的应用密钥索引。
                * ``Cred`` 表示作为低功耗节点时是否使用好友凭证进行发布。
                * ``TTL`` 为发布时使用的 TTL 值，取值范围在 ``0x00`` 到 ``0x07f`` 之间。
                * ``PerRes`` 为发布周期步长的分辨率：

                        * ``0x00`` 表示步长分辨率为 100 毫秒。
                        * ``0x01`` 表示步长分辨率为 1 秒。
                        * ``0x02`` 表示步长分辨率为 10 秒。
                        * ``0x03`` 表示步长分辨率为 10 分钟。
                * ``PerSteps`` 为发布周期步数，设为 0 可禁用周期性发布。
                * ``Count`` 为每条已发布消息的重传次数，取值范围在 ``0`` 到 ``7`` 之间。
                * ``Int`` 为每次重传之间的间隔，以毫秒为单位。必须是 50 的倍数。

``mesh models cfg model pub-va <Addr> <UUID(1-16 hex)> <AppKeyIdx> <Cred(off, on)> <TTL> <PerRes> <PerSteps> <Count> <Int(ms)> <MID> [CID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        设置模型的发布参数。

        * ``Addr`` 为模型所在元素的地址。
        * ``MID`` 为要获取其绑定密钥的模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。

        发布参数：

                * ``UUID`` 为要发布到的目标虚拟地址。提供长度不足 16 字节的十六进制字符串时，会将所提供的字节填充到数组的 N 个最高有效字节中，其余部分用零补齐。
                * ``AppKeyIdx`` 为发布时使用的应用密钥索引。
                * ``Cred`` 表示作为低功耗节点时是否使用好友凭证进行发布。
                * ``TTL`` 为发布时使用的 TTL 值，取值范围在 ``0x00`` 到 ``0x07f`` 之间。
                * ``PerRes`` 为发布周期步长的分辨率：

                        * ``0x00`` 表示步长分辨率为 100 毫秒。
                        * ``0x01`` 表示步长分辨率为 1 秒。
                        * ``0x02`` 表示步长分辨率为 10 秒。
                        * ``0x03`` 表示步长分辨率为 10 分钟。
                * ``PerSteps`` 为发布周期步数，设为 0 可禁用周期性发布。
                * ``Count`` 为每条已发布消息的重传次数，取值范围在 ``0`` 到 ``7`` 之间。
                * ``Int`` 为每次重传之间的间隔，以毫秒为单位。必须是 50 的倍数。


``mesh models cfg model sub-add <ElemAddr> <SubAddr> <MID> [CID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        将模型订阅到组地址。模型只接收发送到其单播地址或其已订阅的组地址或虚拟地址的消息。模型可以订阅多个组地址和虚拟地址。

        * ``ElemAddr`` 为模型所在元素的地址。
        * ``SubAddr`` 为模型应订阅的 16 位组地址，取值范围在 ``0xc000`` 到 ``0xFEFF`` 之间。
        * ``MID`` 为要向其添加订阅的模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。


``mesh models cfg model sub-del <ElemAddr> <SubAddr> <MID> [CID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        取消模型对组地址的订阅。

        * ``ElemAddr`` 为模型所在元素的地址。
        * ``SubAddr`` 为要从模型订阅列表中移除的 16 位组地址，取值范围在 ``0xc000`` 到 ``0xFEFF`` 之间。
        * ``MID`` 为要向其添加订阅的模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。


``mesh models cfg model sub-add-va <ElemAddr> <LabelUUID(1-16 hex)> <MID> [CID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        将模型订阅到虚拟地址。模型只接收发送到其单播地址或其已订阅的组地址或虚拟地址的消息。模型可以订阅多个组地址和虚拟地址。

        * ``ElemAddr`` 为模型所在元素的地址。
        * ``LabelUUID`` 为要订阅的虚拟地址的 128 位标签 UUID。提供长度不足 16 字节的十六进制字符串时，会将所提供的字节填充到数组的 N 个最高有效字节中，其余部分用零补齐。
        * ``MID`` 为要向其添加订阅的模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。


``mesh models cfg model sub-del-va <ElemAddr> <LabelUUID(1-16 hex)> <MID> [CID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        取消模型对虚拟地址的订阅。

        * ``ElemAddr`` 为模型所在元素的地址。
        * ``LabelUUID`` 为要取消订阅的虚拟地址的 128 位标签 UUID。提供长度不足 16 字节的十六进制字符串时，会将所提供的字节填充到数组的 N 个最高有效字节中，其余部分用零补齐。
        * ``MID`` 为要向其添加订阅的模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。

``mesh models cfg model sub-ow <ElemAddr> <SubAddr> <MID> [CID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        用一个新组地址覆盖模型的所有订阅。

        * ``ElemAddr`` 为模型所在元素的地址。
        * ``SubAddr`` 为要添加到模型订阅列表中的 16 位组地址，取值范围在 ``0xc000`` 到 ``0xFEFF`` 之间。
        * ``MID`` 为要向其添加订阅的模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。

``mesh models cfg model sub-ow-va <ElemAddr> <LabelUUID(1-16 hex)> <MID> [CID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        用一个新虚拟地址覆盖模型的所有订阅。模型只接收发送到其单播地址或其已订阅的组地址或虚拟地址的消息。模型可以订阅多个组地址和虚拟地址。

        * ``ElemAddr`` 为模型所在元素的地址。
        * ``LabelUUID`` 为虚拟地址的 128 位标签 UUID，将作为新地址添加到订阅列表中。提供长度不足 16 字节的十六进制字符串时，会将所提供的字节填充到数组的 N 个最高有效字节中，其余部分用零补齐。
        * ``MID`` 为要向其添加订阅的模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。

``mesh models cfg model sub-del-all <ElemAddr> <MID> [CID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        取消模型对组地址和虚拟地址的所有订阅。

        * ``ElemAddr`` 为模型所在元素的地址。
        * ``MID`` 为要取消其全部订阅的模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。

``mesh models cfg model sub-get <ElemAddr> <MID> [CID]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取模型订阅的地址列表。

        * ``ElemAddr`` 为模型所在元素的地址。
        * ``MID`` 为要获取其订阅列表的模型的模型 ID。
        * ``CID`` 若存在，用于确定模型的 Company ID；若省略，则该模型为 Bluetooth SIG 定义的模型。


``mesh models cfg krp <NetKeyIdx> [Phase]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取或设置子网的密钥刷新阶段。

        * ``NetKeyIdx`` 为所标识的网络密钥，用于获取或设置当前密钥刷新阶段状态。
        * ``Phase`` 为新的密钥刷新阶段。有效阶段如下：

                * ``0x00`` 表示正常运行；密钥刷新过程未激活。
                * ``0x01`` 表示密钥刷新过程的第一阶段。
                * ``0x02`` 表示密钥刷新过程的第二阶段。

``mesh models cfg hb-sub [<Src> <Dst> <Per>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取或设置 Heartbeat 订阅参数。节点只接收与 Heartbeat 订阅参数匹配的 Heartbeat 消息。如果提供了参数，则设置 Heartbeat 订阅参数；如果调用时不带任何参数，则打印当前的 Heartbeat 订阅参数。

        * ``Src`` 为接收 Heartbeat 消息的单播源地址。
        * ``Dst`` 为接收 Heartbeat 消息的目标地址。
        * ``Per`` 为 Heartbeat 订阅周期的对数表示：

                * ``0`` 表示将禁用 Heartbeat 订阅。
                * ``1`` 到 ``17`` 表示节点将订阅 Heartbeat 消息，持续 2\ :sup:`(period - 1)` 秒。


``mesh models cfg hb-pub [<Dst> <Count> <Per> <TTL> <Features> <NetKeyIdx>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取或设置 Heartbeat 发布参数。如果提供了参数，则设置 Heartbeat 发布参数；如果调用时不带任何参数，则打印当前的 Heartbeat 发布参数。

        * ``Dst`` 为发布 Heartbeat 消息的目标地址。
        * ``Count`` 为周期性发布的 Heartbeat 消息数量的对数表示：

                * ``0`` 表示不周期性发布 Heartbeat 消息。
                * ``1`` 到 ``17`` 表示节点将周期性发布 2\ :sup:`(count - 1)` 条 Heartbeat 消息。
                * ``255`` 表示将无限期地周期性发布 Heartbeat 消息。

        * ``Per`` 为 Heartbeat 发布周期的对数表示：

                * ``0`` 表示不周期性发布 Heartbeat 消息。
                * ``1`` 到 ``17`` 表示节点将每隔 2\ :sup:`(period - 1)` 秒发布一次 Heartbeat 消息。

        * ``TTL`` 为发布 Heartbeat 消息所用的 TTL 值，取值范围在 ``0x00`` 到 ``0x7f`` 之间。
        * ``Features`` 为发生变化时应触发 Heartbeat 发布的特性位域：

                * ``Bit 0`` 表示中继功能。
                * ``Bit 1`` 表示代理功能。
                * ``Bit 2`` 表示好友功能。
                * ``Bit 3`` 表示低功耗功能。

        * ``NetKeyIdx`` 为用于发布 Heartbeat 消息的网络密钥索引。


健康客户端
----------

健康客户端模型是一个可选的 Mesh 子系统，可通过 :kconfig:option:`CONFIG_BT_MESH_HEALTH_CLI` 配置选项启用。它以独立模块 ``mesh models health`` 的形式实现，位于 ``mesh models`` 子命令列表中。只要启用了上述 shell 配置选项，并且应用程序的组成数据中存在一个或多个健康客户端模型，该模块就能适用于任意健康客户端模型实例。此 shell 模块可用于触发 Mesh 网络中设备上的健康客户端与服务器之间的交互。

默认情况下，使用健康客户端命令时，该模块会选择组成数据中的第一个健康客户端实例。要选择特定的健康客户端实例，用户可以使用 ``mesh models health instance set`` 和 ``mesh models health instance get-all`` 命令。

健康客户端可以使用由 ``mesh target dst`` 以及 ``mesh target net`` 和 ``mesh target app`` 设置的通用消息参数，将消息发送到特定节点。如果 shell 的目标地址设置为零，则被选定的健康客户端将尝试使用其配置的发布参数发布消息。

``mesh models health instance set <ElemIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        设置要使用的健康客户端模型实例。

        * ``ElemIdx`` 为健康客户端模型的元素索引。

``mesh models health instance get-all``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        打印设备上所有可用的健康客户端模型实例。

``mesh models health fault-get <CID>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取指定 Company ID 的已注册故障列表。

        * ``CID`` ：要获取其故障的 Company ID。


``mesh models health fault-clear <CID>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        清除某个 Company ID 的故障列表。

        * ``CID`` ：要清除其故障的 Company ID。


``mesh models health fault-clear-unack <CID>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        清除某个 Company ID 的故障列表，且不请求响应。

        * ``CID`` ：要清除其故障的 Company ID。


``mesh models health fault-test <CID> <TestID>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        调用自检过程，并显示已触发的故障列表。

        * ``CID`` ：要对其执行自检的 Company ID。
        * ``TestID`` ：要执行的测试。


``mesh models health fault-test-unack <CID> <TestID>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        调用自检过程，且不请求响应。

        * ``CID`` ：要对其执行自检的 Company ID。
        * ``TestID`` ：要执行的测试。


``mesh models health period-get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取当前 Health Server 的发布周期除数。


``mesh models health period-set <Divisor>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        设置当前 Health Server 的发布周期除数。当检测到故障时，Health Server 将以缩短的间隔开始发布其故障状态。缩短的间隔由 Health Server 发布周期除数决定：故障发布周期 = 发布周期 / 2\ :sup:`divisor` 。

        * ``Divisor`` ：新的 Health Server 发布周期除数。


``mesh models health period-set-unack <Divisor>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        设置当前 Health Server 的发布周期除数。当检测到故障时，Health Server 将以缩短的间隔开始发布其故障状态。缩短的间隔由 Health Server 发布周期除数决定：故障发布周期 = 发布周期 / 2\ :sup:`divisor` 。

        * ``Divisor`` ：新的 Health Server 发布周期除数。


``mesh models health attention-get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取当前 Health Server 的注意状态。


``mesh models health attention-set <Time(s)>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        在一段时间内启用 Health Server 的注意状态。

        * ``Time`` ：注意状态的持续时间，取值范围为 ``0`` 到 ``255`` 秒。


``mesh models health attention-set-unack <Time(s)>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        在一段时间内启用 Health Server 的注意状态，且不请求响应。

        * ``Time`` ：注意状态的持续时间，取值范围为 ``0`` 到 ``255`` 秒。


二进制大对象（BLOB）传输客户端模型
----------------------------------

可以将 :ref:`bluetooth_mesh_blob_cli` 添加到 Mesh shell，方法是启用 :kconfig:option:`CONFIG_BT_MESH_BLOB_CLI` 选项并禁用 :kconfig:option:`CONFIG_BT_MESH_DFU_CLI` 选项。

``mesh models blob cli target <Addr>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        为下一次 BLOB 传输添加目标节点。

        * ``Addr`` ：目标节点的 BLOB Transfer Server 模型的单播地址。


``mesh models blob cli caps [<Group> [<TimeoutBase>]]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取目标节点的传输能力。

        * ``Group`` ：与目标节点通信时使用的可选组地址。如果省略，BLOB Transfer Client 将分别对每个目标节点寻址。
        * ``TimeoutBase`` ：等待目标节点响应的可选时间，以 10 秒为步长。


``mesh models blob cli tx <Id> <Size> <BlockSizeLog> <ChunkSize> [<Group> [<Mode(push, pull)>]]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        向目标节点执行 BLOB 传输。BLOB Transfer Client 会向所有目标节点发送一个虚拟 BLOB，并在传输完成后发出消息。请注意，必须首先使用 ``mesh models blob srv rx`` 命令将所有目标节点配置为接收该传输。

        * ``Id`` ：64 位 BLOB 传输 ID。
        * ``Size`` ：BLOB 的大小，单位为字节。
        * ``BlockSizeLog`` ：BLOB 块大小的对数表示。最终块大小将为 ``1 << block size log`` 字节。
        * ``ChunkSize`` ：分块大小，单位为字节。
        * ``Group`` ：与目标节点通信时使用的可选组地址。如果省略或设置为 0，BLOB Transfer Client 将分别对每个目标节点寻址。
        * ``Mode`` ：要使用的 BLOB 传输模式。必须为 ``push`` （Push BLOB Transfer Mode）或 ``pull`` （Pull BLOB Transfer Mode）。如果省略，则默认使用 ``push`` 模式。


``mesh models blob cli tx-cancel``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        取消正在进行的 BLOB 传输。

``mesh models blob cli tx-get [Group]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        确定先前运行的 BLOB 传输的进度。可在未执行 BLOB 传输时使用。

        * ``Group`` ：与目标节点通信时使用的可选组地址。如果省略或设置为 0，BLOB Transfer Client 将分别对每个目标节点寻址。


``mesh models blob cli tx-suspend``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        暂停正在进行的 BLOB 传输。


``mesh models blob cli tx-resume``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        恢复已暂停的 BLOB 传输。

``mesh models blob cli instance-set <ElemIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        在使用其他 BLOB Transfer Client 模型命令时，应使用指定元素上的 BLOB Transfer Client 模型实例。

        * ``ElemIdx``: 要在其上查找要使用的 BLOB Transfer Client 模型实例的元素。

``mesh models blob cli instance-get-all``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取节点上所有 BLOB Transfer Client 模型实例的列表。


BLOB Transfer Server 模型
-------------------------

:ref:`bluetooth_mesh_blob_srv` 可以通过启用 :kconfig:option:`CONFIG_BT_MESH_BLOB_SRV` 选项添加到 Mesh shell。BLOB Transfer Server 模型能够接收任何 BLOB 数据，但 Mesh shell 中的实现会丢弃传入的数据。


``mesh models blob srv rx <ID> [<TimeoutBase(10s steps)>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        准备接收 BLOB 传输。

        * ``ID``: 要接收的 64 位 BLOB 传输 ID。
        * ``TimeoutBase``: 可选的额外时间，用于等待客户端消息，以 10 秒为增量。


``mesh models blob srv rx-cancel``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        取消正在进行的 BLOB 传输。

``mesh models blob srv instance-set <ElemIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        在使用其他 BLOB Transfer Server 模型命令时，应使用指定元素上的 BLOB Transfer Server 模型实例。

        * ``ElemIdx``: 要在其上查找要使用的 BLOB Transfer Server 模型实例的元素。

``mesh models blob srv instance-get-all``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取节点上所有 BLOB Transfer Server 模型实例的列表。


二进制大对象（BLOB）传输 Flash 流
---------------------------------
通过启用 :kconfig:option:`CONFIG_BT_MESH_SHELL_BLOB_IO_FLASH` 选项，可以将 BLOB Flash 流配置添加到 Mesh shell。默认情况下，shell 使用虚拟 BLOB 流。此选项允许用户指定要使用 Flash 中的哪个区域。请参见 :ref:`flash_map_api` 了解如何获取相关参数。

``mesh models blob flash-stream-set <AreaID> [<Offset>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        将 BLOB 流设置为指定的区域。

        * ``AreaID``: 用于写入或读取 BLOB 的 Flash 区域 ID。
        * ``Offset``: 可选的 Flash 区域偏移量，用于指定 BLOB 的放置位置（以字节为单位）。

``mesh models blob flash-stream-unset``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        将 BLOB 流恢复为虚拟流。


Firmware Update Client 模型
---------------------------

通过启用 :kconfig:option:`CONFIG_BT_MESH_BLOB_CLI` 和 :kconfig:option:`CONFIG_BT_MESH_DFU_CLI` 这两个配置选项，可以将 Firmware Update Client 模型添加到 Mesh shell。Firmware Update Client 通过向一组目标节点传输虚拟固件更新，来演示固件更新分发者角色。


``mesh models dfu slot add <Size> <FwID> [<Metadata>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        添加一个虚拟 DFU 映像槽，该槽可作为 DFU 映像传输。将为该映像槽分配一个映像槽索引，该索引会作为响应打印，并可用于在其他命令中引用该槽。要更新映像槽，请使用 ``mesh models dfu slot del`` shell 命令将其删除，然后重新添加。

        * ``Size``: DFU 映像槽大小，以字节为单位。
        * ``FwID``: 固件 ID，格式为十六进制字符串。
        * ``Metadata``: 可选的固件元数据，格式为十六进制字符串。


``mesh models dfu slot del <SlotIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        删除给定索引处的 DFU 映像槽。

        * ``SlotIdx``: 要删除的槽的索引。


``mesh models dfu slot get <SlotIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取 DFU 映像槽的所有可用信息。

        * ``SlotIdx``: 要获取的槽的索引。


``mesh models dfu cli target <Addr> <ImgIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        添加一个目标节点。

        * ``Addr``: 目标节点的单播地址。
        * ``ImgIdx``: 目标节点上要寻址的映像索引。


``mesh models dfu cli target-state``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        检查配置的目标地址处设备的 DFU Target 状态。


``mesh models dfu cli target-imgs [<MaxCount>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取配置的目标地址处设备上的 DFU 映像列表。

        * ``MaxCount``: 可选，要返回的最大映像数。如果省略，则对返回的映像数没有限制。


``mesh models dfu cli target-check <SlotIdx> <TargetImgIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        检查配置的目标地址处的设备是否会接受从给定 DFU 映像槽向目标节点上给定索引处的 DFU 映像进行的 DFU 传输，以及将会产生什么效果。

        * ``SlotIdx``: 要检查的本地 DFU 映像槽的索引。
        * ``TargetImgIdx`` ：要检查的目标节点 DFU 映像的索引。


``mesh models dfu cli send <SlotIdx> [<Group>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        向所有已添加的目标节点发起 DFU 传输。

        * ``SlotIdx`` ：要发送的本地 DFU 映像槽的索引。
        * ``Group`` ：与目标节点通信时要使用的可选组地址。如果省略，Firmware Update Client 将逐个寻址每个目标节点。


``mesh models dfu cli cancel [<Addr>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        取消特定目标节点或所有目标节点上处于任意状态的 DFU 过程。当提供目标节点地址时，Firmware Update Client 模型将尝试取消指定目标节点上的 DFU 过程。否则，Firmware Update Client 模型将尝试取消所有目标节点上正在进行的 DFU 过程。

        * ``Addr`` ：目标节点的可选单播地址，用于取消该节点上的 DFU 过程。


``mesh models dfu cli apply``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        在所有目标节点上应用最近的 DFU 传输。仅可在 DFU 传输完成后调用。


``mesh models dfu cli confirm``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        确认最近的 DFU 传输已在所有目标节点上成功应用。仅可在 DFU 传输完成并应用后调用。


``mesh models dfu cli suspend``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        暂停正在进行的 DFU 传输。


``mesh models dfu cli resume``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        恢复已暂停的 DFU 传输。


``mesh models dfu cli progress``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        检查当前传输的进度。


``mesh models dfu cli instance-set <ElemIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        在使用其他 Firmware Update Client 模型命令时，应使用指定元素上的 Firmware Update Client 模型实例。

        * ``ElemIdx`` ：要在其上查找要使用的 Firmware Update Client 模型实例的元素。

``mesh models dfu cli instance-get-all``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取节点上所有 Firmware Update Client 模型实例的列表。


Firmware Update Server 模型
---------------------------

通过启用 :kconfig:option:`CONFIG_BT_MESH_BLOB_SRV` 和 :kconfig:option:`CONFIG_BT_MESH_DFU_SRV` 这两个配置选项，可以将 Firmware Update Server 模型添加到 Mesh shell。Firmware Update Server 通过接受任意固件更新来演示固件更新目标角色。Mesh shell 中的 Firmware Update Server 会丢弃传入的固件数据，但在其他方面的行为与正常的固件更新目标节点相同。


``mesh models dfu srv applied``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        将最近的 DFU 传输标记为已应用。仅可在 DFU 传输完成且分发者已请求应用该传输后调用。

        由于 Mesh shell 中的 Firmware Update Server 实际上不会应用传入的固件映像，因此可以使用此命令来模拟“已应用”状态，以通知分发者该传输已成功。


``mesh models dfu srv progress``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        检查当前传输的进度。

``mesh models dfu srv rx-cancel``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        取消传入的 DFU 传输。

``mesh models dfu srv instance-set <ElemIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        在使用其他 Firmware Update Server 模型命令时，应使用指定元素上的 Firmware Update Server 模型实例。

        * ``ElemIdx`` ：要在其上查找要使用的 Firmware Update Server 模型实例的元素。

``mesh models dfu srv instance-get-all``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取节点上所有 Firmware Update Server 模型实例的列表。


.. _bluetooth_mesh_shell_dfd_server:

Firmware Distribution Server 模型
---------------------------------

通过启用 :kconfig:option:`CONFIG_BT_MESH_DFD_SRV` 配置选项，可以将 Firmware Distribution Server 模型命令添加到 Mesh shell。此模型的 shell 命令与 Firmware Distribution Client 模型发送给服务器的消息相对应。要使用这些命令，必须由应用实例化 Firmware Distribution Server。

``mesh models dfd receivers-add <Addr>,<FwIdx>[;<Addr>,<FwIdx>]...``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        将接收方添加到 Firmware Distribution Server。以逗号分隔的 addr,fw_idx 对列表形式提供接收方，各对之间用分号分隔，例如 ``0x0001,0;0x0002,0;0x0004,1`` 。接收方列表中不得使用空格。重复调用此命令将继续填充接收方列表，直到调用 ``mesh models dfd receivers-delete-all`` 为止。

        * ``Addr`` ：接收节点的地址。
        * ``FwIdx`` ：要发送到 ``Addr`` 的固件槽的索引。

``mesh models dfd receivers-delete-all``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        从服务器中删除所有接收方。

``mesh models dfd receivers-get <First> <Count>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取有关固件接收方的信息列表。

        * ``First`` ：要从接收方列表中获取的第一个接收方的索引。
        * ``Count`` ：要获取其信息的接收方数量。

``mesh models dfd capabilities-get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取服务器的能力。

``mesh models dfd get``
^^^^^^^^^^^^^^^^^^^^^^^

        获取有关当前分发状态、分发阶段和传输参数的信息。

``mesh models dfd start <AppKeyIdx> <SlotIdx> [<Group> [<PolicyApply> [<TTL> [<TimeoutBase> [<XferMode>]]]]]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        启动固件分发。

        * ``AppKeyIdx`` ：用于发送的应用密钥索引。公共应用密钥应绑定到 Distributor 和 Target 节点上的 Firmware Update 和 BLOB Transfer 模型。
        * ``SlotIdx`` ：要发送的本地镜像槽的索引。
        * ``Group`` ：与目标节点通信时使用的可选组地址。如果省略，Firmware Distribution Server 将逐个寻址每个目标节点。要在更改其他参数的同时保持逐个寻址每个目标节点，请将此参数值设置为 0。
        * ``PolicyApply`` ：与更新策略对应的可选字段。将其设置为 ``true`` 将使 Firmware Distribution Server 在传输完成后立即应用该镜像。
        * ``TTL`` ：可选。发送时使用的 TTL 值。默认为已配置的默认 TTL。
        * ``TimeoutBase`` ：用于计算固件分发过程中超时值的可选附加值，以 10 秒为增量。有关如何使用 ``timeout_base`` 计算传输超时的信息，请参见 :ref:`bluetooth_mesh_blob_timeout` 一节。默认为 0。
        * ``XferMode`` ：可选的 BLOB 传输模式。1 = Push 模式（Push BLOB Transfer Mode），2 = Pull 模式（Pull BLOB Transfer Mode）。默认为 Push 模式。

``mesh models dfd suspend``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

        暂停正在进行的分发。

``mesh models dfd cancel``
^^^^^^^^^^^^^^^^^^^^^^^^^^

        取消正在进行的分发。

``mesh models dfd apply``
^^^^^^^^^^^^^^^^^^^^^^^^^

        应用已分发的固件。

``mesh models dfd fw-get <FwID>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取有关已上传到服务器的固件镜像的信息。

        * ``FwID`` ：要获取的镜像的固件 ID。

``mesh models dfd fw-get-by-idx <Idx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取有关已上传到服务器指定槽位的固件镜像的信息。

        * ``Idx`` ：要从中获取镜像的槽的索引。

``mesh models dfd fw-delete <FwID>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        从服务器删除固件镜像。

        * ``FwID`` ：要删除的镜像的固件 ID。

``mesh models dfd fw-delete-all``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        从服务器删除所有固件镜像。

``mesh models dfd instance-set <ElemIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        在使用其他 Firmware Distribution Server 模型命令时，应使用指定元素上的 Firmware Distribution Server 模型实例。

        * ``ElemIdx`` ：要在其上查找要使用的 Firmware Distribution Server 模型实例的元素。

``mesh models dfd instance-get-all``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取节点上所有 Firmware Distribution Server 模型实例的列表。


.. _bluetooth_mesh_shell_dfu_metadata:

DFU 元数据
----------

DFU 元数据 shell 命令可用于生成元数据，目标节点可使用这些元数据在接受固件之前对其进行检查。这些命令通过 :kconfig:option:`CONFIG_BT_MESH_SHELL_DFU_METADATA` 配置选项启用。

``mesh models dfu metadata comp-clear``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        清除为目标节点存储的组成数据。

``mesh models dfu metadata comp-add <CID> <ProductID> <VendorID> <Crpl> <Features>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        创建组成数据第 0 页的头部。

        * ``CID`` ：由 Bluetooth SIG 分配的公司标识符。
        * ``ProductID`` ：厂商分配的产品标识符。
        * ``VendorID`` ：厂商分配的版本标识符。
        * ``Crpl`` ：重放保护列表的大小。
        * ``Features`` ：节点支持的功能，采用位域格式：

                * ``0`` ：中继。
                * ``1`` ：代理。
                * ``2`` ：好友。
                * ``3`` ：低功耗。

``mesh models dfu metadata comp-elem-add <Loc> <NumS> <NumV> {<SigMID>|<VndCID> <VndMID>}...``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        添加目标节点的元素描述。

        * ``Loc`` 表示元素位置。
        * ``NumS`` 表示元素上实例化的 SIG 模型数量。
        * ``NumV`` 表示元素上实例化的厂商模型数量。
        * ``SigMID`` 表示 SIG 模型 ID。
        * ``VndCID`` 表示厂商模型公司标识符。
        * ``VndMID`` 表示厂商模型标识符。

``mesh models dfu metadata comp-hash-get [<Key(16 hex)>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        生成所存储组成数据的哈希，供元数据使用。

        * ``Key`` 表示用于生成哈希的可选 128 位密钥。如果提供的十六进制字符串短于 16 字节，则会用它填充数组的 N 个最高有效字节，其余字节补零。

``mesh models dfu metadata encode <Major> <Minor> <Rev> <BuildNum> <Size> <CoreType> <Hash> <Elems> [<UserData>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        为 DFU 编码元数据。

        * ``Major`` 表示固件的主版本号。
        * ``Minor`` 表示固件的次版本号。
        * ``Rev`` 表示固件的修订号。
        * ``BuildNum`` 表示构建编号。
        * ``Size`` 表示已签名 bin 文件的大小。
        * ``CoreType`` 表示新固件的核心类型：

                * ``1`` 表示应用核心。
                * ``2`` 表示网络核心。
                * ``4`` 表示应用特定的 BLOB。
        * ``Hash`` 表示使用 ``mesh models dfu metadata comp-hash-get`` 命令生成的组成数据哈希。
        * ``Elems`` 表示新固件上的元素数量。
        * ``UserData`` 表示随元数据提供的用户数据。


分段与重组（SAR）配置客户端
---------------------------

SAR 配置客户端是一种可选的 Mesh 模型，可通过 :kconfig:option:`CONFIG_BT_MESH_SAR_CFG_CLI` 配置选项启用。SAR 配置客户端模型用于配置支持 SAR 配置服务器模型的节点的下层传输层行为。


``mesh models sar tx-get``
^^^^^^^^^^^^^^^^^^^^^^^^^^

        发送 SAR Configuration Transmitter Get 消息。

``mesh models sar tx-set <SegIntStep> <UniRetransCnt> <UniRetransWithoutProgCnt> <UniRetransIntStep> <UniRetransIntInc> <MultiRetransCnt> <MultiRetransInt>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        发送 SAR Configuration Transmitter Set 消息。

        * ``SegIntStep`` 表示 SAR 分段间隔步长状态。
        * ``UniRetransCnt`` 表示 SAR 单播重传次数状态。
        * ``UniRetransWithoutProgCnt`` 表示 SAR 无进展的单播重传次数状态。
        * ``UniRetransIntStep`` 表示 SAR 单播重传间隔步长状态。
        * ``UniRetransIntInc`` 表示 SAR 单播重传间隔增量状态。
        * ``MultiRetransCnt`` 表示 SAR 多播重传次数状态。
        * ``MultiRetransInt`` 表示 SAR 多播重传间隔状态。

``mesh models sar rx-get``
^^^^^^^^^^^^^^^^^^^^^^^^^^

        发送 SAR Configuration Receiver Get 消息。

``mesh models sar rx-set <SegThresh> <AckDelayInc> <DiscardTimeout> <RxSegIntStep> <AckRetransCount>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        发送 SAR Configuration Receiver Set 消息。

        * ``SegThresh`` 表示 SAR 分段阈值状态。
        * ``AckDelayInc`` 表示 SAR 确认延迟增量状态。
        * ``DiscardTimeout`` 表示 SAR 丢弃超时状态。
        * ``RxSegIntStep`` 表示 SAR 接收端分段间隔步长状态。
        * ``AckRetransCount`` 表示 SAR 确认重传次数状态。


私有信标客户端
--------------

私有信标客户端模型是一种可选的 Mesh 子系统，可通过 :kconfig:option:`CONFIG_BT_MESH_PRIV_BEACON_CLI` 配置选项启用。

``mesh models prb priv-beacon-get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取目标的私有信标状态。可能的值：

                * ``0x00`` 表示节点不广播私有信标。
                * ``0x01`` ：节点广播私有信标。

``mesh models prb priv-beacon-set <Val(off, on)> <RandInt(10s steps)>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        设置目标节点的私有信标状态。

        * ``Val`` ：控制私有信标状态。
        * ``RandInt`` ：随机刷新间隔（以 10 秒为步长），或为 0 以保持当前值。

``mesh models prb priv-gatt-proxy-get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取目标节点的 Private GATT Proxy 状态。可能的值如下：

                * ``0x00`` ：支持 Private Proxy 功能，但处于禁用状态。
                * ``0x01`` ：Private Proxy 功能已启用。
                * ``0x02`` ：不支持 Private Proxy 功能。

``mesh models prb priv-gatt-proxy-set <Val(off, on)>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        设置目标节点的 Private GATT Proxy 状态。

        * ``Val`` ：新的 Private GATT Proxy 值：

                * ``0x00`` ：禁用 Private Proxy 功能。
                * ``0x01`` ：启用 Private Proxy 功能。

``mesh models prb priv-node-id-get <NetKeyIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取目标节点的 Private Node Identity 状态。可能的值如下：

                * ``0x00`` ：节点未使用 Private Node Identity 进行广播。
                * ``0x01`` ：节点使用 Private Node Identity 进行广播。
                * ``0x02`` ：节点不支持使用 Private Node Identity 进行广播。

        * ``NetKeyIdx`` ：要获取其 Private Node Identity 状态的网络密钥索引。

``mesh models prb priv-node-id-set <NetKeyIdx> <State>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        设置目标节点的 Private Node Identity 状态。

        * ``NetKeyIdx`` ：要设置其 Private Node Identity 状态的网络密钥索引。
        * ``State`` ：新的 Private Node Identity 值：

                * ``0x00`` ：停止使用 Private Node Identity 进行广播。
                * ``0x01`` ：开始使用 Private Node Identity 进行广播。


Opcodes Aggregator 客户端
-------------------------

Opcodes Aggregator 客户端是一种可选的蓝牙 Mesh 模型，可通过 :kconfig:option:`CONFIG_BT_MESH_OP_AGG_CLI` 配置选项启用。Opcodes Aggregator 客户端模型用于支持将一系列访问层消息分派给支持 Opcodes Aggregator 服务器模型的节点。

``mesh models opagg seq-start <ElemAddr>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        启动 Opcodes Aggregator Sequence 消息。此命令会初始化用于聚合消息的上下文，并将后续 shell 命令的目标地址设置为 ``elem_addr`` 。

        * ``ElemAddr`` ：将处理聚合操作码的元素地址。

``mesh models opagg seq-send``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        发送 Opcodes Aggregator Sequence 消息。此命令会完成该过程，将聚合后的序列消息发送到目标节点，并清除上下文。

``mesh models opagg seq-abort``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        中止 Opcodes Aggregator Sequence 消息。此命令会清除 Opcodes Aggregator 客户端上下文。


远程配网客户端
--------------

远程配网客户端是一种可选的蓝牙 Mesh 模型，可通过 :kconfig:option:`CONFIG_BT_MESH_RPR_CLI` 配置选项启用。远程配网客户端模型通过使用远程配网服务器模型，支持将设备远程配网到 Mesh 网络中。

此 shell 模块可用于触发 Mesh 网络中设备上的远程配网客户端与远程配网服务器之间的交互。

``mesh models rpr scan <Timeout(s)> [<UUID(1-16 hex)>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        开始扫描未配网设备。

        * ``Timeout`` ：扫描超时时间（以秒为单位）。必须至少为 1 秒。
        * ``UUID`` ：要扫描的设备 UUID。如果提供的十六进制字符串短于 16 字节，则用该字符串填充数组的 N 个最高有效字节，其余字节补零。如果省略，则报告所有设备。

``mesh models rpr scan-ext <Timeout(s)> <UUID(1-16 hex)> [<ADType> ... ]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        开始对未配网设备进行扩展扫描。

        * ``Timeout`` ：扫描超时时间（以秒为单位）。有效值可以是从 :c:macro:`BT_MESH_RPR_EXT_SCAN_TIME_MIN` 到 :c:macro:`BT_MESH_RPR_EXT_SCAN_TIME_MAX` 之间的任意值。
        * ``UUID`` ：要为其启动扩展扫描的设备 UUID。如果提供的十六进制字符串短于 16 字节，则用该字符串填充数组的 N 个最高有效字节，其余字节补零。
        * ``ADType`` ：要包含在扫描报告中的 AD 类型列表。必须包含 1 到 :kconfig:option:`CONFIG_BT_MESH_RPR_AD_TYPES_MAX` 个条目。

``mesh models rpr scan-srv [<ADType> ... ]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        开始对远程配网服务器进行扩展扫描。

        * ``ADType`` ：要包含在扫描报告中的 AD 类型列表。必须包含 1 到 :kconfig:option:`CONFIG_BT_MESH_RPR_AD_TYPES_MAX` 个条目。

``mesh models rpr scan-caps``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取远程配网服务器的扫描能力。

``mesh models rpr scan-get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取远程配网服务器的当前扫描状态。

``mesh models rpr scan-stop``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        停止远程配网服务器上任何正在进行的扫描。

``mesh models rpr link-get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取远程配网服务器的当前链路状态。

``mesh models rpr link-close``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        关闭远程配网服务器上的任何已打开链路。

``mesh models rpr provision-remote <UUID(1-16 hex)> <NetKeyIdx> <Addr>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        通过 PB-Remote 配网承载对 Mesh 节点进行配网。

        * ``UUID`` ：未配网节点的 UUID。如果提供的十六进制字符串短于 16 字节，则用该字符串填充数组的 N 个最高有效字节，其余字节补零。
        * ``NetKeyIdx`` ：要分配给未配网节点的网络密钥索引。
        * ``Addr`` ：要分配给远程设备的地址。如果 ``addr`` 为 0，则将选择可用的最低地址。

``mesh models rpr reprovision-remote <Addr> [<CompChanged(false, true)>]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        通过 PB-Remote 配网承载对 Mesh 节点重新配网。

        * ``Addr`` ：要分配给远程设备的地址。如果 ``addr`` 为 0，则将选择可用的最低地址。
        * ``CompChanged`` ：目标节点已指示其组成数据已更改。默认为 false。

``mesh models rpr instance-set <ElemIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        在使用其他远程配网客户端模型命令时，应使用指定元素上的远程配网客户端模型实例。

        * ``ElemIdx`` ：要在其上查找要使用的远程配网客户端模型实例的元素。

``mesh models rpr instance-get-all``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取节点上所有远程配网客户端模型实例的列表。


大型组成数据客户端
------------------

大型组成数据客户端是一种可选的蓝牙 Mesh 模型，可通过 :kconfig:option:`CONFIG_BT_MESH_LARGE_COMP_DATA_CLI` 配置选项启用。大型组成数据客户端模型用于支持以下功能：读取无法装入一条 Config Composition Data Status 消息的组成数据页，以及读取模型实例的元数据。

``mesh models lcd large-comp-data-get <Page> <Offset>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        发送 Large Composition Data Get 消息，以查询节点组成数据状态的一部分。

        * ``Page`` ：组成数据的页码。
        * ``Offset`` ：页内偏移量。

``mesh models lcd models-metadata-get <Page> <Offset>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        发送 Models Metadata Get 消息，以查询 Models Metadata 状态中某一页的一部分。

        * ``Page`` ：Models Metadata 的页码。
        * ``Offset`` ：页内偏移量。


桥接配置客户端
--------------

桥接配置客户端模型是一种可选的蓝牙 Mesh 模型，可通过 :kconfig:option:`CONFIG_BT_MESH_BRG_CFG_CLI` 配置选项启用。该模型可用于配置 Mesh 节点的子网桥接功能。

``mesh models brg get``
^^^^^^^^^^^^^^^^^^^^^^^

        获取当前子网桥接状态。

``mesh models brg set <State(disable, enable)>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        设置子网桥接状态。

        * ``State`` ：禁用或启用子网桥接功能。

``mesh models brg table-size-get``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取桥接表的当前大小。

``mesh models brg table-add <Directions> <NetIdx1> <NetIdx2> <Addr1> <Addr2>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        向桥接表添加一个条目。

        * ``Directions`` ：桥接流量允许的方向。有效值为：

                * ``0x01`` ：仅允许对源地址为 ``Addr1`` 且目标地址为 ``Addr2`` 的消息进行桥接。
                * ``0x02`` ：允许双向桥接。

        * ``NetIdx1`` ：第一个子网的 NetKey 索引。
        * ``NetIdx2`` ：第二个子网的 NetKey 索引。
        * ``Addr1`` ：第一个子网中节点的地址。
        * ``Addr2`` ：第二个子网中节点的地址。

``mesh models brg table-remove <NetIdx1> <NetIdx2> <Addr1> <Addr2>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        从桥接表中移除一个条目。

        * ``NetIdx1`` ：第一个子网的 NetKey 索引。
        * ``NetIdx2`` ：第二个子网的 NetKey 索引。
        * ``Addr1`` ：第一个子网中节点的地址。
        * ``Addr2`` ：第二个子网中节点的地址。

``mesh models brg subnets-get <Filter> <NetIdx> <StartIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取从桥接表中提取的经过筛选的 NetKey 索引对集合。

        * ``Filter`` 表示报告从桥接表中提取的 NetKey 索引对时应用的筛选器。允许值：

                * ``0x00`` 表示报告所有索引对。
                * ``0x01`` 表示报告第一个子网的 NetKey 索引与 ``NetIdx`` 匹配的索引对。
                * ``0x02`` 表示报告第二个子网的 NetKey 索引与 ``NetIdx`` 匹配的索引对。
                * ``0x03`` 表示报告其中一个 NetKey 索引与 ``NetIdx`` 匹配的索引对。

        * ``NetIdx`` 表示任意子网的 NetKey 索引。
        * ``StartIdx`` 表示读取时的起始偏移量，以 NetKey 索引对为单位。

``mesh models brg table-get <NetIdx1> <NetIdx2> <StartIdx>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        获取桥接表条目的地址列表以及允许的流量方向。

        * ``NetIdx1`` ：第一个子网的 NetKey 索引。
        * ``NetIdx2`` ：第二个子网的 NetKey 索引。
        * ``StartIdx`` 表示读取时的起始偏移量，以桥接表状态条目为单位。


配置数据库
==========

配置数据库是一个可选的 Mesh 子系统，可通过 :kconfig:option:`CONFIG_BT_MESH_CDB` 配置选项启用。配置数据库仅在配网器设备上可用，允许它们存储有关 Mesh 网络的所有信息。为避免冲突，网络中应只有一个启用了配置数据库的 Mesh 节点。该节点是配置器，负责向网络添加新节点并对其进行配置。

``mesh cdb create [NetKey(1-16 hex)]``
--------------------------------------

        创建配置数据库。

        * ``NetKey`` 表示主网络密钥（NetKeyIndex=0）的可选网络密钥值。如果提供的十六进制字符串短于 16 字节，将用它填充数组的 N 个最高有效字节，其余字节补零。如果省略，则默认为默认密钥值。


``mesh cdb clear``
------------------

        清除配置数据库中的所有数据。


``mesh cdb show``
-----------------

        显示配置数据库中的所有数据。


``mesh cdb node-add <UUID(1-16 hex)> <Addr> <ElemCnt> <NetKeyIdx> [DevKey(1-16 hex)]``
--------------------------------------------------------------------------------------

        手动向配置数据库添加 Mesh 节点。请注意，如果配置数据库已启用并已创建，使用 ``mesh provision`` 和 ``mesh provision-adv`` 配网的设备将自动添加。

        * ``UUID`` 表示节点的 128 位十六进制 UUID。如果提供的十六进制字符串短于 16 字节，将用它填充数组的 N 个最高有效字节，其余字节补零。
        * ``Addr`` 表示节点的单播地址，或设为 0 以自动选择最低的可用地址。
        * ``ElemCnt`` 表示节点上的元素数量。
        * ``NetKeyIdx`` 表示该节点配网时使用的网络密钥。
        * ``DevKey`` 表示设备可选的 128 位设备密钥值。如果提供的十六进制字符串短于 16 字节，将用它填充数组的 N 个最高有效字节，其余字节补零。如果省略，将生成一个随机值。


``mesh cdb node-del <Addr>``
----------------------------

        从配置数据库中删除 Mesh 节点。如有可能，在从配置数据库中删除该节点之前，应使用 ``mesh reset`` 重置该节点，以避免意外行为和对网络的不受控访问。

        * ``Addr`` 表示要删除的节点的地址。


``mesh cdb subnet-add <NetKeyIdx> [<NetKey(1-16 hex)>]``
--------------------------------------------------------

        向配置数据库添加网络密钥。之后可以将该网络密钥传递给网络中的 Mesh 节点。请注意，向配置数据库添加密钥不会自动将其添加到本地节点的已知网络密钥列表中。

        * ``NetKeyIdx`` 表示要添加的网络密钥的密钥索引。
        * ``NetKey`` 表示可选的 128 位网络密钥值。如果提供的十六进制字符串短于 16 字节，将用它填充数组的 N 个最高有效字节，其余字节补零。如果省略，将生成一个随机值。


``mesh cdb subnet-del <NetKeyIdx>``
-----------------------------------

        从配置数据库中删除网络密钥。

        * ``NetKeyIdx`` 表示要删除的网络密钥的密钥索引。


``mesh cdb app-key-add <NetKeyIdx> <AppKeyIdx> [<AppKey(1-16 hex)>]``
---------------------------------------------------------------------

        向配置数据库添加应用密钥。之后可以将该应用密钥传递给网络中的 Mesh 节点。请注意，向配置数据库添加密钥不会自动将其添加到本地节点的已知应用密钥列表中。

        * ``NetKeyIdx`` 表示应用密钥所绑定的网络密钥索引。
        * ``AppKeyIdx`` 表示要添加的应用密钥的密钥索引。
        * ``AppKey`` 表示可选的 128 位应用密钥值。如果提供的十六进制字符串短于 16 字节，将用它填充数组的 N 个最高有效字节，其余字节补零。如果省略，将生成一个随机值。


``mesh cdb app-key-del <AppKeyIdx>``
------------------------------------

        从配置数据库中删除应用密钥。

        * ``AppKeyIdx`` 表示要删除的应用密钥的密钥索引。


按需私有 GATT 代理客户端
------------------------

按需私有 GATT 代理客户端模型是一个可选的 Mesh 子系统，可通过 :kconfig:option:`CONFIG_BT_MESH_OD_PRIV_PROXY_CLI` 配置选项启用。

``mesh models od_priv_proxy od-priv-gatt-proxy [Dur(s)]``
---------------------------------------------------------

        在当前目标上设置 On-Demand Private GATT Proxy 状态，或从该目标获取此状态的值。

        * ``Dur`` 如果给定，则将 On-Demand Private GATT Proxy 的状态设置为该值（单位为秒）。否则获取此状态的值。


Solicitation PDU RPL 客户端
---------------------------

Solicitation PDU RPL 客户端模型是一个可选的 Mesh 子系统，可通过 :kconfig:option:`CONFIG_BT_MESH_SOL_PDU_RPL_CLI` 配置选项启用。

``mesh models sol_pdu_rpl sol-pdu-rpl-clear <RngStart> <Ackd> [RngLen]``
------------------------------------------------------------------------

        清除当前目标在给定 solicitation source（SSRC）地址范围内的 solicitation 重放保护列表（SRPL）。

        * ``RngStart`` 表示 SSRC 范围的起始地址。
        * ``Ackd`` 参数决定发送确认消息还是未确认消息。
        * ``RngLen`` 表示要从 solicitation RPL 列表中清除的 SSRC 地址范围长度。此参数为可选参数；如果未提供，则只清除单个 SSRC 地址。


统计信息
========

统计信息是一个可选的 Mesh 模块，可通过 :kconfig:option:`CONFIG_BT_MESH_STATISTIC` 配置选项启用。

``mesh stat adv_get``
---------------------

        获取帧统计信息。该命令会打印接收到的帧数，以及计划发送和成功发送的尝试次数。


``mesh stat adv_clear``
-----------------------

        清除之前收集的帧统计信息。


``mesh stat lpn_get``
---------------------

        获取测量得到的 LPN 好友关系定时参数。该命令会打印根据轮询周期中采集的时间戳推导出的 ReceiveDelay 和 ReceiveWindow 值。需要启用 :kconfig:option:`CONFIG_BT_MESH_LOW_POWER` 选项。


``mesh stat lpn_clear``
-----------------------

        清除之前收集的 LPN 定时统计信息。需要启用 :kconfig:option:`CONFIG_BT_MESH_LOW_POWER` 选项。
