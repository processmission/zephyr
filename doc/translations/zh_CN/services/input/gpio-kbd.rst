.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _gpio-kbd:

GPIO 键盘矩阵
#############

:dtcompatible:`gpio-kbd-matrix` 驱动支持多种键盘矩阵硬件配置，并提供了许多选项来改变其行为。下文概述了一些常见配置以及驱动如何支持它们。

所有这些配置的常规做法是：驱动读取行 GPIO（输入），并通过列 GPIO（输出）进行选择。

基本用例：无隔离二极管、GPIO 支持中断
*************************************

这是消费级键盘中常见的配置，这类键盘使用薄膜按键和柔性电路板，没有隔离二极管，需要鬼键检测（默认启用）。

.. figure:: no-diodes.svg
      :align: center
      :width: 50%

      3x3 矩阵，无二极管

系统必须支持 GPIO 中断，并且必须能够同时在所有行 GPIO 上启用中断。

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        row-gpios = <&gpio0 0 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>,
                    <&gpio0 1 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>,
                    <&gpio0 2 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>;
        col-gpios = <&gpio0 3 GPIO_ACTIVE_LOW>,
                    <&gpio0 4 GPIO_ACTIVE_LOW>,
                    <&gpio0 5 GPIO_ACTIVE_LOW>;
   };

在此配置下，一旦所有按键都释放，矩阵扫描库就会进入空闲模式；只有按下某个按键时，键盘矩阵线程才会唤醒。

当前未选中的列 GPIO 会配置为高阻态。这意味着行状态可能需要一些时间才能稳定，以避免将一个列的按键状态误读为下一个列的状态。可以通过修改 ``settle-time-us`` 属性来调整稳定时间。

隔离二极管
**********

如果矩阵为每个按键都带有隔离二极管，则可以：

 - 禁用鬼键检测，从而可以检测任意按键组合
 - 将驱动配置为把未选中的列 GPIO 驱动到非活动状态，而不是高阻态；这样可以减少稳定时间（可能降至 0），并使用更高效的整端口 GPIO 读取 API（如果 GPIO 引脚是连续的，这一行为会自动生效）

二极管从行连接到列的矩阵必须在行上使用上拉，并使用低电平有效的列。

.. figure:: diodes-rc.svg
      :align: center
      :width: 50%

      带有行到列隔离二极管的 3x3 矩阵。

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        row-gpios = <&gpio0 0 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>,
                    <&gpio0 1 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>,
                    <&gpio0 2 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>;
        col-gpios = <&gpio0 3 GPIO_ACTIVE_LOW>,
                    <&gpio0 4 GPIO_ACTIVE_LOW>,
                    <&gpio0 5 GPIO_ACTIVE_LOW>;
        col-drive-inactive;
        settle-time-us = <0>;
        no-ghostkey-check;
   };

二极管从列连接到行的矩阵必须在行上使用下拉，并使用高电平有效的列。

.. figure:: diodes-cr.svg
      :align: center
      :width: 50%

      带有列到行隔离二极管的 3x3 矩阵。

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        row-gpios = <&gpio0 0 (GPIO_PULL_DOWN | GPIO_ACTIVE_HIGH)>,
                    <&gpio0 1 (GPIO_PULL_DOWN | GPIO_ACTIVE_HIGH)>,
                    <&gpio0 2 (GPIO_PULL_DOWN | GPIO_ACTIVE_HIGH)>;
        col-gpios = <&gpio0 3 GPIO_ACTIVE_HIGH>,
                    <&gpio0 4 GPIO_ACTIVE_HIGH>,
                    <&gpio0 5 GPIO_ACTIVE_HIGH>;
        col-drive-inactive;
        settle-time-us = <0>;
        no-ghostkey-check;
   };

不支持中断的 GPIO
*****************

某些 GPIO 控制器对 GPIO 中断有限制，可能不支持同时在所有行 GPIO 上启用中断。

在这种情况下，可以将驱动配置为完全不使用中断，转而通过选中所有列并在行 GPIO 上持续轮询来进入空闲状态；如果引脚是连续的，这只需一次 GPIO API 操作。

可以通过将 ``idle-mode`` 属性设置为 ``poll`` 来启用此配置：

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        ...
        idle-mode = "poll";
   };

GPIO 多路复用器
***************

在更极端的情况下，例如列使用多路复用器且无法同时选中所有列时，可以将驱动配置为连续扫描。

可以通过将 ``idle-mode`` 设置为 ``scan``、并将 ``poll-timeout-ms`` 设置为 ``0`` 来实现。

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        ...
        poll-timeout-ms = <0>;
        idle-mode = "scan";
   };

行和列 GPIO 的选择
******************

如果行 GPIO 是连续的并且位于同一个 gpio 控制器上，驱动会自动切换 API，从整个 GPIO 端口读取，而不是读取单个引脚。当 GPIO 未进行内存映射时（例如在 I2C 或 SPI 端口扩展器上），这一点尤其有用，因为它能显著减少相应总线上的事务数量。

列 GPIO 也是如此，但前提是矩阵配置了 ``col-drive-inactive``，因此仅适用于带有隔离二极管的矩阵。

16 位行支持
***********

默认情况下，驱动使用 8 位数据类型存储行状态，这会将矩阵行大小限制为 8。可以通过启用 :kconfig:option:`CONFIG_INPUT_KBD_MATRIX_16_BIT_ROW` 选项将其增加到 16。

实际按键掩码配置
****************

如果按键矩阵不完整，可以使用 ``actual-key-mask`` 属性指定实际装配的按键映射。这样可以在鬼键检测之前过滤矩阵状态，移除不存在的按键，从而可能允许原本会被鬼键检测阻止的按键组合。

例如，对于一个缺少某个按键的 3x3 矩阵：

.. figure:: no-sw4.svg
      :align: center
      :width: 50%

      一个缺少某个按键的 3x3 矩阵。

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        ...
        actual-key-mask = <0x07 0x05 0x07>;
   };

例如，这样可以检测到同时按下 ``Sw1``、``SW2`` 和 ``SW4``，而不会触发防鬼键。

可以通过启用 :kconfig:option:`CONFIG_INPUT_KBD_ACTUAL_KEY_MASK_DYNAMIC` 并在运行时使用 :c:func:`input_kbd_matrix_actual_key_mask_set` API 来更改实际按键掩码。

键位映射配置
************

键盘矩阵设备会报告一系列 x/y/触摸事件。可以使用 :dtcompatible:`input-keymap` 驱动将它们映射为普通按键事件。

例如，以下配置会设置一个 ``keymap`` 设备，该设备将 x/y/触摸事件作为输入，并生成相应的按键事件作为输出：

.. code-block:: devicetree

  kbd {
      ...
      keymap {
          compatible = "input-keymap";
          keymap = <
              MATRIX_KEY(0, 0, INPUT_KEY_1)
              MATRIX_KEY(0, 1, INPUT_KEY_2)
              MATRIX_KEY(0, 2, INPUT_KEY_3)
              MATRIX_KEY(1, 0, INPUT_KEY_4)
              MATRIX_KEY(1, 1, INPUT_KEY_5)
              MATRIX_KEY(1, 2, INPUT_KEY_6)
              MATRIX_KEY(2, 0, INPUT_KEY_7)
              MATRIX_KEY(2, 1, INPUT_KEY_8)
              MATRIX_KEY(2, 2, INPUT_KEY_9)
          >;
          row-size = <3>;
          col-size = <3>;
      };
  };

.. doxygengroup:: input_keymap

键盘矩阵 Shell 命令
*******************

可以使用 shell 命令 ``kbd_matrix_state_dump`` 测试任何基于键盘矩阵库实现的键盘矩阵驱动的功能。启用后，它会在矩阵状态每次变化时记录该状态；禁用后，它会打印检测到的所有按键的按位或掩码，可用于设置 ``actual-key-mask`` 属性。

可以使用 :kconfig:option:`CONFIG_INPUT_SHELL_KBD_MATRIX_STATE` 启用该命令。

用法示例：

.. code-block:: console

   uart:~$ device list
   devices:
   - kbd-matrix (READY)
   uart:~$ input kbd_matrix_state_dump kbd-matrix
   Keyboard state logging enabled for kbd-matrix
   [00:01:41.678,466] <inf> input: kbd-matrix state [01 -- -- --] (1)
   [00:01:41.784,912] <inf> input: kbd-matrix state [-- -- -- --] (0)
   ...
   press more buttons
   ...
   uart:~$ input kbd_matrix_state_dump off
   Keyboard state logging disabled
   [00:01:47.967,651] <inf> input: kbd-matrix key-mask [07 05 07 --] (8)

键盘矩阵库
**********

GPIO 键盘矩阵驱动基于通用的键盘矩阵库，该库实现了扫描延迟、去抖、空闲模式等核心功能。它可以复用来实现其他键盘矩阵驱动，这些驱动可以是应用专用的。

.. doxygengroup:: input_kbd_matrix
