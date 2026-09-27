.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _modem:

调制解调器模块
##############

该服务提供与调制解调器通信所需的模块。

调制解调器是自包含设备，实现执行 RF（射频）通信所需的硬件和软件，涵盖 GNSS、蜂窝、WiFi 等。

调制解调器模块通过数据输入/输出管道动态互连，因此可独立测试且高度灵活，从而确保稳定性和可扩展性。

调制解调器管道
**************

该模块用于以线程安全的方式，对 UART、CMUX DLCI 通道等多种机制上的数据输入/输出通信进行抽象。

调制解调器后端内部会包含一个 modem_pipe 结构实例，以及抽象其底层机制所需的缓冲区和附加结构。

.. image:: images/modem_pipes.svg
        :alt: 调制解调器管道
        :align: center

初始化时，调制解调器后端会返回指向其内部 modem_pipe 结构的指针，通过调制解调器管道 API 与该后端交互时将使用该指针。

.. doxygengroup:: modem_pipe

调制解调器 PPP
**************

该模块定义 L2 PPP 网络接口（见 :ref:`net_l2_interface`），并将其绑定到调制解调器后端。L2 PPP 接口收发网络数据包。这些网络数据包在通过调制解调器后端传输之前，必须封装在 PPP 帧中。该模块负责上述封装。

.. doxygengroup:: modem_ppp

调制解调器 CMUX
***************

该模块是遵循 3GPP 27.010 规范的 CMUX 实现。CMUX 是一种多路复用协议，允许多个双向数据流，称为 DLCI 通道。该模块连接到单个调制解调器后端，并对外暴露多个调制解调器后端，每个后端代表一个 DLCI 通道。

协议定义了简单的分帧方式，用于将每个 DLC 拆分为小块数据。

.. image:: images/cmux_frame.svg
        :alt: CMUX 基本帧
        :align: center

Zephyr 实现基本帧类型，其 MTU 大小可在构建时配置。

对于支持该功能的调制解调器，该模块还使用 CMUX 省电命令（PSC）实现省电。更多详情见下文 :ref:`cmux-power-saving` 一节。

.. doxygengroup:: modem_cmux

调制解调器管道链接
******************

该模块用于全局共享调制解调器管道，旨在将设备驱动中调制解调器管道的创建与设置，与这些管道的使用者解耦。有关如何在设备驱动和应用之间使用调制解调器管道链接的示例，请参见 :zephyr_file:`drivers/modem/modem_at_shell.c` 和 :zephyr_file:`drivers/modem/modem_cellular.c`。

.. doxygengroup:: modem_pipelink

调制解调器聊天
**************

该模块实现与调制解调器之间基于脚本的 AT 命令通信。AT 命令以 **脚本** 的形式组织，每个脚本都是一系列命令–响应交换。该模块通过调制解调器管道发送命令字符串，然后等待与某个预期模式匹配的响应。找到匹配项后，会调用可选回调并传入解析后的参数。

脚本在构建时使用 :c:macro:`MODEM_CHAT_SCRIPT_DEFINE` 和 :c:macro:`MODEM_CHAT_SCRIPT_CMDS_DEFINE` 宏定义。每个脚本条目将一个请求字符串与一个或多个 :c:struct:`modem_chat_match` 模式配对。匹配模式支持通过指定分隔符（例如 ``","``）来解析参数，从而可以轻松地从 ``+CSQ: 20,99`` 等响应中提取字段。

除了脚本化交换外，该模块还会持续监视数据流中的 **非请求** 响应——即调制解调器在没有前置命令的情况下发送的消息（例如 ``+CEREG:`` 网络注册更新）。这些响应由聊天实例初始化时注册的另一组匹配模式处理。

聊天模块可以连接到任意调制解调器管道，因此既可通过原始 UART 后端通信，也可通过 CMUX DLCI 通道通信，二者可互换。

.. doxygengroup:: modem_chat

.. _cellular-modem:

蜂窝调制解调器
**************

通用蜂窝调制解调器驱动 :zephyr_file:`drivers/modem/modem_cellular.c` 汇集了上文所述的所有模块，实现完整且与硬件无关的蜂窝数据连接。它公开标准的 Zephyr 网络接口，使应用无需任何调制解调器专用代码即可使用 :ref:`BSD sockets API <bsd_sockets_interface>`。

架构概述
========

该驱动将调制解调器模块组合成分层管道架构：

#. **UART 后端** —— :c:struct:`modem_backend_uart` 实例提供最底层的调制解调器管道。它将物理 UART 外设抽象为调制解调器管道 API，执行线程安全的中断驱动传输。

#. **CMUX** —— :c:struct:`modem_cmux` 实例连接到 UART 管道，并按照 3GPP 27.010 规范将其多路复用为两个 DLCI 通道。

#. **DLCI 通道 1（数据）** —— 该管道在初始化期间承载 AT 命令流量，连接建立后则承载 PPP 封装的 IP 数据。

#. **DLCI 通道 2（命令）** —— 该管道在数据连接活动期间专用于 AT 命令流量，使驱动能够查询信号质量、注册状态和其他参数，而不会中断数据流。

#. **调制解调器聊天** —— :c:struct:`modem_chat` 实例执行 AT 命令脚本。在 CMUX 启动之前，它直接连接到 UART 管道；之后，它会转到 DLCI 1 执行初始化脚本，然后转到 DLCI 2 进行周期性监视。

#. **调制解调器 PPP** —— :c:struct:`modem_ppp` 实例将 Zephyr IP 数据包封装在 PPP 帧中，并通过 DLCI 1 发送。在接收方向上，它剥离 PPP 帧封装，将数据包交付给网络协议栈。

同时使用两个 DLCI 通道是关键所在：调制解调器可以在 DLCI 1 上全速传输 IP 数据，而驱动可以在后台继续通过 DLCI 2 交换 AT 命令。

连接生命周期
============

该驱动围绕内部状态机构建，状态机会经历以下阶段：

上电与硬件复位
--------------

驱动会脉冲触发调制解调器的复位和电源 GPIO（如果在设备树中定义），并等待调制解调器做出响应。

初始 AT 配置
------------

调制解调器聊天模块直接连接到 UART 管道，并运行调制解调器专用的 ``init_chat_script``。该脚本通常会禁用回显，查询 IMEI、型号、固件版本，并配置非请求响应上报。此阶段的所有通信都是通过 UART 发送的普通 AT 命令——此时 CMUX 尚未启用。

CMUX 启动
---------

初始化脚本成功后，驱动发送 ``AT+CMUX`` 命令，将调制解调器切换到多路复用模式。CMUX 模块连接到 UART 管道，并打开 DLCI 1 和 DLCI 2。从此时起，所有通信都封装在 CMUX 帧内。

APN 配置与拨号
--------------

驱动将调制解调器聊天连接到 DLCI 1，运行动态构建的 APN 脚本（``AT+CGDCONT``），随后运行拨号脚本（``ATD*99#`` 或等效命令）。成功后，调制解调器会在 DLCI 1 上进入数据模式。

数据连接
--------

调制解调器 PPP 模块连接到 DLCI 1 管道，调制解调器聊天则转到 DLCI 2。``net_if_carrier_on()`` 会在 ``+CEREG`` （或 ``+CREG`` / ``+CGREG``）非请求响应表明调制解调器已注册到网络后被调用。

此时，Zephyr 网络协议栈通过 DLCI 1 协商 PPP 会话，应用可以正常使用 socket。与此同时，DLCI 2 上的周期性聊天脚本会监视信号质量和注册状态。

关机
----

驱动运行关机脚本并脉冲触发断电 GPIO，以干净地关闭调制解调器电源。状态机返回空闲状态。

添加对新调制解调器的支持
========================

通用蜂窝驱动使用通过设备树兼容绑定及其关联聊天脚本提供的按调制解调器配置。添加新调制解调器需要三项内容：

#. 包含通用蜂窝调制解调器基础绑定的 **设备树绑定**。

#. **聊天脚本** ，定义用于初始化、拨号、周期性监视以及（可选）关机的 AT 命令序列。

#. 将聊天脚本和硬件配置关联在一起的 **设备实例化宏**。

该驱动自动处理所有管道连接、CMUX 管理、PPP 封装和状态机逻辑。

支持的调制解调器
----------------

以下调制解调器已在 :zephyr_file:`drivers/modem/modem_cellular.c` 中得到支持：

* Fibocom LE250
* Quectel BG95, BG96
* Quectel EG25-G, EG800Q
* SIMCom SIM7080, A76xx
* u-blox SARA-R4, SARA-R5, LARA-R6
* Sierra Wireless HL7800
* Telit ME910G1, ME310G1, LE910C1 Thread-x, LEx10Q1
* Nordic Semiconductor nRF91 SLM
* Sequans GM02S

每个受支持的调制解调器都使用同一组宏定义（``MODEM_CHAT_SCRIPT_CMDS_DEFINE`` 、``MODEM_CHAT_SCRIPT_DEFINE`` 、``MODEM_CELLULAR_DEFINE_INSTANCE`` 等）。有关初始化、拨号、周期性和关机聊天脚本的完整示例，请参见 :zephyr_file:`drivers/modem/modem_cellular.c`。所有调制解调器共用的基础设备树属性记录在 :zephyr_file:`dts/bindings/modem/zephyr,cellular-modem-device.yaml` 中。

树外调制解调器
--------------

驱动宏和数据结构通过 :zephyr_file:`include/zephyr/drivers/modem/modem_cellular.h` 导出，因此可以在 Zephyr 树 **之外** 定义全新的调制解调器——例如在应用源代码中——而无需修改任何上游文件。这对于为特定用例微调 AT 命令序列，或在向上游提交之前开发新调制解调器的支持很有用。

首先创建一个包含通用基础绑定的设备树绑定，然后使用 ``modem_cellular.h`` 中的宏编写驱动源文件。只需以下三个文件。

**设备树绑定** —— ``app/dts/bindings/my,modem.yaml``：

.. code-block:: yaml

   compatible: "my,modem"

   include: zephyr,cellular-modem-device.yaml

**设备树叠加层** —— ``app.overlay`` （部分）：

.. code-block:: devicetree

   &uart30 {
       modem: modem {
           compatible = "my,modem";
           status = "okay";
           mdm-power-gpios = <&gpio1 13 GPIO_ACTIVE_HIGH>;
       };
   };

**驱动源代码** —— ``app/src/my_modem.c``：

.. code-block:: c

   #include <zephyr/drivers/modem/modem_cellular.h>
   #include <zephyr/device.h>

   MODEM_CELLULAR_COMMON_CHAT_MATCHES();
   MODEM_CHAT_MATCHES_DEFINE(my_modem_unsol,
       MODEM_CELLULAR_COMMON_UNSOL_MATCHES);

   /* Init script — configure the modem, enable unsolicited LTE
    * registration notifications, then switch to CMUX.
    */
   MODEM_CHAT_SCRIPT_CMDS_DEFINE(init_chat_script_cmds,
       MODEM_CHAT_SCRIPT_CMD_RESP("ATE0",              ok_match),
       MODEM_CHAT_SCRIPT_CMD_RESP("AT+CEREG=1",        ok_match),
       MODEM_CHAT_SCRIPT_CMD_RESP("AT+CMUX=0,0,5,127", ok_match));

   MODEM_CHAT_SCRIPT_DEFINE(init_chat_script, init_chat_script_cmds,
       abort_matches, modem_cellular_chat_callback_handler, 1);

   /* Dial script — enable the radio and open data mode */
   MODEM_CHAT_SCRIPT_CMDS_DEFINE(dial_chat_script_cmds,
       MODEM_CHAT_SCRIPT_CMD_RESP("AT+CFUN=1", ok_match),
       MODEM_CHAT_SCRIPT_CMD_RESP("ATD*99#",   connect_match));

   MODEM_CHAT_SCRIPT_DEFINE(dial_chat_script, dial_chat_script_cmds,
       dial_abort_matches, modem_cellular_chat_callback_handler, 60);

   static const struct modem_cellular_vendor_config my_modem_vendor = {
       .scripts = {
           .init = &init_chat_script,
           .dial = &dial_chat_script,
       },
       .unsol_matches = {
           .matches = my_modem_unsol,
           .size = ARRAY_SIZE(my_modem_unsol),
       },
       .chat_delimiter = "\r",
       .chat_filter = "\n",
       .power_pulse_duration_ms = 1000,
       .reset_pulse_duration_ms = 100,
       .startup_time_ms = 5000,
       .shutdown_time_ms = 5000,
   };

   /* Macro for defining a DT instance */
   #define MY_MODEM_DEVICE(inst)                                                   \
       MODEM_DT_INST_PPP_DEFINE(inst,                                              \
           MODEM_CELLULAR_INST_NAME(ppp, inst), NULL, 1500, 64);                   \
                                                                                   \
       static struct modem_cellular_data                                           \
           MODEM_CELLULAR_INST_NAME(data, inst);                                   \
                                                                                   \
       MODEM_CELLULAR_DEFINE_AND_INIT_USER_PIPES(inst,                             \
           (user_pipe_0, 3), (user_pipe_1, 4))                                     \
                                                                                   \
       MODEM_CELLULAR_DEFINE_INSTANCE(inst, &my_modem_vendor, NULL)

   #define DT_DRV_COMPAT my_modem
   DT_INST_FOREACH_STATUS_OKAY(MY_MODEM_DEVICE)
   #undef DT_DRV_COMPAT

上面的示例虽然简单，但足以在通用蜂窝调制解调器上启动 PPP 连接。更完整的示例请参见 :zephyr_file:`drivers/modem/modem_cellular.c`。

板级专用初始化脚本
==================

初始化、网络和拨号脚本的作用域为供应商级（以设备树 compatible 为键），因此对于使用同一调制解调器的不同板卡，若配置不同（例如 RF 调谐器频段路由），否则就需要派生供应商驱动。板卡可以改为使用 :c:macro:`MODEM_CELLULAR_BOARD_INIT_DEFINE` 注册自己的聊天脚本。该脚本在 CMUX 建立之后、APN 和网络配置之前，通过 AT 控制通道运行。未注册脚本的板卡不会增加 ROM 或 RAM 占用。

驱动会用推进连接序列的回调覆盖脚本的完成回调，因此脚本上设置的任何回调都会被忽略。

.. code-block:: c

   MODEM_CHAT_MATCH_DEFINE(board_init_ok_match, "OK", "", NULL);
   MODEM_CHAT_SCRIPT_CMDS_DEFINE(board_init_cmds,
       MODEM_CHAT_SCRIPT_CMD_RESP("AT+QCFG=\"rf/tuner_cfg\",0,\"12,28\"", board_init_ok_match));
   MODEM_CHAT_SCRIPT_NO_ABORT_DEFINE(board_init, board_init_cmds, NULL, 10);

   MODEM_CELLULAR_BOARD_INIT_DEFINE(DT_NODELABEL(modem), &board_init);

.. _cmux-power-saving:

CMUX 省电
*********

3GPP TS 27.010 规定了 CMUX 的省电机制；当调制解调器支持时，可在 Zephyr 中使用该机制。

规范中的以下章节介绍了该省电机制：

* 5.2.5 帧间填充
* 5.4.6.3.2 省电控制（PSC）消息
* 5.4.7 电源控制与唤醒机制

该省电机制为 CMUX 模块使用的 UART 设备提供运行时电源管理。当任何 DLCI 通道上都没有数据要发送或接收时，CMUX 模块会在可配置的超时之后进入空闲状态。在空闲状态下，CMUX 模块会向调制解调器发送省电控制（Power Saving Control）消息，请求其进入低功耗状态。随后，CMUX 模块可以关闭管道设备；如果启用了运行时电源管理，则允许 UART 设备断电。

当任何 DLCI 通道上要发送或接收数据时，CMUX 模块会退出空闲状态，并通过发送标志字符来唤醒调制解调器，直到从调制解调器收到一个标志字符。

对于通过 CMUX 之外的硬件线（而非带内协议）控制睡眠和唤醒的调制解调器，``cmux-no-powersave-handshake`` 属性会在两端跳过握手。进入时，CMUX 跳过 PSC 帧交换，直接转换到省电状态。退出时，管道重新打开后，CMUX 跳过标志字符交换，直接转换到已连接状态。下一个发出的帧会自行重新同步分帧。

某些调制解调器仅允许在 DTR（Data Terminal Ready，数据终端就绪）信号取消断言时关闭 UART 电源。在这种情况下，可以将支持 DTR 的 UART 设备与 CMUX 模块配合使用，根据 UART 的电源状态控制 DTR 信号。

UART 断电时若要靠传入数据唤醒，需要调制解调器支持 RING 信号来唤醒主机。RING 信号由调制解调器驱动处理；检测到 RING 信号后，驱动会打开管道设备，使 CMUX 模块能够唤醒调制解调器并处理传入数据。

:zephyr_file:`subsys/modem/modem_cmux.c` 模块使用以下状态机实现该省电机制。

.. image:: images/cmux_state_machine.svg
        :alt: 使用省电时的 CMUX 状态机
        :align: center

在已连接状态下，需要由 ``modem_cmux_process_received_byte()`` 按规范 5.2.5 帧间填充所述，回复重复的标志字符。空闲计时器持续运行，并在每次发送或接收帧时清除；计时器到期将启动向省电模式的转换。

在 POWERSAVE 状态下，所有 DLC 管道保持打开，但通向 UART 的管道被阻塞或关闭，因此所有数据都缓存在 CMUX 环形缓冲区中等待唤醒。在此状态下，还会回复重复的标志字符，以便远端按照 5.4.7 所述继续执行唤醒流程。如果管道关闭，则在启用运行时电源管理时允许 UART 设备断电。

当 CONNECTED 状态下的空闲计时器到期时，CMUX 状态机会阻塞所有 DLC 管道并发送 PSC 命令，让远端启动向 POWERSAVE 状态的转换。收到 PSC 命令的回复后，CMUX 转换到 POWERSAVE 模式。

在 CONNECTED 状态下，远端可能发送 PSC 命令来启动向省电模式的转换。CMUX 会阻塞所有 DLC 管道并发送 PSC 响应。当 TX 缓冲区排空后，CMUX 进入 POWERSAVE 状态。

在 POWERSAVE 状态期间，当任一 DLC 管道尝试发送数据时，CMUX 会将其缓冲，并转入 WAKEUP 状态；该状态按照 5.4.7 的规定，通过发送重复的标志字符流启动唤醒流程。远端回复标志字符，表示已准备好接收数据。随后 CMUX 停止发送标志字符，回到 CONNECTED 状态，恢复正常运行。

可以使用以下设备树属性配置 CMUX 省电机制：

.. code-block:: yaml

  cmux-enable-runtime-power-save:
    type: boolean
    description: Enable runtime power saving using CMUX PSC commands.
                 This requires modem to support CMUX and PSC commands while keeping the data
                 connection active.
  cmux-close-pipe-on-power-save:
    type: boolean
    description: Close the modem pipe when entering power save mode.
                When runtime power management is enabled, this closes the UART.
                This requires modem to support waking up the UART using RING signal.
  cmux-idle-timeout-ms:
    type: int
    description: Time in milliseconds after which CMUX will enter power save mode.
    default: 10000


启用省电的 CMUX 设备树配置示例：

.. code-block:: devicetree

  &uart1 {
    status = "okay";
    zephyr,pm-device-runtime-auto;

    uart_dtr: uart-dtr {
      compatible = "zephyr,uart-dtr";
      dtr-gpios = <&interface_to_nrf9160 4 GPIO_ACTIVE_LOW>;
      status = "okay";
      zephyr,pm-device-runtime-auto;

      modem: modem {
        compatible = "nordic,nrf91-slm";
        status = "okay";
        mdm-ring-gpios = <&interface_to_nrf9160 5 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>;
        zephyr,pm-device-runtime-auto;
        cmux-enable-runtime-power-save;
        cmux-close-pipe-on-power-save;
        cmux-idle-timeout-ms = <5000>;
      };
    };
  };

上面的示例展示了一个支持 DTR 的 UART 设备，由支持 CMUX 和 PSC 命令的调制解调器使用。DTR 信号用于控制 UART 的电源状态。调制解调器发出的 RING 信号用于在其断电时唤醒调制解调器子系统。
