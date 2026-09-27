.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

TF-M 要求
#########

以下是一些可以与 TF-M 一起使用的开发板：

.. list-table::
   :header-rows: 1

   * - 开发板
     - NSPE 开发板名称
   * - :ref:`mps2_an521_board`
     - ``mps2/an521/cpu0/ns`` （支持 qemu）
   * - :zephyr:board:`mps3`
     -
       - ``mps3/corstone300/fvp/ns`` （支持 armfvp）
       - ``mps3/corstone310/fvp/ns`` （支持 armfvp）
   * - :zephyr:board:`mps4`
     -
       - ``mps4/corstone315/fvp/ns`` （支持 armfvp）
       - ``mps4/corstone320/fvp/ns`` （支持 armfvp）
   * - :zephyr:board:`bl5340_dvk`
     - ``bl5340_dvk/nrf5340/cpuapp/ns``
   * - :zephyr:board:`lpcxpresso55s69`
     - ``lpcxpresso55s69_ns``
   * - :zephyr:board:`nrf9160dk_nrf9160 <nrf9160dk>`
     - ``nrf9160dk/nrf9160/ns``
   * - :zephyr:board:`nrf5340dk`
     - ``nrf5340dk/nrf5340/cpuapp/ns``
   * - :zephyr:board:`b_u585i_iot02a`
     - ``b_u585i_iot02a/stm32u585xx/ns``
   * - :zephyr:board:`nucleo_l552ze_q`
     - ``nucleo_l552ze_q/stm32l552xx/ns``
   * - :zephyr:board:`stm32l562e_dk`
     - ``stm32l562e_dk/stm32l562xx/ns``
   * - :zephyr:board:`v2m_musca_b1`
     - ``v2m_musca_b1/musca_b1/ns``

要确认某块开发板的输出支持 TF-M，请检查该开发板的默认配置中是否将 :kconfig:option:`CONFIG_TRUSTED_EXECUTION_NONSECURE` 设置为 ``y``。

软件要求
********

构建 TF-M 二进制文件时所需的 Python 模块列在 TF-M 仓库的 ``tools/requirements.txt`` 中。

你可以通过以下命令安装：

   .. code-block:: bash

      $ pip3 install -r "$(west list trusted-firmware-m -f '{abspath}')/tools/requirements.txt"

TF-M 的签名工具会使用它们来准备固件镜像，以供 bootloader 校验。

为 QEMU 生成二进制文件，以及在特定平台上合并已签名的安全和非安全二进制文件，这一过程中的一部分也需要使用 ``srec_cat`` 工具。

在 Linux 上可以通过以下命令安装：

   .. code-block:: bash

      $ sudo apt-get install srecord

在 OS X 上则通过以下命令安装：

   .. code-block:: bash

      $ brew install srecord

对于 Windows 系统，请确保系统路径中有该工具的副本。例如参见：`SRecord for Windows <https://sourceforge.net/projects/srecord/files/srecord-win32>`_
