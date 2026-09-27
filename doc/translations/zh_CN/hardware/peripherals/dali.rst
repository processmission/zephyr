.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _dali_api:

DALI
####

DALI 即数字可寻址照明接口，是一种用于专业照明解决方案的通信标准。此 API 尚不稳定，可能会发生变化。

基本操作
********

DALI 标准采用基于总线系统交换帧的通信模型。帧由采用曼彻斯特编码的数据组成，并以停止条件结束。DALI 标准对发送器和接收器的行为有具体要求。

配置选项
********

相关配置选项：

* :kconfig:option:`CONFIG_DALI`
* :kconfig:option:`CONFIG_DALI_PWM`


API 参考
********

.. doxygengroup:: dali_interface
