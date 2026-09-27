.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_mender_mcu:

mender-mcu
##########

简介
****

`mender-mcu`_ 与 Zephyr 集成，为资源受限设备提供可靠的固件更新。它实现 Update Module 接口，允许模块定义具体的更新处理方式。默认 Update Module 与 MCUboot 集成，支持 A/B 更新，使 MCU 能执行原子的、故障安全的 OTA 更新，并在失败时自动回滚，类似于 Mender 为 Linux 设备提供的更新机制。

客户端与 Mender 服务器通信，上报设备清单与身份，检查可用更新、下载新固件，并协调 Update Module 安全安装更新。Mender 服务器提供采用 Apache-2.0 许可证的开源版，以及采用商业许可证的企业版；商业方案支持本地部署及全托管的 hosted Mender 服务。

mender-mcu 采用 Apache-2.0 许可证。

要求
****

* 使用 cJSON 解析 JSON

在 Zephyr 中使用
****************

要将 mender-mcu 作为 Zephyr :ref:`模块 <modules>` 引入，可以在 ``west.yaml`` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/mender-mcu.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: mender-mcu
         url: https://github.com/mendersoftware/mender-mcu
         revision: main
         path: modules/mender-mcu # adjust the path as needed

详细说明和 API 文档见 `mender-mcu documentation`_。`Zephyr reference project`_ 提供了参考集成示例。

参考资料
********

.. target-notes::

.. _mender-mcu:
   https://github.com/mendersoftware/mender-mcu

.. _mender-mcu documentation:
   https://docs.mender.io/operating-system-updates-zephyr

.. _Zephyr reference project:
   https://github.com/mendersoftware/mender-mcu-integration
