.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _pm-device-runtime:

设备运行时电源管理
##################

简介
****

设备运行时电源管理（PM）框架是一种主动式电源管理机制，它通过独立于系统状态地挂起空闲或未使用的设备来降低系统整体功耗。可以通过设置 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME` 来启用它。在这种模型中，设备驱动负责表明何时需要该设备、何时不需要。系统据此并基于使用计数决定何时挂起或恢复设备。

在设备上启用设备运行时电源管理后，其状态最初会被设为 :c:enumerator:`PM_DEVICE_STATE_SUSPENDED`，表示该设备未被使用。首次请求该设备时，设备会被恢复，从而进入 :c:enumerator:`PM_DEVICE_STATE_ACTIVE` 状态。设备将一直保持此状态，直到不再被使用。此时设备会被挂起，直到下一次请求。如果挂起是同步执行的，设备会立即进入 :c:enumerator:`PM_DEVICE_STATE_SUSPENDED` 状态；如果挂起是异步执行的，设备会先进入 :c:enumerator:`PM_DEVICE_STATE_SUSPENDING` 状态，并在该动作执行后进入 :c:enumerator:`PM_DEVICE_STATE_SUSPENDED` 状态。

对于位于电源域上的设备（通过 devicetree 的 'power-domains' 属性指定），设备运行时电源管理会在对子设备调用 :c:func:`pm_device_runtime_get` 和 :c:func:`pm_device_runtime_put` 时自动尝试申请和释放所依赖的域。

要让上述机制自动控制电源域状态，必须在电源域设备上启用设备运行时 PM。要在全局启用设备运行时 PM，请启用 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_DEFAULT_ENABLE`。要仅为部分设备启用设备运行时 PM，请设置 ``zephyr,pm-device-runtime-auto`` devicetree 属性，或对这些设备使用 :c:func:`pm_device_runtime_enable`。

.. graphviz::
   :caption: 设备状态与状态转换

    digraph {
        node [shape=box];
        init [shape=point];

        SUSPENDED [label=PM_DEVICE_STATE_SUSPENDED];
        ACTIVE [label=PM_DEVICE_STATE_ACTIVE];
        SUSPENDING [label=PM_DEVICE_STATE_SUSPENDING];

        init -> SUSPENDED;
        SUSPENDED -> ACTIVE;
        ACTIVE -> SUSPENDED;
        ACTIVE -> SUSPENDING [constraint=false]
        SUSPENDING -> SUSPENDED [constraint=false];
        SUSPENDED -> SUSPENDING [style=invis];
        SUSPENDING -> ACTIVE [style=invis];
    }

设备运行时电源管理框架的设计目标是以最少的应用工作量来降低设备功耗。设备驱动负责表明何时需要设备处于可工作状态、何时不需要。因此，应用不能手动挂起或恢复设备。不过，应用可以决定何时为某个设备禁用或启用运行时电源管理。例如，当应用希望某个设备始终保持活动状态时，这就很有用。

设计原则
********

在设备上启用运行时 PM 后，系统电源状态转换期间不再对该设备执行恢复或挂起操作。设备完全负责表明何时需要该设备、何时不需要。设备运行时 PM API 使用引用计数来跟踪设备的使用情况，从而判断何时需要恢复或挂起设备。该 API 使用 *get* 和 *put* 两个术语分别表示需要或不需要设备。在考虑设备依赖关系时，这一机制十分关键。例如，如果某个总线设备被多个传感器使用，我们可以让总线保持活动状态，直到最后一个传感器使用完毕。

.. note::

    目前，设备运行时电源管理 API 不管理设备之间的依赖关系。这实际上意味着，如果某个设备依赖其他设备才能工作（例如传感器可能依赖总线设备），那么每次事务都会恢复和挂起该总线。一般来说，在子设备被使用时让父设备保持活动状态更高效，因为子设备可能会在短时间内执行多次事务。在此功能加入之前，设备可以手动 *get* 或 *put* 其依赖的设备。

设备驱动可以使用 :c:func:`pm_device_runtime_get` 函数表明它 *需要* 设备处于活动或可工作状态。该函数会增加设备的使用计数，并在必要时恢复设备。类似地，可以使用 :c:func:`pm_device_runtime_put` 函数表明不再需要该设备。该函数会减少设备的使用计数，并在必要时挂起设备。需要注意的是，这两种情况下操作都是同步执行的。下面的时序图展示了设备如何使用该 API 以及预期的事件顺序。

.. figure:: images/devr-sync-ops.svg

    单个设备上的同步操作

同步模型是最简单的模型。但它可能引入不必要的延迟，因为应用要等到设备被挂起（在设备不再被使用时）才能得到操作结果。如果操作很快，例如翻转一个寄存器，这通常不成问题。但如果挂起需要通过较慢的总线发送数据包，情况就不同了。因此，设备驱动也可以使用 :c:func:`pm_device_runtime_put_async` 函数。同样地，该函数会在设备不再被使用时安排挂起操作。


默认情况下，运行时 PM 操作会交给系统工作队列执行。但设备驱动不得在挂起过程中执行任何阻塞操作，因为这会阻塞系统工作队列，降低系统响应能力。

为解决此问题，应用可以通过启用 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_USE_DEDICATED_WQ` 把运行时 PM 配置为使用专用的工作队列。

如果需要阻塞行为，例如访问较慢的外设或等待总线事务，则必须改用 PM 子系统的工作队列。需要这种行为的驱动可以通过启用 :kconfig:option:`CONFIG_PM_DEVICE_DRIVER_NEEDS_DEDICATED_WQ` 显式请求该行为。

对于不需要异步操作且资源受限的目标，可以通过取消选择 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_ASYNC` 完全禁用此功能，从而减少内存占用并降低系统复杂度。


.. figure:: images/devr-async-ops.svg

    单个设备上的异步操作

实现准则
********

首先，设备驱动需要实现 PM 子系统用于挂起或恢复设备的 PM 动作回调。

.. code-block:: c

    static int mydev_pm_action(const struct device *dev,
                               enum pm_device_action action)
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
        default:
            return -ENOTSUP;
        }

        return 0;
    }

PM 子系统会串行化对 PM 动作回调的调用，因此不需要额外的同步。

要在设备上启用设备运行时电源管理，驱动需要在初始化时调用 :c:func:`pm_device_runtime_enable`。注意，如果设备的状态是 :c:enumerator:`PM_DEVICE_STATE_ACTIVE`，该函数会挂起设备。如果设备在物理上已处于挂起状态，初始化函数应在调用 :c:func:`pm_device_runtime_enable` 之前调用 :c:func:`pm_device_init_suspended`。

.. code-block:: c

    /* device driver initialization function */
    static int mydev_init(const struct device *dev)
    {
        int ret;
        ...

        /* OPTIONAL: mark device as suspended if it is physically suspended */
        pm_device_init_suspended(dev);

        /* enable device runtime power management */
        ret = pm_device_runtime_enable(dev);
        if (ret < 0) {
            return ret;
        }
    }

也可以通过在与设备对应的 devicetree 节点上添加 ``zephyr,pm-device-runtime-auto`` 标志，自动为设备实例启用设备运行时电源管理。启用后，在设备的 ``init`` 函数执行并成功返回之后会立即调用 :c:func:`pm_device_runtime_enable`。

.. code-block:: dts

    foo {
        /* ... */
        zephyr,pm-device-runtime-auto;
    };

假设有一个实现了 ``operation`` API 调用的设备驱动，其 *get* 和 *put* 操作可以实现如下：

.. code-block:: c

    static int mydev_operation(const struct device *dev)
    {
        int ret;

        /* "get" device (increases usage count, resumes device if suspended) */
        ret = pm_device_runtime_get(dev);
        if (ret < 0) {
            return ret;
        }

        /* do something with the device */
        ...

        /* "put" device (decreases usage count, suspends device if no more users) */
        return pm_device_runtime_put(dev);
    }

如果挂起操作 *很慢*，设备驱动可以使用异步 API：

.. code-block:: c

    static int mydev_operation(const struct device *dev)
    {
        int ret;

        /* "get" device (increases usage count, resumes device if suspended) */
        ret = pm_device_runtime_get(dev);
        if (ret < 0) {
            return ret;
        }

        /* do something with the device */
        ...

        /* "put" device (decreases usage count, schedule suspend if no more users) */
        return pm_device_runtime_put_async(dev, K_NO_WAIT);
    }

示例
****

以下示例展示了设备运行时电源管理的用法：

* :zephyr_file:`tests/subsys/pm/device_runtime_api/`
* :zephyr_file:`tests/subsys/pm/device_power_domains/`
* :zephyr_file:`tests/subsys/pm/power_domain/`
