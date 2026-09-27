.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _memory_management_shared_multi_heap:

共享多堆
########

共享多堆内存池管理器使用多堆分配器，管理一组具有不同能力或属性（如可缓存、不可缓存等）的保留内存区域。

可以在运行时将这些不同区域加入共享多堆池，并提供一个不透明的“属性”值（整数或枚举值），供驱动程序或应用请求具备特定能力的内存。

此框架的常见用法如下：

1. 启动时，平台代码调用 :c:func:`shared_multi_heap_pool_init()` 初始化共享多堆框架，并通过 :c:func:`shared_multi_heap_add()` 将内存区域加入池中。所需的区域信息也可以从设备树获取。

2. 每个内存区域由一个 :c:struct:`shared_multi_heap_region` 结构体描述。该结构体还包含用户定义的不透明整数值，用于表示区域的能力，例如可缓存性、CPU 亲和性等。

.. code-block:: c

   // Init the shared multi-heap pool
   shared_multi_heap_pool_init()

   // Fill the struct with the data for cacheable memory
   struct shared_multi_heap_region cacheable_r0 = {
        .addr = addr_r0,
        .size = size_r0,
        .attr = SMH_REG_ATTR_CACHEABLE,
   };

   // Add the region to the pool
   shared_multi_heap_add(&cacheable_r0, NULL);

   // Add another cacheable region
   struct shared_multi_heap_region cacheable_r1 = {
        .addr = addr_r1,
        .size = size_r1,
        .attr = SMH_REG_ATTR_CACHEABLE,
   };

   shared_multi_heap_add(&cacheable_r1, NULL);

   // Add a non-cacheable region
   struct shared_multi_heap_region non_cacheable_r2 = {
        .addr = addr_r2,
        .size = size_r2,
        .attr = SMH_REG_ATTR_NON_CACHEABLE,
   };

   shared_multi_heap_add(&non_cacheable_r2, NULL);

3. 驱动程序或应用需要具备特定能力的动态内存时，可以调用 :c:func:`shared_multi_heap_alloc()` 或其对齐版本，通过不透明参数选择所需的内存属性。框架会根据该参数以及各堆的运行时状态（可用内存、堆状态等），选择合适的堆，也就是内存区域，并从中分配内存。

.. code-block:: c

   // Allocate 4K from cacheable memory
   shared_multi_heap_alloc(SMH_REG_ATTR_CACHEABLE, 0x1000);

   // Allocate 4K from non-cacheable memory
   shared_multi_heap_alloc(SMH_REG_ATTR_NON_CACHEABLE, 0x1000);

添加新属性
**********

API 不强制规定属性，但定义了两个最常用的属性：:c:enumerator:`SMH_REG_ATTR_CACHEABLE` 和 :c:enumerator:`SMH_REG_ATTR_NON_CACHEABLE`。

.. doxygengroup:: shared_multi_heap
