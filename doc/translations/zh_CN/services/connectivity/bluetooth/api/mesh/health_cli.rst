.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models_health_cli:

健康客户端
##########

健康客户端模型与健康服务器模型交互，以读取诊断信息并控制节点的注意状态。

健康客户端 API 中的所有消息传递函数都以 ``cli`` 作为第一个参数。它是指向本次函数调用所用客户端模型实例的指针。第二个参数是 ``ctx``，即消息上下文。消息上下文包含目标节点使用的 netkey 索引、appkey 索引和单播地址。

健康客户端模型是可选的，可以实例化在任何元素上。但是，如果将健康客户端模型实例化在非主元素上，则主元素上还必须存在一个实例。

有关规范定义的故障值列表，请参见 :ref:`bluetooth_mesh_health_faults`。

API 参考
********

.. doxygengroup:: bt_mesh_health_cli
