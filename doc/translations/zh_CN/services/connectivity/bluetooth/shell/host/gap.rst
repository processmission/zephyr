.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：GAP Shell
###############

GAP shell 是蓝牙的“主”shell，负责连接管理、扫描、广播等。


身份
****

身份是 Zephyr 主机的一个概念，允许单个物理设备表现为多个逻辑蓝牙设备。

该 shell 允许创建多个身份，最大数量由 Kconfig 符号 :kconfig:option:`CONFIG_BT_ID_MAX` 设置。要创建新身份，请使用 :code:`bt id-create` 命令。然后可以通过其 ID 选择使用它： :code:`bt id-select <id>`。最后，可以使用 :code:`id-show` 列出所有可用身份。

扫描设备
********

使用 :code:`bt scan on` 命令开始扫描。根据所在环境，shell 中可能会打印大量行。要停止扫描，请运行 :code:`bt scan off`，滚动应会停止。

以下是可能看到的内容示例：

.. code-block:: console

        uart:~$ bt scan on
        Bluetooth active scan enabled
        [DEVICE]: R:CB:01:1A:2D:6E:AE, AD evt type 0, RSSI -78  C:1 S:1 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:20:C2:EE:59:85:5B, AD evt type 3, RSSI -62  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:E3:72:76:87:2F:E8, AD evt type 3, RSSI -74  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:1E:19:25:8A:CB:84, AD evt type 3, RSSI -67  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:26:42:F3:D5:A0:86, AD evt type 3, RSSI -73  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:0C:61:D1:B9:5D:9E, AD evt type 3, RSSI -87  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:20:C2:EE:59:85:5B, AD evt type 3, RSSI -66  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:25:3F:7A:EE:0F:55, AD evt type 3, RSSI -83  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        uart:~$ bt scan off
        Scan successfully stopped

如您所见，这可能会导致大量结果。为了减少结果数量并轻松找到特定设备，可以启用扫描过滤器。过滤器有四种类型：按名称、按 RSSI、按地址和按周期性广播间隔。要应用过滤器，请使用 :code:`bt scan-set-filter` 命令，后跟过滤器类型。可以再次使用这些命令来添加多个过滤器。

例如，如果您只想查找名称为 *test shell* 的设备：

.. code-block:: console

        uart:~$ bt scan-filter-set name "test shell"

或者，如果您想查找距离非常近的设备：

.. code-block:: console

        uart:~$ bt scan-filter-set rssi -40
        RSSI cutoff set at -40 dB

最后，如果要移除所有过滤器：

.. code-block:: console

        uart:~$ bt scan-filter-clear all

可以使用 :code:`bt scan on` 命令创建 *主动* 扫描器，这意味着扫描器会通过发送 *扫描请求* 数据包向广播者询问更多信息。或者，可以使用 :code:`bt scan passive` 命令创建 *被动扫描器*，这样扫描器就不会向广播者询问更多信息。

启用 :kconfig:option:`CONFIG_BT_SCAN_EXT_FILTER_POLICY` 后， :code:`bt scan --ext-filter-policy on` 命令会使用扩展扫描器过滤策略启动扫描器。此时控制器还会报告目标地址是其无法解析的可解析私有地址的定向广播。定向广播的目标地址会单独打印在一行上。这要求控制器支持扩展扫描器过滤策略，否则该命令会失败。

连接到设备
**********

要连接到设备，您需要知道其地址和地址类型，并使用 :code:`bt connect` 命令，将地址和类型作为参数。

示例如下：

.. code-block:: console

        uart:~$ bt connect R:52:84:F6:BD:CE:48
        Connection pending
        Connected: R:52:84:F6:BD:CE:48
        Remote LMP version 5.3 (0x0c) subversion 0xffff manufacturer 0x05f1
        LE Features: 0x000000000001412f
        LE PHY updated: TX PHY LE 2M, RX PHY LE 2M
        LE conn  param req: int (0x0018, 0x0028) lat 0 to 42
        LE conn param updated: int 0x0028 lat 0 to 42

可以使用 :code:`bt connections` 命令列出 shell 的活动连接。shell 的最大连接数由 :kconfig:option:`CONFIG_BT_MAX_CONN` 定义。可以使用 :code:`bt disconnect <address: P:XX:XX:XX:XX:XX:XX or R:XX:XX:XX:XX:XX:XX>` 命令断开连接。

.. note::

        如果您之前正在进行扫描，只需运行 :code:`bt connect` 命令即可连接到最近扫描到的设备。

        或者，可以使用 :code:`bt connect-name <name>` 命令自动启用带名称过滤器的扫描，并连接到第一个匹配项。

广播
****

使用 :code:`bt advertise on` 命令开始广播。这将使用默认参数，并以设备名称广播可解析私有地址。您也可以运行 :code:`bt advertise on identity` 命令来选择使用身份地址。要停止广播，请使用 :code:`bt advertise off` 命令。

要启用更高级的广播功能，应使用 :code:`bt adv-create` 命令创建广播器。广播器的参数可以在创建时传入，也可以通过 :code:`bt adv-param` 命令传入。要使用新建的广播器开始广播，请使用 :code:`bt adv-start` 命令，然后使用 :code:`bt adv-stop` 命令停止广播。

使用自定义广播器时，可以选择它是否可连接或可扫描。这会产生四种选项： :code:`conn-scan`、 :code:`conn-nscan`、 :code:`nconn-scan` 和 :code:`nconn-nscan`。创建广播器或更新其参数时，这些参数是必需的。

例如，如果您想创建一个可连接且可扫描的广播器并启动它：

.. code-block:: console

        uart:~$ bt adv-create conn-scan
        Created adv id: 0, adv: 0x200022f0
        uart:~$ bt adv-start
        Advertiser[0] 0x200022f0 set started

您可能会注意到，这样自定义广播器不会广播设备名称；您需要添加名称。继续上一个示例：

.. code-block:: console

        uart:~$ bt adv-stop
        Advertiser set stopped
        uart:~$ bt adv-data dev-name
        uart:~$ bt adv-start
        Advertiser[0] 0x200022f0 set started

现在应该能在广播数据中看到设备名称。也可以使用 :code:`name <custom name>` 而不是 :code:`dev-name` 来设置自定义名称。还可以使用 :code:`bt adv-data` 命令手动设置广播数据。以下示例展示如何使用原始广播数据设置广播器名称：

.. code-block:: console

        uart:~$ bt adv-create conn-scan
        Created adv id: 0, adv: 0x20002348
        uart:~$ bt adv-data 1009426C7565746F6F74682D5368656C6C
        uart:~$ bt adv-start
        Advertiser[0] 0x20002348 set started

数据必须按照蓝牙核心规范进行格式化（参见 5.3 版，第 3 卷，C 部分，11 节）。在此示例中，第一个八位字节是数据大小（数据加上一个表示数据类型的八位字节），第二个八位字节是数据类型， ``0x09`` 是完整本地名称，其余数据是 ASCII 格式的名称。因此，在另一台设备上应能看到名称 *Bluetooth-Shell*。

广播时，如果其他设备使用 *主动* 扫描器，您可能会收到 *扫描请求* 数据包。要查看这些数据包，可以将 :code:`scan-reports` 添加到广播器的参数中。

定向广播
========

如果您想重新连接到某台设备，可以在 shell 中使用定向广播。以下示例演示如何创建定向广播器，地址在 :code:`directed` 参数之后指定。 :code:`low` 参数表示我们希望使用低占空比模式；如果远端设备启用了隐私功能并支持解析定向广播中目标地址的地址，则必须使用 :code:`dir-rpa` 参数。

.. code-block:: console

        uart:~$ bt adv-create conn-scan directed R:D7:54:03:CE:F3:B4 low dir-rpa
        Created adv id: 0, adv: 0x20002348

之后，您可以启动广播器，目标设备便能够重新连接。

扩展广播
========

现在来看一些扩展广播功能。要启用扩展广播，请使用 ``ext-adv`` 参数。

.. code-block:: console

        uart:~$ bt adv-create conn-nscan ext-adv
        Created adv id: 0, adv: 0x200022f0
        uart:~$ bt adv-start
        Advertiser[0] 0x200022f0 set started

这将创建一个可连接且不可扫描的扩展广播器。

加密广播数据
============

Zephyr 支持加密广播数据功能。 :code:`bt encrypted-ad` 子命令允许管理指定广播器的广播数据。

要加密广播数据，需要提供密钥材料，可以使用 :code:`bt encrypted-ad set-keys <session key> <init vector>` 完成。会话密钥长度为 16 字节，初始化向量长度为 8 字节。

可以使用 :code:`bt encrypted-ad add-ad` 和 :code:`bt encrypted-ad add-ead` 添加广播数据。前者会添加一个广播数据结构（如核心规范中所定义），后者会读取给定数据、对其进行加密，然后添加生成的加密广播数据结构。可以混合使用加密和非加密数据；添加完广播数据后，可以使用 :code:`bt encrypted-ad commit-ad` 将更改应用到所选广播器的数据。之后即可如前所述启动广播器。可以使用 :code:`bt encrypted-ad clear-ad` 清除广播数据。

在中心设备侧，可以通过按照前面所述设置正确的密钥材料，然后使用 :code:`bt encrypted-ad decrypt-scan on` 启用数据解密，来解密收到的加密广播数据。

.. note::

        要在扫描报告中查看广播数据，需要启用 :code:`bt scan-verbose-output`。

.. note::

        可以通过增大 :kconfig:option:`CONFIG_BT_CTLR_ADV_DATA_LEN_MAX` 和 :kconfig:option:`CONFIG_BT_CTLR_SCAN_DATA_LEN_MAX` 的值来增加广播数据的长度。

下面是一个演示 EAD 用法的简单示例：

.. tabs::

        .. group-tab:: 外围设备

                .. code-block:: console

                        uart:~$ bt init
                        ...
                        uart:~$ bt adv-create conn-nscan ext-adv
                        Created adv id: 0, adv: 0x81769a0
                        uart:~$ bt encrypted-ad set-keys 9ba22d3824efc70feb800c80294cba38 2e83f3d4d47695b6
                        session key set to:
                        00000000: 9b a2 2d 38 24 ef c7 0f  eb 80 0c 80 29 4c ba 38 |..-8$... ....)L.8|
                        initialisation vector set to:
                        00000000: 2e 83 f3 d4 d4 76 95 b6                          |.....v..         |
                        uart:~$ bt encrypted-ad add-ad 06097368656C6C
                        uart:~$ bt encrypted-ad add-ead 03ffdead03ffbeef
                        uart:~$ bt encrypted-ad commit-ad
                        Advertising data for Advertiser[0] 0x81769a0 updated.
                        uart:~$ bt adv-start
                        Advertiser[0] 0x81769a0 set started

        .. group-tab:: 中心设备

                .. code-block:: console

                        uart:~$ bt init
                        ...
                        uart:~$ bt scan-verbose-output on
                        uart:~$ bt encrypted-ad set-keys 9ba22d3824efc70feb800c80294cba38 2e83f3d4d47695b6
                        session key set to:
                        00000000: 9b a2 2d 38 24 ef c7 0f  eb 80 0c 80 29 4c ba 38 |..-8$... ....)L.8|
                        initialisation vector set to:
                        00000000: 2e 83 f3 d4 d4 76 95 b6                          |.....v..         |
                        uart:~$ bt encrypted-ad decrypt-scan on
                        Received encrypted advertising data will now be decrypted using provided key materials.
                        uart:~$ bt scan on
                        Bluetooth active scan enabled
                        [DEVICE]: R:68:49:30:68:49:30, AD evt type 5, RSSI -59   shell C:1 S:0 D:0 SR:0 E:1 Prim: LE 1M, Secn: LE 2M, Interval: 0x0000 (0 us), SID: 0x0
                                [SCAN DATA START - EXT_ADV]
                                Type 0x09:    shell
                                Type 0x31: Encrypted Advertising Data: 0xe2, 0x17, 0xed, 0x04, 0xe7, 0x02, 0x1d, 0xc9, 0x40, 0x07, uart:~0x18, 0x90, 0x6c, 0x4b, 0xfe, 0x34, 0xad
                                [START DECRYPTED DATA]
                                Type 0xff: 0xde, 0xad
                                Type 0xff: 0xbe, 0xef
                                [END DECRYPTED DATA]
                                [SCAN DATA END]
                        ...

过滤接受列表
************

可以创建一个允许地址列表，用于自动连接到这些地址。操作方法如下：

.. code-block:: console

        uart:~$ bt fal-add R:47:38:76:EA:29:36
        uart:~$ bt fal-add R:66:C8:80:2A:05:73
        uart:~$ bt fal-connect on

然后 shell 会连接到第一个可用设备。在示例中，如果两台设备同时广播，我们将连接到添加到列表的第一个地址。

通过使用 :code:`fal` 选项，过滤接受列表也可用于扫描或广播。例如，如果我们要扫描一组选定的地址，可以设置一个过滤接受列表：

.. code-block:: console

        uart:~$ bt fal-add R:65:4B:9E:83:AF:73
        uart:~$ bt fal-add R:73:72:82:B4:8F:B9
        uart:~$ bt fal-add R:5D:85:50:1C:72:64
        uart:~$ bt scan on fal

您应该只会看到扫描器报告的这三个地址。

启用安全功能
************

连接到设备后，可以启用多个安全级别，以下是蓝牙 LE 的列表：

* **1** 无加密且无身份验证；
* **2** 有加密且无身份验证；
* **3** 有加密且需要身份验证；
* **4** 蓝牙 LE 安全连接。

要启用安全功能，请使用 :code:`bt security <level>` 命令。对于需要身份验证的级别（级别 3 及以上），必须先设置身份验证方法。可以使用 :code:`bt auth all` 命令来完成。之后，当您设置安全级别时，系统会要求您在两台设备上确认通行密钥。在 shell 侧，请使用 :code:`bt auth-passkey-confirm` 命令确认。

配对
====

启用身份验证要求设备可绑定。默认情况下，shell 是可绑定的。可以使用 :code:`bt bondable off` 使 shell 不可绑定。可以使用 :code:`bt bonds` 命令列出所有已配对的设备。

已配对设备的最大数量使用 :kconfig:option:`CONFIG_BT_MAX_PAIRED` 设置。可以使用 :code:`bt clear <address: P:XX:XX:XX:XX:XX:XX or R:XX:XX:XX:XX:XX:XX>` 移除已配对设备，或使用 :code:`bt clear all` 命令移除所有已配对设备。
