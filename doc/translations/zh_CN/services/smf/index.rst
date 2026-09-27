.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _smf:

状态机框架
##########

.. highlight:: c

概述
====

状态机框架（SMF）是一个与应用无关的框架，便于开发者把状态机集成到应用中。只要启用 :kconfig:option:`CONFIG_SMF` 选项，就可以把该框架加入任何项目。

状态创建
========

一个状态由三个函数表示，其中一个实现 Entry 动作，另一个实现 Run 动作，最后一个实现 Exit 动作。entry 和 exit 函数的原型如下：``void funct(void *obj)``，run 动作的原型是 ``enum smf_state_result funct(void *obj)``，其中 ``obj`` 参数是用户定义的结构体，其第一个成员是状态机上下文 :c:struct:`smf_ctx`。例如::

   struct user_object {
      struct smf_ctx ctx;
      /* All User Defined Data Follows */
   };

:c:struct:`smf_ctx` 成员必须放在第一位，因为状态机框架的函数使用 :c:macro:`SMF_CTX` 宏把用户定义的对象强制转换为 :c:struct:`smf_ctx` 类型。

例如，可以不写 ``(struct smf_ctx *)&user_obj``，而使用 ``SMF_CTX(&user_obj)``。

默认情况下，状态可以没有祖先状态，从而构成扁平状态机。但要支持创建层次状态机，必须启用 :kconfig:option:`CONFIG_SMF_ANCESTOR_SUPPORT` 选项。

run 动作的返回值 :c:enum:`smf_state_result` 决定状态机是把事件传播给父级 run 动作（:c:enum:`SMF_EVENT_PROPAGATE`），还是该事件已由本 run 动作处理（:c:enum:`SMF_EVENT_HANDLED`）。扁平状态机没有父级动作，因此返回值被忽略；建议返回 :c:enum:`SMF_EVENT_HANDLED`。

调用 :c:func:`smf_set_state` 会阻止调用父级 run 动作，即使返回 :c:enum:`SMF_EVENT_PROPAGATE` 也是如此。

默认情况下，层次状态机不支持在进入父状态时进行到子状态的初始转换。要启用该功能，必须启用 :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION` 选项。

可以使用下面的宏来方便地创建状态：

* :c:macro:`SMF_CREATE_STATE` 创建一个状态

状态机创建
==========

状态机通过定义一个由枚举索引的状态表来创建。例如，下面创建了三个扁平状态::

   enum demo_state { S0, S1, S2 };

   const struct smf_state demo_states[] = {
      [S0] = SMF_CREATE_STATE(s0_entry, s0_run, s0_exit, NULL, NULL),
      [S1] = SMF_CREATE_STATE(s1_entry, s1_run, s1_exit, NULL, NULL),
      [S2] = SMF_CREATE_STATE(s2_entry, s2_run, s2_exit, NULL, NULL)
   };

而这个示例创建了三个层次状态::

   enum demo_state { S0, S1, S2 };

   const struct smf_state demo_states[] = {
      [S0] = SMF_CREATE_STATE(s0_entry, s0_run, s0_exit, parent_s0, NULL),
      [S1] = SMF_CREATE_STATE(s1_entry, s1_run, s1_exit, parent_s12, NULL),
      [S2] = SMF_CREATE_STATE(s2_entry, s2_run, s2_exit, parent_s12, NULL)
   };


这个示例创建了三个层次状态，并从父状态 S0 到子状态 S2 进行初始转换::

   enum demo_state { S0, S1, S2 };

   /* Forward declaration of state table */
   const struct smf_state demo_states[];

   const struct smf_state demo_states[] = {
      [S0] = SMF_CREATE_STATE(s0_entry, s0_run, s0_exit, NULL, demo_states[S2]),
      [S1] = SMF_CREATE_STATE(s1_entry, s1_run, s1_exit, demo_states[S0], NULL),
      [S2] = SMF_CREATE_STATE(s2_entry, s2_run, s2_exit, demo_states[S0], NULL)
   };

要设置初始状态，应调用 :c:func:`smf_set_initial` 函数。

要在一个状态之间转换到另一个状态，使用 :c:func:`smf_set_state` 函数。

.. note:: 如果未设置 :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION`，则不应向 :c:func:`smf_set_initial` 和 :c:func:`smf_set_state` 函数传入父状态，因为父状态并不知道应转换到哪个子状态。如果已定义到子状态的初始转换，则转换到父状态是可以的。形式良好的 HSM 应为所有父状态定义初始转换。

.. note:: 状态机运行期间，只应从 Entry 或 Run 函数调用 :c:func:`smf_set_state`。从 Exit 函数调用 :c:func:`smf_set_state` 会在日志中产生一条警告，并且不会发生状态转换。

状态机执行
==========

要运行状态机，应以某种与应用相关的方式调用 :c:func:`smf_run_state` 函数。如果该函数返回非零值，应用应停止调用 smf_run_state。

状态机终止
==========

要终止状态机，应调用 :c:func:`smf_set_terminate` 函数。它可以从 entry、run 或 exit 动作中调用。该函数接收一个非零的用户自定义值，该值将由 :c:func:`smf_run_state` 函数返回。

获取当前状态
============

**叶状态**：在层次状态机的语境中，*叶状态* 是不包含任何子状态的状态。它表示层次结构中最细粒度的状态层级，无法进一步分解。

**执行状态**：*执行状态* 是指状态机当前正在执行其 entry、run 或 exit 动作的状态。根据当前操作的不同，它可能是父状态，也可能是叶状态。

要获取当前的叶状态，应调用 :c:func:`smf_get_current_leaf_state` 函数。例如::

   const struct smf_state *leaf_state = smf_get_current_leaf_state(SMF_CTX(&s_obj));

.. note:: 如果未启用 :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION`，或者未定义父状态的初始状态，请始终把状态设为叶状态。否则状态机可能直接进入父状态，而 :c:func:`smf_get_current_leaf_state` 可能返回父状态而不是叶状态。请确保为所有父状态正确配置初始转换，以避免出现形式不良的层次状态机。

要获取当前正在执行其 entry、run 或 exit 动作的状态，请使用 :c:func:`smf_get_current_executing_state` 函数。

UML 状态机
==========

SMF 在状态转换方面遵循 UML 层次状态机规则，即在转换时不执行最近公共祖先的 entry 和 exit 动作，除非该转换是转换到自身。

状态机的 UML 规范见 UML 规范第 14 章，可从以下地址获取：https://www.omg.org/spec/UML/

SMF 在以下方面偏离 UML 规则：

1. 在源状态的上下文中执行与转换相关联的动作，而不是在执行完 exit 动作之后执行。
2. 只允许转换到自身的外部转换，不允许转换到子状态。从父状态到子状态的转换被视为局部转换。
3. 禁止在 exit 动作中使用 :c:func:`smf_set_state` 进行状态转换。

除初始伪状态外，SMF 不提供任何伪状态。终止伪状态可以通过在 'terminate' 状态的 entry 动作中调用 :c:func:`smf_set_terminate` 来建模。正交区域通过对每个区域调用 :c:func:`smf_run_state` 来建模。

状态机示例
==========

扁平状态机示例
**************

这个示例使用 SMF 把下面的状态图转换为代码，其中初始状态是 S0。

.. graphviz::
   :caption: 扁平状态机图

   digraph smf_flat {
      node [style=rounded];
      init [shape = point];
      STATE_S0 [shape = box];
      STATE_S1 [shape = box];
      STATE_S2 [shape = box];

      init -> STATE_S0;
      STATE_S0 -> STATE_S1;
      STATE_S1 -> STATE_S2;
      STATE_S2 -> STATE_S0;
   }

代码::

        #include <zephyr/smf.h>

        /* Forward declaration of state table */
        static const struct smf_state demo_states[];

        /* List of demo states */
        enum demo_state { S0, S1, S2 };

        /* User defined object */
        struct s_object {
                /* This must be first */
                struct smf_ctx ctx;

                /* Other state specific data add here */
        } s_obj;

        /* State S0 */
        static void s0_entry(void *o)
        {
                /* Do something */
        }
        static enum smf_state_result s0_run(void *o)
        {
                smf_set_state(SMF_CTX(&s_obj), &demo_states[S1]);
                return SMF_EVENT_HANDLED;
        }
        static void s0_exit(void *o)
        {
                /* Do something */
        }

        /* State S1 */
        static enum smf_state_result s1_run(void *o)
        {
                smf_set_state(SMF_CTX(&s_obj), &demo_states[S2]);
                return SMF_EVENT_HANDLED;
        }
        static void s1_exit(void *o)
        {
                /* Do something */
        }

        /* State S2 */
        static void s2_entry(void *o)
        {
                /* Do something */
        }
        static enum smf_state_result s2_run(void *o)
        {
                smf_set_state(SMF_CTX(&s_obj), &demo_states[S0]);
                return SMF_EVENT_HANDLED;
        }

        /* Populate state table */
        static const struct smf_state demo_states[] = {
                [S0] = SMF_CREATE_STATE(s0_entry, s0_run, s0_exit, NULL, NULL),
                /* State S1 does not have an entry action */
                [S1] = SMF_CREATE_STATE(NULL, s1_run, s1_exit, NULL, NULL),
                /* State S2 does not have an exit action */
                [S2] = SMF_CREATE_STATE(s2_entry, s2_run, NULL, NULL, NULL),
        };

        int main(void)
        {
                int32_t ret;

                /* Set initial state */
                smf_set_initial(SMF_CTX(&s_obj), &demo_states[S0]);

                /* Run the state machine */
                while(1) {
                        /* State machine terminates if a non-zero value is returned */
                        ret = smf_run_state(SMF_CTX(&s_obj));
                        if (ret) {
                                /* handle return code and terminate state machine */
                                break;
                        }
                        k_msleep(1000);
                }
        }

层次状态机示例
**************

这个示例使用 SMF 把下面的状态图转换为代码，其中 S0 和 S1 共享一个父状态，且 S0 是初始状态。


.. graphviz::
   :caption: 层次状态机图

   digraph smf_hierarchical {
      node [style = rounded];
      init [shape = point];
      STATE_S0 [shape = box];
      STATE_S1 [shape = box];
      STATE_S2 [shape = box];

      subgraph cluster_0 {
         label = "PARENT";
         style = rounded;
         STATE_S0 -> STATE_S1;
      }

      init -> STATE_S0;
      STATE_S1 -> STATE_S2;
      STATE_S2 -> STATE_S0;
   }

代码::

        #include <zephyr/smf.h>

        /* Forward declaration of state table */
        static const struct smf_state demo_states[];

        /* List of demo states */
        enum demo_state { PARENT, S0, S1, S2 };

        /* User defined object */
        struct s_object {
                /* This must be first */
                struct smf_ctx ctx;

                /* Other state specific data add here */
        } s_obj;

        /* Parent State */
        static void parent_entry(void *o)
        {
                /* Do something */
        }
        static void parent_exit(void *o)
        {
                /* Do something */
        }

        /* State S0 */
        static enum smf_state_result s0_run(void *o)
        {
                smf_set_state(SMF_CTX(&s_obj), &demo_states[S1]);
                return SMF_EVENT_HANDLED;
        }

        /* State S1 */
        static enum smf_state_result s1_run(void *o)
        {
                smf_set_state(SMF_CTX(&s_obj), &demo_states[S2]);
                return SMF_EVENT_HANDLED;
        }

        /* State S2 */
        static enum smf_state_result s2_run(void *o)
        {
                smf_set_state(SMF_CTX(&s_obj), &demo_states[S0]);
                return SMF_EVENT_HANDLED;
        }

        /* Populate state table */
        static const struct smf_state demo_states[] = {
                /* Parent state does not have a run action */
                [PARENT] = SMF_CREATE_STATE(parent_entry, NULL, parent_exit, NULL, NULL),
                /* Child states do not have entry or exit actions */
                [S0] = SMF_CREATE_STATE(NULL, s0_run, NULL, &demo_states[PARENT], NULL),
                [S1] = SMF_CREATE_STATE(NULL, s1_run, NULL, &demo_states[PARENT], NULL),
                /* State S2 do not have entry or exit actions and no parent */
                [S2] = SMF_CREATE_STATE(NULL, s2_run, NULL, NULL, NULL),
        };

        int main(void)
        {
                int32_t ret;

                /* Set initial state */
                smf_set_initial(SMF_CTX(&s_obj), &demo_states[S0]);

                /* Run the state machine */
                while(1) {
                        /* State machine terminates if a non-zero value is returned */
                        ret = smf_run_state(SMF_CTX(&s_obj));
                        if (ret) {
                                /* handle return code and terminate state machine */
                                break;
                        }
                        k_msleep(1000);
                }
        }

设计层次状态机时，应考虑以下几点：

- 祖先的 entry 动作先于兄弟状态的 entry 动作执行。例如，parent_entry 函数在 s0_entry 函数之前被调用。
- 在共享祖先的兄弟状态之间转换时，不会重新执行祖先的 entry 动作，也不会执行 exit 动作。例如，从 S0 转换到 S1 时不会调用 parent_entry 函数，也不会调用 parent_exit 函数。
- 祖先的 exit 动作在当前状态的 exit 动作之后执行。例如，s1_exit 函数在 parent_exit 函数之前被调用。
- 只有当 child_run 函数既不调用 :c:func:`smf_set_state` 也不返回 :c:enum:`SMF_EVENT_HANDLED` 时，parent_run 函数才会执行。
- 在未启用 :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION` 时，或者当父状态的初始状态未定义时，请确保状态总是转换到叶状态，以避免出现形式不良的层次状态机。

事件驱动状态机示例
******************

事件并不是状态机框架的显式组成部分，但可以使用 Zephyr :ref:`events` 实现事件驱动的状态机。

.. graphviz::
   :caption: 事件驱动状态机图

   digraph smf_flat {
      node [style=rounded];
      init [shape = point];
      STATE_S0 [shape = box];
      STATE_S1 [shape = box];

      init -> STATE_S0;
      STATE_S0 -> STATE_S1 [label = "BTN EVENT"];
      STATE_S1 -> STATE_S0 [label = "BTN EVENT"];
   }

代码::

        #include <zephyr/kernel.h>
        #include <zephyr/drivers/gpio.h>
        #include <zephyr/smf.h>

        #define SW0_NODE        DT_ALIAS(sw0)

        /* List of events */
        #define EVENT_BTN_PRESS BIT(0)

        static const struct gpio_dt_spec button =
                GPIO_DT_SPEC_GET_OR(SW0_NODE, gpios, {0});

        static struct gpio_callback button_cb_data;

        /* Forward declaration of state table */
        static const struct smf_state demo_states[];

        /* List of demo states */
        enum demo_state { S0, S1 };

        /* User defined object */
        struct s_object {
                /* This must be first */
                struct smf_ctx ctx;

                /* Events */
                struct k_event smf_event;
                int32_t events;

                /* Other state specific data add here */
        } s_obj;

        /* State S0 */
        static void s0_entry(void *o)
        {
                printk("STATE0\n");
        }

        static enum smf_state_result s0_run(void *o)
        {
                struct s_object *s = (struct s_object *)o;

                /* Change states on Button Press Event */
                if (s->events & EVENT_BTN_PRESS) {
                        smf_set_state(SMF_CTX(&s_obj), &demo_states[S1]);
                }
                return SMF_EVENT_HANDLED;
        }

        /* State S1 */
        static void s1_entry(void *o)
        {
                printk("STATE1\n");
        }

        static enum smf_state_result s1_run(void *o)
        {
                struct s_object *s = (struct s_object *)o;

                /* Change states on Button Press Event */
                if (s->events & EVENT_BTN_PRESS) {
                        smf_set_state(SMF_CTX(&s_obj), &demo_states[S0]);
                }
                return SMF_EVENT_HANDLED;
        }

        /* Populate state table */
        static const struct smf_state demo_states[] = {
                [S0] = SMF_CREATE_STATE(s0_entry, s0_run, NULL, NULL, NULL),
                [S1] = SMF_CREATE_STATE(s1_entry, s1_run, NULL, NULL, NULL),
        };

        void button_pressed(const struct device *dev,
                        struct gpio_callback *cb, uint32_t pins)
        {
                /* Generate Button Press Event */
                k_event_post(&s_obj.smf_event, EVENT_BTN_PRESS);
        }

        int main(void)
        {
                int ret;

                if (!gpio_is_ready_dt(&button)) {
                        printk("Error: button device %s is not ready\n",
                                button.port->name);
                        return;
                }

                ret = gpio_pin_configure_dt(&button, GPIO_INPUT);
                if (ret != 0) {
                        printk("Error %d: failed to configure %s pin %d\n",
                                ret, button.port->name, button.pin);
                        return;
                }

                ret = gpio_pin_interrupt_configure_dt(&button,
                        GPIO_INT_EDGE_TO_ACTIVE);
                if (ret != 0) {
                        printk("Error %d: failed to configure interrupt on %s pin %d\n",
                                ret, button.port->name, button.pin);
                        return;
                }

                gpio_init_callback(&button_cb_data, button_pressed, BIT(button.pin));
                gpio_add_callback(button.port, &button_cb_data);

                /* Initialize the event */
                k_event_init(&s_obj.smf_event);

                /* Set initial state */
                smf_set_initial(SMF_CTX(&s_obj), &demo_states[S0]);

                /* Run the state machine */
                while(1) {
                        /* Block until an event is detected */
                        s_obj.events = k_event_wait(&s_obj.smf_event,
                                        EVENT_BTN_PRESS, true, K_FOREVER);

                        /* State machine terminates if a non-zero value is returned */
                        ret = smf_run_state(SMF_CTX(&s_obj));
                        if (ret) {
                                /* handle return code and terminate state machine */
                                break;
                        }
                }
        }

包含初始转换和转换到自身的状态机示例
************************************

:zephyr_file:`tests/lib/smf/src/test_lib_self_transition_smf.c` 定义了一个状态机，用于测试父状态中的初始转换和转换到自身。该测试的状态图如下。


.. graphviz::
   :caption: 用于测试 UML 状态转换的状态机

   digraph smf_hierarchical_initial {
      compound=true;
      node [style = rounded];
      "smf_set_initial()" [shape=plaintext fontname=Courier];
      ab_init_state [shape = point];
      STATE_A [shape = box];
      STATE_B [shape = box];
      STATE_C [shape = box];
      STATE_D [shape = box];
      DC[shape=point height=0 width=0 label="" style="invis"]

      subgraph cluster_root {
         label = "ROOT";
         style = rounded;

         subgraph cluster_ab {
            label = "PARENT_AB";
            style = rounded;
            ab_init_state -> STATE_A;
            STATE_A -> STATE_B;
         }

         subgraph cluster_c {
            label = "PARENT_C";
            style = rounded;
            STATE_B -> STATE_C [ltail=cluster_ab]
         }

         STATE_C -> DC [ltail=cluster_c, dir=none];
         DC -> STATE_C [lhead=cluster_c];
         STATE_C -> STATE_D
      }

      "smf_set_initial()" -> STATE_A [lhead=cluster_ab]
   }


测试插桩
========

SMF 提供了可选的插桩钩子，用于在测试期间观察状态机行为。要启用它们，请设置 :kconfig:option:`CONFIG_SMF_INSTRUMENTATION`。

启用后，可以通过 :c:func:`smf_set_hooks` 在状态机上下文上注册三个钩子回调：

- **on_action** —— 在每个 entry、run 或 exit 动作执行之前调用。
- **on_transition** —— 在当前状态指针更新之后、新状态的 entry 动作执行之前调用。
- **on_error** —— 在检测到无效操作时调用（例如转换目标为 NULL，或试图从 exit 动作发起转换）。

.. important:: :c:func:`smf_set_hooks` 必须在 :c:func:`smf_set_initial` **之后** 调用，因为 :c:func:`smf_set_initial` 会把钩子指针重置为 ``NULL``。因此，在 :c:func:`smf_set_initial` 期间执行的 entry 动作（即初始状态的 entry 动作及其祖先的 entry 动作）将 **不会** 被钩子捕获。

示例::

        #include <zephyr/smf.h>

        static void on_action(struct smf_ctx *ctx,
                              const struct smf_state *state,
                              smf_action_type action_type)
        {
                /* Log or record the action */
        }

        static void on_transition(struct smf_ctx *ctx,
                                  const struct smf_state *source,
                                  const struct smf_state *dest)
        {
                /* Log or record the transition */
        }

        static const struct smf_hooks hooks = {
                .on_action = on_action,
                .on_transition = on_transition,
                /* .on_error = NULL — any member may be NULL */
        };

        void test_example(void)
        {
                struct s_object s_obj;

                /* Set the initial state first */
                smf_set_initial(SMF_CTX(&s_obj), &demo_states[S0]);

                /* Install hooks after init — initial entry actions are not captured */
                smf_set_hooks(SMF_CTX(&s_obj), &hooks);

                /* Run the state machine — hooks fire on every action and transition */
                while (!smf_run_state(SMF_CTX(&s_obj))) {
                        /* ... */
                }
        }

未设置 :kconfig:option:`CONFIG_SMF_INSTRUMENTATION` 时，所有插桩代码都会被编译掉，运行时开销为零。

API 参考
========

.. doxygengroup:: smf
