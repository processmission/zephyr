.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _stepper_api:

步进电机
########

步进电机驱动子系统包含两套设备驱动 API：

步进电机 API
************

步进电机驱动 API 为步进电机驱动提供通用接口。

- 使用 :c:func:`stepper_set_micro_step_res` 和 :c:func:`stepper_get_micro_step_res` 配置 **微步分辨率** 。
- 使用 :c:func:`stepper_enable` **启用** 步进电机驱动。
- 使用 :c:func:`stepper_disable` **禁用** 步进电机驱动。
- 使用 :c:func:`stepper_set_event_cb` 注册 **事件回调** 。

步进电机运动控制器 API
**********************

步进电机运动控制器 API 为步进电机运动控制器提供通用接口。

- 使用 :c:func:`stepper_ctrl_set_reference_position` 和 :c:func:`stepper_ctrl_get_actual_position` 配置以微步为单位的 **参考位置** 。
- 使用 :c:func:`stepper_ctrl_set_microstep_interval` 设置以纳秒为单位的 **步进间隔**
- 使用 :c:func:`stepper_ctrl_move_by` 按正负微步数 **移动指定步数** ，也称为 **相对运动** 。
- 使用 :c:func:`stepper_ctrl_move_to` **移动到** 指定位置，也称为 **绝对运动** 。
- 使用 :c:func:`stepper_ctrl_run` 以 **恒定步进间隔** 沿指定方向连续运行，直到检测到停止。
- 使用 :c:func:`stepper_ctrl_stop` **停止** 步进电机。
- 使用 :c:func:`stepper_ctrl_is_moving` 检查步进电机是否正在 **运动** 。
- 使用 :c:func:`stepper_ctrl_set_event_cb` 注册 **事件回调** 。

.. _stepper-device-tree:

设备树
******

对于步进电机运动控制器，Devicetree 为每个步进电机驱动设备提供初始硬件配置。每个设备都必须在 Zephyr 中指定 Devicetree 绑定，理想情况下还应提供一组硬件配置选项，例如电流设置、加减速参数等。随后即可在开发板的 Devicetree 中使用这些选项，将步进电机驱动配置为初始状态。

驱动组合场景
============

以下是两种典型场景：

.. toctree::
   :maxdepth: 1

   integrated_controller_driver.rst
   individual_controller_driver.rst

步进电机运动控制器 API 测试套件
*******************************

步进电机运动控制器 API 测试套件提供一组测试，用于验证步进电机运动控制器的功能。

.. zephyr-app-commands::
   :zephyr-app: tests/drivers/stepper/stepper_ctrl
   :board: <board>
   :west-args: --extra-dtc-overlay <path/to/board.overlay>
   :goals: build flash

示例输出
========

以下是 h-bridge-stepper-ctrl 测试输出的片段。

.. code-block:: console

   ===================================================================
   TESTSUITE stepper succeeded

   ------ TESTSUITE SUMMARY START ------

   SUITE PASS - 100.00% [stepper_ctrl]: pass = 10, fail = 0, skip = 0, total = 10 duration = 6.869 seconds
    - PASS - [stepper_ctrl.test_actual_position] duration = 0.001 seconds
    - PASS - [stepper_ctrl.test_move_by_negative_step_count] duration = 2.207 seconds
    - PASS - [stepper_ctrl.test_move_by_positive_step_count] duration = 2.202 seconds
    - PASS - [stepper_ctrl.test_move_to_negative_step_count] duration = 1.106 seconds
    - PASS - [stepper_ctrl.test_move_to_positive_step_count] duration = 1.102 seconds
    - PASS - [stepper_ctrl.test_move_zero_steps] duration = 0.006 seconds
    - PASS - [stepper_ctrl.test_run_negative_direction] duration = 0.115 seconds
    - PASS - [stepper_ctrl.test_run_positive_direction] duration = 0.124 seconds
    - PASS - [stepper_ctrl.test_set_micro_step_interval_invalid_zero] duration = 0.002 seconds
    - PASS - [stepper_ctrl.test_stop] duration = 0.004 seconds

   ------ TESTSUITE SUMMARY END ------

   ===================================================================
   PROJECT EXECUTION SUCCESSFUL

API 参考
********

.. _stepper-driver-api-reference:

所有步进电机驱动都应实现的一组通用函数。

.. doxygengroup:: stepper_hw_driver

.. _stepper-ctrl-api-reference:

所有步进电机运动控制器都应实现的一组通用函数。

.. doxygengroup:: stepper_ctrl

步进电机运动控制器专用 API
**************************

Trinamic
========

.. doxygengroup:: trinamic_stepper_ctrl

.. _stepper discord:
   https://discord.com/channels/720317445772017664/1278263869982375946
