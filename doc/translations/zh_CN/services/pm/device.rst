.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

设备电源管理
############

简介
****

Zephyr 中的设备电源管理特性提供了相应机制，可以协调一致地影响对设备驱动所需执行的电源管理动作的控制。这种控制基于系统任何组件都可以设定的明确预期，也基于设备之间可能存在的电源相关依赖关系。

Zephyr 支持两种设备电源管理方法：

 - :ref:`设备运行时电源管理 <pm-device-runtime-pm>`
 - :ref:`系统管理的设备电源管理 <pm-device-system-pm>`

.. _pm-device-runtime-pm:

设备运行时电源管理
==================

设备运行时电源管理涉及设备驱动、子系统和应用之间的协同交互。虽然设备驱动在直接控制设备电源状态方面起着关键作用，但挂起或恢复设备的决定也可能受到软件栈更高层的影响。

每一层（设备驱动、子系统和应用）都可以独立工作，无需了解其他层的具体细节，因为子系统使用引用计数来判断何时需要挂起或恢复设备。

- **设备驱动** 负责管理设备的电源状态。它们直接与硬件交互，在设备不使用时把设备置入低功耗状态（挂起），并在需要时把设备恢复运行。驱动应使用 Zephyr 提供的 :ref:`设备运行时电源管理 API <device_runtime_apis>` 来控制设备的电源状态。

- **子系统** （例如传感器、文件系统和网络）也会影响设备电源管理。子系统可能更了解系统整体状态和工作负载，因此能够就在何时挂起或恢复设备做出明智的决策。例如，如果网络子系统预计近期会有网络活动，它可以决定让网络接口保持上电。

- 在 Zephyr 上运行的 **应用** 也会影响设备电源管理。应用可能对设备使用和功耗有特定要求。例如，通过网络传输流式数据的应用可能需要让网络接口持续上电。

设备驱动、子系统和应用之间的协调是高效设备电源管理的关键。例如，设备驱动可能不知道子系统将执行一系列需要设备保持上电的连续操作。在这种情况下，子系统可以使用设备运行时电源管理来确保设备在操作完成之前保持活动状态。

使用这种设备运行时电源管理时，系统电源管理子系统能够快速改变电源状态，因为它无需花时间挂起和恢复已启用运行时电源管理的设备。

更多信息请参见 :ref:`pm-device-runtime`。

.. _pm-device-system-pm:

系统管理的设备电源管理
======================

系统管理的设备电源管理（PM）框架是一种让设备随系统进入 CPU（或 SoC）电源状态而一起挂起的方法。可以通过设置 :kconfig:option:`CONFIG_PM_DEVICE_SYSTEM_MANAGED` 来启用它。使用这种方法时，设备电源管理主要在 :c:func:`pm_system_suspend()` 内完成。

如果决定进入 CPU 低功耗状态，电源管理子系统会检查所选的低功耗状态是否会触发设备电源管理，然后在改变状态之前挂起设备。子系统按照设备的初始化顺序挂起设备，确保满足设备之间可能的依赖关系。CPU 从睡眠状态唤醒后，设备会按与挂起相反的顺序被恢复。

进入低功耗状态时是否挂起设备，取决于该状态以及它是否设置了 ``zephyr,pm-device-disabled`` 属性。下面是一个目标的示例，它有两个低功耗状态，其中只有一个会触发设备电源管理：

.. code-block:: devicetree

   /* Node in a DTS file */
   cpus {
        power-states {
                state0: state0 {
                        compatible = "zephyr,power-state";
                        power-state-name = "standby";
                        min-residency-us = <5000>;
                        exit-latency-us = <240>;
                        zephyr,pm-device-disabled;
                };
                state1: state1 {
                        compatible = "zephyr,power-state";
                        power-state-name = "suspend-to-ram";
                        min-residency-us = <8000>;
                        exit-latency-us = <360>;
                };
        };
   };

.. note::

   使用 :ref:`pm-system` 时，设备状态转换可以在空闲线程中运行。由于该上下文中的函数不能阻塞，打算使用阻塞 API 的状态转换 **必须** 用 :c:func:`k_can_yield` 检查是否可以这样做。

这种设备电源管理方法在以下场景中很有用：

- 系统中没有设备在挂起和恢复时需要执行阻塞操作。这种实现比设备运行时电源管理简单得多。
- 适用于无法自行做出任何电源管理决策、必须始终保持活动的设备。例如由外部实体（如主机 CPU）控制的 Zephyr 固件。在这种场景下，有些设备必须始终保持活动，并应在此外部实体要求时随 SoC 一起挂起。

需要强调的是，这种方法有缺点（见上文），而 :ref:`设备运行时电源管理 <pm-device-runtime-pm>` 才是实现设备电源管理的 **首选** 方法。

.. note::

    使用这种设备电源管理方法时，如果某个设备无法被挂起，CPU 就不会进入低功耗状态。例如，设备针对 ``PM_DEVICE_ACTION_SUSPEND`` 动作返回 ``-EBUSY`` 之类的错误，表示它正处于无法中断的事务中间。另一种阻止 CPU 进入低功耗状态的情况是：设置了 :kconfig:option:`CONFIG_PM_NEED_ALL_DEVICES_IDLE` 选项且某个设备被标记为忙。

.. note::

   只有当最后一个活动内核进入低功耗状态时设备才会被挂起，而设备由第一个变为活动的内核恢复。

设备电源管理状态
****************

电源管理子系统在 :c:enum:`pm_device_state` 中定义设备状态。该机制用于跟踪特定设备的电源状态。需要强调的是，虽然状态由子系统跟踪，但处理改变设备状态的动作（:c:enum:`pm_device_action`）是每个设备驱动的职责。

设备驱动在内部实现 :c:func:`pm_device_action_cb_t` 钩子，该钩子接收供设备驱动处理的 :c:enum:`pm_device_action`。如果选择了 :kconfig:option:`CONFIG_PM_DEVICE` 选项，设备驱动对这些钩子的实现就会暴露给 PM 子系统，从而可以启用设备的运行时电源管理。

:c:enum:`pm_device_action` 动作与 :c:enum:`pm_device_state` 状态之间存在直接且明确的对应关系：

.. graphviz::
   :caption: 设备动作与状态对照

    digraph {
        node [shape=circle];
        rankdir=LR;
        subgraph {

            SUSPENDED [label=PM_DEVICE_STATE_SUSPENDED];
            SUSPENDING [label=PM_DEVICE_STATE_SUSPENDING];
            ACTIVE [label=PM_DEVICE_STATE_ACTIVE];
            OFF [label=PM_DEVICE_STATE_OFF];

            ACTIVE -> SUSPENDING;
            SUSPENDING -> ACTIVE;
            SUSPENDING -> SUSPENDED ["label"="PM_DEVICE_ACTION_SUSPEND"];

            ACTIVE -> SUSPENDED ["label"="PM_DEVICE_ACTION_SUSPEND"];
            SUSPENDED -> ACTIVE ["label"="PM_DEVICE_ACTION_RESUME"];

            {rank = same; SUSPENDED; SUSPENDING;}

            OFF -> SUSPENDED ["label"="PM_DEVICE_ACTION_TURN_ON"];
            SUSPENDED -> OFF ["label"="PM_DEVICE_ACTION_TURN_OFF"];
        }
    }

如前所述，设备驱动不会直接在这些状态之间切换，这完全由电源管理子系统完成。驱动的职责是实现处理状态变化所需的任何硬件相关操作。

支持设备电源管理的设备模型
**************************

驱动使用宏来初始化设备。这些宏的用法详见 :ref:`device_model_api`。实现设备电源管理支持的驱动必须为这些宏提供能描述其电源管理实现的参数。

使用 :c:macro:`PM_DEVICE_DEFINE` 或 :c:macro:`PM_DEVICE_DT_DEFINE` 来定义驱动所需的电源管理资源。这些宏会分配电源管理子系统所需的驱动专属上下文。

驱动可以使用 :c:macro:`PM_DEVICE_GET` 或 :c:macro:`PM_DEVICE_DT_GET` 获取指向该上下文的指针。这些指针应传给 ``DEVICE_DEFINE`` 或 ``DEVICE_DT_DEFINE``，以初始化每个 :c:struct:`device` 中的电源管理字段。

下面的示例代码展示了如何在设备驱动中实现设备电源管理支持。请注意，为简洁起见这里显式忽略了返回值，在真实驱动中必须处理它们。

.. code-block:: c

   #include <zephyr/pm/device.h>
   #include <zephyr/pm/device_runtime.h>

   #define DT_DRV_COMPAT dummy_device

   struct dummy_driver_data {
           struct gpio_callback int_pin_callback;
           const struct device *dev;
   };

   struct dummy_driver_config {
           const struct device *bus;
           const struct gpio_dt_spec int_gpio;
           const struct gpio_dt_spec enable_pin;
   };

   static void dummy_driver_int_pin_handler(const struct device *dev,
                                            struct gpio_callback *cb,
                                            uint32_t pins)
   {
           struct dummy_driver_data *dev_data =
                   CONTAINER_OF(cb, struct dummy_driver_data, int_pin_callback);
           const struct device *dev = dev_data->dev;
           const struct dummy_driver_config *dev_config = dev->config;

           /* ... */
   }

   static int dummy_driver_pm_suspend(const struct device *dev)
   {
           struct dummy_driver_data *dev_data = dev->data;
           const struct dummy_driver_config *config = dev->config;

           /* Request devices needed by device */
           (void)pm_device_runtime_get(config->enable_pin.port);

           /* Disable and remove interrupt pin interrupt */
           (void)gpio_pin_interrupt_configure_dt(&config->int_gpio, GPIO_INT_DISABLED);
           (void)gpio_remove_callback(config->int_pin.port, &data->int_pin_callback);

           /* Disable the device. In this case, we use the enable pin */
           (void)gpio_pin_set_dt(&config->enable_pin, 0);

           /* Release devices currently not needed by device */
           (void)pm_device_runtime_put(config->enable_pin.port);
           (void)pm_device_runtime_put(config->int_pin.port);

           /*
            * Note that we now have suspended the device and released all the
            * devices this device depends on. We are ready for the power
            * domain being suspended, the device being resumed again, or the
            * device driver being deinitialized.
            */

           return 0;
   }

   static int dummy_driver_pm_resume(const struct device *dev)
   {
           struct dummy_driver_data *dev_data = dev->data;
           const struct dummy_driver_config *config = dev->config;

           /* Request devices needed by device */
           (void)pm_device_runtime_get(config->enable_pin.port);
           (void)pm_device_runtime_get(config->int_pin.port);
           (void)pm_device_runtime_get(config->bus);

           /* Enable the device. In this case, we use the enable pin */
           (void)gpio_pin_set_dt(&config->enable_pin, 1);

           /*
            * Write initial commands to device, in this case configuring
            * the device's interrupt output pin using the bus
            */

           /* ... */

           /* Add and enable interrupt pin interrupt */
           (void)gpio_add_callback(config->int_pin.port, &data->int_pin_callback);
           (void)gpio_pin_interrupt_configure_dt(&config->int_gpio, GPIO_INT_EDGE_TO_ACTIVE);

           /*
            * Release devices currently not needed by device. In this case, we
            * are releasing the bus and the enable pin.
            *
            * The device driver would keep the bus ACTIVE while the device is
            * ACTIVE in cases of high throughput or unsolicitet data on the
            * bus, to avoid inefficient RESUME/SUSPEND cycles of the bus
            * for every transaction, and allowing reception of unsolicited
            * data on buses like UART.
            */
           (void)pm_device_runtime_put(config->bus);
           (void)pm_device_runtime_put(config->enable_pin.port);

           /*
            * Note that the interrupt pin's port is kept resumed as it
            * it needs to service the GPIO interrupt we enabled.
            */

           return 0;
   }

   static int dummy_driver_pm_turn_off(const struct device *dev)
   {
           const struct dummy_driver_config *config = dev->config;

           /* Request devices needed for configuring device */
           (void)pm_device_runtime_get(config->enable_pin.port);

           /*
            * We prepare the device for being powered off. In this case, we
            * have an active low enable pin, which could back power the device
            * once the power domain is suspended, so we configure it as
            * disconnected if supported, input otherwise.
            */
           if (gpio_pin_configure_dt(&config->enable_pin, GPIO_DISCONNECTED)) {
                   (void)gpio_pin_configure_dt(&config->enable_pin, GPIO_INPUT);
           }

           /* Release devices needed for configuring device */
           (void)pm_device_runtime_put(config->enable_pin.port);

           /*
            * We have now prepared the device for being powered off and have
            * released all the devices this device depends on. We assume that
            * the enable pin will retain its configuration, even as we have
            * released the enable pin's port.
            */

            return 0;
   }

   static int dummy_driver_pm_turn_on(const struct device *dev)
   {
           const struct dummy_driver_config *config = dev->config;

           /* Request devices needed for configuring device */
           (void)pm_device_runtime_get(config->enable_pin.port);
           (void)pm_device_runtime_get(config->int_gpio.port);

           /*
            * We ensure the device is suspended, and if possible in its reset
            * state. In this case we are using an enable pin, for other devices
            * we may need to reset them by toggling a reset pin, using an SoC
            * reset controller, or writing a reset command to them using their
            * bus.
            */
           (void)gpio_pin_configure_dt(&config->enable_pin, GPIO_OUTPUT_INACTIVE);

           /* We configure pins for suspended */
           (void)gpio_pin_configure_dt(&config->int_gpio, GPIO_INPUT);

           /* Release devices needed for configuring device */
           (void)pm_device_runtime_put(config->int_gpio.port);
           (void)pm_device_runtime_put(config->enable_pin.port);

           return 0;
   }

   static int dummy_driver_pm_action(const struct device *dev,
                                     enum pm_device_action action)
   {
           int ret;

           switch (action) {
           case PM_DEVICE_ACTION_SUSPEND:
                   ret = dummy_driver_pm_suspend(dev);
                   break;
           case PM_DEVICE_ACTION_RESUME:
                   ret = dummy_driver_pm_resume(dev);
                   break;
           case PM_DEVICE_ACTION_TURN_OFF:
                   ret = dummy_driver_pm_turn_off(dev);
                   break;
           case PM_DEVICE_ACTION_TURN_ON:
                   ret = dummy_driver_pm_turn_on(dev);
                   break;
           default:
                   ret = -EINVAL;
                   break;
           }

           return ret;
   }

   static int dummy_init(const struct device *dev)
   {
           struct dummy_driver_data *dev_data = dev->data;
           const struct dummy_driver_config *dev_config = dev->config;

           /*
            * We must ensure all devices we depend on, excluding a potential
            * power domain, are initialized.
            *
            * If CONFIG_PM_DEVICE=n, this also ensures the devices are ACTIVE.
            */
           if (!device_is_ready(dev_config->bus) ||
               !gpio_is_ready_dt(&dev_config->int_pin) ||
               !gpio_is_ready_dt(&dev_config->enable_pin)) {
                   return -ENODEV;
           }

           /* We then initialize the device driver data structure */
           gpio_init_callback(&dev_data->int_pin_callback,
                              dummy_driver_int_pin_handler,
                              BIT(dev_config->int_pin.pin));

           dev_data->dev = dev;

          /*
           * This call must be the last call of the device init function.
           * It will initialize the device's PM_DEVICE context and use the
           * dummy_driver_pm_action callback to initialize the device into
           * the appropriate state.
            *
            * On success, :c:func:`pm_device_driver_init` returns 0.
            * If the callback fails (for example on ``PM_DEVICE_ACTION_RESUME``),
            * the error is propagated and the device is not marked ``ACTIVE``.
           */
          return pm_device_driver_init(dev, dummy_driver_pm_action);
   }

   #ifdef CONFIG_DEVICE_DEINIT_SUPPORT
   static int dummy_deinit(const struct device *dev)
   {
           int ret;

           /*
            * This call must be the first call of the device deinit function.
            * It will use the dummy_driver_pm_action callback to move the
            * device into, or verify the device is already in, an appropriate
            * state for deinitialization, and deinitialize the device's
            * PM_DEVICE context.
            */
           ret = pm_device_driver_deinit(dev, dummy_driver_pm_action);
           if (ret) {
                   return ret;
           }

           /*
            * The device is now either SUSPENDED or OFF, all the devices this
            * device depends on have been released, and devices with persistent
            * configurations like GPIO pins have been configured to match the
            * device state.
            *
            * The device will be left in this state until a new "owner" takes
            * over.
            */

           /*
            * If we had allocated memory, DMA channels or other resources, we would
            * release them here.
            */

           return ret;
   }
   #endif

   static struct dummy_driver_data data0;

   static struct dummy_driver_config config0 = {
           .bus = DEVICE_DT_GET(DT_INST_PARENT(0)),
           .int_pin = GPIO_DT_SPEC_INST_GET(0, int_gpios),
           .enable_pin = GPIO_DT_SPEC_INST_GET(0, enable_gpios),
   };

   /* Define the device's PM DEVICE context */
   PM_DEVICE_DT_INST_DEFINE(0, dummy_driver_pm_action);

   /* Define the device, pointing to the device's PM DEVICE context */
   DEVICE_DT_INST_DEINIT_DEFINE(
           0,
           &dummy_init,
           &dummy_deinit,
           PM_DEVICE_DT_INST_GET(0),
           &data0,
           &config0,
           POST_KERNEL,
           CONFIG_KERNEL_INIT_PRIORITY_DEFAULT,
           NULL
   );

支持部分设备电源管理的设备模型
******************************

如果未启用 :kconfig:option:`CONFIG_PM_DEVICE`，设备电源状态与设备的初始化状态绑定。

设备初始化完成后，会通过调用 :c:func:`pm_device_driver_init` 使用设备驱动的 PM 动作钩子把设备移到预期的初始状态。按照 ``Device actions x states`` 图和 ``OFF`` 状态的定义，这会先调用 ``PM_DEVICE_ACTION_TURN_ON``，然后调用 ``PM_DEVICE_ACTION_RESUME``。

如果驱动的 PM 钩子返回错误，初始化就会失败，设备保持在其先前的状态（对于支持 PM 的设备，通常是 ``SUSPENDED`` 或 ``OFF``）。

由于电源域和总线本身也是设备，每个电源域和总线都会按照 devicetree 依赖序号在其子设备之前完成初始化并被恢复。设备初始化时，假定每个设备都已上电，并且设备所依赖的设备处于 ``ACTIVE`` 状态。

设备反初始化后，会通过调用 :c:func:`pm_device_driver_deinit` 使用设备驱动的 PM 动作钩子把设备移到 ``SUSPENDED`` 状态。按照 ``Device actions x states``，并假定电源域始终开启，这会调用 ``PM_DEVICE_ACTION_SUSPEND``。

.. _pm-device-shell:

Shell 命令
**********

为便于测试，可以通过 shell 命令触发电源管理动作。为此，请启用 :kconfig:option:`CONFIG_PM_DEVICE_SHELL` 选项，并在 shell 中针对某个设备执行 ``pm`` 命令，例如：

.. code-block:: console

        uart:~$ device list
        - buttons (active)
        uart:~$ pm suspend buttons
        uart:~$ device list
        devices:
        - buttons (suspended)

要打印设备的电源管理状态，请启用 :kconfig:option:`CONFIG_DEVICE_SHELL` 并使用 ``device list`` 命令，例如：

.. code-block:: console

        uart:~$ device list
        devices:
        - i2c@40003000 (active)
        - buttons (active, usage=1)
        - leds (READY)

在此例中，``leds`` 不支持 PM，``i2c`` 支持 PM（采用手动挂起和恢复动作）且当前处于活动状态，``buttons`` 支持运行时 PM 且当前处于活动状态并有一个使用者。

.. _pm-device-busy:

忙状态指示
**********

当系统空闲且 SoC 即将睡眠时，电源管理子系统可以挂起设备，如 :ref:`pm-device-system-pm` 所述。这可能导致设备硬件丢失部分状态。挂起正处于硬件事务中间（例如正在写闪存）的设备，可能导致未定义行为或状态不一致。此 API 通过向内核表明设备正在执行操作、不应被挂起来保护此类事务。

调用 :c:func:`pm_device_busy_set` 后，设备被标记为忙，系统不会对它执行电源管理。当设备不再执行操作、可以被挂起时，应调用 :c:func:`pm_device_busy_clear`。

.. _pm-device-constraint:

设备电源管理与系统电源管理
**************************

在嵌入式系统中管理电源时，理解设备电源状态与系统整体电源状态之间的相互影响至关重要。有些设备可能依赖于系统电源状态。例如，SoC 的某些低功耗状态可能不为外设供电，如果设备正在执行操作就会出问题。为保持系统稳定性和数据完整性，必须进行恰当的协调。

为避免这类问题，设备在执行操作期间必须 :ref:`获取并释放锁 <pm-policy-power-states>` 那些会导致掉电的电源状态。

Zephyr 提供了一种机制，让设备声明哪些电源状态会导致掉电，并提供一个自动对它们加锁和释放锁的 API。把 :kconfig:option:`CONFIG_PM_POLICY_DEVICE_CONSTRAINTS` 设置为 ``y`` 即可启用此功能。

启用此功能后，设备必须在 devicetree 中声明哪些状态会导致掉电。在下面的示例中，设备 ``test_dev`` 声明电源状态 ``state1`` 和 ``state2`` 会导致掉电。

.. code-block:: devicetree

    power-states {
            state0: state0 {
                    compatible = "zephyr,power-state";
                    power-state-name = "suspend-to-idle";
                    min-residency-us = <10000>;
                    exit-latency-us = <100>;
            };

            state1: state1 {
                    compatible = "zephyr,power-state";
                    power-state-name = "standby";
                    min-residency-us = <20000>;
                    exit-latency-us = <200>;
            };

            state2: state2 {
                    compatible = "zephyr,power-state";
                    power-state-name = "suspend-to-ram";
                    min-residency-us = <50000>;
                    exit-latency-us = <500>;
            };

            state3: state3 {
                    compatible = "zephyr,power-state";
                    power-state-name = "suspend-to-ram";
                    status = "disabled";
            };
    };

    test_dev: test_dev {
            compatible = "test-device-pm";
            status = "okay";
            zephyr,disabling-power-states = <&state1 &state2>;
    };

此后，设备可以通过调用 :c:func:`pm_policy_device_power_lock_get` 锁定这些状态，并通过 :c:func:`pm_policy_device_power_lock_put` 释放锁。例如：

.. code-block:: C

    static void timer_expire_cb(struct k_timer *timer)
    {
           struct test_driver_data *data = k_timer_user_data_get(timer);

           data->ongoing = false;
           k_timer_stop(timer);
           pm_policy_device_power_lock_put(data->self);
    }

    void test_driver_async_operation(const struct device *dev)
    {
           struct test_driver_data *data = dev->data;

           data->ongoing = true;
           pm_policy_device_power_lock_get(dev);

           /** Lets set a timer big enough to ensure that any deep
            *  sleep state would be suitable but constraints will
            *  make only state0 (suspend-to-idle) will be used.
            */
           k_timer_start(&data->timer, K_MSEC(500), K_NO_WAIT);
    }

同样的模式也适用于可能产生 :ref:`零延迟中断 <zlis>` 的设备路径。零延迟 ISR 不得调用 PM API 或其他内核 API。如果该 ISR 依赖于某些系统电源状态下不可用的资源，则使能中断源的常规驱动路径可以在该路径活动期间持有设备电源策略锁。当该路径不再活动时，驱动应先屏蔽或禁用中断源，然后再释放锁。

唤醒能力
********

有些设备能够把系统从睡眠状态唤醒。当设备具备这种能力时，应用可以使用 :c:func:`pm_device_wakeup_enable` 动态启用或禁用设备上的该功能。

可以通过在 devicetree 的设备节点中声明 ``wakeup-source`` 属性来设置此属性。例如，下面的 devicetree 片段把 ``gpio0`` 设备设置为唤醒源：

.. code-block:: devicetree

                gpio0: gpio@40022000 {
                        compatible = "ti,cc13xx-cc26xx-gpio";
                        reg = <0x40022000 0x400>;
                        interrupts = <0 0>;
                        status = "disabled";
                        label = "GPIO_0";
                        gpio-controller;
                        wakeup-source;
                        #gpio-cells = <2>;
                };

默认情况下，具备唤醒能力的设备在设备初始化期间不会启用该功能。应用可以稍后调用 :c:func:`pm_device_wakeup_enable` 启用该功能。

.. note::

   此属性 **仅** 供系统电源管理用于识别不应被挂起的设备。驱动或应用有责任完成设备支持该功能所需的任何额外配置。

示例
****

以下示例展示了设备电源管理功能：

* :zephyr_file:`samples/subsys/pm/device_pm/`
* :zephyr_file:`tests/subsys/pm/power_mgmt/`
* :zephyr_file:`tests/subsys/pm/device_wakeup_api/`
* :zephyr_file:`tests/subsys/pm/device_driver_init/`
