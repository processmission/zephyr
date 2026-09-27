.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_emlearn:

emlearn
#######

简介
****

`emlearn`_ 是用于在微控制器和嵌入式系统上部署机器学习模型的开源库，可根据 scikit-learn 或 Keras 训练的模型生成可移植 C 代码。

其 Python 库能将复杂机器学习模型转换为精简的 C 代码表示，使资源受限的嵌入式设备也能执行机器学习推理。

emlearn 采用 MIT 许可证。

在 Zephyr 中使用
****************

emlearn 仓库是一个 Zephyr :ref:`模块 <modules>`，为 Zephyr 应用提供 TinyML 能力，使机器学习模型可以直接运行在 Zephyr 设备上。

要将 emlearn 作为 Zephyr 模块引入，可以在 ``west.yaml`` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/emlearn.yaml``，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: emlearn
         url: https://github.com/emlearn/emlearn.git
         revision: master
         path: modules/lib/emlearn # adjust the path as needed

详细说明和 API 文档见 `emlearn documentation`_，尤其是其中的 `Getting Started on Zephyr RTOS`_ 章节。

参考资料
********

.. target-notes::

.. _emlearn:
   https://github.com/emlearn/emlearn

.. _emlearn documentation:
   https://emlearn.readthedocs.io/en/latest/

.. _Getting Started on Zephyr RTOS:
   https://emlearn.readthedocs.io/en/latest/getting_started_zephyr.html
