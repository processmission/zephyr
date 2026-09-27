.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_edge_impulse:

适用于 Zephyr 的 Edge Impulse SDK
#################################

概述
****

Edge Impulse 是领先的边缘 AI 设计与开发平台，用于将机器学习部署到边缘设备。适用于 Zephyr 的 Edge Impulse SDK 将推理 SDK 封装为 Zephyr 模块，便于与 Zephyr 构建系统集成。可在 `这里 <https://www.edgeimpulse.com/signup>`_ 注册免费账户。

该模块将 Edge Impulse 推理 SDK 封装为 Zephyr 模块，便于集成到构建系统。它还可提供 west 扩展命令，在 Edge Impulse 平台构建模型部署产物，并将其下载到工作区，以便集成到 Zephyr 应用中。

Edge Impulse SDK 采用 `BSD-3-Clause-Clear 许可证 <https://github.com/edgeimpulse/edge-impulse-sdk-zephyr?tab=BSD-3-Clause-Clear-1-ov-file>`_。注意，使用 Edge Impulse 云服务至少需要免费级别账户，或公共项目的 API 密钥；定价和服务条款见 `Edge Impulse 网站 <https://edgeimpulse.com>`_。

向项目添加模块
**************

使用该模块时，添加以下条目，并将 ``v1.82.3`` 替换为所需版本：

.. code-block:: yaml

   manifest:
     projects:
       - name: edge-impulse-sdk-zephyr
         url: https://github.com/edgeimpulse/edge-impulse-sdk-zephyr
         revision: v1.82.3
         path: modules/edge-impulse-sdk-zephyr
         west-commands: west/west-commands.yml

将条目加入 Zephyr 子清单并运行 ``west update``，或加入项目的 ``west.yml`` 清单。

在 Zephyr 中使用
****************

可以使用提供的 west 扩展命令，也可以手动构建和部署 Edge Impulse 模型。详细说明见 `Edge Impulse Zephyr Module Deployment`_。

**West 扩展命令：**

- ``west ei-build``：触发 Studio 构建，可指定参数 ``-e tflite-eon``、``-t int8``、``-i 1``
- ``west ei-deploy``：下载预先构建的部署产物
- 两个命令都要求提供 ``-k`` （API 密钥）和 ``-p`` （项目 ID）选项

与 Zephyr 集成的分步教程和指南见 `Edge Impulse Zephyr Module Deployment`_。

参考资料
********

.. target-notes::

.. _Edge Impulse Zephyr Module Deployment:
   https://docs.edgeimpulse.com/hardware/deployments/run-zephyr-module
