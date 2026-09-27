.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bluetooth_mesh_models:

Mesh 模型
#########

基础模型
********

Bluetooth Mesh 规范定义的基础模型可供网络管理员用于配置和诊断 Mesh 节点。

.. toctree::
   :maxdepth: 1

   brg_cfg_cli
   brg_cfg_srv
   cfg_cli
   cfg_srv
   health_cli
   health_srv
   lcd_cli
   lcd_srv
   od_cli
   od_srv
   op_agg_cli
   op_agg_srv
   priv_beacon_cli
   priv_beacon_srv
   rpr_cli
   rpr_srv
   sar_cfg_cli
   sar_cfg_srv
   srpl_cli
   srpl_srv

模型规范中的模型
****************

除 Bluetooth Mesh 规范中定义的基础模型外，Bluetooth Mesh 模型规范还定义了若干模型，其中一些已在 Zephyr 中实现：

.. toctree::
   :maxdepth: 1

   blob
   dfu
