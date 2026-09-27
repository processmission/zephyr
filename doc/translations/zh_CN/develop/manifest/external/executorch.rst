.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_executorch:

ExecuTorch
##########

简介
****

`ExecuTorch <https://github.com/pytorch/executorch>`_ 是 PyTorch 的端侧推理运行时。它可作为 Zephyr 外部模块集成，在 CPU 和 Arm Ethos-U NPU 上运行模型。

初次接触 ExecuTorch 时，可从以下资料开始：

- `ExecuTorch 工作原理 <https://docs.pytorch.org/executorch/stable/intro-how-it-works.html>`_
- `入门架构概览 <https://docs.pytorch.org/executorch/stable/getting-started-architecture.html>`_

ExecuTorch 采用 `BSD 3-Clause 许可证 <https://github.com/pytorch/executorch/blob/main/LICENSE>`_。

在 Zephyr 中使用
****************

本节介绍 ExecuTorch 模块注册、模型准备，以及 CPU 和 Arm Ethos-U NPU 目标的构建与运行步骤。

.. note::

   **前置条件**

   - **Python 3.12–3.13** —— ExecuTorch 工具要求使用这些版本。可以创建独立虚拟环境，也可以使用由兼容 Python 版本创建的 Zephyr 虚拟环境。
   - **Arm FVP** —— 仅在使用 Corstone FVP 目标（例如 ``mps3/corstone300/fvp``），需要在没有实物硬件时模拟 Cortex-M 和 Ethos-U NPU 的情况下必需。安装步骤见 :ref:`安装 Arm FVP <fvp-install>`。
   - **Docker（仅 macOS）** —— 仅在通过 `FVPs-on-Mac <https://github.com/Arm-Examples/FVPs-on-Mac.git>`_ 执行 Arm Ethos-U NPU 推理流程时必需。

安装 ExecuTorch
===============

**步骤 1：** 将以下项目条目加入 west 清单，将 ExecuTorch 注册为外部模块。可以创建专用子清单 ``zephyrproject/zephyr/submanifests/executorch.yaml``，也可以直接加入应用已有的 ``west.yml``：

.. code-block:: yaml

   manifest:
     projects:
       - name: executorch
         url: https://github.com/pytorch/executorch
         revision: v1.2.0
         path: modules/lib/executorch
         submodules: true

**步骤 2：** 运行 west update：

.. code-block:: console

   west update

**步骤 3：** 安装 ExecuTorch 及其依赖：

.. note::

   请在使用兼容 Python 版本（3.12–3.13）的 Zephyr 虚拟环境中执行这些命令。

.. code-block:: console

   pip install executorch==1.2.0
   pip install tosa-tools==2026.2.1
   pip install ethos-u-vela==5.0.0

构建与运行
==========

嵌入式设备运行 AI 模型时，目标硬件可能带有专用 AI 加速器，通常称为 NPU（神经网络处理单元）。Arm 提供 `Ethos-U NPU 系列 <https://www.arm.com/products/silicon-ip-cpu?families=ethos%20npus>`_，用于高效的端侧 AI 推理。下面的选项卡分别介绍 Ethos-U NPU 加速推理，以及无 NPU 设备上的纯 CPU 推理。

.. _fvp-install:

.. tabs::

   .. group-tab:: Arm Ethos-U NPU 推理

      .. note::

         **安装 Arm FVP**

         固定虚拟平台（FVP）是 Arm 提供的模拟器，可在没有实物硬件时运行 Zephyr。这里需要使用它们，通过 Corstone-300 参考平台模拟 Ethos-U55/U65/U85 加速器。

         .. tabs::

            .. group-tab:: Ubuntu

               **步骤 1：** 从 Arm FVP 页面下载 Corstone-300 安装程序。FVP 可以安装到计算机上的任意位置，无需位于 Zephyr 项目目录内。

               `Arm Corstone FVP <https://developer.arm.com/Tools%20and%20Software/Fixed%20Virtual%20Platforms/IoT%20FVPs>`_

               .. note::

                  FVP 版本号会随发布变化。请根据 Arm 下载页面，将文件名和 URL 设置为所需版本。

                  .. code-block:: console

                     FVP_TGZ="FVP_Corstone_SSE-300_11.27_42_Linux64_armv8l.tgz"
                     FVP_URL="https://developer.arm.com/-/cdn-downloads/permalink/FVPs-Corstone-IoT/Corstone-300/${FVP_TGZ}"
                     curl -L -o "${FVP_TGZ}" "${FVP_URL}"

               **步骤 2：** 解压下载的归档：

               .. code-block:: console

                  tar -xf "${FVP_TGZ}"

               **步骤 3：** 运行安装脚本：

               .. code-block:: console

                  ./FVP_Corstone_SSE-300.sh --i-agree-to-the-contained-eula --no-interactive -q

               **步骤 4：** 将 FVP 加入 ``PATH``。``FVP_Corstone_SSE-300_Ethos-U55`` 和 ``FVP_Corstone_SSE-300_Ethos-U65`` 位于同一目录：

               .. code-block:: console

                  export PATH=$HOME/FVP_Corstone_SSE-300/models/Linux64_armv8l_GCC-9.3:$PATH

               **步骤 5：** 通过 source 执行随附脚本，安装所需运行时依赖 ``libpython3.9.so.1.0``。不同 shell 的方法略有区别：

               *bash：*

               .. code-block:: console

                  source $HOME/FVP_Corstone_SSE-300/scripts/runtime.sh
                  unset PYTHONHOME

               *zsh：* 执行 source 之前必须手动设置 ``BASH_SOURCE``，因为 zsh 不会自动填充该变量：

               .. code-block:: console

                  BASH_SOURCE=$HOME/FVP_Corstone_SSE-300/scripts/runtime.sh
                  source $HOME/FVP_Corstone_SSE-300/scripts/runtime.sh
                  unset PYTHONHOME

               **步骤 6：** 验证安装：

               .. code-block:: console

                  FVP_Corstone_SSE-300_Ethos-U55 --version
                  FVP_Corstone_SSE-300_Ethos-U65 --version

            .. group-tab:: macOS

               在 macOS 上，FVP 通过 `FVPs-on-Mac <https://github.com/Arm-Examples/FVPs-on-Mac.git>`_ 项目提供的 Docker 封装运行。

               **步骤 1：** 克隆仓库并检出所需提交。仓库可以克隆到计算机上的任意位置，无需位于 Zephyr 项目目录内。

               .. code-block:: console

                  git clone https://github.com/Arm-Examples/FVPs-on-Mac.git

               .. code-block:: console

                  cd FVPs-on-Mac
                  git switch --detach 1458860

               **步骤 2：** 构建 Docker 封装：

               .. code-block:: console

                  ./build.sh

               .. note::

                  在 macOS 上执行封装构建和 FVP 命令之前，必须安装并启动 Docker。

               **步骤 3：** 对构建结果作基本检查：

               .. code-block:: console

                  ./bin/FVP_Corstone_SSE-300 --version

               **步骤 4：** 使 FVP 二进制文件可从当前环境访问：

               .. code-block:: console

                  export PATH=$PATH:$(pwd)/bin

            .. group-tab:: Windows

               **步骤 1：** 从 Arm FVP 页面下载 Corstone-300 安装程序。FVP 可以安装到计算机上的任意位置，无需位于 Zephyr 项目目录内。

               `Arm FVP <https://developer.arm.com/Tools%20and%20Software/Fixed%20Virtual%20Platforms/IoT%20FVPs>`_

               选择 Windows 安装程序并运行，按安装向导操作。FVP 二进制文件通常安装在类似 ``C:\Program Files\ARM\FVP_Corstone_SSE-300\models\Win64_VC2019`` 的路径下。

               .. note::

                  如果尚未安装 ``python39.dll``，可能需要先安装它。

               **步骤 2：** 打开新的 PowerShell 窗口并验证安装：

               .. code-block:: console

                  .\FVP_Corstone_SSE-300.exe --version

            .. group-tab:: Zephyr Docker CI

               也可以使用 `Zephyr Docker CI 镜像 <https://github.com/zephyrproject-rtos/docker-image>`_，无需手动安装 FVP。这是 Zephyr 官方 CI 容器，已包含 Corstone-300、Corstone-320 FVP 以及其他全部 Zephyr 构建依赖，无需另行安装 FVP。

               **步骤 1：** 拉取镜像：

               .. code-block:: console

                  docker pull ghcr.io/zephyrproject-rtos/zephyr-build:main

               **步骤 2：** 启动容器，并挂载 Zephyr 工作区和 Zephyr SDK：

               .. code-block:: console

                  docker run -it --rm \
                    -v $HOME/zephyrproject:$HOME/zephyrproject \
                    -v $HOME/zephyr-sdk-0.17.4:$HOME/zephyr-sdk-0.17.4 \
                    -w $HOME/zephyrproject \
                    -e HOME=$HOME \
                    -e ZEPHYR_SDK_INSTALL_DIR=$HOME/zephyr-sdk-0.17.4 \
                    --user root \
                    --entrypoint /bin/bash \
                    ghcr.io/zephyrproject-rtos/zephyr-build:main

               .. note::

                  SDK 版本 ``0.17.4`` 可能变化。请替换为实际安装的版本，或使用以下通用形式：

                  .. code-block:: console

                     docker run -it --rm \
                       -v $HOME/zephyrproject:$HOME/zephyrproject \
                       -v $HOME/zephyr-sdk-<version>:$HOME/zephyr-sdk-<version> \
                       -w $HOME/zephyrproject \
                       -e HOME=$HOME \
                       -e ZEPHYR_SDK_INSTALL_DIR=$HOME/zephyr-sdk-<version> \
                       --user root \
                       --entrypoint /bin/bash \
                       ghcr.io/zephyrproject-rtos/zephyr-build:main

               **步骤 3：** 在容器中激活 Zephyr 虚拟环境：

               .. code-block:: console

                  source $HOME/zephyrproject/.venv/bin/activate

               **步骤 4：** 验证 FVP 可用：

               .. code-block:: console

                  FVP_Corstone_SSE-300 --version
                  FVP_Corstone_SSE-320 --version

               随后便可在容器内，按照下文构建步骤执行任意 ``west build`` 命令。

      .. rubric:: Prepare the Ethos-U55 PTE model

      在 ExecuTorch 中，``.pte`` 是序列化程序文件，也是向边缘和移动设备部署 PyTorch 模型所用的最终二进制格式。如何通过 Arm Ethos-U 后端导出自己的 PyTorch 模型，并将其转换为后端表示，详见 `使用 ExecuTorch Export <https://docs.pytorch.org/executorch/stable/using-executorch-export.html>`_。

      这里使用最小化的 ``add`` 模型，接收两个张量并逐元素相加。其唯一目的是验证完整 ExecuTorch 流程，从模型编译一直到通过 Ethos-U NPU 执行端侧推理，是否正确工作。预期每个输出元素都等于 ``2 + 2 = 4``。

      在 Zephyr 根目录，例如 ``~/zephyrproject``，运行：

      .. tabs::

         .. group-tab:: Ubuntu/macOS

            .. code-block:: console

               cd ~/zephyrproject
               python -m modules.lib.executorch.examples.arm.aot_arm_compiler \
                 --model_name=modules/lib/executorch/examples/arm/example_modules/add.py \
                 --quantize --delegate -t ethos-u55-128 --output=add_u55_128.pte

         .. group-tab:: Windows

            .. code-block:: console

               cd ~/zephyrproject
               python -m modules.lib.executorch.examples.arm.aot_arm_compiler `
                 --model_name=modules/lib/executorch/examples/arm/example_modules/add.py `
                 --quantize --delegate -t ethos-u55-128 --output=add_u55_128.pte

      ``--delegate`` 指示 ``aot_arm_compiler`` 使用 Ethos-U 后端，``-t ethos-u55-128`` 选择 Ethos-U 变体及乘加单元数量。这些设置必须与硬件或 FVP 配置匹配。

      .. rubric:: Build and Run

      在 Zephyr 根目录 ``~/zephyrproject`` 中运行：

      .. tabs::

         .. group-tab:: Ubuntu/macOS

            .. code-block:: console

               cd ~/zephyrproject
               west build -p auto -b mps3/corstone300/fvp \
                 modules/lib/executorch/zephyr/samples/hello-executorch \
                 -t run -- -DET_PTE_FILE_PATH=add_u55_128.pte

         .. group-tab:: Windows

            .. code-block:: console

               cd $env:USERPROFILE\zephyrproject
               west build -p auto -b mps3/corstone300/fvp `
                 modules/lib/executorch/zephyr/samples/hello-executorch -t run -- `
                 "-DET_PTE_FILE_PATH=$PWD\add_u55_128.pte"

   .. group-tab:: 纯 CPU 推理

      .. rubric:: Prepare the model

      这里使用为 Cortex-M55 导出的最小化 ``add`` 模型。示例使用 ExecuTorch Arm AOT 编译器当前提供的纯 CPU 目标，支持的目标可能随时间变化。如果运行时支持所需算子，某些其他 Cortex-M 开发板也可能运行生成的 ``.pte``，但必须逐板验证兼容性。在 Zephyr 根目录，例如 ``~/zephyrproject``，运行：

      .. code-block:: console

         python -m modules.lib.executorch.examples.arm.aot_arm_compiler \
           --model_name=modules/lib/executorch/examples/arm/example_modules/add.py \
           --quantize --target=cortex-m55+int8 --output=add_m55.pte

      .. rubric:: Build and Run

      将 ``<board>`` 替换为目标开发板。对于下文已验证开发板以外的目标，必须在实际目标上验证兼容性。

      .. code-block:: console

         west build -b <board> modules/lib/executorch/zephyr/samples/hello-executorch \
           -t run -- -DET_PTE_FILE_PATH=add_m55.pte

      .. note::

         本示例已使用同一个 ``add_m55.pte`` 产物，在以下开发板上测试：

         - **STM Nucleo-N657X0-Q** （``nucleo_n657x0_q``）：

           .. code-block:: console

              west build -b nucleo_n657x0_q \
                modules/lib/executorch/zephyr/samples/hello-executorch \
                -- -DET_PTE_FILE_PATH=add_m55.pte

         - **nRF5340 DK** （``nrf5340dk/nrf5340/cpuapp``）：

           .. code-block:: console

              west build -b nrf5340dk/nrf5340/cpuapp \
                modules/lib/executorch/zephyr/samples/hello-executorch \
                -- -DET_PTE_FILE_PATH=add_m55.pte

      构建后烧录到硬件：

      .. code-block:: console

         west flash

预期运行输出
============

.. code-block:: console

   I [executorch:arm_executor_runner.cpp:450 main()] Model executed successfully.
   I [executorch:arm_executor_runner.cpp:457 main()] Model outputs:
   I [executorch:arm_executor_runner.cpp:464 main()]   output[0]: tensor scalar_type=Float numel=5
   I [executorch:arm_executor_runner.cpp:481 main()]     [0] = 4.000000
   I [executorch:arm_executor_runner.cpp:481 main()]     [1] = 4.000000
   I [executorch:arm_executor_runner.cpp:481 main()]     [2] = 4.000000
   I [executorch:arm_executor_runner.cpp:481 main()]     [3] = 4.000000
   I [executorch:arm_executor_runner.cpp:481 main()]     [4] = 4.000000
   I [executorch:arm_executor_runner.cpp:499 main()] SUCCESS: Program complete, exiting.

``output`` 值为 ``4.000000`` 表明模型已在设备上成功运行。每个元素都是通过 ExecuTorch 的 Ethos-U NPU 或 CPU 后端计算 ``2 + 2`` 的结果。

ExecuTorch 的 Zephyr 支持正在积极开发，更多复杂而有趣的示例应用也在准备中。可在此跟踪进展并查找新示例：`ExecuTorch Zephyr 示例 <https://github.com/pytorch/executorch/tree/main/zephyr/samples>`_。

参考资料
********

- `ExecuTorch <https://github.com/pytorch/executorch>`_ —— PyTorch 的端侧推理运行时。
- `ExecuTorch 工作原理 <https://docs.pytorch.org/executorch/stable/intro-how-it-works.html>`_ —— ExecuTorch 工作流程入门。
- `入门架构 <https://docs.pytorch.org/executorch/stable/getting-started-architecture.html>`_ —— ExecuTorch 的高层架构概览。
- `Arm FVP <https://developer.arm.com/Tools%20and%20Software/Fixed%20Virtual%20Platforms/IoT%20FVPs>`_ —— 用于 Cortex-M 和 Ethos-U 仿真的固定虚拟平台。
- `FVPs-on-Mac <https://github.com/Arm-Examples/FVPs-on-Mac.git>`_ —— 使 Arm FVP 可在 macOS 上运行的 Docker 封装。
- `Arm Ethos-U NPU 系列 <https://www.arm.com/products/silicon-ip-cpu?families=ethos%20npus>`_ —— 用于高效端侧 AI 推理的 Arm NPU IP。
- `使用 ExecuTorch Export <https://docs.pytorch.org/executorch/stable/using-executorch-export.html>`_ —— ExecuTorch 模型导出与后端转换指南。
- `Zephyr Docker CI 镜像 <https://github.com/zephyrproject-rtos/docker-image>`_ —— Zephyr 官方 CI 容器，预装 FVP 和构建依赖。
- `hello-executorch 示例 <https://github.com/pytorch/executorch/tree/main/zephyr/samples/hello-executorch>`_ —— 本指南使用的最小化 Zephyr ExecuTorch 示例。
