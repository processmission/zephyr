.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _device_model_api:

设备驱动程序模型
################

简介
****
Zephyr 内核支持多种设备驱动程序。某个驱动程序是否可用取决于开发板和驱动程序本身。

Zephyr 设备模型提供一致的模型，用于配置系统中的驱动程序，并负责初始化系统中配置的所有驱动程序。

每种驱动程序（例如 UART、SPI、I2C）都有通用的类型 API。

在此模型中，驱动程序初始化时会填入一个结构体指针，该结构体包含指向其 API 函数的函数指针。这些结构体按照初始化级别顺序放在 RAM 段中。

.. image:: device_driver_model.svg
   :width: 40%
   :align: center
   :alt: Device Driver Model

标准驱动程序
************

以下设备驱动程序存在于所有受支持的开发板配置中。

* **中断控制器**：供内核中断管理子系统使用的设备驱动程序。

* **定时器**：供内核系统时钟和硬件时钟子系统使用的设备驱动程序。

* **串行通信**：供内核系统控制台子系统使用的设备驱动程序。

* **熵**：为随机数生成器子系统提供熵数据源的设备驱动程序。

  .. important::

    请使用 :ref:`随机数 API 函数 <random_api>` 获取随机值。不要直接将 :ref:`熵函数 <entropy_api>` 用作随机数生成器的数据源，因为有些硬件实现旨在为随机数生成器提供熵种子，并不提供密码学安全的随机数流。

同步调用
********

Zephyr 为多种开发板提供了一组设备驱动程序。除非硬件完全不提供中断，否则每个驱动程序都应支持基于中断的实现，而不是轮询。

通过 :file:`i2c.h` 或 :file:`spi.h` 等设备专用 API 进行的高层调用通常设计为同步调用，因此这些调用应当阻塞。

.. _device_driver_api:

驱动程序 API
************

:file:`device.h` 为设备驱动程序提供以下 API。这些 API 仅供设备驱动程序使用，不应在应用程序中使用。

:c:macro:`DEVICE_DEFINE()`
   创建设备对象及相关数据结构，并设置其启动时初始化。

:c:macro:`DEVICE_NAME_GET()`
   将设备标识符转换为设备对象的全局标识符。

:c:macro:`DEVICE_GET()`
   按名称获取指向设备对象的指针。

:c:macro:`DEVICE_DECLARE()`
   声明设备对象。需要前向引用尚未定义的设备时使用。

:c:macro:`DEVICE_API()`
   封装驱动程序 API 声明，将其分配到对应的链接器段。实现上游驱动程序类别的任何驱动程序都必须使用此宏，因为 :c:macro:`DEVICE_API_GET` 和 :c:macro:`DEVICE_API_IS` 依赖 API 实例位于所属类别的链接器段中，以便在运行时验证设备的 API 类别。

.. _device_struct:

驱动程序数据结构
****************

设备初始化宏会在构建时填充一些数据结构，分为只读部分和运行时可变部分。概括如下：

.. code-block:: C

  struct device {
        const char *name;
        const void *config;
        const void *api;
        void * const data;
  };

``config`` 成员用于保存构建时设置的只读配置数据，例如内存映射 I/O 基地址、IRQ 线路编号或设备的其他固定物理特性。它就是传给 ``DEVICE_DEFINE()`` 及相关宏的 ``config`` 指针。

``data`` 结构体保存在 RAM 中，供驱动程序管理各实例的运行时状态，例如引用计数、信号量、临时缓冲区等。

``api`` 结构体将通用子系统 API 映射到驱动程序中的设备专用实现。它通常只读，并在构建时填充。下一节将详细说明。


子系统与 API 结构体
*******************

大多数驱动程序实现的是与设备无关的子系统 API。应用程序只需面向通用 API 编程，无需依赖特定驱动程序实现。

驱动程序 API 实例必须使用 :c:macro:`DEVICE_API()` 声明，以将其放入对应的 API 链接器段。这样 :c:macro:`DEVICE_API_GET` 和 :c:macro:`DEVICE_API_IS` 才能在运行时验证设备的 API 是否属于预期类别。

子系统 API 的定义通常如下：

.. code-block:: C

  typedef int (*subsystem_do_this_t)(const struct device *dev, int foo, int bar);
  typedef void (*subsystem_do_that_t)(const struct device *dev, void *baz);

  __subsystem struct subsystem_driver_api {
        subsystem_do_this_t do_this;
        subsystem_do_that_t do_that;
  };

  static inline int subsystem_do_this(const struct device *dev, int foo, int bar)
  {
        return DEVICE_API_GET(subsystem, dev)->do_this(dev, foo, bar);
  }

  static inline void subsystem_do_that(const struct device *dev, void *baz)
  {
        DEVICE_API_GET(subsystem, dev)->do_that(dev, baz);
  }

实现特定子系统的驱动程序会定义这些 API 的实际实现，并使用 :c:macro:`DEVICE_API()` 包装宏填充 subsystem_driver_api 结构体实例：

.. code-block:: C

  static int my_driver_do_this(const struct device *dev, int foo, int bar)
  {
        ...
  }

  static void my_driver_do_that(const struct device *dev, void *baz)
  {
        ...
  }

  static DEVICE_API(subsystem, my_driver_api_funcs) = {
        .do_this = my_driver_do_this,
        .do_that = my_driver_do_that,
  };

随后，驱动程序将 ``my_driver_api_funcs`` 作为 ``api`` 参数传给 ``DEVICE_DEFINE()``。

.. note::

        由于 ``api`` 结构体引用了 API 函数指针，这些函数即使未使用也会被包含在二进制文件中；链接器的 ``gc-sections`` 选项始终会发现至少一个对它们的引用。要在链接时优化驱动程序 API 的体积，大多数情况下需要通过 Kconfig 选项控制可选功能。

API 类别继承
************

子系统 API 可以扩展另一个子系统 API，形成父子关系。这样，实现子 API 的设备也会被识别为实现了父 API。例如，I3C 控制器扩展了 I2C API，因此可用于任何需要 I2C 设备的场合。

定义子 API 时，将父 API 结构体嵌入为子结构体的 **第一个成员**，并使用 :c:macro:`DEVICE_API_EXTENDS` 声明该关系：

.. code-block:: C

  __subsystem struct child_driver_api {
        struct subsystem_driver_api parent_api;
        child_do_extra_t do_extra;
  };

  DEVICE_API_EXTENDS(child, subsystem, parent_api);

实现子 API 的驱动程序会同时填充父级和子级方法：

.. code-block:: C

  static DEVICE_API(child, my_child_api) = {
        .parent_api = {
                .do_this = my_child_do_this,
                .do_that = my_child_do_that,
        },
        .do_extra = my_child_do_extra,
  };

完成以上设置后，:c:macro:`DEVICE_API_IS` 对父类别和子类别均返回 true，:c:macro:`DEVICE_API_GET` 也可以按任一类型获取 API：

.. code-block:: C

  /* Both return true for a child device */
  DEVICE_API_IS(subsystem, dev);
  DEVICE_API_IS(child, dev);

  /* Access through parent API */
  DEVICE_API_GET(subsystem, dev)->do_this(dev, foo, bar);

支持多级继承（例如孙级扩展子级，子级扩展父级）。同级关系也能正确处理：扩展同一父 API 的两个不同子 API 可通过 :c:macro:`DEVICE_API_IS` 区分。

设备专用 API 扩展
*****************

有些设备可作为 GPIO 等驱动程序子系统的实例，但还提供无法通过标准 API 暴露的额外功能。这些设备将子系统操作与设备专用 API 结合，后者在设备专用头文件中描述。

设备专用 API 的定义通常如下：

.. code-block:: C

   #include <zephyr/drivers/subsystem.h>

   /* When extensions need not be invoked from user mode threads */
   int specific_do_that(const struct device *dev, int foo);

   /* When extensions must be invokable from user mode threads */
   __syscall int specific_from_user(const struct device *dev, int bar);

   /* Only needed when extensions include syscalls */
   #include <zephyr/syscalls/specific.h>

对某个子系统进行扩展的驱动程序，会同时定义子系统 API 和专用 API 的实际实现：

.. code-block:: C

   static int generic_do_this(const struct device *dev, void *arg)
   {
      ...
   }

   static struct generic_api api {
      ...
      .do_this = generic_do_this,
      ...
   };

   /* supervisor-only API is globally visible */
   int specific_do_that(const struct device *dev, int foo)
   {
      ...
   }

   /* syscall API passes through a translation */
   int z_impl_specific_from_user(const struct device *dev, int bar)
   {
      ...
   }

   #ifdef CONFIG_USERSPACE

   #include <zephyr/internal/syscall_handler.h>

   int z_vrfy_specific_from_user(const struct device *dev, int bar)
   {
       K_OOPS(K_SYSCALL_SPECIFIC_DRIVER(dev, K_OBJ_DRIVER_GENERIC, &api));
       return z_impl_specific_do_that(dev, bar)
   }

   #include <zephyr/syscalls/specific_from_user_mrsh.c>

   #endif /* CONFIG_USERSPACE */

应用程序通过子系统 API 和专用 API 共同使用设备。

单个驱动程序，多个实例
**********************

有些驱动程序可以在同一系统中实例化多次，例如多个 GPIO 组或多个 UART。驱动程序的每个实例都有不同的 ``config`` 和 ``data`` 结构体。

为多个驱动程序实例配置中断是一个特例。如果每个实例需要配置不同的中断线路，可以使用每个实例各自的配置函数，因为 ``IRQ_CONNECT()`` 的参数必须能在构建时确定。

例如，假设需要配置两个 ``my_driver`` 实例，各自使用不同的中断线路。在 ``drivers/subsystem/subsystem_my_driver.h`` 中：

.. code-block:: C

  typedef void (*my_driver_config_irq_t)(const struct device *dev);

  struct my_driver_config {
        DEVICE_MMIO_ROM;
        my_driver_config_irq_t config_func;
  };

在通用初始化函数的实现中：

.. code-block:: C

  void my_driver_isr(const struct device *dev)
  {
        /* Handle interrupt */
        ...
  }

  int my_driver_init(const struct device *dev)
  {
        const struct my_driver_config *config = dev->config;

        DEVICE_MMIO_MAP(dev, K_MEM_CACHE_NONE);

        /* Do other initialization stuff */
        ...

        config->config_func(dev);

        return 0;
  }

随后，在声明具体实例时：

.. code-block:: C

  #if CONFIG_MY_DRIVER_0

  DEVICE_DECLARE(my_driver_0);

  static void my_driver_config_irq_0(const struct device *dev)
  {
        IRQ_CONNECT(MY_DRIVER_0_IRQ, MY_DRIVER_0_PRI, my_driver_isr,
                    DEVICE_GET(my_driver_0), MY_DRIVER_0_FLAGS);
  }

  const static struct my_driver_config my_driver_config_0 = {
        DEVICE_MMIO_ROM_INIT(DT_DRV_INST(0)),
        .config_func = my_driver_config_irq_0
  }

  static struct my_data_0;

  DEVICE_DEFINE(my_driver_0, MY_DRIVER_0_NAME, my_driver_init,
                NULL, &my_data_0, &my_driver_config_0,
                POST_KERNEL, MY_DRIVER_0_PRIORITY, &my_api_funcs);

  #endif /* CONFIG_MY_DRIVER_0 */

注意，这里使用 ``DEVICE_DECLARE()``，以避免提供 IRQ 处理函数参数与定义设备本身之间的循环依赖。

初始化级别
**********

驱动程序可能依赖其他驱动程序先完成初始化，或需要使用内核服务。:c:func:`DEVICE_DEFINE()` 及相关 API 允许用户指定初始化函数在启动序列中的执行时机。每个驱动程序都要指定以下三个初始化级别之一：

``PRE_KERNEL_1``
        用于没有依赖的设备，例如仅依赖处理器或 SoC 内部硬件的设备。这些设备在配置期间不能使用任何内核服务，因为此时内核服务尚不可用。不过，中断子系统已经配置好，因此可以设置中断。此级别的初始化函数在中断栈上运行。

``PRE_KERNEL_2``
        用于依赖 ``PRE_KERNEL_1`` 级别设备初始化结果的设备。这些设备在配置期间不能使用任何内核服务，因为此时内核服务尚不可用。此级别的初始化函数在中断栈上运行。

``POST_KERNEL``
        用于在配置期间需要内核服务的设备。此级别的初始化函数在内核主任务上下文中运行。

在每个初始化级别内，还可以指定相对于同级别其他设备的优先级。优先级取值为 0 到 999 的整数，值越小越早初始化。优先级必须是不带前导零或符号的十进制整数字面量（例如 32），或等价的符号名称（例如 ``\#define MY_INIT_PRIO 32``）；*不允许* 使用符号表达式（例如 ``CONFIG_KERNEL_INIT_PRIORITY_DEFAULT + 5``）。

驱动程序及其他系统工具可以使用 :c:func:`k_is_pre_kernel` 函数判断启动过程是否仍处于内核初始化之前的阶段。

延迟初始化
**********

设备初始化也可以推迟到更晚的时刻。此时，Zephyr 不会在启动时自动初始化设备，而是在应用程序调用 :c:func:`device_init` 时进行初始化。要延迟设备驱动程序初始化，请在 DTS 文件的对应设备节点中添加 ``zephyr,deferred-init`` 属性。例如：

.. code-block:: devicetree

   / {
           a-driver@40000000 {
                   reg = <0x40000000 0x1000>;
                   zephyr,deferred-init;
           };
   };

系统驱动程序
************

有时只需在启动时运行一个函数，这种情况下可以使用 :c:macro:`SYS_INIT`。此宏不接受任何配置或运行时数据结构，之后也无法按名称获取设备指针。初始化级别和优先级遵循与设备相同的策略。

检查初始化顺序
**************

通过 :c:macro:`DEVICE_DEFINE` （或其变体）和 :c:macro:`SYS_INIT` 声明的设备驱动程序会在启动时处理，并按照指定级别和优先级依次调用对应的初始化函数。

有时需要检查链接器生成的最终初始化函数调用顺序。可以使用 ``initlevels`` CMake 目标，例如 ``west build -t initlevels``。

错误处理
********

通常，除非失败预期会在正常运行中发生（例如存储设备已满），否则最好使用 ``__ASSERT()`` 宏，而不是返回错误值。错误参数、编程错误、一致性检查、异常或不可恢复的故障等，应使用断言处理。

如果适合返回错误状态供调用者检查，成功时应返回 0，失败时返回 POSIX :file:`errno.h` 错误码。详情参见 https://github.com/zephyrproject-rtos/zephyr/wiki/Naming-Conventions#return-codes。

内存映射
********

在有些系统上，外设内存映射 I/O（MMIO）区域的线性地址无法在构建时确定：

- 必须在运行时从总线探测 I/O 范围，例如 PCI Express。
- 内存管理单元（MMU）已启用，必须将 MMIO 范围的物理地址通过页表映射到内核确定的虚拟内存位置。

这些系统必须在 RAM 中保存 MMIO 范围信息，并在驱动程序初始化函数中建立映射。其他系统无需处理这一问题，可以直接使用 DTS 中的 MMIO 物理地址，也不需要为此占用 RAM 存储。

对于可能需要处理这种情况的驱动程序，提供了 DEVICE_MMIO 范围内的一组 API，以及映射函数 :c:func:`device_map`。

具有一个 MMIO 区域的设备模型驱动程序
====================================

最简单的情况是驱动程序只需维护一个 MMIO 区域。这些驱动程序需要在 ``config_info`` 和 ``driver_data`` 结构体定义中分别使用 ``DEVICE_MMIO_ROM`` 和 ``DEVICE_MMIO_RAM`` 宏，并通过 ``DEVICE_MMIO_ROM_INIT`` 从 DTS 初始化 ``config_info``。在初始化函数中调用 ``DEVICE_MMIO_MAP()``：

.. code-block:: C

   struct my_driver_config {
      DEVICE_MMIO_ROM; /* Must be first */
      ...
   }

   struct my_driver_dev_data {
      DEVICE_MMIO_RAM; /* Must be first */
      ...
   }

   const static struct my_driver_config my_driver_config_0 = {
      DEVICE_MMIO_ROM_INIT(DT_DRV_INST(...)),
      ...
   }

   int my_driver_init(const struct device *dev)
   {
      ...
      DEVICE_MMIO_MAP(dev, K_MEM_CACHE_NONE);
      ...
   }

   int my_driver_some_function(const struct device *dev)
   {
      ...
      /* Write some data to the MMIO region */
      sys_write32(0xDEADBEEF, DEVICE_MMIO_GET(dev));
      ...
   }

这些宏的具体展开形式取决于配置。在没有 MMU 或 PCI-e 的设备上，``DEVICE_MMIO_MAP`` 和 ``DEVICE_MMIO_RAM`` 展开为空。

具有多个 MMIO 区域的设备模型驱动程序
====================================

有些驱动程序可能有多个 MMIO 区域。此外，有些驱动程序可能已经使用某种继承机制，要求将其他数据放在 ``config_info`` 和 ``driver_data`` 结构体的最前面。

可以使用 ``DEVICE_MMIO_NAMED`` 系列宏处理这种情况。它们要求定义 ``DEV_CFG()`` 和 ``DEV_DATA()`` 宏，以获取类型正确的指针，分别指向驱动程序的 config_info 或 dev_data 结构体。例如：

.. code-block:: C

   struct my_driver_config {
      ...
        DEVICE_MMIO_NAMED_ROM(corge);
        DEVICE_MMIO_NAMED_ROM(grault);
      ...
   }

   struct my_driver_dev_data {
           ...
        DEVICE_MMIO_NAMED_RAM(corge);
        DEVICE_MMIO_NAMED_RAM(grault);
        ...
   }

   #define DEV_CFG(_dev) \
      ((const struct my_driver_config *)((_dev)->config))

   #define DEV_DATA(_dev) \
      ((struct my_driver_dev_data *)((_dev)->data))

   const static struct my_driver_config my_driver_config_0 = {
      ...
      DEVICE_MMIO_NAMED_ROM_INIT(corge, DT_DRV_INST(...)),
      DEVICE_MMIO_NAMED_ROM_INIT(grault, DT_DRV_INST(...)),
      ...
   }

   int my_driver_init(const struct device *dev)
   {
      ...
      DEVICE_MMIO_NAMED_MAP(dev, corge, K_MEM_CACHE_NONE);
      DEVICE_MMIO_NAMED_MAP(dev, grault, K_MEM_CACHE_NONE);
      ...
   }

   int my_driver_some_function(const struct device *dev)
   {
      ...
      /* Write some data to the MMIO regions */
      sys_write32(0xDEADBEEF, DEVICE_MMIO_GET(dev, grault));
      sys_write32(0xF0CCAC1A, DEVICE_MMIO_GET(dev, corge));
      ...
   }

同一 DT 节点中具有多个 MMIO 区域的设备模型驱动程序
==================================================

有些驱动程序在同一 DT 设备节点中定义多个 MMIO 区域，并通过 ``reg-names`` 属性区分，例如：

.. code-block:: devicetree

   /dts-v1/;

   / {
           a-driver@40000000 {
                   reg = <0x40000000 0x1000>,
                         <0x40001000 0x1000>;
                   reg-names = "corge", "grault";
           };
   };

可以采用上一节的方法处理，但改用 ``DEVICE_MMIO_NAMED_ROM_INIT_BY_NAME`` 宏。因此，唯一的区别在于驱动程序配置结构体：

.. code-block:: C

   const static struct my_driver_config my_driver_config_0 = {
      ...
      DEVICE_MMIO_NAMED_ROM_INIT_BY_NAME(corge, DT_DRV_INST(...)),
      DEVICE_MMIO_NAMED_ROM_INIT_BY_NAME(grault, DT_DRV_INST(...)),
      ...
   }

不使用 Zephyr 设备模型的驱动程序
================================

有些驱动程序或类似驱动程序的代码不使用 Zephyr 设备模型，需要为 MMIO 数据安排其他存储方式，例如定时器驱动程序或中断控制器代码。

可以使用 ``DEVICE_MMIO_TOPLEVEL`` 系列宏处理，例如：

.. code-block:: C

   DEVICE_MMIO_TOPLEVEL_STATIC(my_regs, DT_DRV_INST(..));

   void some_init_code(...)
   {
      ...
      DEVICE_MMIO_TOPLEVEL_MAP(my_regs, K_MEM_CACHE_NONE);
      ...
   }

   void some_function(...)
      ...
      sys_write32(DEVICE_MMIO_TOPLEVEL_GET(my_regs), 0xDEADBEEF);
      ...
   }

不使用 DTS 的驱动程序
=====================

有些驱动程序不从 DTS 获取 MMIO 物理地址，例如 PCI-E。此时可以直接使用 :c:func:`device_map` 函数：

.. code-block:: C

   void some_init_code(...)
   {
      ...
      struct pcie_bar mbar;
      bool bar_found = pcie_get_mbar(bdf, index, &mbar);

      device_map(DEVICE_MMIO_RAM_PTR(dev), mbar.phys_addr, mbar.size, K_MEM_CACHE_NONE);
      ...
   }

这些情况下，可以省略 DEVICE_MMIO_ROM 指令。

API 参考
********

.. doxygengroup:: device_model
