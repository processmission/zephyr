.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mpu_userspace:

基于 MPU 的用户空间
###################

基于 MPU 的用户空间实现需要额外创建一组栈。这些栈与系统中定义的各个线程栈一一对应。特权栈在构建过程中创建。

构建后脚本 :ref:`gen_kobject_list.py` 会扫描生成的 ELF 文件，找到所有线程栈对象，随后创建一组特权栈、一个查找表和一组辅助函数，并将其加入映像。

在线程降级到用户模式的过程中，会填入特权栈信息。随后，线程切换和系统调用基础设施使用这些信息，为线程栈及其保护区（如适用）正确配置 MPU 区域。

执行系统调用时，会验证用户模式线程对该系统调用的访问权限以及所有传入参数。然后将线程提升到特权模式，将栈切换为特权栈，并调用指定的内核 API。从内核 API 返回后，线程恢复为用户模式，栈也恢复为用户栈。
