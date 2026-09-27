.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _pm-power-domain:

电源域
######

简介
****

Zephyr 电源域抽象旨在支持由同一电源供电的一组设备，以通用的方式接收电源状态变化的通知。使用设备 A 的应用代码无需知道设备 B 位于同一个电源域，也无需知道设备 B 也应被配置为低功耗状态。

Zephyr 中的电源域是可选的，要启用此功能必须设置 :kconfig:option:`CONFIG_PM_DEVICE_POWER_DOMAIN` 选项。

当电源域自身开启或关闭时，电源域负责通知使用它的所有设备，即分别以 :c:enumerator:`PM_DEVICE_ACTION_TURN_ON` 或 :c:enumerator:`PM_DEVICE_ACTION_TURN_OFF` 调用这些设备的电源管理回调。下图展示了这一工作流程。

.. _pm-domain-work-flow:

.. graphviz::
   :caption: 电源域工作流程

   digraph {
       rankdir="TB";

       action [style=invis]
       {
           rank = same;
           rankdir="LR"
           devA [label="gpio0"]
           devB [label="gpio1"]
       }
       domain [label="gpio_domain"]

      action -> devA [label="pm_device_runtime_get()"]
      devA:se -> domain:n [label="pm_device_runtime_get()"]

      domain -> devB [label="action_cb(PM_DEVICE_ACTION_TURN_ON)"]
      domain:sw -> devA:sw [label="action_cb(PM_DEVICE_ACTION_TURN_ON)"]
   }

内部电源域
----------

SoC 中的大多数设备都有独立的电源控制，可以通过开关来降低功耗。但仍有大量静态漏电流无法仅靠设备电源管理来控制。为了解决这个问题，SoC 通常被划分为若干个区域，把通常一起使用的设备归为一组，这样就可以完全关闭未使用的区域以消除漏电流。这些区域称为“电源域”，可以按层级组织，也可以嵌套。

外部电源域
----------

SoC 外部的设备可能由 SoC 主电源之外的电源供电。这些外部电源通常是开关、稳压器或专用电源 IC。多个设备可以由同一个电源供电，这种设备组合通常称为“电源域”。

把设备放到电源域中可以出于多种原因，例如让低功耗模式下功耗较高的设备在不使用时可以被完全关闭。

实现准则
********

首先，充当电源域的设备需要声明兼容 ``power-domain``。以 :ref:`pm-domain-work-flow` 为例，下面的代码定义了一个名为 ``gpio_domain`` 的域。

.. code-block:: devicetree

        gpio_domain: gpio_domain@4 {
                compatible = "power-domain";
                ...
        };

电源域需要实现 PM 子系统用于开启和关闭设备的 PM 动作回调。

.. code-block:: c

    static int mydomain_pm_action(const struct device *dev,
                               enum pm_device_action action)
    {
        switch (action) {
        case PM_DEVICE_ACTION_RESUME:
            /* resume the domain */
            ...
            /* notify children domain is now powered */
            pm_device_children_action_run(dev, PM_DEVICE_ACTION_TURN_ON, NULL);
            break;
        case PM_DEVICE_ACTION_SUSPEND:
            /* notify children domain is going down */
            pm_device_children_action_run(dev, PM_DEVICE_ACTION_TURN_OFF, NULL);
            /* suspend the domain */
            ...
            break;
        case PM_DEVICE_ACTION_TURN_ON:
            /* turn on the domain (e.g. setup control pins to disabled) */
            ...
            break;
        case PM_DEVICE_ACTION_TURN_OFF:
            /* turn off the domain (e.g. reset control pins to default state) */
            ...
            break;
        default:
            return -ENOTSUP;
        }

        return 0;
    }

属于该域的设备可以通过在 ``power-domain`` 节点的属性中引用它来声明。下面的示例声明了属于域 ``gpio_domain`` 的设备 ``gpio0`` 和 ``gpio1``。

.. code-block:: devicetree

        &gpio0 {
                compatible = "zephyr,gpio-emul";
                gpio-controller;
                power-domains = <&gpio_domain>;
        };

        &gpio1 {
                compatible = "zephyr,gpio-emul";
                gpio-controller;
                power-domains = <&gpio_domain>;
        };

当域的状态发生变化时，域下的所有设备都会收到通知。这些通知以动作的形式在设备 PM 动作回调中发送，设备可以利用它们完成所需的额外工作，不过也可以安全地忽略。

.. code-block:: c

    static int mydev_pm_action(const struct device *dev,
                               enum pm_device_action *action)
    {
        switch (action) {
        case PM_DEVICE_ACTION_SUSPEND:
            /* suspend the device */
            ...
            break;
        case PM_DEVICE_ACTION_RESUME:
            /* resume the device */
            ...
            break;
        case PM_DEVICE_ACTION_TURN_ON:
            /* configure the device into low power mode */
            ...
            break;
        case PM_DEVICE_ACTION_TURN_OFF:
            /* prepare the device for power down */
            ...
            break;
        default:
            return -ENOTSUP;
        }

        return 0;
    }

.. note::

   如果依赖某个域的设备被用作“唤醒”源，则驱动或应用有责任把该域也设置为“唤醒”源。

示例
****

以下示例展示了电源域功能的一些用法：

* :zephyr_file:`tests/subsys/pm/device_power_domains/`
* :zephyr_file:`tests/subsys/pm/power_domain/`
