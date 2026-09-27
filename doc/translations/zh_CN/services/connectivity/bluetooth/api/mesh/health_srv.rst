.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models_health_srv:

健康服务器
##########

健康服务器模型为 :ref:`bluetooth_mesh_models_health_cli` 模型提供注意回调和节点诊断。它主要用于报告 Mesh 节点中的故障，并将 Mesh 节点映射到其物理位置。

如果存在，健康服务器模型必须实例化在主元素上。

故障
****

健康服务器模型可以报告设备生命周期内发生过的故障列表。通常，故障是可能改变节点行为的事件或状况，例如断电或外设故障。故障分为警告和错误。警告表示接近节点设计承受极限的状况，但不一定对设备造成损坏。错误表示超出节点设计极限的状况，可能已导致无效行为或对设备造成永久损坏。

故障值 ``0x01`` 到 ``0x7f`` 保留给 Bluetooth Mesh 规范使用，规范定义的完整故障列表参见 :ref:`bluetooth_mesh_health_faults`。故障值 ``0x80`` 到 ``0xff`` 是厂商特定的。报告故障列表时始终会附带公司 ID，以帮助解释厂商特定的故障。

.. _bluetooth_mesh_models_health_srv_attention:

注意状态
********

注意状态用于让设备通过某种物理行为（例如闪烁、发出声音或振动）引起注意。注意状态可以在配网期间使用，让用户知道他们正在为哪个设备配网，也可以在运行时通过健康模型使用。

启用注意状态时，始终会为其分配一个 1 到 255 秒范围内的超时。健康服务器 API 提供两个回调供应用执行其引起注意的行为：在注意期开始时调用 :c:member:`bt_mesh_health_srv_cb.attn_on`，在结束时调用 :c:member:`bt_mesh_health_srv_cb.attn_off`。

注意期的剩余时间可以通过 :c:member:`bt_mesh_health_srv.attn_timer` 查询。

API 参考
********

.. doxygengroup:: bt_mesh_health_srv

.. _bluetooth_mesh_health_faults:

健康故障
========

Bluetooth Mesh 规范定义的故障值。

.. doxygengroup:: bt_mesh_health_faults
