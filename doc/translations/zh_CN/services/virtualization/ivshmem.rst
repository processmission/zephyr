.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _ivshmem_driver:

VM 间共享内存
#############

.. contents::
   :local:
   :depth: 2

概述
****

由于 Zephyr 可以作为客户机操作系统在 Qemu 和 `ACRN <https://projectacrn.github.io/latest/tutorials/using_zephyr_as_uos.html>`_ 上运行，因此可能需要让各 VM 相互感知，或感知主机。这可以通过一个名为 ivshmem 的功能在各参与方之间暴露共享内存来实现，ivshmem 是 inter-VM Shared Memory（VM 间共享内存）的缩写。

目前支持两种类型：普通的共享内存（ivshmem-plain），以及允许一个 VM 向另一个 VM 产生中断、从而自身也能被中断的共享内存（ivshmem-doorbell）。

更多信息请参阅官方的 `Qemu ivshmem 文档 <https://www.qemu.org/docs/master/system/devices/ivshmem.html>`_。

支持
****

Zephyr 对 plain 和 doorbell 两个版本都支持。通过启用 :kconfig:option:`CONFIG_IVSHMEM` 即可构建 Ivshmem 驱动。默认情况下会提供 plain 版本。要获得 doorbell 版本，需要启用 :kconfig:option:`CONFIG_IVSHMEM_DOORBELL`。

由于 doorbell 版本使用 MSI-X 向量来支持通知向量，因此必须将 :kconfig:option:`CONFIG_IVSHMEM_MSI_X_VECTORS` 调整为所需的向量数量。

请注意，通过启用 :kconfig:option:`CONFIG_IVSHMEM_SHELL` 可以提供一个很小的 shell 模块，用于测试 ivshmem 功能。

ivshmem-v2
**********

Zephyr 还支持 ivshmem-v2：

https://github.com/siemens/jailhouse/blob/master/Documentation/ivshmem-v2-specification.md

它主要用于 Jailhouse hypervisor 中的 IPC（例如 :zephyr:code-sample:`eth-ivshmem`）。也可以不使用 Jailhouse 而使用 ivshmem-v2：构建 Siemens 的 QEMU 分支，并修改 QEMU 的启动标志：

https://github.com/siemens/qemu/tree/wip/ivshmem2

API 参考
********

.. doxygengroup:: ivshmem
