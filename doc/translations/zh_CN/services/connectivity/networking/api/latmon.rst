.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _latmon:

Latmon 网络服务
###############

.. contents::
    :local:
    :depth: 2

概述
****

提供基于网络的时延监测所需的功能，包括 socket 管理、客户端-服务器通信，以及与运行在被测系统（System Under Test，SUT）上的 Latmus 服务进行数据交换。

Latmon 网络服务负责在 Latmon 应用（运行于基于 Zephyr 的开发板）与 Latmus 服务（运行于被测系统）之间建立并管理网络通信。

它使用 TCP socket 进行可靠通信，并使用 UDP socket 广播 Latmon 设备的 IP 地址。

API 参考
********

.. doxygengroup:: latmon

功能
****

- **Socket 管理**：创建并管理用于通信的 TCP 和 UDP socket。
- **客户端-服务器通信**：处理来自 Latmus 服务的传入连接。
- **数据交换**：向 Latmus 服务发送时延指标和直方图数据。
- **IP 地址广播**：广播 Latmon 设备的 IP 地址，以便 Latmus 服务发现该设备。
- **线程安全设计**：使用 Zephyr 内核原语（例如消息队列和信号量）进行同步。

工作流
******

Socket 创建
===========

调用 :c:func:`net_latmon_get_socket()` 函数创建并配置用于与 Latmus 服务通信的 TCP socket。可以将连接地址作为参数传入，以便将 socket 绑定到特定接口和端口。

连接处理
========

:c:func:`net_latmon_connect()` 函数等待来自 Latmus 服务的连接。如果在超时时间内未收到连接，该服务将使用 UDP 广播其 IP 地址并返回 ``-EAGAIN``。如果无法发送广播请求，该函数将返回 ``-1``，此时客户端应退出。

启动监测
========

建立连接后，调用 :c:func:`net_latmon_start()` 函数以启动监测过程。该函数使用回调计算时延差值，并将数据发送到 Latmus 服务。

监测状态
========

可以使用 :c:func:`net_latmon_running()` 函数检查监测过程是否处于活动状态。

线程管理
========

该服务使用 Zephyr 线程处理传入连接并管理监测过程。

启用 Latmon 服务
****************

必须在 :file:`prj.conf` 文件中启用以下配置选项。

- :kconfig:option:`CONFIG_NET_LATMON`

可以配置以下选项来自定义 Latmon 服务：

- :kconfig:option:`CONFIG_NET_LATMON_PORT` - Latmon 服务的端口号。
- :kconfig:option:`CONFIG_NET_LATMON_XFER_THREAD_STACK_SIZE`
- :kconfig:option:`CONFIG_NET_LATMON_XFER_THREAD_PRIORITY`
- :kconfig:option:`CONFIG_NET_LATMON_THREAD_STACK_SIZE`
- :kconfig:option:`CONFIG_NET_LATMON_THREAD_PRIORITY`
- :kconfig:option:`CONFIG_NET_LATMON_MONITOR_THREAD_STACK_SIZE`
- :kconfig:option:`CONFIG_NET_LATMON_MONITOR_THREAD_PRIORITY`

示例用法
********

.. code-block:: c

    #include <zephyr/net/latmon.h>
    #include <zephyr/net/socket.h>

    void main(void)
    {
        struct in_addr ip;
        int server_socket, client_socket;

        /* Create and configure the server socket */
        server_socket = net_latmon_get_socket(NULL);

        while (1) {
            /* Wait for a connection from the Latmus service */
            client_socket = net_latmon_connect(server_socket, &ip);
            if (client_socket < 0) {
                if (client_socket == -EAGAIN) {
                    continue;
                }
                goto out;
            }

            /* Start the latency monitoring process */
            net_latmon_start(client_socket, measure_latency_cycles);
        }
    out:
        close(server_socket);
    }
