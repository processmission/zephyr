.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _twister_script:

测试运行器（Twister）
#####################

Twister 扫描 Git 仓库中的测试应用并尝试执行。默认会在开发板定义文件中标记为默认的开发板上构建每个测试应用。

默认选项会在指定的一组开发板上构建大多数测试应用；如果被测架构或配置提供仿真环境，还会在其中运行。

由于执行覆盖有限，Twister 无法保证本地改动在完整构建环境中成功。但它会针对不同开发板和配置构建示例及测试，提供足够的检查，帮助保持整个代码树可构建。

使用至少一个 ``-v`` 选项时，Twister 控制台会显示每个测试应用的运行方式（qemu、native_sim 等），或是否仅构建了二进制文件。测试的最终 :ref:`状态 <twister_statuses>` 也会记录在 ``twister.json`` 等报告中。Twister 只构建而不运行测试的原因包括：

- 测试的 ``.yaml`` 配置中标记了 ``build_only: true``。
- 测试配置定义了 ``harness``，但你没有对应测试适配器或尚未配置。
- 目标设备未连接，无法烧录。
- 你或上层自动化工具使用 ``--build-only`` 调用了 Twister。

在本地代码树中运行 Twister 的步骤如下：

.. code-block:: console

   $ west twister

.. note::

   本文示例使用 :ref:`west <west>` 扩展命令 ``west twister``，在所有主机操作系统上的用法相同。以下调用等效：

   * ``west twister ...`` （推荐）。
   * ``python .\scripts\twister ...`` （Windows）：直接调用脚本，需要先配置 Zephyr 环境（``source zephyr-env.sh`` 或 ``zephyr-env.cmd``）。

   所有调用形式接受相同的命令行选项。

要在一个或多个指定平台上运行测试，可使用 ``--platform`` 平台过滤选项，套件只会在这些平台上构建或运行。它也支持同一开发板的不同修订版本，可用 ``--platform board@revision`` 测试指定版本。

使用 ``west twister --help`` 可查看支持的命令行选项，完整列表见 :ref:`twister_commandline_options`。

以下页面介绍更多 Twister 主题：

.. toctree::
   :maxdepth: 1

   commandline
   pytest
   twister_statuses
   twister_blackbox

.. _twister_board_configuration:

开发板配置
**********

针对指定开发板构建测试，并在真实硬件或 QEMU 等仿真环境中执行部分测试，需要开发板配置文件。其格式足够通用，也可用于其他需要开发板清单的任务，提供通常只有构建时才能获得的开发板及配置信息。

开发板元数据文件位于开发板目录，采用 YAML 格式。下例包含实现该开发板最佳测试覆盖所需的数据：

.. code-block:: yaml

  identifier: frdm_k64f
  name: NXP FRDM-K64F
  type: mcu
  arch: arm
  toolchain:
    - zephyr
    - gnuarmemb
  supported:
    - arduino_gpio
    - arduino_i2c
    - netif:eth
    - adc
    - i2c
    - nvs
    - spi
    - gpio
    - usb_device
    - watchdog
    - can
    - pwm
  testing:
    default: true


identifier:
  与构建系统中的开发板定义匹配的字符串。构建时也使用此字符串，例如调用 ``west build`` 或 ``cmake``：

  .. code-block:: console

     # with west
     west build -b reel_board
     # with cmake
     cmake -DBOARD=reel_board ..

name:
  开发板在宣传资料中的实际名称。
vendor:
  开发板厂商，供测试场景过滤器 ``vendor_allow`` 和 ``vendor_exclude`` 使用。
tier:
  可选整数，表示开发板支持等级，用于报告及按支持程度分组平台。
type:
  开发板或配置类型，为 ``mcu``、``qemu``、``sim``、``unit`` 或 ``native`` 之一。
simulation:
  用于仿真平台的模拟器，例如 qemu。

  .. code-block:: yaml

      simulation:
        - name: qemu
        - name: armfvp
          exec: FVP_Some_Platform
        - name: custom
          exec: AnotherBinary

  默认使用 simulation 数组的首项执行测试，可通过 ``--simulation <simulation_name>`` 选择其他模拟器。``exec`` 属性可选。设置后若所需模拟器不可用，测试仅构建；未设置且模拟器不可用时，测试运行失败。模拟器名称必须匹配 ``SUPPORTED_EMU_PLATFORMS`` 中的一项。
arch:
  开发板架构
toolchain:
  可构建该开发板的受支持工具链列表，应匹配命令行构建时 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 的某个值。除非传入 ``--force-toolchain``，否则 Twister 会过滤掉工具链不在此列表的实例。此列表只说明哪些工具链 *可以* 构建该板，不负责选择工具链；见 :ref:`twister_toolchain_selection`。
preferred_toolchain:
  没有其他选项指定工具链时，Twister 应为此平台使用的工具链。适用于名义上支持多种工具链、但应使用特定工具链测试的开发板。见 :ref:`twister_toolchain_selection`。
build_toolchains:
  可选工具链列表，分配给此平台的每个测试都要用其中各工具链构建。Twister 为每个工具链创建独立测试实例和构建目录，而非只为平台选择一种工具链。例如，同时用 GCC 和 Clang 构建 ``native_sim`` 上的全部测试：

  .. code-block:: yaml

      build_toolchains:
        - host/gnu
        - host/llvm

  由于会成倍增加构建时间，通常不应将其放入开发板定义，而只在 CI 使用的 :ref:`Twister 配置文件 <twister_test_config>` 中启用 ``build_toolchains``。见 :ref:`twister_toolchain_selection`。
ram:
  开发板可用 RAM，单位为 KB，用于匹配测试场景需求。未指定时默认 128KB。
flash:
  开发板可用 FLASH，单位为 KB，用于匹配测试场景需求。未指定时默认 512KB。
sysbuild: [True|False]（默认 False）
  为 true 时，默认使用 :ref:`sysbuild <sysbuild>` 构建此平台的应用。
twister: [True|False]（默认 True）
  为 false 时，Twister 完全忽略此平台，不会在其上构建或运行测试。
supported:
  开发板支持的特性列表，可用单个词表示特性，也可表示某特性类别的变体。例如：

  .. code-block:: yaml

        supported:
          - pci

  这表示开发板支持 PCI。可让测试场景仅在这类开发板上构建或运行，或者：

  .. code-block:: yaml

        supported:
          - netif:eth
          - sensor:bmi16

  测试场景可依赖 'eth' 以仅测试以太网，或依赖 'netif' 以在任意带网络接口的开发板上运行。

testing:
  与测试有关的关键字，用于充分覆盖此开发板的特性。

  .. _twister_default_testing_board:

  binaries:
    为设备测试保留的自定义二进制文件列表。
  default: [True|False]:
    表示默认开发板，具有最高测试优先级，不带额外参数运行简化的 Twister 时也会覆盖它。
  ignore_tags:
    不尝试构建带有这些标签的测试，因此也不会运行。
  only_tags:
    在指定平台上只执行带有这些标签的测试。
  timeout_multiplier: <float>（默认 1）
    .. _twister_board_timeout_multiplier:

    将每个测试场景的超时时间乘以指定比率，可仅调整特定平台的超时。适用于本身较慢的平台，例如低功耗但较慢的 CPU，或运行较慢的指令精确仿真平台。

  flash_before: [True|False]（默认 False）
    使用 pytest/shell 适配器进行硬件测试时，在打开串口前烧录设备。这可避免部分开发板烧录时串口断开的问题，例如烧录期间会复位的 USB CDC 设备。

  renode:
    Renode 模拟器配置，支持两个键：``uart`` 指定适配器连接的 UART 外设，例如 ``sysbus.uart0``；``resc`` 指定设置仿真机器的 Renode 脚本（``.resc``）。

env:
  环境变量列表。Twister 检查这些变量是否全部已设置，否则跳过平台。用户可借此定义仅在所需软件或硬件存在时才使用的平台，并通过环境变量通知 Twister。

variants:
  开发板变体（限定符）名称到各变体覆盖值的映射。每个条目本身也是平台定义，可覆盖上述任意键，其余值继承顶层定义。

.. _twister_toolchain_selection:

工具链选择
**********

影响测试构建工具链的选项分为三类：*选择* 工具链的选项、*过滤* 工具链不可用实例的选项，以及将测试 *扩展* 为多个构建的选项。

Twister 先调用 ``cmake/verify-toolchain.cmake`` 确定本次运行的默认工具链，它遵循 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 环境变量。运行开始时以 ``Using '<toolchain>' toolchain variant.`` 报告此值。

对于每个测试场景与平台组合，按以下顺序选择首个适用项：

#. 测试场景的 ``integration_toolchains``，若已设置，则用列出的每种工具链构建一次。
#. 平台在开发板配置或 :ref:`Twister 配置文件 <twister_test_config>` 中的 ``build_toolchains``，若已设置，则用每种工具链构建一次。
#. 对于 ``posix`` 和 ``unit`` 平台，若运行默认值为 ``host/llvm``，则使用 ``host/llvm``；否则使用 ``host/gnu``。
#. 平台的 ``preferred_toolchain``，如果已设置。
#. 上述运行默认值；无法确定时使用 ``zephyr``。

注意，:envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 只改变列表最后一项的运行默认值，不会覆盖平台的 ``preferred_toolchain``、``build_toolchains`` 或场景的 ``integration_toolchains``。

选定工具链后，生成的测试实例仍可能被过滤：

* 若工具链不在平台的 ``toolchain`` 支持列表中，实例被过滤。``--force-toolchain`` 可禁用检查，无条件使用已选工具链。比较也接受 ``/`` 前的部分，因此 ``host/gnu`` 可匹配列出 ``host`` 的平台。
* 场景的 ``toolchain_allow`` 和 ``toolchain_exclude`` 按已选工具链过滤实例。

``integration_toolchains`` 和 ``build_toolchains`` 为每种工具链生成一个实例，因此会成倍增加构建时间。所以 ``build_toolchains`` 通常不放入开发板配置，仅在 CI 配置文件中启用。

.. _twister_tests_long_version:

测试
****

通过应用项目目录中的 ``tests.yaml`` 检测测试，``sample.yaml`` 和 ``testcase.yaml`` 支持已弃用。此配置文件的 ``tests:`` 部分可包含一个或多个条目，每项标识一个测试场景。

.. _twister_test_project_diagram:

.. figure:: figures/twister_test_project.svg
   :alt: Twister and a Test application project.
   :figclass: align-center

   Twister 与测试应用项目。


测试应用配置使用 YAML 语法，与示例具有相同结构。

测试场景是一组在场景条目中定义的条件和变量，测试套件将在这些条件下构建和执行。

测试套件是一组用于验证软件是否满足特定要求的测试用例。套件内的用例彼此相关，或需要一同执行。

测试场景、套件和用例名称必须遵循以下基本规则：

#. 测试场景标识为不含空格或特殊字符的字符串，允许字母数字及 [\_=]，由多个以点（``.``）分隔的部分组成。

#. 每个测试场景标识以章节名开始，后接用点（``.``）分隔的子章节名。例如，覆盖内核信号量的场景应以 ``kernel.semaphore`` 开头。

#. 所有测试场景名称在 Twister 执行范围内必须唯一。

#. 测试套件的完整规范名称为：``<Test Application Project path>/<Test Scenario identifier>``

#. 根据套件实现，其用例标识至少由以点（``.``）分隔的 **三个部分** 组成：

   * **Ztest 测试**：对应 ``testcase.yaml`` 中的场景标识、Ztest 套件名及 Ztest 测试名，即 ``<Test Scenario identifier>.<Ztest suite name>.<Ztest test name>``。

   * **独立测试和示例**：对应 ``tests.yaml`` 中的场景标识，最后一段表示独立用例名称，例如 ``debug.coredump.logging_backend``。


以下配置示例包含本文介绍的若干选项。


  .. code-block:: yaml

        tests:
          bluetooth.gatt:
            build_only: true
            platform_allow:
              - qemu_cortex_m3
              - qemu_x86
            tags:
              - bluetooth
          bluetooth.gatt.br:
            build_only: true
            extra_args:
              -CONF_FILE="prj_br.conf"
            filter: not CONFIG_DEBUG
            platform_exclude:
              -up_squared
            platform_allow:
              - qemu_cortex_m3 qemu_x86
            tags:
              - bluetooth


带测试的示例具有相同结构，另外包含示例及其演示内容的信息：

  .. code-block:: yaml

        sample:
          name: hello world
          description: Hello World sample, the simplest Zephyr application
        tests:
          sample.basic.hello_world:
            build_only: true
            tags:
              - tests
            min_ram: 16
          sample.basic.hello_world.singlethread:
            build_only: true
            extra_args: CONF_FILE=prj_single.conf
            filter: not CONFIG_BT
            tags:
              - tests
            min_ram: 16

YAML 的 ``tests:`` 字典中，每个场景条目以场景标识为键。

测试应用配置中的每个场景条目可定义以下键值对：

..  _test_config_args:

tags: <list of tags>（必填）
    场景的字符串标签集合，通常表示功能领域，也可用于其他目的。命令行调用可按标签过滤待运行测试。

skip: <True|False>（默认 False）
    无条件跳过场景，例如可用于已损坏的测试。

slow: <True|False>（默认 False）
    除非命令行传入 ``--enable-slow`` 或 ``--enable-slow-only``，否则不运行此场景。适用于仅在每日构建等特定情况下运行的耗时场景。这些场景仍会编译。

extra_args: <list of extra arguments>
    构建或运行场景时，传给构建工具的附加参数。

    可通过命名空间仅对部分硬件应用 extra_args，目前支持架构、平台和模拟器：

    .. code-block:: yaml

        common:
          tags:
           - drivers
           - adc
        tests:
          test:
            depends_on: adc
          test_async:
            extra_args:
              - arch:x86:CONFIG_ADC_ASYNC=y
              - platform:qemu_x86:CONFIG_DEBUG=y
              - platform:mimxrt1060_evk:SHIELD=rk043fn66hs_ctg
              - simulation:qemu:CONFIG_MPU=y

extra_configs: <list of extra configurations>
    构建或运行场景时，与主 prj.conf 合并的附加配置选项，例如：

    .. code-block:: yaml

        common:
          tags:
            - drivers
            - adc
        tests:
          test:
            depends_on: adc
          test_async:
            extra_configs:
              - CONFIG_ADC_ASYNC=y

    可通过命名空间仅对部分硬件应用配置，目前支持架构和平台：

    .. code-block:: yaml

        common:
          tags:
            - drivers
            - adc
        tests:
          test:
            depends_on: adc
          test_async:
            extra_configs:
              - arch:x86:CONFIG_ADC_ASYNC=y
              - platform:qemu_x86:CONFIG_DEBUG=y


extra_conf_files: <list of configuration files>
    合并到构建中的附加 Kconfig 片段文件，可代替在 ``extra_args`` 中传入 ``CONF_FILE=``。``common`` 与场景中的条目会拼接。配置文件应优先使用此字段而非 ``extra_args``。

extra_overlay_confs: <list of overlay configuration files>
    合并到构建中的附加 Kconfig overlay 片段，可代替在 ``extra_args`` 中传入 ``OVERLAY_CONFIG=``。``common`` 与场景中的条目会拼接。

extra_dtc_overlay_files: <list of devicetree overlay files>
    应用到构建的附加设备树 overlay 文件，可代替在 ``extra_args`` 中传入 ``DTC_OVERLAY_FILE=``。``common`` 与场景中的条目会拼接。

build_only: <True|False>（默认 False）
    为 true 时，即使平台支持运行，Twister 也不会尝试执行测试。

    此关键字仅用于验证代码能否构建的测试。``build_only`` 测试不应在任何环境中运行，也不应测试功能，只验证代码可构建。

    此选项常用于检查驱动（例如传感器驱动）是否在 Zephyr 中正确启用且可构建，不应用来验证驱动功能。

build_on_all: <True|False>（默认 False）
    为 true 时，尝试在所有可用平台构建场景，主要供 CI 扩大覆盖。新测试不要使用此标志。

depends_on: <list of features>
    开发板或平台可声明支持的特性。此选项使测试仅在提供相应特性的平台上启用。

levels: <list of levels>
    此测试所属的测试级别。定义级别后，可通过 ``--level <level name>`` 命令行选项选择。

min_ram: <integer>
    估算构建和运行测试所需的最小 RAM，单位为 KB，与开发板元数据比较。

min_flash: <integer>
    估算构建和运行测试所需的最小 ROM，单位为 KB，与开发板元数据比较。

.. _twister_test_case_timeout:

timeout: <number of seconds>
    测试允许运行的时长，超过后自动终止，默认 60 秒。

arch_allow: <list of arches, such as x86, arm, arc>
    仅允许此测试场景运行的架构集合。

arch_exclude: <list of arches, such as x86, arm, arc>
    此测试场景不得运行的架构集合。

toolchain_allow: <list of toolchain variants>
    仅允许此场景使用的工具链变体集合。工具链为本次运行配置的值，见 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`。使用其他工具链构建的平台将被过滤。

toolchain_exclude: <list of toolchain variants>
    此测试场景不得使用的工具链变体集合。

vendor_allow: <list of vendors>
    仅允许此场景运行的平台厂商集合。厂商在开发板定义中声明。关联这些厂商的开发板将被纳入，其他开发板及未声明厂商的开发板均排除。

vendor_exclude: <list of vendors>
    此场景不得运行的平台厂商集合。厂商在开发板定义中声明，关联这些厂商的开发板将被排除。

platform_allow: <list of platforms>
    仅允许此场景运行的平台集合。不要因 CI 时间或资源限制而用它缩小测试或构建范围；只有测试或示例确实只能在这些平台运行时才使用。

integration_platforms: <YML list of platforms/boards>
    以 ``--integration`` 调用 Twister 时，将范围限制为列出的平台。如果目的是因时间或资源限制缩小范围，应使用此项而非 platform_allow。

integration_toolchains: <YML list of toolchain variants>
    将范围扩展到列出的所有工具链变体，按需增加测试维度。默认根据环境配置的工具链生成测试配置：

    测试场景 -> platforms1 -> toolchain1 测试场景 -> platforms2 -> toolchain1


    若平台支持多种工具链，且本次 Twister 运行时可用，可为每种工具链增加测试配置。例如，平台支持 ``toolchain1`` 和 ``toolchain2``，场景包含：

    .. code-block:: yaml

      integration_toolchains:
        - toolchain1
        - toolchain2

    则生成以下配置：

    测试场景 -> platforms1 -> toolchain1 测试场景 -> platforms1 -> toolchain2 测试场景 -> platforms2 -> toolchain1 测试场景 -> platforms2 -> toolchain2


    .. note::

      此功能始终生效，不限于使用 ``--integration`` 时。

    此选项优先于平台的 ``build_toolchains``。若希望扩展平台上每个测试的工具链范围，而非按场景设置，应使用 ``build_toolchains``。见 :ref:`twister_toolchain_selection`。

platform_exclude: <list of platforms>
    此场景不得运行的平台集合。

platform_type: <list of platform types>
    将场景限制到指定类型的平台。平台类型由开发板元数据的 ``type:`` 键声明，支持 ``mcu``、``qemu``、``sim``、``unit`` 和 ``native``。类型不在列表的平台会被过滤。

simulation_exclude: <list of simulators>
    此场景不得运行的模拟器集合。支持 ``qemu``、``simics``、``xt-sim``、``renode``、``nsim``、``mdb-nsim``、``tsim``、``armfvp``、``native`` 和 ``custom``。

extra_sections: <list of extra binary sections>
    计算大小时，若 Zephyr 二进制文件包含未预期的额外段，Twister 会报告错误，除非其名称列在此处。这些段不计入大小。

sysbuild: <True|False>（默认 False）
    使用 sysbuild 基础设施构建项目。测试过滤只使用主项目生成的设备树和 Kconfig。设备测试必须使用硬件映射或 west flash 将镜像加载到目标。此选项不支持 west flash 的 ``--erase``。使用不支持的选项会使需要 sysbuild 的测试被跳过。

harness: <string>
    ``testcase.yaml`` 中的 harness 关键字标识成功运行测试所需的 Twister 测试适配器。适配器由 Twister 提供并实现，部分仅为占位定义，尚未实现。

    适配器可视为 Twister 中用于判断测试是否满足通过条件的处理器。例如，需要键盘交互才能判断结果的测试会设置键盘适配器，但 Twister 目前尚未实现它。

    支持的测试适配器：

    - ztest
    - test
    - console
    - pytest
    - gtest
    - robot
    - ctest
    - shell
    - power
    - display_capture
    - script
    - bsim

    更多信息见 :ref:`twister_harnesses`。

platform_key: <list of platform attributes>
    测试常常只需构建和运行一次即可视为通过。例如某代码库依赖平台架构，对每种架构只需在一个平台通过测试，即足以验证代码。platform_key 属性支持这种选择方式。

    例如，以 (arch, simulation) 为键，确保每种架构和模拟器组合运行一次，这是常见用法：

    .. code-block:: yaml

      platform_key:
        - arch
        - simulation

    若平台（开发板）属性包含 SoC 名称、SoC 系列，甚至实现各外设接口的 IP 块集合，还能支持其他用法。例如，让 SPI 测试对每种不同 IP 块仅构建和运行一次。

harness_config: <harness configuration options>
    用于选择开发板或通过正则表达式处理通用控制台的额外适配器配置。配置可以声明支持的功能，此选项使测试仅在满足外部依赖的平台上运行。


    fixture: <string or list>
        指定场景对传感器等外部设备的依赖，并标识满足依赖的测试装置。自动化环境依据 ``fixture`` 关键字，在满足依赖的多个开发板中选择具体设备，取决于测试装置及开发板选择逻辑。名称示例包括 i2c_hts221、i2c_bme280、i2c_FRAM、ble_fw 和 gpio_loop。

    ztest_suite_repeat: <int>（默认 1）
        指定整个测试套件的重复次数。

    ztest_test_repeat: <int>（默认 1）
        指定套件内每个测试的重复次数。

    ztest_test_shuffle: <True|False>（默认 False）
        指定是否打乱套件内的测试顺序。设为 ``true`` 时按随机顺序执行。



    以下 YAML 示例包含 robot harness_config 选项。

    .. code-block:: yaml

        tests:
          robot.example:
            harness: robot
            harness_config:
              robot_testsuite: [robot file path]

    可通过列表指定多个测试套件。

    .. code-block:: yaml

        tests:
          robot.example:
            harness: robot
            harness_config:
              robot_testsuite:
                - [robot file path 1]
                - [robot file path 2]
                - [robot file path n]

    可以向 robotframework 传入一个或多个选项。

    .. code-block:: yaml

        tests:
          robot.example:
            harness: robot
            harness_config:
              robot_testsuite: [robot file path]
              robot_option:
                - --exclude tag
                - --stop-on-error

filter: <expression>
    在包含以下值的环境中求值表达式，以判断是否运行场景：

    .. code-block:: none

            { ARCH : <architecture>,
              PLATFORM : <platform>,
              <all CONFIG_* key/value pairs in the test's generated defconfig>,
              *<env>: any environment variable available
            }

    Twister 首先分析表达式，判断能否执行“有限”CMake 调用，即使用 package_helper CMake 脚本。

    包含“dt_*”项说明需要设备树。各种 DT 表达式的详细说明见 :ref:`twister_dt_filter_expressions`。

    包含“CONFIG*”项说明需要 Kconfig。若无其他类型的项，可不创建完整构建系统就进行过滤；否则需要完整 CMake 处理。

    表达式语言的语法如下：

    .. code-block:: antlr

        expression : expression 'and' expression
                   | expression 'or' expression
                   | 'not' expression
                   | '(' expression ')'
                   | symbol '==' constant
                   | symbol '!=' constant
                   | symbol '<' NUMBER
                   | symbol '>' NUMBER
                   | symbol '>=' NUMBER
                   | symbol '<=' NUMBER
                   | symbol 'in' list
                   | symbol ':' STRING
                   | symbol
                   ;

        list : '[' list_contents ']';

        list_contents : constant (',' constant)*;

        constant : NUMBER | STRING;

    对于 ``expression ::= symbol``，若符号定义为非空字符串，则结果为 ``true``。

    运算符优先级从低到高如下：

       * or（左结合）
       * and（左结合）
       * not（右结合）
       * 所有比较运算符（不结合）

    ``arch_allow``、``arch_exclude``、``platform_allow``、``platform_exclude`` 都是这些表达式的语法糖。例如：

    .. code-block:: none

        arch_exclude = x86 arc

    等同于：

    .. code-block:: none

        filter = not ARCH in ["x86", "arc"]

    ``:`` 运算符将字符串参数编译为正则表达式，只有环境中的符号值匹配时才返回真。例如，若 ``CONFIG_SOC="stm32f107xc"``，则

    .. code-block:: none

        filter = CONFIG_SOC : "stm.*"

    会匹配该值。

required_snippets: <list of needed snippets>
    Twister 支持需要 :ref:`代码片段 <snippets>` 的测试场景。与普通应用一样，可从 Zephyr 基础片段目录和测试应用目录查找片段。列出的片段会过滤开发板支持的测试：片段必须与开发板兼容，测试才能运行，它们不是可选的。

    以下 YAML 示例包含两个必需片段。

    .. code-block:: yaml

        tests:
          snippet.example:
            required_snippets:
              - cdc-acm-console
              - user-snippet-example

.. _required_applications:

required_applications: <list of required applications>（默认为空）
    指定当前测试运行前必须构建的测试应用列表，支持场景间共享已构建应用，让测试访问其他应用的构建产物。

    每个必需应用条目支持：

    - ``application``：测试场景标识，必填。
    - ``name``：``application`` 的弃用别名，为兼容仍可使用，但新配置应使用 ``application``。
    - ``platform``：目标平台，可选，默认当前测试的平台。
    - ``path``：Twister 搜索应用的目录，可选。可为绝对路径，或相对于测试 YAML 所在目录的路径。支持展开环境变量和 Zephyr 模块目录变量，见 :ref:`twister_module_dir_vars`。未指定时，在引用该应用的测试 YAML 所在目录搜索。

    Twister 自动发现并构建必需应用。若应用尚未加载，则在 ``path`` 指定目录查找；未设置 ``path`` 时，在引用该应用的测试 YAML 所在目录查找。复用构建目录时，例如使用 ``--no-clean``，也可从当前构建目录找到必需应用。

    工作方式：

    - Twister 先构建必需应用
    - 主测试应用等待必需应用完成
    - 必需应用的构建目录向测试适配器开放
    - 对于 pytest 适配器，构建目录通过 ``--required-build`` 传入，可由 ``required_build_dirs`` fixture 访问

    结合 ``build: false`` 时，当前场景完全跳过自身构建，使用第一个必需应用的构建产物作为镜像，适用于仅为其他位置构建的镜像提供测试适配器的场景。

    配置示例：

    .. code-block:: yaml

        tests:
          # Requires two applications, second one from a different path and with a fixed platform
          sample.required_app_demo:
            harness: pytest
            required_applications:
              - application: sample.shared_app
              - application: other.app
                path: ../other_app
                platform: native_sim
          # No self build, use the first required application as the test image
          sample.no_self_build:
            build: false
            harness: pytest
            required_applications:
              - application: sample.basic.helloworld
                path: $ZEPHYR_BASE/samples/hello_world
          sample.shared_app:
            build_only: true

    限制：

    - 不支持 ``--runtime-artifact-cleanup``，因为必须保留必需应用的构建产物供主测试使用。
    - 不支持 ``--subset``，因为必需应用及依赖它的测试可能分配到不同子集，导致执行测试时无法获得产物。

build: <True|False>（默认 True）
    为 false 时，场景跳过自身构建，使用 ``required_applications`` 首项的构建产物作为镜像，适用于仅为其他场景构建的镜像提供测试适配器的情况。

    约束：

    - ``required_applications`` 不得为空。
    - 支持基于 pytest 的适配器，例如 ``pytest``、``shell``，以及 ``bsim``。
    - 不支持 QEMU 平台。

expect_reboot: <True|False>（默认 False）
    通知 Twister，场景执行期间预计会重启。启用后，抑制套件或用例意外多次运行的警告。

modules: <list of module names>
    仅当工作区包含全部列出的 :ref:`模块 <modules>` 时才构建和运行场景。缺少必需模块的场景会被过滤。

type: <string>（默认 integration）
    场景的测试类型。针对 :ref:`unit_testing 开发板 <unit_testing_board>` 构建、无需完整 Zephyr 构建系统而在主机运行的单元测试，应设为 ``unit``。

testcases: <list of test case names>
    显式声明组成场景的用例名称列表。通常会自动检测，例如从 Ztest 源代码提取；仅无法自动检查的适配器才需设置。

ignore_faults: <True|False>（默认 False）
    测试运行期间，即使输出中检测到故障，也不将场景标记为失败。

ignore_qemu_crash: <True|False>（默认 False）
    测试运行期间即使 QEMU 崩溃，也不将场景标记为失败。

实际运行的场景取决于场景文件指令及命令行选项。若有疑问，可使用 ``-v``，或查看 :ref:`测试计划 <twister_output>` （:file:`testplan.json`），了解特定场景被过滤的原因。

要从文件加载参数，在文件名前加 ``+``，例如 ``+file_name``。文件内容应为一个或多个有效参数，用换行而非空白分隔。

多数日常使用无需任何参数。

.. _twister_module_dir_vars:

使用模块目录变量展开路径
========================

使用前会展开场景文件中的路径选项，例如 ``required_applications``、``harness_config: pytest_root``。除环境变量外，还展开与每个模块的 CMake 变量对应的 Zephyr 模块目录变量：

* ``ZEPHYR_<MODULE>_MODULE_DIR``：模块根目录的绝对路径。
* ``ZEPHYR_<MODULE>_MODULE_NAME``：模块名称。

``<MODULE>`` 转为大写，非字母数字字符替换为 ``_``，与 CMake 相同。例如 ``hal_nordic`` 模块对应 ``$ZEPHYR_HAL_NORDIC_MODULE_DIR``。未知引用保持不变。

管理测试超时
============

以下参数在不同层面控制测试超时：

* 每个场景的 ``timeout``，详见 :ref:`此处 <twister_test_case_timeout>`。
* 开发板配置的 ``timeout_multiplier``，详见 :ref:`此处 <twister_board_timeout_multiplier>`。
* Twister 的 ``--timeout-multiplier``，用于调整本次运行的超时。适用于仿真平台，因为仿真时间可能取决于主机速度、负载，或所选仿真方式，例如更慢的周期精确仿真。

场景总超时为上述三个参数的乘积。

.. _twister_dt_filter_expressions:

设备树过滤表达式
================

以“dt_*”开头的表达式在选择场景时，根据 compatible、别名、节点标签、节点属性和 chosen 节点等设备树属性过滤开发板。

.. note::

   这些表达式的源代码位于 :zephyr_file:`scripts/pylib/twister/expr_parser.py`。

表达式
------

``dt_compat_enabled(compat)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查是否存在已启用且具有指定 compatible 字符串（``compat``）的设备树节点。

**参数：**
   - ``compat``：要匹配的 compatible 字符串。

``dt_alias_exists(alias)``
~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查指定别名对应的设备树节点是否存在且已启用。

**参数：**
   - ``alias``：要匹配的别名，定义于 ``aliases`` 节点。

``dt_enabled_alias_with_parent_compat(alias, compat)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查是否存在已启用的别名节点，且其父节点具有指定 compatible 字符串。适用于可能没有自身 compatible 的节点，例如 ``gpio-leds`` 的子节点。

**参数：**
   - ``alias``：要匹配的别名，定义于 ``aliases`` 节点。
   - ``compat``：要匹配的父节点 compatible 字符串。

``dt_label_with_parent_compat_enabled(label, compat)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查指定标签的设备树节点是否存在、已启用，且其父节点具有指定 compatible 字符串。

**参数：**
   - ``label``：要匹配的节点标签。
   - ``compat``：要匹配的父节点 compatible 字符串。

``dt_label_compat_enabled(label, compat)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查指定标签的设备树节点是否存在、已启用，且具有指定 compatible 字符串。

**参数：**
   - ``label``：要匹配的节点标签。
   - ``compat``：要匹配的节点 compatible 字符串。

``dt_chosen_enabled(chosen)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查指定名称的设备树 chosen 属性是否存在，且其所指节点已启用。

**参数：**
   - ``chosen``：chosen 属性名称。

``dt_nodelabel_enabled(label)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查指定标签的设备树节点是否存在且已启用。

**参数：**
   - ``label``：要匹配的节点标签。

``dt_nodelabel_prop_enabled(label, prop)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查指定标签的设备树节点是否存在、已启用，且具有值非空的指定属性。

**参数：**
   - ``label``：要匹配的节点标签。
   - ``prop``：要检查的节点属性。

``dt_node_has_prop(node_id, prop)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查由别名或路径指定的设备树节点是否具有指定属性，不考虑节点状态。适用于没有 status 的节点，例如 ``zephyr,user``。

**参数：**
   - ``node_id``：要匹配的节点别名（定义于 ``aliases`` 节点）或节点路径。
   - ``prop``：要检查的节点属性。

用法
----

Twister 的场景过滤逻辑使用这些表达式选择满足设备树条件的开发板，例如：

.. code-block:: yaml

   tests:
     - test: my_test
       filter: dt_compat_enabled("my-compat-string")

``my_test`` 场景仅会针对启用了 ``my-compat-string`` 设备树节点的开发板构建。

.. _twister_harnesses:

测试适配器
**********

*测试适配器（harness）* 是 Twister 用于运行测试并判断结果的机制。测试镜像构建完成并在真实硬件、模拟器或主机上启动后，适配器驱动与镜像的交互，例如提供输入、捕获输出或将执行交给外部运行器，再解释结果，为每个用例分配 :ref:`状态 <twister_statuses>`。

场景通过 ``tests.yaml`` 的 ``harness:`` 选择适配器，通过 ``harness_config`` 调整行为。未指定时使用默认 ``test`` 适配器。不同适配器满足不同需求，有的将设备控制台输出与预期模式匹配，有的将执行交给 pytest、Robot Framework 或 ctest 等外部框架。以下页面介绍各受支持适配器及其 ``harness_config`` 选项。

``ztest``、``gtest`` 和 ``console`` 适配器通过解析输出并匹配特定语句工作。``ztest`` 和 ``gtest`` 查找各框架定义的通过、失败等结果格式。

一些常用但尚未支持的适配器：

- keyboard
- net
- bluetooth

以下 YAML 示例包含若干 harness_config 选项。

.. code-block:: yaml

      sample:
        name: HTS221 Temperature and Humidity Monitor
      common:
        tags:
          - sensor
        harness: console
        harness_config:
          type: multi_line
          ordered: false
          regex:
            - "Temperature:(.*)C"
            - "Relative Humidity:(.*)%"
          fixture: i2c_hts221
      tests:
        test:
          tags:
            - sensors
          depends_on: i2c

.. toctree::
   :maxdepth: 1

   harness/ctest
   harness/gtest
   harness/pytest
   harness/console
   harness/robot
   harness/power
   harness/display_capture
   harness/script
   harness/bsim
   harness/shell


.. _twister_sidecars:

伴随组件
********

有些测试在运行期间需要主机侧资源，例如仿真客户机通信的守护进程、运行后供主机读取的共享内存，或客户机连接的网络接口。*伴随组件（sidecar）* 对此建模。它由场景的 :file:`tests.yaml` 中的 ``sidecar:`` 选择，与适配器相互独立：适配器解释客户机输出，伴随组件则在运行前后准备和清理主机资源。因此任意适配器，如示例的 ``console`` 或测试的 ``ztest``，都可与任意伴随组件配合。

.. code-block:: yaml

   tests:
     some.test:
       harness: ztest
       sidecar: <name>

Twister 为每个测试实例驱动伴随组件的简短生命周期：

#. **configure（配置）**：准备任何资源前，从实例及其 ``sidecar_config`` 中读取所需信息。
#. **host check（主机检查）**：生成测试计划时，报告主机是否具备所需条件，例如必要的守护程序是否已安装。若不具备，测试 *仅构建* 而不执行，与平台模拟器未安装时相同。
#. **setup（准备）**：处理器运行测试镜像前调用，启用主机资源，例如启动守护程序或创建接口。若此时仍发现资源不可用，例如缺少所需权限，则报告情况，Twister *跳过* 执行，而非将测试判为失败。
#. **teardown（清理）**：处理器返回后在 ``finally`` 块中调用，因此即使测试失败或超时也始终执行。它释放资源，也可收集客户机留下的数据，例如将共享内存内容读回构建目录。

由于资源准备与输出处理解耦，Twister 也可自行给实例附加伴随组件，无需测试显式选择，例如为没有其他主机传输通道的客户机导出覆盖率数据。

每个伴随组件在 ``sidecar_config`` 下以自身名称命名的块中定义配置键，避免彼此冲突。仅使用与场景 ``sidecar:`` 值匹配的块。例如，``virtiofs`` 伴随组件可共享一个从模板初始化的主机目录：

.. code-block:: yaml

   tests:
     some.test:
       harness: console
       sidecar: virtiofs
       sidecar_config:
         virtiofs:
           shared: shared


选择平台范围
************

Twister 的关键能力之一是决定场景应在哪些平台运行。这源于它最初作为 Zephyr CI 测试运行器开发。面对数百个平台和数千项测试，工具需要调整范围，选择相关内容并排除无关内容。

Twister 总是先根据命令行及 :ref:`测试配置 <test_config_args>` 生成初始平台列表，再过滤不满足 YAML 要求（例如最小 RAM）的平台。``--force-platform`` 可覆盖配置中 ``platform_allow``、``platform_exclude``、``arch_allow`` 和 ``arch_exclude`` 导致的过滤。

命令行参数按以下方式定义初始范围：

* ``-p/--platform <platform_name>`` （可重复使用）：仅包含指定平台；
* ``-l/--all``：所有可用平台；
* ``-G/--integration``：使用测试配置的 ``integration_platforms`` 列表。若测试没有 ``integration_platforms``，则进行 *“范围推定”*；
* 未指定范围参数：进行 *“范围推定”*。

*“范围推定”*：先使用 Twister 的 :ref:`默认平台 <twister_default_testing_board>` 列表。若过滤后没有剩余平台，则改用 ``platform_allow`` 作为初始范围。

在集成模式下运行
****************

此模式用于 CI 等自动化环境，为开发者快速反馈改动结果。通过 Twister 的 ``--integration`` 启用；如适用，将构建和测试范围缩小到 ``tests.yaml`` 中 integration 关键字定义的平台。


在自定义模拟器上运行测试
************************

除已支持的 QEMU 等仿真环境外，Twister 还支持运行在开发板 :file:`board.cmake` 中定义的任意树外自定义模拟器。要使用它，在 :file:`custom_board/custom_board.yaml` 添加以下属性：

.. code-block:: yaml

   simulation:
     - name: custom
       exec: <name_of_emu_binary>

这告诉 Twister，该板使用名为 ``<name_of_emu_binary>`` 的自定义模拟器。请确保 PATH 中存在该程序。

然后在 :file:`custom_board/board.cmake` 中将支持的仿真平台设为 ``custom``：

.. code-block:: cmake

   set(SUPPORTED_EMU_PLATFORMS custom)

最后在 :file:`custom_board/board.cmake` 中实现 ``run_custom`` 目标，大致如下：

.. code-block:: cmake

   add_custom_target(run_custom
     COMMAND
     <name_of_emu_binary to invoke during 'run'>
     <any args to be passed to the command, i.e. ${BOARD}, ${APPLICATION_BINARY_DIR}/zephyr/zephyr.elf>
     WORKING_DIRECTORY ${APPLICATION_BINARY_DIR}
     DEPENDS ${logical_target_for_zephyr_elf}
     USES_TERMINAL
     )


随机顺序运行测试
****************
启用 ZTEST 的 :kconfig:option:`CONFIG_ZTEST_SHUFFLE` 可随机运行测试，有助于识别用例间依赖。native_sim 平台可通过 Twister 参数 ``--seed=value`` 指定随机种子。详情见 :ref:`打乱测试顺序 <ztest_shuffle>`。


在硬件上运行测试
****************

除 QEMU 等仿真环境外，Twister 也支持在真实设备上运行大多数测试，并为每次运行生成包含详细 FAIL/PASS 结果的报告。


在单个设备上执行测试
====================

要在单个已连接设备上使用此功能，以以下新选项运行 Twister：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

              west twister --device-testing --device-serial /dev/ttyACM0 \
              --device-serial-baud 115200 -p frdm_k64f  -T tests/kernel

   .. group-tab:: Windows

      .. code-block:: bat

              west twister --device-testing --device-serial COM1 \
              --device-serial-baud 115200 -p frdm_k64f  -T tests/kernel

``--device-serial`` 指定开发板连接的串口设备，运行 Twister 的用户必须有访问权限。一次只能对 ``--platform`` 指定的一块板运行。若平台支持多个串口，可多次提供 ``--device-serial``，这些值会传给 pytest 适配器。也可使用硬件映射，详见 :ref:`多核测试 <twister_multi_core_testing>`。

仅当设备波特率不是 115200 时，才需要 ``--device-serial-baud``。

没有物理串口的设备可使用 ``--device-serial-pty``，例如通过脚本捕获日志。此时可按以下选项运行：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         west twister --device-testing --device-serial-pty "script.py" \
         -p intel_adsp/cavs25 -T tests/kernel

   .. group-tab:: Windows

      .. note::

         不支持 Windows 操作系统

脚本由用户定义，负责传送消息，供 Twister 判断测试执行状态。

``--device-flash-timeout`` 可显式设置烧录超时，例如设备烧录耗时很长时。

``--device-flash-with-test`` 表示该平台烧录时也会执行测试场景，因此烧录超时增加一个场景超时时长。

在多个设备上执行测试
====================

要在主机连接的多个设备上构建和执行测试，需要创建包含全部设备及其串口、波特率、可用 ID 等详情的硬件映射。生成命令如下：

.. code-block:: console

   $ west twister --generate-hardware-map map.yml

生成的硬件映射文件 map.yml 包含已连接设备列表，例如：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: yaml

         - connected: true
           id: "OSHW000032254e4500128002ab98002784d1000097969900"
           platform: unknown
           product: DAPLink CMSIS-DAP
           runner: pyocd
           serial: /dev/cu.usbmodem146114202
         - connected: true
           id: "000683759358"
           platform: unknown
           product: J-Link
           runner: unknown
           serial: /dev/cu.usbmodem0006837593581

   .. group-tab:: Windows

      .. code-block:: yaml

         - connected: true
           id: "OSHW000032254e4500128002ab98002784d1000097969900"
           platform: unknown
           product: unknown
           runner: unknown
           serial: COM1
         - connected: true
           id: "000683759358"
           platform: unknown
           product: unknown
           runner: unknown
           serial: COM2


所有标记为 ``unknown`` 的选项都需改为正确值。上例中的平台名、产品和烧录运行器应替换为对应硬件的实际值。本例使用 reel_board 和 nrf52840dk/nrf52840：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: yaml

         - connected: true
           id: "OSHW000032254e4500128002ab98002784d1000097969900"
           platform: reel_board
           product: DAPLink CMSIS-DAP
           runner: pyocd
           serial: /dev/cu.usbmodem146114202
           baud: 9600
         - connected: true
           id: "000683759358"
           platform: nrf52840dk/nrf52840
           product: J-Link
           runner: nrfjprog
           serial: /dev/cu.usbmodem0006837593581
           baud: 9600

   .. group-tab:: Windows

      .. code-block:: yaml

         - connected: true
           id: "OSHW000032254e4500128002ab98002784d1000097969900"
           platform: reel_board
           product: DAPLink CMSIS-DAP
           runner: pyocd
           serial: COM1
           baud: 9600
         - connected: true
           id: "000683759358"
           platform: nrf52840dk/nrf52840
           product: J-Link
           runner: nrfjprog
           serial: COM2
           baud: 9600

仅当波特率不是 115200 时才需要 baud 条目。

映射文件已存在时，会加入新条目并更新现有条目。因此可维护一份主硬件映射，每次运行前更新，以获取正确串口和设备状态。

准备好硬件映射后，指定它即可运行任意测试：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         west twister --device-testing --hardware-map map.yml -T samples/hello_world/

   .. group-tab:: Windows

      .. code-block:: bat

         west twister --device-testing --hardware-map map.yml -T samples\hello_world

上述命令让 Twister 为映射中的平台构建测试，再烧录并运行。

.. note::

  硬件映射目前仅支持通过 pyocd、nrfjprog、jlink、openocd 或 dediprog 烧录的开发板。需要其他运行器烧录 Zephyr 的开发板仍在开发支持中。

硬件映射可分别通过 ``flash-timeout`` 和 ``flash-with-test`` 字段设置 ``--device-flash-timeout`` 与 ``--device-flash-with-test``。这些值覆盖对应平台的命令行选项。

硬件映射也支持 ``--device-serial-pty`` 提供的串行 PTY：

.. code-block:: yaml

   - connected: true
     id: None
     platform: intel_adsp/cavs25
     product: None
     runner: intel_adsp
     serial_pty: path/to/script.py
     runner_params:
       - --remote-host=remote_host_ip_addr
       - --key=/path/to/key.pem


runner_params 字段指定传给 west 运行器的参数。部分开发板需要附加参数才能正常工作，其效果等同于以下 west 和 Twister 命令。

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         west flash --remote-host remote_host_ip_addr --key /path/to/key.pem

         west twister -p intel_adsp/cavs25 --device-testing --device-serial-pty script.py
         --west-flash="--remote-host=remote_host_ip_addr,--key=/path/to/key.pem"

   .. group-tab:: Windows

      .. note::

         不支持 Windows 操作系统

.. note::

  串行 PTY 无法被“--generate-hardware-map”自动扫描并生成正确映射，需要按上例手动编辑，因为 PTY 串口不是固定的，而是在运行时由系统分配。

若 west 不可用或不知道如何烧录系统，可通过 ``flash-command`` 指定自定义烧录命令。调用脚本时会传入 ``--build-dir`` 指定当前构建路径，并用 ``--board-id`` 在硬件映射包含多个设备时标识具体设备。

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         west twister -p npcx9m6f_evb --device-testing --device-serial /dev/ttyACM0
         --flash-command './custom_flash_script.py,--flag,"complex, argument"'

   .. group-tab:: Windows

      .. note::

         west twister -p npcx9m6f_evb --device-testing
         --device-serial COM1
         --flash-command 'custom_flash_script.py,--flag,"complex, argument"'

会调用 ``./custom_flash_script.py --build-dir <build directory> --board-id <board identification> --flag "complex, argument"``。

.. _twister_fixtures:

测试装置（Fixture）
-------------------

有些测试需要专用设置或接线，缺少这些测试装置可能导致失败。场景可声明所需 fixture，再通过命令行或硬件映射匹配开发板的硬件能力及支持的装置。

fixture 在硬件映射中定义为列表：

.. code-block:: yaml

      - connected: true
        fixtures:
          - gpio_loopback
        id: "0240000026334e450015400f5e0e000b4eb1000097969900"
        platform: frdm_k64f
        product: DAPLink CMSIS-DAP
        runner: pyocd
        serial: /dev/ttyACM9

使用 ``--device-testing`` 运行 ``twister`` 时，将映射中的 fixture 与请求相同装置的场景匹配，并在提供该装置的开发板上执行测试。

要将开发板专门保留给依赖 fixture 的测试，将 ``run_with_fixture_only`` 设为 ``true``。Twister 仅为请求匹配 fixture 的场景选择该板，不用于没有 fixture 要求的场景。

.. code-block:: yaml

      - connected: true
        fixtures:
          - gpio_loopback
        run_with_fixture_only: true
        id: 0240000026334e450015400f5e0e000b4eb1000097969900
        platform: frdm_k64f

.. figure:: figures/fixtures.svg
   :figclass: align-center

也可通过 Twister 的 ``--fixture`` 提供装置。可重复使用此选项，所有值合并为列表并分配给全部开发板，即本次命令指定的所有开发板都可运行请求相同 fixture 的场景。

部分 fixture 可在名称后用 ``:`` 分隔并追加配置字符串。与场景请求匹配时仅比较 fixture 名称。

备注
----

可用 ``notes`` 为硬件映射中的开发板描述添加补充信息，例如：

.. code-block:: yaml

    - connected: false
      fixtures:
        - gpio_loopback
      id: "000683290670"
      notes: An nrf5340dk/nrf5340 is detected as an nrf52840dk/nrf52840 with no serial
        port, and three serial ports with an unknown platform.  The board id of the serial
        ports is not the same as the board id of the development kit.  If you regenerate
        this file you will need to update serial to reference the third port, and platform
        to nrf5340dk/nrf5340/cpuapp or another supported board target.
      platform: nrf52840dk/nrf52840
      product: J-Link
      runner: jlink
      serial: null

覆盖开发板标识
--------------

生成或重新生成硬件映射时，``id`` 键用作烧录的 ``--board-id`` 参数。有时检测到的 ID 不适用，例如使用外部 J-Link 探针。可用 ``probe_id`` 覆盖 ``id``，例如：

.. code-block:: yaml

    - connected: false
      id: "0229000005d9ebc600000000000000000000000097969905"
      platform: mimxrt1060_evk
      probe_id: "000609301751"
      product: DAPLink CMSIS-DAP
      runner: jlink
      serial: null

使用同一开发板测试多个变体
--------------------------

  ``platform`` 属性可以是名称列表，或以空格分隔名称的字符串。这样无需为每个变体重新配置映射，就能在同一物理开发板上运行不同平台变体的测试。例如：

.. code-block:: yaml

    - connected: true
      id: "001234567890"
      platform:
      - nrf5340dk/nrf5340/cpuapp
      - nrf5340dk/nrf5340/cpuapp/ns
      product: J-Link
      runner: nrfjprog
      serial: /dev/ttyACM1

.. _twister_multi_core_testing:

多核测试支持
------------

Twister 支持不同核心使用独立 UART 的多核应用测试，仅适用于 pytest 适配器（``harness: pytest``）。生成的硬件映射应为同一物理设备包含多个条目，分别代表不同核心连接。例如：

.. code-block:: yaml

    - connected: true
      id: "001234567890"
      serial: /dev/ttyACM0
    - connected: true
      id: "001234567890"
      platform:
      - nrf54l15dk/nrf54l15/cpuapp
      product: J-Link
      runner: nrfutil
      serial: /dev/ttyACM1

两个实例共享设备 ID，但串口不同，因此测试可同时与多个核心交互。各连接独立处理并拥有单独的日志文件。

.. _twister_multi_duts_testing:

多 DUT 测试支持
---------------

Twister 支持需要多个设备的场景，仅适用于 pytest 适配器（``harness: pytest``），支持硬件和 ``native_sim`` 执行环境。

在测试 YAML 的 ``harness_config`` 下添加 ``required_devices``，声明额外设备。列表每项描述一个附加 DUT；空条目 ``{}`` 预留与主 DUT 具有相同平台和应用的第二设备。全部选项见 :ref:`required_devices <required_devices>`。

测试配置示例：

.. code-block:: yaml

    tests:
      multidut.basic:
        harness: pytest
        harness_config:
          required_devices:
            - {}

硬件映射必须为每个所需设备提供至少一个条目，且具有匹配的平台和串行连接：

.. code-block:: yaml

    - connected: true
      id: "01"
      platform: nrf52840dk/nrf52840
      serial: /dev/ttyACM0
    - connected: true
      id: "02"
      platform: nrf52840dk/nrf52840
      serial: /dev/ttyACM1

在硬件上运行：

.. code-block:: console

    $ west twister -vv -ll debug -T tests/subsys/testsuite/multidut \
      --device-testing --hardware-map map.yaml

在 ``native_sim`` 上运行，无需硬件映射：

.. code-block:: console

    $ west twister -vv -ll debug -T tests/subsys/testsuite/multidut -p native_sim

Twister 预留全部所需设备，或为 ``native_sim`` 创建占位条目，再连同平台、串行连接、待烧录产物等必要信息传给 pytest，使测试能与所有设备交互。

多 DUT 示例见 :zephyr_file:`tests/subsys/testsuite/multidut`。

隔离
----

Twister 允许通过配置文件列出需要隔离的测试或平台。这些测试会被跳过，并在报告中标记。对于大型套件尤其有用，因为一个测试失败可能影响其他测试，例如使物理开发板进入异常状态。

使用隔离功能时，向 Twister 添加 ``--quarantine-list <PATH_TO_QUARANTINE_YAML>``，可使用多个隔离文件。再加 ``--quarantine-verify`` 可验证名单中测试的当前状态，此时会跳过不在名单内的所有测试。

隔离 YAML 是一组字典，每项至少包含 ``scenarios``、``platforms``、``architectures`` 或 ``simulations`` 之一，也可组合使用。可选 ``comment`` 提供详情，例如已报告问题的链接，也会写入输出报告。

隔离某类测试、套件中的多个场景，或处理子系统内多个问题时，可使用正则表达式。例如 **kernel.*** 会隔离所有内核测试。

隔离 YAML 条目示例：

.. code-block:: yaml

    - scenarios:
        - sample.basic.helloworld
      comment: "Link to the issue: https://github.com/zephyrproject-rtos/zephyr/pull/33287"

    - scenarios:
        - kernel.common
        - kernel.common.(misra|tls)
        - kernel.common.nano64
      platforms:
        - .*_cortex_.*
        - native_sim

    - platforms:
        - qemu_x86
      comment: "filter out qemu_x86"

    - architectures:
        - riscv

    - simulations:
        - armfvp

.. _twister_output:

测试输出与报告
**************

默认将全部输出写入当前工作目录下创建的 :file:`twister-out`。用 ``-O``/``--outdir`` 可选择其他位置。除非使用 ``--no-clean``，否则每次运行都会清理该目录；``--clobber-output`` 控制清理方式。

顶层报告
========

以下文件写入输出目录根部：

:file:`twister.json`
    主要的机器可读报告，为每个选中的套件和用例记录 :ref:`状态 <twister_statuses>`、目标平台、执行时间、内存占用、:ref:`记录数据 <twister_console_harness>`，以及运行环境和选项。

:file:`testplan.json`
    解析后的测试计划，包含 Twister 考虑的每个实例，即场景与平台组合，也包括被过滤的实例及原因。可查看此文件了解某场景为何运行或未运行。通过 ``--load-tests`` 可重用相同选择。

:file:`twister.xml`
    适用于 CI 系统的 JUnit XML 摘要。

:file:`twister_report.xml`
    包含全部用例而不仅是摘要的 JUnit XML 报告。

:file:`twister_suite_report.xml`
    按测试套件分组的 JUnit XML 报告。

:file:`twister.log`
    整个运行过程的人类可读日志。

:file:`twister_footprint.json`
    ROM/RAM 占用报告，仅在使用 ``--footprint-report`` 时生成。

可通过 ``--report-name`` 更改报告基本名称 ``twister``，通过 ``--report-suffix`` 为所有生成文件名追加版本号或提交 ID 等后缀。用 ``-o``/``--report-dir`` 将报告写入其他目录；``--platform-reports`` 额外按平台生成 :file:`<platform>.json` 和 :file:`<platform>.xml`。``--report-summary`` 无需重新构建即可打印最近一次运行的失败摘要。

逐测试产物
==========

每个实例在输出目录下拥有独立构建目录，按平台和测试命名：:file:`twister-out/<platform>/<test path>/<scenario>/`。除常规 Zephyr 产物，例如 :file:`zephyr/zephyr.elf`，还可能包含：

:file:`build.log`
    此实例的构建输出。

:file:`handler.log`
    运行测试时从设备或模拟器捕获的控制台输出。

:file:`twister_harness.log`
    基于 pytest 的适配器生成的日志，例如 ``pytest`` 和 ``shell``。

:file:`recording.csv`
    配置后，由 :ref:`控制台适配器 <twister_console_harness>` 的 ``record`` 选项捕获的数据字段。

.. _twister_console_monitor:

实时运行监视
************

长时间运行时，滚动控制台输出难以清楚展示排队任务、各任务当前构建或运行的内容，以及已失败测试及原因。``--console-monitor`` 会在运行期间用终端全屏实时仪表盘替换普通输出：

.. code-block:: console

   $ west twister -T tests/kernel --console-monitor

仪表盘显示总体进度、通过／失败／错误／过滤统计和预计剩余时间，列出当前 *正在处理* 的实例及其流水线阶段（``cmake``、``build``、``run`` 等），并提供包含计划中全部实例及静态过滤实例的可滚动表格。同时，常规日志写入 :file:`twister.log`。

导航：:kbd:`Tab` 循环切换表格过滤条件（全部／活动／失败／通过／排队／已过滤），:kbd:`f` 直接进入失败视图，:kbd:`/` 开始按实例名和失败原因增量搜索，:kbd:`Esc` 清除搜索。用方向键或 :kbd:`j`/:kbd:`k` 移动选择，按 :kbd:`Enter` 查看实例详情：流水线阶段时间线、失败用例及原因、日志末尾内容。:kbd:`l` 切换日志，:kbd:`j`/:kbd:`k` 或方向键滚动，:kbd:`g`/:kbd:`G` 跳到顶部／末尾；停留在末尾时自动跟随新输出。这便于在其他测试继续运行时检查失败。

运行结束后仪表盘继续显示，供检查失败；按 :kbd:`q` 退出后写入报告，Twister 正常结束。运行期间按 :kbd:`q` 则提前退出仪表盘，恢复普通控制台输出。此选项需要交互式终端，否则忽略，例如 CI 中。

监视器只观察，不干扰运行：监视事件尽力传递，必要时丢弃，绝不延迟构建或执行流水线。

.. _twister_test_config:

Twister 配置文件
****************

通过 ``--test-config`` 传入的 ``test_config.yaml`` 可定制 Twister 各方面行为及默认启用选项和功能，按环境调整过滤能力，并面向不同平台集合调整和改善覆盖。

.. note::

   ``--test-config`` 选择的文件配置整个 Twister 运行，与描述各个 :ref:`测试场景 <twister_tests_long_version>` 的应用级 ``tests.yaml`` 不同。

该配置还支持测试级别，可将某测试分配到一个或多个级别，再通过命令行选择级别，仅执行其中的测试。

此外，可定义级别依赖，并在测试自身未声明时将其额外纳入指定级别。

配置中可通过正则表达式纳入完整组件，并指定从同一文件导入哪些测试级别，便于管理。

为便于在上游 CI 之外测试，本地配置文件还提供以下选项：

- 忽略开发板定义中的默认平台，它们大多是上游 CI 用于运行测试的仿真平台。
- 指定自己的默认平台列表，覆盖上游定义。
- 覆盖某些场景的 ``build_on_all``，使这些测试或示例像其他测试一样，仅针对配置文件或命令行指定的默认平台构建。
- 忽略默认平台不在范围内时自动扩大平台覆盖的部分 Twister 逻辑。


平台配置
========

以下选项控制 Twister 平台过滤：

- ``override_default_platforms``：覆盖开发板配置中的 default 键，改用配置文件提供的默认平台列表。默认为 False。
- ``increased_platform_scope``：默认为 True。禁用后，Twister 不再自动扩大平台覆盖，只在指定平台构建和运行测试。
- ``default_platforms``：额外默认平台列表。根据 ``override_default_platforms`` 的值，替换或扩展现有默认平台。
- ``build_toolchains``：平台名称到工具链列表的映射，平台上的每个测试都使用列出的工具链构建。Twister 为每种工具链创建独立实例和构建目录。此项设置或覆盖开发板定义的 ``build_toolchains``；空列表可禁用平台请求的多工具链构建。由于会成倍增加构建时间，通常只在 CI 配置 ``tests/test_config_ci.yaml`` 中启用，本地仍对每项测试只构建一次。见 :ref:`twister_toolchain_selection`。

平台配置示例：

.. code-block:: yaml

        platforms:
          override_default_platforms: true
          increased_platform_scope: false
          default_platforms:
            - qemu_x86
          build_toolchains:
            native_sim:
              - host/gnu
              - host/llvm


测试级别配置
============

测试配置支持定义级别、级别依赖，以及在测试自身未提供信息时，将其额外纳入指定级别。

可通过正则表达式纳入完整组件，并指定从同一文件导入哪些测试级别，简化管理。

测试级别配置示例：

.. code-block:: yaml

        levels:
          - name: my-test-level
            description: >
              my custom test level
            adds:
              - kernel.threads.*
              - kernel.timer.behavior
              - arch.interrupt
              - boards.*


组合配置
========

可按以下示例混合平台和级别配置：

平台与级别组合配置示例：

.. code-block:: yaml

        platforms:
          override_default_platforms: true
          default_platforms:
            - frdm_k64f
        levels:
          - name: smoke
            description: >
                A plan to be used verifying basic zephyr features.
          - name: unit
            description: >
                A plan to be used verifying unit test.
          - name: integration
            description: >
                A plan to be used verifying integration.
          - name: acceptance
            description: >
                A plan to be used verifying acceptance.
          - name: system
            description: >
                A plan to be used verifying system.
          - name: regression
            description: >
                A plan to be used verifying regression.


使用上述 test_config.yaml 运行时，只在 default_platforms 上运行属于指定测试级别的场景。

.. code-block:: console

   $ west twister --test-config=<path to>/test_config.yaml -T tests --level="smoke"
