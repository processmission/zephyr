.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _promiscuous_interface:

混杂模式
########

.. contents::
    :local:
    :depth: 2

概述
****

混杂模式是网络接口控制器的一种模式，它会将接收到的所有流量都传递给应用，而不是只传递控制器被专门编程接收的帧。该模式通常用于数据包嗅探，通过向应用展示网络上传输的所有数据来诊断网络连接问题。（更多信息见 `Wikipedia article on promiscuous mode <https://en.wikipedia.org/wiki/Promiscuous_mode>`_。）

网络混杂 API 用于启用和禁用该模式，以及等待并接收到达的网络数据。并非所有网络技术或网络设备驱动都支持混杂模式。

用法示例
********

首先，应用需要像这样打开混杂模式：

.. code-block:: c

        ret = net_promisc_mode_on(iface);
        if (ret < 0) {
                if (ret == -EALREADY) {
                        printf("Promiscuous mode already enabled\n");
                } else {
                        printf("Cannot enable promiscuous mode for "
                               "interface %p (%d)\n", iface, ret);
                }
        }


如果没有错误，应用就可以开始等待网络数据：

.. code-block:: c

        while (true) {
                pkt = net_promisc_mode_wait_data(K_FOREVER);
                if (pkt) {
                        print_info(pkt);
                }

                net_pkt_unref(pkt);
        }


最后，应用可以像这样关闭混杂模式：

.. code-block:: c

        ret = net_promisc_mode_off(iface);
        if (ret < 0) {
                if (ret == -EALREADY) {
                        printf("Promiscuous mode already disabled\n");
                } else {
                        printf("Cannot disable promiscuous mode for "
                               "interface %p (%d)\n", iface, ret);
                }
        }


更完整的示例见 :zephyr:code-sample:`net-promiscuous-mode`。


API 参考
********

.. doxygengroup:: promiscuous
