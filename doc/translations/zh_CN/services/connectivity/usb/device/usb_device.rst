.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _usb_device_stack:

USB 设备支持（已弃用）
######################

.. contents::
    :local:
    :depth: 3

概述
****

USB 设备协议栈是 USB 设备控制器驱动与 USB 设备类驱动或客户应用之间的硬件无关接口。它移植自 LPCUSB 设备协议栈，并随时间不断修改和扩展。它提供以下功能：

* 使用设备控制器驱动提供的 :ref:`usb_dc_api` 与 USB 设备控制器交互。
* 响应标准设备请求并返回标准描述符，实质上完成了“第 9 章”处理，具体而言就是通用串行总线规范 2.0 修订版表 9-3 中的标准设备请求。
* 提供供 USB 设备类或客户应用使用的编程接口。API 说明见 :zephyr_file:`include/zephyr/usb/usb_device.h`。

.. note::
   :ref:`usb_api` 中列出的所有 API 以及依赖它们的函数均已弃用，并将在 v4.5.0 中移除。请使用 :ref:`usb_device_next_api` 中的 API 所代表的新 USB 设备支持。

支持的 USB 类
*************

音频
====

音频类目前有一个实验性实现。它遵循 1.00 版规范（``bcdADC 0x0100``），仅支持同步（Synchronous）同步类型。可参考 :zephyr:code-sample:`usb-audio-headphones-microphone` 和 :zephyr:code-sample:`usb-audio-headset` 示例。

蓝牙 HCI USB 传输层
===================

蓝牙 HCI USB 传输层实现使用 :ref:`bt_hci_raw` 向主机公开 HCI 接口。它不完全符合蓝牙规范中的描述，仅包含一个具有以下端点配置的接口：

* 通过控制端点传输的 HCI 命令（仅限主机到设备）
* 通过中断 IN 端点传输的 HCI 事件
* 通过一个批量 IN 端点和一个批量 OUT 端点传输的 ACL 数据

尚未为语音通道实现第二个接口，因为 :ref:`bluetooth` 中不支持该类型。在 Linux 下，如果 HCI USB 传输层是配置中出现的唯一接口，这并不是大问题，btusb 驱动不会尝试占用第二个（等时）接口。但这样一来，如果 HCI USB 用于复合配置并且是第一个接口，Linux btusb 驱动就会同时占用第一个和下一个接口，导致其他复合功能无法工作。由于这个问题，HCI USB 不应在复合配置中使用。此问题已在新的 USB 支持实现中得到修复。

可参考 :zephyr:code-sample:`bluetooth_hci_usb` 示例。

.. _usb_device_cdc_acm:

CDC ACM
=======

在 Zephyr 中，CDC ACM 类被用作不同子系统的后端。不过，对于缺乏经验的用户来说，其配置可能并不容易。下文介绍不同的用例及一些陷阱。

CDC ACM 用户使用的接口是 :ref:`uart_api` 驱动 API。但与真实 UART 控制器相比，其行为有两个重要区别：

* 只有在 USB 设备协议栈初始化并启动后才能进行数据传输，在此之前任何数据都会被丢弃
* 即使设备已连接到主机，也仍需要主机侧有应用来请求数据
* CDC ACM 的 poll out 实现遵循该 API，仅当启用了 hw-flow-control 属性并且从非 ISR 上下文调用时，才会在 TX 环形缓冲区已满时阻塞。

CDC ACM UART 的设备树 compatible 属性为 :dtcompatible:`zephyr,cdc-acm-uart`。当启用 USB 设备支持且设备树源中存在兼容节点时，会自动选择 CDC ACM 支持。如有必要，可以通过 :kconfig:option:`CONFIG_USB_CDC_ACM` 显式禁用 CDC ACM 支持。受控制器上支持的最大端点数量限制，大约可以定义和使用四个 CDC ACM UART 实例。

CDC ACM UART 节点应当是 USB 设备控制器节点的子节点。由于控制器节点的命名因厂商而异，而我们的示例和应用应尽可能通用，默认 USB 设备控制器通常会分配 ``zephyr_udc0`` 节点标签。通常，CDC ACM UART 会在设备树 overlay 文件中描述，如下所示：

.. code-block:: devicetree

        &zephyr_udc0 {
                cdc_acm_uart0: cdc_acm_uart0 {
                        compatible = "zephyr,cdc-acm-uart";
                        label = "CDC_ACM_0";
                };
        };

示例 :zephyr:code-sample:`usb-cdc-acm` 有类似的 overlay 文件。由于不存在特殊属性，使用设备树来描述 CDC ACM UART 似乎有些小题大做。使用设备树的动机在于，应用中能够轻松互换真实 UART 控制器与 CDC ACM UART。

通过 CDC ACM UART 使用控制台
----------------------------

利用上述 CDC ACM UART 节点和 chosen 节点的 ``zephyr,console`` 属性，我们可以描述要将 CDC ACM UART 用于控制台。:zephyr:code-sample:`usb-cdc-acm-console` 示例使用了类似的 overlay 文件。

.. code-block:: devicetree

        / {
                chosen {
                        zephyr,console = &cdc_acm_uart0;
                };
        };

        &zephyr_udc0 {
                cdc_acm_uart0: cdc_acm_uart0 {
                        compatible = "zephyr,cdc-acm-uart";
                        label = "CDC_ACM_0";
                };
        };

在应用使用控制台之前，建议等待 DTR 信号：

.. code-block:: c

        const struct device *const dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_console));
        uint32_t dtr = 0;

        if (usb_enable(NULL)) {
                return;
        }

        while (!dtr) {
                uart_line_ctrl_get(dev, UART_LINE_CTRL_DTR, &dtr);
                k_sleep(K_MSEC(100));
        }

        printk("nuqneH\n");

将 CDC ACM UART 用作后端
------------------------

与控制台示例一样，可以通过设置 :ref:`devicetree-chosen-nodes` 属性，将 CDC ACM UART 配置为其他子系统的后端。

下面列出了一些 Zephyr 特有的 chosen 属性，可用于为子系统或应用选择 CDC ACM UART 作为后端：

* ``zephyr,bt-c2h-uart`` 用于蓝牙，例如参见 :zephyr:code-sample:`bluetooth_hci_uart`
* ``zephyr,ot-uart`` 用于 OpenThread，例如参见 :zephyr:code-sample:`openthread-coprocessor`
* ``zephyr,shell-uart`` 由 shell 用于串行后端，例如参见 :zephyr_file:`samples/subsys/shell/shell_module`
* ``zephyr,uart-mcumgr`` 由 :zephyr:code-sample:`smp-svr` 示例使用

POSIX 默认 tty ECHO 的缓解措施
------------------------------

像 Linux 这样的 POSIX 系统默认在 tty 设备上启用 ECHO。主机侧应用可以通过在 tty 设备上调用 ``open()`` 并发出 ``ioctl()`` （最好通过 ``tcsetattr()``）来禁用 ECHO（如果不需要）。遗憾的是，``open()`` 与 ``ioctl()`` 之间存在固有竞态：在此期间 ECHO 已启用，接收到的任何字符（即使主机应用没有调用 ``read()``）都会被回显。当 CDC ACM 端口在另一端没有真实 UART 的情况下使用时，由于不存在由波特率造成的任意延迟，这个问题尤为明显。

为缓解该问题，Zephyr CDC ACM 实现在设备配置完成后为 IN 端点设置 ZLP。当主机读取 ZLP 时（这基本上可以最好地表明主机应用已打开 tty 设备），Zephyr 会强制延迟 :kconfig:option:`CONFIG_CDC_ACM_TX_DELAY_MS` 毫秒后再发送实际负载。这应能让第一个、也是唯一一个打开 tty 设备的应用有足够时间在不需要 ECHO 时禁用 ECHO。如果完全不需要来自 CDC ACM 设备的 ECHO，最好设置 udev 规则，以便设备一连接就禁用 ECHO。

当 CDC ACM 实例用于 Zephyr shell 时，尤其不希望启用 ECHO，因为发回 shell 的用于设置颜色的控制字符会被解释为（无效的）命令，用户会看到乱码。虽然 minicom 默认禁用 ECHO，但在退出并重置时，它会将 termios 设置恢复为进入时的值。因此，如果 minicom 是第一个打开 tty 设备的应用，那么带重置的退出会重新启用 ECHO，从而给下一个应用带来问题（而 Zephyr 侧无法缓解该问题）。为避免此问题，建议让 minicom 退出时不执行重置，或者在启动 minicom 前禁用 ECHO。

DFU
===

USB DFU 类实现与 :ref:`dfu` 和 :ref:`mcuboot_api` 紧密耦合。这意味着目标平台必须支持 :ref:`flash_img_api` API。

可参考 :zephyr:code-sample:`legacy-usb-dfu` 示例。

USB 人机接口设备（HID）支持
===========================

HID 支持借助 :ref:`device_model_api`，仅仅是为了让应用可以使用 :c:func:`device_get_binding`。请注意，并没有专门的 HID 设备 API；接口由 :c:struct:`hid_ops` 提供。默认实例名称为 ``HID_n``，其中 n 可以是 {0, 1, 2, ...}，具体取决于 :kconfig:option:`CONFIG_USB_HID_DEVICE_COUNT`。

每个 HID 实例都需要一个 HID 报告描述符。核心接口和报告描述符必须使用 :c:func:`usb_hid_register_device` 注册。

由于 USB HID 规范不仅由 USB 子系统使用，USB HID API 参考被分成两部分：:ref:`usb_hid_common` 和 :ref:`usb_hid_device`。应使用 :ref:`usb_hid_common` 中的 HID 辅助宏来构成 HID 报告描述符。宏名称与 USB HID 规范中使用的名称一致。

对于 HID 类接口，每个实例都需要一个 IN 中断端点，OUT 中断端点则是可选的。因此，:c:struct:`hid_ops` 的最低实现要求是提供 ``int_in_ready`` 回调。

.. code-block:: c

        #define REPORT_ID               1
        static bool configured;
        static const struct device *hdev;

        static void int_in_ready_cb(const struct device *dev)
        {
                static uint8_t report[2] = {REPORT_ID, 0};

                if (hid_int_ep_write(hdev, report, sizeof(report), NULL)) {
                        LOG_ERR("Failed to submit report");
                } else {
                        report[1]++;
                }
        }

        static void status_cb(enum usb_dc_status_code status, const uint8_t *param)
        {
                if (status == USB_DC_RESET) {
                        configured = false;
                }

                if (status == USB_DC_CONFIGURED && !configured) {
                        int_in_ready_cb(hdev);
                        configured = true;
                }
        }

        static const uint8_t hid_report_desc[] = {
                HID_USAGE_PAGE(HID_USAGE_GEN_DESKTOP),
                HID_USAGE(HID_USAGE_GEN_DESKTOP_UNDEFINED),
                HID_COLLECTION(HID_COLLECTION_APPLICATION),
                HID_LOGICAL_MIN8(0x00),
                HID_LOGICAL_MAX16(0xFF, 0x00),
                HID_REPORT_ID(REPORT_ID),
                HID_REPORT_SIZE(8),
                HID_REPORT_COUNT(1),
                HID_USAGE(HID_USAGE_GEN_DESKTOP_UNDEFINED),
                HID_INPUT(0x02),
                HID_END_COLLECTION,
        };

        static const struct hid_ops my_ops = {
                .int_in_ready = int_in_ready_cb,
        };

        int main(void)
        {
                int ret;

                hdev = device_get_binding("HID_0");
                if (hdev == NULL) {
                        return -ENODEV;
                }

                usb_hid_register_device(hdev, hid_report_desc, sizeof(hid_report_desc),
                                        &my_ops);

                ret = usb_hid_init(hdev);
                if (ret) {
                        return ret;
                }

                return usb_enable(status_cb);
        }


如果应用希望通过 OUT 中断端点接收输出报告，则必须启用 :kconfig:option:`CONFIG_ENABLE_HID_INT_OUT_EP` 并提供 ``int_out_ready`` 回调。其缺点是，诸如 :kconfig:option:`CONFIG_ENABLE_HID_INT_OUT_EP` 或 :kconfig:option:`CONFIG_HID_INTERRUPT_EP_MPS` 之类的 Kconfig 选项会作用于所有实例。这一设计问题将在新 USB 支持的 HID 类实现中修复。

可参考 :zephyr:code-sample:`usb-hid-mouse` 示例。

大容量存储类（MSC）
===================

MSC 遵循 Bulk-Only 传输规范，并使用 :ref:`disk_access_api` 访问 RAM 磁盘、闪存分区上的仿真块设备或 SD 卡，并将其公开给主机。一次只能导出一个磁盘实例。

该实现使用的磁盘由 :kconfig:option:`CONFIG_MASS_STORAGE_DISK_NAME` 设置，并且应与应用希望公开给主机的磁盘访问驱动所使用的名称相同。Flash、RAM 和 SDMMC/MMC 磁盘驱动使用节点属性 ``disk-name`` 来设置磁盘名称。

对于闪存分区上的仿真块设备，必须在设备树中描述要使用的闪存分区和闪存磁盘。如果存储分区已在板级描述，应用设备树 overlay 还必须先删除 ``storage_partition`` 节点。:kconfig:option:`CONFIG_MASS_STORAGE_DISK_NAME` 应与 ``disk-name`` 属性相同。

.. code-block:: devicetree

        /delete-node/ &storage_partition;

        &mx25r64 {
                partitions {
                        compatible = "fixed-partitions";
                        #address-cells = <1>;
                        #size-cells = <1>;

                        storage_partition: partition@0 {
                                label = "storage";
                                reg = <0x00000000 0x00020000>;
                        };
                };
        };

        / {
                msc_disk0 {
                        compatible = "zephyr,flash-disk";
                        partition = <&storage_partition>;
                        disk-name = "NAND";
                        cache-size = <4096>;
                };
        };

``disk-property`` 的“NAND”可能令人困惑，但这只是某些文件系统标识磁盘的方式。因此，如果应用还要访问所公开磁盘上的文件系统，则应使用默认名称；可参考 :zephyr:code-sample:`usb-mass` 示例。

网络
====

有三种实现以类似方式工作，在远端（USB 主机）与 Zephyr 网络支持之间提供虚拟以太网连接。

* CDC ECM 类，通过 :kconfig:option:`CONFIG_USB_DEVICE_NETWORK_ECM` 启用
* CDC EEM 类，通过 :kconfig:option:`CONFIG_USB_DEVICE_NETWORK_EEM` 启用
* RNDIS 支持，通过 :kconfig:option:`CONFIG_USB_DEVICE_NETWORK_RNDIS` 启用

可参考 :zephyr:code-sample:`legacy-netusb` 示例。

使用 RNDIS 支持的应用应启用 :kconfig:option:`CONFIG_USB_DEVICE_OS_DESC`，以便在运行 Microsoft Windows 操作系统的主机上获得更好的用户体验。

二进制设备对象存储（BOS）支持
*****************************

可以使用 Kconfig 选项 :kconfig:option:`CONFIG_USB_DEVICE_BOS` 启用 BOS 处理。该选项还会将设备描述符 ``bcdUSB`` 改为 ``0210``。应用应使用 :c:func:`usb_bos_register_cap` 注册能力描述符等描述符。已注册的描述符会添加到根 BOS 描述符中，并由协议栈处理。

可参考 :zephyr:code-sample:`legacy-webusb` 示例。

接口编号与端点地址分配
**********************

在 USB 术语中，``function`` 是指向主机提供某项能力的设备，例如实现键盘的 HID 类设备。一个 ``function`` 包含一组 ``interfaces``；至少需要一个接口。一个接口可以包含设备 ``endpoints``；例如，实现 HID 类设备至少需要一个输入端点，而实现 USB DFU 类则不需要任何端点。组合了多个 ``function`` 的 USB 设备称为多功能 USB 设备，例如 HID 类设备与 CDC ACM 设备的组合。

借助 Zephyr RTOS 的 USB 支持，可以通过内置 USB 类/功能或自定义用户实现来组成各种组合。限制在于可用设备端点的数量。每个设备端点都有唯一地址。端点地址由端点方向和端点编号组合而成，是一个四位值。端点编号 0 用于默认控制方式，以初始化并配置 USB 设备。按照规范，功能中最多还可以使用 ``15 IN`` 和 ``15 OUT`` 个设备端点。实际数量取决于所使用的设备控制器。并非所有控制器都支持最大端点数量以及所有端点类型。例如，某个设备控制器可能支持一个 IN 和一个 OUT 等时端点，但仅支持端点编号 8，从而得到的端点地址为 0x88 和 0x08。此外，一个控制器可能在同一个端点编号上具有 IN/OUT 端点，即中断 IN 端点 0x81 和批量 OUT 端点 0x01，而另一个控制器可能只能为每个端点编号处理一个端点。接口、接口特定描述符和端点描述符会向主机提供关于接口数量、接口关联、端点类型和地址的信息。

针对特定功能的主机驱动会使用接口和端点描述符来获取端点地址、类型及其他属性。这使功能主机驱动可以保持通用；例如，可以构建由一个或多个 CDC ACM 以及一个或多个 CDC ECM 类实现组成的多功能设备，且不需要特定驱动。

Zephyr RTOS 中内置 USB 类/功能实现的接口和端点描述符通常按升序分配默认接口编号和端点地址。在初始化期间，默认接口编号可能会根据给定配置中的接口数量重新分配。端点地址会根据控制器能力以及给定配置中的接口数量重新分配，因为并非每个控制器都支持某些端点组合。这也意味着 Zephyr RTOS 中的设备侧类/功能必须在运行时检查实际的接口和端点描述符值。该机制还允许我们提供通用示例和通用多功能示例，这些示例仅受控制器提供的资源（例如端点数量和端点 FIFO 大小）限制。

有些主机驱动针对特定功能，例如 Linux 内核中的某些驱动，它们不读取接口和端点描述符来检查接口编号或端点地址，而是使用硬编码值。因此，这类主机驱动无法以通用方式使用，也就是说，无法与不同设备控制器、不同设备配置以及其他功能组合使用。这也可能是因为该驱动是针对特定硬件设计的，并不打算用于该特定硬件的克隆产品。相反，如果驱动本身是通用的，并且应能与不同硬件变体配合工作，那么它就不能使用硬编码的接口编号和端点地址。Zephyr RTOS 中无法禁用端点重新分配，这可能会妨碍你实现硬件克隆固件。因此，如果可能，应修正主机驱动实现，使其使用接口和端点描述符中的值。

.. _testing_USB_native_sim:

在 native_sim 中通过 USBIP 测试
*******************************

可以使用通过 USBIP 实现的虚拟 USB 控制器来测试 USB 设备协议栈。按照一般构建流程为 :zephyr:board:`native_sim <native_sim>` 配置构建 USB 示例。

使用以下命令运行构建好的示例：

.. code-block:: console

   west build -t run

在终端窗口中运行以下命令以列出 USB 设备：

.. code-block:: console

   $ usbip list -r localhost
   Exportable USB devices
   ======================
    - 127.0.0.1
           1-1: unknown vendor : unknown product (2fe3:0100)
              : /sys/devices/pci0000:00/0000:00:01.2/usb1/1-1
              : (Defined at Interface level) (00/00/00)
              :  0 - Vendor Specific Class / unknown subclass / unknown protocol (ff/00/00)

在终端窗口中运行以下命令以连接 USB 设备：

.. code-block:: console

   $ sudo usbip attach -r localhost -b 1-1

USB 设备应连接到你的 Linux 主机，并使用以下命令进行验证：

.. code-block:: console

   $ sudo usbip port
   Imported USB devices
   ====================
   Port 00: <Port in Use> at Full Speed(12Mbps)
          unknown vendor : unknown product (2fe3:0100)
          7-1 -> usbip://localhost:3240/1-1
              -> remote bus/dev 001/002
   $ lsusb -d 2fe3:0100
   Bus 007 Device 004: ID 2fe3:0100

USB 厂商 ID 和产品 ID
*********************

Zephyr 项目的 USB 厂商 ID 为 ``0x2FE3``。当厂商将 Zephyr USB 设备支持集成到自己的产品中时，不得使用此 USB 厂商 ID。

每个 USB :zephyr:code-sample-category:`sample<usb>` 都有自己唯一的产品 ID。USB 维护者（如果已指定）或 Zephyr 技术指导委员会可以根据有充分理由且已记录的请求分配其他 USB 产品 ID。

当前使用的产品 ID 如下：

+------------------------------------------------------+----------+
| 示例                                                 | PID      |
+======================================================+==========+
| :zephyr:code-sample:`usb-cdc-acm`                    | 0x0001   |
+------------------------------------------------------+----------+
| 保留（以前为：usb-cdc-acm-composite）                | 0x0002   |
+------------------------------------------------------+----------+
| 保留（以前为：usb-hid-cdc）                          | 0x0003   |
+------------------------------------------------------+----------+
| :zephyr:code-sample:`usb-cdc-acm-console`            | 0x0004   |
+------------------------------------------------------+----------+
| :zephyr:code-sample:`usb-dfu` （运行时）             | 0x0005   |
+------------------------------------------------------+----------+
| 保留（以前为：usb-hid）                              | 0x0006   |
+------------------------------------------------------+----------+
| :zephyr:code-sample:`usb-hid-mouse`                  | 0x0007   |
+------------------------------------------------------+----------+
| :zephyr:code-sample:`usb-mass`                       | 0x0008   |
+------------------------------------------------------+----------+
| :zephyr:code-sample:`testusb-app`                    | 0x0009   |
+------------------------------------------------------+----------+
| :zephyr:code-sample:`webusb`                         | 0x000A   |
+------------------------------------------------------+----------+
| :zephyr:code-sample:`bluetooth_hci_usb`              | 0x000B   |
+------------------------------------------------------+----------+
| 保留（以前为：bluetooth_hci_usb_h4）                 | 0x000C   |
+------------------------------------------------------+----------+
| 保留（以前为：wpan-usb）                             | 0x000D   |
+------------------------------------------------------+----------+
| :zephyr:code-sample:`uac2-explicit-feedback`         | 0x000E   |
+------------------------------------------------------+----------+
| :zephyr:code-sample:`uac2-implicit-feedback`         | 0x000F   |
+------------------------------------------------------+----------+
| :zephyr:code-sample:`uvc`                            | 0x0011   |
+------------------------------------------------------+----------+
| :zephyr:code-sample:`usb-dfu` （DFU 模式）           | 0xFFFF   |
+------------------------------------------------------+----------+

USB 设备描述符字段 ``bcdDevice`` 表示设备发布编号，它以二进制编码十进制值表示 Zephyr 内核的主版本号和次版本号。
