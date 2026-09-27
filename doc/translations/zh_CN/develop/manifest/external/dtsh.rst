.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_dtsh:

DTSh
####

简介
****

`DTSh <DTSh-Handbook_>`_ 是具有类 shell 命令行界面的交互式 DTS 文件查看器：

- 便捷地 *浏览* 和 *可视化* 设备树
- 根据支持的总线协议、绑定、生成的 IRQ、内存大小，或“sensor”“PWM”等关键词查找节点
- 将命令输出重定向到文本、HTML 或 SVG 文件，用于记录硬件配置或做笔记
- 支持上下文自动补全、命令历史、语义高亮和用户配置
- 支持脚本执行，即批处理模式

此 Zephyr 模块将 DTSh 作为 West 扩展加入 Zephyr 工作区。


在 Zephyr 中使用
****************

安装 DTSh 模块时，需要定义自己的清单文件，或通过子清单引入。

例如，假设采用与 `Zephyr Getting Started Guide`_ 相同的路径，创建 ``zephyrproject/zephyr/submanifests/dtsh.yaml``，内容如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: dtsh
         url: https://github.com/dottspina/dtsh.git
         revision: zephyr
         path: modules/tools/dtsh
         west-commands: scripts/west-commands.yml


然后更新工作区并安装 DTSh 依赖：

.. code-block:: sh

   west update dtsh
   west packages -m dtsh pip --install

.. note::

   ``west update dtsh`` 会获取 `DTSh project <DTSh-project_>`_ 的所有标签。可忽略这些标签，因为它们并不指向此 Zephyr 模块的版本，与这里的使用无关。


West 命令
*********

安装后，该项目／模块应提供 ``west dtsh`` 命令。

.. code-block:: console

   $ west build
   $ west dtsh
   dtsh (0.2.5-zephyr): Shell-like interface with Devicetree
   How to exit: q, or quit, or exit, or press Ctrl-D

   /
   > cd &flash_controller

   /soc/flash-controller@4001e000
   > find -E --also-known-as (image|storage).* --format NKd -T
                                Also Known As               Description
                                ───────────────────────────────────────────────────────────────────────────────────
   flash-controller@4001e000    flash_controller            Nordic NVMC (Non-Volatile Memory Controller)
   └── flash@0                  flash0                      Flash node
       └── partitions                                       This binding is used to describe fixed partitions…
           ├── partition@c000   image-0, slot0_partition    Each child node of the fixed-partitions node represents…
           ├── partition@82000  image-1, slot1_partition    Each child node of the fixed-partitions node represents…
           └── partition@f8000  storage, storage_partition  Each child node of the fixed-partitions node represents…


运行 ``west dtsh -h`` 可查看完整 West 命令用法。

.. note::

   建议将模块安装到默认位置 ``modules/tools/dtsh``。否则，务必在运行 ``west dtsh`` 前设置 ``ZEPHYR_BASE`` 环境变量。


参考资料
********

- `DTSh project <DTSh-project_>`_
- `DTSh Handbook <DTSh-Handbook_>`_
- `dtsh module <dtsh-module_>`_


.. _DTSh-project: https://github.com/dottspina/dtsh

.. _DTSh-Handbook: https://dottspina.github.io/dtsh/handbook.html

.. _dtsh-module: https://github.com/dottspina/dtsh/tree/zephyr

.. _Zephyr Getting Started Guide: https://docs.zephyrproject.org/latest/develop/getting_started/
