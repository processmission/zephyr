.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _usermode_api:

用户模式
########

Zephyr 支持让线程以较低的特权级运行，我们将其称为用户模式。当前实现面向具有 MPU 硬件的设备。

有关创建在用户模式下运行的线程的详细信息，请参阅 :ref:`lifecycle_v2`。

.. toctree::
    :maxdepth: 2

    overview.rst
    memory_domain.rst
    kernelobjects.rst
    syscalls.rst
    mpu_stack_objects.rst
    mpu_userspace.rst
