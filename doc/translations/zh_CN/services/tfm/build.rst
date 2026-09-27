.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _tfm_build_system:

TF-M 构建系统
#############

构建有效的 ``_ns`` 开发板目标时，TF-M 会在后台构建，并与 Zephyr 非安全应用链接。大多数情况下无需了解 TF-M 的构建系统，下面的命令会构建一对 TF-M 与 Zephyr 镜像，并在 qemu 中运行，无需任何额外步骤：

   .. code-block:: bash

     $ west build -p auto -b mps2/an521/cpu0/ns samples/tfm_integration/psa_protected_storage/ -t run

不过，这里会介绍该构建过程的输出以及某些关键步骤，因为你需要理解这些输出并与之交互，还要在部署安全和非安全镜像之前处理它们的签名。

TF-M 构建生成的镜像
*******************

TF-M 构建系统会创建以下可执行文件：

* tfm_s - TF-M 安全固件
* tfm_ns - TF-M 非安全应用（仅用于回归测试）。
* bl2 - TF-M MCUboot（如果启用）

对于其中每一个，它都会创建 .bin、.hex、.elf 和 .axf 文件。

TF-M 构建系统还会创建 tfm_s 和 tfm_ns 的已签名变体，以及一个将二者合并的文件：

* tfm_s_signed
* tfm_ns_signed
* tfm_s_ns_signed

对于其中每一个，只会创建 .bin 文件。

除运行 TF-M 回归测试套件外，TF-M 非安全应用都会被弃用，改用 Zephyr 非安全应用。

Zephyr 构建系统通常会对 tfm_s 和 Zephyr 非安全应用两者自行签名。详见下文。

“tfm” 目标包含所有这些路径的属性。例如，下面的内容会解析为 ``<path>/tfm_s.hex``：

   .. code-block::

      $<TARGET_PROPERTY:tfm,TFM_S_HEX_FILE>

有关所有属性的概览，请参见 tfm 模块顶层的 CMakeLists.txt 文件。

镜像签名
********

当 :kconfig:option:`CONFIG_TFM_BL2` 设置为 ``y`` 时，TF-M 会使用安全 bootloader（BL2），固件镜像必须使用私钥签名。更新期间，bootloader 会使用存储在安全 bootloader 固件镜像中的相应公钥来校验固件镜像。

默认情况下，使用 ``<tfm-dir>/bl2/ext/mcuboot/root-rsa-3072.pem`` 为安全镜像签名，使用 ``<tfm-dir>/bl2/ext/mcuboot/root-rsa-3072_1.pem`` 为非安全镜像签名。这些默认的 .pem 密钥可以（而且 **应该**）通过 :kconfig:option:`CONFIG_TFM_KEY_FILE_S` 和 :kconfig:option:`CONFIG_TFM_KEY_FILE_NS` 配置标志覆盖。

为满足 `PSA Certified Level 1`_ 的要求，**你必须使用新的密钥对替换默认的 .pem 文件！**

要生成新的公钥/私钥对，请运行以下命令：

   .. code-block:: bash

     $ imgtool keygen -k root-rsa-3072_s.pem -t rsa-3072
     $ imgtool keygen -k root-rsa-3072_ns.pem -t rsa-3072

然后，你可以将新的 .pem 文件放在其他位置（例如 Zephyr 应用文件夹），并在 ``prj.conf`` 文件中通过 :kconfig:option:`CONFIG_TFM_KEY_FILE_S` 和 :kconfig:option:`CONFIG_TFM_KEY_FILE_NS` 配置标志引用它们。

   .. warning::

     务必将私钥文件保存在安全可靠的位置！如果丢失该密钥文件，你将无法为今后的任何固件镜像签名，也无法再在现场更新你的设备！

内置签名脚本运行后，会创建一个 ``tfm_merged.hex`` （以及 ``tfm_merged.bin``）文件，其中包含全部三个二进制文件：bl2、tfm_s 和 zephyr 应用。随后可以将这些文件烧录到开发板，或在 QEMU 中运行。

.. _PSA Certified Level 1:
  https://www.psacertified.org/security-certification/psa-certified-level-1/
.. _PSA Certified Firmware Update API:
  https://arm-software.github.io/psa-api/fwu/

输出文件
********

Zephyr TF-M 构建完成后，会生成以下输出文件：

.. csv-table:: TF-M 输出文件
  :header: 文件名, 创建来源, bootloader 标志, 用法

  ``tfm_s_signed.{hex/bin}``, "TF-M 安全", 已签名, OTA 升级（:kconfig:option:`CONFIG_TFM_MCUBOOT_IMAGE_NUMBER` == 2）
  ``zephyr_ns_signed.{hex/bin}``, "Zephyr 非安全", Signed, OTA Upgrades (:kconfig:option:`CONFIG_TFM_MCUBOOT_IMAGE_NUMBER` == 2)
  ``tfm_s_zephyr_ns_signed.{hex/bin}``, "TF-M 安全、Zephyr 非安全", Signed, OTA 升级（:kconfig:option:`CONFIG_TFM_MCUBOOT_IMAGE_NUMBER` == 1）
  ``tfm_merged.{hex/bin}``, "bootloader、TF-M 安全、Zephyr 非安全", "已签名、已确认", "量产烧录，由 ``west flash`` 执行烧写"

自定义 CMake 参数
=================

在使用 TF-M 构建 Zephyr 应用时，可能需要控制传递给 TF-M 构建的 CMake 参数。

Zephyr TF-M 构建提供了若干用于控制构建的 Kconfig 选项，但并未涵盖 TF-M 构建系统所支持的全部 CMake 参数。

可以使用 ``zephyr_property_target`` 上的 ``TFM_CMAKE_OPTIONS`` 属性向 TF-M 构建系统传递自定义 CMake 参数。

要向 TF-M 构建系统传递 CMake 参数 ``-DFOO=bar``，请在你的 CMakeLists.txt 文件中加入以下 CMake 代码片段。

   .. code-block:: cmake

     set_property(TARGET zephyr_property_target
                  APPEND PROPERTY TFM_CMAKE_OPTIONS
                  -DFOO=bar
     )

.. note::
   ``TFM_CMAKE_OPTIONS`` 是一个列表，因此可以追加多个选项。此外还支持 CMake 生成器表达式，例如 ``$<1:-DFOO=bar>``

由于 ``TFM_CMAKE_OPTIONS`` 是列表参数，它在传递给 TF-M 构建系统之前会被展开。因此，带列表参数的选项必须正确转义，以免被当作列表展开。

   .. code-block:: cmake

     set_property(TARGET zephyr_property_target
                  APPEND PROPERTY TFM_CMAKE_OPTIONS
                  -DFOO="bar\\\;baz"
     )

占用空间与内存使用
******************

构建系统提供了一些目标，用于查看和分析生成镜像中的 RAM 和 ROM 使用情况。这些工具针对最终镜像运行，提供 RAM 和 ROM 中符号大小及代码占用信息。有关这些工具的更多信息，请参见 :ref:`footprint_tools`

使用 ``tfm_ram_report`` 获取 TF-M 安全固件（tfm_s）的 RAM 报告。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: mps2/an521/cpu0/ns
    :goals: tfm_ram_report

使用 ``tfm_rom_report`` 获取 TF-M 安全固件（tfm_s）的 ROM 报告。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: mps2/an521/cpu0/ns
    :goals: tfm_rom_report

如果启用了 TF-M MCUboot，可使用 ``bl2_ram_report`` 获取其 RAM 报告。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: mps2/an521/cpu0/ns
    :goals: bl2_ram_report

如果启用了 TF-M MCUboot，可使用 ``bl2_rom_report`` 获取其 ROM 报告。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: mps2/an521/cpu0/ns
    :goals: bl2_rom_report
