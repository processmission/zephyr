.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _wuc_api:

唤醒控制器（WUC）
#################

概述
****

唤醒控制器（WUC）API 提供了一个通用接口，用于启用和管理可使系统退出低功耗状态的唤醒源。WUC 设备通常在 Devicetree 中描述，并由客户端通过 :c:struct:`wuc_dt_spec` 引用。

Devicetree 配置
***************

客户端节点通过 ``wakeup-ctrls`` 属性引用唤醒控制器。该属性包含指向 WUC 设备的 phandle 和唤醒源标识符。

Devicetree 片段示例：

.. code-block:: devicetree

   wuc0: wakeup-controller@40000000 {
       compatible = "nxp,mcx-wuc";
       reg = <0x40000000 0x1000>;
       #wakeup-ctrl-cells = <1>;
   };

   button0: button@0 {
       wakeup-ctrls = <&wuc0 10>;
   };

基本操作
********

应用通常使用 :c:macro:`WUC_DT_SPEC_GET` 获取 :c:struct:`wuc_dt_spec` ，然后根据需要启用或禁用唤醒源。

.. code-block:: c
   :caption: 启用 Devicetree 中定义的唤醒源

   #define BUTTON0_NODE DT_NODELABEL(button0)

   static const struct wuc_dt_spec button_wuc =
       WUC_DT_SPEC_GET(BUTTON0_NODE);

   if (!device_is_ready(button_wuc.dev)) {
       return -ENODEV;
   }

   return wuc_enable_wakeup_source_dt(&button_wuc);

如果驱动支持，应用可以检查和清除唤醒源的触发状态。如果未实现此功能，相关 API 将返回 ``-ENOSYS`` 。

.. code-block:: c
   :caption: 检查和清除唤醒源的触发状态

   int ret;

   ret = wuc_check_wakeup_source_triggered_dt(&button_wuc);
   if (ret > 0) {
       (void)wuc_clear_wakeup_source_triggered_dt(&button_wuc);
   }

API 参考
********

.. doxygengroup:: wuc_interface
